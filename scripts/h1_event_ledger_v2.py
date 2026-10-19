"""L1: observation-only onset candidates, confirmation and explicit uncertainty.

Intervals are (left,right]; None as left means missing initial history.
Presence and start share a head: their evidence is correlated, never multiplied
into a probability. Confirmation rules are deterministic hypotheses, not proof.
"""
import copy,itertools
from h1_event_model import rule_action

def before(a,b):
    return b[0] is not None and a[1]<=b[0]

def maximal_unresolved_groups(seen,precedence):
    known={tuple(p) for p in precedence};cliques=[]
    for size in range(2,len(seen)+1):
        for group in itertools.combinations(seen,size):
            if all((a,b) not in known and (b,a) not in known for a,b in itertools.combinations(group,2)):cliques.append(set(group))
    return [sorted(g) for g in cliques if not any(g<h for h in cliques)]

class EvidenceLedger:
    def __init__(self,q,presence_threshold=.5,start_threshold=.5,new_threshold=.02):
        self.q=q;self.pt=presence_threshold;self.st=start_threshold;self.nt=new_threshold
        self.events={};self.last_t=-1;self.last_absent=[None]*q;self.weak=[None]*q
        self.previous=None;self.audit=[];self.history_gap=False;self.missing_initial=set()

    def note(self,event,j,t,**details):
        self.audit.append(dict(event=event,instance_id=j,t=t,**copy.deepcopy(details)))

    def update(self,t,presence,progress,geometry,direction,new_ink,start,binding_ambiguous=()):
        if t<=self.last_t:raise ValueError('Online observations must advance')
        if t!=self.last_t+1:self.history_gap=True
        self.last_t=t;binding=set(binding_ambiguous)
        for j in range(self.q):
            p,s,n=float(presence[j]),float(start[j]),float(new_ink[j]);negative=p<self.pt and s<self.st and n<self.nt
            e=self.events.get(j)
            if e and e['status']=='confirmed':
                if negative and self.previous and self.previous['presence'][j]>=self.pt:self.note('contradictory_absence_after_confirmation',j,t)
                e.update(last_observed_progress=progress[j],geometry_state=geometry[j])
                if direction[j]!='unknown':e['direction']=direction[j]
                continue
            if negative:
                if e:
                    self.note('candidate_rejected',j,t,reason='three_signals_below_threshold',rejected=e)
                    del self.events[j];self.missing_initial.discard(j)
                self.last_absent[j]=t;self.weak[j]=None;continue
            if self.weak[j] and self.weak[j]['t']<t-1:self.weak[j]=None
            previous_weak=self.weak[j]
            evidence=dict(t=t,presence=p,start=s,new_ink=n)
            if s>=self.st and n>=self.nt:self.weak[j]=evidence
            if p<self.pt:
                if e:e.update(status='ambiguous',conflict='presence_not_persistent')
                continue
            if e is None:
                interval=[self.last_absent[j],t]
                e=dict(instance_id=j,status='candidate' if s>=self.st or n>=self.nt else 'ambiguous',
                    possible_onset_interval=interval,first_detection_interval=[max(0,t-1),t],confirmation_interval=None,
                    evidence_sources=[evidence],direction=direction[j],last_observed_progress=progress[j],geometry_state=geometry[j])
                self.events[j]=e;self.note('candidate_created' if e['status']=='candidate' else 'presence_without_onset_support',j,t,possible_interval=interval)
                if t==0:self.missing_initial.add(j)
            e.update(last_observed_progress=progress[j],geometry_state=geometry[j])
            if direction[j]!='unknown':e['direction']=direction[j]
            if j in binding:
                e.update(status='ambiguous',conflict='instance_masks_overlap');continue
            interval=e['possible_onset_interval'];first=e['first_detection_interval'][1];confirmed=False;rule=None
            if t>0 and s>=self.st and n>=self.nt:
                candidate=[t-1,t]
                if interval[0] is not None and candidate[0]>=interval[0] and candidate[1]<=interval[1]:
                    interval=candidate;confirmed=True;rule='simultaneous_presence_start_change'
                else:e.update(status='ambiguous',conflict='start_outside_candidate_interval')
            if not confirmed and t>0 and n>=self.nt and previous_weak and previous_weak['t']==t-1:
                candidate=[t-2,t-1]
                if interval[0] is not None and candidate[0]>=interval[0] and candidate[1]<=interval[1]:
                    interval=candidate;confirmed=True;rule='previous_start_change_current_presence'
                    e['evidence_sources'].append(previous_weak)
            if not confirmed and t==first+1 and self.previous:
                prior=self.previous
                if prior['presence'][j]>=self.pt and prior['new_ink'][j]>=self.nt and interval[0] is not None:
                    confirmed=True;rule='persistent_presence_and_change'
            if confirmed:
                e.update(status='confirmed',possible_onset_interval=interval,confirmation_interval=[max(0,t-1),t],confirmation_rule=rule)
                e['evidence_sources'].append(evidence);self.weak[j]=None
                self.note('candidate_confirmed',j,t,possible_interval=interval,rule=rule)
        self.previous=dict(presence=list(presence),start=list(start),new_ink=list(new_ink))
        return self.state(progress,geometry,direction,binding)

    def state(self,progress,geometry,direction,binding):
        seen=sorted(self.events);precedence=[]
        for a in seen:
            for b in seen:
                ea,eb=self.events[a],self.events[b]
                if ea['status']==eb['status']=='confirmed' and a not in binding and b not in binding and before(ea['possible_onset_interval'],eb['possible_onset_interval']):precedence.append([a,b])
        groups=maximal_unresolved_groups(seen,precedence)
        pending=[j for j,w in enumerate(self.weak) if w and j not in self.events]
        unconfirmed=[j for j,e in self.events.items() if e['status']!='confirmed']
        if self.history_gap or self.missing_initial:reason='insufficient_history'
        elif binding.intersection(seen):reason='uncertain_instance_binding'
        elif pending or unconfirmed:reason='uncertain_onset_detection'
        elif groups:
            # An inferred common visual interval is still conditional on detections.
            same_intervals=all(len({tuple(self.events[j]['possible_onset_interval']) for j in g})==1 for g in groups)
            reason='merged_onset_interval' if same_intervals else 'uncertain_onset_detection'
        else:reason=None
        order=None if reason else sorted(seen,key=lambda j:self.events[j]['possible_onset_interval'][1])
        stored_direction=[self.events[j]['direction'] if j in self.events else direction[j] for j in range(self.q)]
        entries=copy.deepcopy([self.events[j] for j in seen])
        state=dict(observed_ids=seen,event_order=order,progress=list(progress),geometry_state=list(geometry),direction=stored_direction,
            onset_intervals={str(j):e['possible_onset_interval'][:] for j,e in self.events.items()},
            first_detection_intervals={str(j):e['first_detection_interval'][:] for j,e in self.events.items()},
            confirmation_intervals={str(j):copy.deepcopy(e['confirmation_interval']) for j,e in self.events.items()},
            confirmed_precedence=precedence,unresolved_order_groups=groups,uncertain_instance_ids=sorted(set(unconfirmed+pending)),
            uncertainty_reason=reason,observation_confidence=0. if reason else 1.,pen_lift_evidence='unknown',
            recovery='review_past_observations_or_request_denser_sampling' if reason else None,
            physical_irrecoverability='not_established_by_learned_detections',ledger=entries,
            instance_event_status=[self.events[j]['status'] if j in self.events else 'unseen' for j in range(self.q)],audit=copy.deepcopy(self.audit))
        decision_progress=[0. if c==0 else 1. if c==2 else min(.984,max(.001,p)) for c,p in zip(geometry,progress)]
        state['decision']=rule_action(dict(event_order=order,progress=decision_progress,direction=stored_direction),list(range(self.q)))
        return state
