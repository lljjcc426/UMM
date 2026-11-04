"""Small safe drawing DSL + CPU renderer. No Python execution from model output."""
from dataclasses import dataclass
import json
import math
from pathlib import Path
import time

import numpy as np


@dataclass(frozen=True)
class Stroke:
    order: int
    stroke_type: int
    path: tuple[tuple[float, float], ...]
    width: float
    frames: int


@dataclass(frozen=True)
class Program:
    canvas: tuple[int, int]
    strokes: tuple[Stroke, ...]
    fps: int = 24


def parse_program(value) -> Program:
    """Accept only a bounded, declarative JSON schema; no commands, imports, URLs."""
    if isinstance(value, (str, bytes)):
        value = json.loads(value)
    if not isinstance(value, dict) or set(value) != {'version', 'canvas', 'fps', 'strokes'} or value['version'] != 1:
        raise ValueError('Invalid program schema/version')
    canvas = value['canvas']
    if (not isinstance(canvas, list) or len(canvas) != 2 or any(type(n) != int or n < 64 or n > 1024 for n in canvas)
            or any(n % 2 for n in canvas)):
        raise ValueError('Canvas must have even 64..1024 dimensions')
    if type(value['fps']) != int or value['fps'] < 6 or value['fps'] > 60:
        raise ValueError('Invalid frame rate')
    rows = value['strokes']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 64:
        raise ValueError('A program requires 1..64 strokes')
    strokes = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or set(row) != {'order', 'type', 'path', 'width', 'frames'}:
            raise ValueError('Invalid stroke schema')
        if type(row['order']) != int or row['order'] != index:
            raise ValueError('Stroke order must be consecutive as emitted by the model')
        if type(row['type']) != int or not 1 <= row['type'] <= 5:
            raise ValueError('Invalid five-class stroke type')
        pts = row['path']
        if not isinstance(pts, list) or not 2 <= len(pts) <= 128:
            raise ValueError('Invalid path length')
        for p in pts:
            if (not isinstance(p, list) or len(p) != 2 or
                any(type(c) not in (float, int) or not math.isfinite(c) or c < 0 or c > 1 for c in p)):
                raise ValueError('Path must contain finite normalized points')
        if not math.isfinite(sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))) or sum(
            math.dist(p, q) for p, q in zip(pts, pts[1:])) < 0.005:
            raise ValueError('Degenerate stroke')
        width, frames = row['width'], row['frames']
        if type(width) not in (int, float) or not math.isfinite(width) or not 0.002 <= width <= 0.12:
            raise ValueError('Invalid stroke width')
        if type(frames) != int or not 2 <= frames <= 120:
            raise ValueError('Invalid frame count')
        strokes.append(Stroke(index, row['type'], tuple(map(tuple, pts)), width, frames))
    return Program(tuple(canvas), tuple(strokes), value['fps'])


def program_geometry(program: Program):
    """Convert only the supplied paths to the repository's source coordinates.

    No character, reference SVG, instance identities or expected sequence is
    available to this route. It preserves the program's emitted order.
    """
    from scripts.p0.geometry import stroke_geometry
    strokes, medians, widths = [], [], []
    canvas = np.asarray(program.canvas)
    for stroke in program.strokes:
        points = np.asarray(stroke.path) * (canvas - 1)
        source = (points - 10) * 1024 / (canvas - 20)
        source[:, 1] = 900 - source[:, 1]
        medians.append(source.tolist())
        strokes.append('M ' + ' L '.join(f'{x:.14f} {y:.14f}' for x, y in source) + ' Z')
        widths.append(max(1, round(stroke.width * min(program.canvas))))
    return stroke_geometry({'strokes': strokes, 'medians': medians},
                           renderer='centerline', size=program.canvas, centerline_widths=widths)


def render_frames(program: Program, intro=4, outro=4):
    from hanzi_video.render import mask_frames
    masks, progress = program_geometry(program)
    yield from mask_frames(masks, progress, [s.frames for s in program.strokes], intro, outro)


def save_mp4(program: Program, path: Path) -> dict:
    from hanzi_video.render import render_masks_video
    path = Path(path)
    if path.exists():
        raise FileExistsError('Run output must be a new path')
    path.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    masks, progress = program_geometry(program)
    result = render_masks_video(masks, progress, path, fps=program.fps,
        durations=[s.frames for s in program.strokes], opening=4, closing=4)
    return {'frames': result['frames'], 'fps': program.fps, 'canvas': list(program.canvas),
            'seconds': time.perf_counter() - started, 'bytes': path.stat().st_size,
            'generator': 'CPU shared renderer; input program supplied externally',
            'model_generated': False, 'normative_order_independently_verified': False}


def audit_mp4(path: Path) -> dict:
    """Observe decoded RGB, without a reference or renderer event log."""
    import imageio_ffmpeg
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt='rgb24')
    try:
        metadata = next(reader)
        w, h = metadata['size']
        previous, count, max_erased, first_blank = None, 0, 0, False
        for raw in reader:
            rgb = np.frombuffer(raw, dtype=np.uint8).reshape(h, w, 3)
            ink = rgb.mean(axis=2) < 100
            if previous is None:
                first_blank = not bool(ink.any())
            else:
                max_erased = max(max_erased, int((previous & ~ink).sum()))
            previous, count = ink, count + 1
    finally:
        reader.close()
    if count == 0:
        raise ValueError('No decoded frames')
    return {'decoded_frames': count, 'dimensions': [h, w], 'blank_first': first_blank,
            'final_ink_pixels': int(previous.sum()), 'max_erased_pixels': max_erased,
            'normative_order_independently_verified': False,
            'uses_renderer_event_log_for_metrics': False}


def order_signature(program: Program) -> tuple[int, ...]:
    return tuple(s.stroke_type for s in program.strokes)
