"""Build and score the two prerequisites for H1: answer interface and visible state."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'data/h1/state_gate_v1'
SIZE = 432
LAYOUTS = {
    'single_h': {'横线': [(70, 105), (350, 105)]},
    'single_v': {'竖线': [(216, 30), (216, 180)]},
    'parallel_h': {'上横': [(75, 45), (350, 45)],
                   '中横': [(130, 105), (285, 105)],
                   '下横': [(45, 170), (385, 170)]},
    'parallel_v': {'左竖': [(130, 35), (130, 180)],
                   '右竖': [(300, 55), (300, 165)]},
    'cross': {'横线': [(65, 105), (360, 105)],
              '竖线': [(216, 30), (216, 185)]},
    'fold': {'折线': [(85, 50), (335, 50), (335, 175)]},
}
STATES = ('未出现', '部分', '完整')


def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))


def read_jsonl(path):
    return [json.loads(s) for s in Path(path).read_text().splitlines()]


def path_length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def prefix(points, fraction):
    remaining = path_length(points) * fraction
    result = [points[0]]
    for a, b in zip(points, points[1:]):
        length = math.dist(a, b)
        if remaining < length:
            result.append(tuple(x + (y - x) * remaining / length for x, y in zip(a, b)))
            break
        result.append(b)
        remaining -= length
    return result


def panel(strokes, fractions, width, offset):
    image = Image.new('RGB', (SIZE, SIZE), 'white')
    draw = ImageDraw.Draw(image)
    for name, points in strokes.items():
        if fractions[name] > 0:
            draw.line([(round(x), round(y + offset)) for x, y in prefix(points, fractions[name])],
                      fill='black', width=width, joint='curve')
    return image


def render(case):
    full = {name: 1 for name in case['strokes']}
    reference = panel(case['strokes'], full, case['width'], 0)
    current = panel(case['strokes'], case['fractions'], case['width'], SIZE // 2)
    reference.paste(current.crop((0, SIZE // 2, SIZE, SIZE)), (0, SIZE // 2))
    return reference, current


def build(output, splits=None, views=None, forms=None, version='state_gate_v1', isolate_text=False,
          stretch_y=False, exclude_from=None):
    splits = splits or [('dev', 1, 1729), ('test', 5, 2718)]
    views = views or ['oracle_text', 'reference_current', 'current_only']
    forms = forms or ['plain', 'json']
    output.mkdir(parents=True, exist_ok=True)
    if any(v != 'oracle_text' for v in views):
        (output / 'images').mkdir(exist_ok=True)
    cases = []
    # Every state and wording variant of one geometry stays in the same split.
    for split, count, seed in splits:
        rng = random.Random(seed)
        for layout, template in LAYOUTS.items():
            for index in range(count):
                dx, dy = rng.randint(-10, 10), rng.randint(-6, 6)
                sx = rng.uniform(.84, 1.02)
                sy = rng.uniform(.8, 1.2) if stretch_y else 1
                strokes = {n: [(round(216 + (x - 216) * sx + dx), round(105 + (y - 105) * sy + dy)) for x, y in pts]
                           for n, pts in template.items()}
                target = list(strokes)[index % len(strokes)]
                others = {n: rng.choice([0, .5, 1]) for n in strokes}
                width = rng.choice([5, 7, 9])
                group = f'{split}-{layout}-{index:02d}'
                for variant, fraction in enumerate([0, .35, .75, 1]):
                    cases.append(dict(case_id=f'{group}-{variant}', group_id=group, split=split,
                                      layout=layout, strokes=strokes, target=target, width=width,
                                      fractions={**others, target: fraction}, reference_pair=None))
        # Identical current pixels, different reference lengths, opposite completion labels.
        for index in range(count):
            start = rng.randint(60, 90)
            visible = rng.randint(100, 130)
            y, width = rng.randint(85, 125), rng.choice([5, 7, 9])
            group = f'{split}-reference-{index:02d}'
            for variant, factor in [('short', 1), ('long', 2)]:
                cases.append(dict(case_id=f'{group}-{variant}', group_id=group, split=split,
                                  layout='reference_control',
                                  strokes={'横线': [(start, y), (start + visible * factor, y)]},
                                  target='横线', width=width, fractions={'横线': 1 / factor},
                                  reference_pair=group))

    inputs, labels = [], []
    for case in cases:
        cid, target = case['case_id'], case['target']
        if any(v != 'oracle_text' for v in views):
            reference, current = render(case)
            reference.save(output / 'images' / f'{cid}.png')
            current.save(output / 'images' / f'{cid}-current.png')
        lengths = [(name, round(path_length(points), 2),
                    round(path_length(points) * case['fractions'][name], 2))
                   for name, points in case['strokes'].items()]
        facts = '；'.join(f'{n}：参考完整长度{full}，当前已有长度{seen}' for n, full, seen in lengths)
        frac = case['fractions'][target]
        for view in views:
            context = {
                'oracle_text': '这是纯文字状态题，无需图像。每条线均沿参考路径从起点连续画出，'
                               '已画部分没有偏移、隐藏或重复。以下长度记录准确，单位相同。' + facts +
                               '。当前已有长度为0表示未出现；大于0且小于参考完整长度表示部分完成；'
                               '等于参考完整长度表示已经完整。',
                'reference_current': '图片上半部是完整参考，下半部是当前实际画面，两部分使用相同比例和位置。',
                'current_only': '图片只有下半部的当前画面，没有完整参考、目标长度或过程。'
                                '已出现的线条可能是完整短线，也可能是较长目标的一部分。',
            }[view]
            context += '本题只评价当前状态，不判断先后或笔内方向。'
            if view != 'oracle_text':
                context += '上、中、下及左、右均指下半部书写区域中的固定位置，名称不随其他线条缺失而重新排序。'
            question_target = target
            if view == 'current_only' and case['layout'] == 'fold':
                # A horizontal prefix alone does not reveal that its target will turn.
                question_target = '目标笔迹'
                context += '本题只有一个目标笔迹实例，它的完整形状没有提供。'
            for task in ['presence', 'completion']:
                expected = ('有' if frac > 0 else '无') if task == 'presence' else (
                    '未出现' if frac == 0 else '未知' if view == 'current_only' else
                    '完整' if frac == 1 else '部分')
                questions = {
                    'presence': [f'当前画面中有没有{question_target}？', f'{question_target}现在是否已经出现？'],
                    'completion': [f'相对完整参考，当前{question_target}的完成状态是什么？',
                                   f'当前{question_target}有没有达到参考中的完整形状？请给出完成状态。'],
                }
                domain = ['有', '无'] if task == 'presence' else ['未出现', '部分', '完整', '未知']
                rule = ('部分线条也算已出现；出现写“有”，未出现写“无”。' if task == 'presence' else
                        '没有出现写“未出现”；已出现且达到参考全部形状写“完整”；'
                        '只达到一部分写“部分”；缺少判断完成程度的依据写“未知”。')
                for wording, question in enumerate(questions[task]):
                    for form in forms:
                        ending = ('只输出判断词，不写解释。' if form == 'plain' else
                                  '只输出一个JSON对象，只含answer字段，值为判断词，不写解释。')
                        sid = f'{cid}-{view}-{task}-q{wording}-{form}'
                        inputs.append(dict(sample_id=sid, case_id=cid, group_id=case['group_id'],
                                           split=case['split'], layout=case['layout'], view=view,
                                           task=task, wording=wording, response_format=form,
                                           images=[] if view == 'oracle_text' else [
                                               f'images/{cid}' + ('-current.png' if view == 'current_only' else '.png')],
                                           prompt=context + question + rule + ending))
                        labels.append(dict(sample_id=sid, expected=expected, allowed=domain,
                                           reference_pair=case['reference_pair']))
    excluded = []
    if isolate_text or exclude_from:
        seen_prompts = ({r['prompt'] for r in read_jsonl(exclude_from / 'inputs.jsonl')} if exclude_from else
                        {r['prompt'] for r in inputs if r['split'] == 'dev'})
        excluded = sorted({r['group_id'] for r in inputs
                           if (exclude_from or r['split'] == 'train') and r['prompt'] in seen_prompts})
        inputs = [r for r in inputs if r['group_id'] not in excluded]
        retained = {r['sample_id'] for r in inputs}
        labels = [r for r in labels if r['sample_id'] in retained]
        cases = [c for c in cases if c['group_id'] not in excluded]
        # Geometry hidden from a text-only input cannot create independent evidence.
        prompts_by_group = defaultdict(set)
        for row in inputs:
            prompts_by_group[(row['split'], row['group_id'])].add(row['prompt'])
        canonical, aliases = {}, {}
        for (split, group), prompts in prompts_by_group.items():
            signature = (split, tuple(sorted(prompts)))
            aliases[group] = canonical.setdefault(signature, group)
        for row in inputs + cases:
            row['group_id'] = aliases[row['group_id']]
    write_jsonl(output / 'inputs.jsonl', inputs)
    write_jsonl(output / 'labels.jsonl', labels)
    (output / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n')
    summary = dict(version=version, seed_by_split={s: seed for s, _, seed in splits},
                   cases_by_split=dict(Counter(c['split'] for c in cases)),
                   groups_by_split={s: len({c['group_id'] for c in cases if c['split'] == s})
                                    for s, _, _ in splits},
                   input_rows=len(inputs), contains_model_predictions=False,
                   scope='Synthetic line-state diagnosis only; no order or font generalization claim.')
    if isolate_text or exclude_from:
        summary.update(excluded_groups_for_shared_text=excluded,
                       grouping='Text-equivalent geometry groups merged for confidence intervals.',
                       unique_prompts_by_split={s: len({r['prompt'] for r in inputs if r['split'] == s}) for s, _, _ in splits})
    if exclude_from:
        summary.update(exclude_visible_text_from=str(exclude_from.relative_to(ROOT)),
                       vertical_scale=[.8, 1.2] if stretch_y else [1, 1],
                       evaluation_policy='Fixed v1 adapter and fixed-answer decoding before test; no tuning on test results.')
    (output / 'build.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def build_basic_control(output):
    """Small whole-image control for vision access, without reference matching."""
    (output / 'images').mkdir(parents=True, exist_ok=True)
    shapes = {
        'blank': [],
        'horizontal': [[(70, 216), (350, 216)]],
        'vertical': [[(216, 70), (216, 350)]],
        'three_horizontal': [[(70, y), (350, y)] for y in (105, 216, 325)],
    }
    rows, labels = [], []
    for name, strokes in shapes.items():
        image = Image.new('RGB', (SIZE, SIZE), 'white')
        draw = ImageDraw.Draw(image)
        for points in strokes:
            draw.line(points, fill='black', width=7)
        path = f'images/basic-{name}.png'
        image.save(output / path)
        for task, questions, expected, allowed in [
            ('presence', ['Is there any black line in this image?',
                          'Does this image contain at least one black line?'],
             'yes' if strokes else 'no', ['yes', 'no']),
            ('count', ['How many black lines are in this image?',
                       'What is the number of black lines shown?'],
             str(len(strokes)), ['0', '1', '2', '3']),
        ]:
            ending = ' Answer with exactly yes or no.' if task == 'presence' else ' Answer with a single digit.'
            for wording, question in enumerate(questions):
                sid = f'basic-{name}-{task}-q{wording}'
                rows.append(dict(sample_id=sid, case_id=f'basic-{name}', group_id=f'basic-{name}',
                                 split='dev', layout=name, view='current_only', task=task,
                                 wording=wording, response_format='plain', images=[path],
                                 prompt=question + ending))
                labels.append(dict(sample_id=sid, expected=expected, allowed=allowed, reference_pair=None))
    write_jsonl(output / 'basic_visual_controls.jsonl', rows)
    write_jsonl(output / 'basic_visual_control_labels.jsonl', labels)
    print(f'{len(shapes)} simple images; {len(rows)} vision-access control questions.')


def build_relation_control(output):
    """Short binary questions on existing single-line reference/current images."""
    cases = [c for c in json.loads((output / 'cases.json').read_text())
             if c['split'] == 'dev' and c['layout'] in ('single_h', 'single_v', 'reference_control')]
    rows, labels = [], []
    context = ('The top half shows a complete reference line. '
               'The bottom half shows the current drawing at the same scale. ')
    for case in cases:
        cid = case['case_id']
        fraction = case['fractions'][case['target']]
        for task, questions, expected in [
            ('presence', ['Is there a black line in the bottom half?',
                          'Does the lower half contain any black line?'], 'yes' if fraction > 0 else 'no'),
            ('completion', ['Is the entire reference line present in the bottom half?',
                            'Does the bottom half show the full reference line with no part missing?'],
             'yes' if fraction == 1 else 'no'),
        ]:
            for wording, question in enumerate(questions):
                sid = f'simple-en-{cid}-{task}-q{wording}'
                rows.append(dict(sample_id=sid, case_id=cid, group_id=case['group_id'], split='dev',
                                 layout=case['layout'], view='reference_current', task=task,
                                 wording=wording, response_format='plain', images=[f'images/{cid}.png'],
                                 prompt=context + question + ' Answer with exactly yes or no.'))
                labels.append(dict(sample_id=sid, expected=expected, allowed=['yes', 'no'],
                                   reference_pair=case['reference_pair']))
    write_jsonl(output / 'simple_relation_controls.jsonl', rows)
    write_jsonl(output / 'simple_relation_control_labels.jsonl', labels)
    print(f'{len(cases)} existing dev cases; {len(rows)} short relation-control questions.')


def build_region_control(output):
    """Hold question and current pixels fixed; remove only the upper reference."""
    source = read_jsonl(output / 'simple_relation_controls.jsonl')
    source_labels = {r['sample_id']: r for r in read_jsonl(output / 'simple_relation_control_labels.jsonl')}
    rows, labels = [], []
    questions = ['Is there a black line in the bottom half of this image?',
                 'Does the lower half of this image contain any black line?']
    for inp in source:
        if inp['task'] != 'presence':
            continue
        for view in ['reference_current', 'current_only']:
            sid = f'region-{inp["case_id"]}-{view}-q{inp["wording"]}'
            row = dict(inp, sample_id=sid, view=view,
                       prompt=questions[inp['wording']] + ' Answer with exactly yes or no.',
                       images=[f'images/{inp["case_id"]}' + ('-current.png' if view == 'current_only' else '.png')])
            rows.append(row)
            labels.append(dict(source_labels[inp['sample_id']], sample_id=sid))
    write_jsonl(output / 'region_controls.jsonl', rows)
    write_jsonl(output / 'region_control_labels.jsonl', labels)
    print(f'{len(rows)} questions with matched wording and current pixels.')


def parse(raw, form, allowed):
    value = raw.strip()
    if form == 'json':
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return None
        if not isinstance(value, dict) or set(value) != {'answer'}:
            return None
        value = value['answer']
    return value if isinstance(value, str) and value in allowed else None


def interval(values_by_group):
    """Percentile bootstrap of whole geometry groups, preserving dependent variants."""
    groups = list(values_by_group.values())
    if len(groups) < 2:
        return None
    rng = random.Random(3901)
    estimates = []
    for _ in range(2000):
        sample = [v for group in rng.choices(groups, k=len(groups)) for v in group]
        estimates.append(sum(sample) / len(sample))
    estimates.sort()
    return [estimates[49], estimates[1949]]


def word_audit(inputs, labels, predictions):
    """Post-hoc word interpretation; never replaces the strict interface score."""
    aliases = {'有': '有', '无': '无', '未出现': '未出现', '部分': '部分',
               '完整': '完整', '未知': '未知', 'yes': '有', 'no': '无',
               'absent': '未出现', 'part': '部分', 'partial': '部分', 'partially': '部分',
               'complete': '完整', 'unknown': '未知'}
    tasks, pairs, reference_pairs, details = {}, defaultdict(list), defaultdict(list), []
    for sid, inp in inputs.items():
        raw = predictions.get(sid, {}).get('raw_response', '').strip()
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = raw
        if isinstance(value, dict) and set(value) == {'answer'}:
            value = value['answer']
        answer = aliases.get(value) if isinstance(value, str) else None
        expected = aliases.get(labels[sid]['expected'], labels[sid]['expected'])
        correct = answer == expected
        key = f'{inp["view"]}/{inp["task"]}'
        task = tasks.setdefault(key, dict(n=0, interpretable=0, correct=0, confusion={}))
        task['n'] += 1
        task['interpretable'] += int(answer is not None)
        task['correct'] += int(correct)
        confusion = task['confusion'].setdefault(expected, {})
        confusion[answer or 'uninterpretable'] = confusion.get(answer or 'uninterpretable', 0) + 1
        pairs[(key, inp['case_id'])].append(correct)
        ref = labels[sid]['reference_pair']
        if ref and inp['view'] == 'reference_current' and inp['task'] == 'completion':
            reference_pairs[(key, ref, inp['wording'])].append(correct)
        details.append(dict(sample_id=sid, interpreted=answer, expected=expected, correct=correct))
    for key, task in tasks.items():
        cases = [values for (k, _), values in pairs.items() if k == key]
        refs = [values for (k, _, _), values in reference_pairs.items() if k == key]
        task['both_wordings_correct'] = dict(correct=sum(len(v) == 2 and all(v) for v in cases), n=len(cases))
        if refs:
            task['reference_pairs_correct'] = dict(correct=sum(len(v) == 2 and all(v) for v in refs), n=len(refs))
    return dict(role='Post-hoc diagnostic only; not a replacement for strict scores or a gate pass.',
                method='Exact standalone word or single-field answer JSON; no explanation extraction.',
                aliases=aliases, tasks=tasks, details=details)


def evaluate(data, predictions, split, form, output, view=None, audit=False):
    inputs = {r['sample_id']: r for r in read_jsonl(data / 'inputs.jsonl')
              if r['split'] == split and r['response_format'] == form
              and (view is None or r['view'] == view)}
    labels = {r['sample_id']: r for r in read_jsonl(data / 'labels.jsonl')}
    rows = read_jsonl(predictions)
    pred = {r['sample_id']: r for r in rows}
    if len(rows) != len(pred):
        raise ValueError('Keep repeated attempts in separate run files.')
    if set(pred) - set(inputs):
        raise ValueError('Prediction IDs do not match the selected split and format.')
    groups = defaultdict(lambda: defaultdict(list))
    paired = defaultdict(dict)
    states, confusion = defaultdict(dict), defaultdict(lambda: defaultdict(Counter))
    detail = []
    # Missing rows count as failures; partial runs cannot silently improve the denominator.
    for sid, inp in inputs.items():
        lab = labels[sid]
        answer = parse(pred.get(sid, {}).get('raw_response', ''), form, lab['allowed'])
        valid, correct = answer is not None, answer == lab['expected']
        key = f'{inp["view"]}/{inp["task"]}'
        confusion[key][lab['expected']][answer or 'invalid'] += 1
        for metric, value in [('format', valid), ('correct', correct),
                              (f'class_{lab["expected"]}', correct),
                              (f'wording_{inp["wording"]}', correct)]:
            groups[f'{key}/{metric}'][inp['group_id']].append(int(value))
        if inp.get('layout'):
            groups[f'{key}/layout_{inp["layout"]}'][inp['group_id']].append(int(correct))
        states[(inp['view'], inp['case_id'], inp['wording'], inp['group_id'])][inp['task']] = (answer, correct)
        paired[(key, inp['case_id'])][inp['wording']] = correct
        if lab['reference_pair'] and inp['task'] == 'completion' and inp['view'] == 'reference_current':
            paired[(f'{key}/reference_pair_q{inp["wording"]}', lab['reference_pair'])][inp['case_id']] = correct
        detail.append(dict(sample_id=sid, expected=lab['expected'], parsed=answer,
                           valid=valid, correct=correct, missing=sid not in pred))
    for (input_view, _, _, group), state in states.items():
        if 'presence' in state and 'completion' in state:
            presence, presence_correct = state['presence']
            completion, completion_correct = state['completion']
            groups[f'{input_view}/joint_state/correct'][group].append(int(presence_correct and completion_correct))
            consistent = (presence is not None and completion is not None and
                          ((presence == '无') == (completion == '未出现')))
            groups[f'{input_view}/joint_state/logical_consistency'][group].append(int(consistent))
    for (key, case), values in paired.items():
        group = next(r['group_id'] for r in inputs.values()
                     if r['case_id'] == case or r['group_id'] == case)
        groups[key + '/both_correct'][group].append(int(len(values) == 2 and all(values.values())))
    report = dict(split=split, response_format=form, view=view, expected_rows=len(inputs),
                  attempted_rows=len(pred), missing_rows=len(inputs) - len(pred),
                  confusion=confusion, metrics={})
    for name, grouped in sorted(groups.items()):
        values = [v for group in grouped.values() for v in group]
        report['metrics'][name] = dict(correct=sum(values), n=len(values),
                                        rate=sum(values) / len(values), independent_groups=len(grouped),
                                        cluster_bootstrap_95=interval(grouped))
    output.mkdir(parents=True, exist_ok=True)
    (output / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    write_jsonl(output / 'scored.jsonl', detail)
    if audit:
        (output / 'word_audit.json').write_text(json.dumps(
            word_audit(inputs, labels, pred), ensure_ascii=False, indent=2) + '\n')
    print(f'{len(pred)}/{len(inputs)} attempted; report: {output / "summary.json"}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['build', 'build-training', 'build-visual-training', 'build-text-test', 'build-basic-control', 'build-relation-control', 'build-region-control', 'score'])
    p.add_argument('--data', type=Path)
    p.add_argument('--predictions', type=Path)
    p.add_argument('--split', choices=['train', 'dev', 'test'], default='dev')
    p.add_argument('--format', choices=['plain', 'json'], default='plain')
    p.add_argument('--output', type=Path)
    p.add_argument('--view', choices=['oracle_text', 'reference_current', 'current_only'])
    p.add_argument('--audit-words', action='store_true', help='Separately interpret exact answer words after scoring.')
    args = p.parse_args()
    defaults = {'build-training': ROOT / 'data/h1/state_training_v1',
                'build-visual-training': ROOT / 'data/h1/state_visual_training_v1',
                'build-text-test': ROOT / 'data/h1/state_text_test_v1'}
    args.data = args.data or defaults.get(args.command, DEFAULT)
    if args.command == 'build':
        build(args.data)
    elif args.command == 'build-training':
        build(args.data, [('train',6,10317),('dev',2,20429)], ['oracle_text'], ['json'],
              'state_training_v1', isolate_text=True)
    elif args.command == 'build-text-test':
        build(args.data, [('test',8,40519)], ['oracle_text'], ['json'], 'state_text_test_v1',
              stretch_y=True, exclude_from=ROOT / 'data/h1/state_training_v1')
    elif args.command == 'build-visual-training':
        build(args.data, [('train',3,50623)], ['reference_current', 'current_only'], ['json'],
              'state_visual_training_v1', stretch_y=True)
    elif args.command == 'build-basic-control':
        build_basic_control(args.data)
    elif args.command == 'build-relation-control':
        build_relation_control(args.data)
    elif args.command == 'build-region-control':
        build_region_control(args.data)
    else:
        if not args.predictions or not args.output:
            p.error('score requires --predictions and --output')
        evaluate(args.data, args.predictions, args.split, args.format, args.output, args.view, args.audit_words)
