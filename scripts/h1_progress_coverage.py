"""Matched continuation of UMM state readouts with broader partial-progress coverage."""
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import math
import random
import time

import numpy as np
from PIL import Image, ImageDraw

import h1_region_state as previous
from h1_region_state import ROOT, CLASSES, KINDS, render, target_mask, make_state_head
from h1_target_grid_generalization import geometry, prompt, make_head as make_target_head, CACHE as TARGET_CACHE
from h1_target_grid import ADAPTER, mask_box
from h1_spatial_probe import CACHE as SPATIAL_CACHE
from h1_run_showo import load_model, StateImageEncoder, image_prompt_embeds
from h1_train_state import load_adapter
from h1_state_gate import interval, write_jsonl, read_jsonl

DATA=ROOT/'data/h1/progress_coverage_v1'
RESULT=ROOT/'results/h1/showo2_video_1_5b/progress_coverage_v1'
CACHE=ROOT/'checkpoints/h1_progress_coverage_v1'
LOW=[.05,.1,.15,.25,.4]
HIGH=[.6,.75,.85,.9,.95]
FRESH=[0,.08,.3,.7,.9,.97,1]


def save(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def build():
    DATA.mkdir(parents=True,exist_ok=False);(DATA/'images').mkdir()
    RESULT.mkdir(parents=True,exist_ok=False);CACHE.mkdir(parents=True,exist_ok=False)
    images=json.loads((previous.DATA/'images.json').read_text())
    queries=json.loads((previous.DATA/'queries.json').read_text())
    old_cases=json.loads((previous.DATA/'cases.json').read_text())
    retained=[old_cases[i] for i in previous.unique_indices(old_cases)]
    train=[dict(r) for r in retained if r['split']=='train']
    old_dev=[dict(r) for r in retained if r['split']=='dev']
    reused_images=len(images);reused_queries=len(queries)
    def picture(name, image, split):
        path=DATA/'images'/f'{name}.png';image.save(path)
        images.append(dict(image=str(path.relative_to(ROOT)),split=split));return len(images)-1
    qi=[i for i,q in enumerate(queries) if q['split']=='train' and q['kind'] in KINDS]
    rng=random.Random(10440);rng.shuffle(qi)
    low={q:LOW[i%len(LOW)] for i,q in enumerate(qi)}
    rng.shuffle(qi);high={q:HIGH[i%len(HIGH)] for i,q in enumerate(qi)}
    scenes=defaultdict(list)
    for r in train:
        if r['kind'] in KINDS:scenes[r['scene_id']].append(r)
    changes={};new_current={}
    for scene,rows in scenes.items():
        first=rows[0];q=queries[first['query_index']]
        progress={r['target']:(low[r['query_index']] if r['fraction']==.25 else high[r['query_index']] if r['fraction']==.6 else r['fraction']) for r in rows}
        if any(progress[r['target']]!=r['fraction'] for r in rows):
            new_current[scene]=picture('coverage-'+scene,render(q['strokes'],progress,q['width']),'train')
        for r in rows:changes[r['sample_id']]=progress[r['target']]
    coverage=[]
    for row in train:
        row=dict(row)
        if row['scene_id'] in new_current:row['current_index']=new_current[row['scene_id']]
        row['original_fraction']=row['fraction'];row['fraction']=changes.get(row['sample_id'],row['fraction'])
        coverage.append(row)
    # New evaluation geometry and co-occurrence pattern are fixed before training.
    fresh=[];rng=random.Random(10441)
    def query(gid,kind,strokes,width,target,ref):
        index=len(queries)
        queries.append(dict(query_id=index,group_id=gid,split='fresh',kind=kind,target=target,
            reference_index=ref,prompt=prompt(target),strokes=strokes,width=width))
        return index
    for kind in KINDS:
        for gi in range(8):
            gid=f'progress-fresh-{kind}-{gi:02}'
            boxes=geometry(rng,kind);strokes={k:[b[:2],b[2:]] for k,b in boxes.items()};width=rng.choice([3,5,7,9])
            ref=picture(gid+'-reference',render(strokes,{k:1 for k in strokes},width),'fresh')
            ids={k:query(gid,kind,strokes,width,k,ref) for k in strokes}
            for vi in range(len(FRESH)):
                progress={k:FRESH[(vi+2*j)%len(FRESH)] for j,k in enumerate(strokes)}
                cur=picture(f'{gid}-current-{vi}',render(strokes,progress,width),'fresh')
                for target,index in ids.items():
                    frac=progress[target]
                    fresh.append(dict(sample_id=f'{gid}-{vi}-{target}',group_id=gid,split='fresh',kind=kind,
                        scene_id=f'{gid}-{vi}',query_index=index,reference_index=ref,current_index=cur,
                        target=target,fraction=frac,reference_available=True,reference_pair=None,
                        stress=frac==.97,expected=CLASSES[0 if frac==0 else 2 if frac==1 else 1]))
    for gi in range(6):
        gid=f'progress-fresh-reference-{gi:02}'
        x=rng.randint(24,85);y=rng.randint(30,190);length=rng.randint(90,145);width=rng.choice([3,5,7,9])
        strokes={'横线':[[x,y],[x+length,y]]}
        cur=picture(gid+'-current',render(strokes,{'横线':1},width),'fresh')
        for factor in (1,2):
            full={'横线':[[x,y],[x+length*factor,y]]}
            ref=picture(f'{gid}-reference-{factor}',render(full,{'横线':1},width),'fresh')
            index=query(gid,'reference_control',full,width,'横线',ref)
            fresh.append(dict(sample_id=f'{gid}-{factor}',group_id=gid,split='fresh',kind='reference_control',
                scene_id=f'{gid}-{factor}',query_index=index,reference_index=ref,current_index=cur,target='横线',
                fraction=1/factor,reference_available=True,reference_pair=gid,stress=False,
                expected='完整' if factor==1 else '部分'))
    for gi in range(6):
        gid=f'progress-fresh-unknown-{gi:02}'
        if gi%2:
            x=rng.randint(45,380);strokes={'目标笔迹':[[x,30],[x,rng.randint(140,195)]]}
        else:
            y=rng.randint(30,190);strokes={'目标笔迹':[[45,y],[rng.randint(200,390),y]]}
        width=rng.choice([3,5,7,9])
        for vi,frac in enumerate(FRESH):
            if frac==0 and gi>0:continue
            cur=0 if frac==0 else picture(f'{gid}-current-{vi}',render(strokes,{'目标笔迹':frac},width),'fresh')
            fresh.append(dict(sample_id=f'{gid}-{vi}',group_id=gid,split='fresh',kind='unknown_control',
                scene_id=f'{gid}-{vi}',query_index=None,reference_index=0,current_index=cur,target='目标笔迹',
                fraction=frac,reference_available=False,reference_pair=None,stress=False,
                expected='未出现' if frac==0 else '未知'))
    save(DATA/'images.json',images);save(DATA/'queries.json',queries)
    for name,rows in [('train_replay',train),('train_coverage',coverage),('dev_previous',old_dev),('dev_fresh',fresh)]:save(DATA/f'{name}.json',rows)
    save(DATA/'progress_changes.json',[dict(query_index=q,low=low[q],high=high[q]) for q in sorted(low)])
    plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),
        question='Does broader partial-progress supervision improve completion boundaries at fixed update budget, including new geometry?',
        model='Full frozen Show-o2-1.5B-w-video-und; original state adapter, target head and ink head unchanged.',
        arms=['replay','coverage'],region_sources=['oracle','predicted'],
        initialization='Both continuation arms start from the same previous final head for their respective region source. Optimizer reinitialized identically.',
        matched='Same 509 cases, geometry, target, labels, row order, class weights and minibatch indices. Only partial progress in multi-target current images changes. Reference-pair and current-only controls unchanged.',
        training_progress=dict(previous=[0,.25,.6,1],coverage_low=LOW,coverage_high=HIGH,
            assignment='Seed10440; shuffled reference target keys, round-robin levels; fixed per target and old partial-state type.'),
        training=dict(steps=400,batch_size=32,lr=.0003,weight_decay=.01,seed=10442,parameters=57764,
            optimizer='AdamW',loss='Four-class inverse-frequency weighted cross entropy; same weights in both arms.'),
        evaluation=dict(previous_cases=len(old_dev),fresh_cases=len(fresh),fresh_groups=len({r['group_id'] for r in fresh}),
            fresh_seed=10441,progress=FRESH,co_occurrence='Cyclic stride 2 across targets, versus previous stride 1.',
            stress='97% progress with reference is separately declared boundary stress before training; retained in overall results as well. Core excludes only these 56 declared stress cases.',
            masks='Initial heads and both continuations evaluated on their own region source; predicted-region continuations additionally evaluated on oracle regions.',
            policy='Final checkpoints only; no threshold or checkpoint selection. Old development is retention, fresh development is prospective. Original 130-case visual test unused.'),
        metrics='Completion/presence, class confusion, actual progress, false-complete on partial, false-partial on complete, reference pairs, target pairs, old retention; paired geometry bootstrap.',
        costs=dict(reused_images=reused_images,reused_queries=reused_queries,new_images=len(images)-reused_images,
            new_queries=len(queries)-reused_queries,changed_training_images=len(new_current)),
        scope='Continued auxiliary UMM feature readout only. No new language-model benchmark or base-weight update; no order, font, Chinese or unified-learning claim.',
        blank='One visible empty current-only control per evaluation set; shared with training and not novel-geometry evidence.')
    save(RESULT/'plan.json',plan)
    draw_examples()
    print(json.dumps(dict(train_cases=len(train),fresh_cases=len(fresh),costs=plan['costs']),ensure_ascii=False))


