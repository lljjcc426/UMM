"""Matched target-location training and retention controls for the full Show-o2 UMM."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import contextlib
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw

if __package__:
    from .h1_state_gate import ROOT, DEFAULT, read_jsonl, write_jsonl, evaluate, interval
    from .h1_target_controls import CUE, score_different_targets, compare_different_targets, different_target_outcomes
    from .h1_compare_state_runs import compare
else:
    from h1_state_gate import ROOT, DEFAULT, read_jsonl, write_jsonl, evaluate, interval
    from h1_target_controls import CUE, score_different_targets, compare_different_targets, different_target_outcomes
    from h1_compare_state_runs import compare

DATA = ROOT / 'data/h1/state_target_cue_v1'
RESULTS = ROOT / 'results/h1/showo2_video_1_5b/target_cue_v1'
INITIAL = ROOT / 'checkpoints/h1_target_contrast_lora_v1/adapter.pt'
TEXT = ROOT / 'data/h1/state_training_v1'
VISUAL = ROOT / 'data/h1/state_visual_training_v1'
CONTRAST = ROOT / 'data/h1/state_target_contrast_v1'
CONTROLS = ROOT / 'data/h1/state_target_controls_v1'


def add_target_box(image, reference_points):
    """Location comes only from the complete reference; preserve every ink pixel."""
    xs, ys = zip(*reference_points)
    bounds = [min(xs)-12, min(ys)-12, max(xs)+12, max(ys)+12]
    overlay = Image.new('L', image.size)
    draw = ImageDraw.Draw(overlay)
    for offset in (0, 216):
        x0, y0, x1, y1 = bounds
        draw.rectangle((x0, y0+offset, x1, y1+offset), outline=255, width=3)
    white = image.convert('L').point(lambda x: 255 if x == 255 else 0)
    mask = ImageChops.multiply(overlay, white)
    result = image.copy()
    result.paste((30, 90, 210), mask=mask)
    return result


def build(data=DATA, results=RESULTS):
    data.mkdir(parents=True, exist_ok=False)
    results.mkdir(parents=True, exist_ok=False)
    contrast_rows = read_jsonl(CONTROLS / 'contrast_training_subset/inputs.jsonl')
    current_rows = [r for r in read_jsonl(VISUAL/'inputs.jsonl') if r['view'] == 'current_only']
    ref_dev = [r for r in read_jsonl(DEFAULT/'inputs.jsonl')
               if r['split'] == 'dev' and r['view'] == 'reference_current' and r['response_format'] == 'json']
    target_dev = read_jsonl(CONTROLS/'all_target_queries/inputs.jsonl')
    scenes = {c['case_id']: c for c in json.loads((CONTRAST/'scenes.json').read_text())}
    cases = {c['case_id']: c for c in json.loads((DEFAULT/'cases.json').read_text()) if c['split'] == 'dev'}
    label_map = {}
    for directory in (CONTRAST, VISUAL, DEFAULT, CONTROLS/'all_target_queries'):
        label_map.update({r['sample_id']: r for r in read_jsonl(directory/'labels.jsonl')})
    manifests = {
        'train': [(r, CONTROLS/'contrast_training_subset') for r in contrast_rows]
                 + [(r, VISUAL) for r in current_rows],
        'train_reference': [(r, CONTROLS/'contrast_training_subset') for r in contrast_rows],
        'reference_dev': [(r, DEFAULT) for r in ref_dev],
        'all_targets_dev': [(r, CONTROLS/'all_target_queries') for r in target_dev],
    }
    box_sources = {}
    for arm in ('raw', 'boxed'):
        (data/arm/'images').mkdir(parents=True)
        for name, source_rows in manifests.items():
            directory = data/arm/name
            directory.mkdir()
            rows = []
            for original, source in source_rows:
                row = dict(original)
                image_path = source / row['images'][0]
                if row['view'] == 'reference_current':
                    row['prompt'] = CUE + row['prompt']
                    scene_id = row.get('scene_id', row['case_id'])
                    scene = scenes[scene_id] if row['split'] == 'train' else cases[scene_id]
                    target = row.get('target', scene.get('target'))
                    target_index = list(scene['strokes']).index(target)
                    key = f'{scene_id}-target-{target_index}'
                    points = scene['strokes'][target]
                    if arm == 'boxed':
                        destination = data/arm/'images'/f'{key}.png'
                        if not destination.exists():
                            with Image.open(image_path) as source_image:
                                add_target_box(source_image.convert('RGB'), points).save(destination)
                        image_path = destination
                        box_sources[key] = dict(scene_id=scene_id, target=target,
                                                complete_reference_points=points)
                    row.update(scene_id=scene_id, target=target)
                row['images'] = [os.path.relpath(image_path, directory)]
                row['cue_condition'] = arm if row['view'] == 'reference_current' else 'unmarked_current_replay'
                rows.append(row)
            write_jsonl(directory/'inputs.jsonl', rows)
            write_jsonl(directory/'labels.jsonl', [label_map[r['sample_id']] for r in rows])
    (data/'box_sources.json').write_text(json.dumps(box_sources, ensure_ascii=False, indent=2)+'\n')
    plan = dict(created_utc=datetime.now(timezone.utc).isoformat(),
        objective='Test trained reference-derived target boxes against matched unmarked training, while retaining text and no-reference judgments.',
        initial_adapter=str(INITIAL.relative_to(ROOT)),
        arms=['raw', 'boxed'],
        visual_training_rows=dict(reference_current=len(contrast_rows), current_only=len(current_rows)),
        text_replay_rows=512, text_replay=str(TEXT.relative_to(ROOT)),
        training=dict(epochs=3, steps=942, accumulation=4, learning_rate=2e-4, seed=731,
                      rank=8, alpha=16, layers=list(range(20,28)), trainable_parameters=311296,
                      gradient_checkpointing=False, loss='Same answer and EOS cross entropy.'),
        controls='Same initial weights, row order, optimizer, update count and reference-current prompts in both arms. Only those images gain boxes in the boxed arm. Current-only and text replay are identical.',
        cue='Blue bounds from complete reference geometry plus 12-pixel margin, repeated in current panel, independent of current progress; only white pixels painted. No boxes on current-only input.',
        interpretation='Known-reference target-location assistance. Not autonomous target localization. No current-state label determines the cue.',
        evaluation=dict(policy='Final checkpoints only; no intermediate selection. Original visual test unused.',
                        per_arm=['432 matched training reference questions', '104 matched reference dev questions',
                                 '112 raw target dev questions', '112 boxed target dev questions',
                                 '104 original current-only dev questions', '208 original text dev questions'],
                        primary='Both differently labelled targets correct; training and dev reported separately.',
                        retention='Current-only and text scores deduplicated by actual visible inputs.',
                        no_claim='Static synthetic line states do not demonstrate character, font, temporal or generation competence.'))
    (results/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    (data/'build.json').write_text(json.dumps(dict(
        generated_reference_images=len(box_sources), manifests={k:len(v) for k,v in manifests.items()},
        training_labels_by_view_task={f'{v}/{t}':dict(Counter(label_map[r['sample_id']]['expected']
             for r,_ in manifests['train'] if r['view']==v and r['task']==t))
             for v in ('reference_current','current_only') for t in ('presence','completion')},
        plan=str((results/'plan.json').relative_to(ROOT))),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(plan,ensure_ascii=False,indent=2))


def execute(data=DATA, results=RESULTS, adapter_prefix='h1_target_cue'):
    """Run the predeclared two-arm experiment once, retaining every final evaluation."""
    env = dict(os.environ, PYTORCH_ENABLE_MPS_FALLBACK='1')
    for arm in ('raw', 'boxed'):
        adapter = ROOT/f'checkpoints/{adapter_prefix}_{arm}_v1/adapter.pt'
        training = results/arm/'training'
        print(f'START TRAIN {arm}',flush=True)
        subprocess.run([sys.executable,str(ROOT/'scripts/h1_train_state.py'),
            '--data',str(data/arm/'train'),'--views','reference_current','current_only',
            '--text-replay',str(TEXT),'--init-adapter',str(INITIAL),'--epochs','3',
            '--output',str(training),'--adapter',str(adapter),
            '--eval-policy','Matched raw/boxed final checkpoints only; training fit, both cue conditions, current-only and text retention; original test untouched.'],
            env=env,cwd=ROOT,check=True)
        evaluations = [
            ('train_reference',data/arm/'train_reference','train','reference_current'),
            ('reference_dev',data/arm/'reference_dev','dev','reference_current'),
            ('targets_raw_dev',data/'raw/all_targets_dev','dev','reference_current'),
            ('targets_boxed_dev',data/'boxed/all_targets_dev','dev','reference_current'),
            ('current_dev',DEFAULT,'dev','current_only'),
            ('text_dev',TEXT,'dev','oracle_text')]
        for name,directory,split,view in evaluations:
            output=results/arm/name
            print(f'START EVAL {arm}/{name}',flush=True)
            subprocess.run([sys.executable,str(ROOT/'scripts/h1_run_showo.py'),'--device','mps',
                '--inputs',str(directory/'inputs.jsonl'),'--split',split,'--view',view,
                '--format','json','--constrain-answers','--adapter',str(adapter),'--output',str(output)],
                env=env,cwd=ROOT,check=True)
            with contextlib.redirect_stdout(io.StringIO()):
                evaluate(directory,output/'predictions.jsonl',split,'json',output/'score',view)
                if name == 'train_reference' or name.startswith('targets_'):
                    pairs=score_different_targets(directory,output,output/'score/different_target_pairs.json')
                if name in ('current_dev','text_dev'):
                    prior=ROOT/'results/h1/showo2_video_1_5b'/f'target_contrast_v1_{name}'
                    compare(directory,prior,output,results/arm/f'{name}_vs_initial.json',view,'dev')
            summary=json.loads((output/'score/summary.json').read_text())
            print('RESULT',arm,name,{k:(v['correct'],v['n']) for k,v in summary['metrics'].items()
                                      if k.endswith('/correct') or k.endswith('/both_correct')},flush=True)
            if name == 'train_reference' or name.startswith('targets_'):
                print('TARGET PAIRS',pairs['metrics'],flush=True)
    with contextlib.redirect_stdout(io.StringIO()):
        for name,directory,view,split in [
            ('train_reference',data/'raw/train_reference','reference_current','train'),
            ('reference_dev',data/'raw/reference_dev','reference_current','dev'),
            ('targets_raw_dev',data/'raw/all_targets_dev','reference_current','dev'),
            ('targets_boxed_dev',data/'boxed/all_targets_dev','reference_current','dev'),
            ('current_dev',DEFAULT,'current_only','dev'),('text_dev',TEXT,'oracle_text','dev')]:
            output=results/f'{name}_boxed_training_vs_raw_training.json'
            compare(directory,results/'raw'/name,results/'boxed'/name,output,view,split)
            report=json.loads(output.read_text())
            report['comparison_scope']=('Matched state IDs and prompts; both training and evaluation images differ by reference-derived cues.'
                if name in ('train_reference','reference_dev') else
                'Identical evaluation inputs; models differ in whether reference-current training images carried cues.')
            output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            if name == 'train_reference' or name.startswith('targets_'):
                compare_different_targets(directory,results/'raw'/name,results/'boxed'/name,
                    results/f'{name}_target_pairs_boxed_training_vs_raw_training.json')
    print('ALL MATCHED TARGET CUE RUNS COMPLETED',flush=True)


def analyze(data=DATA, results=RESULTS):
    """Separate training-cue and inference-cue effects on the same target pairs."""
    runs={}
    for training in ('raw','boxed'):
        for observed in ('raw','boxed'):
            directory=results/training/f'targets_{observed}_dev'
            metadata=json.loads((directory/'run.json').read_text())
            if not metadata.get('finished_utc'):
                raise ValueError(f'Evaluation is still running: {directory}')
            runs[(training,observed)]=different_target_outcomes(data/observed/'all_targets_dev',directory)
    report=dict(
        role='Four completed final-checkpoint conditions on the same underlying scenes; target boxes change with the queried target.',
        unit='Both differently labelled targets correct, for one wording; geometry-group bootstrap.',
        formulas={
            'training_effect_on_raw':'boxed-trained/raw-input minus raw-trained/raw-input',
            'training_effect_on_boxed':'boxed-trained/boxed-input minus raw-trained/boxed-input',
            'cue_effect_in_raw_model':'raw-trained/boxed-input minus raw-trained/raw-input',
            'cue_effect_in_boxed_model':'boxed-trained/boxed-input minus boxed-trained/raw-input',
            'cue_by_training_interaction':'cue effect in boxed-trained model minus cue effect in raw-trained model'},
        limitations='Three development geometry groups and one seed; assisted localization and task adaptation only, not independent H1 or UMM generation benefit.',
        cells={}, contrasts={})
    for task in ('presence','completion'):
        cells={key:[r for r in rows if r['task']==task] for key,rows in runs.items()}
        report['cells'][task]={f'{a}_training/{b}_input':dict(
            correct=sum(r['correct'] for r in rows), n=len(rows)) for (a,b),rows in cells.items()}
        grouped=defaultdict(lambda:defaultdict(list))
        reference=cells[('raw','raw')]
        indexed={key:{tuple(r['sample_ids']):r['correct'] for r in rows} for key,rows in cells.items()}
        for row in reference:
            sid=tuple(row['sample_ids'])
            rr,rb,br,bb=[indexed[key][sid] for key in [('raw','raw'),('raw','boxed'),('boxed','raw'),('boxed','boxed')]]
            values=dict(training_effect_on_raw=br-rr,training_effect_on_boxed=bb-rb,
                        cue_effect_in_raw_model=rb-rr,cue_effect_in_boxed_model=bb-br,
                        cue_by_training_interaction=(bb-br)-(rb-rr))
            for name,value in values.items():
                grouped[name][row['group_id']].append(value)
        report['contrasts'][task]={name:dict(
            difference=sum(sum(xs) for xs in groups.values())/sum(map(len,groups.values())),
            n_pairs=sum(map(len,groups.values())), geometry_groups=len(groups),
            cluster_bootstrap_95=interval(groups)) for name,groups in grouped.items()}
    (results/'cue_training_interaction.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['build','run','analyze'])
    p.add_argument('--data',type=Path,default=DATA)
    p.add_argument('--results',type=Path,default=RESULTS)
    p.add_argument('--adapter-prefix',default='h1_target_cue')
    args=p.parse_args()
    if args.command=='build':
        build(args.data,args.results)
    elif args.command=='analyze':
        analyze(args.data,args.results)
    else:
        execute(args.data,args.results,args.adapter_prefix)
