"""Retain command, exit, wall/CPU time and child RSS for one local P0 stage."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--name',required=True)
parser.add_argument('command',nargs=argparse.REMAINDER)
args=parser.parse_args()
command=args.command[1:] if args.command[:1]==['--'] else args.command
root=Path('data/research/runs/p0_data_eval_2026-10-27')
record_path=root/f'{args.name}.json'
if record_path.exists():
    raise SystemExit('Stage record exists; use a new attempt name to retain prior evidence')
record=dict(command=command,started_at_utc=datetime.now(timezone.utc).isoformat(),status='running',
            execution_host='local_CPU',gpu_hours=0,cloud_compute_used=False)
record_path.write_text(json.dumps(record,indent=2)+'\n')
started=time.perf_counter()
with (root/f'{args.name}.log').open('w') as log:
    result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
record.update(exit_code=result.returncode,status='passed' if result.returncode==0 else 'failed',
              finished_at_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.perf_counter()-started,
              child_user_cpu_seconds=usage.ru_utime,child_system_cpu_seconds=usage.ru_stime,
              child_peak_rss_bytes=usage.ru_maxrss*(1 if platform.system()=='Darwin' else 1024))
record_path.write_text(json.dumps(record,indent=2)+'\n')
sys.exit(result.returncode)
