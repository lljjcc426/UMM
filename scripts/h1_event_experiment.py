"""Execute the single preregistered T4 study; no automatic search or extensions."""
import argparse,copy,json,time
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from h1_event_data import ROOT,save
from h1_event_observe import CACHE,pixel_observer
from h1_event_study import STUDY,OUT
from h1_event_train import prepare,grid,spatial_metrics,event_inputs,temporal_loss,event_metrics,decode_state
from h1_event_model import StrokeGrounding,InkChange,EventState,mask_loss,rule_action
WEIGHTS=CACHE/'T4'
FEATURES=CACHE/'study_features.pt'
MANIFEST=OUT/'feature_manifest.json'
CASES=STUDY/'cases.json'

def pixel_baseline(items):
    records=[]
    for x in items:
        row=x['row']
        for t in range(3,8):
            observed=pixel_observer(row,[Image.open(ROOT/p) for p in row['frames'][:t+1]])
            p=np.array(observed['progress'])[-1];classes=np.where(p>.985,2,np.where(p>.02,1,0)).tolist()
            state=dict(observed_ids=observed['observed_ids'],event_order=observed['event_order'],progress=p.tolist(),geometry_state=classes,direction=observed['direction'],pen_lift_evidence='unknown')
            state['decision']=rule_action(state,list(range(len(p))));records.append(dict(id=row['id'],group=row['group'],t=t,prediction=state,truth_state=x['state'][t].tolist(),truth_order=x['orders'][t],truth_progress=x['progress'][t].tolist(),order_correct=state['event_order']==x['orders'][t],state_correct=[a==b for a,b in zip(classes,x['state'][t].tolist())],action_correct=state['decision']==x['truth'][t],progress_mae=float(np.abs(p-np.array(x['progress'][t])).mean())))
    return records

def train_spatial(items):
    a=StrokeGrounding();b=InkChange();opt=torch.optim.AdamW(list(a.parameters())+list(b.parameters()),lr=.001,weight_decay=.01)
    train=[x for x in items if x['row']['split']=='train'];dev=[x for x in items if x['row']['split']=='dev'];pairs=[(i,t) for i in range(len(train)) for t in range(1,8)]
    rng=torch.Generator().manual_seed(42);best=float('inf');bad=0;history=[];start=time.perf_counter()
    def loss_one(x,t):
        masks,conf=a(x['reference'][None],x['kinds'][None],x['hints'][None]);target=x['masks'][None];prob=masks.detach().sigmoid();inter=(prob*target).sum(-1)
        quality=inter/(prob.sum(-1)+target.sum(-1)-inter).clamp_min(1e-6)
        change=b(x['visual'][t-1:t],x['visual'][t:t+1],x['rgb'][t:t+1])
        return mask_loss(masks,target)+mask_loss(change,x['change'][t:t+1])+.1*F.binary_cross_entropy_with_logits(conf,quality)
    for epoch in range(12):
        a.train();b.train();order=torch.randperm(len(pairs),generator=rng).tolist();total=0
        for offset in range(0,len(order),8):
            chosen=order[offset:offset+8];opt.zero_grad();loss=sum(loss_one(train[pairs[k][0]],pairs[k][1]) for k in chosen)/len(chosen);loss.backward()
            if epoch==0 and offset==0:
                save(OUT/'spatial_first_gradients.json',{prefix+'.'+n:float(p.grad.norm()) if p.grad is not None else None for prefix,module in [('A',a),('B',b)] for n,p in module.named_parameters()})
            opt.step();total+=float(loss.detach())*len(chosen)
        a.eval();b.eval()
        with torch.no_grad():validation=float(torch.stack([loss_one(x,t) for x in dev for t in [2,4,7]]).mean())
        history.append(dict(epoch=epoch+1,train_loss=total/len(pairs),dev_loss=validation,seconds=time.perf_counter()-start));save(OUT/'spatial_training.json',history)
        if validation<best:best=validation;bad=0;best_state=copy.deepcopy((a.state_dict(),b.state_dict()))
        else:bad+=1
        if bad>=3:break
    torch.save(dict(a=a.state_dict(),b=b.state_dict()),WEIGHTS/'spatial_final.pt');a.load_state_dict(best_state[0]);b.load_state_dict(best_state[1]);torch.save(dict(a=a.state_dict(),b=b.state_dict()),WEIGHTS/'spatial_best.pt')
    metrics={split:spatial_metrics(a,b,[x for x in items if x['row']['split']==split]) for split in ['train','dev']};metrics['fit_pass']=metrics['train']['instance_match_rate']>=.9 and metrics['train']['new_soft_dice']>=.7
    save(OUT/'spatial_train_dev_metrics.json',metrics);return a.eval().requires_grad_(False),b.eval().requires_grad_(False),metrics

