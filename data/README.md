# 文献与研究数据

更新：2026-11-02。研究与实验入口见[当前导航](../docs/research/next/README.md)和[工作区交接](../docs/project/WORKSPACE_HANDOFF.md)。

| 目录 | 用途 |
|---|---|
| `research/next/` | 当前诊断准备与原冻结请求清单 |
| `research/runs/` | 实际实验执行、授权与失败记录 |
| `research/reviews/` | 对已有实验的追加科学复核 |
| `research/datasets/` | 历史数据清单与划分，保留引用关系 |
| `engineering/` | 工程验证与本地模型试验记录 |

`literature.json`为文献主数据，当前360项：333篇论文／研究、27项资源。每项记录保留来源、版本、核查范围、历史编号及`evidence_history`。本次只修正文档计数，未重渲染文献导出或修改主数据。

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

历史批次文件继续保留原路径。整理前本页原文见[导航快照](../archive/workspace_navigation_2026-11-02/data_README.md.txt)。
