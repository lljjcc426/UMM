# paired-strokes-v1 CPU候选数据

256字、2243笔、1504条离线请求。状态见`build_record.json`；定义见[协议](../../../docs/research/paired_strokes_v1/protocol.md)。全部为开发候选，独立人工逐笔审核提交为0。

| 文件/目录 | 内容与读取权限 |
|---|---|
| `manifest.jsonl` | 全部来源、许可、字符/模板分组、规范序列与资格；不直接喂给模型 |
| `training_pairs.jsonl`、`data_schema.json` | 仅192个训练候选的字图+描述；这是训练端唯一数据入口 |
| `media/` | 256张256×256黑字白底图；文件名和PNG元信息无答案字符 |
| `splits.json` | 192/24/24开发分区及16字审核区，不含正式保留集 |
| `source_subset.jsonl`、`licenses/` | 固定revision的256字SVG/medians子集与未修改许可；几何不属于原配对训练监督 |
| `source_licenses.csv`、`model_metadata.json` | 逐源用途/限制与S0模型revision/许可，不是运行验证 |
| `requests.jsonl` | 已准备、未执行的评价请求；输入只取`model_inputs` |
| `evaluation_only/labels.jsonl` | 固定请求答案，禁止泄漏到模型输入 |
| `evaluation_only/geometry.jsonl`、`evaluation_only/masks/` | 未独立审核的mask/路径/关系候选及其版本 |
| `evaluation_only/normative_extracts.jsonl` | 规范数字编码与页码事实，独立于SVG提取 |
| `evaluation_only/sequence_collisions.jsonl` | 同序列异字碰撞；去尾字兼容，不能标成负例 |
| `evaluation_only/reviews.jsonl` | 实际独立审核记录，目前为空 |
| `evaluation_only/review_template.jsonl`、`review_schema.json` | 48条待填审核记录及正式审核字段要求；待填记录不算提交 |
| `source_rejections.jsonl` | 逐字排除/冲突原因，保留全来源分母 |
| `build_record.json`、`scope_record.json`、`verification.json`、`*.log` | 构建、授权范围、实际验证与失败说明 |

来源字形及衍生媒体采用Arphic Public License，版权属Arphic Technology Co., Ltd.，修改说明嵌入源码子集、PNG和NPZ；保留`licenses/`原文。规范原PDF及页面图仅在私有目录查阅。本目录的候选几何不能自我认证为独立金标，也不报告模型成绩。
