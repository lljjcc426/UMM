"""Separate target selection from state comparison on existing H1 development cases."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
import json
import os
from pathlib import Path

from PIL import ImageDraw

if __package__:
    from .h1_state_gate import ROOT, DEFAULT, render, read_jsonl, write_jsonl, evaluate, parse, interval
    from .h1_compare_state_runs import compare
else:
    from h1_state_gate import ROOT, DEFAULT, render, read_jsonl, write_jsonl, evaluate, parse, interval
    from h1_compare_state_runs import compare

DATA = ROOT / 'data/h1/state_target_controls_v1'
RESULTS = ROOT / 'results/h1/showo2_video_1_5b/target_controls_v1'
CUE = '若图中有蓝色框，它们只标示参考与当前的目标区域；框线不计入笔迹。仍按黑色目标线条判断。'
CONDITIONS = ['original', 'prompt_only', 'target_boxes', 'target_only']


def target_box(case):
    points = case['strokes'][case['target']]
    xs, ys = zip(*points)
    return [min(xs) - 12, min(ys) - 12, max(xs) + 12, max(ys) + 12]


def controlled_image(case, condition):
    if condition == 'target_only':
        target = case['target']
        isolated = dict(case, strokes={target: case['strokes'][target]},
                        fractions={target: case['fractions'][target]})
        return render(isolated)[0]
    image = render(case)[0]
    if condition == 'target_boxes':
        draw = ImageDraw.Draw(image)
        x0, y0, x1, y1 = target_box(case)
        for offset in (0, 216):
            draw.rectangle((x0, y0 + offset, x1, y1 + offset), outline=(30, 90, 210), width=3)
    return image


def build(data):
    cases = [c for c in json.loads((DEFAULT / 'cases.json').read_text())
             if c['split'] == 'dev' and c['layout'] in ('parallel_h', 'parallel_v', 'cross')]
    case_ids = {c['case_id'] for c in cases}
    inputs = [r for r in read_jsonl(DEFAULT / 'inputs.jsonl') if r['case_id'] in case_ids
              and r['view'] == 'reference_current' and r['response_format'] == 'json']
    input_ids = {r['sample_id'] for r in inputs}
    labels = [r for r in read_jsonl(DEFAULT / 'labels.jsonl') if r['sample_id'] in input_ids]
    data.mkdir(parents=True, exist_ok=True)
    for condition in CONDITIONS:
        directory = data / condition
        directory.mkdir(exist_ok=True)
        if condition in ('target_boxes', 'target_only'):
            (directory / 'images').mkdir(exist_ok=True)
            for case in cases:
                controlled_image(case, condition).save(directory / 'images' / f'{case["case_id"]}.png')
        rows = []
        for row in inputs:
            path = (f'images/{row["case_id"]}.png' if condition in ('target_boxes', 'target_only') else
                    os.path.relpath(DEFAULT / row['images'][0], directory))
            rows.append(dict(row, condition=condition, images=[path],
                             prompt=(CUE if condition in ('prompt_only', 'target_boxes') else '') + row['prompt']))
        write_jsonl(directory / 'inputs.jsonl', rows)
        write_jsonl(directory / 'labels.jsonl', labels)
    (data / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n')
    metadata = dict(source_data=str(DEFAULT.relative_to(ROOT)), split='dev', cases=len(cases),
                    groups=len({c['group_id'] for c in cases}), rows_per_condition=len(inputs),
                    conditions=CONDITIONS, cue=CUE,
                    target_boxes={c['case_id']: target_box(c) for c in cases},
                    box_policy='Full reference path bounds plus 12 pixels, repeated at y+216; independent of current fraction.',
                    isolation_policy='Re-render only the known target in reference and current; preserve scale, location, width and target progress.',
                    source_model_run='results/h1/showo2_video_1_5b/visual_adaptation_v1_reference_dev',
                    model_adapter='checkpoints/h1_visual_state_lora_v1/adapter.pt',
                    interpretation='Known-target diagnostic only. No training, no held-out inference, no autonomous localization claim.')
    (data / 'build.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(cases)} existing cases; {len(inputs)} questions per condition; three new model runs.')


def analyze(data, results):
    original = results / 'original_subset'
    original.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'results/h1/showo2_video_1_5b/visual_adaptation_v1_reference_dev'
    inputs = read_jsonl(data / 'original/inputs.jsonl')
    ids = {r['sample_id'] for r in inputs}
    write_jsonl(original / 'inputs.jsonl', inputs)
    write_jsonl(original / 'predictions.jsonl', [r for r in read_jsonl(source / 'predictions.jsonl') if r['sample_id'] in ids])
    metadata = dict(record_type='Subset of a completed run; no new model calls.',
                    source_run=str(source.relative_to(ROOT)),
                    source_run_metadata=json.loads((source / 'run.json').read_text()),
                    rows=len(inputs), extracted_utc=datetime.now(timezone.utc).isoformat())
    (original / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')
    for condition in CONDITIONS:
        run = original if condition == 'original' else results / condition
        evaluate(data / condition, run / 'predictions.jsonl', 'dev', 'json', run / 'score', 'reference_current')
    for name, before, after in [('prompt_vs_original', original, 'prompt_only'),
                                ('boxes_vs_matched_prompt', results / 'prompt_only', 'target_boxes'),
                                ('isolation_vs_original', original, 'target_only')]:
        path = results / f'{name}.json'
        compare(data / after, before, results / after, path, 'reference_current')
        report = json.loads(path.read_text())
        report['comparison_scope'] = 'Fixed model, matched source cases; input intervention. Deduplication uses after-condition visible inputs.'
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


def build_training_subset(data):
    source = ROOT / 'data/h1/state_visual_training_v1'
    groups = {'train-parallel_h-00', 'train-parallel_v-00', 'train-cross-00'}
    rows = [r for r in read_jsonl(source / 'inputs.jsonl') if r['group_id'] in groups
            and r['view'] == 'reference_current' and r['response_format'] == 'json']
    directory = data / 'training_subset'
    directory.mkdir(parents=True, exist_ok=True)
    rows = [dict(r, condition='training_subset', images=[os.path.relpath(source / r['images'][0], directory)]) for r in rows]
    ids = {r['sample_id'] for r in rows}
    write_jsonl(directory / 'inputs.jsonl', rows)
    write_jsonl(directory / 'labels.jsonl', [r for r in read_jsonl(source / 'labels.jsonl') if r['sample_id'] in ids])
    (directory / 'build.json').write_text(json.dumps(dict(
        role='Seen-training-example fit check; never a development or held-out result.',
        source_data=str(source.relative_to(ROOT)), split='train', groups=sorted(groups),
        cases=len({r['case_id'] for r in rows}), rows=len(rows),
        selection='First geometry of each of the three multi-instance layouts; all four states and both wordings.'), indent=2) + '\n')
    print(f'{len(rows)} seen training questions; training split retained.')


def build_all_target_queries(data):
    if __package__:
        from .h1_target_contrast import visual_templates, target_blind_bound
    else:
        from h1_target_contrast import visual_templates, target_blind_bound
    templates = visual_templates(ROOT / 'data/h1/state_visual_training_v1')
    cases = json.loads((data / 'cases.json').read_text())
    directory = data / 'all_target_queries'
    directory.mkdir(parents=True, exist_ok=True)
    rows, labels = [], []
    for scene in cases:
        for index, target in enumerate(scene['strokes']):
            case_id = f'{scene["case_id"]}-target-{index}'
            fraction = scene['fractions'][target]
            for task in ('presence','completion'):
                expected = ('有' if fraction else '无') if task == 'presence' else (
                    '未出现' if fraction == 0 else '完整' if fraction == 1 else '部分')
                for wording in (0,1):
                    template = templates[(scene['layout'],target,'reference_current',task,wording)]
                    suffix = f'-reference_current-{task}-q{wording}-json'
                    sid = case_id + suffix
                    rows.append(dict(template, sample_id=sid, case_id=case_id, split='dev',
                                     group_id=scene['group_id'], scene_id=scene['case_id'], target=target,
                                     source_sample_id=scene['case_id']+suffix if target == scene['target'] else None,
                                     images=[os.path.relpath(DEFAULT / 'images' / f'{scene["case_id"]}.png', directory)]))
                    labels.append(dict(sample_id=sid, expected=expected,
                                       allowed=['有','无'] if task == 'presence' else ['未出现','部分','完整','未知'],
                                       reference_pair=None))
    write_jsonl(directory / 'inputs.jsonl', rows)
    write_jsonl(directory / 'new_queries.jsonl', [r for r in rows if r['source_sample_id'] is None])
    write_jsonl(directory / 'labels.jsonl', labels)
    (directory / 'build.json').write_text(json.dumps(dict(
        role='Same original development images, all target names queried; no new held-out claim.',
        scenes=len(cases), groups=len({c['group_id'] for c in cases}), rows=len(rows),
        target_cases=len({r['case_id'] for r in rows}),
        reusable_baseline_rows=sum(r['source_sample_id'] is not None for r in rows),
        new_baseline_rows=sum(r['source_sample_id'] is None for r in rows),
        target_blind_per_scene_upper_bound=target_blind_bound(rows,{r['sample_id']:r['expected'] for r in labels}),
        baseline_adapter='checkpoints/h1_visual_state_lora_v1/adapter.pt'), indent=2) + '\n')
    print(f'{len(rows)} target-conditioned questions on the same {len(cases)} development images.')


def analyze_target_queries(data, results, after):
    directory = data / 'all_target_queries'
    rows = read_jsonl(directory / 'inputs.jsonl')
    labels = {r['sample_id']: r for r in read_jsonl(directory / 'labels.jsonl')}
    source = ROOT / 'results/h1/showo2_video_1_5b/visual_adaptation_v1_reference_dev'
    new_source = results / 'all_target_new_queries'
    old = {r['sample_id']: r for r in read_jsonl(source / 'predictions.jsonl')}
    new = {r['sample_id']: r for r in read_jsonl(new_source / 'predictions.jsonl')}
    before = results / 'all_target_baseline'
    before.mkdir(parents=True, exist_ok=False)
    predictions = []
    for row in rows:
        reused = row['source_sample_id']
        record = old[reused] if reused else new[row['sample_id']]
        predictions.append(dict(record, sample_id=row['sample_id'], source_sample_id=record['sample_id'],
                                source_run=str((source if reused else new_source).relative_to(ROOT))))
    write_jsonl(before / 'inputs.jsonl', rows)
    write_jsonl(before / 'predictions.jsonl', predictions)
    (before / 'run.json').write_text(json.dumps(dict(
        record_type='48 identical original inputs reused, plus 64 new queries from the same model.',
        source_runs=[str(p.relative_to(ROOT)) for p in (source,new_source)],
        assembled_utc=datetime.now(timezone.utc).isoformat(), model_adapter='checkpoints/h1_visual_state_lora_v1/adapter.pt'), indent=2) + '\n')
    for run in (before,after):
        evaluate(directory, run / 'predictions.jsonl', 'dev', 'json', run / 'score', 'reference_current')
    compare(directory,before,after,results / 'all_target_comparison.json','reference_current')
    runs = [{r['sample_id']:r for r in read_jsonl(p / 'predictions.jsonl')} for p in (before,after)]
    scene_queries = defaultdict(list)
    for row in rows:
        scene_queries[(row['scene_id'],row['task'],row['wording'])].append(row)
    metrics = defaultdict(lambda: defaultdict(list))
    for (_,task,_), queries in scene_queries.items():
        for a,b in combinations(queries,2):
            if labels[a['sample_id']]['expected'] == labels[b['sample_id']]['expected']:
                continue
            correct = []
            for run in runs:
                correct.append(int(all(parse(run.get(r['sample_id'],{}).get('raw_response',''),'json',
                                             labels[r['sample_id']]['allowed']) == labels[r['sample_id']]['expected']
                                       for r in (a,b))))
            metrics[task][a['group_id']].append(correct)
    report = dict(role='Two differently labelled targets in the same image must both be correct.',
                  before=str(before.relative_to(ROOT)), after=str(after.relative_to(ROOT)), metrics={})
    for task,grouped in metrics.items():
        values = [s for group in grouped.values() for s in group]
        changes = {g:[b-a for a,b in v] for g,v in grouped.items()}
        report['metrics'][task] = dict(n_target_pairs=len(values), geometry_groups=len(grouped),
                                       before_correct=sum(a for a,b in values), after_correct=sum(b for a,b in values),
                                       paired_cluster_bootstrap_95=interval(changes))
    (results / 'different_target_pairs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2) + '\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['build', 'build-training-subset', 'build-all-target-queries', 'analyze', 'analyze-target-queries'])
    p.add_argument('--data', type=Path, default=DATA)
    p.add_argument('--results', type=Path, default=RESULTS)
    p.add_argument('--after', type=Path, default=ROOT / 'results/h1/showo2_video_1_5b/target_contrast_v1_all_targets_dev')
    args = p.parse_args()
    args.data, args.results, args.after = args.data.resolve(), args.results.resolve(), args.after.resolve()
    if args.command == 'build':
        build(args.data)
    elif args.command == 'build-training-subset':
        build_training_subset(args.data)
    elif args.command == 'build-all-target-queries':
        build_all_target_queries(args.data)
    elif args.command == 'analyze-target-queries':
        analyze_target_queries(args.data, args.results, args.after)
    else:
        analyze(args.data, args.results)
