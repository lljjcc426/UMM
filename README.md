# UMM 与中文书写过程生成

研究统一多模态模型（Unified Multimodal Model，UMM）如何结合理解与生成，重点关注中文书写视频中的笔画顺序、实际执行和艺术风格控制。

核心问题是：模型能否根据已经发生的书写过程，判断下一笔并正确生成？在相同数据、输入和计算预算下，统一训练是否优于规则渲染、专门轨迹模型或外部视觉语言模型指导？

## 当前探索主线

暂定题目：**实际笔顺理解驱动的统一多模态中文书写视频生成**。

通过联合训练学习实际过程理解，并在生成时读回每段实际结果、更新状态后继续书写。研究按H1“读懂过程”、H2“理解改善生成”、H3“统一学习优于可比分离方案”推进。**H1-T7实例绑定与起笔确认实验已完成，决定REVISE；完整H1尚未通过，H2与H3未开始。** 本批为冻结Show-o2特征上的独立事件读取，不能称为UMM联合训练改善。见[T7决策](results/h1/instance_onset_v1/T7_DECISION.md)、[T6决策](results/h1/early_history_v1/T6_DECISION.md)与[此前T5决策](results/h1/event_v3/T5_DECISION.md)。

本主线使用单独分支 [`research/stroke-order-joint-feedback`](https://github.com/lljjcc426/UMM/tree/research/stroke-order-joint-feedback)，后续相关工作沿用该分支。入口：[总跟踪Issue #1](https://github.com/lljjcc426/UMM/issues/1) · [主线定义](docs/project/MAINLINE.md) · [当前进度](docs/project/STATUS.md) · [实验安排](docs/project/EXPERIMENTS.md)。

最新T7：90独立几何、3/5笔混合，A0/A1等预算各480更新，B、M1与UMM冻结。A1实例匹配105→111/120（92.5%），但E11历史配对77.04%，E00为77.78%；正确可用覆盖82.22%、未定组87.78%。正确区域仍有起笔漏读与候选区间冲突，下一项应先单独研究这个接口，本轮停止训练和规则修改。见[T7结果入口](results/h1/instance_onset_v1/README.md)与[协议](docs/experiments/h1_t7_protocol.md)。

此前T6：固定20／8／20独立几何组、24观察，主测试每个决策40个“最近输入相同、早期真实历史不同”配对。三决策合计，Full Transformer配对16.7%，预测事件表77.5%，同一局部头换用正确区域的事件表100%。Full与Ledger未知召回均100%，但Ledger回答覆盖83.3%、未定组完全正确85%；当前优先修复近邻实例绑定和首次起笔读取，保持UMM冻结。全部预算和失败见[T6结果入口](results/h1/early_history_v1/README.md)与[预注册协议](docs/experiments/h1_t6_early_history_protocol.md)。

此前T1—T5：固定20组几何／120段受控视频，测试30段。B4因果模块严格顺序95.33%，相同输入的无时序头B3为98%；同终态配对4/5对3/5，尚无稳定全面优势。实例定位仅7/11达到IoU.5，未知21/25；“三”的实际换序仍可能读成规范顺序。全部消融与失败已保留，本批停止训练。入口：[协议](docs/experiments/h1_v3_protocol.md) · [方法](docs/experiments/h1_v3_method.md) · [前作与边界](docs/experiments/RELATED_METHODS_AND_GAPS.md) · [完整结果](results/h1/event_v3/README.md)。1—4像素缺口继续独立保留，当前安排以v3协议为准。

此前静态诊断（v2历史安排）：固定其他笔迹、只改变目标末端，UMM预测区域状态头的完整／缺1像素配对仅1/56，完整／缺16像素22/56；同一头用正确区域后16像素为37/56。只改变其他线条，完整目标的答案也改变19/56，完整正确40→29/56。8–16像素通常能改变分数方向，尚未形成稳定答案。该轮提出目标末端与背景分别变化的配对监督；准备仅编码、未训练，随后转入v3事件研究。原适配器与正确／预测区域对照保持。见[末端配对诊断](results/h1/showo2_video_1_5b/endpoint_pairs_v1/README.md)与[此前进度覆盖](results/h1/showo2_video_1_5b/progress_coverage_v1/README.md)。

## 阅读导航

| 内容 | 入口 |
|---|---|
| 研究范围、主要发现与开放问题 | [综合分析](docs/RESEARCH_MAP.md) |
| 中文笔顺生成的直接前作、方法与实验设计 | [笔顺专项](docs/handwriting/05_stroke_order_umm.md) · [证据核查](docs/handwriting/06_stroke_order_evidence.md) |
| UMM架构、理解与生成协同 | [UMM综述](docs/umm/00_overview.md) · [相关文献](docs/umm/literature.md) |
| 书写轨迹、艺术字与视频生成 | [能力与问题](docs/handwriting/02_capability_matrix.md) · [相关文献](docs/handwriting/literature.md) |
| 重点论文的方法、结果与限制 | [论文精读](docs/handwriting/papers/README.md) · [四篇指定论文精读](docs/evidence/attachment_reviews.md) · [公开版本对照](docs/evidence/public_preprint_reviews.md) |
| 数据、标准与评价 | [数据与标准](docs/handwriting/03_data_and_standards.md) · [评测协议](docs/experiments/benchmark_protocol.md) |
| 研究进展与后续实验 | [研究进展](docs/project/STATUS.md) · [结论依据](docs/project/DECISIONS.md) · [实验计划](docs/project/EXPERIMENTS.md) · [最小研究方案](docs/experiments/stroke_order_pilot.md) |
| 全部文献 | [文献总表](docs/all_literature.md) · [CSV](data/literature.csv) · [Excel](data/literature_public.xlsx) |

## 主要判断

- **读写联合与中文书法统一生成已有前作。** [InkSight](https://arxiv.org/abs/2402.05804)联合识别与笔迹恢复，[UniCalli](https://arxiv.org/abs/2510.13745)统一列级书法识别与静态生成。研究贡献需要具体到过程理解及其对生成的作用。
- **笔顺条件不等于过程正确。** 静态字形、最终帧OCR和文字笔顺问答都不能独立证明实际生成顺序；需要检查具体笔画的身份、先后、方向与落笔状态。
- **轨迹、物理渲染和视频文字控制已有可比较的方法。** [OnOff](https://arxiv.org/abs/2608.03198)连接轨迹与墨迹渲染；[VidScribe](https://arxiv.org/abs/2609.36598)和[VTR-Bench](https://arxiv.org/abs/2610.01499)提供视频文字评测。它们的指标与规范笔顺验证仍有区别。
- **UMM的额外收益尚需实验确认。** 先比较过程理解与生成执行，再扩展多字、布局、风格和效率。不能仅凭一个模型同时支持理解和生成就认定二者互相促进。

## 文献与证据

主目录包含 **270项论文／研究记录、11项资源，共281条记录**。每项记录包括研究主张、方法、问题、结果、限制、原始来源、版本及核查范围。数量不代表全文精读数量；文献中的数值为作者报告。

[候选目录](data/discovery/README.md)另含573条arXiv检索记录和200条综述目录候选，两者有重叠，也与主目录重叠。详细记录规则见[核查方法](docs/evidence/method_and_status.md)，早期分析见[研究档案](archive/README.md)。

## 数据维护

`data/literature.json` 为文献主数据。安装依赖后生成Markdown、CSV和Excel视图，并检查记录及仓库内链接：

```bash
python -m pip install -r requirements.txt
python scripts/render_catalog.py
python scripts/validate_catalog.py
```

`scripts/stroke_metrics.py` 提供已标注事件序列的指标示例，不负责从视频识别笔画。[像素过程小实验](docs/experiments/process_probe.md)验证同终态反例和模板辅助的顺序/方向观测，可用 `python scripts/process_probe.py` 复现并查看[动画](examples/process_probe/comparison.gif)。

本轮Show-o2的[接口与状态诊断](docs/experiments/h1_state_gate.md)使用`requirements-h1-showo.txt`及适合平台的PyTorch，数据、原始回答、评分、文字/视觉适配配置及训练损失已保存。此前[Janus-Pro诊断](docs/experiments/h1_umm_diagnostic.md)使用`requirements-h1-umm.txt`；Qwen3-VL保留为[外部辅助诊断](docs/experiments/h1_diagnostic.md)，使用`requirements-h1.txt`。另已完成H1-v3冻结特征上的时空事件小模块监督与固定消融；视频生成及统一主干的过程联合训练尚未开展。
