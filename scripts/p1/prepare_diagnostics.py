"""Materialize the authorized CPU controls and frozen SO-01 inputs, without a model call."""
import copy
import json
from pathlib import Path
import shutil
import subprocess

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

from scripts.p0.evaluate_decoupled import load_inputs, geometry_for
from scripts.p0.final_calibration import draw_stroke, prefix_points
from scripts.p1.full_common import input_fingerprint, sha256

PUBLIC = Path('data/research/runs/p1_full_server_2026-10-30')
PRIVATE = Path('private/p1_full_server_2026-10-30')
PAYLOAD = PRIVATE / 'diagnostics'
CLOUD = Path('/root/umm-p1-full-20261030')


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def encode(path, frames, fps, lossless=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-f', 'rawvideo', '-pixel_format', 'rgb24',
               '-video_size', f'{frames.shape[2]}x{frames.shape[1]}', '-framerate', str(fps), '-i', '-', '-an']
    if lossless:
        command += ['-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'bgr0']
    else:
        command += ['-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p']
    # No -y: existing evidence must never be overwritten.
    subprocess.run(command + [str(path)], input=frames.tobytes(), check=True)


def render(strokes, total=132, order=None, completed_count=None):
    order = list(range(len(strokes))) if order is None else order
    result = []
    stages = []
    for stroke in strokes:
        full = Image.new('L', (128, 128), 0)
        draw_stroke(ImageDraw.Draw(full), stroke, 255)
        stages.append(np.asarray(full) > 0)
    n = len(strokes) if completed_count is None else completed_count
    # 4 opening blank frames, 4 closing frames; equal synthetic stroke time.
    boundaries = np.linspace(4, total-4, n+1)
    for t in range(total):
        ink = np.zeros((128, 128), bool)
        for rank, index in enumerate(order[:n]):
            fraction = float(np.clip((t-boundaries[rank]) / (boundaries[rank+1]-boundaries[rank]-1), 0, 1))
            if fraction <= 0:
                continue
            if fraction >= 1:
                ink |= stages[index]
            else:
                im = Image.new('L', (128, 128), 0)
                draw_stroke(ImageDraw.Draw(im), prefix_points(strokes[index], fraction), 255)
                ink |= (np.asarray(im)>0) & stages[index]
        im = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)).resize((848, 480), Image.Resampling.NEAREST)
        result.append(np.asarray(im.convert('RGB')))
    return np.stack(result), boundaries.tolist()


