"""No-training observability, upstream video adapter and frozen feature probes."""
import argparse,ast,json,time
from pathlib import Path
import numpy as np
from PIL import Image
from h1_event_data import ROOT,DATA,RESULT,draw,save
CACHE=ROOT/'checkpoints/h1_event_v3'

def decode(path):
    import av
    with av.open(str(path)) as c:
        fps=float(c.streams.video[0].average_rate);frames=[f.to_ndarray(format='rgb24') for f in c.decode(video=0)]
    return frames,fps

class VideoReaderAV:
    """Only decord calls used by the original load_video; no sampling rewrite."""
    def __init__(self,path,ctx=None,num_threads=1):self.frames,self.fps=decode(path)
    def __len__(self):return len(self.frames)
    def get_avg_fps(self):return self.fps
    def get_batch(self,indices):
        class Batch:
            def asnumpy(s):return np.stack([self.frames[i] for i in indices])
        return Batch()

def official_load_video(path,n):
    source=ROOT/'checkpoints/Show-o-source/show-o2/utils.py'
    node=next(x for x in ast.parse(source.read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='load_video')
    namespace=dict(np=np,Image=Image,VideoReader=VideoReaderAV,cpu=lambda x:x)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),namespace)
    return namespace['load_video'](str(path),n,fps=1,force_sample=True)

def masks_for(row):
    n=len(row['strokes']);masks=[]
    for j in range(n):
        p=[0.]*n;p[j]=1.;masks.append(np.asarray(draw(row['strokes'],p,width=row['width']))[:,:,0]<128)
    return np.stack(masks)

def pixel_observer(row,frames):
    masks=masks_for(row);exclusive=masks & (masks.sum(0)==1)
    ink=np.stack([np.asarray(f)[:,:,0]<128 for f in frames])
    progress=np.array([[(frame&m).sum()/max(1,m.sum()) for m in exclusive] for frame in ink])
    onsets=[next((i for i,v in enumerate(progress[:,j]) if v>.02),-1) for j in range(len(masks))]
    seen=[j for j,t in enumerate(onsets) if t>=0];unknown=len(set(onsets[j] for j in seen))!=len(seen) or any(onsets[j]==0 for j in seen)
    order=sorted(seen,key=lambda j:onsets[j]) if not unknown else None
    directions=[]
    for j,points in enumerate(row['strokes']):
        times=[]
        for x,y in (points[0],points[-1]):
            region=np.zeros_like(masks[j]);region[max(0,y-8):y+9,max(0,x-8):x+9]=True
            region &= exclusive[j];times.append(next((i for i,v in enumerate(ink) if (v&region).any()),-1))
        directions.append('unknown' if times[0]==times[1] else 'forward' if times[0]>=0 and (times[1]<0 or times[0]<times[1]) else 'reverse')
    new=ink & ~np.concatenate([np.zeros_like(ink[:1]),ink[:-1]],axis=0)
    return dict(event_order=order,unknown=unknown,observed_ids=seen,progress=progress.tolist(),direction=directions,
                pen_lift_evidence='unknown',new_pixels=new.sum((1,2)).tolist())

def pixels():
    rows=json.loads((DATA/'probe.json').read_text());out=[];sampling=[]
    for row in rows:
        decoded,fps=decode(ROOT/row['video']);frames,ts,duration=official_load_video(ROOT/row['video'],8)
        exact=all(np.array_equal(np.asarray(f),decoded[i]) for f,i in zip(frames,row['indices']))
        saved=all(np.array_equal(np.asarray(f),np.asarray(Image.open(ROOT/p))) for f,p in zip(frames,row['frames']))
        for n in [8,32]:
            actual,_,_=official_load_video(ROOT/row['video'],n);pred=pixel_observer(row,actual)
            truth=row['label_order'];order_ok=pred['event_order']==truth if row['history_observable'] else pred['unknown']
            ptrue=np.array(row['label_progress'])[-1];last=np.array(pred['progress'])[-1]
            out.append(dict(id=row['id'],group=row['group'],variant=row['variant'],n=n,prediction=pred,
                truth_order=truth if row['history_observable'] else None,order_correct=order_ok,
                completion_correct=bool(np.array_equal(last>.985,ptrue==1)),progress_mae=float(np.abs(last-ptrue).mean()),
                prefix_state_accuracy=float(np.mean(np.where(np.array(pred['progress'])>.985,2,np.where(np.array(pred['progress'])>.02,1,0))==np.where(np.array(row['label_progress'])==1,2,np.where(np.array(row['label_progress'])>0,1,0)))) if n==8 else None))
        sampling.append(dict(id=row['id'],indices=row['indices'],timestamps=ts,duration=duration,decoded_matches_saved=saved,adapter_matches_indices=exact))
    save(RESULT/'T2_pixel_predictions.json',out);save(RESULT/'T2_sampling.json',sampling)
    result={str(n):{'order_or_unknown_correct':sum(r['order_correct'] for r in out if r['n']==n),'count':sum(r['n']==n for r in out),
        'completion_correct':sum(r['completion_correct'] for r in out if r['n']==n),'progress_mae':float(np.mean([r['progress_mae'] for r in out if r['n']==n]))} for n in [8,32]}
    result['all_decoded_pixels_exact']=all(r['decoded_matches_saved'] and r['adapter_matches_indices'] for r in sampling)
    result['same_final_equal']={k:bool(np.array_equal(np.asarray(Image.open(ROOT/next(r for r in rows if r['id']==k+'-correct')['frames'][-1])),np.asarray(Image.open(ROOT/next(r for r in rows if r['id']==k+'-swap')['frames'][-1])))) for k in sorted(set(r['group'] for r in rows))}
    save(RESULT/'T2_pixel_metrics.json',result);print(json.dumps(result,indent=2))

