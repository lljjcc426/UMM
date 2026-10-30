"""Summarize all fixed slots and auxiliary RGB evidence; leave human judgments empty."""
from collections import Counter
import csv
import json
from pathlib import Path
import re

import numpy as np
from PIL import Image, ImageDraw

from scripts.p0.evaluate_decoupled import load_inputs, geometry_for, reference_for
from scripts.p0.rgb_observation import observe_rgb
from scripts.p0.judgments import judge_normative

PRIVATE=Path('private/p1_full_server_2026-10-30')
PUBLIC=Path('data/research/runs/p1_full_server_2026-10-30')
PILOT=Path('private/p1_native_pilot_issue3_2026-10-30/requests')


def save(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def small_rgb(frames):
    return np.stack([np.asarray(Image.fromarray(f).resize((128,128),Image.Resampling.NEAREST)) for f in frames])


def main():
    manifest=json.loads((PUBLIC/'manifest.json').read_text())
    state=json.loads((PRIVATE/'state.final.json').read_text())
    freeze=json.loads((PUBLIC/'auxiliary_analysis_freeze.json').read_text())
    tasks,_,_=load_inputs()
    audits=json.loads(Path('data/research/runs/p0_decoupled_d1_d4_2026-10-29/static_qualification_audit.json').read_text())
    generated=[];preview_rows=[]
    for row in manifest['generation']:
        entry=next(e for e in state['generation'] if e['id']==row['id'])
        result={k:row[k] for k in ['id','norm_id','character','condition','seed','task','geometry_permission','reused']}
        result.update(status=entry['status'],actual_calls_this_run=entry['actual_calls'],
                      initial_calls_including_pilot=entry.get('historical_actual_calls',0)+entry['actual_calls'],
                      formal_human_judgment='pending_human_review',verified_success=None)
        base=(PILOT if row['reused'] else PRIVATE/'requests')/row['id']
        summaries=list(base.glob('runs/*/summary.json'))
        if summaries:
            native_summary=json.loads(summaries[0].read_text());attempt_summary=native_summary['attempts'][0]
            measures=attempt_summary.get('measurements',{})
            result.update(native_process_wall_seconds=native_summary['elapsed_seconds'],
                device_sampled_peak_MiB=attempt_summary.get('gpu_sampling',{}).get('device_used_memory_peak_mib'),
                torch_peak_allocated_bytes=measures.get('cuda_peak_allocated_bytes'),
                torch_peak_reserved_bytes=measures.get('cuda_peak_reserved_bytes'),host_peak_RSS_bytes=measures.get('host_peak_rss_bytes'))
            if measures.get('error'):
                result['technical_failure']={k:v for k,v in measures['error'].items() if k in ['type','message']}
                result['failure_stage']='Instrumentation at generation entry after GPU VAE preprocessing; no denoising output; not retried'
        arrays=list(base.glob('runs/*/'+row['task']+'/decoded_rgb_uint8.npz'))
        if arrays:
            attempt=arrays[0].parent;frames=np.load(arrays[0])['frames']
            source=np.load(attempt/'source_rgb_uint8.npz')['frames']
            probe=json.loads((attempt/'ffprobe.json').read_text())
            stream=next(s for s in probe['streams'] if s['codec_type']=='video')
            pts=[float(f['best_effort_timestamp_time']) for f in probe['frames'] if f['media_type']=='video']
            actual=json.loads((attempt/'actual_generation_input.json').read_text())
            metrics=json.loads((attempt/'worker_metrics.json').read_text())
            native=json.loads((attempt.parent/'summary.json').read_text())
            input_audit=json.loads((attempt/'integrity_audit.json').read_text())
            result.update(valid_RGB=input_audit['passed'],decoded_shape=list(frames.shape),frame_count=len(frames),
                PTS=pts,pixel_format=stream['pix_fmt'],fps=stream['avg_frame_rate'],duration_seconds=float(stream['duration']),
                exact_adjacent_duplicate_frames=int(np.all(frames[1:]==frames[:-1],axis=(1,2,3)).sum()),
                encoding_MAE=float(np.abs(source.astype(np.int16)-frames.astype(np.int16)).mean()),
                first_frame_dark_pixel_fraction=float((frames[0].min(-1)<128).mean()),
                actual_prompt_verified=input_audit['actual_caption_contains_exact_prepared_prompt'],
                recorded_entry_seed=actual.get('torch_initial_seed'),
                seed_evidence='native method entry' if 'torch_initial_seed' in actual else 'archived native argv + frozen plan + pinned set_seed path; pilot did not record entry seed',
                entry_native_parameters={k:actual[k] for k in ['num_timesteps','cfg_text_scale','video_sizes','VIT_input_elements'] if k in actual},
                torch_peak_allocated_bytes=metrics.get('cuda_peak_allocated_bytes'),torch_peak_reserved_bytes=metrics.get('cuda_peak_reserved_bytes'),
                host_peak_RSS_bytes=metrics.get('host_peak_rss_bytes'),native_process_wall_seconds=native['elapsed_seconds'],
                device_sampled_peak_MiB=native['attempts'][0]['gpu_sampling']['device_used_memory_peak_mib'],
                raw_video=str(next((attempt/'outputs').glob('*.mp4'))),
                artifact_directory=str(attempt))
            if 'torch_initial_seed' in actual:
                assert actual['torch_initial_seed']==row['seed']
                assert actual['num_timesteps']==30 and actual['cfg_text_scale']==4
                assert actual['video_sizes']==[[33,480,848]]
                if row['task']=='t2v':assert actual['VIT_input_elements']==0
            if row['task']=='i2v':
                blank=attempt.parent/'inputs/blank.png';pixels=np.asarray(Image.open(blank).convert('RGB'))
                result['archived_conditioning_image_all_white']=bool(np.all(pixels==255));assert result['archived_conditioning_image_all_white']
            preview_rows.append((row,frames[[0,8,16,24,32]]))
        else:result.update(valid_RGB=False,missing_reason=entry.get('reason',entry.get('CPU_audit_error','No decoded output')))
        result['automatic_observer']=dict(decision='not_applicable' if row['geometry_permission']=='G0' else 'unknown',
            reason='Free generated geometry lacks independently qualified instance binding; no source template imposed',human_primary=True)
        generated.append(result)
    preview_dir=PRIVATE/'AI_contact_sheets';preview_dir.mkdir(exist_ok=False)
    for page in range(0,len(preview_rows),8):
        subset=preview_rows[page:page+8];sheet=Image.new('RGB',(1060,len(subset)*150),'#eee');draw=ImageDraw.Draw(sheet)
        for j,(row,frames) in enumerate(subset):
            draw.text((5,j*150+3),row['id'],fill='black')
            for k,frame in enumerate(frames):sheet.paste(Image.fromarray(frame).resize((212,120)),(k*212,j*150+25))
        sheet.save(preview_dir/f'page-{page//8+1:02}.jpg',quality=90)
    controls=[]
    for row in manifest['controls']:
        nid=row['norm_id'];base=PRIVATE/'diagnostics/controls'/row['id']
        frames=np.load(base/'decoded_RGB_12fps.npz')['frames'];geometry,*_=geometry_for(tasks[nid])
        evidence=observe_rgb(small_rgb(frames),np.arange(len(frames))/12,geometry,freeze['thresholds'])
        judgment=judge_normative(evidence,reference_for(nid,audits))
        controls.append(dict(id=row['id'],formal_human_gold=False,auxiliary_only=True,evidence=evidence,judgment=judgment,
                             observer_receives_synthetic_events=False,geometry_permission='O_exact_development_geometry'))
    codec=[]
    for row in manifest['codec']:
        entry=next(e for e in state['codec'] if e['id']==row['id']);base=PRIVATE/'requests'/row['id']
        result=dict(id=row['id'],status=entry['status'],actual_calls=entry['actual_calls'],human_event_gold=False)
        if (base/'result.json').exists():result['execution']=json.loads((base/'result.json').read_text())
        if (base/'gpu_samples.csv').exists():
            with (base/'gpu_samples.csv').open() as stream:
                samples=list(csv.reader(stream))
            result['device_sampled_peak_MiB']=max(float(s[1]) for s in samples if len(s)>=2)
        if result.get('execution',{}).get('completed'):
            sampling=json.loads((base/'actual_sampling.json').read_text())[0]
            original=np.load(base/(sampling['trace_id']+'-read_RGB.npz'))['frames']
            reconstructed=np.load(base/'reconstructed_RGB_uint8.npz')['frames']
            geometry,*_=geometry_for(tasks[row['norm_id']]);times=np.array(sampling['reader_PTS_intervals'])[:,0]
            observations=[observe_rgb(small_rgb(f),times,geometry,freeze['thresholds']) for f in [original,reconstructed]]
            judgments=[judge_normative(e,reference_for(row['norm_id'],audits)) for e in observations]
            transitions=[]
            for identity in observations[0]['events']:
                a,b=[e['events'][identity] for e in observations]
                transitions.append(dict(instance_id=identity,
                    source_onset=a['onset'],reconstructed_onset=b['onset'],
                    source_complete=a['complete'],reconstructed_complete=b['complete'],
                    source_anchors=a['anchors'],reconstructed_anchors=b['anchors'],
                    source_final_coverage=a['final_coverage'],reconstructed_final_coverage=b['final_coverage']))
            result.update(actual_sampling=sampling,source_observation=observations[0],reconstruction_observation=observations[1],
                          auxiliary_judgments=judgments,event_comparison=transitions,
                          inference_limit='Eight synthetic development inputs; anchor/threshold evidence is auxiliary, not independent human event gold or proof that codec is harmless')
        codec.append(result)
    understanding=[]
    for row in manifest['understanding']:
        entry=next(e for e in state['understanding'] if e['id']==row['id']);base=PRIVATE/'requests'/row['id']
        result=dict(id=row['id'],norm_id=row['norm_id'],condition=row['condition'],source=row['source'],
                    status=entry['status'],actual_calls=entry['actual_calls'],human_evaluation='pending_human_review')
        outputs=list(base.glob('runs/*/x2t_video/outputs/result.json'))
        if outputs:
            result['raw_answer_records']=json.loads(outputs[0].read_text())
            # Native result records may contain server paths; public report keeps the raw answer text only.
            result['raw_answer_records']=[{k:v for k,v in r.items() if k in ['answer','question']} for r in result['raw_answer_records']]
            attempt=outputs[0].parent.parent
            result['sampling']=json.loads((attempt/'actual_sampling.json').read_text())
            result['sampling']=[{k:v for k,v in s.items() if k!='media'} for s in result['sampling']]
            result['input_integrity']=json.loads((attempt/'input_integrity_audit.json').read_text())
            read=result['sampling'][0]
            duration=read['reader_frame_count']/read['reader_fps']
            answer='\n'.join(r['answer'] for r in result['raw_answer_records'])
            claim=re.search(r'(\d+(?:\.\d+)?) seconds? long',answer)
            result['duration_literal_check']=dict(reader_nominal_container_seconds=duration,
                matched_literal_seconds=float(claim.group(1)) if claim else None,
                literal_conflicts_with_container=abs(float(claim.group(1))-duration)>.1 if claim else None,
                scope='Posthoc literal text check only; not stroke accuracy or human judgment')
            metrics=json.loads((attempt/'worker_metrics.json').read_text());summary=json.loads((attempt.parent/'summary.json').read_text())
            result.update(native_process_wall_seconds=summary['elapsed_seconds'],
                torch_peak_allocated_bytes=metrics.get('cuda_peak_allocated_bytes'),torch_peak_reserved_bytes=metrics.get('cuda_peak_reserved_bytes'),
                host_peak_RSS_bytes=metrics.get('host_peak_rss_bytes'),device_sampled_peak_MiB=summary['attempts'][0]['gpu_sampling']['device_used_memory_peak_mib'])
        understanding.append(result)
    understanding_pairs=[]
    indexed={r['id']:r for r in understanding}
    for row in understanding:
        if row['condition']=='full_prefix':continue
        full=indexed[row['id'].rsplit('-',1)[0]+'-full_prefix']
        left,right=[r.get('raw_answer_records') for r in [full,row]]
        understanding_pairs.append(dict(full=full['id'],other=row['id'],condition=row['condition'],
            raw_answer_text_identical=left==right if left is not None and right is not None else None,
            actual_read_indices_match=(full['sampling'][0]['indices']==row['sampling'][0]['indices']) if 'sampling' in full and 'sampling' in row else None,
            formal_accuracy_comparison='pending_human_review',
            interpretation='Answer equality/difference does not establish correct history use or causal bottleneck'))
    pairs=[]
    for nid in [r['norm_id'] for r in manifest['controls']]:
        for seed in [11,29,47]:pairs.append(dict(norm_id=nid,seed=seed,left=f'{nid}-T_G0_native_simple-s{seed}',right=f'{nid}-T_G0_order_text-s{seed}',outcome='pending_human_review'))
        pairs.append(dict(norm_id=nid,seed=11,left=f'{nid}-T_G0_order_text-s11',right=f'{nid}-T_G0_blank_i2v-s11',outcome='pending_human_review',interface_difference='text-only vs actual blank first-frame condition'))
    distances=[]
    by_id={r['id']:r for r in generated}
    for pair in pairs:
        left,right=[by_id[pair[k]] for k in ['left','right']]
        if left['valid_RGB'] and right['valid_RGB']:
            a,b=[np.load(Path(r['artifact_directory'])/'decoded_rgb_uint8.npz')['frames'] for r in [left,right]]
            distances.append(dict(left=left['id'],right=right['id'],pixel_MAE_0_255=float(np.abs(a.astype(np.int16)-b.astype(np.int16)).mean()),
                                  interpretation='Descriptive RGB distance, sensitive to background; no human accuracy or causal interpretation'))
    def counts(kind):
        entries=state[kind]
        return dict(slots=len(entries),actual_initial_calls_this_run=sum(e.get('actual_calls',0) for e in entries),
                    reused_initial_calls=sum(e.get('historical_actual_calls',0) for e in entries),statuses=dict(Counter(e['status'] for e in entries)))
    summary=dict(server_status=state['server_status'],counts={k:counts(k) for k in ['generation','understanding','codec','controls']},
        valid_RGB=sum(r['valid_RGB'] for r in generated),generation_frames=sum(r.get('frame_count',0) for r in generated),
        generation_seconds=sum(r.get('duration_seconds',0) for r in generated),controls=8,
        native_process_wall_seconds=dict(generation_including_pilot=sum(r.get('native_process_wall_seconds',0) for r in generated),
            generation_this_run=sum(r.get('native_process_wall_seconds',0) for r in generated if not r['reused']),
            understanding=sum(r.get('native_process_wall_seconds',0) for r in understanding),
            codec=sum(r.get('execution',{}).get('wall_seconds',0) for r in codec)),
        sampled_device_peak_MiB=max([r.get('device_sampled_peak_MiB',0) or 0 for r in generated+understanding+codec]),
        billing=dict(rate_CNY_per_hour=None,actual_bill_CNY=None,status='unknown; user declined bill management; measured durations retained'),
        EVAL_02='pending_human_review',scientific_acceptance='pending',verified_success=None,training_calls=0,extra_GPU_retries=0)
    save(PUBLIC/'generation_media_and_inputs.json',generated);save(PUBLIC/'controlled_auxiliary_evidence.json',controls)
    save(PUBLIC/'codec_auxiliary_evidence.json',codec);save(PUBLIC/'understanding_answers_and_sampling.json',understanding)
    save(PUBLIC/'understanding_paired_auxiliary.json',understanding_pairs)
    save(PUBLIC/'paired_evaluation_pending.json',pairs);save(PUBLIC/'execution_summary.json',summary)
    save(PUBLIC/'paired_RGB_distances_auxiliary.json',distances)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
