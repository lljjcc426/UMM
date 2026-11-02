# UMM 汉字书写视频

研究目标是生成内容、笔画方向与笔画先后正确的汉字书写视频。本仓库同时保留原生视频模型实验、理解—生成诊断、受控执行工程原型与文献资料，几类结果分别记录。

**当前分支：`codex/research/new`。2026-11-02：静态图文配对CPU工具已落地，16字/54笔独立人审已归档，保留“未”的关系未知；其余240字待审。没有模型调用或训练，Batch B/C及本方案S2–S6执行未获批准。**

先阅读[当前状态](docs/project/STATUS.md)和[实验交接](docs/project/WORKSPACE_HANDOFF.md)。P0/P1维持有限负结果结项，Batch A的工程完整性不代表模型能力通过。

## 当前入口

| 内容 | 入口 |
|---|---|
| 静态字图与有序笔形配对：S0–S1实际交付与真值缺口 | [独立审核接收](docs/research/paired_strokes_v1/human_review_receipt_2026-11-02.md) · [原执行报告](docs/research/paired_strokes_v1/execution_report_2026-11-02.md) · [冻结协议](docs/research/paired_strokes_v1/protocol.md) · [数据入口](data/research/paired_strokes_v1/README.md) |
| 下一轮实验的起点、资源与待解决事项 | [工作区交接](docs/project/WORKSPACE_HANDOFF.md) · [新实验计划模板](templates/experiment_plan.md) |
| Batch A科学结论与FIT-01准入判断 | [只读复核报告](docs/research/next/batch_A_scientific_review_2026-11-01.md) |
| Batch A全部调用、环境、资源与备份 | [执行报告](docs/research/next/batch_A_results_2026-11-01.md) · [实际执行登记](data/research/runs/diagnostic_batch_A_2026-11-01/execution_summary.json) |
| 理解—生成Benchmark、SC-CoIT与训练对照准备 | [本轮研究导航](docs/research/next/README.md) |
| 本地工程预览与原生LTX试验 | [8字工程原型](docs/engineering/hanzi_video_v1.md) · [LTX本机试验](docs/engineering/ltx_local_trial_2026-11-01.md) |
| 已结项阶段与原始验收限制 | [P0最终报告](docs/research/v2/p0_final_scientific_closeout_2026-10-30.md) · [P1最终报告](docs/research/v2/p1_final_scientific_closeout_2026-10-31.md) |
| 文献与研究资料 | [阅读总览](docs/reading/README.md) · [研究导航](docs/research/README.md) |
| 执行与分支约束 | [AGENTS.md](AGENTS.md) · [分支工作流](docs/project/BRANCH_WORKFLOW.md) · [维护规范](CONTRIBUTING.md) |

复核保留四项识字错答、实际历史理解错误，以及第023项左到右横线增长的正面个案。原生图像正控、主模型加载键覆盖、可靠监督与训练配方仍需完善；详细依据见复核报告。没有新的模型改进、完整规范金标或独立保留验证结果。

## 本地入口

已有`.venv`时直接使用，基础依赖见[requirements.txt](requirements.txt)。该环境用于CPU工程和分析；Lance GPU与LTX MPS使用各自独立环境。

```bash
# 目录、记录与本地链接检查；无模型调用
.venv/bin/python scripts/validate_catalog.py

# 8字受控执行预览
.venv/bin/python -m hanzi_video.server --port 8780
```

预览页面为`http://127.0.0.1:8780/`。支持士、丑、小、以、广、刃、乞、点；未配置真实UMM时页面明确使用CPU预览。8字绑定仅为AI工程核对，不能当作真人逐笔规范金标或UMM能力证明。

## 文件布局

| 目录 | 用途 |
|---|---|
| `scripts/diagnostics/` | 当前诊断数据、评价、运行器和汇总代码 |
| `configs/research/next/` | 诊断与训练对照配置 |
| `data/research/next/` | 科研重启准备记录；原冻结清单保留 |
| `data/research/runs/` | 实际实验、原授权、失败与运行证据 |
| `data/research/reviews/` | 对已有实验的追加复核，不覆盖原结果 |
| `docs/research/next/` | 当前报告、方法审计与候选实验方案 |
| `hanzi_video/`、`scripts/engineering/` | 受控执行原型与本地模型试验 |
| `docs/research/v2/`、`docs/project/stages/` | 历史阶段协议、契约、正式报告与门禁 |
| `data/literature.json`、`docs/reading/`、`docs/reviews/` | 文献主数据、阅读索引与逐篇资料 |
| `private/`、`checkpoints/` | Git忽略的原片、审核包、论文、权重及独立环境 |
| `archive/` | 历史资料与导航原文快照 |

私有审核ZIP：`private/batch_A_readonly_2026-11-01/Batch_A_scientific_review_sanitized.zip`，解压后打开`index.html`。交付回执见[data/research/reviews中的记录](data/research/reviews/batch_A_readonly_2026-11-01/delivery_receipt.json)。它不会随普通Git提交上传。

本次整理前的README及其他旧导航原文保存在[导航快照](archive/workspace_navigation_2026-11-02/README.md)。实验数据、原人审、阈值、失败、正式发布状态和旧分支均保留。
