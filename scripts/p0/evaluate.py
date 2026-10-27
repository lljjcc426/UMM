"""Calibrate on development only; freeze before a single held-out evaluation."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from scripts.p0.build_data import DATA, RUN, ROLES
from scripts.p0.geometry import read_clip, stroke_geometry
from scripts.p0.observer import DEFAULT_THRESHOLDS, observe, one_sided_upper, model_input


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def rows_for(role):
    return [json.loads(line) for line in (DATA/f'manifest_{role}.jsonl').read_text().splitlines()]


def summarize(rows):
    groups = defaultdict(list)
    classes = defaultdict(Counter)
    for row in rows:
        groups[row['source_group_id']].append(row)
        classes[row['case']][row['decision']] += 1
    # Unknown abstentions cannot manufacture high coverage: report coverage for
    # both all clearly constructed cases and correct controls separately.
    clear = [r for r in rows if r['case'] not in ['flash','sparse']]
    positives = [r for r in rows if r['case']=='correct']
    negatives = [r for r in rows if r['case']!='correct']
    bad_groups = [g for g, values in groups.items()
                  if any(r['case']!='correct' and r['decision']=='correct' for r in values)]
    invalid = sum(r['decision']=='invalid' for r in rows)
    coverage = sum(r['decision'] in ['correct','incorrect'] for r in clear)/len(clear) if clear else 0.
    positive_coverage = sum(r['decision'] in ['correct','incorrect'] for r in positives)/len(positives) if positives else 0.
    positive_acceptance = sum(r['decision']=='correct' for r in positives)/len(positives) if positives else 0.
    upper = one_sided_upper(len(bad_groups), len(groups))
    return dict(attempts=len(rows), valid_outputs=len(rows)-invalid, invalid_outputs=invalid,
                decisions=dict(Counter(r['decision'] for r in rows)), by_case={k:dict(v) for k,v in classes.items()},
                independent_groups=len(groups), false_accept_groups=len(bad_groups),
                false_accept_group_ids=bad_groups, false_accept_group_upper95_one_sided=upper,
                negative_attempts=len(negatives), negative_false_accepts=sum(r['decision']=='correct' for r in negatives),
                clear_constructed_attempts=len(clear), clear_coverage=coverage,
                positive_control_attempts=len(positives), positive_control_coverage=positive_coverage,
                positive_control_acceptance=positive_acceptance,
                ambiguous_attempts=sum(r['case'] in ['flash','sparse'] for r in rows),
                ambiguous_correct_accepts=sum(r['case'] in ['flash','sparse'] and r['decision']=='correct' for r in rows),
                auto_gate_passed=coverage>=.9 and positive_coverage>=.9 and positive_acceptance>=.9
                                and upper is not None and upper<=.05,
                human_reference_status='pending; labels currently synthetic constructions, not independent human gold',
                scientific_acceptance=False)


def score(role, candidates):
    templates = {t['template_id']:t for t in json.loads((DATA/'templates.json').read_text())['templates']}
    geometry = {}
    results = [[] for _ in candidates]
    samples = rows_for(role)
    for index, sample in enumerate(samples):
        key = sample['template_id'], sample['renderer_id']
        if key not in geometry:
            geometry[key] = stroke_geometry(templates[key[0]],key[1])
        try:
            frames, times, _ = read_clip(Path(sample['media_path']))
            for rows, thresholds in zip(results, candidates):
                prediction = observe(frames, *geometry[key], thresholds)
                # Labels and schedules are joined AFTER the RGB-only observation.
                rows.append(dict(sample_id=sample['sample_id'], source_group_id=sample['source_group_id'],
                                 renderer=sample['renderer_id'], case=sample['evaluation_only']['construction_case'],
                                 expected=sample['evaluation_only']['expected'], **prediction))
        except (OSError, ValueError) as exc:
            for rows in results:
                rows.append(dict(sample_id=sample['sample_id'],source_group_id=sample['source_group_id'],
                                 renderer=sample['renderer_id'],case=sample['evaluation_only']['construction_case'],
                                 decision='invalid',error=repr(exc)))
        if (index+1)%128==0:
            print(role,index+1,'/',len(samples),flush=True)
    return results


def calibrate():
    started=time.perf_counter()
    candidates=[]
    for completion in [.92,.96,.99]:
        t=deepcopy(DEFAULT_THRESHOLDS)
        t['complete']=completion
        candidates.append(t)
    all_results=score('observer_dev', candidates)
    summaries=[summarize(rows) for rows in all_results]
    # Favor safety first; tune solely on development. Positive-control acceptance
    # breaks ties without consulting any held-out result.
    winner=max(range(len(candidates)),key=lambda i:(-summaries[i]['false_accept_groups'],
               summaries[i]['clear_coverage'],summaries[i]['positive_control_acceptance']))
    freeze=dict(protocol_id='stroke-video-v2',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
                selected_candidate=winner,thresholds=candidates[winner],
                development_manifest_sha256=hashlib.sha256((DATA/'manifest_observer_dev.jsonl').read_bytes()).hexdigest(),
                observer_source_sha256=hashlib.sha256(Path('scripts/p0/observer.py').read_bytes()).hexdigest(),
                geometry_source_sha256=hashlib.sha256(Path('scripts/p0/geometry.py').read_bytes()).hexdigest(),
                selection_rule='Minimize development groups with any false accept; maximize clear coverage then positive acceptance',
                candidates=[dict(thresholds=t,summary=s) for t,s in zip(candidates,summaries)],
                holdout_accessed=False,wall_seconds=time.perf_counter()-started)
    save(RUN/'threshold_freeze.json',freeze)
    (RUN/'development_predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in all_results[winner]))
    save(RUN/'development_metrics.json',summaries[winner])
    print('Frozen candidate',winner,summaries[winner]['clear_coverage'],flush=True)


def evaluate():
    started=time.perf_counter()
    freeze=json.loads((RUN/'threshold_freeze.json').read_text())
    # One source identity check enforces the declared freeze, not a repeated scan.
    if hashlib.sha256(Path('scripts/p0/observer.py').read_bytes()).hexdigest()!=freeze['observer_source_sha256']:
        raise RuntimeError('Observer changed after threshold freeze')
    prediction_path=RUN/'holdout_predictions.jsonl'
    if prediction_path.exists():
        raise RuntimeError('Held-out predictions already exist; preserve the original evaluation')
    rows=score('observer_holdout',[freeze['thresholds']])[0]
    prediction_path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    metrics=summarize(rows)
    metrics['by_renderer']={name:summarize([r for r in rows if r['renderer']==name])
                            for name in sorted({r['renderer'] for r in rows})}
    # Last-frame baseline intentionally measures the same final geometry. It
    # demonstrates the limitation of final-image agreement on matched pairs.
    matched=[r for r in rows if r['case'] in ['correct','swap','reverse']]
    metrics['last_frame_baseline']=dict(attempts=len(matched),
        correct_controls=sum(r['case']=='correct' for r in matched),
        wrong_controls=sum(r['case']!='correct' for r in matched),
        final_iou_threshold=.98, accepted_wrong=sum(r['case']!='correct' and r.get('final_iou',0)>=.98 for r in matched),
        accepted_correct=sum(r['case']=='correct' and r.get('final_iou',0)>=.98 for r in matched))
    metrics.update(frozen_at_utc=freeze['frozen_at_utc'],evaluated_at_utc=datetime.now(timezone.utc).isoformat(),
                   wall_seconds=time.perf_counter()-started,thresholds_retuned_after_holdout=False,
                   limits=['G1 known reference geometry and fixed camera only',
                           'No independent human labels yet',
                           'No real generator-output domain calibration; reserved for EVAL-02',
                           'Independent binomial-group assumption is conditional; groups share source library and renderer',
                           'Synthetic renderer/width variation is not independent font/writer generalization'])
    save(RUN/'holdout_metrics.json',metrics)
    print(json.dumps({k:v for k,v in metrics.items() if k in ['attempts','clear_coverage','false_accept_groups','false_accept_group_upper95_one_sided','auto_gate_passed']},indent=2),flush=True)


def input_audit():
    # Observable future frames contain a deliberately unique marker. The P
    # allowlist must exclude it; T receives no frames/targets at all.
    sample={'character':'十','evaluation_only':{'answer':'SENTINEL'},'training_targets':{'future':'SENTINEL'}}
    frames=np.full((4,8,8,3),255,dtype=np.uint8)
    frames[2:]=17
    times=np.array([0.,.1,.2,.3])
    t=model_input(sample,frames,times,'T')
    p=model_input(sample,frames,times,'P',prefix_end=.1)
    ok=set(t)=={'character','instruction'} and len(p['prefix_rgb'])==2 and bool((p['prefix_rgb']==255).all())
    save(RUN/'input_permission_audit.json',dict(passed=ok,T_keys=list(t),P_keys=list(p),
        P_retained_frame_count=len(p['prefix_rgb']),future_marker_absent=bool((p['prefix_rgb']==255).all()),
        evaluation_truth_passed_to_observer=False,scope='Implemented T/P allowlist; no native model training performed'))
    if not ok:
        raise RuntimeError('Input permission audit failed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['calibrate','evaluate','input_audit'])
    args=parser.parse_args()
    {'calibrate':calibrate,'evaluate':evaluate,'input_audit':input_audit}[args.stage]()
