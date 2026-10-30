"""Derive the public pilot index from preserved private execution evidence."""
import argparse
import csv
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import numpy as np

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--private-root',type=Path,required=True)
parser.add_argument('--output-root',type=Path,required=True)
args=parser.parse_args()
private=args.private_root
public=args.output_root
def read(path):return json.loads(path.read_text())
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
ledger=read(private/'execution_ledger.latest.json')
if ledger.get('last_completed_phase')!='remainder':
    raise SystemExit('Final export requires the completed remainder phase; do not fill pending results')
rows=[]
previews=[]
for entry in ledger['requests']:
    rid=entry['request_id']
    bundle=private/'requests'/rid
    run=next((bundle/'runs').iterdir())
    plan=read(bundle/'plan.json')
    meta=plan['request']
    attempt=run/'t2v'
    audit=read(attempt/'integrity_audit.json')
    result=read(attempt/'result.json')
    measurement=result['measurements']
    video=next((attempt/'outputs').glob('*.mp4'))
    relative_video=str(video.relative_to(private))
    row=dict(request_id=rid,character=meta['character'],condition=meta['condition'],seed=meta['seed'],geometry_permission=meta['geometry_permission'],
        execution_status=entry['status'],return_code=entry['return_code'],started_at_utc=entry['started_at_utc'],finished_at_utc=entry['finished_at_utc'],
        native_wall_seconds=entry['wall_seconds'],worker_seconds_including_load=measurement['worker_elapsed_seconds_including_loading'],
        CPU_output_audit_seconds=entry['audit_wall_seconds'],sampled_device_peak_MiB=result['gpu_sampling']['device_used_memory_peak_mib'],
        CUDA_peak_allocated_bytes=measurement['cuda_peak_allocated_bytes'],CUDA_peak_reserved_bytes=measurement['cuda_peak_reserved_bytes'],
        host_peak_RSS_bytes=measurement['host_peak_rss_bytes'],frames=audit['decoded_shape'][0],width=audit['native_stream']['width'],height=audit['native_stream']['height'],
        fps=audit['native_stream']['fps'],duration_seconds=float(audit['native_stream']['duration']),PTS_12fps_passed=audit['monotone_expected_12fps_PTS'],
        exact_prepared_prompt_at_generation_entry=audit['actual_caption_contains_exact_prepared_prompt'],
        source_decoded_pixel_MAE=audit['source_decoded_mean_absolute_pixel_difference'],
        local_private_video=str(video),cloud_private_run=entry['native_run'],private_archive=entry['private_archive'],private_archive_bytes=entry['private_archive_bytes'],
        formal_human_evaluation='not_performed',stroke_order_score=None,actual_billed_CNY=None)
    rows.append(row)
    previews.append(f'<article><h2>{html.escape(meta["character"])} · {html.escape(meta["condition"])} · seed {meta["seed"]}</h2><video controls preload="metadata" src="{html.escape(relative_video)}"></video><p>{html.escape(rid)}</p><a href="previews/{html.escape(rid)}-all-decoded-frames.jpg">查看全部33帧</a><details><summary>实际提示</summary><p>{html.escape(audit["actual_caption"][0])}</p></details></article>')
