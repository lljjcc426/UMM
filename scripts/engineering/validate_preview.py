"""Save eight actual previews and five fault-injection cases, CPU only."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time
import uuid

import imageio_ffmpeg
import numpy as np

from hanzi_video.audit import audit_video
from hanzi_video.catalog import canonical_plan, load_catalog, reference
from hanzi_video.render import render_video


def main():
    output = Path('private/engineering_hanzi_video') / ('verification-' + uuid.uuid4().hex[:8])
    output.mkdir(parents=True)
    started = time.perf_counter()
    results, faults = [], []
    for char, ref in load_catalog()['characters'].items():
        path = output / (f'{ord(char):04x}.mp4')
        rendering = render_video(ref, canonical_plan(ref), path)
        audit = audit_video(path, ref)
        results.append({'character': char, 'video': str(path), 'rendering': rendering, 'audit': audit})
    ref = reference('士')
    for kind in ('wrong_order', 'reverse_direction', 'missing_stroke'):
        altered = deepcopy(ref)
        if kind == 'wrong_order':
            altered['sequence'].reverse()
        elif kind == 'reverse_direction':
            altered['sequence'][0]['direction'] = 'reverse'
        else:
            altered['sequence'].pop()
        path = output / f'fault-{kind}.mp4'
        render_video(altered, canonical_plan(altered), path, size=128)
        faults.append({'kind': kind, 'video': str(path), 'audit': audit_video(path, ref, size=128)})
    # Faults below alter actual encoded RGB, not the observer's expected events.
    # Use a native 128px reference render without rescaling the reference.
    native = output / 'fault-source.mp4'
    render_video(ref,canonical_plan(ref),native,size=128)
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(native),
        '-pix_fmt','rgb24','-f','rawvideo','pipe:1'],capture_output=True,check=True).stdout
    frames = np.frombuffer(raw,np.uint8).reshape(-1,128,128,3)
    for kind in ('flash', 'erasure'):
        altered = frames.copy()
        if kind == 'flash':
            altered[12:] = frames[-1]
        else:
            altered[-6:-3] = frames[0]
        path = output / f'fault-{kind}.mp4'
        writer = imageio_ffmpeg.write_frames(str(path),(128,128),fps=24,codec='libx264',
            output_params=['-crf','10'],ffmpeg_log_level='error')
        writer.send(None)
        for frame in altered:
            writer.send(frame)
        writer.close()
        faults.append({'kind':kind,'video':str(path),'audit':audit_video(path,ref,size=128)})
    result = {'created_at':datetime.now(timezone.utc).isoformat(), 'reference_version':load_catalog()['version'],
        'scope':'CPU controlled execution preview; no real UMM inference', 'model_calls':0, 'gpu_calls':0,
        'source_visual_comparison':'private/engineering_hanzi_video/reference_binding_comparison.png',
        'human_gold':False, 'output_directory':str(output), 'previews':results,'fault_injections':faults,
        'passed_previews':sum(r['audit']['passed'] for r in results),
        'rejected_faults':sum(not r['audit']['passed'] for r in faults),
        'elapsed_seconds':time.perf_counter()-started}
    destination = Path('data/engineering/hanzi_video_v1')
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('previews','fault_injections')},ensure_ascii=False,indent=2))
    if result['passed_previews'] != 8 or result['rejected_faults'] != 5:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
