"""Fixed-budget small-fit / temporal experiment, CPU fp32 heads, cached frozen UMM."""
import argparse,json,time,copy
from pathlib import Path
import numpy as np
import torch
from PIL import Image
import torch.nn.functional as F
from h1_event_data import ROOT,DATA,RESULT,save
from h1_event_observe import CACHE,masks_for,pixel_observer
from h1_event_model import StrokeGrounding,InkChange,EventState,mask_loss,rule_action

def grid(pixels):return F.avg_pool2d(torch.as_tensor(pixels.copy(),dtype=torch.float32).reshape(-1,1,432,432),16).reshape(-1,729)

def prepare(rows_path=None,features_path=None,manifest_path=None):
    torch.set_num_threads(4);torch.manual_seed(42)
    feats=torch.load(features_path or CACHE/'probe_features.pt',map_location='cpu',weights_only=True)['features'].float()
    index=json.loads((manifest_path or RESULT/'T2_feature_manifest.json').read_text())['index'];rows=json.loads((rows_path or DATA/'probe.json').read_text());items=[]
    # Fixed label-free 64-D projection of standardized frozen visual channels.
    normal=torch.load(ROOT/'checkpoints/h1_spatial_probe_v1/readout.pt',map_location='cpu',weights_only=True)
    features=(feats-normal['mean'])/normal['std'];projection=torch.randn(1536,64)/1536**.5
    reduced=features@projection
    for row in rows:
        ids=[index[p] for p in row['frames']];ref=index[row['reference']];n=len(row['strokes'])
        ink=np.stack([np.asarray(Image.open(ROOT/p))[:,:,0]<128 for p in row['frames']]);previous=np.concatenate([np.zeros_like(ink[:1]),ink[:-1]],0)
        current=grid(ink);new=grid(ink&~previous);gone=grid(previous&~ink)
        rgb=torch.stack([new,gone],1);targets=torch.stack([current,new,gone],1)
        hints=[];kinds=[]
        for points in row['strokes']:
            center=np.mean(points,0)/432;hints.append((np.round(center*4)/4*2-1).tolist())
            a,b=points[0],points[-1];kinds.append(3 if len(points)>2 else 1 if a[1]==b[1] else 2 if a[0]==b[0] else 4)
        p=torch.tensor(row['label_progress']);state=torch.where(p==1,2,torch.where(p>0,1,0));starts=(p>0)&~torch.cat([torch.zeros_like(p[:1],dtype=torch.bool),p[:-1]>0]);complete=(p==1)&~torch.cat([torch.zeros_like(p[:1],dtype=torch.bool),p[:-1]==1])
        # Labels use the same observations as the task; merged onsets stay unknown.
        onsets=torch.full((8,n),-1,dtype=torch.long);confidence=[];directions=[];active=[];orders=[];truth=[]
        for t in range(8):
            observed=pixel_observer(row,[Image.open(ROOT/path) for path in row['frames'][:t+1]])
            confidence.append(not observed['unknown']);directions.append([['unknown','forward','reverse'].index(s) for s in observed['direction']]);orders.append(observed['event_order'])
            for j in range(n):
                seen=(p[:t+1,j]>0).nonzero();onsets[t,j]=int(seen[0]) if len(seen) else -1
            changed=torch.nonzero((p[t]-(p[t-1] if t else 0))>0).flatten();active.append(int(changed[0])+1 if len(changed)==1 else 0)
            state_truth=dict(event_order=observed['event_order'],observed_ids=observed['observed_ids'],progress=p[t].tolist(),direction=observed['direction'])
            truth.append(rule_action(state_truth,list(range(n))))
        items.append(dict(row=row,reference=features[ref],visual=features[ids],small=reduced[ids],ref_small=reduced[ref],kinds=torch.tensor(kinds),hints=torch.tensor(hints,dtype=torch.float32),
            masks=grid(masks_for(row)),ink_grid=current,rgb=rgb,change=targets,progress=p,state=state,start=starts.float(),complete=complete.float(),
            direction=torch.tensor(directions),active=torch.tensor(active),confidence=torch.tensor(confidence,dtype=torch.float32),onsets=onsets,orders=orders,truth=truth))
    return items

