"""Build same-image, different-target state supervision with the existing visual replay."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import product
import json
import os
from pathlib import Path
import random

if __package__:
    from .h1_state_gate import ROOT, LAYOUTS, render, read_jsonl, write_jsonl
else:
    from h1_state_gate import ROOT, LAYOUTS, render, read_jsonl, write_jsonl

DEFAULT = ROOT / 'data/h1/state_target_contrast_v1'


def visual_templates(source):
    cases = {c['case_id']: c for c in json.loads((source / 'cases.json').read_text())}
    return {(r['layout'], cases[r['case_id']]['target'], r['view'], r['task'], r['wording']): r
            for r in read_jsonl(source / 'inputs.jsonl')}


def target_blind_bound(rows, labels):
    grouped = defaultdict(Counter)
    for row in rows:
        grouped[(row['view'],row['task'],row['wording'],tuple(row['images']))][labels[row['sample_id']]] += 1
    totals = defaultdict(lambda: [0,0])
    for (view,task,_,_), counts in grouped.items():
        totals[f'{view}/{task}'][0] += max(counts.values())
        totals[f'{view}/{task}'][1] += sum(counts.values())
    return {key:dict(correct_upper_bound=a,n=n,rate=a/n) for key,(a,n) in totals.items()}


def build(output):
    source = ROOT / 'data/h1/state_visual_training_v1'
    replay = read_jsonl(source / 'inputs.jsonl')
    # Visual prompts contain the target name but no geometry or progress values.
    templates = visual_templates(source)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'images').mkdir(exist_ok=True)
    rng = random.Random(70847)
    rows, labels, scenes = [], [], []
    for layout in ('parallel_h', 'parallel_v', 'cross'):
        template = LAYOUTS[layout]
        names = list(template)
        for geometry in range(2):
            dx, dy = rng.randint(-14,14), rng.randint(-6,6)
            sx, sy = rng.uniform(.82,1.02), rng.uniform(.8,1.2)
            width = rng.choice([5,7,9])
            partial = [.35,.75][geometry]
            strokes = {n: [(round(216+(x-216)*sx+dx), round(105+(y-105)*sy+dy)) for x,y in points]
                       for n,points in template.items()}
            if len(names) == 3:
                base = [0,partial,1]
                patterns = [base[i:] + base[:i] for i in range(3)] + [[f]*3 for f in base]
            else:
                patterns = list(product([0,partial,1], repeat=2))
            group = f'contrast-train-{layout}-{geometry:02d}'
            for index, pattern in enumerate(patterns):
                scene_id = f'{group}-state-{index:02d}'
                scene = dict(case_id=scene_id, group_id=group, split='train', layout=layout,
                             strokes=strokes, width=width, fractions=dict(zip(names,pattern)),
                             reference_pair=None)
                scenes.append(scene)
                reference, current = render(scene)
                reference.save(output / 'images' / f'{scene_id}.png')
                current.save(output / 'images' / f'{scene_id}-current.png')
                for target_index, target in enumerate(names):
                    fraction = scene['fractions'][target]
                    case_id = f'{scene_id}-target-{target_index}'
                    for view in ('reference_current','current_only'):
                        for task in ('presence','completion'):
                            expected = ('有' if fraction else '无') if task == 'presence' else (
                                '未出现' if fraction == 0 else '未知' if view == 'current_only' else
                                '完整' if fraction == 1 else '部分')
                            for wording in (0,1):
                                template_row = templates[(layout,target,view,task,wording)]
                                sid = f'{case_id}-{view}-{task}-q{wording}-json'
                                image = f'images/{scene_id}' + ('-current.png' if view == 'current_only' else '.png')
                                rows.append(dict(template_row, sample_id=sid, case_id=case_id, group_id=group,
                                                 scene_id=scene_id, target=target, images=[image],
                                                 source_dataset='new_target_contrasts'))
                                labels.append(dict(sample_id=sid, expected=expected,
                                                   allowed=['有','无'] if task == 'presence' else ['未出现','部分','完整','未知'],
                                                   reference_pair=None))
    new_rows = len(rows)
    for row in replay:
        rows.append(dict(row, images=[os.path.relpath(source / row['images'][0], output)],
                         source_dataset=str(source.relative_to(ROOT))))
    labels.extend(read_jsonl(source / 'labels.jsonl'))
    write_jsonl(output / 'inputs.jsonl', rows)
    write_jsonl(output / 'labels.jsonl', labels)
    (output / 'scenes.json').write_text(json.dumps(scenes, ensure_ascii=False, indent=2) + '\n')
    metadata = dict(seed=70847, split='train', new_scenes=len(scenes),
                    new_geometry_groups=len({c['group_id'] for c in scenes}), new_rows=new_rows,
                    new_target_cases=len({r['case_id'] for r in rows[:new_rows]}),
                    replay_rows=len(replay), visual_total_rows=len(rows),
                    new_rows_by_view=Counter(r['view'] for r in rows[:new_rows]), new_image_files=len(scenes)*2,
                    target_blind_per_scene_upper_bound=target_blind_bound(rows[:new_rows],{r['sample_id']:r['expected'] for r in labels}),
                    source_replay=str(source.relative_to(ROOT)),
                    text_replay='data/h1/state_training_v1',
                    training_plan=dict(initial_adapter='checkpoints/h1_visual_state_lora_v1/adapter.pt',
                                       epochs=1, accumulation=4, lr=2e-4, seed=731,
                                       adapter='same last-eight-layer rank-8 q/v LoRA',
                                       total_rows=len(rows)+512, total_steps=(len(rows)+512)//4),
                    evaluation='Fixed final adapter, original visual dev and text dev; no test calls; no mid-training selection.',
                    scope='Synthetic whole-image state learning; no target boxes, isolated targets, order, characters or fonts.')
    (output / 'build.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=DEFAULT)
    build(p.parse_args().output)
