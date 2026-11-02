# 16字独立逐笔审核接收报告

收到用户“审完了”及`S1_stroke_review_1.json`，审核者代号`1`，导出时间2026-11-02 19:47:52.840（北京时间）。文件声明审核者未参与候选标签构建，并已亲自对照规范核查。按本协议的单名独立审核要求登记，不宣称双人一致性或独立来源分割标注。

**16字、54笔的实例/笔序及规范起终点审核完成；E4有14字通过，“未”保留无法判断，“一”不适用。16对D-SMOKE在数据侧具备资格，尚未拟合或运行模型。其余240字仍为未审候选。**

## 实际记录

200项手工选择全部完成：199项符合、1项无法判断、待填0、明确有误0。导出48条字×指标记录，46条accepted、2条unknown；其中1条unknown是单笔字E4不适用。

| 范围 | 审核结果 |
|---|---|
| 五类规范序列 | 16字通过 |
| 实例身份与规范笔序（E3） | 16字、54笔通过 |
| 规范起终点与方向（E5） | 16字、54笔通过 |
| 笔画关系（E4） | 14字通过；“未”unknown；“一”不适用 |
| 完整性 | 200项原始判断、48条汇总、0待填；原始与汇总一致 |
| 来源与版本 | package revision、审核者声明、规范页码/字表序号、geometry revision及笔号覆盖均匹配 |

用户原文件按字节保留在`private/paired_strokes_v1_2026-11-02/human_review_1/S1_stroke_review_1.json`；登记文件仅计算一次原件校验值，未重复扫描图像或模型缓存。48条审核原文及逐项判断写入[evaluation_only/reviews.jsonl](../../../data/research/paired_strokes_v1/evaluation_only/reviews.jsonl)。此前该文件为空，未覆盖旧审核者记录。

## “未”的未知项

结构化原始选择为`465a1d3fe7badc02:pair:2:4 = unknown`。审核者原话完整保留：

> 蓝色第2笔，相对橙色第4笔的中线更长：未知（容差带）；可能是长一点但没有差别不大

冻结几何中，这一笔画对的longer候选为true。备注中的“未知（容差带）”与该候选值不同；接收时以实际选择unknown登记，并保留原话。没有将接近的判断改成true，没有修改5%容差、候选几何或评价答案。

按既有整字/指标资格规则，“未”的整个E4保留unknown，涉及本轮6条请求暂不计分；不在读到审核结果后改成只排除单个关系。E3/E5已分别通过，继续保持其独立资格。单笔“一”没有实例对，E4不适用不算关系错误。

## 可评分范围

下面统计的是标签资格与分母，模型预测和得分仍为空：

| 指标 | 冻结请求 | 当前可评分 | 真值容差带未知 | 审核资格不足 |
|---|---:|---:|---:|---:|
| E3 | 54 | 54 | 0 | 0 |
| E4 | 108 | 84 | 18 | 6 |
| E5 | 54 | 54 | 0 | 0 |

E4可评分84项中，重复笔型58项、其他笔型26项。18项落入原先冻结的几何容差带，保留ambiguous_gold；另外6项因“未”的整字E4 unknown保留unqualified_gold。合计108，分母没有缩小。

审核后资格作为[叠加登记](../../../data/research/paired_strokes_v1/human_review_2026-11-02/qualification_overlay.jsonl)保存；原始`manifest.jsonl`、`geometry.jsonl`、`build_record.json`等继续表示构建时快照，不批量改写256字为已审核。最新数量见[current_status.json](../../../data/research/paired_strokes_v1/current_status.json)。

16对已审核训练单元另存[smoke_pairs_reviewed.jsonl](../../../data/research/paired_strokes_v1/smoke_pairs_reviewed.jsonl)，只含原字图与五类描述，不增加实例/方向/关系训练监督。它们是已暴露的开发字，不能变成新的正式保留测试集；合格D-PILOT仍为0，额外240字和独立字体来源缺口仍保留。

几何来源仍为SVG。审核支持这16字对应的实例绑定与规范方向资格，没有产生独立手工像素mask，Mask AP不据此获得执行资格。单名审核者的结果也不能提供双人一致性统计。

## 本轮变更与检查

- `evaluation_only/reviews.jsonl`：归档48条实际独立审核记录，保留原始判断与备注。
- `human_review_2026-11-02/intake_record.json`、`qualification_overlay.jsonl`：新增接收来源、版本/覆盖一致性核对及16字资格。
- `current_status.json`、`smoke_pairs_reviewed.jsonl`：新增当前状态和16对可用于后续获准FIT的数据导出；模型指标保持null。
- 本报告、模块README、数据README、冻结协议的状态说明、原执行报告的追加入口、审核操作说明、AGENTS、根README、工作区交接及`docs/research/next/README.md`：更新当前人审入口；初始构建/审核包准备记录保留为历史快照。
- `human_review_2026-11-02/checks.json`、`cpu_tests.log`及`reports/validation.json`：保存本次专项CPU回归、脚本语法和目录链接检查结果。
- `scripts/paired_strokes/check_review_form.cjs`：将“正式审核文件必须为空”改成“界面测试前后正式审核文件一致”，适应已有真实记录；模拟导出仍在私有测试目录，不计人工提交。

接收核对只在入口进行一次，检查200项原始判断与48条汇总、规范/版本/笔号覆盖一致性。适用CPU回归与目录链接检查见本次[检查记录](../../../data/research/paired_strokes_v1/human_review_2026-11-02/checks.json)。没有为此次材料接收扩大模型测试或重复全缓存哈希。

无文件删除。P0/P1/Batch A状态、阈值、失败与原人审均不变。新增模型调用、GPU/MPS、训练、收费资源、远端推送及main操作均为0，S2–S6未启动。
