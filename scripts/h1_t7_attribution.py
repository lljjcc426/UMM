"""T7-1: frozen T6 replay and observation-level attribution, no fitting."""
import json
from collections import Counter
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from h1_event_data import ROOT, save
from h1_event_model import StrokeGrounding, InkChange, EventState
from h1_event_ledger import EventLedger
from h1_event_observe import masks_for
from h1_event_train import grid, decode_state
from h1_early_history_io import normalization
from h1_early_history_score import load_jsonl, estimate, compute_pairs, partial_score

OLD = ROOT/'results/h1/early_history_v1'
OUT = ROOT/'results/h1/instance_onset_v1'
W = ROOT/'checkpoints/h1_early_history_v1'

def main():
    torch.set_num_threads(4)
    items = torch.load(W/'compact.pt', weights_only=False)
    raw = {(r['method'], r['id']): r['outputs'] for r in load_jsonl(OLD/'raw_model_outputs.jsonl')
           if r['method'] in ['M1', 'M4_oracle_region']}
    old_predictions = load_jsonl(OLD/'predictions.jsonl')
    locked = torch.load(W/'spatial_best.pt', weights_only=True)
    a, b, m = StrokeGrounding(), InkChange(), EventState(temporal=False)
    a.load_state_dict(locked['a']); b.load_state_dict(locked['b'])
    m.load_state_dict(torch.load(W/'M1_best.pt', weights_only=True))
    for model in [a,b,m]: model.eval().requires_grad_(False)
    mean, std, _ = normalization()
    spatial = {}; observations = []; errors = []; replays = []
    for x in items:
        r=x['row']
        if r['split'] not in ['test','diagnostic']: continue
        q=len(r['strokes']); g=r['group']
        if g not in spatial:
            meta=json.loads((OLD/'feature_manifests'/f'{g}.json').read_text())
            ref=torch.load(ROOT/meta['shard'], weights_only=True)['features'][meta['index'][r['reference']]].float()
            target=grid(masks_for(r)); target_binary=target>.25
            with torch.no_grad(): logits,conf=a(((ref-mean)/std)[None],torch.tensor(r['query']['kinds'])[None],torch.tensor(r['query']['hints'])[None])
            prob=logits[0].sigmoid(); pred=prob>.5
            iou=(pred[:,None]&target_binary[None]).sum(-1)/(pred[:,None]|target_binary[None]).sum(-1).clamp_min(1)
            exclusive=target_binary & (target_binary.sum(0)==1)[None]
            spatial[g]=dict(ious=iou.tolist(),confidence=conf[0].sigmoid().tolist(),
                other_exclusive_mass=[float((prob[j]*exclusive[torch.arange(q)!=j].any(0)).sum()/prob[j].sum().clamp_min(1e-6)) for j in range(q)])
        sp=spatial[g]
        outputs={name:{k:torch.tensor(v)[None] for k,v in raw[name,r['id']].items()} for name in ['M1','M4_oracle_region']}
        ledgers={name:EventLedger(q) for name in outputs}; final={}
        for t in range(24):
            for name,o in outputs.items():
                s=decode_state(o,x,t); inp=x['inputs'] if name=='M1' else x['oracle_inputs']
                p=(1-o['state'][0,t].softmax(-1)[:,0]).tolist()
                state=ledgers[name].update(t,p,s['progress'],s['geometry_state'],s['direction'],inp[t,:,193].tolist())
                if t in [15,20,23]:
                    method='D0' if name=='M1' else 'D1'
                    replays.append(dict(method=method,id=r['id'],group=g,split=r['split'],variant=r['variant'],q=q,t=t,prediction=state,truth=x['truth_states'][t],order_correct=state['event_order']==x['truth_states'][t]['event_order']))
                final[name]=state
            p=(1-outputs['M1']['state'][0,t].softmax(-1)[:,0]).tolist()
            po=(1-outputs['M4_oracle_region']['state'][0,t].softmax(-1)[:,0]).tolist()
            start=outputs['M1']['start'][0,t].sigmoid().tolist()
            starto=outputs['M4_oracle_region']['start'][0,t].sigmoid().tolist()
            for j in range(q):
                observations.append(dict(id=r['id'],group=g,split=r['split'],family=r['family'],t=t,instance=j,
                    presence=p[j],start=start[j],new_ink=float(x['inputs'][t,j,193]),oracle_region_presence=po[j],oracle_region_start=starto[j],oracle_region_new_ink=float(x['oracle_inputs'][t,j,193]),
                    target_iou=sp['ious'][j][j],best_iou_instance=int(np.argmax(sp['ious'][j])),other_exclusive_mass=sp['other_exclusive_mass'][j],
                    true_present=j in x['truth_states'][t]['observed_ids'],true_onset=x['truth_states'][t]['onset_intervals'].get(str(j)),
                    first_detection_interval=final['M1']['onset_intervals'].get(str(j))))
        truth=x['truth_states'][-1]
        for j in range(q):
            actual=truth['onset_intervals'].get(str(j)); got=final['M1']['onset_intervals'].get(str(j)); cats=[]
            if got is None or (actual and got[1]>actual[1]):cats.append('missed_onset')
            if got and actual and got[1]<actual[1]:cats.append('false_early_onset')
            if sp['ious'][j][j]<.5 or int(np.argmax(sp['ious'][j]))!=j:cats.append('wrong_instance')
            if any(j in group for group in final['M1']['unresolved_order_groups']):cats.append('merged_onset')
            if j in final['M1']['uncertain_instance_ids']:cats.append('uncertain_detection')
            evidence=[v for v in observations[-24*q:] if v['instance']==j and v['t'] in {actual[1] if actual else -1,got[1] if got else -1}]
            if cats:
                errors.append(dict(id=r['id'],group=g,split=r['split'],family=r['family'],instance=j,categories=cats,true_interval=actual,predicted_interval=got,
                    oracle_region_interval=final['M4_oracle_region']['onset_intervals'].get(str(j)),evidence=evidence,
                    onset_incorrect=got!=actual))
    # Replacing observable onset intervals includes event identity/visibility, a privileged upper bound.
    for r in old_predictions:
        if r['method']=='M5':
            for method in ['D2','D3']:
                replays.append(dict(**{k:v for k,v in r.items() if k!='method'},method=method))
    summaries={}
    for method in ['D0','D1','D2','D3']:
        rs=[r for r in replays if r['method']==method and r['split']=='test']
        pairs=compute_pairs(rs); visible=[r for r in rs if r['truth']['event_order'] is not None]; hidden=[r for r in rs if r['variant']=='mergedA']
        summaries[method]=dict(pair=estimate(pairs,lambda r:r['both_correct']),strict=estimate(visible,lambda r:r['order_correct']),
            answer_coverage=estimate(visible,lambda r:r['prediction']['event_order'] is not None),unknown=estimate(hidden,lambda r:r['prediction']['event_order'] is None),partial_order=partial_score(hidden))
    by_old={(r['method'],r['id'],r['t']):r for r in old_predictions}
    assert all(r['prediction']==by_old['M4' if r['method']=='D0' else 'M4_oracle_region',r['id'],r['t']]['prediction'] for r in replays if r['method'] in ['D0','D1'])
    trainable={n:sum(p.numel() for p in mod.parameters()) for n,mod in [('A',a),('B',b),('M1',m)]}
    onset_obs=[v for v in observations if v['split']=='test' and v['true_onset'] and v['true_onset'][1]==v['t']]
    absent_obs=[v for v in observations if v['split']=='test' and not v['true_present']]
    counts=Counter(c for e in errors if e['split']=='test' for c in e['categories'])
    matrix=dict(conditions=summaries,categories=dict(counts),
        onset_signal_at_true_first_interval=dict(n=len(onset_obs),presence_ge05=float(np.mean([v['presence']>=.5 for v in onset_obs])),start_ge05=float(np.mean([v['start']>=.5 for v in onset_obs])),new_ge002=float(np.mean([v['new_ink']>=.02 for v in onset_obs]))),
        absent_instance_false_evidence=dict(n=len(absent_obs),presence_ge05=sum(v['presence']>=.5 for v in absent_obs),start_ge05=sum(v['start']>=.5 for v in absent_obs),new_ge002=sum(v['new_ink']>=.02 for v in absent_obs),oracle_region_new_ge002=sum(v['oracle_region_new_ink']>=.02 for v in absent_obs)),
        parameters=trainable,updated_parameters=0,cached_feature_shards=len(list((W/'features').glob('*.pt'))),
        limits=['D1 changes A pooling and thus both B aggregation and M1 input; it does not isolate A from M1 distribution shift.',
                'D2/D3 insert true observable event identity and interval. Their equality is a privileged construction, not an independent demonstration of perfect B/M1.',
                'new_ink is a soft pooled probability, not literal new-pixel fraction. Neighbor contamination and B false positive cannot be separated solely by that scalar.',
                'start reports first observed ink, not visible pen contact. No source sub-frame order is inferred.',
                'T6 test is historical diagnosis only; no T7 rule or threshold is selected on it.'])
    save(OUT/'failure_taxonomy.json',dict(categories=['false_early_onset','missed_onset','wrong_instance','merged_onset','uncertain_detection'],unit='instance per clip; categories overlap; merged group alone need not be error'))
    save(OUT/'t6_attribution_matrix.json',matrix);save(OUT/'t6_attribution_cases.json',errors)
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'t6_observation_evidence.jsonl').open('w') as f:
        for r in observations:f.write(json.dumps(r)+'\n')
    print(json.dumps({k:dict(pair=v['pair']['value'],strict=v['strict']['value']) for k,v in summaries.items()}))

if __name__=='__main__':main()
