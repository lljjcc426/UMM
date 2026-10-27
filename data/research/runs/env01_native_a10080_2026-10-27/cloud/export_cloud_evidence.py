"""Archive this task's logs and media without weights, environments or caches."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

ROOT = Path('/root/umm-env01-20261027-a10080')
ARCHIVE = ROOT.parent / 'umm-env01-20261027-a10080-evidence.tar.gz'
for source in Path('/tmp').glob('pip-wheel-*/flash-attn_*/setup.py'):
    shutil.copyfile(source, ROOT / 'flash-attn-build-setup.py')
    license_file = source.parent / 'LICENSE'
    if license_file.exists():
        shutil.copyfile(license_file, ROOT / 'flash-attn-build-LICENSE')
    for name in ('build.ninja', '.ninja_log'):
        for path in (source.parent / 'build').glob('temp*/' + name):
            shutil.copyfile(path, ROOT / ('flash-attn-' + name.lstrip('.')))

inventory = {
    'captured_at_utc': datetime.now(timezone.utc).isoformat(),
    'task_disk_usage': subprocess.check_output(['du', '-sk', str(ROOT)], text=True),
    'filesystem': subprocess.check_output(['df', '-B1', str(ROOT)], text=True),
    'uptime_seconds': float(Path('/proc/uptime').read_text().split()[0]),
    'billing': {'actual_billed_cny': None, 'reason': 'Platform bill not provided'},
}
(ROOT / 'collection_inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')


def include(info):
    parts = Path(info.name).parts
    if any(part in {'runtime', 'downloads', 'download-client', 'wheelhouse',
                    'weight-partials-before-acceleration', '__pycache__'} for part in parts):
        return None
    if info.name.endswith(('.tar.gz', '.whl')):
        return None
    return info


with tarfile.open(ARCHIVE, 'w:gz') as handle:
    handle.add(ROOT, arcname='cloud', filter=include)
print(json.dumps({'archive': str(ARCHIVE), 'bytes': ARCHIVE.stat().st_size}))
