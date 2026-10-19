"""One fixed 4/2/2-geometry interface/resource test; no optimizer updates."""
import json,time,resource
import torch
from h1_event_data import ROOT,save
from h1_early_history_data import OUT
from h1_early_history_io import prepare_group,model_input
from h1_early_history_experiment import shared_modules,tensor_batch,sequence_loss
from h1_event_train import event_inputs
from h1_event_model import EventState

def run():
    torch.set_num_threads(4);torch.manual_seed(42);splits=json.loads((OUT/'splits.json').read_text());selected={k:splits[k][:n] for k,n in [('train',4),('dev',2),('test',2)]}
    a,b=shared_modules(ROOT/'checkpoints/h1_event_v3/T4/spatial_best.pt');train=[];shapes=[];start=time.perf_counter()
    for split,groups in selected.items():
        for group in groups:
            x=prepare_group(group)[0]
            with torch.no_grad():x['inputs']=event_inputs(model_input(x),a,b)
            shapes.append(dict(group=group,shape=list(x['inputs'].shape)))
            if split=='train':train.append({k:v for k,v in x.items() if k in ['inputs','state','direction','active','start','complete','confidence','onsets','progress']})
    batch=tensor_batch(train*2);results=[]
    for temporal in [False,True]:
        model=EventState(temporal=temporal);loss=sequence_loss(model(batch['inputs']),batch);loss.backward()
        gradients=[p.grad for p in model.parameters() if p.grad is not None];finite=all(bool(g.isfinite().all()) for g in gradients)
        results.append(dict(temporal=temporal,batch_shape=list(batch['inputs'].shape),loss=float(loss.detach()),finite_gradients=finite,nonzero_gradients=sum(bool(g.norm()>0) for g in gradients),optimizer_updates=0))
        assert finite and bool(loss.isfinite())
    save(OUT/'preflight.json',dict(groups=selected,inputs=shapes,heads=results,seconds=time.perf_counter()-start,max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,test_labels_used_for_gradient=False,optimizer_updates=0))

if __name__=='__main__':run()
