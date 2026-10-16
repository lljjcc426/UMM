"""A template-assisted pixel probe, not a learned handwriting recognizer.

Render matched-final-image counterexamples and recover visible stroke events
from frames. The observer receives canonical geometry, never rendering events.
Only fixed-camera, opaque, straight strokes on a blank background are covered.
"""
from __future__ import annotations

import argparse
import json
import platform
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import PIL
from PIL import Image, ImageDraw


@dataclass(frozen=True)
class Stroke:
    id: str
    start: tuple[int, int]
    end: tuple[int, int]


def stroke_mask(stroke, size, width=7, begin=0.0, end=1.0):
    image = Image.new('L', size, 0)
    def point(t):
        return tuple(round(a + t * (b - a)) for a, b in zip(stroke.start, stroke.end))
    ImageDraw.Draw(image).line([point(begin), point(end)], fill=255, width=width)
    return np.asarray(image) > 0


def render(strokes, order, reverse=(), size=(160, 160), steps=12):
    by_id = {s.id: s for s in strokes}
    ink = np.zeros((size[1], size[0]), dtype=bool)
    frames = [np.full(ink.shape, 255, dtype=np.uint8)]
    for stroke_id in order:
        stroke = by_id[stroke_id]
        for step in range(1, steps + 1):
            progress = step / steps
            lo, hi = (1-progress, 1) if stroke_id in reverse else (0, progress)
            current = ink | stroke_mask(stroke, size, begin=lo, end=hi)
            frames.append(np.where(current, 0, 255).astype(np.uint8))
        ink |= stroke_mask(stroke, size)
        frames.extend([frames[-1].copy(), frames[-1].copy()])
    return np.stack(frames)


def first_at(values, threshold):
    indices = np.flatnonzero(values >= threshold)
    return int(indices[0]) if len(indices) else None


def observe(frames, strokes):
    """Read pixels using known instance masks and canonical endpoint regions.

    Onset ties and endpoint ties remain unknown. Exclusive masks avoid crediting
    a crossing pixel to both strokes. This is not suitable for arbitrary videos.
    """
    ink = np.asarray(frames) < 128
    size = (ink.shape[2], ink.shape[1])
    masks = np.stack([stroke_mask(s, size) for s in strokes])
    exclusive = masks & (masks.sum(axis=0) == 1)
    events = []
    for stroke, mask in zip(strokes, exclusive):
        coverage = ink[:, mask].mean(axis=1)
        onset = first_at(coverage, 0.05)
        complete = first_at(coverage, 0.98)
        start_region = mask & stroke_mask(stroke, size, end=0.2)
        end_region = mask & stroke_mask(stroke, size, begin=0.8)
        start_time = first_at(ink[:, start_region].mean(axis=1), 0.15)
        end_time = first_at(ink[:, end_region].mean(axis=1), 0.15)
        direction = None
        if start_time is not None and end_time is not None and start_time != end_time:
            direction = 'forward' if start_time < end_time else 'reverse'
        events.append(dict(id=stroke.id, onset_frame=onset, complete_frame=complete,
                           direction=direction, final_coverage=float(coverage[-1])))

    onsets = [e['onset_frame'] for e in events]
    observable = (all(t is not None and t > 0 for t in onsets)
                  and len(set(onsets)) == len(onsets))
    ordered = sorted(events, key=lambda e: e['onset_frame']) if observable else []
    sequence = [e['id'] for e in ordered] if observable else None
    sequence_exact = sequence == [s.id for s in strokes] if observable else None
    directions = [e['direction'] for e in events]
    direction_exact = (False if 'reverse' in directions else
                       None if None in directions else True)
    complete_before_next = None
    if observable:
        complete_before_next = all(
            a['complete_frame'] is not None and a['complete_frame'] < b['onset_frame']
            for a, b in zip(ordered, ordered[1:]))
    target = masks.any(axis=0)
    final = ink[-1]
    final_iou = float((target & final).sum() / (target | final).sum())
    geometry_complete = all(e['final_coverage'] >= 0.98 for e in events)
    checks = [sequence_exact, direction_exact, complete_before_next, geometry_complete]
    strict = False if False in checks else None if None in checks else True
    return dict(sequence=sequence, sequence_observable=observable,
                sequence_exact=sequence_exact, direction_exact=direction_exact,
                complete_before_next=complete_before_next, strict_process_correct=strict,
                final_ink_iou=final_iou, events=events)


