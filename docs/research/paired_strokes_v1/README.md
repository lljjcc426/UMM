# 汉字笔画图文配对 S0–S1

最新：[第一批20字审核接收](batch_01_review_receipt_2026-11-03.md)。累计36字/130笔，合格pilot图文对20，仍220字待审；本批6字关系unknown按原规则保留。难以确认的几何关系可先未知或待填，PAIR/E3/E5分别接收。

11月2日[CPU补齐与审核包准备](s0_s1_completion_2026-11-02.md)已完成，完整离线套件2232条。12批审核包中第1批已返回，原16字无需重审。

最初16字/54笔审核的范围见[接收报告](human_review_receipt_2026-11-02.md)，D-SMOKE数据侧16对具备资格。原执行记录见[报告](execution_report_2026-11-02.md)，可复现定义见[协议](protocol.md)；当前仍无正式保留集或模型得分。

审核包的转交步骤与准备时文件变更见[审核交接说明](human_review_guide.md)。构建与审核包准备记录中的0保留为历史快照；最新人审数量见[current_status](../../../data/research/paired_strokes_v1/current_status.json)。

| 产物 | 入口 |
|---|---|
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
