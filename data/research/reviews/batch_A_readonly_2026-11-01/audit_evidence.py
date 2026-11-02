"""CPU-only evidence review. Reads historical evidence; writes new audit outputs only.

Run from repository root with .venv/bin/python and --evidence/--out/--visuals.
No model imports, network, inference, training, or original-file writes.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw

from scripts.diagnostics.media import decode


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load_array(path):
    with np.load(path) as f:
        return f[f.files[0]]


def mask_stats(frames, threshold):
    masks = frames.mean(axis=-1) < threshold
    rows = []
    for i, mask in enumerate(masks):
        y, x = np.nonzero(mask)
        rows.append({'frame': i, 'PTS_nominal': i / 12,
                     'ink_pixels': int(mask.sum()),
                     'xmin': int(x.min()) if len(x) else None,
                     'xmax': int(x.max()) if len(x) else None,
                     'ymin': int(y.min()) if len(y) else None,
                     'ymax': int(y.max()) if len(y) else None,
                     'new_pixels': int((mask & ~masks[i-1]).sum()) if i else 0,
                     'lost_pixels': int((masks[i-1] & ~mask).sum()) if i else 0})
    return {'threshold': threshold, 'frames': rows,
            'first': rows[0], 'last': rows[-1],
            'total_lost_pixels': sum(r['lost_pixels'] for r in rows),
            'adjacent_mask_changes': sum(not np.array_equal(masks[i], masks[i-1]) for i in range(1, len(masks))),
            'xmax_monotone_nondecreasing': all(b['xmax'] >= a['xmax'] for a, b in zip(rows, rows[1:]) if a['xmax'] is not None and b['xmax'] is not None)}


def contact(frames, path, label, width=212):
    height = round(frames.shape[1] * width / frames.shape[2])
    canvas = Image.new('RGB', (width * 6, (height + 22) * 6 + 24), 'white')
    draw = ImageDraw.Draw(canvas)
    draw.text((4, 4), label, fill='black')
    for i, frame in enumerate(frames):
        x, y = (i % 6) * width, (i // 6) * (height + 22) + 24
        canvas.paste(Image.fromarray(frame).resize((width, height)), (x, y + 20))
        draw.text((x + 4, y + 3), f'{i:02d}   {i/12:.3f}s', fill='black')
    canvas.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--visuals', type=Path, required=True)
    args = parser.parse_args()
    args.evidence = args.evidence.resolve()
    args.visuals.mkdir(parents=True, exist_ok=False)
    args.out.mkdir(parents=True, exist_ok=True)
    repo = Path.cwd()
    old = repo / 'data/research/runs/diagnostic_batch_A_2026-11-01'
    frozen = read(repo / 'data/research/next/gpu_pilot_manifest.json')
    state = read(old / 'state.json')
    summary = read(old / 'execution_summary.json')
    rows, arrays, final_tensors, generation, history = [], {}, {}, [], []
    for proposed, actual in zip(frozen['requests'], state['requests'], strict=True):
        request_id = actual['id']
        task = proposed['native_task']
        run = args.evidence / actual['native_run']
        native = run / task
        plan = read(run / 'plan.json')
        integrity = read(native / 'input_output_integrity.json')
        metrics = read(native / 'worker_metrics.json')
        logs = (native / 'process.log').read_text()
        row = {'id': request_id, 'sample_id': proposed['sample_id'], 'track': proposed['track'],
               'id_matches_frozen': request_id == proposed['id'],
               'native_run': actual['native_run'], 'native_task': task,
               'prompt': proposed['prompt'], 'seed': proposed['seed'],
               'plan_matches_frozen_parameters': all(plan[k] == v for k, v in proposed['native_parameters'].items()),
               'status': actual['status'], 'process_attempts': actual['process_attempts'],
               'return_code': actual['return_code'], 'timed_out': actual['timed_out'],
               'wall_seconds': actual['wall_seconds'],
               'recorded_integrity': integrity['passed'],
               'recorded_gpu_allocation': metrics['cuda_peak_allocated_bytes'],
               'native_log_completed': '100%' in logs,
               'raw_answer': None, 'formal_human_judgment': None,
               'formal_primary_metric': None}
        truth = read(repo / 'private/research_restart_2026-11-01/benchmark_v02/evaluation_only' / (proposed['sample_id'] + '.json'))
        row['truth'] = truth
        if task == 'x2t_video':
            answer = read(native / 'outputs/result.json')[0]
            metadata = read(native / 'answer_token_metadata.json')
            inp = read(native / 'actual_understanding_input.json')
            sampling = read(native / 'actual_sampling.json')[0]
            trace = sampling['trace_id']
            rgb = load_array(native / (trace + '-read_RGB.npz'))
            tensor = load_array(native / (trace + '-transformed.npz'))
            arrays[request_id] = rgb
            final_tensors[request_id] = tensor[:, -1].copy()
            context = inp['conditioning_decoded_text']
            raw_native = next(iter(read(native / 'outputs/prompt.json').values()))
            tokens = load_array(native / 'raw_generated_token_ids.npz')
            original_summary_answer = next(a for a in summary['understanding_answers'] if a['id'] == request_id)['raw_answer'][0]['answer']
            input_config = next(iter(read(run / 'inputs/x2t_video.json').values()))
            media_hash = digest(run / 'inputs/visible.mp4')
            frozen_media_hash = next(f['sha256'] for f in proposed['input_files'] if f['path'].endswith('.mp4'))
            visual_slots = inp['conditioning_text_ids'].count(151656)
            expected_slots = (tensor.shape[1] // 2) * (tensor.shape[2] // 14) * (tensor.shape[3] // 14) // 4
            row.update(raw_answer=answer['answer'], question_matches=answer['question'] == proposed['prompt'],
                       question_in_conditioning=proposed['prompt'] in context,
                       full_answer_matches_native=raw_native.replace('<|im_end|>', '').strip() == answer['answer'],
                       full_answer_matches_summary=original_summary_answer == answer['answer'],
                       raw_token_count=int(tokens.shape[0]), token_metadata=metadata,
                       token_count_matches=int(tokens.shape[0]) == metadata['generated_tokens'][0],
                       actual_seed=inp['torch_initial_seed'], visual_token_slots=visual_slots,
                       expected_visual_token_slots=expected_slots, visual_slot_count_consistent=visual_slots == expected_slots,
                       packed_length=len(inp['packed_text_ids']), context_length=len(inp['conditioning_text_ids']),
                       context_cut_consistent=len(inp['conditioning_text_ids']) == inp['ce_loss_indexes'][0]+1,
                       placeholder_withheld='Reference answer withheld.' not in context,
                       literal_fixture_absent='十' not in context,
                       input_config_question_matches=input_config['interleave_array'][1][1] == proposed['prompt'],
                       actual_input_MP4_matches_frozen=media_hash == frozen_media_hash,
                       actual_indices=sampling['indices'], actual_RGB_shape=list(rgb.shape),
                       actual_transformed_shape=list(tensor.shape), tensor_finite=bool(np.isfinite(tensor).all()),
                       native_temporal_padding_duplicates_last=bool(np.array_equal(tensor[:, -1], tensor[:, -2])),
                       RGB_all_frames_identical=bool(np.all(rgb == rgb[:1])),
                       transformed_all_frames_identical=bool(np.all(tensor == tensor[:, :1])),
                       original_answer_file=str((native / 'outputs/result.json').relative_to(repo)),
                       conditioning_without_visual_placeholders=context.replace('<|video_pad|>', ''))
            contact(rgb, args.visuals / f'{request_id}-actual_input.png', request_id, width=128)
            if proposed['track'] == 'K-CHAR':
                mean = np.array([.48145466, .4578275, .40821073])[:, None, None]
                std = np.array([.26862954, .26130258, .27577711])[:, None, None]
                reconstructed = np.rint(np.clip(tensor[:, 0] * std + mean, 0, 1) * 255).astype('uint8').transpose(1, 2, 0)
                Image.fromarray(reconstructed).save(args.visuals / f'{request_id}-ViT_denormalized.png')
                row['intended_character'] = truth['character']
                row['AI_identity_case'] = 'answer_does_not_identify_expected_character'
            if proposed['track'] == 'H-ACTUAL':
                entry = {'id': request_id, 'RGB_mask_audit': mask_stats(rgb, 128)}
                if 'evaluation_regions' in truth:
                    entry['regions'] = []
                    for region in truth['evaluation_regions']:
                        x0,y0,x1,y1 = region['box']
                        entry['regions'].append({'id':region['id'], 'box':region['box'],
                            'stats':mask_stats(rgb[:,y0:y1,x0:x1],128),
                            'note':'Coordinates relative to this fixed region; independent pixels, no construction event log.'})
                history.append(entry)
            del tensor
        else:
            src = load_array(native / 'source_rgb_uint8.npz')
            archived_dec = load_array(native / 'decoded_rgb_uint8.npz')
            video = native / 'outputs/000001.mp4'
            decoded, pts = decode(video)
            inp = read(native / 'actual_generation_input.json')
            entry = {'id':request_id, 'source_shape':list(src.shape), 'decoded_shape':list(decoded.shape),
                     'actual_PTS':pts.tolist(), 'PTS_matches_i_over_12':bool(np.allclose(pts,np.arange(33)/12,atol=5e-6)),
                     'locally_decoded_equals_archived_RGB':bool(np.array_equal(decoded,archived_dec)),
                     'codec_mean_absolute_RGB_error':float(np.abs(src.astype('int16')-decoded.astype('int16')).mean()),
                     'codec_max_absolute_RGB_error':int(np.abs(src.astype('int16')-decoded.astype('int16')).max()),
                     'source':{str(t):mask_stats(src,t) for t in [64,128,192]},
                     'decoded':{str(t):mask_stats(decoded,t) for t in [64,128,192]}}
            generation.append(entry)
            row.update(actual_caption=inp['caption'], caption_matches=inp['caption'] == proposed['prompt'],
                       actual_generation_input={k:v for k,v in inp.items() if 'text_ids' not in k and 'text' not in k},
                       video=str(video.relative_to(repo)), decoded_frames=len(decoded), PTS_consistent=entry['PTS_matches_i_over_12'],
                       archived_decode_reproduced=entry['locally_decoded_equals_archived_RGB'])
            for name, frames in [('source',src),('decoded',decoded)]:
                contact(frames,args.visuals/f'{request_id}-{name}-33frames.png',f'{request_id} {name} RGB; every frame')
                frame_dir=args.visuals/f'{request_id}-{name}-frames'
                frame_dir.mkdir()
                for i,frame in enumerate(frames):
                    Image.fromarray(frame).save(frame_dir/f'{i:02d}.png')
        rows.append(row)
    pairs=[]
    for a,b in [(13,14),(15,16),(17,18),(17,19),(17,20)]:
        x,y=rows[a-1],rows[b-1];ia,ib=x['id'],y['id']
        pairs.append({'ids':[ia,ib], 'same_prompt':x['prompt']==y['prompt'],
                      'same_actual_indices':x['actual_indices']==y['actual_indices'],
                      'same_final_read_RGB':bool(np.array_equal(arrays[ia][-1],arrays[ib][-1])),
                      'same_final_transformed':bool(np.array_equal(final_tensors[ia],final_tensors[ib])),
                      'different_actual_history':bool(not np.array_equal(arrays[ia],arrays[ib])),
                      'same_answer':x['raw_answer']==y['raw_answer'],
                      'interpretation':'Different answers alone do not establish correct history use or a causal mechanism.'})
    receipt=read(old/'backup_receipt.json')
    archive=Path(receipt['local_archive'])
    actual_hash=digest(archive)
    backup={'archive':str(archive.relative_to(repo)),'bytes':archive.stat().st_size,'expected_sha256':receipt['sha256'],
            'actual_sha256':actual_hash,'matches_receipt':actual_hash==receipt['sha256'],
            'weight_hashes_not_repeated':True}
    test_logs=[]
    for name in ['CPU_tests.log','CPU_runner_regression.log','CPU_vsync_regression.log']:
        text=(old/name).read_text()
        count=re.search(r'Ran (\d+) tests in ([0-9.]+)s',text)
        test_logs.append({'file':name,'recorded_tests':int(count[1]) if count else None,
                          'recorded_seconds':float(count[2]) if count else None,
                          'ends_OK':text.rstrip().endswith('OK'),
                          'scope':'Historical CPU regression log; no model capability measurement; not rerun.'})
    code=[]
    executed_repo=args.evidence/'repository'
    for path in sorted(executed_repo.rglob('*')):
        if path.is_file() and path.suffix in {'.py','.sh'} and '__pycache__' not in str(path):
            rel=path.relative_to(executed_repo)
            committed=subprocess.run(['git','show',f'a1c2d5fb:{rel}'],capture_output=True,check=False)
            code.append({'path':str(rel),'present_in_commit':committed.returncode==0,
                         'executed_copy_equals_commit':committed.returncode==0 and committed.stdout==path.read_bytes()})
    timing={'state_updated_at_utc':state['updated_at_utc'],
            'first_call_started_at_utc':state['requests'][0]['started_at_utc'],
            'last_call_finished_at_utc':state['requests'][-1]['finished_at_utc'],
            'finding':'state updated_at predates execution; stale metadata, not a valid completion timestamp. Use per-request times/logs.'}
    save(args.out/'per_request_evidence.json',rows)
    save(args.out/'generation_frame_audit.json',generation)
    save(args.out/'history_pixel_audit.json',history)
    save(args.out/'same_final_history_pairs.json',pairs)
    save(args.out/'backup_test_code_audit.json',{'backup':backup,'tests':test_logs,'executed_code':code,'timestamp_caveat':timing})
    fields=['id','track','status','native_task','seed','wall_seconds','raw_token_count','raw_answer','video']
    with (args.out/'per_request_evidence.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    with (args.out/'generation_all_frames.csv').open('x',newline='') as f:
        fields=['id','stream','threshold','frame','PTS_nominal','ink_pixels','xmin','xmax','ymin','ymax','new_pixels','lost_pixels']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for g in generation:
            for stream in ['source','decoded']:
                for threshold,stats in g[stream].items():
                    for frame in stats['frames']:
                        writer.writerow({'id':g['id'],'stream':stream,'threshold':threshold,**frame})
    print(json.dumps({'requests':len(rows),'answers':sum(r['raw_answer'] is not None for r in rows),
                      'videos':len(generation),'backup_hash_matches':backup['matches_receipt'],
                      'code_differences':[r['path'] for r in code if not r['executed_copy_equals_commit']],
                      'new_model_calls':0,'new_training_runs':0},ensure_ascii=False))


if __name__=='__main__':
    main()
