"""Freeze a twelve-card AI-visible diagnostic review; never create human gold."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import random

AI_RUN = Path('data/research/runs/p0_ai_prereview_2026-10-28')
RUN = Path('data/research/runs/p0_quick_review_2026-10-28')
SEED = 2026102803
REACTIONS = ['agree', 'disagree', 'uncertain']
SLOTS = [('2-5', 'correct'), ('2-5', 'incorrect'), ('6-8', 'incorrect'),
         ('6-8', 'unknown'), ('9-12', 'correct'), ('13-20', 'incorrect')]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def proposal(task):
    ai = task['ai_suggestion']
    if task['type'] == 'normative':
        return ('AI在当前图示可辨范围内，未发现笔画身份及累计次序差异。完整方向、异写范围仍待核验。'
                if ai['facets']['order'] == 'pass' else
                '图示中的密集部件不足以确认笔画身份或次序，AI建议保留未知。完整方向、异写范围仍待核验。')
    reasons = {'wrong_order': '先后错误', 'reverse_direction': '方向错误', 'missing': '缺笔或未完成',
               'extra': '额外墨迹', 'concurrent': '同步或提前增长', 'disappeared': '墨迹消失', 'blank': '空白'}
    if ai['decision'] == 'correct':
        return 'AI程序未发现过程违规；这条意见仍依赖尚未核准的源字形，需对照实际视频。'
    if ai['decision'] == 'incorrect':
        flags = '、'.join(reasons[r] for r in ai['reasons'] if r in reasons)
        return 'AI怀疑存在'+(flags or '过程问题')+'，请查看实际视频后判断是否同意。'
    return 'AI不能确认完整过程是否正确，建议保留未知；看不出明确结论时可直接选“看不清”。'


def card(norm, rgb, position, selection):
    norm, rgb = deepcopy(norm), deepcopy(rgb)
    for task in [norm, rgb]:
        task['batch'] = 'quick_cards'
        task['review_proposal'] = proposal(task)
    ai = rgb['ai_suggestion']
    # Navigation hints only, derived from already saved AI evidence.
    # They do not replace the video or create an event annotation.
    hints = sorted({int(e[k]) for e in ai['events']
                    if e.get('direction') in ['unknown', 'reverse']
                    for k in ['onset_frame', 'complete_frame'] if e.get(k) is not None})
    return dict(blind_id=f'Q-{position:02d}', type='quick_card', batch='quick_cards',
                character=norm['character'], normative=norm, rgb=rgb,
                selection=selection, frame_hints=hints[:6])


def draft():
    if (RUN/'quick_review_freeze.json').exists():
        raise ValueError('已冻结；保留当前版本，修订须使用新版本')
    old = json.loads((AI_RUN/'assisted_review_pack.json').read_text())
    norms = {t['character']: t for t in old['batches']['assisted_norm']}
    rgb = old['batches']['assisted_rgb']
    differences = json.loads((AI_RUN/'comparison_to_frozen_observer.json').read_text())['differences']
    by_id = {t['original_id']: t for t in rgb}
    used = {d['character'] for d in differences} | set('犬仓穴刁己冯')
    rng = random.Random(SEED)
    selected = []
    selection_pools = []
    for stratum, decision in SLOTS:
        candidates = [t for t in rgb if t['stratum'] == stratum and
                      t['ai_suggestion']['decision'] == decision and t['character'] not in used]
        characters = sorted({t['character'] for t in candidates})
        chosen = rng.choice(characters)
        clips = sorted((t for t in candidates if t['character'] == chosen), key=lambda t:t['original_id'])
        clip = rng.choice(clips)
        selected.append((clip, dict(kind='stratified_random', stratum=stratum, AI_decision=decision)))
        selection_pools.append(dict(stratum=stratum, AI_decision=decision,
            eligible_characters=len(characters), eligible_clips=len(candidates), selected_character=chosen,
            selected_id=clip['original_id'], selected_character_eligible_clips=len(clips)))
        used.add(chosen)
    diagnostic = sorted((by_id[d['sample_id']] for d in differences),
                        key=lambda t:(len(norms[t['character']]['candidate_strokes']), t['character']))
    selected += [(t, dict(kind='fixed_method_difference', original='correct', AI='unknown')) for t in diagnostic]
    cards = [card(norms[t['character']], t, i, why) for i, (t, why) in enumerate(selected, 1)]
    protocol = dict(id='p0-quick-ai-visible-review-v1', revision='1.0', mode='quick',
        status='draft_operation_test_pending', seed=SEED, character_count=12, RGB_count=12,
        scope='First diagnostic spotcheck only; not full DATA-01/EVAL-01 calibration or P0 acceptance',
        workload='12 paired cards; normative and RGB reactions stored separately; no required detailed forms',
        reactions=REACTIONS, AI_suggestions_visible=True, independent_blind_review=False,
        normative_approval_from_agreement=False, RGB_gold_from_agreement=False,
        semantics={'agree':'Agrees with the displayed bounded AI proposal; unknown remains unknown',
                   'disagree':'Disagrees with displayed AI proposal; no opposite correctness label inferred',
                   'uncertain':'Human cannot determine; no pass or fail inferred'},
        second_reviewer='Only cards with primary ID1 disagreement or uncertainty; own answers, primary answers hidden',
        prior_protocol_preserved=str(AI_RUN/'assisted_protocol.json'),
        prior_full_workload_active=False, scientific_status='DATA-01/EVAL-01 blocked; P0 not accepted',
        base_commit='3ea92d8f', source_pack=str(AI_RUN/'assisted_review_pack.json'),
        evaluator_modified=False, thresholds_modified=False, no_unsampled_human_credit=True)
    pack = dict(protocol=protocol, batches={'quick_cards':cards}, tutorial=[])
    write(RUN/'quick_review_draft.json', pack)
    # Operate the interface only on developer characters before freezing.
    dev = sorted((t for t in rgb if t['role'] == 'observer_dev'), key=lambda t:t['original_id'])
    practice = []
    for decision in ['correct', 'unknown']:
        t = next(t for t in dev if t['ai_suggestion']['decision'] == decision and
                 t['character'] not in {c['character'] for c in practice})
        practice.append(card(norms[t['character']], t, len(practice)+1, dict(kind='non_holdout_UI_test')))
    test_protocol = dict(protocol, id='p0-quick-operation-test-v1', status='operation_test_only',
                         character_count=2, RGB_count=2)
    write(RUN/'operation_test_pack.json', dict(protocol=test_protocol, batches={'quick_cards':practice}, tutorial=[]))
    write(RUN/'sampling_audit.json', dict(seed=SEED, fixed_diagnostic_clips=6,
        random_clips=6, random_slots=selection_pools,
        selection='Within each prespecified stroke-count/AI-decision slot: uniform character then uniform eligible clip; without repeated characters',
        excluded_legacy_characters=list('犬仓穴刁己冯'),
        review_order='Six random cards from simple to dense; then six diagnostic cards by stroke count',
        bias='Half targeted, half conditional stratified sample; not a representative accuracy estimate',
        role_counts=dict(Counter(t['role'] for t, _ in selected)),
        stratum_counts=dict(Counter(t['stratum'] for t, _ in selected)),
        original_holdout_used_for_diagnostics=True, original_0_of_64_not_revalidated=True,
        all_human_records_created=0))
    print('Draft: 12 paired cards; operation tests use2 non-holdout characters')


def freeze():
    if (RUN/'quick_review_freeze.json').exists():
        raise ValueError('当前协议已冻结，不覆盖')
    check = json.loads((RUN/'browser_operation_check.json').read_text())
    if not check['passed'] or check['scientific_human_records_created'] != 0:
        raise ValueError('先完成隔离非保留集操作检查')
    pack = json.loads((RUN/'quick_review_draft.json').read_text())
    pack['protocol'].update(status='frozen_waiting_for_actual_human_spotcheck',
                            frozen_at_utc=datetime.now(timezone.utc).isoformat(),
                            operation_check=str(RUN/'browser_operation_check.json'))
    write(RUN/'quick_review_freeze.json', pack)
    write(RUN/'quick_protocol.json', pack['protocol'])
    with (RUN/'selection_manifest.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['position','card_id','character','kind','stratum','role',
            'normative_id','video_id','AI_video_decision'])
        writer.writeheader()
        for i, c in enumerate(pack['batches']['quick_cards'], 1):
            writer.writerow(dict(position=i,card_id=c['blind_id'],character=c['character'],
                kind=c['selection']['kind'],stratum=c['rgb']['stratum'],role=c['rgb']['role'],
                normative_id=c['normative']['original_id'],video_id=c['rgb']['original_id'],
                AI_video_decision=c['rgb']['ai_suggestion']['decision']))
    print('Frozen12-character/12-video diagnostic batch; scientific acceptance unchanged')


def validate_feedback(entry, task, protocol_id):
    if entry.get('protocol_id') != protocol_id or entry.get('type') != 'quick_card':
        raise ValueError('记录与小批次协议不匹配')
    for key in ['normative_feedback', 'rgb_feedback']:
        if entry.get(key, {}).get('reaction') not in REACTIONS:
            raise ValueError('规范与视频分别选择同意、不同意或看不清')
    if 'decision' in entry or 'facets' in entry:
        raise ValueError('小批次只记录对AI意见的反馈，不自动生成完整规范或RGB真值')
    return entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['draft', 'freeze'])
    {'draft':draft, 'freeze':freeze}[parser.parse_args().action]()
