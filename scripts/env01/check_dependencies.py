"""Retain pip's observed Decord tag failure and require actual fixture decoding."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import traceback
from importlib.metadata import distribution

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bundle', type=Path, required=True)
parser.add_argument('--setup', type=Path, required=True)
args = parser.parse_args()
check = subprocess.run([sys.executable, '-m', 'pip', 'check'], capture_output=True, text=True)
text = check.stdout + check.stderr
(args.setup / 'pip-check.log').write_text(text)
record = {'pip_check_exit_code': check.returncode, 'pip_check_output': text,
          'status': 'failed', 'package_metadata_modified': False}
try:
    if check.returncode == 0:
        record['status'] = 'passed'
    elif text.strip() == 'decord 0.6.0 is not supported on this platform':
        # PyPI publishes py3-none; this wheel's embedded WHEEL says cp36-cp36m.
        # Keep both facts visible and verify the exact input used by this probe.
        import decord
        plan = json.loads((args.bundle / 'plan.json').read_text())
        reader = decord.VideoReader(str(args.bundle / 'inputs/observed_strokes.mp4'), ctx=decord.cpu(0))
        frames = reader.get_batch(list(range(len(reader)))).asnumpy()
        expected = (plan['num_frames'], plan['height'], plan['width'], 3)
        if frames.shape != expected:
            raise RuntimeError(f'Decord decoded {frames.shape}; expected {expected}')
        record.update(status='known_upstream_wheel_tag_warning_actual_decode_passed',
                      wheel_metadata=distribution('decord').read_text('WHEEL'),
                      official_metadata_source='https://pypi.org/pypi/decord/0.6.0/json',
                      published_wheel='decord-0.6.0-py3-none-manylinux2010_x86_64.whl',
                      decoded_shape=list(frames.shape),
                      limitation='pip check still reports the upstream platform tag failure; this is not a fully clean packaging check')
    else:
        raise RuntimeError('Dependency check failed; inspect the complete pip-check.log')
except BaseException:
    record['error'] = traceback.format_exc()
    traceback.print_exc()
finally:
    (args.setup / 'dependency-check.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record), flush=True)
raise SystemExit(1 if record['status'] == 'failed' else 0)
