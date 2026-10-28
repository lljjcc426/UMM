"""Read-only evidence audit and private visual aids; never rescore the holdout."""
from collections import Counter, defaultdict
import csv
import gzip
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from scripts.p0.ai_prereview import read_rgb, SETTINGS, REFERENCE
from scripts.p0.prepare_acceptance import load_existing
from scripts.p0.prereview_v2 import RUN

PRIVATE=Path('private/p0_program_ai_audit_2026-10-28')
OLD=Path('data/research/runs/p0_ai_prereview_2026-10-28')
FONT='/System/Library/Fonts/STHeiti Light.ttc'


def save(name,value):
    (RUN/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def inventory():
    started=time.perf_counter();templates,samples=load_existing()
    roles=defaultdict(list)
    for t in templates:roles[t['role']].append(t)
    pack=json.loads((OLD/'assisted_review_pack.json').read_text())
    ai={t['original_id']:t for t in pack['batches']['assisted_rgb']}
    rows=[];finals={};pair_rows=[]
    for s in samples:
        frames,times,durations=read_rgb(s['media_path']);case=s['evaluation_only']['construction_case']
        row=dict(sample_id=s['sample_id'],character=s['character'],role=s['role'],renderer=s['renderer_id'],
            construction_case=case,decoded_frames=len(frames),duration_seconds=sum(durations),
            frame_count_matches=len(frames)==s['frame_count'],
            timestamps_match=bool(np.allclose(times,s['frame_timestamps'],atol=1e-6,rtol=0)),
            durations_match=bool(np.allclose(durations,s['frame_durations'],atol=1e-6,rtol=0)),
            positive_durations=all(d>0 for d in durations),strict_chronology=bool(np.all(np.diff(times)>0)),
            effective_AI_decision=ai[s['sample_id']]['ai_suggestion']['decision'])
        rows.append(row);key=(s['template_id'],s['renderer_id'])
        finals.setdefault(key,{})[case]=frames[-1]
    same_final_cases={'swap','reverse','concurrent','flash','low_sampling','partial_prefix','correct'}
    for key,cases in finals.items():
        if 'correct' not in cases:continue
        for case,frame in cases.items():
            if case not in same_final_cases or case=='correct':continue
            pair_rows.append(dict(template_id=key[0],renderer=key[1],construction_case=case,
                final_pixels_equal=bool(np.array_equal(cases['correct'],frame))))
    (RUN/'all_video_integrity.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    (RUN/'same_final_pairs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in pair_rows))
    with (RUN/'character_inventory.csv').open('w') as h:
        w=csv.DictWriter(h,fieldnames=['character','unicode','template_id','role','stroke_count','stratum','source_group_id','videos','current_576_projection'])
        w.writeheader()
        for t in templates:w.writerow(dict(character=t['character'],unicode=f'U+{ord(t["character"]):04X}',template_id=t['template_id'],
            role=t['role'],stroke_count=len(t['strokes']),stratum=t['stroke_count_stratum'],source_group_id=t['source_group_id'],
            videos=sum(s['template_id']==t['template_id'] for s in samples),current_576_projection=t['role']!='observer_holdout'))
    unknown=[r for r in rows if r['effective_AI_decision']=='unknown']
    summary=dict(characters=len(templates),videos=len(rows),decoded_frames=sum(r['decoded_frames'] for r in rows),
        role_counts={role:dict(characters=len(ts),videos=sum(r['role']==role for r in rows),
            strata=dict(Counter(t['stroke_count_stratum'] for t in ts))) for role,ts in roles.items()},
        unique_characters=len({t['character'] for t in templates}),unique_source_groups=len({t['source_group_id'] for t in templates}),
        role_character_overlap=sum(len({t['character'] for t in roles[a]}&{t['character'] for t in roles[b]})
            for i,a in enumerate(roles) for b in list(roles)[i+1:]),
        original_plan=576,additional_observer_holdout=64,current_minus_holdout=576,
        original_frozen_576_list_available=False,original_576_exact_identity_claim=False,
        failures=[r['sample_id'] for r in rows if not all(r[k] for k in ['frame_count_matches','timestamps_match','durations_match','positive_durations','strict_chronology'])],
        duration_seconds=sum(r['duration_seconds'] for r in rows),
        same_final_by_case={c:dict(pairs=sum(r['construction_case']==c for r in pair_rows),
            equal=sum(r['construction_case']==c and r['final_pixels_equal'] for r in pair_rows)) for c in sorted({r['construction_case'] for r in pair_rows})},
        effective_AI_decisions=dict(Counter(r['effective_AI_decision'] for r in rows)),
        unknown=dict(total=len(unknown),two_frame=sum(r['decoded_frames']<3 for r in unknown),multiframe=sum(r['decoded_frames']>=3 for r in unknown)),
        no_holdout_rescoring=True,no_media_rewritten=True,wall_seconds=time.perf_counter()-started,GPU_hours=0)
    save('inventory_summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))


def visual_aids():
    import pypdfium2
    templates,samples=load_existing();template_by_id={t['template_id']:t for t in templates}
    pack=json.loads((OLD/'assisted_review_pack.json').read_text())
    refs={r['template_id']:r for r in json.loads((OLD/'official_reference_extraction.json').read_text())['records']}
    with gzip.open('private/p0_ai_prereview_2026-10-28/svg_masks.json.gz','rt') as f:raw=json.load(f)
    norm=[n for n in pack['batches']['assisted_norm'] if n['ai_suggestion']['facets']['order']=='unknown']
    pdf=pypdfium2.PdfDocument(REFERENCE);font=ImageFont.truetype(FONT,23);small=ImageFont.truetype(FONT,16)
    for sub in ['reference_large','norm_sheets','RGB_sheets']:(PRIVATE/sub).mkdir(parents=True,exist_ok=True)
    index=[]
    # Eight rows per sheet. Native large official crop plus 128px candidate
    # masks reduced to64px per stroke; diagrams stay private (not redistributable).
    for start in range(0,len(norm),8):
        sheet=Image.new('RGB',(1900,8*330),'white');draw=ImageDraw.Draw(sheet)
        for row,n in enumerate(norm[start:start+8]):
            tid=n['ai_suggestion']['template_id'];t=template_by_id[tid];r=refs[tid];page=pdf[r['official_page']-1]
            ox,oy=r['page_origin'];left,top,right,bottom=r['row_bbox'];width,height=page.get_size()
            crop=page.render(scale=8,crop=(left-ox,height-(bottom-oy),width-(right-ox),top-oy)).to_pil().convert('RGB')
            path=PRIVATE/'reference_large'/f'{ord(t["character"]):05X}.png';crop.save(path)
            crop.thumbnail((560,285));y=row*330
            draw.text((8,y+3),f'{start+row+1:03d} {t["character"]} | PDF {r["official_page"]} | {len(t["strokes"])} strokes',font=font,fill='black')
            sheet.paste(crop,(0,y+40))
            masks=[]
            for indices in raw[tid+'|outline']:
                mask=np.zeros(128*128,bool);mask[indices]=True;masks.append(mask.reshape(128,128))
            past=np.zeros((128,128),bool)
            for i,m in enumerate(masks):
                im=np.full((128,128,3),255,np.uint8);im[past]=[185,190,196];im[m]=[28,76,166]
                x=570+(i%20)*66;cell=Image.fromarray(im).resize((64,64))
                sheet.paste(cell,(x,y+80));draw.text((x+22,y+149),str(i+1),font=small,fill='black');past|=m
            draw.line((0,y+328,1900,y+328),fill='#b0b0b0')
            index.append(dict(ordinal=start+row+1,character=t['character'],template_id=tid,sheet=str(PRIVATE/'norm_sheets'/f'{start//8+1:02}.jpg'),reference_large=str(path),prior_order='unknown'))
        sheet.save(PRIVATE/'norm_sheets'/f'{start//8+1:02}.jpg',quality=95)
    save('normative_visual_index.json',index)
    unknown=[n for n in pack['batches']['assisted_rgb'] if n['ai_suggestion']['decision']=='unknown' and n['ai_suggestion']['metrics']['frame_count']>=3]
    ri=[]
    for start in range(0,len(unknown),6):
        sheet=Image.new('RGB',(1500,6*230),'white');draw=ImageDraw.Draw(sheet)
        for row,t in enumerate(unknown[start:start+6]):
            frames,times,_=read_rgb(t['media_path']);selected=np.unique(np.linspace(0,len(frames)-1,10,dtype=int))
            y=row*230;draw.text((5,y+2),f'{start+row+1:02} {t["character"]} / {t["original_id"]} / {len(frames)} frames',font=font,fill='black')
            for i,k in enumerate(selected):
                sheet.paste(Image.fromarray(frames[k]).resize((145,145)),(i*150,y+35));draw.text((i*150+10,y+185),f'f{k} {times[k]:.2f}s',font=small,fill='black')
            draw.line((0,y+228,1500,y+228),fill='#b0b0b0')
            ri.append(dict(ordinal=start+row+1,sample_id=t['original_id'],character=t['character'],role=t['role'],frames=len(frames),viewed_frames=selected.tolist(),sheet=str(PRIVATE/'RGB_sheets'/f'{start//6+1:02}.jpg'),full_frame_AI_visual_review=False))
        sheet.save(PRIVATE/'RGB_sheets'/f'{start//6+1:02}.jpg',quality=94)
    save('RGB_visual_index.json',ri)
    print(json.dumps(dict(normative_characters=len(norm),normative_sheets=(len(norm)+7)//8,RGB_clips=len(unknown),RGB_sheets=(len(unknown)+5)//6)))


def diagnostics():
    templates,samples=load_existing();by_id={t['template_id']:t for t in templates}
    pack=json.loads((OLD/'assisted_review_pack.json').read_text())
    with gzip.open('private/p0_ai_prereview_2026-10-28/svg_masks.json.gz','rt') as f:raw=json.load(f)
    unknowns=[];six=[]
    consensus=json.loads(Path('data/research/runs/p0_quick_consensus_2026-10-28/summary.json').read_text())
    quick=json.loads(Path('data/research/runs/p0_quick_review_2026-10-28/quick_review_freeze.json').read_text())
    consensus_ids={c['rgb']['original_id'] for c in quick['batches']['quick_cards'] if c['character'] in consensus['consensus_characters']}
    for task in pack['batches']['assisted_rgb']:
        a=task['ai_suggestion']
        if a['decision']!='unknown':continue
        reasons=Counter();anchors=[];key=a['template_id']+'|'+task['renderer']
        masks=[]
        for indices in raw[key]:
            m=np.zeros(128*128,bool);m[indices]=True;masks.append(m.reshape(128,128))
        masks=np.asarray(masks);exclusive=masks&(masks.sum(axis=0)==1)
        t=by_id[a['template_id']]
        for i,event in enumerate(a['events']):
            if event['direction']!='unknown':continue
            core=np.asarray(Image.fromarray(exclusive[i]).filter(ImageFilter.MinFilter(3)),bool)
            if core.sum()<8:core=exclusive[i]
            yy,xx=np.nonzero(core);coords=np.c_[xx,yy]
            points=np.asarray(t['medians'][i],float).copy();points[:,1]=900-points[:,1];points=10+points*108/1024
            sets=[np.argsort(((coords-point)**2).sum(axis=1))[:8] for point in [points[0],points[-1]]]
            same=bool(np.array_equal(np.sort(sets[0]),np.sort(sets[1])))
            reason=('insufficient_exclusive_pixels' if len(coords)<8 else 'identical_endpoint_pixel_sets' if same
                else 'endpoint_displacement_below2px' if np.linalg.norm(points[-1]-points[0])<=2
                else 'tied_or_invisible_endpoint_times')
            reasons[reason]+=1
            anchors.append(dict(stroke=i+1,core_pixels=len(coords),start_region_size=len(sets[0]),end_region_size=len(sets[1]),
                region_intersection=len(np.intersect1d(*sets)),identical_sets=same,
                start_anchor_frame=event.get('start_anchor_frame'),end_anchor_frame=event.get('end_anchor_frame'),diagnostic=reason))
        row=dict(sample_id=task['original_id'],character=task['character'],role=task['role'],frames=a['metrics']['frame_count'],
            unknown_facets=[k for k,v in a['facets'].items() if v=='unknown'],endpoint_diagnostics=dict(reasons),events=anchors,
            contains_intermediate_frames=a['metrics']['frame_count']>=3,
            AI_decision_preserved='unknown',candidate_v2_holdout_rescoring_performed=False)
        unknowns.append(row)
        if task['original_id'] in consensus_ids:six.append(row)
    save('unknown_diagnostics.json',dict(total=len(unknowns),records=unknowns))
    save('six_consensus_root_cause.json',dict(records=six,
        interpretation='All six have an8-pixel core used for both8-nearest endpoint regions; identical evidence cannot establish direction. This explains AI abstention, not a defect in the unchanged frozen observer.',
        human_global_process_consensus_count=6,human_notes_verbatim='视频完整过程正确',human_per_stroke_gold_inferred=0,original_holdout_rescored=False))
    integrity=[json.loads(line) for line in (RUN/'all_video_integrity.jsonl').read_text().splitlines()]
    static=[r for r in integrity if r['decoded_frames']==1];bad=[r for r in integrity if not all(r[k] for k in ['frame_count_matches','timestamps_match','durations_match','strict_chronology']) or (r['decoded_frames']>1 and not r['positive_durations'])]
    save('integrity_adjudication.json',dict(decoded_files=len(integrity),animated_clips=sum(r['decoded_frames']>1 for r in integrity),
        static_blank_controls=len(static),static_cases=dict(Counter(r['construction_case'] for r in static)),
        duration_for_static_controls='not encoded; duration0 is missing timing, not zero-duration executed writing',
        invalid_animated_timestamps_or_durations=len(bad),invalid_samples=bad,
        initial_raw_audit='inventory_summary.json retains192 positive-duration flags, all static blank controls',
        effect='Blank visual rejection remains supported; static controls provide no temporal or writing-process evidence'))
    # Expand the initial matched-final table to all planned same-terminal cases.
    final=defaultdict(dict)
    for s in samples:
        with Image.open(s['media_path']) as im:
            im.seek(im.n_frames-1);frame=np.asarray(im.convert('RGB'))
        final[(s['template_id'],s['renderer_id'])][s['evaluation_only']['construction_case']]=frame
    pairs=[]
    for key,cases in final.items():
        if 'correct' not in cases:continue
        for case in ['swap','reverse','simultaneous','early_next','flash','sparse']:
            if case in cases:pairs.append(dict(template_id=key[0],renderer=key[1],case=case,equal=bool(np.array_equal(cases[case],cases['correct']))))
    save('expanded_same_final_pairs.json',dict(pairs=pairs,by_case={case:dict(total=sum(r['case']==case for r in pairs),equal=sum(r['case']==case and r['equal'] for r in pairs)) for case in sorted({r['case'] for r in pairs})}))
    from scripts.p0.evaluate import summarize
    old_run=Path('data/research/runs/p0_data_eval_2026-10-27')
    predictions=[json.loads(line) for line in (old_run/'holdout_predictions.jsonl').read_text().splitlines()]
    metrics=summarize(predictions)
    save('scorer_independence_and_statistics.json',dict(recomputed_from_saved_predictions_only=metrics,
        observer_inputs=['decoded_RGB_frames','canonical_masks','canonical_arc_progress','frozen_thresholds'],
        event_log_or_construction_label_used_inside_observe=False,labels_joined_after_observation=True,
        reference_geometry_shared_with_renderer=True,arc_projection_implementation_shared_with_renderer=True,
        SVG_AI_prereview_uses_independent_rasterizer=True,SVG_AI_prereview_still_uses_same_source_strokes_and_medians=True,
        geometric_source_independence=False,temporal_event_log_independence=True,
        prefix_adapter_excludes_future_RGB=True,
        condition_for_binomial_bound=['64 character groups are independent and representative of the declared sampling population',
            'within each group fixed controlled negatives define any-false-accept outcome',
            'construction labels correctly describe observable events',
            'no threshold selection on holdout'],
        source_geometry_lineages_observed=1,real_writer_recordings=0,independent_domain_sample_size_known=False,
        hypothetical_effective_group_sensitivity=[dict(assumed_independent_groups=n,zero_event_upper95=1-.05**(1/n)) for n in [64,32,16,8,4,1]],
        sensitivity_is_not_an_estimated_adjusted_confidence_interval=True,
        later_exposure='Holdout labels and human opinions have now been inspected; any new observer version needs a fresh locked validation set',
        current_holdout_predictions_changed=False,holdout_observer_run_count_added=0))
    print(json.dumps(dict(unknowns=len(unknowns),six=len(six),static_controls=len(static),animated_integrity_errors=len(bad),paired_finals=len(pairs))))


if __name__=='__main__':
    import sys
    {'inventory':inventory,'visuals':visual_aids,'diagnostics':diagnostics}[sys.argv[1]]()
