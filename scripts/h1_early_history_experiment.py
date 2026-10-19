"""T6 one shared spatial adaptation and two fixed-budget heads, no search."""
import argparse,copy,json,time
from collections import OrderedDict
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from h1_event_data import ROOT,save
from h1_event_model import StrokeGrounding,InkChange,EventState,mask_loss,rule_action
from h1_event_train import grid,event_inputs,decode_state
from h1_event_observe import masks_for
from h1_early_history_data import DATA,OUT,WEIGHTS,DECISIONS
from h1_early_history_io import prepare_group,model_input,normalization
from h1_event_ledger import EventLedger

def rows():return json.loads((DATA/'cases.json').read_text())
def shared_modules(path=None):
    state=torch.load(path or WEIGHTS/'spatial_best.pt',map_location='cpu',weights_only=True)
    a=StrokeGrounding();b=InkChange();a.load_state_dict(state['a']);b.load_state_dict(state['b'])
    return a.eval(),b.eval()

class SpatialData:
    """Keep four geometry shards; construct only the requested reference/frame tensors."""
    def __init__(self):
        self.rows=rows();self.cache=OrderedDict();self.grids={};self.masks={}
        for r in self.rows:
            if r['split'] not in ['train','dev']:continue
            ink=np.stack([np.asarray(Image.open(ROOT/p))[:,:,0]<128 for p in r['frames']]);prev=np.concatenate([np.zeros_like(ink[:1]),ink[:-1]])
            self.grids[r['id']]=torch.stack([grid(ink),grid(ink&~prev),grid(prev&~ink)],1)
            if r['group'] not in self.masks:self.masks[r['group']]=grid(masks_for(r))
    def get(self,r,t):
        g=r['group']
        if g not in self.cache:
            meta=json.loads((OUT/'feature_manifests'/f'{g}.json').read_text());mean,std,_=normalization()
            f=torch.load(ROOT/meta['shard'],map_location='cpu',weights_only=True)['features'].float()
            self.cache[g]=((f-mean)/std,meta['index'])
            if len(self.cache)>4:self.cache.popitem(last=False)
        self.cache.move_to_end(g);f,idx=self.cache[g]
        return (f[idx[r['reference']]],f[idx[r['frames'][t-1]]],f[idx[r['frames'][t]]],
            torch.tensor(r['query']['kinds']),torch.tensor(r['query']['hints']),self.masks[g],self.grids[r['id']][t])
    def batch(self,pairs):return [torch.stack(v) for v in zip(*(self.get(r,t) for r,t in pairs))]

def spatial_loss(a,b,batch):
    ref,prev,cur,kinds,hints,target,change=batch;mask,conf=a(ref,kinds,hints);prob=mask.detach().sigmoid();inter=(prob*target).sum(-1)
    quality=inter/(prob.sum(-1)+target.sum(-1)-inter).clamp_min(1e-6)
    return mask_loss(mask,target)+mask_loss(b(prev,cur,change[:,1:]),change)+.1*F.binary_cross_entropy_with_logits(conf,quality)

