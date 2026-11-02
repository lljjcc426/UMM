# 当前研究入口：理解—生成诊断

2026-11-02新增任务：[静态图文配对S0–S1](../paired_strokes_v1/README.md)已完成CPU候选配对与评价工具，并已[归档16字/54笔独立审核](../paired_strokes_v1/human_review_receipt_2026-11-02.md)；“未”的关系保持unknown，其余240字仍待审。实际工作分支为`codex/research/new`；S2–S6未执行、未授权。下表继续保存此前Batch A诊断入口。

更新：2026-11-02。当前分支`exp/p1-process-diagnostic`。先读[工作区交接](../../project/WORKSPACE_HANDOFF.md)，再读下表。本目录按批次保存计划、执行及复核，准备时的未执行状态不能覆盖后续真实运行。

| 顺序 | 材料 | 用途 |
|---|---|---|
| 1 | [Batch A科学复核](batch_A_scientific_review_2026-11-01.md) | 最新证据边界、逐请求判断、能力矩阵及FIT-01准入 |
| 2 | [Batch A原执行报告](batch_A_results_2026-11-01.md) | 24次调用、20原答、4原片、资源、环境和完整分母 |
| 3 | [诊断Benchmark](diagnostic_benchmark_v0_1.md) | 识字、规范知识、几何、实际历史与原子生成的分离条件 |
| 4 | [SC-CoIT方法审计](SC_COIT_method_audit.md) | Policy/Draw Error、屏蔽、恢复、回放及接口前提 |
| 5 | [模型能力与接口审计](model_feasibility_matrix.md) | 原生视频、交错状态与静态任务的边界 |
| 6 | [科研启动准备报告](kickoff_execution_report.md) · [P1证据复用](p1_evidence_intake.md) | D0–D5准备范围及历史来源 |
| 7 | [原GPU申请](gpu_pilot_request.md) · [部署阻塞历史](batch_A_execution_2026-11-01.md) | 原计划和补充批准前快照；不授权再次执行 |

实际记录：[Batch A运行](../../../data/research/runs/diagnostic_batch_A_2026-11-01/state.json)、[独立复核](../../../data/research/reviews/batch_A_readonly_2026-11-01/review_scope_and_checks.json)、[准备登记](../../../data/research/next/experiments.json)。

## 可复用内容

`scripts/diagnostics/`为CPU构造、评价、采样审计和真实运行器；配置在`configs/research/next/`。已暴露的4字、74份开发样本、P1原片、同末帧微任务均可用于开发/回归，资格按原记录保留，不能重新充当独立保留集。

原片、原答、实际读帧、变换张量和固定源代码在`private/diagnostic_batch_A_2026-11-01/server_artifacts/`。去敏审核ZIP在`private/batch_A_readonly_2026-11-01/`，普通Git提交不会上传该目录。原Lance恢复授权仅适用已完成的Batch A，不能自动复用为新调用或训练批准。

## 下一实验的判断起点

4项识字错答仍有原生图像/官方正控、加载键覆盖等接口混杂；第023项保留原子增长正证据；多项过程回答存在事实错误。新实验应围绕待检验问题冻结精确对照，避免先认定知识、观察或生成中的唯一瓶颈。

FIT-01尚未准入训练执行；Batch B/C继续独立审批。六项接口正控及几何微任务FIT只是复核报告中的建议，本轮未新建请求清单或执行。计划可使用[模板](../../../templates/experiment_plan.md)整理，待用户给出下一目标与批准。
