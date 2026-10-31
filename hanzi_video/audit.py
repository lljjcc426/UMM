"""Read actual MP4 RGB/PTS; inspect reference landmarks without renderer events.

This is a constrained-executor check against the same trusted reference, not a
general observer or evidence that the reference itself is normatively correct.
"""
import re
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageFilter

from scripts.p0.geometry import stroke_geometry, transform
from .catalog import geometry


def audit_video(path, ref, size=512, fps=24):
    template = geometry(ref)
    masks, _ = stroke_geometry(template, size=size)
    union = masks.any(axis=0)
    allowed = np.asarray(Image.fromarray(union).filter(ImageFilter.MaxFilter(3))) > 0
    probes = []
    # Independently interpolate center-line landmarks, without reveal maps/events.
    for mask, median in zip(masks, template['medians']):
        center = transform(median, size)
        lengths = np.r_[0, np.cumsum(np.linalg.norm(np.diff(center, axis=0), axis=1))]
        exclusive = mask & (masks.sum(axis=0) == 1)
        points = []
        for fraction in np.linspace(.08, .92, 13):
            xy = [np.interp(fraction * lengths[-1], lengths, center[:, i]) for i in (0, 1)]
            x, y = np.rint(xy).astype(int)
            patch = np.zeros_like(mask)
            patch[max(0, y-2):y+3, max(0, x-2):x+3] = True
            selected = np.flatnonzero(patch & exclusive)
            if len(selected) >= 3:
                points.append(selected)
        probes.append(points)
    arrivals = [[None] * len(points) for points in probes]
    ever = np.zeros_like(union)
    max_erasure, max_extra, count = 0, 0, 0
    first_blank, last = False, ever
    frame_bytes = size * size * 3
    with tempfile.TemporaryFile() as log:
        process = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-i', str(path),
            '-vf', 'showinfo', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'],
            stdout=subprocess.PIPE, stderr=log)
        try:
            while True:
                raw = process.stdout.read(frame_bytes)
                if not raw:
                    break
                if len(raw) != frame_bytes:
                    raise ValueError('视频帧尺寸或数据不完整')
                rgb = np.frombuffer(raw, np.uint8).reshape(size, size, 3)
                ink = rgb.mean(axis=2) < 96
                if count == 0:
                    first_blank = not ink.any()
                max_erasure = max(max_erasure, int((ever & ~ink).sum()))
                max_extra = max(max_extra, int((ink & ~allowed).sum()))
                flat = ink.ravel()
                for si, points in enumerate(probes):
                    for pi, pixels in enumerate(points):
                        if arrivals[si][pi] is None and flat[pixels].mean() >= .5:
                            arrivals[si][pi] = count
                ever |= ink
                last = ink
                count += 1
        finally:
            process.stdout.close()
            code = process.wait()
        log.seek(0)
        diagnostic = log.read().decode(errors='replace')
    pts = [float(x) for x in re.findall(r'\bn:\s*\d+\s+pts:\s*\S+\s+pts_time:([\d.e+-]+)', diagnostic)]
    shapes = re.findall(r'\bs:(\d+)x(\d+)\b', diagnostic)
    errors = []
    if code or not count:
        errors.append('视频无法完整解码')
    if not shapes or any(s != (str(size), str(size)) for s in shapes):
        errors.append('视频尺寸错误')
    if len(pts) != count or any(abs(t - i/fps) > .0001 for i, t in enumerate(pts)):
        errors.append('PTS或帧率不符合约定')
    if not first_blank:
        errors.append('视频未从空白开始')
    completeness = float((last & union).sum() / max(1, union.sum()))
    if completeness < .995:
        errors.append('最终笔画不完整')
    if max_erasure > max(3, round(union.sum() * .001)):
        errors.append('已有墨迹消失')
    if max_extra > 3:
        errors.append('出现参考字形之外的墨迹')
    previous_end = -1
    for si, times in enumerate(arrivals):
        if len(times) < 5 or any(t is None for t in times):
            errors.append(f'第{si+1}笔的可观察证据不足')
            continue
        if any(b < a-1 for a, b in zip(times, times[1:])) or times[-1] <= times[0]:
            errors.append(f'第{si+1}笔方向或中途行笔错误')
        if times[0] < previous_end:
            errors.append(f'第{si+1}笔提前或顺序错误')
        if len(set(times)) < 5 or times[-1] - times[0] < max(3, round(fps*.2)):
            errors.append(f'第{si+1}笔缺少可见书写过程')
        previous_end = max(times)
    return {'passed': not errors, 'errors': errors, 'decoded_frames': count, 'pts_seconds': pts,
            'dimensions': [size, size], 'fps': fps, 'blank_first_frame': first_blank,
            'final_completeness': completeness, 'max_erased_pixels': max_erasure,
            'max_extra_pixels': max_extra, 'landmark_first_frames': arrivals,
            'renderer_event_log_used': False, 'independent_normative_gold': False}
