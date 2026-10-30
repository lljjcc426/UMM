"""Summarize the completed fixed human batch without changing its labels or scorer."""
from collections import Counter
from datetime import datetime, timezone
import csv
import json
from pathlib import Path
import time

from scripts.p0.observer import one_sided_upper

SOURCE = Path('data/research/runs/p0_final_calibration_2026-10-28')
OUTPUT = Path('data/research/runs/p0_human_acceptance_2026-10-29')
PRIVATE = Path('private/p0_final_calibration_2026-10-28')
MODELS = ['frozen_observer', 'AI_v1', 'AI_v2']


def save(name, value):
    (OUTPUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def table(name, rows):
    with (OUTPUT/name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def scope_metrics(rows):
    clear = [r for r in rows if r['human_reference'] != 'unknown']
    negative = {r['writer_id'] for r in clear if r['human_reference'] == 'incorrect'}
    result = {}
    for model in MODELS:
        failures = {r['writer_id'] for r in clear if r['human_reference'] == 'incorrect' and r[model] == 'correct'}
        matrix = {human: {auto: sum(r['human_reference'] == human and r[model] == auto for r in rows)
                          for auto in ['correct', 'incorrect', 'unknown']}
                  for human in ['correct', 'incorrect', 'unknown']}
        result[model] = dict(attempts=len(rows), human_reference_counts=dict(Counter(r['human_reference'] for r in rows)),
            confusion=matrix, clear_reference_attempts=len(clear),
            clear_coverage=sum(r[model] != 'unknown' for r in clear)/len(clear) if clear else None,
            negative_writer_groups=len(negative), false_accept_writer_groups=len(failures),
            false_accept_group_fraction=len(failures)/len(negative) if negative else None,
            false_accept_upper95=one_sided_upper(len(failures), len(negative)))
    return result


def summarize():
    started = time.monotonic()
    if (OUTPUT/'analysis_summary.json').exists():
        raise ValueError('Preserve completed analysis; use a separately dated/versioned output for another analysis')
    result = json.loads((OUTPUT/'human_calibration_results.json').read_text())
    pack = json.loads((PRIVATE/'pack_frozen.json').read_text())
    tasks = {t['id']: t for t in pack['tasks']}
    predictions = {r['id']: r for r in map(json.loads, (SOURCE/'predictions.jsonl').read_text().splitlines())}
    pairs = result['pairs']; videos = result['video_reference']
    joined = []
    for pair in pairs:
        t = tasks[pair['internal_id']]
        joined.append(dict(internal_id=pair['internal_id'], blind_id=pair['blind_id'], kind=pair['kind'], character=t['character'],
            reviewer1=json.dumps(pair['reviewer1'].get('judgments', pair['reviewer1'].get('decision')), ensure_ascii=False),
            reviewer2=json.dumps(pair['reviewer2'].get('judgments', pair['reviewer2'].get('decision')), ensure_ascii=False),
            paired_reference=pair['paired_reference'], disagreement=pair['disagreement'],
            reasons1=json.dumps(pair['reviewer1']['reasons'], ensure_ascii=False), reasons2=json.dumps(pair['reviewer2']['reasons'], ensure_ascii=False),
            notes1=pair['reviewer1']['notes'], notes2=pair['reviewer2']['notes']))
    table('per_sample_evidence.csv', joined)
    normative = [p for p in pairs if p['kind'] == 'normative']
    accepted = [r for r in joined if r['kind'] == 'normative' and r['paired_reference'] == 'pass']
    quarantine = [r for r in joined if r['kind'] == 'normative' and r['paired_reference'] != 'pass']
    table('normative_accepted_candidates.csv', accepted)
    table('normative_quarantined_candidates.csv', quarantine)
    table('independent_record_judgments.csv', [r for r in joined if r['kind'] == 'record'])
    paired_by_id = {p['internal_id']: p for p in pairs}
    agreement = {}
    for kind in ['normative', 'rgb', 'record']:
        rows = [p for p in pairs if p['kind'] == kind]
        n = sum(not p['disagreement'] for p in rows)
        agreement[kind] = dict(tasks=len(rows), exact_agreement=n, disagreement=len(rows)-n,
            exact_agreement_fraction=n/len(rows), paired_reference_counts=dict(Counter(p['paired_reference'] for p in rows)))
    save('agreement.json', dict(by_kind=agreement,
        normative_facets={field: dict(Counter(p['reviewer1']['judgments'][field]
            if p['reviewer1']['judgments'][field] == p['reviewer2']['judgments'][field] else 'unknown'
            for p in normative)) for field in ['identity_order', 'direction']},
        RGB_reference_after_normative_gate=result['metrics']['frozen_observer']['human_reference_counts'],
        RGB_correct_downgraded_to_unknown=[v['id'] for v in videos if paired_by_id[v['id']]['paired_reference']=='correct' and v['human_reference']=='unknown']))
    scopes = dict(frozen_collector_all144=videos,
        excluding_predeclared_two_frame_controls=[v for v in videos if predictions[v['id']]['nominal_case'] != 'sparse'],
        posthoc_normative_pass=[v for v in videos if v['normative_reference']=='pass'],
        posthoc_normative_pass_observable=[v for v in videos if v['normative_reference']=='pass' and predictions[v['id']]['nominal_case']!='sparse'])
    save('scope_metrics.json', dict(metrics={s: scope_metrics(v) for s, v in scopes.items()},
        label_policy='All actual button judgments, reasons and notes unchanged. Scopes are filters, not rewritten human labels.',
        two_frame_scope='16 controls predeclared insufficient temporal evidence; separate from actual incorrect button counts.',
        posthoc_scope='Normative pass subsets are descriptive only; not a replacement primary gate or independently selected validation.'))
    false_accepts = []
    for v in videos:
        failing = [m for m in MODELS if v['human_reference']=='incorrect' and v[m]=='correct']
        if failing:
            t=tasks[v['id']]; p=paired_by_id[v['id']]
            false_accepts.append(dict(id=v['id'], character=t['character'], writer_id=v['writer_id'],
                nominal_case=predictions[v['id']]['nominal_case'], human_reference=v['human_reference'],
                normative_reference=v['normative_reference'], accepted_by=','.join(failing),
                reasons1=json.dumps(p['reviewer1']['reasons'], ensure_ascii=False), reasons2=json.dumps(p['reviewer2']['reasons'], ensure_ascii=False)))
    table('false_accepts.csv', false_accepts)
    by_case = {}
    for case in ['source_order','swap','reverse','missing','extra','simultaneous','early_next','disappear','blank','sparse']:
        rows=[v for v in videos if predictions[v['id']]['nominal_case']==case]
        by_case[case]=dict(attempts=len(rows), human_reference=dict(Counter(v['human_reference'] for v in rows)),
            false_accepts={m:sum(v['human_reference']=='incorrect' and v[m]=='correct' for v in rows) for m in MODELS})
    save('case_analysis.json', dict(by_case=by_case, false_accept_root='All accepted human negatives are recorded-source-order candidates, with no accepted constructed negative among human-confirmed negatives.',
        reference_geometry_limit='Observer receives masks/progress indexed by the same recorded-source strokes; this does not establish conformity to the independent normative standard.',
        old_zero64='Original same-source constructed-case0/64 retained; do not pool or generalize it as new human-referenced performance.'))
    sparse = [p for p in pairs if p['kind']=='rgb' and predictions[p['internal_id']]['nominal_case']=='sparse']
    flags=[]
    for p in normative:
        for rid in ['reviewer1','reviewer2']:
            a=p[rid]
            if all(x=='pass' for x in a['judgments'].values()) and a['reasons']:
                flags.append(dict(id=p['internal_id'], reviewer=rid, judgments=a['judgments'], reasons=a['reasons'], notes=a['notes']))
    action_audit={}
    for rid in ['reviewer1','reviewer2']:
        rgb=[p[rid] for p in pairs if p['kind']=='rgb']
        action_audit[rid]=dict(normative_sequence_open=sum(p[rid]['view_actions']['sequence_open'] for p in normative),
            normative_total=64, RGB_play_clicked=sum(a['view_actions']['play_clicked'] for a in rgb), RGB_total=144,
            RGB_last_frame_visited=sum(len(tasks[p['internal_id']]['frame_timestamps'])-1 in p[rid]['view_actions']['frames'] for p in pairs if p['kind']=='rgb'))
    save('annotation_scope_audit.json', dict(sparse_controls=len(sparse), sparse_both_incorrect=sum(p['paired_reference']=='incorrect' for p in sparse),
        sparse_both_only_temporal_ambiguity=sum(all(p[r]['reasons']==['temporal_ambiguity'] for r in ['reviewer1','reviewer2']) for p in sparse),
        sparse_actual_records=[dict(id=p['internal_id'], reviewer1=p['reviewer1'], reviewer2=p['reviewer2']) for p in sparse],
        label_vs_reason_flags=flags, actions=action_audit, actions_are_not_attention_proof=True,
        original_labels_overridden=False, extra_human_round_assigned=False,
        interpretation='Two-frame temporal ambiguity is an observability limit; incorrect buttons cannot prove missing unobserved events. Keep button-level primary result and separately report the predeclared temporal scope.'))
    primary=result['metrics']['frozen_observer']
    gates={m:dict(coverage_min=.9, observed_coverage=result['metrics'][m]['clear_coverage'],
        coverage_met=result['metrics'][m]['clear_coverage']>=.9, false_accept_upper95_max=.05,
        observed_false_accept_upper95=result['metrics'][m]['false_accept_upper95'],
        false_accept_met=result['metrics'][m]['false_accept_upper95']<=.05,
        overall_met=(result['metrics'][m]['clear_coverage']>=.9 and result['metrics'][m]['false_accept_upper95']<=.05)) for m in MODELS}
    save('gate_assessment.json', dict(gates=gates, primary_method='frozen_observer', thresholds_changed=False,
        raw_labels_changed=False, methods_selected_or_promoted=False,
        observable_scope_does_not_resolve_false_accept_failure=True, posthoc_subsets_do_not_replace_frozen_acceptance=True,
        DATA_01_status='blocked_reference_quality_and_qualified_crossed_subset', EVAL_01_status='blocked_frozen_gate_failed_negative_result',
        P0_status='not_accepted', human_work_complete=True, new_human_tasks=0))
    save('analysis_summary.json', dict(completed_at_utc=datetime.now(timezone.utc).isoformat(), independent_reviewers=2,
        reviewer_completion={'1':216,'2':216}, unique_tasks=216, formal_submissions=432, raw_versions=441,
        normative_reference=result['consensus_counts']['normative'], RGB_buttons=result['consensus_counts']['rgb'],
        RGB_reference=primary['human_reference_counts'], independent_records=result['consensus_counts']['record'],
        primary_clear_coverage=primary['clear_coverage'], primary_false_accept_groups=primary['false_accept_writer_groups'],
        primary_negative_groups=primary['negative_writer_groups'], primary_false_accept_upper95=primary['false_accept_upper95'],
        remaining_human_tasks=0, no_automatic_new_human_batch=True, GPU_hours=0, training=False,
        scientific_acceptance=False, analysis_wall_seconds=time.monotonic()-started))
    print(json.dumps(dict(agreement=agreement, gates=gates), ensure_ascii=False))


if __name__=='__main__':
    summarize()
