"""Approved D1-D4 CPU development on exposed material; never a holdout evaluator."""
from collections import Counter
from dataclasses import asdict, replace
from datetime import datetime, timezone
import argparse
import copy
import inspect
import json
from pathlib import Path
import platform
import random
import shutil
import subprocess
import time

import numpy as np

from scripts.p0.ai_prereview import read_rgb
from scripts.p0.final_calibration import reference_geometry, render_trajectory, save_animation
from scripts.p0.judgments import (DeclaredPlan, judge_execution, judge_normative,
                                 judge_plan_normativity, normative_plan)
from scripts.p0.normative_reference import (BindingItem, GeometryBinding, NormSpec, qualify_reference)
from scripts.p0.observer import observe, one_sided_upper
from scripts.p0.rgb_observation import GeometryInstance, observe_rgb

SOURCE = Path('data/research/runs/p0_final_calibration_2026-10-28')
HUMAN = Path('data/research/runs/p0_human_acceptance_2026-10-29')
RUN = Path('data/research/runs/p0_decoupled_d1_d4_2026-10-29')
PRIVATE = Path('private/p0_decoupled_d1_d4_2026-10-29')
SOURCE_PRIVATE = Path('private/p0_final_calibration_2026-10-28')
POSITIVE_IDS = ['N017', 'N019', 'N030', 'N039', 'N043', 'N066', 'N076', 'N079']
SELECTED = POSITIVE_IDS + ['N022', 'N024', 'N045', 'N046', 'N034', 'N037', 'N049', 'N070']
# These are an explicit AI comparison of the displayed official rows and each
# individual source stroke, not an inference from the global human pass fields.
# Canonical positions below refer to the cited official exemplar, never the
# order in which an RGB observer sees an instance.
AUDITS = {
    'N017': ('竖 横 竖 横折 横 点 点 点 点', [1,2,3,4,5,6,7,8,9], 'BAAAAAAAA', '上占的竖横及口三画，下面四点逐一对应；上竖由上向下。'),
    'N019': ('横折 竖 横 横', [1,2,3,4], 'ABAA', '首画上横转下折，次画中竖，内横与底横依次对应。'),
    'N030': ('点 横 撇', [1,2,3], 'AAB', '上点、上横、左下长撇分别对应；长撇从右上走向左下。'),
    'N039': ('竖提 点 撇 点', [1,2,3,4], 'AABA', '左竖提、左内点、中长撇、右捺点；长撇先右上后左下。'),
    'N043': ('撇 横 横折弯钩', [1,2,3], 'BAA', '左上短撇、上横、下部折弯钩；比较可见主干方向，不认证回锋物理运动。'),
    'N066': ('横折钩 撇 点', [1,2,3], 'ABB', '外横折钩、内撇和刃点三实例；内撇与点均先上后下。'),
    'N076': ('横 竖 横', [1,2,3], 'AAA', '上长横、中竖、下短横；两横从左至右，中竖从上至下。'),
    'N079': ('竖钩 撇 点', [1,2,3], 'BAA', '中竖钩、左短撇、右点；竖钩主干上到下，左笔上到下，右点左上到右下。'),
    'N022': ('撇 捺 横 点 点 撇 横 竖 竖钩', [1,2,3,4,5,7,6,8,9], 'BAAABABBB', '源6为佥底横，应为规范7；源7为右侧短撇，应为规范6；右刂两竖身份另核。'),
    'N024': ('横折钩 撇 点 点 卧钩 点 点', [1,2,3,4,5,7,6], 'ABBBABA', '源6是心右点（规范7），源7是心上点（规范6），末两实例的规范身份交换。'),
    'N045': ('横 竖 横折 横 竖 竖 横 竖 横折 横 横', [1,2,3,4,7,5,6,8,9,10,11], 'ABAAABBBAAA', '源5为上部底横（规范7），源6/7为内部两竖（规范5/6），下日四画独立对应。'),
    'N046': ('竖 竖折 竖 横 撇 点 竖折', [2,1,3,4,7,5,6], 'ABBAABA', '山部源1竖折为规范2、源2竖为规范1；区部源5封框竖折为规范7，源6/7为规范5/6。'),
    'N049': ('横 竖 撇 点 点 点 横钩 撇 点 撇 横 竖 横 横', list(range(1,15)), 'ABBABAABABABAA', '木四画、穴五画、乍五画分别对应；首画横、次画竖，独立于旧视频按钮。'),
    'N034': ('撇 竖 横 横', [1,2,3,4], 'BAAA', '源3呈短斜点，不能核准为规范上横；保留身份对应未知。'),
    'N037': ('竖 竖 横撇 捺 竖 横折 撇 点', list(range(1,9)), 'ABBAAABA', '源1/3/5有折返与连接歧义，不能核准逐笔身份及可见方向。'),
    'N070': ('横 竖', [1,2], 'AA', '源1横在交叉处有明显回折保留意见；不把两份整体通过升为完整几何资格。'),
}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def load_inputs():
    pack = json.loads((SOURCE_PRIVATE/'pack_frozen.json').read_text())
    tasks = {t['id']: t for t in pack['tasks']}
    predictions = {p['id']: p for p in map(json.loads, (SOURCE/'predictions.jsonl').read_text().splitlines())}
    cfg = json.loads(Path('data/research/runs/p0_data_eval_2026-10-27/threshold_freeze.json').read_text())['thresholds']
    return tasks, predictions, cfg