def extract():
    import torch
    from h1_run_showo import load_model,StateImageEncoder
    CACHE.mkdir(parents=True,exist_ok=True);rows=json.loads((DATA/'probe.json').read_text());paths=[];lookup={};mapping={}
    for row in rows:
        for p in [row['reference']]+row['frames']:
            key=Image.open(ROOT/p).tobytes()
            if key not in lookup:lookup[key]=len(paths);paths.append(p)
            mapping[p]=lookup[key]
    save(RESULT/'T2_feature_manifest.json',dict(paths=paths,index=mapping))
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','cpu')
    encoder=StateImageEncoder(model,ROOT/'checkpoints/Show-o-assets','mps');features=[];start=time.perf_counter()
    with (CACHE/'progress.jsonl').open('w') as log:
        for i,p in enumerate(paths):
            features.append(encoder.encode(ROOT/p).squeeze(0).cpu());encoder.cache.clear()
            log.write(json.dumps(dict(completed=i+1,total=len(paths),seconds=time.perf_counter()-start))+'\n');log.flush()
    torch.save(dict(features=torch.stack(features)),CACHE/'probe_features.pt')
    save(RESULT/'T2_extraction.json',dict(images=len(paths),shape=list(torch.stack(features).shape),seconds=time.perf_counter()-start,
        full_umm_parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0,
        adaptation='CPU fp32 VAE; MPS bf16 frozen fusion; framewise processing equivalent to official frames as batch, deterministic per-frame seed0'))

def feature_probe():
    import torch
    import torch.nn.functional as F
    f=torch.load(CACHE/'probe_features.pt',map_location='cpu',weights_only=True)['features'].float()
    m=json.loads((RESULT/'T2_feature_manifest.json').read_text())['index'];rows=json.loads((DATA/'probe.json').read_text());pred=[]
    ink=torch.load(ROOT/'checkpoints/h1_spatial_probe_v1/readout.pt',map_location='cpu',weights_only=True)
    f14=F.interpolate(f.reshape(-1,27,27,1536).permute(0,3,1,2),size=(14,14),mode='bilinear').permute(0,2,3,1).reshape(-1,196,1536)
    for row in rows:
        feats=f[[m[p] for p in row['frames']]];small=f14[[m[p] for p in row['frames']]]
        probes={}
        for size,sequence in [(27,feats),(14,small)]:
            logit=torch.nn.functional.linear((sequence-ink['mean'])/ink['std'],ink['state_dict']['weight'],ink['state_dict']['bias'])
            prob=F.interpolate(logit.reshape(8,1,size,size),size=(432,432),mode='bilinear',align_corners=False).sigmoid()
            pictures=[Image.fromarray(np.repeat((np.where(p[0].numpy()>.5,0,255).astype('uint8'))[:,:,None],3,axis=2)) for p in prob]
            prediction=pixel_observer(row,pictures)
            probes[str(size)]=dict(prediction=prediction,order_correct=prediction['event_order']==row['label_order'] if row['history_observable'] else prediction['unknown'])
        pred.append(dict(id=row['id'],deltas27=(feats[1:]-feats[:-1]).abs().mean((1,2)).tolist(),deltas14=(small[1:]-small[:-1]).abs().mean((1,2)).tolist(),
            existing_ink_readout=probes,warning='Fixed old ink head and oracle regions; threshold0.5, no new training. 14 grid is out of head training resolution, so failure cannot establish information loss.'))
    pairs=[]
    for kind in sorted(set(r['group'] for r in rows)):
        a=next(r for r in rows if r['id']==kind+'-correct');b=next(r for r in rows if r['id']==kind+'-swap')
        ia=[m[p] for p in a['frames']];ib=[m[p] for p in b['frames']]
        pairs.append(dict(group=kind,last_frame_equal=bool(torch.equal(f[ia[-1]],f[ib[-1]])),sequence_l1_27=float((f[ia]-f[ib]).abs().mean()),sequence_l1_14=float((f14[ia]-f14[ib]).abs().mean())))
    save(RESULT/'T2_feature_predictions.json',pred);save(RESULT/'T2_feature_pairs.json',pairs);print(json.dumps(pairs,indent=2))

