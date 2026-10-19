"""Fixed T6 scores, geometry-clustered intervals and all failures. No training."""
import json
from collections import defaultdict
import numpy as np
from h1_event_data import save
from h1_early_history_data import OUT,DECISIONS

def load_jsonl(path):return [json.loads(line) for line in path.read_text().splitlines()]
def mean(v):return float(np.mean(v)) if len(v) else None

def cluster_ci(values):
    groups=sorted(values);rng=np.random.default_rng(42)
    if not groups:return None
    samples=[np.mean([values[g] for g in rng.choice(groups,len(groups),replace=True)]) for _ in range(2000)]
    return np.quantile(samples,[.025,.975]).tolist()

def estimate(records,fn):
    grouped=defaultdict(list)
    for r in records:grouped[r['group']].append(float(fn(r)))
    values={g:mean(v) for g,v in grouped.items()}
    return dict(value=mean([fn(r) for r in records]),CI=cluster_ci(values),geometry_groups=len(grouped),n=len(records))

def relation_pairs(groups):return {tuple(sorted((a,b))) for g in groups for i,a in enumerate(g) for b in g[i+1:]}

def partial_score(records):
    values=[]
    for r in records:
        p=r['prediction'];t=r['truth'];pp={tuple(v) for v in p.get('confirmed_precedence',[])};tp={tuple(v) for v in t['confirmed_precedence']}
        pu=relation_pairs(p.get('unresolved_order_groups',[]));tu=relation_pairs(t['unresolved_order_groups'])
        values.append(dict(id=r['id'],group=r['group'],t=r['t'],confirmed_correct=len(pp&tp),confirmed_predicted=len(pp),confirmed_true=len(tp),unresolved_correct=len(pu&tu),unresolved_predicted=len(pu),unresolved_true=len(tu),
            exact_unresolved=p.get('unresolved_order_groups',[])==t['unresolved_order_groups'],unresolved_erroneously_ordered=sum((a,b) in pp or (b,a) in pp for a,b in tu)))
    totals={k:sum(v[k] for v in values) for k in ['confirmed_correct','confirmed_predicted','confirmed_true','unresolved_correct','unresolved_predicted','unresolved_true','unresolved_erroneously_ordered']}
    return dict(**totals,confirmed_precision=totals['confirmed_correct']/totals['confirmed_predicted'] if totals['confirmed_predicted'] else None,
        confirmed_recall=totals['confirmed_correct']/totals['confirmed_true'] if totals['confirmed_true'] else None,
        unresolved_precision=totals['unresolved_correct']/totals['unresolved_predicted'] if totals['unresolved_predicted'] else None,
        unresolved_recall=totals['unresolved_correct']/totals['unresolved_true'] if totals['unresolved_true'] else None,exact_unresolved_rate=mean([v['exact_unresolved'] for v in values]),records=values)

def compute_pairs(records):
    by={(r['id'],r['t']):r for r in records};pairs=[]
    for g in sorted({r['group'] for r in records}):
        for v in ['swap1','swap2'] if records[0]['q']==5 else ['swap1']:
            for t in DECISIONS:
                a,b=by[g+'-correct',t],by[g+'-'+v,t]
                pairs.append(dict(group=g,variant=v,t=t,both_correct=a['order_correct'] and b['order_correct'],orders=[a['prediction']['event_order'],b['prediction']['event_order']],truth=[a['truth']['event_order'],b['truth']['event_order']]))
    return pairs

