"""Extract eight licensed glyphs, with explicitly reviewed normative bindings.

Run: python -m scripts.engineering.build_catalog --graphics path/to/graphics.txt
No source downloads, automatic normative inference, or human-gold upgrades.
"""
import argparse
import json
from pathlib import Path
import shutil

from hanzi_video.catalog import ASSETS

# Each tuple binds a normative position to a source stroke and its orientation.
# Reviewed against GF0023-2020 crops and the actual Arphic median overlays.
BINDINGS = {
    '士': ('N076', [('k8r', 0, '横', '从左向右'), ('k2b', 1, '竖', '从上向下'), ('k5p', 2, '横', '从左向右')]),
    '丑': ('N019', [('a7f', 0, '横折', '先右后下'), ('a2n', 1, '竖', '从上向下'), ('a9c', 2, '横', '从左向右'), ('a4q', 3, '横', '从左向右')]),
    '小': ('N079', [('b6m', 0, '竖钩', '下行后向左上出钩'), ('b1s', 1, '撇', '从右上向左下'), ('b8d', 2, '点', '从左上向右下')]),
    '以': ('N039', [('c9v', 0, '竖提', '下行后右上提'), ('c3a', 1, '点', '从左上向右下'), ('c1r', 2, '撇', '从右上向左下'), ('c7w', 3, '点', '从左上向右下')]),
    '广': ('N030', [('d5k', 0, '点', '从左上向右下'), ('d9e', 1, '横', '从左向右'), ('d2u', 2, '撇', '从上向左下')]),
    '刃': ('N066', [('e8x', 0, '横折钩', '先右后下再向左上出钩'), ('e1j', 1, '撇', '从右上向左下'), ('e4h', 2, '点', '侧点，从右上向左下')]),
    '乞': ('N043', [('f7z', 0, '撇', '从右上向左下'), ('f2i', 1, '横', '从左向右'), ('f5l', 2, '横折弯钩', '先右、转左下、向右弯行，末端向上出钩')]),
    '点': ('N017', [('g9q', 0, '竖', '从上向下'), ('g1t', 1, '横', '从左向右'), ('g7e', 2, '竖', '从上向下'), ('g3n', 3, '横折', '先右后下'), ('g6v', 4, '横', '从左向右'), ('g2y', 5, '点', '左侧点，从右上向左下'), ('g8b', 6, '点', '从左上向右下'), ('g4p', 7, '点', '从左上向右下'), ('g5a', 8, '点', '从左上向右下')]),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--graphics', type=Path, required=True)
    args = parser.parse_args()
    rows = {}
    with args.graphics.open() as source:
        for line in source:
            row = json.loads(line)
            if row['character'] in BINDINGS:
                rows[row['character']] = row
    original = json.loads(Path('data/research/runs/p0_closeout_2026-10-30/reference_catalog.json').read_text())
    refs = {r['character']: r for r in original['selected']}
    result = {'version': 'engineering-eight-v1', 'coverage': 'development_preview',
        'modification_notice': '2026-10-31 lljjcc426: extracted eight glyphs from graphics.txt, renamed to Yibi Kai Preview, added explicit normative bindings and reordered geometry storage; outlines/median coordinates unchanged. Derivative geometry remains under Arphic Public License.',
        'normative_document': 'GF0023-2020', 'normative_url': original['source_url'],
        'source': {'name': 'Make Me a Hanzi / Arphic PL Kai',
                   'revision': 'bddc96d41bef78427ed0e034e9f7e31d71fd1b92',
                   'url': 'https://github.com/skishore/makemeahanzi',
                   'license': 'Arphic Public License; see licenses/'}, 'characters': {}}
    for char, (ref_id, bindings) in BINDINGS.items():
        row, prior = rows[char], refs[char]
        sequence, shapes = [], []
        for stroke_id, source_index, name, direction_text in bindings:
            sequence.append({'id': stroke_id, 'name': name, 'direction': 'forward', 'instruction': direction_text})
            shapes.append({'id': stroke_id, 'outline': row['strokes'][source_index],
                           'path': row['medians'][source_index], 'source_index': source_index,
                           'binding_evidence': 'AI visual comparison of this source outline/median with official stroke diagram, 2026-10-31'})
        result['characters'][char] = {'character': char, 'reference_id': ref_id,
            'official_page': prior['official_page'], 'official_crop': prior['official_reference_crop'],
            'qualification': 'AI_reviewed_engineering_preview', 'human_per_stroke_gold': False,
            'inherited_human_scope': 'Prior global candidate review; different geometry; not per-stroke gold',
            'sequence': sequence, 'geometry': sorted(shapes, key=lambda s: s['id'])}
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / 'catalog.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    license_dir = ASSETS / 'licenses'
    license_dir.mkdir(exist_ok=True)
    for name in ('COPYING', 'ARPHICPL.TXT'):
        shutil.copyfile(Path('data/research/datasets/p0_stroke_synthetic_v1/licenses') / name, license_dir / name)
    print(f'Extracted {len(result["characters"])} licensed, explicitly bound development glyphs')


if __name__ == '__main__':
    main()
