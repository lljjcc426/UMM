"""Narrow trainer-facing paired data reader. Never read evaluation-only labels."""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from PIL import Image

COARSE_TYPES = {"横": 1, "竖": 2, "撇": 3, "点": 4, "折": 5}
TOKEN_NAMES = {v: k for k, v in COARSE_TYPES.items()}
PAD, MASK, BOS, EOS = 0, 6, 7, 8
_SAMPLE_ID = re.compile(r"^[0-9a-f]{16}$")
_MEDIA = re.compile(r"^media/[0-9a-f]{16}\.png$")

@dataclass(frozen=True)
class Pair:
    sample_id: str
    image_path: Path
    strokes: tuple[int, ...]
    character: str
    image_digest: str
    description: str


def parse_description(value: str) -> tuple[tuple[int, ...], str]:
    """Parse the *actual stored* v1 description (no literal [EOF])."""
    if not isinstance(value, str) or '[EOF]' in value or '[EOS]' in value:
        raise ValueError('Invalid stored description/EOS')
    items = value.split('、')
    if len(items) < 2 or len(items[-1]) != 1 or not items[-1].strip():
        raise ValueError('Expected stroke types followed by exactly one result character')
    if any(t not in COARSE_TYPES for t in items[:-1]):
        raise ValueError('Description contains non-v1 coarse-stroke types')
    return tuple(COARSE_TYPES[t] for t in items[:-1]), items[-1]


def _image_path(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not _MEDIA.fullmatch(rel):
        raise ValueError('Image path must be opaque media/<sample_id>.png')
    base = root.resolve()
    path = (base / rel).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError('Missing or disallowed image path')
    return path


def read_pairs(jsonl: Path, data_root: Path) -> list[Pair]:
    """Read only the exported paired view, rejecting provenance/gold additions."""
    pairs = []
    seen_ids, seen_hashes = set(), set()
    for n, line in enumerate(jsonl.read_text(encoding='utf8').splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if set(record) != {'id', 'model_inputs', 'training_targets'}:
            raise ValueError(f'Line {n}: unexpected source or label field')
        if set(record['model_inputs']) != {'image'} or set(record['training_targets']) != {'description'}:
            raise ValueError(f'Line {n}: expected only image and description')
        sid = record['id']
        if not isinstance(sid, str) or not _SAMPLE_ID.fullmatch(sid) or sid in seen_ids:
            raise ValueError('Invalid/duplicate sample ID')
        path = _image_path(data_root, record['model_inputs']['image'])
        if path.stem != sid:
            raise ValueError('Sample ID differs from opaque image file ID')
        description = record['training_targets']['description']
        strokes, char = parse_description(description)
        if len(strokes) > 64:
            raise ValueError('Sample exceeds 64 strokes')
        # Load once; decoding errors surface here. White backgrounds contain ink.
        with Image.open(path) as im:
            im = im.convert('L')
            if im.getextrema()[0] >= 128:
                raise ValueError('No visible character ink in supplied image')
        digest = sha256(path.read_bytes()).hexdigest()
        if digest in seen_hashes:
            raise ValueError('Exact image duplication within one training export')
        pairs.append(Pair(sid, path, strokes, char, digest, description))
        seen_ids.add(sid)
        seen_hashes.add(digest)
    return pairs


def audit_disjoint(partitions: dict[str, list[Pair]]) -> dict:
    """Detect character, image and ID overlap *between* partitions."""
    slots = {}
    for split, rows in partitions.items():
        for row in rows:
            for kind, value in (('character', row.character), ('image', row.image_digest), ('id', row.sample_id)):
                key = kind, value
                if key in slots and slots[key] != split:
                    raise ValueError(f'{kind} leakage between {slots[key]} and {split}')
                slots[key] = split
    return {'passed': True, 'partitions': {k: len(v) for k, v in partitions.items()}, 'checks': ['character', 'image_sha256', 'id']}
