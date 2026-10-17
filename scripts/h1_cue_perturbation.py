"""Hold ink and the full UMM fixed while perturbing reference-derived target cues."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw

from h1_state_gate import ROOT, DEFAULT, read_jsonl, write_jsonl, parse, interval
from h1_target_controls import different_target_outcomes
from h1_target_grid import ADAPTER

DATA = ROOT/'data/h1/cue_perturbation_v1'
RESULT = ROOT/'results/h1/showo2_video_1_5b/cue_perturbation_v1'
SOURCE = ROOT/'data/h1/state_target_cue_v1/raw/all_targets_dev'
CORRECT = ROOT/'results/h1/showo2_video_1_5b/target_cue_v1/boxed/targets_boxed_dev'
VARIANTS = ('x_minus6','x_plus6','y_minus6','y_plus6',
            'length_minus6','length_plus6','width_minus6','width_plus6')


def save(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def shifted_bounds(points, variant):
    xs,ys=zip(*points)
    bounds=[min(xs)-12,min(ys)-12,max(xs)+12,max(ys)+12]
    axis,sign=variant.split('_')
    delta=-6 if sign=='minus6' else 6
    if axis in ('x','y'):
        a=0 if axis=='x' else 1
        bounds[a]+=delta;bounds[a+2]+=delta
    else:
        along=0 if max(xs)-min(xs)>max(ys)-min(ys) else 1
        a=along if axis=='length' else 1-along
        bounds[a]-=delta;bounds[a+2]+=delta
    return bounds


def paint(image,bounds):
    overlay=Image.new('L',image.size)
    draw=ImageDraw.Draw(overlay)
    x0,y0,x1,y1=bounds
    for offset in (0,216):
        draw.rectangle((x0,y0+offset,x1,y1+offset),outline=255,width=3)
    white=image.convert('L').point(lambda x:255 if x==255 else 0)
    result=image.copy();result.paste((30,90,210),mask=ImageChops.multiply(overlay,white))
    return result


def build():
    DATA.mkdir(parents=True,exist_ok=False);RESULT.mkdir(parents=True,exist_ok=False)
    sources=read_jsonl(SOURCE/'inputs.jsonl')
    labels={r['sample_id']:r for r in read_jsonl(SOURCE/'labels.jsonl')}
    scenes={r['case_id']:r for r in json.loads((DEFAULT/'cases.json').read_text()) if r['split']=='dev'}
    rows=[];truth=[];image_records=[]
    for variant in VARIANTS:
        (DATA/'images'/variant).mkdir(parents=True)
        for original in sources:
            row=dict(original)
            path=DATA/'images'/variant/f'{row["case_id"]}.png'
            if not path.exists():
                source=Image.open(SOURCE/row['images'][0]).convert('RGB')
                bounds=shifted_bounds(scenes[row['scene_id']]['strokes'][row['target']],variant)
                image=paint(source,bounds)
                # This is the causal control: frame changes must preserve all ink.
                ink_same=np.array_equal(np.asarray(source).max(-1)<128,np.asarray(image).max(-1)<128)
                if not ink_same: raise ValueError('Cue perturbation changed black ink.')
                image.save(path)
                image_records.append(dict(variant=variant,case_id=row['case_id'],bounds=bounds,ink_preserved=bool(ink_same)))
            row.update(original_sample_id=original['sample_id'],original_case_id=original['case_id'],
                       sample_id=f'{variant}::{original["sample_id"]}',case_id=f'{variant}::{original["case_id"]}',
                       cue_variant=variant,cue_condition='perturbed_correct_reference_box',images=[str(path.relative_to(DATA))])
            rows.append(row)
            truth.append(dict(labels[original['sample_id']],sample_id=row['sample_id']))
    write_jsonl(DATA/'inputs.jsonl',rows);write_jsonl(DATA/'labels.jsonl',truth)
    save(DATA/'cue_geometry.json',image_records)
    save(RESULT/'plan.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        role='Paired input intervention on previously inspected development states; no training, no independent acceptance.',
        adapter=str(ADAPTER.relative_to(ROOT)),questions=len(rows),source_questions=len(sources),
        geometries=3,source_target_cases=28,variants=list(VARIANTS),
        intervention='Correct reference centerline bounds plus original 12px margin; translate both panels by +/-6px in x/y or expand/contract both ends by 6px along/across the line. Stroke width/color stay unchanged.',
        controls='Same full UMM, state adapter, prompts, labels, constrained decoding and black pixels. Reuse saved correct-cue baseline. Every drawn frame stays defined by the complete reference, independent of current progress.',
        geometry='Frame contractions leave at least 6px padding from the target centerline. Width here means perpendicular frame size, not the 3px border thickness.',
        ink_invariant=dict(images=len(image_records),preserved=sum(r['ink_preserved'] for r in image_records)),
        metrics='Presence/completion accuracy, answer changes, correct-to-wrong and wrong-to-correct, both-wording accuracy, different-target pairs and correctness across all variants including baseline. Bootstrap by the three underlying geometries.',
        policy='Fixed eight interventions, one final model; do not select a best test-time cue from development results.',
        limitation='Assisted target location, fixed simple geometry and full reference; no new-character, font, temporal or unknown-state evaluation.'))
    # Fixed first previously discussed complete middle-horizontal example.
    original=next(r for r in sources if r['scene_id']=='dev-parallel_h-00-0' and r['target']=='中横')
    original_image=Image.open(SOURCE/original['images'][0]).convert('RGB')
    points=scenes[original['scene_id']]['strokes'][original['target']]
    xs,ys=zip(*points)
    chosen=[('Correct cue',paint(original_image,[min(xs)-12,min(ys)-12,max(xs)+12,max(ys)+12]))]
    for variant in ('x_plus6','length_plus6','width_plus6'):
        chosen.append((variant,Image.open(DATA/'images'/variant/f'{original["case_id"]}.png')))
    panel=Image.new('RGB',(4*222,242),'white');draw=ImageDraw.Draw(panel)
    for col,(title,im) in enumerate(chosen):
        panel.paste(im.resize((216,216)),(col*222,22));draw.text((col*222,4),title,fill='black')
    panel.save(RESULT/'examples.png')
    print(dict(questions=len(rows),images=len(image_records),ink_preserved=True))


def run():
    subprocess.run([sys.executable,str(ROOT/'scripts/h1_run_showo.py'),'--device','mps',
        '--inputs',str(DATA/'inputs.jsonl'),'--split','dev','--view','reference_current',
        '--format','json','--constrain-answers','--adapter',str(ADAPTER),'--output',str(RESULT/'run')],
        cwd=ROOT,env=dict(os.environ,PYTORCH_ENABLE_MPS_FALLBACK='1'),check=True)
    score()


def score():
    rows=read_jsonl(DATA/'inputs.jsonl')
    labels={r['sample_id']:r for r in read_jsonl(DATA/'labels.jsonl')}
    responses={r['sample_id']:r for r in read_jsonl(RESULT/'run/predictions.jsonl')}
    baseline={r['sample_id']:r for r in read_jsonl(CORRECT/'predictions.jsonl')}
    scored=[]
    for row in rows:
        label=labels[row['sample_id']]
        actual=parse(responses[row['sample_id']]['raw_response'],'json',label['allowed'])
        before=parse(baseline[row['original_sample_id']]['raw_response'],'json',label['allowed'])
        scored.append(dict(sample_id=row['sample_id'],original_sample_id=row['original_sample_id'],
            original_case_id=row['original_case_id'],group_id=row['group_id'],variant=row['cue_variant'],
            target=row['target'],task=row['task'],wording=row['wording'],expected=label['expected'],
            answer=actual,baseline_answer=before,correct=actual==label['expected'],
            baseline_correct=before==label['expected'],answer_changed=actual!=before))
    write_jsonl(RESULT/'scored.jsonl',scored)
    summary={};pair_definitions=different_target_outcomes(SOURCE,CORRECT)
    for variant in VARIANTS:
        for task in ('presence','completion'):
            selected=[r for r in scored if r['variant']==variant and r['task']==task]
            lookup={r['original_sample_id']:r for r in selected}
            groups=defaultdict(list);changes=defaultdict(list);cases=defaultdict(list)
            for row in selected:
                groups[row['group_id']].append(int(row['correct']))
                changes[row['group_id']].append(int(row['correct'])-int(row['baseline_correct']))
                cases[row['original_case_id']].append(row)
            pairs=[dict(group_id=p['group_id'],correct=all(lookup[s]['correct'] for s in p['sample_ids']))
                   for p in pair_definitions if p['task']==task]
            summary[f'{variant}/{task}']=dict(n=len(selected),correct=sum(r['correct'] for r in selected),
                answer_changes=sum(r['answer_changed'] for r in selected),
                regressions=sum(r['baseline_correct'] and not r['correct'] for r in selected),
                repairs=sum(not r['baseline_correct'] and r['correct'] for r in selected),
                both_wordings_correct=sum(all(r['correct'] for r in group) for group in cases.values()),cases=len(cases),
                target_pairs_correct=sum(r['correct'] for r in pairs),target_pairs=len(pairs),
                cluster_bootstrap_95=interval(groups),paired_difference_bootstrap_95=interval(changes))
    robust={}
    for task in ('presence','completion'):
        by_question=defaultdict(list)
        for row in scored:
            if row['task']==task:by_question[row['original_sample_id']].append(row)
        outcomes=[]
        for sid,values in by_question.items():
            outcomes.append(dict(sample_id=sid,group_id=values[0]['group_id'],
                all_correct=values[0]['baseline_correct'] and all(r['correct'] for r in values),
                all_same=all(not r['answer_changed'] for r in values)))
        grouped=defaultdict(list)
        for r in outcomes:grouped[r['group_id']].append(int(r['all_correct']))
        robust[task]=dict(questions=len(outcomes),all_conditions_correct=sum(r['all_correct'] for r in outcomes),
            all_answers_same=sum(r['all_same'] for r in outcomes),cluster_bootstrap_95=interval(grouped))
    save(RESULT/'score.json',dict(conditions=summary,including_baseline_robustness=robust,
        limitation='Repeated three-group development intervention; correlated perturbations are not new independent geometries. No best-cue selection.'))
    print(json.dumps(dict(conditions=summary,robustness=robust),ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','run','score'])
    parser.add_argument('--data',type=Path,default=DATA);parser.add_argument('--output',type=Path,default=RESULT)
    args=parser.parse_args();DATA,RESULT=args.data.resolve(),args.output.resolve()
    {'build':build,'run':run,'score':score}[args.command]()
