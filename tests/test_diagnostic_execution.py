"""CPU checks for the actual Batch A launcher; no CUDA imports or calls."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

from scripts.diagnostics.execute import archive_inputs, execute, resources_available, run_owned, validate_authorization


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

    def test_shared_gpu_requires_measured_headroom(self):
        free = {'compute_processes':'', 'gpu_free_MiB':81000, 'RAM_available_MiB':40000}
        self.assertTrue(resources_available(free))
        self.assertTrue(resources_available({**free,'compute_processes':'1234, 30720'}))
        for change in ({'gpu_free_MiB':10000}, {'RAM_available_MiB':20000}):
            self.assertFalse(resources_available({**free, **change}))

    def test_timeout_stops_only_owned_child_process(self):
        import os
        with tempfile.TemporaryDirectory() as folder:
            code, timed_out, pid = run_owned([sys.executable, '-c', 'import time; time.sleep(5)'],
                Path(folder)/'log', .1, os.environ.copy())
            self.assertTrue(timed_out)
            self.assertNotEqual(code, 0)
            self.assertGreater(pid, 0)

    def test_resume_skips_failed_slot_without_retrying_it(self):
        from unittest.mock import patch, Mock
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'upstream'
            for name in ('Lance_3B_Video/model.safetensors','Qwen2.5-VL-ViT/vit.safetensors','Wan2.2_VAE.pth'):
                p=source/'downloads'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'TEST_ONLY_NO_WEIGHTS')
            def save(name,value):(root/name).write_text(json.dumps(value))
            save('authorization.json',self.auth);save('manifest.json',self.proposal)
            save('runtime.json',{'source_directory':str(source)})
            save('model_provenance.json',{'model_revision':self.proposal['batch_A']['model_revision'],
                'code_revision':self.proposal['batch_A']['code_revision'],'all_download_metadata_matches':True})
            save('state.json',{'deadline_unix':None,'requests':[{'id':r['id'],'status':'pending'} for r in self.proposal['requests']]})
            for row in self.proposal['requests'][:2]:
                path=root/'inputs'/row['id'];path.mkdir(parents=True)
                (path/'x2t_video.json').write_text(json.dumps({'0001':{'interleave_array':['visible.mp4', ['system',row['prompt'],'withheld']],
                    'element_dtype_array':['video','text']}}));(path/'visible.mp4').write_bytes(b'TEST_ONLY')
            snapshot={'compute_processes':'','gpu_free_MiB':80000,'RAM_available_MiB':40000}
            with patch('scripts.diagnostics.execute.resource_snapshot',return_value=snapshot), \
                 patch('scripts.diagnostics.execute.subprocess.Popen',return_value=Mock()), \
                 patch('scripts.diagnostics.execute.run_owned',return_value=(1,False,12345)) as run:
                self.assertEqual(execute(root),2)
                self.assertEqual(execute(root),2)
            invoked=[call.args[0][call.args[0].index('--worker')+1] for call in run.call_args_list]
            self.assertEqual(invoked,[r['id'] for r in self.proposal['requests'][:2]])
            state=json.loads((root/'state.json').read_text())
            self.assertEqual(state['status'],'paused_after_retained_failure')
            self.assertEqual([r['status'] for r in state['requests'][:3]],['failed','failed','pending'])
            self.assertEqual((state['process_attempts'],state['native_model_calls'],state['technical_failures'],state['blocked_unrun_slots']),(2,0,2,22))

    def test_partial_batch_keeps_all_slots_and_separates_calls_from_method_entries(self):
        from scripts.diagnostics.summarize_batch import summarize
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'manifest.json').write_text(json.dumps(self.proposal))
            entries=[{'id':r['id'],'status':'pending','process_attempts':0,'native_method_entered':False} for r in self.proposal['requests']]
            entries[0].update(status='failed',process_attempts=1)
            entries[1].update(status='completed',process_attempts=1,native_method_entered=True,wall_seconds=12)
            (root/'state.json').write_text(json.dumps({'requests':entries}))
            result=summarize(root)
            self.assertEqual(result['status'],'partial')
            self.assertEqual((result['requested_slots'],result['process_attempts'],result['native_method_entries']),(24,2,1))
            self.assertEqual((result['integrity_valid_answers'],result['technical_failed_slots'],result['unrun_slots']),(1,1,22))
            self.assertIsNone(result['actual_cost_CNY']);self.assertIsNone(result['formal_primary_metrics'])
