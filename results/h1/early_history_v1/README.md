# T6：早期历史记忆

当前为执行中。[训练前协议](../../../docs/experiments/h1_t6_early_history_protocol.md)与preregistration.json固定范围和预算；各阶段独立提交，既有T1—T5保持。

- 数据：data/h1/early_history_v1，20／8／20几何组，另2组三笔诊断。
- data_contract_checks.json：RGB、参考、查询、时间、冻结特征与B3全部输入的严格相等，以及可观察性门槛。
- data_contract_initial_failure.json：首轮前缀核对错误的失败证据。第15观察只有前4笔，最初将其与5笔全序比较；改为与源日志中已实际出现的实例子序列核对。原RGB及标签均未修改，不涉及根据学习成绩改评分。
- pixel_states.json／oracle_ledger_predictions.json：独立像素可观察状态与oracle事件表的逐前缀记录。

复现顺序：h1_early_history_data.py build → contracts → h1_early_history_features.py → h1_early_history_contracts.py oracle → h1_early_history_contracts.py features。特征、权重保存在忽略的checkpoints/h1_early_history_v1，Git只保存清楚D0视频、实际采样PNG、代码及证据。不要覆盖已有固定运行目录。
