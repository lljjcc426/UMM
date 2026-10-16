"""Reference-only coordinate diagnosis using the full UMM, without candidate boxes."""
from pathlib import Path
import json
import argparse
import random
import time
from datetime import datetime, timezone
from PIL import Image, ImageDraw

from h1_run_showo import (ROOT, load_model, StateImageEncoder, image_prompt_embeds,
                         SOURCE_REVISION, MODEL_REVISION)
from h1_train_state import load_adapter

DATA = ROOT/'data/h1/reference_localization_v1'
RESULT = ROOT/'results/h1/showo2_video_1_5b/reference_localization_v1'


def build():
    DATA.mkdir(parents=True, exist_ok=False)
    (DATA/'images').mkdir()
    rng=random.Random(10417)
    rows=[]
    for kind in ('parallel_h','parallel_v','cross'):
        for i in range(4):
            x0,x1=rng.randint(55,95),rng.randint(325,375)
            y0,y1=rng.randint(30,50),rng.randint(165,190)
            if kind=='parallel_h':
                strokes={name:[(x0,y),(x1,y)] for name,y in zip(('上横','中横','下横'),(y0,(y0+y1)//2,y1))}
            elif kind=='parallel_v':
                strokes={name:[(x,y0),(x,y1)] for name,x in zip(('左竖','右竖'),(x0,x1))}
            else:
                strokes={'横线':[(x0,(y0+y1)//2),(x1,(y0+y1)//2)],
                         '竖线':[((x0+x1)//2,y0),((x0+x1)//2,y1)]}
            gid=f'{kind}-{i}'
            image=Image.new('RGB',(432,432),'white')
            draw=ImageDraw.Draw(image)
            for points in strokes.values():
                draw.line(points,fill='black',width=5)
            path=f'images/{gid}.png'
            image.save(DATA/path)
            for target,points in strokes.items():
                xs,ys=zip(*points)
                rows.append(dict(sample_id=f'{gid}-{target}',group_id=gid,target=target,image=path,
                    expected_box=[min(xs),min(ys),max(xs),max(ys)]))
    (DATA/'cases.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    plan=dict(role='New development geometry; reference-only localization, not independent H1 acceptance.',
        seed=10417,groups=12,targets=len(rows),adapter='checkpoints/h1_target_cue_boxed_v1/adapter.pt',
        input='Complete reference in top 432x216 region; blank lower half. No current state, candidate boxes, labels or target markers.',
        output='Four integer centerline bounds x_min,y_min,x_max,y_max; fixed syntax, all coordinates in canvas range are eligible.',
        scoring='Mean absolute coordinate error; all four coordinates within 12 pixels; invalid box rate; per geometry group.',
        policy='One prompt, one final adapter, no prompt search or training; no original visual test cases.')
    (DATA/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(plan)


def localization_prompt(target):
    return (f'图片大小432×432像素，上半部是完整线条参考，下半部空白。请定位上半部的{target}。'
        '坐标原点为整张图左上角，x向右，y向下。输出这条线中心路径的最小x、最小y、最大x、最大y。'
        '横线的两个y相同，竖线的两个x相同。只输出JSON：{"box":[最小x,最小y,最大x,最大y]}。')


def run(data=DATA, result=RESULT, adapter=ROOT/'checkpoints/h1_target_cue_boxed_v1/adapter.pt', blank=False):
    import torch
    from h1_run_showo import image_prompt_embeds
    result.mkdir(parents=True,exist_ok=False)
    assets=ROOT/'checkpoints/Show-o-assets'
    model,tok,ids=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',assets,'mps')
    config=load_adapter(model,adapter,'mps')
    model.eval().requires_grad_(False)
    encoder=StateImageEncoder(model,assets,'mps')
    from models import omni_attn_mask_naive
    metadata=dict(model='showlab/show-o2-1.5B-w-video-und',model_revision=MODEL_REVISION,
        source_revision=SOURCE_REVISION,adapter_config=config,device='MPS bf16; VAE CPU fp32',
        adapter=str(adapter.relative_to(ROOT)),blank_image=blank,
        started_utc=datetime.now(timezone.utc).isoformat(),plan=json.loads((data/'plan.json').read_text()),
        decoding='Greedy token trie over all in-range integer coordinates; fixed JSON punctuation. No candidate boxes or label access.')
    (result/'run.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    rows=json.loads((data/'cases.json').read_text())
    inputs=[{k:v for k,v in r.items() if k!='expected_box'} for r in rows]
    (result/'inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    with torch.inference_mode(),(result/'predictions.jsonl').open('w') as out:
        for row in inputs:
            prompt=localization_prompt(row['target'])
            start=time.perf_counter()
            emb,mods=image_prompt_embeds(model,tok,ids,prompt,encoder.encode(None if blank else data/row['image']),'mps')
            generated=[]
            def append(token):
                nonlocal emb
                generated.append(token)
                emb=torch.cat((emb,model.showo.model.embed_tokens(torch.tensor([[token]],device='mps'))),dim=1)
            for token in tok('{"box":[',add_special_tokens=False).input_ids:
                append(token)
            for axis,limit in enumerate((432,216,432,216)):
                suffix=',' if axis<3 else ']}'
                candidates=[tok(str(n)+suffix,add_special_tokens=False).input_ids for n in range(limit)]
                while candidates and candidates[0]:
                    allowed=sorted({seq[0] for seq in candidates})
                    if len(allowed)==1:
                        token=allowed[0]
                    else:
                        mask=omni_attn_mask_naive(B=1,LEN=emb.shape[1],modalities=mods,device='mps',inverted=True).to(emb.dtype)
                        logits=model.showo(inputs_embeds=emb,attention_mask=mask,use_cache=False,num_logits_to_keep=1)['logits'][0,-1]
                        token=allowed[logits[allowed].argmax().item()]
                    append(token)
                    candidates=[seq[1:] for seq in candidates if seq[0]==token]
            answer=tok.decode(generated,skip_special_tokens=True)
            out.write(json.dumps(dict(sample_id=row['sample_id'],prompt=prompt,raw_response=answer,seconds=time.perf_counter()-start),ensure_ascii=False)+'\n')
            out.flush()
    metadata['finished_utc']=datetime.now(timezone.utc).isoformat()
    (result/'run.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    score(data,result)


def score(data=DATA, result=RESULT):
    from collections import defaultdict
    from h1_state_gate import interval
    rows=json.loads((data/'cases.json').read_text())
    predictions={r['sample_id']:r for r in map(json.loads,(result/'predictions.jsonl').read_text().splitlines())}
    scored=[]
    groups=defaultdict(list)
    for row in rows:
        box=json.loads(predictions[row['sample_id']]['raw_response'])['box']
        error=[abs(a-b) for a,b in zip(box,row['expected_box'])]
        valid=box[0]<=box[2] and box[1]<=box[3]
        hit=valid and max(error)<=12
        groups[row['group_id']].append(int(hit))
        scored.append(dict(**row,predicted_box=box,coordinate_errors=error,valid=valid,within_12px=hit))
    report=dict(targets=len(scored),geometry_groups=len(groups),within_12px=sum(r['within_12px'] for r in scored),
        invalid_boxes=sum(not r['valid'] for r in scored),mean_absolute_coordinate_error=sum(sum(r['coordinate_errors']) for r in scored)/(4*len(scored)),
        cluster_bootstrap_95=interval(groups),cases=scored)
    (result/'score.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in report.items() if k!='cases'})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['build','run','score'])
    p.add_argument('--data',type=Path,default=DATA)
    p.add_argument('--output',type=Path,default=RESULT)
    p.add_argument('--adapter',type=Path,default=ROOT/'checkpoints/h1_target_cue_boxed_v1/adapter.pt')
    p.add_argument('--blank-image',action='store_true')
    args=p.parse_args()
    if args.command=='build': build()
    elif args.command=='run': run(args.data,args.output,args.adapter,args.blank_image)
    else: score(args.data,args.output)
