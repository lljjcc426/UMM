# UMM 与汉字书写视频：证据、方法与实验

2026-10-30：**用户最终审批已通过P0有限结项**，见[正式审批与P1交接](docs/research/v2/p0_final_acceptance_and_p1_handoff_2026-10-30.md)。[P0报告](docs/research/v2/p0_final_scientific_closeout_2026-10-30.md)保留原指标未达标结论：ENV-01维持已验证配方通过，DATA-01为completed_with_limitations，EVAL-01为completed_negative；原阈值、人审及失败不变。正式评价仍用可信规范＋独立人工实际RGB主评＋自动辅助＋严格unknown。[P1方案](docs/research/v2/p1_baseline_failure_plan_2026-10-30.md)聚焦UMM真实视频的笔顺错误及改进，已有8字/64请求，首批4字/16请求；该P1方案记录的是准备与部署快照，不代表已完成推理、训练或新人工任务。**P0有限结项及P1准备已通过[PR #2](https://github.com/lljjcc426/UMM/pull/2)合入main**，原科学门槛未达标结论保留。

以下保留此前设计与执行快照；当前状态以上段及结项报告为准。

**研究核心：提升生成RGB中实际笔画事件与规范书写的一致性，通过已有视频UMM的后训练形成方法和模型。** 先验证同数据普通适配后的执行缺口，再研究事件状态条件、共享训练；自主纠错和效率为可选扩展。

## 当前有效设计：stroke-video-v2

更新于2026-10-29。[设计v2总览](docs/research/v2/README.md)是当前科学设计主入口；[阶段路线](docs/project/ROADMAP.md)与[实验矩阵](docs/project/EXPERIMENTS.md)提供执行导航。

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

[本轮小批次人工审核已完成](docs/research/v2/p0_quick_consensus_2026-10-28.md)：12张首审＋6张复核全部收齐。晌、剿、潜、篇、聪、耀6段均有两份“视频完整过程正确”的一致原文；原AI未知意见保留。19个原始提交版本已归档，本批剩余人工任务0，不自动追加。完整科学校准及独立来源证据仍缺，DATA-01/EVAL-01保持blocked。

2026-10-29 D1–D4开发完成：[解耦执行报告](docs/research/v2/p0_decoupled_d1_d4_report_2026-10-29.md)记录36个四格条件、96次权限/表示检查及144份暴露材料公平对照。完整解耦与“旧观察器＋相同独立规范简单门控”输出完全相同；全量清晰覆盖23.70%、正确接受9/32、111份unknown，不能凭0/63误接受认定通过。13组仅获AI逐实例开发资格，原人审未升级为逐笔金标。Pot1.0Test仅余194、213两位候选，64个新作者组资源不足。DATA-01/EVAL-01仍blocked，P0未验收；新增8段CPU开发媒体，无新增人工、下载、训练或GPU。当前停止等待下一项授权。

[双人固定包已全部完成并归档](docs/research/v2/p0_human_acceptance_2026-10-29.md)：两位独立真人各216项，432有效提交、441原始版本保留，剩余人工任务0。64规范候选34通过/23不通过/7未知；144份RGB冻结门控后32正确/103错误/9未知。原观察器误接受25/63负例书写者组，条件95%上界50.82%，高于5%门槛；排除两帧控制后覆盖97.48%，误接受仍失败。DATA-01参考资格和EVAL-01门槛保持blocked，完整P0未验收。原640字/2,752媒体、旧人审、旧预测及阈值保留；不自动追加第三轮、训练或进入下一阶段。

新增关键检查：同数据普通SFT和轨迹/硬控制强基线；真实模型输出上的评价器校准；事件身份/进度/空间干预；共享与分离系统的同接口对照。ENV-01已完成三项原生接口、最小部分参数训练和独立重载，见[训练与重载报告](docs/research/v2/env01_training_reload_report_2026-10-27.md)。默认策略容量已有OOM负结果，收敛与笔顺质量未验证，完整P0尚未验收，其余14项planned。[PX-01八个受控像素案例](docs/experiments/process_probe.md)保留。

## 文献与证据

2026-10-30新增 **[扩散、Flow与Drifting专题](docs/generative/README.md)**：取消篇数上限后补充142项去重记录，含10项重点章节核读、31项正文片段选读、101项摘要筛选；[综合分析](docs/generative/synthesis.md)对照原理、理论条件、实验与UMM适用边界。该补充专题独立登记，不增加下述主目录的核心完成计数；[检索边界](docs/generative/search_scope.md)与[文件变更](docs/generative/changes_2026-10-30.md)可追溯。

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

P0有限结项已通过PR #2进入 `main`，原研究分支与证据保留。后续研究仍按阶段分支执行，`main` 仅接收完成工程和科研验收、经用户批准的 PR。Codex 执行审批约束见 [AGENTS.md](AGENTS.md)，分支及证据合并标准见 [BRANCH_WORKFLOW.md](docs/project/BRANCH_WORKFLOW.md)。有效正、负结论都可以记录；新阶段实验尚未完成。
