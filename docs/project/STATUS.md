# 当前状态

更新：2026-11-02。当前工作分支：`exp/p1-process-diagnostic`。入口：[工作区交接](WORKSPACE_HANDOFF.md)、[当前研究导航](../research/next/README.md)。

## Batch A执行与科学复核

同一Lance_3B_Video检查点的精确24次调用已完成：20份理解原答、4段原生MP4均工程有效，技术失败、阻塞、未运行、额外GPU重试、本任务训练均为0。182项CPU回归测试通过，原备份724份文件完整。本任务GPU进程在原退出记录中已退出；没有对当前服务器状态作新检查。

2026-11-02只读复核补充了以下科学边界：

- 4项K-CHAR在静态重复视频接口中均有明确错答；原生图像和官方正控、主模型加载键覆盖仍缺，不能完全排除接口混杂。
- 第023项在编码前RGB和解码视频中均显示左到右横线增长；另外三项存在形状或过程缺失。不能据此认定复杂汉字生成通过。
- 实际历史理解存在方向、数量、移动和墨迹脱落等事实错误；保留第013项局部时序正证据。017/018/020回答截断。
- 原生固定时间grid与真实采样PTS不一致；不同FFmpeg版本的解码像素略有差异，主要视觉结论一致，精确像素统计须标明来源。
- FIT-01可继续方案准备，尚未满足训练执行准入。没有新的真人金标、独立保留验证、模型改进或因果机制结论。

证据：[执行报告](../research/next/batch_A_results_2026-11-01.md)、[科学复核报告](../research/next/batch_A_scientific_review_2026-11-01.md)、[逐请求证据](../../data/research/reviews/batch_A_readonly_2026-11-01/per_request_evidence.json)。D0–D5中的`prepared_unexecuted`等保留为准备时快照；实际运行以Batch A执行登记为准。

## 正式阶段与工程原型

| 范围 | 当前状态 | 限制/入口 |
|---|---|---|
| P0 | 已获批有限负结果结项 | ENV-01限已验证配方；DATA-01/EVAL-01原缺口及负结果保留；[最终报告](../research/v2/p0_final_scientific_closeout_2026-10-30.md) |
| P1 | `closed_with_negative_results` | 63原生片与1失败保留；双人粗筛已完成，不能升级完整七维金标；[最终报告](../research/v2/p1_final_scientific_closeout_2026-10-31.md)；main合并未批准 |
| 8字工程原型 | CPU受控执行与页面已实现 | 真实UMM识别/规划链路未完成正式验收；[工程报告](../engineering/hanzi_video_v1.md) |
| LTX本地验证 | 两段真实原生MP4，失败保留 | 未形成正确逐笔过程，方向/笔顺unknown；[试验报告](../engineering/ltx_local_trial_2026-11-01.md) |

## 下一项实验

当前仅完成仓库整理与本地保存，尚未启动新实验。新任务的目标、模型/数据、精确请求或训练配方、资源、验收和分支由下一次明确授权确定。Batch B/C、额外GPU/MPS调用、远端推送和main合并仍未授权。

当前目录说明、私有证据路径及下一任务须继承的限制见[WORKSPACE_HANDOFF.md](WORKSPACE_HANDOFF.md)。整理前的完整STATUS原文保存在[历史导航快照](../../archive/workspace_navigation_2026-11-02/STATUS.md.txt)。本页为导航更新，不改写阶段发布文件或旧实验登记。