def extract():
    import torch
    start=time.perf_counter();plan=json.loads((RESULT/'plan.json').read_text())
    old=torch.load(previous.CACHE/'features.pt',map_location='cpu',weights_only=True)['features']
    assets=ROOT/'checkpoints/Show-o-assets'
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',assets,'cpu')
    encoder=StateImageEncoder(model,assets,'mps');values=[]
    rows=json.loads((DATA/'images.json').read_text())[plan['costs']['reused_images']:]
    with (CACHE/'progress.jsonl').open('w') as log:
        for i,r in enumerate(rows):
            values.append(encoder.encode(ROOT/r['image']).squeeze(0).cpu());encoder.cache.clear()
            if (i+1)%12==0:
                log.write(json.dumps(dict(stage='vision',completed=i+1,seconds=time.perf_counter()-start))+'\n');log.flush()
    features=torch.cat([old,torch.stack(values)])
    torch.save(dict(features=features),CACHE/'features.pt')
    save(RESULT/'extraction.json',dict(seconds=time.perf_counter()-start,new_images=len(rows),reused_images=len(old),
        shape=list(features.shape),full_model_parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0))


def locate():
    import torch
    start=time.perf_counter();plan=json.loads((RESULT/'plan.json').read_text())
    queries=json.loads((DATA/'queries.json').read_text())
    features=torch.load(CACHE/'features.pt',map_location='cpu',weights_only=True)['features']
    old=torch.load(previous.CACHE/'masks.pt',map_location='cpu',weights_only=True)
    predicted=[r for r in old['predicted']];oracle=[r for r in old['oracle']]
    records=json.loads((previous.RESULT/'localizations.json').read_text())
    model,tok,ids=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','mps')
    load_adapter(model,ADAPTER,'mps');model.eval().requires_grad_(False)
    model.time_embed.to('mps');model.time_embed_proj.to('mps')
    from models import omni_attn_mask_naive
    target=torch.load(TARGET_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    ink=torch.load(SPATIAL_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    head=make_target_head().eval();head.load_state_dict(target['state_dict'])
    ink_head=torch.nn.Linear(1536,1).eval();ink_head.load_state_dict(ink['state_dict'])
    with torch.inference_mode():
        for row in queries[plan['costs']['reused_queries']:]:
            visual=features[row['reference_index']]
            emb,mods=image_prompt_embeds(model,tok,ids,row['prompt'],visual[None].to('mps'),'mps')
            attn=omni_attn_mask_naive(B=1,LEN=emb.shape[1],modalities=mods,device='mps',inverted=True).to(emb.dtype)
            hidden=model.showo.model(inputs_embeds=emb,attention_mask=attn,use_cache=False,return_dict=True).last_hidden_state[0,-1].cpu().float()
            v=visual.float()
            selected=(head.v((v-target['vmean'])/target['vstd'])*head.q((hidden-target['qmean'])/target['qstd'])).sum(-1)/math.sqrt(32)+head.bias>=0
            mask=selected&(ink_head((v-ink['mean'])/ink['std']).squeeze(-1)>=0)
            predicted.append(mask);gold=torch.tensor(target_mask(row['strokes'],row['target'],row['width']));oracle.append(gold)
            box=mask_box(mask.numpy());xs,ys=zip(*row['strokes'][row['target']]);expected=[min(xs),min(ys),max(xs),max(ys)]
            records.append(dict(query_id=row['query_id'],group_id=row['group_id'],split='fresh',kind=row['kind'],target=row['target'],
                predicted_box=box,expected_box=expected,within_12px=box is not None and max(abs(a-b) for a,b in zip(box,expected))<=12,
                predicted_cells=mask.nonzero().flatten().tolist(),oracle_cells=gold.nonzero().flatten().tolist()))
    torch.save(dict(predicted=torch.stack(predicted),oracle=torch.stack(oracle)),CACHE/'masks.pt')
    save(RESULT/'localizations.json',records)
    fresh=records[plan['costs']['reused_queries']:]
    save(RESULT/'localization_summary.json',dict(seconds=time.perf_counter()-start,reused_queries=len(old['oracle']),
        fresh_targets=len(fresh),fresh_hits=sum(r['within_12px'] for r in fresh)))


def prepared():
    import torch
    # Keep the large immutable feature bank in bf16; normalize selected batches.
    features=torch.load(CACHE/'features.pt',map_location='cpu',weights_only=True)['features'].to('mps')
    stats=torch.load(SPATIAL_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    mean,std=stats['mean'].to('mps'),stats['std'].to('mps')
    masks=torch.load(CACHE/'masks.pt',map_location='cpu',weights_only=True)
    masks['connected']=torch.stack([torch.tensor(largest_component(mask.numpy())) for mask in masks['predicted']])
    upper=torch.zeros(729,dtype=torch.bool);upper[:14*27]=True
    def inputs(rows,region):
        ref=(features[[r['reference_index'] for r in rows]].float()-mean)/std
        cur=(features[[r['current_index'] for r in rows]].float()-mean)/std
        mask=torch.stack([masks[region][r['query_index']] if r['reference_available'] else upper for r in rows]).to('mps')
        available=torch.tensor([float(r['reference_available']) for r in rows],device='mps')
        return ref,cur,mask,available
    return inputs


def largest_component(mask):
    grid=np.asarray(mask).reshape(27,27);seen=set();components=[]
    for y,x in zip(*np.where(grid)):
        if (int(y),int(x)) in seen:continue
        queue=deque([(int(y),int(x))]);seen.add((int(y),int(x)));component=[]
        while queue:
            point=queue.popleft();component.append(point)
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                q=(point[0]+dy,point[1]+dx)
                if 0<=q[0]<27 and 0<=q[1]<27 and grid[q] and q not in seen:seen.add(q);queue.append(q)
        components.append(component)
    result=np.zeros((27,27),dtype=bool)
    if components:
        for point in max(components,key=len):result[point]=True
    return result.reshape(-1)


def connected_diagnostic():
    import torch
    inputs=prepared();head=make_state_head().to('mps').eval()
    head.load_state_dict(torch.load(CACHE/'coverage_predicted.pt',map_location='mps',weights_only=True)['state_dict'])
    baseline={(r['evaluation_set'],r['sample_id']):r for r in read_jsonl(RESULT/'predictions.jsonl') if r['condition']=='coverage_predicted/predicted'}
    records=[];summary={};comparisons={};start=time.perf_counter()
    with torch.no_grad():
        for subset in ('dev_previous','dev_fresh'):
            rows=json.loads((DATA/f'{subset}.json').read_text());scored=[]
            for offset in range(0,len(rows),32):
                batch=rows[offset:offset+32]
                probs=torch.softmax(head(*inputs(batch,'connected')),-1).cpu().tolist()
                for row,p in zip(batch,probs):
                    answer=CLASSES[int(np.argmax(p))]
                    scored.append(dict(**row,condition='coverage_predicted/connected',evaluation_set=subset,
                        answer=answer,probabilities=p,correct=answer==row['expected'],presence_correct=(answer!='未出现')==(row['expected']!='未出现')))
            records.extend(scored);summary[subset]=measures(scored)
            for name,selected in [('all',scored),('core',[r for r in scored if not r.get('stress',False)])]:
                groups=defaultdict(list)
                for r in selected:groups[r['group_id']].append(int(r['correct'])-int(baseline[(subset,r['sample_id'])]['correct']))
                comparisons[f'{subset}/{name}']=dict(n=len(selected),difference=sum(map(sum,groups.values()))/len(selected),
                    paired_cluster_bootstrap95=interval(groups),repairs=sum(r['correct'] and not baseline[(subset,r['sample_id'])]['correct'] for r in selected),
                    regressions=sum(not r['correct'] and baseline[(subset,r['sample_id'])]['correct'] for r in selected))
    write_jsonl(RESULT/'connected_predictions.jsonl',records)
    save(RESULT/'connected_score.json',dict(seconds=time.perf_counter()-start,metrics=summary,comparisons=comparisons))
    print(json.dumps({k:v['all'] for k,v in summary.items()},indent=2))


def train():
    import torch
    import torch.nn.functional as F
    inputs=prepared()
    data={arm:json.loads((DATA/f'train_{arm}.json').read_text()) for arm in ('replay','coverage')}
    labels=[CLASSES.index(r['expected']) for r in data['replay']]
    assert labels==[CLASSES.index(r['expected']) for r in data['coverage']]
    counts=torch.tensor([labels.count(i) for i in range(4)],dtype=torch.float32,device='mps');weight=counts.sum()/(4*counts)
    for region in ('oracle','predicted'):
        for arm in ('replay','coverage'):
            torch.manual_seed(10442);generator=torch.Generator().manual_seed(10442)
            head=make_state_head().to('mps');head.load_state_dict(torch.load(previous.CACHE/f'{region}_head.pt',map_location='mps',weights_only=True)['state_dict'])
            opt=torch.optim.AdamW(head.parameters(),lr=.0003,weight_decay=.01)
            start=time.perf_counter();name=f'{arm}_{region}'
            with (RESULT/f'{name}_training.jsonl').open('w') as log:
                for step in range(400):
                    index=torch.randint(len(labels),(32,),generator=generator).tolist()
                    batch=[data[arm][i] for i in index]
                    logits=head(*inputs(batch,region));truth=torch.tensor([labels[i] for i in index],device='mps')
                    loss=F.cross_entropy(logits,truth,weight=weight)
                    opt.zero_grad();loss.backward();opt.step()
                    if (step+1)%25==0:
                        log.write(json.dumps(dict(step=step+1,loss=float(loss.detach())))+'\n');log.flush()
            torch.mps.synchronize()
            torch.save(dict(state_dict={k:v.cpu() for k,v in head.state_dict().items()}),CACHE/f'{name}.pt')
            save(RESULT/f'{name}_training.json',dict(seconds=time.perf_counter()-start,steps=400,train_cases=len(labels),
                parameters=sum(p.numel() for p in head.parameters()),umm_updated_parameters=0,class_counts=counts.cpu().tolist()))


def measures(rows):
    result={}
    subsets={'all':rows,'core':[r for r in rows if not r.get('stress',False)],
        'reference':[r for r in rows if r['reference_available']],
        'visible_completion':[r for r in rows if r['reference_available'] and r['expected'] in ('部分','完整')],
        'unknown':[r for r in rows if not r['reference_available']]}
    for name,subset in subsets.items():
        grouped=defaultdict(list);presence=defaultdict(list)
        for r in subset:grouped[r['group_id']].append(int(r['correct']));presence[r['group_id']].append(int(r['presence_correct']))
        result[name]=dict(n=len(subset),groups=len(grouped),completion=sum(r['correct'] for r in subset),presence=sum(r['presence_correct'] for r in subset),
            completion_ci95=interval(grouped),presence_ci95=interval(presence))
    result['classes']={c:dict(n=sum(r['expected']==c for r in rows),correct=sum(r['expected']==c and r['correct'] for r in rows),
        answers=dict(Counter(r['answer'] for r in rows if r['expected']==c))) for c in CLASSES}
    result['reference_progress']={str(f):dict(n=sum(r['reference_available'] and r['fraction']==f for r in rows),
        correct=sum(r['reference_available'] and r['fraction']==f and r['correct'] for r in rows),
        answers=dict(Counter(r['answer'] for r in rows if r['reference_available'] and r['fraction']==f)))
        for f in sorted({r['fraction'] for r in rows if r['reference_available']})}
    result['premature_complete']=dict(n=sum(r['expected']=='部分' for r in rows),errors=sum(r['expected']=='部分' and r['answer']=='完整' for r in rows))
    result['complete_as_partial']=dict(n=sum(r['expected']=='完整' for r in rows),errors=sum(r['expected']=='完整' and r['answer']=='部分' for r in rows))
    reference=defaultdict(list);scenes=defaultdict(list);target_pairs=defaultdict(list)
    for r in rows:
        if r['reference_pair']:reference[r['reference_pair']].append(r)
        if r['kind'] in KINDS:scenes[r['scene_id']].append(r)
    for scene in scenes.values():
        for i,a in enumerate(scene):
            for b in scene[i+1:]:
                if a['expected']!=b['expected']:target_pairs[a['group_id']].append(int(a['correct'] and b['correct']))
    result['reference_pairs']=dict(n=len(reference),correct=sum(all(r['correct'] for r in p) for p in reference.values()))
    result['target_pairs']=dict(n=sum(map(len,target_pairs.values())),correct=sum(map(sum,target_pairs.values())),ci95=interval(target_pairs))
    return result


def evaluate():
    import torch
    inputs=prepared();records=[];summary={}
    datasets={name:json.loads((DATA/f'{name}.json').read_text()) for name in ('train_replay','train_coverage','dev_previous','dev_fresh')}
    with torch.no_grad():
        for region in ('oracle','predicted'):
            for arm in ('initial','replay','coverage'):
                name=f'{arm}_{region}'
                path=previous.CACHE/f'{region}_head.pt' if arm=='initial' else CACHE/f'{name}.pt'
                head=make_state_head().to('mps').eval();head.load_state_dict(torch.load(path,map_location='mps',weights_only=True)['state_dict'])
                sources=[region]+(['oracle'] if region=='predicted' and arm!='initial' else [])
                for source in sources:
                    sets=['dev_previous','dev_fresh']+([f'train_{arm}'] if arm!='initial' and source==region else [])
                    for subset in sets:
                        scored=[]
                        for start in range(0,len(datasets[subset]),32):
                            batch=datasets[subset][start:start+32]
                            probabilities=torch.softmax(head(*inputs(batch,source)),-1).cpu().tolist()
                            for row,p in zip(batch,probabilities):
                                answer=CLASSES[int(np.argmax(p))]
                                scored.append(dict(**row,condition=f'{name}/{source}',evaluation_set=subset,answer=answer,probabilities=p,
                                    correct=answer==row['expected'],presence_correct=(answer!='未出现')==(row['expected']!='未出现')))
                        records.extend(scored);summary[f'{name}/{source}/{subset}']=measures(scored)
    write_jsonl(RESULT/'predictions.jsonl',records);save(RESULT/'score.json',summary)
    compare()
    print(json.dumps({k:v['all'] for k,v in summary.items() if k.endswith('dev_fresh')},indent=2))


def compare():
    records=read_jsonl(RESULT/'predictions.jsonl');result={}
    for subset in ('dev_previous','dev_fresh'):
        for region in ('oracle','predicted'):
            before={r['sample_id']:r for r in records if r['condition']==f'replay_{region}/{region}' and r['evaluation_set']==subset}
            after=[r for r in records if r['condition']==f'coverage_{region}/{region}' and r['evaluation_set']==subset]
            for name,selected in [('all',after),('core',[r for r in after if not r.get('stress',False)]),
                ('near_complete',[r for r in after if r['reference_available'] and .8<=r['fraction']<1])]:
                groups=defaultdict(list)
                for r in selected:groups[r['group_id']].append(int(r['correct'])-int(before[r['sample_id']]['correct']))
                result[f'{subset}/{region}/{name}']=dict(n=len(selected),
                    before_correct=sum(before[r['sample_id']]['correct'] for r in selected),after_correct=sum(r['correct'] for r in selected),
                    difference=sum(map(sum,groups.values()))/len(selected),paired_cluster_bootstrap95=interval(groups))
    save(RESULT/'paired_comparisons.json',result)


def diagnose():
    records=read_jsonl(RESULT/'predictions.jsonl')+read_jsonl(RESULT/'connected_predictions.jsonl')
    selected=[r for r in records if r['evaluation_set']=='dev_fresh']
    by_condition={}
    for r in selected:by_condition.setdefault(r['condition'],{})[r['sample_id']]=r
    queries=json.loads((DATA/'queries.json').read_text());locations=json.loads((RESULT/'localizations.json').read_text())
    conditions=['replay_oracle/oracle','coverage_oracle/oracle','replay_predicted/predicted',
        'coverage_predicted/predicted','coverage_predicted/oracle','coverage_predicted/connected']
    analysis={};errors=[]
    for condition in conditions:
        rows=list(by_condition[condition].values());bands=defaultdict(list);scenes=defaultdict(list);pairs=defaultdict(list)
        for r in rows:
            if r['reference_available'] and r['fraction']==.97:
                a,b=queries[r['query_index']]['strokes'][r['target']]
                end=[round(x+(y-x)*.97) for x,y in zip(a,b)]
                gap=math.dist(end,b);band='1-3px' if gap<=3 else '4-7px' if gap<8 else '>=8px'
                bands[band].append(r['correct'])
            if r['kind'] in KINDS and not r.get('stress',False):scenes[r['scene_id']].append(r)
        for scene in scenes.values():
            for i,a in enumerate(scene):
                for b in scene[i+1:]:
                    if a['expected']!=b['expected']:pairs[a['group_id']].append(int(a['correct'] and b['correct']))
        analysis[condition]=dict(stress_by_rendered_gap={k:dict(n=len(v),correct=sum(v)) for k,v in bands.items()},
            core_target_pairs=dict(n=sum(map(len,pairs.values())),correct=sum(map(sum,pairs.values())),ci95=interval(pairs)))
    baseline=by_condition['coverage_predicted/predicted']
    for r in baseline.values():
        if r['correct']:continue
        loc=locations[r['query_index']];pred=set(loc['predicted_cells']);gold=set(loc['oracle_cells'])
        errors.append(dict(sample_id=r['sample_id'],group_id=r['group_id'],kind=r['kind'],target=r['target'],fraction=r['fraction'],
            expected=r['expected'],answer=r['answer'],stress=r.get('stress',False),localization_within_12px=loc['within_12px'],
            extra_mask_cells=len(pred-gold),missing_mask_cells=len(gold-pred),predicted_mask_cells=len(pred),oracle_mask_cells=len(gold),
            same_head_oracle_answer=by_condition['coverage_predicted/oracle'][r['sample_id']]['answer'],
            connected_answer=by_condition['coverage_predicted/connected'][r['sample_id']]['answer']))
    save(RESULT/'diagnosis.json',dict(role='Post-hoc error analysis; no change to weights, scores or declared cohorts.',
        conditions=analysis,predicted_head_errors=errors))
    print(json.dumps(analysis,ensure_ascii=False,indent=2))


def draw_examples():
    images=json.loads((DATA/'images.json').read_text());queries=json.loads((DATA/'queries.json').read_text())
    replay=json.loads((DATA/'train_replay.json').read_text());coverage=json.loads((DATA/'train_coverage.json').read_text())
    selected=[]
    for level in (.05,.9,.95):
        i=next(i for i,r in enumerate(coverage) if r['kind'] in KINDS and r['fraction']==level and r['target']==list(queries[r['query_index']]['strokes'])[0])
        selected.append((replay[i],coverage[i]))
    canvas=Image.new('RGB',(3*330,3*188),'white');draw=ImageDraw.Draw(canvas)
    for y,(old,new) in enumerate(selected):
        for x,(title,index) in enumerate([('Reference: first target',new['reference_index']),
            (f'Replay progress {old["fraction"]}',old['current_index']),(f'Coverage progress {new["fraction"]}',new['current_index'])]):
            im=Image.open(ROOT/images[index]['image']).convert('RGB').crop((0,0,432,216)).resize((324,162))
            canvas.paste(im,(x*330,y*188+22));draw.text((x*330,y*188+4),title,fill='black')
    canvas.save(RESULT/'training_examples.png')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','extract','locate','train','evaluate','compare','connected','diagnose'])
    parser.add_argument('--data',type=Path,default=DATA);parser.add_argument('--output',type=Path,default=RESULT);parser.add_argument('--cache',type=Path,default=CACHE)
    args=parser.parse_args();DATA,RESULT,CACHE=args.data.resolve(),args.output.resolve(),args.cache.resolve()
    {'build':build,'extract':extract,'locate':locate,'train':train,'evaluate':evaluate,'compare':compare,'connected':connected_diagnostic,'diagnose':diagnose}[args.command]()
