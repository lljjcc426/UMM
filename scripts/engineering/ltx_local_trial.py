"""Two small native LTX requests on a Mac; stages run in separate processes.

Uses unmodified official LTX source. Prompt encoding finishes and exits before
video weights load, because CPU and MPS share this machine's physical memory.
"""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import sys
import threading
import time
import traceback


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def worker(args, config):
    import torch
    from safetensors.torch import load_file, save_file

    sys.path.insert(0, str(args.upstream.resolve()))
    torch.set_num_threads(6)
    torch.mps.set_per_process_memory_fraction(.95)
    started = time.monotonic()
    metrics = {'stage': args.stage, 'device': 'mps', 'status': 'running',
               'peak_mps_allocated_bytes': 0, 'peak_mps_driver_bytes': 0}
    stopped = threading.Event()

    def sample():
        while not stopped.wait(.5):
            metrics['peak_mps_allocated_bytes'] = max(
                metrics['peak_mps_allocated_bytes'], torch.mps.current_allocated_memory())
            metrics['peak_mps_driver_bytes'] = max(
                metrics['peak_mps_driver_bytes'], torch.mps.driver_allocated_memory())

    monitor = threading.Thread(target=sample, daemon=True)
    monitor.start()
    try:
        if args.stage == 'encode':
            from transformers import T5EncoderModel, T5Tokenizer
            from unittest.mock import patch
            from ltx_video.pipelines.pipeline_ltx_video import LTXVideoPipeline
            tokenizer = T5Tokenizer.from_pretrained(args.models / 'tokenizer', local_files_only=True)
            prompts = LTXVideoPipeline._text_preprocessing(None, [config['prompt'], ''])
            tokens = tokenizer(prompts, padding='max_length', max_length=256,
                               truncation=True, return_tensors='pt')
            actual = {'raw_prompts': [config['prompt'], ''], 'preprocessed_prompts': prompts,
                      'input_ids': tokens.input_ids.tolist(),
                      'attention_mask': tokens.attention_mask.tolist(),
                      'unknown_token_counts': (tokens.input_ids == tokenizer.unk_token_id).sum(1).tolist()}
            save(args.output / 'actual_text_input.json', actual)
            print('Loading T5 on MPS in bfloat16, without video weights', flush=True)
            # Transformers 4.51.3 prewarms its allocator with one 9.12 GiB
            # buffer. Metal rejects that single allocation before any weights
            # load. Skip only this performance optimization; real tensors are
            # still loaded normally, with unchanged weights and arithmetic.
            print('MPS loader: skip CUDA-oriented single-buffer allocator warmup', flush=True)
            with patch('transformers.modeling_utils.caching_allocator_warmup', lambda *a, **kw: None):
                encoder = T5EncoderModel.from_pretrained(
                    args.models / 'text_encoder', torch_dtype=torch.bfloat16,
                    device_map={'': 'mps'}, low_cpu_mem_usage=True, local_files_only=True).eval()
            tensors = {}
            with torch.inference_mode():
                for index, key in enumerate(('positive', 'negative')):
                    ids = tokens.input_ids[index:index + 1].to('mps')
                    mask = tokens.attention_mask[index:index + 1].to('mps')
                    tensors[key] = encoder(ids, attention_mask=mask)[0].cpu().contiguous()
                    tensors[key + '_mask'] = mask.cpu().contiguous()
            save_file(tensors, str(args.output / 'prompt_embeddings.safetensors'))
            metrics['finite_embeddings'] = all(torch.isfinite(t).all().item() for t in tensors.values())
            if not metrics['finite_embeddings']:
                raise ValueError('Text encoder produced non-finite embeddings')
        else:
            import numpy as np
            import imageio.v2 as imageio
            from safetensors import safe_open
            from ltx_video.models.autoencoders.causal_video_autoencoder import CausalVideoAutoencoder
            from ltx_video.models.transformers.transformer3d import Transformer3DModel
            from ltx_video.models.transformers.symmetric_patchifier import SymmetricPatchifier
            from ltx_video.schedulers.rf import RectifiedFlowScheduler
            from ltx_video.pipelines.pipeline_ltx_video import LTXVideoPipeline, ConditioningItem
            from ltx_video.inference import load_image_to_tensor_with_resize_and_crop

            checkpoint = args.models / config['checkpoint']
            with safe_open(checkpoint, framework='pt') as f:
                checkpoint_config = json.loads(f.metadata()['config'])
            save(args.output / 'checkpoint_config.json', checkpoint_config)
            print('Loading video transformer and VAE; text encoder is absent', flush=True)
            transformer = Transformer3DModel.from_pretrained(checkpoint).to(dtype=torch.bfloat16)
            vae = CausalVideoAutoencoder.from_pretrained(checkpoint, torch_dtype=torch.bfloat16)
            pipeline = LTXVideoPipeline(
                tokenizer=None, text_encoder=None, vae=vae, transformer=transformer,
                scheduler=RectifiedFlowScheduler.from_pretrained(checkpoint),
                patchifier=SymmetricPatchifier(patch_size=1),
                prompt_enhancer_image_caption_model=None,
                prompt_enhancer_image_caption_processor=None,
                prompt_enhancer_llm_model=None, prompt_enhancer_llm_tokenizer=None,
                allowed_inference_steps=checkpoint_config.get('allowed_inference_steps')).to('mps')
            # The official pipeline moves cached embeddings, but assumes cached
            # masks already share their device. Keep both on MPS for SDPA.
            embeddings = {key: value.to('mps') for key, value in
                          load_file(str(args.output / 'prompt_embeddings.safetensors')).items()}
            conditioning = None
            if args.stage == 'image':
                media = load_image_to_tensor_with_resize_and_crop(
                    str(args.output / 'target.png'), config['height'], config['width'])
                conditioning = [ConditioningItem(media_item=media,
                    media_frame_number=config['image_condition_frame'], conditioning_strength=1.)]
            request = dict(config, stage=args.stage, text_encoder_present=False,
                           conditioning_image=str(args.output / 'target.png') if conditioning else None,
                           prompt_embedding_file=str(args.output / 'prompt_embeddings.safetensors'))
            save(args.output / f'{args.stage}_actual_request.json', request)

            def step(pipe, index, timestep, values):
                torch.mps.synchronize()
                print(json.dumps({'step': index, 'timestep': float(timestep),
                                  'elapsed_seconds': round(time.monotonic() - started, 2),
                                  'mps_driver_bytes': torch.mps.driver_allocated_memory()}), flush=True)

            torch.manual_seed(config['seed'])
            torch.mps.manual_seed(config['seed'])
            inference_started = time.monotonic()
            with torch.inference_mode():
                images = pipeline(
                    height=config['height'], width=config['width'], num_frames=config['num_frames'],
                    frame_rate=config['fps'], prompt=None, negative_prompt=None,
                    prompt_embeds=embeddings['positive'], prompt_attention_mask=embeddings['positive_mask'],
                    negative_prompt_embeds=embeddings['negative'],
                    negative_prompt_attention_mask=embeddings['negative_mask'],
                    timesteps=config['timesteps'], num_inference_steps=len(config['timesteps']),
                    guidance_scale=1., stg_scale=0., rescaling_scale=1.,
                    decode_timestep=.05, decode_noise_scale=.025,
                    generator=torch.Generator(device='mps').manual_seed(config['seed']),
                    conditioning_items=conditioning, image_cond_noise_scale=.15,
                    output_type='pt', callback_on_step_end=step,
                    is_video=True, vae_per_channel_normalize=True,
                    enhance_prompt=False, mixed_precision=False, offload_to_cpu=False,
                    stochastic_sampling=False).images
            torch.mps.synchronize()
            metrics['inference_seconds'] = time.monotonic() - inference_started
            metrics['finite_video_tensor'] = torch.isfinite(images).all().item()
            if not metrics['finite_video_tensor']:
                raise ValueError('Video model produced non-finite pixels')
            frames = (images[0].permute(1, 2, 3, 0).float().cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
            np.save(args.output / f'{args.stage}_source_rgb.npy', frames)
            imageio.mimwrite(args.output / f'{args.stage}.mp4', frames, fps=config['fps'],
                            codec='libx264', quality=9, macro_block_size=1)
            metrics['source_shape'] = list(frames.shape)
        metrics['status'] = 'completed'
    except Exception:
        metrics['status'] = 'failed'
        metrics['traceback'] = traceback.format_exc()
        raise
    finally:
        stopped.set()
        monitor.join()
        metrics['wall_seconds'] = time.monotonic() - started
        metrics['peak_process_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        save(args.output / f'{args.stage}_metrics.json', metrics)


def audit(output, stage):
    import av
    import numpy as np
    from PIL import Image, ImageDraw
    with av.open(str(output / f'{stage}.mp4')) as video:
        stream = video.streams.video[0]
        fps = float(stream.average_rate)
        decoded = list(video.decode(video=0))
        pts = [float(f.pts * f.time_base) for f in decoded]
        frames = np.stack([f.to_ndarray(format='rgb24') for f in decoded])
    indices = np.linspace(0, len(frames) - 1, 9, dtype=int).tolist()
    sheet = Image.new('RGB', (3 * 256, 3 * 280), 'white')
    draw = ImageDraw.Draw(sheet)
    for position, index in enumerate(indices):
        x, y = position % 3 * 256, position // 3 * 280
        sheet.paste(Image.fromarray(frames[index]), (x, y + 24))
        draw.text((x + 4, y + 4), f'{stage} frame {index} / {pts[index]:.3f}s', fill='black')
    sheet.save(output / f'{stage}_contact.png')
    return {'frames': len(frames), 'shape': list(frames.shape), 'fps': fps, 'pts_seconds': pts,
            'pts_strictly_increasing': all(a < b for a, b in zip(pts, pts[1:])),
            'mean_frame_change': float(np.abs(np.diff(frames.astype('float32'), axis=0)).mean()),
            'first_frame_dark_fraction': float((frames[0].mean(2) < 128).mean()),
            'last_frame_dark_fraction': float((frames[-1].mean(2) < 128).mean())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--models', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage', choices=['encode', 'text', 'image'])
    args = parser.parse_args()
    config = json.loads((args.output / 'config.json').read_text())
    if args.stage:
        worker(args, config)
        return
    results = {}
    for stage in ('encode', 'text', 'image'):
        if stage == 'encode' and (args.output / 'prompt_embeddings.safetensors').exists():
            results[stage] = {'status': 'reused', 'source': config['embedding_source']}
            save(args.output / 'results.json', results)
            continue
        command = [sys.executable, '-u', str(Path(__file__).resolve()), '--upstream', str(args.upstream),
                   '--models', str(args.models), '--output', str(args.output), '--stage', stage]
        started = time.monotonic()
        with (args.output / f'{stage}.log').open('w') as log:
            try:
                process = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=600)
                result = {'returncode': process.returncode, 'status': 'completed' if process.returncode == 0 else 'failed'}
            except subprocess.TimeoutExpired:
                result = {'status': 'timeout', 'limit_seconds': 600}
        result['wall_seconds'] = time.monotonic() - started
        if stage != 'encode' and result['status'] == 'completed':
            result['decode'] = audit(args.output, stage)
        results[stage] = result
        save(args.output / 'results.json', results)
        print(json.dumps({stage: result}, ensure_ascii=False), flush=True)
        if stage == 'encode' and result['status'] != 'completed':
            results.update({s: {'status': 'blocked', 'reason': 'text_encoding_failed'} for s in ('text', 'image')})
            save(args.output / 'results.json', results)
            break


if __name__ == '__main__':
    main()
