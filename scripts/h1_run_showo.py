"""Run answer and current-image-state diagnostics with the complete Show-o2 video UMM."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REVISION = '45a5a2de01d1ebd10cd5864d29310a76476cdf23'
MODEL_REVISION = '412f647429897ad888771d18008de4edfb2c42a6'


def run(args):
    sys.path.insert(0, str(args.source.resolve() / 'show-o2'))
    import torch
    from transformers import SiglipConfig
    from models import Showo2Qwen2_5, omni_attn_mask_naive
    from models.misc import get_text_tokenizer
    from models.modeling_siglip import SiglipModel

    rows = [json.loads(s) for s in args.inputs.read_text().splitlines()]
    rows = [r for r in rows if r['split'] == args.split
            and r['response_format'] == args.format and r['view'] == args.view]
    if args.limit:
        rows = rows[:args.limit]
    if not rows:
        raise ValueError('No matching inputs.')
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'inputs.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    torch.manual_seed(0)
    tokenizer, token_ids = get_text_tokenizer(
        str(args.assets / 'Qwen2.5-1.5B-Instruct'), return_showo_token_ids=True)

    # All retained SigLIP weights are in the unified checkpoint. Construct its
    # architecture under the upstream meta initialization, then load the full
    # checkpoint with upstream missing-key checks. No separate base weights used.
    def siglip_structure(path, **kwargs):
        return SiglipModel(SiglipConfig.from_pretrained(path, local_files_only=True))

    with patch.object(SiglipModel, 'from_pretrained', side_effect=siglip_structure):
        model = Showo2Qwen2_5.from_pretrained(
            str(args.model), use_safetensors=False, torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            llm_model_path=str(args.assets / 'Qwen2.5-1.5B-Instruct'),
            clip_pretrained_model_path=str(args.assets / 'siglip'))
    model.eval().requires_grad_(False)
    # Move only executed components; retain unused generation heads on CPU.
    model.showo.to(args.device)
    visual = args.blank_image or any(r['images'] for r in rows)
    if visual:
        from models import WanVAE
        vae = WanVAE(vae_pth=str(args.assets / 'Wan2.1_VAE.pth'), dtype=torch.float32, device='cpu')
        vae.model.float()
        for name in ['image_embedder_und', 'image_embedder_gen', 'position_embedding',
                     'und_trans', 'fusion_proj', 'time_embed', 'time_embed_proj']:
            getattr(model, name).to(args.device)
        model.image_position_ids = model.image_position_ids.to(args.device)
    image_cache = {}
    metadata = dict(
        model_id='showlab/show-o2-1.5B-w-video-und', model_revision=MODEL_REVISION,
        download_source='ModelScope', source_revision=SOURCE_REVISION,
        condition='frozen_full_UMM_image_path' if visual else 'frozen_full_UMM_text_state_prerequisite',
        model_components=list(dict(model.named_children())),
        total_parameters=sum(p.numel() for p in model.parameters()),
        understanding_parameters=sum(p.numel() for p in model.showo.parameters()),
        device=args.device, dtype='bfloat16', unused_modules_device='cpu',
        input_manifest=str(args.inputs.resolve().relative_to(ROOT)),
        samples=[r['sample_id'] for r in rows], split=args.split, response_format=args.format,
        source_prompt=args.chat_template,
        view=args.view, blank_visual_condition=args.blank_image,
        image_preprocessing='432x432 RGB [-1,1]; already square input; no crop' if visual else None,
        vae_device='cpu' if visual else None, vae_dtype='float32' if visual else None,
        vae_sampling='sample; seed=0 per image; embeddings cached per image' if visual else None,
        decoding='official mmu_generate; top_k=1; seed=0', max_new_tokens=args.max_tokens,
        checkpoint_loading='upstream complete state load; SigLIP architecture-only initialization',
        started_utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
        platform=platform.platform(),
        packages={p: importlib.metadata.version(p) for p in
                  ['torch', 'transformers', 'diffusers', 'accelerate', 'timm', 'Pillow']})
    (args.output / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Loaded full UMM: {metadata["total_parameters"]:,} parameters', flush=True)
    system = tokenizer('system\nYou are a helpful assistant.<|im_end|>', add_special_tokens=False).input_ids
    user = tokenizer('\n<|im_start|>user\n', add_special_tokens=False).input_ids
    assistant = tokenizer('\n<|im_start|>assistant\n', add_special_tokens=False).input_ids

    def synchronize():
        if args.device == 'cuda':
            torch.cuda.synchronize()
        elif args.device == 'mps':
            torch.mps.synchronize()

    def encode_image(row):
        from PIL import Image
        import numpy as np
        key = 'blank' if args.blank_image else row['images'][0]
        if key not in image_cache:
            image = Image.new('RGB', (432, 432), 'white') if args.blank_image else Image.open(
                args.inputs.parent / key).convert('RGB')
            if image.size != (432, 432):
                raise ValueError('This state benchmark requires uncropped 432x432 images.')
            pixels = torch.from_numpy(np.asarray(image).copy()).permute(2, 0, 1).float() / 127.5 - 1
            torch.manual_seed(0)
            latents = vae.sample(pixels[None, :, None]).squeeze(2).to(args.device, torch.bfloat16)
            und = model.image_embedder_und(latents)
            gen = model.image_embedder_gen(latents)
            und = model.und_trans(und + model.position_embedding(model.image_position_ids))['last_hidden_state']
            image_cache[key] = model.fusion_proj(torch.cat([und, gen], dim=-1))
        return image_cache[key]

    with (args.output / 'predictions.jsonl').open('w') as out, torch.inference_mode():
        for index, row in enumerate(rows, 1):
            encode_started = time.perf_counter()
            if visual:
                vision = encode_image(row)
                a = torch.tensor([[token_ids['bos_id']] + system + user], device=args.device)
                b = torch.tensor([[token_ids['boi_id'], token_ids['eoi_id']] + tokenizer(
                    row['prompt'], add_special_tokens=False).input_ids + assistant], device=args.device)
                a_embeds = model.showo.model.embed_tokens(a)
                b_embeds = model.showo.model.embed_tokens(b)
                time_embed = model.time_embed(torch.tensor([[1.0]], device=args.device), a_embeds.dtype)
                time_embed = model.time_embed_proj(time_embed)
                embeds = torch.cat([a_embeds, b_embeds[:, :1], time_embed, vision, b_embeds[:, 1:]], dim=1)
                # Preserve the upstream image MMU modality block convention.
                modalities = torch.tensor([[[a.shape[1] + 2, vision.shape[1] + 1]]], device=args.device)
            elif args.chat_template == 'official_mmu':
                ids = [token_ids['bos_id']] + system + user + tokenizer(
                    row['prompt'], add_special_tokens=False).input_ids + assistant
            else:
                ids = tokenizer.apply_chat_template([
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': row['prompt']}], add_generation_prompt=True)
            if not visual:
                ids = torch.tensor([ids], device=args.device)
                embeds = model.showo.model.embed_tokens(ids)
                modalities = torch.empty((1, 0, 2), dtype=torch.long)
            mask = omni_attn_mask_naive(
                B=1, LEN=embeds.shape[1], modalities=modalities,
                device=args.device, inverted=True).to(embeds.dtype)
            synchronize()
            encode_seconds = time.perf_counter() - encode_started
            started = time.perf_counter()
            tokens = model.mmu_generate(input_embeds=embeds, attention_mask=mask,
                                        top_k=1, max_new_tokens=args.max_tokens,
                                        eos_token=tokenizer.eos_token_id)
            synchronize()
            raw = tokenizer.decode([t.item() for t in tokens], skip_special_tokens=True)
            record = dict(sample_id=row['sample_id'], raw_response=raw,
                          prompt_tokens=embeds.shape[1], generation_tokens=len(tokens),
                          input_preparation_seconds=encode_seconds,
                          seconds=time.perf_counter() - started)
            out.write(json.dumps(record, ensure_ascii=False) + '\n')
            out.flush()
            print(f'{index}/{len(rows)} {row["sample_id"]} {raw!r} {record["seconds"]:.2f}s', flush=True)
    metadata['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (args.output / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=ROOT / 'checkpoints/Show-o-source')
    p.add_argument('--model', type=Path, default=ROOT / 'checkpoints/Show-o2-1.5B-video')
    p.add_argument('--assets', type=Path, default=ROOT / 'checkpoints/Show-o-assets')
    p.add_argument('--inputs', type=Path, default=ROOT / 'data/h1/state_gate_v1/inputs.jsonl')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--device', choices=['cpu', 'cuda', 'mps'], default='cuda')
    p.add_argument('--split', choices=['dev', 'test'], default='dev')
    p.add_argument('--format', choices=['plain', 'json'], default='plain')
    p.add_argument('--max-tokens', type=int, default=32)
    p.add_argument('--limit', type=int)
    p.add_argument('--chat-template', choices=['official_mmu', 'tokenizer'], default='tokenizer')
    p.add_argument('--view', choices=['oracle_text', 'reference_current', 'current_only'], default='oracle_text')
    p.add_argument('--blank-image', action='store_true', help='Use a blank image with text facts to check native MMU routing.')
    args = p.parse_args()
    if args.blank_image and args.view != 'oracle_text':
        p.error('--blank-image is only a control for oracle_text; it cannot replace observed images.')
    if args.blank_image or args.view != 'oracle_text':
        args.chat_template = 'official_mmu'
    run(args)
