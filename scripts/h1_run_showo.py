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
STATE_WORDS = {'presence': ['有', '无'], 'completion': ['未出现', '部分', '完整', '未知']}


def load_model(source, model_path, assets, device):
    """Load the unified checkpoint; shared by frozen inference and adaptation."""
    sys.path.insert(0, str(source.resolve() / 'show-o2'))
    import torch
    from transformers import SiglipConfig
    from models import Showo2Qwen2_5
    from models.misc import get_text_tokenizer
    from models.modeling_siglip import SiglipModel

    torch.manual_seed(0)
    tokenizer, token_ids = get_text_tokenizer(
        str(assets / 'Qwen2.5-1.5B-Instruct'), return_showo_token_ids=True)

    # All retained SigLIP weights are in the unified checkpoint. Construct its
    # architecture under the upstream meta initialization, then load the full
    # checkpoint with upstream missing-key checks. No separate base weights used.
    def siglip_structure(path, **kwargs):
        return SiglipModel(SiglipConfig.from_pretrained(path, local_files_only=True))

    with patch.object(SiglipModel, 'from_pretrained', side_effect=siglip_structure):
        model = Showo2Qwen2_5.from_pretrained(
            str(model_path), use_safetensors=False, torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            llm_model_path=str(assets / 'Qwen2.5-1.5B-Instruct'),
            clip_pretrained_model_path=str(assets / 'siglip'))
    model.eval().requires_grad_(False)
    # Move only executed components; retain unused generation heads on CPU.
    model.showo.to(device)
    return model, tokenizer, token_ids


def text_prompt_ids(tokenizer, token_ids, prompt, template='tokenizer'):
    if template == 'tokenizer':
        return tokenizer.apply_chat_template([
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}], add_generation_prompt=True)
    parts = ['system\nYou are a helpful assistant.<|im_end|>', '\n<|im_start|>user\n',
             prompt, '\n<|im_start|>assistant\n']
    return [token_ids['bos_id']] + [i for part in parts for i in
                                   tokenizer(part, add_special_tokens=False).input_ids]


class StateImageEncoder:
    """Frozen native image path shared by state training and evaluation."""
    def __init__(self, model, assets, device):
        import torch
        from models import WanVAE
        self.model, self.device = model, device
        self.vae = WanVAE(vae_pth=str(assets / 'Wan2.1_VAE.pth'), dtype=torch.float32, device='cpu')
        self.vae.model.float()
        for name in ['image_embedder_und', 'image_embedder_gen', 'position_embedding',
                     'und_trans', 'fusion_proj', 'time_embed', 'time_embed_proj']:
            getattr(model, name).to(device)
        model.image_position_ids = model.image_position_ids.to(device)
        self.cache = {}

    def encode(self, path=None):
        import torch
        import numpy as np
        from PIL import Image
        key = str(path) if path is not None else 'blank'
        if key not in self.cache:
            image = Image.open(path).convert('RGB') if path is not None else Image.new('RGB', (432, 432), 'white')
            if image.size != (432, 432):
                raise ValueError('This state benchmark requires uncropped 432x432 images.')
            # no_grad keeps features usable as constants in later adapter autograd.
            with torch.no_grad():
                pixels = torch.from_numpy(np.asarray(image).copy()).permute(2, 0, 1).float() / 127.5 - 1
                torch.manual_seed(0)
                latents = self.vae.sample(pixels[None, :, None]).squeeze(2).to(self.device, torch.bfloat16)
                und = self.model.image_embedder_und(latents)
                gen = self.model.image_embedder_gen(latents)
                und = self.model.und_trans(und + self.model.position_embedding(self.model.image_position_ids))['last_hidden_state']
                self.cache[key] = self.model.fusion_proj(torch.cat([und, gen], dim=-1)).cpu()
        return self.cache[key].to(self.device)


def image_prompt_embeds(model, tokenizer, token_ids, prompt, vision, device):
    """Keep the upstream MMU prompt and modality mask convention unchanged."""
    import torch
    system = tokenizer('system\nYou are a helpful assistant.<|im_end|>', add_special_tokens=False).input_ids
    user = tokenizer('\n<|im_start|>user\n', add_special_tokens=False).input_ids
    assistant = tokenizer('\n<|im_start|>assistant\n', add_special_tokens=False).input_ids
    a = torch.tensor([[token_ids['bos_id']] + system + user], device=device)
    b = torch.tensor([[token_ids['boi_id'], token_ids['eoi_id']] + tokenizer(
        prompt, add_special_tokens=False).input_ids + assistant], device=device)
    a_embeds = model.showo.model.embed_tokens(a)
    b_embeds = model.showo.model.embed_tokens(b)
    time_embed = model.time_embed(torch.tensor([[1.0]], device=device), a_embeds.dtype)
    time_embed = model.time_embed_proj(time_embed)
    embeds = torch.cat([a_embeds, b_embeds[:, :1], time_embed, vision, b_embeds[:, 1:]], dim=1)
    modalities = torch.tensor([[[a.shape[1] + 2, vision.shape[1] + 1]]], device=device)
    return embeds, modalities


