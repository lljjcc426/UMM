"""Audit existing P0 artifacts and prepare a versioned human review protocol.

No renderer, observer scoring, model execution or media generation is invoked.
The freeze step requires a successful non-holdout browser operation test.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import random
import subprocess
import uuid

from scripts.p0.build_data import DATA, ROLES

RUN = Path('data/research/runs/p0_human_review_preparation_2026-10-28')
REVIEW = DATA / 'review_v2'
SEED = 2026102801
STRATA = ['2-5', '6-8', '9-12', '13-20']
STATUS_VALUES = ['pass', 'fail', 'unknown', 'not_applicable']
FACETS = {
    'normative': {
        'character_identity': '规范字符与地区对应', 'stroke_count': '笔画数与拆并笔',
        'stroke_identity': '候选笔画与规范空间身份对应', 'order': '逐笔次序',
        'direction': '笔内方向与折笔', 'variant_scope': '所依据规范及异写适用范围'},
    'rgb_event': {
        'visible_content': '可见内容与最终完整性', 'stroke_identity_count': '实例身份与笔画数',
        'order': '实际可见先后', 'direction': '实际笔内方向',
        'completion_sequence': '前笔完成后再开始后笔',
        'simultaneous_growth': '可见增长是否逐笔分开', 'ink_preservation': '旧墨迹是否保持'},
}
REASONS = {
    'wrong_order': '先后错误', 'reverse_direction': '方向错误', 'missing': '缺笔/未完成',
    'extra': '多笔/额外墨迹', 'concurrent': '同步或提前增长', 'disappeared': '墨迹消失',
    'blank': '空白/无内容', 'temporal_ambiguity': '时间采样不足或同帧跳变',
    'geometry_ambiguity': '空间身份不明', 'norm_conflict': '规范或异写冲突', 'other': '其他',
}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def load_existing():
    templates = json.loads((DATA / 'templates.json').read_text())['templates']
    samples = []
    for role, _ in ROLES:
        samples.extend(json.loads(line) for line in (DATA / f'manifest_{role}.jsonl').read_text().splitlines())
    return templates, samples


def audit():
    templates, samples = load_existing()
    by_template = {t['template_id']: t for t in templates}
    by_id = {s['sample_id']: s for s in samples}
    imported = json.loads((RUN / 'raw_user_export_2026-10-28.json').read_text())
    normalized, coverage, disputes = [], defaultdict(lambda: dict(normative=[], rgb=[])), []
    for entry in imported['annotations']:
        if entry['type'] == 'normative':
            template = by_template[entry['sample_id'].removeprefix('norm-')]
            sample = None
            coverage[template['character']]['normative'].append(entry['sample_id'])
        else:
            sample = by_id[entry['sample_id']]
            template = by_template[sample['template_id']]
            coverage[template['character']]['rgb'].append(entry['sample_id'])
        if entry['source_group_id'] != template['source_group_id']:
            raise ValueError('Export source group mismatch: ' + entry['sample_id'])
        item = dict(original=entry, character=template['character'], role=template['role'],
                    origin='user_export_v1_pre_protocol', formal_eligible=False,
                    formal_exclusion_reason='Pre-freeze exploratory labels without facet-level rubric or confirmed blinding',
                    explicit_fields_present=[k for k, value in entry.items() if value not in ['', None]],
                    unrecorded_fields=list(FACETS[entry['type']]), reference_consulted='not_recorded',
                    independence='single_reviewer_id_1_not_adjudicated')
        normalized.append(item)
        if sample and entry['decision'] != sample['evaluation_only']['expected']:
            disputes.append(dict(sample_id=entry['sample_id'], character=template['character'],
                construction_case=sample['evaluation_only']['construction_case'],
                original_human_decision=entry['decision'], synthetic_expected=sample['evaluation_only']['expected'],
                human_notes=entry['notes'], status='unresolved_semantic_scope_no_automatic_relabel',
                issue='Whole-process invalidity and unobservable stroke order are separate judgments'))
    char_coverage = []
    for char, seen in coverage.items():
        available = [s for s in samples if s['character'] == char and s['role'] == 'observer_dev']
        missing = [dict(sample_id=s['sample_id'], construction_case=s['evaluation_only']['construction_case'])
                   for s in available if s['sample_id'] not in seen['rgb']]
        char_coverage.append(dict(character=char, normative_global_records=len(seen['normative']),
            rgb_global_records=len(seen['rgb']), rgb_cases_missing=missing,
            all_facet_and_frame_labels_explicit=False, official_reference_use_confirmed=False,
            user_named_three=char in '犬仓穴', extra_character_confirmation_pending=char not in '犬仓穴'))
    save(RUN / 'legacy_annotation_audit.json', dict(raw_records=len(normalized),
        normalized_records=normalized, character_coverage=char_coverage, disagreements=disputes,
        formal_normative_count=0, formal_RGB_count=0,
        answer_exposure=dict(explicit_UI_scores_or_case_labels=False,
            deterministic_case_order=True, repeated_11_case_cycle=True,
            accessible_repository_predictions_via_old_root_server=True,
            actual_human_access_to_external_answers='unknown_no_access_trace',
            reference_examples_or_rubric_before_annotation=False,
            conclusion='Do not assert confirmed blind or formal accuracy; preserve original exploratory records')))
    save(DATA / 'human_annotations.json', dict(schema='p0-human-records-v2',
        status='legacy_user_records_preserved_formal_protocol_pending',
        original_export=str(RUN / 'raw_user_export_2026-10-28.json'),
        annotations=imported['annotations'], legacy_records=len(normalized),
        human_global_normative_records=sum(e['type'] == 'normative' for e in imported['annotations']),
        human_global_RGB_records=sum(e['type'] == 'rgb_event' for e in imported['annotations']),
        formal_human_verified_normative_characters=0, formal_human_verified_rgb_clips=0,
        facet_labels_inferred=False, record_audit=str(RUN / 'legacy_annotation_audit.json')))
    rows = []
    for template in templates:
        media = [s for s in samples if s['template_id'] == template['template_id']]
        rows.append(dict(character=template['character'], ucs=f'{ord(template["character"]):05X}',
            role=template['role'], stroke_count=len(template['strokes']), stratum=template['stroke_count_stratum'],
            source_group_id=template['source_group_id'], source_revision=template['source_revision'],
            source_family=template['source_font_family'], normative_index=template['norm_reference']['index'],
            normative_pdf_page=template['norm_reference']['pdf_page'], video_count=len(media),
            renderers=';'.join(sorted({s['renderer_id'] for s in media})),
            quantity_delta='additional_observer_holdout_64' if template['role'] == 'observer_holdout' else 'current_576_projection_only',
            human_normative_pending_items='character,count,identity,order,direction,variant_scope'))
    with (RUN / 'character_inventory.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    save(RUN / 'character_inventory.json', rows)
    role_stats = []
    for role, _ in ROLES:
        media = [s for s in samples if s['role'] == role]
        role_templates = [t for t in templates if t['role'] == role]
        role_stats.append(dict(role=role, characters=len(role_templates), videos=len(media),
            strata=dict(Counter(t['stroke_count_stratum'] for t in role_templates)),
            cases=dict(Counter(s['evaluation_only']['construction_case'] for s in media)),
            renderers=dict(Counter(s['renderer_id'] for s in media)),
            decoded_frames=sum(s['frame_count'] for s in media),
            duration_seconds=sum(sum(s['frame_durations']) for s in media),
            source_groups=len({s['source_group_id'] for s in media})))
    groups = defaultdict(set)
    for t in templates: groups[t['source_group_id']].add(t['role'])
    save(RUN / 'population_audit.json', dict(original_quantity_plan=576, actual_characters=640,
        delta=64, delta_role='observer_holdout', original_frozen_576_character_list_exists=False,
        historical_evidence_commit='6dc1bb23',
        reconciliation='Initial config specified quantities only. Excluding current observer_holdout yields a 576-character projection, not a recovered historical character list. The inserted allocation may change later role membership under the same shuffle.',
        prior_execution_record_disclosed_128_observer_characters=True,
        original_user_question_named_64_observer_characters=True,
        exact_expansion_approval_not_proven_by_quantity_answer_alone=True,
        acceptance_of_640_requires_explicit_final_scope_confirmation=True,
        roles=role_stats, total_videos=len(samples),
        cross_role_source_overlap=[g for g, roles in groups.items() if len(roles) > 1],
        independent_font_families_confirmed=0, independent_writers=0,
        source_root='Make Me a Hanzi graphics / Arphic font lineage',
        renderer_independence='Outline and centerline share source geometry, progress projection and Pillow backend'))
    tree = ast.parse(Path('scripts/p0/observer.py').read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'observe')
    save(RUN / 'observer_independence_audit.json', dict(
        observe_arguments=[a.arg for a in function.args.args],
        event_log_arguments=False, filenames_or_sample_ID_arguments=False,
        construction_labels_joined_after_observation=True,
        raw_RGB_decoding='Pillow RGB conversion; PNG text metadata not passed to observer',
        reference_dependency='Renderer and observer both call stroke_geometry with the same canonical masks and median projection; reference geometry is privileged G1 information',
        independence_levels=dict(event_schedule='separate from actual observer input',
            geometry_algorithm='shared, not independent',source_library='one shared Arphic lineage',
            independent_human_truth='not established', independent_model_output_domain='not tested'),
        zero_over_64=dict(group='one character-source template with all 22 negative/control variants grouped',
            event='any negative video confidently accepted as correct', bound95=1 - .05**(1/64),
            assumptions=['Distinct sampled character groups treated as independent Bernoulli trials',
                         'Same fixed case suite and geometry/renderer limits apply to all groups',
                         'No weighting of correlated variants or individual frames as extra independent trials'],
            limits=['Shared strokes/radicals/font/renderer may correlate group failures',
                    'One source cluster cannot estimate between-source uncertainty',
                    'Finite stratified sample from this source; no general guarantee for real handwriting',
                    'Construction truth and human judgments may differ; original automatic result remains provisional']),
        old_observer_and_thresholds_changed=False, heldout_scoring_rerun=False))
    print('Preserved/imported', len(normalized), 'legacy records; audited', len(templates), 'characters', len(samples), 'videos')


def build_draft():
    templates, samples = load_existing()
    rng = random.Random(SEED)
    # All names and orders are determined before formal human holdout review.
    # Source/case mappings remain in the audit file, never the browser payload.
    tasks = []
    for t in templates:
        tasks.append(dict(original_id='norm-' + t['template_id'], type='normative',
            character=t['character'], role=t['role'], stratum=t['stroke_count_stratum'],
            official_page=t['norm_reference']['pdf_page'], official_index=t['norm_reference']['index'],
            candidate_strokes=t['strokes'], candidate_medians=t['medians']))
    by_char = {t['character']: t for t in templates}
    for s in samples:
        tasks.append(dict(original_id=s['sample_id'], type='rgb_event', character=s['character'],
            role=s['role'], stratum=by_char[s['character']]['stroke_count_stratum'],
            official_page=s['evaluation_only']['norm_reference']['pdf_page'],
            media_path=s['media_path'], frame_timestamps=s['frame_timestamps'],
            renderer=s['renderer_id'], case=s['evaluation_only']['construction_case']))
    practice_chars = ['犬']
    for stratum in STRATA[1:]:
        choices=sorted(t['character'] for t in templates if t['role']=='observer_dev' and t['stroke_count_stratum']==stratum)
        practice_chars.append(rng.choice(choices))
    batches = {}
    selections = {
        'practice_norm': [t for t in tasks if t['type']=='normative' and t['character'] in practice_chars],
        'practice_rgb': [t for t in tasks if t['type']=='rgb_event' and t['character'] in practice_chars and t.get('case') in ['correct','swap','sparse']],
        'holdout_norm': [t for t in tasks if t['type']=='normative' and t['role']=='observer_holdout'],
        'holdout_rgb': [t for t in tasks if t['type']=='rgb_event' and t['role']=='observer_holdout'],
        'development_norm': [t for t in tasks if t['type']=='normative' and t['role']=='observer_dev'],
        'development_rgb': [t for t in tasks if t['type']=='rgb_event' and t['role']=='observer_dev'],
        'main_norm': [t for t in tasks if t['type']=='normative' and t['role'].startswith('model_')],
        'main_rgb': [t for t in tasks if t['type']=='rgb_event' and t['role'].startswith('model_')],
    }
    for name, selected in selections.items():
        bins = [[t.copy() for t in selected if t['stratum']==stratum] for stratum in STRATA]
        for values in bins: rng.shuffle(values)
        ordered = []
        while any(bins):
            positions = list(range(4)); rng.shuffle(positions)
            for position in positions:
                if bins[position]: ordered.append(bins[position].pop())
        for position,t in enumerate(ordered):
            t['blind_id'] = 'R-' + uuid.UUID(int=rng.getrandbits(128)).hex[:16]
            t['batch']=name; t['ordinal']=position+1
        batches[name] = ordered
    tutorial = [t.copy() for t in tasks if t['type']=='rgb_event' and t['character']=='犬']
    for i,t in enumerate(tutorial):
        t.update(blind_id=f'guide-{i+1:02}',batch='tutorial',ordinal=i+1)
    protocol = dict(id='p0-human-review-v2',seed=SEED,status='draft_non_holdout_testing',
        facets=FACETS,status_values=STATUS_VALUES,error_reasons=REASONS,
        batch_order=list(selections),practice_characters=practice_chars,
        tutorial_character='犬',tutorial_clips=11,
        practice_normative=4,practice_RGB=12,
        formal_total_normative=640,formal_total_RGB=2752,
        controlled_observer_only=dict(normative=128,RGB=2112),
        first_priority=dict(normative=64,RGB=1408,character_groups=64),
        reviewer2_recommended=dict(normative=64,RGB=1408,source='same blinded holdout, independent identity and order'),
        legacy_records_formal_count=0,
        no_automatic_gold_from_tutorial=True,reviewer_onboarding_requires_human_action=True,
        preserve_prior_results=True,new_evaluator_requires_new_independent_validation=True)
    save(RUN/'review_draft.json',dict(protocol=protocol,batches=batches,tutorial=tutorial))
    print('Prepared draft: 4 non-holdout practice characters; formal tasks',sum(len(v) for k,v in batches.items() if not k.startswith('practice')))


def freeze():
    check=json.loads((RUN/'ui_operation_test.json').read_text())
    if not check['passed'] or check['holdout_media_requests']:
        raise ValueError('Freeze requires successful non-holdout operation test')
    target=RUN/'review_freeze.json'
    if target.exists(): raise ValueError('Keep existing freeze; create a new version for changes')
    draft=json.loads((RUN/'review_draft.json').read_text())
    draft['protocol'].update(status='frozen_waiting_for_human_onboarding',
        frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        non_holdout_operation_test=str(RUN/'ui_operation_test.json'),
        code_base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
    # One-time source identity at protocol freeze, no repeated hash scans.
    import hashlib
    draft['protocol']['source_identities']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [Path('scripts/p0/review_v2.html'),Path('scripts/p0/review_server.py'),Path(__file__)]}
    save(target,draft)
    with (RUN/'frozen_review_order.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['batch','ordinal','blind_id','original_id','character','type','role','stratum'])
        writer.writeheader()
        for tasks in draft['batches'].values():
            writer.writerows({key:t.get(key) for key in writer.fieldnames} for t in tasks)
    print('Frozen protocol/order after browser checks; formal human reviews remain 0')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['audit','draft','freeze'])
    args=parser.parse_args()
    {'audit':audit,'draft':build_draft,'freeze':freeze}[args.stage]()
