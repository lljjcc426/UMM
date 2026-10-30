"""Pinned-source geometry and synthetic RGB rendering, with no learned models."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageSequence, PngImagePlugin


def flatten_path(path):
    """Flatten the absolute M/L/Q/C/Z commands used in the selected source."""
    tokens = re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)', path)
    points, current, start = [], np.zeros(2), None
    index = 0
    arities = {'M': 2, 'L': 2, 'Q': 4, 'C': 6}
    while index < len(tokens):
        command = tokens[index]
        index += 1
        if command == 'Z':
            if start is not None:
                points.append(start.copy())
            continue
        if command not in arities:
            raise ValueError(f'Unsupported source path command {command}')
        count = arities[command]
        values = np.asarray([float(x) for x in tokens[index:index+count]]).reshape(-1, 2)
        index += count
        if command in ('M', 'L'):
            current = values[0]
            if command == 'M':
                start = current.copy()
            points.append(current.copy())
        else:
            for t in np.linspace(0, 1, 13)[1:]:
                if command == 'Q':
                    point = (1-t)**2*current + 2*(1-t)*t*values[0] + t*t*values[1]
                else:
                    point = ((1-t)**3*current + 3*(1-t)**2*t*values[0]
                             + 3*(1-t)*t*t*values[1] + t**3*values[2])
                points.append(point)
            current = values[-1]
    return np.asarray(points)


def transform(points, size):
    points = np.asarray(points, dtype=float).copy()
    points[:, 1] = 900-points[:, 1]
    return 10 + points*(size-20)/1024


def stroke_geometry(template, renderer='outline', size=128):
    masks, progress_maps = [], []
    yy, xx = np.mgrid[:size, :size]
    for path, median in zip(template['strokes'], template['medians']):
        outline = transform(flatten_path(path), size)
        center = transform(median, size)
        image = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(image)
        if renderer == 'outline':
            draw.polygon([tuple(p) for p in outline], fill=255)
        elif renderer == 'centerline':
            vertices = [tuple(p) for p in center]
            draw.line(vertices, fill=255, width=5, joint='curve')
            for x, y in [vertices[0], vertices[-1]]:
                draw.ellipse((x-2, y-2, x+2, y+2), fill=255)
        else:
            raise ValueError(renderer)
        mask = np.asarray(image) > 0
        lengths = np.linalg.norm(np.diff(center, axis=0), axis=1)
        total = lengths.sum()
        if total <= 0:
            raise ValueError('Zero-length median')
        best_distance = np.full((size, size), np.inf)
        progress = np.zeros((size, size), dtype=np.float32)
        cumulative = 0.
        for a, b, length in zip(center, center[1:], lengths):
            if length == 0:
                continue
            dx, dy = b-a
            fraction = np.clip(((xx-a[0])*dx+(yy-a[1])*dy)/(length*length), 0, 1)
            distance = (xx-a[0]-fraction*dx)**2+(yy-a[1]-fraction*dy)**2
            closer = distance < best_distance
            progress[closer] = ((cumulative+fraction*length)/total)[closer]
            best_distance[closer] = distance[closer]
            cumulative += length
        masks.append(mask)
        progress_maps.append(progress)
    return np.stack(masks), np.stack(progress_maps)


def render(template, renderer='outline', case='correct', size=128, steps=8):
    """Return pixels and construction events; observers never receive events."""
    masks, progress = stroke_geometry(template, renderer, size)
    n = len(masks)
    order = list(range(n))
    if case == 'swap':
        order[0], order[1] = order[1], order[0]
    if case == 'missing':
        order.pop()
    schedule = []
    cursor = 1
    for i, stroke in enumerate(order):
        onset = 1 if case == 'simultaneous' else cursor
        schedule.append(dict(stroke_index=stroke, start_frame=onset, end_frame=onset+steps-1,
                             reverse=case == 'reverse'))
        cursor += steps//2 if case == 'early_next' else steps+2
    count = max((e['end_frame'] for e in schedule), default=1)+4
    frames = np.full((count, size, size, 3), 255, dtype=np.uint8)
    for t in range(count):
        ink = np.zeros((size, size), dtype=bool)
        for event in schedule:
            fraction = np.clip((t-event['start_frame']+1)/steps, 0, 1)
            if fraction <= 0:
                continue
            j = event['stroke_index']
            amount = 1-progress[j] if event['reverse'] else progress[j]
            ink |= masks[j] & (amount <= fraction)
        if case == 'extra' and t >= count-3:
            ink[3:6, 3:17] = True
        if case == 'disappear' and t >= count-3:
            ink[masks[0] & (masks.sum(axis=0) == 1)] = False
        frames[t, ink] = 0
    if case in ('flash', 'sparse'):
        frames = frames[[0, -1]]
    if case == 'blank':
        frames[:] = 255
    return frames, schedule


def save_clip(path, frames, metadata, fps=12):
    """APNG retains exact RGB frames and per-frame durations without a codec."""
    info = PngImagePlugin.PngInfo()
    for key, value in metadata.items():
        info.add_text(key, str(value))
    images = [Image.fromarray(frame) for frame in frames]
    images[0].save(path, format='PNG', save_all=True, append_images=images[1:],
                   duration=round(1000/fps), loop=0, pnginfo=info, compress_level=1,
                   disposal=0, blend=0)


def read_clip(path):
    frames, durations = [], []
    with Image.open(path) as image:
        for frame in ImageSequence.Iterator(image):
            frames.append(np.asarray(frame.convert('RGB')).copy())
            durations.append(float(frame.info.get('duration', 0))/1000)
    times = np.concatenate([[0.], np.cumsum(durations[:-1])])
    return np.stack(frames), times, durations


def write_contact(path, named_frames):
    width = 128*5
    sheet = Image.new('RGB', (width, 154*len(named_frames)), '#eceef1')
    draw = ImageDraw.Draw(sheet)
    for row, (name, frames) in enumerate(named_frames):
        draw.text((8, row*154+4), name, fill='black')
        for col, i in enumerate(np.linspace(0, len(frames)-1, 5, dtype=int)):
            sheet.paste(Image.fromarray(frames[i]), (col*128, row*154+24))
    sheet.save(path)
