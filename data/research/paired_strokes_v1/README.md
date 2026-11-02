# paired-strokes-v1 CPU候选数据

256字、2243笔、1504条离线请求。最新状态见`current_status.json`，初始构建快照见`build_record.json`；定义见[协议](../../../docs/research/paired_strokes_v1/protocol.md)。已归档1名独立审核者的16字/54笔审核，E3/E5各16字通过，E4为14字通过、“未”unknown、“一”不适用；其余240字待审。全部仍属开发数据，无正式保留集。

| 文件/目录 | 内容与读取权限 |
|---|---|
| `complete_suite_v1/` | 2232条完整离线请求与标签、PRE-01至PRE-07、72张oracle高亮图和分层；额外权限单列，主表仍只用原1504条 |
| `s1_completion_2026-11-02/` | CPU与人审分别验收、240字分批登记、208项CPU/浏览器/接收检查、未执行资源提案 |
| `current_status.json`、`human_review_2026-11-02/` | 当前人审数量、原件来源、未知项和按指标资格叠加登记，不批量升级原构建快照 |
| `smoke_pairs_reviewed.jsonl` | 16对数据侧合格D-SMOKE，仅字图+五类描述；拟合尚未执行 |
| `pilot_train_pairs_reviewed.jsonl`、`pilot_validation_pairs_reviewed.jsonl`、`pilot_test_pairs_reviewed.jsonl` | 接收PAIR后按原split分别导出的合格图文对，目前均为空；PAIR不授予空间/方向资格 |
| `manifest.jsonl` | 全部来源、许可、字符/模板分组、规范序列与资格；不直接喂给模型 |
| `training_pairs.jsonl`、`data_schema.json` | 仅192个训练候选的字图+描述；训练端只读此类窄导出或上述已审核16对，不读完整manifest或评价目录 |
| `media/` | 256张256×256黑字白底图；文件名和PNG元信息无答案字符 |
| `splits.json` | 192/24/24开发分区及16字审核区，不含正式保留集 |
| `source_subset.jsonl`、`licenses/` | 固定revision的256字SVG/medians子集与未修改许可；几何不属于原配对训练监督 |
| `source_licenses.csv`、`model_metadata.json` | 逐源用途/限制与S0模型revision/许可，不是运行验证 |
| `requests.jsonl` | 已准备、未执行的评价请求；输入只取`model_inputs` |
| `evaluation_only/labels.jsonl` | 固定请求答案，禁止泄漏到模型输入 |
| `evaluation_only/geometry.jsonl`、`evaluation_only/masks/` | 构建时的mask/路径/关系候选及版本；后续逐指标资格另读审核记录，不改写来源快照 |
| `evaluation_only/normative_extracts.jsonl` | 规范数字编码与页码事实，独立于SVG提取 |
| `evaluation_only/sequence_collisions.jsonl` | 同序列异字碰撞；去尾字兼容，不能标成负例 |
| `evaluation_only/reviews.jsonl` | 审核者1的48条实际记录及逐项判断/备注；46条accepted，2条unknown（含单笔不适用） |
| `evaluation_only/review_template.jsonl`、`review_schema.json` | 48条待填审核记录及正式审核字段要求；待填记录不算提交 |
| `source_rejections.jsonl` | 逐字排除/冲突原因，保留全来源分母 |
| `build_record.json`、`scope_record.json`、`verification.json`、`*.log` | 构建、授权范围、实际验证与失败说明 |

来源字形及衍生媒体采用Arphic Public License，版权属Arphic Technology Co., Ltd.，修改说明嵌入源码子集、PNG和NPZ；保留`licenses/`原文。规范原PDF及页面图仅在私有目录查阅。本目录的候选几何不能自我认证为独立金标，也不报告模型成绩。
