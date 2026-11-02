# S0–S1全量补齐与剩余人审

后续进展（2026-11-03）：[第一批20字审核已返回](batch_01_review_receipt_2026-11-03.md)，累计36字/130笔，合格pilot图文对20，仍220字待审；本页以下保留11月2日CPU补齐时的数量快照。

用户追加要求：“S0–S1完成了没，没有的话全部完成”。本轮延续已授权本地CPU工作，核对原计划H节的S0/S1、B节评价、C节数据与D节离线测试定义。

**S0已完成；S1代码、配对构建和离线评价准备已补齐。256字中仍只有16字有实际独立逐笔审核，240字尚无审核记录，因此当前全量数据审核未完成，不能把S0–S1整体标为全部完成。**唯一需要继续交还的外部材料是实际独立审核结果；本轮已经生成完整240字材料和可接收部分进度的工具。

原计划D-PILOT的200–400字和D-MAIN规模是分阶段建议，不能将≥1500字、独立字体、模型推理或最小拟合追加为本轮CPU验收要求。本次全量补齐以当前已经选定的256字为界；同一来源、五类笔形、开发分区与已有未知项均保留。

## 逐项核对

| 项目 | 当前结果 | 证据 |
|---|---|---|
| S0来源、许可、规范及模型元信息 | 完成；未获资格的CCD/CCSE等没有导入，单一Arphic来源限制保留 | [协议](protocol.md)、[来源登记](../../../data/research/paired_strokes_v1/source_licenses.csv)、[模型登记](../../../data/research/paired_strokes_v1/model_metadata.json) |
| schema、split、泄漏隔离、可复现渲染 | 完成；256字/2243笔，192/24/24与16审核字分开，无正式保留集 | [构建记录](../../../data/research/paired_strokes_v1/build_record.json)、原[执行报告](execution_report_2026-11-02.md) |
| 困难配对、序列/点身份/关系/方向评价 | 完成；原1504条请求、标签和阈值不改写 | [原清单](../../../data/research/paired_strokes_v1/requests.jsonl)、[评分器](../../../scripts/paired_strokes/evaluate.py) |
| 文字先验、oracle高亮及OCR健康检查 | 本轮补齐；PRE-01至PRE-07全覆盖，文字/高亮/OCR均单列 | [完整离线套件](../../../data/research/paired_strokes_v1/complete_suite_v1/preparation.json) |
| 笔画分层与成本准备 | 本轮补齐重复笔型、轮廓接触、短笔、同序列异字、预定相似字分组，以及请求量/输出上限 | [分层](../../../data/research/paired_strokes_v1/complete_suite_v1/analysis_strata.jsonl)、[未执行提案](../../../data/research/paired_strokes_v1/s1_completion_2026-11-02/inference_contract_proposal.json) |
| 已完成16字审核 | 完成；E3/E5各54项可评分，E4可评分84项、几何未知18项、审核资格不足6项 | [接收报告](human_review_receipt_2026-11-02.md) |
| 其余240字实际独立审核 | 待交还；材料和接收工具已完成，尚未创建新的真人记录 | [分批登记](../../../data/research/paired_strokes_v1/s1_completion_2026-11-02/review_batches.json) |

各项最新状态由[current_status.json](../../../data/research/paired_strokes_v1/current_status.json)和[验收登记](../../../data/research/paired_strokes_v1/s1_completion_2026-11-02/acceptance.json)区分CPU完成、实际审核覆盖及合格数据数量。完成审核可以得到accepted/disputed/unknown；完成数量与通过数量分别统计，不要求为结项强行通过。

## 本轮完成的CPU工作

完整套件共2232条请求：原主清单1504条、文字先验256条、OCR健康检查256条、oracle高亮216条。新增72张高亮字图，不绘制起终点或答案；高亮提供实例身份特权，评分只进入单独对照表。主表、按split分表和主终点bootstrap继续只用原1504条，避免新增对照混入主分母。E8只检查单字OCR，不计入主要终点。

分层标签中的重复笔型取规范五类序列；轮廓接触和短笔取SVG候选几何，资格明确为source-derived。短笔定义为中心路径弧长小于本字中位路径长度的0.5倍；相似字预先限为土/士、木/未/末、人/大。分层不构成新人工真值或额外训练字段。

如未来另行授权四个冻结模型，完整套件为8928次请求；以候选每次最多256输出token计，输出上限2285568 token。真实视觉/文本输入token、GPU小时、显存和金额尚未测量，保持空值。本轮没有执行这些请求。

评价示例（只处理未来已有回答，不发模型请求）：

