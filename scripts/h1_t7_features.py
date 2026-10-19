"""T7 frozen native27 UMM cache and exact recent-input equality."""
import argparse,json,time
import torch
from PIL import Image
from h1_event_data import ROOT,save
from h1_t7_data import rows,OUT,WEIGHTS,DECISIONS

def extract():
    from h1_run_showo import load_model,StateImageEncoder
    cases=rows();manifest={};count=0;blank=None;start=time.perf_counter()
    model,_,_=load_model(ROOT/'checkpoints/Show-o-source',ROOT/'checkpoints/Show-o2-1.5B-video',ROOT/'checkpoints/Show-o-assets','cpu')
    encoder=StateImageEncoder(model,ROOT/'checkpoints/Show-o-assets','mps')
    for group in sorted({r['group'] for r in cases}):
        target=WEIGHTS/'features'/f'{group}.pt';entry=OUT/'feature_manifests'/f'{group}.json'
        if target.exists():manifest[group]=json.loads(entry.read_text());continue
        paths=[];index={};lookup={}
        for r in [r for r in cases if r['group']==group]:
            for p in [r['reference']]+r['frames']:
                key=Image.open(ROOT/p).tobytes()
                if key not in lookup:lookup[key]=len(paths);paths.append(p)
                index[p]=lookup[key]
        features=[]
        for p in paths:
            is_blank=Image.open(ROOT/p).getextrema()==((255,255),)*3
            if is_blank and blank is not None:f=blank
            else:
                f=encoder.encode(ROOT/p).squeeze(0).cpu();encoder.cache.clear();count+=1
                if is_blank:blank=f
            features.append(f);save(WEIGHTS/'extraction_progress.json',dict(group=group,encoded=count,seconds=time.perf_counter()-start))
        target.parent.mkdir(parents=True,exist_ok=True);tensor=torch.stack(features);torch.save(dict(features=tensor),target)
        manifest[group]=dict(paths=paths,index=index,shard=str(target.relative_to(ROOT)),shape=list(tensor.shape));save(entry,manifest[group])
    save(OUT/'feature_manifest.json',manifest)
    save(OUT/'extraction.json',dict(encoded=count,seconds=time.perf_counter()-start,parameters=sum(p.numel() for p in model.parameters()),umm_updated_parameters=0,shards=len(manifest),
        method='Unchanged T6 StateImageEncoder: CPU fp32 VAE, MPS bf16 fusion, native27, seed0 per image'))

def contracts():
    cases=rows();checks=[]
    for g in sorted({r['group'] for r in cases}):
        meta=json.loads((OUT/'feature_manifests'/f'{g}.json').read_text());f=torch.load(ROOT/meta['shard'],weights_only=True)['features'];idx=meta['index']
        by={r['variant']:r for r in cases if r['group']==g};a=by['correct'];q=len(a['strokes'])
        for name in ['swap1']+(['swap2'] if q==5 else []):
            for t in DECISIONS:
                left=f[[idx[p] for p in a['frames'][t-8:t+1]]];right=f[[idx[p] for p in by[name]['frames'][t-8:t+1]]]
                assert torch.equal(left,right)
                checks.append(dict(group=g,variant=name,t=t,exact_recent8_and_predecessor=True))
        assert torch.equal(f[[idx[p] for p in by['mergedA']['frames']]],f[[idx[p] for p in by['mergedB']['frames']]])
    save(OUT/'feature_contract_checks.json',dict(passed=True,checks=checks))
    d=json.loads((OUT/'data_contract_checks.json').read_text());d.update(feature_gate=True,training_permitted=d['pixel_gate']);save(OUT/'data_contract_checks.json',d)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['extract','contracts']);a=p.parse_args();globals()[a.stage]()
