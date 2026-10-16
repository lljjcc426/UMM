"""Build short, event-preserving H1 questions for an image-level UMM."""
from __future__ import annotations

import itertools
import argparse
import json
import random

from h1_dataset import ROOT, CANONICAL, write_jsonl

NAMES = dict(top='上横', middle='中横', bottom='下横', horizontal='横', vertical='竖')


def names(ids):
    return '、'.join(NAMES[x] for x in ids) if ids else '无'


def build():
    source = ROOT/'data/h1/pilot_v1'
    output = ROOT/'data/h1/umm_pilot_v1'
    output.mkdir(parents=True, exist_ok=True)
    original = {r['sample_id']:r for r in map(json.loads,(source/'inputs.jsonl').read_text().splitlines())}
    truths = {r['sample_id']:r for r in map(json.loads,(source/'labels.jsonl').read_text().splitlines())}
    sources = {r['case_id']:r for r in json.loads((source/'source_cases.json').read_text())}
    inputs, labels = [], []
    rng = random.Random(20261016)

    def row(cid):
        return original[cid+'-sampled_frames']

    def truth(cid):
        return truths[cid+'-sampled_frames']['expected']

    def frames(cid, indices):
        return [f'images/{cid}/f{i:02d}.png' for i in indices]

    def add(cid, task, prompt, images, correct, alternatives, meaning):
        distractors = list(dict.fromkeys(x for x in alternatives if x != correct))
        rng.shuffle(distractors)
        choices = distractors[:3]
        position = len(inputs) % 4
        choices.insert(position, correct)
        assert len(choices) == 4
        prompt += '\n'+'\n'.join(f'{letter}. {text}' for letter,text in zip('ABCD',choices))
        prompt += '\n只回答一个选项字母A、B、C或D，不写解释。'
        sid = cid+'-'+task
        inputs.append(dict(sample_id=sid,case_id=cid,glyph=row(cid)['glyph'],view=task,
                           images=['../pilot_v1/'+p for p in images],prompt=prompt,options=choices))
        labels.append(dict(sample_id=sid,expected={'answer':'ABCD'[position]},score_fields=['answer'],
                           expected_text=correct,semantic_target=meaning,
                           construction=truths[cid+'-sampled_frames']['construction']))

    for cid in ['c00','c01','c02','c03','c04','c06','c07','c11']:
        glyph=row(cid)['glyph']; ids=CANONICAL[glyph]
        alternatives=[names(s) for n in range(len(ids)+1) for s in itertools.combinations(ids,n)]
        seen=[s for s in ids if s in truth(cid)['seen']]
        add(cid,'seen_mc','观察当前图。按线条所在位置区分上横、中横、下横；横线与竖线按方向区分。部分线条也算已出现。实际可见哪些线条？',
            row(cid)['images'][-1:],names(seen),alternatives,seen)

    for cid in ['c01','c02','c03','c04','c07','c11']:
        glyph=row(cid)['glyph']; ids=CANONICAL[glyph]
        def state(finished,unfinished):
            return '完整：'+names([s for s in ids if s in finished])+'；未完成：'+names([s for s in ids if s in unfinished])
        states=([([],['top']),(['top'],[]),(['top'],['middle']),(['middle'],['top']),
                 (['top','middle','bottom'],[]),([],[])] if glyph=='three' else
                [([],['horizontal']),(['horizontal'],[]),(['horizontal','vertical'],[]),([],[])])
        correct=state(truth(cid)['finished'],truth(cid)['unfinished'])
        add(cid,'completion_mc','第一张是完整目标参考，第二张是当前实际画面。比较端点和长度，哪些线条已经完整、哪些只写了部分？完全没有出现的线条不列入。',
            [row(cid)['images'][0],row(cid)['images'][-1]],correct,[state(*x) for x in states],
            {k:truth(cid)[k] for k in ['finished','unfinished']})

    for cid in ['c04','c05','c09','c10']:
        total=0; indices=[0]
        for _,progress,_ in sources[cid]['events']:
            total+=round(progress*4);indices.append(total)
        seq=truth(cid)['order']; glyph=row(cid)['glyph']
        alternatives=([names(x) for x in itertools.permutations(CANONICAL[glyph])]
                      if glyph=='three' else ['横、竖','竖、横','横、横','无法确定'])
        add(cid,'order_mc','这些图片全部是实际过程，按时间从早到晚排列，第一张为空白。只根据各条线首次出现的先后，实际顺序是什么？不要用常规笔顺替代实际过程。',
            frames(cid,indices),names(seq),alternatives,seq)
        first=truth(cid)['first_error']
        correct='顺序符合规范' if first is None else f'首次顺序错误在第{first}笔'
        add(cid,'first_error_mc','这些图片按时间从早到晚排列，第一张为空白。指定规范顺序为'+names(CANONICAL[glyph])+'。只评价各笔首次出现的顺序，第一笔序号为1。第一次顺序错误在哪里？',
            frames(cid,indices),correct,['顺序符合规范','首次顺序错误在第1笔','首次顺序错误在第2笔','无法确定'],first)

    for cid,correct in [('c02','从左向右'),('c08','从右向左')]:
        add(cid,'direction_mc','两张图按时间从早到晚展示同一条横线增长。黑线实际向哪个方向延伸？',
            frames(cid,[1,2]),correct,['从左向右','从右向左','从上向下','无法确定'],correct)

    for cid,before,after,correct in [('c03',4,5,'上一笔已写完，再开始新笔'),('c07',2,3,'上一笔未写完，就开始新笔')]:
        add(cid,'early_switch_mc','第一张是完整目标参考，第二、三张是连续的实际过程。观察第三张新出现的线条：换笔时，上一笔是否已经写完？',
            [row(cid)['images'][0]]+frames(cid,[before,after]),correct,
            ['上一笔已写完，再开始新笔','上一笔未写完，就开始新笔','尚未开始新笔','无法确定'],truth(cid)['early_switch'])

    states={
        'c01':'只开始上横，从左向右写了一半，其他笔尚未开始。',
        'c02':'上横从左向右已经写完，其他笔尚未开始。',
        'c05':'先完整写上横，再完整写下横，最后完整写中横；各笔均从左向右。',
        'c07':'上横从左向右只写一半就开始中横；中横写完，仍未补完上横。',
        'c08':'先完整写上横，但方向从右向左；随后中横、下横从左向右写完。',
    }
    for cid,state in states.items():
        correct={'continue':'继续上横','start':'开始中横','stop_error':'停止并处理已发生的错误'}[truth(cid)['next']]
        add(cid,'oracle_action_mc','以下实际状态准确，不需要看图：'+state+
            '规则：三应按上横、中横、下横书写，每笔从左向右，写完当前笔才换笔。已确认违规就停止；合法半笔就继续；合法完整前缀就开始下一笔；合法整字才结束。现在应当做什么？',
            [],correct,['继续上横','开始中横','结束，整字已经正确完成','停止并处理已发生的错误'],
            {k:truth(cid)[k] for k in ['next','target']})

    for cid in ['c04','c09']:
        alternatives=(['上横、中横、下横','上横、下横、中横','下横、中横、上横','无法从终态确定']
                      if row(cid)['glyph']=='three' else ['横、竖','竖、横','同时出现','无法从终态确定'])
        add(cid,'static_unknown_mc','只提供一张最终静态图，没有中间过程。实际书写时，各笔首次出现的顺序是什么？',
            row(cid)['images'][-1:],'无法从终态确定',alternatives,None)

    write_jsonl(output/'inputs.jsonl',inputs)
    write_jsonl(output/'labels.jsonl',labels)
    print(f'{len(inputs)} UMM diagnostic inputs; maximum {max(len(r["images"]) for r in inputs)} images')


def build_position_control():
    source=ROOT/'data/h1/umm_pilot_v1'
    output=ROOT/'data/h1/umm_position_control_v1'
    output.mkdir(parents=True,exist_ok=True)
    inputs=[json.loads(s) for s in (source/'inputs.jsonl').read_text().splitlines()]
    labels=[json.loads(s) for s in (source/'labels.jsonl').read_text().splitlines()]
    for row,label in zip(inputs,labels):
        previous=row['options']
        row['options']=previous[-1:]+previous[:-1]
        question=row['prompt'].split('\nA. ',1)[0]
        row['prompt']=question+'\n'+'\n'.join(f'{k}. {v}' for k,v in zip('ABCD',row['options']))
        row['prompt']+='\n只回答一个选项字母A、B、C或D，不写解释。'
        label['expected']['answer']='ABCD'[('ABCD'.index(label['expected']['answer'])+1)%4]
    write_jsonl(output/'inputs.jsonl',inputs)
    write_jsonl(output/'labels.jsonl',labels)
    print(f'{len(inputs)} inputs with rotated option positions -> {output}')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--position-control',action='store_true')
    args=p.parse_args()
    build_position_control() if args.position_control else build()
