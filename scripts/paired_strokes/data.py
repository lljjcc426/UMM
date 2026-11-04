"""Independent normative text ingestion and narrow training exports."""
import hashlib
import json
import re

REVISION = 'bddc96d41bef78427ed0e034e9f7e31d71fd1b92'
CLASSES = {'1': '横', '2': '竖', '3': '撇', '4': '点', '5': '折'}
NOTICE = ('UMM Paired Stroke Pilot, modified 2026-11-02 by lljjcc426 from '
          'Make Me a Hanzi graphics@' + REVISION + '. Selected glyphs, rasterized '
          'outlines, generated instance IDs and evaluation geometry. '
          'Copyright (C) 1999 Arphic Technology Co., Ltd. '
          'Derived geometry/media under Arphic Public License; no warranty. '
          'See licenses/ARPHICPL.TXT and licenses/COPYING.')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def parse_norm(text):
    """Read the cached pdftotext -layout output, independently of SVG order.

    The official table wraps sequences before AND after its index/UCS line.
    A record must have one code point, one count and exactly that many codes.
    Incomplete/misaligned text stays in the rejection ledger, without repair.
    """
    records, rejected = {}, []
    for page, content in enumerate(text.split('\f'), 1):
        lines = content.splitlines()
        headers = [list(re.finditer('汉字', line)) for line in lines
                   if line.count('汉字') == 2 and 'UCS' in line]
        if not headers:
            continue
        cut = headers[0][1].start()
        if lines and re.fullmatch(r'\s*\d+\s*', lines[-1]):
            lines = lines[:-1]  # Printed page number, outside the table.
        for right in (False, True):
            blocks, block = [], None
            for line in lines:
                line = line[cut:] if right else line[:cut]
                if (re.match(r'^\s*[\u3400-\u9fff\U00020000-\U000323af](?:\s|$)', line)
                        and not line.lstrip().startswith(('汉字', '序号'))):
                    if block:
                        blocks.append(block)
                    block = []
                if block is not None:
                    block.append(line)
            if block:
                blocks.append(block)
            for block in blocks:
                raw = '\n'.join(block)
                codes = re.findall(r'\b(\d{4})\s+([0-9A-F]{5})\b', raw)
                counts = re.findall(r'(\d+)\s*画', raw)
                if len(codes) != 1 or len(counts) != 1:
                    rejected.append({'pdf_page': page, 'reason': 'ambiguous_text_block',
                                     'source_text': raw})
                    continue
                index, ucs = codes[0]
                char, count = chr(int(ucs, 16)), int(counts[0])
                stripped = re.sub(r'\b\d{4}\s+[0-9A-F]{5}\b|\d+\s*画', '', raw)
                sequence = re.findall(r'(?<!\w)[1-5](?!\w)', stripped)
                if len(sequence) != count or raw.lstrip()[0] != char or char in records:
                    rejected.append({'character': char, 'pdf_page': page,
                                     'reason': 'incomplete_or_misaligned_sequence',
                                     'expected_count': count, 'parsed_codes': sequence,
                                     'source_text': raw})
                    continue
                records[char] = {'character': char, 'standard': 'GF0023-2020',
                                 'index': int(index), 'pdf_page': page,
                                 'sequence': sequence, 'stroke_count': count,
                                 'source_text': raw}
    return records, rejected


def description(character, sequence):
    # EOS is supplied later by each model's actual tokenizer, never a literal token.
    return '、'.join([CLASSES[s] for s in sequence] + [character])


def training_view(row):
    """The entire trainer-facing record; no provenance, instance or answer extras."""
    return {'id': row['id'], 'model_inputs': {'image': row['model_inputs']['image']},
            'training_targets': {'description': row['training_targets']['description']}}


def validate_manifest(rows):
    ids, partitions = set(), {}
    for row in rows:
        if row['id'] in ids:
            raise ValueError('Duplicate sample ID')
        ids.add(row['id'])
        if set(row['model_inputs']) != {'image'} or set(row['training_targets']) != {'description'}:
            raise ValueError('Training boundary contains additional supervision')
        if row['training_targets']['description'] != description(row['character'], row['sequence']):
            raise ValueError('Description and normative sequence differ')
        for field in ('char_id', 'glyph_template_id', 'source_record_id', 'group_id', 'file_hash'):
            group = (field, row[field])
            if group in partitions and partitions[group] != row['split']:
                raise ValueError('Character/template/source/image leakage across partitions')
            partitions[group] = row['split']
        if row.get('formal_gold'):
            raise ValueError('This candidate release contains no independently accepted formal gold')
    return {'samples': len(rows), 'character_groups': len({r['char_id'] for r in rows}),
            'formal_gold': 0}
