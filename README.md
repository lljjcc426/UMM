# UMM 与汉字书写视频：证据、方法与实验

**研究核心：提升生成RGB中实际笔画事件与规范书写的一致性，通过已有视频UMM的后训练形成方法和模型。** 先验证同数据普通适配后的执行缺口，再研究事件状态条件、共享训练；自主纠错和效率为可选扩展。

## 当前有效设计：stroke-video-v2

更新于2026-10-27。[设计v2总览](docs/research/v2/README.md)是当前科学设计主入口；[阶段路线](docs/project/ROADMAP.md)与[实验矩阵](docs/project/EXPERIMENTS.md)提供执行导航。

| 内容 | 当前入口 |
| --- | --- |
| 目标、最近前作及v1修订 | **[研究设计v2](docs/research/v2/README.md)** · [近期来源审计](docs/research/v2/source_audit.md) |
| 模型可见信息、事件表示和损失 | [方法](docs/research/v2/method.md) |
| 数据划分、独立评价与统计 | [数据和评价](docs/research/v2/data_evaluation.md) |
| 17个实验的目的与停止条件 | **[详细实验](docs/research/v2/experiments.md)** · [机器登记v2](data/research/experiments_v2.json) |
| 实现、资源与接口缺项 | [实现方案](docs/research/v2/implementation.md) |
| 配置及运行证据 | [配置v2](configs/research/stroke_video_v2.json) · [运行模板v2](templates/research_run_v2.json) |
| 实际状态 | [STATUS](docs/project/STATUS.md) |

初始范围为固定画布、无手遮挡、规范和实例可辨的风格化单字。T从空白完整生成是主结果，P实际前缀续写用于机制分析，O真值控制为特权上界，I目标图到过程是可选独立任务。字库几何权限G0/G1分开。不得以计划正确、最终OCR或teacher-forced一步成绩替代完整过程成功。

新增关键检查：同数据普通SFT和轨迹/硬控制强基线；真实模型输出上的评价器校准；事件身份/进度/空间干预；共享与分离系统的同接口对照。ENV-01获准的三项原生接口子任务已完成，完整实验仍为running，其余16项仍为planned；未训练、构建新数据集或校准通用RGB观察器。实际状态见[ENV-01执行记录](data/research/runs/env01_native_a10080_2026-10-27/task_record.json)；[PX-01八个受控像素案例](docs/experiments/process_probe.md)保留。

## 文献与证据

主目录保持360条（333篇论文/研究、27项资源），327篇核心阅读完成；具体范围见单篇。A06、F05、L002、L006、L021、L022继续[停止主动追取](docs/reading/scope.md)，未计完成。本轮新增来源审计未自动增加论文或完成计数。

**[阅读总览](docs/reading/README.md)** · **[跨论文综合](docs/reading/synthesis.md)** · [全部逐篇卡](docs/reviews/README.md)

| 会议 | 会议 | 会议 |
| --- | --- | --- |
| [CVPR](docs/reading/cvpr.md) | [ICCV](docs/reading/iccv.md) | [ECCV](docs/reading/eccv.md) |
| [NeurIPS](docs/reading/neurips.md) | [ICLR](docs/reading/iclr.md) | [ICML](docs/reading/icml.md) |

主题入口：[架构](docs/reading/architecture.md)、[协同](docs/reading/synergy.md)、[书写](docs/reading/handwriting.md)、[视频](docs/reading/video.md)、[绘画](docs/reading/drawing.md)、[数据评价](docs/reading/evaluation_data.md)、[基础效率](docs/reading/foundations_efficiency.md)。

证据入口：[研究地图](docs/RESEARCH_MAP.md)、[笔顺专项](docs/handwriting/05_stroke_order_umm.md)、[验收台账](docs/evidence/reading_ledger_2026-10-19.md)、[资源边界](docs/evidence/resource_protocol_completion_and_source_limits_2026-10-25.md)、[文献总表](docs/all_literature.md)、[CSV](data/literature.csv)、[Excel](data/literature_public.xlsx)。

## 维护与校验

```bash
python scripts/validate_research_v2.py
python -m unittest tests.test_research_v2 -v
python scripts/validate_catalog.py
# v1历史结构与既有单元测试继续保留
python scripts/validate_research_plan.py
python -m unittest tests.test_research_plan tests.test_stroke_metrics -v
```

[CONTRIBUTING](CONTRIBUTING.md)规定文献、当前设计、运行结果和历史的职责。本轮不修改文献主数据或其导出表；不要重跑文献生成器覆盖人工变更。[v2修订记录](docs/evidence/research_revision_v2_2026-10-27.md)列出备份与验证边界。[v1冻结版本](https://github.com/lljjcc426/UMM/tree/199646c6960677f656594b3c542c8eb8aaf890f9)可完整追溯。

校验通过只支持字段、依赖及本地链接正确；不证明数据授权、观察器可靠、GPU可运行或科学假设成立。

## 阶段研究分支

当前 P0 在 `research/p0-stroke-video-foundation` 独立开发，`main` 仅接收完成工程和科研验收、经用户批准的 PR。Codex 执行审批约束见 [AGENTS.md](AGENTS.md)，分支及证据合并标准见 [BRANCH_WORKFLOW.md](docs/project/BRANCH_WORKFLOW.md)。有效正、负结论都可以记录；新阶段实验尚未完成。
