"""Check exposure, information permissions and proposed denominators without a GPU."""
import json
from pathlib import Path
import unittest

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
