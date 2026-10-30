"""Serial, resumable execution of the explicitly authorized P1 GPU slots."""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback

if __package__:
    from .execute_pilot import audit_output
    from .full_common import input_fingerprint, validate_scope
else:
    from execute_pilot import audit_output
    from full_common import input_fingerprint, validate_scope


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(temporary, path)


def run_owned(command, log_path, seconds):
    with log_path.open('w') as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            return process.wait(timeout=seconds), False
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            return process.returncode, True


def audit_understanding(bundle, run, row):
    attempt = run / row['task']
    result = json.loads((attempt / 'outputs/result.json').read_text())
    actual = json.loads((attempt / 'actual_understanding_input.json').read_text())
    prepared = json.loads((bundle / 'inputs/x2t_video.json').read_text())
    question = prepared['0001']['interleave_array'][1][1]
    sampling = json.loads((attempt / 'actual_sampling.json').read_text())
    audit = dict(nonempty_answer=len(result) == 1 and bool(result[0].get('answer')),
        archived_input_matches_freeze=input_fingerprint(run / 'inputs/x2t_video.json') == row['input_sha256'],
        question_in_actual_conditioning=question in actual['conditioning_decoded_text'],
        placeholder_withheld='Reference answer withheld.' not in actual['conditioning_decoded_text'],
        actual_seed_matches=actual['torch_initial_seed'] == row['seed'],
        actual_video_read_recorded=bool(sampling) and all(s.get('indices') for s in sampling))
    audit['passed'] = all(audit.values())
    save(attempt / 'input_integrity_audit.json', audit)
    return audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--phase', choices=['generation', 'understanding', 'codec'], required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    auth = json.loads((root / 'authorization.json').read_text())
    manifest = validate_scope(auth, json.loads((root / 'manifest.json').read_text()))
    lock = (root / 'GPU_queue.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state_path = root / 'state.json'
    state = json.loads(state_path.read_text())
    deadline = datetime.fromisoformat(auth['hard_stop_at_utc']).timestamp()
    gate = json.loads((root / 'first_request_gate.json').read_text())
    if gate.get('technical_integrity_passed') is not True:
        raise ValueError('Preserved first native request has not passed the input/RGB gate')
    for row in manifest[args.phase]:
        entry = next(r for r in state[args.phase] if r['id'] == row['id'])
        if entry['status'] != 'pending':
            continue  # No failed or interrupted GPU attempt is automatically retried.
        remaining = deadline - time.time()
        if remaining <= 0:
            state['stop_reason'] = '12-hour global hard stop; no additional calls'
            break
        bundle = root / 'bundles' / row['id']
        if args.phase != 'codec':
            plan = json.loads((bundle / 'plan.json').read_text())
            task = row['task']
            if (plan['approval']['approved_request_id'] != row['id'] or plan['seed'] != row['seed']
                    or input_fingerprint(bundle / 'inputs' / (task + '.json')) != row['input_sha256']):
                entry.update(status='blocked', reason='Pre-call frozen input/seed/approval mismatch', actual_calls=0)
                save(state_path, state)
                raise ValueError(entry['reason'])
            command = [sys.executable, str(root / 'tools/run_interfaces.py'), '--bundle', str(bundle)]
        else:
            command = [sys.executable, str(root / 'tools/run_codec.py'), '--root', str(root), '--id', row['id']]
        entry.update(status='running', actual_calls=1, started_at_utc=datetime.now(timezone.utc).isoformat())
        save(state_path, state)
        started = time.perf_counter()
        log = root / 'job_logs' / (row['id'] + '.log')
        returncode, timed_out = run_owned(command, log, min(auth['per_call_timeout_seconds'], remaining))
        entry.update(return_code=returncode, timed_out=timed_out,
                     wall_seconds=time.perf_counter() - started,
                     finished_at_utc=datetime.now(timezone.utc).isoformat(), status='failed')
        if args.phase != 'codec':
            summaries = list((bundle / 'runs').glob('*/summary.json'))
            if summaries:
                run = summaries[0].parent
                entry['native_run'] = str(run.relative_to(root))
                entry['summary'] = json.loads(summaries[0].read_text())
            if returncode == 0 and summaries:
                try:
                    if args.phase == 'generation':
                        audit = audit_output(bundle, run, row)
                        entry['integrity_passed'] = audit['passed']
                    else:
                        entry['integrity_passed'] = audit_understanding(bundle, run, row)['passed']
                    entry['status'] = 'completed' if entry['integrity_passed'] else 'failed'
                except Exception:
                    entry['CPU_audit_error'] = traceback.format_exc()
            archive = root / 'archives' / (row['id'] + '.tar.gz')
            subprocess.run(['tar', '--exclude=./upstream', '-czf', str(archive), '-C', str(bundle), '.'], check=True)
            entry.update(private_archive=str(archive.relative_to(root)), archive_bytes=archive.stat().st_size)
        else:
            result_path = root / 'codec' / row['id'] / 'result.json'
            if result_path.exists():
                entry['result'] = json.loads(result_path.read_text())
                if returncode == 0 and entry['result'].get('completed'):
                    entry['status'] = 'completed'
            archive = root / 'archives' / (row['id'] + '.tar.gz')
            subprocess.run(['tar', '-czf', str(archive), '-C', str(root / 'codec' / row['id']), '.'], check=True)
            entry.update(private_archive=str(archive.relative_to(root)), archive_bytes=archive.stat().st_size)
        save(state_path, state)
        print(json.dumps({k:entry[k] for k in ['id', 'status', 'wall_seconds', 'return_code']}, ensure_ascii=False), flush=True)
        if entry.get('integrity_passed') is False or entry.get('CPU_audit_error') or returncode != 0:
            state['stop_reason'] = 'Inspect failure before resuming pending slots; no GPU retry of the attempted slot'
            save(state_path, state)
            return 2
    state['last_executed_phase'] = args.phase
    save(state_path, state)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
