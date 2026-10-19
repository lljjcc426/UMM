"""T7 fixed A-only training; subsequent stages use frozen selected checkpoints."""
import argparse,copy,json,time,subprocess
import numpy as np
import torch
from h1_event_data import ROOT,save
from h1_event_model import StrokeGrounding,InkChange,EventState
from h1_event_train import event_inputs,decode_state
from h1_event_ledger import EventLedger
from h1_event_ledger_v2 import EvidenceLedger
from h1_early_history_experiment import record
from h1_target_contrast import grounding_loss
from h1_t7_data import OUT,WEIGHTS,DECISIONS
from h1_t7_io import reference_examples,prepare_group,model_input

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

def compact_groups(groups,target):
    torch.set_num_threads(4);a0,b,m=modules('A0');a1,_,_=modules('A1');models={'A0':a0,'A1':a1,'Oracle':a0}
    items=[];checks=[];begin=time.perf_counter()
    for group in groups:
        group_items=[]
        for x in prepare_group(group):
            item={k:x[k] for k in ['row','progress','state','truth_states','truth']};item['views']={}
            with torch.no_grad():
                for name,a in models.items():
                    oracle=name=='Oracle';inp=event_inputs(model_input(x,oracle),a,b,oracle=oracle)
                    logits,confidence=a(x['reference'][None],x['kinds'][None],x['hints'][None]);mask=x['masks']>.25 if oracle else logits[0].sigmoid()>.5
                    overlap=(mask[:,None]&mask[None]).sum(-1)/(mask[:,None]|mask[None]).sum(-1).clamp_min(1);overlap.fill_diagonal_(0)
                    ambiguous=(overlap>=.5).any(-1).nonzero().flatten().tolist()
                    start=time.perf_counter();o=m(inp[None]);elapsed=time.perf_counter()-start
                    item['views'][name]=dict(inputs=inp,outputs={k:v[0] for k,v in o.items()},binding_ambiguous=ambiguous,A_confidence=confidence[0].sigmoid(),head_sequence_seconds=elapsed)
            items.append(item);group_items.append(item)
        by={x['row']['variant']:x for x in group_items};q=len(group_items[0]['row']['strokes'])
        for name in models:
            for variant in ['swap1']+(['swap2'] if q==5 else []):
                for t in DECISIONS:
                    assert torch.equal(by['correct']['views'][name]['inputs'][t-7:t+1],by[variant]['views'][name]['inputs'][t-7:t+1])
                    checks.append(dict(group=group,region=name,variant=variant,t=t,exact=True))
            assert torch.equal(by['mergedA']['views'][name]['inputs'],by['mergedB']['views'][name]['inputs'])
    torch.save(items,WEIGHTS/target)
    save(OUT/(target.removesuffix('.pt')+'_inputs.json'),dict(groups=len(groups),exact_local_checks=checks,seconds=time.perf_counter()-begin))
    return items

def compact_train_dev():
    assert (OUT/'models_frozen.json').exists() and not (OUT/'test_unlock.json').exists()
    splits=json.loads((OUT/'splits.json').read_text())
    compact_groups(splits['train']+splits['dev'],'compact_train_dev.pt')

def ledger_states(x,region,version):
    view=x['views'][region];o={k:v[None] for k,v in view['outputs'].items()};q=len(x['row']['strokes'])
    ledger=EventLedger(q) if version==0 else EvidenceLedger(q);states=[];timings=[]
    for t in range(len(x['row']['frames'])):
        current=decode_state(o,x,t);presence=(1-o['state'][0,t].softmax(-1)[:,0]).tolist();start=o['start'][0,t].sigmoid().tolist()
        values=(t,presence,current['progress'],current['geometry_state'],current['direction'],view['inputs'][t,:,193].tolist())
        begin=time.perf_counter()
        state=ledger.update(*values) if version==0 else ledger.update(*values,start=start,binding_ambiguous=view['binding_ambiguous'])
        timings.append(time.perf_counter()-begin)
        state['ledger_data_bytes']=len(json.dumps(ledger.__dict__,default=list).encode())
        states.append(state)
    return states,timings

