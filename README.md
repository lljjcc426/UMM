# UMM 与中文书写过程生成

研究统一多模态模型（Unified Multimodal Model，UMM）如何结合理解与生成，重点关注中文书写视频中的笔画顺序、实际执行和艺术风格控制。

核心问题是：模型能否根据已经发生的书写过程，判断下一笔并正确生成？在相同数据、输入和计算预算下，统一训练是否优于规则渲染、专门轨迹模型或外部视觉语言模型指导？

## 阅读导航

| 内容 | 入口 |
|---|---|
| 研究范围、主要发现与开放问题 | [综合分析](docs/RESEARCH_MAP.md) |
| 中文笔顺生成的直接前作、方法与实验设计 | [笔顺专项](docs/handwriting/05_stroke_order_umm.md) · [证据核查](docs/handwriting/06_stroke_order_evidence.md) |
| UMM架构、理解与生成协同 | [UMM综述](docs/umm/00_overview.md) · [相关文献](docs/umm/literature.md) |
| 书写轨迹、艺术字与视频生成 | [能力与问题](docs/handwriting/02_capability_matrix.md) · [相关文献](docs/handwriting/literature.md) |
| 重点论文的方法、结果与限制 | [论文精读](docs/handwriting/papers/README.md) · [ORVOS、BoxTuning与Timage](docs/evidence/public_preprint_reviews.md) |
| 数据、标准与评价 | [数据与标准](docs/handwriting/03_data_and_standards.md) · [评测协议](docs/experiments/benchmark_protocol.md) |
| 研究进展与后续实验 | [研究进展](docs/project/STATUS.md) · [结论依据](docs/project/DECISIONS.md) · [实验计划](docs/project/EXPERIMENTS.md) |
| 全部文献 | [文献总表](docs/all_literature.md) · [CSV](data/literature.csv) · [Excel](data/literature_public.xlsx) |

## 主要判断

- **读写联合与中文书法统一生成已有前作。** [InkSight](https://arxiv.org/abs/2402.05804)联合识别与笔迹恢复，[UniCalli](https://arxiv.org/abs/2510.13745)统一列级书法识别与静态生成。研究贡献需要具体到过程理解及其对生成的作用。
- **笔顺条件不等于过程正确。** 静态字形、最终帧OCR和文字笔顺问答都不能独立证明实际生成顺序；需要检查具体笔画的身份、先后、方向与落笔状态。
- **轨迹、物理渲染和视频文字控制已有可比较的方法。** [OnOff](https://arxiv.org/abs/2608.03198)连接轨迹与墨迹渲染；[VidScribe](https://arxiv.org/abs/2609.36598)和[VTR-Bench](https://arxiv.org/abs/2610.01499)提供视频文字评测。它们的指标与规范笔顺验证仍有区别。
- **UMM的额外收益尚需实验确认。** 先比较过程理解与生成执行，再扩展多字、布局、风格和效率。不能仅凭一个模型同时支持理解和生成就认定二者互相促进。

## 文献与证据

主目录包含 **269项论文／研究记录、11项资源，共280条记录**。每项记录包括研究主张、方法、问题、结果、限制、原始来源、版本及核查范围。数量不代表全文精读数量；文献中的数值为作者报告。

[候选目录](data/discovery/README.md)另含573条arXiv检索记录和200条综述目录候选，两者有重叠，也与主目录重叠。详细记录规则见[核查方法](docs/evidence/method_and_status.md)，早期分析见[研究档案](archive/README.md)。

## 数据维护

`data/literature.json` 为文献主数据。安装依赖后生成Markdown、CSV和Excel视图，并检查记录及仓库内链接：

```bash
python -m pip install -r requirements.txt
python scripts/render_catalog.py
python scripts/validate_catalog.py
```

`scripts/stroke_metrics.py` 提供已标注事件序列的指标示例，不负责从视频识别笔画。实验设计与模型结果分开记录，当前尚无模型实验结果。
