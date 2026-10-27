"""Finish the already approved probe after the dedicated extension build exits."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time
import traceback

ROOT = Path('/root/umm-env01-20261027-a10080')
BUNDLE = ROOT / 'env01-cloud'
record = {'status': 'waiting_for_extension', 'started_at_utc': datetime.now(timezone.utc).isoformat()}


def save():
    (ROOT / 'controller_status.json').write_text(json.dumps(record, indent=2) + '\n')


def run_step(name, command, log):
    record.update(status=name, command=command)
    save()
    started = time.monotonic()
    with (ROOT / log).open('w') as output:
        code = subprocess.call(command, stdout=output, stderr=subprocess.STDOUT, env=env)
    record[name] = {'exit_code': code, 'elapsed_seconds': time.monotonic() - started, 'log': log}
    save()
    if code:
        raise RuntimeError(f'{name} exited {code}; retain the complete log')


env = os.environ.copy()
env.update(PATH=str(BUNDLE / 'runtime/bin') + ':/home/vipuser/miniconda3/bin:/usr/local/cuda-12.4/bin:' + env['PATH'],
           CUDA_HOME='/usr/local/cuda-12.4', LD_LIBRARY_PATH='/usr/local/cuda-12.4/lib64',
           PYTHONUNBUFFERED='1', PIP_DISABLE_PIP_VERSION_CHECK='1',
           PIP_INDEX_URL='https://pypi.tuna.tsinghua.edu.cn/simple',
           HF_HUB_DOWNLOAD_TIMEOUT='90', HF_HUB_ETAG_TIMEOUT='30')
save()
try:
    build_pid = int((ROOT / 'flash-attn-wheel-ninja.pid').read_text())
    while Path(f'/proc/{build_pid}/stat').exists():
        if Path(f'/proc/{build_pid}/stat').read_text().split()[2] == 'Z':
            break
        time.sleep(5)
    wheels = list((BUNDLE / 'wheelhouse').glob('flash_attn-2.6.3*.whl'))
    if len(wheels) != 1:
        raise RuntimeError('Dedicated build produced no unique FlashAttention wheel; inspect its retained log')
    record['extension_wheel'] = str(wheels[0])
    run_step('setup_final', ['bash', str(BUNDLE / 'tools/bootstrap.sh')], 'bootstrap-final.log')
    run_step('native_interfaces', [str(BUNDLE / 'runtime/bin/python'), str(BUNDLE / 'tools/run_interfaces.py'),
                                  '--bundle', str(BUNDLE)], 'inference-launch.log')
    record['status'] = 'approved_interface_probe_completed'
except BaseException:
    record.update(status='failed', error=traceback.format_exc())
    traceback.print_exc()
finally:
    record['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    save()
