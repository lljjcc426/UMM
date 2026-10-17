"""Connect learned reference localization to the existing UMM state questions."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import contextlib
import io
import json
import math
import os
import subprocess
import sys
import time

from PIL import Image, ImageDraw

from h1_run_showo import ROOT, load_model, StateImageEncoder, image_prompt_embeds
from h1_train_state import load_adapter
from h1_target_grid import mask_box, ADAPTER
from h1_target_grid_generalization import make_head, prompt, save, CACHE as TARGET_CACHE
from h1_spatial_probe import CACHE as SPATIAL_CACHE
from h1_target_cue import add_target_box
from h1_state_gate import DEFAULT, read_jsonl, write_jsonl, evaluate, parse
from h1_target_controls import score_different_targets, compare_different_targets
from h1_compare_state_runs import compare

SOURCE = ROOT/'data/h1/state_target_cue_v1/raw/all_targets_dev'
DATA = ROOT/'data/h1/predicted_target_cue_v1'
RESULT = ROOT/'results/h1/showo2_video_1_5b/predicted_target_cue_v1'
OLD = ROOT/'results/h1/showo2_video_1_5b/target_cue_v1/boxed'


def build():
    DATA.mkdir(parents=True, exist_ok=False)
    (DATA/'references').mkdir(); (DATA/'images').mkdir()
    RESULT.mkdir(parents=True, exist_ok=False)
    rows = read_jsonl(SOURCE/'inputs.jsonl')
    queries = {}
    for row in rows:
        ref = DATA/'references'/f'{row["group_id"]}.png'
        if not ref.exists():
            image = Image.open(SOURCE/row['images'][0]).convert('RGB')
            image.paste('white', (0,216,432,432))
            image.save(ref)
        key = (row['group_id'], row['target'])
        queries[key] = dict(group_id=row['group_id'], target=row['target'],
                           image=str(ref.relative_to(ROOT)), prompt=prompt(row['target']))
    save(DATA/'localization_inputs.json', list(queries.values()))
    save(RESULT/'plan.json', dict(created_utc=datetime.now(timezone.utc).isoformat(),
        role='Exploratory connection check on previously inspected state development cases, after expanded-geometry and mask-intersection diagnostics; not independent acceptance.',
        state_questions=len(rows), state_geometries=3, reference_targets=len(queries),
        localizer='Full frozen Show-o2 with original state adapter, expanded target head and old all-ink head; .5 masks intersected, same largest-component box.',
        localization_input='Only reference upper half plus a blank lower half and target question; no coordinate or state label.',
        state_adapter=str(ADAPTER.relative_to(ROOT)),
        state_cue='Predicted box plus the existing 12px margin in reference and current panels, only white pixels painted; no current-state-dependent adjustment.',
        controls='Reuse saved no-box and correct-reference-box results from the same state adapter, prompts and state IDs; no retraining.',
        interpretation='Measure downstream sensitivity to predicted positions despite imperfect geometry localization. Formatting remains guaranteed by the existing answer trie.',
        caveat='Only three repeatedly inspected geometries; results do not establish unseen-state, character, font or temporal generalization.'))


def locate():
    import torch
    start=time.perf_counter()
    model,tok,ids=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','mps')
    load_adapter(model,ADAPTER,'mps');model.eval().requires_grad_(False)
    encoder=StateImageEncoder(model,ROOT/'checkpoints/Show-o-assets','mps')
    from models import omni_attn_mask_naive
    target=torch.load(TARGET_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    ink=torch.load(SPATIAL_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    head=make_head().eval();head.load_state_dict(target['state_dict'])
    ink_head=torch.nn.Linear(1536,1).eval();ink_head.load_state_dict(ink['state_dict'])
    predictions=[]
    with torch.inference_mode():
        for row in json.loads((DATA/'localization_inputs.json').read_text()):
            visual=encoder.encode(ROOT/row['image'])
            emb,mods=image_prompt_embeds(model,tok,ids,row['prompt'],visual,'mps')
            mask=omni_attn_mask_naive(B=1,LEN=emb.shape[1],modalities=mods,device='mps',inverted=True).to(emb.dtype)
            hidden=model.showo.model(inputs_embeds=emb,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state[0,-1].cpu().float()
            v=visual[0].cpu().float()
            vproj=head.v((v-target['vmean'])/target['vstd'])
            query=head.q((hidden-target['qmean'])/target['qstd'])
            selected=(vproj*query).sum(-1)/math.sqrt(32)+head.bias>=0
            foreground=ink_head((v-ink['mean'])/ink['std']).squeeze(-1)>=0
            gated=(selected&foreground).numpy()
            predictions.append(dict(**row,predicted_box=mask_box(gated),predicted_ink_cells=gated.nonzero()[0].tolist()))
    save(RESULT/'localizations.json',predictions)
    lookup={(r['group_id'],r['target']):r for r in predictions}
    rows=read_jsonl(SOURCE/'inputs.jsonl')
    for row in rows:
        image=Image.open(SOURCE/row['images'][0]).convert('RGB')
        box=lookup[(row['group_id'],row['target'])]['predicted_box']
        if box is not None: image=add_target_box(image,[(box[0],box[1]),(box[2],box[3])])
        path=DATA/'images'/f'{row["case_id"]}.png'
        if not path.exists(): image.save(path)
        row['images']=[str(path.relative_to(DATA))]
        row['cue_condition']='predicted_reference_box'
    write_jsonl(DATA/'inputs.jsonl',rows)
    # Labels are first opened after all localization and cue generation finishes.
    write_jsonl(DATA/'labels.jsonl',read_jsonl(SOURCE/'labels.jsonl'))
    scenes={r['case_id']:r for r in json.loads((DEFAULT/'cases.json').read_text())}
    examples={(r['group_id'],r['target']):r for r in rows}
    scored=[]
    for r in predictions:
        example=examples[(r['group_id'],r['target'])]
        points=scenes[example['scene_id']]['strokes'][r['target']]
        xs,ys=zip(*points);expected=[min(xs),min(ys),max(xs),max(ys)]
        box=r['predicted_box']
        scored.append(dict(group_id=r['group_id'],target=r['target'],predicted_box=box,expected_box=expected,
            within_12px=box is not None and max(abs(a-b) for a,b in zip(box,expected))<=12))
    save(RESULT/'localization_score.json',dict(targets=len(scored),hits=sum(r['within_12px'] for r in scored),
        seconds=time.perf_counter()-start,cases=scored))


def run_state():
    subprocess.run([sys.executable,str(ROOT/'scripts/h1_run_showo.py'),'--device','mps',
        '--inputs',str(DATA/'inputs.jsonl'),'--split','dev','--view','reference_current','--format','json',
        '--constrain-answers','--adapter',str(ADAPTER),'--output',str(RESULT/'state_dev')],
        cwd=ROOT,env=dict(os.environ,PYTORCH_ENABLE_MPS_FALLBACK='1'),check=True)
    score()


def score():
    run=RESULT/'state_dev'
    with contextlib.redirect_stdout(io.StringIO()):
        evaluate(DATA,run/'predictions.jsonl','dev','json',run/'score','reference_current')
        pairs=score_different_targets(DATA,run,run/'score/different_target_pairs.json')
        for name,old in [('no_box',OLD/'targets_raw_dev'),('correct_box',OLD/'targets_boxed_dev')]:
            compare(DATA,old,run,RESULT/f'vs_{name}.json','reference_current','dev')
            compare_different_targets(DATA,old,run,RESULT/f'pairs_vs_{name}.json')
    print(json.dumps(pairs['metrics'],ensure_ascii=False,indent=2))


def diagnose():
    inputs=read_jsonl(DATA/'inputs.jsonl')
    labels={r['sample_id']:r for r in read_jsonl(DATA/'labels.jsonl')}
    predictions={r['sample_id']:r for r in read_jsonl(RESULT/'state_dev/predictions.jsonl')}
    previous={r['sample_id']:r for r in read_jsonl(OLD/'targets_boxed_dev/predictions.jsonl')}
    locations={(r['group_id'],r['target']):r for r in json.loads((RESULT/'localization_score.json').read_text())['cases']}
    errors=[];regressions=repairs=0
    for row in inputs:
        if row['task']!='completion':continue
        label=labels[row['sample_id']]
        actual=parse(predictions[row['sample_id']]['raw_response'],'json',label['allowed'])
        before=parse(previous[row['sample_id']]['raw_response'],'json',label['allowed'])
        if actual!=label['expected']:
            errors.append(dict(sample_id=row['sample_id'],scene_id=row['scene_id'],target=row['target'],
                expected=label['expected'],predicted=actual,correct_box_answer=before,
                localization_within_12px=locations[(row['group_id'],row['target'])]['within_12px']))
        regressions+=int(actual!=label['expected'] and before==label['expected'])
        repairs+=int(actual==label['expected'] and before!=label['expected'])
    report=dict(role='Post-hoc scoring diagnosis; state failures grouped by reference localization tolerance, not used to modify predictions.',
        completion_errors=len(errors),errors_within_localization_tolerance=sum(r['localization_within_12px'] for r in errors),
        regressions_vs_correct_box=regressions,repairs_vs_correct_box=repairs,cases=errors)
    save(RESULT/'state_error_analysis.json',report)
    # First regression in each layout, explicitly an error illustration.
    directories=[SOURCE,SOURCE.parent.parent/'boxed/all_targets_dev',DATA]
    indexed=[{r['sample_id']:r for r in read_jsonl(d/'inputs.jsonl')} for d in directories]
    selected=[next(r for r in errors if kind in r['sample_id'] and r['correct_box_answer']==r['expected'])
              for kind in ('parallel_h','parallel_v','cross')]
    panel=Image.new('RGB',(3*222,3*242),'white');draw=ImageDraw.Draw(panel)
    for i,row in enumerate(selected):
        for j,(name,directory,source) in enumerate(zip(['No cue','Correct reference cue','Predicted cue'],directories,indexed)):
            image=Image.open(directory/source[row['sample_id']]['images'][0]).convert('RGB').resize((216,216))
            panel.paste(image,(j*222,i*242+22));draw.text((j*222,i*242+4),name,fill='black')
    panel.save(RESULT/'state_examples.png')
    print({k:v for k,v in report.items() if k!='cases'})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','locate','run-state','score','diagnose'])
    parser.add_argument('--data',type=Path,default=DATA)
    parser.add_argument('--output',type=Path,default=RESULT)
    parser.add_argument('--target-cache',type=Path,default=TARGET_CACHE)
    args=parser.parse_args()
    DATA,RESULT,TARGET_CACHE=args.data.resolve(),args.output.resolve(),args.target_cache.resolve()
    {'build':build,'locate':locate,'run-state':run_state,'score':score,'diagnose':diagnose}[args.command]()
