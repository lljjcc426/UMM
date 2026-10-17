"""Compare reference/current UMM spatial features without painting target cues."""
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import math
import os
import random
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

from h1_state_gate import ROOT, prefix, interval, write_jsonl, read_jsonl, parse
from h1_run_showo import load_model, StateImageEncoder, image_prompt_embeds, MODEL_REVISION, SOURCE_REVISION
from h1_target_grid_generalization import geometry, prompt, make_head as make_target_head, CACHE as TARGET_CACHE
from h1_spatial_probe import CACHE as SPATIAL_CACHE
from h1_target_grid import ADAPTER, mask_box
from h1_train_state import load_adapter
from h1_target_cue import add_target_box, CUE

DATA=ROOT/'data/h1/region_state_v1'
RESULT=ROOT/'results/h1/showo2_video_1_5b/region_state_v1'
CACHE=ROOT/'checkpoints/h1_region_state_v1'
CLASSES=['未出现','部分','完整','未知']
KINDS=['parallel_h','parallel_v','cross']


def save(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def render(strokes, fractions, width):
    im=Image.new('RGB',(432,432),'white');draw=ImageDraw.Draw(im)
    for name,points in strokes.items():
        if fractions[name]>0:
            draw.line([tuple(round(c) for c in p) for p in prefix(points,fractions[name])],fill='black',width=width)
    return im


def target_mask(strokes, target, width):
    im=render({target:strokes[target]},{target:1},width)
    return (np.asarray(im).max(-1)<128).reshape(27,16,27,16).sum((1,3)).reshape(-1)>=8


def build():
    DATA.mkdir(parents=True,exist_ok=False);(DATA/'images').mkdir()
    RESULT.mkdir(parents=True,exist_ok=False);CACHE.mkdir(parents=True,exist_ok=False)
    images=[];queries=[];cases=[];signatures={}
    def picture(name, image, split):
        path=DATA/'images'/f'{name}.png';image.save(path)
        images.append(dict(image=str(path.relative_to(ROOT)),split=split));return len(images)-1
    blank=picture('blank',Image.new('RGB',(432,432),'white'),'control')
    def query(gid,split,kind,strokes,width,target,ref):
        idx=len(queries)
        queries.append(dict(query_id=idx,group_id=gid,split=split,kind=kind,target=target,
            reference_index=ref,prompt=prompt(target),strokes=strokes,width=width))
        return idx
    for split,n,seed in [('train',16,10430),('dev',8,10431)]:
        rng=random.Random(seed)
        fractions=[0,.25,.6,1] if split=='train' else [0,.15,.45,.85,1]
        for kind in KINDS:
            for gi in range(n):
                gid=f'region-{split}-{kind}-{gi:02}'
                boxes=geometry(rng,kind);strokes={k:[v[:2],v[2:]] for k,v in boxes.items()}
                width=rng.choice([3,5,7,9]);signature=(tuple((k,tuple(v)) for k,v in boxes.items()),width)
                if signature in signatures:raise ValueError('Repeated full geometry across groups.')
                signatures[signature]=gid
                ref=picture(gid+'-reference',render(strokes,{k:1 for k in strokes},width),split)
                ids={k:query(gid,split,kind,strokes,width,k,ref) for k in strokes}
                for vi in range(len(fractions)):
                    progress={k:fractions[(vi+j)%len(fractions)] for j,k in enumerate(strokes)}
                    cur=picture(f'{gid}-current-{vi}',render(strokes,progress,width),split)
                    for target,qi in ids.items():
                        frac=progress[target]
                        cases.append(dict(sample_id=f'{gid}-{vi}-{target}',group_id=gid,split=split,kind=kind,
                            scene_id=f'{gid}-{vi}',query_index=qi,reference_index=ref,current_index=cur,
                            target=target,fraction=frac,reference_available=True,
                            expected=CLASSES[0 if frac==0 else 2 if frac==1 else 1],reference_pair=None))
        # Same current pixels, two different references and opposite completion states.
        for gi in range(12 if split=='train' else 6):
            gid=f'region-{split}-reference-{gi:02}'
            x=rng.randint(24,85);y=rng.randint(30,190);length=rng.randint(90,145);width=rng.choice([3,5,7,9])
            current={'横线':[[x,y],[x+length,y]]}
            cur=picture(gid+'-current',render(current,{'横线':1},width),split)
            for factor in (1,2):
                strokes={'横线':[[x,y],[x+length*factor,y]]}
                ref=picture(f'{gid}-reference-{factor}',render(strokes,{'横线':1},width),split)
                qi=query(gid,split,'reference_control',strokes,width,'横线',ref)
                cases.append(dict(sample_id=f'{gid}-{factor}',group_id=gid,split=split,kind='reference_control',
                    scene_id=f'{gid}-{factor}',query_index=qi,reference_index=ref,current_index=cur,target='横线',
                    fraction=1/factor,reference_available=True,expected='完整' if factor==1 else '部分',reference_pair=gid))
        # No-reference controls expose no target extent, target mask or hidden reference.
        for gi in range(12 if split=='train' else 6):
            gid=f'region-{split}-unknown-{gi:02}'
            if gi%2:
                x=rng.randint(45,380);strokes={'目标笔迹':[[x,30],[x,rng.randint(140,195)]]}
            else:
                y=rng.randint(30,190);strokes={'目标笔迹':[[45,y],[rng.randint(200,390),y]]}
            width=rng.choice([3,5,7,9])
            for vi,frac in enumerate(fractions):
                cur=picture(f'{gid}-current-{vi}',render(strokes,{'目标笔迹':frac},width),split)
                cases.append(dict(sample_id=f'{gid}-{vi}',group_id=gid,split=split,kind='unknown_control',
                    scene_id=f'{gid}-{vi}',query_index=None,reference_index=blank,current_index=cur,
                    target='目标笔迹',fraction=frac,reference_available=False,
                    expected='未出现' if frac==0 else '未知',reference_pair=None))
    save(DATA/'images.json',images);save(DATA/'queries.json',queries);save(DATA/'cases.json',cases)
    plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),model='showlab/show-o2-1.5B-w-video-und',
        model_revision=MODEL_REVISION,source_revision=SOURCE_REVISION,adapter=str(ADAPTER.relative_to(ROOT)),
        role='Prospective new-state geometry development; no Chinese/font/video or H1 acceptance.',
        counts={s:dict(cases=sum(r['split']==s for r in cases),groups=len({r['group_id'] for r in cases if r['split']==s}),
            kinds=dict(Counter(r['kind'] for r in cases if r['split']==s))) for s in ('train','dev')},
        splits='New geometry seeds 10430/10431. All targets and progress variants of one geometry remain together. Same-current reference pairs remain together.',
        progress=dict(train=[0,.25,.6,1],dev=[0,.15,.45,.85,1]),
        input='Full reference and current images encoded separately in identical top-half coordinates; no colored cues, image cropping or target pixels removed.',
        selection='Oracle target occupancy versus previous frozen UMM question-conditioned target mask intersected with predicted all-ink mask. Fixed .5 thresholds, no dev tuning. No current state enters selection.',
        unknown='Single-target current-only cases use a fixed full upper-region mask, blank reference and reference_available=0; no hidden reference geometry enters the model.',
        readout='Shared 1536->32 GELU projection of aligned reference/current tokens. Masked means of reference/current/absolute difference and masked maximum absolute difference, plus reference-availability flag; 129->64 GELU->4 classifier. Presence derived from four-state output.',
        normalization='Fixed training-only visual mean/std from prior spatial probe.',
        training=dict(arms=['oracle','predicted'],steps=400,batch_size=32,lr=.001,weight_decay=.01,seed=10432,
            optimizer='AdamW',loss='Four-class cross entropy, inverse-frequency weights from this training split only.',
            policy='Same initialization and minibatch order; only target mask differs. Final checkpoints only; no dev checkpoint/threshold search.'),
        controls=['Cross-evaluate both heads with oracle and predicted masks',
            'For predicted-trained head: swap target mask within same reference image, retaining original scoring labels',
            'Replace current tokens with blank-image tokens, retain other inputs; visual dependence diagnostic',
            'Replace reference tokens with blank-image tokens but retain reference-derived mask; not a no-reference test'],
        language_baseline='Original unchanged state adapter on the same dev cases, one wording each for presence/completion; predicted reference box painted on composite image. Compare output states, not parameter-matched training. Unknown cases receive no box or reference.',
        metrics='Case accuracy, presence derived from state, class confusion, near-complete subsets, same-current reference pair success, different-target/different-label pair success; bootstrap by whole geometry. Format consistency is structural.',
        scope='Learned auxiliary head on a complete frozen UMM; original language answers are not overwritten. This does not establish unified training benefits. Original 130-case visual test unused.')
    kept=unique_indices(cases)
    plan['visible_input_deduplication']=dict(declared_before_training=True,
        policy='Deduplicate identical current-only RGB inputs within each split for training and metrics; retain raw rows. The empty no-reference control is also shared across splits and is not novel-geometry evidence.',
        retained_counts={s:sum(cases[i]['split']==s for i in kept) for s in ('train','dev')})
    save(RESULT/'plan.json',plan)
    print(json.dumps(plan['counts'],ensure_ascii=False))


