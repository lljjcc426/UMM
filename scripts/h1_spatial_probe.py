"""Read coarse ink occupancy from frozen full-UMM visual tokens; no language training."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import time
import numpy as np
from PIL import Image, ImageDraw

from h1_run_showo import ROOT, load_model, StateImageEncoder, MODEL_REVISION, SOURCE_REVISION
from h1_state_gate import interval

RESULT=ROOT/'results/h1/showo2_video_1_5b/spatial_probe_v1'
CACHE=ROOT/'checkpoints/h1_spatial_probe_v1'
SOURCES={'train':ROOT/'data/h1/reference_localization_training_v1',
         'dev':ROOT/'data/h1/reference_localization_v1'}
GRID=27
CELL=16


def ink_grid(path):
    pixels=np.asarray(Image.open(path).convert('RGB'))
    black=(pixels.max(axis=-1)<128)
    return (black.reshape(GRID,CELL,GRID,CELL).sum(axis=(1,3))>=8).reshape(-1)


def build():
    RESULT.mkdir(parents=True,exist_ok=False)
    CACHE.mkdir(parents=True,exist_ok=False)
    rows=[]
    for split,source in SOURCES.items():
        groups={r['group_id']:r for r in json.loads((source/'cases.json').read_text())}
        for gid,row in groups.items():
            rows.append(dict(group_id=gid,split=split,image=str((source/row['image']).relative_to(ROOT))))
    (RESULT/'inputs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),model='showlab/show-o2-1.5B-w-video-und',
        source_revision=SOURCE_REVISION,model_revision=MODEL_REVISION,train_groups=36,dev_groups=12,
        input='Existing complete reference images, one image per geometry; no target names or coordinates.',
        features='729 spatial tokens of 1536 dimensions, after frozen fusion_proj and before language model.',
        grid='27x27, row-major; nominal 16x16 input-pixel cells. A cell is ink if at least 8 pixels have all RGB channels below 128.',
        probe='One shared linear binary readout (1537 parameters), no coordinate input; UMM fully frozen.',
        normalization='Channel mean/std computed on training tokens only; std clamped to 1e-6.',
        optimization=dict(steps=300,batch_size=4096,optimizer='AdamW',lr=.01,weight_decay=.01,seed=10419,
                          loss='Binary cross entropy, positive weight = training negative/positive cell count.'),
        prediction_threshold=.5,
        controls=['Training foreground frequency at each grid position, with same positive weighting and threshold',
                  'Same fitted head on blank-image UMM tokens, preserving spatial indices'],
        metrics='Per-image foreground IoU and F1, macro means and geometry bootstrap; pooled precision/recall. No background accuracy claim.',
        evaluation='Only final head; no dev threshold or checkpoint search. Original visual test unused.',
        interpretation='Coarse all-ink decodability only. No queried instance, completion, coordinate generation, order or H1 acceptance.')
    (RESULT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(plan)


def extract():
    import torch
    started=time.perf_counter()
    assets=ROOT/'checkpoints/Show-o-assets'
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',assets,'cpu')
    model.eval().requires_grad_(False)
    encoder=StateImageEncoder(model,assets,'mps')
    rows=json.loads((RESULT/'inputs.json').read_text())
    values=[];labels=[]
    for row in rows:
        features=encoder.encode(ROOT/row['image']).squeeze(0).cpu()
        if features.shape != (729,1536):
            raise ValueError(f'Unexpected spatial token grid: {features.shape}')
        values.append(features)
        labels.append(torch.from_numpy(ink_grid(ROOT/row['image'])))
    blank=encoder.encode(None).squeeze(0).cpu()
    torch.save(dict(features=torch.stack(values),labels=torch.stack(labels),blank=blank),CACHE/'features.pt')
    metadata=dict(finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.perf_counter()-started,
        full_model_parameters=sum(p.numel() for p in model.parameters()),umm_trainable_parameters=0,
        executed='Frozen Wan VAE CPU fp32; semantic/generative patch embedding, semantic transformer and fusion MPS bf16; language model retained CPU and not executed.',
        features_shape=list(torch.stack(values).shape),blank_shape=list(blank.shape))
    (RESULT/'extraction.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(metadata)


def metrics(pred,truth):
    tp=int((pred&truth).sum());fp=int((pred&~truth).sum());fn=int((~pred&truth).sum())
    return dict(tp=tp,fp=fp,fn=fn,iou=tp/(tp+fp+fn) if tp+fp+fn else 1.,
                f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 1.)


def fit():
    import torch
    import torch.nn.functional as F
    data=torch.load(CACHE/'features.pt',map_location='cpu',weights_only=True)
    rows=json.loads((RESULT/'inputs.json').read_text())
    train_idx=[i for i,r in enumerate(rows) if r['split']=='train']
    train=data['features'][train_idx].float().reshape(-1,1536)
    target=data['labels'][train_idx].float().reshape(-1)
    mean=train.mean(0);std=train.std(0).clamp_min(1e-6)
    x=((train-mean)/std).to('mps');y=target.to('mps')
    pos_weight=(1-target).sum()/target.sum()
    torch.manual_seed(10419)
    head=torch.nn.Linear(1536,1).to('mps')
    optimizer=torch.optim.AdamW(head.parameters(),lr=.01,weight_decay=.01)
    generator=torch.Generator().manual_seed(10419)
    started=time.perf_counter()
    with (RESULT/'training.jsonl').open('w') as log:
        for step in range(300):
            indices=torch.randint(len(x),(4096,),generator=generator).to('mps')
            logits=head(x[indices]).squeeze(-1)
            loss=F.binary_cross_entropy_with_logits(logits,y[indices],pos_weight=pos_weight.to('mps'))
            optimizer.zero_grad();loss.backward();optimizer.step()
            if (step+1)%25==0:
                log.write(json.dumps(dict(step=step+1,loss=float(loss.detach())))+'\n');log.flush()
    torch.mps.synchronize()
    elapsed=time.perf_counter()-started
    head=head.cpu().eval()
    torch.save(dict(state_dict=head.state_dict(),mean=mean,std=std),CACHE/'readout.pt')
    with torch.no_grad():
        probability=torch.sigmoid(head((data['features'].float()-mean)/std).squeeze(-1)).numpy()
        blank_probability=torch.sigmoid(head((data['blank'].float()-mean)/std).squeeze(-1)).numpy()
    frequency=data['labels'][train_idx].float().mean(0).numpy()
    w=float(pos_weight)
    prior_probability=(w*frequency)/(w*frequency+1-frequency)
    conditions={'visual_tokens':probability>=.5,
                'position_prior':np.tile(prior_probability>=.5,(len(rows),1)),
                'blank_tokens':np.tile(blank_probability>=.5,(len(rows),1))}
    truth=data['labels'].numpy()
    scores=[];summary={}
    for name,predictions in conditions.items():
        for split in ('train','dev'):
            selected=[]
            for i,row in enumerate(rows):
                if row['split']!=split:continue
                m=metrics(predictions[i],truth[i]);selected.append(dict(group_id=row['group_id'],**m))
                scores.append(dict(condition=name,**row,**m,truth_ink_cells=np.flatnonzero(truth[i]).tolist(),
                    predicted_ink_cells=np.flatnonzero(predictions[i]).tolist()))
            tp=sum(r['tp'] for r in selected);fp=sum(r['fp'] for r in selected);fn=sum(r['fn'] for r in selected)
            summary[f'{name}/{split}']=dict(images=len(selected),tp=tp,fp=fp,fn=fn,
                pooled_precision=tp/(tp+fp) if tp+fp else 0.,pooled_recall=tp/(tp+fn),
                **{f'macro_{key}':sum(r[key] for r in selected)/len(selected) for key in ('iou','f1')},
                **{f'{key}_cluster_bootstrap_95':interval({r['group_id']:[r[key]] for r in selected}) for key in ('iou','f1')})
    comparisons={}
    for baseline in ('position_prior','blank_tokens'):
        a={r['group_id']:r for r in scores if r['condition']==baseline and r['split']=='dev'}
        b=[r for r in scores if r['condition']=='visual_tokens' and r['split']=='dev']
        comparisons[baseline]={key:dict(mean_difference=sum(r[key]-a[r['group_id']][key] for r in b)/len(b),
            paired_cluster_bootstrap_95=interval({r['group_id']:[r[key]-a[r['group_id']][key]] for r in b})) for key in ('iou','f1')}
    report=dict(finished_utc=datetime.now(timezone.utc).isoformat(),head_parameters=1537,umm_updated_parameters=0,
        training_seconds=elapsed,positive_weight=w,train_foreground_cells=int(target.sum()),train_cells=len(target),
        metrics=summary,paired_dev_comparisons=comparisons,
        limitation='Linear occupancy readout on 12 development geometries; not language grounding or H1 acceptance.')
    (RESULT/'score.json').write_text(json.dumps(report,indent=2)+'\n')
    with (RESULT/'predictions.jsonl').open('w') as out:
        for row in scores:out.write(json.dumps(row,ensure_ascii=False)+'\n')
    # Fixed first development example of each layout; no favorable-example selection.
    chosen=[]
    for prefix in ('parallel_h','parallel_v','cross'):
        chosen.append(next(i for i,r in enumerate(rows) if r['split']=='dev' and r['group_id'].startswith(prefix)))
    panel=Image.new('RGB',(4*222,3*242),'white');draw=ImageDraw.Draw(panel)
    for row_index,i in enumerate(chosen):
        base_y=row_index*242
        original=Image.open(ROOT/rows[i]['image']).resize((216,216))
        panel.paste(original,(0,base_y+22))
        for col,(title,mask) in enumerate([('Truth',truth[i]),('UMM features',conditions['visual_tokens'][i]),('Position prior',conditions['position_prior'][i])],1):
            grid=Image.fromarray(np.where(mask.reshape(27,27),0,255).astype('uint8')).resize((216,216),Image.Resampling.NEAREST).convert('RGB')
            panel.paste(grid,(col*222,base_y+22));draw.text((col*222,base_y+4),title,fill='black')
        draw.text((0,base_y+4),rows[i]['group_id'],fill='black')
    panel.save(RESULT/'examples.png')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['build','extract','fit'])
    args=p.parse_args();{'build':build,'extract':extract,'fit':fit}[args.command]()
