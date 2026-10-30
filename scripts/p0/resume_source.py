"""Resume the pinned graphics file with bounded parallel HTTP ranges."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.request

ROOT=Path('private/p0_data_eval_2026-10-27/sources')
TARGET=ROOT/'graphics.txt'
URL='https://raw.githubusercontent.com/skishore/makemeahanzi/bddc96d41bef78427ed0e034e9f7e31d71fd1b92/graphics.txt'
SIZE=30778076  # Pinned GitHub contents metadata, not an inferred response size.
RECORD=Path('data/research/runs/p0_data_eval_2026-10-27/source_resume.json')


def fetch(bounds):
    begin,end=bounds
    path=ROOT/f'graphics-range-{begin}-{end}.bin'
    started=time.perf_counter()
    row=dict(begin=begin,end=end,path=str(path),attempts=[])
    if path.exists() and path.stat().st_size==end-begin+1:
        row.update(status='reused_completed_range',bytes=path.stat().st_size)
        return row
    for attempt in range(1,4):
        try:
            request=urllib.request.Request(URL,headers={'User-Agent':'lljjcc426-UMM-research',
                'Range':f'bytes={begin}-{end}','Accept-Encoding':'identity'})
            with urllib.request.urlopen(request,timeout=35) as response:
                if response.status!=206 or response.headers.get('Content-Range')!=f'bytes {begin}-{end}/{SIZE}':
                    raise RuntimeError('Source server did not honor the requested byte range')
                data=response.read()
            if len(data)!=end-begin+1:
                raise RuntimeError('Incomplete HTTP range')
            path.write_bytes(data)
            row['attempts'].append(dict(attempt=attempt,status='downloaded'))
            row.update(status='downloaded',bytes=len(data),wall_seconds=time.perf_counter()-started)
            return row
        except Exception as exc:
            row['attempts'].append(dict(attempt=attempt,status='failed',error=repr(exc)))
    row.update(status='failed',wall_seconds=time.perf_counter()-started)
    return row


def main():
    start=TARGET.stat().st_size
    record=dict(url=URL,started_at_utc=datetime.now(timezone.utc).isoformat(),
                resume_offset=start,total_bytes=SIZE,ranges=[],status='running')
    ranges=[(i,min(i+1024*1024-1,SIZE-1)) for i in range(start,SIZE,1024*1024)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for future in as_completed([pool.submit(fetch,b) for b in ranges]):
            row=future.result();record['ranges'].append(row)
            RECORD.write_text(json.dumps(record,indent=2)+'\n')
            print(row['begin'],row['status'],flush=True)
    if any(row['status']=='failed' for row in record['ranges']):
        record['status']='failed_ranges_retained'
    else:
        with TARGET.open('ab') as target:
            for row in sorted(record['ranges'],key=lambda r:r['begin']):
                target.write(Path(row['path']).read_bytes())
        record.update(status='completed',final_bytes=TARGET.stat().st_size,
                      sha256=hashlib.sha256(TARGET.read_bytes()).hexdigest())
    record['finished_at_utc']=datetime.now(timezone.utc).isoformat()
    RECORD.write_text(json.dumps(record,indent=2)+'\n')
    if record['status']!='completed':
        raise SystemExit(1)


if __name__=='__main__':
    main()
