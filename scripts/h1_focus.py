"""Build a bounded follow-up separating visual questions from output load."""
from __future__ import annotations

import json
from h1_dataset import ROOT, DESCRIPTIONS, CANONICAL, write_jsonl


def build():
    source = ROOT/'data/h1/pilot_v1'
    output = ROOT/'data/h1/focused_v1'
    output.mkdir(parents=True, exist_ok=True)
    original = {r['sample_id']: r for r in map(json.loads, (source/'inputs.jsonl').read_text().splitlines())}
    truths = {r['sample_id']: r for r in map(json.loads, (source/'labels.jsonl').read_text().splitlines())}
    inputs, labels = [], []

    def add(cid, task, prompt, images, expected):
        base = original[cid+'-sampled_frames']
        sid = cid+'-'+task
        inputs.append(dict(sample_id=sid, case_id=cid, glyph=base['glyph'], view=task,
                           prompt=prompt, images=['../pilot_v1/'+p for p in images]))
        labels.append(dict(sample_id=sid, expected=expected, score_fields=list(expected),
                           construction=truths[cid+'-sampled_frames']['construction']))

    # Same final state, question and model; only the reference-image condition changes.
    for cid in ['c00','c01','c02','c07']:
        row = original[cid+'-sampled_frames']
        truth = truths[cid+'-sampled_frames']['expected']
        question = DESCRIPTIONS[row['glyph']]+'画面上实际可见哪些实例？部分出现也算可见。只输出JSON：{"seen":[实例ID]}。空白填[]。'
        add(cid, 'seen_no_reference', question, row['images'][-1:], {'seen':truth['seen']})
        add(cid, 'seen_with_reference', '第一张是完整目标参考，第二张是实际当前画面。只回答第二张。'+question,
            [row['images'][0],row['images'][-1]], {'seen':truth['seen']})

    for cid in ['c01','c02','c03','c07']:
        row = original[cid+'-sampled_frames']
        truth = truths[cid+'-sampled_frames']['expected']
        question = ('第一张是完整目标参考，第二张是实际当前画面。'+DESCRIPTIONS[row['glyph']]+
                    '对照参考，第二张中哪些笔完整、哪些只画了部分？完全未出现的笔不要列入。'
                    '只输出JSON：{"finished":[完整实例ID],"unfinished":[部分实例ID]}。')
        add(cid, 'completion_only', question, [row['images'][0],row['images'][-1]],
            {k:truth[k] for k in ['finished','unfinished']})

    for cid in ['c04','c05','c09','c10']:
        row = original[cid+'-sampled_frames']
        prompt = (DESCRIPTIONS[row['glyph']]+'图片全部是实际过程，按时间从早到晚排列，第一张为空白。'
                  '按各笔首次出现的时间，列出实际实例顺序。只列每笔一次，不列帧编号。不要按常识改正错误顺序。'
                  '只输出JSON：{"order":[实例ID]}。')
        add(cid, 'order_only', prompt, row['images'][1:],
            {'order':truths[cid+'-sampled_frames']['expected']['order']})

    for cid, direction in [('c02','forward'),('c08','reverse')]:
        row = original[cid+'-sampled_frames']
        prompt = ('这些图片按时间从早到晚展示同一条横线逐渐出现。它从左向右还是从右向左延伸？'
                  '只输出JSON：{"direction":"forward"}表示左向右，或{"direction":"reverse"}表示右向左。')
        add(cid, 'direction_only', prompt, row['images'][1:6], {'direction':direction})

    for cid in ['c01','c02','c05','c07','c08']:
        row = original[cid+'-sampled_frames']
        truth = truths[cid+'-sampled_frames']['expected']
        state = {k:truth[k] for k in ['seen','finished','unfinished','order','directions','early_switch']}
        common = (DESCRIPTIONS[row['glyph']]+'指定顺序：'+', '.join(CANONICAL[row['glyph']])+
                  '。各笔方向应为forward；当前笔完成后才能开始下一笔。以下是准确的实际状态：'+
                  json.dumps(state, ensure_ascii=False)+'\n')
        add(cid, 'oracle_judgment', common+
            '以上已发生过程是否违反任一规则？只输出JSON：{"status":"valid"}或{"status":"invalid"}。',
            [], {'status':truth['status']})
        add(cid, 'oracle_action', common+
            '下一动作按这些规则选：已违反任一规则则stop_error；合法半笔则continue当前笔；合法完整前缀则start下一笔；合法整字则done。'
            '只输出JSON，必须同时包含next和target两个键；target是start/continue的实例ID，其余为null。',
            [], {k:truth[k] for k in ['next','target']})

    for cid in ['c04','c09']:
        row = original[cid+'-sampled_frames']
        add(cid, 'static_order_unknown', DESCRIPTIONS[row['glyph']]+
            '只有一张最终静态图，没有中间过程。能确定这些笔实际先后出现的顺序吗？'
            '只输出JSON：{"order":null}表示无法确定；有证据才填写实例ID顺序数组。',
            row['images'][-1:], {'order':None})

    write_jsonl(output/'inputs.jsonl', inputs)
    write_jsonl(output/'labels.jsonl', labels)
    print(f'{len(inputs)} focused diagnostic inputs -> {output}')


if __name__ == '__main__':
    build()
