"""Narrow geometric microtask observer. Reads actual pixels, never construction logs.

Geometry is an explicit evaluation-only O privilege. It is NOT a free-glyph judge.
Thresholds apply only to synthetic black/white nonoverlapping line fixtures.
"""
import numpy as np


def observe_rgb(frames, pts, regions):
    ink=frames.mean(axis=-1)<128
    loss=ink[:-1]&~ink[1:]
    persistence='incorrect' if np.count_nonzero(loss)>5 else 'correct'
    events=[]; unknown=[]
    for item in regions:
        x0,y0,x1,y1=item['box'];patch=ink[:,y0:y1,x0:x1]
        amount=patch.mean(axis=(1,2));active=np.flatnonzero(amount>.01)
        if not len(active):
            events.append({'instance_id':item['id'],'status':'missing','onset':None,'completion':None,'direction':'unknown'})
            continue
        onset=int(active[0]); maximum=float(amount.max())
        completion=int(np.flatnonzero(amount>=maximum*.98)[0])
        partial=np.flatnonzero((amount>maximum*.05)&(amount<maximum*.90))
        if len(partial)<2:
            direction='unknown';unknown.append('insufficient_visible_growth:'+item['id'])
        else:
            a=patch[partial[0]];b=patch[partial[-1]]
            ya,xa=np.nonzero(a);yb,xb=np.nonzero(b)
            dx=float(xb.mean()-xa.mean());dy=float(yb.mean()-ya.mean())
            axis=item['axis'];delta=dx if axis=='x' else dy
            direction=('positive' if delta>1 else 'negative') if abs(delta)>1 else 'unknown'
        events.append({'instance_id':item['id'],'status':'observed','onset':float(pts[onset]),
                       'completion':float(pts[completion]),'direction':direction,'partial_frames':len(partial)})
    visible=[e for e in events if e['onset'] is not None]
    order=sorted(visible,key=lambda e:e['onset'])
    simultaneous=len({e['onset'] for e in visible})!=len(visible)
    confirmed_overlap=any(a['onset']==b['onset'] and a.get('partial_frames',0)>=2 and b.get('partial_frames',0)>=2
                          for i,a in enumerate(visible) for b in visible[i+1:])
    support=np.zeros(ink.shape[1:],bool)
    for item in regions:
        x0,y0,x1,y1=item['box'];support[y0:y1,x0:x1]=True
    extra=bool(np.count_nonzero(ink & ~support[None])>5)
    return {'events':events,'observed_order':[e['instance_id'] for e in order],
            'order_observable':not simultaneous and bool(visible),
            'confirmed_overlap':confirmed_overlap,
            'historical_ink':persistence,'extra_ink':extra,'unknown_reasons':unknown,
            'domain':'synthetic_disjoint_line_regions_only','uses_renderer_events':False}


def judge_execution(observed, reference):
    events=observed['events'];missing=any(e['status']=='missing' for e in events)
    order=('incorrect' if observed['confirmed_overlap'] else 'unknown' if not observed['order_observable'] else
           'correct' if observed['observed_order']==reference['order'] else 'incorrect')
    dirs=[e['direction'] for e in events if e['status']=='observed']
    direction=('unknown' if not dirs or 'unknown' in dirs else
               'correct' if all(e['direction']==reference['directions'][e['instance_id']] for e in events if e['status']=='observed') else 'incorrect')
    return {'stroke_order':order,'direction':direction,
            'completeness':'incorrect' if missing or observed['extra_ink'] else 'correct',
            'historical_ink':observed['historical_ink'],
            'temporal_observability':'correct' if order!='unknown' and direction!='unknown' else 'unknown',
            'final_glyph':'not_applicable','task_compliance':'incorrect' if missing or observed['extra_ink'] else 'unknown'}
