"""Monotone, one-stroke-at-a-time executor. No model-drawn RGB."""
import time
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image

from scripts.p0.geometry import stroke_geometry
from .catalog import geometry, validate_plan


def render_video(ref, plan, destination, size=512, fps=24, speed=1.0):
    errors = validate_plan(plan, ref)
    if errors:
        raise ValueError('；'.join(errors))
    started = time.perf_counter()
    masks, progress = stroke_geometry(geometry(ref), size=size)
    write_frames = max(8, round(.75 * fps / speed))
    pause_frames = max(2, round(.18 * fps / speed))
    opening, closing = round(.5 * fps), round(.8 * fps)
    writer = imageio_ffmpeg.write_frames(str(destination), (size, size), fps=fps,
        codec='libx264', pix_fmt_in='rgb24', pix_fmt_out='yuv420p',
        output_params=['-crf', '10', '-preset', 'fast', '-movflags', '+faststart'],
        macro_block_size=1, ffmpeg_log_level='error')
    writer.send(None)
    ink = np.zeros((size, size), dtype=bool)
    frames, schedule = 0, []

    def send():
        nonlocal frames
        rgb = np.full((size, size, 3), 255, dtype=np.uint8)
        rgb[ink] = 0
        writer.send(rgb)
        frames += 1

    try:
        for _ in range(opening):
            send()
        for index, (mask, distance) in enumerate(zip(masks, progress)):
            first = frames
            for step in range(1, write_frames + 1):
                ink |= mask & (distance <= step / write_frames)
                send()
            schedule.append({'stroke_id': ref['sequence'][index]['id'],
                             'first_frame': first, 'last_frame': frames - 1})
            for _ in range(pause_frames):
                send()
        for _ in range(closing):
            send()
    finally:
        writer.close()
    Image.fromarray(np.where(ink[..., None], 0, 255).astype('uint8').repeat(3, axis=2)).save(
        Path(destination).with_suffix('.png'))
    return {'frames': frames, 'size': [size, size], 'fps': fps,
            'duration_seconds': frames / fps, 'schedule': schedule,
            'cpu_elapsed_seconds': time.perf_counter() - started}
