"""Real S0–S1 data integration. All commands are CPU-only and never fit models."""
from collections import defaultdict
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image

from scripts.paired_strokes.data import write_json, write_jsonl
from .batches import collate
from .paired import read_pairs, audit_disjoint, EOS


EXPORTS = {'train_development': 'training_pairs.jsonl',
           'validation_development': 'pilot_validation_pairs_reviewed.jsonl',
           'test_development': 'pilot_test_pairs_reviewed.jsonl',
           'audit_development': 'smoke_pairs_reviewed.jsonl'}


def audit_dataset(dataset):
    partitions = {name: read_pairs(dataset / file, dataset) for name, file in EXPORTS.items()}
    splits = json.loads((dataset / 'splits.json').read_text())['groups']
    for name, pairs in partitions.items():
        if {p.sample_id for p in pairs} != set(splits[name]):
            raise ValueError(f'Export and frozen split differ: {name}')
    result = audit_disjoint(partitions)
    expected = dict(zip(EXPORTS, (192, 24, 24, 16)))
    if result['partitions'] != expected:
        raise ValueError('Expected existing 192/24/24 development splits and 16 audit characters')
    groups = defaultdict(list)
    for pair in partitions['train_development']:
        groups[pair.strokes].append(pair.sample_id)
    result.update(training_pairs=192, training_strokes=sum(len(p.strokes) for p in partitions['train_development']),
        same_sequence_different_character_groups=[{'sequence': list(seq), 'ids': ids}
            for seq, ids in groups.items() if len(ids) > 1],
        model_inputs=['RGB image'], supervision=['original full description including terminal character'],
        evaluation_only_loaded=False, formal_holdout_characters=0)
    return partitions, result


def audit_svg_reconstruction(pairs, dataset):
    """Offline renderer audit; never used by collate or a model's feature input."""
    from scripts.paired_strokes.gold import render_masks
    sources = {r['character']: r for r in map(json.loads, (dataset / 'source_subset.jsonl').read_text().splitlines())}
    details = []
    for pair in pairs:
        with Image.open(pair.image_path) as image:
            rgb = np.asarray(image.convert('RGB'))
        masks = render_masks(sources[pair.character], size=rgb.shape[0])
        rebuilt = np.where(masks.any(axis=0)[..., None], 0, 255).astype('uint8').repeat(3, axis=2)
        different = int(np.any(rgb != rebuilt, axis=2).sum())
        details.append({'id': pair.sample_id, 'different_pixels': different})
    return {'samples': len(details), 'exact_matches': sum(d['different_pixels'] == 0 for d in details),
            'renderer': 'scripts.paired_strokes.gold.render_masks → scripts.p0.geometry.flatten_path/transform',
            'purpose': 'source/render fidelity only; no independent stroke identity qualification', 'details': details}


def audit_features(pairs, batch_size=8):
    """Every RGB goes through each random interface; backward once/mode, step=0."""
    import torch
    from .fusion import TinyPairedStrokeModel, MODES, stroke_sequence_loss, global_contrastive_loss
    torch.set_num_threads(1)
    torch.default_generator.manual_seed(20261104)
    modes = {}
    for mode in MODES:
        model = TinyPairedStrokeModel(mode=mode, width=32).cpu().eval()
        encoded, shapes, gradients = [], set(), {}
        before = time.perf_counter()
        for start in range(0, len(pairs), batch_size):
            batch = collate(pairs[start:start + batch_size])
            images = torch.from_numpy(batch.images)
            targets = torch.from_numpy(batch.targets)
            characters = torch.from_numpy(batch.character_unicode) if mode != 'sft' else None
            if start == 0:
                output = model(images, targets, characters)
                loss = stroke_sequence_loss(output, targets)
                if mode != 'sft':
                    loss = loss + global_contrastive_loss(output)
                if not bool(torch.isfinite(loss)):
                    raise ValueError(f'Non-finite CPU contract loss: {mode}')
                loss.backward()
                for name, parameter in model.named_parameters():
                    if parameter.requires_grad:
                        gradients[name] = parameter.grad is not None and bool(torch.isfinite(parameter.grad).all()) and bool(parameter.grad.abs().sum() > 0)
                if not all(gradients.values()):
                    raise ValueError(f'Missing/non-finite/zero gradient in {mode}: {gradients}')
            else:
                with torch.no_grad():
                    output = model(images, targets, characters)
            if not bool(torch.isfinite(output.logits).all()):
                raise ValueError(f'Non-finite image features/logits: {mode}')
            encoded.extend(batch.ids)
            shapes.add(tuple(batch.images.shape[1:]))
        modes[mode] = {'samples_encoded': len(encoded), 'ids': encoded, 'RGB_shapes': sorted(shapes),
            'patch_grid': [16, 16], 'patch_count': 256, 'width': 32,
            'trainable_parameters': sum(p.numel() for p in model.parameters() if p.requires_grad),
            'gradient_paths': gradients, 'backward_batches': 1, 'optimizer_steps': 0,
            'seconds': time.perf_counter() - before}
    return {'modes': modes, 'torch_version': torch.__version__, 'device': 'cpu',
            'pretrained_weights_loaded': False, 'native_model_processors_executed': False,
            'actual_training_steps': 0, 'GPU_MPS_calls': 0,
            'interpretation': 'real RGB through random CPU interface modules; no model capability results'}


def integrate(dataset, output, *, features=False):
    output.mkdir(parents=True, exist_ok=False)
    partitions, audit = audit_dataset(dataset)
    write_json(output / 'pairs.json', audit)
    train = partitions['train_development']
    svg = audit_svg_reconstruction(train, dataset)
    write_json(output / 'svg_reconstruction.json', svg)
    if svg['exact_matches'] != len(train):
        raise ValueError('Source SVG reconstruction differs from original training RGB; inspect retained report')
    inputs = []
    for start in range(0, len(train), 8):
        batch = collate(train[start:start + 8])
        for index, sid in enumerate(batch.ids):
            inputs.append({'id': sid, 'RGB_shape': list(batch.images[index].shape),
                'RGB_range': [float(batch.images[index].min()), float(batch.images[index].max())],
                'valid_target_tokens_including_EOS': int(batch.target_mask[index].sum()),
                'last_valid_target': int(batch.targets[index][batch.target_mask[index]][-1]),
                'contract_EOS': EOS, 'description_preserved': batch.descriptions[index] == train[start + index].description})
    write_jsonl(output / 'feature_inputs.jsonl', inputs)
    if features:
        write_json(output / 'features.json', audit_features(train))
    return {'training_pairs': len(train), 'SVG_exact_matches': svg['exact_matches'],
            'RGB_inputs_checked': len(inputs), 'fusion_features_executed': features,
            'GPU_MPS_calls': 0, 'training_steps': 0}
