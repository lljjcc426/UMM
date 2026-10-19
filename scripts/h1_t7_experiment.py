"""T7 fixed A-only training; subsequent stages use frozen selected checkpoints."""
import argparse,copy,json,time
import numpy as np
import torch
from h1_event_data import ROOT,save
from h1_event_model import StrokeGrounding,InkChange,EventState
from h1_target_contrast import grounding_loss
from h1_t7_data import OUT,WEIGHTS
from h1_t7_io import reference_examples

def batch(examples):
    return {k:torch.stack([x[k] for x in examples]) for k in ['reference','kinds','hints','target','exclusive','shared']}

def batches(examples,repeat=1,generator=None):
    result=[]
    for q in [3,5]:
        group=[x for x in examples if x['q']==q]*repeat
        order=torch.randperm(len(group),generator=generator).tolist() if generator else list(range(len(group)))
        result.extend([[group[i] for i in order[k:k+8]] for k in range(0,len(order),8)])
    return result

def modules(name=None):
    old=torch.load(ROOT/'checkpoints/h1_early_history_v1/spatial_best.pt',weights_only=True)
    a,b,m=StrokeGrounding(),InkChange(),EventState(temporal=False)
    a.load_state_dict(torch.load(WEIGHTS/(name+'_best.pt'),weights_only=True) if name else old['a'])
    b.load_state_dict(old['b']);m.load_state_dict(torch.load(ROOT/'checkpoints/h1_early_history_v1/M1_best.pt',weights_only=True))
    for model in [a,b,m]:model.eval().requires_grad_(False)
    return a,b,m

def mask_record(model,x):
    with torch.no_grad():
        logits,conf=model(x['reference'][None],x['kinds'][None],x['hints'][None])
        pred=logits[0].sigmoid()>.5;truth=x['target']>.25
        iou=(pred[:,None]&truth[None]).sum(-1)/(pred[:,None]|truth[None]).sum(-1).clamp_min(1)
        diagonal=iou.diag();identity=[bool(diagonal[j]>torch.cat([iou[j,:j],iou[j,j+1:]]).max()) for j in range(x['q'])]
        shared=(x['shared']>0)[None]&truth
        return dict(group=x['group'],split=x['split'],family=x['family'],q=x['q'],ious=diagonal.tolist(),iou_matrix=iou.tolist(),identity_correct=identity,
            confidence=conf[0].sigmoid().tolist(),shared_instance_correct=int((pred&shared).sum()),shared_instance_total=int(shared.sum()))

def train():
    gate=json.loads((OUT/'data_contract_checks.json').read_text())
    assert gate['training_permitted'] and (OUT/'preregistration.json').exists()
    assert not (OUT/'test_unlock.json').exists()
    if any((WEIGHTS/(n+'_best.pt')).exists() for n in ['A0','A1']):raise FileExistsError('T7 training already selected; no additional fit')
    torch.set_num_threads(4);train=reference_examples('train');dev=reference_examples('dev');WEIGHTS.mkdir(parents=True,exist_ok=True)
    curves={};runs={}
    for name,contrast in [('A0',False),('A1',True)]:
        torch.manual_seed(42);a,b,m=modules();a.requires_grad_(True)
        opt=torch.optim.AdamW(a.parameters(),lr=.001,weight_decay=.01);rng=torch.Generator().manual_seed(42)
        history=[];best=float('inf');start=time.perf_counter();updates=0
        for epoch in range(12):
            a.train();total=np.zeros(3);n=0
            for examples in batches(train,8,rng):
                opt.zero_grad();loss,base,target=grounding_loss(a,batch(examples),contrast);loss.backward()
                if updates==0:save(OUT/(name+'_first_gradients.json'),dict(A={k:float(p.grad.norm()) if p.grad is not None else None for k,p in a.named_parameters()},B_has_gradient=any(p.grad is not None for p in b.parameters()),M1_has_gradient=any(p.grad is not None for p in m.parameters())))
                if not torch.isfinite(loss):raise RuntimeError('Nonfinite A loss')
                opt.step();updates+=1;n+=len(examples);total+=np.array([float(v.detach()) for v in [loss,base,target]])*len(examples)
            a.eval();val=np.zeros(3)
            with torch.no_grad():
                for examples in batches(dev):
                    values=grounding_loss(a,batch(examples),contrast);val+=np.array([float(v) for v in values])*len(examples)
            val/=len(dev);history.append(dict(epoch=epoch+1,train_total=total[0]/n,train_base=total[1]/n,train_target=total[2]/n,dev_total=val[0],dev_base=val[1],dev_target=val[2],seconds=time.perf_counter()-start))
            curves[name]=history;save(OUT/'train_curves.json',curves)
            if val[1]<best:best=float(val[1]);selected=epoch+1;best_state=copy.deepcopy(a.state_dict())
        torch.save(a.state_dict(),WEIGHTS/(name+'_final.pt'));torch.save(best_state,WEIGHTS/(name+'_best.pt'))
        a.load_state_dict(best_state);a.eval();save(OUT/(name+'_dev_masks.json'),[mask_record(a,x) for x in dev])
        runs[name]=dict(selected_epoch=selected,updates=updates,epochs=12,image_exposures=12*8*len(train),parameters=sum(p.numel() for p in a.parameters()),
            B_updated=0,M1_updated=0,UMM_updated=0,seconds=time.perf_counter()-start,selection='minimum common dev_base')
        save(OUT/'training_runs.json',runs)
    assert runs['A0']['updates']==runs['A1']['updates']==480
    save(OUT/'models_frozen.json',dict(A0=runs['A0']['selected_epoch'],A1=runs['A1']['selected_epoch'],further_training=False,timestamp=time.time()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['train']);args=p.parse_args();globals()[args.stage]()
