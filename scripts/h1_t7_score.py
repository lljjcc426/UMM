"""Preregistered mixed-Q T7 scoring and geometry-clustered paired effects."""
import json
from collections import defaultdict
import numpy as np
from h1_event_data import save
from h1_early_history_score import load_jsonl,partial_score
from h1_t7_data import OUT,DECISIONS

def estimate(records,fn):
    grouped=defaultdict(list)
    for r in records:grouped[r['group']].append(float(fn(r)))
    if not records:return dict(value=None,CI=None,n=0,geometry_groups=0)
    groups=sorted(grouped);sums=np.array([sum(grouped[g]) for g in groups]);counts=np.array([len(grouped[g]) for g in groups]);rng=np.random.default_rng(42)
    choices=rng.integers(0,len(groups),(2000,len(groups)));values=sums[choices].sum(1)/counts[choices].sum(1)
    return dict(value=float(sums.sum()/counts.sum()),geometry_balanced=float(np.mean(sums/counts)),CI=np.quantile(values,[.025,.975]).tolist(),n=int(counts.sum()),geometry_groups=len(groups))

def pairs(records):
    by={(r['group'],r['variant'],r['t']):r for r in records};result=[]
    for g in sorted({r['group'] for r in records}):
        q=next(r['q'] for r in records if r['group']==g)
        for v in ['swap1']+(['swap2'] if q==5 else []):
            for t in DECISIONS:
                a,b=by[g,'correct',t],by[g,v,t]
                result.append(dict(group=g,q=q,family=a['family'],variant=v,t=t,both_correct=a['order_correct'] and b['order_correct']))
    return result

def partial_intervals(summary):
    rs=summary['records'];groups=sorted({r['group'] for r in rs});rng=np.random.default_rng(42);ci={}
    for key,a,b in [('confirmed_precision','confirmed_correct','confirmed_predicted'),('confirmed_recall','confirmed_correct','confirmed_true'),('unresolved_precision','unresolved_correct','unresolved_predicted'),('unresolved_recall','unresolved_correct','unresolved_true')]:
        numerator=np.array([sum(r[a] for r in rs if r['group']==g) for g in groups]);denominator=np.array([sum(r[b] for r in rs if r['group']==g) for g in groups]);idx=rng.integers(0,len(groups),(2000,len(groups)))
        n=numerator[idx].sum(1);d=denominator[idx].sum(1);valid=d>0
        ci[key]=dict(value=summary[key],CI=np.quantile(n[valid]/d[valid],[.025,.975]).tolist() if valid.any() else None)
    ci['exact_unresolved']=estimate(rs,lambda r:r['exact_unresolved']);return ci

def macro_f1(records):
    truth=[c for r in records for c in r['truth_geometry']];pred=[c for r in records for c in r['prediction']['geometry_state']];scores=[]
    for c in [0,1,2]:
        tp=sum(a==b==c for a,b in zip(truth,pred));fp=sum(a!=c and b==c for a,b in zip(truth,pred));fn=sum(a==c and b!=c for a,b in zip(truth,pred))
        scores.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.)
    return dict(macro=float(np.mean(scores)),by_class=scores)