def distribution(items):
    result={}
    for split in sorted({x['row']['split'] for x in items}):
        selected=[x for x in items if x['row']['split']==split and x['row']['variant']!='mergedB'];values={}
        for block,a,b in [('current',0,64),('feature_change',64,128),('reference_difference',128,192),('current_ink',192,193),('new_ink',193,194),('gone_ink',194,195),('time',195,196)]:
            vectors={v:torch.cat([x['views'][v]['inputs'][:,:,a:b].reshape(-1,b-a) for x in selected]) for v in ['A0','A1','Oracle']}
            values[block]=dict(A1_minus_A0_RMS=float((vectors['A1']-vectors['A0']).square().mean().sqrt()),A0_oracle_RMS=float((vectors['A0']-vectors['Oracle']).square().mean().sqrt()),A1_oracle_RMS=float((vectors['A1']-vectors['Oracle']).square().mean().sqrt()))
        states={v:torch.cat([x['views'][v]['outputs']['state'].argmax(-1).flatten() for x in selected]) for v in ['A0','A1','Oracle']}
        result[split]=dict(blocks=values,M1_A0_A1_state_disagreement=float((states['A0']!=states['A1']).float().mean()),M1_A0_oracle_state_disagreement=float((states['A0']!=states['Oracle']).float().mean()),M1_A1_oracle_state_disagreement=float((states['A1']!=states['Oracle']).float().mean()),
            interpretation='paired region intervention with fixed M1; RMS is not a calibrated OOD threshold')
    return result

def ledger_dev():
    assert not (OUT/'test_unlock.json').exists()
    from h1_t7_score import pairs,estimate
    from h1_early_history_score import partial_score
    items=torch.load(WEIGHTS/'compact_train_dev.pt',weights_only=False);summary={};cases=[]
    for region,version,method in [('A0',0,'E00'),('A0',1,'E01'),('A1',0,'E10'),('A1',1,'E11'),('Oracle',0,'Oracle_L0'),('Oracle',1,'Oracle_L1')]:
        rs=[]
        for x in items:
            if x['row']['split']!='dev':continue
            states,_=ledger_states(x,region,version)
            for t in DECISIONS:rs.append(record(x,t,states[t],method))
            cases.append(dict(method=method,id=x['row']['id'],onsets=states[-1]['onset_intervals'],truth=x['truth_states'][-1]['onset_intervals'],reason=states[-1]['uncertainty_reason'],order=states[-1]['event_order'],truth_order=x['truth_states'][-1]['event_order']))
        rs=[r for r in rs if r['variant']!='mergedB'];visible=[r for r in rs if r['truth']['event_order'] is not None];hidden=[r for r in rs if r['variant']=='mergedA']
        summary[method]=dict(pair=estimate(pairs(rs),lambda r:r['both_correct']),strict=estimate(visible,lambda r:r['order_correct']),raw_coverage=estimate(visible,lambda r:r['prediction']['event_order'] is not None),
            unknown=estimate(hidden,lambda r:r['prediction']['event_order'] is None),partial=partial_score(hidden))
    save(OUT/'ledger_dev_summary.json',summary);save(OUT/'ledger_dev_cases.json',cases);save(OUT/'input_distribution_train_dev.json',distribution(items))
    save(OUT/'ledger_rules_locked.json',dict(version='L1-v1.1',thresholds=dict(presence=.5,start=.5,new_ink=.02),binding_overlap_threshold=.5,
        development_runs=2,rule_variants_tried=2,threshold_searches=0,rules_changed_after_initial_dev=True,amendment='ledger_rule_amendment.json',training=False,selection_reason='One pre-test amendment: persistent ink can confirm a prior change even when writing has finished; original interval retained. Initial Dev results preserved.',timestamp=time.time(),test_labels_read=False))
    print(json.dumps({m:dict(pair=v['pair']['value'],raw_coverage=v['raw_coverage']['value']) for m,v in summary.items()}))