def geometry_for(task):
    masks, progress = reference_geometry([np.asarray(s) for s in task['strokes']])
    exclusive = masks & (masks.sum(0) == 1)
    # Deterministic opaque IDs; their spelling and container order carry no rank.
    rng = random.Random(2026102903 + int(task['id'][1:]))
    ids = ['g_' + format(rng.getrandbits(48), '012x') for _ in masks]
    geometry, source_axes = [], {}
    for key, mask, region, position in zip(ids, masks, exclusive, progress):
        lo, hi = np.quantile(position[region], [.22, .78])
        pair = [region & (position <= lo), region & (position >= hi)]
        centers = [(float(np.nonzero(a)[1].mean()), float(np.nonzero(a)[0].mean())) for a in pair]
        order = sorted(range(2), key=lambda k: centers[k])
        names = {old: ['A', 'B'][j] for j, old in enumerate(order)}
        geometry.append(GeometryInstance(key, mask, {names[i]: pair[i] for i in range(2)}))
        source_axes[key] = (names[0], names[1])  # Compatibility/source-plan fact only.
    return geometry, source_axes, masks, progress


def build_static_audit(tasks):
    result = {}
    for nid in SELECTED:
        task = tasks[nid]
        geometry, _, _, _ = geometry_for(task)
        descriptions, mapping, starts, note = AUDITS[nid]
        assert len(descriptions.split()) == len(mapping) == len(starts) == len(geometry)
        rows = []
        for j, (g, canonical, start) in enumerate(zip(geometry, mapping, starts), 1):
            ambiguous = nid in ['N034', 'N037', 'N070']
            rows.append(dict(instance_id=g.instance_id, source_stroke_number=j,
                canonical_id=f's{canonical:02}', start_anchor=start, end_anchor='B' if start=='A' else 'A',
                norm_reference_id='GF0023-2020:'+task['character'], normative_position=canonical,
                normative_stroke_description=descriptions.split()[canonical-1],
                identity_status='unknown' if ambiguous else 'verified',
                direction_status='unknown' if ambiguous else 'verified',
                evidence_id=f'{nid}-static-AI-{j:02}', audit_level='AI_static_development_not_human_gold',
                evidence=f'源单笔{j}与规范笔画{canonical}（{descriptions.split()[canonical-1]}）图形、部件位置和A/B锚点比较。'+note,
                normative_comparison=task['reference_path'],
                scope='instance_identity_and_visible_anchor_direction; not full physical pen path or allowed variants'))
        result[nid] = dict(character=task['character'], official_page=task['official_page'],
            descriptions=descriptions.split(), review_records=rows,
            source_order_is_normative_truth=False, human_global_labels_upgraded=False,
            viewed_static_contact='private/p0_decoupled_d1_d4_2026-10-29/qualification_candidates_'+
                ('01.jpg' if nid in POSITIVE_IDS else '02.jpg' if nid in ['N022','N024','N045','N046'] else '03.jpg'))
    return result


