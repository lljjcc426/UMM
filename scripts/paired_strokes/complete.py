"""Finish the CPU benchmark suite and strata; never invoke a model."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

import numpy as np

from .data import digest, read_jsonl, write_json, write_jsonl
from .gold import save_png


def prepare(dataset, output):
    output.mkdir(parents=True, exist_ok=False)
    rows = read_jsonl(dataset / 'manifest.jsonl')
    geometry = {g['id']: g for g in read_jsonl(dataset / 'evaluation_only/geometry.jsonl')}
    base = read_jsonl(dataset / 'requests.jsonl')
    base_labels = read_jsonl(dataset / 'evaluation_only/labels.jsonl')
    labels_by_id = {r['id']: r for r in base_labels}
    requests, labels, strata = [], [], []
    for r in base:
        pre = {'E2': 'PRE-01', 'E3': 'PRE-04', 'E4': 'PRE-03',
               'E5': 'PRE-04', 'E6': 'PRE-05', 'E6R': 'PRE-05'}[r['metric']]
        requests.append({**r, 'pre_id': pre, 'permission': 'main'})
    labels.extend(base_labels)
    image_root = output.relative_to(dataset).as_posix()

    for row in rows:
        sid, item = row['id'], geometry[row['id']]
        for metric, pre, permission, condition, prompt, target, inputs in [
            ('E2', 'PRE-02', 'text_only', 'character_only_normative_prior',
             f'给出汉字“{row["character"]}”在中国大陆规范下的有序五类笔形编码。'
             '1横类(含提)，2竖类，3撇类，4点类(含捺)，5折类。'
             '仅回答JSON，例如{"sequence":["1","2"]}；无法判断回答{"answer":"unknown"}。',
             {'sequence': row['sequence']}, {}),
            ('E8', 'PRE-07', 'health_only', 'image_only_character_OCR',
             '识别图片中的单个汉字，仅回答JSON，例如{"character":"字"}；无法判断回答{"answer":"unknown"}。',
             {'character': row['character']}, {'image': row['model_inputs']['image']})
        ]:
            key = digest(f'paired-strokes-controls-v1:{sid}:{pre}'.encode())[:20]
            requests.append({'id': key, 'sample_id': sid, 'metric': metric, 'pre_id': pre,
                             'permission': permission, 'condition': condition,
                             'split': row['split'], 'stratum': row['stroke_count_stratum'],
                             'model_inputs': {**inputs, 'prompt': prompt}})
            labels.append({'id': key, **target})

        sequence = row['sequence']
        lengths = [float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum()) for p in item['paths']]
        tags = ['repeated_type' if len(set(sequence)) < len(sequence) else 'no_repeated_type']
        tags.append('raster_contact' if any(r['relation'] == 'intersect' and r['answer']
                                           for r in item['relations']) else 'no_raster_contact')
        tags.append('short_stroke' if min(lengths) < .5 * np.median(lengths) else 'no_short_stroke')
        if any(r['id'] != sid and r['split'] == row['split'] and r['sequence'] == sequence for r in rows):
            tags.append('same_sequence_other_character')
        if row['character'] in '土士木未末人大':
            tags.append('predeclared_similar_character_group')
        strata.append({'sample_id': sid, 'stroke_count_stratum': row['stroke_count_stratum'],
                       'tags': tags, 'geometry_tags_qualification': 'source_derived_candidate',
                       'short_stroke_definition': 'median_path_length_ratio_below_0.5',
                       'similar_groups': ['土士', '木未末', '人大']})

    masks_by_sample = {}
    for request in base:
        if request['metric'] not in ('E3', 'E4', 'E5'):
            continue
        sid = request['sample_id']
        label = labels_by_id[request['id']]
        if sid not in masks_by_sample:
            with np.load(dataset / geometry[sid]['mask_archive']) as archive:
                masks_by_sample[sid] = archive['masks']
        masks = masks_by_sample[sid]
        if request['metric'] == 'E4':
            # The frozen prompt identifies the two normative stroke numbers.
            a, b = map(int, re.search(r'第(\d+)笔相对第(\d+)笔', request['model_inputs']['prompt']).groups())
            strokes = (a, b)
            explanation = f'蓝色标记规范第{a}笔，橙色标记规范第{b}笔，紫色为交叠。'
        else:
            stroke = int(re.search(r'第(\d+)笔', request['model_inputs']['prompt']).group(1))
            strokes = (stroke,)
            explanation = f'蓝色已标记规范第{stroke}笔。未显示起终点。'
        filename = f'{sid}-' + '-'.join(map(str, strokes)) + '.png'
        image = output / 'evaluation_only/oracle_media' / filename
        if not image.exists():
            rgb = np.full((*masks.shape[1:], 3), 255, dtype='uint8')
            rgb[masks.any(axis=0)] = [210, 210, 210]
            rgb[masks[strokes[0] - 1]] = [25, 85, 210]
            if len(strokes) == 2:
                rgb[masks[strokes[1] - 1]] = [205, 60, 25]
                rgb[masks[strokes[0] - 1] & masks[strokes[1] - 1]] = [135, 30, 160]
            save_png(image, rgb)
        key = digest(f'paired-strokes-controls-v1:oracle:{request["id"]}'.encode())[:20]
        requests.append({**request, 'id': key, 'pre_id': 'PRE-06', 'permission': 'oracle_highlight',
                         'condition': 'oracle_' + request['condition'], 'paired_main_request_id': request['id'],
                         'model_inputs': {'image': f'{image_root}/evaluation_only/oracle_media/{filename}',
                                          'prompt': explanation + request['model_inputs']['prompt']}})
        labels.append({**label, 'id': key})

    write_jsonl(output / 'requests.jsonl', requests)
    write_jsonl(output / 'evaluation_only/labels.jsonl', labels)
    write_jsonl(output / 'analysis_strata.jsonl', strata)
    record = {'suite_revision': 'paired-strokes-cpu-complete-v1',
              'original_requests_preserved': len(base), 'requests': len(requests),
              'by_pre_id': dict(Counter(r['pre_id'] for r in requests)),
              'by_permission': dict(Counter(r['permission'] for r in requests)),
              'oracle_images': len(list((output / 'evaluation_only/oracle_media').glob('*.png'))),
              'strata_characters': len(strata), 'model_calls': 0, 'model_metrics': None,
              'four_model_total_requests_if_later_authorized': len(requests) * 4,
              'resource_estimate': 'Measured throughput and GPU hours unavailable until separately authorized interface trials',
              'scope': 'offline preparation only; no authorization for S2-S6'}
    write_json(output / 'preparation.json', record)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=Path('data/research/paired_strokes_v1'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.dataset, args.output), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
