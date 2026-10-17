"""Broader geometry supervision for the frozen UMM's target spatial readout."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import math
import random
import time

import numpy as np
from PIL import Image, ImageDraw

from h1_run_showo import ROOT, load_model, StateImageEncoder, image_prompt_embeds, MODEL_REVISION, SOURCE_REVISION
from h1_train_state import load_adapter
from h1_target_grid import mask_box, ADAPTER, CACHE as OLD_CACHE
from h1_spatial_probe import metrics, CACHE as SPATIAL_CACHE
from h1_state_gate import interval

DATA = ROOT / 'data/h1/target_grid_generalization_v1'
RESULT = ROOT / 'results/h1/showo2_video_1_5b/target_grid_generalization_v1'
CACHE = ROOT / 'checkpoints/h1_target_grid_generalization_v1'
KINDS = ('parallel_h', 'parallel_v', 'cross')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def prompt(target):
    return f'上半部是完整线条参考，下半部为空白。请只定位{target}，不要选择其他线条。'


def geometry(rng, kind):
    if kind == 'parallel_h':
        while True:
            ys = sorted(rng.sample(range(24, 197), 3))
            if min(b-a for a, b in zip(ys, ys[1:])) >= 24:
                break
        strokes = {}
        for name, y in zip(('上横', '中横', '下横'), ys):
            x = rng.randint(24, 260)
            strokes[name] = [x, y, x + rng.randint(60, min(330, 408-x)), y]
    elif kind == 'parallel_v':
        while True:
            xs = sorted(rng.sample(range(40, 393), 2))
            if xs[1]-xs[0] >= 40:
                break
        strokes = {name: [x, rng.randint(20, 95), x, rng.randint(125, 202)]
                   for name, x in zip(('左竖', '右竖'), xs)}
    else:
        x, y = rng.randint(80, 350), rng.randint(60, 160)
        strokes = {'横线': [rng.randint(24, x-24), y, rng.randint(x+24, 408), y],
                   '竖线': [x, rng.randint(20, y-24), x, rng.randint(y+24, 202)]}
    return strokes


def grid(row):
    im = Image.new('L', (432, 432), 255)
    x0, y0, x1, y1 = row['expected_box']
    ImageDraw.Draw(im).line([(x0, y0), (x1, y1)], fill=0, width=row['line_width'])
    return ((np.asarray(im) < 128).reshape(27, 16, 27, 16).sum(axis=(1, 3)) >= 8).reshape(-1)


def build():
    DATA.mkdir(parents=True, exist_ok=False)
    (DATA/'images').mkdir()
    RESULT.mkdir(parents=True, exist_ok=False)
    CACHE.mkdir(parents=True, exist_ok=False)
    rows, images = [], []
    for split, count, seed in [('train', 48, 10421), ('dev', 16, 10422)]:
        rng = random.Random(seed)
        for kind in KINDS:
            for number in range(count):
                strokes = geometry(rng, kind)
                width = rng.choice([3, 5, 7, 9])
                gid = f'grid-{split}-{kind}-{number:03}'
                path = DATA/'images'/f'{gid}.png'
                im = Image.new('RGB', (432, 432), 'white')
                draw = ImageDraw.Draw(im)
                for x0, y0, x1, y1 in strokes.values():
                    draw.line([(x0, y0), (x1, y1)], fill='black', width=width)
                im.save(path)
                image = dict(group_id=gid, split=split, kind=kind, image=str(path.relative_to(ROOT)))
                images.append(image)
                for target, box in strokes.items():
                    rows.append(dict(**image, sample_id=f'{gid}-{target}', target=target,
                                     expected_box=box, line_width=width))
    save(DATA/'cases.json', rows)
    save(DATA/'images.json', images)
    save(RESULT/'inputs.json', [dict(sample_id=r['sample_id'], group_id=r['group_id'], split=r['split'],
         image=r['image'], prompt=prompt(r['target'])) for r in rows])
    plan = dict(created_utc=datetime.now(timezone.utc).isoformat(),
        role='Prospective geometry development diagnostic; no Chinese, style or temporal acceptance.',
        model='showlab/show-o2-1.5B-w-video-und', model_revision=MODEL_REVISION, source_revision=SOURCE_REVISION,
        adapter=str(ADAPTER.relative_to(ROOT)), data=str(DATA.relative_to(ROOT)),
        train_groups=144, train_targets=336, dev_groups=48, dev_targets=112,
        split='Independent seeds 10421/10422, split by entire geometry; all questions of an image stay together.',
        variations='Independent horizontal spans, vertical extents, relative spacing, off-center crossings; width 3/5/7/9. Same simple renderer and target words.',
        model_input='Only the complete reference image and target question. No boxes, masks, current-state image, completion labels or coordinates.',
        head='Same 98,369-parameter 32-dimensional bilinear head; frozen complete UMM and original state adapter.',
        normalization='Visual mean/std reused from old training-only occupancy probe. Question mean/std from the 336 new training queries only.',
        optimization=dict(steps=1000, batch='All 336 training targets per update', lr=.0003,
            weight_decay=.01, optimizer='AdamW', seed=10420, loss='BCE, pos_weight = train negative / positive grid cells'),
        decoding='Fixed .5 threshold; largest four-connected component; extreme cell centers; four coordinate errors <=12px.',
        controls=['Previous final target head evaluated unchanged on the same new cases',
                  'New head with cyclically swapped questions within each image',
                  'Previous all-ink linear head with same component decoder'],
        evaluation='Final checkpoint only; no development-dependent threshold or checkpoint selection. Geometry-cluster bootstrap intervals.',
        caveat='More data and four times as many target presentations as the old 84-target full-batch run; not a fixed-compute data-coverage ablation.',
        next='If target localization remains below 90%, diagnose masks and target selection before any sequence learning. Do not count this as full H1.')
    save(RESULT/'plan.json', plan)
    save(DATA/'plan.json', plan)
    upper = {}
    for split in ('train', 'dev'):
        selected = [r for r in rows if r['split'] == split]
        hits = sum(max(abs(a-b) for a,b in zip(mask_box(grid(r)), r['expected_box'])) <= 12 for r in selected)
        upper[split] = dict(targets=len(selected), oracle_grid_hits=hits)
    save(RESULT/'grid_upper_bound.json', dict(role='Annotation-derived discretization check, not a model score', splits=upper))
    print(dict(groups=len(images), targets=len(rows), grid_upper_bound=upper))


def extract_vision():
    import torch
    start = time.perf_counter()
    assets = ROOT/'checkpoints/Show-o-assets'
    model, _, _ = load_model(ROOT/'checkpoints/Show-o-source', ROOT/'checkpoints/Show-o2-1.5B-video', assets, 'cpu')
    encoder = StateImageEncoder(model, assets, 'mps')
    rows = json.loads((DATA/'images.json').read_text())
    values = []
    with (CACHE/'extraction_progress.jsonl').open('a') as log:
        for i, row in enumerate(rows):
            values.append(encoder.encode(ROOT/row['image']).squeeze(0).cpu())
            if (i+1) % 12 == 0:
                log.write(json.dumps(dict(stage='vision', completed=i+1, seconds=time.perf_counter()-start))+'\n')
                log.flush()
    features = torch.stack(values)
    torch.save(dict(features=features), CACHE/'features.pt')
    save(RESULT/'visual_extraction.json', dict(seconds=time.perf_counter()-start, shape=list(features.shape),
         full_model_parameters=sum(p.numel() for p in model.parameters()), umm_updated_parameters=0,
         device='Wan VAE CPU fp32; visual modules MPS bf16; language retained CPU'))


def extract_questions():
    import torch
    start = time.perf_counter()
    model, tok, ids = load_model(ROOT/'checkpoints/Show-o-source', ROOT/'checkpoints/Show-o2-1.5B-video',
                                ROOT/'checkpoints/Show-o-assets', 'mps')
    load_adapter(model, ADAPTER, 'mps')
    model.eval().requires_grad_(False)
    model.time_embed.to('mps'); model.time_embed_proj.to('mps')
    from models import omni_attn_mask_naive
    images = json.loads((DATA/'images.json').read_text())
    index = {r['image']: i for i,r in enumerate(images)}
    rows = json.loads((RESULT/'inputs.json').read_text())
    features = torch.load(CACHE/'features.pt', map_location='cpu', weights_only=True)['features']
    hidden = []
    with torch.inference_mode(), (CACHE/'extraction_progress.jsonl').open('a') as log:
        for i, row in enumerate(rows):
            emb, mods = image_prompt_embeds(model, tok, ids, row['prompt'], features[index[row['image']]][None].to('mps'), 'mps')
            mask = omni_attn_mask_naive(B=1, LEN=emb.shape[1], modalities=mods, device='mps', inverted=True).to(emb.dtype)
            output = model.showo.model(inputs_embeds=emb, attention_mask=mask, use_cache=False, return_dict=True)
            hidden.append(output.last_hidden_state[0,-1].cpu())
            if (i+1) % 28 == 0:
                log.write(json.dumps(dict(stage='question', completed=i+1, seconds=time.perf_counter()-start))+'\n')
                log.flush()
    torch.save(dict(hidden=torch.stack(hidden), image_indices=[index[r['image']] for r in rows]), CACHE/'questions.pt')
    save(RESULT/'question_extraction.json', dict(seconds=time.perf_counter()-start, shape=list(torch.stack(hidden).shape),
         full_model_parameters=sum(p.numel() for p in model.parameters()), umm_updated_parameters=0))


def make_head():
    import torch
    class Readout(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.v = torch.nn.Linear(1536, 32)
            self.q = torch.nn.Linear(1536, 32)
            self.bias = torch.nn.Parameter(torch.zeros(()))
        def forward(self, visual, question, indices):
            return (self.v(visual)[indices] * self.q(question)[:,None]).sum(-1)/math.sqrt(32) + self.bias
    return Readout()


def fit():
    import torch
    import torch.nn.functional as F
    rows = json.loads((DATA/'cases.json').read_text())
    images = json.loads((DATA/'images.json').read_text())
    ti = [i for i,r in enumerate(rows) if r['split']=='train']
    vi = [i for i,r in enumerate(images) if r['split']=='train']
    spatial = torch.load(CACHE/'features.pt', map_location='cpu', weights_only=True)['features']
    params = torch.load(SPATIAL_CACHE/'readout.pt', map_location='cpu', weights_only=True)
    question = torch.load(CACHE/'questions.pt', map_location='cpu', weights_only=True)
    q = question['hidden'][ti].float()
    qm, qs = q.mean(0), q.std(0).clamp_min(1e-6)
    q = ((q-qm)/qs).to('mps')
    visual = ((spatial[vi].float()-params['mean'])/params['std']).to('mps')
    # Training images occupy the first contiguous block, matching image_indices.
    indices = torch.tensor([question['image_indices'][i] for i in ti], device='mps')
    truth = np.stack([grid(rows[i]) for i in ti])
    labels = torch.tensor(truth, dtype=torch.float32, device='mps')
    weight = (1-labels).sum()/labels.sum()
    torch.manual_seed(10420)
    head = make_head().to('mps')
    opt = torch.optim.AdamW(head.parameters(), lr=.0003, weight_decay=.01)
    start = time.perf_counter()
    with (RESULT/'training.jsonl').open('w') as log:
        for step in range(1000):
            loss = F.binary_cross_entropy_with_logits(head(visual, q, indices), labels, pos_weight=weight)
            opt.zero_grad(); loss.backward(); opt.step()
            if (step+1) % 25 == 0:
                log.write(json.dumps(dict(step=step+1, loss=float(loss.detach())))+'\n'); log.flush()
    torch.mps.synchronize()
    torch.save(dict(state_dict={k:v.cpu() for k,v in head.state_dict().items()}, qmean=qm, qstd=qs,
                    vmean=params['mean'], vstd=params['std']), CACHE/'readout.pt')
    save(RESULT/'training_summary.json', dict(seconds=time.perf_counter()-start,
        parameters=sum(p.numel() for p in head.parameters()), umm_updated_parameters=0, positive_weight=float(weight)))


def evaluate():
    import torch
    rows = json.loads((DATA/'cases.json').read_text())
    visual = torch.load(CACHE/'features.pt', map_location='cpu', weights_only=True)['features']
    questions = torch.load(CACHE/'questions.pt', map_location='cpu', weights_only=True)
    q = questions['hidden'].float()
    image_indices = questions['image_indices']
    groups = defaultdict(list)
    for i,r in enumerate(rows): groups[r['group_id']].append(i)
    swap = list(range(len(rows)))
    for group in groups.values():
        for a,b in zip(group, group[1:]+group[:1]): swap[a]=b
    predictions = {}
    with torch.no_grad():
        for name, path in [('expanded_training',CACHE/'readout.pt'), ('previous_head',OLD_CACHE/'readout_fit.pt')]:
            params = torch.load(path, map_location='cpu', weights_only=True)
            head = make_head().eval()
            head.load_state_dict(params['state_dict'])
            v = torch.cat([head.v((batch.float()-params['vmean'])/params['vstd']) for batch in visual.split(8)])
            query = head.q((q-params['qmean'])/params['qstd'])
            def infer(qvalues):
                return (((v[image_indices]*qvalues[:,None]).sum(-1)/math.sqrt(32)+head.bias)>=0).numpy()
            predictions[name] = infer(query)
            if name=='expanded_training': predictions['swapped_question']=infer(query[swap])
        params = torch.load(SPATIAL_CACHE/'readout.pt', map_location='cpu', weights_only=True)
        head = torch.nn.Linear(1536,1).eval(); head.load_state_dict(params['state_dict'])
        ink = torch.cat([head((batch.float()-params['mean'])/params['std']).squeeze(-1) for batch in visual.split(8)])>=0
        predictions['all_ink'] = ink[image_indices].numpy()
    truth = np.stack([grid(r) for r in rows])
    records, summary = [], {}
    for condition, masks in predictions.items():
        for split in ('train','dev'):
            selected = []
            for i,r in enumerate(rows):
                if r['split']!=split: continue
                box = mask_box(masks[i])
                errors = [abs(a-b) for a,b in zip(box,r['expected_box'])] if box else None
                row = dict(**r, condition=condition, **metrics(masks[i],truth[i]), predicted_box=box,
                    coordinate_errors=errors, within_12px=box is not None and max(errors)<=12,
                    predicted_ink_cells=np.flatnonzero(masks[i]).tolist(), truth_ink_cells=np.flatnonzero(truth[i]).tolist())
                records.append(row); selected.append(row)
            group_values=defaultdict(list)
            for r in selected: group_values[r['group_id']].append(int(r['within_12px']))
            summary[f'{condition}/{split}'] = dict(targets=len(selected), groups=len(group_values),
                hits=sum(r['within_12px'] for r in selected), macro_iou=np.mean([r['iou'] for r in selected]),
                macro_f1=np.mean([r['f1'] for r in selected]), hit_cluster_bootstrap_95=interval(group_values),
                by_kind={kind:dict(targets=sum(r['kind']==kind for r in selected),
                                  hits=sum(r['kind']==kind and r['within_12px'] for r in selected)) for kind in KINDS})
    comparisons = {}
    primary=[r for r in records if r['condition']=='expanded_training' and r['split']=='dev']
    for control in ('previous_head','swapped_question','all_ink'):
        other={r['sample_id']:r for r in records if r['condition']==control and r['split']=='dev'}
        differences=defaultdict(list)
        for r in primary: differences[r['group_id']].append(int(r['within_12px'])-int(other[r['sample_id']]['within_12px']))
        comparisons[control]=dict(hit_difference=sum(map(sum,differences.values()))/len(primary),
                                 paired_cluster_bootstrap_95=interval(differences))
    # Scoring-only diagnosis: annotation masks never enter the prediction path.
    diagnosis = {}
    for split in ('train','dev'):
        counts = dict(targets=0, correct_instance_overlap=0, wrong_instance_overlap=0,
                      overlap_tie=0, correct_instance_but_bad_boundary=0, union_boundary_hits=0)
        for i,r in enumerate(rows):
            if r['split'] != split: continue
            mask = predictions['expanded_training'][i]
            actual = metrics(mask,truth[i])['iou']
            other = max(metrics(mask,truth[j])['iou'] for j in groups[r['group_id']] if j!=i)
            box = mask_box(mask)
            hit = box is not None and max(abs(a-b) for a,b in zip(box,r['expected_box']))<=12
            counts['targets'] += 1
            counts['correct_instance_overlap'] += int(actual>other)
            counts['wrong_instance_overlap'] += int(actual<other)
            counts['overlap_tie'] += int(actual==other)
            counts['correct_instance_but_bad_boundary'] += int(actual>other and not hit)
            ys,xs = np.where(mask.reshape(27,27))
            union = [xs.min()*16+7.5,ys.min()*16+7.5,xs.max()*16+7.5,ys.max()*16+7.5] if len(xs) else None
            counts['union_boundary_hits'] += int(union is not None and max(abs(a-b) for a,b in zip(union,r['expected_box']))<=12)
        diagnosis[split]=counts
    save(RESULT/'score.json', dict(metrics=summary, paired_dev_comparisons=comparisons,
        mask_diagnosis=diagnosis,
        limitation='48 simple-shape development geometries; added trained head; no current-state, Chinese, style or sequence acceptance.'))
    (RESULT/'predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    # Fixed first development target of each layout, selected without scores.
    chosen=[next(i for i,r in enumerate(rows) if r['split']=='dev' and r['kind']==kind) for kind in KINDS]
    panel=Image.new('RGB',(4*222,3*242),'white'); draw=ImageDraw.Draw(panel)
    for row_num,i in enumerate(chosen):
        y=row_num*242
        panel.paste(Image.open(ROOT/rows[i]['image']).resize((216,216)),(0,y+22))
        draw.text((0,y+4),rows[i]['kind'],fill='black')
        for col,(title,mask) in enumerate([('Target truth',truth[i]),('Expanded training',predictions['expanded_training'][i]),
                                         ('Previous head',predictions['previous_head'][i])],1):
            im=Image.fromarray(np.where(mask.reshape(27,27),0,255).astype('uint8')).resize((216,216),Image.Resampling.NEAREST).convert('RGB')
            panel.paste(im,(col*222,y+22)); draw.text((col*222,y+4),title,fill='black')
    panel.save(RESULT/'examples.png')
    print(json.dumps(summary,indent=2))


def diagnose_gate():
    """Post-hoc fixed intersection of two learned masks; no label-based filtering."""
    records = [json.loads(s) for s in (RESULT/'predictions.jsonl').read_text().splitlines()]
    all_ink = {r['sample_id']:set(r['predicted_ink_cells']) for r in records if r['condition']=='all_ink'}
    report = dict(created_utc=datetime.now(timezone.utc).isoformat(),
        role='Exploratory diagnosis after the primary evaluation; unchanged .5 thresholds, no new training or UMM calls.',
        method='Intersect question-conditioned predicted foreground and old all-ink predicted foreground, then use the same largest-component decoder. Scoring labels are never used in the intersection.',
        splits={}, cases=[])
    for split in ('train','dev'):
        selected = [r for r in records if r['condition']=='expanded_training' and r['split']==split]
        cases=[]; values=defaultdict(list); differences=defaultdict(list)
        for row in selected:
            mask=np.zeros(729,dtype=bool)
            keep=sorted(set(row['predicted_ink_cells']) & all_ink[row['sample_id']])
            mask[keep]=True
            truth=np.zeros(729,dtype=bool);truth[row['truth_ink_cells']]=True
            box=mask_box(mask)
            hit=box is not None and max(abs(a-b) for a,b in zip(box,row['expected_box']))<=12
            record=dict(sample_id=row['sample_id'],group_id=row['group_id'],split=split,
                expected_box=row['expected_box'],predicted_box=box,within_12px=hit,
                original_hit=row['within_12px'],predicted_ink_cells=keep,**metrics(mask,truth))
            cases.append(record)
            values[row['group_id']].append(int(hit))
            differences[row['group_id']].append(int(hit)-int(row['within_12px']))
        report['cases'].extend(cases)
        report['splits'][split]=dict(targets=len(cases),hits=sum(r['within_12px'] for r in cases),
            repairs=sum(r['within_12px'] and not r['original_hit'] for r in cases),
            regressions=sum(not r['within_12px'] and r['original_hit'] for r in cases),
            macro_iou=np.mean([r['iou'] for r in cases]),macro_f1=np.mean([r['f1'] for r in cases]),
            hit_cluster_bootstrap_95=interval(values),
            difference=sum(map(sum,differences.values()))/len(cases),paired_cluster_bootstrap_95=interval(differences))
    cases=report.pop('cases')
    report['predictions_file']='gate_predictions.jsonl'
    (RESULT/'gate_predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in cases))
    save(RESULT/'gate_diagnosis.json',report)
    print(json.dumps(report['splits'],indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','extract-vision','extract-questions','fit','evaluate','diagnose-gate'])
    parser.add_argument('--data',type=Path,default=DATA)
    parser.add_argument('--output',type=Path,default=RESULT)
    parser.add_argument('--cache',type=Path,default=CACHE)
    args=parser.parse_args()
    DATA,RESULT,CACHE=args.data.resolve(),args.output.resolve(),args.cache.resolve()
    {'build':build,'extract-vision':extract_vision,'extract-questions':extract_questions,'fit':fit,'evaluate':evaluate,
     'diagnose-gate':diagnose_gate}[args.command]()
