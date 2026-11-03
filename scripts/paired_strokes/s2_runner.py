"""S2 controller. No framework imports, model downloads or implicit authorization.

The worker sees public requests only. Labels and the positive-control gate stay
here. A fresh output directory represents exactly one load and zero retries.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

from .data import read_jsonl, write_json, write_jsonl
from .s2 import score, score_controls
from .s2_watchdog import (GIB, deadline_reason, directory_bytes, host_capacity, limit_reason, nvidia_snapshot,
                          process_group, stop_owned)

ROOT = Path(__file__).resolve().parents[2]
BASELINE = '7c843c37a7d360b9482dd6104e3795966134450d'
DATA = ROOT / 'data/research/paired_strokes_v1'
SUITE = DATA / 's2_preflight_v1'
CONFIG = ROOT / 'configs/research/paired_strokes_v1'


class RunFailure(RuntimeError):
    def __init__(self, kind, message):
        super().__init__(message)
        self.kind = kind


def checkpoint_integrity(snapshot, specification, output):
    """One streaming pass over the fixed revision, including tokenizer and code."""
    report = {'model': specification['id'], 'revision': specification['revision'],
              'files': [], 'complete': False}
    try:
        for entry in specification['files']:
            path = snapshot / entry['path']
            if not path.is_file() or path.stat().st_size != entry['bytes']:
                raise RunFailure('checkpoint_integrity', f'Missing/truncated file: {entry["path"]}')
            h = hashlib.sha256() if entry['algorithm'] == 'sha256' else hashlib.sha1()
            if entry['algorithm'] == 'git_blob_sha1':
                h.update(f'blob {entry["bytes"]}\0'.encode())
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                    h.update(block)
            actual = h.hexdigest()
            report['files'].append({'path': entry['path'], 'bytes': entry['bytes'],
                                    'digest': actual, 'matches': actual == entry['digest']})
            if actual != entry['digest']:
                raise RunFailure('checkpoint_integrity', f'File differs from official revision: {entry["path"]}')
        report['complete'] = True
    finally:
        write_json(output, report)


def admit(key, authorization):
    """Validate frozen inputs and one explicit per-model resource approval once."""
    app_path = SUITE / 'gpu_applications' / f'{key}.json'
    paths = [app_path, SUITE / 'requests.jsonl', SUITE / 'evaluation_only/labels.jsonl',
             CONFIG / 's2_models.json']
    for path in paths:
        original = subprocess.check_output(['git', 'show', f'{BASELINE}:{path.relative_to(ROOT)}'], cwd=ROOT)
        if path.read_bytes() != original:
            raise ValueError(f'Frozen baseline file changed: {path.relative_to(ROOT)}')
    app = json.loads(app_path.read_text())
    model = next(m for m in json.loads((CONFIG / 's2_models.json').read_text())['models'] if m['key'] == key)
    expected = {'baseline': BASELINE, 'gpu_authorized': True, 'model': app['model'],
                'revision': app['revision'], 'approved_request_ids': app['request_ids'],
                'maximum_generation_calls': 36, 'extra_retries': 0,
                'allow_training': False, 'allow_download_weights': False,
                'resource_caps': app['resource_caps']}
    if any(authorization.get(k) != v for k, v in expected.items()):
        raise PermissionError('Matching explicit per-model GPU authorization is required; no run started')
    if not authorization.get('approval_text') or not authorization.get('gpu_uuid', '').startswith('GPU-'):
        raise PermissionError('Approval text and the approved GPU UUID are required')
    return app, model


def initial_state(requests, model):
    return {'baseline': BASELINE, 'model': model['id'], 'revision': model['revision'],
            'status': 'preflight', 'fixed_denominator': len(requests),
            'load_attempts': 0, 'generation_calls_started': 0, 'extra_retries': 0,
            'visual_controls_passed': False, 'capability_metrics': None,
            'scope': 'four-character development technical preexperiment; no generalization claim',
            'slots': [{'id': r['id'], 'status': 'not_run_after_stop', 'generation_started': False}
                      for r in requests]}


def accept_result(state, request, result, labels):
    slot = next(s for s in state['slots'] if s['id'] == request['id'])
    slot.update(status='success', **result)
    if request['metric'] == 'VPC':
        control = score_controls([request], [{'id': request['id'], 'output': result['output']}], labels)
        slot['control_status'] = control['details'][0]['status']
        if not control['all_passed']:
            slot.update(status='failure', failure_type='visual_positive_control_' + slot['control_status'])
            raise RunFailure(slot['failure_type'], 'Visual interface/model capability unresolved; stop this model')


def execute(key, snapshot, output, authorization_path, source_root=None):
    authorization = json.loads(authorization_path.read_text())
    app, model = admit(key, authorization)  # Must precede nvidia-smi and worker creation.
    output.mkdir(parents=True, exist_ok=False)
    requests = read_jsonl(SUITE / 'requests.jsonl')
    labels = {r['id']: r for r in read_jsonl(SUITE / 'evaluation_only/labels.jsonl')}
    state = initial_state(requests, model)
    write_json(output / 'state.json', state)
    started, process, active = time.monotonic(), None, None
    predictions = []
    try:
        write_json(output / 'authorization.json', authorization)
        write_json(output / 'application.json', app)
        write_json(output / 'model.json', model)
        write_jsonl(output / 'requests.jsonl', requests)
        write_json(output / 'controller_environment.json', {
            'python': sys.version, 'platform': sys.platform,
            'runner_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()})
        if sys.platform != 'linux':
            raise RunFailure('resource_preflight', 'Approved runner requires Linux /proc and NVIDIA; no MPS fallback')
        device = nvidia_snapshot(authorization['gpu_uuid'])
        write_json(output / 'gpu_before_load.json', device)
        caps = app['resource_caps']
        if ('A100' not in device['name'] or device['total_MiB'] < 79000
                or device['free_MiB'] < caps['process_gpu_memory_GiB'] * 1024
                or device['processes'] or device['used_MiB'] > 512 or device['utilization']):
            raise RunFailure('resource_conflict', 'One idle A100 80GB is required; unrelated processes are left alone')
        host = host_capacity()
        write_json(output / 'host_before_load.json', host)
        if host['available_RAM_bytes'] < caps['host_memory_GiB'] * GIB or host['available_CPU_cores'] < caps['cpu_cores']:
            raise RunFailure('resource_preflight', 'Insufficient available host RAM or CPU cores')
        checkpoint_bytes = directory_bytes(snapshot)
        if checkpoint_bytes >= caps['local_disk_GiB'] * GIB or shutil.disk_usage(output).free < caps['local_disk_GiB'] * GIB - checkpoint_bytes:
            raise RunFailure('disk_cap', 'Checkpoint and run artifacts must fit within the 64 GiB allocation')
        if model['family'] == 'internvlu':
            if source_root is None:
                raise RunFailure('source_revision', 'Pinned InternVL-U source checkout is required')
            revision = subprocess.check_output(['git', '-C', str(source_root), 'rev-parse', 'HEAD'], text=True).strip()
            dirty = subprocess.check_output(['git', '-C', str(source_root), 'status', '--porcelain', '--untracked-files=no'], text=True)
            if revision != model['source_revision'] or dirty:
                raise RunFailure('source_revision', 'InternVL-U source revision is not the frozen clean checkout')
        public = output / 'inputs'
        public.mkdir()
        for req in requests:
            if 'image' in req['model_inputs']:
                source = DATA / req['model_inputs']['image']
                target = public / req['model_inputs']['image']
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        environment = os.environ.copy()
        environment.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_DATASETS_OFFLINE='1',
                           CUDA_VISIBLE_DEVICES=authorization['gpu_uuid'], TOKENIZERS_PARALLELISM='false',
                           OMP_NUM_THREADS='8', MKL_NUM_THREADS='8', OPENBLAS_NUM_THREADS='8',
                           HF_HOME=str(output / 'hf_cache'), HF_MODULES_CACHE=str(output / 'hf_modules'))
        # Private worker protocol; public execution enters through this controller.
        command = [sys.executable, '-m', 'scripts.paired_strokes.s2_native', '--worker',
                   str(snapshot), str(output), key]
        if source_root:
            environment['PYTHONPATH'] = os.pathsep.join([str(source_root), str(ROOT)])
        with (output / 'stdout.log').open('w') as stdout, (output / 'stderr.log').open('w') as stderr:
            process = subprocess.Popen(command, cwd=ROOT, env=environment, stdin=subprocess.PIPE,
                                       stdout=stdout, stderr=stderr, text=True, start_new_session=True)
            # Pass the validated contract over stdin; keep all labels in the controller.
            process.stdin.write(json.dumps({'application': app, 'model': model}) + '\n')
            process.stdin.flush()
            state.update(status='loading', worker_attempts=1)
            event_path = output / 'events.jsonl'
            stage, stage_started, offset, buffer = 'load', time.monotonic(), 0, ''
            next_sample = 0
            while True:
                now = time.monotonic()
                deadline = deadline_reason(caps, now - started, now - stage_started, stage)
                if deadline:
                    raise RunFailure(deadline, 'External watchdog deadline reached')
                if event_path.exists():
                    with event_path.open() as stream:
                        stream.seek(offset)
                        buffer += stream.read()
                        offset = stream.tell()
                    lines = buffer.split('\n')
                    buffer = lines.pop()
                    for line in lines:
                        event = json.loads(line)
                        kind = event['event']
                        if kind == 'load_started':
                            state['load_attempts'] += 1
                        if kind == 'failure':
                            raise RunFailure(event['failure_type'], event['message'])
                        if kind == 'generation_started':
                            state['slots'][active]['generation_started'] = True
                            state['generation_calls_started'] += 1
                        if kind == 'result':
                            if event['id'] != requests[active]['id']:
                                raise RunFailure('worker_protocol', 'Unexpected request ID')
                            predictions.append({'id': event['id'], 'output': event['result']['output']})
                            write_jsonl(output / 'predictions.jsonl', predictions)
                            if event['result'].get('torch_peak_reserved_bytes', 0) > caps['process_gpu_memory_GiB'] * GIB:
                                raise RunFailure('gpu_memory_cap', 'Retained allocator peak exceeds process GPU cap')
                            accept_result(state, requests[active], event['result'], labels)
                            if active == 3:
                                state['visual_controls_passed'] = True
                            if active == len(requests) - 1:
                                state['status'] = 'completed'
                                process.stdin.write('{"stop":true}\n')
                                process.stdin.flush()
                                process.wait(timeout=5)
                                if process.returncode:
                                    raise RunFailure('worker_exit', 'Worker exited with an error after the last result')
                                break
                        if kind == 'ready' or kind == 'result':
                            active = 0 if active is None else active + 1
                            stage, stage_started = 'request', time.monotonic()
                            state.update(status='running', active_request_id=requests[active]['id'])
                            state['slots'][active]['status'] = 'running'
                            process.stdin.write(json.dumps(requests[active], ensure_ascii=False) + '\n')
                            process.stdin.flush()
                    write_json(output / 'state.json', state)
                if state['status'] == 'completed':
                    break
                if process.poll() is not None:
                    raise RunFailure('worker_exit', f'Worker exited {process.returncode}; see stderr.log')
                if now >= next_sample:
                    next_sample = now + 1
                    gpu = nvidia_snapshot(authorization['gpu_uuid'])
                    pids, rss = process_group(process.pid)
                    sample = {'seconds': now - started, 'gpu_bytes': sum(p['MiB'] for p in gpu['processes'] if p['pid'] in pids) * 1024 ** 2,
                              'rss_bytes': rss, 'disk_bytes': checkpoint_bytes + directory_bytes(output),
                              'foreign_pids': [p['pid'] for p in gpu['processes'] if p['pid'] not in pids]}
                    with (output / 'resources.jsonl').open('a') as stream:
                        stream.write(json.dumps(sample) + '\n')
                    reason = limit_reason(caps, sample, now - started, now - stage_started, stage)
                    if reason:
                        raise RunFailure(reason, 'External watchdog stopped this model')
                time.sleep(0.1)
    except Exception as error:
        kind = error.kind if isinstance(error, RunFailure) else 'controller_error'
        state.update(status='stopped', failure_type=kind, error=str(error), capability_metrics=None)
        if active is not None and state['slots'][active]['status'] in ('running', 'success'):
            state['slots'][active].update(status='failure', failure_type=kind)
        (output / 'controller_error.log').write_text(traceback.format_exc())
    finally:
        if process is not None:
            stop_owned(process)
            process.stdin.close()
        state['wall_seconds'] = time.monotonic() - started
        state['successes'] = sum(s['status'] == 'success' for s in state['slots'])
        state['failures'] = sum(s['status'] == 'failure' for s in state['slots'])
        state['not_run'] = sum(s['status'] == 'not_run_after_stop' for s in state['slots'])
        write_json(output / 'state.json', state)
        # Never score Hanzi ability when the positive-control/interface gate failed.
        evaluation = score(DATA, SUITE, predictions) if state['visual_controls_passed'] and state['status'] == 'completed' else {
            'capability_metrics': None, 'reason': 'technical run incomplete; interface/model capability unresolved',
            'visual_positive_controls': score_controls(requests[:4], predictions, labels)}
        evaluation['execution'] = {k: state[k] for k in ('status', 'fixed_denominator', 'generation_calls_started',
                                                        'successes', 'failures', 'not_run')}
        write_json(output / 'evaluation.json', evaluation)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True, choices=[p.stem for p in (SUITE / 'gpu_applications').glob('*.json')])
    parser.add_argument('--checkpoint', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--authorization', required=True, type=Path)
    parser.add_argument('--source-root', type=Path)
    args = parser.parse_args()
    state = execute(args.model, args.checkpoint.resolve(), args.output.resolve(), args.authorization,
                    args.source_root.resolve() if args.source_root else None)
    print(json.dumps(state, ensure_ascii=False))
    raise SystemExit(0 if state['status'] == 'completed' else 1)


if __name__ == '__main__':
    main()
