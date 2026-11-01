"""Read historical P1 evidence and sample local media without rewriting P1."""
import argparse
from collections import Counter
import json
from pathlib import Path

from .contracts import save
from .media import decode,validate_media

P1=Path('data/research/runs/p1_full_server_2026-10-30')


def intake():
    release=json.loads(Path('docs/project/stages/P1-release.json').read_text())
    status=json.loads((P1/'request_status.json').read_text())
    execution=json.loads((P1/'execution_summary.json').read_text())
    manifest=json.loads((P1/'manifest.json').read_text())
    answers=json.loads((P1/'understanding_answers_and_sampling.json').read_text())
    aux=json.loads((P1/'SO01_auxiliary_summary.json').read_text())
    atlas=json.loads((P1/'failure_atlas_auxiliary.json').read_text())
    review=json.loads((P1/'offline_review_manifest.json').read_text())
    counts={k:dict(Counter(r['status'] for r in rows)) for k,rows in status['requests'].items()}
    conditions=[]
    indexed={r['id']:r for r in status['requests']['generation']}
    for condition in sorted({r['condition'] for r in manifest['generation']}):
        rows=[r for r in manifest['generation'] if r['condition']==condition]
        conditions.append({'condition':condition,'attempts':len(rows),'statuses':dict(Counter(indexed[r['id']]['status'] for r in rows)),
                           'geometry_permissions':sorted({r['geometry_permission'] for r in rows})})
    roots=[Path('private/p1_native_pilot_issue3_2026-10-30/requests/N076-T_G0_native_simple-s11'),
           Path('private/p1_full_server_2026-10-30/requests/N019-T_G0_blank_i2v-s11'),
           Path('private/p1_full_server_2026-10-30/diagnostics/controls/O-N076'),
           Path('private/p1_full_server_2026-10-30/requests/SO00-codec-N076')]
    sampled=[]
    for root in roots:
        clips=sorted(root.rglob('*.mp4'))
        row={'root':str(root),'root_available':root.exists(),'matching_MP4_files':len(clips)}
        if clips:
            frames,pts=decode(clips[0]);row.update(path=str(clips[0]),status='decoded',
                media=validate_media('native_video',frames,pts),scope='one deterministic first MP4 per selected root; content not re-human-reviewed')
        else:row['status']='unavailable'
        sampled.append(row)
    understanding=Path('private/p1_full_server_2026-10-30/requests/SO01-C-N076-full_prefix')
    samplingfiles=sorted(understanding.rglob('actual_sampling.json'))
    samplingcheck={'root':str(understanding),'sampling_paths':[str(p) for p in samplingfiles],
                   'archived_arrays':len(list(understanding.rglob('*read_RGB.npz'))),
                   'raw_answer_count':sum(len(a['raw_answer_records']) for a in answers),
                   'sampling_records':sum(len(a['sampling']) for a in answers)}
    return {'status':'historical_evidence_reused_read_only','counts':counts,'conditions':conditions,
        'original_execution_counts':execution['counts'],'formal_phase_status':release['status'],
        'EVAL_02_current':release['EVAL_02'],'startup_stale_fields':['p1_state_expected.human_review_status','P1 unclosed description'],
        'human_evidence':release['coarse_human_screening'],'formal_human_metrics':None,
        'human_submission_scope':release['human_record_status'],'new_human_tasks':0,
        'formal_facet_export_count':release['formal_human_reviews'],
        'original_offline_package_snapshot':review,'sampled_private_media':sampled,'sampling_sample':samplingcheck,
        'prior_backup_audit_scope':'2192-file SHA check belongs to historical P1 run; not repeated in this task',
        'SO01_summary':aux,'auxiliary_atlas_records':len(atlas['records']),
        'failed_generation':[r for r in status['requests']['generation'] if r['status']=='failed'],
        'models_newly_run':0,'hypotheses':{k:'unverified' for k in ['H_K','H_V','H_U','H_UE','H_R']}}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    if Path(a.output).exists():raise ValueError('Use a new intake path; preserve earlier audits')
    value=intake();save(a.output,value);print(json.dumps({'counts':value['counts'],'media':[(r['status'],r.get('media',{}).get('frames')) for r in value['sampled_private_media']]}))

if __name__=='__main__':main()
