"""Prepare a small, fixed pre-training evaluation; this module never loads models."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from PIL import Image, ImageDraw

from .data import digest, read_jsonl, write_json, write_jsonl
from .evaluate import evaluate
from .gold import qualify


CHARACTERS = ('士', '木', '口', '永')
STROKES = (2, 3, 2, 5)
RELATIONS = (('above', 'longer'), ('below', 'intersect'), ('left', 'right'), ('left', 'longer'))
DECODING = {'do_sample': False, 'num_beams': 1, 'max_new_tokens': 128}


def generated_continuations(family, generated_ids, input_lengths):
    """Only Qwen's native call returns the input prefix alongside new tokens."""
    if family == 'qwen3_vl':
        return [ids[length:] for ids, length in zip(generated_ids, input_lengths)]
    return generated_ids


def native_arguments(family, model_inputs, dataset):
    """Map only public model inputs to the audited native interface arguments.

    This constructs PIL images and arguments, without importing ML frameworks,
    running a processor or loading any model/tokenizer.
    """
    prompt = model_inputs['prompt']
    if 'description' in model_inputs:
        prompt += '\n描述：' + model_inputs['description']
    image = None
    if 'image' in model_inputs:
        with Image.open(dataset / model_inputs['image']) as source:
            image = source.convert('RGB')
    if family == 'internvlu':
        return {'prompt': prompt, 'image': image, 'generation_mode': 'text', **DECODING}
    if family == 'ovis_u1':
        return {'text_or_conversations': ('<image>\n' if image is not None else '') + prompt,
                'images': [image] if image is not None else [], 'generation_preface': '',
                'return_labels': False, 'propagate_exception': True,
                'multimodal_type': 'single_image', 'fix_sample_overall_length_navit': False,
                'enable_thinking': False}
    if family == 'qwen3_vl':
        content = ([{'type': 'image', 'image': image}] if image is not None else [])
        content.append({'type': 'text', 'text': prompt})
        return {'conversation': [{'role': 'user', 'content': content}], 'tokenize': True,
                'add_generation_prompt': True, 'return_dict': True, 'return_tensors': 'pt'}
    raise ValueError(f'Unsupported model family: {family}')


def score_controls(requests, predictions, labels):
    """Positive controls are reported separately, including every frozen slot."""
    answers = {p['id']: p['output'] for p in predictions}
    details = []
    for req in requests:
        raw = answers.get(req['id'])
        if raw is None or raw == '':
            status = 'no_output'
        else:
            try:
                obj = json.loads(raw) if isinstance(raw, str) else raw
            except json.JSONDecodeError:
                obj = None
            if not isinstance(obj, dict) or obj.get('label') not in ('red', 'blue', 'left', 'right'):
                status = 'unknown' if isinstance(obj, dict) and obj.get('answer') == 'unknown' else 'format_error'
            else:
                status = 'correct' if obj['label'] == labels[req['id']]['label'] else 'incorrect'
        details.append({'id': req['id'], 'pair_id': req['pair_id'], 'status': status})
    counts = Counter(d['status'] for d in details)
    return {'requests': len(requests), 'statuses': dict(counts),
            'all_passed': bool(requests) and counts['correct'] == len(requests), 'details': details}


def score(dataset, suite, predictions):
    requests = read_jsonl(suite / 'requests.jsonl')
    labels = {r['id']: r for r in read_jsonl(suite / 'evaluation_only/labels.jsonl')}
    ids = [p['id'] for p in predictions]
    if len(set(ids)) != len(ids) or set(ids) - {r['id'] for r in requests}:
        raise ValueError('Predictions must have unique IDs within the frozen S2 queue')
    controls = [r for r in requests if r['metric'] == 'VPC']
    regular = [r for r in requests if r['metric'] != 'VPC']
    result = evaluate(regular, [p for p in predictions if p['id'] not in {r['id'] for r in controls}],
                      labels, {g['id']: g for g in read_jsonl(dataset / 'evaluation_only/geometry.jsonl')},
                      read_jsonl(dataset / 'evaluation_only/reviews.jsonl'), dataset)
    result['visual_positive_controls'] = score_controls(controls, predictions, labels)
    result['requests_including_controls'] = len(requests)
    result['interpretation'] = 'development preflight only; no final generalization claim'
    return result


