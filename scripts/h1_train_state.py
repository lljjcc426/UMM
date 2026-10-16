"""Small local LoRA adaptation of the complete UMM on accurate text state only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import math
from pathlib import Path
import random
import time

import torch
from torch import nn
from torch.nn import functional as F

from h1_run_showo import ROOT, SOURCE_REVISION, MODEL_REVISION, load_model, text_prompt_ids


class LoRALinear(nn.Module):
    def __init__(self, base, rank, alpha):
        super().__init__()
        self.base = base
        self.scale = alpha / rank
        self.lora_a = nn.Parameter(torch.empty(rank, base.in_features, device=base.weight.device))
        self.lora_b = nn.Parameter(torch.zeros(base.out_features, rank, device=base.weight.device))
        nn.init.kaiming_uniform_(self.lora_a, a=math.sqrt(5))

    def forward(self, x):
        update = F.linear(F.linear(x.float(), self.lora_a), self.lora_b)
        return self.base(x) + (update * self.scale).to(x.dtype)


def add_adapter(model, config):
    for index in config['layers']:
        attention = model.showo.model.layers[index].self_attn
        for name in config['projections']:
            setattr(attention, name, LoRALinear(getattr(attention, name), config['rank'], config['alpha']))


def load_adapter(model, path, device):
    checkpoint = torch.load(path, map_location='cpu', weights_only=True)
    add_adapter(model, checkpoint['config'])
    parameters = dict(model.named_parameters())
    with torch.no_grad():
        for name, value in checkpoint['state_dict'].items():
            parameters[name].copy_(value.to(device))
    return checkpoint['config']


def run(args):
    from h1_state_gate import read_jsonl, write_jsonl
    rows = [r for r in read_jsonl(args.data / 'inputs.jsonl') if r['split'] == 'train'
            and r['view'] == 'oracle_text' and r['response_format'] == 'json']
    labels = {r['sample_id']: r for r in read_jsonl(args.data / 'labels.jsonl')}
    args.output.mkdir(parents=True, exist_ok=False)
    args.adapter.parent.mkdir(parents=True, exist_ok=True)
    if args.adapter.exists():
        raise FileExistsError(args.adapter)
    write_jsonl(args.output / 'train_inputs.jsonl', rows)
    write_jsonl(args.output / 'train_labels.jsonl', [labels[r['sample_id']] for r in rows])
    model, tokenizer, token_ids = load_model(args.source, args.model, args.assets, args.device)
    from models import omni_attn_mask_naive
    torch.manual_seed(args.seed)
    adapter_config = dict(rank=args.rank, alpha=args.rank * 2,
                          layers=list(range(len(model.showo.model.layers) - args.last_layers,
                                            len(model.showo.model.layers))),
                          projections=['q_proj', 'v_proj'],
                          training_run=str(args.output.resolve().relative_to(ROOT)))
    add_adapter(model, adapter_config)
    model.showo.train()
    parameters = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=args.lr, weight_decay=0.01)
    encoded = []
    for row in rows:
        prompt = text_prompt_ids(tokenizer, token_ids, row['prompt'])
        answer = json.dumps({'answer': labels[row['sample_id']]['expected']}, ensure_ascii=False, separators=(',', ':'))
        answer_ids = tokenizer(answer, add_special_tokens=False).input_ids
        encoded.append((prompt + answer_ids, answer_ids + [tokenizer.eos_token_id]))
    steps_per_epoch = math.ceil(len(rows) / args.accumulation)
    total_steps = steps_per_epoch * args.epochs
    metadata = dict(model_id='showlab/show-o2-1.5B-w-video-und', model_revision=MODEL_REVISION,
                    source_revision=SOURCE_REVISION, stage='accurate_text_state_only',
                    train_rows=len(rows), train_cases=len({r['case_id'] for r in rows}),
                    train_groups=len({r['group_id'] for r in rows}), adapter_config=adapter_config,
                    trainable_parameters=sum(p.numel() for p in parameters),
                    base_dtype='bfloat16', adapter_dtype='float32', device=args.device,
                    epochs=args.epochs, steps=total_steps, accumulation=args.accumulation,
                    learning_rate=args.lr, schedule='10% warmup then cosine to 10% of peak',
                    optimizer='AdamW; weight_decay=0.01; clip_grad_norm=1.0', seed=args.seed,
                    loss='Mean answer-token cross entropy including EOS; prompt tokens not supervised.',
                    eval_policy='Evaluate frozen and final model on dev; no intermediate checkpoint selection.',
                    data=str(args.data.resolve().relative_to(ROOT)),
                    adapter_path=str(args.adapter.resolve().relative_to(ROOT)),
                    started_utc=datetime.now(timezone.utc).isoformat(),
                    packages={p: importlib.metadata.version(p) for p in ['torch', 'transformers', 'diffusers']})
    (args.output / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'{len(rows)} training rows; {metadata["trainable_parameters"]:,} trainable adapter parameters; {total_steps} steps', flush=True)
    rng, step = random.Random(args.seed), 0
    started = time.perf_counter()
    with (args.output / 'training.jsonl').open('w') as log:
        for epoch in range(args.epochs):
            order = list(range(len(rows)))
            rng.shuffle(order)
            for start in range(0, len(order), args.accumulation):
                selected = order[start:start + args.accumulation]
                optimizer.zero_grad(set_to_none=True)
                warmup = max(1, round(total_steps * .1))
                scale = ((step + 1) / warmup if step < warmup else
                         .1 + .9 * .5 * (1 + math.cos(math.pi * (step - warmup) / (total_steps - warmup))))
                for group in optimizer.param_groups:
                    group['lr'] = args.lr * scale
                loss_sum = 0.0
                for index in selected:
                    input_ids, target_ids = encoded[index]
                    ids = torch.tensor([input_ids], device=args.device)
                    targets = torch.tensor(target_ids, device=args.device)
                    mask = omni_attn_mask_naive(B=1, LEN=ids.shape[1], modalities=torch.empty((1,0,2), dtype=torch.long),
                                               device=args.device, inverted=True).to(torch.bfloat16)
                    logits = model.showo(input_ids=ids, attention_mask=mask, use_cache=False,
                                         num_logits_to_keep=len(target_ids))['logits'][0]
                    loss = F.cross_entropy(logits.float(), targets)
                    (loss / len(selected)).backward()
                    loss_sum += loss.detach().item()
                norm = torch.nn.utils.clip_grad_norm_(parameters, 1.0, error_if_nonfinite=True)
                optimizer.step()
                step += 1
                record = dict(step=step, epoch=epoch + 1, loss=loss_sum / len(selected),
                              lr=optimizer.param_groups[0]['lr'], gradient_norm=float(norm),
                              sample_ids=[rows[i]['sample_id'] for i in selected],
                              elapsed_seconds=time.perf_counter() - started)
                log.write(json.dumps(record) + '\n')
                log.flush()
                if step == 1 or step % 10 == 0 or step == total_steps:
                    print(f'step {step}/{total_steps}: loss={record["loss"]:.4f}; {record["elapsed_seconds"]:.1f}s', flush=True)
    state = {name: p.detach().cpu() for name, p in model.named_parameters() if p.requires_grad}
    torch.save(dict(config=adapter_config, state_dict=state), args.adapter)
    metadata.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                    elapsed_seconds=time.perf_counter() - started,
                    final_loss=record['loss'], completed_steps=step)
    (args.output / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Saved adapter: {args.adapter}', flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, default=ROOT / 'data/h1/state_training_v1')
    p.add_argument('--source', type=Path, default=ROOT / 'checkpoints/Show-o-source')
    p.add_argument('--model', type=Path, default=ROOT / 'checkpoints/Show-o2-1.5B-video')
    p.add_argument('--assets', type=Path, default=ROOT / 'checkpoints/Show-o-assets')
    p.add_argument('--device', choices=['cpu','mps','cuda'], default='mps')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--rank', type=int, default=8)
    p.add_argument('--last-layers', type=int, default=8)
    p.add_argument('--epochs', type=int, default=2)
    p.add_argument('--accumulation', type=int, default=4)
    p.add_argument('--lr', type=float, default=2e-4)
    p.add_argument('--seed', type=int, default=731)
    run(p.parse_args())
