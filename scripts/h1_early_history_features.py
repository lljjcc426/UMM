"""Frozen UMM encoding in geometry shards; no model training or label features."""
import argparse, hashlib, json, time
from pathlib import Path
import torch
from PIL import Image
from h1_event_data import ROOT,save
from h1_early_history_data import DATA,OUT,WEIGHTS

def extract():
    from h1_run_showo import load_model,StateImageEncoder
    rows=json.loads((DATA/'cases.json').read_text());groups=sorted({r['group'] for r in rows});manifest={};count=0;blank=None;start=time.perf_counter()
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','cpu')
    encoder=StateImageEncoder(model,ROOT/'checkpoints/Show-o-assets','mps')
    for group in groups:
        target=WEIGHTS/'features'/f'{group}.pt';entry=OUT/'feature_manifests'/f'{group}.json'
        if target.exists():
            manifest[group]=json.loads(entry.read_text());continue
        paths=[];index={};lookup={}
        for row in [r for r in rows if r['group']==group]:
            for p in [row['reference']]+row['frames']:
                key=hashlib.sha256(Image.open(ROOT/p).tobytes()).digest()
                if key not in lookup:lookup[key]=len(paths);paths.append(p)
                index[p]=lookup[key]
        features=[]
        for p in paths:
            is_blank=Image.open(ROOT/p).getextrema()==((255,255),)*3
            if is_blank and blank is not None:f=blank
            else:
                f=encoder.encode(ROOT/p).squeeze(0).cpu();encoder.cache.clear();count+=1
                if is_blank:blank=f
            features.append(f)
            save(WEIGHTS/'extraction_progress.json',dict(group=group,encoded=count,seconds=time.perf_counter()-start))
        target.parent.mkdir(parents=True,exist_ok=True);torch.save(dict(features=torch.stack(features)),target)
        manifest[group]=dict(paths=paths,index=index,shard=str(target.relative_to(ROOT)),shape=list(torch.stack(features).shape));save(entry,manifest[group])
    save(OUT/'feature_manifest.json',manifest)
    save(OUT/'extraction.json',dict(encoded=count,seconds=time.perf_counter()-start,parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0,
        path='T4 native27 fusion, CPU fp32 VAE / MPS bf16, per-image seed0; RGB-identical images share cached tensors',shards=len(groups)))

if __name__=='__main__':
    argparse.ArgumentParser().parse_args();extract()
