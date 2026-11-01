"""Small, exposed development suite. CPU renderer truth is never human gold."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import time

import numpy as np
from PIL import Image, ImageDraw

from hanzi_video.catalog import reference, geometry
from scripts.p0.geometry import stroke_geometry
from .contracts import save, validate_input, validate_manifest
from .media import encode, decode, sha256, validate_media
from .observer import observe_rgb, judge_execution

CHARACTERS=('士','丑','小','以','广','刃','乞','点')
SEED=20261101
REGIONS=[{'id':'upper','box':[12,24,116,34],'axis':'x'},
         {'id':'lower','box':[12,84,116,94],'axis':'x'}]
REFERENCE={'order':['upper','lower'],'directions':{'upper':'positive','lower':'positive'}}


def render_lines(case):
    frames=np.full((33,128,128,3),255,np.uint8)
    order=[0,1] if case!='swap' else [1,0]
    for t in range(33):
        for rank,i in enumerate(order):
            if case=='missing' and i==1:continue
            start=3+rank*12
            if case=='overlap':start=3
            fraction=float(np.clip((t-start+1)/10,0,1))
            if fraction<=0:continue
            a=int(round(96*fraction));y=28 if i==0 else 88
            x0,x1=(112-a,112) if case=='reverse' and i==0 else (16,16+a)
            frames[t,y-2:y+3,x0:x1]=0
        if case=='extra' and t>=29:frames[t,55:60,40:60]=0
        if case=='disappear' and t>=29:frames[t,24:34]=255
    if case=='flash':frames[1:]=frames[-1];frames[0]=255
    if case=='sparse':frames=frames[[0,-1]]
    if case=='blank':frames[:]=255
    return frames


def render_hanzi(ref, swap=False):
    masks,progress=stroke_geometry(geometry(ref),size=128)
    order=list(range(len(masks)))
    if swap:order[0],order[1]=order[1],order[0]
    boundaries=np.linspace(3,29,len(order)+1)
    frames=np.full((33,128,128,3),255,np.uint8)
    events=[]
    for rank,i in enumerate(order):
        events.append({'instance_id':ref['sequence'][i]['id'],'source':'construction_log_only',
                       'start_frame':float(boundaries[rank]),'end_frame':float(boundaries[rank+1])})
    for t in range(33):
        ink=np.zeros((128,128),bool)
        for rank,i in enumerate(order):
            p=float(np.clip((t-boundaries[rank])/(boundaries[rank+1]-boundaries[rank]-1),0,1))
            if p>0:ink|=masks[i]&(progress[i]<=p)
        frames[t,ink]=0
    return frames,events


def build(destination):
    destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();rows=[];micro_results=[];counter=0
    def add(track,group,prompt,answer,media=None,character=None,qual='programmatic_microtask',permission='G0'):
        nonlocal counter
        counter+=1
        sid='S'+hashlib.sha256(f'{SEED}:{counter}'.encode()).hexdigest()[:12]
        directory=destination/'model_inputs'/sid;directory.mkdir(parents=True)
        payload={'id':sid,'track':track,'prompt':prompt,'geometry_permission':permission,'media':[]}
        media_audit=None
        if media is not None:
            (directory/'media').mkdir()
            if media.ndim==4:
                file=directory/'media'/'visible.mp4';encode(file,media)
                actual,pts=decode(file)
                media_audit=validate_media('native_video',actual,pts,len(media))
                media_audit.update(sha256=sha256(file),source_RGB_sha256=hashlib.sha256(media.tobytes()).hexdigest(),
                    pixel_MAE=float(np.abs(media.astype(float)-actual).mean()),decoded_rgb_event_gold=False)
            else:
                file=directory/'media'/'visible.png';Image.fromarray(media).save(file)
                media_audit={'kind':'static_image','sha256':sha256(file),'size':list(Image.open(file).size)}
            payload['media']=['media/'+file.name]
        validate_input(payload);save(directory/'request.json',payload)
        save(destination/'evaluation_only'/f'{sid}.json',answer)
        row={'id':sid,'track':track,'source_group':group,'split':'development_only','seed':SEED,
             'character':character,'qualification':qual,'formal_gold':False,
             'input':f'model_inputs/{sid}/request.json','evaluation':f'evaluation_only/{sid}.json',
             'geometry_permission':permission,'media_audit':media_audit,'source_revision':'parent d40d7647 + current CPU constructor',
             'source_order_is_normative_truth':False}
        rows.append(row)
        return sid,directory
    for char in CHARACTERS:
        ref=reference(char);group='exposed-hanzi-'+ref['reference_id'];qual=ref['qualification']
        correct,events=render_hanzi(ref);swapped,sevents=render_hanzi(ref,True)
        if not np.array_equal(correct[-1],swapped[-1]):raise AssertionError('Different final RGB')
        final=correct[-1];seq=ref['sequence']
        add('K-CHAR',group,'Identify the single character in this image. Return unknown if unreadable.',
            {'character':char,'qualification':qual},final,qual=qual)
        add('K-ORDER',group,f'For mainland standard simplified Chinese character {char}, describe distinct stroke instances, their relative order and travel directions. State uncertainty.',
            {'character':char,'development_reference':seq,'formal_gold':False},character=char,qual=qual)
        add('V-STRUCT',group,'Describe distinct spatial stroke instances, start/end candidates and relations. Do not infer time order from this static image.',
            {'character':char,'development_geometry':ref['geometry'],'formal_gold':False,'temporal_answer':'not_applicable'},final,qual=qual)
        add('G-GLYPH',group,f'Generate a static standard black glyph of {char} on white.',
            {'character':char,'reference_image_qualification':qual,'formal_gold':False},character=char,qual=qual)
        add('G-STROKE',group,f'Generate one native video of standard character {char}, starting blank, drawing strokes in mainland standard order and directions, preserving all previous ink. Black on white.',
            {'character':char,'development_reference':seq,'formal_gold':False},character=char,qual=qual)
        decoded_pair=[]
        for variant,frames,log in [('canonical',correct,events),('swap',swapped,sevents)]:
            sid,directory=add('H-ACTUAL',group,'Describe only actual visible events and their spatial identities, onset/completion, travel directions and uncertainty. Never replace observed history with standard order.',
                {'variant':variant,'pair_id':group,'intended_normative_program':seq,'construction_events':log,
                 'observed_events':None,'observed_events_status':'requires_independent_pixel_or_human_audit',
                 'formal_gold':False,'same_final_different_history':True},frames,qual=qual)
            decoded,_=decode(directory/'media/visible.mp4');decoded_pair.append(decoded)
            if variant=='canonical':
                save(destination/'training_targets'/f'{sid}.json',{'source_sample':sid,'video':rows[-1]['input'].replace('request.json','media/visible.mp4'),
                     'character':char,'sequence':seq,'qualification':qual,'eligible_for_formal_training':False,
                     'reason':'Development wiring only; complete normative qualification remains missing'})
        if not np.array_equal(decoded_pair[0][-1],decoded_pair[1][-1]):
            raise AssertionError('Same-final history pair differs after actual video decoding')
    cases=('correct','swap','reverse','missing','extra','flash','disappear','sparse','blank','overlap')
    for case in cases:
        frames=render_lines(case)
        sid,directory=add('H-ACTUAL','micro-two-lines','Describe the visible order, spatial identities, directions, completion and any disappearing or extra ink. Report uncertainty.',
            {'case':case,'construction_reference':REFERENCE,'evaluation_regions':REGIONS,'formal_hanzi_gold':False,
             'construction_truth_scope':'non-Hanzi geometric instruction only'},frames)
        actual,pts=decode(directory/'media/visible.mp4');observed=observe_rgb(actual,pts,REGIONS)
        micro_results.append({'id':sid,'case':case,'observation':observed,'facets':judge_execution(observed,REFERENCE),
                              'authority':'CPU development diagnostic; no model prediction'})
    for name,prompt in [('one_line','Grow a horizontal black line from left to right on white.'),
                        ('reverse_line','Grow a horizontal black line from right to left on white.'),
                        ('two_lines','On white, grow an upper horizontal line left to right, then a lower line left to right. Preserve previous ink.'),
                        ('vertical','Grow a vertical black line from top to bottom on white.')]:
        add('G-ATOMIC','micro-'+name,prompt,{'instruction':name,'requires_visible_growth':True})
    for name in ['valid','policy','draw','unattributable']:
        sid,directory=add('X-RECOVERY','micro-two-lines','Inspect the current visible state and explicit proposed action. Diagnose only with evidence. If feasible, propose a same-step replacement; otherwise reject. Do not claim the published past was repaired.',
            {'case':name,'same_step_adapter_required':True,'formal_gold':False},render_lines('missing')[-1])
        payload=json.loads((directory/'request.json').read_text())
        payload['visible_state']={'description':'Upper line present; lower line absent. This is a synthetic action-state microtask.'}
        payload['action']=({'operation':'remove','target':'absent_lower_line'} if name=='policy' else
                           {'operation':'draw','target':'lower_line','direction':'left_to_right'})
        if name=='draw':payload['visible_state']['prior_action']='draw lower line left to right; actual result still upper line only'
        if name=='unattributable':payload.pop('action')
        validate_input(payload);save(directory/'request.json',payload)
    # A frozen order for later model calls; it is not a new independent holdout.
    random.Random(SEED).shuffle(rows)
    validation=validate_manifest(rows)
    (destination/'manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    save(destination/'microtask_pixel_results.json',micro_results)
    summary={'schema':'diagnostic-benchmark-v0.1','status':'development_materialized','seed':SEED,
             'tracks':dict(Counter(r['track'] for r in rows)),**validation,
             'CPU_videos':sum((r['media_audit'] or {}).get('kind')=='native_video' for r in rows),
             'formal_human_metrics':None,'new_model_calls':0,'new_human_tasks':0,
             'cpu_wall_seconds':time.perf_counter()-started,'directory':str(destination.resolve())}
    save(destination/'build_summary.json',summary)
    return summary


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    args=p.parse_args();print(json.dumps(build(args.output),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
