"""Single-boundary input validation and explicit evidence permissions."""
import json
from pathlib import Path

TRACKS = ('K-CHAR','K-ORDER','V-STRUCT','H-ACTUAL','G-GLYPH','G-ATOMIC','G-STROKE','X-RECOVERY')
INPUT_KEYS = {'id','track','prompt','media','geometry_permission','prefix_end_seconds','visible_state','action'}
LABELS = {'correct','incorrect','unknown','not_applicable'}
FACETS = ('stroke_order','direction','completeness','historical_ink','temporal_observability','final_glyph','task_compliance')


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def validate_input(value):
    if set(value)-INPUT_KEYS or value.get('track') not in TRACKS:
        raise ValueError('Unknown input fields or track; evaluation/training information is forbidden')
    if not value.get('id') or not isinstance(value.get('prompt'),str):
        raise ValueError('Input ID and prompt required')
    if value['track']!='X-RECOVERY' and ({'visible_state','action'} & set(value)):
        raise ValueError('Explicit action/state hints belong only to the recovery track')
    for p in value.get('media',[]):
        path = Path(p)
        if path.is_absolute() or '..' in path.parts or path.parts[0] != 'media':
            raise ValueError('Media must stay inside the model-input media directory')
    if value['track'] == 'K-CHAR':
        text = json.dumps(value,ensure_ascii=False)
        if any('\u3400' <= c <= '\u9fff' for c in text):
            raise ValueError('K-CHAR must not expose the character in metadata or prompt')
    if value['track'] == 'H-ACTUAL' and value.get('geometry_permission') != 'G0':
        raise ValueError('History diagnostic inputs contain pixels only, no normative geometry')
    if value['track']=='H-ACTUAL' and any(s in json.dumps(value) for s in
            ('normative_program','observed_events','construction_events','true_event_order','standard_order=')):
        raise ValueError('Answer/log fields are forbidden in the actual-history prompt')
    return value


def validate_manifest(rows):
    seen=set(); groups={}
    for row in rows:
        if row['id'] in seen:
            raise ValueError('Duplicate sample ID')
        seen.add(row['id'])
        group=row['source_group']; split=row['split']
        if group in groups and groups[group] != split:
            raise ValueError('Source-group leakage across splits')
        groups[group]=split
        if row.get('formal_gold') and row['qualification'] != 'independent_per_stroke_human_gold':
            raise ValueError('Weak reference cannot become formal normative gold')
        if split != 'development_only':
            raise ValueError('This release creates development data only; no new holdout authorized')
    return {'samples':len(rows),'source_groups':len(groups),'formal_holdout':0}
