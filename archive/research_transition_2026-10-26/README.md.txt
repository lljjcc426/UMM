# UMM与中文书写过程生成

研究统一多模态模型（UMM）如何结合理解与生成，重点关注中文书写中的实际历史、笔画决策、执行与风格控制。

核心问题：模型能否依据已经发生的书写过程，正确决定并生成后续？在相同信息、数据和计算预算下，共享训练能否优于专门模型及外部视觉语言模型指导系统？

## 从这里阅读

**[已分析论文总览](docs/reading/README.md)**：按会议和研究问题组织全部已完成论文。**[跨论文分析与20篇核心对照](docs/reading/synthesis.md)**：比较方法、证据边界及其对当前研究的意义。

| 会议索引 | 会议索引 | 会议索引 |
| --- | --- | --- |
| [CVPR](docs/reading/cvpr.md) | [ICCV](docs/reading/iccv.md) | [ECCV](docs/reading/eccv.md) |
| [NeurIPS](docs/reading/neurips.md) | [ICLR](docs/reading/iclr.md) | [ICML](docs/reading/icml.md) |

会议索引区分已核会议归属、作者录用声明和Workshop／Findings／Demo等类型；实际阅读版本与出版身份分别记录。

| 研究问题 | 阅读入口 |
| --- | --- |
| 统一哪些组件，如何保留生成细节？ | [架构与表示](docs/reading/architecture.md) |
| 理解怎样影响生成，共享训练是否有收益？ | [协同、反馈与推理](docs/reading/synergy.md) |
| 中文字形、在线轨迹与规范笔画如何对应？ | [书写与书法](docs/reading/handwriting.md) |
| 如何建模历史、运动与实际执行？ | [视频与时序控制](docs/reading/video.md) |
| 图形程序与绘画动作能提供哪些前作？ | [绘画与矢量过程](docs/reading/drawing.md) |
| 数据与指标能支持什么结论？ | [数据与评价](docs/reading/evaluation_data.md) |
| 生成理论、适配与效率有哪些约束？ | [基础与效率](docs/reading/foundations_efficiency.md) |

## 当前范围

截至2026-10-25，主目录共360条记录：333篇论文／研究、27项资源。327篇已完成所记录范围的核心阅读；A06、F05、L002、L006、L021、L022的资料缺项保留，**按用户要求停止跟进，当前未完成阅读队列为0**，详见[范围决定](docs/reading/scope.md)。27项资源的公开制品协议审查已完成，实际制品缺项见[资源审查](docs/evidence/resource_protocol_completion_and_source_limits_2026-10-25.md)。

本次重点转为CVPR、ICCV、ECCV、NeurIPS、ICLR、ICML已有分析的整理。其他直接前作继续保留。正文、附录、代码及制品的具体核查范围以逐篇笔记为准；论文报告结果与本仓库实验分别记载。

## 研究与证据入口

| 内容 | 入口 |
| --- | --- |
| 研究范围与主要判断 | [研究地图](docs/RESEARCH_MAP.md) · [研究判断](docs/project/DECISIONS.md) |
| UMM架构与理解生成协同 | [UMM综述](docs/umm/00_overview.md) · [UMM文献](docs/umm/literature.md) |
| 中文笔顺的直接前作与实验设计 | [笔顺专项](docs/handwriting/05_stroke_order_umm.md) · [证据核查](docs/handwriting/06_stroke_order_evidence.md) |
| 数据与评价协议 | [数据与标准](docs/handwriting/03_data_and_standards.md) · [评测协议](docs/experiments/benchmark_protocol.md) |
| 当前进展与实验方案 | [研究进展](docs/project/STATUS.md) · [实验计划](docs/project/EXPERIMENTS.md) · [最小研究方案](docs/experiments/stroke_order_pilot.md) |
| 逐篇证据与核查范围 | [360份笔记](docs/reviews/README.md) · [验收台账](docs/evidence/reading_ledger_2026-10-19.md) · [核查方法](docs/evidence/method_and_status.md) |
| 全部文献与候选题录 | [文献总表](docs/all_literature.md) · [CSV](data/literature.csv) · [Excel](data/literature_public.xlsx) · [候选目录](data/discovery/README.md) |
| 历史与本次改动 | [历史记录](docs/project/history/README.md) · [本次文件说明](docs/evidence/repository_organization_changes_2026-10-25.md) |

## 维护

`data/literature.json`是文献主数据；`data/reading_guide_2026-10-25.json`记录会议归属、主题及停止跟进的范围。更新相应数据后执行：

```bash
python scripts/render_reviews.py
python scripts/render_reading_guide.py
python scripts/validate_catalog.py
```

主目录数据变更时再用`python scripts/render_catalog.py`生成总表、CSV和Excel。本次整理保留这些主数据与导出表。

[受控像素过程小实验](docs/experiments/process_probe.md)验证了同终态反例及模板辅助的顺序／方向观测；模型训练和推理实验尚未开展。此前批次流水、旧状态与旧队列已保存在[历史目录](docs/project/history/README.md)。
