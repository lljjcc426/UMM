"""Separate visible plan execution from independently referenced normativity."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DeclaredPlan:
    plan_id: str
    order: tuple[str, ...]
    directions: dict[str, tuple[str, str]]


def _compare(evidence, plan):
    events = evidence['events']
    errors, unknown = [], []
    if evidence['all_blank']:
        errors.append('blank_output')
    if evidence['extra_ink']:
        errors.append('extra_visible_ink')
    if evidence['ink_disappeared']:
        errors.append('visible_ink_disappeared')
    if evidence['concurrent_growth']:
        errors.append('observable_concurrent_growth')
    if evidence['initial_ink_pixels']:
        unknown.append('nonblank_initial_frame')
    if not evidence['temporal_sampling_available']:
        unknown.append('insufficient_temporal_samples')
    if set(plan.order) != set(events):
        unknown.append('plan_geometry_identity_mismatch')
    for key in plan.order:
        e = events.get(key)
        if e is None or not e['geometry_observable']:
            unknown.append('unobservable_geometry:' + key)
            continue
        if e['final_coverage'] < evidence['completion_fraction']:
            errors.append('missing_or_incomplete:' + key)
        direction = plan.directions.get(key)
        if direction is None:
            unknown.append('unspecified_direction:' + key)
            continue
        a, b = [e['anchors'].get(name) for name in direction]
        if a is None or b is None or a['frame'] == b['frame']:
            unknown.append('unobservable_direction:' + key)
        elif a['frame'] > b['frame']:
            errors.append('opposite_visible_direction:' + key)
    for left, right in zip(plan.order, plan.order[1:]):
        a, b = events.get(left), events.get(right)
        if a is None or b is None or a['onset'] is None or b['onset'] is None:
            unknown.append('unobservable_order:' + left + ':' + right)
        elif a['onset']['frame'] > b['onset']['frame']:
            errors.append('order_conflict:' + left + ':' + right)
        elif a['onset']['frame'] == b['onset']['frame']:
            unknown.append('tied_visible_onsets:' + left + ':' + right)
        elif a['complete'] is None or a['complete']['frame'] >= b['onset']['frame']:
            unknown.append('completion_before_next_not_established:' + left + ':' + right)
    return dict(errors=sorted(set(errors)), unknown_reasons=sorted(set(unknown)))


def judge_execution(evidence, declared_plan):
    if declared_plan is None:
        return dict(decision='not_applicable', errors=[], unknown_reasons=['no_declared_plan'])
    result = _compare(evidence, declared_plan)
    return dict(decision='mismatch' if result['errors'] else 'unknown' if result['unknown_reasons'] else 'match',
                against_plan=declared_plan.plan_id, **result)


def normative_plan(reference):
    by_canonical = {i.canonical_id: i for i in reference.binding.items}
    items = [by_canonical[c] for c in reference.spec.canonical_order]
    return DeclaredPlan('norm:' + reference.spec.reference_id, tuple(i.instance_id for i in items),
                        {i.instance_id: (i.start_anchor, i.end_anchor) for i in items})


def judge_plan_normativity(declared_plan, reference):
    if reference.status != 'qualified':
        return 'unknown'
    expected = normative_plan(reference)
    return 'correct' if declared_plan.order == expected.order and declared_plan.directions == expected.directions else 'incorrect'


def judge_normative(evidence, reference):
    """No declared/source plan is accessible here; unqualified geometry cannot certify correctness."""
    if reference.status != 'qualified':
        # A blank T output is a confirmed task-content failure independent of a stroke binding.
        return dict(decision='incorrect' if evidence['all_blank'] else 'unknown',
            errors=['blank_output'] if evidence['all_blank'] else [],
            unknown_reasons=list(reference.reasons), reference_status=reference.status)
    result = _compare(evidence, normative_plan(reference))
    return dict(decision='incorrect' if result['errors'] else 'unknown' if result['unknown_reasons'] else 'correct',
                reference_status=reference.status, reference_id=reference.spec.reference_id,
                binding_id=reference.binding.binding_id, audit_level=reference.audit_level, **result)