def reference_for(nid, audit):
    row = audit[nid]
    spec = NormSpec('GF0023-2020:' + row['character'], row['character'],
        tuple(f's{i+1:02}' for i in range(len(row['descriptions']))), tuple(row['descriptions']),
        f'GF0023-2020 page {row["official_page"]}; independent official crop and per-instance AI development audit')
    items = tuple(BindingItem(r['instance_id'], r['canonical_id'], r['start_anchor'], r['end_anchor'])
                  for r in row['review_records'])
    return qualify_reference(spec, GeometryBinding('AI-dev-binding:' + nid, items), row['review_records'])


def writer_audit():
    directory = json.loads((SOURCE_PRIVATE/'pot_directory.json').read_text())
    entries = sorted((e for e in directory if e['name'].lower().endswith('.pot')), key=lambda e:e['offset'])
    all_ids = {Path(e['name']).stem for e in entries}
    roster = json.loads((SOURCE/'writer_selection_freeze.json').read_text())
    selected = set(roster['development'] + roster['validation'])
    pilot = set(roster['prior_exposed_writers_excluded'])
    local = {p.stem for p in SOURCE_PRIVATE.glob('*.pot')}
    attempt_sets = {str(p): sorted({r['writer_id'] for r in json.loads(p.read_text())['records']})
                    for p in SOURCE.glob('**/selection_freeze.json')}
    exposed = selected | pilot | local | {w for ws in attempt_sets.values() for w in ws}
    requests = [json.loads(line) for line in (SOURCE_PRIVATE/'range_requests.jsonl').read_text().splitlines()]
    remaining = all_ids - exposed
    accesses = {}
    for i, e in enumerate(entries):
        writer = Path(e['name']).stem
        if writer not in remaining:
            continue
        # Next ZIP member bounds the possible compressed member bytes. Directory
        # metadata alone does not constitute exposure to decoded handwriting.
        end = entries[i+1]['offset']-1 if i+1 < len(entries) else e['offset']+30+len(e['name'])+e['compressed_size']
        hits = [r for r in requests if r['url'].endswith('/Pot1.0Test.zip') and r['start'] <= end and r['end'] >= e['offset']]
        accesses[writer] = dict(archive_member=e['name'], local_POT_present=writer in local,
                               saved_member_range_accesses=len(hits))
    return dict(source_directory=str(SOURCE_PRIVATE/'pot_directory.json'),
        source_freeze=str(SOURCE/'writer_selection_freeze.json'), archive_POT_members=len(entries),
        unique_writer_filename_ids=len(all_ids), selected_writers=len(selected), pilot_writers=len(pilot),
        historical_selection_writer_sets=attempt_sets, all_saved_exposed_writer_ids=sorted(exposed),
        selected_pilot_overlap=sorted(selected & pilot), locally_present_writer_ids=sorted(local),
        remaining_unselected_writer_ids=sorted(remaining), remaining_candidates=accesses,
        max_new_writer_groups_from_this_archive=len(remaining), requested_new_groups=64,
        shortfall_at_least=64-len(remaining), new_source_bytes_downloaded=0, new_writers_parsed=0,
        independent_human_identity_beyond_filename_verified=False,
        cross_archive_writer_identity_or_other_archives_audited=False,
        prior_failures='Same selected80 writers appear in attempt01 and final freezes; local82 includes both pilots. Range log also inspected for remaining member accesses.',
        scope='Directory IDs and saved acquisition evidence; no proof of recruitment independence or new-character availability',
        ready_for_64_new_writer_holdout=False)


