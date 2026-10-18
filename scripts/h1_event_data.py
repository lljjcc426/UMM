"""D0 cumulative-ink videos; logs are labels, never model inputs."""
import argparse, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/h1/event_v3'
RESULT=ROOT/'results/h1/event_v3'

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def partial(points,fraction):
    lengths=[math.dist(a,b) for a,b in zip(points,points[1:])];remaining=sum(lengths)*fraction;out=[points[0]]
    for a,b,length in zip(points,points[1:],lengths):
        if remaining<=0:break
        scale=min(1,remaining/length);out.append([a[k]+(b[k]-a[k])*scale for k in range(2)]);remaining-=length
        if scale<1:break
    return out

def draw(strokes,progress,width=13,reverse=None):
    image=Image.new('RGB',(432,432),'white');p=ImageDraw.Draw(image)
    for j,(points,f) in enumerate(zip(strokes,progress)):
        if f<=0:continue
        pts=partial(points[::-1] if reverse==j else points,f)
        p.line([tuple(x) for x in pts],fill='black',width=width,joint='curve')
    return image

def geometry(kind,variant=0):
    base={
        'san':[[[100,110],[330,110]],[[120,216],[310,216]],[[80,322],[350,322]]],
        'cross':[[[80,216],[352,216]],[[216,80],[216,352]]],
        'parallel_v':[[[125,85],[125,345]],[[290,85],[290,345]]],
        'fold':[[[95,105],[330,105],[330,320]],[[95,215],[245,215]]],
        'diagonal':[[[95,95],[335,335]],[[330,100],[100,330]]],
    }[kind]
    dx=[0,-17,13,5][variant];dy=[0,11,-15,-8][variant]
    scale=[1,.92,.88,1.05][variant]
    return [[[round((x-216)*scale+216+dx),round((y-216)*scale+216+dy)] for x,y in s] for s in base]

def sequence(strokes,variant):
    n=len(strokes);order=list(range(n));reverse=None
    if variant=='swap':order[0],order[1]=order[1],order[0]
    if variant=='reverse':reverse=0
    steps=16;timeline=[];events=[];state=[0.]*n
    timeline.append(state.copy())
    for k,j in enumerate(order):
        limit=.5 if variant in ('half','early') and k==0 else 1.
        if variant=='half' and k>0:break
        for a in range(1,steps+1):
            state[j]=min(limit,a/steps);timeline.append(state.copy())
        events.append(j)
    # All videos have identical frame count and duration; stopped prefixes hold.
    while len(timeline)<1+n*steps:timeline.append(state.copy())
    if variant=='short':
        # Two whole events in a single observation interval: history is ambiguous.
        timeline=[([0.]*n)]+[([1.,1.]+[0.]*(n-2)) for _ in range(len(timeline)-2)]+[[1.]*n]
    return timeline,reverse

def write_video(path,frames):
    import av
    container=av.open(str(path),'w');stream=container.add_stream('libx264rgb',rate=24)
    stream.width=432;stream.height=432;stream.pix_fmt='rgb24';stream.options={'crf':'0','preset':'ultrafast'}
    for image in frames:
        for packet in stream.encode(av.VideoFrame.from_image(image)):container.mux(packet)
    for packet in stream.encode():container.mux(packet)
    container.close()

def build_probe():
    DATA.mkdir(parents=True,exist_ok=True);rows=[]
    for kind in ['san','cross','parallel_v','fold','diagonal']:
        strokes=geometry(kind);folder=DATA/'probe'/kind;folder.mkdir(parents=True,exist_ok=True)
        ref=folder/'reference.png';draw(strokes,[1.]*len(strokes)).save(ref)
        for variant in ['correct','swap','reverse','half','early','short']:
            timeline,reverse=sequence(strokes,variant);frames=[draw(strokes,p,reverse=reverse) for p in timeline]
            video=folder/(variant+'.mp4');write_video(video,frames)
            indices=np.linspace(0,len(frames)-1,8,dtype=int).tolist();paths=[]
            for i in indices:
                p=folder/f'{variant}-{i:02d}.png';frames[i].save(p);paths.append(str(p.relative_to(ROOT)))
            rows.append(dict(id=kind+'-'+variant,group=kind,variant=variant,strokes=strokes,width=13,
                video=str(video.relative_to(ROOT)),reference=str(ref.relative_to(ROOT)),frames=paths,
                indices=indices,fps=24,total_frames=len(frames),label_progress=[timeline[i] for i in indices],
                label_direction=['reverse' if j==reverse else 'forward' for j in range(len(strokes))],
                label_order=([1,0]+list(range(2,len(strokes)))) if variant=='swap' else list(range(len(strokes))) if variant!='half' else [0],
                history_observable=variant!='short',pen_lift_evidence='unknown'))
    save(DATA/'probe.json',rows)
    save(RESULT/'T2_preregistration.json',dict(question='Are actual events retained by sampling and 14/27 feature representation?',
       cases=len(rows),sampling='8 uniform past frames over the presented prefix; official force_sample=True',
       high_sampling='official 32 indices source audit plus decoded pixel baseline',
       train=False,probe_only=True,stop='If pixel oracle fails clean distinguishable events, stop before training.'))
    (DATA/'README.md').write_text('''# H1-v3 D0事件数据

所有几何由scripts/h1_event_data.py原创构造，允许本项目复用，不含私人数据。probe.json为T2可观察性检查，五类结构、六种过程；不能充作汉字泛化测试。视频24fps、432×432、无损RGB编码；frames保留八个实际输入，完整轨迹与状态日志仅用于监督／评分。参考实例编号由指定规范给出，错误顺序保存在标签中。折笔为一次连续运动。

同终态correct/swap保持最终像素、笔数、风格、总时长一致。short特意把两笔合并进一次观察，历史不可观察；半笔与提前换笔不要求同终态。主条件只有过去帧，事件边界条件须另报oracle。画面没有笔尖或手部，抬笔证据一律unknown。原1—4像素压力数据保持原路径，不在本批扩训。
''')
    print('Saved',len(rows),'probe videos')

if __name__=='__main__':
    argparse.ArgumentParser(description=__doc__).parse_args();build_probe()
