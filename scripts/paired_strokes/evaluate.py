"""Score a fixed request denominator, retaining missing and malformed outputs."""
import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

import numpy as np

from .data import read_jsonl, write_json
from .gold import qualify


def edit_distance(a, b):
    costs = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        next_costs = [i]
        for j, y in enumerate(b, 1):
            next_costs.append(min(next_costs[-1] + 1, costs[j] + 1, costs[j - 1] + (x != y)))
        costs = next_costs
    return costs[-1]


def sequence_metrics(expected, actual):
    return {'exact': expected == actual, 'count_correct': len(expected) == len(actual),
            'count_absolute_error': abs(len(expected) - len(actual)),
            'normalized_edit_distance': edit_distance(expected, actual) / max(len(expected), len(actual), 1),
            'position_correct': sum(x == y for x, y in zip(expected, actual)),
            'position_total': max(len(expected), len(actual))}


def parse_prediction(raw, metric):
    if raw is None or raw == '':
        return 'no_output', None
    try:
        obj = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError:
        return 'format_error', None
    if not isinstance(obj, dict):
        return 'format_error', None
    if obj.get('answer') == 'unknown':
        return 'unknown', None
    if metric == 'E2':
        value = obj.get('sequence')
        ok = isinstance(value, list) and bool(value) and all(type(x) is str and x in '12345'
                                                           and len(x) == 1 for x in value)
    elif metric in ('E4', 'E6'):
        value = obj.get('answer')
        ok = type(value) is bool
    elif metric == 'E6R':
        value = obj.get('token')
        ok = type(value) is str and value in ('1', '2', '3', '4', '5')
    elif metric == 'E3':
        value = obj.get('point')
        ok = (isinstance(value, list) and len(value) == 2
              and all(type(x) in (int, float) and math.isfinite(x) and 0 <= x <= 1 for x in value))
    elif metric == 'E8':
        value = obj.get('character')
        ok = isinstance(value, str) and len(value) == 1
    else:
        value = obj.get('direction')
        ok = value in ('right', 'down_right', 'down', 'down_left', 'left', 'up_left', 'up', 'up_right')
        if ok and ('start' in obj or 'end' in obj):
            points = [obj.get('start'), obj.get('end')]
            ok = all(isinstance(p, list) and len(p) == 2 and all(
                type(x) in (int, float) and math.isfinite(x) and 0 <= x <= 1 for x in p) for p in points)
    return ('valid', obj) if ok else ('format_error', None)


