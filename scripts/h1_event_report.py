"""T4 fixed-result diagnostics and paired geometry intervals; no new training."""
import json
from collections import Counter
import numpy as np
from h1_event_data import save
from h1_event_study import OUT,STUDY
from h1_event_experiment import ci

def main():
    metrics=json.loads((OUT/'metrics.json').read_text());records={n:json.loads((OUT/(n+'_predictions.json')).read_text()) for n in metrics if (OUT/(n+'_predictions.json')).exists()};rows={r['id']:r for r in json.loads((STUDY/'cases.json').read_text())}
    effects={}
    for name in ['B3_pointwise','B4_no_delta','B4_whole_pool','B4_no_progress','B4_time_shuffle']:
        base={(r['id'],r['t']):r for r in records[name]};groups=sorted(set(r['group'] for r in records['B4']));delta={g:float(np.mean([int(r['order_correct'])-int(base[(r['id'],r['t'])]['order_correct']) for r in records['B4'] if r['group']==g])) for g in groups}
        effects[name]=dict(B4_minus_condition=float(np.mean(list(delta.values()))),group_CI=ci(delta),by_group=delta)
    failures=[]
    for r in records['B4']:
        if not r['order_correct'] or not all(r['state_correct']) or not r['action_correct']:
            p=r['prediction'];failures.append(dict(id=r['id'],group=r['group'],t=r['t'],frames=rows[r['id']]['frames'][:r['t']+1],truth_order=r['truth_order'],truth_state=r['truth_state'],truth_progress=r['truth_progress'],prediction=p))
    consistency={}
    for name,rs in records.items():
        if name=='B0':continue
        full=[p for r in rs for c,p in zip(r['prediction']['geometry_state'],r['prediction']['progress']) if c==2]
        consistency[name]=dict(predicted_full_count=len(full),full_regression_below_95_percent=sum(p<.95 for p in full),full_regression_range=[min(full),max(full)] if full else None,
            note='Post-hoc diagnostic at 5 percentage-point disagreement, not a new acceptance metric. D uses geometry classes (absent0/full1/partial clipped below.985), not raw continuous progress.')
    save(OUT/'paired_effects.json',effects);save(OUT/'B4_failures.json',failures);save(OUT/'progress_consistency.json',consistency)
    print(json.dumps(effects,indent=2));print(json.dumps(consistency['B4'],indent=2));print('B4 failure decisions',len(failures))

if __name__=='__main__':main()
