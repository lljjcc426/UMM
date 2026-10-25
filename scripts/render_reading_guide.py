"""Organize existing reviews by research question and verified conference scope."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'data/reading_guide_2026-10-25.json'
GROUPS = {
    'confirmed_conference': '已核会议论文与官方接收条目',
    'author_acceptance_claim': '作者声明录用，未另核正式目录',
    'other_track': 'Workshop、Findings、Demo与关联短版',
}


def cell(value):
    return str(value).replace('|', r'\|').replace('\n', '<br>')


def main():
    cfg = json.loads(CONFIG.read_text())
    catalog = json.loads((ROOT / 'data/literature.json').read_text())
    acceptance = {r['id']: r for r in json.loads(
        (ROOT / 'data/reading_acceptance_2026-10-20.json').read_text())['records']}
    papers = {r['id']: r for r in catalog if r['record_type'] != 'resource'}
    topics = {r['id']: r for r in cfg['topics']}
    if set(cfg['primary_topic_by_id']) != set(papers):
        raise ValueError('Topic assignments must cover the paper catalog exactly.')
    complete = {i for i, r in acceptance.items()
                if r.get('full_three_pass_completed') is True and i in papers}
    deferred = set(cfg['deferred_paper_ids'])
    active = set(papers) - complete - deferred
    folder = ROOT / 'docs/reading'
    folder.mkdir(exist_ok=True)
    records = []
    for ident, r in papers.items():
        conf = cfg['conference_assignments'].get(ident)
        records.append(dict(
            id=ident, title=r['title'], primary_topic=cfg['primary_topic_by_id'][ident],
            core_reading_completed=ident in complete,
            followup='deferred_by_user' if ident in deferred else
                     'active' if ident in active else 'completed',
            note_path=r['review_path'], conference=conf,
            source_urls=list(dict.fromkeys(r['source_urls'] +
                             (conf or {}).get('additional_sources', []))),
        ))
    done = [r for r in records if r['core_reading_completed']]
    counts = {conf: {g: sum(r['conference'] is not None and
                           r['conference']['conference'] == conf and
                           r['conference']['group'] == g for r in done)
                     for g in GROUPS} for conf in cfg['priority_conferences']}
    topic_counts = Counter(r['primary_topic'] for r in done)
    summary = dict(
        date=cfg['date'], catalog_papers=len(papers), completed_papers=len(done),
        deferred_paper_ids=cfg['deferred_paper_ids'], active_incomplete_paper_ids=sorted(active),
        resource_protocol_reviews=27, priority_conference_counts=counts,
        priority_confirmed_conference_papers=sum(v['confirmed_conference'] for v in counts.values()),
        primary_topic_counts=dict(topic_counts),
        scope='组织已有阅读，不新增论文完成或模型复现；各论文实际版本见逐篇笔记。',
    )
    (ROOT / 'data/reading_organization_2026-10-25.json').write_text(
        json.dumps(dict(summary=summary, records=records), ensure_ascii=False, indent=2) + '\n')

    def title_link(r):
        return f'[{cell(r["id"] + " · " + r["title"])}](../reviews/{r["id"]}.md)'

    def venue(r):
        c = r['conference']
        return f'{c["conference"]} {c["year"]} · {c["track"]}' if c else '其他会议／期刊／预印本'

    for conf in cfg['priority_conferences']:
        lines = [f'# {conf}：已分析论文', '', '[阅读总览](README.md) · [跨论文分析](synthesis.md)', '',
                 '依据已有逐篇核查整理。会议归属与实际阅读版本分别记录；下列论文均已完成所记录范围的核心阅读，完整附录/正式修订/代码缺项以原笔记为准。', '']
        for group, label in GROUPS.items():
            rows = [r for r in done if r['conference'] and
                    r['conference']['conference'] == conf and r['conference']['group'] == group]
            lines += [f'## {label}（{len(rows)}篇）', '']
            if not rows:
                lines += ['本库暂无此类已完成记录。', '']
                continue
            lines += ['| 年份／类型 | 论文与阅读笔记 | 研究主题 | 归属依据 |', '| --- | --- | --- | --- |']
            for r in sorted(rows, key=lambda x: (-x['conference']['year'], x['primary_topic'], x['id'])):
                c = r['conference']
                urls = c.get('additional_sources') or r['source_urls']
                # Prefer an existing official publication/meeting link when one is recorded.
                official = next((u for u in urls if any(d in u for d in
                    ('openaccess.thecvf.com', 'proceedings.iclr.cc', 'proceedings.mlr.press',
                     'proceedings.neurips.cc', 'papers.nips.cc', 'iclr.cc/Downloads'))), urls[0])
                lines.append(f'| {c["year"]} · {cell(c["track"])} | {title_link(r)} | '
                             f'[{topics[r["primary_topic"]]["title"]}]({r["primary_topic"]}.md) | '
                             f'[来源]({official})；{cell(c["evidence"])} |')
            lines.append('')
        (folder / f'{conf.lower()}.md').write_text('\n'.join(lines).rstrip() + '\n')

    for topic_id, t in topics.items():
        rows = [r for r in done if r['primary_topic'] == topic_id]
        # Put confirmed target conferences first, then retain all other analyzed research.
        rows.sort(key=lambda r: (0 if r['conference'] and r['conference']['group'] ==
                                'confirmed_conference' else 1, r['id']))
        lines = [f'# {t["title"]}', '', '[阅读总览](README.md) · [跨论文分析](synthesis.md)', '',
                 t['question'], '', f'本主题主分类包含{len(rows)}篇已完成核心阅读的论文。跨主题方法在综合分析中关联；每篇在主题计数中只出现一次。', '',
                 '| 论文与阅读笔记 | 来源范围 |', '| --- | --- |']
        lines += [f'| {title_link(r)} | {cell(venue(r))} |' for r in rows]
        lines += ['', '方法、数据、结果、消融、限制和可检验问题均在所链接的逐篇笔记中。索引排序只服务当前研究重点。', '']
        (folder / f'{topic_id}.md').write_text('\n'.join(lines))

    lines = ['# 已分析论文：会议索引与研究脉络', '',
             '当前重点为CVPR、ICCV、ECCV、NeurIPS、ICLR、ICML。先用研究问题比较方法，再按会议查找具体论文。', '',
             f'主目录{len(papers)}篇论文／研究，{len(done)}篇已完成所记录范围的核心阅读。其余{len(deferred)}篇已按用户要求停止跟进；未计作完成。27项资源公开协议审查另列。', '',
             '**先看[跨论文分析与20篇核心对照](synthesis.md)**，再进入会议或主题索引。所有单篇分析均可从下表点击到达。', '',
             '## 六个会议', '',
             '| 会议 | 已核会议论文／官方接收 | 作者声明录用 | Workshop／Findings／Demo等 |',
             '| --- | ---: | ---: | ---: |']
    for conf, c in counts.items():
        lines.append(f'| [{conf}]({conf.lower()}.md) | {c["confirmed_conference"]} | '
                     f'{c["author_acceptance_claim"]} | {c["other_track"]} |')
    total = summary['priority_confirmed_conference_papers']
    lines += ['', f'已核会议归属共{total}篇；该列包含NeurIPS Datasets and Benchmarks及已核官方接收条目，具体类型逐条列出。ECCV2026的EvoTok为官方初步名单，出版检查仍保留。正式会议身份不表示本库读过其所有终版差异。', '',
              '## 按研究问题查阅', '', '| 主题 | 已完成论文 | 研究用途 |', '| --- | ---: | --- |']
    for ident, t in topics.items():
        lines.append(f'| [{t["title"]}]({ident}.md) | {topic_counts[ident]} | {t["question"]} |')
    lines += ['', '七个主分类合计覆盖全部已完成论文；其他期刊、会议和预印本作为直接前作或机制背景保留。会议筛选服务阅读优先级，研究结论仍依据方法和实验。', '',
              '## 当前范围与维护', '',
              f'- [停止跟进的{len(deferred)}篇及原因](scope.md)：' + '、'.join(cfg['deferred_paper_ids']) + '。',
              '- [全部逐篇笔记](../reviews/README.md)与[论文／资源验收台账](../evidence/reading_ledger_2026-10-19.md)。',
              '- [研究进展](../project/STATUS.md)、[研究判断](../project/DECISIONS.md)与[实验计划](../project/EXPERIMENTS.md)。',
              '- [历史批次](../project/history/reading_updates_2026-10-19_to_25.md)保存原来的阅读流水，不作为当前待办。',
              '- 配置为[data/reading_guide_2026-10-25.json](../../data/reading_guide_2026-10-25.json)；执行`python scripts/render_reading_guide.py`更新索引。', '',
              '## 会议归属容易混淆的记录', '',
              '以下论文保留原有研究分析，未因模板、相关前作或二手标签而放进六会议主表。', '',
              '| 记录 | 本次组织规则 |', '| --- | --- |']
    for ident, reason in cfg['excluded_conference_mentions'].items():
        r = papers[ident]
        lines.append(f'| [{ident} · {cell(r["title"])}](../reviews/{ident}.md) | {reason} |')
    (folder / 'README.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
