"""CPU image/target batches from the narrow pair export; no gold or SVG reads."""
from dataclasses import dataclass

import numpy as np
from PIL import Image

from .paired import PAD, EOS


@dataclass
class Batch:
    ids: tuple[str, ...]
    images: np.ndarray
    targets: np.ndarray
    target_mask: np.ndarray
    character_unicode: np.ndarray
    descriptions: tuple[str, ...]


def collate(pairs):
    """Preserve RGB size; coarse/EOS IDs are CPU contract tokens, not an LLM tokenizer."""
    images = []
    targets = np.full((len(pairs), max(len(p.strokes) + 1 for p in pairs)), PAD, dtype=np.int64)
    for i, pair in enumerate(pairs):
        with Image.open(pair.image_path) as image:
            images.append(np.asarray(image.convert('RGB'), dtype=np.float32).transpose(2, 0, 1) / 255)
        targets[i, :len(pair.strokes) + 1] = [*pair.strokes, EOS]
    return Batch(tuple(p.sample_id for p in pairs), np.stack(images), targets,
                 targets != PAD, np.array([ord(p.character) for p in pairs], dtype=np.int64),
                 tuple(p.description for p in pairs))
