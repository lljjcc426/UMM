"""Approved ENV-01 partial native training, decoder audit and fresh-process resume.

The checkpoint contains every trainable tensor and optimizer state. Frozen tensors
are reconstructed from the pinned original checkpoint with the recorded seed.
This exercises native packing/encoders/forward/loss, not the full FSDP launcher.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import gc
import json
import os
from pathlib import Path
import random
import re
import resource
import subprocess
import sys
import time
import traceback


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def log(message):
    print(datetime.now(timezone.utc).isoformat(), message, flush=True)


def seed_all(seed):
    import numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def rng_state():
    import numpy as np
    import torch
    return dict(python=random.getstate(), numpy=np.random.get_state(),
                torch_cpu=torch.get_rng_state(), torch_cuda=torch.cuda.get_rng_state_all())


def restore_rng(state):
    import numpy as np
    import torch
    random.setstate(state['python'])
    np.random.set_state(state['numpy'])
    torch.set_rng_state(state['torch_cpu'])
    torch.cuda.set_rng_state_all(state['torch_cuda'])


def tokenizer_for(bundle):
    from modeling.qwen2 import Qwen2Tokenizer
    from data.data_utils import add_special_tokens
    tokenizer = Qwen2Tokenizer.from_pretrained(str(bundle/'upstream/downloads/Lance_3B_Video'))
    tokenizer, tokens, added = add_special_tokens(tokenizer)
    tokens['image_token_id'] = 151656  # replaced with the actual model config below
    from modeling.qwen2.modeling_qwen2 import Qwen2Config
    config = Qwen2Config.from_json_file(str(bundle/'upstream/downloads/Lance_3B_Video/llm_config.json'))
    tokens['image_token_id'] = config.video_token_id
    return tokenizer, tokens, added


def audit_and_pack(bundle, run, plan):
    import ctypes
    from importlib.metadata import distribution
    import shutil
    import io
    import numpy as np
    import torch
    import decord
    import imageio_ffmpeg
    import pyarrow as pa
    import pyarrow.parquet as pq
    import yaml
    from data.base_mm_parquet_dataset import BaseMMParquetDataset
    from data.dataset_base_train import DataConfig, PackedDataset

    ffmpeg = shutil.which('ffmpeg') or imageio_ffmpeg.get_ffmpeg_exe()
    ffprobe = shutil.which('ffprobe')
    paths = [bundle/'inputs/observed_strokes.mp4']
    paths += sorted((bundle/'runs/20261027T114559963105Z').glob('*/outputs/*.mp4'))
    audit = {'wheel_metadata': distribution('decord').read_text('WHEEL'),
             'published_wheel': 'decord-0.6.0-py3-none-manylinux2010_x86_64.whl',
             'cause': 'Published generic Python filename conflicts with embedded cp36-cp36m platform tag',
             'loader': 'decord._ffi.base._load_lib uses ctypes.CDLL',
             'metadata_modified': False, 'ffmpeg': ffmpeg, 'clips': []}
    for path in paths:
        vr = decord.VideoReader(io.BytesIO(path.read_bytes()), num_threads=1)
        actual = vr.get_batch(list(range(len(vr)))).asnumpy()
        h, w = actual.shape[1:3]
        proc = subprocess.run([ffmpeg, '-v', 'error', '-i', str(path), '-f', 'rawvideo',
                               '-pix_fmt', 'rgb24', '-vsync', '0', '-'], capture_output=True, check=True)
        reference = np.frombuffer(proc.stdout, dtype=np.uint8).reshape(-1, h, w, 3)
        delta = np.abs(actual.astype(np.int16)-reference.astype(np.int16))
        matched = [int(np.argmin(np.mean(np.abs(reference.astype(np.int16)-frame.astype(np.int16)), axis=(1,2,3)))) for frame in actual]
        timestamps = vr.get_frame_timestamp(list(range(len(vr)))).tolist()
        row = dict(path=str(path), shape=list(actual.shape), max_pixel_difference=int(delta.max()),
                   mean_pixel_difference=float(delta.mean()), nearest_reference_frame=matched,
                   timestamps=timestamps, fps=vr.get_avg_fps(), frame_count_equal=len(reference)==len(actual),
                   ordered_pixels_within_tolerance=bool(delta.max()<=plan['acceptance']['decord_pixel_max_abs']))
        if ffprobe:
            probe=subprocess.run([ffprobe,'-v','error','-select_streams','v:0','-show_frames',
                                  '-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)],capture_output=True,text=True,check=True)
            times=[float(f['best_effort_timestamp_time']) for f in json.loads(probe.stdout)['frames']]
            row['ffprobe_pts']=times
            row['max_timestamp_difference_seconds']=float(np.max(np.abs(np.asarray(times)-np.asarray(timestamps)[:,0])))
        else:
            timing=subprocess.run([ffmpeg,'-v','info','-i',str(path),'-vf','showinfo','-vsync','0','-f','null','-'],capture_output=True,text=True,check=True)
            times=[float(x) for x in re.findall(r'\bn:\s*\d+.*?\bpts_time:([\d.eE+-]+)',timing.stderr)]
            row['independent_ffmpeg_showinfo_pts']=times
            row['max_timestamp_difference_seconds']=float(np.max(np.abs(np.asarray(times)-np.asarray(timestamps)[:,0])))
        audit['clips'].append(row)
        write_json(run/'decord_audit.json',audit)
        if not row['ordered_pixels_within_tolerance'] or row['max_timestamp_difference_seconds']>plan['acceptance']['decord_timestamp_atol_seconds']:
            raise RuntimeError('Decord and independent decoding disagree; inspect audit before training')
    # Exercise exactly the raw-byte batch reader used by the native training data path.
    source=paths[0].read_bytes()
    vr=decord.VideoReader(io.BytesIO(source),num_threads=1)
    indexes=[0,8,16,24,32]
    native=np.stack([np.asarray(p) for p in BaseMMParquetDataset._read_decord(vr,indexes)])
    audit['native_raw_byte_reader_exact']=bool(np.array_equal(native,vr.get_batch(indexes).asnumpy()))
    audit['status']='non_blocking_wheel_metadata_warning_for_verified_paths'
    write_json(run/'decord_audit.json',audit)
    tokenizer,tokens,_=tokenizer_for(bundle)
    specs={
        'ce': ('v2t_local.yaml',{'video_bytes':source,'caption_i':'Describe the stroke order.','caption_q':'What is drawn first and second?','caption_a':'A horizontal stroke is drawn first, followed by a vertical stroke.'}),
        'fm': ('t2v_local.yaml',{'video_bytes':source,'caption':'On white paper draw a black horizontal stroke, then a vertical stroke crossing it.'})}
    batches={}
    metadata={}
    for task,(config_name,row) in specs.items():
        parquet=run/f'{task}.parquet'
        pq.write_table(pa.Table.from_pylist([row]),parquet)
        config=yaml.safe_load((bundle/'upstream/config/train_local'/config_name).read_text())
        settings=next(iter(config['D1'].values()))
        settings['dataset_names']={'env01_original':{'data_dir':[str(parquet)]}}
        settings['debug_parquet_repeat']=1
        settings['video_transform_args']['resolution']=plan['input']['understanding_resolution' if task=='ce' else 'generation_resolution']
        settings['video_frame_sampler_args']['params'].update(sample_fps=plan['input']['frame_sample_fps'],max_duration=plan['input']['max_duration_seconds'],truncate=False,assert_seconds=False)
        if task=='fm':
            settings.update(task_type='t2v',caption_key='caption')
            settings.pop('task_type_rate',None)
        (run/f'{task}_dataset.yaml').write_text(yaml.safe_dump(config))
        dc=DataConfig(grouped_datasets=deepcopy(config),text_cond_dropout_prob=0,vit_cond_dropout_prob=0,vae_cond_dropout_prob=0,latent_patch_size=(1,1,1),max_num_frames=121)
        packer=PackedDataset(dc,tokenizer,tokens,local_rank=0,world_size=1,num_workers=1,
                            expected_num_tokens=1,max_num_tokens=1024,max_num_tokens_per_sample=1024,
                            use_flex=True,apply_chat_template=False,image_token_id=tokens['image_token_id'])
        sample=next(iter(packer.grouped_datasets[0]))
        batch=packer.to_tensor(packer.pack_sequence(sample,packer.set_sequence_status()))
        batches[task]=batch
        metadata[task]={'sequence_length':batch['sequence_length'],'sample_lens':batch['sample_lens'],
                        'attn_modes':batch['attn_modes'],'tensor_shapes':{k:list(v.shape) for k,v in batch.items() if isinstance(v,torch.Tensor)},
                        'video_shapes':[list(x.shape) for x in batch.get('padded_videos',[])],
                        'vit_video_shapes':[list(x.shape) for x in batch.get('padded_videos_vit',[])],
                        'native_sample_tokens':sample['num_tokens']}
        log(f'Packed {task}: {metadata[task]}')
    torch.save(batches,run/'packed_batches.pt')
    write_json(run/'batch_metadata.json',metadata)


def build_model(bundle,run,plan):
    import torch
    from safetensors.torch import load_file
    from transformers.models.qwen2_5_vl.configuration_qwen2_5_vl import Qwen2_5_VLVisionConfig
    from modeling.qwen2.modeling_qwen2 import Qwen2Config
    from modeling.lance import Lance,LanceConfig,Qwen2ForCausalLM
    from modeling.vit.qwen2_5_vl_vit import Qwen2_5_VisionTransformerPretrainedModel
    from modeling.vae.wan.model import WanVideoVAE
    from config.config_factory import TrainingArguments
    seed_all(plan['seed'])
    path=bundle/'upstream/downloads/Lance_3B_Video'
    cfg=Qwen2Config.from_json_file(str(path/'llm_config.json'))
    cfg.layer_module='Qwen2MoTDecoderLayer'
    cfg.qk_norm=cfg.qk_norm_und=cfg.qk_norm_gen=True
    cfg.tie_word_embeddings=False
    cfg.freeze_und=False
    cfg.apply_qwen_2_5_vl_pos_emb=True
    lm=Qwen2ForCausalLM(cfg)
    vitcfg=Qwen2_5_VLVisionConfig.from_pretrained(str(bundle/'upstream/downloads/Qwen2.5-VL-ViT'))
    vit=Qwen2_5_VisionTransformerPretrainedModel(vitcfg)
    vae=WanVideoVAE()
    args=TrainingArguments()
    args.apply_qwen_2_5_vl_pos_emb=True
    args.freeze_und=False
    args.incre_time_pro=0
    config=LanceConfig(llm_config=cfg,vit_config=vitcfg,vae_config=vae.vae_config,
                       latent_patch_size=(1,1,1),max_num_frames=121,max_latent_size=64,timestep_shift=4.0)
    model=Lance(lm,vit,vit_type='qwen_2_5_vl_original',config=config,training_args=args).cuda()
    tokenizer,tokens,added=tokenizer_for(bundle)
    weights=load_file(str(path/'model.safetensors'),device='cpu')
    weights.pop('latent_pos_embed.pos_embed',None)
    msg=model.load_state_dict(weights,strict=False)
    write_json(run/f'load_report_{STAGE}.json',dict(missing=msg.missing_keys,unexpected=msg.unexpected_keys))
    if msg.missing_keys!=['latent_pos_embed.pos_embed'] or msg.unexpected_keys:
        raise RuntimeError('Unexpected base model load mismatch')
    del weights
    gc.collect()
    if added:
        lm.resize_token_embeddings(len(tokenizer))
    model.update_tokenizer(tokenizer)
    model.to(dtype=torch.bfloat16)
    last=len(lm.model.layers)-1
    prefixes=[f'language_model.model.layers.{last}.self_attn.q_proj',f'language_model.model.layers.{last}.self_attn.q_proj_moe_gen','vae2llm','llm2vae','time_embedder']
    selected={}
    for name,param in model.named_parameters():
        enabled=name=='language_model.model.embed_tokens.weight' or any(name==s or name.startswith(s+'.') for s in prefixes)
        param.requires_grad_(enabled)
        if enabled:
            param.data=param.data.float()
            selected[name]=param
    model.train()
    model.vit_model.eval()
    # Embedding lookup is not autocast by PyTorch. Keep FP32 optimizer/master
    # weights while matching the BF16 packed visual stream, preserving autograd.
    lm.model.embed_tokens.register_forward_hook(lambda module, inputs, output: output.to(torch.bfloat16))
    torch.cuda.empty_cache()
    write_json(run/f'parameters_{STAGE}.json',{'all_parameters':sum(p.numel() for p in model.parameters()),
                'trainable_parameters':sum(p.numel() for p in selected.values()),'last_decoder_layer':last,
                'trainable':{n:{'shape':list(p.shape),'dtype':str(p.dtype),'numel':p.numel()} for n,p in selected.items()},
                'shared_candidate':'language_model.model.embed_tokens.weight',
                'sharing_limit':'UND and GEN Transformer experts have separate QKV/MLP/norm tensors; shared embedding gradients alone do not establish positive transfer'})
    return model,vae,selected


def to_device(value):
    import torch
    if isinstance(value,torch.Tensor): return value.cuda()
    if isinstance(value,list): return [to_device(x) for x in value]
    if isinstance(value,tuple): return tuple(to_device(x) for x in value)
    if isinstance(value,dict): return {k:to_device(v) for k,v in value.items()}
    return value


def one_step(model,vae,selected,optimizer,scheduler,batches,plan,step,run,label):
    import torch
    from common.val.utils import make_padded_latent
    started=time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    optimizer.zero_grad(set_to_none=True)
    before={n:p.detach().cpu().clone() for n,p in selected.items()}
    frozen_versions={n:p._version for n,p in model.named_parameters() if not p.requires_grad}
    task_records=[]
    for task in ['ce','fm']:
        data=to_device(deepcopy(batches[task]))
        weights=data.pop('ce_loss_weights',None)
        data.pop('batch_data_indexes',None)
        videos=data.pop('padded_videos')
        modes=data.pop('vae_data_mode')
        data.pop('padded_videos_vit',None)
        model.config.visual_gen=task=='fm'
        if task=='fm':
            with torch.no_grad(): data['padded_latent']=make_padded_latent(videos,modes,vae)
        with torch.autocast('cuda',dtype=torch.bfloat16):
            outputs=model(**data)
            raw=outputs['ce'].float().mean() if task=='ce' else outputs['mse'].float().mean()
            loss=raw*plan['ce_weight' if task=='ce' else 'mse_weight']
        if not torch.isfinite(loss): raise RuntimeError(f'Non-finite {task} loss')
        # Clear each task independently, retain the resulting real gradients for accumulation.
        existing={n:p.grad for n,p in selected.items()}
        for p in selected.values(): p.grad=None
        loss.backward()
        gradients={n:{'present':p.grad is not None,'finite':bool(torch.isfinite(p.grad).all()) if p.grad is not None else None,
                      'norm':float(p.grad.norm()) if p.grad is not None else 0.0} for n,p in selected.items()}
        expected=['language_model.model.embed_tokens.weight']
        expected += [n for n in selected if ('.q_proj.' in n and 'moe_gen' not in n)] if task=='ce' else [n for n in selected if ('q_proj_moe_gen' in n or n.startswith(('vae2llm.','llm2vae.','time_embedder.')))]
        # A bias can have an exact zero gradient for symmetry; require each target module's weight.
        expected=[n for n in expected if n.endswith('weight')]
        valid=all(gradients[n]['finite'] and gradients[n]['norm']>0 for n in expected)
        row={'task':task,'raw_loss':float(raw.detach()),'weighted_loss':float(loss.detach()),'gradients':gradients,'required_nonzero':expected,'passed':valid}
        task_records.append(row)
        write_json(run/f'{label}_step{step}_gradients.json',task_records)
        log(f'{label} step {step} {task} loss={row["raw_loss"]}, gradients={valid}')
        if not valid: raise RuntimeError(f'{task} expected native gradients missing, zero or non-finite')
        for n,p in selected.items():
            if existing[n] is not None:
                if p.grad is None: p.grad=existing[n]
                else: p.grad.add_(existing[n])
        del data,outputs,raw,loss,existing
    total_norm=torch.nn.utils.clip_grad_norm_(list(selected.values()),plan['max_grad_norm'],error_if_nonfinite=True)
    optimizer.step()
    scheduler.step()
    torch.cuda.synchronize()
    updates={n:{'max_abs_delta':float((p.detach().cpu()-before[n]).abs().max()),'changed':not torch.equal(p.detach().cpu(),before[n])} for n,p in selected.items()}
    unchanged_frozen=all(p._version==frozen_versions[n] for n,p in model.named_parameters() if not p.requires_grad)
    row={'step':step,'tasks':task_records,'updates':updates,'frozen_parameter_versions_unchanged':unchanged_frozen,
         'gradient_norm_before_clip':float(total_norm),'optimizer_lr_after_step':optimizer.param_groups[0]['lr'],
         'cuda_peak_allocated_bytes':torch.cuda.max_memory_allocated(),'cuda_peak_reserved_bytes':torch.cuda.max_memory_reserved(),
         'wall_seconds':time.perf_counter()-started,'host_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
    if not unchanged_frozen or not all(updates[n]['changed'] for n in task_records[0]['required_nonzero']+task_records[1]['required_nonzero']):
        raise RuntimeError('Target update or frozen-parameter integrity failed')
    write_json(run/f'{label}_step{step}.json',row)
    optimizer.zero_grad(set_to_none=True)
    return row


def snapshot(selected,optimizer,scheduler,step,plan):
    import torch
    # CPU copies avoid saving device allocations or retaining a second model on GPU.
    def cpu(x):
        if isinstance(x,torch.Tensor):return x.detach().cpu().clone()
        if isinstance(x,dict):return {k:cpu(v) for k,v in x.items()}
        if isinstance(x,list):return [cpu(v) for v in x]
        if isinstance(x,tuple):return tuple(cpu(v) for v in x)
        return x
    return dict(trainable=cpu(selected),optimizer=cpu(optimizer.state_dict()),scheduler=scheduler.state_dict(),
                rng=rng_state(),step=step,data_progress={'fixed_batch_next_step':step+1},plan=plan,
                frozen_base=dict(code_revision=plan['code_revision'],weight_revision=plan['weight_revision'],initialization_seed=plan['seed']))


def equal_tree(left,right):
    import torch
    import numpy as np
    if isinstance(left,torch.Tensor): return isinstance(right,torch.Tensor) and torch.equal(left.cpu(),right.cpu())
    if isinstance(left,np.ndarray): return isinstance(right,np.ndarray) and np.array_equal(left,right)
    if isinstance(left,dict): return left.keys()==right.keys() and all(equal_tree(left[k],right[k]) for k in left)
    if isinstance(left,(tuple,list)): return type(left)==type(right) and len(left)==len(right) and all(equal_tree(x,y) for x,y in zip(left,right))
    return left==right


def train_or_resume(bundle,run,plan,stage):
    import torch
    model,vae,selected=build_model(bundle,run,plan)
    loading_peak={'allocated':torch.cuda.max_memory_allocated(),'reserved':torch.cuda.max_memory_reserved()}
    batches=torch.load(run/'packed_batches.pt',weights_only=False,map_location='cpu')
    opt=plan['optimizer']
    optimizer=torch.optim.AdamW(list(selected.values()),lr=opt['lr'],betas=tuple(opt['betas']),eps=opt['eps'],weight_decay=opt['weight_decay'],foreach=opt['foreach'])
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=1,gamma=plan['scheduler']['gamma'])
    if stage=='train':
        seed_all(plan['seed']+1)
        one_step(model,vae,selected,optimizer,scheduler,batches,plan,1,run,'initial')
        checkpoint=snapshot(selected,optimizer,scheduler,1,plan)
        torch.save(checkpoint,run/'checkpoint_step1.pt')
        del checkpoint
        gc.collect()
        one_step(model,vae,selected,optimizer,scheduler,batches,plan,2,run,'reference')
        torch.save(snapshot(selected,optimizer,scheduler,2,plan),run/'reference_step2.pt')
        write_json(run/'train_result.json',{'status':'passed','loading_cuda_peak_bytes':loading_peak,'initial_steps':1,'reference_continuation_steps':1})
    else:
        checkpoint=torch.load(run/'checkpoint_step1.pt',map_location='cpu',weights_only=False)
        if checkpoint['plan']!=plan or checkpoint['trainable'].keys()!=selected.keys():raise RuntimeError('Checkpoint recipe/parameter names mismatch')
        with torch.no_grad():
            for name,p in selected.items():p.copy_(checkpoint['trainable'][name])
        optimizer.load_state_dict(checkpoint['optimizer'])
        scheduler.load_state_dict(checkpoint['scheduler'])
        restore_rng(checkpoint['rng'])
        restored=snapshot(selected,optimizer,scheduler,checkpoint['step'],plan)
        checks={key:equal_tree(checkpoint[key],restored[key]) for key in checkpoint}
        write_json(run/'reload_exact_comparison.json',checks)
        if not all(checks.values()):raise RuntimeError('Saved training state did not restore exactly')
        del checkpoint,restored
        gc.collect()
        result=one_step(model,vae,selected,optimizer,scheduler,batches,plan,2,run,'resumed')
        reference=torch.load(run/'reference_step2.pt',map_location='cpu',weights_only=False)
        actual=snapshot(selected,optimizer,scheduler,2,plan)
        parameter_deltas={n:float((actual['trainable'][n]-reference['trainable'][n]).abs().max()) for n in selected}
        tol=plan['acceptance']
        params_close=all(torch.allclose(actual['trainable'][n],reference['trainable'][n],atol=tol['continuation_parameter_atol'],rtol=tol['continuation_parameter_rtol']) for n in selected)
        original=json.loads((run/'reference_step2.json').read_text())
        losses_close=all(abs(a['raw_loss']-b['raw_loss'])<=tol['continuation_loss_atol']+tol['continuation_loss_rtol']*abs(a['raw_loss']) for a,b in zip(original['tasks'],result['tasks']))
        comparison={'parameters_exact':equal_tree(actual['trainable'],reference['trainable']),'parameters_within_preregistered_tolerance':params_close,
                    'parameter_max_abs_difference':parameter_deltas,'losses_within_preregistered_tolerance':losses_close,
                    'optimizer_exact':equal_tree(actual['optimizer'],reference['optimizer']),
                    'scheduler_exact':equal_tree(actual['scheduler'],reference['scheduler']),'rng_exact':equal_tree(actual['rng'],reference['rng']),
                    'status':'passed' if params_close and losses_close else 'failed','loading_cuda_peak_bytes':loading_peak}
        write_json(run/'continuation_comparison.json',comparison)
        if comparison['status']!='passed':raise RuntimeError('Continuation differs beyond preregistered tolerance')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,required=True)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--stage',choices=['audit','train','resume'],required=True)
    args=parser.parse_args()
    STAGE=args.stage
    bundle=args.bundle.resolve();run=args.run.resolve()
    os.chdir(bundle/'upstream');sys.path.insert(0,str(bundle/'upstream'))
    plan=json.loads((run/'plan.json').read_text())
    started=time.perf_counter()
    try:
        if STAGE=='audit': audit_and_pack(bundle,run,plan)
        else:train_or_resume(bundle,run,plan,STAGE)
    except BaseException:
        write_json(run/f'{STAGE}_failure.json',{'error':traceback.format_exc(),'elapsed_seconds':time.perf_counter()-started})
        raise
    finally:
        metrics={'wall_seconds':time.perf_counter()-started,'host_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
        torch=sys.modules.get('torch')
        if torch is not None and torch.cuda.is_initialized():
            metrics.update(cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated(),cuda_peak_reserved_bytes=torch.cuda.max_memory_reserved())
        write_json(run/f'{STAGE}_duration.json',metrics)
