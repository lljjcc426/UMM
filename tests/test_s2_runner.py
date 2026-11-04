"""CPU tests use an explicit protocol fixture, never a model or GPU runtime."""
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts.paired_strokes import s2_runner as runner
from scripts.paired_strokes.data import read_jsonl
from scripts.paired_strokes.s2_native import audit_loading, check_input_contract
from scripts.paired_strokes.s2_watchdog import GIB, limit_reason, stop_owned


REQUESTS = read_jsonl(runner.SUITE / 'requests.jsonl')
LABELS = {r['id']: r for r in read_jsonl(runner.SUITE / 'evaluation_only/labels.jsonl')}
APP = json.loads((runner.SUITE / 'gpu_applications/qwen3-vl-4b-instruct.json').read_text())
CAPS = APP['resource_caps']

# This fixture tests only the process protocol. Its answers are NOT predictions.
FIXTURE = r'''
import json, pathlib, sys, time
out, mode, labels = pathlib.Path(sys.argv[1]), sys.argv[2], json.loads(sys.argv[3])
def emit(kind, **fields):
    with (out/'events.jsonl').open('a') as f:
        f.write(json.dumps(dict(event=kind, **fields))+'\n')
json.loads(sys.stdin.readline())
emit('load_started')
if mode == 'load_failure':
    emit('failure', failure_type='loading_keys', message='CPU fixture missing key')
    sys.exit(1)
emit('ready')
for line in sys.stdin:
    req=json.loads(line)
    if req.get('stop'): break
    if mode == 'preprocess_failure':
        emit('failure', failure_type='preprocessing_exception', message='CPU fixture image failure')
        sys.exit(1)
    emit('generation_started', id=req['id'])
    if mode == 'hang': time.sleep(30)
    answer={'label':labels[req['id']]['label']} if req['metric']=='VPC' else {'answer':'unknown'}
    if mode == 'fourth_wrong' and req['id']==list(labels)[3]: answer={'label':'left'}
    emit('result', id=req['id'], result={'output':json.dumps(answer),'generated_tokens':4})
'''


def approval():
    return {'baseline': runner.BASELINE, 'gpu_authorized': True, 'model': APP['model'],
            'revision': APP['revision'], 'approved_request_ids': APP['request_ids'],
            'maximum_generation_calls': 36, 'extra_retries': 0,
            'allow_training': False, 'allow_download_weights': False,
            'resource_caps': CAPS, 'gpu_uuid': 'GPU-CPU-TEST-FIXTURE',
            'approval_text': 'CPU TEST FIXTURE ONLY; not a real execution approval'}


