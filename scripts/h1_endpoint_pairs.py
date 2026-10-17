"""Frozen UMM readout on endpoint pairs with identical surrounding strokes."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse
import json
import math
import time

import numpy as np
from PIL import Image, ImageDraw

import h1_progress_coverage as prior
from h1_region_state import ROOT, CLASSES, KINDS, render, make_state_head
from h1_run_showo import load_model, StateImageEncoder
from h1_spatial_probe import CACHE as SPATIAL_CACHE
from h1_state_gate import interval, write_jsonl, read_jsonl

DATA = ROOT / 'data/h1/endpoint_pairs_v1'
RESULT = ROOT / 'results/h1/showo2_video_1_5b/endpoint_pairs_v1'
CACHE = ROOT / 'checkpoints/h1_endpoint_pairs_v1'
GAPS = [0, 1, 2, 4, 8, 16]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def build():
    DATA.mkdir(parents=True, exist_ok=False)
    (DATA / 'images').mkdir()
    RESULT.mkdir(parents=True, exist_ok=False)
    CACHE.mkdir(parents=True, exist_ok=False)
    old_images = json.loads((prior.DATA / 'images.json').read_text())
    queries = [q for q in json.loads((prior.DATA / 'queries.json').read_text())
               if q['split'] == 'fresh' and q['kind'] in KINDS]
    images, references, cases = [], {}, []
    for q in queries:
        old = q['reference_index']
        if old not in references:
            references[old] = len(images)
            images.append(dict(**old_images[old], reused_index=old))
    for q in queries:
        target = q['target']
        a, b = q['strokes'][target]
        length = math.dist(a, b)
        background = {k: .5 for k in q['strokes']}
        complete = np.asarray(render(q['strokes'], dict(background, **{target: 1}), q['width']))
        for gap in GAPS:
            fractions = dict(background, **{target: 1 - gap / length})
            current = render(q['strokes'], fractions, q['width'])
            changed = np.any(np.asarray(current) != complete, axis=-1)
            # Exact raster evidence is part of annotation, never a model input.
            if int(changed.sum()) != gap * q['width']:
                raise ValueError('A target gap is hidden or its raster length differs from the label.')
            name = f"q{q['query_id']:03}-gap{gap:02}"
            path = DATA / 'images' / f'{name}.png'
            current.save(path)
            index = len(images)
            images.append(dict(image=str(path.relative_to(ROOT)), split='development'))
            cases.append(dict(sample_id=name, group_id=q['group_id'], query_index=q['query_id'],
                kind=q['kind'], target=target, reference_index=references[q['reference_index']],
                current_index=index, gap_px=gap, fraction=fractions[target], line_width=q['width'],
                background_fraction=.5, expected='完整' if gap == 0 else '部分',
                changed_pixels=int(changed.sum())))
    save(DATA / 'images.json', images)
    save(DATA / 'queries.json', queries)
    save(DATA / 'cases.json', cases)
    save(RESULT / 'plan.json', dict(created_utc=datetime.now(timezone.utc).isoformat(),
        question='Can frozen state heads distinguish complete target strokes from exact endpoint gaps when other strokes remain identical?',
        input='432x432 images; full reference and current separately encoded. All non-target current strokes fixed at 50%; only queried endpoint changes. No crop or colored cue.',
        model='Full frozen Show-o2-1.5B-w-video-und native fused visual features; existing original language adapter and question-conditioned reference localizer unchanged.',
        data=dict(cases=len(cases), targets=len(queries), groups=len(references), gaps_px=GAPS,
            reused_reference_images=len(references), new_current_images=len(cases),
            geometry='Reuse previous progress-fresh development geometry: 8 groups per kind, 24 total. Previously used for diagnosis; no independent acceptance claim.',
            raster='Axis-aligned integer endpoints; shortened endpoint differs by exactly gap_px. Pixel delta equals gap_px * width. Background unchanged within each target family.'),
        conditions=['replay_oracle/oracle', 'coverage_oracle/oracle',
                    'replay_predicted/predicted', 'coverage_predicted/predicted',
                    'replay_predicted/oracle', 'coverage_predicted/oracle'],
        metrics='Per-gap state accuracy; complete/partial pair both correct; complete-minus-partial logit ranking with ties separate; all six states correct per target; group bootstrap. Feature differences only test input sensitivity, not successful understanding.',
        policy='No training, threshold adjustment, checkpoint selection or default model replacement. Conditions and gaps fixed before new encoding and scoring.',
        scope='All targets are present and references available. This diagnoses completion boundaries only; no absence, unknown, Chinese, order, free language generation or UMM synergy claim. Original 130-case visual test unused.'))
    draw_examples(cases, images)
    print(json.dumps(dict(cases=len(cases), targets=len(queries), new_images=len(cases))))


def draw_examples(cases, images):
    canvas = Image.new('RGB', (7 * 216, 3 * 150), '#eeeeee')
    draw = ImageDraw.Draw(canvas)
    for row, kind in enumerate(KINDS):
        first = next(r for r in cases if r['kind'] == kind)
        family = [r for r in cases if r['query_index'] == first['query_index']]
        indices = [first['reference_index']] + [r['current_index'] for r in family]
        labels = [f"reference q{first['query_index']}"] + [f"gap {r['gap_px']} px" for r in family]
        for col, (index, label) in enumerate(zip(indices, labels)):
            # Preview only; model receives the full-resolution uncropped image.
            picture = Image.open(ROOT / images[index]['image']).crop((0, 0, 432, 216)).resize((216, 108))
            canvas.paste(picture, (col * 216, row * 150 + 30))
            draw.text((col * 216 + 5, row * 150 + 8), label, fill='black')
    canvas.save(RESULT / 'examples.png')


def extract():
    import torch
    start = time.perf_counter()
    images = json.loads((DATA / 'images.json').read_text())
    old = torch.load(prior.CACHE / 'features.pt', map_location='cpu', weights_only=True)['features']
    features = [old[r['reused_index']].clone() for r in images if 'reused_index' in r]
    reused = len(features)
    del old
    assets = ROOT / 'checkpoints/Show-o-assets'
    model, _, _ = load_model(ROOT / 'checkpoints/Show-o-source', ROOT / 'checkpoints/Show-o2-1.5B-video', assets, 'cpu')
    encoder = StateImageEncoder(model, assets, 'mps')
    with (CACHE / 'progress.jsonl').open('w') as log:
        for i, row in enumerate(images[reused:]):
            features.append(encoder.encode(ROOT / row['image']).squeeze(0).cpu())
            encoder.cache.clear()
            if (i + 1) % 12 == 0:
                log.write(json.dumps(dict(completed=i + 1, seconds=time.perf_counter() - start)) + '\n')
                log.flush()
    features = torch.stack(features)
    torch.save(dict(features=features), CACHE / 'features.pt')
    save(RESULT / 'extraction.json', dict(seconds=time.perf_counter() - start, new_images=len(images) - reused,
        reused_images=reused, shape=list(features.shape), full_model_parameters=sum(p.numel() for p in model.parameters()),
        umm_updated_parameters=0, native_path='Wan VAE CPU fp32, semantic/generative fusion MPS bf16; seed 0 per image, as in prior experiments.'))


def metrics(rows):
    def count(selected, field='correct'):
        groups = defaultdict(list)
        for r in selected:
            groups[r['group_id']].append(int(r[field]))
        return dict(n=len(selected), correct=sum(r[field] for r in selected), ci95=interval(groups))
    families = defaultdict(list)
    for r in rows:
        families[r['query_index']].append(r)
    pairs, all_six = [], []
    for family in families.values():
        full = next(r for r in family if r['gap_px'] == 0)
        all_six.append(dict(group_id=full['group_id'], correct=all(r['correct'] for r in family)))
        for r in family:
            if r['gap_px'] == 0:
                continue
            delta = full['complete_minus_partial'] - r['complete_minus_partial']
            pairs.append(dict(query_index=r['query_index'], group_id=r['group_id'], gap_px=r['gap_px'],
                correct=full['correct'] and r['correct'], ranked=delta > 0, tied=delta == 0, logit_delta=delta))
    by_gap = {}
    for gap in GAPS:
        selected = [r for r in rows if r['gap_px'] == gap]
        entry = dict(**count(selected), answers=dict(Counter(r['answer'] for r in selected)))
        if gap:
            subset = [r for r in pairs if r['gap_px'] == gap]
            entry['both_correct'] = count(subset)
            entry['ranked_correctly'] = count(subset, 'ranked')
            entry['ranking_ties'] = sum(r['tied'] for r in subset)
            entry['median_logit_delta'] = float(np.median([r['logit_delta'] for r in subset]))
        by_gap[str(gap)] = entry
    return dict(all=count(rows), by_gap=by_gap, pairs=count(pairs), all_six=count(all_six)), pairs


def evaluate():
    import torch
    start = time.perf_counter()
    rows = json.loads((DATA / 'cases.json').read_text())
    features = torch.load(CACHE / 'features.pt', map_location='cpu', weights_only=True)['features'].to('mps')
    masks = torch.load(prior.CACHE / 'masks.pt', map_location='cpu', weights_only=True)
    stats = torch.load(SPATIAL_CACHE / 'readout.pt', map_location='cpu', weights_only=True)
    mean, std = stats['mean'].to('mps'), stats['std'].to('mps')
    plan = json.loads((RESULT / 'plan.json').read_text())
    summary, predictions, pair_records = {}, [], []
    with torch.inference_mode():
        for condition in plan['conditions']:
            name, region = condition.split('/')
            head = make_state_head().to('mps').eval()
            head.load_state_dict(torch.load(prior.CACHE / f'{name}.pt', map_location='mps', weights_only=True)['state_dict'])
            scored = []
            for offset in range(0, len(rows), 32):
                batch = rows[offset:offset + 32]
                ref = (features[[r['reference_index'] for r in batch]].float() - mean) / std
                cur = (features[[r['current_index'] for r in batch]].float() - mean) / std
                mask = torch.stack([masks[region][r['query_index']] for r in batch]).to('mps')
                logits = head(ref, cur, mask, torch.ones(len(batch), device='mps')).cpu()
                probabilities = torch.softmax(logits, -1).tolist()
                for r, p, logit in zip(batch, probabilities, logits.tolist()):
                    answer = CLASSES[int(np.argmax(p))]
                    scored.append(dict(**r, condition=condition, answer=answer, correct=answer == r['expected'],
                        logits=logit, probabilities=p, complete_minus_partial=logit[2] - logit[1]))
            summary[condition], pairs = metrics(scored)
            predictions.extend(scored)
            pair_records.extend(dict(**r, condition=condition) for r in pairs)
    write_jsonl(RESULT / 'predictions.jsonl', predictions)
    write_jsonl(RESULT / 'pairs.jsonl', pair_records)
    save(RESULT / 'score.json', summary)
    # Separate sensitivity of the frozen representation from head decisions.
    families = defaultdict(list)
    for r in rows:
        families[r['query_index']].append(r)
    sensitivity = []
    for family in families.values():
        full = next(r for r in family if r['gap_px'] == 0)
        for r in family:
            if not r['gap_px']:
                continue
            diff = (features[full['current_index']].float() - features[r['current_index']].float()) / std
            for region in ('oracle', 'predicted'):
                mask = masks[region][r['query_index']].to('mps')
                selected = diff[mask]
                sensitivity.append(dict(query_index=r['query_index'], group_id=r['group_id'], gap_px=r['gap_px'],
                    region=region, cells=int(mask.sum()), normalized_rms=float(selected.square().mean().sqrt()) if selected.numel() else None,
                    changed_fraction=float((selected != 0).float().mean()) if selected.numel() else None))
    write_jsonl(RESULT / 'feature_sensitivity.jsonl', sensitivity)
    save(RESULT / 'evaluation.json', dict(seconds=time.perf_counter() - start, parameters_updated=0,
        bootstrap='2000 whole-geometry resamples; repeated full members stay in their group. Single fixed model; no training-seed uncertainty.'))
    print(json.dumps({k:dict(all=v['all'], pairs=v['pairs'], all_six=v['all_six']) for k, v in summary.items()}, indent=2))


def diagnose():
    """Post-hoc background comparison; uses existing predictions, no new fit."""
    current = read_jsonl(RESULT / 'predictions.jsonl')
    old = [r for r in read_jsonl(prior.RESULT / 'predictions.jsonl')
           if r['evaluation_set'] == 'dev_fresh' and r['kind'] in KINDS]
    by_key = {(r['condition'], r['query_index']): r for r in old if r['fraction'] == 1}
    paired, summary = [], {}
    for condition in sorted({r['condition'] for r in current}):
        groups = defaultdict(list)
        records = []
        for r in current:
            if r['condition'] != condition or r['gap_px'] != 0:
                continue
            before = by_key[(condition, r['query_index'])]
            record = dict(query_index=r['query_index'], group_id=r['group_id'], condition=condition,
                before_sample=before['sample_id'], after_sample=r['sample_id'],
                before_answer=before['answer'], after_answer=r['answer'],
                before_correct=before['correct'], after_correct=r['correct'],
                before_background={b['target']: b['fraction'] for b in old
                    if b['condition'] == condition and b['scene_id'] == before['scene_id'] and b['target'] != r['target']},
                after_background_fraction=.5)
            records.append(record)
            groups[r['group_id']].append(int(r['correct']) - int(before['correct']))
        paired.extend(records)
        summary[condition] = dict(n=len(records), before_correct=sum(r['before_correct'] for r in records),
            after_correct=sum(r['after_correct'] for r in records),
            changed_answers=sum(r['before_answer'] != r['after_answer'] for r in records),
            repairs=sum(r['after_correct'] and not r['before_correct'] for r in records),
            regressions=sum(r['before_correct'] and not r['after_correct'] for r in records),
            difference=sum(map(sum, groups.values())) / len(records), paired_ci95=interval(groups))
    by_condition = {(r['condition'], r['sample_id']): r for r in current}
    region_comparison = {}
    for gap in GAPS:
        rows = [r for r in current if r['condition'] == 'coverage_predicted/predicted' and r['gap_px'] == gap]
        groups = defaultdict(list)
        for r in rows:
            oracle = by_condition[('coverage_predicted/oracle', r['sample_id'])]
            groups[r['group_id']].append(int(oracle['correct']) - int(r['correct']))
        region_comparison[str(gap)] = dict(n=len(rows), difference=sum(map(sum, groups.values())) / len(rows),
            paired_ci95=interval(groups))
    write_jsonl(RESULT / 'background_pairs.jsonl', paired)
    balance = {}
    for condition in sorted({r['condition'] for r in current}):
        rows = [r for r in current if r['condition'] == condition]
        rates = [sum(r['correct'] for r in rows if r['expected'] == label) /
                 sum(r['expected'] == label for r in rows) for label in ('完整', '部分')]
        balance[condition] = sum(rates) / 2
    save(RESULT / 'diagnosis.json', dict(scope='Post-hoc descriptive controls using already saved predictions. No fitting or model replacement.',
        class_imbalance=dict(full=56, partial=280, always_partial_correct=280,
            always_partial_pair_success=0, balanced_accuracy=balance),
        background='Same full target and complete reference; previous other-stroke fractions replaced by 50%. Geometry and queried region unchanged. Only multi-target cases, excluding 6 reference controls.',
        background_comparison=summary, same_head_oracle_minus_predicted=region_comparison))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'extract', 'evaluate', 'diagnose'])
    parser.add_argument('--data', type=lambda p: ROOT / p, default=DATA)
    parser.add_argument('--output', type=lambda p: ROOT / p, default=RESULT)
    parser.add_argument('--cache', type=lambda p: ROOT / p, default=CACHE)
    args = parser.parse_args()
    DATA, RESULT, CACHE = args.data, args.output, args.cache
    globals()[args.command]()