def score():
    all_records=load_jsonl(OUT/'predictions.jsonl');records=[r for r in all_records if r['variant']!='mergedB'];methods=sorted({r['method'] for r in records})
    metrics={};paired={};uncertainty={};failures=[];onsets={}
    for method in methods:
        rs=[r for r in records if r['method']==method];visible=[r for r in rs if r['truth']['event_order'] is not None];hidden=[r for r in rs if r['variant']=='mergedA'];ps=pairs(rs);paired[method]=ps
        accepted=[r for r in visible if r['prediction']['event_order'] is not None]
        partial=partial_score(hidden)
        uncertainty[method]=dict(unknown_recall=estimate(hidden,lambda r:r['prediction']['event_order'] is None),unknown_false_acceptance=estimate(hidden,lambda r:r['prediction']['event_order'] is not None),
            correct_usable_coverage=estimate(visible,lambda r:r['order_correct']),raw_answer_coverage=estimate(visible,lambda r:r['prediction']['event_order'] is not None),
            visible_wrong_acceptance=estimate(visible,lambda r:r['prediction']['event_order'] is not None and not r['order_correct']),accepted_answer_error=estimate(accepted,lambda r:not r['order_correct']),partial_order=partial,partial_intervals=partial_intervals(partial))
        metrics[method]=dict(pair=estimate(ps,lambda r:r['both_correct']),strict_observable=estimate(visible,lambda r:r['order_correct']),
            correct_usable_coverage=uncertainty[method]['correct_usable_coverage'],raw_answer_coverage=uncertainty[method]['raw_answer_coverage'],
            action_all_fields=estimate(rs,lambda r:r['decision_correct']),first_error_position=estimate(visible,lambda r:r['prediction']['decision']['first_error']==r['truth_decision']['first_error']),
            geometry_macro_f1=macro_f1(rs),progress_mae=estimate(rs,lambda r:np.mean(np.abs(np.array(r['prediction']['progress'])-r['truth_progress']))),
            progress_inconsistent=sum((c==2 and p<.95) or (c==0 and p>.02) or (c==1 and p>=.985) for r in rs for c,p in zip(r['prediction']['geometry_state'],r['prediction']['progress'])),
            by_q={str(q):estimate([p for p in ps if p['q']==q],lambda p:p['both_correct']) for q in [3,5]},
            by_time={str(t):estimate([p for p in ps if p['t']==t],lambda p:p['both_correct']) for t in DECISIONS},
            by_family={f:estimate([p for p in ps if p['family']==f],lambda p:p['both_correct']) for f in sorted({p['family'] for p in ps})})
        event_records=[]
        for r in rs:
            if r['t']!=23:continue
            for j,true in r['truth']['onset_intervals'].items():
                pred=r['prediction'].get('onset_intervals',{}).get(j)
                category='missing' if pred is None else 'exact' if pred==true else 'early' if pred[1]<true[1] else 'late' if pred[0] is not None and pred[0]>=true[1] else 'wide_or_shifted'
                event_records.append(dict(group=r['group'],id=r['id'],instance=int(j),true=true,predicted=pred,category=category))
        onsets[method]=dict(exact=estimate(event_records,lambda r:r['category']=='exact'),counts={c:sum(r['category']==c for r in event_records) for c in ['exact','early','late','missing','wide_or_shifted']},records=event_records)
        for r in rs:
            p=r['prediction'];truth=r['truth'];cats=[]
            if p['observed_ids']!=truth['observed_ids']:cats.append('instance_detection')
            if not r['order_correct']:cats.append('actual_history')
            if not r['decision_correct']:cats.append('action_or_first_error')
            if p['geometry_state']!=r['truth_geometry']:cats.append('geometry_state')
            if truth['event_order'] is None and (p.get('unresolved_order_groups')!=truth['unresolved_order_groups'] or p.get('confirmed_precedence')!=truth['confirmed_precedence']):cats.append('partial_order')
            if cats:failures.append(dict(**r,failure_categories=cats))
    effects={}
    for a,b in [('E10','E00'),('E11','E01'),('E01','E00'),('E11','E10')]:
        by={(p['group'],p['variant'],p['t']):p for p in paired[b]};diff=[dict(group=p['group'],delta=float(p['both_correct'])-float(by[p['group'],p['variant'],p['t']]['both_correct'])) for p in paired[a]]
        effects[a+'_minus_'+b]=estimate(diff,lambda r:r['delta'])
    by={m:{(p['group'],p['variant'],p['t']):float(p['both_correct']) for p in paired[m]} for m in ['E00','E01','E10','E11']}
    interaction=[dict(group=k[0],delta=by['E11'][k]-by['E10'][k]-by['E01'][k]+by['E00'][k]) for k in by['E00']]
    effects['interaction']=estimate(interaction,lambda r:r['delta'])
    masks=json.loads((OUT/'mask_predictions.json').read_text());mask_metrics={}
    for method in ['A0','A1']:
        current=[r for r in masks if r['method']==method];instances=[dict(group=r['group'],q=r['q'],family=r['family'],iou=v,identity=r['identity_correct'][j]) for r in current for j,v in enumerate(r['ious'])]
        mask_metrics[method]=dict(match=estimate(instances,lambda r:r['iou']>=.5),mean_iou=estimate(instances,lambda r:r['iou']),identity=estimate(instances,lambda r:r['identity']),
            by_family={f:dict(match=estimate([r for r in instances if r['family']==f],lambda r:r['iou']>=.5),identity=estimate([r for r in instances if r['family']==f],lambda r:r['identity'])) for f in sorted({r['family'] for r in instances})},
            by_q={str(q):estimate([r for r in instances if r['q']==q],lambda r:r['iou']>=.5) for q in [3,5]},shared_region_recall=sum(r['shared_instance_correct'] for r in current)/max(1,sum(r['shared_instance_total'] for r in current)))
    save(OUT/'factorial_results.json',metrics);save(OUT/'paired_results.json',paired);save(OUT/'paired_effects.json',effects);save(OUT/'uncertainty_results.json',uncertainty)
    save(OUT/'mask_metrics.json',mask_metrics);save(OUT/'onset_metrics.json',onsets);save(OUT/'failure_cases.json',failures)
    print(json.dumps({m:dict(pair=v['pair']['value'],strict=v['strict_observable']['value'],raw_coverage=v['raw_answer_coverage']['value']) for m,v in metrics.items()},indent=2))

if __name__=='__main__':score()
