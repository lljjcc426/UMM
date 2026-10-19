"""Causal event ledger; observations only, no target order or source log in update."""
import copy
from h1_event_model import rule_action

class EventLedger:
    def __init__(self,q,presence_threshold=.5,new_threshold=.02):
        self.q=q;self.presence_threshold=presence_threshold;self.new_threshold=new_threshold
        self.events={};self.last_t=-1;self.unconfirmed=set()
    def update(self,t,presence,progress,geometry,direction,new_ink):
        if t<=self.last_t:raise ValueError('Online observations must advance')
        self.last_t=t
        for j in range(self.q):
            if j not in self.events and presence[j]>=self.presence_threshold:
                confirmed=new_ink[j]>=self.new_threshold and t>0
                self.events[j]=dict(instance_id=j,first_observed_interval=[max(0,t-1),t],last_observed_progress=progress[j],geometry_state=geometry[j],onset_confidence=presence[j],confirmed=confirmed,direction=direction[j])
                if not confirmed:self.unconfirmed.add(j)
            if j in self.events:
                self.events[j].update(last_observed_progress=progress[j],geometry_state=geometry[j])
                if direction[j]!='unknown':self.events[j]['direction']=direction[j]
        return self.state(progress,geometry,direction)
    def state(self,progress,geometry,direction):
        seen=sorted(self.events);groups={}
        for j,e in self.events.items():groups.setdefault(e['first_observed_interval'][1],[]).append(j)
        unresolved=[sorted(g) for _,g in sorted(groups.items()) if len(g)>1]
        precedence=[[a,b] for a in seen for b in seen if self.events[a]['confirmed'] and self.events[b]['confirmed'] and self.events[a]['first_observed_interval'][1]<self.events[b]['first_observed_interval'][1]]
        reason='uncertain_onset_detection' if self.unconfirmed else 'merged_onset_interval' if unresolved else None
        order=None if reason else sorted(seen,key=lambda j:self.events[j]['first_observed_interval'][1])
        stored_direction=[self.events[j]['direction'] if j in self.events else direction[j] for j in range(self.q)]
        state=dict(observed_ids=seen,event_order=order,progress=list(progress),geometry_state=list(geometry),direction=stored_direction,
            onset_intervals={str(j):e['first_observed_interval'][:] for j,e in self.events.items()},confirmed_precedence=precedence,unresolved_order_groups=unresolved,
            uncertain_instance_ids=sorted(self.unconfirmed),uncertainty_reason=reason,observation_confidence=0. if reason else 1.,pen_lift_evidence='unknown',
            recovery='requires_missing_past_observations' if reason else None,ledger=copy.deepcopy(list(self.events.values())))
        decision_progress=[0. if c==0 else 1. if c==2 else min(.984,max(.001,p)) for c,p in zip(geometry,progress)]
        state['decision']=rule_action(dict(event_order=order,progress=decision_progress,direction=stored_direction),list(range(self.q)))
        return state
