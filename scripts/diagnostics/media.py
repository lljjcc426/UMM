"""Real FFmpeg encode/decode and PTS capture on CPU, with no interpolation."""
import hashlib
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
import numpy as np


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(path, frames, fps=12):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    h,w=frames.shape[1:3]
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-nostdin',
        '-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','pipe:0',
        '-an','-c:v','libx264','-crf','0','-pix_fmt','yuv444p',str(path)],
        input=frames.tobytes(),check=True,capture_output=True)


def decode(path, audit_directory=None):
    command=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','info','-nostdin','-i',str(path),
        '-map','0:v:0','-vf','showinfo','-vsync','0','-an','-f','rawvideo','-pix_fmt','rgb24','pipe:1']
    run=subprocess.run(command,
        capture_output=True,check=True)
    lines=run.stderr.decode(errors='replace')
    if audit_directory is not None:
        import json
        audit_directory=Path(audit_directory)
        (audit_directory/'decode_ffmpeg.log').write_text(lines)
        (audit_directory/'decode_command.json').write_text(json.dumps(command,indent=2)+'\n')
    records=re.findall(r' n:\s*\d+.*?pts_time:([\d.eE+\-]+).*? s:(\d+)x(\d+)',lines)
    if not records:
        raise ValueError('No decoded frame/PTS records')
    pts=np.array([float(r[0]) for r in records]);w,h=int(records[0][1]),int(records[0][2])
    frames=np.frombuffer(run.stdout,dtype=np.uint8).reshape(-1,h,w,3).copy()
    if len(frames)!=len(pts) or (len(pts)>1 and np.any(np.diff(pts)<=0)):
        raise ValueError('Frame count or monotone PTS failure')
    return frames,pts


def validate_media(kind, frames=None, pts=None, expected_count=None):
    if kind == 'interleaved_images':
        return {'kind':kind,'dense_video_eligible':False,'reason':'Image states have no native temporal evidence'}
    if kind == 'static_image':
        return {'kind':kind,'dense_video_eligible':False,'reason':'Static output is a separate task'}
    if kind!='native_video' or frames is None or pts is None:
        raise ValueError('Native video requires decoded frames and actual PTS')
    if len(frames)!=len(pts) or len(pts)<2 or np.any(np.diff(pts)<=0):
        raise ValueError('Incomplete or unordered native video')
    if expected_count is not None and len(frames)!=expected_count:
        raise ValueError('Missing native frames')
    return {'kind':kind,'dense_video_eligible':True,'frames':len(frames),'size':[frames.shape[2],frames.shape[1]],
            'PTS':np.asarray(pts).tolist(),'nominal_end_PTS':float(pts[-1])}
