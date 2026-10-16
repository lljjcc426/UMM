"""Build a small, fully specified H1 diagnostic set; no model inference."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/h1/pilot_v1'
SIZE = (224, 224)
STROKES = {
    'three': {'top': ((60, 50), (164, 50)),
              'middle': ((76, 112), (148, 112)),
              'bottom': ((40, 174), (184, 174))},
    'ten': {'horizontal': ((40, 112), (184, 112)),
            'vertical': ((112, 36), (112, 188))},
}
CANONICAL = {'three': ['top', 'middle', 'bottom'], 'ten': ['horizontal', 'vertical']}
DESCRIPTIONS = {
    'three': '目标字为三。实例ID：bottom=下横，top=上横，middle=中横。',
    'ten': '目标字为十。实例ID：vertical=竖，horizontal=横。',
}


def render(glyph, events):
    image = Image.new('RGB', SIZE, 'white')
    frames = [image.copy()]
    for sid, progress, reverse in events:
        start, end = STROKES[glyph][sid]
        if reverse:
            start, end = end, start
        base = image.copy()
        for step in range(1, round(progress * 4) + 1):
            image = base.copy()
            endpoint = tuple(round(a + step/4 * (b-a)) for a, b in zip(start, end))
            ImageDraw.Draw(image).line([start, endpoint], fill='black', width=9)
            frames.append(image)
    return frames


def cases():
    return [
        ('c00', 'three', [], 'blank'),
        ('c01', 'three', [('top', .5, False)], 'partial_first'),
        ('c02', 'three', [('top', 1, False)], 'complete_first'),
        ('c03', 'three', [('top', 1, False), ('middle', .5, False)], 'partial_second'),
        ('c04', 'three', [('top', 1, False), ('middle', 1, False), ('bottom', 1, False)], 'correct'),
        ('c05', 'three', [('top', 1, False), ('bottom', 1, False), ('middle', 1, False)], 'swapped'),
        ('c06', 'three', [('top', 1, False), ('bottom', 1, False)], 'wrong_prefix'),
        ('c07', 'three', [('top', .5, False), ('middle', 1, False)], 'early_switch'),
        ('c08', 'three', [('top', 1, True), ('middle', 1, False), ('bottom', 1, False)], 'reverse'),
        ('c09', 'ten', [('horizontal', 1, False), ('vertical', 1, False)], 'correct'),
        ('c10', 'ten', [('vertical', 1, False), ('horizontal', 1, False)], 'swapped'),
        ('c11', 'ten', [('horizontal', .5, False)], 'partial_first'),
    ]


def annotation(glyph, events, view):
    seq = [x[0] for x in events]
    finished = [sid for sid, progress, _ in events if progress == 1]
    unfinished = [sid for sid, progress, _ in events if progress < 1]
    result = dict(seen=sorted(seq), finished=sorted(finished), unfinished=sorted(unfinished))
    if view in {'last_frame', 'endpoints'} and events:
        result.update(order=seq if len(seq) == 1 else None,
                      directions={sid: 'unknown' for sid in seq},
                      early_switch=None if len(seq) == 1 else 'unknown',
                      status='unknown', first_error='unknown', error_type='unknown',
                      next='need_more_frames', target=None)
        # A static state can already exclude every valid history, although it
        # cannot tell which invalid history actually occurred.
        prefix = CANONICAL[glyph][:len(seq)]
        if set(seq) != set(prefix):
            result.update(status='invalid', error_type='order', next='stop_error')
        elif unfinished and unfinished != [prefix[-1]]:
            result.update(status='invalid', next='stop_error')
        return result
    early = next((i+1 for i in range(1, len(events)) if events[i-1][1] < 1), None)
    result.update(order=seq, directions={sid: 'reverse' if reverse else 'forward'
                                        for sid, _, reverse in events}, early_switch=early)
    errors = []
    for i, (sid, _, reverse) in enumerate(events):
        if sid != CANONICAL[glyph][i]:
            errors.append((i+1, 'order'))
        if reverse:
            errors.append((i+1, 'direction'))
        if early == i+1:
            errors.append((i+1, 'early_switch'))
    if errors:
        first, kind = min(errors)
        result.update(status='invalid', first_error=first, error_type=kind,
                      next='stop_error', target=None)
    else:
        result.update(status='valid', first_error=None, error_type='none')
        if unfinished:
            result.update(next='continue', target=unfinished[-1])
        elif len(seq) == len(CANONICAL[glyph]):
            result.update(next='done', target=None)
        else:
            result.update(next='start', target=CANONICAL[glyph][len(seq)])
    return result


def make_prompt(glyph, view, oracle=None):
    introduction = DESCRIPTIONS[glyph] + '\n指定规范顺序：' + ', '.join(CANONICAL[glyph])
    introduction += '。每个横从左向右，每个竖从上向下；当前笔完成后才能开始下一笔。\n'
    if view == 'oracle_state':
        introduction += '这是文字状态对照，不含图片。下面是准确的实际观测，请依据它判断与选动作：\n'
        introduction += json.dumps(oracle, ensure_ascii=False) + '\n'
    else:
        introduction += '第一张图片是完整目标参考，不属于时间序列。后续图片按时间从早到晚排列。'
        introduction += {'sampled_frames': '给出了从空白开始的每个四分之一笔进度帧。',
                         'last_frame': '只给过程的最后一帧，之前的历史没有给出。',
                         'endpoints': '只给空白首帧和末帧，中间过程没有给出。'}[view] + '\n'
    return introduction + '''请分清实际观测、规范判断和下一动作。错误笔顺也必须如实描述，不要用规范顺序代替实际顺序。
本小实验限定单色累积直线，只有这些实例，不存在擦除、隐形重描或额外笔；不需要判断笔尖接触状态。
仅凭静态终态无法知道笔内运动方向或多笔先后。没有证据时填unknown或null，不猜历史。
行动策略：有已确认错误就stop_error；历史或方向无法核验就need_more_frames；合法且当前笔未完成就continue；合法且当前笔已完成就start下一笔；合法且全部完成才done。这里只选择动作，不生成图像。
只输出一个JSON对象，包含以下键，不写解释：
seen：末帧可见实例ID数组；finished：末帧完整实例ID数组；unfinished：末帧部分完成实例ID数组。
order：实际开始出现的实例顺序数组；无法确定填null。空白为[]，只有一个可见实例时顺序可确定。
directions：各可见实例ID到forward/reverse/unknown的映射；方向需来自过程变化。
early_switch：上一笔未完成就开始新笔时，新笔是第几个出现的实例（从1计）；无此现象为null；历史不足为字符串unknown。
status：valid/invalid/unknown，表示已观察前缀是否满足顺序、方向及完成后换笔的规则。
first_error：首次违规发生在第几个实例（从1计）；无违规为null；无法确定为字符串unknown。
error_type：none/order/direction/early_switch/unknown，表示首错类型。
next：start/continue/done/stop_error/need_more_frames；target：start或continue对应的实例ID，其余为null。
'''


def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))


def build(output=OUT):
    output.mkdir(parents=True, exist_ok=True)
    inputs, labels, sources = [], [], []
    previews = []
    observation_keys = ['seen', 'finished', 'unfinished', 'order', 'directions', 'early_switch']
    for cid, glyph, events, kind in cases():
        folder = output/'images'/cid
        folder.mkdir(parents=True, exist_ok=True)
        frames = render(glyph, events)
        reference = render(glyph, [(sid, 1, False) for sid in CANONICAL[glyph]])[-1]
        reference.save(folder/'reference.png')
        frame_names = []
        for i, frame in enumerate(frames):
            name = f'images/{cid}/f{i:02d}.png'
            frame.save(output/name)
            frame_names.append(name)
        sources.append(dict(case_id=cid, glyph=glyph, construction=kind, events=events,
                            frame_count=len(frames), step_fraction=.25))
        views = ['sampled_frames']
        if events:
            views.append('last_frame')
        if kind in {'correct', 'swapped', 'reverse'}:
            views.append('endpoints')
        if cid in {'c01', 'c02', 'c05', 'c07', 'c08'}:
            views.append('oracle_state')
        for view in views:
            truth = annotation(glyph, events, view)
            oracle = {k: truth[k] for k in observation_keys} if view == 'oracle_state' else None
            chosen = (frame_names if view == 'sampled_frames' else
                      [frame_names[-1]] if view == 'last_frame' else
                      [frame_names[0], frame_names[-1]])
            images = [] if oracle is not None else [f'images/{cid}/reference.png'] + chosen
            sample_id = f'{cid}-{view}'
            inputs.append(dict(sample_id=sample_id, case_id=cid, view=view, glyph=glyph,
                               images=images, prompt=make_prompt(glyph, view, oracle)))
            labels.append(dict(sample_id=sample_id, expected=truth, construction=kind,
                               score_observation=oracle is None))
        if cid in {'c01', 'c02', 'c04', 'c05', 'c07'}:
            previews.append((cid, kind, frames))
    write_jsonl(output/'inputs.jsonl', inputs)
    write_jsonl(output/'labels.jsonl', labels)
    (output/'source_cases.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2)+'\n')
    sheet = Image.new('RGB', (224*4, 250*len(previews)), 'white')
    draw = ImageDraw.Draw(sheet)
    for row, (cid, kind, frames) in enumerate(previews):
        for col, index in enumerate(np.linspace(0, len(frames)-1, 4).round().astype(int)):
            sheet.paste(frames[index], (col*224, row*250+25))
            draw.text((col*224+5, row*250+6), f'{cid} {kind} f{index}', fill='black')
    sheet.save(output/'preview.png')
    print(f'{len(sources)} source cases; {len(inputs)} diagnostic inputs -> {output}')


if __name__ == '__main__':
    build()