```bash
.venv/bin/python -m scripts.paired_strokes.evaluate \
  --dataset data/research/paired_strokes_v1 \
  --suite data/research/paired_strokes_v1/complete_suite_v1 \
  --predictions /absolute/path/to/actual_predictions.jsonl \
  --output /absolute/path/to/evaluation.json
```

## 剩余审核怎么交付

离线包：`private/paired_strokes_v1_2026-11-02/S1_remaining_240_review_v1.zip`（约70.33MiB）。解压整个ZIP后打开根目录`index.html`。共12批，每批20字，已完成的16字未列入，不要求重审。

每个字第一项核对“完整字图为本字，五类序列与规范原页一致”。可以先完成这240项并导出，单独接收PAIR图文对记录；未完成的逐笔/关系项继续待审。完整逐笔覆盖包含2189笔及10154个笔画对，总14772个选择项。每对阅读全部六项关系后作一次选择。无法判断如实填写unknown。

PAIR不授予E3/E4/E5资格。审核者可继续分批填写实例身份/次序、起终点和关系；每批各自保存草稿，导出文件名包含批号，导入可以恢复进度。所有选择初始为空，无批量通过。返回各批导出的JSON即可。

收到真实文件后使用接收入口，例如：

```bash
.venv/bin/python -m scripts.paired_strokes.intake \
  --file /absolute/path/to/S1_stroke_review_1_batch-01.json \
  --archive private/paired_strokes_v1_2026-11-02/received_batch_01
```

入口核对原始选择与汇总、实际覆盖、规范引用和geometry revision，归档原件后追加新记录。它保留未知、争议和旧版本，不从未填项生成accepted。合格pilot训练/验证/测试对分开导出，训练文件只接收原train_development中的已通过图文对，避免审核后合并分区。

当前D-SMOKE合格16对，D-PILOT合格0，新增真人提交0。“未”的E4 unknown、单笔“一”的不适用及冻结几何未知继续保留；完成S1不要求把这些未知改成通过。没有模型预测，全部模型成绩仍为null。

## 检查与文件变更

208项全仓CPU测试通过；新增4项覆盖对照表不混主分数、OCR输出解析、PAIR部分导出与空间资格隔离、原始争议不能被汇总覆盖。一个浏览器工作流通过空白初态、图片加载、PAIR部分导出、恢复、批次草稿隔离及正式登记不变；浏览器模拟导出只进入私有目录，并以check-only方式验证接收，不归档为真人记录。规范页10/311和审核页面已作AI显示检查，不算人审。具体结果见[检查记录](../../../data/research/paired_strokes_v1/s1_completion_2026-11-02/checks.json)。

| 修改/新增路径 | 原因 |
|---|---|
| `scripts/paired_strokes/complete.py` | 新增离线对照、72张高亮图和分层生成 |
| `scripts/paired_strokes/evaluate.py` | 增加E8解析、对照权限单列、主表/CI隔离与分层输出；原指标阈值不变 |
| `scripts/paired_strokes/review.py`、`review_app.js` | 支持任意指定批次、独立PAIR核查及动态进度，原16字导出格式继续兼容 |
| `scripts/paired_strokes/review_batches.py` | 新增240字分批审核材料生成，复用本地规范PDF，不下载新数据 |
| `scripts/paired_strokes/intake.py` | 新增实际审核文件校核/归档、资格重算与按原split导出 |
| `scripts/paired_strokes/check_completion.cjs`、`tests/test_paired_strokes.py` | 新增一个浏览器工作流及4项必要CPU回归 |
| `data/research/paired_strokes_v1/complete_suite_v1/` | 新增完整请求、独立标签、72张oracle图和256字分层；生成中的标签/高亮草稿移入本套件`evaluation_only/`隔离保存，原1504条登记不移动 |
| `data/research/paired_strokes_v1/s1_completion_2026-11-02/` | 新增批次登记、验收、未执行成本提案、CPU/浏览器/接收检查记录 |
| `review_schema.json`、`current_status.json`、`pilot_{train,validation,test}_pairs_reviewed.jsonl` | 新增PAIR的明确范围、当前真实覆盖与分区导出；三个pilot导出目前均为空 |
| 本报告、模块/数据README、根README、AGENTS和工作区交接 | 更新本轮入口及“CPU完成/全量人审待补”的区别 |
| `private/.../S1_remaining_240_review_v1[.zip]`、`pilot_reference_pages_v1/`、`completion_ui_check/` | 新增实际转交包、178张规范参考页和界面检查证据；不进入普通Git提交 |

没有删除或覆盖原审核JSON、48条实际记录、256字原图、规范序列、split、原1504条请求/标签、原几何、P0/P1/Batch A证据或历史快照。S2–S6、GPU/MPS、训练、权重下载、付费资源、远端推送和main操作均未启动。
