"""Compare paired state predictions, counting identical text inputs only once."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

if __package__:
    from .h1_state_gate import read_jsonl, parse, interval
else:
    from h1_state_gate import read_jsonl, parse, interval


def compare(data, before, after, output, view='oracle_text', split='dev'):
    inputs = [r for r in read_jsonl(data / 'inputs.jsonl')
              if r['split'] == split and r['view'] == view and r['response_format'] == 'json']
    labels = {r['sample_id']: r for r in read_jsonl(data / 'labels.jsonl')}
    runs = [{r['sample_id']: r for r in read_jsonl(p / 'predictions.jsonl')} for p in (before, after)]
    tasks, seen = defaultdict(list), set()
    input_cases = defaultdict(list)
    for inp in inputs:
        input_cases[(inp['task'], inp['case_id'])].append(inp)
        key = (inp['prompt'], tuple(inp['images']))
        if key in seen:
            continue
        seen.add(key)
        sid, lab = inp['sample_id'], labels[inp['sample_id']]
        scores = [int(parse(run.get(sid, {}).get('raw_response', ''), 'json', lab['allowed']) == lab['expected'])
                  for run in runs]
        tasks[inp['task']].append(dict(sample_id=sid, group_id=inp['group_id'],
                                       before=scores[0], after=scores[1], delta=scores[1] - scores[0]))
    report = dict(view=view, split=split, source_rows=len(inputs), unique_inputs=len(seen),
                  method='Exact prompt and image-path duplicates counted once; paired bootstrap over input groups.',
                  before=str(before), after=str(after), metrics={})
    for task, rows in tasks.items():
        grouped, before_values, after_values = defaultdict(list), defaultdict(list), defaultdict(list)
        for row in rows:
            grouped[row['group_id']].append(row['delta'])
            before_values[row['group_id']].append(row['before'])
            after_values[row['group_id']].append(row['after'])
        report['metrics'][task] = dict(n=len(rows), groups=len(grouped),
                                       before_correct=sum(r['before'] for r in rows),
                                       after_correct=sum(r['after'] for r in rows),
                                       accuracy_difference=sum(r['delta'] for r in rows) / len(rows),
                                       before_cluster_bootstrap_95=interval(before_values),
                                       after_cluster_bootstrap_95=interval(after_values),
                                       paired_cluster_bootstrap_95=interval(grouped))
    seen_cases, case_scores = set(), defaultdict(list)
    for (task, _), rows in input_cases.items():
        signature = tuple(sorted((r['wording'], r['prompt'], tuple(r['images'])) for r in rows))
        if (task, signature) in seen_cases:
            continue
        seen_cases.add((task, signature))
        scores = []
        for run in runs:
            correct = [parse(run.get(r['sample_id'], {}).get('raw_response', ''), 'json',
                             labels[r['sample_id']]['allowed']) == labels[r['sample_id']]['expected'] for r in rows]
            scores.append(int(len(correct) == 2 and all(correct)))
        case_scores[task].append((rows[0]['group_id'], scores))
    for task, values in case_scores.items():
        before_groups, after_groups, changes = defaultdict(list), defaultdict(list), defaultdict(list)
        for group, (a, b) in values:
            before_groups[group].append(a)
            after_groups[group].append(b)
            changes[group].append(b - a)
        report['metrics'][task]['unique_cases_both_wordings'] = dict(
            n=len(values), before_correct=sum(s[0] for _, s in values), after_correct=sum(s[1] for _, s in values),
            before_cluster_bootstrap_95=interval(before_groups),
            after_cluster_bootstrap_95=interval(after_groups), paired_change_bootstrap_95=interval(changes))
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--before', type=Path, required=True)
    p.add_argument('--after', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--view', default='oracle_text')
    p.add_argument('--split', default='dev')
    args = p.parse_args()
    compare(args.data, args.before, args.after, args.output, args.view, args.split)
