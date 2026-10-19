# H1-T7结果

结论：[REVISE，先处理起笔证据冲突](T7_DECISION.md)。T7-1→T7-6完成，本轮停止训练与规则修改。A1实例匹配92.5%，E11历史配对77.04%、正确可用覆盖82.22%、未定组87.78%；没有支持相对E00的整体收益。完整H1、H2/H3未通过。

阅读顺序：[T6冻结归因](T7_1_ATTRIBUTION.md) → [新数据与预注册](T7_2_DATA.md) → [A0/A1](T7_3_GROUNDING.md) → [L规则](T7_4_LEDGER.md) → [正式结果](T7_5_RESULTS.md) → [最终分析](T7_DECISION.md)。

[协议](../../../docs/experiments/h1_t7_protocol.md)、[方法](../../../docs/experiments/h1_t7_method.md)、[数据](../../../data/h1/instance_onset_v1/README.md)、[状态接口含义](../../../data/h1/instance_onset_v1/state_schema.json)对应本批固定实现。两版Dev及修订原因完整保留，Test解锁前停止选择。

## 主要证据

- `factorial_results.json`、`paired_results.json`、`paired_effects.json`：30几何、135配对决定、固定seed的几何组重采样区间。
- `mask_metrics.json`、`onset_metrics.json`、`uncertainty_results.json`：实例/起笔/关系与覆盖，不用unknown召回替代完整可靠性。
- `predictions.jsonl`：2430正式记录；`history_predictions.jsonl`：19440前缀，去除重复完整audit，仅保存audit条数；完整最终audit在`ledger_audits.jsonl`。
- `raw_model_outputs.jsonl`、`onset_evidence.jsonl`、`onset_instance_evidence.json`、`oracle_absent_signal_evidence.json`：固定头输出、概率、实际RGB变化和逐实例区间；oracle含正确区域特权。
- `failure_cases.json`、`failure_analysis.json`、`confirmation_lags.json`：全部失败、机制及确认延迟，包含错误提前。
- `train_curves.json`、`training_runs.json`、`models_frozen.json`、`ledger_rules_locked.json`、`ledger_rule_amendment.json`、`test_unlock.json`：预算、选择和锁定时间；不存在测试后训练或规则选择。
- `resources.json`、`timing.json`、`memory.json`：共用编码成本与缓存后成本的边界。

## 已执行命令

以下记录实际流程；现有目录设有训练/测试防覆盖锁，不能把重复执行当成新的独立实验。原始视频、PNG和标签均已提供，冻结特征及模型权重仅在本机checkpoints，外部复现需要同版本底座、T6选定权重和独立输出目录。底座配置沿用T6：Show-o2视频1.5B发布名，完整3,063,740,640参数，权重revision `412f647429897ad888771d18008de4edfb2c42a6`。

```bash
checkpoints/Show-o-env/bin/python scripts/h1_t7_attribution.py
checkpoints/Show-o-env/bin/python scripts/h1_t7_data.py build
checkpoints/Show-o-env/bin/python scripts/h1_t7_data.py contracts
checkpoints/Show-o-env/bin/python scripts/h1_t7_features.py extract
checkpoints/Show-o-env/bin/python scripts/h1_t7_features.py contracts
checkpoints/Show-o-env/bin/python scripts/h1_t7_experiment.py train
checkpoints/Show-o-env/bin/python scripts/h1_t7_experiment.py compact_train_dev
checkpoints/Show-o-env/bin/python scripts/h1_t7_experiment.py ledger_dev
checkpoints/Show-o-env/bin/python -m unittest discover -s tests -p test_h1_t7.py
checkpoints/Show-o-env/bin/python scripts/h1_t7_experiment.py evaluate
checkpoints/Show-o-env/bin/python scripts/h1_t7_score.py
checkpoints/Show-o-env/bin/python scripts/h1_t7_analysis.py
```

L初版和修订版各一次Dev重放；精确差别见修订JSON。静态科学图使用Matplotlib 3.10.7。核心运行环境为Python3.12、PyTorch2.7.1、NumPy2.5.4、Pillow12.3、PyAV19.0.1；UMM/CPU与MPS路径沿用T6，无主干训练。

文件新增与修改说明见最终报告末表。没有删除文件或覆盖T6；本轮不自动启动新seed、D1或生成。
