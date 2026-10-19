"""T7 feature access. The formal reader receives a label-free whitelist."""
import json
import numpy as np
import torch
from PIL import Image
from h1_event_data import ROOT
from h1_event_train import grid
from h1_event_observe import masks_for
from h1_early_history_io import normalization,model_input
from h1_t7_data import rows,OUT,DATA

def reference_examples(split):
    if split=='test' and not (OUT/'test_unlock.json').exists():raise RuntimeError('Test masks locked')
    cases={r['group']:r for r in rows(split)}
    mean,std,_=normalization();examples=[]
    for g,r in sorted(cases.items()):
        meta=json.loads((OUT/'feature_manifests'/f'{g}.json').read_text())
        raw=torch.load(ROOT/meta['shard'],map_location='cpu',weights_only=True)['features']
        reference=(raw[meta['index'][r['reference']]].float()-mean)/std
        masks=masks_for(r);unique=masks&(masks.sum(0)==1)[None];shared=masks.sum(0)>1
        examples.append(dict(group=g,family=r['family'],split=split,q=len(masks),reference=reference,
            kinds=torch.tensor(r['query']['kinds']),hints=torch.tensor(r['query']['hints'],dtype=torch.float32),
            target=grid(masks),exclusive=grid(unique),shared=grid(shared)[0]))
    return examples

def prepare_group(group):
    if group.startswith('test-') and not (OUT/'test_unlock.json').exists():raise RuntimeError('Test labels locked')
    meta=json.loads((OUT/'feature_manifests'/f'{group}.json').read_text());index=meta['index']
    raw=torch.load(ROOT/meta['shard'],weights_only=True)['features'].float();mean,std,projection=normalization()
    features=(raw-mean)/std;small=features@projection;truths={}
    for r in json.loads((OUT/'labels'/f'{group}.json').read_text()):truths.setdefault(r['id'],[]).append(r['state'])
    for row in json.loads((DATA/group/'cases.json').read_text()):
        ids=[index[p] for p in row['frames']];ref=index[row['reference']]
        ink=np.stack([np.asarray(Image.open(ROOT/p))[:,:,0]<128 for p in row['frames']]);prev=np.concatenate([np.zeros_like(ink[:1]),ink[:-1]])
        p=torch.tensor(row['label_progress']);states=truths[row['id']]
        from h1_event_model import rule_action
        yield dict(row=row,reference=features[ref],visual=features[ids],small=small[ids],ref_small=small[ref],
            kinds=torch.tensor(row['query']['kinds']),hints=torch.tensor(row['query']['hints'],dtype=torch.float32),masks=grid(masks_for(row)),rgb=torch.stack([grid(ink&~prev),grid(prev&~ink)],1),
            progress=p,state=torch.where(p==1,2,torch.where(p>0,1,0)),truth_states=states,
            truth=[rule_action(dict(event_order=s['event_order'],progress=p[t].tolist(),direction=s['direction']),list(range(len(p[t])))) for t,s in enumerate(states)])
