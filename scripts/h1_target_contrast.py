"""Same-image instance supervision; shared pixels are never contrastive negatives."""
import torch
import torch.nn.functional as F
from h1_event_model import mask_loss

def target_contrast(logits,target,exclusive,shared,kinds,hints):
    b,q,_=logits.shape;terms=[];weights=[]
    per_pixel=F.binary_cross_entropy_with_logits(logits,(target>.25).float(),reduction='none')
    for i in range(q):
        for j in range(q):
            if i==j:continue
            # Entire native cells containing legitimate shared pixels are excluded.
            pos=exclusive[:,i]*(shared==0)
            neg=exclusive[:,j]*(target[:,i]==0)*(shared==0)
            positive=(per_pixel[:,i]*pos).sum(-1)/pos.sum(-1).clamp_min(1e-6)
            negative=(per_pixel[:,i]*neg).sum(-1)/neg.sum(-1).clamp_min(1e-6)
            hard=(kinds[:,i]==kinds[:,j])|((hints[:,i]-hints[:,j]).norm(dim=-1)<=.6)
            weight=1+hard.float();valid=(pos.sum(-1)>0)&(neg.sum(-1)>0)
            terms.append(.5*(positive+negative)*weight*valid);weights.append(weight*valid)
    return torch.stack(terms).sum()/torch.stack(weights).sum().clamp_min(1)

def grounding_loss(model,batch,contrast=False):
    logits,conf=model(batch['reference'],batch['kinds'],batch['hints']);target=batch['target'];prob=logits.detach().sigmoid()
    intersection=(prob*target).sum(-1);quality=intersection/(prob.sum(-1)+target.sum(-1)-intersection).clamp_min(1e-6)
    base=mask_loss(logits,target)+.1*F.binary_cross_entropy_with_logits(conf,quality)
    target_loss=target_contrast(logits,target,batch['exclusive'],batch['shared'],batch['kinds'],batch['hints']) if contrast else logits.sum()*0
    return base+.2*target_loss,base,target_loss
