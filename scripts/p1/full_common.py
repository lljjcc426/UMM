"""Shared input fingerprints and exact scope checks for the authorized P1 run."""
import hashlib
import json
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def normalized_input(path):
    sample = json.loads(Path(path).read_text())
    assets = {}
    for row in sample.values():
        if isinstance(row, dict):
            for i, kind in enumerate(row['element_dtype_array']):
                if kind in ['image', 'video']:
                    media = Path(row['interleave_array'][i])
                    assets[media.name] = sha256(media)
                    row['interleave_array'][i] = media.name
    return dict(sample=sample, assets=assets)


def input_fingerprint(path):
    normalized = normalized_input(path)
    return hashlib.sha256(json.dumps(normalized, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def validate_scope(auth, manifest):
    expected_counts = dict(generation=64, understanding=28, codec=8, controls=8)
    if auth['user_approved'] is not True or auth['max_extra_GPU_retries'] != 0:
        raise ValueError('Full execution requires explicit approval and zero extra GPU retries')
    for kind, count in expected_counts.items():
        ids = [r['id'] for r in manifest[kind]]
        if len(ids) != count or len(set(ids)) != count or set(ids) != set(auth['approved_ids'][kind]):
            raise ValueError('Exact frozen scope mismatch: ' + kind)
    for row in manifest['generation']:
        if row['id'] != f"{row['norm_id']}-{row['condition']}-s{row['seed']}":
            raise ValueError('Generation ID and frozen fields differ')
        if (row['task'] not in ['t2v', 'i2v'] or row['seed'] not in [11, 29, 47]
                or row['condition'] not in auth['generation_conditions']
                or row['norm_id'] not in auth['norm_ids']):
            raise ValueError('Generation fields exceed the frozen matrix')
        if (row['task'] == 'i2v') != (row['condition'] == 'T_G0_blank_i2v'):
            raise ValueError('Task/condition mismatch')
        expected = 'G1_fixed_development_template' if row['condition'] == 'T_G1_template_text' else 'G0'
        if row['geometry_permission'] != expected:
            raise ValueError('Geometry permission mismatch')
    return manifest
