"""All-attempt accounting; independent formal metrics stay separate from CPU fixtures."""
from collections import Counter,defaultdict
from .contracts import FACETS,LABELS


def summarize(records, authority='CPU_development', required_facets=FACETS):
    ids=set()
    for row in records:
        if row['id'] in ids or row['status'] not in {'failed','completed','unknown','not_applicable'}:
            raise ValueError('Duplicate attempt or invalid status')
        ids.add(row['id'])
        if any(v not in LABELS for v in row.get('facets',{}).values()):
            raise ValueError('Invalid facet label')
        if row['status']=='failed' and any(v=='incorrect' for v in row.get('facets',{}).values()):
            raise ValueError('Technical failure is not evidence of wrong stroke order')
    n=len(records); ratio=lambda x:x/n if n else None
    counts=Counter(r['status'] for r in records); dimensions={}
    for key in FACETS+('identity',):
        c=Counter(r.get('facets',{}).get(key,'unknown') for r in records if r['status']!='failed')
        judged=c['correct']+c['incorrect']
        dimensions[key]={'counts':dict(c),'correct_all_attempts':ratio(c['correct']),
                         'clear_coverage':ratio(judged),'conditional_correct':c['correct']/judged if judged else None}
    successes=sum(r['status']=='completed' and all(r.get('facets',{}).get(k)=='correct' for k in required_facets) for r in records)
    result={'initial_attempts':n,'status_counts':dict(counts),'verified_success_count':successes,
            'all_attempt_success_lower_bound':ratio(successes),'technical_failure_rate':ratio(counts['failed']),
            'process_observability':dimensions['temporal_observability']['correct_all_attempts'],
            'dimensions':dimensions,'authority':authority,
            'formal_primary_metrics':None,'joint_success_definition':list(required_facets),
            'cost':{k:sum(r.get('cost',{}).get(k,0) or 0 for r in records) for k in ('wall_seconds','gpu_seconds','CNY')},
            'cost_complete':all(all(r.get('cost',{}).get(k) is not None for k in ('wall_seconds','gpu_seconds','CNY')) for r in records)}
    if authority=='independent_human_adjudicated' and all(r.get('human_evidence_qualified') for r in records):
        result['formal_primary_metrics']={'verified_full_process_success':ratio(successes),
            'process_observability':result['process_observability']}
    return result


def paired_attempts(records):
    groups=defaultdict(list)
    for row in records:groups[(row['character'],row['seed'])].append(row)
    return [{'character':char,'seed':seed,'attempt_ids':[r['id'] for r in group],
             'conditions':[r['condition'] for r in group],'statuses':[r['status'] for r in group]}
            for (char,seed),group in sorted(groups.items())]


def classify_error(action_valid=None, visual_transition_correct=None, explicit_action_state=False):
    if not explicit_action_state or action_valid is None:return 'unattributed'
    if not action_valid:return 'policy_error'
    if visual_transition_correct is False:return 'draw_error'
    return 'valid' if visual_transition_correct is True else 'unknown'


def score_response(track, prediction, answer):
    """Structured response comparator. Narrative answers remain unparsed/unknown."""
    if not isinstance(prediction,dict):return {'status':'unknown','reason':'unparsed narrative; human interpretation not fabricated'}
    if track=='K-CHAR':
        correct=prediction.get('character')==answer['character']
    elif track=='K-ORDER':
        return {'status':'unknown','reason':'Free-text instance descriptions require qualified semantic/geometry binding; opaque source IDs are not model-answer targets',
                'formal_metric_eligible':False}
    elif track=='H-ACTUAL':
        expected=answer.get('observed_events')
        if expected is None:return {'status':'unknown','reason':'No independently observed event answer; construction log is not substituted'}
        correct=prediction.get('events')==expected
    else:return {'status':'unknown','reason':'Requires actual media or qualified geometry/event evaluation'}
    return {'status':'correct' if correct else 'incorrect','qualification':answer.get('qualification','development_only'),
            'formal_metric_eligible':False}
