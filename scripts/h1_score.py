"""Score observed state, judgment, and proposed action separately."""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MISSING = object()


def same(actual, expected):
    return type(actual) is type(expected) and actual == expected


def same_set(actual, expected):
    return (isinstance(actual, list) and all(isinstance(x, str) for x in actual)
            and len(actual) == len(set(actual)) and set(actual) == set(expected))


def score(prediction, label):
    p = prediction if isinstance(prediction, dict) else {}
    e = label['expected']
    metrics = {}
    if 'score_fields' in label:
        for key in label['score_fields']:
            check = same_set if key in {'seen','finished','unfinished'} else same
            metrics[key] = check(p.get(key, MISSING), e[key])
        metrics['all_required'] = all(metrics.values())
        return metrics
    if label['score_observation']:
        metrics['seen'] = same_set(p.get('seen'), e['seen'])
        metrics['completion'] = all(same_set(p.get(k), e[k]) for k in ['finished','unfinished'])
        for key in ['order','directions','early_switch']:
            metrics[key] = same(p.get(key, MISSING), e[key])
    metrics['judgment'] = all(same(p.get(k, MISSING), e[k])
                              for k in ['status','first_error','error_type'])
    metrics['status'] = same(p.get('status', MISSING), e['status'])
    metrics['first_error'] = same(p.get('first_error', MISSING), e['first_error'])
    metrics['action'] = all(same(p.get(k, MISSING), e[k]) for k in ['next','target'])
    metrics['next_action'] = same(p.get('next', MISSING), e['next'])
    metrics['all_required'] = all(metrics.values())
    return metrics


def evaluate(inputs_path, labels_path, predictions_path):
    inputs = {r['sample_id']: r for r in map(json.loads, inputs_path.read_text().splitlines())}
    labels = {r['sample_id']: r for r in map(json.loads, labels_path.read_text().splitlines())}
    predictions = [json.loads(s) for s in predictions_path.read_text().splitlines()]
    ids = [r['sample_id'] for r in predictions]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate sample predictions: keep repeated runs separate')
    groups = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    detailed = []
    for r in predictions:
        sid = r['sample_id']
        inp, label = inputs[sid], labels[sid]
        metrics = score(r.get('prediction'), label)
        format_metric = 'parsed_choice' if label.get('score_fields') == ['answer'] else 'json_object'
        metrics[format_metric] = isinstance(r.get('prediction'), dict)
        if label.get('score_fields') == ['answer']:
            # Secondary analysis: accept an explicit letter plus an exact option
            # echo. The original strict score and prediction remain unchanged.
            raw=r.get('raw_response','').strip()
            match=re.fullmatch(r'([A-D])[.。]?|([A-D])[.、．]\s*(.+)',raw)
            choice=None
            if match:
                if match.group(1):
                    choice=match.group(1)
                elif match.group(3)==inp['options']['ABCD'.index(match.group(2))]:
                    choice=match.group(2)
            metrics['choice_content']=choice==label['expected']['answer']
            metrics['parsed_choice_content']=choice is not None
        for key, value in metrics.items():
            groups[inp['view']][key][0] += int(value)
            groups[inp['view']][key][1] += 1
        detailed.append(dict(sample_id=sid, construction=label['construction'],
                             metrics=metrics, prediction=r.get('prediction'), expected=label['expected']))
    summary = {view: {metric: dict(correct=c, total=n, fraction=c/n)
                       for metric, (c, n) in group.items()} for view, group in groups.items()}
    by_id = {r['sample_id']: r for r in detailed}
    pairs = []
    for a, b in [('c04','c05'), ('c09','c10')]:
        x, y = by_id.get(a+'-sampled_frames'), by_id.get(b+'-sampled_frames')
        if x and y:
            pairs.append(dict(cases=[a,b], both_orders_correct=x['metrics']['order'] and y['metrics']['order'],
                              both_judgments_correct=x['metrics']['judgment'] and y['metrics']['judgment']))
        x, y = by_id.get(a+'-order_mc'), by_id.get(b+'-order_mc')
        if x and y:
            pairs.append(dict(cases=[a,b],view='order_mc',
                              both_orders_correct=x['metrics']['answer'] and y['metrics']['answer']))
    return dict(kind='h1_small_controlled_pilot', attempted=len(predictions),
                planned=len(inputs), missing=sorted(set(inputs)-set(ids)),
                by_view=summary, same_final_pairs=pairs, details=detailed)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('predictions', type=Path)
    p.add_argument('--dataset', type=Path, default=ROOT/'data/h1/pilot_v1')
    args = p.parse_args()
    report = evaluate(args.dataset/'inputs.jsonl', args.dataset/'labels.jsonl', args.predictions)
    path = args.predictions.parent/'scores.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'details'}, ensure_ascii=False, indent=2))
