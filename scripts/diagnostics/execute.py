"""Run only the newly approved Batch A, with one retained attempt per slot.

The ENV-01 worker is reused directly; its fixture-producing controller is never
called. Each worker runs in its own process group and reads archived real inputs.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback

from .contracts import save
from .prepare import CODE_REVISION, MODEL_REVISION, NATIVE


def validate_authorization(proposal, authorization):
    rows = proposal['requests']
    expected = proposal['batch_A']['unique_request_ids']
    if not authorization.get('gpu_authorized'):
        raise PermissionError('A new, explicit Batch A approval is required')
    if len(rows) != 24 or [r['id'] for r in rows] != expected or len(set(expected)) != 24:
        raise ValueError('Only the exact frozen 24-slot Batch A may execute')
    if authorization['approved_request_ids'] != expected:
        raise ValueError('Approval and frozen request list differ')
    if (authorization['max_technical_retries'] != 0 or authorization['allow_training']
            or authorization['max_new_gpu_calls'] != 24 or authorization['max_gpu_hours'] != 2):
        raise ValueError('Batch A call/time/training limits changed')
    for row in rows:
        if (row['model_revision'] != MODEL_REVISION or row['code_revision'] != CODE_REVISION
                or row['native_parameters'] != NATIVE or row['geometry_permission'] != 'G0'
                or row['legacy_ENV_fixture_allowed']):
            raise ValueError('Frozen checkpoint, inputs or native parameters changed')
    if [r['native_task'] for r in rows] != ['x2t_video'] * 20 + ['t2v'] * 4:
        raise ValueError('Batch A must contain 20 understanding and four generation slots')
    return rows


def archive_inputs(source, destination, task):
    """Only relocate the media pathname; leave all prompt and target text intact."""
    shutil.copytree(source, destination)
    path = destination / (task + '.json')
    value = json.loads(path.read_text())
    if task == 'x2t_video':
        row = value['0001']
        for i, kind in enumerate(row['element_dtype_array']):
            if kind == 'video':
                media = Path(row['interleave_array'][i])
                if media.is_absolute() or media.name != 'visible.mp4':
                    raise ValueError('Unexpected frozen video pathname')
                row['interleave_array'][i] = str(destination / media.name)
        save(path, value)
    return value


def resource_snapshot():
    query = subprocess.run(['nvidia-smi', '--query-gpu=memory.free,memory.used,utilization.gpu',
        '--format=csv,noheader,nounits'], capture_output=True, text=True, check=True)
    values = [float(x.strip()) for x in query.stdout.strip().split(',')]
    processes = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,used_gpu_memory',
        '--format=csv,noheader,nounits'], capture_output=True, text=True, check=True)
    mem = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    return {'gpu_free_MiB': values[0], 'gpu_used_MiB': values[1], 'gpu_util_percent': values[2],
            'compute_processes': processes.stdout.strip(),
            'RAM_available_MiB': int(mem['MemAvailable'].split()[0]) / 1024}


def resources_available(snapshot):
    # Coexistence policy: wait for GPU compute to be idle, never stop other jobs.
    return (not snapshot['compute_processes'] and snapshot['gpu_free_MiB'] >= 44000
            and snapshot['RAM_available_MiB'] >= 35000)


def run_owned(command, logfile, timeout, environment):
    with logfile.open('w') as stream:
        process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT,
            env=environment, start_new_session=True)
        try:
            return process.wait(timeout=timeout), False, process.pid
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            return process.returncode, True, process.pid


def audit_output(row, run):
    import numpy as np
    task = row['native_task']
    attempt = run / task
    actual_name = 'actual_understanding_input.json' if task == 'x2t_video' else 'actual_generation_input.json'
    actual = json.loads((attempt / actual_name).read_text())
    checks = {'seed_matches': actual['torch_initial_seed'] == row['seed']}
    if task == 'x2t_video':
        answer = json.loads((attempt / 'outputs/result.json').read_text())
        sampling = json.loads((attempt / 'actual_sampling.json').read_text())
        context = actual['conditioning_decoded_text']
        checks.update(nonempty_answer=len(answer) == 1 and bool(answer[0].get('answer')),
            prompt_in_actual_context=row['prompt'] in context,
            withheld_placeholder_not_conditioned='Reference answer withheld.' not in context,
            sampling_recorded=bool(sampling) and all(s.get('indices') for s in sampling))
        result = {'checks': checks, 'raw_answer': answer, 'sampling': sampling,
                  'formal_accuracy': None}
    else:
        caption = actual['caption']
        captions = [caption] if isinstance(caption, str) else caption
        checks.update(exact_literal_prompt=len(captions) == 1 and row['prompt'] in captions[0],
            no_ENV_fixture=all('Chinese character 十 ' not in c for c in captions),
            no_image_condition=actual['VIT_input_elements'] == 0,
            frozen_steps=actual['num_timesteps'] == 30,
            frozen_CFG=actual['cfg_text_scale'] == 4.0)
        videos = list((attempt / 'outputs').glob('*.mp4'))
        if len(videos) != 1:
            raise ValueError('Expected one original native MP4')
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_frames',
            '-of', 'json', str(videos[0])], check=True, text=True, capture_output=True)
        (attempt / 'ffprobe.json').write_text(probe.stdout)
        info = json.loads(probe.stdout)
        frames = [f for f in info['frames'] if f['media_type'] == 'video']
        pts = [float(f['best_effort_timestamp_time']) for f in frames]
        import imageio.v2 as imageio
        with imageio.get_reader(str(videos[0]), format='ffmpeg') as reader:
            decoded = np.stack([frame for frame in reader])
        np.savez_compressed(attempt / 'decoded_rgb_uint8.npz', frames=decoded)
        source = np.load(attempt / 'source_rgb_uint8.npz')['frames']
        checks.update(source_and_decoded_shape=list(source.shape) == list(decoded.shape) == [33, 480, 848, 3],
            actual_PTS=len(pts) == 33 and all(abs(t-i/12) < .00002 for i,t in enumerate(pts)))
        result = {'checks': checks, 'actual_caption': captions, 'PTS_seconds': pts,
                  'source_shape': list(source.shape), 'decoded_shape': list(decoded.shape),
                  'scientific_process_judgment': 'pending_actual_RGB_analysis'}
    result['passed'] = all(checks.values())
    save(attempt / 'input_output_integrity.json', result)
    return result


def execute(root, limit=None):
    root = Path(root).resolve()
    auth = json.loads((root / 'authorization.json').read_text())
    rows = validate_authorization(json.loads((root / 'manifest.json').read_text()), auth)
    runtime = json.loads((root / 'runtime.json').read_text())
    source = Path(runtime['source_directory'])
    for required in ['Lance_3B_Video/model.safetensors', 'Qwen2.5-VL-ViT/vit.safetensors', 'Wan2.2_VAE.pth']:
        if not (source / 'downloads' / required).is_file():
            raise FileNotFoundError('Fixed checkpoint cache missing: ' + required)
    provenance = json.loads((root / 'model_provenance.json').read_text())
    if (provenance['model_revision'] != MODEL_REVISION or provenance['code_revision'] != CODE_REVISION
            or not provenance['all_download_metadata_matches']):
        raise ValueError('Fixed checkpoint provenance is not established')
    with (root / 'queue.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        statepath = root / 'state.json'
        state = json.loads(statepath.read_text())
        launched = 0
        for row, entry in zip(rows, state['requests']):
            if entry['status'] != 'pending':
                continue  # Failed/interrupted calls are never retried.
            snapshot = resource_snapshot()
            state['last_resource_snapshot'] = snapshot
            if not resources_available(snapshot):
                state['stop_reason'] = 'Resource conflict; other processes left untouched'
                save(statepath, state)
                return 3
            if state.get('deadline_unix') is None:
                state['deadline_unix'] = time.time() + auth['max_gpu_hours'] * 3600
            remaining = state['deadline_unix'] - time.time()
            if remaining <= 0:
                state['stop_reason'] = 'Two-hour hard stop; pending slots not called'
                save(statepath, state)
                return 4
            bundle = root / 'bundles' / row['id']
            bundle.mkdir(parents=True, exist_ok=True)
            if not (bundle / 'upstream').exists():
                (bundle / 'upstream').symlink_to(source, target_is_directory=True)
            run = bundle / 'runs' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            run.mkdir(parents=True, exist_ok=False)
            archive_inputs(root / 'inputs' / row['id'], run / 'inputs', row['native_task'])
            attempt = run / row['native_task']
            attempt.mkdir()
            plan = {**row['native_parameters'], 'expected_gpu_count': 1,
                    'audit_native_rgb_inputs': True, 'audit_native_sampling': True}
            save(run / 'plan.json', plan)
            command = [sys.executable, '-m', 'scripts.diagnostics.execute', '--root', str(root),
                       '--worker', row['id'], '--run', str(run)]
            environment = os.environ.copy()
            environment.update(CUDA_VISIBLE_DEVICES='0', EXP_HW_20250819='False', POSITION_EMBEDDING_3D_VERSION='v2',
                CUDA_LAUNCH_BLOCKING='0', PYTHONUNBUFFERED='1', TOKENIZERS_PARALLELISM='false',
                HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', WANDB_MODE='disabled',
                OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2')
            for key in ('RANK', 'WORLD_SIZE', 'LOCAL_RANK'):
                environment.pop(key, None)
            save(attempt / 'command.json', {'command': command, 'environment_overrides':
                {k: environment[k] for k in ('CUDA_VISIBLE_DEVICES','HF_HUB_OFFLINE','OMP_NUM_THREADS')},
                'resource_snapshot_before_call': snapshot})
            entry.update(status='running', process_attempts=1, native_run=str(run.relative_to(root)),
                         started_at_utc=datetime.now(timezone.utc).isoformat())
            save(statepath, state)
            started = time.perf_counter()
            with (attempt / 'gpu_samples.csv').open('w') as gpu_log:
                monitor = subprocess.Popen(['nvidia-smi', '-i', '0',
                    '--query-gpu=timestamp,memory.used,memory.total,utilization.gpu',
                    '--format=csv,noheader,nounits', '-l', '1'], stdout=gpu_log, stderr=subprocess.STDOUT)
                try:
                    code, timeout, pid = run_owned(command, attempt / 'process.log', min(900, remaining), environment)
                finally:
                    monitor.terminate()
                    monitor.wait()
            entry.update(status='failed', return_code=code, timed_out=timeout, worker_pid=pid,
                wall_seconds=time.perf_counter()-started, finished_at_utc=datetime.now(timezone.utc).isoformat())
            entry['native_method_entered'] = any((attempt / n).exists() for n in
                ('actual_understanding_input.json','actual_generation_input.json'))
            metrics = attempt / 'worker_metrics.json'
            if metrics.is_file():
                entry['measurements'] = json.loads(metrics.read_text())
            if code == 0:
                try:
                    audit = audit_output(row, run)
                    entry.update(integrity_passed=audit['passed'], status='completed' if audit['passed'] else 'failed')
                except Exception:
                    entry['CPU_audit_error'] = traceback.format_exc()
            save(statepath, state)
            print(json.dumps({k: entry[k] for k in ('id','status','wall_seconds','return_code')}, ensure_ascii=False), flush=True)
            launched += 1
            if entry['status'] != 'completed':
                state['stop_reason'] = 'Inspect retained failed slot; no technical retry permitted'
                save(statepath, state)
                return 2
            if limit is not None and launched >= limit:
                state['stop_reason'] = 'Requested inspection checkpoint; pending slots untouched'
                save(statepath, state)
                return 0
        state['stop_reason'] = 'All 24 slots processed'
        save(statepath, state)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--worker')
    parser.add_argument('--run')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.worker:
        # The controller alone creates archived inputs and marks the single attempt.
        proposal = json.loads((root / 'manifest.json').read_text())
        rows = validate_authorization(proposal, json.loads((root / 'authorization.json').read_text()))
        row = next(r for r in rows if r['id'] == args.worker)
        run = Path(args.run).resolve()
        if not run.is_relative_to(root / 'bundles' / row['id'] / 'runs'):
            raise ValueError('Worker output must remain inside its own request directory')
        from scripts.env01.run_interfaces import worker
        os.nice(10)
        return worker(root / 'bundles' / row['id'], run / row['native_task'], row['native_task'],
                      json.loads((run / 'plan.json').read_text()))
    return execute(root, args.limit)


if __name__ == '__main__':
    raise SystemExit(main())
