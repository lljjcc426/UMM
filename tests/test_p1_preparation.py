"""Check exposure, information permissions and proposed denominators without a GPU."""
import json
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.env01 import fixtures, run_interfaces
from scripts.p1.prepare_baseline import build_requests, prompt_for


class P1PreparationTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads(Path('configs/research/p1_baseline_plan.json').read_text())
        self.audits=json.loads(Path('data/research/runs/p0_decoupled_d1_d4_2026-10-29/static_qualification_audit.json').read_text())
        self.rows=build_requests(self.plan,self.audits)

    def test_pilot_is_counted_once_within_full_queue(self):
        self.assertEqual(len(self.rows),64)
        self.assertEqual(len({r['id'] for r in self.rows}),64)
        self.assertEqual(sum(r['pilot'] for r in self.rows),16)
        self.assertEqual(sum(r['task']=='i2v' for r in self.rows),8)

    def test_no_geometry_or_gold_upgrades_in_G0(self):
        for row in self.rows:
            self.assertFalse(row['formal_geometry_gold'])
            if row['geometry_permission']=='G0':
                self.assertNotIn('bbox',prompt_for(row,self.audits[row['norm_id']]))
        self.assertFalse(self.plan['constraints']['GPU_authorized'])
        self.assertFalse(self.plan['constraints']['automatic_primary_judge'])

    def test_blank_image_condition_is_T_and_not_real_prefix_P(self):
        rows=[r for r in self.rows if r['task']=='i2v']
        self.assertTrue(all(r['condition']=='T_G0_blank_i2v' and r['geometry_permission']=='G0' for r in rows))

    def start_without_gpu(self, task, sample, prepared_request=True):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        bundle = Path(temp.name).resolve()
        (bundle / 'inputs').mkdir()
        (bundle / 'inputs' / f'{task}.json').write_text(json.dumps(sample, ensure_ascii=False))
        (bundle / 'inputs/blank.png').write_bytes(b'original blank-image fixture')
        plan = dict(self.plan['native'], tasks=[task], seed=11, scope='CPU test fixture',
                    experiment_id='BASE-01', approval={'user_approved':True})
        if prepared_request:
            plan['request'] = {'id':'CPU-test-fixture', 'character':'士'}
        (bundle / 'plan.json').write_text(json.dumps(plan))
        with patch.object(sys, 'argv', ['run_interfaces', '--bundle', str(bundle)]), \
             patch.object(fixtures, 'prepare_inputs') as fixture_builder, \
             patch.object(run_interfaces.subprocess, 'Popen', side_effect=RuntimeError('CPU test stops before GPU access')), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(run_interfaces.main(), 1)
        run = next((bundle / 'runs').iterdir())
        return bundle, run, fixture_builder

    def test_real_execution_start_preserves_prepared_character_prompt(self):
        sample = {'0001':'Write 士 with the prepared normative order, starting from blank.'}
        bundle, run, builder = self.start_without_gpu('t2v', sample)
        builder.assert_not_called()
        self.assertEqual(json.loads((run / 'inputs/t2v.json').read_text()), sample)
        self.assertEqual(json.loads((bundle / 'inputs/t2v.json').read_text()), sample)
        self.assertIn('P1 generation attempt', json.loads((run / 'summary.json').read_text())['scientific_claim'])

    def test_blank_i2v_asset_relocates_without_substituting_env01_prefix(self):
        sample = {'0001':dict(interleave_array=['Write 士 from blank.', '/old-host/inputs/blank.png'],
                            element_dtype_array=['text','image'], istarget_in_interleave=[0,0])}
        bundle, run, builder = self.start_without_gpu('i2v', sample)
        builder.assert_not_called()
        archived = json.loads((run / 'inputs/i2v.json').read_text())['0001']
        self.assertEqual(archived['interleave_array'][0], sample['0001']['interleave_array'][0])
        self.assertEqual(Path(archived['interleave_array'][1]), run / 'inputs/blank.png')
        self.assertEqual((run / 'inputs/blank.png').read_bytes(), (bundle / 'inputs/blank.png').read_bytes())
        self.assertEqual(json.loads((bundle / 'inputs/i2v.json').read_text()), sample)

    def test_env01_still_builds_its_original_interface_fixtures(self):
        bundle, _, builder = self.start_without_gpu('t2v', {'0001':'ENV fixture'}, prepared_request=False)
        self.assertEqual(builder.call_args.args[0], bundle)
        self.assertTrue(builder.call_args.kwargs['encode_video'])
