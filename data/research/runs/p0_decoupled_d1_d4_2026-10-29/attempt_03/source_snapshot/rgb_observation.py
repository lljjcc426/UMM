"""RGB evidence on an unordered G1 geometry set, without a normative plan."""
from dataclasses import dataclass

import numpy as np

from scripts.p0.observer import DEFAULT_THRESHOLDS


@dataclass(frozen=True)
class GeometryInstance:
    instance_id: str
    mask: np.ndarray
    anchors: dict[str, np.ndarray]


def observe_rgb(frames, timestamps, geometry_set, observation_config=None):
    """Extract pixel evidence; anchor names and container position have no order semantics."""
    cfg = DEFAULT_THRESHOLDS if observation_config is None else observation_config
    frames = np.asarray(frames)
    times = np.asarray(timestamps, float)
    if frames.ndim != 4 or len(frames) != len(times) or not len(times) or np.any(np.diff(times) <= 0):
        raise ValueError('Expected RGB frames and strictly increasing sampling timestamps')
    ids = [g.instance_id for g in geometry_set]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError('Geometry instance IDs must be unique and nonempty')
    ink = frames.min(axis=-1) < cfg['ink']
    masks = np.asarray([g.mask for g in geometry_set], bool)
    exclusive = masks & (masks.sum(axis=0) == 1)
    target = masks.any(axis=0)
    events = {}

    def hit(values):
        indexes = np.flatnonzero(values)
        if not len(indexes):
            return None
        k = int(indexes[0])
        return dict(frame=k, interval=[float(times[k-1]) if k else None, float(times[k])])

    for g, region in zip(geometry_set, exclusive):
        area = int(region.sum())
        e = dict(exclusive_pixels=area, onset=None, complete=None, final_coverage=None,
                 anchors={}, geometry_observable=area >= cfg['minimum_exclusive_pixels'])
        if e['geometry_observable']:
            coverage = ink[:, region].mean(axis=1)
            e.update(onset=hit(coverage >= cfg['onset']), complete=hit(coverage >= cfg['complete']),
                     final_coverage=float(coverage[-1]))
            for name, anchor in g.anchors.items():
                anchor = anchor & region
                e['anchors'][name] = (hit(ink[:, anchor].mean(axis=1) >= cfg['region'])
                    if anchor.sum() >= cfg['minimum_region_pixels'] else None)
        events[g.instance_id] = e
    partial = np.zeros(len(frames), int)
    for e in events.values():
        if e['onset'] is not None and e['complete'] is not None:
            partial[e['onset']['frame']:e['complete']['frame']] += 1
    outside = (ink & ~target).sum(axis=(1, 2))
    lost = (ink[:-1] & ~ink[1:]).sum(axis=(1, 2)) if len(ink) > 1 else np.array([0])
    intersection = int((ink[-1] & target).sum())
    union = int((ink[-1] | target).sum())
    return dict(schema='p0-rgb-evidence-v1', events=events, frame_count=len(frames),
        timestamps=times.tolist(), temporal_sampling_available=len(frames) >= 3,
        completion_fraction=cfg['complete'],
        initial_ink_pixels=int(ink[0].sum()), all_blank=not bool(ink.any()),
        extra_ink=bool(outside.max() > cfg['extra_ink_pixels']),
        ink_disappeared=bool(lost.max() > cfg['disappeared_pixels']),
        concurrent_growth=bool((partial > 1).sum() >= 2),
        maximum_outside_pixels=int(outside.max()), maximum_lost_pixels=int(lost.max()),
        concurrent_partial_frames=int((partial > 1).sum()), final_iou=intersection/union if union else None)
