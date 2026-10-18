"""T4: one fixed study, independent D0 geometry groups, matched head budgets."""
import argparse,copy,json,time
import numpy as np
import torch
from PIL import Image
from h1_event_data import ROOT,DATA,RESULT,geometry,sequence,draw,write_video,save
from h1_event_observe import CACHE
STUDY=DATA/'study';OUT=RESULT/'T4'

def fresh_geometry(kind,rng):
    points=copy.deepcopy(geometry(kind))
    if kind=='san':
        return [[[int(rng.integers(65,135)),int(y+rng.integers(-15,16))],[int(rng.integers(300,365)),0]] for y in [108,216,324]]
    if kind=='parallel_v':
        return [[[int(x+rng.integers(-20,21)),int(rng.integers(65,110))],[0,int(rng.integers(320,370))]] for x in [120,290]]
    if kind=='cross':
        x=int(rng.integers(175,255));y=int(rng.integers(175,255));return [[[int(rng.integers(65,110)),y],[int(rng.integers(320,370)),y]],[[x,int(rng.integers(65,110))],[x,int(rng.integers(320,370))]]]
    if kind=='fold':
        x=int(rng.integers(280,355));y=int(rng.integers(75,135));return [[[int(rng.integers(65,125)),y],[x,y],[x,int(rng.integers(300,365))]],[[int(rng.integers(65,125)),int(rng.integers(185,245))],[int(rng.integers(220,265)),0]]]
    return [[[int(x+rng.integers(-25,26)),int(y+rng.integers(-25,26))] for x,y in s] for s in points]

def build():
    OUT.mkdir(parents=True,exist_ok=True);STUDY.mkdir(parents=True,exist_ok=True);rows=[];rng=np.random.default_rng(20261018)
    old=json.loads((DATA/'probe.json').read_text());kinds=['san','cross','parallel_v','fold','diagonal']
    for kind in kinds:
        for oldrow in [r for r in old if r['group']==kind]:
            row=copy.deepcopy(oldrow);row.update(id=kind+'-train0-'+row['variant'],group=kind+'-train0',family=kind,split='train');rows.append(row)
        for split in ['train','dev','test']:
            strokes=fresh_geometry(kind,rng)
            if kind=='san':
                for s in strokes:s[1][1]=s[0][1]
            if kind=='parallel_v':
                for s in strokes:s[1][0]=s[0][0]
            if kind=='fold':strokes[1][1][1]=strokes[1][0][1]
            group=kind+'-'+split+'1';folder=STUDY/group;folder.mkdir(parents=True,exist_ok=True)
            ref=folder/'reference.png';draw(strokes,[1.]*len(strokes)).save(ref)
            for variant in ['correct','swap','reverse','half','early','short']:
                timeline,reverse=sequence(strokes,variant);images=[draw(strokes,p,reverse=reverse) for p in timeline]
                video=folder/(variant+'.mp4');write_video(video,images);indices=np.linspace(0,len(images)-1,8,dtype=int).tolist();paths=[]
                for i in indices:
                    p=folder/f'{variant}-{i:02d}.png';images[i].save(p);paths.append(str(p.relative_to(ROOT)))
                row=dict(id=group+'-'+variant,group=group,family=kind,split=split,variant=variant,strokes=strokes,width=13,video=str(video.relative_to(ROOT)),reference=str(ref.relative_to(ROOT)),frames=paths,
                    indices=indices,fps=24,total_frames=len(images),label_progress=[timeline[i] for i in indices],label_direction=['reverse' if j==reverse else 'forward' for j in range(len(strokes))],
                    label_order=[1,0]+list(range(2,len(strokes))) if variant=='swap' else [0] if variant=='half' else list(range(len(strokes))),history_observable=variant!='short',pen_lift_evidence='unknown')
                rows.append(row)
    save(STUDY/'cases.json',rows)
    save(OUT/'preregistration.json',dict(question='Does causal temporal reading improve actual events over matched pointwise reading on held geometry?',seed=42,data_seed=20261018,
        groups={'train':10,'dev':5,'test':5},clips={'train':60,'dev':30,'test':30},same_final_test_pairs=5,
        scope='D0 mechanism only; independent sampled coordinate trajectories within known primitive families, one renderer, no held fonts or character-disjoint H1 acceptance',
        split_policy='All variants/prefixes of each base coordinate trajectory remain in one split. Old T2 probe geometries reused only as train0.',
        queries='Normative instance index/type + template-derived center quantized to quarter canvas; no exact mask or actual event log at inference; fully autonomous hint-free grounding not tested',
        conditions=['B0 RGB+oracle','B1_lastframe_head','B3_pointwise_same_event_inputs','B4_causal','B4_oracle_matched','B4_no_delta','B4_whole_pool','B4_no_progress','B4_time_shuffle_eval'],
        spatial=dict(epochs_max=12,patience=3,lr=.001,batch=8,weight_decay=.01,loss='mask BCE+Dice + change BCE+Dice + 0.1 instance confidence BCE to detached soft IoU; fixes T3 untrained confidence, common to all heads'),
        temporal=dict(epochs_max=12,patience=3,lr=.001,batch=8,weight_decay=.01,loss='event +0.5pair-order+0.5SmoothL1',selection='min dev loss, each condition independently',budget='same sequence/decision exposures and seed; heads ~1.1M parameters',decisions='prefixes of 4,5,6,7,8 observed frames'),
        shuffle='At each decision shuffle only available interior frames, preserve blank first and current last; recompute visual and RGB deltas; reset slot timestamps; same original task labels',
        primary='strict actual event order and same-final pair-both correct; report CI by 5 geometry groups; no H1 acceptance on D0',
        stops='If clean RGB fails: stop train. If spatial cannot fit: stop temporal. No rank/lr/prompt search, no added epochs, no Stage3. After one group report T5.'))
    print('Saved fixed study',len(rows),'clips')

def extract():
    from h1_run_showo import load_model,StateImageEncoder
    original=json.loads((RESULT/'T2_feature_manifest.json').read_text());rows=json.loads((STUDY/'cases.json').read_text());paths=original['paths'].copy();mapping=original['index'].copy();lookup={Image.open(ROOT/p).tobytes():i for i,p in enumerate(paths)}
    for row in rows:
        for p in [row['reference']]+row['frames']:
            key=Image.open(ROOT/p).tobytes()
            if key not in lookup:lookup[key]=len(paths);paths.append(p)
            mapping[p]=lookup[key]
    save(OUT/'feature_manifest.json',dict(paths=paths,index=mapping));features=list(torch.load(CACHE/'probe_features.pt',weights_only=True)['features'].unbind());start=time.perf_counter()
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','cpu');encoder=StateImageEncoder(model,ROOT/'checkpoints/Show-o-assets','mps')
    with (CACHE/'study_progress.jsonl').open('w') as log:
        for i in range(len(features),len(paths)):
            features.append(encoder.encode(ROOT/paths[i]).squeeze(0).cpu());encoder.cache.clear();log.write(json.dumps(dict(completed=i+1,total=len(paths),seconds=time.perf_counter()-start))+'\n');log.flush()
    torch.save(dict(features=torch.stack(features)),CACHE/'study_features.pt');save(OUT/'extraction.json',dict(images=len(paths),reused=len(original['paths']),new=len(paths)-len(original['paths']),seconds=time.perf_counter()-start,shape=list(torch.stack(features).shape),umm_updated_parameters=0))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['build','extract']);args=p.parse_args();{'build':build,'extract':extract}[args.stage]()
