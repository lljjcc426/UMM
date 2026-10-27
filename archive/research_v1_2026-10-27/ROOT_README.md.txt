# UMM 与汉字书写视频：文献证据与研究实施

研究统一多模态模型如何读取实际书写历史、判断笔画状态，并生成符合指定规范的可见书写过程。核心假设：**过程理解能改善实际视觉执行；在相同信息、数据和计算条件下，共享训练可能具有额外收益。** 两个假设分别验证，不预设 UMM 优于专用模型或组合系统。

## 当前阶段：从调研转入实验准备

更新：2026-10-26。基于 `e95bed3766fa43b03a704145483dd05b43a6d326` 整理。文献主目录保持 **360 条：333 篇论文／研究、27 项资源**；327 篇完成所记录范围的核心阅读。A06、F05、L002、L006、L021、L022 保留资料缺项并退出主动追取队列，未计入完成。此次整理不增加论文完成数。[范围决定](docs/reading/scope.md)

**已有实验**仅为 [PX-01 受控像素反例](docs/experiments/process_probe.md)。新的数据、评价器校准、模型推理、微调及结果比较尚未开展；文档中的样本量、阈值和预算均为拟定设置。

## 研究实施入口

| 要做什么 | 唯一主入口 |
| --- | --- |
| 理解目标、阶段、交付物与停止条件 | **[分阶段研究路线](docs/project/ROADMAP.md)** |
| 查每个实验的假设、对照和依赖 | **[实验矩阵](docs/project/EXPERIMENTS.md)** · [结构化登记](data/research/experiments_v1.json) |
| 确定任务、方法与最近前作的区别 | [任务与方法设计](docs/research/task_and_method.md) |
| 选数据、标注和划分，防止泄漏 | [数据实施协议](docs/research/data_protocol.md) |
| 定义真实 RGB 笔顺、不可观察及质量指标 | **[评价协议 v1](docs/research/evaluation_protocol.md)** |
| 选择底座、检查接口和启动顺序 | [实现与资源方案](docs/research/implementation.md) |
| 查看真实完成状态 | [当前状态](docs/project/STATUS.md) |
| 创建配置和运行记录 | [计划配置](configs/research/stroke_video_v1.json) · [运行模板](templates/research_run.json) |

初始范围：单字、固定视角、无手遮挡、保留明确笔画结构的风格化墨迹。先完成可观察性、单任务和正确控制实验，再进行联合训练；多字、真实手持笔、行草及加速按阶段解锁。

## 文献与证据入口

**[阅读总览](docs/reading/README.md)** · **[跨论文分析与20篇核心对照](docs/reading/synthesis.md)**

| 会议 | 会议 | 会议 |
| --- | --- | --- |
| [CVPR](docs/reading/cvpr.md) | [ICCV](docs/reading/iccv.md) | [ECCV](docs/reading/eccv.md) |
| [NeurIPS](docs/reading/neurips.md) | [ICLR](docs/reading/iclr.md) | [ICML](docs/reading/icml.md) |

会议身份、实际阅读版本、Workshop／Demo及作者声明继续分开记录。

| 主题 | 入口 |
| --- | --- |
| 架构与表示 | [主题索引](docs/reading/architecture.md) · [UMM综述](docs/umm/00_overview.md) · [UMM文献](docs/umm/literature.md) |
| 协同、反馈与推理 | [主题索引](docs/reading/synergy.md) · [研究判断](docs/project/DECISIONS.md) |
| 中文笔迹与书法 | [主题索引](docs/reading/handwriting.md) · [笔顺专项](docs/handwriting/05_stroke_order_umm.md) |
| 视频与绘画 | [视频控制](docs/reading/video.md) · [绘画与矢量](docs/reading/drawing.md) |
| 数据、评价与基础 | [数据评价索引](docs/reading/evaluation_data.md) · [基础效率](docs/reading/foundations_efficiency.md) |
| 单篇证据 | [360份笔记](docs/reviews/README.md) · [验收台账](docs/evidence/reading_ledger_2026-10-19.md) |
| 全量题录与资源 | [文献总表](docs/all_literature.md) · [CSV](data/literature.csv) · [Excel](data/literature_public.xlsx) · [候选目录](data/discovery/README.md) |
| 边界与历史 | [资源实际制品边界](docs/evidence/resource_protocol_completion_and_source_limits_2026-10-25.md) · [历史记录](docs/project/history/README.md) · [本轮整理说明](docs/evidence/research_transition_2026-10-26.md) |

## 维护与验证

目录职责、权威来源及状态定义见 [维护规范](CONTRIBUTING.md)；研究工作区导航见 [docs/research](docs/research/README.md)。

```bash
# 无网络、无权重：验证计划结构、依赖和本地引用
python scripts/validate_research_plan.py
python -m unittest discover -s tests -p 'test_research_plan.py' -v
# 全仓库文献字段与 Markdown 相对链接检查
python scripts/validate_catalog.py
```

`data/literature.json` 为文献主数据；`data/reading_guide_2026-10-25.json` 为阅读分组配置。只在相应源数据变化后运行 `scripts/render_reviews.py`、`scripts/render_reading_guide.py`；主目录变更后运行 `scripts/render_catalog.py` 同步总表、CSV和Excel。本轮不修改这些文献数据或导出文件。

计划校验通过仅说明文件与依赖满足规则，不表示模型性能、数据授权、评价器有效性或科学假设得到验证。