def prepare():
    tasks, _, cfg = load_inputs()
    if (RUN/'development_freeze.json').exists():
        return
    PRIVATE.mkdir(parents=True, exist_ok=True)
    save(RUN/'static_qualification_audit.json', build_static_audit(tasks))
    save(RUN/'writer_resource_audit.json', writer_audit())
    save(RUN/'development_freeze.json', dict(frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        approval='User explicitly approved first-stage D1-D4, added same-norm simple gate and writer feasibility audit.',
        selected_record_groups=SELECTED, D1_record_groups=POSITIVE_IDS,
        selection='Eight simpler explicit instance audits, four order-failure records, two uncertain references,榨 and十 challenges. Not four-stratum representative sampling.',
        actual_selected_stroke_counts={nid:len(tasks[nid]['strokes']) for nid in SELECTED},
        thresholds=cfg, threshold_source='Original frozen threshold_freeze.json; complete=.92, no tuning',
        new_video_budget=8, new_videos='One necessary first-two-instance swap for each D1 group; existing source-order counterpart reused',
        regression='All original144 paired media; plus predeclared subsets for qualification/temporal scope; development only',
        reference_audit='AI per-instance static comparison; no independent human per-stroke gold claim',
        primary_development_method='decoupled', methods=['legacy_original','legacy_simple_norm_gate','legacy_events_with_norm','decoupled'],
        human_labels_or_original_predictions_changed=False, new_human_tasks=0, GPU_hours=0,
        downloads_authorized=False, new_holdout_created=False))
    # Generate only the approved eight files once; later code/debug runs reuse them.
    inventory = []
    for nid in POSITIVE_IDS:
        path = PRIVATE/(nid+'-swap.png')
        if not path.exists():
            save_animation(path, render_trajectory([np.asarray(s) for s in tasks[nid]['strokes']], 'swap'))
        frames, timestamps, _ = read_rgb(path)
        inventory.append(dict(id=nid+'-swap', path=str(path), decoded_frames=len(frames),
                              encoded_seconds=float(timestamps[-1]), derivation='first two recorded instances interchanged; verify actual RGB separately',
                              native_RGB=False, physical_timing=False))
    save(RUN/'new_media_inventory.json', dict(new_video_files=len(inventory), items=inventory,
         raw_media_private=True, old_media_modified=False))


def legacy_evidence(prediction, times, geometry, source_axes, cfg):
    """Adapt only old saved events/facts; no fresh pixel observation in this arm."""
    def point(frame):
        return None if frame is None else dict(frame=frame, interval=[float(times[frame-1]) if frame else None, float(times[frame])])
    events = {}
    for g, e in zip(geometry, prediction['events']):
        a,b = source_axes[g.instance_id]
        events[g.instance_id] = dict(exclusive_pixels=e['exclusive_pixels'],
            geometry_observable=e['exclusive_pixels'] >= cfg['minimum_exclusive_pixels'],
            onset=point(e['onset']), complete=point(e['complete']), final_coverage=e['final_coverage'],
            anchors={a:point(e.get('start_region_frame')), b:point(e.get('end_region_frame'))})
    errors = prediction['errors']
    return dict(schema='legacy-events-adapter-v1', events=events, frame_count=len(times),
        timestamps=times.tolist(), completion_fraction=cfg['complete'], temporal_sampling_available=len(times)>=3,
        initial_ink_pixels=int('nonblank_initial_frame' in prediction['unknown_reasons']),
        all_blank=all(e['final_coverage']==0 for e in prediction['events']) and prediction['final_iou']==0 and 'extra_visible_ink' not in errors,
        extra_ink='extra_visible_ink' in errors, ink_disappeared='visible_ink_disappeared' in errors,
        concurrent_growth='observable_concurrent_growth' in errors)