def extract():
    import torch
    start=time.perf_counter();assets=ROOT/'checkpoints/Show-o-assets'
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',assets,'cpu')
    encoder=StateImageEncoder(model,assets,'mps');features=[]
    with (CACHE/'progress.jsonl').open('w') as log:
        for i,row in enumerate(json.loads((DATA/'images.json').read_text())):
            features.append(encoder.encode(ROOT/row['image']).squeeze(0).cpu())
            encoder.cache.clear()
            if (i+1)%12==0:
                log.write(json.dumps(dict(stage='vision',completed=i+1,seconds=time.perf_counter()-start))+'\n');log.flush()
    features=torch.stack(features);torch.save(dict(features=features),CACHE/'features.pt')
    save(RESULT/'extraction.json',dict(seconds=time.perf_counter()-start,shape=list(features.shape),
        full_model_parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0,
        path='Frozen native Wan VAE CPU fp32 and fused semantic/generative visual path MPS bf16; full language model retained CPU.'))


def locate():
    import torch
    start=time.perf_counter()
    features=torch.load(CACHE/'features.pt',map_location='cpu',weights_only=True)['features']
    queries=json.loads((DATA/'queries.json').read_text())
    model,tok,ids=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','mps')
    load_adapter(model,ADAPTER,'mps');model.eval().requires_grad_(False)
    model.time_embed.to('mps');model.time_embed_proj.to('mps')
    from models import omni_attn_mask_naive
    target=torch.load(TARGET_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    ink=torch.load(SPATIAL_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    head=make_target_head().eval();head.load_state_dict(target['state_dict'])
    ink_head=torch.nn.Linear(1536,1).eval();ink_head.load_state_dict(ink['state_dict'])
    records=[];masks=[];truth=[]
    with torch.inference_mode(),(CACHE/'progress.jsonl').open('a') as log:
        for i,row in enumerate(queries):
            visual=features[row['reference_index']]
            emb,mods=image_prompt_embeds(model,tok,ids,row['prompt'],visual[None].to('mps'),'mps')
            attn=omni_attn_mask_naive(B=1,LEN=emb.shape[1],modalities=mods,device='mps',inverted=True).to(emb.dtype)
            hidden=model.showo.model(inputs_embeds=emb,attention_mask=attn,use_cache=False,return_dict=True).last_hidden_state[0,-1].cpu().float()
            v=visual.float();selected=(head.v((v-target['vmean'])/target['vstd'])*head.q((hidden-target['qmean'])/target['qstd'])).sum(-1)/math.sqrt(32)+head.bias>=0
            foreground=ink_head((v-ink['mean'])/ink['std']).squeeze(-1)>=0
            mask=(selected&foreground).numpy();masks.append(mask)
            gold=target_mask(row['strokes'],row['target'],row['width']);truth.append(gold)
            box=mask_box(mask);points=row['strokes'][row['target']];xs,ys=zip(*points)
            expected=[min(xs),min(ys),max(xs),max(ys)]
            records.append(dict(query_id=i,group_id=row['group_id'],split=row['split'],kind=row['kind'],target=row['target'],
                predicted_box=box,expected_box=expected,within_12px=box is not None and max(abs(a-b) for a,b in zip(box,expected))<=12,
                predicted_cells=np.flatnonzero(mask).tolist(),oracle_cells=np.flatnonzero(gold).tolist()))
            if (i+1)%28==0:
                log.write(json.dumps(dict(stage='localization',completed=i+1,seconds=time.perf_counter()-start))+'\n');log.flush()
    torch.save(dict(predicted=torch.tensor(np.stack(masks)),oracle=torch.tensor(np.stack(truth))),CACHE/'masks.pt')
    save(RESULT/'localizations.json',records)
    save(RESULT/'localization_summary.json',dict(seconds=time.perf_counter()-start,
        counts={s:dict(n=sum(r['split']==s for r in records),hits=sum(r['split']==s and r['within_12px'] for r in records)) for s in ('train','dev')}))
    draw_examples()


def draw_examples():
    cases=json.loads((DATA/'cases.json').read_text());images=json.loads((DATA/'images.json').read_text())
    locations=json.loads((RESULT/'localizations.json').read_text())
    chosen=[next(r for r in cases if r['split']=='dev' and r['kind']==kind and r['fraction']==.85) for kind in KINDS]
    chosen.append(next(r for r in cases if r['split']=='dev' and r['kind']=='reference_control' and r['fraction']==.5))
    canvas=Image.new('RGB',(4*330,len(chosen)*188),'white');draw=ImageDraw.Draw(canvas)
    for y,row in enumerate(chosen):
        pictures=[Image.open(ROOT/images[row[k]]['image']).convert('RGB') for k in ('reference_index','current_index')]
        loc=locations[row['query_index']]
        for key in ('oracle_cells','predicted_cells'):
            grid=np.full(729,255,dtype=np.uint8);grid[loc[key]]=0
            pictures.append(Image.fromarray(grid.reshape(27,27)).resize((432,432),Image.Resampling.NEAREST).convert('RGB'))
        for x,(title,picture) in enumerate(zip(['Reference','Current','Oracle target','UMM target'],pictures)):
            canvas.paste(picture.crop((0,0,432,216)).resize((324,162)),(x*330,y*188+22))
            draw.text((x*330,y*188+4),f'{title}: {row["kind"]}',fill='black')
    canvas.save(RESULT/'examples.png')


def make_state_head():
    import torch
    class RegionState(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.projection=torch.nn.Sequential(torch.nn.Linear(1536,32),torch.nn.GELU())
            self.classifier=torch.nn.Sequential(torch.nn.Linear(129,64),torch.nn.GELU(),torch.nn.Linear(64,4))
        def forward(self,reference,current,mask,available):
            r=self.projection(reference);c=self.projection(current);d=(r-c).abs()
            weights=mask.float().unsqueeze(-1);denom=weights.sum(1).clamp_min(1)
            means=[(value*weights).sum(1)/denom for value in (r,c,d)]
            maximum=d.masked_fill(~mask.unsqueeze(-1),0).amax(1)
            return self.classifier(torch.cat([*means,maximum,available[:,None]],dim=-1))
    return RegionState()


def prepared():
    import torch
    rows=json.loads((DATA/'cases.json').read_text())
    cache=torch.load(CACHE/'features.pt',map_location='cpu',weights_only=True)
    params=torch.load(SPATIAL_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    features=((cache['features'].float()-params['mean'])/params['std']).to('mps')
    masks=torch.load(CACHE/'masks.pt',map_location='cpu',weights_only=True)
    upper=torch.zeros(729,dtype=torch.bool);upper[:14*27]=True
    mask_by_arm={arm:torch.stack([masks[arm][r['query_index']] if r['reference_available'] else upper for r in rows]).to('mps') for arm in ('oracle','predicted')}
    return rows,features,mask_by_arm


def unique_indices(rows):
    # Current-only empty canvases repeat across nominal geometries. Count and
    # train on each visible current-only input once per split, without hashing.
    images=json.loads((DATA/'images.json').read_text());seen=set();retained=[]
    for i,r in enumerate(rows):
        if not r['reference_available']:
            pixels=Image.open(ROOT/images[r['current_index']]['image']).convert('RGB').tobytes()
            key=(r['split'],pixels)
            if key in seen:continue
            seen.add(key)
        retained.append(i)
    return retained


def train():
    import torch
    import torch.nn.functional as F
    rows,features,masks=prepared()
    retained=unique_indices(rows)
    indices=torch.tensor([i for i in retained if rows[i]['split']=='train'])
    ref=torch.tensor([r['reference_index'] for r in rows],device='mps')
    cur=torch.tensor([r['current_index'] for r in rows],device='mps')
    available=torch.tensor([float(r['reference_available']) for r in rows],device='mps')
    labels=torch.tensor([CLASSES.index(r['expected']) for r in rows],device='mps')
    counts=torch.tensor([sum(rows[i]['expected']==c for i in indices.tolist()) for c in CLASSES],dtype=torch.float32,device='mps')
    weight=counts.sum()/(4*counts)
    for arm in ('oracle','predicted'):
        torch.manual_seed(10432);generator=torch.Generator().manual_seed(10432)
        head=make_state_head().to('mps');opt=torch.optim.AdamW(head.parameters(),lr=.001,weight_decay=.01)
        start=time.perf_counter()
        with (RESULT/f'{arm}_training.jsonl').open('w') as log:
            for step in range(400):
                batch=indices[torch.randint(len(indices),(32,),generator=generator)].to('mps')
                logits=head(features[ref[batch]],features[cur[batch]],masks[arm][batch],available[batch])
                loss=F.cross_entropy(logits,labels[batch],weight=weight)
                opt.zero_grad();loss.backward();opt.step()
                if (step+1)%25==0:
                    log.write(json.dumps(dict(step=step+1,loss=float(loss.detach())))+'\n');log.flush()
        torch.mps.synchronize()
        torch.save(dict(state_dict={k:v.cpu() for k,v in head.state_dict().items()}),CACHE/f'{arm}_head.pt')
        save(RESULT/f'{arm}_training.json',dict(seconds=time.perf_counter()-start,steps=400,
            train_cases=len(indices),trainable_parameters=sum(p.numel() for p in head.parameters()),umm_updated_parameters=0,
            class_counts=counts.cpu().tolist(),class_weights=weight.cpu().tolist()))


def summarize_predictions(records):
    summary={}
    original_rows=json.loads((DATA/'cases.json').read_text())
    retained={original_rows[i]['sample_id'] for i in unique_indices(original_rows)}
    for condition in sorted({r['condition'] for r in records}):
        for split in ('train','dev'):
            selected=[r for r in records if r['condition']==condition and r['split']==split and r['sample_id'] in retained]
            if not selected:continue
            report={}
            for name,subset in [('all',selected),('reference',[r for r in selected if r['reference_available']]),
                                ('unknown',[r for r in selected if not r['reference_available']])]:
                groups=defaultdict(list);pg=defaultdict(list)
                for r in subset:groups[r['group_id']].append(int(r['correct']));pg[r['group_id']].append(int(r['presence_correct']))
                report[name]=dict(n=len(subset),groups=len(groups),completion=sum(r['correct'] for r in subset),
                    presence=sum(r['presence_correct'] for r in subset),completion_ci95=interval(groups),presence_ci95=interval(pg))
            report['classes']={c:dict(n=sum(r['expected']==c for r in selected),correct=sum(r['expected']==c and r['correct'] for r in selected)) for c in CLASSES}
            report['by_fraction']={str(f):dict(n=sum(r['fraction']==f for r in selected),correct=sum(r['fraction']==f and r['correct'] for r in selected)) for f in sorted({r['fraction'] for r in selected})}
            report['confusion']={c:dict(Counter(r['answer'] for r in selected if r['expected']==c)) for c in CLASSES}
            report['by_kind']={kind:dict(n=sum(r['kind']==kind for r in selected),completion=sum(r['kind']==kind and r['correct'] for r in selected),
                presence=sum(r['kind']==kind and r['presence_correct'] for r in selected)) for kind in sorted({r['kind'] for r in selected})}
            report['reference_by_fraction']={str(f):dict(n=sum(r['fraction']==f and r['reference_available'] for r in selected),
                correct=sum(r['fraction']==f and r['reference_available'] and r['correct'] for r in selected))
                for f in sorted({r['fraction'] for r in selected if r['reference_available']})}
            pairs=defaultdict(list);scenes=defaultdict(list)
            for r in selected:
                if r['reference_pair']:pairs[r['reference_pair']].append(r)
                if r['kind'] in KINDS:scenes[r['scene_id']].append(r)
            report['same_current_reference_pairs']=dict(n=len(pairs),both_correct=sum(all(r['correct'] for r in p) for p in pairs.values()))
            target_pairs=[];pair_groups=defaultdict(list)
            for scene in scenes.values():
                for i,a in enumerate(scene):
                    for b in scene[i+1:]:
                        if a['expected']!=b['expected']:
                            success=int(a['correct'] and b['correct']);target_pairs.append(success);pair_groups[a['group_id']].append(success)
            report['different_target_pairs']=dict(n=len(target_pairs),correct=sum(target_pairs),ci95=interval(pair_groups))
            summary[f'{condition}/{split}']=report
    save(RESULT/'score.json',summary)
    return summary


def evaluate_heads():
    import torch
    rows,features,masks=prepared();queries=json.loads((DATA/'queries.json').read_text())
    same_ref=defaultdict(list)
    for i,q in enumerate(queries):same_ref[q['reference_index']].append(i)
    swap={}
    for group in same_ref.values():
        for a,b in zip(group,group[1:]+group[:1]):swap[a]=b
    qmask=torch.load(CACHE/'masks.pt',map_location='cpu',weights_only=True)['predicted']
    swapped=torch.stack([qmask[swap[r['query_index']]] if r['reference_available'] else masks['predicted'][i].cpu() for i,r in enumerate(rows)]).to('mps')
    records=[]
    with torch.no_grad():
        for arm in ('oracle','predicted'):
            head=make_state_head().to('mps').eval();head.load_state_dict(torch.load(CACHE/f'{arm}_head.pt',map_location='mps',weights_only=True)['state_dict'])
            conditions=[('oracle',masks['oracle']),('predicted',masks['predicted'])]
            if arm=='predicted':conditions += [('swapped_target',swapped),('blank_current',masks['predicted']),('blank_reference',masks['predicted'])]
            for name,mask in conditions:
                for start in range(0,len(rows),32):
                    chunk=rows[start:start+32]
                    ref=[0 if name=='blank_reference' else r['reference_index'] for r in chunk]
                    cur=[0 if name=='blank_current' else r['current_index'] for r in chunk]
                    available=torch.tensor([float(r['reference_available']) for r in chunk],device='mps')
                    probabilities=torch.softmax(head(features[ref],features[cur],mask[start:start+len(chunk)],available),-1).cpu().numpy()
                    for r,p in zip(chunk,probabilities):
                        answer=CLASSES[int(p.argmax())]
                        records.append(dict(**r,condition=f'{arm}_head/{name}',answer=answer,probabilities=p.tolist(),
                            correct=answer==r['expected'],presence_correct=(answer!='未出现')==(r['expected']!='未出现')))
    write_jsonl(RESULT/'head_predictions.jsonl',records)
    summary=summarize_predictions(records)
    print(json.dumps({k:v['all'] for k,v in summary.items() if k.endswith('/dev')},ensure_ascii=False,indent=2))


def build_language_baseline():
    directory=DATA/'language_baseline';(directory/'images').mkdir(parents=True,exist_ok=False)
    cases=json.loads((DATA/'cases.json').read_text());images=json.loads((DATA/'images.json').read_text())
    locations=json.loads((RESULT/'localizations.json').read_text());rows=[];labels=[]
    for case in cases:
        if case['split']!='dev':continue
        current=Image.open(ROOT/images[case['current_index']]['image']).convert('RGB')
        im=Image.new('RGB',(432,432),'white');im.paste(current.crop((0,0,432,216)),(0,216))
        if case['reference_available']:
            reference=Image.open(ROOT/images[case['reference_index']]['image']).convert('RGB')
            im.paste(reference.crop((0,0,432,216)),(0,0))
            box=locations[case['query_index']]['predicted_box']
            if box is not None:im=add_target_box(im,[(box[0],box[1]),(box[2],box[3])])
        image=f'images/{case["sample_id"]}.png';im.save(directory/image)
        context=('图片上半部是完整参考，下半部是当前实际画面，两部分使用相同比例和位置。' if case['reference_available'] else
            '图片只有下半部的当前画面，没有完整参考、目标长度或过程。已出现的线条可能是完整短线，也可能是较长目标的一部分。')
        context+='本题只评价当前状态，不判断先后或笔内方向。上、中、下及左、右均指下半部书写区域中的固定位置，名称不随其他线条缺失而重新排序。'
        if case['reference_available']:context=CUE+context
        if not case['reference_available']:context+='本题只有一个目标笔迹实例，它的完整形状没有提供。'
        for task in ('presence','completion'):
            question=(f'当前画面中有没有{case["target"]}？部分线条也算已出现；出现写“有”，未出现写“无”。' if task=='presence' else
                f'相对完整参考，当前{case["target"]}的完成状态是什么？没有出现写“未出现”；已出现且达到参考全部形状写“完整”；只达到一部分写“部分”；缺少判断完成程度的依据写“未知”。')
            sid=f'{case["sample_id"]}-{task}'
            rows.append(dict(sample_id=sid,case_id=case['sample_id'],group_id=case['group_id'],split='dev',view='reference_current',
                task=task,wording=0,response_format='json',images=[image],prompt=context+question+'只输出一个JSON对象，只含answer字段，值为判断词，不写解释。'))
            labels.append(dict(sample_id=sid,expected=('无' if case['expected']=='未出现' else '有') if task=='presence' else case['expected'],
                allowed=['有','无'] if task=='presence' else CLASSES))
    write_jsonl(directory/'inputs.jsonl',rows);write_jsonl(directory/'labels.jsonl',labels)


def run_language_baseline():
    with (CACHE/'language_baseline.log').open('w') as log:
        subprocess.run([sys.executable,str(ROOT/'scripts/h1_run_showo.py'),'--device','mps','--inputs',str(DATA/'language_baseline/inputs.jsonl'),
            '--split','dev','--view','reference_current','--format','json','--constrain-answers','--adapter',str(ADAPTER),
            '--output',str(RESULT/'language_baseline')],cwd=ROOT,env=dict(os.environ,PYTORCH_ENABLE_MPS_FALLBACK='1'),stdout=log,stderr=subprocess.STDOUT,check=True)
    score_language_baseline()


def score_language_baseline():
    responses={r['sample_id']:r for r in read_jsonl(RESULT/'language_baseline/predictions.jsonl')}
    records=read_jsonl(RESULT/'head_predictions.jsonl')
    for case in json.loads((DATA/'cases.json').read_text()):
        if case['split']!='dev':continue
        answer=parse(responses[case['sample_id']+'-completion']['raw_response'],'json',CLASSES)
        presence=parse(responses[case['sample_id']+'-presence']['raw_response'],'json',['有','无'])
        records.append(dict(**case,condition='original_language/predicted_box',answer=answer,presence_answer=presence,
            correct=answer==case['expected'],presence_correct=presence==('无' if case['expected']=='未出现' else '有')))
    write_jsonl(RESULT/'all_predictions.jsonl',records);summarize_predictions(records)
    baseline={r['sample_id']:r for r in records if r['condition']=='original_language/predicted_box'}
    original_rows=json.loads((DATA/'cases.json').read_text())
    retained={original_rows[i]['sample_id'] for i in unique_indices(original_rows)}
    comparisons={}
    for condition in ['oracle_head/oracle','predicted_head/predicted','predicted_head/swapped_target','predicted_head/blank_current']:
        selected=[r for r in records if r['condition']==condition and r['split']=='dev' and r['sample_id'] in retained]
        groups=defaultdict(list)
        for r in selected:groups[r['group_id']].append(int(r['correct'])-int(baseline[r['sample_id']]['correct']))
        comparisons[condition]=dict(n=len(selected),completion_difference=sum(map(sum,groups.values()))/len(selected),
            paired_cluster_bootstrap95=interval(groups))
    save(RESULT/'language_comparisons.json',comparisons)
    diagnose()
    print(json.dumps(comparisons,ensure_ascii=False,indent=2))


def diagnose():
    rows=json.loads((DATA/'cases.json').read_text())
    queries=json.loads((DATA/'queries.json').read_text())
    retained={rows[i]['sample_id'] for i in unique_indices(rows)}
    predictions=read_jsonl(RESULT/'all_predictions.jsonl')
    by_condition={}
    for r in predictions:by_condition.setdefault(r['condition'],{})[r['sample_id']]=r
    localizations=json.loads((RESULT/'localizations.json').read_text())
    selected=[r for r in predictions if r['condition']=='predicted_head/predicted' and r['split']=='dev' and r['sample_id'] in retained]
    errors=[];comparisons={}
    for condition in ('oracle_head/oracle','predicted_head/oracle','predicted_head/swapped_target','predicted_head/blank_current','predicted_head/blank_reference'):
        groups=defaultdict(list);changed=0
        for r in selected:
            other=by_condition[condition][r['sample_id']]
            groups[r['group_id']].append(int(r['correct'])-int(other['correct']))
            changed+=int(r['answer']!=other['answer'])
        comparisons[condition]=dict(completion_difference=sum(map(sum,groups.values()))/len(selected),
            paired_cluster_bootstrap95=interval(groups),answer_changes=changed)
    for r in selected:
        if r['correct']:continue
        loc=localizations[r['query_index']] if r['reference_available'] else None
        errors.append(dict(sample_id=r['sample_id'],group_id=r['group_id'],kind=r['kind'],target=r['target'],fraction=r['fraction'],
            expected=r['expected'],answer=r['answer'],probabilities=r['probabilities'],
            localization_within_12px=loc['within_12px'] if loc else None,
            same_head_oracle_answer=by_condition['predicted_head/oracle'][r['sample_id']]['answer'],
            oracle_trained_answer=by_condition['oracle_head/oracle'][r['sample_id']]['answer'],
            language_answer=by_condition['original_language/predicted_box'][r['sample_id']]['answer']))
    near_complete={}
    for condition in ('oracle_head/oracle','predicted_head/predicted','predicted_head/oracle'):
        groups=defaultdict(list);answers=Counter()
        for r in by_condition[condition].values():
            if r['split']!='dev' or r['fraction']!=.85 or not r['reference_available']:continue
            points=queries[r['query_index']]['strokes'][r['target']]
            gap=sum(math.dist(a,b) for a,b in zip(points,points[1:]))*.15
            band='<16px' if gap<16 else '16-32px' if gap<32 else '>=32px'
            groups[band].append(r['correct']);answers[r['answer']]+=1
        near_complete[condition]=dict(answers=dict(answers),by_missing_length={k:dict(n=len(v),correct=sum(v)) for k,v in groups.items()})
    language=[r for r in by_condition['original_language/predicted_box'].values() if r['sample_id'] in retained]
    disagreements=sum((r['presence_answer']=='有')!=(r['answer']!='未出现') for r in language)
    save(RESULT/'diagnosis.json',dict(role='Post-hoc failure analysis; no checkpoint or threshold changes.',
        dev_cases=len(selected),completion_errors=len(errors),language_presence_completion_disagreements=disagreements,
        comparisons=comparisons,near_complete=near_complete,cases=errors))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','extract','locate','train','evaluate','build-baseline','run-baseline','score-baseline','diagnose'])
    parser.add_argument('--data',type=Path,default=DATA)
    parser.add_argument('--output',type=Path,default=RESULT)
    parser.add_argument('--cache',type=Path,default=CACHE)
    args=parser.parse_args()
    DATA,RESULT,CACHE=args.data.resolve(),args.output.resolve(),args.cache.resolve()
    {'build':build,'extract':extract,'locate':locate,'train':train,'evaluate':evaluate_heads,
     'build-baseline':build_language_baseline,'run-baseline':run_language_baseline,'score-baseline':score_language_baseline,'diagnose':diagnose}[args.command]()