def score():
    records=load_jsonl(OUT/'predictions.jsonl');main=[r for r in records if r['split']=='test'];methods=sorted({r['method'] for r in main});metrics={};paired={};unknown={};failures=[]
    for method in methods:
        rs=[r for r in main if r['method']==method];visible=[r for r in rs if r['truth']['event_order'] is not None];hidden=[r for r in rs if r['variant']=='mergedA'];pairs=compute_pairs(rs);paired[method]=dict(overall=estimate(pairs,lambda r:r['both_correct']),by_time={str(t):estimate([p for p in pairs if p['t']==t],lambda r:r['both_correct']) for t in DECISIONS},pairs=pairs)
        states=[a==b for r in rs for a,b in zip(r['prediction']['geometry_state'],r['truth_geometry'])];progress=[abs(a-b) for r in rs for a,b in zip(r['prediction']['progress'],r['truth_progress'])]
        confidence=[]
        for lo,hi in [(0,.5),(.5,.9),(.9,.99),(.99,1.00001)]:
            chosen=[r for r in rs if lo<=r['prediction']['observation_confidence']<hi]
            confidence.append(dict(low=lo,high=min(hi,1),n=len(chosen),observability_accuracy=mean([(r['prediction']['observation_confidence']>=.5)==(r['truth']['event_order'] is not None) for r in chosen]),actual_order_accuracy=mean([r['order_correct'] for r in chosen])))
        unknown[method]=dict(unknown_recall=estimate(hidden,lambda r:r['prediction']['event_order'] is None),false_acceptance=estimate(hidden,lambda r:r['prediction']['event_order'] is not None),observable_answer_coverage=estimate(visible,lambda r:r['prediction']['event_order'] is not None),partial_order=partial_score(hidden),
            high_observability_confidence_wrong=[dict(id=r['id'],t=r['t'],confidence=r['prediction']['observation_confidence'],order=r['prediction']['event_order'],truth=r['truth']['event_order']) for r in rs if r['prediction']['observation_confidence']>=.9 and not r['order_correct']],confidence_bins=confidence,confidence_semantics='observability, not probability that the sorted answer is correct; ledger values are deterministic evidence flags')
        wrong=[r for r in visible if r['truth_decision']['first_error'] is not None]
        metrics[method]=dict(pair=paired[method]['overall'],strict_observable_order=estimate(visible,lambda r:r['order_correct']),strict_all_order_or_unknown=estimate(rs,lambda r:r['order_correct']),
            by_time={str(t):dict(pair=paired[method]['by_time'][str(t)],strict=estimate([r for r in visible if r['t']==t],lambda r:r['order_correct'])) for t in DECISIONS},
            state_accuracy=mean(states),progress_mae=mean(progress),action_only=estimate(rs,lambda r:r['prediction']['decision']['action']==r['truth_decision']['action']),action_all_fields=estimate(rs,lambda r:r['decision_correct']),
            first_error_position=estimate(visible,lambda r:r['prediction']['decision']['first_error']==r['truth_decision']['first_error']),wrong_case_first_error=estimate(wrong,lambda r:r['prediction']['decision']['first_error']==r['truth_decision']['first_error']),
            predicted_full_progress_below95=sum(c==2 and p<.95 for r in rs for c,p in zip(r['prediction']['geometry_state'],r['prediction']['progress'])),
            predicted_partial_progress_above985=sum(c==1 and p>=.985 for r in rs for c,p in zip(r['prediction']['geometry_state'],r['prediction']['progress'])),
            observed_ids_geometry_disagreement=sum(set(r['prediction']['observed_ids'])!={j for j,c in enumerate(r['prediction']['geometry_state']) if c>0} for r in rs),
            unknown_recall=unknown[method]['unknown_recall'],observable_answer_coverage=unknown[method]['observable_answer_coverage'])
        for r in rs:
            if r['order_correct'] and r['decision_correct'] and r['prediction']['geometry_state']==r['truth_geometry']:continue
            p=r['prediction'];truth=r['truth'];category=[]
            if p['observed_ids']!=truth['observed_ids']:category.append('instance_presence_or_binding')
            if method.startswith('M4'):
                for j,interval in truth['onset_intervals'].items():
                    observed=p.get('onset_intervals',{}).get(j)
                    if observed is None:category.append('ledger_missing_onset')
                    elif observed!=interval:category.append('ledger_onset_interval_error')
            if (p['event_order'] is None)!=(truth['event_order'] is None):category.append('observability')
            if p['observed_ids']==truth['observed_ids'] and not r['order_correct'] and truth['event_order'] is not None:category.append('history_order_readout')
            if p['geometry_state']!=r['truth_geometry']:category.append('geometry_state')
            failures.append(dict(**r,failure_categories=sorted(set(category)) or ['decision_or_progress']))
    contrasts={}
    for a,b in [('M2','M4'),('M2','M3_K4'),('M2','M3_K8'),('M4','M4_oracle_region'),('M2','M2_oracle_region')]:
        av={(r['group'],r['variant'],r['t']):r for r in paired[a]['pairs']};bv={(r['group'],r['variant'],r['t']):r for r in paired[b]['pairs']};diffs=[dict(group=k[0],t=k[2],delta=float(v['both_correct'])-float(bv[k]['both_correct'])) for k,v in av.items()]
        contrasts[a+'_minus_'+b]=estimate(diffs,lambda r:r['delta'])
    diagnostic={m:dict(pairs=compute_pairs([r for r in records if r['method']==m and r['split']=='diagnostic'])) for m in methods}
    history=load_jsonl(OUT/'history_predictions.jsonl');forgetting={}
    for method in ['M1','M2','M4']:
        hs=[r for r in history if r['method']==method and r['split']=='test' and not r['variant'].startswith('merged')];by=defaultdict(dict)
        for r in hs:by[r['id']][r['t']]=r
        summaries=[]
        for key,ts in by.items():
            correct_early=ts[6]['order_correct'];later=[]
            for t in DECISIONS:
                r=ts[t];expected_norm=list(range(len(r['truth']['event_order'])))
                later.append(dict(t=t,order_correct=r['order_correct'],early_correct_later_wrong=correct_early and not r['order_correct'],wrongly_normative=r['prediction']['event_order']==expected_norm and r['truth']['event_order']!=expected_norm))
            summaries.append(dict(id=key,group=ts[6]['group'],early_t6_correct=correct_early,later=later))
        forgetting[method]=dict(early_t6_order_accuracy=mean([s['early_t6_correct'] for s in summaries]),trajectories=summaries,early_correct_later_wrong=sum(v['early_correct_later_wrong'] for s in summaries for v in s['later']),late_wrongly_normative=sum(v['wrongly_normative'] for s in summaries for v in s['later']))
    spatial=json.loads((OUT/'spatial_predictions.json').read_text());unique={r['group']:r for r in spatial if r['split']=='test'};ious=[v for r in unique.values() for v in r['ious']]
    save(OUT/'metrics.json',dict(methods=metrics,contrasts=contrasts,diagnostic=diagnostic,spatial=dict(instance_IoU50_match=mean([v>=.5 for v in ious]),mean_iou=mean(ious),independent_groups=len(unique),instances=len(ious)),scope='20 independent test geometry groups, single seed, D0 only',forgetting=forgetting))
    save(OUT/'paired_results.json',paired);save(OUT/'unknown_results.json',unknown);save(OUT/'failure_cases.json',failures)
    if paired['M1']['overall']['value']!=0:raise RuntimeError('B3 identical-input bound violated')
    for name in ['M0','M5']:
        assert paired[name]['overall']['value']==1 and unknown[name]['unknown_recall']['value']==1
    print(json.dumps({m:dict(pair=metrics[m]['pair']['value'],unknown=metrics[m]['unknown_recall']['value'],coverage=metrics[m]['observable_answer_coverage']['value']) for m in methods},indent=2))

if __name__=='__main__':score()
