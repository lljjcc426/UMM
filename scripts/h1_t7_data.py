"""Independent T7 D0 geometries and observation-grounded contracts."""
import argparse,json
import numpy as np
from PIL import Image
from h1_event_data import ROOT,draw,save,write_video
from h1_event_observe import masks_for,pixel_observer,decode
from h1_early_history_data import timeline,query

DATA=ROOT/'data/h1/instance_onset_v1'
OUT=ROOT/'results/h1/instance_onset_v1'
WEIGHTS=ROOT/'checkpoints/h1_instance_onset_v1'
DECISIONS=[15,20,23]
FAMILIES=['parallel','close','cross','fold','mixed']

def rows():return json.loads((DATA/'cases.json').read_text())

def geometry(family,q,rng,vertical):
    if family in ['parallel','close']:
        ys=np.linspace(65,365,q) if family=='parallel' else 216+(np.arange(q)-(q-1)/2)*28
        strokes=[[[int(rng.integers(60,105)),int(y+rng.integers(-3,4))],[int(rng.integers(320,373)),0]] for y in ys]
        for s in strokes:s[1][1]=s[0][1]
    else:
        bases={
            'cross':[[[65,110],[345,110]],[[155,55],[155,365]],[[65,325],[345,325]],[[305,60],[305,370]],[[60,220],[370,220]]],
            'fold':[[[65,75],[190,75],[190,190]],[[270,65],[370,65],[370,175]],[[65,215],[175,215],[175,340]],[[260,215],[365,215]],[[245,320],[360,365]]],
            'mixed':[[[60,85],[180,85]],[[270,55],[270,185]],[[60,295],[180,295]],[[315,210],[365,260]],[[65,345],[190,345],[190,385]]]
        }
        strokes=[[[x+int(dx),y+int(dy)] for x,y in s] for s in bases[family][:q] for dx,dy in [rng.integers(-10,11,2)]]
    if vertical:strokes=[[[y,x] for x,y in s] for s in strokes]
    return strokes

def observation_states(row,frames):
    """Unique pixels measure visible events; training masks retain all shared pixels."""
    observed=pixel_observer(row,frames);progress=np.array(observed['progress']);masks=masks_for(row)
    exclusive=masks&(masks.sum(0)==1);ink=np.stack([np.asarray(f)[:,:,0]<128 for f in frames]);endpoint_times=[]
    for j,points in enumerate(row['strokes']):
        times=[]
        for x,y in [points[0],points[-1]]:
            region=np.zeros_like(masks[j]);region[max(0,y-8):y+9,max(0,x-8):x+9]=True;region&=exclusive[j]
            times.append(next((t for t,f in enumerate(ink) if (f&region).any()),-1))
        endpoint_times.append(times)
    states=[]
    for t in range(len(frames)):
        onset={j:next(k for k in range(t+1) if progress[k,j]>.02) for j in range(len(masks)) if (progress[:t+1,j]>.02).any()}
        groups=[sorted(j for j,v in onset.items() if v==k) for k in sorted(set(onset.values()))]
        unresolved=[g for g in groups if len(g)>1 or onset[g[0]]==0]
        direction=[]
        for a,b in endpoint_times:
            a=a if 0<=a<=t else -1;b=b if 0<=b<=t else -1
            direction.append('unknown' if a==b else 'forward' if a>=0 and (b<0 or a<b) else 'reverse')
        states.append(dict(event_order=None if unresolved else sorted(onset,key=onset.get),observed_ids=sorted(onset),progress=progress[t].tolist(),direction=direction,
            onset_intervals={str(j):[max(0,k-1),k] for j,k in onset.items()},confirmed_precedence=[[a,b] for a in onset for b in onset if onset[a]<onset[b]],
            unresolved_order_groups=unresolved,uncertainty_reason='merged_onset_interval' if unresolved else None))
    return states