def simple_gate(old, adapted, reference, source_plan):
    if adapted['all_blank']:
        return 'incorrect'
    if reference.status != 'qualified':
        return 'unknown'
    physical = ['extra_visible_ink','visible_ink_disappeared','observable_concurrent_growth']
    if any(error in physical or error.startswith('missing_or_incomplete_stroke:') for error in old['errors']):
        return 'incorrect'
    validity = judge_plan_normativity(source_plan, reference)
    if validity == 'correct':
        return old['decision']
    return 'incorrect' if old['decision']=='correct' else 'unknown'


def metrics(rows, name):
    clear = [r for r in rows if r['human_reference']!='unknown']
    positive = [r for r in clear if r['human_reference']=='correct']
    negative = {r['writer_id'] for r in clear if r['human_reference']=='incorrect'}
    bad = {r['writer_id'] for r in clear if r['human_reference']=='incorrect' and r['decisions'][name]=='correct'}
    return dict(attempts=len(rows), decisions=dict(Counter(r['decisions'][name] for r in rows)),
        human_reference=dict(Counter(r['human_reference'] for r in rows)), clear_reference_count=len(clear),
        clear_coverage=sum(r['decisions'][name]!='unknown' for r in clear)/len(clear) if clear else None,
        positive_count=len(positive), positive_correct_accepts=sum(r['decisions'][name]=='correct' for r in positive),
        positive_acceptance=sum(r['decisions'][name]=='correct' for r in positive)/len(positive) if positive else None,
        negative_writer_groups=len(negative), false_accept_writer_groups=len(bad),
        false_accepts=sum(r['human_reference']=='incorrect' and r['decisions'][name]=='correct' for r in rows),
        conditional_upper95=one_sided_upper(len(bad), len(negative)),
        scope='Exposed development data; reference error and sampling dependence limitations retained; not new validation')


def invariant_trials(frames, times, geometry, reference, plan, cfg):
    base = observe_rgb(frames,times,geometry,cfg)
    variants = []
    # Test storage permutation independently from ID and anchor spelling changes.
    variants.append(('storage_reverse', list(reversed(geometry)), reference, plan, {}, {}))
    ids = {g.instance_id:'renamed_'+str(900-i) for i,g in enumerate(geometry)}
    for name, rename_ids, rename_anchors in [('instance_rename',True,False),('anchor_rename',False,True),('combined',True,True)]:
        new_ids = ids if rename_ids else {}
        anchors = {'A':'right_label','B':'left_label'} if rename_anchors else {}
        gs = [GeometryInstance(new_ids.get(g.instance_id,g.instance_id),g.mask,
                               {anchors.get(k,k):v for k,v in g.anchors.items()}) for g in reversed(geometry)]
        binding = replace(reference.binding,items=tuple(replace(i,instance_id=new_ids.get(i.instance_id,i.instance_id),
            start_anchor=anchors.get(i.start_anchor,i.start_anchor),end_anchor=anchors.get(i.end_anchor,i.end_anchor)) for i in reference.binding.items))
        ref = replace(reference,binding=binding)
        p = replace(plan,order=tuple(new_ids.get(i,i) for i in plan.order),directions={new_ids.get(i,i):tuple(anchors.get(a,a) for a in d) for i,d in plan.directions.items()})
        variants.append((name,gs,ref,p,new_ids,anchors))
    result = []
    for name,gs,ref,p,ids,anchors in variants:
        e = observe_rgb(frames,times,gs,cfg)
        inv_ids={v:k for k,v in ids.items()};inv_a={v:k for k,v in anchors.items()}
        normalized=copy.deepcopy(e)
        normalized['events']={inv_ids.get(i,i):dict(v,anchors={inv_a.get(a,a):t for a,t in v['anchors'].items()}) for i,v in e['events'].items()}
        result.append(dict(transform=name,evidence_equal=normalized==base,
            execution_equal=judge_execution(e,p)['decision']==judge_execution(base,plan)['decision'],
            normative_equal=judge_normative(e,ref)['decision']==judge_normative(base,reference)['decision']))
    return result


