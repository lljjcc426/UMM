"""Render source-scoped reading notes and an honest completion ledger.

No retrieval result is used to upgrade a reading status. Curated review JSON is
edited only after reading the cited source sections; generated notes preserve gaps.
"""
from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]


def main():
    catalog = json.loads((ROOT / 'data/literature.json').read_text(encoding='utf-8'))
    by_id = {r['id']: r for r in catalog}
    reviews = []
    for name in ('critical_reviews_2026-10-19.json', 'foundation_reviews_2026-10-19.json'):
        reviews.extend(json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))['records'])
    acceptance_file = ROOT / 'data/reading_acceptance_2026-10-20.json'
    acceptance = {r['id']: r for r in json.loads(acceptance_file.read_text(encoding='utf-8'))['records']} if acceptance_file.exists() else {}
    folder = ROOT / 'docs/reviews'
    folder.mkdir(exist_ok=True)
    index = ['# 第二轮原文阅读与批判分析', '',
             '以下笔记按实际阅读范围记录。相关章节核查不等于三遍完整精读；没有进行模型复现。未填完的实验条件与消融明确保留，不能计作全部完成。', '',
             '[逐条完成台账](../evidence/reading_ledger_2026-10-19.md) · [理论与实验迁移](../evidence/foundations_and_transfer_2026-10-19.md)', '',
             '| 编号 | 论文 | 核查范围 |', '| --- | --- | --- |']
    for d in reviews:
        r = by_id[d['id']]
        sources = '\n'.join(f'- [原始来源 {i+1}]({url})' for i, url in enumerate(r['source_urls']))
        accepted = acceptance.get(d['id'])
        complete = accepted and accepted.get('full_three_pass_completed') is True
        completion = ('核心三遍阅读与五项书面理解检查已完成；未独立复现。' if complete else
                      '五项阅读检查已逐项记录；完整三遍尚未逐条确认，未独立复现。' if accepted else
                      '相关内容已经阅读，完整三遍验收尚未完成；未独立复现。')
        text = f'''# {r['id']} · {r['title']}

论文标题：{r['title']}

发表会议/年份：{d['venue']}

核查日期：{d['checked_on']}

已读范围：{d['sections_read']}

阅读层级：{d['reading_status']}；{completion}

{sources}

## 第一遍：三句话定位

已有困难：{d['motivation']}

作者提出：{d['contribution']}

目前证据：{d['results']}

## 1. 研究问题（Problem）

{d['problem']}

## 2. 现有方法不足（Motivation）

{d['motivation']}

## 3. 核心创新（Contribution）

{d['contribution']}

## 4. 方法流程（Method）

输入与输出：{d['input_output']}

方法框架与模型结构：{d['architecture']}

数据集与分布：{d['data']}

## 5. 实验结果（Experiments）

主要基线：{d['baselines']}

关键指标：{d['metrics']}

实验条件：{d['experimental_conditions']}

结果及解释：{d['results']}

消融实验：{d['ablation']}

所有分数均为作者报告；条件、版本和样本数不同的数字不得直接排名。

## 6. 局限与疑问（Limitations）

{d['limitations']}

需继续追问：该局限是否已被其他研究解决？当前笔记的假设在未完成追引与对照前不计作新课题。

## 7. 我的思考（Insights）

优势假设（本仓库分析，尚未验证）：{d['advantage_hypothesis']}

可证伪实验（建议方案，尚未运行）：{d['falsification']}

这两项分别回答“在什么任务/分布/指标下有优势”与“如何验证”；上文问题、动机、贡献回答前面三个研究分析问题。

## 8. 一句话总结

{d['problem']}——作者采用{d['contribution']}；可采信范围以第5–6项为界。

## 研究写作学习

{d['writing_lesson']}

写作时按问题定义→现有不足→机制假设→模块→对应实验组织 Introduction 与 Method；Claim 必须包含任务、比较对象与条件；Limitations 区分作者已说明的限制和本笔记提出的待测问题。

## 三遍阅读验收

| 检查项 | 当前状态 |
| --- | --- |
| 不看原文，两分钟解释问题与动机 | 尚未进行独立口述验收；笔记已给出解释 |
| 指着框架图解释输入、模块和输出 | 已记录文字流程；除明确注明的视觉核对外，不声称已逐图验收 |
| 解释关键创新及作用 | 已按已读范围分析；待核字段仍以原文为准 |
| 解释一张主表和一组消融 | 见第5项；若标注待核，则该项未完成 |
| 提出两个有依据的问题 | 见局限和可证伪实验；仍需相关工作追引 |

没有用统一的“5/5”掩盖上述待完成项。重建论文全部符号、补齐附录/代码条件及独立复现属于后续不同验收层级。
'''
        if accepted:
            text = text[:text.index('## 三遍阅读验收')]
            text += '## 三遍阅读验收\n\n逐项记录的书面理解检查；计时口试和模型复现另列，不额外作为阅读完成的门槛。\n\n'
            for check in accepted['checks']:
                text += f"### {check['criterion']}\n\n{check['answer']}\n\n证据：{check['evidence']}\n\n"
            text += f"复核边界：{accepted['boundary']}\n"
        (folder / f'{r["id"]}.md').write_text(text, encoding='utf-8')
        index.append(f'| {r["id"]} | [{r["title"]}]({r["id"]}.md) | {d["sections_read"]} |')
    (folder / 'README.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    review_map = {r['id']: r for r in reviews}
    ledger = ['# 全目录逐条阅读台账', '',
              f'主目录 {len(catalog)} 条，本批有 {len(reviews)} 份结构化笔记。此表列出全部记录，不将来源访问、摘要核对、章节核对与完整三遍精读混为一项。', '',
              '核心三遍完成需逐条核问题/方法/框架图、主表/消融及有依据的批判分析，并记录五项书面检查。计时口试、完整代码审查和独立复现另列；没有自动把模板填齐计为完成。', '',
              '| ID | 记录 | 原目录核查状态 | 本批笔记 | 三遍验收 |', '| --- | --- | --- | --- | --- |']
    for r in catalog:
        note = f'[结构化分析](../reviews/{r["id"]}.md)' if r['id'] in review_map else '本批未新增逐篇精读'
        done = ('核心三遍与五项检查完成' if acceptance.get(r['id'], {}).get('full_three_pass_completed') is True else
                '五项检查已记录；三遍待确认' if r['id'] in acceptance else '未完成')
        ledger.append(f'| {r["id"]} | {r["title"].replace("|", "/")} | {r["verification"]} | {note} | {done} |')
    (ROOT / 'docs/evidence/reading_ledger_2026-10-19.md').write_text('\n'.join(ledger) + '\n', encoding='utf-8')
    as_of = max(r.get('last_updated') or r.get('checked_on') or '2026-10-19' for r in catalog)
    report = dict(date=as_of, catalog_entries=len(catalog), curated_reviews=len(reviews),
                  by_verification=dict(Counter(r['verification'] for r in catalog)),
                  by_review_depth=dict(Counter(r['reading_status'] for r in reviews)),
                  three_pass_acceptance_completed=sum(r.get('full_three_pass_completed') is True for r in acceptance.values()),
                  five_item_written_checks_recorded=len(acceptance), independently_reproduced=0,
                  warning='Source access, section review, complete three-pass reading and reproduction are distinct.')
    (ROOT / 'data/reading_progress_2026-10-19.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