def build():
    if (DATA/'cases.json').exists():raise FileExistsError('T7 geometry already fixed')
    rng=np.random.default_rng(2026101907);cases=[];splits={};logs=[]
    for split,count in [('train',4),('dev',2),('test',3)]:
        splits[split]=[]
        for family in FAMILIES:
            for q in [3,5]:
                for i in range(count):
                    group=f'{split}-{family}-q{q}-{i:02d}';splits[split].append(group)
                    strokes=geometry(family,q,rng,i%2==1);folder=DATA/group;folder.mkdir(parents=True)
                    reference=folder/'reference.png';draw(strokes,[1.]*q).save(reference)
                    for variant in ['correct','swap1']+(['swap2'] if q==5 else [])+['mergedA','mergedB']:
                        source,order=timeline(q,variant);images=[draw(strokes,p) for p in source];video=folder/(variant+'.mp4');write_video(video,images)
                        indices=list(range(0,93,4));paths=[]
                        for t,k in enumerate(indices):
                            p=folder/f'{variant}-{t:02d}.png';images[k].save(p);paths.append(str(p.relative_to(ROOT)))
                        cases.append(dict(id=group+'-'+variant,group=group,split=split,family=family,variant=variant,target=f'{family} {q}-stroke D0 geometry',strokes=strokes,width=13,
                            query=query(strokes),reference=str(reference.relative_to(ROOT)),frames=paths,video=str(video.relative_to(ROOT)),indices=indices,timestamps=[k/24 for k in indices],fps=24,total_frames=93,
                            label_progress=[source[k] for k in indices],label_source_order=order,decisions=DECISIONS))
                        logs.append(dict(id=group+'-'+variant,scope='labels and oracle only',source_progress=source,source_order=order))
    save(DATA/'cases.json',cases);save(DATA/'event_logs.json',logs);save(OUT/'splits.json',splits)

def contracts():
    cases=rows();checks=[];pixels=[];unique=set();old=json.loads((ROOT/'data/h1/early_history_v1/cases.json').read_text())
    old_geometry={json.dumps(r['strokes']) for r in old}
    for group in sorted({r['group'] for r in cases}):
        rs=[r for r in cases if r['group']==group];by={r['variant']:r for r in rs};key=json.dumps(rs[0]['strokes'])
        assert key not in unique and key not in old_geometry;unique.add(key)
        arrays={};states={};decoded_exact=True
        for r in rs:
            frames=[Image.open(ROOT/p).convert('RGB') for p in r['frames']];arrays[r['variant']]=[np.asarray(f) for f in frames]
            actual,fps=decode(ROOT/r['video']);decoded_exact &= fps==24 and all(np.array_equal(actual[k],f) for k,f in zip(r['indices'],arrays[r['variant']]))
            states[r['variant']]=observation_states(r,frames)
            for t,s in enumerate(states[r['variant']]):
                visible=[j for j,p in enumerate(r['label_progress'][t]) if p>0]
                expected=None if r['variant'].startswith('merged') and t>0 else [j for j in r['label_source_order'] if j in visible]
                assert s['event_order']==expected,(r['id'],t,s['event_order'],expected)
                assert s['observed_ids']==visible
                pixels.append(dict(id=r['id'],group=group,split=r['split'],t=t,state=s))
        a=arrays['correct'];masks=masks_for(rs[0]);shared=int((masks.sum(0)>1).sum())
        assert rs[0]['query']['instance_ids']==list(range(len(masks)))
        for variant in ['swap1']+(['swap2'] if len(masks)==5 else []):
            b=arrays[variant];assert np.array_equal(a[-1],b[-1])
            assert all(np.array_equal(x,y) for t in DECISIONS for x,y in zip(a[t-8:t+1],b[t-8:t+1]))
        assert all(np.array_equal(x,y) for x,y in zip(arrays['mergedA'],arrays['mergedB']))
        assert states['mergedA'][-1]['unresolved_order_groups']==[[0,1]]
        checks.append(dict(group=group,split=rs[0]['split'],q=len(masks),family=rs[0]['family'],decoded_exact=bool(decoded_exact),onset_visible=True,unique_ids=True,
            final_rgb_equal=True,recent8_with_predecessor_equal=True,merged_input_equal=True,shared_pixels=shared,multi_membership_preserved=True,source_disjoint=True))
    assert all(c['decoded_exact'] for c in checks)
    save(OUT/'pixel_states.json',pixels)
    save(OUT/'data_contract_checks.json',dict(pixel_gate=True,feature_gate=False,training_permitted=False,groups=len(unique),clips=len(cases),observations=len(pixels),checks=checks))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['build','contracts']);args=p.parse_args();globals()[args.stage]()
