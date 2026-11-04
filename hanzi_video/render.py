"""Monotone CPU mask executor shared by the catalog and raw program routes."""
import time
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image

from scripts.p0.geometry import stroke_geometry
from .catalog import geometry, validate_plan


def mask_frames(masks, progress, durations, opening, closing, pause_frames=0):
    """Execute the supplied masks/order without a character or catalog lookup."""
    h, w = masks.shape[-2:]
    ink = np.zeros((h, w), dtype=bool)

    def rgb():
        frame = np.full((h, w, 3), 255, dtype=np.uint8)
        frame[ink] = 0
        return frame

    for _ in range(opening):
        yield rgb()
    for mask, distance, steps in zip(masks, progress, durations):
        for step in range(1, steps + 1):
            ink |= mask & (distance <= step / steps)
            yield rgb()
        for _ in range(pause_frames):
            yield rgb()
    for _ in range(closing):
        yield rgb()


def render_masks_video(masks, progress, destination, *, fps, durations, opening, closing, pause_frames=0):
    """Low-level renderer. Program validation and permissions belong upstream."""
    started = time.perf_counter()
    h, w = masks.shape[-2:]
    writer = imageio_ffmpeg.write_frames(str(destination), (w, h), fps=fps,
        codec='libx264', pix_fmt_in='rgb24', pix_fmt_out='yuv420p',
        output_params=['-crf', '10', '-preset', 'fast', '-movflags', '+faststart'],
        macro_block_size=1, ffmpeg_log_level='error')
    writer.send(None)
    frames = 0
    try:
        for frame in mask_frames(masks, progress, durations, opening, closing, pause_frames):
            writer.send(frame)
            frames += 1
    finally:
        writer.close()
    Image.fromarray(frame).save(Path(destination).with_suffix('.png'))
    return {'frames': frames, 'size': [w, h], 'fps': fps, 'duration_seconds': frames / fps,
            'cpu_elapsed_seconds': time.perf_counter() - started}


def render_video(ref, plan, destination, size=512, fps=24, speed=1.0):
    started = time.perf_counter()
    errors = validate_plan(plan, ref)
    if errors:
        raise ValueError('；'.join(errors))
    masks, progress = stroke_geometry(geometry(ref), size=size)
    write_frames = max(8, round(.75 * fps / speed))
    pause_frames = max(2, round(.18 * fps / speed))
    opening, closing = round(.5 * fps), round(.8 * fps)
    report = render_masks_video(masks, progress, destination, fps=fps,
        durations=[write_frames] * len(masks), opening=opening, closing=closing, pause_frames=pause_frames)
    report['schedule'] = [{'stroke_id': row['id'],
        'first_frame': opening + i * (write_frames + pause_frames),
        'last_frame': opening + i * (write_frames + pause_frames) + write_frames - 1}
        for i, row in enumerate(ref['sequence'])]
    report['cpu_elapsed_seconds'] = time.perf_counter() - started
    return report
