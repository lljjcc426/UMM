"""Target-conditioned spatial readout from frozen UMM image and question states."""
from pathlib import Path
from collections import defaultdict,deque
from datetime import datetime,timezone
import argparse
import json
import math
import time
import numpy as np
from PIL import Image,ImageDraw
from h1_run_showo import ROOT,load_model,image_prompt_embeds,MODEL_REVISION,SOURCE_REVISION
from h1_train_state import load_adapter
from h1_spatial_probe import SOURCES,metrics,RESULT as SPATIAL_RESULT,CACHE as SPATIAL_CACHE
from h1_state_gate import interval

RESULT=ROOT/'results/h1/showo2_video_1_5b/target_grid_v1'
CACHE=ROOT/'checkpoints/h1_target_grid_v1'
ADAPTER=ROOT/'checkpoints/h1_target_cue_boxed_v1/adapter.pt'


def build():
    if (RESULT/'plan.json').exists():
        raise FileExistsError(RESULT/'plan.json')
    RESULT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
    rows=[]
    for split,source in SOURCES.items():
        for row in json.loads((source/'cases.json').read_text()):
            rows.append({**row,'split':split,'image':str((source/row['image']).relative_to(ROOT))})
    (RESULT/'cases.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),model='showlab/show-o2-1.5B-w-video-und',
        model_revision=MODEL_REVISION,source_revision=SOURCE_REVISION,adapter=str(ADAPTER.relative_to(ROOT)),
        train_targets=84,train_geometry_groups=36,dev_targets=28,dev_geometry_groups=12,
        features='Frozen 729 fusion visual tokens plus final prompt hidden state from the full UMM language path, conditioned on reference image and target question.',
        query='上半部是完整线条参考，下半部为空白。请只定位{target}，不要选择其他线条。',
        head='32-dimensional bilinear visual/question interaction with scalar bias; base UMM and existing state adapter frozen.',
        labels='Selected reference line only, rendered width 5 from training centerline bounds; 27x27 cells, >=8 black pixels per cell.',
        normalization='Visual channel statistics from the preceding training-only cache; question channel statistics from 84 training queries only.',
        optimization=dict(steps=400,batch_size=8,lr=.003,optimizer='AdamW',weight_decay=.01,seed=10420,
                          loss='Binary cross entropy, positive weight set by all training target cells.'),
        decoding='Threshold .5; largest 4-connected component; bounding coordinates are extreme cell centers (16-pixel spacing). Empty mask is a localization failure.',
        controls=['Cycle the other actual target-question hidden states within the same image, keeping scoring labels fixed',
                  'Use the previous all-ink readout mask for every target, with identical largest-component decoding'],
        evaluation='Final head only; target IoU/F1 and four-coordinate tolerance 12 pixels; grouped by geometry; no test or H1 acceptance.',
        scope='Added spatial head on frozen UMM; no free coordinate generation, no temporal input and no current completion information.')
    (RESULT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(plan)


def extract():
    import torch
    assets=ROOT/'checkpoints/Show-o-assets'
    start=time.perf_counter()
    model,tok,ids=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',assets,'mps')
    config=load_adapter(model,ADAPTER,'mps');model.eval().requires_grad_(False)
    model.time_embed.to('mps');model.time_embed_proj.to('mps')
    from models import omni_attn_mask_naive
    pool=torch.load(SPATIAL_CACHE/'features.pt',map_location='cpu',weights_only=True)['features']
    image_rows=json.loads((SPATIAL_RESULT/'inputs.json').read_text())
    index={r['image']:i for i,r in enumerate(image_rows)}
    rows=json.loads((RESULT/'cases.json').read_text())
    hidden=[];inputs=[]
    with torch.inference_mode():
        for row in rows:
            prompt=f'上半部是完整线条参考，下半部为空白。请只定位{row["target"]}，不要选择其他线条。'
            emb,mods=image_prompt_embeds(model,tok,ids,prompt,pool[index[row['image']]][None].to('mps'),'mps')
            mask=omni_attn_mask_naive(B=1,LEN=emb.shape[1],modalities=mods,device='mps',inverted=True).to(emb.dtype)
            output=model.showo.model(inputs_embeds=emb,attention_mask=mask,use_cache=False,return_dict=True)
            hidden.append(output.last_hidden_state[0,-1].cpu())
            inputs.append(dict(sample_id=row['sample_id'],image=row['image'],prompt=prompt))
    torch.save(dict(hidden=torch.stack(hidden),image_indices=[index[r['image']] for r in rows]),CACHE/'questions.pt')
    (RESULT/'inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    (RESULT/'extraction.json').write_text(json.dumps(dict(finished_utc=datetime.now(timezone.utc).isoformat(),
        elapsed_seconds=time.perf_counter()-start,adapter_config=config,full_model_parameters=sum(p.numel() for p in model.parameters()),
        umm_trainable_parameters=0,question_hidden_shape=list(torch.stack(hidden).shape)),indent=2)+'\n')


