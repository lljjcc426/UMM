"""Fetch the selected files through ModelScope, checking HF weight identities once.

The expected manifest is captured from the official, pinned Hugging Face revision.
Only model downloads are concurrent; original failed transfers are retained.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import time

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    files = json.loads(args.manifest.read_text())
    revision = '933a33a1bfacefb22e41297766c2c669627c33cd'

    def fetch(item):
        target = args.destination / item['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise FileExistsError(f'Preserve existing file: {target}')
        url = f'https://modelscope.cn/models/AI-ModelScope/LTX-Video/resolve/{revision}/{item["file"]}'
        started = time.monotonic()
        digest, size = hashlib.sha256(), 0
        session = requests.Session()
        session.trust_env = False
        print('START', item['file'], flush=True)
        with session.get(url, stream=True, timeout=(15, 90)) as response:
            response.raise_for_status()
            with target.with_suffix(target.suffix + '.ms-partial').open('wb') as out:
                for chunk in response.iter_content(4 * 1024 * 1024):
                    out.write(chunk)
                    digest.update(chunk)
                    size += len(chunk)
        actual = digest.hexdigest()
        if size != item['size'] or (item['sha256'] and actual != item['sha256']):
            raise ValueError(f'Weight identity or size mismatch: {item["file"]}')
        target.with_suffix(target.suffix + '.ms-partial').rename(target)
        result = dict(item, actual_sha256=actual, seconds=time.monotonic() - started,
                      source_url=url, official_hash_matched=bool(item['sha256']))
        print(json.dumps(result), flush=True)
        return result

    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        for future in as_completed([pool.submit(fetch, item) for item in files]):
            results.append(future.result())
            (args.destination.parent / 'download_receipts.json').write_text(
                json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