def spatial_metrics(a,b,items):
    a.eval();b.eval();ious=[];dices=[];predictions=[]
    with torch.no_grad():
        for x in items:
            mask,conf=a(x['reference'][None],x['kinds'][None],x['hints'][None]);p=mask[0].sigmoid()>.5;truth=x['masks']>.25
            iou=(p&truth).sum(-1)/(p|truth).sum(-1).clamp_min(1);ious.extend(iou.tolist())
            cur=x['visual'];prev=torch.cat([cur[:1],cur[:-1]],0);out=b(prev,cur,x['rgb']).sigmoid()
            dice=(2*(out[:,1]*x['change'][:,1]).sum(-1)+1)/(out[:,1].sum(-1)+x['change'][:,1].sum(-1)+1);dices.extend(dice.tolist())
            predictions.append(dict(id=x['row']['id'],mask_iou=iou.tolist(),confidence=conf[0].sigmoid().tolist(),change_new_dice=dice.tolist()))
    return dict(instance_match_rate=sum(v>=.5 for v in ious)/len(ious),mean_iou=float(np.mean(ious)),new_soft_dice=float(np.mean(dices)),predictions=predictions)

def spatial(items,folder):
    a=StrokeGrounding();b=InkChange();optimizer=torch.optim.AdamW(list(a.parameters())+list(b.parameters()),lr=.001,weight_decay=.01)
    train=[x for x in items if x['row']['group']!='diagonal'];dev=[x for x in items if x['row']['group']=='diagonal']
    history=[];best=float('inf');patience=0;start=time.perf_counter();generator=torch.Generator().manual_seed(42)
    def loss_one(x,t):
        mask,_=a(x['reference'][None],x['kinds'][None],x['hints'][None]);cur=x['visual'][t:t+1];prev=x['visual'][max(0,t-1):max(0,t-1)+1]
        change=b(prev,cur,x['rgb'][t:t+1]);return mask_loss(mask,x['masks'][None])+mask_loss(change,x['change'][t:t+1])
    pairs=[(i,t) for i in range(len(train)) for t in range(1,8)]
    for epoch in range(12):
        a.train();b.train();total=0;order=torch.randperm(len(pairs),generator=generator).tolist()
        for offset in range(0,len(order),8):
            optimizer.zero_grad();chosen=order[offset:offset+8];loss=sum(loss_one(train[pairs[k][0]],pairs[k][1]) for k in chosen)/len(chosen)
            loss.backward();optimizer.step();total+=float(loss.detach())*len(chosen)
        a.eval();b.eval()
        with torch.no_grad():validation=float(torch.stack([loss_one(x,t) for x in dev for t in [2,4,7]]).mean())
        history.append(dict(epoch=epoch+1,train_loss=total/len(pairs),dev_loss=validation,seconds=time.perf_counter()-start))
        save(folder/'spatial_training.json',history)
        if validation<best:best=validation;patience=0;best_state=copy.deepcopy((a.state_dict(),b.state_dict()))
        else:patience+=1
        if patience>=3:break
    # Preserve final and dev-selected states; evaluate both rather than overwrite.
    torch.save(dict(a=a.state_dict(),b=b.state_dict()),CACHE/'T3_spatial_final.pt')
    a.load_state_dict(best_state[0]);b.load_state_dict(best_state[1]);torch.save(dict(a=a.state_dict(),b=b.state_dict()),CACHE/'T3_spatial_best.pt')
    metrics=dict(train=spatial_metrics(a,b,train),dev=spatial_metrics(a,b,dev),parameters=sum(p.numel() for p in a.parameters())+sum(p.numel() for p in b.parameters()),umm_updated_parameters=0,epochs=len(history))
    metrics['fit_pass']=metrics['train']['instance_match_rate']>=.9 and metrics['train']['new_soft_dice']>=.7
    save(folder/'spatial_metrics.json',metrics)
    return a,b,metrics

