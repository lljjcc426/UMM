"""CPU checks for the actual Batch A launcher; no CUDA imports or calls."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

from scripts.diagnostics.execute import archive_inputs, resources_available, run_owned, validate_authorization


class BatchAExecutionTests(unittest.TestCase):
    def setUp(self):
        self.proposal = json.loads(Path('data/research/next/gpu_pilot_manifest.json').read_text())
        self.auth = {'gpu_authorized': True,
            'approved_request_ids': self.proposal['batch_A']['unique_request_ids'],
            'max_technical_retries': 0, 'allow_training': False,
            'max_new_gpu_calls': 24, 'max_gpu_hours': 2}

    def test_exact_approved_scope_and_native_recipe(self):
        rows = validate_authorization(self.proposal, self.auth)
        self.assertEqual(len(rows), 24)
        for change in ({'seed': 29}, {'model_revision': 'other'}):
            proposal = copy.deepcopy(self.proposal)
            if 'seed' in change:
                proposal['requests'][0]['native_parameters']['seed'] = change['seed']
            else:
                proposal['requests'][0].update(change)
            with self.assertRaises(ValueError):
                validate_authorization(proposal, self.auth)

    def test_no_old_approval_expansion_or_training(self):
        for change in ({'gpu_authorized': False}, {'max_technical_retries': 1},
                       {'allow_training': True}, {'approved_request_ids': ['old-P1-id']}):
            with self.assertRaises((ValueError, PermissionError)):
                validate_authorization(self.proposal, {**self.auth, **change})

    def test_archiving_preserves_questions_and_only_relocates_video(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            src = root / 'source'; src.mkdir()
            value = {'0001': {'interleave_array': ['visible.mp4', ['System', 'Question?', 'Withheld']],
                'element_dtype_array': ['video','text'], 'istarget_in_interleave': [0,1]}}
            (src / 'x2t_video.json').write_text(json.dumps(value))
            (src / 'visible.mp4').write_bytes(b'TEST_ONLY_NOT_A_VIDEO')
            got = archive_inputs(src, root / 'archive', 'x2t_video')
            self.assertEqual(got['0001']['interleave_array'][1], value['0001']['interleave_array'][1])
            self.assertEqual(got['0001']['interleave_array'][0], str(root/'archive/visible.mp4'))
            self.assertEqual(json.loads((src/'x2t_video.json').read_text()), value)
            with self.assertRaises(FileExistsError):
                archive_inputs(src, root / 'archive', 'x2t_video')

    def test_t2v_literal_prompt_not_replaced_by_fixture(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); src = root/'source'; src.mkdir()
            value = {'0001': 'Grow a horizontal black line from right to left on white.'}
            (src/'t2v.json').write_text(json.dumps(value))
            self.assertEqual(archive_inputs(src, root/'archive', 't2v'), value)

    def test_other_gpu_work_or_low_available_memory_pauses_queue(self):
        free = {'compute_processes':'', 'gpu_free_MiB':81000, 'RAM_available_MiB':40000}
        self.assertTrue(resources_available(free))
        for change in ({'compute_processes':'1234, 1024'}, {'gpu_free_MiB':10000}, {'RAM_available_MiB':20000}):
            self.assertFalse(resources_available({**free, **change}))

    def test_timeout_stops_only_owned_child_process(self):
        import os
        with tempfile.TemporaryDirectory() as folder:
            code, timed_out, pid = run_owned([sys.executable, '-c', 'import time; time.sleep(5)'],
                Path(folder)/'log', .1, os.environ.copy())
            self.assertTrue(timed_out)
            self.assertNotEqual(code, 0)
            self.assertGreater(pid, 0)