def spatial():
    if (WEIGHTS/'spatial_best.pt').exists():raise FileExistsError('Shared fit already exists; do not retrain')
    assert json.loads((OUT/'data_contract_checks.json').read_text())['zero_training_gate']
    torch.set_num_threads(4);torch.manual_seed(42);data=SpatialData();a,b=shared_modules(ROOT/'checkpoints/h1_event_v3/T4/spatial_best.pt')
    needs=json.loads((OUT/'old_spatial_coverage.json').read_text())['requires_single_shared_fit']
    if not needs:
        torch.save(dict(a=a.state_dict(),b=b.state_dict()),WEIGHTS/'spatial_best.pt');return
    opt=torch.optim.AdamW(list(a.parameters())+list(b.parameters()),lr=.001,weight_decay=.01)
    train=[(r,t) for r in data.rows if r['split']=='train' for t in range(1,len(r['frames']))]
    dev=[(r,t) for r in data.rows if r['split']=='dev' for t in range(1,len(r['frames']))]
    rng=torch.Generator().manual_seed(42);best=float('inf');history=[];start=time.perf_counter()
    for epoch in range(12):
        a.train();b.train();indices=torch.randperm(len(train),generator=rng).tolist();total=0
        for offset in range(0,len(indices),8):
            chosen=indices[offset:offset+8];opt.zero_grad();loss=spatial_loss(a,b,data.batch([train[i] for i in chosen]));loss.backward()
            if epoch==0 and offset==0:save(OUT/'spatial_first_gradients.json',{prefix+'.'+n:float(p.grad.norm()) if p.grad is not None else None for prefix,m in [('A',a),('B',b)] for n,p in m.named_parameters()})
            if not torch.isfinite(loss):raise RuntimeError('Nonfinite spatial loss; stop')
            opt.step();total+=float(loss.detach())*len(chosen)
        a.eval();b.eval();validation=0
        with torch.no_grad():
            for offset in range(0,len(dev),8):
                batch=dev[offset:offset+8];validation+=float(spatial_loss(a,b,data.batch(batch)))*len(batch)
        validation/=len(dev);history.append(dict(epoch=epoch+1,train_loss=total/len(train),dev_loss=validation,seconds=time.perf_counter()-start));save(OUT/'spatial_training.json',history)
        if validation<best:best=validation;selected=epoch+1;best_state=copy.deepcopy((a.state_dict(),b.state_dict()))
    torch.save(dict(a=a.state_dict(),b=b.state_dict()),WEIGHTS/'spatial_final.pt')
    torch.save(dict(a=best_state[0],b=best_state[1]),WEIGHTS/'spatial_best.pt')
    save(OUT/'spatial_run.json',dict(initial='T4/spatial_best.pt',epochs=12,selected_epoch=selected,updates=12*((len(train)+7)//8),frame_exposures=12*len(train),parameters=sum(p.numel() for m in [a,b] for p in m.parameters()),seconds=time.perf_counter()-start))

def compact():
    if (WEIGHTS/'compact.pt').exists():raise FileExistsError('Compact inputs already exist')
    torch.set_num_threads(4);a,b=shared_modules();a.requires_grad_(False);b.requires_grad_(False);all_items=[];spatial_records=[]
    for group in sorted({r['group'] for r in rows()}):
        for x in prepare_group(group):
            with torch.no_grad():
                inp=event_inputs(model_input(x),a,b);oracle=event_inputs(model_input(x,True),a,b,oracle=True)
                mask,conf=a(x['reference'][None],x['kinds'][None],x['hints'][None]);pred=mask[0].sigmoid()>.5;truth=x['masks']>.25
                iou=(pred&truth).sum(-1)/(pred|truth).sum(-1).clamp_min(1)
            spatial_records.append(dict(id=x['row']['id'],split=x['row']['split'],group=group,ious=iou.tolist(),confidence=conf[0].sigmoid().tolist()))
            keep=['row','progress','state','onsets','confidence','orders','direction','active','start','complete','truth_states','truth']
            all_items.append(dict(**{k:x[k] for k in keep},inputs=inp,oracle_inputs=oracle))
    torch.save(all_items,WEIGHTS/'compact.pt')
    # Test spatial scores stay locked until both temporal heads have selected their checkpoints.
    torch.save(spatial_records,WEIGHTS/'spatial_scores_locked.pt')
    checks=[];by={x['row']['id']:x for x in all_items}
    for g in sorted({r['group'] for r in rows()}):
        for name in ['swap1','swap2'] if len(next(r for r in rows() if r['group']==g)['strokes'])==5 else ['swap1']:
            a,b=by[g+'-correct'],by[g+'-'+name]
            for t in DECISIONS:
                assert torch.equal(a['inputs'][t-7:t+1],b['inputs'][t-7:t+1]);checks.append(dict(group=g,pair=name,t=t,exact=True))
    save(OUT/'shared_spatial_input_checks.json',checks)

def sequence_loss(o,batch):
    """All methods see the same 23 supervised times; ties carry no unique order label."""
    sl=slice(1,None)
    event=F.cross_entropy(o['state'][:,sl].reshape(-1,3),batch['state'][:,sl].reshape(-1))
    event+=F.cross_entropy(o['direction'][:,sl].reshape(-1,3),batch['direction'][:,sl].reshape(-1))
    event+=.5*F.cross_entropy(o['active'][:,sl].reshape(-1,o['active'].shape[-1]),batch['active'][:,sl].reshape(-1))
    for key in ['start','complete','confidence']:event+=F.binary_cross_entropy_with_logits(o[key][:,sl],batch[key][:,sl])
    onset=batch['onsets'][:,sl];score=o['order'][:,sl];q=score.shape[-1];terms=[]
    for i in range(q):
        for j in range(i+1,q):
            valid=(onset[:,:,i]>=0)&(onset[:,:,j]>=0)&(onset[:,:,i]!=onset[:,:,j])
            logits=torch.stack([score[:,:,i],score[:,:,j]],-1);target=(onset[:,:,i]>onset[:,:,j]).long()
            terms.append(F.cross_entropy(logits.reshape(-1,2),target.reshape(-1),reduction='none').reshape_as(valid)*valid)
    # Per-time pair average, then mean over videos/times, matching the original loss.
    counts=sum(((onset[:,:,i]>=0)&(onset[:,:,j]>=0)&(onset[:,:,i]!=onset[:,:,j])).float() for i in range(q) for j in range(i+1,q))
    order=(sum(terms)/counts.clamp_min(1)).mean()
    return event+.5*order+.5*F.smooth_l1_loss(o['progress'][:,sl],batch['progress'][:,sl])

def tensor_batch(items):
    return {k:torch.stack([x[k] for x in items]) for k in ['inputs','state','direction','active','start','complete','confidence','onsets','progress']}

def heads():
    if any((WEIGHTS/(n+'_best.pt')).exists() for n in ['M1','M2']):raise FileExistsError('Selected head exists; no retraining')
    torch.set_num_threads(4);items=torch.load(WEIGHTS/'compact.pt',weights_only=False);train=[x for x in items if x['row']['split']=='train'];dev=[x for x in items if x['row']['split']=='dev']
    torch.manual_seed(42);initial=copy.deepcopy(EventState().state_dict())
    for name,temporal in [('M1',False),('M2',True)]:
        torch.manual_seed(42);model=EventState(temporal=temporal);own=model.state_dict();model.load_state_dict({k:initial[k] if k in initial and initial[k].shape==v.shape else v for k,v in own.items()})
        opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01);rng=torch.Generator().manual_seed(42);best=float('inf');history=[];start=time.perf_counter()
        for epoch in range(12):
            model.train();order=torch.randperm(len(train),generator=rng).tolist();total=0
            for offset in range(0,len(order),8):
                chosen=order[offset:offset+8];batch=tensor_batch([train[i] for i in chosen]);opt.zero_grad();loss=sequence_loss(model(batch['inputs']),batch);loss.backward()
                if epoch==0 and offset==0:save(OUT/(name+'_first_gradients.json'),{n:float(p.grad.norm()) if p.grad is not None else None for n,p in model.named_parameters()})
                if not torch.isfinite(loss):raise RuntimeError('Nonfinite temporal loss; stop')
                opt.step();total+=float(loss.detach())*len(chosen)
            model.eval();validation=0
            with torch.no_grad():
                for offset in range(0,len(dev),8):
                    chosen=dev[offset:offset+8];batch=tensor_batch(chosen);validation+=float(sequence_loss(model(batch['inputs']),batch))*len(chosen)
            validation/=len(dev);history.append(dict(epoch=epoch+1,train_loss=total/len(train),dev_loss=validation,seconds=time.perf_counter()-start));save(OUT/(name+'_training.json'),history)
            if validation<best:best=validation;selected=epoch+1;best_state=copy.deepcopy(model.state_dict())
        torch.save(model.state_dict(),WEIGHTS/(name+'_final.pt'));torch.save(best_state,WEIGHTS/(name+'_best.pt'))
        save(OUT/(name+'_run.json'),dict(seed=42,epochs=12,selected_epoch=selected,updates=12*((len(train)+7)//8),video_exposures=12*len(train),supervised_state_times=12*len(train)*23,parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0,seconds=time.perf_counter()-start))

def partial_fields(state):
    order=state['event_order'];seen=state['observed_ids']
    state.update(onset_intervals={},confirmed_precedence=[[a,b] for i,a in enumerate(order or []) for b in (order or [])[i+1:]],
        unresolved_order_groups=[seen] if order is None and seen else [],uncertainty_reason='history_not_identified' if order is None else None,
        recovery='requires_missing_past_observations' if order is None else None)
    return state

def record(x,t,state,method,elapsed=0):
    truth=x['truth_states'][t]
    return dict(method=method,id=x['row']['id'],group=x['row']['group'],family=x['row']['family'],split=x['row']['split'],variant=x['row']['variant'],q=len(x['row']['strokes']),t=t,timestamp=x['row']['timestamps'][t],
        prediction=state,truth=truth,truth_geometry=x['state'][t].tolist(),truth_progress=x['progress'][t].tolist(),truth_decision=x['truth'][t],order_correct=state['event_order']==truth['event_order'],
        decision_correct=state['decision']==x['truth'][t],inference_seconds=elapsed)

def evaluate():
    assert all((WEIGHTS/(n+'_best.pt')).exists() for n in ['M1','M2'])
    if (OUT/'predictions.jsonl').exists():raise FileExistsError('Locked test was evaluated already')
    torch.set_num_threads(4);items=torch.load(WEIGHTS/'compact.pt',weights_only=False);models={}
    for name,temporal in [('M1',False),('M2',True)]:
        m=EventState(temporal=temporal);m.load_state_dict(torch.load(WEIGHTS/(name+'_best.pt'),weights_only=True));models[name]=m.eval()
    save(OUT/'test_unlock.json',dict(checkpoints_selected={n:json.loads((OUT/(n+'_run.json')).read_text())['selected_epoch'] for n in models},timestamp=time.time(),additional_training_permitted=False))
    raw=open(OUT/'raw_model_outputs.jsonl','w');history=open(OUT/'history_predictions.jsonl','w');predictions=[];timings={};constraints=[]
    with torch.no_grad():
        for x in items:
            if x['row']['split'] not in ['test','diagnostic']:continue
            outputs={}
            for method,model in models.items():
                begin=time.perf_counter();o=model(x['inputs'][None]);seconds=time.perf_counter()-begin;outputs[method]=o
                timings.setdefault(method,[]).append(seconds)
                for t in DECISIONS:
                    current=x['inputs'][t:t+1] if method=='M1' else x['inputs'][:t+1]
                    begin_query=time.perf_counter();model(current[None]);timings.setdefault(method+'_per_query',[]).append(time.perf_counter()-begin_query)
                raw.write(json.dumps(dict(method=method,id=x['row']['id'],outputs={k:v[0].tolist() for k,v in o.items()}))+'\n')
                for t in range(1,24):
                    s=partial_fields(decode_state(o,x,t));r=record(x,t,s,method,seconds/23);history.write(json.dumps(r)+'\n')
                    if t in DECISIONS:predictions.append(r)
            # M4 uses only local M1 predictions and shared B new-ink inputs.
            ledger=EventLedger(len(x['row']['strokes']));o=outputs['M1'];begin=time.perf_counter()
            for t in range(24):
                update_start=time.perf_counter()
                s=decode_state(o,x,t);presence=(1-o['state'][0,t].softmax(-1)[:,0]).tolist()
                state=ledger.update(t,presence,s['progress'],s['geometry_state'],s['direction'],x['inputs'][t,:,193].tolist())
                timings.setdefault('M4_incremental_without_head',[]).append(time.perf_counter()-update_start)
                r=record(x,t,state,'M4');history.write(json.dumps(r)+'\n')
                if t in DECISIONS:predictions.append(r)
            timings.setdefault('M4_update_only',[]).append(time.perf_counter()-begin)
            for window in [4,8]:
                name='M3_K'+str(window)
                for t in DECISIONS:
                    inp=x['inputs'][max(0,t-window+1):t+1];begin=time.perf_counter();o=models['M2'](inp[None]);seconds=time.perf_counter()-begin
                    raw.write(json.dumps(dict(method=name,id=x['row']['id'],t=t,window_start=max(0,t-window+1),outputs={k:v[0].tolist() for k,v in o.items()}))+'\n')
                    state=partial_fields(decode_state(o,x,len(inp)-1));predictions.append(record(x,t,state,name,seconds));timings.setdefault(name,[]).append(seconds)
            for name,base in [('M2_oracle_region','M2'),('M4_oracle_region','M1')]:
                o=models[base](x['oracle_inputs'][None])
                raw.write(json.dumps(dict(method=name,id=x['row']['id'],outputs={k:v[0].tolist() for k,v in o.items()}))+'\n')
                ledger=EventLedger(len(x['row']['strokes']))
                for t in range(24):
                    state=decode_state(o,x,t)
                    if base=='M1':state=ledger.update(t,(1-o['state'][0,t].softmax(-1)[:,0]).tolist(),state['progress'],state['geometry_state'],state['direction'],x['oracle_inputs'][t,:,193].tolist())
                    else:state=partial_fields(state)
                    if t in DECISIONS:predictions.append(record(x,t,state,name))
    raw.close();history.close()
    # Oracle predictions use only actual-observation-derived labels, never hidden source ordering.
    oracle={r['id']:{} for r in json.loads((OUT/'oracle_ledger_predictions.json').read_text())}
    for r in json.loads((OUT/'oracle_ledger_predictions.json').read_text()):oracle[r['id']][r['t']]=r['prediction']
    pixels={(r['id'],r['t']):r['state'] for r in json.loads((OUT/'pixel_states.json').read_text())}
    for x in items:
        if x['row']['split'] not in ['test','diagnostic']:continue
        for t in DECISIONS:
            s=copy.deepcopy(pixels[x['row']['id'],t]);s['geometry_state']=[2 if p>.985 else 1 if p>.02 else 0 for p in s['progress']]
            s['observation_confidence']=float(s['event_order'] is not None);s['pen_lift_evidence']='unknown';s['decision']=rule_action(s,list(range(len(s['progress']))));s['recovery']='requires_missing_past_observations' if s['event_order'] is None else None
            predictions.append(record(x,t,s,'M0'));predictions.append(record(x,t,oracle[x['row']['id']][t],'M5'))
    with (OUT/'predictions.jsonl').open('w') as f:
        for p in predictions:f.write(json.dumps(p)+'\n')
    spatial=torch.load(WEIGHTS/'spatial_scores_locked.pt',weights_only=False);save(OUT/'spatial_predictions.json',spatial)
    save(OUT/'timing.json',{k:dict(mean_seconds=float(np.mean(v)),n=len(v),scope='cached head / ledger only; excludes UMM encoding and shared A+B') for k,v in timings.items()})
    # Deterministic local/window predictions must agree for every strict local-input pair.
    by={(r['method'],r['id'],r['t']):r for r in predictions}
    for g in sorted({x['row']['group'] for x in items if x['row']['split'] in ['test','diagnostic']}):
        for v in ['swap1','swap2'] if 'san' not in g else ['swap1']:
            for method in ['M1','M3_K4','M3_K8']:
                for t in DECISIONS:
                    same=by[method,g+'-correct',t]['prediction']==by[method,g+'-'+v,t]['prediction'];assert same
                    constraints.append(dict(group=g,variant=v,method=method,t=t,prediction_equal=same))
    save(OUT/'deterministic_input_constraint.json',constraints)
    save(OUT/'run_config.json',dict(preregistration='preregistration.json',weights='checkpoints/h1_early_history_v1',shared_spatial='spatial_best.pt',models=['M0','M1','M2','M3_K4','M3_K8','M4','M5'],oracle_region_diagnostic='same selected weights; no matched oracle retraining',state_times=24,q_main=5,q_diagnostic=3,torch_threads=4,head_device='CPU fp32',UMM='frozen native27 fusion',additional_training=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['spatial','compact','heads','evaluate']);args=p.parse_args();globals()[args.stage]()
