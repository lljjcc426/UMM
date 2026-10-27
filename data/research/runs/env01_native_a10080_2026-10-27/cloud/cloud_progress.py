"""Read the active probe's progress without changing its execution."""
from datetime import datetime, timezone
import json
from pathlib import Path

root = Path('/root/umm-env01-20261027-a10080')
state = json.loads((root / 'controller_status.json').read_text())
out = {'time_utc': datetime.now(timezone.utc).isoformat(), 'controller': state}
logs = list(Path('/tmp').glob('pip-wheel-*/flash-attn_*/build/temp*/.ninja_log'))
if logs:
    rows = logs[0].read_text().splitlines()[1:]
    out['compiled_objects'] = len({row.split('\t')[3] for row in rows})
for name in ['MemAvailable', 'SwapFree']:
    line = next(line for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith(name + ':'))
    out[name + '_mib'] = int(line.split()[1]) // 1024
if state['status'] != 'waiting_for_extension':
    for name in ['bootstrap-final.log', 'inference-launch.log']:
        path = root / name
        if path.exists():
            out[name] = path.read_text(errors='replace')[-2200:]
out['runs'] = []
for path in sorted((root / 'env01-cloud/runs').glob('*/summary.json')):
    summary = json.loads(path.read_text())
    out['runs'].append({'run_id': summary['run_id'], 'status': summary['status'],
                        'attempts': [{'task': row['task'], 'status': row['status'],
                                      'error': row.get('measurements', {}).get('error'),
                                      'wall_seconds': row.get('wall_seconds'),
                                      'output_check': row.get('output_check')} for row in summary['attempts']]})
print(json.dumps(out, ensure_ascii=False))
with (root / 'progress_samples.jsonl').open('a') as log:
    log.write(json.dumps({key: out[key] for key in ['time_utc', 'MemAvailable_mib', 'SwapFree_mib']} |
                         {'controller_status': state['status'], 'compiled_objects': out.get('compiled_objects')}) + '\n')
