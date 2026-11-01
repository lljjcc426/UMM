"""Summarize actual Batch A attempts without assigning human or scientific gold."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path

from .contracts import save


def summarize(root):
    root=Path(root)
    proposal=json.loads((root/'manifest.json').read_text())
    state=json.loads((root/'state.json').read_text())
    entries={r['id']:r for r in state['requests']}
    tracks=defaultdict(Counter)
    attempts=[];answers=[];peaks=[];shared=0;wall=0
    for row in proposal['requests']:
        entry=entries[row['id']]
        status=entry['status'];track=tracks[row['track']]
        track['requested']+=1;track[status]+=1
        track['process_attempts']+=entry.get('process_attempts',0)
        track['native_method_entries']+=bool(entry.get('native_method_entered'))
        item={**entry,'track':row['track'],'native_task':row['native_task'],'source_group':row['source_group']}
        metrics=entry.get('measurements',{})
        for key in ('cuda_peak_allocated_bytes','cuda_peak_reserved_bytes','host_peak_rss_bytes'):
            if metrics.get(key) is not None:peaks.append((key,metrics[key]))
        wall+=entry.get('wall_seconds',0)
        if entry.get('native_run'):
            attempt=root/entry['native_run']/row['native_task']
            command=attempt/'command.json'
            if command.exists():
                snap=json.loads(command.read_text())['resource_snapshot_before_call']
                shared+=bool(snap.get('compute_processes'))
            sample=attempt/'gpu_samples.csv'
            if sample.exists():
                values=[float(line.split(',')[1]) for line in sample.read_text().splitlines() if len(line.split(','))>=4]
                item['whole_device_sampled_peak_MiB']=max(values) if values else None
            if row['native_task']=='x2t_video':
                text=attempt/'outputs/result.json';token=attempt/'answer_token_metadata.json'
                answers.append({'id':row['id'],'track':row['track'],'question':row['prompt'],
                    'raw_answer':json.loads(text.read_text()) if text.exists() else None,
                    'token_metadata':json.loads(token.read_text()) if token.exists() else None,
                    'status':status,'scientific_judgment':None})
        attempts.append(item)
    counts=Counter(r['status'] for r in state['requests'])
    total=len(proposal['requests']);called=sum(r.get('process_attempts',0) for r in state['requests'])
    complete=counts['completed'];failed=counts['failed'];unrun=total-called
    valid_text=sum(r['status']=='completed' and r['native_task']=='x2t_video' for r in attempts)
    valid_video=sum(r['status']=='completed' and r['native_task']=='t2v' for r in attempts)
    result={'status':('completed' if complete==total else 'completed_with_failures' if called==total else 'partial'),
        'requested_slots':total,'process_attempts':called,
        'native_method_entries':sum(bool(r.get('native_method_entered')) for r in state['requests']),
        'integrity_valid_outputs':complete,'integrity_valid_answers':valid_text,'integrity_valid_videos':valid_video,
        'technical_failed_slots':failed,'unrun_slots':unrun,'status_counts':dict(counts),
        'per_track':{k:dict(v) for k,v in tracks.items()},'native_worker_wall_seconds_including_loading':wall,
        'per_process_peaks':{key:max(v for k,v in peaks if k==key) for key in {k for k,v in peaks}},
        'calls_with_other_GPU_processes_present':shared,
        'whole_device_samples_attribution':'Shared device; not the memory footprint of Lance alone',
        'automatic_GPU_retries':0,'training_runs':0,'actual_cost_CNY':None,
        'formal_primary_metrics':None,'human_review_created':False,
        'model_revision':proposal['batch_A']['model_revision'],'code_revision':proposal['batch_A']['code_revision'],
        'attempts':attempts,'understanding_answers':answers}
    dates=[r[k] for r in state['requests'] for k in ('started_at_utc','finished_at_utc') if k in r]
    if dates:
        times=[datetime.fromisoformat(t) for t in dates]
        result.update(first_call_started_at_utc=min(times).isoformat(),last_call_finished_at_utc=max(times).isoformat(),
                      scheduler_span_seconds=(max(times)-min(times)).total_seconds())
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True);p.add_argument('--output',required=True)
    args=p.parse_args();result=summarize(args.root);save(args.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('attempts','understanding_answers')},indent=2))


if __name__=='__main__':main()
