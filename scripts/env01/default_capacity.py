"""Instrument the pinned native default training policy; stop at a measured OOM.

Run controller with --root, --bundle and --plan. Worker subprocesses keep failed
attempts and CUDA resources isolated. This measures capacity, not model quality.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
import functools
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import traceback


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def log(message):
    print(now(), message, flush=True)


def move(value):
    import torch
    if isinstance(value, torch.Tensor):
        return value.cuda()
    if isinstance(value, list):
        return [move(v) for v in value]
    if isinstance(value, tuple):
        return tuple(move(v) for v in value)
    if isinstance(value, dict):
        return {k: move(v) for k, v in value.items()}
    return value


def parameters(model, gradients=False):
    counts = Counter()
    rows = {}
    for name, p in model.named_parameters():
        counts[f'{"trainable" if p.requires_grad else "frozen"}:{p.dtype}'] += p.numel()
        row = dict(shape=list(p.shape), numel=p.numel(), dtype=str(p.dtype), trainable=p.requires_grad)
        if gradients and p.requires_grad:
            row['gradient'] = None if p.grad is None else dict(
                dtype=str(p.grad.dtype), numel=p.grad.numel(),
                finite=bool(p.grad.isfinite().all()), norm=float(p.grad.norm()))
        rows[name] = row
    return dict(counts=dict(counts), tensors=rows)


def optimizer_inventory(optimizer):
    counts = Counter()
    tensors = 0
    for state in optimizer.state.values():
        for key, value in state.items():
            if hasattr(value, 'numel'):
                counts[f'{key}:{value.dtype}:{value.device.type}'] += value.numel()
                tensors += 1
    return dict(parameters_with_state=len(optimizer.state), state_tensors=tensors, elements=dict(counts))


def pack(bundle, run, plan, tier, tokenizer, tokens):
    import torch
    import yaml
    import pyarrow as pa
    import pyarrow.parquet as pq
    from data.dataset_base_train import DataConfig, PackedDataset

    source = (bundle/'inputs/observed_strokes.mp4').read_bytes()
    rows = {
        'ce': dict(video_bytes=source, caption_i='Describe the stroke order.',
                   caption_q='What is drawn first and second?',
                   caption_a='A horizontal stroke is drawn first, followed by a vertical stroke.'),
        'fm': dict(video_bytes=source, caption='On white paper draw a black horizontal stroke, then a vertical stroke crossing it.')}
    samples = []
    configurations = {}
    budget = plan[tier]['max_num_tokens']
    for task, filename in [('ce', 'v2t_local.yaml'), ('fm', 't2v_local.yaml')]:
        parquet = run/f'{task}.parquet'
        pq.write_table(pa.Table.from_pylist([rows[task]]), parquet)
        config = yaml.safe_load((bundle/'upstream/config/train_local'/filename).read_text())
        setting = next(iter(config['D1'].values()))
        setting['dataset_names'] = {'env01_original': {'data_dir': [str(parquet)]}}
        setting['debug_parquet_repeat'] = 1
        if tier == 'small':
            setting['video_transform_args']['resolution'] = plan[tier][
                'understanding_resolution' if task == 'ce' else 'generation_resolution']
            setting['video_frame_sampler_args']['params'].update(
                sample_fps=plan[tier]['sample_fps'], max_duration=plan[tier]['max_duration'],
                truncate=False, assert_seconds=False)
        if task == 'fm':
            setting.update(task_type='t2v', caption_key='caption')
            setting.pop('task_type_rate', None)
        configurations[task] = config
        (run/f'{task}_dataset.yaml').write_text(yaml.safe_dump(config))
        dc = DataConfig(grouped_datasets=deepcopy(config), text_cond_dropout_prob=.1,
                        vit_cond_dropout_prob=.1, vae_cond_dropout_prob=0,
                        latent_patch_size=(1, 1, 1), max_num_frames=121)
        packer = PackedDataset(dc, tokenizer, tokens, local_rank=0, world_size=1,
                              num_workers=1, expected_num_tokens=budget,
                              max_num_tokens=budget, max_num_tokens_per_sample=budget,
                              use_flex=True, apply_chat_template=False,
                              image_token_id=tokens['image_token_id'], require_und_gen=True)
        samples.append(next(iter(packer.grouped_datasets[0])))
    state = packer.set_sequence_status()
    consumed = []
    # The same native sequence packer handles both task records in one forward.
    while True:
        added = False
        for i, sample in enumerate(samples):
            candidate = packer.pack_sequence(deepcopy(sample), deepcopy(state))
            if sum(candidate['sample_lens']) <= budget:
                state = candidate
                consumed.append('ce' if i == 0 else 'fm')
                added = True
        if tier == 'small' or not added:
            break
    if not {'ce', 'fm'}.issubset(consumed):
        raise RuntimeError('Joint CE/FM records did not fit in the approved packed budget')
    batch = packer.to_tensor(state)
    save(run/'batch_metadata.json', dict(
        sequence_length=batch['sequence_length'], sample_lens=batch['sample_lens'],
        budget=budget, consumed_tasks=consumed, native_num_tokens=[s['num_tokens'] for s in samples],
        tensor_shapes={k: list(v.shape) for k, v in batch.items() if isinstance(v, torch.Tensor)},
        video_shapes=[list(v.shape) for v in batch.get('padded_videos', [])],
        vit_video_shapes=[list(v.shape) for v in batch.get('padded_videos_vit', [])],
        attn_modes=batch['attn_modes']))
    torch.save(batch, run/'packed_joint_batch.pt')
    return batch


def worker(args):
    bundle, run = args.bundle, args.root/args.attempt
    plan = json.loads(args.plan.read_text())
    sys.path.insert(0, str(bundle/'upstream'))
    os.chdir(bundle/'upstream')
    import torch
    import torch.distributed as dist
    from transformers import set_seed
    from config.config_factory import ModelArguments, TrainingArguments
    from train.train_utils import (setup_model_components, prepare_checkpoint_loader,
                                  build_fsdp_config, build_lr_scheduler, compute_training_loss)
    from train.fsdp_utils import fsdp_wrapper, grad_checkpoint_check_fn
    from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (
        apply_activation_checkpointing, checkpoint_wrapper, CheckpointImpl)
    from modeling.lance import Lance, LanceConfig
    from modeling.qwen2 import Qwen2Tokenizer
    from data.data_utils import add_special_tokens
    from common.val.utils import make_padded_latent

    state = dict(status='running', tier=args.tier, started_at_utc=now(), events=[], steps=[])
    phase = 'initialize'
    model = optimizer = None
    started = time.perf_counter()

    def mark(name):
        nonlocal phase
        phase = name
        free, total = torch.cuda.mem_get_info()
        event = dict(phase=name, time_utc=now(), elapsed_seconds=time.perf_counter()-started,
                     allocated_bytes=torch.cuda.memory_allocated(), reserved_bytes=torch.cuda.memory_reserved(),
                     peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                     peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                     device_free_bytes=free, device_total_bytes=total,
                     host_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
        state['events'].append(event)
        save(run/'metrics.json', state)
        log(event)

    try:
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        torch.cuda.set_device(0)
        dist.init_process_group('nccl', init_method=f'file://{run}/nccl-init', rank=0, world_size=1)
        set_seed(plan['seed'])
        ma = ModelArguments(model_path=str(bundle/'upstream/downloads/Lance_3B_Video'),
                            vit_path=str(bundle/'upstream/downloads/Qwen2.5-VL-ViT'),
                            vit_type='qwen_2_5_vl_original', latent_patch_size=(1, 1, 1),
                            max_num_frames=121, vae_cond_dropout_prob=0, vit_cond_dropout_prob=.1)
        ta = TrainingArguments(load_from_lance_checkpoint=True, copy_init_moe=True,
                               apply_qwen_2_5_vl_pos_emb=True, freeze_llm_embed_tokens=True,
                               use_ema=False, use_flex=True, global_seed=2026, timestep_shift=4.,
                               lr=1e-4, min_lr=1e-6, warmup_steps=500, ce_weight=.25,
                               resume_model_only=True)
        ta.N_key_frame = -1
        ta.incre_time_pro = 0
        save(run/'resolved_arguments.json', dict(model=asdict(ma), training=asdict(ta)))
        mark('components_begin')
        lc, lm, vc, vit, vae, vac = setup_model_components(ma, ta, log)
        cfg = LanceConfig(visual_gen=ta.visual_gen, visual_und=ta.visual_und,
                          llm_config=lc, vit_config=vc, vae_config=vac,
                          latent_patch_size=ma.latent_patch_size, max_num_frames=ma.max_num_frames,
                          max_latent_size=ma.max_latent_size, vit_max_num_patch_per_side=ma.vit_max_num_patch_per_side,
                          connector_act=ma.connector_act, interpolate_pos=ma.interpolate_pos,
                          timestep_shift=ta.timestep_shift)
        model = Lance(lm, vit, vit_type=ma.vit_type, config=cfg, training_args=ta)
        mark('checkpoint_load_begin')
        tokenizer, tokens, added = add_special_tokens(Qwen2Tokenizer.from_pretrained(ma.model_path))
        loader = prepare_checkpoint_loader(ma, ta, lc, lm, tokenizer, added, log, report_dir=str(run))
        loader(model)
        save(run/'parameters_before_fsdp.json', parameters(model))
        mark('packing_begin')
        tokens['image_token_id'] = lm.config.video_token_id
        batch = pack(bundle, run, plan, args.tier, tokenizer, tokens)
        mark('fsdp_begin')
        model = fsdp_wrapper(model, build_fsdp_config(ta))
        apply_activation_checkpointing(model,
            checkpoint_wrapper_fn=functools.partial(checkpoint_wrapper, checkpoint_impl=CheckpointImpl.NO_REENTRANT),
            check_fn=grad_checkpoint_check_fn)
        from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
        save(run/'fsdp_configuration.json', [dict(name=n, strategy=str(m.sharding_strategy),
             mixed_precision=str(m.mixed_precision), cpu_offload=str(m.cpu_offload))
             for n, m in model.named_modules() if isinstance(m, FSDP)])
        save(run/'parameters_after_fsdp.json', parameters(model))
        optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                                      lr=ta.lr, betas=(ta.beta1, ta.beta2), eps=ta.eps, weight_decay=0)
        scheduler = build_lr_scheduler(optimizer, ta)
        save(run/'optimizer_configuration.json', {k:v for k,v in optimizer.param_groups[0].items() if k!='params'})
        model.train()
        mark('model_ready')
        for step in range(plan[args.tier]['steps']):
            row = dict(step=step, optimizer_lr=optimizer.param_groups[0]['lr'])
            state['steps'].append(row)
            mark(f'step{step}_input_begin')
            data = move(deepcopy(batch))
            weights = data.pop('ce_loss_weights', None)
            data.pop('batch_data_indexes', None)
            with torch.autocast('cuda', dtype=torch.bfloat16):
                modes = data.pop('vae_data_mode')
                videos = data.pop('padded_videos')
                with torch.no_grad():
                    data['padded_latent'] = make_padded_latent(videos, modes, vae)
                del videos
                data.pop('padded_videos_vit', None)
                mark(f'step{step}_forward_begin')
                outputs = model(**data)
            mark(f'step{step}_loss_begin')
            loss, losses, ce_tokens, mse_tokens = compute_training_loss(outputs, data, weights, ta, 0, 1)
            row.update(loss=float(loss.detach()), ce=float(losses['ce']), fm=float(losses['mse']),
                       ce_tokens=int(ce_tokens), fm_tokens=int(mse_tokens))
            if not bool(torch.isfinite(loss)):
                raise RuntimeError('Non-finite joint loss')
            # Same operation order as optimizer_step_with_ema; boundaries expose
            # lazy optimizer state allocation separately from real backward.
            optimizer.zero_grad()
            mark(f'step{step}_backward_begin')
            loss.backward()
            mark(f'step{step}_backward_complete')
            save(run/f'gradients_step{step}.json', parameters(model, gradients=True))
            mark(f'step{step}_clip_begin')
            row['gradient_norm'] = float(model.clip_grad_norm_(ta.max_grad_norm))
            if not torch.isfinite(torch.tensor(row['gradient_norm'])):
                raise RuntimeError('Non-finite global gradient norm')
            save(run/f'optimizer_before_step{step}.json', optimizer_inventory(optimizer))
            mark(f'step{step}_optimizer_begin')
            optimizer.step()
            torch.cuda.synchronize()
            row['optimizer_completed'] = True
            scheduler.step()
            save(run/f'optimizer_after_step{step}.json', optimizer_inventory(optimizer))
            mark(f'step{step}_complete')
            del data, outputs, loss
        state['status'] = 'passed'
        mark('completed')
    except Exception as exc:
        state.update(status='cuda_oom' if isinstance(exc, torch.OutOfMemoryError) else 'software_error',
                     failed_phase=phase, error_type=type(exc).__name__, error=str(exc),
                     traceback=traceback.format_exc())
        if optimizer is not None:
            save(run/'optimizer_at_failure.json', optimizer_inventory(optimizer))
        save(run/'allocator_at_failure.json', torch.cuda.memory_stats())
        (run/'allocator_at_failure.txt').write_text(torch.cuda.memory_summary())
        mark(phase)
        traceback.print_exc()
    finally:
        state.update(finished_at_utc=now(), wall_seconds=time.perf_counter()-started)
        save(run/'metrics.json', state)
        if dist.is_initialized():
            dist.destroy_process_group()
    return 0 if state['status']=='passed' else 2


def controller(args):
    args.root.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(PATH=str(args.bundle/'runtime/bin')+':/usr/local/cuda-12.4/bin:'+env['PATH'],
               CUDA_HOME='/usr/local/cuda-12.4', CUDA_VISIBLE_DEVICES='0', EXP_HW_20250819='False',
               POSITION_EMBEDDING_3D_VERSION='v2', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
               WANDB_MODE='disabled', PYTHONUNBUFFERED='1', TOKENIZERS_PARALLELISM='false', OMP_NUM_THREADS='4')
    state = dict(status='running', started_at_utc=now(), runs=[], environment=env_subset(env))
    for tier in ['small', 'default_budget']:
        attempt = args.attempt+'-'+tier
        run = args.root/attempt
        run.mkdir()  # Preserve previous attempts; never overwrite their evidence.
        (run/'plan.json').write_bytes(args.plan.read_bytes())
        (run/'script.py').write_bytes(Path(__file__).read_bytes())
        command = [str(args.bundle/'runtime/bin/python'), str(Path(__file__).resolve()),
                   '--worker', '--bundle', str(args.bundle), '--root', str(args.root),
                   '--plan', str(args.plan), '--attempt', attempt, '--tier', tier]
        row = dict(tier=tier, attempt=attempt, command=command, started_at_utc=now())
        state['runs'].append(row)
        save(args.root/f'{args.attempt}-controller.json', state)
        start = time.perf_counter()
        with (run/'process.log').open('w') as out, (run/'gpu_samples.csv').open('w') as gpu:
            monitor = subprocess.Popen(['nvidia-smi', '--query-gpu=timestamp,memory.used,utilization.gpu',
                                        '--format=csv,noheader,nounits', '-l', '1'], stdout=gpu, stderr=subprocess.STDOUT)
            try:
                proc = subprocess.run(command, env=env, stdout=out, stderr=subprocess.STDOUT)
            finally:
                monitor.terminate()
                monitor.wait()
        row.update(exit_code=proc.returncode, wall_seconds=time.perf_counter()-start, finished_at_utc=now())
        metrics = run/'metrics.json'
        row['status'] = json.loads(metrics.read_text())['status'] if metrics.exists() else 'process_error'
        save(args.root/f'{args.attempt}-controller.json', state)
        if proc.returncode:
            state['status'] = row['status']
            state['skipped'] = ['default_budget'] if tier=='small' else []
            break
    else:
        state['status'] = 'passed'
    state['finished_at_utc'] = now()
    save(args.root/f'{args.attempt}-controller.json', state)


def env_subset(env):
    return {k: env[k] for k in ['PATH', 'CUDA_HOME', 'CUDA_VISIBLE_DEVICES', 'EXP_HW_20250819',
            'POSITION_EMBEDDING_3D_VERSION', 'HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE', 'WANDB_MODE',
            'PYTHONUNBUFFERED', 'TOKENIZERS_PARALLELISM', 'OMP_NUM_THREADS']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--attempt', default='attempt01')
    parser.add_argument('--tier', choices=['small', 'default_budget'], default='small')
    parser.add_argument('--worker', action='store_true')
    cli = parser.parse_args()
    if cli.worker:
        sys.exit(worker(cli))
    controller(cli)
