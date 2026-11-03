import json
from pathlib import Path
import unittest

from scripts.paired_strokes.data import read_jsonl
from scripts.paired_strokes.gold import qualify
from scripts.paired_strokes.s2 import generated_continuations, native_arguments, score, score_controls


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/research/paired_strokes_v1'
SUITE = DATA / 's2_preflight_v1'


class S2PreparationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests = read_jsonl(SUITE / 'requests.jsonl')
        cls.labels = {r['id']: r for r in read_jsonl(SUITE / 'evaluation_only/labels.jsonl')}
        cls.controls = [r for r in cls.requests if r['metric'] == 'VPC']

    def test_hanzi_payloads_and_labels_are_unchanged_frozen_subsets(self):
        original = {r['id']: r for r in read_jsonl(DATA / 'complete_suite_v1/requests.jsonl')}
        labels = {r['id']: r for r in read_jsonl(DATA / 'complete_suite_v1/evaluation_only/labels.jsonl')}
        for req in self.requests:
            if req['metric'] == 'VPC':
                continue
            self.assertEqual(req, original[req['id']])
            self.assertEqual(self.labels[req['id']], labels[req['id']])
            self.assertEqual(req['split'], 'audit_development')

    def test_spatial_requests_have_itemwise_gold_and_all_six_relations(self):
        geometry = {g['id']: g for g in read_jsonl(DATA / 'evaluation_only/geometry.jsonl')}
        reviews = read_jsonl(DATA / 'evaluation_only/reviews.jsonl')
        for req in self.requests:
            if req['metric'] in ('E3', 'E4', 'E5'):
                self.assertTrue(qualify(geometry[req['sample_id']], reviews, req['metric']))
        relations = {self.labels[r['id']]['relation'] for r in self.requests if r['metric'] == 'E4'}
        self.assertEqual(relations, {'left', 'right', 'above', 'below', 'intersect', 'longer'})

    def test_native_interfaces_receive_real_rgb_and_pair_description(self):
        req = next(r for r in self.requests if r['metric'] == 'E6')
        args = {family: native_arguments(family, req['model_inputs'], DATA)
                for family in ('internvlu', 'ovis_u1', 'qwen3_vl')}
        self.assertIn(req['model_inputs']['description'], args['internvlu']['prompt'])
        self.assertIn(req['model_inputs']['description'], args['ovis_u1']['text_or_conversations'])
        self.assertTrue(args['ovis_u1']['propagate_exception'])
        self.assertEqual(args['ovis_u1']['text_or_conversations'].count('<image>'), 1)
        content = args['qwen3_vl']['conversation'][0]['content']
        images = [args['internvlu']['image'], args['ovis_u1']['images'][0], content[0]['image']]
        for image in images:
            self.assertEqual(image.mode, 'RGB')
            self.assertEqual(image.size, (256, 256))
            self.assertEqual(image.tobytes(), images[0].tobytes())
        self.assertIn(req['model_inputs']['description'], content[1]['text'])

    def test_text_prior_uses_no_visual_placeholder_or_fake_image(self):
        inputs = next(r['model_inputs'] for r in self.requests if r['permission'] == 'text_only')
        self.assertIsNone(native_arguments('internvlu', inputs, DATA)['image'])
        ovis = native_arguments('ovis_u1', inputs, DATA)
        self.assertEqual(ovis['images'], [])
        self.assertNotIn('<image>', ovis['text_or_conversations'])
        qwen = native_arguments('qwen3_vl', inputs, DATA)
        self.assertEqual([r['type'] for r in qwen['conversation'][0]['content']], ['text'])

    def test_output_slicing_matches_each_native_generation_path(self):
        self.assertEqual(generated_continuations('qwen3_vl', [[10, 11, 20]], [2]), [[20]])
        for family in ('internvlu', 'ovis_u1'):
            self.assertEqual(generated_continuations(family, [[20]], [2]), [[20]])

    def test_positive_control_pairs_prevent_a_constant_answer_passing(self):
        for pair in ('color', 'position'):
            rows = [r for r in self.controls if r['pair_id'] == pair]
            self.assertEqual(rows[0]['model_inputs']['prompt'], rows[1]['model_inputs']['prompt'])
            self.assertNotEqual(self.labels[rows[0]['id']]['label'], self.labels[rows[1]['id']]['label'])
        constant = [{'id': r['id'], 'output': {'label': 'red'}} for r in self.controls]
        self.assertFalse(score_controls(self.controls, constant, self.labels)['all_passed'])
        mixed = [{'id': self.controls[0]['id'], 'output': self.labels[self.controls[0]['id']]},
                 {'id': self.controls[1]['id'], 'output': {'answer': 'unknown'}},
                 {'id': self.controls[2]['id'], 'output': 'bad JSON'}]
        result = score_controls(self.controls, mixed, self.labels)
        self.assertEqual(result['statuses'], {'correct': 1, 'unknown': 1, 'format_error': 1, 'no_output': 1})

    def test_control_and_text_permissions_do_not_enter_main_denominators(self):
        result = score(DATA, SUITE, [])
        self.assertEqual(result['requests_including_controls'], 36)
        self.assertEqual(result['metrics']['E1']['requests'], 4)
        self.assertEqual(result['metrics']['E2']['requests'], 4)
        self.assertEqual(result['metrics']['E4']['eligible'], 8)
        self.assertEqual(result['metrics']['E8']['requests'], 0)
        self.assertEqual(result['visual_positive_controls']['requests'], 4)
        self.assertEqual(result['by_group']['permission']['text_only']['E2']['requests'], 4)
        self.assertEqual(result['by_group']['permission']['health_only']['E8']['requests'], 4)

    def test_each_gpu_application_fixes_the_same_queue_and_requires_approval(self):
        paths = list((SUITE / 'gpu_applications').glob('*.json'))
        self.assertEqual(len(paths), 4)
        for path in paths:
            app = json.loads(path.read_text())
            self.assertEqual(app['request_ids'], [r['id'] for r in self.requests])
            self.assertEqual(app['maximum_generation_calls'], 36)
            self.assertEqual(app['extra_retries'], 0)
            self.assertFalse(app['permissions']['GPU'])
            self.assertFalse(app['permissions']['download_weights'])
            self.assertFalse(app['permissions']['training'])
            self.assertEqual(app['actual_generation_calls'], 0)


if __name__ == '__main__':
    unittest.main()
