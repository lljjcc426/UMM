"""Check evidence controls and scoring, without treating them as model results."""
import json
from pathlib import Path
import tempfile
import unittest
from collections import defaultdict
from PIL import Image

from scripts.h1_state_gate import DEFAULT, evaluate, parse, read_jsonl, render, write_jsonl
from scripts.h1_compare_state_runs import compare
from scripts.h1_target_controls import target_box, controlled_image


class StateGateTest(unittest.TestCase):
    def test_training_text_does_not_leak_into_development(self):
        rows = read_jsonl(DEFAULT.parent / 'state_training_v1/inputs.jsonl')
        train = {r['prompt'] for r in rows if r['split'] == 'train'}
        dev = {r['prompt'] for r in rows if r['split'] == 'dev'}
        self.assertFalse(train & dev)
        vertical = {r['group_id'] for r in rows if r['split'] == 'dev' and r['layout'] == 'single_v'}
        self.assertEqual(len(vertical), 1)
        held_out = {r['prompt'] for r in read_jsonl(DEFAULT.parent / 'state_text_test_v1/inputs.jsonl')}
        self.assertFalse((train | dev) & held_out)

    def test_duplicate_correct_cases_cannot_inflate_paired_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows, labels, predictions = [], [], []
            for case, prompt, expected in [('a','visible','有'), ('b','visible','有'), ('c','empty','无')]:
                for wording in range(2):
                    sid = f'{case}-{wording}'
                    rows.append(dict(sample_id=sid, case_id=case, group_id=prompt, split='dev',
                                     view='oracle_text', task='presence', response_format='json',
                                     wording=wording, images=[], prompt=f'{prompt} q{wording}'))
                    labels.append(dict(sample_id=sid, expected=expected, allowed=['有','无']))
                    predictions.append(dict(sample_id=sid, raw_response='{"answer":"有"}'))
            for name, values in [('inputs',rows), ('labels',labels), ('predictions',predictions)]:
                write_jsonl(root / f'{name}.jsonl', values)
            compare(root,root,root,root/'comparison.json')
            report = json.loads((root/'comparison.json').read_text())
            paired = report['metrics']['presence']['unique_cases_both_wordings']
            self.assertEqual(report['unique_inputs'], 4)
            self.assertEqual((paired['after_correct'], paired['n']), (1, 2))

    def test_identical_current_requires_reference_to_decide_completion(self):
        cases = {r['case_id']: r for r in json.loads((DEFAULT / 'cases.json').read_text())}
        short, short_current = render(cases['dev-reference-00-short'])
        long, long_current = render(cases['dev-reference-00-long'])
        self.assertEqual(short_current.tobytes(), long_current.tobytes())
        self.assertNotEqual(short.tobytes(), long.tobytes())
        labels = {r['sample_id']: r for r in read_jsonl(DEFAULT / 'labels.jsonl')}
        prefix = 'dev-reference-00-'
        for variant, expected in [('short', '完整'), ('long', '部分')]:
            self.assertEqual(labels[prefix + variant + '-reference_current-completion-q0-plain']['expected'], expected)
            self.assertEqual(labels[prefix + variant + '-current_only-completion-q0-plain']['expected'], '未知')

    def test_same_pixels_with_different_names_are_one_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows, labels, predictions = [], [], []
            for case, color, expected in [('a','white','无'), ('b','white','无'), ('c','black','有')]:
                Image.new('RGB', (8,8), color).save(root / f'{case}.png')
                for wording in range(2):
                    sid = f'{case}-{wording}'
                    rows.append(dict(sample_id=sid, case_id=case, group_id=color, split='dev',
                                     view='current_only', task='presence', response_format='json',
                                     wording=wording, images=[f'{case}.png'], prompt=f'question {wording}'))
                    labels.append(dict(sample_id=sid, expected=expected, allowed=['有','无']))
                    predictions.append(dict(sample_id=sid, raw_response='{"answer":"无"}'))
            for name, values in [('inputs',rows), ('labels',labels), ('predictions',predictions)]:
                write_jsonl(root / f'{name}.jsonl', values)
            compare(root,root,root,root/'comparison.json',view='current_only')
            report = json.loads((root/'comparison.json').read_text())
            metric = report['metrics']['presence']
            self.assertEqual((report['unique_inputs'], metric['after_correct'], metric['n']), (4,2,4))
            paired = metric['unique_cases_both_wordings']
            self.assertEqual((paired['after_correct'], paired['n']), (1,2))

    def test_missing_answer_and_one_wrong_paraphrase_cannot_pass_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = [dict(sample_id=f'q{i}', split='dev', response_format='plain',
                           view='oracle_text', task='completion', wording=i,
                           case_id='case', group_id='geometry') for i in range(2)]
            labels = [dict(sample_id=f'q{i}', expected='部分', allowed=['部分', '完整'],
                           reference_pair=None) for i in range(2)]
            write_jsonl(root / 'inputs.jsonl', inputs)
            write_jsonl(root / 'labels.jsonl', labels)
            write_jsonl(root / 'predictions.jsonl', [dict(sample_id='q0', raw_response='部分')])
            evaluate(root, root / 'predictions.jsonl', 'dev', 'plain', root / 'score', 'oracle_text')
            report = json.loads((root / 'score/summary.json').read_text())
            self.assertEqual(report['missing_rows'], 1)
            self.assertEqual(report['metrics']['oracle_text/completion/correct']['rate'], .5)
            self.assertEqual(report['metrics']['oracle_text/completion/both_correct']['rate'], 0)

    def test_format_scoring_never_extracts_a_correct_word_from_an_explanation(self):
        self.assertEqual(parse('{"answer":"部分"}', 'json', ['部分', '完整']), '部分')
        self.assertIsNone(parse('部分，也可能完整', 'plain', ['部分', '完整']))
        self.assertIsNone(parse('{"answer":"部分","extra":"完整"}', 'json', ['部分', '完整']))

    def test_target_controls_preserve_labels_and_hide_progress_from_boxes(self):
        root = DEFAULT.parent / 'state_target_controls_v1'
        cases = json.loads((root / 'cases.json').read_text())
        grouped = {}
        for case in cases:
            grouped.setdefault(case['group_id'], set()).add(tuple(target_box(case)))
            current = controlled_image(case, 'target_only').crop((0,216,432,432))
            contains_ink = current.convert('L').getextrema()[0] == 0
            self.assertEqual(contains_ink, case['fractions'][case['target']] > 0)
        self.assertTrue(all(len(bounds) == 1 for bounds in grouped.values()))
        labels = read_jsonl(root / 'original/labels.jsonl')
        for condition in ('prompt_only', 'target_boxes', 'target_only'):
            self.assertEqual(read_jsonl(root / condition / 'labels.jsonl'), labels)
        for first, second in [('original','target_only'), ('prompt_only','target_boxes')]:
            a, b = [read_jsonl(root / condition / 'inputs.jsonl') for condition in (first, second)]
            self.assertEqual([r['prompt'] for r in a], [r['prompt'] for r in b])

    def test_target_contrasts_require_different_answers_for_the_same_image(self):
        root = DEFAULT.parent / 'state_target_contrast_v1'
        rows = [r for r in read_jsonl(root / 'inputs.jsonl') if r['source_dataset'] == 'new_target_contrasts']
        labels = {r['sample_id']: r['expected'] for r in read_jsonl(root / 'labels.jsonl')}
        scenes = {s['case_id']: s for s in json.loads((root / 'scenes.json').read_text())}
        paired = defaultdict(list)
        for row in rows:
            self.assertEqual(row['split'], 'train')
            if row['view'] == 'reference_current' and row['wording'] == 0:
                paired[(row['group_id'], row['images'][0], row['task'])].append(row)
                fraction = scenes[row['scene_id']]['fractions'][row['target']]
                expected = ('有' if fraction > 0 else '无') if row['task'] == 'presence' else (
                    '未出现' if fraction == 0 else '完整' if fraction == 1 else '部分')
                self.assertEqual(labels[row['sample_id']], expected)
        for task in ('presence','completion'):
            groups = {group for (group, _, kind), items in paired.items() if kind == task
                      and len({labels[r['sample_id']] for r in items}) > 1}
            self.assertEqual(len(groups), 6)

    def test_reused_target_queries_have_the_exact_original_model_inputs(self):
        rows = read_jsonl(DEFAULT.parent / 'state_target_controls_v1/all_target_queries/inputs.jsonl')
        source = {r['sample_id']:r for r in read_jsonl(DEFAULT / 'inputs.jsonl')}
        directory = DEFAULT.parent / 'state_target_controls_v1/all_target_queries'
        reused = [r for r in rows if r['source_sample_id']]
        self.assertEqual(len(reused), 48)
        self.assertEqual(sum(r['source_sample_id'] is None for r in rows), 64)
        for row in reused:
            original = source[row['source_sample_id']]
            self.assertEqual(row['prompt'], original['prompt'])
            self.assertEqual((directory/row['images'][0]).resolve(), (DEFAULT/original['images'][0]).resolve())


if __name__ == '__main__':
    unittest.main()
