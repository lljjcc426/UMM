"""Finish observed holes left by interrupted HF transfer; verify the repaired file once."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import time
import traceback
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    plan = json.loads((bundle / 'plan.json').read_text())
    folder = bundle / 'upstream/downloads'
    filename = 'Lance_3B_Video/model.safetensors'
    partial, = (folder / '.cache/huggingface/download/Lance_3B_Video').glob('*.incomplete')
    record = {'status': 'failed', 'file': filename, 'revision': plan['weight_revision'], 'ranges': []}
    started = time.monotonic()
    try:
        api = f"https://huggingface.co/api/models/{plan['weight_repository']}/revision/{plan['weight_revision']}?blobs=true"
        with urlopen(api, timeout=30) as response:
            metadata = json.load(response)
        asset = next(item for item in metadata['siblings'] if item['rfilename'] == filename)
        expected = asset['lfs']['sha256']
        assert partial.stat().st_size == asset['size']
        descriptor = os.open(partial, os.O_RDWR)
        try:
            position, size = 0, partial.stat().st_size
            while position < size:
                start = os.lseek(descriptor, position, os.SEEK_HOLE)
                if start >= size:
                    break
                try:
                    end = os.lseek(descriptor, start, os.SEEK_DATA)
                except OSError as error:
                    if error.errno != errno.ENXIO:
                        raise
                    end = size
                record['ranges'].append([start, end - 1])
                position = end
            url = f"https://huggingface.co/{plan['weight_repository']}/resolve/{plan['weight_revision']}/{filename}?download=true"

            def fill(bounds):
                start, end = bounds
                request = Request(url, headers={'Range': f'bytes={start}-{end}'})
                with urlopen(request, timeout=45) as response:
                    assert response.status == 206
                    assert response.headers['Content-Range'] == f'bytes {start}-{end}/{size}'
                    data = response.read()
                assert len(data) == end - start + 1
                assert os.pwrite(descriptor, data, start) == len(data)
                print(json.dumps({'filled_range': bounds, 'bytes': len(data)}), flush=True)

            with ThreadPoolExecutor(max_workers=3) as pool:
                list(pool.map(fill, record['ranges']))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        digest = hashlib.sha256()
        with partial.open('rb') as handle:
            for block in iter(lambda: handle.read(16 * 1024 * 1024), b''):
                digest.update(block)
        record.update(expected_sha256=expected, observed_sha256=digest.hexdigest(), hash_passes=1)
        assert record['observed_sha256'] == expected
        destination = folder / filename
        assert not destination.exists()
        partial.rename(destination)
        from huggingface_hub._local_folder import write_download_metadata
        write_download_metadata(folder, filename, plan['weight_revision'], expected)
        record['status'] = 'repaired_and_verified'
    except BaseException:
        record['error'] = traceback.format_exc()
        traceback.print_exc()
    finally:
        record['elapsed_seconds'] = time.monotonic() - started
        (bundle.parent / 'weight-range-repair.json').write_text(json.dumps(record, indent=2) + '\n')
    return 0 if record['status'] == 'repaired_and_verified' else 1


if __name__ == '__main__':
    raise SystemExit(main())