def constrained_state_generate(model, tokenizer, embeds, modalities, task):
    """Greedy decoding inside a fixed answer trie; no ground-truth label is read."""
    import torch
    from models import omni_attn_mask_naive
    candidates = [tokenizer(json.dumps({'answer': word}, ensure_ascii=False, separators=(',', ':')),
                            add_special_tokens=False).input_ids + [tokenizer.eos_token_id]
                  for word in STATE_WORDS[task]]
    output = []
    for position in range(max(map(len, candidates))):
        allowed = sorted({seq[position] for seq in candidates})
        if len(allowed) == 1:
            token = allowed[0]
        else:
            mask = omni_attn_mask_naive(B=1, LEN=embeds.shape[1], modalities=modalities,
                                       device=embeds.device, inverted=True).to(embeds.dtype)
            logits = model.showo(inputs_embeds=embeds, attention_mask=mask, use_cache=False,
                                 num_logits_to_keep=1)['logits'][0, -1]
            token = allowed[logits[allowed].argmax().item()]
        output.append(token)
        candidates = [seq for seq in candidates if seq[position] == token]
        if token == tokenizer.eos_token_id:
            break
        new = model.showo.model.embed_tokens(torch.tensor([[token]], device=embeds.device))
        embeds = torch.cat([embeds, new], dim=1)
    return output


def run(args):
    import torch
    rows = [json.loads(s) for s in args.inputs.read_text().splitlines()]
    rows = [r for r in rows if r['split'] == args.split
            and r['response_format'] == args.format and r['view'] == args.view]
    if args.limit:
        rows = rows[:args.limit]
    if not rows:
        raise ValueError('No matching inputs.')
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'inputs.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    model, tokenizer, token_ids = load_model(args.source, args.model, args.assets, args.device)
    from models import omni_attn_mask_naive
    adapter_config = None
    if args.adapter:
        from h1_train_state import load_adapter
        adapter_config = load_adapter(model, args.adapter, args.device)
        model.eval().requires_grad_(False)
    visual = args.blank_image or any(r['images'] for r in rows)
    encoder = StateImageEncoder(model, args.assets, args.device) if visual else None
    metadata = dict(
        model_id='showlab/show-o2-1.5B-w-video-und', model_revision=MODEL_REVISION,
        download_source='ModelScope', source_revision=SOURCE_REVISION,
        condition=('adapted_' if args.adapter else 'frozen_') +
                  ('full_UMM_image_path' if visual else 'full_UMM_text_state_prerequisite'),
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
        decoding=('greedy fixed-answer trie; shared tokens forced; no label access' if args.constrain_answers else
                  'official mmu_generate; top_k=1; seed=0'), max_new_tokens=args.max_tokens,
        constrained_state_words=STATE_WORDS if args.constrain_answers else None,
        checkpoint_loading='upstream complete state load; SigLIP architecture-only initialization',
        adapter=str(args.adapter.resolve().relative_to(ROOT)) if args.adapter else None,
        adapter_config=adapter_config,
        started_utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
        platform=platform.platform(),
        packages={p: importlib.metadata.version(p) for p in
                  ['torch', 'transformers', 'diffusers', 'accelerate', 'timm', 'Pillow']})
    (args.output / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Loaded full UMM: {metadata["total_parameters"]:,} parameters', flush=True)

    def synchronize():
        if args.device == 'cuda':
            torch.cuda.synchronize()
        elif args.device == 'mps':
            torch.mps.synchronize()

    with (args.output / 'predictions.jsonl').open('w') as out, torch.inference_mode():
        for index, row in enumerate(rows, 1):
            encode_started = time.perf_counter()
            if visual:
                vision = encoder.encode(None if args.blank_image else args.inputs.parent / row['images'][0])
                embeds, modalities = image_prompt_embeds(model, tokenizer, token_ids, row['prompt'], vision, args.device)
            else:
                ids = text_prompt_ids(tokenizer, token_ids, row['prompt'], args.chat_template)
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
            if args.constrain_answers:
                tokens = constrained_state_generate(model, tokenizer, embeds, modalities, row['task'])
            else:
                tokens = model.mmu_generate(input_embeds=embeds, attention_mask=mask,
                                            top_k=1, max_new_tokens=args.max_tokens,
                                            eos_token=tokenizer.eos_token_id)
            synchronize()
            raw = tokenizer.decode([int(t) for t in tokens], skip_special_tokens=True)
            record = dict(sample_id=row['sample_id'], raw_response=raw,
                          prompt_tokens=embeds.shape[1], generation_tokens=len(tokens),
                          input_preparation_seconds=encode_seconds,
                          seconds=time.perf_counter() - started)
            out.write(json.dumps(record, ensure_ascii=False) + '\n')
            out.flush()
            if index == 1 or index % 25 == 0 or index == len(rows):
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
    p.add_argument('--split', choices=['train', 'dev', 'test'], default='dev')
    p.add_argument('--format', choices=['plain', 'json'], default='plain')
    p.add_argument('--max-tokens', type=int, default=32)
    p.add_argument('--limit', type=int)
    p.add_argument('--chat-template', choices=['official_mmu', 'tokenizer'], default='tokenizer')
    p.add_argument('--view', choices=['oracle_text', 'reference_current', 'current_only'], default='oracle_text')
    p.add_argument('--blank-image', action='store_true', help='Use a blank image with text facts to check native MMU routing.')
    p.add_argument('--adapter', type=Path, help='Local adapter checkpoint from h1_train_state.py.')
    p.add_argument('--constrain-answers', action='store_true', help='Generate only JSON with Chinese state words; format guaranteed by the interface.')
    args = p.parse_args()
    if args.constrain_answers and args.format != 'json':
        p.error('--constrain-answers requires --format json.')
    if args.blank_image and args.view != 'oracle_text':
        p.error('--blank-image is only a control for oracle_text; it cannot replace observed images.')
    if args.blank_image or args.view != 'oracle_text':
        args.chat_template = 'official_mmu'
    run(args)
