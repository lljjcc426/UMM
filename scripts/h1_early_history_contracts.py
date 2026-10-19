"""T6 zero-training checks with oracle memory and actual old A+B inputs."""
import json
import numpy as np
import torch
from h1_event_data import ROOT,save
from h1_early_history_data import DATA,OUT,WEIGHTS,DECISIONS
from h1_event_ledger import EventLedger

def oracle_checks():
    rows={r['id']:r for r in json.loads((DATA/'cases.json').read_text())};states=json.loads((OUT/'pixel_states.json').read_text());by={}
    for r in states:by.setdefault(r['id'],[]).append(r)
    results=[]
    for key,records in by.items():
        ledger=EventLedger(len(rows[key]['strokes']));previous=np.zeros(ledger.q)
        for record in records:
            s=record['state'];p=np.array(s['progress']);geometry=np.where(p>.985,2,np.where(p>.02,1,0)).tolist()
            prediction=ledger.update(record['t'],(p>.02).astype(float).tolist(),p.tolist(),geometry,s['direction'],np.maximum(p-previous,0).tolist());previous=p
            ok=prediction['event_order']==s['event_order'] and sorted(prediction['confirmed_precedence'])==sorted(s['confirmed_precedence']) and prediction['unresolved_order_groups']==s['unresolved_order_groups']
            results.append(dict(id=key,t=record['t'],pass_check=ok,prediction=prediction))
    save(OUT/'oracle_ledger_predictions.json',results)
    if not all(r['pass_check'] for r in results):raise RuntimeError('Oracle Ledger failed')
    result=json.loads((OUT/'data_contract_checks.json').read_text());result['oracle_ledger_all_prefixes']=dict(passed=True,n=len(results));save(OUT/'data_contract_checks.json',result)

def feature_checks():
    from h1_early_history_io import prepare_group,model_input
    from h1_event_train import event_inputs
    from h1_event_model import StrokeGrounding,InkChange
    weights=torch.load(ROOT/'checkpoints/h1_event_v3/T4/spatial_best.pt',map_location='cpu',weights_only=True)
    a=StrokeGrounding().eval();b=InkChange().eval();a.load_state_dict(weights['a']);b.load_state_dict(weights['b'])
    result=json.loads((OUT/'data_contract_checks.json').read_text());metrics=[];audits=[]
    for group in sorted({r['group'] for r in json.loads((DATA/'cases.json').read_text())}):
        items=prepare_group(group,labels=False);by={x['row']['variant']:x for x in items}
        with torch.no_grad():values={k:event_inputs(model_input(x),a,b) for k,x in by.items()}
        for name in ['swap1','swap2'] if 'swap2' in by else ['swap1']:
            for t in DECISIONS:
                exact=torch.equal(values['correct'][t-7:t+1],values[name][t-7:t+1]);assert exact
                raw_exact=torch.equal(by['correct']['visual'][t-8:t+1],by[name]['visual'][t-8:t+1]);assert raw_exact
                audits.append(dict(group=group,pair=name,t=t,B3_current_input_exact=bool(torch.equal(values['correct'][t],values[name][t])),recent8_inputs_exact=exact,feature_cache_exact=raw_exact))
        assert torch.equal(values['mergedA'],values['mergedB'])
        if group.startswith(('train','dev')):
            x=items[0]
            with torch.no_grad():logits,_=a(x['reference'][None],x['kinds'][None],x['hints'][None])
            p=logits[0].sigmoid()>.5;truth=x['masks']>.25;iou=(p&truth).sum(-1)/(p|truth).sum(-1).clamp_min(1)
            metrics.append(dict(group=group,ious=iou.tolist(),new_instance_3_4_match=(iou[3:]>=.5).tolist()))
    result.update(feature_equality='passed exact torch.equal',B3_input_checks=audits,zero_training_gate=bool(result['passed'] and result['oracle_ledger_all_prefixes']['passed'] and all(r['B3_current_input_exact'] for r in audits)))
    save(OUT/'data_contract_checks.json',result)
    values=[v for r in metrics for v in r['new_instance_3_4_match']]
    save(OUT/'old_spatial_coverage.json',dict(weights='checkpoints/h1_event_v3/T4/spatial_best.pt',records=metrics,new_instance_match=sum(values)/len(values),requires_single_shared_fit=sum(values)/len(values)<.9))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['oracle','features']);args=p.parse_args()
    oracle_checks() if args.stage=='oracle' else feature_checks()
