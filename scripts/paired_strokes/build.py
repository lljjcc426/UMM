"""Build an isolated, reproducible development release from existing CPU sources."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path
import random
import re
import shutil
import time

import numpy as np
from PIL import Image, ImageDraw

from scripts.p0.geometry import transform
from .data import (CLASSES, NOTICE, REVISION, description, digest, parse_norm,
                   training_view, validate_manifest, write_json, write_jsonl)
from .gold import direction, render_masks, save_png, spatial_relations

AUDIT_CHARACTERS = '一二三十土士木未末口日田人大中永'
SEED = 20261102


def stratum(count):
    return '1-3' if count <= 3 else '4-6' if count <= 6 else '7-10' if count <= 10 else '>10'


def historical_characters(root):
    """Reuse explicit old manifests, never relabel their review qualifications."""
    paths = [root / 'data/research/datasets/p0_stroke_synthetic_v1/templates.json',
             root / 'hanzi_video/assets/catalog.json']
    characters = set(AUDIT_CHARACTERS)
    for path in paths:
        obj = json.loads(path.read_text())
        if 'templates' in obj:
            characters.update(r['character'] for r in obj['templates'])
        else:
            characters.update(obj['characters'])
    # Current Batch A and restart inputs are known development exposures.
    for path in (root / 'data/research/next').glob('*.json*'):
        obj_text = path.read_text()
        characters.update(re.findall(r'"character"\s*:\s*"(.)"', obj_text))
        characters.update(re.findall(r'"target_character"\s*:\s*"(.)"', obj_text))
    return characters, [str(p.relative_to(root)) for p in paths]


def build(args):
    started = time.perf_counter()
    root, out = Path.cwd(), args.output
    out.mkdir(parents=True, exist_ok=False)
    norm, norm_rejections = parse_norm(args.norm_text.read_text())
    graphics_bytes = args.graphics.read_bytes()
    graphics = {g['character']: g for g in map(json.loads, graphics_bytes.decode().splitlines())}
    exposed, exposure_sources = historical_characters(root)
    eligible, rejected = {}, []
    for char, graphic in graphics.items():
        ref = norm.get(char)
        reason = None
        if ref is None:
            reason = 'normative_text_unavailable_or_rejected'
        elif len(graphic['strokes']) != ref['stroke_count']:
            reason = 'norm_and_svg_stroke_count_disputed'
        elif (len(graphic['strokes']) != len(graphic['medians'])
              or any(len(p) < 2 for p in graphic['medians'])):
            reason = 'incomplete_source_geometry'
        elif ref['index'] > 3500:
            reason = 'outside_first_level_scope_v1'
        if reason:
            rejected.append({'character': char, 'reason': reason})
        else:
            eligible[char] = ref
    if not set(AUDIT_CHARACTERS) <= eligible.keys():
        raise ValueError('An explicit audit character lacks source/norm agreement')

    rng = random.Random(SEED)
    bins = defaultdict(list)
    for char, ref in eligible.items():
        if char not in exposed:
            bins[stratum(ref['stroke_count'])].append(char)
    selected = [(c, 'audit_development') for c in AUDIT_CHARACTERS]
    # 240 additional characters: 192/24/24 character-disjoint development partitions.
    for name, quota in [('1-3', 10), ('4-6', 50), ('7-10', 90), ('>10', 90)]:
        pool = sorted(bins[name], key=ord)
        rng.shuffle(pool)
        if len(pool) < quota:
            raise ValueError(f'Insufficient unexposed candidates in {name}: {len(pool)} < {quota}')
        for i, char in enumerate(pool[:quota]):
            split = 'train_development' if i < quota * .8 else ('validation_development' if i < quota * .9 else 'test_development')
            selected.append((char, split))

    source_assets = args.graphics.parent
    for name in ('COPYING', 'ARPHICPL.TXT'):
        target = out / 'licenses' / name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(source_assets / name, target)
    manifest, gold, source_subset = [], [], []
    for char, split in selected:
        graphic, ref = graphics[char], eligible[char]
        sid = digest(('paired-strokes-v1:' + char).encode())[:16]
        masks = render_masks(graphic)
        image = np.where(masks.any(axis=0)[..., None], 0, 255).astype('uint8').repeat(3, axis=2)
        image_path = 'media/' + sid + '.png'
        save_png(out / image_path, image)
        file_hash = digest((out / image_path).read_bytes())
        norm_reference = {'standard': 'GF0023-2020', 'pdf_page': ref['pdf_page'], 'index': ref['index']}
        row = {'id': sid, 'character': char, 'char_id': f'U+{ord(char):04X}',
               'glyph_template_id': f'mmh-{ord(char):05X}',
               'source_record_id': f'mmh:{REVISION}:{ord(char):05X}',
               'font_family': 'Arphic_source_per_glyph_family_unspecified',
               'group_id': f'mmh:{REVISION}:{ord(char):05X}', 'norm_revision': 'GF0023-2020',
               'source_revision': REVISION, 'license': 'Arphic Public License',
               'split': split, 'file_hash': file_hash, 'sequence_version': 'GF0023-five-v1',
               'sequence': ref['sequence'], 'stroke_count_stratum': stratum(ref['stroke_count']),
               'historically_exposed': char in exposed, 'formal_gold': False,
               'qualification': 'official_sequence_source_geometry_binding_pending_independent_review',
               'model_inputs': {'image': image_path},
               'training_targets': {'description': description(char, ref['sequence'])},
               'evaluation_only': {'sample_ref': sid}, 'norm_reference': norm_reference}
        manifest.append(row)
        paths = [transform(median, 256) / 256 for median in graphic['medians']]
        mask_archive = f'evaluation_only/masks/{sid}.npz'
        (out / mask_archive).parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out / mask_archive, masks=masks, notice=NOTICE)
        gold.append({'id': sid, 'gold_revision': 'source-geometry-candidate-v1',
                     'qualification': 'source_derived_unreviewed', 'formal_gold': False,
                     'norm_reference': norm_reference, 'stroke_ids': list(range(1, len(masks) + 1)),
                     'mask_archive': mask_archive, 'mask_archive_hash': digest((out / mask_archive).read_bytes()),
                     'paths': [p.tolist() for p in paths],
                     'directions': [{'direction': direction(p), 'start': p[0].tolist(), 'end': p[-1].tolist()} for p in paths],
                     'relations': spatial_relations(masks, graphic['medians']),
                     'instance_binding': 'SVG source order is a candidate; no normative identity audit inferred'})
        source_subset.append({'character': char, 'notice': NOTICE, **graphic})

    validate_manifest(manifest)
    write_jsonl(out / 'manifest.jsonl', manifest)
    write_jsonl(out / 'training_pairs.jsonl', [training_view(r) for r in manifest if r['split'] == 'train_development'])
    write_jsonl(out / 'evaluation_only/geometry.jsonl', gold)
    write_jsonl(out / 'evaluation_only/reviews.jsonl', [])
    write_jsonl(out / 'source_subset.jsonl', source_subset)
    # Normative text extracts contain factual codes and local page references only.
    write_jsonl(out / 'evaluation_only/normative_extracts.jsonl', [eligible[c] for c, _ in selected])
    write_jsonl(out / 'source_rejections.jsonl', rejected)
    # Raw rejected official text stays private, not in the distributable release.
    write_json(args.private_output / 'norm_text_rejections.json', norm_rejections)

    requests, labels = [], []

    def request(row, metric, condition, prompt, target, extra=None):
        key = digest(f'{row["id"]}:{metric}:{condition}:{prompt}'.encode())[:20]
        inputs = {'image': row['model_inputs']['image'], 'prompt': prompt}
        if extra:
            inputs.update(extra)
        requests.append({'id': key, 'sample_id': row['id'], 'metric': metric, 'condition': condition,
                         'split': row['split'], 'stratum': row['stroke_count_stratum'], 'model_inputs': inputs})
        labels.append({'id': key, **target})

    for row, geometry in zip(manifest, gold):
        request(row, 'E2', 'image_only',
                '按中国大陆规范给出图中字的有序五类笔形编码。1横类(含提)，2竖类，3撇类，4点类(含捺)，5折类。'
                '仅回答JSON，例如{"sequence":["1","2"]}；无法判断回答{"answer":"unknown"}。', {'sequence': row['sequence']})
        request(row, 'E6', 'positive', '判断图片与描述是否相符，仅回答{"answer":true/false}。',
                {'answer': True}, {'description': row['training_targets']['description']})
        seq = row['sequence']
        swapped = next((i for i in range(len(seq) - 1) if seq[i] != seq[i + 1]), None)
        if swapped is not None:
            changed = seq.copy()
            changed[swapped], changed[swapped + 1] = changed[swapped + 1], changed[swapped]
            request(row, 'E6', 'same_char_wrong_order', '判断图片与描述是否相符，仅回答{"answer":true/false}。',
                    {'answer': False}, {'description': description(row['character'], changed)})
        changed = seq.copy()
        changed[-1] = str(int(changed[-1]) % 5 + 1)
        request(row, 'E6', 'same_char_wrong_type', '判断图片与描述是否相符，仅回答{"answer":true/false}。',
                {'answer': False}, {'description': description(row['character'], changed)})
        masked = seq.copy()
        missing = len(seq) // 2
        masked[missing] = '[MASK]'
        request(row, 'E6R', 'masked_sequence_character_hidden',
                '根据图片补全五类笔形序列中的[MASK]。1横类，2竖类，3撇类，4点类，5折类。'
                'token取1至5中的一个编码，仅回答JSON，例如{"token":"1"}。', {'token': seq[missing]},
                {'description': '、'.join(masked)})
        if row['split'] != 'audit_development':
            continue
        for stroke in geometry['stroke_ids']:
            request(row, 'E3', 'unmarked_image', f'指出规范第{stroke}笔内部的一个点，避开交叠区。'
                    '图左上为(0,0)，右下为(1,1)。仅回答{"point":[x,y]}。', {'stroke': stroke})
            request(row, 'E5', 'normative_endpoint_displacement', f'给出规范第{stroke}笔从起点到终点位移的八方向类别。'
                    '这是静态图的规范推断。类别为right、down_right、down、down_left、left、up_left、up、up_right。'
                    '仅回答JSON，例如{"direction":"right"}，'
                    '可附start/end归一化坐标。', geometry['directions'][stroke - 1])
        pairs = [(i + 1, j + 1) for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] == seq[j]][:2]
        if not pairs and len(seq) > 1:
            pairs = [(1, 2)]
        for rel in geometry['relations']:
            if (rel['a'], rel['b']) in pairs:
                prompt = (f'规范第{rel["a"]}笔相对第{rel["b"]}笔，关系{rel["relation"]}是否成立？'
                          '上下左右按轮廓质心比较(画布2%容差)，longer按中线弧长比较(5%容差)，'
                          'intersect指轮廓接触或重叠。仅回答{"answer":true/false}；不确定回答{"answer":"unknown"}。')
                request(row, 'E4', 'repeated_type' if seq[rel['a'] - 1] == seq[rel['b'] - 1] else 'other_type',
                        prompt, {'answer': rel['answer'], 'relation': rel['relation']})

    collision_rows = []
    for row in manifest:
        peer = next((p for p in manifest if p['split'] == row['split'] and p['id'] != row['id']
                     and p['sequence'] == row['sequence']), None)
        if peer:
            request(row, 'E6', 'same_sequence_other_character_OCR_control',
                    '判断图片与描述是否相符，仅回答{"answer":true/false}。', {'answer': False},
                    {'description': description(peer['character'], peer['sequence'])})
            request(row, 'E6', 'same_sequence_character_hidden_compatible_control',
                    '此描述未给末尾汉字。判断图片是否与这条五类笔形序列兼容，仅回答{"answer":true/false}。',
                    {'answer': True}, {'description': '、'.join(CLASSES[s] for s in peer['sequence'])})
            collision_rows.append({'sample_id': row['id'], 'other_sample_id': peer['id'],
                                   'split': row['split'], 'sequence': row['sequence'],
                                   'without_terminal_character': 'compatible_not_negative',
                                   'with_terminal_character': 'OCR_solvable_control_not_spatial_evidence'})
    write_jsonl(out / 'requests.jsonl', requests)
    write_jsonl(out / 'evaluation_only/labels.jsonl', labels)
    write_jsonl(out / 'evaluation_only/sequence_collisions.jsonl', collision_rows)
    review_template = [{'sample_id': g['id'], 'gold_revision': g['gold_revision'],
                        'facet': facet, 'reviewer_id': None, 'reviewer_kind': 'human',
                        'independent_of_label_construction': None, 'norm_reference': g['norm_reference'],
                        'stroke_ids': g['stroke_ids'], 'verdict': 'pending', 'evidence': None}
                       for r, g in zip(manifest, gold) if r['split'] == 'audit_development'
                       for facet in ('E3', 'E4', 'E5')]
    write_jsonl(out / 'evaluation_only/review_template.jsonl', review_template)
    make_review(out, manifest, gold, args.private_output)
    splits = {name: [r['id'] for r in manifest if r['split'] == name]
              for name in sorted({r['split'] for r in manifest})}
    write_json(out / 'splits.json', {'seed': SEED, 'scope': 'development_partitions_only',
                                    'groups': splits, 'formal_holdout': 0,
                                    'style_OOD': None, 'future_main': 'not_created'})
    stats = {'protocol': 'paired-strokes-v1', 'data_status': 'development_candidates_built',
             'S0': 'completed_with_documented_source_limitations',
             'S1': 'cpu_pipeline_complete_independent_gold_pending',
             'graphics_revision': REVISION, 'graphics_hash': digest(graphics_bytes),
             'norm_text_hash': digest(args.norm_text.read_bytes()),
             'graphics_rows': len(graphics), 'norm_records_parsed': len(norm),
             'norm_index_entries': len(set(re.findall(r'\b\d{4}\s+([0-9A-F]{5})\b', args.norm_text.read_text()))),
             'norm_blocks_rejected': len(norm_rejections), 'eligible_before_exposure_filter': len(eligible),
             'source_rejection_counts': dict(Counter(r['reason'] for r in rejected)),
             'historical_exposure_characters': len(exposed), 'exposure_sources': exposure_sources,
             'pairs': len(manifest), 'strokes': sum(len(r['sequence']) for r in manifest),
             'partitions': dict(Counter(r['split'] for r in manifest)),
             'strata': dict(Counter(r['stroke_count_stratum'] for r in manifest)),
             'requests': len(requests), 'requests_by_metric': dict(Counter(r['metric'] for r in requests)),
             'requests_by_condition': dict(Counter(r['condition'] for r in requests)),
             'independent_accepted_gold': 0, 'qualified_D_SMOKE': 0,
             'qualified_D_PILOT': 0, 'model_calls': 0, 'GPU_MPS_calls': 0, 'training': 0,
             'main_changes': 0, 'remote_pushes': 0, 'wall_seconds': time.perf_counter() - started}
    write_json(out / 'build_record.json', stats)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def make_review(out, rows, gold, private):
    private.mkdir(parents=True, exist_ok=True)
    (private / 'licenses').mkdir(exist_ok=True)
    for name in ('COPYING', 'ARPHICPL.TXT'):
        shutil.copyfile(out / 'licenses' / name, private / 'licenses' / name)
    cards = []
    for row, item in zip(rows, gold):
        if row['split'] != 'audit_development':
            continue
        with np.load(out / item['mask_archive']) as archive:
            masks = archive['masks']
        tiles = []
        for i, path in enumerate(item['paths']):
            mask = masks[i]
            rgb = np.full((256, 256, 3), 255, dtype='uint8')
            rgb[mask] = 0
            im = Image.fromarray(rgb)
            draw = ImageDraw.Draw(im)
            start, end = np.asarray(path[0]) * 256, np.asarray(path[-1]) * 256
            for point, color in [(start, 'green'), (end, 'red')]:
                x, y = point
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
            filename = f'{row["id"]}-{i + 1:02d}.png'
            save_png(private / filename, np.asarray(im))
            tiles.append(f'<figure><img src="{filename}"><figcaption>候选第{i + 1}笔 / 五类{row["sequence"][i]} / '
                         f'{item["directions"][i]["direction"]}</figcaption></figure>')
        page = row['norm_reference']['pdf_page']
        cards.append(f'<article><h2>{html.escape(row["character"])} / {row["id"]}</h2>'
                     f'<p>规范PDF物理页 {page}，字表序号 {row["norm_reference"]["index"]}。'
                     '绿点起点，红点终点；这些标记是待核查候选。</p>'
                     f'<p>规范编码：{" ".join(row["sequence"])}</p>'
                     f'<a href="official/page-{page:03d}.png">查看独立规范原页（本地查阅）</a>'
                     '<div class="tiles">' + ''.join(tiles) + '</div></article>')
    (private / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>S1逐笔候选审核</title>'
        '<style>body{font:16px sans-serif;margin:32px;color:#222}article{border-top:1px solid #bbb;padding:16px 0}'
        '.tiles{display:flex;flex-wrap:wrap}figure{margin:8px}img{width:192px}figcaption{font-size:14px}</style>'
        '<h1>S1独立逐笔审核材料</h1><p>16字开发候选。已有P0/P1粗筛不构成本包逐笔审核。'
        '本页面展示SVG候选；核对规范顺序、实例身份、起终点和每项关系后，单独提交有来源的review记录。'
        '当前独立审核提交为0。</p><p>' + html.escape(NOTICE) + '</p>'
        '<p><a href="licenses/ARPHICPL.TXT">Arphic Public License</a> · '
        '<a href="licenses/COPYING">上游版权说明</a></p>' + ''.join(cards))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphics', type=Path, required=True)
    parser.add_argument('--norm-text', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--private-output', type=Path, required=True)
    build(parser.parse_args())


if __name__ == '__main__':
    main()