def event_inputs(x,a,b,oracle=False,whole=False,no_delta=False):
    with torch.no_grad():
        logits,_=a(x['reference'][None],x['kinds'][None],x['hints'][None]);mask=x['masks'] if oracle else logits[0].sigmoid()
        if whole:mask=torch.ones_like(mask)
        weights=mask/mask.sum(-1,keepdim=True).clamp_min(1e-6)
        cur=x['small'];prev=torch.cat([cur[:1],cur[:-1]],0);ref=x['ref_small']
        c=torch.einsum('qp,tpd->tqd',weights,cur);d=torch.einsum('qp,tpd->tqd',weights,cur-prev);r=torch.einsum('qp,tpd->tqd',weights,ref[None]-cur)
        visual=x['visual']
        change=b(visual,visual,torch.zeros_like(x['rgb'])).sigmoid() if no_delta else b(torch.cat([visual[:1],visual[:-1]],0),visual,x['rgb']).sigmoid()
        delta=torch.einsum('qp,tcp->tqc',weights,change)
        if no_delta:d.zero_();delta[:,:,1:]=0
        times=torch.tensor(x['row']['indices'],dtype=torch.float32)/24
        # 64 current + 64 adjacent change +64 reference difference +3 ink +1 time
        return torch.cat([c,d,r,delta,times[:,None,None].expand(-1,len(mask),1)],-1)

def temporal_loss(output,x,t,progress=True):
    event=F.cross_entropy(output['state'][0,t],x['state'][t])+F.cross_entropy(output['direction'][0,t],x['direction'][t])
    event=event+.5*F.cross_entropy(output['active'][0,t:t+1],x['active'][t:t+1])+F.binary_cross_entropy_with_logits(output['start'][0,t],x['start'][t])+F.binary_cross_entropy_with_logits(output['complete'][0,t],x['complete'][t])+F.binary_cross_entropy_with_logits(output['confidence'][0,t],x['confidence'][t])
    onset=x['onsets'][t];pairs=[(i,j) for i in range(len(onset)) for j in range(i+1,len(onset)) if min(onset[i],onset[j])>=0 and onset[i]!=onset[j]]
    order=torch.stack([F.cross_entropy(torch.stack([output['order'][0,t,i],output['order'][0,t,j]])[None],torch.tensor([int(onset[i]>onset[j])])) for i,j in pairs]).mean() if pairs else event*0
    return event+.5*order+(.5*F.smooth_l1_loss(output['progress'][0,t],x['progress'][t]) if progress else 0)

def decode_state(output,x,t):
    classes=output['state'][0,t].argmax(-1);seen=classes.nonzero().flatten().tolist();confidence=float(output['confidence'][0,t].sigmoid());order=sorted(seen,key=lambda j:float(output['order'][0,t,j]),reverse=True) if confidence>=.5 else None
    direction=[['unknown','forward','reverse'][v] for v in output['direction'][0,t].argmax(-1).tolist()]
    progress=output['progress'][0,t].tolist()
    # Discrete geometry and continuous regression remain separate for evaluation.
    decision_progress=[0. if c==0 else 1. if c==2 else min(.984,max(.001,p)) for c,p in zip(classes.tolist(),progress)]
    state=dict(observed_ids=seen,event_order=order,active_id=int(output['active'][0,t].argmax())-1,progress=progress,geometry_state=classes.tolist(),
        stroke_start=(output['start'][0,t].sigmoid()>.5).tolist(),stroke_complete=(output['complete'][0,t].sigmoid()>.5).tolist(),direction=direction,observation_confidence=confidence,pen_lift_evidence='unknown')
    state['decision']=rule_action(dict(event_order=order,progress=decision_progress,direction=direction),list(range(len(classes))))
    return state

def event_metrics(model,items,inputs):
    records=[];model.eval()
    with torch.no_grad():
        for x,inp in zip(items,inputs):
            output=model(inp[None])
            for t in range(3,8):
                state=decode_state(output,x,t);truth=x['state'][t].tolist();order=x['orders'][t]
                records.append(dict(id=x['row']['id'],group=x['row']['group'],t=t,prediction=state,truth_state=truth,truth_order=order,truth_progress=x['progress'][t].tolist(),
                    order_correct=state['event_order']==order,state_correct=[a==b for a,b in zip(state['geometry_state'],truth)],
                    action_correct=state['decision']==x['truth'][t],progress_mae=float((output['progress'][0,t]-x['progress'][t]).abs().mean())))
    state_values=[v for r in records for v in r['state_correct']];final=[r for r in records if r['t']==7]
    return dict(state_accuracy=sum(state_values)/len(state_values),strict_order=sum(r['order_correct'] for r in records)/len(records),final_order=sum(r['order_correct'] for r in final)/len(final),
        action_accuracy=sum(r['action_correct'] for r in records)/len(records),progress_mae=float(np.mean([r['progress_mae'] for r in records])),records=records)

