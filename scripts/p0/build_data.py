"""Prepare the approved P0 source subset, grouped manifest and RGB media."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import random
import re
import shutil
import time
import traceback

import numpy as np
import PIL

from scripts.p0.geometry import render, save_clip, read_clip, stroke_geometry, write_contact

REVISION = 'bddc96d41bef78427ed0e034e9f7e31d71fd1b92'
SEED = 20261027
DATA = Path('data/research/datasets/p0_stroke_synthetic_v1')
RUN = Path('data/research/runs/p0_data_eval_2026-10-27')
PRIVATE = Path('private/p0_data_eval_2026-10-27')
ROLES = [('observer_dev', 64), ('observer_holdout', 64), ('model_train', 320),
         ('model_validation', 64), ('model_character_test', 128)]
CASES = ['correct', 'swap', 'reverse', 'missing', 'extra', 'simultaneous',
         'early_next', 'flash', 'disappear', 'sparse', 'blank']
NOTICE = ('UMM P0 synthetic stroke data, modified 2026-10-27 from Make Me a Hanzi '
          f'graphics@{REVISION}; subset, IDs, synthetic timing and raster rendering added. '
          'Derived glyph geometry/media: Arphic Public License; '
          'copyright (C) 1999 Arphic Technology Co., Ltd.; '
          'retain licenses/ARPHICPL.TXT and source attribution. No warranty.')


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tier(n):
    return '2-5' if n<=5 else '6-8' if n<=8 else '9-12' if n<=12 else '13-20'


def prepare(norm_text):
    started = time.perf_counter()
    graphics = PRIVATE/'sources/graphics.txt'
    rows = [json.loads(line) for line in graphics.read_text().splitlines()]
    # A factual codepoint/index/page map; no full normative images redistributed.
    norm = {}
    for page, text in enumerate(norm_text.read_text().split('\f'), 1):
        for sequence, ucs in re.findall(r'\b(\d{4})\s+([0-9A-F]{5})\b', text):
            norm[chr(int(ucs, 16))] = dict(index=int(sequence), ucs=ucs, pdf_page=page)
    if len(norm) != 8105:
        raise ValueError(f'Official index extraction yielded {len(norm)}, expected 8105')
    excluded, eligible = [], []
    for row in rows:
        reason = None
        char = row['character']
        count = len(row['strokes'])
        if char not in norm:
            reason = 'outside_GF0023_character_scope'
        elif norm[char]['index'] > 3500:
            reason = 'outside_first_level_3500_scope_for_this_pilot'
        elif not 2<=count<=20:
            reason = 'outside_predeclared_2_to_20_stroke_range'
        elif count != len(row['medians']) or any(len(m)<2 for m in row['medians']):
            reason = 'invalid_geometry_alignment'
        if reason:
            excluded.append(dict(character=char, reason=reason))
        else:
            eligible.append(row)
    strata = defaultdict(list)
    for row in eligible:
        strata[tier(len(row['strokes']))].append(row)
    rng = random.Random(SEED)
    for name in sorted(strata):
        strata[name].sort(key=lambda x: ord(x['character']))
        rng.shuffle(strata[name])
    selected = []
    # Every role receives the same four stroke-count strata, without replacements.
    for role, count in ROLES:
        for name in ['2-5', '6-8', '9-12', '13-20']:
            chosen = strata[name][:count//4]
            if len(chosen) != count//4:
                raise ValueError(f'Insufficient source coverage in {name}')
            del strata[name][:count//4]
            for row in chosen:
                char = row['character']
                selected.append(dict(character=char, template_id=f'mmh-{ord(char):05X}',
                                     source_group_id=f'mmh:{REVISION}:{ord(char):05X}',
                                     role=role, source_revision=REVISION,
                                     norm_reference={'standard':'GF0023-2020', **norm[char]},
                                     norm_review_status='pending_human_per_stroke_comparison',
                                     allowed_orders_candidate=[list(range(len(row['strokes'])))],
                                     stroke_count_stratum=name, strokes=row['strokes'], medians=row['medians'],
                                     source_font_family='Arphic_source_per_glyph_family_unspecified',
                                     license='Arphic Public License'))
    save(DATA/'templates.json', dict(modification_notice=NOTICE, license_file='licenses/ARPHICPL.TXT',
                                    source_uri=f'https://github.com/skishore/makemeahanzi/tree/{REVISION}',
                                    geometry_count=len(selected), templates=selected))
    for name in ['COPYING', 'ARPHICPL.TXT']:
        shutil.copyfile(PRIVATE/'sources'/name, DATA/'licenses'/name)
    save(RUN/'source_audit.json', dict(
        graphics_revision=REVISION, source_bytes=graphics.stat().st_size, source_sha256=sha(graphics),
        full_graphics_rows=len(rows), unique_source_characters=len({r['character'] for r in rows}),
        official_index_count=len(norm), official_index_scope='Membership/index/page only; not manual stroke-order agreement',
        source_publication=f'https://github.com/skishore/makemeahanzi/blob/{REVISION}/COPYING',
        standard_uri='https://www.moe.gov.cn/jyb_sjzl/ziliao/A19/202103/W020210318300204215237.pdf',
        standard_local_reference=str(norm_text), eligible_characters=len(eligible),
        selected_characters=len(selected), seed=SEED, role_counts=dict(Counter(t['role'] for t in selected)),
        excluded_count=len(excluded), excluded_reason_counts=dict(Counter(x['reason'] for x in excluded)),
        excluded_rows=excluded, per_stroke_human_verified=0,
        permissions=dict(graphics='APL permits redistribution/modification with retained terms/notices',
                         dictionary='Not downloaded or incorporated; its LGPL scope remains separate',
                         normative_pdf='Reference-only local cache; not redistributed'),
        environment=dict(python=platform.python_version(), numpy=np.__version__, pillow=PIL.__version__,
                         platform=platform.platform(), gpu_used=False),
        wall_seconds=time.perf_counter()-started))
    print('Prepared', len(selected), 'characters', flush=True)


def make_media(role):
    started = time.perf_counter()
    templates = json.loads((DATA/'templates.json').read_text())['templates']
    target = [t for t in templates if t['role']==role]
    output = PRIVATE/'media'/role
    output.mkdir(parents=True, exist_ok=False)
    records, failures, roundtrip = [], [], []
    preview = []
    for ti, template in enumerate(target):
        renderers = ['outline'] if role in ['observer_dev','model_train','model_validation'] else ['outline','centerline']
        cases = CASES if role.startswith('observer_') else ['correct']
        for renderer in renderers:
            masks, _ = stroke_geometry(template, renderer)
            exclusive_pixels = [int(m.sum()) for m in masks & (masks.sum(axis=0)==1)]
            for case in cases:
                identity = f'{SEED}:{template["template_id"]}:{renderer}:{case}'
                sample_id = hashlib.sha256(identity.encode()).hexdigest()[:20]
                path = output/f'{sample_id}.png'
                try:
                    frames, events = render(template, renderer, case)
                    save_clip(path, frames, dict(modification_notice=NOTICE, license='Arphic Public License',
                                                source_revision=REVISION, timing_origin='synthetic',
                                                sample_id=sample_id))
                    decoded, timestamps, durations = read_clip(path)
                    changed = np.r_[True, np.any(frames[1:] != frames[:-1],axis=(1,2,3))]
                    exact_pixels = bool(np.array_equal(decoded, frames[changed]))
                    exact_times = bool(np.allclose(timestamps,np.flatnonzero(changed)*.083,atol=1e-6))
                    roundtrip.append(dict(sample_id=sample_id, all_decoded_RGB_runs_exact=exact_pixels,
                                          decoded_run_timestamps_exact=exact_times, frame_shape=list(decoded.shape)))
                    if not exact_pixels or not exact_times:
                        raise RuntimeError('APNG did not preserve the RGB run sequence and encoded timestamps')
                    for event in events:
                        event.update(start_seconds=event['start_frame']*.083,
                                     end_first_visible_seconds=event['end_frame']*.083)
                    sample = dict(
                        sample_id=sample_id, character=template['character'], template_id=template['template_id'],
                        source_group_id=template['source_group_id'], role=role, source_revision=REVISION,
                        license='Arphic Public License', modification_notice=NOTICE,
                        locale='zh-CN', normative_standard='GF0023-2020',
                        norm_status='source_candidate_pending_human_check', annotation_status='synthetic_construction_only_human_pending',
                        writer_id=None, source_font_family=template['source_font_family'],
                        renderer_id=renderer, synthetic_style_family='outline_fill' if renderer=='outline' else 'constant_width_centerline',
                        synthetic_style_is_independent_font=False, timing_origin='synthetic_arc_progress', pressure_origin='not_available',
                        source_native_fps=None, render_nominal_fps=12, encoded_base_frame_seconds=.083,
                        codec='lossless_RGB_APNG_variable_duration', resolution=[128,128],
                        frame_count=len(decoded), frame_timestamps=timestamps.tolist(), frame_durations=durations,
                        media_path=str(path), media_sha256=sha(path),
                        model_inputs={'character':template['character'], 'instruction':'按规范笔顺逐笔书写这个汉字。'},
                        training_targets={'rgb_path':str(path), 'eligible_for_normative_generation':case=='correct',
                                          'release_ready':False},
                        evaluation_only={'construction_case':case, 'construction_events':events,
                                         'construction_event_frame_grid':'Original nominal 12fps before APNG duplicate-frame coalescing',
                                         'expected':'correct' if case=='correct' else 'unknown' if case in ['flash','sparse'] else 'incorrect',
                                         'clear_constructed_case':case not in ['flash','sparse'],
                                         'pair_group_id':template['source_group_id']+':'+renderer,
                                         'exclusive_pixels':exclusive_pixels, 'norm_reference':template['norm_reference'],
                                         'contact_state':None, 'human_annotator':None})
                    records.append(sample)
                    if ti==0 and renderer=='outline' and case in ['correct','swap','reverse','simultaneous','flash','disappear']:
                        preview.append((case, decoded))
                except Exception:
                    failures.append(dict(sample_id=sample_id, character=template['character'], renderer=renderer,
                                         case=case, traceback=traceback.format_exc()))
        if (ti+1)%8==0:
            print(role, ti+1, '/', len(target), 'clips', len(records), 'failures', len(failures), flush=True)
    manifest = DATA/f'manifest_{role}.jsonl'
    manifest.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    save(RUN/f'media_{role}.json', dict(role=role, groups=len(target), successful_clips=len(records),
                                     expected_clips=sum((1 if role in ['observer_dev','model_train','model_validation'] else 2)*
                                                        (len(CASES) if role.startswith('observer_') else 1) for _ in target),
                                     failures=failures, roundtrip_checks=roundtrip,
                                     media_bytes=sum(Path(r['media_path']).stat().st_size for r in records),
                                     wall_seconds=time.perf_counter()-started,
                                     completed_at_utc=datetime.now(timezone.utc).isoformat()))
    if preview:
        write_contact(RUN/f'{role}_contact.png', preview)
    if failures:
        raise RuntimeError(f'{len(failures)} media constructions failed; see original records')


def audit():
    templates = json.loads((DATA/'templates.json').read_text())['templates']
    samples = []
    for role, _ in ROLES:
        samples += [json.loads(line) for line in (DATA/f'manifest_{role}.jsonl').read_text().splitlines()]
    groups = defaultdict(set)
    characters = defaultdict(set)
    failures = []
    for sample in samples:
        groups[sample['source_group_id']].add(sample['role'])
        characters[sample['character']].add(sample['role'])
        if not all(b>a for a,b in zip(sample['frame_timestamps'],sample['frame_timestamps'][1:])):
            failures.append(dict(sample_id=sample['sample_id'], error='nonmonotonic_timestamps'))
        if set(sample['model_inputs']) != {'character','instruction'}:
            failures.append(dict(sample_id=sample['sample_id'], error='unexpected_model_input_field'))
    group_overlap = {k:list(v) for k,v in groups.items() if len(v)>1}
    character_overlap = {k:list(v) for k,v in characters.items() if len(v)>1}
    pair_checks = []
    for role in ['observer_dev','observer_holdout']:
        pairs = defaultdict(dict)
        for sample in samples:
            if sample['role']==role:
                pairs[sample['evaluation_only']['pair_group_id']][sample['evaluation_only']['construction_case']] = sample
        for group, cases in pairs.items():
            finals = [read_clip(Path(cases[k]['media_path']))[0][-1] for k in ['correct','swap','reverse']]
            ok = all(np.array_equal(finals[0], x) for x in finals[1:])
            pair_checks.append(dict(group_id=group, same_final_pixels=ok))
    result = dict(source_groups=len(groups), characters=len(characters), manifest_samples=len(samples),
                  source_group_overlap=group_overlap, character_overlap=character_overlap,
                  failures=failures, matched_final_pairs=pair_checks,
                  role_counts=dict(Counter(s['role'] for s in samples)),
                  normative_human_verified=0, rgb_event_human_verified=0,
                  source_geometry_review_pending=True,
                  crossed_matrix=[
                      {'content':'unseen_character','synthetic_renderer':'seen_outline','status':'available','groups':128},
                      {'content':'unseen_character','synthetic_renderer':'unseen_centerline','status':'available_synthetic_domain_only','groups':128},
                      {'content':'seen_character','independent_font_or_writer':'unseen','status':'unavailable_needs_independent_source','groups':0},
                      {'content':'unseen_character','independent_font_or_writer':'unseen','status':'unavailable_needs_independent_source','groups':0},
                      {'content':'seen_character','independent_record':'heldout_ID','status':'unavailable_single_source_template_per_character','groups':0}],
                  release_ready=False,
                  scientific_blockers=['No independent human normative/event verification',
                                       'No independently sourced same-character font/writer/record holdout'],
                  passed_engineering=not group_overlap and not character_overlap and not failures
                                     and all(x['same_final_pixels'] for x in pair_checks))
    save(RUN/'data_audit.json', result)
    save(DATA/'splits.json', dict(seed=SEED, unit='immutable source glyph; all counterfactual/render variants stay together',
                                 roles={role:[t['character'] for t in templates if t['role']==role] for role,_ in ROLES},
                                 crossed_matrix=result['crossed_matrix']))
    print('Data audit:', result['passed_engineering'], 'samples:', len(samples), flush=True)
    if not result['passed_engineering']:
        raise RuntimeError('Data engineering audit failed')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare','media','audit'])
    parser.add_argument('--role', choices=[r for r,_ in ROLES])
    parser.add_argument('--norm-text', type=Path)
    args=parser.parse_args()
    if args.stage=='prepare':
        prepare(args.norm_text)
    elif args.stage=='media':
        make_media(args.role)
    else:
        audit()
