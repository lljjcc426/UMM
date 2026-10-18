# H1-v3首批结果

2026-10-18，固定分支research/stroke-order-joint-feedback，完整Show-o2-1.5B-w-video-und，M5／16GiB。首批按T1→T5完成，UMM全部冻结，只训练独立A—C小模块。**完整H1未通过，H2／H3未开始；本批停止新增训练。**

| 阶段 | 可复核记录 |
|---|---|
| 详细计划／资源 | [协议](../../../docs/experiments/h1_v3_protocol.md) · [resources.json](resources.json) |
| T1现有代码与权重 | [审计](T1_AUDIT.md) · [实际形状](audit.json) |
| T2无训练可观察性 | [报告](T2_REPORT.md) · [官方路径](T2_SOURCE_AUDIT.md) · [像素逐例](T2_pixel_predictions.json) · [原生回答](T2_direct_predictions.json) |
| T3指定A—D小集拟合 | [报告](T3/REPORT.md) · [预注册](T3/preregistration.json) · [空间预测](T3/spatial_predictions.json) · [事件预测](T3/B4_metrics.json) |
| T4一次固定实验 | [报告](T4/REPORT.md) · [预注册](T4/preregistration.json) · [全部指标](T4/metrics.json) · [B4逐例](T4/B4_predictions.json) · [全部失败](T4/B4_failures.json) |
| T5决策 | [七问与理论分析](T5_DECISION.md) · [状态接口](../../../data/h1/event_v3/state_schema.json) |
| 方法与前作 | [A—D](../../../docs/experiments/h1_v3_method.md) · [RELATED_METHODS_AND_GAPS](../../../docs/experiments/RELATED_METHODS_AND_GAPS.md) |

核心结果：B4决定顺序95.33%，同输入无跨帧普通头98%；同终态配对4/5对3/5，实例匹配7/11，未知21/25。正确区域使状态100%，仍未解决“三”的历史排序；移除变化／实例区域均下降。完整预测和负结果保持，不用单一总分宣布成功。

在仓库根目录使用checkpoints/Show-o-env/bin/python。权重与大特征位于本地checkpoints/h1_event_v3，不上传。复现训练须指定新目录，不能覆盖已记录结果；例如已有固定数据和冻结特征时：

```bash
checkpoints/Show-o-env/bin/python scripts/h1_event_train.py smallfit \
  --output results/h1/event_v3/T3_reproduction \
  --weights checkpoints/h1_event_v3/T3_reproduction

checkpoints/Show-o-env/bin/python scripts/h1_event_experiment.py \
  --output results/h1/event_v3/T4_reproduction \
  --weights checkpoints/h1_event_v3/T4_reproduction
```

以上为复现说明，不属于本批追加运行。原始执行命令及配置见各阶段报告；初始数据由h1_event_data.py、h1_event_study.py构造，冻结编码由h1_event_observe.py／h1_event_study.py完成。初始资源检查记录当时尚未安装视频解码器，随后在专用环境安装PyAV19.0.1并记录本机适配。

本轮新增event_v3原创数据、视频与标注、模块和训练评价代码、方法与前作说明、完整结果和决策；更新项目入口与依赖。旧state_pairs_v1保留为仅编码记录，无训练成绩。没有删除任何文件或覆盖旧权重／原始结果。