def evaluate(requests, predictions, labels, geometry, reviews, root, strata=()):
    request_ids = {r['id'] for r in requests}
    if len(request_ids) != len(requests):
        raise ValueError('Duplicate request ID')
    answers = {}
    for prediction in predictions:
        key = prediction['id']
        if key not in request_ids or key in answers:
            raise ValueError('Unexpected or duplicate prediction ID')
        answers[key] = prediction.get('output')
    details = []
    masks = {}
    strata_by_id = {s['sample_id']: s['tags'] for s in strata}
    for request in requests:
        key, metric = request['id'], request['metric']
        label = labels[key]
        status, output = parse_prediction(answers.get(key), metric)
        item = {'id': key, 'metric': metric, 'sample_id': request['sample_id'],
                'split': request['split'], 'stratum': request['stratum'],
                'condition': request['condition'], 'output_status': status}
        item['permission'] = request.get('permission', 'main')
        item['analysis_tags'] = strata_by_id.get(request['sample_id'], [])
        if metric == 'E4':
            item['relation'] = label['relation']
        if metric in ('E3', 'E4', 'E5') and not qualify(geometry[request['sample_id']], reviews, metric):
            item['status'] = 'unqualified_gold'
        elif label.get('answer') is None and metric in ('E4', 'E6'):
            item['status'] = 'ambiguous_gold'
        elif status != 'valid':
            item['status'] = status
        elif metric == 'E2':
            item.update(sequence_metrics(label['sequence'], output['sequence']))
            item['status'] = 'correct' if item['exact'] else 'incorrect'
        elif metric in ('E4', 'E6'):
            item['status'] = 'correct' if output['answer'] == label['answer'] else 'incorrect'
        elif metric == 'E6R':
            item['status'] = 'correct' if output['token'] == label['token'] else 'incorrect'
        elif metric == 'E8':
            item['status'] = 'correct' if output['character'] == label['character'] else 'incorrect'
        elif metric == 'E5':
            item['status'] = 'correct' if output['direction'] == label['direction'] else 'incorrect'
            if 'start' in output:
                item['endpoint_error'] = sum(math.dist(output[k], label[k]) for k in ('start', 'end')) / (2 * math.sqrt(2))
        else:
            if request['sample_id'] not in masks:
                with np.load(root / geometry[request['sample_id']]['mask_archive']) as archive:
                    masks[request['sample_id']] = archive['masks']
            sample_masks = masks[request['sample_id']]
            size = sample_masks[0].shape[0]
            x, y = [min(size - 1, int(c * size)) for c in output['point']]
            hits = [i + 1 for i, mask in enumerate(sample_masks) if mask[y, x]]
            item['status'] = ('unknown' if len(hits) > 1 else
                              'correct' if hits == [label['stroke']] else 'incorrect')
        details.append(item)

    def summarize(rows):
        result = {}
        for metric in ('E2', 'E3', 'E4', 'E5', 'E6', 'E6R', 'E8'):
            group = [r for r in rows if r['metric'] == metric]
            counts = Counter(r['status'] for r in group)
            eligible = len(group) - counts['unqualified_gold'] - counts['ambiguous_gold']
            report = {'requests': len(group), 'eligible': eligible, 'statuses': dict(counts),
                      'output_statuses': dict(Counter(r['output_status'] for r in group)),
                      'accuracy': counts['correct'] / eligible if eligible else None}
            if metric == 'E2':
                parsed = [r for r in group if 'exact' in r]
                positions = sum(r.get('position_total', len(labels[r['id']]['sequence'])) for r in group)
                report.update({'normalized_edit_distance_valid': sum(r['normalized_edit_distance'] for r in parsed) / len(parsed) if parsed else None,
                               'valid_sequence_outputs': len(parsed),
                               'position_accuracy_all_requests': sum(r['position_correct'] for r in parsed) / positions if positions else None})
                result['E1'] = {'requests': len(group), 'accuracy': sum(r['count_correct'] for r in parsed) / len(group) if group else None,
                                'count_MAE_valid': sum(r['count_absolute_error'] for r in parsed) / len(parsed) if parsed else None,
                                'valid_count_outputs': len(parsed), 'derived_from_sequence': True,
                                'output_statuses': dict(Counter(r['output_status'] for r in group))}
            if metric == 'E5':
                errors = [r['endpoint_error'] for r in group if 'endpoint_error' in r]
                report['endpoint_error_mean_valid'] = sum(errors) / len(errors) if errors else None
                report['endpoint_output_count'] = len(errors)
            result[metric] = report
        return result

    grouped = {}
    main_rows = [r for r in details if r['permission'] == 'main']
    for field in ('split', 'stratum'):
        grouped[field] = {value: summarize([r for r in main_rows if r[field] == value])
                          for value in sorted({r[field] for r in main_rows})}
    for field in ('condition', 'permission'):
        grouped[field] = {value: summarize([r for r in details if r[field] == value])
                          for value in sorted({r[field] for r in details})}
    grouped['analysis_tag'] = {tag: summarize([r for r in main_rows if tag in r['analysis_tags']])
                               for tag in sorted({tag for r in main_rows for tag in r['analysis_tags']})}
    relation_rows = [r for r in main_rows if r['metric'] == 'E4']
    grouped['relation'] = {value: summarize([r for r in relation_rows if r['relation'] == value])
                           for value in sorted({r['relation'] for r in relation_rows})}
    return {'protocol': 'paired-strokes-v1', 'scope': 'development_candidates_only',
            'predictions_received': len(predictions), 'requests': len(requests),
            'metrics': summarize(main_rows), 'by_group': grouped, 'details': details,
            'primary_CI95_by_character': {metric: grouped_interval(main_rows, metric) for metric in ('E2', 'E4')},
            'fine_type_metrics': None, 'mask_AP': None,
            'limitation': 'Point identity is not mask AP. No formal model result is inferred from fixtures.'}


def grouped_interval(details, metric, repeats=2000, seed=20261102):
    """Resample whole characters, preserving dependent queries within each glyph."""
    groups = defaultdict(list)
    for row in details:
        if row['metric'] == metric and row['status'] not in ('unqualified_gold', 'ambiguous_gold'):
            groups[row['sample_id']].append(row['status'] == 'correct')
    if len(groups) < 2:
        return {'groups': len(groups), 'interval': None, 'repeats': repeats, 'seed': seed}
    totals = np.array([(sum(values), len(values)) for _, values in sorted(groups.items())])
    indices = np.random.default_rng(seed).integers(len(totals), size=(repeats, len(totals)))
    sampled = totals[indices].sum(axis=1)
    lower, upper = np.quantile(sampled[:, 0] / sampled[:, 1], [.025, .975])
    return {'groups': len(groups), 'interval': [float(lower), float(upper)], 'repeats': repeats,
            'seed': seed, 'unit': 'character', 'scope': 'development_only_no_significance_claim'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--predictions', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--suite', type=Path, help='Optional completed CPU suite directory; image paths remain relative to dataset')
    args = parser.parse_args()
    suite = args.suite or args.dataset
    labels_path = suite / 'evaluation_only/labels.jsonl'
    labels = {r['id']: r for r in read_jsonl(labels_path)}
    geometry = {r['id']: r for r in read_jsonl(args.dataset / 'evaluation_only/geometry.jsonl')}
    strata = read_jsonl(suite / 'analysis_strata.jsonl') if args.suite else []
    result = evaluate(read_jsonl(suite / 'requests.jsonl'), read_jsonl(args.predictions),
                      labels, geometry, read_jsonl(args.dataset / 'evaluation_only/reviews.jsonl'), args.dataset, strata)
    write_json(args.output, result)
    print(json.dumps(result['metrics'], ensure_ascii=False))


if __name__ == '__main__':
    main()
