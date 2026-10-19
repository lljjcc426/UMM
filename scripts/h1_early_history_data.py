"""T6 fixed 24-observation D0 histories. Generation logs are labels only."""
import argparse, copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from h1_event_data import ROOT, draw, save, write_video
from h1_event_observe import decode, masks_for, pixel_observer
DATA=ROOT/'data/h1/early_history_v1'
OUT=ROOT/'results/h1/early_history_v1'
WEIGHTS=ROOT/'checkpoints/h1_early_history_v1'
DECISIONS=[15,20,23]
FAMILIES=['parallel','mixed','cross','fold','close']

def geometry(family,rng,q=5):
    if q==3:
        return [[[int(rng.integers(65,115)),int(y)],[int(rng.integers(300,365)),int(y)]] for y in sorted(rng.integers([85,195,305],[120,230,340]))]
    if family in ['parallel','close']:
        ys=[70,140,210,280,350] if family=='parallel' else [140,174,208,242,276]
        return [[[int(rng.integers(65,115)),int(y+rng.integers(-5,6))],[int(rng.integers(305,365)),0]] for y in ys]
    bases={
      'mixed':[[[75,75],[180,75]],[[260,65],[260,170]],[[70,210],[185,210]],[[320,210],[320,345]],[[65,350],[215,350]]],
      'cross':[[[65,105],[230,105]],[[150,55],[150,220]],[[265,75],[365,175]],[[65,310],[225,310]],[[310,230],[310,370]]],
      'fold':[[[65,65],[180,65],[180,155]],[[265,65],[365,65]],[[65,215],[175,215]],[[275,175],[355,175],[355,270]],[[65,345],[245,345]]]
    }
    # One independent translation per stroke; shared junctions within a stroke remain intact.
    return [[[x+int(dx),y+int(dy)] for x,y in s] for s in bases[family] for dx,dy in [rng.integers(-14,15,2)]]

def timeline(q,variant):
    order=list(range(q))
    if variant in ['swap1','mergedB']:order[0],order[1]=order[1],order[0]
    if variant=='swap2':order[1],order[2]=order[2],order[1]
    source=np.zeros((93,q),float)
    if variant.startswith('merged'):
        # Both finish before sampled source frame 4; the unseen source order differs.
        source[1:,order[0]]=1;source[2:,order[1]]=1
        early=[2] if q==5 else []
        starts=[20] if q==5 else []
    else:
        early=order[:3] if q==5 else order[:2];starts=[4,12,20][:len(early)]
    for j,start in zip(early,starts):
        source[start:,j]=.5;source[start+4:,j]=1
    if q==5:remaining=[(3,56),(4,80)]
    else:remaining=[(2,56)]
    for j,start in remaining:
        for offset,p in [(0,.25),(4,.5),(8,.75),(12,1.)]:source[start+offset:,j]=p
    return source.tolist(),order

def query(strokes):
    kinds=[];hints=[]
    for points in strokes:
        a,b=points[0],points[-1]
        kinds.append(3 if len(points)>2 else 1 if a[1]==b[1] else 2 if a[0]==b[0] else 4)
        hints.append((np.round(np.mean(points,0)/432*4)/4*2-1).tolist())
    return dict(instance_ids=list(range(len(strokes))),kinds=kinds,hints=hints)

def observed_truth(row,frames):
    o=pixel_observer(row,frames);onsets={j:next(i for i,p in enumerate(o['progress']) if p[j]>.02) for j in o['observed_ids']}
    groups={t:[j for j,v in onsets.items() if v==t] for t in sorted(set(onsets.values()))}
    precedence=[[a,b] for a,ta in onsets.items() for b,tb in onsets.items() if ta<tb]
    unresolved=[g for t,g in groups.items() if len(g)>1 or t==0]
    return dict(event_order=o['event_order'],observed_ids=o['observed_ids'],progress=o['progress'][-1],direction=o['direction'],
       onset_intervals={str(j):[max(0,t-1),t] for j,t in onsets.items()},confirmed_precedence=precedence,unresolved_order_groups=unresolved,
       uncertainty_reason='merged_onset_interval' if unresolved else None)

