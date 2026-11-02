# 汉字笔画图文配对 S0–S1

本轮执行记录见[报告](execution_report_2026-11-02.md)，可复现定义见[协议](protocol.md)。当前为 CPU 数据与评测器准备；独立逐笔金标尚缺，S1未取得完整科学准入。

2026-11-02：用户可以安排独立审核者，已提供离线填写、进度恢复及JSON导出的新版审核包。转交步骤与文件变更见[审核交接说明](human_review_guide.md)。实际审核提交仍为0。

| 产物 | 入口 |
|---|---|
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