def target_grid(row):
    canvas=Image.new('L',(432,432),255)
    x0,y0,x1,y1=row['expected_box']
    ImageDraw.Draw(canvas).line([(x0,y0),(x1,y1)],fill=0,width=5)
    return (np.asarray(canvas).reshape(27,16,27,16)<128).sum(axis=(1,3)).reshape(-1)>=8


def mask_box(mask):
    mask=np.asarray(mask).reshape(27,27);seen=set();components=[]
    for y,x in zip(*np.where(mask)):
        if (y,x) in seen:continue
        todo=deque([(int(y),int(x))]);seen.add((y,x));component=[]
        while todo:
            p=todo.popleft();component.append(p)
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                q=(p[0]+dy,p[1]+dx)
                if 0<=q[0]<27 and 0<=q[1]<27 and mask[q] and q not in seen:
                    seen.add(q);todo.append(q)
        components.append(component)
    if not components:return None
    ys,xs=zip(*max(components,key=len))
    return [min(xs)*16+7.5,min(ys)*16+7.5,max(xs)*16+7.5,max(ys)*16+7.5]


def fit(result=RESULT, full_batch=False):
    import torch
    import torch.nn.functional as F
    rows=json.loads((RESULT/'cases.json').read_text())
    steps,rate,batch_size=(1000,.0003,84) if full_batch else (400,.003,8)
    if result!=RESULT:
        result.mkdir(parents=True,exist_ok=False)
        plan=json.loads((RESULT/'plan.json').read_text())
        plan.update(created_utc=datetime.now(timezone.utc).isoformat(),role='Follow-up fitting diagnostic after the initial head had poor training fit; same cached inputs and initialization, different optimizer budget. No independent acceptance.',source_cases=str((RESULT/'cases.json').relative_to(ROOT)))
        plan['optimization'].update(steps=steps,batch_size=batch_size,lr=rate,full_batch=full_batch)
        (result/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    spatial=torch.load(SPATIAL_CACHE/'features.pt',map_location='cpu',weights_only=True)
    params=torch.load(SPATIAL_CACHE/'readout.pt',map_location='cpu',weights_only=True)
    question=torch.load(CACHE/'questions.pt',map_location='cpu',weights_only=True)
    train_idx=[i for i,r in enumerate(rows) if r['split']=='train']
    q=question['hidden'].float();qm=q[train_idx].mean(0);qs=q[train_idx].std(0).clamp_min(1e-6)
    q=((q-qm)/qs).to('mps')
    visual=((spatial['features'].float()-params['mean'])/params['std']).to('mps')
    image_idx=torch.tensor(question['image_indices'],device='mps')
    truth=np.stack([target_grid(r) for r in rows]);labels=torch.tensor(truth,dtype=torch.float32,device='mps')
    pos_weight=(1-labels[train_idx]).sum()/labels[train_idx].sum()
    torch.manual_seed(10420)
    class Readout(torch.nn.Module):
        def __init__(self):
            super().__init__();self.v=torch.nn.Linear(1536,32);self.q=torch.nn.Linear(1536,32)
            self.bias=torch.nn.Parameter(torch.zeros(()))
        def forward(self,v,q):return (self.v(v)*self.q(q)[:,None]).sum(-1)/math.sqrt(32)+self.bias
    head=Readout().to('mps')
    opt=torch.optim.AdamW(head.parameters(),lr=rate,weight_decay=.01)
    generator=torch.Generator().manual_seed(10420);training=torch.tensor(train_idx)
    start=time.perf_counter()
    with (result/'training.jsonl').open('w') as log:
        for step in range(steps):
            idx=(training if full_batch else training[torch.randint(len(training),(batch_size,),generator=generator)]).to('mps')
            logits=head(visual[image_idx[idx]],q[idx])
            loss=F.binary_cross_entropy_with_logits(logits,labels[idx],pos_weight=pos_weight)
            opt.zero_grad();loss.backward();opt.step()
            if (step+1)%25==0:
                log.write(json.dumps(dict(step=step+1,loss=float(loss.detach())))+'\n');log.flush()
    torch.mps.synchronize();elapsed=time.perf_counter()-start
    groups=defaultdict(list)
    for i,r in enumerate(rows):groups[r['group_id']].append(i)
    swapped=list(range(len(rows)))
    for group in groups.values():
        for a,b in zip(group,group[1:]+group[:1]):swapped[a]=b
    with torch.no_grad():
        v=head.v(visual);query=head.q(q)
        correct=torch.sigmoid((v[image_idx]*query[:,None]).sum(-1)/math.sqrt(32)+head.bias).cpu().numpy()>=.5
        swapped_masks=torch.sigmoid((v[image_idx]*query[swapped,None]).sum(-1)/math.sqrt(32)+head.bias).cpu().numpy()>=.5
    all_ink={r['image']:r['predicted_ink_cells'] for r in map(json.loads,(SPATIAL_RESULT/'predictions.jsonl').read_text().splitlines()) if r['condition']=='visual_tokens'}
    all_masks=np.zeros_like(truth)
    for i,r in enumerate(rows):all_masks[i,all_ink[r['image']]]=True
    records=[];summaries={}
    for condition,prediction in [('question_conditioned',correct),('swapped_question',swapped_masks),('all_ink',all_masks)]:
        for split in ('train','dev'):
            selected=[];group_values=defaultdict(list)
            for i,r in enumerate(rows):
                if r['split']!=split:continue
                m=metrics(prediction[i],truth[i]);box=mask_box(prediction[i])
                errors=[abs(a-b) for a,b in zip(box,r['expected_box'])] if box else None
                hit=box is not None and max(errors)<=12
                record=dict(**r,condition=condition,**m,predicted_box=box,coordinate_errors=errors,within_12px=hit,
                            predicted_ink_cells=np.flatnonzero(prediction[i]).tolist(),truth_ink_cells=np.flatnonzero(truth[i]).tolist())
                records.append(record);selected.append(record);group_values[r['group_id']].append(int(hit))
            summaries[f'{condition}/{split}']=dict(targets=len(selected),groups=len(group_values),
                hits=sum(r['within_12px'] for r in selected),empty=sum(r['predicted_box'] is None for r in selected),
                macro_iou=sum(r['iou'] for r in selected)/len(selected),macro_f1=sum(r['f1'] for r in selected)/len(selected),
                hit_cluster_bootstrap_95=interval(group_values))
    comparisons={}
    base=[r for r in records if r['condition']=='question_conditioned' and r['split']=='dev']
    for control in ('swapped_question','all_ink'):
        other={r['sample_id']:r for r in records if r['condition']==control and r['split']=='dev'}
        values=defaultdict(list)
        for r in base:values[r['group_id']].append(int(r['within_12px'])-int(other[r['sample_id']]['within_12px']))
        comparisons[control]=dict(hit_difference=sum(map(sum,values.values()))/len(base),paired_cluster_bootstrap_95=interval(values))
    torch.save(dict(state_dict={k:v.cpu() for k,v in head.state_dict().items()},qmean=qm,qstd=qs,
                    vmean=params['mean'],vstd=params['std']),CACHE/('readout_fit.pt' if full_batch else 'readout.pt'))
    report=dict(finished_utc=datetime.now(timezone.utc).isoformat(),head_parameters=sum(p.numel() for p in head.parameters()),
        umm_updated_parameters=0,training_seconds=elapsed,optimization=dict(steps=steps,learning_rate=rate,batch_size=batch_size,full_batch=full_batch),positive_weight=float(pos_weight),metrics=summaries,paired_dev_comparisons=comparisons,
        limitation='Added supervised spatial head; existing simple-shape development groups, fixed target words; not autonomous language-coordinate generation or H1 acceptance.')
    (result/'score.json').write_text(json.dumps(report,indent=2)+'\n')
    (result/'predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    print(json.dumps(report,indent=2))

def diagnose(result):
    """Separate mask errors and component selection without rerunning the model."""
    rows=[r for r in map(json.loads,(result/'predictions.jsonl').read_text().splitlines()) if r['condition']=='question_conditioned']
    report=dict(role='Post-hoc decoder diagnosis at the unchanged 0.5 mask threshold; oracle grid uses scoring labels and is not a model result.',splits={},cases=[])
    for split in ('train','dev'):
        totals=dict(n=0,largest_component_hits=0,all_foreground_hits=0,oracle_grid_hits=0,largest_only_hits=0,union_only_hits=0)
        for r in rows:
            if r['split']!=split:continue
            rec=dict(sample_id=r['sample_id'],split=split,largest_component_hit=r['within_12px'])
            for key,field in [('all_foreground','predicted_ink_cells'),('oracle_grid','truth_ink_cells')]:
                ys,xs=divmod(np.array(r[field]),27)
                box=[float(xs.min()*16+7.5),float(ys.min()*16+7.5),float(xs.max()*16+7.5),float(ys.max()*16+7.5)] if len(xs) else None
                hit=box is not None and max(abs(a-b) for a,b in zip(box,r['expected_box']))<=12
                rec[key+'_box']=box;rec[key+'_hit']=bool(hit);totals[key+'_hits']+=int(hit)
            totals['n']+=1;totals['largest_component_hits']+=int(r['within_12px'])
            totals['largest_only_hits']+=int(r['within_12px'] and not rec['all_foreground_hit'])
            totals['union_only_hits']+=int(not r['within_12px'] and rec['all_foreground_hit'])
            report['cases'].append(rec)
        report['splits'][split]=totals
    (result/'decoder_diagnosis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(report['splits'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['build','extract','fit','diagnose'])
    p.add_argument('--output',type=Path,default=RESULT)
    p.add_argument('--full-batch',action='store_true')
    args=p.parse_args()
    if args.command=='fit': fit(args.output,args.full_batch)
    elif args.command=='diagnose': diagnose(args.output)
    else: {'build':build,'extract':extract}[args.command]()