def temporal(items,a,b,folder,temporal=True,name='B4',epochs=12):
    a.eval().requires_grad_(False);b.eval().requires_grad_(False)
    inputs=[event_inputs(x,a,b) for x in items];train=[i for i,x in enumerate(items) if x['row']['group']!='diagonal'];dev=[i for i,x in enumerate(items) if x['row']['group']=='diagonal']
    torch.manual_seed(42);model=EventState(temporal=temporal);optimizer=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01);rng=torch.Generator().manual_seed(42)
    examples=[(i,t) for i in train for t in range(3,8)];history=[];best=float('inf');patience=0;start=time.perf_counter()
    for epoch in range(epochs):
        model.train();order=torch.randperm(len(examples),generator=rng).tolist();total=0
        for offset in range(0,len(order),8):
            optimizer.zero_grad();chosen=order[offset:offset+8];loss=sum(temporal_loss(model(inputs[examples[k][0]][None]),items[examples[k][0]],examples[k][1]) for k in chosen)/len(chosen)
            loss.backward();optimizer.step();total+=float(loss.detach())*len(chosen)
        model.eval()
        with torch.no_grad():validation=float(torch.stack([temporal_loss(model(inputs[i][None]),items[i],t) for i in dev for t in [3,5,7]]).mean())
        history.append(dict(epoch=epoch+1,train_loss=total/len(examples),dev_loss=validation,seconds=time.perf_counter()-start));save(folder/(name+'_training.json'),history)
        if validation<best:best=validation;patience=0;best_state=copy.deepcopy(model.state_dict())
        else:patience+=1
        if patience>=3:break
    torch.save(model.state_dict(),CACHE/(name+'_final.pt'));model.load_state_dict(best_state);torch.save(model.state_dict(),CACHE/(name+'_best.pt'))
    metrics=dict(train=event_metrics(model,[items[i] for i in train],[inputs[i] for i in train]),dev=event_metrics(model,[items[i] for i in dev],[inputs[i] for i in dev]),epochs=len(history),parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0)
    metrics['fit_pass']=metrics['train']['state_accuracy']>=.85 and metrics['train']['final_order']>=.9
    save(folder/(name+'_metrics.json'),metrics);return model,metrics

def smallfit():
    folder=RESULT/'T3';folder.mkdir(parents=True,exist_ok=True)
    save(folder/'preregistration.json',dict(question='Can the specified A/B/C fit a fixed small D0 set?',seed=42,train_groups=['san','cross','parallel_v','fold'],dev_groups=['diagonal'],
        split_scope='small-fit only; no independent H1 acceptance',UMM='frozen all parameters, same cached 27x27 native path',optimizer='AdamW',lr=.001,weight_decay=.01,batch=8,epochs_max=12,dev_patience=3,selected='minimum dev loss',
        A='256 projection, 2 decoder layers, 4 heads, variable queries <=16',B='current/difference UMM + signed RGB-difference, BCE+Dice',
        C='256 causal, 2 layers, 4 heads, dropout .1; L_event+.5L_pair_order+.5SmoothL1',
        fit_gate=dict(A_instance_IoU50_match=.9,B_new_soft_dice=.7,C_train_state=.85,C_train_final_order=.9),
        stop='No extra steps or parameter search. Stage1 gate fails: do not train C; causal interface tested without fitting. T4 blocked until fit evidence exists.'))
    items=prepare();a,b,spatial_result=spatial(items,folder)
    inp=event_inputs(items[0],a,b);model=EventState();output=model(inp[None]);save(folder/'interface.json',dict(input_shape=list(inp[None].shape),output_shapes={k:list(v.shape) for k,v in output.items()},finite_loss=bool(temporal_loss(output,items[0],7).isfinite()),A_masks=list(a(items[0]['reference'][None],items[0]['kinds'][None],items[0]['hints'][None])[0].shape)))
    if spatial_result['fit_pass']:temporal(items,a,b,folder)
    else:save(folder/'decision.json',dict(status='spatial_fit_failed',C_training='not_started',T4='blocked by fixed small-fit gate',next='Report exact failure; no extra epochs or LoRA.'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['smallfit']);args=parser.parse_args();smallfit()
