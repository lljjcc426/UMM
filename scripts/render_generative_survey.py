"""Render the supplementary generative-model survey; preserve the main catalog."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/discovery/generative_models_2026-10-30.json"
OUT = ROOT / "docs/generative"
TOPICS = {
    "diffusion": "扩散、score与采样",
    "flow_consistency": "Flow Matching、Rectified Flow、Consistency与Flow Map",
    "representation": "生成表征、RAE与像素空间",
    "distillation_alignment": "蒸馏、分布匹配与偏好对齐",
    "drifting_theory": "Drifting原理、理论与前史",
    "drifting_methods": "Drifting训练方法与算力分配",
    "video_policy": "视频、世界模型与机器人策略",
    "language_audio": "离散语言、语音与音频",
    "domain_geometry": "物理、几何、医学与其他领域",
}
LEVELS = {
    "targeted_sections": "重点章节核读",
    "body_excerpts": "正文片段选读",
    "abstract_screened": "摘要筛选",
}


def anchor(record):
    return "paper-" + record["key"].replace(".", "-")


def link(record):
    return f'{record["topic"]}.md#{anchor(record)}'


def venue_text(record):
    values = []
    for item in record["venue_evidence"]:
        tag = "正式论文集" if item["evidence"] == "formal_proceedings" else "官方目录"
        label = f'{item["venue"]} {item["year"]}（{tag}）'
        values.append(f'[{label}]({item["url"]})')
    return "；".join(values) or "会议/期刊归属未由本轮官方来源确认；作者自报见下文。"


def render():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = data["records"]
    OUT.mkdir(parents=True, exist_ok=True)
    for topic, title in TOPICS.items():
        selected = [r for r in rows if r["topic"] == topic]
        text = [f"# {title}", "", "[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)", "",
                f"本页 {len(selected)} 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。", ""]
        for row in selected:
            text += [f'<a id="{anchor(row)}"></a>', "", f'## {row["title"]}', ""]
            authors = row["authors"]
            author_text = "、".join(authors[:4]) + (f" 等{len(authors)}人" if len(authors) > 4 else "")
            text += [f'作者：{author_text}。标识：`{row["arxiv_id"] or row["key"]}`。首次公开：{row["published"][:10]}；所查版本更新：{(row["updated"] or "未提供")[:10]}。', "",
                     f'阅读层级：**{LEVELS[row["reading_level"]]}**。范围：{row["reading_scope_zh"]}', "",
                     f'来源归属：{venue_text(row)}', "", f'方法：{row["method_zh"]}', "", f'限制与判断：{row["limitations_zh"]}', ""]
            evidence = row["reading_evidence"]
            if evidence.get("finding"):
                text += [f'本轮核读所得：{evidence["finding"]}', ""]
            if evidence.get("local_extracted_line_starts"):
                positions = ", ".join(map(str, evidence["local_extracted_line_starts"]))
                text += [f'片段定位：本地HTML提取文本起始行 {positions}；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。', ""]
            if row["author_reported_comment"] or row["author_reported_journal_ref"]:
                claim = "；".join(x for x in [row["author_reported_comment"], row["author_reported_journal_ref"]] if x)
                text += [f'作者元数据备注（与独立核实分开）：{claim}', ""]
            text += ["原始来源：" + " · ".join(f'[来源{i}]({u})' for i, u in enumerate(row["sources"], 1)), ""]
        (OUT / f"{topic}.md").write_text("\n".join(text), encoding="utf-8")

    counts = Counter(r["reading_level"] for r in rows)
    official = [r for r in rows if r["venue_evidence"]]
    formal = sum(any(v["evidence"] == "formal_proceedings" for v in r["venue_evidence"]) for r in rows)
    text = ["# 扩散、Flow与Drifting生成模型专题", "", "检索截止：2026-10-30。用户已撤销数量上限。本轮以Drifting机制和关联生成路线为边界，按引用、标题、摘要及官方会议来源扩展，新增 **142项** 去重补充记录。", "",
            "**[综合分析：机制、理论、实验与UMM](synthesis.md)** · **[检索与停止边界](search_scope.md)** · [本轮文件变更](changes_2026-10-30.md)", "",
            "142项中，10项完成重点章节核读，31项完成正文片段选读，101项完成摘要筛选。这里没有将142项计为全文精读完成。原目录360条、327篇核心完成及6篇停止追取的状态维持原记录；旧论文通过链接复用。", "",
            "## 阅读覆盖", "", "| 范围 | 数量 | 支持的结论 |", "| --- | ---: | --- |"]
    for level in LEVELS:
        scope = {"targeted_sections": "可对指定公式、假设、实验与反例作讨论；未宣称全文逐行复核", "body_excerpts": "支持具体片段的方法判断；证明及全部实验仍可能未覆盖", "abstract_screened": "支持问题归类和初步方法概括；数值及理论为作者声明"}[level]
        text.append(f"| {LEVELS[level]} | {counts[level]} | {scope} |")
    text += ["", "## 按问题阅读", "", "| 主题 | 新增项数 |", "| --- | ---: |"]
    for topic, title in TOPICS.items():
        text.append(f'| [{title}]({topic}.md) | {sum(r["topic"] == topic for r in rows)} |')
    text += ["", "## 六个优先会议的来源入口", "", f"新增记录中，{len(official)}项定位到官方目录或正式论文集，其中{formal}项直接定位正式论文集页/PDF。其余官方目录记录未据此自动认定主会轨道、报告形式或奖项。作者在arXiv备注中的接收声明另存；未确认的会议归属保持未确认。", "",
             "| 论文 | 官方来源 | 本轮阅读 |", "| --- | --- | --- |"]
    order = {name: i for i, name in enumerate(["CVPR", "ICCV", "ECCV", "NeurIPS", "ICLR", "ICML"])}
    for row in sorted(official, key=lambda r: (min(order.get(v["venue"], 99) for v in r["venue_evidence"]), r["published"], r["title"])):
        text.append(f'| [{row["title"]}]({link(row)}) | {venue_text(row)} | {LEVELS[row["reading_level"]]} |')
    text += ["", "## 预印本与尚未核实的会议身份", "", "重要预印本单列于[预印本及未核实身份索引](preprints.md)，包括W-Flow、score联系、Companion-Elliptic、DriftWorld、GR00T技术报告等。未找到本轮官方证据表示身份未确认，不能推断已经证明未被接收；作者自报期刊另列。"]
    text += ["", "## 复用原目录中的基础文献", "", "下列卡片为此前已有阅读；本轮复用，未重新累计为新增或重新宣称完成全篇核读。CFG的workshop归属须与主会区分。", "",
             "| 文献 | 已有记录 |", "| --- | --- |",
             "| DDPM、Score SDE、LDM、DiT | [G001](../reviews/G001.md) · [G002](../reviews/G002.md) · [G003](../reviews/G003.md) · [G004](../reviews/G004.md) |",
             "| Flow Matching、Rectified Flow、Consistency、DPM-Solver | [G005](../reviews/G005.md) · [G006](../reviews/G006.md) · [G007](../reviews/G007.md) · [G008](../reviews/G008.md) |",
             "| CFG、EDM | [G026](../reviews/G026.md) · [G027](../reviews/G027.md) |",
             "| MeanFlow、Improved MeanFlow | [E01](../reviews/E01.md) · [E02](../reviews/E02.md) |",
             "| Diffusion Forcing、Self Forcing、Consistency Policy、Discrete Flow Matching | [G030](../reviews/G030.md) · [D05](../reviews/D05.md) · [E03](../reviews/E03.md) · [E04](../reviews/E04.md) |", "",
             "## 数据与维护", "", "[机器可读清单](../../data/discovery/generative_models_2026-10-30.json) · [检索审计](../../data/discovery/generative_search_2026-10-30.json) · [渲染脚本](../../scripts/render_generative_survey.py)", "",
             "本目录README、9个主题页和预印本索引由补充JSON生成；综合分析、检索边界与变更说明手工维护。运行 `python scripts/render_generative_survey.py` 只更新本专题生成页。", "",
             "文献调研的费用与GPU使用为0，没有训练、推理或数据集下载。文献中的分数和速度均为作者报告。2026-10-30用户另行批准发布到GitHub main，按仓库PR流程交付；见[发布与文件变更记录](changes_2026-10-30.md)。专题不改变P0有限结项及P1实验授权。", ""]
    (OUT / "README.md").write_text("\n".join(text), encoding="utf-8")
    unconfirmed = [r for r in rows if not r["venue_evidence"]]
    journal = [r for r in unconfirmed if r["author_reported_journal_ref"]]
    preprints = [r for r in unconfirmed if not r["author_reported_journal_ref"]]
    highlights = {"2603.07514", "2603.09936", "2603.12366", "2604.24196", "2605.05118", "2605.11755", "2607.15065", "2608.29749", "2609.18108", "2609.27598", "2511.13720"}
    text = ["# 重要预印本与未核实身份索引", "", "[专题总览](README.md) · [综合分析](synthesis.md)", "",
            f"共有{len(unconfirmed)}项尚未在本轮定位到官方会议目录或正式论文集。下表保留arXiv版本、阅读层级与单篇链接。它们可能有作者自报的接收或期刊状态；未核实不等于未发表。", "",
            "## 直接影响本轮判断的重要条目", "", "| 论文 | 版本 | 阅读 |", "| --- | --- | --- |"]
    for row in unconfirmed:
        if row["key"] in highlights:
            text.append(f'| [{row["title"]}]({link(row)}) | `{row["arxiv_id"]}` | {LEVELS[row["reading_level"]]} |')
    text += ["", "## 预印本及会议身份尚未核实的全部条目", "", "| 论文 | 版本 | 阅读 |", "| --- | --- | --- |"]
    for row in preprints:
        text.append(f'| [{row["title"]}]({link(row)}) | `{row["arxiv_id"]}` | {LEVELS[row["reading_level"]]} |')
    text += ["", "## 作者报告期刊发表，独立期刊身份核查尚未完成", "", "| 论文 | 作者报告的期刊 | 阅读 |", "| --- | --- | --- |"]
    for row in journal:
        text.append(f'| [{row["title"]}]({link(row)}) | {row["author_reported_journal_ref"]} | {LEVELS[row["reading_level"]]} |')
    text.append("")
    (OUT / "preprints.md").write_text("\n".join(text), encoding="utf-8")
    print(f"Rendered {len(rows)} supplementary records in {len(TOPICS)} topics.")


if __name__ == "__main__":
    render()