def build():
    if (DATA/'cases.json').exists():raise FileExistsError('Fixed data already exists')
    rng=np.random.default_rng(20261019);rows=[];splits={}
    for split,count in [('train',20),('dev',8),('test',20),('diagnostic',2)]:
        splits[split]=[]
        for i in range(count):
            family=FAMILIES[i%5] if split!='diagnostic' else 'san';q=3 if split=='diagnostic' else 5
            strokes=geometry(family,rng,q)
            if family in ['parallel','close']:
                for s in strokes:s[-1][1]=s[0][1]
            group=f'{split}-{i:02d}-{family}';splits[split].append(group);folder=DATA/group;folder.mkdir(parents=True)
            ref=folder/'reference.png';draw(strokes,[1.]*q).save(ref)
            for variant in ['correct','swap1','swap2','mergedA','mergedB'] if q==5 else ['correct','swap1','mergedA','mergedB']:
                progress,order=timeline(q,variant);video=folder/(variant+'.mp4')
                images=[draw(strokes,p) for p in progress];write_video(video,images)
                indices=list(range(0,93,4));paths=[]
                for t,index in enumerate(indices):
                    path=folder/f'{variant}-{t:02d}.png';images[index].save(path);paths.append(str(path.relative_to(ROOT)))
                rows.append(dict(id=group+'-'+variant,group=group,family=family,split=split,variant=variant,target='三' if q==3 else family+' five-stroke structure',
                    strokes=strokes,width=13,query=query(strokes),reference=str(ref.relative_to(ROOT)),frames=paths,video=str(video.relative_to(ROOT)),indices=indices,timestamps=[v/24 for v in indices],fps=24,total_frames=93,
                    label_progress=[progress[k] for k in indices],label_source_order=order,common_suffix_start=6 if q==5 else 4,decisions=DECISIONS))
    save(DATA/'cases.json',rows);save(OUT/'splits.json',splits)
    (DATA/'README.md').write_text('''# T6固定早期历史数据\n\n原创D0几何，允许本项目复用。20训练／8开发／20锁定测试几何组，每组正常、两种换序、两个全输入相同的合并事件源视频；另有2组三笔“三”诊断。所有衍生样本随几何划分。无真实字形、字体、手部或艺术风格泛化证据。\n\n源视频432×432、24fps、93帧、无损RGB；固定每4帧观察，共24帧。正常前3笔先后独立出现，共同后缀从第6观察开始，最后两笔在第14／20观察开始。评价第15、20、23观察。变体、源日志和真实区域仅用于标注、oracle与评分；主模型输入仅参考RGB、实际观察RGB、规范ID／类型／粗位置与实际时间戳。\n\nmergedA/B的源先后不同，全部24个实际观察相同；保留可确定的后续关系，完整顺序为null。三笔诊断单列，不进入训练或主20组统计。\n''')

def contracts():
    rows=json.loads((DATA/'cases.json').read_text());checks=[];oracle=[]
    for group in sorted({r['group'] for r in rows}):
        group_rows=[r for r in rows if r['group']==group];by={r['variant']:r for r in group_rows};arrays={r['variant']:[np.asarray(Image.open(ROOT/p)) for p in r['frames']] for r in group_rows}
        # Decode each source once, prove the saved model observations are real lossless samples.
        decoded={}
        for r in group_rows:
            d,fps=decode(ROOT/r['video']);decoded[r['variant']]=fps==24 and all(np.array_equal(d[i],f) for i,f in zip(r['indices'],arrays[r['variant']]))
            for t in range(24):oracle.append(dict(id=r['id'],group=group,split=r['split'],t=t,state=observed_truth(r,[Image.fromarray(v) for v in arrays[r['variant']][:t+1]])))
        for name in ['swap1','swap2'] if len(group_rows)==5 else ['swap1']:
            a,b=by['correct'],by[name];fa,fb=arrays['correct'],arrays[name];first=next(t for t,(x,y) in enumerate(zip(fa,fb)) if not np.array_equal(x,y))
            entry=dict(group=group,pair=['correct',name],source_orders=[a['label_source_order'],b['label_source_order']],first_visible_difference=first,common_suffix_start=a['common_suffix_start'],
                sampled_indices=a['indices'],timestamps=a['timestamps'],same_target=a['target']==b['target'],same_reference=Image.open(ROOT/a['reference']).tobytes()==Image.open(ROOT/b['reference']).tobytes(),same_query=a['query']==b['query'],same_timestamps=a['timestamps']==b['timestamps'],decoded_exact=all(decoded.values()),decisions=[])
            for t in DECISIONS:
                hashes=[[hashlib.sha256(v.tobytes()).hexdigest() for v in f[t-7:t+1]] for f in [fa,fb]]
                entry['decisions'].append(dict(t=t,hashes_recent8=hashes,final_rgb_hashes=[hashlib.sha256(f[-1].tobytes()).hexdigest() for f in [fa,fb]],
                    recent8_and_predecessor_equal=all(np.array_equal(x,y) for x,y in zip(fa[t-8:t+1],fb[t-8:t+1])),
                    early_history_recoverable=all(observed_truth(r,[Image.fromarray(v) for v in arrays[r['variant']][:t+1]])['event_order']==r['label_source_order'] for r in [a,b]),
                    history_distance_seconds=[a['timestamps'][t]-a['timestamps'][1],a['timestamps'][t]-a['timestamps'][3]]))
            entry['pass']=all(entry[k] for k in ['same_target','same_reference','same_query','same_timestamps','decoded_exact']) and all(d['recent8_and_predecessor_equal'] and d['early_history_recoverable'] for d in entry['decisions']);checks.append(entry)
        ma,mb=arrays['mergedA'],arrays['mergedB'];s=observed_truth(by['mergedA'],[Image.fromarray(v) for v in ma]);assert all(np.array_equal(a,b) for a,b in zip(ma,mb));assert s['event_order'] is None and s['unresolved_order_groups']==[[0,1]] and len(s['confirmed_precedence'])>0
    save(OUT/'pixel_states.json',oracle)
    result=dict(passed=all(e['pass'] for e in checks),pairs=checks,unknown_full_sequence_pairs=len({r['group'] for r in rows}),locked_test_pairs=sum(r['split']=='test' and not r['variant'].startswith('merged') and r['variant']!='correct' for r in rows),feature_equality='pending frozen feature cache in T6-2')
    save(OUT/'data_contract_checks.json',result)
    if not result['passed']:raise RuntimeError('Data contract failed; training forbidden')
    print(json.dumps({k:v for k,v in result.items() if k!='pairs'}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['build','contracts']);a=p.parse_args();globals()[a.stage]()
