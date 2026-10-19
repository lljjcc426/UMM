"""Geometry-sized frozen feature reader and explicit model-input whitelist."""
import json
from functools import lru_cache
import numpy as np
import torch
from PIL import Image
from h1_event_data import ROOT
from h1_event_observe import masks_for
from h1_event_train import grid
from h1_early_history_data import DATA,OUT,WEIGHTS

@lru_cache(maxsize=1)
def normalization():
    torch.set_num_threads(4)
    normal=torch.load(ROOT/'checkpoints/h1_spatial_probe_v1/readout.pt',map_location='cpu',weights_only=True)
    rng=torch.Generator().manual_seed(42)
    return normal['mean'],normal['std'],torch.randn(1536,64,generator=rng)/1536**.5

def prepare_group(group,labels=True):
    manifest=json.loads((OUT/'feature_manifests'/f'{group}.json').read_text());index=manifest['index']
    raw=torch.load(ROOT/manifest['shard'],map_location='cpu',weights_only=True)['features'].float()
    mean,std,projection=normalization();features=(raw-mean)/std;small=features@projection
    rows=[r for r in json.loads((DATA/'cases.json').read_text()) if r['group']==group]
    truths={}
    if labels:
        for r in json.loads((OUT/'pixel_states.json').read_text()):
            if r['group']==group:truths.setdefault(r['id'],[]).append(r['state'])
    items=[]
    for row in rows:
        ids=[index[p] for p in row['frames']];ref=index[row['reference']]
        ink=np.stack([np.asarray(Image.open(ROOT/p))[:,:,0]<128 for p in row['frames']]);previous=np.concatenate([np.zeros_like(ink[:1]),ink[:-1]])
        current=grid(ink);new=grid(ink&~previous);gone=grid(previous&~ink)
        x=dict(row=row,reference=features[ref],visual=features[ids],small=small[ids],ref_small=small[ref],kinds=torch.tensor(row['query']['kinds']),hints=torch.tensor(row['query']['hints'],dtype=torch.float32),
            masks=grid(masks_for(row)),rgb=torch.stack([new,gone],1),change=torch.stack([current,new,gone],1))
        if labels:
            states=truths[row['id']];p=torch.tensor(row['label_progress']);geometry=torch.where(p==1,2,torch.where(p>0,1,0))
            onsets=torch.tensor([[s['onset_intervals'].get(str(j),[0,-1])[1] for j in range(p.shape[1])] for s in states])
            changed=(p-torch.cat([torch.zeros_like(p[:1]),p[:-1]]))>0
            active=torch.tensor([int(v.nonzero()[0])+1 if v.sum()==1 else 0 for v in changed])
            from h1_event_model import rule_action
            x.update(progress=p,state=geometry,onsets=onsets,confidence=torch.tensor([s['event_order'] is not None for s in states],dtype=torch.float32),
                orders=[s['event_order'] for s in states],direction=torch.tensor([[['unknown','forward','reverse'].index(v) for v in s['direction']] for s in states]),active=active,
                start=((p>0)&~torch.cat([torch.zeros_like(p[:1],dtype=torch.bool),p[:-1]>0])).float(),complete=((p==1)&~torch.cat([torch.zeros_like(p[:1],dtype=torch.bool),p[:-1]==1])).float(),
                truth_states=states,truth=[rule_action(dict(event_order=s['event_order'],progress=p[t].tolist(),direction=s['direction']),list(range(p.shape[1]))) for t,s in enumerate(states)])
        items.append(x)
    return items

def model_input(x,oracle=False):
    # No path/variant/split/source order/label/instance mask reaches the main reader.
    view={k:x[k] for k in ['reference','visual','small','ref_small','kinds','hints','rgb']}
    view['row']={'indices':x['row']['indices']}
    if oracle:view['masks']=x['masks']
    return view
