# 汉字笔画图文配对 S0–S1

2026-11-04最新：[CPU方法接入报告及后续执行顺序](method_cpu_integration_2026-11-04.md)。原192条训练导出已接入，192/192 SVG重建一致，四路随机CPU特征/梯度检查完成且更新0；原型和程序视频均不算模型能力结果。下一步独立GPU授权后执行冻结S2，再推进强SFT基线和程序迁移，原数据与资格保持。

此前：[S2原生运行器CPU审核报告与扩大覆盖提案](s2_runner_preparation_2026-11-03.md)。用户已认可基线`7c843c37`；运行器和watchdog已实现，尚未实际加载或执行模型。原[S2准备及真值资格审核报告](s2_preparation_audit_2026-11-03.md)保留。现有256字/2243笔和开发划分保留。36字/130笔具逐项审核记录；220字概括确认用于开发配对接受，E3/E4/E5不自动取得独立真值资格。当前E3/E5各36字通过，E4为27通过/7未知/2不适用。

S2每模型36条请求、四模型最多144次，覆盖规范笔数/序列、实例、六种空间关系、方向、配对及视觉正控；尚无实际模型调用。D-SMOKE16对、D-PILOT240对（192/24/24）配对数据保留，正式保留集为0。

[CPU补齐报告](s0_s1_completion_2026-11-02.md)记录2232条完整离线请求。原[执行报告](execution_report_2026-11-02.md)和[协议](protocol.md)保留构建定义；当前仍无正式保留集或模型得分。

审核包的转交步骤与准备时文件变更见[审核交接说明](human_review_guide.md)。构建与审核包准备记录中的0保留为历史快照；最新人审数量见[current_status](../../../data/research/paired_strokes_v1/current_status.json)。

| 产物 | 入口 |
|---|---|
| S2接口核验、少量请求与逐模型GPU申请 | [模型配置](../../../configs/research/paired_strokes_v1/s2_models.json) · [准备登记](../../../data/research/paired_strokes_v1/s2_preflight_v1/preparation.json) |
| CPU验收、完整评测套件、240字审核批次 | [验收登记](../../../data/research/paired_strokes_v1/s1_completion_2026-11-02/acceptance.json) · [套件](../../../data/research/paired_strokes_v1/complete_suite_v1/preparation.json) · [批次](../../../data/research/paired_strokes_v1/s1_completion_2026-11-02/review_batches.json) |
| 已归档审核、当前资格与16对D-SMOKE | [实际审核](../../../data/research/paired_strokes_v1/evaluation_only/reviews.jsonl) · [最新状态](../../../data/research/paired_strokes_v1/current_status.json) · [16对导出](../../../data/research/paired_strokes_v1/smoke_pairs_reviewed.jsonl) |
| 256字图文候选、来源、规范及分组 | [manifest](../../../data/research/paired_strokes_v1/manifest.jsonl) |
| 192条窄训练导出 | [training_pairs](../../../data/research/paired_strokes_v1/training_pairs.jsonl) · [schema](../../../data/research/paired_strokes_v1/data_schema.json) |
| 来源许可与实际使用 | [source_licenses](../../../data/research/paired_strokes_v1/source_licenses.csv) |
| 开发分区 | [splits](../../../data/research/paired_strokes_v1/splits.json) |
| 空间/方向候选及独立审核入口 | [geometry](../../../data/research/paired_strokes_v1/evaluation_only/geometry.jsonl) · [待填记录](../../../data/research/paired_strokes_v1/evaluation_only/review_template.jsonl) |
| 1504条未执行请求 | [requests](../../../data/research/paired_strokes_v1/requests.jsonl) |
| 实际数量与限制 | [build_record](../../../data/research/paired_strokes_v1/build_record.json) · [范围记录](../../../data/research/paired_strokes_v1/scope_record.json) |

数据重建需使用**新的空输出目录**，保留已冻结产物：

```bash
.venv/bin/python -m scripts.paired_strokes.build \
  --graphics private/p0_data_eval_2026-10-27/sources/graphics.txt \
  --norm-text /Users/cc/.cache/umm-survey-20261023/223/R06-full.txt \
  --output private/paired_strokes_rebuild \
  --private-output private/paired_strokes_rebuild_review

.venv/bin/python -m unittest tests.test_paired_strokes -v
```

评价器接受保存好的 `{id, output}` JSONL，执行固定请求分母；这条命令本身不调用模型：

```bash
.venv/bin/python -m scripts.paired_strokes.evaluate \
  --dataset data/research/paired_strokes_v1 \
  --predictions /absolute/path/to/predictions.jsonl \
  --output /absolute/path/to/evaluation.json
```

相对字图路径的基准为dataset目录。模型输入只取request的`model_inputs`；完整请求索引、标签、manifest和gold不拼进提示。训练端只取训练导出，禁止递归读取整个数据目录。独立审核未完成时 E3/E4/E5 返回资格不足和空分值。
