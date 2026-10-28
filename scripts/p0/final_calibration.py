"""Prepare one finite human calibration package on fresh CASIA acquisitions.

All source geometry/media stays private under CASIA academic-use conditions.
No human conclusion, natural writing time or normative order is inferred.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime,timezone
import csv
import json
from pathlib import Path
import random
import time

import numpy as np
from PIL import Image,ImageDraw,ImageFont

from scripts.p0.casia_subset import RUN,PRIVATE,parse_pot,save
from scripts.p0.prepare_acceptance import load_existing
from scripts.p0.ai_prereview import read_rgb,inspect_rgb,REFERENCE,infer_basic_kind
from scripts.p0.prereview_v2 import inspect_rgb_v2
from scripts.p0.observer import observe,one_sided_upper

SEED=2026102804
STRATA=['2-5','6-8','9-12','13-20']
NEGATIVES=['swap','reverse','missing','extra','simultaneous','early_next','disappear','blank']


def normalize(strokes):
    pts=np.concatenate([np.asarray(s,float) for s in strokes]);lo=pts.min(0);hi=pts.max(0)
    scale=104/max(hi-lo);origin=(128-(hi-lo)*scale)/2
    return [(np.asarray(s,float)-lo)*scale+origin for s in strokes]


def resample(points,count=33):
    points=np.asarray(points,float)
    if len(points)==1:return np.repeat(points,count,axis=0)
    length=np.r_[0,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
    if length[-1]==0:return np.repeat(points[:1],count,axis=0)
    return np.c_[np.interp(np.linspace(0,length[-1],count),length,points[:,0]),
                 np.interp(np.linspace(0,length[-1],count),length,points[:,1])]


def prefix_points(points,fraction):
    """Keep every original bend before the interpolated moving endpoint."""
    points=np.asarray(points,float)
    if fraction>=1 or len(points)==1:return points
    length=np.r_[0,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
    end=fraction*length[-1];i=min(np.searchsorted(length,end,side='right'),len(points)-1)
    if length[i]==length[i-1]:return points[:i+1]
    tip=points[i-1]+(points[i]-points[i-1])*(end-length[i-1])/(length[i]-length[i-1])
    return np.vstack([points[:i],tip])


def draw_stroke(draw,points,fill=0):
    if len(points)==1:
        x,y=points[0];draw.ellipse((x-2,y-2,x+2,y+2),fill=fill)
    else:draw.line([tuple(p) for p in points],fill=fill,width=5,joint='curve')


def reference_geometry(strokes):
    """Static stroke identities and nearest-vertex arc coordinates, no events."""
    masks=[];progress=[];yy,xx=np.mgrid[:128,:128]
    for s in strokes:
        im=Image.new('L',(128,128),0);draw_stroke(ImageDraw.Draw(im),s,255)
        masks.append(np.asarray(im)>0)
        points=resample(s,33);distance=(xx[:,:,None]-points[:,0])**2+(yy[:,:,None]-points[:,1])**2
        progress.append(distance.argmin(-1).astype(np.float32)/32)
    return np.asarray(masks),np.asarray(progress)


def median_units(strokes):
    return [np.c_[(s[:,0]-10)*1024/108,900-(s[:,1]-10)*1024/108].tolist() for s in strokes]


def render_trajectory(strokes,case,steps=12):
    """Independent prefix-polyline rendering, with artificial uniform timing.

    The observer never receives this schedule. Coordinate order is recorded;
    synthetic frame timing is not the writer's physical sampling time.
    """
    order=list(range(len(strokes)))
    if case=='swap':order[0],order[1]=order[1],order[0]
    if case=='missing':order.pop()
    masks=[];growth=[]
    for s in strokes:
        full=Image.new('L',(128,128),0);draw_stroke(ImageDraw.Draw(full),s,255);mask=np.asarray(full)>0
        path=s[::-1] if case=='reverse' else s;stages=[np.zeros((128,128),bool)]
        for step in range(1,steps+1):
            im=Image.new('L',(128,128),0);draw_stroke(ImageDraw.Draw(im),prefix_points(path,step/steps),255)
            stages.append(stages[-1]|((np.asarray(im)>0)&mask))
        stages[-1]=mask;masks.append(mask);growth.append(stages)
    masks=np.asarray(masks)
    cursor=1;schedule=[]
    for i in order:
        onset=1 if case=='simultaneous' else cursor
        schedule.append((i,onset));cursor+=steps//2 if case=='early_next' else steps+3
    count=max(s for _,s in schedule)+steps+3
    frames=[]
    for t in range(count):
        ink=np.zeros((128,128),bool)
        for j,start in schedule:
            if t<start:continue
            ink|=growth[j][min(steps,t-start+1)]
        if case=='extra' and t>=count-3:ink[2:6,2:17]=True
        if case=='blank':ink[:]=False
        if case=='disappear' and t>=count-3:
            ink[masks[0]&(masks.sum(0)==1)]=False
        a=np.full((128,128,3),255,np.uint8);a[ink]=0;frames.append(Image.fromarray(a))
    if case=='sparse':frames=[frames[0],frames[-1]]
    return frames


def save_animation(path,frames):
    # No original IDs, cases or timing logs in media metadata.
    frames[0].save(path,format='PNG',save_all=True,append_images=frames[1:],duration=80,loop=0,disposal=0,blend=0,compress_level=1)


def text_candidates(templates):
    """Tentative text segmentation, subject to explicit human verification."""
    by_char={t['character']:t for t in templates};candidates=[]
    for f in sorted(PRIVATE.glob('006-P*-page.json')):
        page=json.loads(f.read_text())
        for line_index,line in enumerate(page['lines']):
            intervals=sorted((min(p[0] for p in page['strokes'][i]),max(p[0] for p in page['strokes'][i]),i) for i in line['stroke_indices'])
            groups=[]
            for lo,hi,i in intervals:
                if groups and lo<=groups[-1][1]:groups[-1][1]=max(hi,groups[-1][1]);groups[-1][2].append(i)
                else:groups.append([lo,hi,[i]])
            if len(groups)!=len(line['text']):continue
            for position,(char,group) in enumerate(zip(line['text'],groups)):
                if char not in by_char or by_char[char]['role']!='model_train':continue
                indexes=sorted(group[2]);source=[page['strokes'][i] for i in indexes]
                candidates.append(dict(character=char,page_file=f.name,writer_id='006',line_index=line_index,position=position,
                    line_text=line['text'],line_strokes=[page['strokes'][i] for i in line['stroke_indices']],
                    strokes=source,x_interval=group[:2],stroke_indices=indexes,segmentation_status='candidate_not_gold'))
    unique={}
    for c in candidates:unique.setdefault(c['character'],c)
    return list(unique.values())


def official_crop(template,reference,target):
    import pypdfium2
    pdf=pypdfium2.PdfDocument(REFERENCE);page=pdf[reference['official_page']-1]
    left,top,right,bottom=reference['row_bbox'];ox,oy=reference['page_origin'];w,h=page.get_size()
    page.render(scale=6,crop=(left-ox,h-(bottom-oy),w-(right-ox),top-oy)).to_pil().convert('RGB').save(target)
    page.close();pdf.close()


def prepare():
    if (RUN/'predictions.jsonl').exists():raise ValueError('Preserve completed calibration; do not overwrite')
    started=time.monotonic();rng=random.Random(SEED);templates,_=load_existing()
    by_char={t['character']:t for t in templates};source=json.loads((RUN/'writer_source_inventory.json').read_text())
    roster=json.loads((RUN/'writer_selection_freeze.json').read_text());writers={}
    for r in source['writers']:
        writers[r['writer_id']]={x['character']:x for x in parse_pot(Path(r['local_file']).read_bytes())}
    prior=RUN/'attempt01_renderer'/'selection_freeze.json'
    exposed={(r['writer_id'],r['character']) for r in json.loads(prior.read_text())['records']} if prior.exists() else set()
    selected=[];used=set();part_of={w:p for p in ['development','validation'] for w in roster[p]}
    quotas={(p,s,r):n for p,n in [('development',2),('validation',8)] for s in STRATA for r in ['model_train','model_character_test']}
    options={}
    for writer in writers:
        cs=sorted(c for c,t in by_char.items() if t['role'] in ['model_train','model_character_test'] and (writer,c) not in exposed
                  and c in writers[writer] and len(writers[writer][c]['strokes'])==len(t['strokes']))
        rng.shuffle(cs);options[writer]=cs
    def category(w,c):return (part_of[w],by_char[c]['stroke_count_stratum'],by_char[c]['role'])
    def assign(remaining):
        if not remaining:return []
        eligible={w:[c for c in options[w] if c not in used and quotas[category(w,c)]>0] for w in remaining}
        if any(not c for c in eligible.values()):return None
        for key,n in quotas.items():
            if n and sum(any(category(w,c)==key for c in cs) for w,cs in eligible.items())<n:return None
        w=min(remaining,key=lambda x:len(eligible[x]));rest=[x for x in remaining if x!=w]
        for c in eligible[w]:
            key=category(w,c);quotas[key]-=1;used.add(c);result=assign(rest)
            if result is not None:return [(w,c)]+result
            used.remove(c);quotas[key]+=1
        return None
    assignment=assign(list(part_of))
    if assignment is None:raise ValueError('Fixed writer/stratum/role quotas have no count-matched unique-character assignment')
    for writer,c in sorted(assignment,key=lambda v:(part_of[v[0]]!='development',roster[part_of[v[0]]].index(v[0]))):
        record=writers[writer][c];role=by_char[c]['role'];stratum=by_char[c]['stroke_count_stratum']
        selected.append(dict(character=c,writer_id=writer,part=part_of[writer],stratum=stratum,original_role=role,
            template_id=by_char[c]['template_id'],record_offset=record['record_offset'],record_bytes=record['record_bytes'],
            source_pen_strokes=len(record['strokes']),strokes=record['strokes']))
    # Fixed source/character membership before any observer prediction.
    selection=[{k:v for k,v in r.items() if k!='strokes'} for r in selected]
    save(RUN/'selection_freeze.json',dict(frozen_at_utc=datetime.now(timezone.utc).isoformat(),seed=SEED,records=selection,
        eligibility='Existing main train/character-test roles; not old observer development/holdout; source pen-stroke count must match official candidate count',
        count_matching_is_not_normative_order_confirmation=True,selection_before_scoring=True,development_groups=16,validation_writer_groups=64,
        distinct_characters=len(used),distinct_writers=len(writers),prior_invalid_writer_character_pairs_excluded=True,
        renderer_revision=2,prior_invalid_render_writer_exposure_disclosed=True,
        sampling_target='Declared count-matched available-character subset of official test writers; not all handwriting'))
    (PRIVATE/'media').mkdir(exist_ok=True);(PRIVATE/'reference').mkdir(exist_ok=True)
    refs={r['template_id']:r for r in json.loads(Path('data/research/runs/p0_ai_prereview_2026-10-28/official_reference_extraction.json').read_text())['records']}
    thresholds=json.loads(Path('data/research/runs/p0_data_eval_2026-10-27/threshold_freeze.json').read_text())['thresholds']
    pack=dict(protocol={},tasks=[],tutorial=[]);predictions=[];media=[];norm=[]
    negative_index=Counter()
    for k,r in enumerate(selected):
        t=by_char[r['character']];strokes=normalize(r['strokes']);masks,progress=reference_geometry(strokes);medians=median_units(strokes)
        nid=f'N{k+1:03d}';refpath=PRIVATE/'reference'/f'{nid}.png';official_crop(t,refs[t['template_id']],refpath)
        task=dict(id=nid,kind='normative',character=r['character'],part=r['part'],reference_path=str(refpath),
            official_page=t['norm_reference']['pdf_page'],strokes=[p.tolist() for p in strokes],
            fields=['identity_order','direction'],source_scope='本候选为独立书写记录，笔数相符尚不代表规范笔顺相符。')
        norm.append(task);pack['tasks'].append(task)
        j=negative_index[r['part']];negative_index[r['part']]+=1
        cases=['source_order',NEGATIVES[j%8]]
        if r['part']=='validation' and j%4==0:cases.append('sparse')
        for q,case in enumerate(cases):
            mid=f'V{k+1:03d}-{q+1}';path=PRIVATE/'media'/f'{mid}.png'
            frames=render_trajectory(strokes,case);save_animation(path,frames)
            actual,times,durations=read_rgb(path)
            old=observe(actual,masks,progress,thresholds);v1=inspect_rgb(actual,times,masks,medians);v2=inspect_rgb_v2(actual,times,masks,medians)
            prediction=dict(id=mid,character=r['character'],writer_id=r['writer_id'],part=r['part'],stratum=r['stratum'],
                nominal_case=case,nominal_source_order_is_not_normative_gold=True,
                frozen_observer=old,AI_v1=v1,AI_v2=v2,last_frame_reference_iou=old['final_iou'])
            predictions.append(prediction)
            row=dict(id=mid,norm_id=nid,character=r['character'],writer_id=r['writer_id'],part=r['part'],stratum=r['stratum'],
                nominal_case=case,path=str(path),decoded_frames=len(actual),encoded_duration_seconds=sum(durations),native_RGB=False,physical_timing=False)
            media.append(row)
            pack['tasks'].append(dict(id=mid,kind='rgb',character=r['character'],part=r['part'],norm_id=nid,
                reference_path=str(refpath),official_page=t['norm_reference']['pdf_page'],path=str(path),frame_timestamps=times.tolist()))
    # Fill a prospective character x writer matrix from the separately exposed
    # pilot writers; no actual model exposure or performance is claimed.
    pool={w:{r['character']:r for r in json.loads((PRIVATE/(w+'-records.json')).read_text())} for w in ['006','205']}
    repeats=text_candidates(templates);rng.shuffle(repeats);repeats=repeats[:8]
    repeated_chars={r['character'] for r in repeats}
    crossed=[];chars=[]
    for role in ['model_train','model_character_test']:
        eligible=sorted(c for c,t in by_char.items() if t['role']==role and all(c in p for p in pool.values()))
        initial=sorted(repeated_chars) if role=='model_train' else []
        rng.shuffle(eligible);chars.extend(initial+[c for c in eligible if c not in initial][:32-len(initial)])
    for writer in pool:
        for c in chars:
            t=by_char[c];crossed.append(dict(character=c,writer_id=writer,original_role=t['role'],
                proposed_cell=('train_reference' if t['role']=='model_train' else 'character_holdout') if writer=='006'
                    else ('writer_holdout' if t['role']=='model_train' else 'character_and_writer_holdout'),
                original_offset=pool[writer][c]['record_offset'],source_pen_strokes=len(pool[writer][c]['strokes']),normative_status='unverified',
                model_training_performed=False))
    save(RUN/'crossed_source_matrix.json',dict(characters=64,writers=2,source_records=len(crossed),records=crossed,
        cells=dict(Counter(r['proposed_cell'] for r in crossed)),same_source_group_overlap_across_cells=0,
        split_scope='Prospective separate extension, not a silent change to original640role assignments or evidence of model exposure',
        isolated_record_ID_candidates=len(repeats),repeated_page_recordings='10 original WPTT acquisitions, character cuts remain candidates until human verification'))
    for k,r in enumerate(repeats):
        rid=f'I{k+1:02d}';pts=np.concatenate([np.asarray(s,float) for s in r['line_strokes']]);lo=pts.min(0);hi=pts.max(0)
        scale=1400/max(hi-lo);margin=15;size=(1430,max(180,int((hi[1]-lo[1])*scale)+30))
        im=Image.new('RGB',size,'white');draw=ImageDraw.Draw(im)
        for s in r['line_strokes']:
            p=(np.asarray(s,float)-lo)*scale+margin;draw.line([tuple(a) for a in p],fill='black',width=3)
        left,right=[int((x-lo[0])*scale)+margin for x in r['x_interval']]
        draw.rectangle((max(0,left-3),3,min(size[0]-1,right+3),size[1]-4),outline='#166dba',width=3)
        context=PRIVATE/f'{rid}-context.png';im.save(context)
        preview=PRIVATE/f'{rid}-cut.png';cut=Image.new('RGB',(128,128),'white');d=ImageDraw.Draw(cut)
        for s in normalize(r['strokes']):draw_stroke(d,s,(0,0,0))
        cut.save(preview)
        pack['tasks'].append(dict(id=rid,kind='record',character=r['character'],part='record_audit',context_path=str(context),cut_path=str(preview),
            line_text=r['line_text'],position=r['position']+1,
            question='蓝框是否完整对应指定字符，且没有混入相邻字？仅核对记录身份和裁切，不据此核准规范或真实时间。'))
    save(PRIVATE/'ID_record_candidates.json',repeats)
    for r in pack['tasks']:r['formal']=r['part'] in ['validation','record_audit']
    public_protocol=dict(id='p0-final-independent-calibration-v1',status='draft_UI_test_pending',seed=SEED,
        population='Fresh count-matched CASIA isolated handwritten records; artificial timing and known per-record G1 geometry',
        human_characters=64,human_normative_tasks=64,human_RGB_tasks=144,human_record_tasks=len(repeats),
        tasks_per_reviewer=208+len(repeats),reviewers=['1','2'],independent_full_passes=2,AI_answers_visible_during_formal_review=False,
        reference_examples=4,new_human_batches_after_completion=0,disagreement_policy='Preserve disagreement as unknown; no third review round is automatically required',
        decisions={'normative':['pass','fail','unknown'],'rgb':['correct','incorrect','unknown'],'record':['pass','fail','unknown']},
        formal_task_order='Per-reviewer independently shuffled normative tasks, then shuffled RGB and record tasks; no case/AI/other-human answers',
        annotation_scope='Explicit identity/order and direction judgments; RGB overall process with error reasons; no inferred per-stroke timings or allowed-variant gold',
        second_reviewer='Entire same fixed calibration subset, not only disputes; same actors may have prior AI-visible experience, disclosed',
        thresholds_modified=False,old_holdout_reused=False,source_license='CASIA academic research group use only; raw assets private',
        no_native_RGB_claim=True,no_natural_timing_claim=True)
    pack['protocol']=public_protocol
    pack['reviewer_orders']={}
    for reviewer in ['1','2']:
        order_rng=random.Random(SEED+int(reviewer));a=[r['id'] for r in pack['tasks'] if r['formal'] and r['kind']=='normative'];b=[r['id'] for r in pack['tasks'] if r['formal'] and r['kind']!='normative']
        order_rng.shuffle(a);order_rng.shuffle(b);pack['reviewer_orders'][reviewer]=a+b
    # Operation tests and examples only use already exposed source/old dev.
    dev_norm=next(n for n in norm if n['part']=='development')
    test_norm=dict(dev_norm,id='TEST-N',part='operation_only',formal=False)
    test_video=next(t for t in pack['tasks'] if t['kind']=='rgb' and t['part']=='development')
    test_video=dict(test_video,id='TEST-V',part='operation_only',formal=False)
    context=Image.new('RGB',(300,100),'white');draw=ImageDraw.Draw(context)
    draw.text((10,10),'犬仓穴',font=ImageFont.truetype('/System/Library/Fonts/STHeiti Light.ttc',64),fill='black')
    draw.rectangle((5,5,78,90),outline='#166dba',width=3)
    context.save(PRIVATE/'TEST-context.png');context.crop((5,5,78,90)).save(PRIVATE/'TEST-cut.png')
    test_record=dict(id='TEST-I',kind='record',character='犬',part='operation_only',formal=False,
        context_path=str(PRIVATE/'TEST-context.png'),cut_path=str(PRIVATE/'TEST-cut.png'),line_text='犬仓穴',position=1,
        question='TEST_ONLY操作示意，不计科研记录')
    preview=dict(protocol=dict(public_protocol,id='p0-final-operation-only',status='preview',tasks_per_reviewer=3),
        tasks=[test_norm,test_video,test_record],reviewer_orders={'1':['TEST-N','TEST-V','TEST-I'],'2':['TEST-V','TEST-N','TEST-I']},tutorial=[])
    for case in ['correct','swap','reverse','sparse']:
        path=Path('examples/p0_data_eval')/(('flash' if case=='sparse' else case)+'.png')
        if path.exists():
            pack['tutorial'].append(dict(id='DEMO-'+case,kind='rgb',character='犬',path=str(path),
                explanation={'correct':'示意：依次完成且方向一致。','swap':'示意：先后交换，需要指出实际错误。','reverse':'示意：同一笔反向形成，末帧相同仍有过程差异。','sparse':'示意：仅首末帧，缺少中间证据，次序和方向保留未知。'}[case]))
    save(PRIVATE/'pack_draft.json',pack);save(PRIVATE/'operation_pack.json',preview)
    from scripts.p0.final_review_server import prepare_blind_ids
    prepare_blind_ids(PRIVATE/'pack_draft.json');prepare_blind_ids(PRIVATE/'operation_pack.json')
    save(RUN/'protocol_draft.json',public_protocol)
    (RUN/'predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in predictions))
    save(RUN/'new_media_inventory.json',dict(records=media,files=len(media),formal_files=sum(r['part']=='validation' for r in media),
        decoded_frames=sum(r['decoded_frames'] for r in media),encoded_seconds=sum(r['encoded_duration_seconds'] for r in media),
        synthetic_uniform_frame_duration_ms=80,old_media_unchanged=True,raw_assets_private=True))
    summary=dict(samples=len(predictions),by_part={p:dict(Counter(r['nominal_case'] for r in predictions if r['part']==p)) for p in ['development','validation']},
        decisions={p:{model:dict(Counter(r[model]['decision'] for r in predictions if r['part']==p)) for model in ['frozen_observer','AI_v1','AI_v2']} for p in ['development','validation']},
        human_reference_status='pending; construction and recorded pen order are not normative gold',thresholds_modified=False,old_holdout_runs_added=0,
        tuning_after_new_validation=False,scientific_acceptance=False,wall_seconds=time.monotonic()-started,GPU_hours=0)
    save(RUN/'program_summary.json',summary)
    with (RUN/'selection_manifest.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(selection[0]));w.writeheader();w.writerows(selection)
    print(json.dumps(dict(prepared=len(predictions),human_tasks_per_reviewer=public_protocol['tasks_per_reviewer'],norm64=True,RGB144=True,ID=len(repeats))))


def freeze():
    target=PRIVATE/'pack_frozen.json'
    if target.exists():raise ValueError('Protocol already frozen')
    check=json.loads((RUN/'browser_operation_check.json').read_text())
    if not check['passed'] or check['formal_samples_used']!=0:raise ValueError('Nonholdout browser test must pass first')
    pack=json.loads((PRIVATE/'pack_draft.json').read_text());p=pack['protocol']
    p.update(status='frozen_waiting_for_real_human_records',frozen_at_utc=datetime.now(timezone.utc).isoformat())
    save(target,pack);save(RUN/'protocol_frozen.json',p)
    save(RUN/'review_order_frozen.json',pack['reviewer_orders'])
    print(json.dumps(p,ensure_ascii=False))


def collect():
    """Aggregate actual paired human labels; incomplete passes stay pending."""
    from scripts.p0.final_review_server import FinalStore
    pack=json.loads((PRIVATE/'pack_frozen.json').read_text());store=FinalStore(pack,PRIVATE/'human_records')
    states={r:store.state(r) for r in ['1','2']}
    progress={r:dict(saved=s['saved'],total=s['total'],remaining=s['total']-s['saved']) for r,s in states.items()}
    if any(p['remaining'] for p in progress.values()):
        out=dict(status='waiting_for_actual_human_records',reviewers=progress,human_conclusions_inferred=False)
        save(RUN/'human_progress.json',out);print(json.dumps(out));return out
    annotations={r:{a['blind_id']:a for a in s['annotations']} for r,s in states.items()}
    consensus={};pairs=[]
    for task in pack['tasks']:
        if not task['formal']:continue
        bid=task['blind_id'];a,b=[annotations[r][bid] for r in ['1','2']]
        if task['kind']=='normative':
            agreed={k:a['judgments'][k] if a['judgments'][k]==b['judgments'][k] else 'unknown' for k in ['identity_order','direction']}
            value='pass' if all(v=='pass' for v in agreed.values()) else 'fail' if 'fail' in agreed.values() else 'unknown'
        else:value=a['decision'] if a['decision']==b['decision'] else 'unknown'
        consensus[task['id']]=value;pairs.append(dict(blind_id=bid,internal_id=task['id'],kind=task['kind'],
            reviewer1=a,reviewer2=b,paired_reference=value,disagreement=a.get('judgments',a.get('decision'))!=b.get('judgments',b.get('decision'))))
    predictions={p['id']:p for p in (json.loads(l) for l in (RUN/'predictions.jsonl').read_text().splitlines())}
    videos=[]
    for task in pack['tasks']:
        if not task['formal'] or task['kind']!='rgb':continue
        p=predictions[task['id']];gold=consensus[task['id']]
        if gold=='correct' and consensus[task['norm_id']]!='pass':gold='unknown'
        videos.append(dict(id=task['id'],writer_id=p['writer_id'],human_reference=gold,
            normative_reference=consensus[task['norm_id']],**{m:p[m]['decision'] for m in ['frozen_observer','AI_v1','AI_v2']}))
    metrics={}
    exposure=json.loads((RUN/'pre_review_exposure.json').read_text())
    flagged_writers=set(exposure['character_named_AI_flag_writer_ids'])
    for model in ['frozen_observer','AI_v1','AI_v2']:
        negative={v['writer_id'] for v in videos if v['human_reference']=='incorrect'}
        failure={v['writer_id'] for v in videos if v['human_reference']=='incorrect' and v[model]=='correct'}
        clear=[v for v in videos if v['human_reference'] in ['correct','incorrect']];positive=[v for v in clear if v['human_reference']=='correct']
        accepted=sum(v[model]=='correct' for v in positive)
        metrics[model]=dict(attempts=len(videos),human_reference_counts=dict(Counter(v['human_reference'] for v in videos)),
            decisions=dict(Counter(v[model] for v in videos)),clear_reference_attempts=len(clear),
            clear_coverage=sum(v[model]!='unknown' for v in clear)/len(clear) if clear else None,
            positive_controls=len(positive),positive_accepted=accepted,positive_acceptance=accepted/len(positive) if positive else None,
            positive_rejected=sum(v[model]=='incorrect' for v in positive),negative_writer_groups=len(negative),
            false_accept_writer_groups=len(failure),false_accept_upper95=one_sided_upper(len(failure),len(negative)),
            unknown_reference_accepted=sum(v['human_reference']=='unknown' and v[model]=='correct' for v in videos),
            reject_all_positive_failure=bool(positive and not accepted),
            inference_scope='Conditional on independent/representative sampled writers and paired labels; not native RGB or arbitrary handwriting')
        clean=[v for v in videos if v['writer_id'] not in flagged_writers]
        clean_negative={v['writer_id'] for v in clean if v['human_reference']=='incorrect'}
        clean_failure={v['writer_id'] for v in clean if v['human_reference']=='incorrect' and v[model]=='correct'}
        metrics[model]['prior_AI_character_flag_exclusion']=dict(excluded_writer_groups=len(flagged_writers),
            remaining_writer_groups=len({v['writer_id'] for v in clean}),negative_writer_groups=len(clean_negative),
            false_accept_writer_groups=len(clean_failure),false_accept_upper95=one_sided_upper(len(clean_failure),len(clean_negative)),
            status='Predeclared sensitivity excluding two character-level AI concerns disclosed in progress commentary; not a replacement primary denominator')
    out=dict(status='paired_human_labels_collected_scientific_review_required',reviewers=progress,
        consensus_counts={kind:dict(Counter(consensus[t['id']] for t in pack['tasks'] if t['formal'] and t['kind']==kind)) for kind in ['normative','rgb','record']},
        metrics=metrics,pairs=pairs,video_reference=videos,full_per_stroke_timings_inferred=False,
        additional_human_round_required=False,DATA_01_auto_pass=False,EVAL_01_auto_pass=False,P0_auto_pass=False)
    save(RUN/'human_calibration_results.json',out);print(json.dumps(dict(status=out['status'],metrics=metrics),ensure_ascii=False));return out


if __name__=='__main__':
    import sys
    {'prepare':prepare,'freeze':freeze,'collect':collect}[sys.argv[1]]()
