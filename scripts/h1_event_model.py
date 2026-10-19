"""Specified A/B/C modules; all trainable layers are independent of frozen UMM."""
import math
import torch
from torch import nn
import torch.nn.functional as F

class StrokeGrounding(nn.Module):
    def __init__(self):
        super().__init__();self.proj=nn.Sequential(nn.LayerNorm(1536),nn.Linear(1536,256));self.xy=nn.Linear(2,256)
        self.index=nn.Embedding(16,256);self.kind=nn.Embedding(5,256);self.hint=nn.Linear(2,256)
        layer=nn.TransformerDecoderLayer(256,4,512,.1,batch_first=True,norm_first=True)
        self.decoder=nn.TransformerDecoder(layer,2);self.mask=nn.Linear(256,256);self.confidence=nn.Linear(256,1);self.bias=nn.Parameter(torch.tensor(-2.))
        y,x=torch.meshgrid(torch.linspace(-1,1,27),torch.linspace(-1,1,27),indexing='ij');self.register_buffer('coords',torch.stack([x,y],-1).reshape(729,2))
    def forward(self,reference,kinds,hints):
        memory=self.proj(reference)+self.xy(self.coords)[None]
        q=self.index(torch.arange(kinds.shape[1],device=kinds.device))[None]+self.kind(kinds)+self.hint(hints)
        q=self.decoder(q,memory)
        return torch.einsum('bqd,bpd->bqp',self.mask(q),memory)/math.sqrt(256)+self.bias,self.confidence(q).squeeze(-1)

class InkChange(nn.Module):
    def __init__(self):
        super().__init__();self.proj=nn.Sequential(nn.LayerNorm(1536),nn.Linear(1536,32),nn.GELU())
        self.head=nn.Sequential(nn.Conv2d(66,32,3,padding=1),nn.GELU(),nn.Conv2d(32,3,1))
    def forward(self,previous,current,rgb_delta):
        # RGB signed change is available from observations. No instance labels.
        x=torch.cat([self.proj(current),self.proj(current-previous),rgb_delta.transpose(1,2)],-1)
        return self.head(x.transpose(1,2).reshape(-1,66,27,27)).reshape(-1,3,729)

class EventState(nn.Module):
    def __init__(self,input_dim=196,temporal=True):
        super().__init__();self.input=nn.Linear(input_dim,256);self.temporal=temporal
        if temporal:
            layer=nn.TransformerEncoderLayer(256,4,512,.1,batch_first=True,norm_first=True)
            self.encoder=nn.TransformerEncoder(layer,2,enable_nested_tensor=False)
        else:self.encoder=nn.Sequential(nn.Linear(256,2048),nn.GELU(),nn.Dropout(.1),nn.Linear(2048,256),nn.GELU())
        self.state=nn.Linear(256,3);self.progress=nn.Linear(256,1);self.direction=nn.Linear(256,3)
        self.start=nn.Linear(256,1);self.complete=nn.Linear(256,1);self.order=nn.Linear(256,1)
        self.active=nn.Linear(256,1);self.none=nn.Linear(256,1);self.confidence=nn.Linear(256,1)
    @staticmethod
    def causal_mask(t,q,device=None):
        """Same-time instances can interact; future times are always masked."""
        times=torch.arange(t,device=device).repeat_interleave(q)
        return times[None,:]>times[:,None]
    def forward(self,x):
        b,t,q,_=x.shape;h=self.input(x).reshape(b,t*q,256)
        if self.temporal:
            h=self.encoder(h,mask=self.causal_mask(t,q,x.device))
        else:h=self.encoder(h)
        h=h.reshape(b,t,q,256);pooled=h.mean(2)
        return dict(state=self.state(h),progress=self.progress(h).squeeze(-1).sigmoid(),direction=self.direction(h),
            start=self.start(h).squeeze(-1),complete=self.complete(h).squeeze(-1),order=self.order(h).squeeze(-1),
            active=torch.cat([self.none(pooled),self.active(h).squeeze(-1)],-1),confidence=self.confidence(pooled).squeeze(-1))

def mask_loss(logit,target):
    prob=logit.sigmoid();dice=(2*(prob*target).sum(-1)+1)/(prob.sum(-1)+target.sum(-1)+1)
    return F.binary_cross_entropy_with_logits(logit,target)+(1-dice).mean()

def rule_action(state,expected):
    """D: deterministic mapping; no labels or generated schedule read here."""
    if state['event_order'] is None:return dict(first_error=None,error_type='unobservable',next_legal=None,action='request_observation')
    order=state['event_order'];first=None;error=None;progress=state['progress']
    for pos,j in enumerate(order):
        if j!=expected[pos]:first=pos;error='wrong_order';break
        if state['direction'][j]=='reverse':first=pos;error='reverse_direction';break
        if pos+1<len(order) and progress[j]<.985:first=pos+1;error='early_switch';break
    if first is not None:return dict(first_error=first,error_type=error,next_legal=None,action='stop_erroneous_process')
    unfinished=[j for j in order if progress[j]<.985]
    if unfinished:return dict(first_error=None,error_type=None,next_legal=unfinished[-1],action='continue')
    next_id=next((j for j in expected if j not in order),None)
    return dict(first_error=None,error_type=None,next_legal=next_id,action='end_ink_task' if next_id is None else 'start')
