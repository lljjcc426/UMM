"""Explicit normative bindings, separate from source storage order."""
import json
from pathlib import Path

ASSETS = Path(__file__).parent / 'assets'


def load_catalog():
    return json.loads((ASSETS / 'catalog.json').read_text())


def reference(character):
    entries = load_catalog()['characters']
    if character not in entries:
        raise ValueError('当前原型仅支持：' + '、'.join(entries))
    return entries[character]


def canonical_plan(ref):
    """For explicit CPU previews and tests; never presented as a model answer."""
    return {'character': ref['character'], 'strokes': [
        {'id': s['id'], 'direction': s['direction']} for s in ref['sequence']]}


def validate_plan(plan, ref):
    errors = []
    if not isinstance(plan, dict) or plan.get('character') != ref['character']:
        return ['目标字与输入不一致']
    strokes = plan.get('strokes')
    if not isinstance(strokes, list) or len(strokes) != len(ref['sequence']):
        return ['笔画数量错误']
    for index, (actual, expected) in enumerate(zip(strokes, ref['sequence']), 1):
        if not isinstance(actual, dict) or actual.get('id') != expected['id']:
            errors.append(f'第{index}笔的身份或顺序错误')
        elif actual.get('direction') != expected['direction']:
            errors.append(f'第{index}笔的方向错误')
    return errors


def geometry(ref):
    # Only this explicit, separately audited mapping binds geometry to the norm.
    strokes = {s['id']: s for s in ref['geometry']}
    return {'strokes': [strokes[s['id']]['outline'] for s in ref['sequence']],
            'medians': [strokes[s['id']]['path'] if s['direction'] == 'forward'
                        else list(reversed(strokes[s['id']]['path'])) for s in ref['sequence']]}