def evaluate():
    assert (OUT/'models_frozen.json').exists() and (OUT/'ledger_rules_locked.json').exists()
    if (OUT/'test_unlock.json').exists():raise FileExistsError('T7 formal test already unlocked')
    torch.set_num_threads(4)
    save(OUT/'test_unlock.json',dict(timestamp=time.time(),code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        models=json.loads((OUT/'models_frozen.json').read_text()),ledger=json.loads((OUT/'ledger_rules_locked.json').read_text()),
        scoring='scripts/h1_t7_score.py',further_model_or_rule_selection=False,conditions=['E00','E01','E10','E11','Oracle_L0','Oracle_L1']))
    begin=time.perf_counter();groups=json.loads((OUT/'splits.json').read_text())['test'];items=compact_groups(groups,'compact_test.pt')
    records=[];timings={};memory={};aliases={};alias_checks=0
    with (OUT/'history_predictions.jsonl').open('w') as history,(OUT/'raw_model_outputs.jsonl').open('w') as raw,(OUT/'onset_evidence.jsonl').open('w') as evidence,(OUT/'ledger_audits.jsonl').open('w') as audits:
        for x in items:
            for region in ['A0','A1','Oracle']:
                view=x['views'][region];o=view['outputs'];raw.write(json.dumps(dict(id=x['row']['id'],region=region,outputs={k:v.tolist() for k,v in o.items()}))+'\n')
                evidence.write(json.dumps(dict(id=x['row']['id'],region=region,presence=(1-o['state'].softmax(-1)[:,:,0]).tolist(),start=o['start'].sigmoid().tolist(),
                    new_ink=view['inputs'][:,:,193].tolist(),binding_ambiguous=view['binding_ambiguous'],A_confidence=view['A_confidence'].tolist()))+'\n')
            for region,version,method in [('A0',0,'E00'),('A0',1,'E01'),('A1',0,'E10'),('A1',1,'E11'),('Oracle',0,'Oracle_L0'),('Oracle',1,'Oracle_L1')]:
                states,seconds=ledger_states(x,region,version);timings.setdefault(method,[]).extend(seconds)
                for t,state in enumerate(states):
                    r=record(x,t,state,method,seconds[t])
                    if t in DECISIONS:records.append(r);memory.setdefault(method,[]).append(state['ledger_data_bytes'])
                    concise=copy.deepcopy(r);audit=concise['prediction'].pop('audit',[]);concise['prediction']['audit_count']=len(audit)
                    history.write(json.dumps(concise)+'\n')
                audits.write(json.dumps(dict(method=method,id=x['row']['id'],audit=states[-1].get('audit',[])))+'\n')
                key=(method,x['row']['group'])
                if x['row']['variant']=='mergedA':aliases[key]=states
                elif x['row']['variant']=='mergedB':assert states==aliases.pop(key);alias_checks+=1
    with (OUT/'predictions.jsonl').open('w') as f:
        for r in records:f.write(json.dumps(r)+'\n')
    masks=[]
    examples=reference_examples('test')
    for name in ['A0','A1']:
        a,_,_=modules(name)
        masks.extend(dict(**mask_record(a,x),method=name) for x in examples)
    save(OUT/'mask_predictions.json',masks);save(OUT/'input_distribution_test.json',distribution(items))
    save(OUT/'timing.json',{k:dict(update_mean_seconds=float(np.mean(v)),updates=len(v),scope='CPU cached ledger update only; excludes decoding, M1, A+B, UMM and JSON serialization') for k,v in timings.items()})
    save(OUT/'memory.json',{k:dict(mean_ledger_data_bytes=float(np.mean(v)),max_ledger_data_bytes=max(v),scope='JSON size of ledger fields including candidates, evidence buffer and full audit; excludes Python overhead, common weights and visual scratch',current_instance_vectors_bytes_q3=3*196*4,current_instance_vectors_bytes_q5=5*196*4) for k,v in memory.items()})
    save(OUT/'test_execution.json',dict(seconds=time.perf_counter()-begin,clips=len(items),decision_records=len(records),exact_merged_prediction_checks=alias_checks,all_passed=True,training_updates=0))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['train','compact_train_dev','ledger_dev','evaluate']);args=p.parse_args();globals()[args.stage]()
