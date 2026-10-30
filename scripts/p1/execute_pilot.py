"""Execute the Issue #3 allowlist once; the first output requires an external audit gate."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def validate_scope(authorization, manifest):
    rows = manifest['pilot_requests']
    ids = [row['id'] for row in rows]
    if len(ids) != 16 or len(set(ids)) != 16 or set(ids) != set(authorization['approved_request_ids']):
        raise ValueError('Only the exact 16 unique authorized request IDs may run')
    for row in rows:
        if (row['task'] != 't2v' or row['geometry_permission'] != 'G0'
                or row['condition'] not in authorization['conditions']
                or row['character'] not in authorization['approved_characters']
                or row['seed'] not in authorization['seeds']):
            raise ValueError('Request fields exceed the Issue #3 G0 T2V scope')
    if not authorization['user_approved']:
        raise ValueError('Missing user approval')
    return rows


def audit_output(bundle, run, expected):
    import imageio.v2 as imageio
    import numpy as np
    attempt = run / 't2v'
    prepared = json.loads((bundle / 'inputs/t2v.json').read_text())
    archived = json.loads((run / 'inputs/t2v.json').read_text())
    actual = json.loads((attempt / 'actual_generation_input.json').read_text())
    native_prompts = json.loads((attempt / 'outputs/prompt.json').read_text())
    caption = actual['caption']
    captions = [caption] if isinstance(caption, str) else caption
    prompt_ok = (archived == prepared and len(captions) == 1 and prepared['0001'] in captions[0]
                 and expected['character'] in captions[0] and 'Chinese character 十 ' not in captions[0])
    videos = list((attempt / 'outputs').glob('*.mp4'))
    if len(videos) != 1:
        raise ValueError('Expected exactly one native MP4')
    video = videos[0]
    probe_run = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_frames',
                                '-of', 'json', str(video)], check=True, text=True, capture_output=True)
    (attempt / 'ffprobe.json').write_text(probe_run.stdout)
    probe = json.loads(probe_run.stdout)
    stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    pts = [float(f['best_effort_timestamp_time']) for f in probe['frames'] if f['media_type'] == 'video']
    with imageio.get_reader(str(video), format='ffmpeg') as reader:
        decoded = np.stack([frame for frame in reader])
    np.savez_compressed(attempt / 'decoded_rgb_uint8.npz', frames=decoded)
    source = np.load(attempt / 'source_rgb_uint8.npz')['frames']
    size_ok = list(source.shape) == [33, 480, 848, 3] and list(decoded.shape) == list(source.shape)
    pts_ok = len(pts) == 33 and all(abs(t-i/12) < 0.00002 for i,t in enumerate(pts))
    result = dict(passed=prompt_ok and size_ok and pts_ok,
        request_id=expected['id'], actual_caption_contains_exact_prepared_prompt=prompt_ok,
        actual_caption=captions, native_saved_prompt=native_prompts,
        source_shape=list(source.shape), decoded_shape=list(decoded.shape),
        monotone_expected_12fps_PTS=pts_ok, PTS_seconds=pts,
        native_stream=dict(width=stream['width'],height=stream['height'],fps=stream['avg_frame_rate'],
                           duration=stream.get('duration'),codec=stream['codec_name']),
        source_decoded_mean_absolute_pixel_difference=float(np.abs(source.astype(np.int16)-decoded.astype(np.int16)).mean()) if size_ok else None,
        video=video.name, scientific_order_judgment='not_human_evaluated',
        meaning='Input/encoding integrity only; video content may be incorrect or unobservable')
    save(attempt / 'integrity_audit.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--phase', choices=['first', 'remainder'], required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    auth = json.loads((root / 'authorization.json').read_text())
    manifest = json.loads((root / 'pilot_manifest.json').read_text())
    rows = validate_scope(auth, manifest)
    first = auth['execution_policy']['first_request_id']
    if args.phase == 'remainder':
        gate = json.loads((root / 'first_request_gate.json').read_text())
        if gate['request_id'] != first or gate['technical_integrity_passed'] is not True or gate['AI_visual_output_inspected'] is not True:
            raise ValueError('First request has not passed the actual-input and RGB audit')
    ledger_path = root / 'execution_ledger.json'
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text())
    else:
        ledger = dict(initial_attempt_denominator=16, automatic_retries=0, training_steps=0,
            started_at_utc=datetime.now(timezone.utc).isoformat(),
            requests=[dict(request_id=r['id'],status='not_started') for r in rows])
    selected = [r for r in rows if (r['id'] == first) == (args.phase == 'first')]
    for row in selected:
        entry = next(e for e in ledger['requests'] if e['request_id'] == row['id'])
        if entry['status'] != 'not_started':
            raise ValueError('Already launched; retries are not authorized')
        bundle = root / 'bundles' / row['id']
        entry.update(status='running', started_at_utc=datetime.now(timezone.utc).isoformat())
        save(ledger_path, ledger)
        started = time.perf_counter()
        command = ['timeout','--signal=TERM','--kill-after=10s',str(auth['execution_policy']['timeout_seconds_per_attempt'])+'s',
                   sys.executable,str(root/'tools/run_interfaces.py'),'--bundle',str(bundle)]
        with (bundle/'controller.log').open('w') as log:
            execution = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        entry.update(return_code=execution.returncode, wall_seconds=time.perf_counter()-started,
                     finished_at_utc=datetime.now(timezone.utc).isoformat(),status='technical_failure')
        summaries = list((bundle/'runs').glob('*/summary.json'))
        if summaries:
            run = summaries[0].parent
            entry['native_run'] = str(run.relative_to(root))
            entry['native_summary'] = json.loads(summaries[0].read_text())
        save(ledger_path,ledger)
        if execution.returncode != 0:
            print(json.dumps(entry,ensure_ascii=False),flush=True)
            return 1
        entry['status'] = 'audit_pending'
        save(ledger_path,ledger)
        audit_started = time.perf_counter()
        audit = audit_output(bundle, run, row)
        entry.update(status='output_integrity_passed' if audit['passed'] else 'integrity_failure',
                     audit_wall_seconds=time.perf_counter()-audit_started,
                     integrity_audit=str((run/'t2v/integrity_audit.json').relative_to(root)))
        save(ledger_path, ledger)
        print(json.dumps({k:entry[k] for k in ['request_id','status','wall_seconds']},ensure_ascii=False),flush=True)
        if not audit['passed']:
            return 1
        archives = root / 'archives'
        archives.mkdir(exist_ok=True)
        archive = archives / (row['id'] + '.tar.gz')
        subprocess.run(['tar','--exclude=./upstream','-czf',str(archive),'-C',str(bundle),'.'],check=True)
        entry['private_archive'] = str(archive.relative_to(root))
        entry['private_archive_bytes'] = archive.stat().st_size
        save(ledger_path, ledger)
    ledger['last_completed_phase'] = args.phase
    save(ledger_path, ledger)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
