"""Validate actual exported human decisions once, archive, and refresh coverage."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from .data import digest, read_jsonl, training_view, write_json, write_jsonl
from .gold import qualify


def review_rows(dataset, revision):
    rows = read_jsonl(dataset / 'manifest.jsonl')
    if revision == 'S1-independent-review-form-v1':
        return [r for r in rows if r['split'] == 'audit_development'], False
    packages = json.loads((dataset / 's1_completion_2026-11-02/review_batches.json').read_text())
    batch = next(b for b in packages['batches'] if b['package_revision'] == revision)
    return [r for r in rows if r['id'] in batch['sample_ids']], True


def validate_payload(payload, rows, geometry, include_pair=False):
    """Cross-check raw decisions, facet summaries and the frozen reference version."""
    reviewer, raw = payload['reviewer_id'], payload['raw_answers']
    if not reviewer.strip() or payload['independent_of_label_construction'] is not True:
        raise ValueError('A named independent human reviewer is required')
    if raw.get('reviewer_id') != reviewer or raw.get('independent') is not True:
        raise ValueError('Raw reviewer declaration differs from export')
    expected, pending, allowed = {}, [], {'reviewer_id', 'independent'}
    completed, choices = 0, Counter()
    for row in rows:
        sid, item = row['id'], geometry[row['id']]
        sequence = [f'{sid}:sequence']
        identities = sequence + [f'{sid}:identity:{k}' for k in item['stroke_ids']]
        directions = [f'{sid}:direction:{k}' for k in item['stroke_ids']]
        pairs = sorted({f'{sid}:pair:{r["a"]}:{r["b"]}' for r in item['relations']})
        allowed.update(identities + directions + pairs + [f'{sid}:notes'])
        for key in identities + directions + pairs:
            value = raw.get(key, '')
            if value not in ('', 'accepted', 'disputed', 'unknown'):
                raise ValueError(f'Invalid manual choice: {key}')
            if value:
                completed += 1
                choices[value] += 1
        facets = {'E3': identities, 'E4': identities + pairs, 'E5': identities + directions}
        if include_pair:
            facets = {'PAIR': sequence, **facets}
        for facet, keys in facets.items():
            values = [raw.get(k, '') for k in keys]
            if '' in values:
                pending.append({'sample_id': sid, 'facet': facet})
                continue
            verdict = 'disputed' if 'disputed' in values else 'unknown' if 'unknown' in values else 'accepted'
            not_applicable = facet == 'E4' and not pairs
            if not_applicable:
                verdict = 'unknown'
            expected[(sid, facet)] = {'verdict': verdict, 'not_applicable': not_applicable,
                                      'item_decisions': {k: raw[k] for k in keys},
                                      'reviewer_notes': raw.get(f'{sid}:notes', ''),
                                      'gold_revision': item['gold_revision'],
                                      'norm_reference': item['norm_reference'],
                                      'stroke_ids': item['stroke_ids']}
    if set(raw) - allowed:
        raise ValueError('Raw answers include choices outside this review batch')
    actual = {(r['sample_id'], r['facet']): r for r in payload['records']}
    if len(actual) != len(payload['records']) or actual.keys() != expected.keys():
        raise ValueError('Facet records do not match completed raw choices')
    if sorted(payload['pending'], key=lambda r: (r['sample_id'], r['facet'])) != sorted(pending, key=lambda r: (r['sample_id'], r['facet'])):
        raise ValueError('Pending records do not match incomplete raw choices')
    for key, expected_fields in expected.items():
        record = actual[key]
        if any(record.get(k) != v for k, v in expected_fields.items()):
            raise ValueError(f'Raw choices/reference and facet summary differ: {key}')
        if (record.get('reviewer_id') != reviewer or record.get('reviewer_kind') != 'human'
                or record.get('independent_of_label_construction') is not True
                or record.get('annotated_at') != payload['exported_at'] or not record.get('evidence')):
            raise ValueError(f'Facet lacks matching independent provenance: {key}')
    return {'passed': True, 'completed_manual_decisions': completed, 'choices': dict(choices),
            'facet_records': len(actual), 'pending': len(pending)}


def refresh(dataset):
    rows = read_jsonl(dataset / 'manifest.jsonl')
    geometry = {g['id']: g for g in read_jsonl(dataset / 'evaluation_only/geometry.jsonl')}
    reviews = read_jsonl(dataset / 'evaluation_only/reviews.jsonl')
    labels = {r['id']: r for r in read_jsonl(dataset / 'evaluation_only/labels.jsonl')}
    status = json.loads((dataset / 'current_status.json').read_text())
    paired = [r for r in rows if qualify(geometry[r['id']], reviews, 'PAIR') or qualify(geometry[r['id']], reviews, 'E3')]
    pilot = [r for r in paired if r['split'] != 'audit_development']
    smoke = [r for r in paired if r['split'] == 'audit_development']
    coverage = {}
    for metric in ('E3', 'E4', 'E5'):
        counts, by_condition = Counter(), {}
        for req in read_jsonl(dataset / 'requests.jsonl'):
            if req['metric'] != metric:
                continue
            key = ('unqualified_gold' if not qualify(geometry[req['sample_id']], reviews, metric)
                   else 'ambiguous_gold' if metric == 'E4' and labels[req['id']]['answer'] is None
                   else 'scorable')
            counts[key] += 1
            by_condition.setdefault(req['condition'], Counter())[key] += 1
        coverage[metric] = {'requests': sum(counts.values()), **counts,
                            'by_condition': {k: dict(v) for k, v in by_condition.items()}}
    accepted = {m: sum(qualify(g, reviews, m) for g in geometry.values()) for m in ('E3', 'E4', 'E5')}
    completed_facets = {(r['sample_id'], r['facet']) for r in reviews}
    pilot_ids = {r['id'] for r in rows if r['split'] != 'audit_development'}
    pilot_pair_reviewed = sum((sid, 'PAIR') in completed_facets or (sid, 'E3') in completed_facets for sid in pilot_ids)
    pilot_spatial_reviewed = sum(all((sid, f) in completed_facets for f in ('E3', 'E4', 'E5')) for sid in pilot_ids)
    e4_unknown = {r['sample_id'] for r in reviews if r['facet'] == 'E4' and r['verdict'] == 'unknown'
                  and not r.get('not_applicable') and not qualify(geometry[r['sample_id']], reviews, 'E4')}
    e4_na = {r['sample_id'] for r in reviews if r['facet'] == 'E4' and r.get('not_applicable')}
    status.update(independent_reviewers=len({r['reviewer_id'] for r in reviews}), records_received=len(reviews),
                  completed_manual_decisions=len({(r['reviewer_id'], r['gold_revision'], k)
                                                  for r in reviews for k in r['item_decisions']}),
                  reviewed_characters=sum(qualify(g, reviews, 'E3') and qualify(g, reviews, 'E5') for g in geometry.values()),
                  reviewed_strokes=sum(len(g['stroke_ids']) for g in geometry.values()
                                       if qualify(g, reviews, 'E3') and qualify(g, reviews, 'E5')),
                  E3_accepted_characters=accepted['E3'], E4_accepted_characters=accepted['E4'], E5_accepted_characters=accepted['E5'],
                  E4_unknown_characters=len(e4_unknown), E4_not_applicable_characters=len(e4_na),
                  qualified_D_SMOKE_pairs=len(smoke), qualified_D_PILOT=len(pilot),
                  remaining_unreviewed_pilot_candidates=len(pilot_ids) - pilot_pair_reviewed,
                  gold_request_coverage=coverage, model_metrics=None)
    characters = {r['id']: r['character'] for r in rows}
    latest_review = max((r['annotated_at'] for r in reviews), default=None)
    if latest_review:
        status['last_review_exported_at'] = latest_review
        status['date'] = datetime.fromisoformat(latest_review.replace('Z', '+00:00')).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat()
    status['reviewer_notes'] = [{k: r[k] for k in ('sample_id', 'facet', 'verdict', 'reviewer_notes')}
                              | {'character': characters[r['sample_id']]} for r in reviews if r.get('reviewer_notes')]
    status['CPU_deliverables'] = 'complete_with_PRE01_to_PRE07_controls_and_strata'
    status['unknown_policy'] = 'Preserve E4 unknown at whole-character facet scope; single-stroke E4 is not applicable; no partial promotion or threshold adjustment'
    status['S1'] = ('cpu_complete_pilot_independent_review_pending' if pilot_pair_reviewed < len(pilot_ids)
                    else 'pilot_pairs_audited_additional_spatial_review_pending' if pilot_spatial_reviewed < len(pilot_ids)
                    else 'complete_with_documented_gold_limitations')
    status['paired_characters_audited'] = len(paired)
    status['pilot_characters_with_completed_spatial_review'] = pilot_spatial_reviewed
    status['pilot_spatial_review_remaining'] = len(pilot_ids) - pilot_spatial_reviewed
    status['pilot_review_batches'] = 's1_completion_2026-11-02/review_batches.json'
    status['stage_acceptance'] = 's1_completion_2026-11-02/acceptance.json'
    write_json(dataset / 'current_status.json', status)
    write_jsonl(dataset / 'smoke_pairs_reviewed.jsonl', [training_view(r) for r in smoke])
    for part in ('train', 'validation', 'test'):
        write_jsonl(dataset / f'pilot_{part}_pairs_reviewed.jsonl',
                    [training_view(r) for r in pilot if r['split'] == part + '_development'])
    write_json(dataset / 's1_completion_2026-11-02/acceptance.json', {
        'S0': status['S0'], 'S1_CPU_deliverables': 'complete',
        'S1_all_selected_candidate_audits_complete': pilot_pair_reviewed == len(pilot_ids) == pilot_spatial_reviewed,
        'overall': 'complete_with_documented_gold_limitations' if pilot_pair_reviewed == len(pilot_ids) == pilot_spatial_reviewed
                   else 'CPU_complete_independent_pilot_audits_pending',
        'selected_pairs': len(rows), 'qualified_D_SMOKE': len(smoke), 'qualified_D_PILOT': len(pilot),
        'pilot_pair_reviews_remaining': len(pilot_ids) - pilot_pair_reviewed,
        'pilot_spatial_reviews_remaining': len(pilot_ids) - pilot_spatial_reviewed,
        'unknown_and_disputed_policy': 'Completed review is distinct from accepted gold; never force a positive verdict',
        'gold_request_coverage': coverage, 'model_metrics': None,
        'not_required_to_finish_S0_S1': ['S2 model inference', 'S3 FIT', 'S4 D-MAIN and training', 'new independent fonts when unavailable'],
        'checks': 'checks.json', 'review_batches': 'review_batches.json'})
    return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=Path('data/research/paired_strokes_v1'))
    parser.add_argument('--file', type=Path)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if args.file:
        blob = args.file.read_bytes()
        payload = json.loads(blob)
        rows, include_pair = review_rows(args.dataset, payload['package_revision'])
        geometry = {g['id']: g for g in read_jsonl(args.dataset / 'evaluation_only/geometry.jsonl')}
        validation = validate_payload(payload, rows, geometry, include_pair)
        if args.check_only:
            print(json.dumps(validation, ensure_ascii=False, indent=2))
            return
        if args.archive is None:
            parser.error('--archive is required when importing a file')
        old = read_jsonl(args.dataset / 'evaluation_only/reviews.jsonl')
        key = lambda r: (r['sample_id'], r['facet'], r['reviewer_id'], r['annotated_at'])
        previous = {key(r): r for r in old}
        added = []
        for record in payload['records']:
            if key(record) in previous:
                if previous[key(record)] != record:
                    raise ValueError('An archived export cannot be changed in place')
            else:
                added.append(record)
        args.archive.mkdir(parents=True, exist_ok=False)
        (args.archive / args.file.name).write_bytes(blob)
        write_json(args.archive / 'receipt.json', {'source_file': str(args.file), 'original_sha256': digest(blob),
                   'package_revision': payload['package_revision'], 'validation': validation, 'added': len(added)})
        write_jsonl(args.dataset / 'evaluation_only/reviews.jsonl', old + added)
    print(json.dumps(refresh(args.dataset), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
