import copy
import json
from pathlib import Path
import unittest

import numpy as np
from PIL import Image

from scripts.paired_strokes.data import (description, parse_norm, read_jsonl,
                                         training_view, validate_manifest)
from scripts.paired_strokes.evaluate import evaluate, grouped_interval, parse_prediction, sequence_metrics
from scripts.paired_strokes.gold import direction, qualify, review_keys, spatial_relations
from scripts.paired_strokes.intake import validate_payload

ROOT = Path(__file__).resolve().parents[1] / 'data/research/paired_strokes_v1'


class PairedStrokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = read_jsonl(ROOT / 'manifest.jsonl')
        cls.requests = read_jsonl(ROOT / 'requests.jsonl')
        cls.labels = {r['id']: r for r in read_jsonl(ROOT / 'evaluation_only/labels.jsonl')}
        cls.geometry = {r['id']: r for r in read_jsonl(ROOT / 'evaluation_only/geometry.jsonl')}

    def score(self, requests, predictions, reviews=()):
        return evaluate(requests, predictions, self.labels, self.geometry, reviews, ROOT)

    def test_norm_parser_reads_wrapped_codes_before_metadata(self):
        content = ('汉字      笔顺      UCS'.ljust(40) + '汉字       笔顺     UCS\n'
                   '武  1 1 2 1 2 1 5\n 0946 06B66\n8画\n   4\n\n' + ' ' * 75 + '63\n')
        records, rejected = parse_norm(content)
        self.assertEqual(records['武']['sequence'], list('11212154'))
        self.assertFalse(rejected)

    def test_norm_parser_quarantines_incomplete_sequence(self):
        content = ('汉字      笔顺      UCS'.ljust(40) + '汉字       笔顺     UCS\n'
                   '武  1 1 2 1 2 1 5\n 0946 06B66\n8画\n\n' + ' ' * 75 + '63\n')
        records, rejected = parse_norm(content)
        self.assertFalse(records)
        self.assertEqual(rejected[0]['reason'], 'incomplete_or_misaligned_sequence')

    def test_official_coarse_sequence_not_fine_type_inference(self):
        row = next(r for r in self.rows if r['character'] == '永')
        self.assertEqual(row['sequence'], list('45534'))
        self.assertEqual(description('永', row['sequence']), '点、折、折、撇、点、永')
        self.assertNotIn('[EOF]', row['training_targets']['description'])

    def test_training_export_excludes_all_geometry_and_labels(self):
        for row in self.rows:
            exported = training_view(row)
            self.assertEqual(set(exported), {'id', 'model_inputs', 'training_targets'})
            self.assertEqual(set(exported['model_inputs']), {'image'})
            self.assertEqual(set(exported['training_targets']), {'description'})
            self.assertNotIn('evaluation_only', json.dumps(exported))
        self.assertEqual(len(read_jsonl(ROOT / 'training_pairs.jsonl')), 192)

    def test_same_character_other_template_cannot_cross_split(self):
        rows = copy.deepcopy(self.rows[:2])
        rows[1]['char_id'] = rows[0]['char_id']
        rows[1]['split'] = 'test_development'
        with self.assertRaisesRegex(ValueError, 'leakage'):
            validate_manifest(rows)

    def test_identical_image_other_group_cannot_cross_split(self):
        rows = copy.deepcopy(self.rows[:2])
        rows[1]['file_hash'] = rows[0]['file_hash']
        rows[1]['split'] = 'test_development'
        with self.assertRaisesRegex(ValueError, 'leakage'):
            validate_manifest(rows)

    def test_extra_supervision_is_rejected_at_export_boundary(self):
        rows = copy.deepcopy(self.rows[:1])
        rows[0]['training_targets']['mask'] = 'answer.png'
        with self.assertRaisesRegex(ValueError, 'additional supervision'):
            validate_manifest(rows)

    def test_historical_exposures_are_only_in_audit_partition(self):
        self.assertFalse(any(r['historically_exposed'] for r in self.rows if r['split'] != 'audit_development'))
        self.assertEqual(len({r['character'] for r in self.rows}), 256)

    def test_no_empty_or_unchanged_order_negatives(self):
        rows = {r['id']: r for r in self.rows}
        for request in self.requests:
            if request['condition'] == 'same_char_wrong_order':
                self.assertNotEqual(request['model_inputs']['description'],
                                    rows[request['sample_id']]['training_targets']['description'])
                self.assertFalse(self.labels[request['id']]['answer'])

    def test_same_sequence_without_character_is_compatible(self):
        controls = [r for r in self.requests if r['condition'] == 'same_sequence_character_hidden_compatible_control']
        self.assertTrue(controls)
        for request in controls:
            self.assertTrue(self.labels[request['id']]['answer'])
            self.assertFalse(any('\u3400' <= c <= '\u9fff' for c in request['model_inputs']['description']
                                 if c not in '横竖撇点折'))

    def test_order_error_is_not_character_success(self):
        result = sequence_metrics(list('1234'), list('1324'))
        self.assertFalse(result['exact'])
        self.assertTrue(result['count_correct'])
        self.assertEqual(result['normalized_edit_distance'], .5)
        self.assertEqual(result['position_correct'], 2)

    def test_format_unknown_and_missing_remain_in_denominator(self):
        requests = [r for r in self.requests if r['metric'] == 'E2'][:4]
        predictions = [{'id': requests[0]['id'], 'output': {'sequence': self.labels[requests[0]['id']]['sequence']}},
                       {'id': requests[1]['id'], 'output': {'answer': 'unknown'}},
                       {'id': requests[2]['id'], 'output': 'invalid json'}]
        metrics = self.score(requests, predictions)['metrics']
        self.assertEqual(metrics['E2']['accuracy'], .25)
        self.assertEqual(metrics['E2']['statuses'], {'correct': 1, 'unknown': 1, 'format_error': 1, 'no_output': 1})
        self.assertEqual(metrics['E1']['accuracy'], .25)

    def test_unreviewed_geometry_never_scores(self):
        requests = [r for r in self.requests if r['metric'] in ('E3', 'E4', 'E5')]
        report = self.score(requests, [])
        self.assertIn('left', report['by_group']['relation'])
        result = report['metrics']
        for metric in ('E3', 'E4', 'E5'):
            self.assertIsNone(result[metric]['accuracy'])
            self.assertEqual(result[metric]['eligible'], 0)
            self.assertEqual(result[metric]['output_statuses']['no_output'], result[metric]['requests'])

    def test_AI_review_cannot_upgrade_geometry(self):
        item = next(iter(self.geometry.values()))
        review = {'sample_id': item['id'], 'facet': 'E3', 'gold_revision': item['gold_revision'],
                  'verdict': 'accepted', 'reviewer_kind': 'AI', 'reviewer_id': 'synthetic_fixture',
                  'independent_of_label_construction': True, 'norm_reference': item['norm_reference'],
                  'stroke_ids': item['stroke_ids'], 'evidence': 'unit-test-only',
                  'item_decisions': {k: 'accepted' for k in review_keys(item, 'E3')}}
        self.assertFalse(qualify(item, [review], 'E3'))
        review['reviewer_kind'] = 'human'
        self.assertTrue(qualify(item, [review], 'E3'))
        dispute = {**review, 'verdict': 'disputed', 'reviewer_id': 'other_fixture'}
        self.assertFalse(qualify(item, [review, dispute], 'E3'))

    def test_identity_point_scoring_requires_independent_review(self):
        request = next(r for r in self.requests if r['metric'] == 'E3')
        item = self.geometry[request['sample_id']]
        with np.load(ROOT / item['mask_archive']) as archive:
            masks = archive['masks']
        stroke = self.labels[request['id']]['stroke'] - 1
        yy, xx = np.nonzero(masks[stroke] & (masks.sum(axis=0) == 1))
        point = [(int(xx[0]) + .5) / 256, (int(yy[0]) + .5) / 256]
        review = {'sample_id': item['id'], 'facet': 'E3', 'gold_revision': item['gold_revision'],
                  'verdict': 'accepted', 'reviewer_kind': 'human', 'reviewer_id': 'unit-test-fictional',
                  'independent_of_label_construction': True, 'norm_reference': item['norm_reference'],
                  'stroke_ids': item['stroke_ids'], 'evidence': 'unit-test fixture, never saved as real review',
                  'item_decisions': {k: 'accepted' for k in review_keys(item, 'E3')}}
        metrics = self.score([request], [{'id': request['id'], 'output': {'point': point}}], [review])['metrics']
        self.assertEqual(metrics['E3']['accuracy'], 1)

    def test_summary_confirmation_never_qualifies_geometry(self):
        reviews = read_jsonl(ROOT / 'evaluation_only/reviews.jsonl')
        summaries = [r for r in reviews if not r['item_decisions']]
        self.assertTrue(summaries)
        for review in summaries:
            item = self.geometry[review['sample_id']]
            self.assertEqual(qualify(item, [review], review['facet']), review['facet'] == 'PAIR')

    def test_geometry_requires_complete_accepted_facet_choices(self):
        item = next(g for g in self.geometry.values() if len(g['stroke_ids']) > 1)
        base = {'sample_id': item['id'], 'gold_revision': item['gold_revision'],
                'verdict': 'accepted', 'reviewer_kind': 'human', 'reviewer_id': 'unit-test-only',
                'independent_of_label_construction': True, 'norm_reference': item['norm_reference'],
                'stroke_ids': item['stroke_ids'], 'evidence': 'unit-test-only'}
        for facet in ('E3', 'E4', 'E5'):
            keys = review_keys(item, facet)
            record = {**base, 'facet': facet, 'item_decisions': {k: 'accepted' for k in keys}}
            self.assertTrue(qualify(item, [record], facet))
            record['item_decisions'].pop(keys[-1])
            self.assertFalse(qualify(item, [record], facet))
            record['item_decisions'][keys[-1]] = 'unknown'
            self.assertFalse(qualify(item, [record], facet))

    def test_summary_outputs_are_excluded_from_formal_denominators(self):
        requests, reviews, predictions = [], [], []
        for metric in ('E3', 'E4', 'E5'):
            req = next(r for r in self.requests if r['metric'] == metric)
            item = self.geometry[req['sample_id']]
            requests.append(req)
            reviews.append({'sample_id': item['id'], 'gold_revision': item['gold_revision'],
                            'facet': metric, 'verdict': 'accepted', 'reviewer_kind': 'human',
                            'reviewer_id': 'unit-test-only', 'independent_of_label_construction': True,
                            'norm_reference': item['norm_reference'], 'stroke_ids': item['stroke_ids'],
                            'evidence': 'unit-test summary only', 'item_decisions': {}})
            output = {'point': [.5, .5]} if metric == 'E3' else {'answer': True} if metric == 'E4' else {'direction': 'right'}
            predictions.append({'id': req['id'], 'output': output})
        result = self.score(requests, predictions, reviews)
        for metric in ('E3', 'E4', 'E5'):
            report = result['metrics'][metric]
            self.assertEqual(report['eligible'], 0)
            self.assertIsNone(report['accuracy'])
            self.assertEqual(report['statuses'], {'unqualified_gold': 1})
            self.assertEqual(report['output_statuses'], {'valid': 1})

    def test_source_masks_match_actual_input_pixels(self):
        for row in self.rows[::32]:
            with np.load(ROOT / self.geometry[row['id']]['mask_archive']) as archive:
                masks = archive['masks']
            pixels = np.asarray(Image.open(ROOT / row['model_inputs']['image']).convert('L')) < 128
            self.assertTrue(np.array_equal(masks.any(axis=0), pixels))

    def test_analytic_spatial_relations_and_uncertain_band(self):
        masks = np.zeros((2, 100, 100), dtype=bool)
        masks[0, 10:12, 10:25] = True
        masks[1, 70:72, 60:80] = True
        relations = {r['relation']: r['answer'] for r in spatial_relations(masks, [[[0, 0], [10, 0]], [[0, 0], [20, 0]]])}
        self.assertTrue(relations['above'])
        self.assertTrue(relations['left'])
        self.assertFalse(relations['intersect'])
        self.assertFalse(relations['longer'])
        masks[1] = masks[0]
        relations = {r['relation']: r['answer'] for r in spatial_relations(masks, [[[0, 0], [10, 0]]] * 2)}
        self.assertIsNone(relations['above'])
        self.assertIsNone(relations['longer'])

    def test_direction_uses_image_y_axis(self):
        self.assertEqual(direction([[0, 0], [0, 1]]), 'down')
        self.assertEqual(direction([[1, 0], [0, 0]]), 'left')

    def test_masked_recovery_is_separate_from_matching(self):
        request = next(r for r in self.requests if r['metric'] == 'E6R')
        prediction = {'id': request['id'], 'output': {'token': self.labels[request['id']]['token']}}
        result = self.score([request], [prediction])['metrics']
        self.assertEqual(result['E6R']['accuracy'], 1)
        self.assertIsNone(result['E6']['accuracy'])

    def test_boolean_numbers_and_nonfinite_points_are_format_errors(self):
        self.assertEqual(parse_prediction({'answer': 1}, 'E4')[0], 'format_error')
        self.assertEqual(parse_prediction({'point': [float('nan'), .5]}, 'E3')[0], 'format_error')
        self.assertEqual(parse_prediction({'sequence': [1, 2]}, 'E2')[0], 'format_error')

    def test_unexpected_and_duplicate_predictions_are_rejected(self):
        request = self.requests[0]
        prediction = {'id': request['id'], 'output': None}
        with self.assertRaises(ValueError):
            self.score([request], [prediction, prediction])
        with self.assertRaises(ValueError):
            self.score([request], [{'id': 'unexpected', 'output': None}])

    def test_bootstrap_resamples_character_groups(self):
        rows = [{'metric': 'E2', 'sample_id': c, 'status': s}
                for c, s in [('a', 'correct'), ('a', 'correct'), ('b', 'incorrect')]]
        result = grouped_interval(rows, 'E2', repeats=50)
        self.assertEqual(result['groups'], 2)
        self.assertEqual(result, grouped_interval(rows, 'E2', repeats=50))
        self.assertIsNone(grouped_interval([], 'E4')['interval'])

    def test_text_oracle_and_health_controls_do_not_enter_main_score(self):
        suite = ROOT / 'complete_suite_v1'
        requests = read_jsonl(suite / 'requests.jsonl')
        labels = {r['id']: r for r in read_jsonl(suite / 'evaluation_only/labels.jsonl')}
        main = next(r for r in requests if r['metric'] == 'E2' and r['permission'] == 'main')
        text = next(r for r in requests if r['permission'] == 'text_only')
        health = next(r for r in requests if r['permission'] == 'health_only')
        oracle = next(r for r in requests if r['permission'] == 'oracle_highlight')
        self.assertNotIn('image', text['model_inputs'])
        self.assertEqual(set(r['pre_id'] for r in requests), {f'PRE-0{i}' for i in range(1, 8)})
        predictions = [{'id': main['id'], 'output': {'sequence': labels[main['id']]['sequence']}},
                       {'id': text['id'], 'output': {'answer': 'unknown'}},
                       {'id': health['id'], 'output': {'character': labels[health['id']]['character']}}]
        result = evaluate([main, text, health, oracle], predictions, labels, self.geometry, [], ROOT,
                          read_jsonl(suite / 'analysis_strata.jsonl'))
        self.assertEqual(result['metrics']['E2']['requests'], 1)
        self.assertEqual(result['metrics']['E2']['accuracy'], 1)
        self.assertEqual(result['by_group']['permission']['text_only']['E2']['accuracy'], 0)
        self.assertEqual(result['by_group']['permission']['health_only']['E8']['accuracy'], 1)
        self.assertEqual(result['metrics']['E8']['requests'], 0)
        self.assertEqual(result['primary_CI95_by_character']['E2']['groups'], 1)

    def test_health_prediction_unknown_and_format_are_distinct(self):
        self.assertEqual(parse_prediction({'character': '木'}, 'E8')[0], 'valid')
        self.assertEqual(parse_prediction({'character': '木未'}, 'E8')[0], 'format_error')
        self.assertEqual(parse_prediction({'answer': 'unknown'}, 'E8')[0], 'unknown')

    def partial_pair_export(self):
        row = next(r for r in self.rows if r['split'] != 'audit_development')
        item, sid = self.geometry[row['id']], row['id']
        raw = {'reviewer_id': 'UNIT_TEST_ONLY', 'independent': True, f'{sid}:sequence': 'accepted'}
        record = {'sample_id': sid, 'facet': 'PAIR', 'reviewer_id': 'UNIT_TEST_ONLY', 'reviewer_kind': 'human',
                  'independent_of_label_construction': True, 'annotated_at': 'test-time',
                  'verdict': 'accepted', 'not_applicable': False, 'gold_revision': item['gold_revision'],
                  'norm_reference': item['norm_reference'], 'stroke_ids': item['stroke_ids'],
                  'item_decisions': {f'{sid}:sequence': 'accepted'}, 'reviewer_notes': '', 'evidence': 'unit test only'}
        return row, {'reviewer_id': 'UNIT_TEST_ONLY', 'independent_of_label_construction': True,
                     'exported_at': 'test-time', 'raw_answers': raw, 'records': [record],
                     'pending': [{'sample_id': sid, 'facet': facet} for facet in ('E3', 'E4', 'E5')]}

    def test_pair_only_review_does_not_qualify_spatial_gold(self):
        row, payload = self.partial_pair_export()
        result = validate_payload(payload, [row], self.geometry, include_pair=True)
        self.assertEqual(result['facet_records'], 1)
        self.assertEqual(result['pending'], 3)
        self.assertTrue(qualify(self.geometry[row['id']], payload['records'], 'PAIR'))
        self.assertFalse(qualify(self.geometry[row['id']], payload['records'], 'E3'))

    def test_review_summary_cannot_override_raw_disagreement(self):
        row, payload = self.partial_pair_export()
        payload['raw_answers'][f'{row["id"]}:sequence'] = 'disputed'
        with self.assertRaisesRegex(ValueError, 'summary differ'):
            validate_payload(payload, [row], self.geometry, include_pair=True)


if __name__ == '__main__':
    unittest.main()
