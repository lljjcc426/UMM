"""Train reference coordinates with state replay, then evaluate the fixed final adapter."""
import json
import os
import random
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from h1_reference_localization import localization_prompt, DATA as DEV
from h1_state_gate import ROOT, read_jsonl, write_jsonl, evaluate, DEFAULT
from h1_compare_state_runs import compare
from h1_target_controls import score_different_targets

DATA=ROOT/'data/h1/reference_localization_training_v1'
RESULT=ROOT/'results/h1/showo2_video_1_5b/reference_localization_training_v1'
ADAPTER=ROOT/'checkpoints/h1_reference_localization_v1/adapter.pt'
INITIAL=ROOT/'checkpoints/h1_target_cue_boxed_v1/adapter.pt'


def build():
    DATA.mkdir(parents=True,exist_ok=False)
    (DATA/'images').mkdir()
    RESULT.mkdir(parents=True,exist_ok=False)
    rng=random.Random(10418)
    cases=[]
    inputs=[]
    labels=[]
    for kind in ('parallel_h','parallel_v','cross'):
        for i in range(12):
            x0=rng.randint(30,160);x1=x0+rng.randint(120,230)
            y0=rng.randint(18,65);y1=y0+rng.randint(85,125)
            xm=rng.randint(x0+35,x1-35);ym=rng.randint(y0+25,y1-25)
            if kind=='parallel_h':
                strokes={n:[(x0,y),(x1,y)] for n,y in zip(('上横','中横','下横'),(y0,ym,y1))}
            elif kind=='parallel_v':
                strokes={n:[(x,y0),(x,y1)] for n,x in zip(('左竖','右竖'),(x0,x1))}
            else:
                strokes={'横线':[(x0,ym),(x1,ym)],'竖线':[(xm,y0),(xm,y1)]}
            gid=f'loc-train-{kind}-{i}'
            image=Image.new('RGB',(432,432),'white')
            for pts in strokes.values():ImageDraw.Draw(image).line(pts,fill='black',width=5)
            image_path=f'images/{gid}.png';image.save(DATA/image_path)
            for target,pts in strokes.items():
                xs,ys=zip(*pts);box=[min(xs),min(ys),max(xs),max(ys)];sid=f'{gid}-{target}'
                cases.append(dict(sample_id=sid,group_id=gid,target=target,image=image_path,expected_box=box))
                for repeat in range(4):
                    sample=f'{sid}-repeat-{repeat}'
                    inputs.append(dict(sample_id=sample,case_id=sid,group_id=gid,split='train',layout=kind,
                        view='reference_only',task='localization',wording=0,response_format='json',
                        images=[image_path],prompt=localization_prompt(target)))
                    labels.append(dict(sample_id=sample,response={'box':box}))
    # Reuse the exact successful state replay composition; no development answers.
    source=ROOT/'data/h1/state_target_cue_v1/boxed/train'
    for row in read_jsonl(source/'inputs.jsonl'):
        row['images']=[os.path.relpath(source/p,DATA) for p in row['images']]
        inputs.append(row)
    labels.extend(read_jsonl(source/'labels.jsonl'))
    write_jsonl(DATA/'inputs.jsonl',inputs);write_jsonl(DATA/'labels.jsonl',labels)
    (DATA/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    plan=dict(objective='Teach reference coordinate output while preserving state judgments; H1 prerequisites only.',
        training_geometry_groups=36,unique_localization_targets=84,localization_repeats=4,localization_rows=336,
        visual_state_replay_rows=744,text_replay_rows=512,total_rows=1592,
        train_seed=731,geometry_seed=10418,initial_adapter=str(INITIAL.relative_to(ROOT)),
        configuration=dict(epochs=3,steps=1194,learning_rate=2e-4,accumulation=4,last_layers=8,rank=8,alpha=16),
        output='Same four-coordinate JSON and prompt as the preceding diagnostic; only answer/EOS tokens supervised.',
        input='Reference-only upper-half image and target name for localization; no current-state information.',
        evaluation=['84 unique training localization targets','28 prior development targets with actual image',
                    'same 28 targets with blank image','112 original boxed target development questions',
                    '104 current-only development questions','208 text development questions'],
        policy='Final adapter only; fixed budget, no intermediate selection. Original visual test untouched.',
        limitations='Same synthetic shape families and renderer. Prior dev has been inspected; this is development, not independent acceptance.')
    for p in (DATA/'plan.json',RESULT/'plan.json'):p.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(plan)


def run():
    env=dict(os.environ,PYTORCH_ENABLE_MPS_FALLBACK='1')
    def call(script,*args):
        subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],env=env,cwd=ROOT,check=True)
    call('h1_train_state.py','--data',DATA,'--views','reference_only','reference_current','current_only',
        '--text-replay',ROOT/'data/h1/state_training_v1','--init-adapter',INITIAL,
        '--output',RESULT/'training','--adapter',ADAPTER,'--epochs',3,'--accumulation',4,'--lr',.0002,
        '--eval-policy','Final localization train/dev, blank-image control and state retention; original test unused.')
    for name,data,blank in [('train_localization',DATA,False),('dev_localization',DEV,False),('blank_dev',DEV,True)]:
        call('h1_reference_localization.py','run','--data',data,'--output',RESULT/name,'--adapter',ADAPTER,
             *(['--blank-image'] if blank else []))
    for name,data,view in [('targets_boxed_dev',ROOT/'data/h1/state_target_cue_v1/boxed/all_targets_dev','reference_current'),
                           ('current_dev',DEFAULT,'current_only'),('text_dev',ROOT/'data/h1/state_training_v1','oracle_text')]:
        out=RESULT/name
        call('h1_run_showo.py','--inputs',data/'inputs.jsonl','--split','dev','--view',view,
             '--format','json','--constrain-answers','--adapter',ADAPTER,'--output',out)
        evaluate(data,out/'predictions.jsonl','dev','json',out/'score',view)
        if name=='targets_boxed_dev':
            score_different_targets(data,out,out/'score/different_target_pairs.json')
        compare(data,ROOT/'results/h1/showo2_video_1_5b/target_cue_v1/boxed'/name,out,
                RESULT/f'{name}_vs_initial.json',view,'dev')
    print('LOCALIZATION TRAINING AND FINAL EVALUATIONS COMPLETED',flush=True)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['build','run'])
    args=p.parse_args();{'build':build,'run':run}[args.command]()
