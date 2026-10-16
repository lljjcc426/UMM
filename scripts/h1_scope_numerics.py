"""Audit the observed initial-loss difference between the last-8 and all-28 LoRA runs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import torch
from torch.nn import functional as F

from h1_run_showo import (ROOT, load_model, StateImageEncoder, image_prompt_embeds,
                         constrained_state_generate)
from h1_train_state import load_adapter, extend_adapter_layers
from h1_state_gate import read_jsonl


def run(output):
    experiments = ROOT / 'results/h1/showo2_video_1_5b/fit_scope_v1'
    initial_steps = {name: read_jsonl(experiments / f'{name}_training/training.jsonl')[0]
                     for name in ('last8', 'all28')}
    data = ROOT / 'data/h1/state_target_controls_v1/training_subset'
    inputs = {r['sample_id']: r for r in read_jsonl(data / 'inputs.jsonl')}
    labels = {r['sample_id']: r for r in read_jsonl(data / 'labels.jsonl')}
    sample_ids = initial_steps['last8']['sample_ids']
    if sample_ids != initial_steps['all28']['sample_ids']:
        raise ValueError('The observed first batches differ.')
    assets = ROOT / 'checkpoints/Show-o-assets'
    model, tokenizer, token_ids = load_model(ROOT / 'checkpoints/Show-o-source',
        ROOT / 'checkpoints/Show-o2-1.5B-video', assets, 'mps')
    from models import omni_attn_mask_naive
    torch.manual_seed(731)
    config = load_adapter(model, ROOT / 'checkpoints/h1_target_contrast_lora_v1/adapter.pt', 'mps')
    encoder = StateImageEncoder(model, assets, 'mps')
    prepared = []
    with torch.no_grad():
        for sid in sample_ids:
            row = inputs[sid]
            vision = encoder.encode(data / row['images'][0])
            prompt, modalities = image_prompt_embeds(model, tokenizer, token_ids, row['prompt'], vision, 'mps')
            answer = json.dumps({'answer': labels[sid]['expected']}, ensure_ascii=False, separators=(',', ':'))
            ids = tokenizer(answer, add_special_tokens=False).input_ids
            answer_embeds = model.showo.model.embed_tokens(torch.tensor([ids], device='mps'))
            embeds = torch.cat([prompt, answer_embeds], dim=1)
            target = torch.tensor(ids + [tokenizer.eos_token_id], device='mps')
            mask = omni_attn_mask_naive(B=1, LEN=embeds.shape[1], modalities=modalities,
                device='mps', inverted=True).to(torch.bfloat16)
            prepared.append((row, prompt, modalities, embeds, target, mask))
    encoder.vae = None
    model.showo.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    report = dict(created_utc=datetime.now(timezone.utc).isoformat(),
        role='Post-hoc numeric diagnosis of the observed initial-loss difference; no updates or new model selection.',
        initial_adapter='checkpoints/h1_target_contrast_lora_v1/adapter.pt',
        sample_ids=sample_ids, original_first_steps=initial_steps,
        feature_policy='Encode each image once; reuse identical prompt and answer tensors in every condition.',
        conditions={})
    logits_by_condition = {}
    for scope in ('last8', 'all28'):
        if scope == 'all28':
            config = extend_adapter_layers(model, config, 28)
        for mode in ('inference', 'train', 'train_input_grad'):
            model.showo.train(mode != 'inference')
            entries, snapshots = [], []
            for row, prompt, modalities, embeds, target, mask in prepared:
                with torch.set_grad_enabled(mode != 'inference'):
                    x = embeds.detach().requires_grad_(mode == 'train_input_grad')
                    logits = model.showo(inputs_embeds=x, attention_mask=mask, use_cache=False,
                        num_logits_to_keep=len(target))['logits'][0]
                    loss = float(F.cross_entropy(logits.float(), target).detach())
                    snapshots.append(logits.detach().float().cpu())
                entries.append(dict(sample_id=row['sample_id'], answer_loss=loss))
                if mode == 'inference':
                    with torch.no_grad():
                        tokens = constrained_state_generate(model, tokenizer, prompt, modalities, row['task'])
                    entries[-1]['raw_response'] = tokenizer.decode(tokens, skip_special_tokens=True)
            key = f'{scope}/{mode}'
            logits_by_condition[key] = snapshots
            report['conditions'][key] = dict(mean_answer_loss=sum(x['answer_loss'] for x in entries)/len(entries), rows=entries)
            print(key, report['conditions'][key]['mean_answer_loss'], flush=True)
    report['logit_comparisons'] = {}
    for mode in ('inference', 'train', 'train_input_grad'):
        a, b = [logits_by_condition[f'{scope}/{mode}'] for scope in ('last8', 'all28')]
        report['logit_comparisons'][mode] = dict(
            max_abs_difference=max(float((x-y).abs().max()) for x,y in zip(a,b)),
            mean_abs_difference=sum(float((x-y).abs().mean()) for x,y in zip(a,b))/len(a))
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args().output)