def make_cases():
    ten = [Stroke('ten.horizontal', (32, 80), (128, 80)),
           Stroke('ten.vertical', (80, 28), (80, 132))]
    three = [Stroke('three.top', (48, 40), (112, 40)),
             Stroke('three.middle', (58, 78), (102, 78)),
             Stroke('three.bottom', (32, 120), (128, 120))]
    phrase = ten + [Stroke(s.id, (s.start[0]+160, s.start[1]),
                           (s.end[0]+160, s.end[1])) for s in three]
    cases = []
    def add(name, strokes, order=None, reverse=(), sparse=False):
        order = order or [s.id for s in strokes]
        frames = render(strokes, order, reverse, (320, 160) if strokes is phrase else (160, 160))
        if sparse:
            frames = frames[[0, -1]]
        cases.append((name, strokes, frames))
    add('ten_correct', ten)
    add('ten_swapped', ten, [ten[1].id, ten[0].id])
    add('ten_reverse_horizontal', ten, reverse=[ten[0].id])
    add('three_correct', three)
    add('three_swap_lower', three, [three[0].id, three[2].id, three[1].id])
    add('phrase_correct', phrase)
    add('phrase_interleaved', phrase, [phrase[i].id for i in [0, 2, 1, 3, 4]])
    add('ten_sparse', ten, sparse=True)
    return cases


def save_visuals(cases, output):
    selected = cases[:3]
    animation = []
    for t in range(len(selected[0][2])):
        image = Image.new('RGB', (480, 200), 'white')
        draw = ImageDraw.Draw(image)
        for j, (name, _, frames) in enumerate(selected):
            image.paste(Image.fromarray(frames[t]), (160*j, 30))
            draw.text((160*j+6, 8), name.replace('ten_', ''), fill='black')
        draw.text((6, 188), 'Same final pixels; different order or direction.', fill='black')
        animation.append(image)
    durations = [100] * len(animation)
    durations[-1] = 1500
    animation[0].save(output/'comparison.gif', save_all=True,
                      append_images=animation[1:], duration=durations, loop=0)
    samples = [0, 6, 12, 20, 28]
    sheet = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(sheet)
    for row, (name, _, frames) in enumerate(selected):
        for col, t in enumerate(samples):
            sheet.paste(Image.fromarray(frames[t]), (160*col, 200*row+30))
            draw.text((160*col+6, 200*row+10), f'{name}: f{t}', fill='black')
    sheet.save(output/'frames.png')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).resolve().parents[1]/'examples/process_probe')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    results = [dict(case=name, frames=len(frames), **observe(frames, strokes))
               for name, strokes, frames in cases]
    report = dict(kind='deterministic_pixel_probe_not_model_evaluation',
                  observer_inputs='frame pixels and canonical instance geometry; no rendering events',
                  environment=dict(python=platform.python_version(), numpy=np.__version__,
                                   pillow=PIL.__version__, machine=platform.machine()),
                  cases=results)
    (args.output/'results.json').write_text(json.dumps(report, indent=2)+'\n')
    save_visuals(cases, args.output)
    for r in results:
        print(r['case'], 'IoU=', r['final_ink_iou'], 'order=', r['sequence_exact'],
              'direction=', r['direction_exact'], 'strict=', r['strict_process_correct'])


if __name__ == '__main__':
    main()