class S2RunnerTest(unittest.TestCase):
    def test_unauthorized_entry_never_queries_gpu_or_starts_worker(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'nvidia_snapshot') as gpu, patch.object(runner.subprocess, 'Popen') as process:
            auth = Path(tmp) / 'auth.json'
            auth.write_text(json.dumps({'gpu_authorized': False}))
            # git show uses Popen too; admission is read-only and is mocked here.
            with patch.object(runner.subprocess, 'check_output', side_effect=lambda args, **kw:
                              (runner.ROOT / args[2].split(':', 1)[1]).read_bytes()):
                with self.assertRaises(PermissionError):
                    runner.execute('qwen3-vl-4b-instruct', Path(tmp), Path(tmp) / 'run', auth)
            gpu.assert_not_called()
            process.assert_not_called()
            self.assertFalse((Path(tmp) / 'run').exists())

    def test_admission_rejects_changed_queue_and_changed_approval(self):
        with patch.object(runner.subprocess, 'check_output', return_value=b'changed'):
            with self.assertRaisesRegex(ValueError, 'Frozen baseline'):
                runner.admit('qwen3-vl-4b-instruct', approval())
        for field, value in [('extra_retries', 1), ('allow_download_weights', True),
                             ('maximum_generation_calls', 37), ('approved_request_ids', [])]:
            changed = approval()
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(PermissionError):
                runner.admit('qwen3-vl-4b-instruct', changed)

    def fixture_run(self, mode, watchdog=False):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            root = Path(tmp)
            snapshot, output = root / 'snapshot', root / 'run'
            snapshot.mkdir()
            auth = root / 'authorization.json'
            auth.write_text(json.dumps(approval()))
            real_popen = subprocess.Popen
            workers = []
            def start(command, **kwargs):
                if '-m' not in command:
                    return real_popen(command, **kwargs)  # Actual git baseline comparison.
                process = real_popen([sys.executable, '-u', '-c', FIXTURE, str(output), mode,
                                      json.dumps(LABELS)], **kwargs)
                workers.append(process)
                return process
            stack.enter_context(patch.object(runner.sys, 'platform', 'linux'))
            stack.enter_context(patch.object(runner, 'host_capacity', return_value={
                'available_RAM_bytes': 64 * GIB, 'available_CPU_cores': 8}))
            stack.enter_context(patch.object(runner.shutil, 'disk_usage', return_value=SimpleNamespace(free=128 * GIB)))
            stack.enter_context(patch.object(runner, 'nvidia_snapshot', return_value={
                'uuid': 'GPU-CPU-TEST-FIXTURE', 'name': 'A100 80GB CPU FIXTURE',
                'total_MiB': 81920, 'free_MiB': 81920, 'used_MiB': 0,
                'processes': [], 'utilization': 0}))
            stack.enter_context(patch.object(runner, 'process_group', return_value=([], 1024)))
            stack.enter_context(patch.object(runner.subprocess, 'Popen', side_effect=start))
            if watchdog:
                stack.enter_context(patch.object(runner, 'limit_reason', side_effect=lambda caps, sample, elapsed, stage_elapsed, stage:
                                                'request_timeout' if stage == 'request' else None))
            state = runner.execute('qwen3-vl-4b-instruct', snapshot, output, auth)
            evaluation = json.loads((output / 'evaluation.json').read_text())
            predictions = read_jsonl(output / 'predictions.jsonl') if (output / 'predictions.jsonl').exists() else []
            self.assertEqual(len(workers), 1)
            self.assertIsNotNone(workers[0].poll())
            self.assertEqual(state['successes'] + state['failures'] + state['not_run'], 36)
            self.assertEqual(state['extra_retries'], 0)
            return state, evaluation, predictions

    def test_all_four_controls_release_exactly_remaining_32(self):
        state, _, predictions = self.fixture_run('pass')
        self.assertEqual(state['status'], 'completed')
        self.assertTrue(state['visual_controls_passed'])
        self.assertEqual(state['generation_calls_started'], 36)
        self.assertEqual([p['id'] for p in predictions], APP['request_ids'])

    def test_fourth_control_failure_keeps_32_unrun_and_raw_answer(self):
        state, evaluation, predictions = self.fixture_run('fourth_wrong')
        self.assertEqual(state['status'], 'stopped')
        self.assertEqual(state['failure_type'], 'visual_positive_control_incorrect')
        self.assertEqual((state['generation_calls_started'], state['successes'], state['failures'], state['not_run']), (4, 3, 1, 32))
        self.assertIsNone(evaluation['capability_metrics'])
        self.assertEqual(evaluation['visual_positive_controls']['statuses'], {'correct': 3, 'incorrect': 1})
        self.assertEqual(len(predictions), 4)

    def test_load_and_preprocessor_failures_do_not_become_hanzi_errors(self):
        for mode, failure, not_run in [('load_failure', 'loading_keys', 36),
                                      ('preprocess_failure', 'preprocessing_exception', 35)]:
            with self.subTest(mode=mode):
                state, evaluation, _ = self.fixture_run(mode)
                self.assertEqual(state['failure_type'], failure)
                self.assertEqual(state['generation_calls_started'], 0)
                self.assertEqual(state['not_run'], not_run)
                self.assertIsNone(evaluation['capability_metrics'])

    def test_watchdog_terminates_owned_worker_and_keeps_denominator(self):
        state, _, _ = self.fixture_run('hang', watchdog=True)
        self.assertEqual(state['failure_type'], 'request_timeout')
        self.assertEqual(state['not_run'], 35)
        self.assertEqual(state['generation_calls_started'], 1)

    def test_checkpoint_one_pass_detects_same_size_corruption_and_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = b'actual checkpoint fixture'
            path = root / 'weight.safetensors'
            path.write_bytes(data)
            spec = {'id': 'fixture', 'revision': 'fixed', 'files': [
                {'path': path.name, 'bytes': len(data), 'algorithm': 'sha256',
                 'digest': hashlib.sha256(data).hexdigest()}]}
            runner.checkpoint_integrity(root, spec, root / 'report.json')
            self.assertTrue(json.loads((root / 'report.json').read_text())['complete'])
            path.write_bytes(b'X' * len(data))
            with self.assertRaisesRegex(runner.RunFailure, 'differs'):
                runner.checkpoint_integrity(root, spec, root / 'report.json')
            path.unlink()  # Temporary test fixture only.
            with self.assertRaisesRegex(runner.RunFailure, 'Missing'):
                runner.checkpoint_integrity(root, spec, root / 'report.json')

    def test_manifest_covers_all_frozen_weights_and_their_total_bytes(self):
        manifest = json.loads((runner.CONFIG / 's2_checkpoint_files.json').read_text())['models']
        for model in json.loads((runner.CONFIG / 's2_models.json').read_text())['models']:
            files = manifest[model['key']]['files']
            weights = [f for f in files if f['path'].endswith('.safetensors')]
            self.assertEqual(sorted(f['path'] for f in weights), sorted(model['weight_files']))
            self.assertEqual(sum(f['bytes'] for f in weights), model['weight_bytes'])
            self.assertEqual(manifest[model['key']]['revision'], model['revision'])

    def test_loading_keys_stop_before_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            for kind in ('missing_keys', 'unexpected_keys', 'mismatched_keys', 'error_msgs'):
                with self.subTest(kind=kind), self.assertRaises(runner.RunFailure):
                    audit_loading({'vision': {kind: ['unresolved']}}, Path(tmp) / 'loading.json')

    def test_native_tensor_and_expanded_token_limits(self):
        check_input_contract('ovis_u1', 400, 448 * 448, 256, True, CAPS)
        check_input_contract('qwen3_vl', 100, 0, 0, False, CAPS)
        for tokens, pixels, span, image, failure in [
            (4097, 200704, 256, True, 'input_token_cap'),
            (400, 262145, 256, True, 'image_pixel_cap'),
            (400, 0, 0, True, 'image_wiring'),
            (400, 200704, 0, True, 'image_wiring'),
            (100, 200704, 256, False, 'image_wiring')]:
            with self.subTest(failure=failure), self.assertRaises(runner.RunFailure) as caught:
                check_input_contract('ovis_u1', tokens, pixels, span, image, CAPS)
            self.assertEqual(caught.exception.kind, failure)

    def test_all_frozen_watchdog_bounds(self):
        base = {'gpu_bytes': 0, 'rss_bytes': 0, 'disk_bytes': 0, 'foreign_pids': []}
        self.assertIsNone(limit_reason(CAPS, base, 0, 0, 'load'))
        for elapsed, stage_elapsed, stage, update, expected in [
            (3600, 0, 'load', {}, 'wall_timeout'), (0, 600, 'load', {}, 'load_timeout'),
            (0, 120, 'request', {}, 'request_timeout'),
            (0, 0, 'request', {'gpu_bytes': 72 * GIB + 1}, 'gpu_memory_cap'),
            (0, 0, 'request', {'rss_bytes': 48 * GIB + 1}, 'host_memory_cap'),
            (0, 0, 'request', {'disk_bytes': 64 * GIB + 1}, 'disk_cap'),
            (0, 0, 'load', {'foreign_pids': [9999]}, 'resource_conflict')]:
            with self.subTest(expected=expected):
                self.assertEqual(limit_reason(CAPS, {**base, **update}, elapsed, stage_elapsed, stage), expected)

    def test_kill_scope_is_own_session(self):
        owned = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True)
        unrelated = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True)
        try:
            stop_owned(owned)
            self.assertIsNotNone(owned.poll())
            self.assertIsNone(unrelated.poll())
        finally:
            stop_owned(unrelated)


if __name__ == '__main__':
    unittest.main()
