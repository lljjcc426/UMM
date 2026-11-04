"""Evaluation-only geometry candidates; qualification is separate from rendering."""
import math

import numpy as np
from PIL import Image, ImageDraw, PngImagePlugin

from scripts.p0.geometry import flatten_path, transform
from .data import NOTICE


def render_masks(graphic, size=256):
    masks = []
    for outline in graphic['strokes']:
        image = Image.new('1', (size, size))
        ImageDraw.Draw(image).polygon([tuple(p) for p in transform(flatten_path(outline), size)], fill=1)
        masks.append(np.asarray(image, dtype=bool))
    return np.stack(masks)


def save_png(path, array):
    path.parent.mkdir(parents=True, exist_ok=True)
    info = PngImagePlugin.PngInfo()
    info.add_text('Notice', NOTICE)
    Image.fromarray(array).save(path, pnginfo=info)


def spatial_relations(masks, medians):
    """Image coordinates: x right, y down. Binary predicates have an unknown band.

    Centroid margin: 0.02 canvas; length ratio margin: 5%; intersect means
    raster-outline contact/overlap, NOT a normative crossing classification.
    """
    size = masks.shape[-1]
    centers = [np.asarray(np.nonzero(m)[::-1]).mean(axis=1) / size for m in masks]
    lengths = [float(np.linalg.norm(np.diff(np.asarray(p), axis=0), axis=1).sum()) for p in medians]
    rows = []
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            dx, dy = centers[j] - centers[i]
            uncertain = lambda delta: None if abs(delta) <= .02 else bool(delta > 0)
            ratio = lengths[i] / lengths[j]
            values = {'left': uncertain(dx), 'right': uncertain(-dx),
                      'above': uncertain(dy), 'below': uncertain(-dy),
                      'intersect': bool((masks[i] & masks[j]).any()),
                      'longer': None if 1 / 1.05 <= ratio <= 1.05 else bool(ratio > 1)}
            rows.extend({'a': i + 1, 'b': j + 1, 'relation': key, 'answer': value}
                        for key, value in values.items())
    return rows


def direction(path):
    """Eight-way start-to-end displacement; does not describe every turn."""
    dx, dy = np.asarray(path[-1]) - np.asarray(path[0])
    angle = math.atan2(dy, dx)
    return ('right', 'down_right', 'down', 'down_left', 'left',
            'up_left', 'up', 'up_right')[round(angle / (math.pi / 4)) % 8]


def review_keys(item, facet):
    """The manual choices required by the existing per-character review form."""
    sid = item['id']
    sequence = [f'{sid}:sequence']
    identities = sequence + [f'{sid}:identity:{k}' for k in item['stroke_ids']]
    if facet == 'PAIR':
        return sequence
    if facet == 'E3':
        return identities
    if facet == 'E4':
        return identities + sorted({f'{sid}:pair:{r["a"]}:{r["b"]}' for r in item['relations']})
    return identities + [f'{sid}:direction:{k}' for k in item['stroke_ids']]


def qualify(item, reviews, facet):
    """One independent, documented audit per facet and item, from a named reviewer.

    An approval must identify the geometry version, normative reference and an
    external evidence record. E3/E4/E5 also require every relevant manual choice
    to be accepted. A summary confirmation can accept development pairs only.
    Source-derived candidates cannot self-qualify.
    A disagreement keeps the item disputed even when another review passes it.
    """
    relevant = [r for r in reviews if r.get('sample_id') == item['id']
                and r.get('facet') == facet and r.get('gold_revision') == item['gold_revision']]
    if any(r.get('verdict') == 'disputed' for r in relevant):
        return False
    return any(r.get('verdict') == 'accepted' and r.get('reviewer_kind') == 'human'
               and r.get('reviewer_id') and r.get('independent_of_label_construction') is True
               and r.get('norm_reference') == item['norm_reference'] and r.get('evidence')
               and set(r.get('stroke_ids', [])) == set(item['stroke_ids'])
               and (facet == 'PAIR' or all(r.get('item_decisions', {}).get(k) == 'accepted'
                                           for k in review_keys(item, facet))) for r in relevant)
