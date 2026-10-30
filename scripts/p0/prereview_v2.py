"""Candidate prereview fix; development data only, never overwrite frozen evaluation."""
from collections import Counter
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import time

import numpy as np

from scripts.p0.ai_prereview import inspect_rgb, read_rgb, SETTINGS

RUN=Path('data/research/runs/p0_program_ai_audit_2026-10-28')


def disjoint_endpoint_regions(coords,start,end):
    """Shrink nearest-endpoint regions until distinct evidence is available.

    A region needs at least two pixels; coincident endpoints or overlapping
    evidence remain unknown. No direction or timing threshold is retuned.
    """
    ranked=[np.argsort(((coords-point)**2).sum(axis=1)) for point in [start,end]]
    for count in range(min(SETTINGS['endpoint_pixels'],len(coords)//2),1,-1):
        a,b=ranked[0][:count],ranked[1][:count]
        if not np.intersect1d(a,b).size:return [a,b]
    return [np.array([],dtype=int),np.array([],dtype=int)]


def inspect_rgb_v2(frames,times,masks,medians):
    result=inspect_rgb(frames,times,masks,medians,anchor_selector=disjoint_endpoint_regions)
    result['review_method']='Candidatev2: same prereview thresholds; nearest endpoint regions must be disjoint and contain at least2 pixels'
    result['candidate_version']='p0-ai-prereview-v2-dev-only'
    result['independent_validation_completed']=False
    return result


def development():
    target=RUN/'development_v2_predictions.jsonl'
    if target.exists():raise ValueError('Preserve completed development result; use another version for changes')
    method=json.loads((RUN/'method_v2_frozen.json').read_text())
    templates={t['template_id']:t for t in json.loads(Path('data/research/datasets/p0_stroke_synthetic_v1/templates.json').read_text())['templates']}
    manifest=Path('data/research/datasets/p0_stroke_synthetic_v1/manifest_observer_dev.jsonl')
    samples=[json.loads(line) for line in manifest.read_text().splitlines()]
    with gzip.open('private/p0_ai_prereview_2026-10-28/svg_masks.json.gz','rt') as handle:raw=json.load(handle)
    masks={};rows=[];started=time.perf_counter()
    for s in samples:
        key=s['template_id']+'|'+s['renderer_id']
        if key not in masks:
            values=raw[key];array=np.zeros((len(values),128*128),bool)
            for i,indices in enumerate(values):array[i,indices]=True
            masks[key]=array.reshape(-1,128,128)
        frames,times,_=read_rgb(s['media_path'])
        result=inspect_rgb_v2(frames,times,masks[key],templates[s['template_id']]['medians'])
        # Construction labels enter only after the candidate decision.
        rows.append(dict(sample_id=s['sample_id'],character=s['character'],role='observer_dev',
                         case=s['evaluation_only']['construction_case'],**result))
    target.write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows))
    summary=dict(version='p0-ai-prereview-v2-dev-only',method_frozen_at=method['frozen_at_utc'],
        samples=len(rows),character_groups=len({s['source_group_id'] for s in samples}),
        decisions=dict(Counter(r['decision'] for r in rows)),
        by_construction_case={case:dict(Counter(r['decision'] for r in rows if r['case']==case)) for case in sorted({r['case'] for r in rows})},
        construction_negative_confident_accepts=sum(r['case']!='correct' and r['decision']=='correct' for r in rows),
        role='observer_dev_only',holdout_rescored=False,thresholds_retuned=False,
        independent_validation_completed=False,scientific_acceptance=False,wall_seconds=time.perf_counter()-started,GPU_hours=0)
    (RUN/'development_v2_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':development()