def direct():
    import torch
    import torch.nn.functional as F
    from h1_run_showo import load_model,image_prompt_embeds
    model,tokenizer,tokens=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','mps')
    from h1_run_showo import StateImageEncoder
    from models import omni_attn_mask_naive
    from datasets.utils import resize_and_pad_image,to_tensor_and_normalize
    encoder=StateImageEncoder(model,ROOT/'checkpoints/Show-o-assets','mps')
    rows=json.loads((DATA/'probe.json').read_text());outputs=[]
    for row in [r for r in rows if r['group']=='san' and r['variant'] in ['correct','swap','half','early']]:
        frames,ts,duration=official_load_video(ROOT/row['video'],8)
        torch.manual_seed(42);features=[]
        with torch.no_grad():
            for image in frames:
                pixels=to_tensor_and_normalize(resize_and_pad_image(image,(432,432)))
                latent=encoder.vae.sample(pixels[None,:,None]).squeeze(2).to('mps',torch.bfloat16)
                und=model.image_embedder_und(latent);gen=model.image_embedder_gen(latent)
                und=model.und_trans(und+model.position_embedding(model.image_position_ids))['last_hidden_state']
                features.append(model.fusion_proj(torch.cat([und,gen],dim=-1)))
            all_features=torch.cat(features)
            small=F.interpolate(all_features.reshape(8,27,27,1536).permute(0,3,1,2),size=(14,14),mode='bilinear')
            vision=small.permute(0,2,3,1).reshape(1,8*196,1536)
            for condition,view in [('B2_official_span730',vision),('B1_last_frame',vision[:,-196:])]:
                prompt='The video shows three horizontal strokes. Label the TOP stroke 1, MIDDLE stroke 2, BOTTOM stroke 3. Report ONLY the order in which strokes actually first appear, e.g. [1,2,3]. Do not infer standard handwriting order. If the order cannot be observed, answer unknown.'
                embeds,modalities=image_prompt_embeds(model,tokenizer,tokens,prompt,view,'mps')
                # Preserve official fixed span, including its mismatch for >3 frames.
                modalities[:,:,1]=730
                mask=omni_attn_mask_naive(B=1,LEN=embeds.shape[1],modalities=modalities,device='mps',inverted=True).to(embeds.dtype)
                started=time.perf_counter()
                generated=model.mmu_generate(input_embeds=embeds,attention_mask=mask,top_k=1,max_new_tokens=48,eos_token=tokenizer.eos_token_id)
                text=tokenizer.decode(torch.stack(generated).tolist(),skip_special_tokens=True)
                outputs.append(dict(id=row['id'],condition=condition,input_shape=list(embeds.shape),visual_tokens=view.shape[1],modality_span=730,raw_response=text,seconds=time.perf_counter()-started,timestamps_returned_but_not_prompted=ts))
                save(RESULT/'T2_direct_predictions.json',outputs)
                del embeds,mask,generated
                torch.mps.empty_cache()
    save(RESULT/'T2_direct_path.json',dict(upstream='inference_mmu_vid.py',decoder='PyAV19.0.1 adapter executes unmodified upstream load_video AST',
        preserved=['forced uniform index sampling','official resize/normalize','Wan sample with length1 clips','semantic/generative fusion','27 to14 bilinear','time-major flatten','single diffusion time1','fixed modality span730','topk1'],
        local_adaptations=['CPU fp32 VAE instead of CUDA bf16','serial frame batches1 to bound memory; same sequence seed42 without per-frame reset','MPS bf16 fusion/LLM','8 frames instead of demo32','max_new_tokens48 instead of300'],
        note='Official timestamps are not inserted in the prompt. This is a local execution of its algorithm, not a bitwise CUDA reproduction.'))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['pixels','extract','features','direct']);args=p.parse_args()
    {'pixels':pixels,'extract':extract,'features':feature_probe,'direct':direct}[args.stage]()