def prepare(dataset, output, models):
    output.mkdir(parents=True, exist_ok=False)
    rows = {r['character']: r for r in read_jsonl(dataset / 'manifest.jsonl')}
    geometry = {g['id']: g for g in read_jsonl(dataset / 'evaluation_only/geometry.jsonl')}
    reviews = read_jsonl(dataset / 'evaluation_only/reviews.jsonl')
    full = dataset / 'complete_suite_v1'
    source = read_jsonl(full / 'requests.jsonl')
    labels_by_id = {r['id']: r for r in read_jsonl(full / 'evaluation_only/labels.jsonl')}
    requests, labels = [], []
    prefix = output.relative_to(dataset).as_posix()
    # Two paired prompts: changing only the image must change the answer.
    for kind, value in (('color', 'red'), ('color', 'blue'), ('position', 'left'), ('position', 'right')):
        key = digest(f's2-v1-vpc:{kind}:{value}'.encode())[:20]
        image = Image.new('RGB', (256, 256), 'white')
        draw = ImageDraw.Draw(image)
        if kind == 'color':
            draw.rectangle((64, 64, 192, 192), fill=value)
            prompt = '图片中央实心方块是什么颜色？只回答{"label":"red"}或{"label":"blue"}。'
        else:
            x = 48 if value == 'left' else 208
            draw.ellipse((x - 24, 104, x + 24, 152), fill='black')
            prompt = '图中的黑色圆点在画布左半边还是右半边？只回答{"label":"left"}或{"label":"right"}。'
        path = output / 'media' / f'{key}.png'
        path.parent.mkdir(exist_ok=True)
        image.save(path)
        requests.append({'id': key, 'sample_id': key, 'metric': 'VPC', 'permission': 'health_only',
                         'condition': 'paired_visual_positive_control', 'pair_id': kind,
                         'split': 'synthetic_health_control', 'stratum': 'not_hanzi',
                         'model_inputs': {'image': f'{prefix}/media/{key}.png', 'prompt': prompt}})
        labels.append({'id': key, 'label': value})

    chosen = []
    for char, stroke, relations in zip(CHARACTERS, STROKES, RELATIONS):
        sid = rows[char]['id']
        for metric in ('E8', 'E2', 'E3', 'E5'):
            req = next(r for r in source if r['sample_id'] == sid and r['metric'] == metric
                       and r['permission'] == ('health_only' if metric == 'E8' else 'main')
                       and (metric not in ('E3', 'E5') or
                            int(re.search(r'第(\d+)笔', r['model_inputs']['prompt']).group(1)) == stroke))
            chosen.append(req)
        for relation in relations:
            chosen.append(next(r for r in source if r['sample_id'] == sid and r['metric'] == 'E4'
                               and r['permission'] == 'main' and labels_by_id[r['id']]['relation'] == relation
                               and labels_by_id[r['id']]['answer'] is not None))
        condition = 'positive' if char in ('士', '口') else 'same_char_wrong_order'
        chosen.append(next(r for r in source if r['sample_id'] == sid and r['metric'] == 'E6'
                           and r['condition'] == condition and r['permission'] == 'main'))
        chosen.append(next(r for r in source if r['sample_id'] == sid and r['metric'] == 'E2'
                           and r['permission'] == 'text_only'))
    chosen.sort(key=lambda r: {'health_only': 0, 'main': 1, 'text_only': 2}[r['permission']])
    for req in chosen:
        if req['metric'] in ('E3', 'E4', 'E5') and not qualify(geometry[req['sample_id']], reviews, req['metric']):
            raise ValueError(f'S2 request has insufficient independent gold: {req["id"]}')
        requests.append(req)
        labels.append(labels_by_id[req['id']])
    write_jsonl(output / 'requests.jsonl', requests)
    write_jsonl(output / 'evaluation_only/labels.jsonl', labels)

    for model in models['models']:
        application = {
            'status': 'proposed_not_authorized', 'model': model['id'], 'revision': model['revision'],
            'source_revision': model['source_revision'], 'family': model['family'],
            'request_ids': [r['id'] for r in requests], 'maximum_generation_calls': len(requests),
            'maximum_model_load_attempts': 1,
            'maximum_image_conditioned_calls': sum('image' in r['model_inputs'] for r in requests),
            'maximum_text_only_calls': sum('image' not in r['model_inputs'] for r in requests),
            'queue': '../requests.jsonl', 'seed': 20261103, 'decoding': DECODING,
            'batch_size': 1, 'quantization': None, 'dtype': 'bfloat16',
            'native_image_processor': 'checkpoint defaults; one RGB image per image request',
            'resource_caps': {
                'requested_gpu': 'one NVIDIA A100 80GB; no reservation or availability assumed',
                'gpu_count': 1, 'process_gpu_memory_GiB': 72, 'host_memory_GiB': 48,
                'cpu_cores': 8, 'local_disk_GiB': 64,
                'wall_seconds': 3600, 'load_timeout_seconds': 600, 'request_timeout_seconds': 120,
                'input_tokens_per_request': 4096, 'processed_pixels_per_image': 262144,
                'generated_tokens': len(requests) * DECODING['max_new_tokens']},
            'measurements_required': [
                'GPU UUID/model/total/free memory and unrelated process occupancy before load',
                'whole-process GPU memory sampled every second, torch allocated/reserved peaks',
                'host RSS, monotonic load/request/total time, input and generated token counts',
                'source RGB size, native tensor shapes/dtypes, image grids and visual token span'],
            'enforcement_required_before_execution': [
                'external wall/load/request watchdog; process-only termination',
                'GPU process-memory and host-RSS monitor; stop at resource cap',
                'no tokenizer truncation; stop on token/pixel limits',
                'refuse occupied/shared GPU rather than evict unrelated processes'],
            'checkpoint_weight_bytes_from_official_metadata': model['weight_bytes'],
            'actual_peak_memory_GiB': None, 'actual_seconds': None, 'actual_cost': None,
            'actual_generation_calls': 0, 'extra_retries': 0,
            'stop_conditions': [
                'load failure, critical missing/unexpected model keys, non-finite tensors, OOM or timeout',
                'any of the first four visual positive controls fails; interface or model failure remains unresolved',
                'any resource cap exceeded, missing/placeholder-only image on an image request or preprocessing exception',
                'all frozen request slots processed; no new prompt, seed, model or retry'],
            'failure_accounting': 'preserve every slot as success, failure or not_run_after_stop; never shrink denominator',
            'raw_artifacts': [
                'environment versions, pinned source/model configs and per-component loading report',
                'original request/model_inputs, source RGB, exact formatted prompt and input token IDs',
                'native pixel tensors and grid tensors, complete generated token IDs and unedited decoded output',
                'stdout/stderr, exception/traceback, token truncation flags, resource/time samples',
                'one record per frozen slot, strict parsed result and eligibility-aware evaluation'],
            'permissions': {'GPU': False, 'download_weights': False, 'training': False,
                            'requires_later_explicit_authorization': True},
            'runtime_status': 'source_audited_only; native imports, loading and cap enforcement not exercised',
        }
        write_json(output / 'gpu_applications' / f'{model["key"]}.json', application)
    record = {
        'version': 's2-preflight-v1', 'date': '2026-11-03', 'status': 'prepared_not_executed',
        'characters': list(CHARACTERS), 'requests_per_model': len(requests),
        'four_model_maximum_calls': 4 * len(requests), 'actual_calls': 0,
        'by_metric': dict(Counter(r['metric'] for r in requests)),
        'by_permission': dict(Counter(r['permission'] for r in requests)),
        'E1': 'derived from E2 sequence length, unchanged frozen definition',
        'visual_positive_control_gate': 'first four requests; same prompt within each image pair; require 4/4',
        'models': '../../../../configs/research/paired_strokes_v1/s2_models.json',
        'formal_holdout_characters': 0, 'all_hanzi_split': 'audit_development; existing splits unchanged',
        'scope': 'development pre-training preflight; no final generalization or model-capability claim',
        'maximum_total_GPU_hours_if_all_four_later_authorized': 4,
        'GPU_MPS_calls': 0, 'weights_downloaded': False, 'training': 0,
    }
    write_json(output / 'preparation.json', record)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=Path('data/research/paired_strokes_v1'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--predictions', type=Path)
    parser.add_argument('--models', type=Path, default=Path('configs/research/paired_strokes_v1/s2_models.json'))
    args = parser.parse_args()
    if args.predictions:
        result = score(args.dataset, args.dataset / 's2_preflight_v1', read_jsonl(args.predictions))
        write_json(args.output, result)
    else:
        result = prepare(args.dataset, args.output or args.dataset / 's2_preflight_v1',
                         json.loads(args.models.read_text()))
    print(json.dumps(result.get('metrics', result), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