def run():
    if not (RUN/'new_media_inventory.json').exists():
        raise ValueError('Run prepare first; no media generation during evaluation')
    start=time.monotonic()
    attempts=sorted(RUN.glob('attempt_*'))
    output=RUN/f'attempt_{len(attempts)+1:02}'
    output.mkdir()
    snapshot=output/'source_snapshot';snapshot.mkdir()
    for name in ['rgb_observation.py','normative_reference.py','judgments.py','evaluate_decoupled.py']:
        shutil.copyfile(Path('scripts/p0')/name,snapshot/name)
    tasks,predictions,cfg=load_inputs()
    audit=json.loads((RUN/'static_qualification_audit.json').read_text())
    references={nid:reference_for(nid,audit) for nid in SELECTED}
    save(output/'qualification_results.json',{nid:asdict(q) for nid,q in references.items()})
    d1=[];d2=[];cache={};actual_witness=[]
    for nid in POSITIVE_IDS:
        geometry,axes,_,_=geometry_for(tasks[nid]);ref=references[nid]
        correct_plan=normative_plan(ref)
        order=list(correct_plan.order);order[0],order[1]=order[1],order[0]
        bad_plan=replace(correct_plan,plan_id='explicit-wrong-plan:'+nid,order=tuple(order))
        for actual in ['correct','incorrect']:
            path=Path(tasks['V'+nid[1:]+'-1']['path']) if actual=='correct' else PRIVATE/(nid+'-swap.png')
            frames,times,_=read_rgb(path);e=observe_rgb(frames,times,geometry,cfg)
            cache[nid,actual]=(frames,times,e)
            for valid,p in [(True,correct_plan),(False,bad_plan)]:
                ex=judge_execution(e,p);no=judge_normative(e,ref)
                expected_ex='match' if (actual=='correct')==valid else 'mismatch'
                d1.append(dict(group=nid,actual_condition=actual,plan_normative=valid,
                    execution=ex,normative=no,expected_execution=expected_ex,expected_normative=actual,
                    passed=ex['decision']==expected_ex and no['decision']==actual,
                    truth_scope='Existing paired global RGB label plus independent per-instance AI static audit; new swap requires actual RGB witness; no new human gold'))
            for result in invariant_trials(frames,times,geometry,ref,correct_plan,cfg):d2.append(dict(group=nid,actual_condition=actual,**result))
            reversed_direction=dict(correct_plan.directions)
            first=correct_plan.order[0]
            reversed_direction[first]=tuple(reversed(reversed_direction[first]))
            direction_plan=replace(correct_plan,plan_id='wrong-direction-plan:'+nid,directions=reversed_direction)
            direction_result=judge_execution(e,direction_plan)
            # The same RGB and reference remain normative irrespective of this
            # intentionally wrong direction request.
            d2.append(dict(group=nid,actual_condition=actual,transform='declared_direction_only',
                evidence_equal=observe_rgb(frames,times,geometry,cfg)==e,
                normative_equal=judge_normative(e,ref)['decision']==actual,
                direction_conflict_detected='opposite_visible_direction:'+first in direction_result['errors'],
                execution_invariance_applicable=False,
                execution_decision=direction_result['decision']))
            # Plan and normative specification changes cannot enter observe_rgb.
            # A reference version change must lose qualification until its own
            # per-instance evidence exists. Do not forge an alternate official norm.
            alternate_spec=replace(ref.spec,reference_id='unreviewed-alternate:'+ref.spec.reference_id)
            alternate_ref=qualify_reference(alternate_spec,ref.binding,audit[nid]['review_records'])
            d2.append(dict(group=nid,actual_condition=actual,transform='normative_spec_only',
                evidence_equal=observe_rgb(frames,times,geometry,cfg)==e,
                execution_equal=judge_execution(observe_rgb(frames,times,geometry,cfg),correct_plan)['decision']==judge_execution(e,correct_plan)['decision'],
                alternate_reference_status=alternate_ref.status,
                normative_change_observed=judge_normative(e,alternate_ref)['decision']!=judge_normative(e,ref)['decision']))
            actual_witness.append(dict(group=nid,condition=actual,path=str(path),
                frame_indices=[int(np.argmin(abs(times-t))) for t in [0,.4,.8,1.2,1.6,2.0,2.4]],
                first_two_instance_hits={key:ev['onset'] for key,ev in e['events'].items() if key in correct_plan.order[:2]}))
    save(output/'D1_four_cells.json',d1);save(output/'D2_invariance.json',d2)
    save(output/'actual_RGB_witness_index.json',actual_witness)
    human=json.loads((HUMAN/'human_calibration_results.json').read_text())
    rows=[]
    for v in human['video_reference']:
        t=tasks[v['id']];nid=t['norm_id'];geometry,axes,_,_=geometry_for(tasks[nid])
        frames,times,_=read_rgb(Path(t['path']))
        source_plan=DeclaredPlan('recorded-source-plan:'+nid,tuple(g.instance_id for g in geometry),axes)
        old=predictions[v['id']]['frozen_observer'];adapted=legacy_evidence(old,times,geometry,axes,cfg)
        if nid in references:
            ref=references[nid]
        else:
            ref=qualify_reference(NormSpec('unreviewed:'+nid,t['character'],(),(),''),GeometryBinding('unreviewed:'+nid,()),[])
        e=observe_rgb(frames,times,geometry,cfg)
        new=judge_normative(e,ref);split=judge_normative(adapted,ref)
        rows.append(dict(id=v['id'],norm_id=nid,writer_id=v['writer_id'],human_reference=v['human_reference'],
            nominal_case=predictions[v['id']]['nominal_case'],reference_status=ref.status,
            audit_level=ref.audit_level,decisions=dict(legacy_original=old['decision'],
                legacy_simple_norm_gate=simple_gate(old,adapted,ref,source_plan),
                legacy_events_with_norm=split['decision'],decoupled=new['decision']),
            execution=judge_execution(e,source_plan),normative=new,split_normative=split,
            pixel_evidence_decision_matches_legacy_readout=new['decision']==split['decision']))
    names=['legacy_original','legacy_simple_norm_gate','legacy_events_with_norm','decoupled']
    scopes={'all144_original_reference':rows,
            'excluding_predeclared_sparse':[r for r in rows if r['nominal_case']!='sparse'],
            'statically_qualified_development':[r for r in rows if r['reference_status']=='qualified'],
            'statically_qualified_observable':[r for r in rows if r['reference_status']=='qualified' and r['nominal_case']!='sparse']}
    save(output/'D3_D4_predictions.json',rows)
    save(output/'D3_D4_metrics.json',{scope:{name:metrics(rs,name) for name in names} for scope,rs in scopes.items()})
    save(output/'failure_cases.json',dict(D1_nonmatching=[r for r in d1 if not r['passed']],
        reference_qualified_but_RGB_unknown=[r for r in rows if r['reference_status']=='qualified' and r['decisions']['decoupled']=='unknown'],
        known_human_reference_discrepancy=[r for r in rows if r['id']=='V049-2'],
        old_false_accepts_on_qualified=[r for r in rows if r['reference_status']=='qualified' and r['human_reference']=='incorrect' and r['decisions']['legacy_original']=='correct'],
        clear_reference_abstentions=[r['id'] for r in rows if r['human_reference']!='unknown' and r['decisions']['decoupled']=='unknown'],
        pixel_method_differences=[r for r in rows if not r['pixel_evidence_decision_matches_legacy_readout']],
        sparse_raw_labels_unchanged=[r for r in rows if r['nominal_case']=='sparse']))
    q=Counter(ref.status for ref in references.values())
    summary=dict(completed_at_utc=datetime.now(timezone.utc).isoformat(),
        D1_conditions=len(d1),D1_conditions_passed=sum(r['passed'] for r in d1),
        D2_trials=len(d2),D2_evidence_invariance=all(r['evidence_equal'] for r in d2),
        D2_execution_invariance=all(r['execution_equal'] for r in d2 if r.get('execution_invariance_applicable',True)),
        D2_execution_invariance_trials=sum(r.get('execution_invariance_applicable',True) for r in d2),
        D2_trial_types=dict(Counter(r['transform'] for r in d2)),
        D2_normative_invariance_to_direction_plan=all(r.get('normative_equal',True) for r in d2),
        D2_direction_plan_conflicts_detected=all(r.get('direction_conflict_detected',True) for r in d2),
        D2_unreviewed_reference_versions_refused=all(r.get('alternate_reference_status','unknown')=='unknown' for r in d2),
        qualification_counts=dict(q),regression_attempts=len(rows),
        new_vs_legacy_event_readout_differences=sum(not r['pixel_evidence_decision_matches_legacy_readout'] for r in rows),
        original_thresholds_modified=False,original_labels_modified=False,development_only=True,
        new_video_files=8,new_human_tasks=0,GPU_hours=0,training_runs=0,
        python=platform.python_version(),platform=platform.platform(),wall_seconds=time.monotonic()-start,
        no_independent_holdout_created=True,scientific_acceptance=False)
    save(output/'information_permissions.json',dict(
        qualify_reference=list(inspect.signature(qualify_reference).parameters),
        observe_rgb=list(inspect.signature(observe_rgb).parameters),
        judge_execution=list(inspect.signature(judge_execution).parameters),
        judge_normative=list(inspect.signature(judge_normative).parameters),
        declared_plan_available_to_normative_judge=False,
        normative_reference_or_declared_plan_available_to_pixel_observer=False,
        RGB_or_plan_available_to_reference_qualification=False))
    save(output/'summary.json',summary)
    print(json.dumps(dict(output=str(output),**summary),ensure_ascii=False))


