"""Tool-assisted AI prereview of existing P0 data, separate from human gold.

Reference: independent official PDF text/diagrams, source candidate geometry.
RGB: all decoded frames, independent SVG raster masks and median anchors.
Does not call the renderer/observer or read schedules/predictions to decide.
Human-visible suggestions are preliminary; no human annotations are created.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import re
import time

import numpy as np
from PIL import Image, ImageFilter, ImageSequence

from scripts.p0.prepare_acceptance import FACETS, RUN as OLD_RUN, load_existing, save

RUN = Path('data/research/runs/p0_ai_prereview_2026-10-28')
PRIVATE = Path('private/p0_ai_prereview_2026-10-28')
REFERENCE = Path('/Users/cc/.cache/umm-survey-20261023/223/R06-beijing.pdf')
VERSION = 'p0-ai-prereview-v1'
# Diagnostic constants fixed before the full pass. Not evaluator thresholds.
SETTINGS = dict(ink=128, mask_core_erosion=3, endpoint_pixels=8,
    onset_fraction=.06, completion_fraction=.94, min_exclusive_pixels=8,
    significant_changed_pixels=12, outside_tolerance_pixels=18,
    anchor_displacement_fraction=.10)


def official_reference():
    import pdfplumber
    import pypdfium2
    templates, _ = load_existing()
    pages = defaultdict(list)
    for template in templates: pages[template['norm_reference']['pdf_page']].append(template)
    references=[]
    (PRIVATE/'reference').mkdir(parents=True,exist_ok=True)
    with pdfplumber.open(REFERENCE) as pdf:
        rendered=pypdfium2.PdfDocument(REFERENCE)
        for page_no, items in sorted(pages.items()):
            page=pdf.pages[page_no-1]
            chars=page.chars; lines=page.lines
            bitmap=rendered[page_no-1].render(scale=3).to_pil()
            for template in items:
                character=template['character']
                candidates=[c for c in chars if c['text']==character and 'STROKE' in c['fontname']]
                result=dict(character=character,template_id=template['template_id'],official_page=page_no,
                    official_index=template['norm_reference']['index'],status='unresolved_reference_layout')
                if len(candidates)==1:
                    c=candidates[0]
                    horizontal=sorted({l['top'] for l in lines if l['height']<.2 and l['x0']<c['x0']<l['x1']})
                    top=max(y for y in horizontal if y<c['top']); bottom=min(y for y in horizontal if y>c['bottom'])
                    vertical=sorted({round(l['x0'],2) for l in lines if l['width']<.2 and l['top']<=c['top']<=l['bottom']})
                    right=[x for x in vertical if x>c['x1']]
                    left=max(x for x in vertical if x<c['x0'])
                    seq_left,seq_right=right[:2]
                    digits=[d for d in chars if seq_left<d['x0']<seq_right and top<d['top']<bottom and d['text'] in '12345' and d['size']<12]
                    digits.sort(key=lambda d:(round(d['top']/3),d['x0']))
                    count_text=''.join(d['text'] for d in sorted(chars,key=lambda d:(round(d['top']/3),d['x0']))
                        if left<d['x0']<seq_left and top<d['top']<bottom)
                    count_match=re.search(r'(\d+)画',count_text)
                    image_path=PRIVATE/'reference'/f'{ord(character):05X}.png'
                    # pdfplumber coordinates include the nonzero MediaBox
                    # origin; PDFium bitmaps begin at (0,0) of that box.
                    ox,oy=page.bbox[:2]
                    bitmap.crop((round((left-ox)*3),round((top-oy)*3),round((seq_right-ox)*3),round((bottom-oy)*3))).save(image_path)
                    result.update(status='extracted',official_codes=''.join(d['text'] for d in digits),
                        printed_stroke_count=int(count_match.group(1)) if count_match else None,
                        row_bbox=[left,top,seq_right,bottom],page_origin=[ox,oy],diagram_path=str(image_path),
                        numeric_code_positions=[dict(code=d['text'],x=d['x0'],top=d['top']) for d in digits])
                references.append(result)
            page.flush_cache()
            print('reference page',page_no,'characters',len(references),flush=True)
    save(RUN/'official_reference_extraction.json',dict(reference_file=str(REFERENCE),
        extraction='PDF text positions + local original row crops; no OCR or inferred official sequence',
        no_new_human_verification=True,records=references))


def infer_basic_kind(median):
    """Coarse diagnostic only: not a complete Chinese stroke classifier."""
    p=np.asarray(median,float).copy();p[:,1]*=-1
    segments=np.diff(p,axis=0);length=np.linalg.norm(segments,axis=1)
    total=length.sum(); major=segments[length>.10*total]
    if len(major)>1:
        unit=major/np.linalg.norm(major,axis=1)[:,None]
        if np.any((unit[:-1]*unit[1:]).sum(axis=1)<.30): return '5'
    dx,dy=p[-1]-p[0]
    if dx>0 and abs(dy)<.6*dx:return '1'
    if dy>0 and abs(dx)<.18*dy:return '2'
    if total<250:return '?'
    if dx<0 and dy>0:return '3'
    if dx>=0 and dy>0:return '4'
    return '?'


def normative_suggestion(template,reference):
    n=len(template['strokes']);facets={k:'unknown' for k in FACETS['normative']}
    codes=reference.get('official_codes','')
    count=reference.get('printed_stroke_count')
    facets['character_identity']='pass' if reference['status']=='extracted' else 'unknown'
    facets['stroke_count']='pass' if count==n==len(codes) else 'fail' if count is not None and count!=n else 'unknown'
    inferred=''.join(infer_basic_kind(m) for m in template['medians'])
    suspects=[i+1 for i,(a,b) in enumerate(zip(inferred,codes)) if a!='?' and a!=b]
    evidence=[f'GF0023—2020 PDF第{reference["official_page"]}页，条目{reference["official_index"]}。',
        f'官方印刷笔数={count}；源候选笔数={n}；提取编码={codes or "未成功提取"}。',
        f'候选中线粗分类={inferred}（?为无法粗分；该分类不具备规范裁判效力）。',
        '相同编码仍可能对应不同空间笔画；没有以编码一致替代完整次序、折笔方向或异写核验。']
    if suspects:evidence.append('需优先核对粗分类差异笔号：'+','.join(map(str,suspects))+'；差异也可能由粗分类方法造成。')
    return dict(type='normative',character=template['character'],decision='conflict' if facets['stroke_count']=='fail' else 'unverified',
        facets=facets,reasons=['norm_conflict'] if facets['stroke_count']=='fail' else [],
        disputed=facets['stroke_count']=='fail',notes='\n'.join(evidence),events='',observed_order='',
        evidence=evidence,priority='high' if facets['stroke_count']=='fail' or suspects or not codes else 'normative_confirmation',
        classification_suspects=suspects,official_codes=codes,candidate_coarse_codes=inferred,
        review_method='AI-engineered reference extraction/coarse geometry screening; not per-item visual certification',
        review_coverage=dict(official_row_extracted=reference['status']=='extracted',full_normative_semantics_verified=False),
        reference_diagram=reference.get('diagram_path'),reference_consulted=False,
        reference_required=True,model_version=VERSION)


def read_rgb(path):
    frames=[];durations=[]
    with Image.open(path) as image:
        for frame in ImageSequence.Iterator(image):
            frames.append(np.asarray(frame.convert('RGB')).copy())
            durations.append(float(frame.info.get('duration',0))/1000)
    return np.stack(frames),np.r_[0,np.cumsum(durations[:-1])],durations


def first_frame(values):
    indexes=np.flatnonzero(values)
    return int(indexes[0]) if len(indexes) else None


def inspect_rgb(frames,times,masks,medians):
    """No construction labels, schedule, original prediction or progress map."""
    ink=frames.min(axis=-1)<SETTINGS['ink'];n=len(masks)
    union=masks.any(axis=0)
    # Ignore one-pixel SVG/Pillow boundary differences, not actual excess ink.
    expanded=np.asarray(Image.fromarray(union).filter(ImageFilter.MaxFilter(5)),bool)
    outside=(ink&~expanded).sum(axis=(1,2))
    lost=(ink[:-1]&~ink[1:]).sum(axis=(1,2)) if len(ink)>1 else np.array([0])
    exclusive=masks&(masks.sum(axis=0)==1)
    events=[]; reasons=[]; failures=[]
    facets={k:'unknown' for k in FACETS['rgb_event']}
    blank=not bool(ink.any())
    if blank: failures.append('blank')
    if int(outside.max())>SETTINGS['outside_tolerance_pixels']:failures.append('extra')
    if int(lost.max())>SETTINGS['significant_changed_pixels']:failures.append('disappeared')
    facets['ink_preservation']='fail' if 'disappeared' in failures else 'pass' if len(ink)>1 and not blank else 'not_applicable'
    partial_counts=np.zeros(len(ink),int)
    for i,region in enumerate(exclusive):
        core=np.asarray(Image.fromarray(region).filter(ImageFilter.MinFilter(SETTINGS['mask_core_erosion'])),bool)
        if core.sum()<SETTINGS['min_exclusive_pixels']:core=region
        event=dict(stroke=i+1,exclusive_pixels=int(core.sum()),onset_frame=None,complete_frame=None,
            onset_seconds=None,complete_seconds=None,direction='unknown')
        if core.sum()<SETTINGS['min_exclusive_pixels']:
            events.append(event);reasons.append('geometry_ambiguity');continue
        cov=ink[:,core].mean(axis=1)
        onset=first_frame(cov>=SETTINGS['onset_fraction']);complete=first_frame(cov>=SETTINGS['completion_fraction'])
        event.update(onset_frame=onset,complete_frame=complete,final_coverage=round(float(cov[-1]),4),
            onset_seconds=float(times[onset]) if onset is not None else None,
            complete_seconds=float(times[complete]) if complete is not None else None)
        if cov[-1]<.85:failures.append('missing')
        if onset is not None and complete is not None:partial_counts[onset:complete]+=1
        # Sample the median itself. Earliest-ink times near its start/end are
        # independent of the renderer's per-pixel arc progress projection.
        points=np.asarray(medians[i],float).copy();points[:,1]=900-points[:,1]
        points=10+points*(frames.shape[1]-20)/1024
        yy,xx=np.nonzero(core);coords=np.c_[xx,yy]
        anchors=[]
        for point in [points[0],points[-1]]:
            nearest=np.argsort(((coords-point)**2).sum(axis=1))[:SETTINGS['endpoint_pixels']]
            region_times=[first_frame(ink[:,yy[j],xx[j]]) for j in nearest]
            visible=[v for v in region_times if v is not None]
            anchors.append(float(np.median(visible)) if len(visible)>=max(2,len(nearest)//2) else None)
        start,end=anchors
        event.update(start_anchor_frame=start,end_anchor_frame=end)
        if start is not None and end is not None and np.linalg.norm(points[-1]-points[0])>2:
            event['direction']='forward' if start<end else 'reverse' if end<start else 'unknown'
            if end<start:failures.append('reverse_direction')
        events.append(event)
    onsets=[e['onset_frame'] for e in events];complete=[e['complete_frame'] for e in events]
    order=None
    if all(v is not None for v in onsets) and len(set(onsets))==n:
        order=sorted(range(n),key=lambda i:onsets[i])
        facets['order']='pass' if order==list(range(n)) else 'fail'
        if facets['order']=='fail':failures.append('wrong_order')
        if all(c is not None for c in complete):
            violations=[i for i,j in zip(order,order[1:]) if complete[i]>onsets[j]]
            facets['completion_sequence']='fail' if violations else 'pass'
            if violations:failures.append('concurrent')
    if (partial_counts>1).sum()>=2:failures.append('concurrent')
    facets['simultaneous_growth']='fail' if 'concurrent' in failures else 'pass' if order is not None else 'unknown'
    direction=[e['direction'] for e in events]
    facets['direction']='fail' if 'reverse' in direction else 'pass' if all(d=='forward' for d in direction) else 'unknown'
    has_missing='missing' in failures
    facets['stroke_identity_count']='fail' if has_missing or 'extra' in failures or blank else 'pass' if all(e.get('final_coverage',0)>=.94 for e in events) else 'unknown'
    facets['visible_content']='fail' if has_missing or 'extra' in failures or blank else 'pass' if facets['stroke_identity_count']=='pass' else 'unknown'
    if blank:
        for k in ['order','direction','completion_sequence','simultaneous_growth','ink_preservation']:facets[k]='not_applicable'
    elif len(ink)<3:
        for k in ['order','direction','completion_sequence','simultaneous_growth']:facets[k]='unknown'
        reasons.append('temporal_ambiguity')
    if any(v=='unknown' for v in facets.values()):reasons.append('geometry_ambiguity' if len(ink)>=3 else 'temporal_ambiguity')
    decision='incorrect' if failures else 'unknown' if 'unknown' in facets.values() else 'correct'
    return dict(decision=decision,facets=facets,reasons=sorted(set(failures+reasons)),
        events=events,observed_order=[i+1 for i in order] if order is not None else None,
        metrics=dict(frame_count=len(frames),stroke_count=n,maximum_ink_loss_pixels=int(lost.max()),
            maximum_outside_reference_pixels=int(outside.max()),initial_ink_pixels=int(ink[0].sum()),
            final_ink_pixels=int(ink[-1].sum()),concurrent_partial_frames=int((partial_counts>1).sum())),
        review_coverage=dict(all_decoded_frames_checked=True,AI_visually_watched_all_frames=False,
            direction_reference='source candidate median, not human-confirmed normative direction'),
        review_method='AI-engineered all-frame RGB analysis with independently rasterized SVG reference; provisional, source-geometry dependent')


def run_review():
    if (RUN/'ai_suggestions.jsonl').exists():raise ValueError('Keep completed prereview; use a new version/run for corrections')
    start=time.monotonic();templates,samples=load_existing()
    references=json.loads((RUN/'official_reference_extraction.json').read_text())['records']
    refs={r['template_id']:r for r in references};by_template={t['template_id']:t for t in templates}
    with gzip.open(PRIVATE/'svg_masks.json.gz','rt') as handle: raw_masks=json.load(handle)
    masks={}
    for key,values in raw_masks.items():
        output=np.zeros((len(values),128*128),bool)
        for i,indices in enumerate(values):output[i,indices]=True
        masks[key]=output.reshape(-1,128,128)
    records=[]
    for t in templates:
        item=normative_suggestion(t,refs[t['template_id']]);item.update(original_id='norm-'+t['template_id'],
            template_id=t['template_id'],source_group_id=t['source_group_id'])
        records.append(item)
    for i,s in enumerate(samples):
        frames,times,durations=read_rgb(s['media_path']);template=by_template[s['template_id']]
        item=inspect_rgb(frames,times,masks[s['template_id']+'|'+s['renderer_id']],template['medians'])
        text=[f'程序检查全部{len(frames)}个实际解码帧，媒体时长{sum(durations):.3f}秒。',
            f'参考是源候选几何；规范次序/方向尚需人工确认。',
            '初筛：'+item['decision']+'；原因：'+(','.join(item['reasons']) or '当前规则未发现违规。')]
        if len(frames)<3:text.append('只有首末等少量帧，不能恢复中间逐笔顺序。整体过程判定与顺序未知分别复核。')
        item.update(type='rgb_event',original_id=s['sample_id'],template_id=s['template_id'],
            source_group_id=s['source_group_id'],character=s['character'],model_version=VERSION,
            notes='\n'.join(text),evidence=text,disputed=False,priority='high' if item['decision']!='correct' else 'routine',
            reference_consulted=False,frame_timestamps=times.tolist())
        records.append(item)
        if (i+1)%100==0:print('RGB reviewed',i+1,'/',len(samples),flush=True)
    with (RUN/'ai_suggestions.jsonl').open('w') as handle:
        for item in records:handle.write(json.dumps(item,ensure_ascii=False)+'\n')
    # Original predictions enter only this post-hoc comparison; never inspect_rgb.
    original={p['sample_id']:p for p in (json.loads(line) for line in Path('data/research/runs/p0_data_eval_2026-10-27/holdout_predictions.jsonl').read_text().splitlines())}
    differences=[dict(sample_id=r['original_id'],character=r['character'],old=original[r['original_id']]['decision'],new=r['decision'])
        for r in records if r['original_id'] in original and r['decision']!=original[r['original_id']]['decision']]
    save(RUN/'comparison_to_frozen_observer.json',dict(purpose='Diagnostic disagreement queue, never human gold or threshold tuning',differences=differences))
    summary=dict(version=VERSION,completed_at_utc=datetime.now(timezone.utc).isoformat(),
        norm_count=len(templates),RGB_count=len(samples),formal_human_labels_created=0,
        decisions={kind:dict(Counter(r['decision'] for r in records if r['type']==kind)) for kind in ['normative','rgb_event']},
        normative_unresolved_facets=['spatial identity','full order within same basic stroke category','complete bend/direction','allowed variants'],
        full_frame_program_scan=True,AI_per_item_visual_review=False,observer_reused=False,renderer_reused=False,
        shared_source_geometry=True,independent_SVG_rasterizer='Chromium canvas SVG',
        old_holdout_predictions_modified=False,old_evaluator_thresholds_modified=False,
        disagreements_with_old_frozen_observer=len(differences),settings=SETTINGS,
        local_CPU_wall_seconds=time.monotonic()-start,GPU_hours=0,
        science_acceptance='Not established; pending actual human review of AI results and independent sources')
    save(RUN/'summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))


def make_assisted_pack():
    import csv
    import random
    old=json.loads((OLD_RUN/'review_freeze.json').read_text())
    rows={r['original_id']:r for r in (json.loads(line) for line in (RUN/'ai_suggestions.jsonl').read_text().splitlines())}
    visual=[json.loads(line) for line in (RUN/'AI_normative_visual_reviews.jsonl').read_text().splitlines()]
    refs={r['template_id']:r for r in json.loads((RUN/'official_reference_extraction.json').read_text())['records']}
    for review in visual:
        ai=next(r for r in rows.values() if r['type']=='normative' and r['character']==review['character'])
        ai['facets'].update(stroke_identity=review['stroke_identity_opinion'],order=review['order_opinion'])
        ai['reference_diagram']=refs[ai['template_id']]['diagram_path']
        ai['review_coverage']['AI_visual_reference_comparison']=True
        ai['model_version']=VERSION+'+visual1'
        ai['review_method']='All-character official/source diagram visual comparison plus code screening; direction and variant scope unresolved'
        message=('AI已逐字比较规范图示与候选累计图：空间笔画身份、累计次序在缩图可辨范围内一致。'
            if review['order_opinion']=='pass' else 'AI已查看规范与候选图示；密集部件在缩图中不足以确认身份和次序，保留未知。')
        message+=' 完整折笔方向、允许异写范围仍未核准；本条整体保持未核实。'
        ai['notes']+='\n'+message;ai['evidence'].append(message)
        ai['priority']='high' if review['order_opinion']=='unknown' else 'normative_confirmation'
    followups=json.loads((RUN/'AI_visual_followup.json').read_text())['records']
    for followup in followups:
        ai=rows[followup['original_id']]
        ai['raw_algorithm_decision']=ai['decision'];ai['raw_algorithm_reasons']=ai['reasons']
        ai.update(decision='unknown',disputed=True,reasons=['geometry_ambiguity'],priority='high')
        ai['model_version']=VERSION+'+visual1'
        for facet in ['order','direction','completion_sequence','simultaneous_growth']:
            if ai['facets'][facet]=='fail':ai['facets'][facet]='unknown'
        message='AI另看了7张实际关键帧：尚不能确认初筛报告的违规，亦不能排除帧间问题；现列为未知/争议，保留初筛原结果。'
        ai['evidence'].append(message);ai['notes']+='\n'+message
        ai['review_coverage']['AI_keyframes_visually_inspected']=7
    disagreements={r['sample_id'] for r in json.loads((RUN/'comparison_to_frozen_observer.json').read_text())['differences']}
    cross=disagreements|{f['original_id'] for f in followups}
    templates,_=load_existing();strata=defaultdict(list)
    for template in templates:strata[(template['role'],template['stroke_count_stratum'])].append(template)
    rng=random.Random(2026102802);assignment={}
    for key,items in sorted(strata.items()):
        items=sorted(items,key=lambda t:t['character']);rng.shuffle(items)
        for i,t in enumerate(items):assignment[t['template_id']]='A' if i<len(items)//2 else 'B'
    batches={'assisted_norm':[],'assisted_rgb':[]}
    for name,tasks in old['batches'].items():
        if name.startswith('practice'):continue
        for task in tasks:
            t=dict(task);ai=rows[t['original_id']]
            t.update(ai_suggestion=ai,blind_id='A-'+t['blind_id'][2:],
                batch='assisted_norm' if t['type']=='normative' else 'assisted_rgb',
                assigned_partition=assignment[t['original_id'].removeprefix('norm-') if t['type']=='normative' else ai['template_id']],
                cross_review=t['original_id'] in cross)
            batches[t['batch']].append(t)
    for tasks in batches.values():
        tasks.sort(key=lambda t:(t['ai_suggestion']['priority']!='high',t['character'],t['ordinal']))
    inherited={key:old['protocol'][key] for key in ['facets','status_values','error_reasons']}
    protocol=dict(inherited,id='p0-human-assisted-review-v1',mode='assisted',revision='1.0',
        status='AI_prereview_completed_waiting_for_human_review',batch_order=list(batches),
        practice_normative=0,practice_RGB=0,human_AI_suggestions_visible=True,
        second_reviewer='User can arrange; no participation or agreement inferred',
        replaces_blind_workflow_for_current_user=True,old_protocol_preserved=True,
        seed=None,not_the_proposed_320_clip_sample=True,review_count_normative=640,review_count_RGB=2752,
        human_reviewer_workload='Full AI results available; final confirmed human count is actual saved submissions only',
        legacy_records_formal_count=0,preserve_prior_results=True,
        new_evaluator_requires_new_independent_validation=True,
        previous_protocol=str(OLD_RUN/'review_freeze.json'),
        code_base_commit='a53f031c',
        source_files=['scripts/p0/ai_prereview.py','scripts/p0/review_server.py','scripts/p0/review_assisted.html'],
        rubric='Existing facet definitions retained; AI-visible explicit human adoption/edit; unknown is not verified gold',
        partition_seed=2026102802,partition_is_recommended_not_identity_assignment=True,
        review_order='Each person: own partition normative; both review36 cross-review RGB; remaining own partition RGB',
        sampling='Full census640 normative+2752RGB; no320-clip sampling claim',
        frozen_at_utc=datetime.now(timezone.utc).isoformat())
    save(RUN/'assisted_review_pack.json',dict(protocol=protocol,batches=batches,tutorial=[]))
    save(RUN/'assisted_protocol.json',protocol)
    with (RUN/'assisted_review_order.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['batch','position','blind_id','character','role','assigned_partition','cross_review','original_id'])
        writer.writeheader()
        for name,tasks in batches.items():
            for position,t in enumerate(tasks,1):
                writer.writerow(dict(batch=name,position=position,**{k:t[k] for k in ['blind_id','character','role','assigned_partition','cross_review','original_id']}))
    save(RUN/'human_assignment_plan.json',dict(seed=2026102802,
        method='Within each existing role/stroke-count stratum, seeded shuffle then equal halves; keep all videos of one character together',
        partitions={part:{name:sum(t['assigned_partition']==part for t in tasks) for name,tasks in batches.items()} for part in ['A','B']},
        cross_review_RGB=len(cross),extra_second_reviews=len(cross),
        extra_reviews_by_partition={part:sum(t['cross_review'] and t['assigned_partition']!=part for t in batches['assisted_rgb']) for part in ['A','B']},
        human_people_or_IDs_not_yet_registered=True,
        no_blind_reviewer_claim=True,unknown_suggestions_not_verified_gold=True))
    save(RUN/'effective_prereview_summary.json',dict(
        raw_algorithm_summary=str(RUN/'summary.json'),AI_visual_followup=str(RUN/'AI_visual_followup.json'),
        decisions={kind:dict(Counter(r['decision'] for r in rows.values() if r['type']==kind)) for kind in ['normative','rgb_event']},
        total_items=len(rows),AI_normative_visually_compared=len(visual),
        normative_visual_opinions=dict(Counter(r['order_opinion'] for r in visual)),
        normative_full_direction_and_variant_scope_verified=0,
        AI_keyframe_reviewed_clips=len(followups),AI_full_frame_visually_certified_clips=0,
        full_frame_program_checked_clips=2752,formal_human_records_created=0))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['reference','review','pack'])
    args=parser.parse_args()
    {'reference':official_reference,'review':run_review,'pack':make_assisted_pack}[args.stage]()