def inputs_for(items,a,b,condition):
    out=[]
    for x in items:
        value=event_inputs(x,a,b,oracle=condition=='B4_oracle',whole=condition=='B4_whole_pool',no_delta=condition in ['B4_no_delta','B1_lastframe_head'])
        if condition=='B1_lastframe_head':
            value[:,:,64:128]=0;value[:,:,193:195]=0;value[:,:,-1]=0
        out.append(value)
    return out

def train_head(items,inputs,condition,initial):
    model=EventState(temporal=condition not in ['B3_pointwise','B1_lastframe_head'])
    own=model.state_dict();model.load_state_dict({k:initial[k] if k in initial and initial[k].shape==v.shape else v for k,v in own.items()})
    opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01);rng=torch.Generator().manual_seed(42)
    train=[i for i,x in enumerate(items) if x['row']['split']=='train'];dev=[i for i,x in enumerate(items) if x['row']['split']=='dev'];pairs=[(i,t) for i in train for t in range(3,8)];history=[];best=float('inf');start=time.perf_counter()
    for epoch in range(12):
        model.train();order=torch.randperm(len(pairs),generator=rng).tolist();total=0
        for offset in range(0,len(order),8):
            chosen=order[offset:offset+8];opt.zero_grad();loss=sum(temporal_loss(model(inputs[pairs[k][0]][None]),items[pairs[k][0]],pairs[k][1],progress=condition!='B4_no_progress') for k in chosen)/len(chosen)
            loss.backward();opt.step();total+=float(loss.detach())*len(chosen)
        model.eval()
        with torch.no_grad():validation=float(torch.stack([temporal_loss(model(inputs[i][None]),items[i],t,progress=condition!='B4_no_progress') for i in dev for t in [3,5,7]]).mean())
        history.append(dict(epoch=epoch+1,train_loss=total/len(pairs),dev_loss=validation,seconds=time.perf_counter()-start));save(OUT/(condition+'_training.json'),history)
        if validation<best:best=validation;selected_epoch=epoch+1;best_state=copy.deepcopy(model.state_dict())
    torch.save(model.state_dict(),WEIGHTS/(condition+'_final.pt'));model.load_state_dict(best_state);torch.save(model.state_dict(),WEIGHTS/(condition+'_best.pt'))
    save(OUT/(condition+'_run.json'),dict(seed=42,epochs=12,updates=12*((len(pairs)+7)//8),decision_exposures=12*len(pairs),selected_epoch=selected_epoch,parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0,seconds=time.perf_counter()-start))
    return model.eval()

def shuffled_records(model,items,a,b):
    records=[];rng=np.random.default_rng(42)
    with torch.no_grad():
        for x in items:
            for t in range(3,8):
                interior=rng.permutation(np.arange(1,t)).tolist();order=[0]+interior+[t];z=dict(x)
                for key in ['visual','small','ink_grid']:z[key]=x[key][order]
                ink=np.stack([np.asarray(Image.open(ROOT/x['row']['frames'][i]))[:,:,0]<128 for i in order]);previous=np.concatenate([ink[:1],ink[:-1]],0)
                z['rgb']=torch.stack([grid(ink&~previous),grid(previous&~ink)],1)
                z['row']=dict(x['row'],indices=x['row']['indices'][:t+1]);value=event_inputs(z,a,b);o=model(value[None]);state=decode_state(o,x,t)
                truth=x['state'][t].tolist();records.append(dict(id=x['row']['id'],group=x['row']['group'],t=t,permutation=order,prediction=state,truth_state=truth,truth_order=x['orders'][t],truth_progress=x['progress'][t].tolist(),order_correct=state['event_order']==x['orders'][t],state_correct=[a==b for a,b in zip(state['geometry_state'],truth)],action_correct=state['decision']==x['truth'][t],progress_mae=float((o['progress'][0,t]-x['progress'][t]).abs().mean())))
    return records

def ci(values):
    groups=sorted(values);rng=np.random.default_rng(42);samples=[np.mean([values[g] for g in rng.choice(groups,len(groups),replace=True)]) for _ in range(2000)]
    return np.quantile(samples,[.025,.975]).tolist()

def summarize(records,items):
    confusion=np.zeros((3,3),dtype=int);by_id={x['row']['id']:x for x in items};direction=[];start=[];complete=[];first_error=[];action=[];active=[]
    for r in records:
        x=by_id[r['id']];t=r['t'];p=r['prediction']
        for truth,pred in zip(r['truth_state'],p['geometry_state']):confusion[truth,pred]+=1
        for j,true in enumerate(x['direction'][t].tolist()):
            if true!=0:direction.append(p['direction'][j]==['unknown','forward','reverse'][true])
        if r['truth_order'] is not None:first_error.append(p['decision']['first_error']==x['truth'][t]['first_error'] and p['decision']['error_type']==x['truth'][t]['error_type'])
        action.append(p['decision']['action']==x['truth'][t]['action'])
        if 'active_id' in p:active.append(p['active_id']==int(x['active'][t])-1)
        if 'stroke_start' in p:start.extend(a==b for a,b in zip(p['stroke_start'],x['start'][t].bool().tolist()));complete.extend(a==b for a,b in zip(p['stroke_complete'],x['complete'][t].bool().tolist()))
    f1=[2*confusion[i,i]/max(1,int(confusion[i].sum()+confusion[:,i].sum())) for i in range(3)]
    groups=sorted(set(r['group'] for r in records));group_order={g:np.mean([r['order_correct'] for r in records if r['group']==g]) for g in groups};group_state={g:np.mean([v for r in records if r['group']==g for v in r['state_correct']]) for g in groups}
    finals=[r for r in records if r['t']==7];pairs=[]
    for g in groups:
        selected=[r for r in finals if r['group']==g and r['id'].endswith(('-correct','-swap'))];pairs.append(dict(group=g,both_correct=all(r['order_correct'] for r in selected)))
    unknown=[r for r in records if r['truth_order'] is None];visible=[r for r in records if r['truth_order'] is not None]
    return dict(n_decisions=len(records),n_instances=int(confusion.sum()),state_accuracy=float(np.trace(confusion)/confusion.sum()),state_CI=ci(group_state),state_macro_f1=float(np.mean(f1)),state_f1=f1,confusion=confusion.tolist(),
        partial_as_full=int(confusion[1,2]),full_as_partial=int(confusion[2,1]),strict_order=float(np.mean([r['order_correct'] for r in records])),strict_order_CI=ci(group_order),
        final_order=float(np.mean([r['order_correct'] for r in finals])),same_final_pair_both=sum(p['both_correct'] for p in pairs),pairs=pairs,pair_CI=ci({p['group']:p['both_correct'] for p in pairs}),
        progress_mae=float(np.mean([r['progress_mae'] for r in records])),direction_accuracy=float(np.mean(direction)),first_error_observable_accuracy=float(np.mean(first_error)),action_only_accuracy=float(np.mean(action)),
        action_all_fields_accuracy=float(np.mean([r['action_correct'] for r in records])),active_accuracy=float(np.mean(active)) if active else None,start_accuracy=float(np.mean(start)) if start else None,completion_event_accuracy=float(np.mean(complete)) if complete else None,
        unknown_true=len(unknown),unknown_recall=float(np.mean([r['prediction']['event_order'] is None for r in unknown])),unknown_false_acceptance=float(np.mean([r['prediction']['event_order'] is not None for r in unknown])),
        unknown_output_coverage=float(np.mean([r['prediction']['event_order'] is None for r in records])),observable_answer_coverage=float(np.mean([r['prediction']['event_order'] is not None for r in visible])),format_valid=1.,format_note='Deterministic serializer, not autonomous instruction-following gain.')

def run():
    if (OUT/'spatial_training.json').exists() or any(WEIGHTS.glob('*.pt')):
        raise FileExistsError('Preserve existing run. Select fresh --output and --weights paths.')
    WEIGHTS.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    items=prepare(CASES,FEATURES,MANIFEST);test=[x for x in items if x['row']['split']=='test']
    # Gate uses train/dev only; save independent pixel failure evidence before any training.
    baseline=pixel_baseline(items);save(OUT/'B0_predictions.json',baseline)
    if not all(r['order_correct'] and all(r['state_correct']) for r in baseline):
        save(OUT/'decision.json',dict(status='pixel_gate_failed',training='not_started'));return
    torch.manual_seed(42);a,b,spatial_result=train_spatial(items)
    if not spatial_result['fit_pass']:
        save(OUT/'decision.json',dict(status='spatial_fit_failed',temporal='not_started'));return
    torch.manual_seed(42);initial=copy.deepcopy(EventState().state_dict());models={};values={}
    conditions=['B1_lastframe_head','B3_pointwise','B4','B4_oracle','B4_no_delta','B4_whole_pool','B4_no_progress']
    for condition in conditions:
        torch.manual_seed(42);inputs=inputs_for(items,a,b,condition);models[condition]=train_head(items,inputs,condition,initial);values[condition]=inputs
        if condition=='B1_lastframe_head':
            equal=[]
            for group in sorted(set(x['row']['group'] for x in items)):
                indices=[next(i for i,x in enumerate(items) if x['row']['group']==group and x['row']['variant']==v) for v in ['correct','swap']]
                equal.append(dict(group=group,last_input_equal=bool(torch.equal(inputs[indices[0]][-1],inputs[indices[1]][-1]))))
            save(OUT/'B1_same_final_inputs.json',equal)
    # All heads selected before held-geometry scores are read.
    metrics={};test_indices=[i for i,x in enumerate(items) if x['row']['split']=='test']
    for condition,model in models.items():
        result=event_metrics(model,test,[values[condition][i] for i in test_indices]);records=result['records'];save(OUT/(condition+'_predictions.json'),records);metrics[condition]=summarize(records,test)
        train=[i for i,x in enumerate(items) if x['row']['split']=='train'];train_result=event_metrics(model,[items[i] for i in train],[values[condition][i] for i in train]);save(OUT/(condition+'_fit.json'),train_result)
    records=shuffled_records(models['B4'],test,a,b);save(OUT/'B4_time_shuffle_predictions.json',records);metrics['B4_time_shuffle']=summarize(records,test)
    records=[r for r in baseline if by_split(r,items)=='test'];metrics['B0']=summarize(records,test)
    save(OUT/'metrics.json',metrics);save(OUT/'spatial_test_metrics.json',spatial_metrics(a,b,test))
    with torch.no_grad():
        masks=[]
        for x in test:
            if x['row']['variant']!='correct':continue
            out,conf=a(x['reference'][None],x['kinds'][None],x['hints'][None]);blank,_=a(torch.zeros_like(x['reference'][None]),x['kinds'][None],x['hints'][None]);truth=x['masks']>.25;pred=blank[0].sigmoid()>.5;blank_iou=(pred&truth).sum(-1)/(pred|truth).sum(-1).clamp_min(1)
            masks.append(dict(group=x['row']['group'],soft_masks=out[0].sigmoid().tolist(),confidence=conf[0].sigmoid().tolist(),blank_feature_iou=blank_iou.tolist()))
        save(OUT/'spatial_test_predictions.json',masks)
    save(OUT/'decision.json',dict(status='fixed_study_completed',UMM_LoRA='not_started',extra_training='stopped after preregistered conditions; proceed T5'))

def by_split(record,items):return next(x['row']['split'] for x in items if x['row']['id']==record['id'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=OUT);parser.add_argument('--weights',type=Path,default=WEIGHTS);parser.add_argument('--features',type=Path,default=FEATURES);parser.add_argument('--manifest',type=Path,default=MANIFEST);parser.add_argument('--cases',type=Path,default=CASES)
    parser.add_argument('--early-history',choices=['spatial','compact','heads','evaluate'],help='Independent T6 entry; keeps all T4 paths and results intact');args=parser.parse_args()
    if args.early_history:
        import h1_early_history_experiment as t6
        getattr(t6,args.early_history)()
        raise SystemExit(0)
    original_protocol=OUT/'preregistration.json';OUT=args.output;WEIGHTS=args.weights;FEATURES=args.features;MANIFEST=args.manifest;CASES=args.cases
    if OUT!=original_protocol.parent:
        OUT.mkdir(parents=True,exist_ok=True)
        if not (OUT/'preregistration.json').exists():save(OUT/'preregistration.json',json.loads(original_protocol.read_text()))
    run()
