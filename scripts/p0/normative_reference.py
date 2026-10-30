"""Static reference qualification. This module cannot read RGB or a supplied plan."""
from dataclasses import dataclass


@dataclass(frozen=True)
class NormSpec:
    reference_id: str
    character: str
    canonical_order: tuple[str, ...]
    stroke_descriptions: tuple[str, ...]
    provenance: str
    variant_scope: str = 'listed_GF0023_2020_sequence_only'


@dataclass(frozen=True)
class BindingItem:
    instance_id: str
    canonical_id: str
    start_anchor: str
    end_anchor: str


@dataclass(frozen=True)
class GeometryBinding:
    binding_id: str
    items: tuple[BindingItem, ...]


@dataclass(frozen=True)
class QualifiedReference:
    spec: NormSpec
    binding: GeometryBinding
    status: str
    reasons: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    audit_level: str


def qualify_reference(norm_spec, geometry_binding, review_records):
    """Require an explicit per-instance static audit, never a global human pass."""
    canonical = norm_spec.canonical_order
    items = geometry_binding.items
    if (len(set(canonical)) != len(canonical) or
            len({i.instance_id for i in items}) != len(items) or
            len({i.canonical_id for i in items}) != len(items)):
        raise ValueError('Duplicate normative or geometry identity')
    records = {r['instance_id']: r for r in review_records}
    rank = {key: i for i, key in enumerate(canonical)}
    reasons = []
    if set(canonical) != {i.canonical_id for i in items}:
        reasons.append('incomplete_identity_binding')
    for item in items:
        r = records.get(item.instance_id)
        if (r is None or r.get('canonical_id') != item.canonical_id or
                r.get('norm_reference_id') != norm_spec.reference_id or
                r.get('normative_position') != rank.get(item.canonical_id, -1) + 1 or
                r.get('normative_stroke_description') != dict(zip(canonical, norm_spec.stroke_descriptions)).get(item.canonical_id) or
                r.get('start_anchor') != item.start_anchor or r.get('end_anchor') != item.end_anchor or
                r.get('identity_status') != 'verified' or r.get('direction_status') != 'verified' or
                not r.get('evidence') or not r.get('normative_comparison')):
            reasons.append('unqualified_instance:' + item.instance_id)
    if not norm_spec.provenance or not items:
        reasons.append('reference_provenance_or_binding_missing')
    levels = {r.get('audit_level', 'unspecified') for r in review_records}
    return QualifiedReference(norm_spec, geometry_binding, 'qualified' if not reasons else 'unknown',
        tuple(reasons), tuple(r['evidence_id'] for r in review_records if r.get('evidence_id')),
        next(iter(levels)) if len(levels) == 1 else 'mixed_or_missing')
