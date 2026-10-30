"""G1 reference-geometry observer; inputs are decoded RGB and canonical masks.

Renderer schedules, sample names, injected-case labels, target event times and
future frames for a prefix task are absent from the observation API.
"""
from __future__ import annotations

import numpy as np


DEFAULT_THRESHOLDS = dict(ink=128, onset=.04, complete=.96, region=.12,
                          minimum_exclusive_pixels=10, minimum_region_pixels=3,
                          extra_ink_pixels=12, disappeared_pixels=12)


def first_true(values):
    indexes = np.flatnonzero(values)
    return int(indexes[0]) if len(indexes) else None


def observe(frames, masks, progress, thresholds=None):
    thresholds = DEFAULT_THRESHOLDS if thresholds is None else thresholds
    ink = np.asarray(frames).min(axis=-1) < thresholds['ink']
    target = masks.any(axis=0)
    exclusive = masks & (masks.sum(axis=0) == 1)
    events, reasons, certain_errors = [], [], []
    if bool(ink[0].any()):
        reasons.append('nonblank_initial_frame')
    outside = (ink & ~target).sum(axis=(1, 2))
    if int(outside.max()) > thresholds['extra_ink_pixels']:
        certain_errors.append('extra_visible_ink')
    lost = (ink[:-1] & ~ink[1:]).sum(axis=(1, 2)) if len(ink)>1 else np.array([0])
    if int(lost.max()) > thresholds['disappeared_pixels']:
        certain_errors.append('visible_ink_disappeared')
    for i, mask in enumerate(exclusive):
        area = int(mask.sum())
        event = dict(stroke_index=i, exclusive_pixels=area, onset=None, complete=None,
                     direction='unknown', final_coverage=None)
        if area < thresholds['minimum_exclusive_pixels']:
            reasons.append(f'insufficient_exclusive_geometry:{i}')
            events.append(event)
            continue
        coverage = ink[:, mask].mean(axis=1)
        event.update(onset=first_true(coverage >= thresholds['onset']),
                     complete=first_true(coverage >= thresholds['complete']),
                     final_coverage=float(coverage[-1]))
        if coverage[-1] < thresholds['complete']:
            certain_errors.append(f'missing_or_incomplete_stroke:{i}')
        # Endpoint regions use canonical arc progress, independent of event time.
        lo, hi = np.quantile(progress[i][mask], [.22, .78])
        start_mask = mask & (progress[i] <= lo)
        end_mask = mask & (progress[i] >= hi)
        if min(int(start_mask.sum()), int(end_mask.sum())) >= thresholds['minimum_region_pixels']:
            start = first_true(ink[:, start_mask].mean(axis=1) >= thresholds['region'])
            end = first_true(ink[:, end_mask].mean(axis=1) >= thresholds['region'])
            event.update(start_region_frame=start, end_region_frame=end)
            if start is not None and end is not None:
                event['direction'] = 'forward' if start < end else 'reverse' if end < start else 'unknown'
                if end < start:
                    certain_errors.append(f'reverse_visible_direction:{i}')
            if event['direction'] == 'unknown':
                reasons.append(f'direction_not_observable:{i}')
        else:
            reasons.append(f'endpoint_regions_not_observable:{i}')
        events.append(event)
    onsets = [e['onset'] for e in events]
    complete = [e['complete'] for e in events]
    if all(t is not None for t in onsets):
        if len(set(onsets)) == len(onsets):
            order = sorted(range(len(events)), key=lambda i: onsets[i])
            if order != list(range(len(events))):
                certain_errors.append('wrong_instance_order')
        else:
            order = None
            reasons.append('tied_visible_onsets')
        # Same-frame jumps do not prove physical overlap. Multiple frames of
        # concurrent partial growth do provide observable overlap evidence.
        partial = np.zeros(len(ink), dtype=int)
        for e in events:
            if e['onset'] is not None and e['complete'] is not None:
                partial[e['onset']:e['complete']] += 1
        if int((partial > 1).sum()) >= 2:
            certain_errors.append('observable_concurrent_growth')
        if order is not None:
            for a, b in zip(order, order[1:]):
                if complete[a] is None or complete[a] >= onsets[b]:
                    reasons.append('completion_before_next_not_established')
    else:
        order = None
        reasons.append('missing_visible_onset')
    if len(ink)<3:
        reasons.append('insufficient_temporal_samples')
    if certain_errors:
        decision = 'incorrect'
    elif reasons:
        decision = 'unknown'
    else:
        decision = 'correct'
    intersection = int((ink[-1] & target).sum())
    union = int((ink[-1] | target).sum())
    return dict(decision=decision, errors=sorted(set(certain_errors)),
                unknown_reasons=sorted(set(reasons)), observed_order=order,
                events=events, final_iou=intersection/union if union else None)


def model_input(sample, frames, timestamps, protocol='T', prefix_end=None):
    """Construct a minimal input allowlist; evaluation/training fields stay out."""
    result = dict(character=sample['character'], instruction='按规范笔顺逐笔书写这个汉字。')
    if protocol == 'P':
        if prefix_end is None:
            raise ValueError('P requires prefix_end')
        keep = np.asarray(timestamps) <= prefix_end
        result.update(prefix_rgb=np.asarray(frames)[keep], prefix_timestamps=np.asarray(timestamps)[keep])
    elif protocol != 'T':
        raise ValueError('This adapter implements the approved T/P inputs only')
    return result


def one_sided_upper(k, n, alpha=.05):
    """Exact one-sided binomial bound, using stdlib arithmetic and bisection."""
    import math
    if n == 0:
        return None
    if k == n:
        return 1.
    def cdf(p):
        return sum(math.comb(n, j)*p**j*(1-p)**(n-j) for j in range(k+1))
    lo, hi = 0., 1.
    for _ in range(60):
        mid = (lo+hi)/2
        if cdf(mid) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2