save(public/'request_results.json',rows)
with (public/'request_results.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
start=datetime.fromisoformat(rows[0]['started_at_utc'])
finish=datetime.fromisoformat(rows[-1]['finished_at_utc'])
wall=sum(r['native_wall_seconds'] for r in rows)
summary=dict(protocol_id='stroke-video-v2',phase='P1',issue=3,branch='research/p1-native-baselines',
    recorded_at_utc=datetime.now(timezone.utc).isoformat(),status='authorized_16_initial_requests_completed',
    initial_attempt_denominator=16,launched=len(rows),technical_output_integrity_passed=sum(r['execution_status']=='output_integrity_passed' for r in rows),
    technical_failures=sum(r['return_code']!=0 for r in rows),unattempted=16-len(rows),retries=0,training_steps=0,understanding_calls=0,other_48_generation_calls=0,CPU_deterministic_control_videos_created=0,
    character_count=len(set(r['character'] for r in rows)),condition_count=len(set(r['condition'] for r in rows)),seeds=sorted(set(r['seed'] for r in rows)),
    raw_MP4_count=len(rows),raw_MP4_frames=sum(r['frames'] for r in rows),source_RGB_archives=len(rows),decoded_RGB_archives=len(rows),
    all_actual_prompts_verified=all(r['exact_prepared_prompt_at_generation_entry'] for r in rows),all_PTS_verified=all(r['PTS_12fps_passed'] for r in rows),
    first_started_at_utc=rows[0]['started_at_utc'],last_native_finished_at_utc=rows[-1]['finished_at_utc'],
    sum_native_process_wall_seconds=wall,sum_native_process_wall_hours=wall/3600,
    model_worker_seconds_including_load=sum(r['worker_seconds_including_load'] for r in rows),
    first_start_to_last_finish_seconds=(finish-start).total_seconds(),
    inter_request_gate_and_CPU_archive_seconds=(finish-start).total_seconds()-wall,
    CPU_output_audit_seconds=sum(r['CPU_output_audit_seconds'] for r in rows),
    per_request_native_wall_range_seconds=[min(r['native_wall_seconds'] for r in rows),max(r['native_wall_seconds'] for r in rows)],
    peak_device_memory_MiB=max(r['sampled_device_peak_MiB'] for r in rows),
    peak_CUDA_allocated_bytes=max(r['CUDA_peak_allocated_bytes'] for r in rows),peak_CUDA_reserved_bytes=max(r['CUDA_peak_reserved_bytes'] for r in rows),
    peak_host_RSS_bytes=max(r['host_peak_RSS_bytes'] for r in rows),
    source_decoded_MAE_range=[min(r['source_decoded_pixel_MAE'] for r in rows),max(r['source_decoded_pixel_MAE'] for r in rows)],
    private_bundle_archive_bytes=sum(r['private_archive_bytes'] for r in rows),local_private_backups=len(list((private/'archives').glob('*.tar.gz'))),
    model_code_revision='4baeee086648996f6ab12e673cbe461b0b149997',model_weight_revision='7395315758865e6f56ab87ad06a88c7ac172f056',operator_commit='291cd4a00180f76f682a7bfc54a4919638896edd',
    actual_billed_CNY=None,actual_hourly_rate_CNY=None,billing_note='User explicitly declined bill/tariff management. Measured durations retained; no advertised rate substituted for an actual invoice.',
    resource_time_limitation='Summed process wall time includes model loading, source RGB capture and native encoding; it is not CUDA-kernel time or total rental billing. First-to-last interval includes first-request audit and inter-request CPU work; setup and later backup are additional.',
    human_reviews=0,formal_stroke_order_accuracy=None,formal_glyph_accuracy=None,EVAL_02_completed=False,P1_scientific_acceptance=False,
    SO_00_scope='Native uint8 RGB supplied to MP4 encoder versus all decoded MP4 frames/PTS only; not a VAE encode-decode or understanding-sampler experiment')
save(public/'execution_summary.json',summary)
save(public/'execution_ledger.json',ledger)
(private/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>P1首批16次原生生成证据</title><style>body{font:16px system-ui;max-width:1300px;margin:32px auto;padding:0 20px;background:#f4f5f7;color:#17202a}main{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{background:white;padding:18px;border-radius:8px}h2{font-size:17px}video{width:100%}p{line-height:1.5}details p{white-space:pre-wrap} @media(max-width:800px){main{grid-template-columns:1fr}}</style><h1>P1首批16次原生生成证据</h1><p>保留全部原片与33帧索引。此页用于浏览运行证据，未开展正式人工评分；方法和种子可见，后续盲审应另行准备。技术解码成功不代表书写任务成功。</p><main>'+''.join(previews)+'</main></html>')
print(json.dumps(summary,ensure_ascii=False,indent=2))
