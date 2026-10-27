"""Contract tests only; these tests never load datasets or learned models."""
import copy
import json
import unittest
from pathlib import Path
from scripts.validate_research_v2 import validate_v2

ROOT = Path(__file__).resolve().parents[1]


class V2Contracts(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / 'configs/research/stroke_video_v2.json').read_text(encoding='utf-8'))
        self.registry = json.loads((ROOT / 'data/research/experiments_v2.json').read_text(encoding='utf-8'))

    def check_bad(self, phrase):
        result = validate_v2(self.config, self.registry)
        self.assertFalse(result['passed'])
        self.assertTrue(any(phrase in e for e in result['errors']), result['errors'])

    def test_repository_design_and_paths(self):
        result = validate_v2(self.config, self.registry, ROOT)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['experiments'], 17)
        self.assertFalse(result['model_results_verified'])

    def test_no_oracle_boundaries(self):
        self.config['inference_uses_gold_event_boundaries'] = True
        self.check_bad('gold event')

    def test_no_self_log_truth(self):
        self.config['generator_logs_are_evaluation_truth'] = True
        self.check_bad('generator logs')

    def test_primary_is_generation(self):
        self.config['primary_protocol'] = 'P'
        self.check_bad('complete T')

    def test_sft_baseline_cannot_disappear(self):
        self.config['required_baselines'].remove('same_data_sft')
        self.check_bad('baseline')

    def test_no_optional_dependency_on_core(self):
        row = next(r for r in self.registry['experiments'] if r['id'] == 'SO-04')
        row['depends_on'].append('REC-01')
        self.check_bad('optional work')

    def test_no_indirect_optional_dependency(self):
        row = next(r for r in self.registry['experiments'] if r['id'] == 'SO-03C')
        row['depends_on'].append('REC-01')
        self.check_bad('optional work')

    def test_cpu_calibration_is_independent(self):
        row = next(r for r in self.registry['experiments'] if r['id'] == 'EVAL-01')
        row['depends_on'].append('ENV-01')
        self.check_bad('CPU')

    def test_missing_adaptation_experiment(self):
        self.registry['experiments'] = [r for r in self.registry['experiments'] if r['id'] != 'ADAPT-01']
        self.check_bad('required v2')

    def test_no_unsupported_sharing_claim(self):
        self.config['status'] = 'design_only'
        self.config['sharing_benefit_established'] = True
        self.check_bad('sharing benefit')

    def test_schema_rejects_fabricated_completion(self):
        self.registry['experiments'][0]['status'] = 'completed'
        self.registry['experiments'][0]['run_records'] = []
        self.registry['experiments'][0]['result_artifacts'] = []
        self.check_bad('completed requires')

    def test_invalid_top_level(self):
        result = validate_v2([], copy.deepcopy(self.registry))
        self.assertFalse(result['passed'])


if __name__ == '__main__':
    unittest.main()
