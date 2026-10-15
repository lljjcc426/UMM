# 文献与研究数据

`literature.json` 为主数据，包含269项论文／研究记录和11项资源。每项记录保留研究内容、来源、版本、核查范围、历史编号及 `evidence_history`。

| 文件 | 内容 |
|---|---|
| `literature.csv`、`literature_public.xlsx` | 主目录的表格视图 |
| `umm.*`、`resources.*` | UMM研究和资源分类视图 |
| `new_handwriting.*`、`local_additions.*` | 重点书写研究与补充文献视图 |
| `historical_public.*` | 2026-10-14文献目录的53条公开记录 |
| `record_aliases.json` | 来源编号与主目录编号的对应关系 |
| `provenance.json` | 来源记录、去重标识及数量 |
| `excluded_records.json` | 撤回研究及排除原因 |
| `public_video_audit_manifest.json` | 公开样例的来源、帧率、分辨率与抽帧记录 |
| `discovery/` | 尚待筛选或核读的候选题录 |
| `experiment_template.csv` | 实验记录模板 |

分类视图和候选题录与主目录存在重叠，不能相加作为文献数量。Markdown、CSV和Excel由 `scripts/render_catalog.py` 生成。

核查字段的含义见[文献整理与核查方法](../docs/evidence/method_and_status.md)。
