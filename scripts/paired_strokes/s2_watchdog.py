"""External Linux/NVIDIA sampling. Only the worker's own process group is killed."""
import csv
import io
import os
from pathlib import Path
import signal
import subprocess


GIB = 1024 ** 3


def nvidia_snapshot(uuid):
    def query(kind, fields):
        result = subprocess.run(['nvidia-smi', f'--query-{kind}={fields}',
                                 '--format=csv,noheader,nounits'],
                                text=True, capture_output=True, check=True, timeout=5)
        return list(csv.reader(io.StringIO(result.stdout), skipinitialspace=True))
    devices = query('gpu', 'uuid,name,memory.total,memory.free,memory.used,utilization.gpu')
    device = next(row for row in devices if row[0] == uuid)
    processes = query('compute-apps', 'gpu_uuid,pid,used_gpu_memory')
    return {'uuid': uuid, 'name': device[1], 'total_MiB': float(device[2]),
            'free_MiB': float(device[3]), 'used_MiB': float(device[4]),
            'utilization': float(device[5]),
            'processes': [{'pid': int(p[1]), 'MiB': float(p[2])}
                          for p in processes if p[0] == uuid]}


def process_group(group):
    """PIDs and summed RSS for this session, including tokenizer helper children."""
    pids, rss = [], 0
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            fields = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == group:  # pgrp (stat field 5)
                pids.append(int(entry.name))
                rss += int(fields[21]) * os.sysconf('SC_PAGE_SIZE')
        except (FileNotFoundError, ProcessLookupError):
            pass  # A process may exit between listing and reading stat.
    return pids, rss


def directory_bytes(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def host_capacity():
    available = int(next(s.split()[1] for s in Path('/proc/meminfo').read_text().splitlines()
                         if s.startswith('MemAvailable:'))) * 1024
    return {'available_RAM_bytes': available, 'available_CPU_cores': len(os.sched_getaffinity(0))}


def deadline_reason(caps, elapsed, stage_elapsed, stage):
    if elapsed >= caps['wall_seconds']:
        return 'wall_timeout'
    bound = caps['load_timeout_seconds'] if stage == 'load' else caps['request_timeout_seconds']
    if stage_elapsed >= bound:
        return 'load_timeout' if stage == 'load' else 'request_timeout'
    return None


def limit_reason(caps, sample, elapsed, stage_elapsed, stage):
    """Pure policy, shared with CPU tests; no device calls."""
    deadline = deadline_reason(caps, elapsed, stage_elapsed, stage)
    if deadline:
        return deadline
    if sample['gpu_bytes'] > caps['process_gpu_memory_GiB'] * GIB:
        return 'gpu_memory_cap'
    if sample['rss_bytes'] > caps['host_memory_GiB'] * GIB:
        return 'host_memory_cap'
    if sample['disk_bytes'] > caps['local_disk_GiB'] * GIB:
        return 'disk_cap'
    if sample['foreign_pids']:
        return 'resource_conflict'
    return None


def stop_owned(process):
    """No PID lookup or termination outside our Popen session."""
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