def main():
    if PAYLOAD.exists():
        raise ValueError('Diagnostics already materialized; preserve them instead of regenerating')
    PAYLOAD.mkdir(parents=True)
    manifest = json.loads((PUBLIC/'manifest_initial.json').read_text())
    tasks, _, _ = load_inputs()
    audit = json.loads(Path('data/research/runs/p0_decoupled_d1_d4_2026-10-29/static_qualification_audit.json').read_text())
    control_data = {}
    for row in manifest['controls']:
        nid = row['norm_id']; task = tasks[nid]
        _, axes, _, _ = geometry_for(task)
        bindings = sorted(audit[nid]['review_records'], key=lambda r:r['normative_position'])
        strokes = []
        for binding in bindings:
            assert binding['identity_status'] == binding['direction_status'] == 'verified'
            stroke = np.asarray(task['strokes'][binding['source_stroke_number']-1], float)
            if axes[binding['instance_id']][0] != binding['start_anchor']:
                stroke = stroke[::-1]
            strokes.append(stroke)
        frames, boundaries = render(strokes)
        directory = PAYLOAD/'controls'/row['id'];directory.mkdir(parents=True)
        native = frames[np.arange(33)*4]
        np.savez_compressed(directory/'source_RGB_48fps.npz', frames=frames)
        np.savez_compressed(directory/'native_RGB_12fps.npz', frames=native)
        encode(directory/'source_48fps.mkv', frames, 48, lossless=True)
        encode(directory/'control.mp4', native, 12)
        evidence = dict(id=row['id'],norm_id=nid,character=task['character'],formal_geometry_gold=False,
            qualification='official GF0023-2020 reference plus existing overall human reviews and explicit AI development bindings; not per-stroke human gold',
            binding_records=bindings, oriented_strokes=[s.tolist() for s in strokes],
            synthetic_timing=dict(source_frames=132,source_fps=48,native_frames=33,native_fps=12,
                native_source_indices=(np.arange(33)*4).tolist(),stroke_boundaries_source_frames=boundaries),
            geometry='CASIA development paths rasterized at128 then stretched to848x480; exact O geometry permission',
            source_order_is_normative_truth=False,physical_writer_timing=False)
        save(directory/'construction.json',evidence)
        row.update(source_file=f'controls/{row["id"]}/source_48fps.mkv',native_file=f'controls/{row["id"]}/control.mp4',
                   source_sha256=sha256(directory/'source_48fps.mkv'),native_sha256=sha256(directory/'control.mp4'))
        control_data[nid] = (strokes, frames, boundaries, task['character'])
    question = ('Describe only the visible RGB evidence for the intended Chinese character {character}. '
        'State the observed order and visible travel directions of strokes, completed and active strokes, '
        'the earliest directly observable anomaly with approximate time, and uncertainty. '
        'Do not substitute the standard writing order for observed events; report when motion cannot be determined.')
    condition_audits=[]
    for row in manifest['understanding']:
        nid=row['norm_id'];condition=row['condition'];strokes,source,boundaries,char=control_data[nid]
        if row['source']=='controlled_prefix':
            # Freeze at completion of stroke 2, before any pixel of stroke 3.
            end=int(np.ceil(boundaries[2]))
            indices=np.arange(0,end,4)
            prefix=source[indices].copy()
            # Last frame is made exactly complete by selecting the pre-transition frame.
            if not np.array_equal(prefix[-1], source[end-1]):
                prefix=np.concatenate([prefix,source[end-1:end]])
                indices=np.r_[indices,end-1]
            a=dict(id=row['id'], source_indices=indices.tolist(), fps=12,source_prefix_stop_exclusive=end,
                   future_frames_supplied=False, terminal_frame_policy='append exact pre-transition frame if needed; synthetic diagnostic timing')
            if condition=='last_frame':
                frames=np.repeat(prefix[-1:],[len(prefix)],axis=0)
            elif condition in ['relevant_occlusion','irrelevant_occlusion']:
                frames=prefix.copy();yy,xx=np.nonzero(prefix[-1,:,:,0]<128)
                # Deterministic fixed 96x96 region; unrelated area is searched using this prefix only.
                side=96
                if condition=='relevant_occlusion':
                    y=int(np.clip(np.median(yy)-side//2,0,480-side));x=int(np.clip(np.median(xx)-side//2,0,848-side))
                else:
                    y,x=next((y,x) for y in range(0,480-side+1,16) for x in range(0,848-side+1,16)
                             if np.all(prefix[:,:, :,0][:,y:y+side,x:x+side]==255))
                frames[:,y:y+side,x:x+side]=255
                a.update(occlusion_xywh=[x,y,side,side],occluded_area_pixels=side*side,time_frame_interval=[0,len(prefix)-1])
            elif condition=='alternate_history':
                alternate,_=render(strokes,total=end,order=[1,0],completed_count=2)
                frames=alternate[indices].copy()
                assert np.array_equal(frames[-1],prefix[-1]), 'Same-final-frame control is not exact'
                assert not np.array_equal(frames,prefix), 'Histories must differ'
                a.update(construction='new monotone drawing of the same first two bound strokes in swapped order; not shuffled real frames',
                         identical_final_RGB=True,different_history_RGB=True)
            else:frames=prefix
        else:
            old=Path('private/p1_native_pilot_issue3_2026-10-30/requests')/row['source_request_id']
            decoded=next(old.glob('runs/*/t2v/decoded_rgb_uint8.npz'))
            source_video=next(old.glob('runs/*/t2v/outputs/*.mp4'))
            frames=np.load(decoded)['frames']
            a=dict(id=row['id'],source_request_id=row['source_request_id'],original_MP4_sha256=sha256(source_video),
                   source_indices=list(range(len(frames))),fps=12,future_frames_supplied=False,
                   selection='predeclared pilot simple-s11 IDs; prior AI exposure disclosed')
            if condition=='last_frame':frames=np.repeat(frames[-1:],[len(frames)],axis=0)
        bundle=PAYLOAD/'bundles'/row['id'];inputs=bundle/'inputs';inputs.mkdir(parents=True)
        encode(inputs/'visible.mkv',frames,12,lossless=True)
        sample={'0001':{'interleave_array':[str((inputs/'visible.mkv').resolve()),
            ['Answer from visible video evidence only.',question.format(character=char),'Reference answer withheld.']],
            'element_dtype_array':['video','text'],'istarget_in_interleave':[0,1]}}
        save(inputs/'x2t_video.json',sample)
        row['input_sha256']=input_fingerprint(inputs/'x2t_video.json')
        sample['0001']['interleave_array'][0]=str(CLOUD/'bundles'/row['id']/'inputs/visible.mkv')
        save(inputs/'x2t_video.json',sample)
        template=json.loads(Path('private/p1_full_server_2026-10-30/deployment/bundles/N076-T_G0_native_simple-s47/plan.json').read_text())
        template.update(experiment_id='SO-01',tasks=['x2t_video'],seed=11,request=row,
                        scope='One frozen observational understanding input, no future frames or normative answer',
                        audit_native_rgb_inputs=False,audit_native_sampling=True)
        template['approval']['approved_request_id']=row['id']
        save(bundle/'plan.json',template)
        a.update(input_sha256=row['input_sha256'],video_sha256=sha256(inputs/'visible.mkv'),container_frames=len(frames),
                 video_encoding='FFV1 lossless, bgr0, MKV; format matched within all history controls')
        condition_audits.append(a)
    for row in manifest['codec']:
        control=next(r for r in manifest['controls'] if r['id']==row['source_control_id'])
        row.update(input_file=control['source_file'],input_sha256=control['source_sha256'],
                   eligibility='Visible monotone CPU drawing with explicit AI-development binding; human event gold absent')
    freeze=dict(question_template=question, understanding=condition_audits,codec=manifest['codec'],
                human_labels_created=0,all_inputs_frozen_before_answers=True)
    save(PAYLOAD/'input_construction_freeze.json',freeze)
    save(PUBLIC/'input_construction_freeze.json',freeze)
    save(PAYLOAD/'manifest.json',manifest)
    save(PUBLIC/'manifest.json',manifest)
    print(json.dumps(dict(controls=8,understanding=28,codec=8)))


if __name__=='__main__':main()