def direction_probe():
    """Additional four cells on the existing reverse clip; no media generation."""
    target=RUN/'D1_direction_probe.json'
    if target.exists():
        raise ValueError('Preserve the completed direction probe')
    tasks,predictions,cfg=load_inputs()
    audit=json.loads((RUN/'static_qualification_audit.json').read_text())
    nid='N066'  # Only one of the preselected eight with an existing reverse clip.
    assert predictions['V066-2']['nominal_case']=='reverse'
    geometry,_,_,_=geometry_for(tasks[nid]);ref=reference_for(nid,audit)
    correct=normative_plan(ref)
    reversed_plan=replace(correct,plan_id='explicit-reversed-directions',
                          directions={k:tuple(reversed(v)) for k,v in correct.directions.items()})
    rows=[]
    for mid,actual in [('V066-1','correct'),('V066-2','incorrect')]:
        frames,times,_=read_rgb(Path(tasks[mid]['path']));e=observe_rgb(frames,times,geometry,cfg)
        for valid,plan in [(True,correct),(False,reversed_plan)]:
            ex=judge_execution(e,plan);no=judge_normative(e,ref)
            expected='match' if (actual=='correct')==valid else 'mismatch'
            rows.append(dict(sample=mid,actual_condition=actual,plan_normative=valid,
                execution=ex,normative=no,expected_execution=expected,expected_normative=actual,
                passed=ex['decision']==expected and no['decision']==actual))
    shutil.copyfile(Path(__file__),RUN/'direction_probe_source_snapshot.py')
    save(target,dict(scope='Additional exposed-development direction counterfactual; original human labels untouched',
        rows=rows,conditions=len(rows),passed=sum(r['passed'] for r in rows),new_video_files=0))
    print(json.dumps(dict(conditions=len(rows),passed=sum(r['passed'] for r in rows))))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run','direction-probe']);args=p.parse_args()
    {'prepare':prepare,'run':run,'direction-probe':direction_probe}[args.action]()
