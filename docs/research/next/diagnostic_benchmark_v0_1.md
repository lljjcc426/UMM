# 理解—生成双向诊断 Benchmark v0.1

2026-11-01，`diagnostic-v0.1-dev3`。这是已暴露材料上的开发诊断，不是独立泛化测试或已验证的模型排行榜。

## 已实际材料化的任务

| 轨道 | 数量 | 输入→输出 | 资格与比较边界 |
|---|---:|---|---|
| K-CHAR |8|无答案字图→字符|中性ID/文件名，无字符元信息；仅测识别|
| K-ORDER |8|字符→实例描述、顺序、方向|规范候选需核准；自由描述须独立语义/几何绑定，不能要求模型猜源ID|
| V-STRUCT |8|静态图→端点、身份、关系|静态结构不能给出实际时序|
| H-ACTUAL |26|实际RGB→事件、方向、未知|8字各正确/交换两段；另10段无汉字几何微任务|
| G-GLYPH |8|字符→静态图|独立静态任务，不计视频成功|
| G-ATOMIC |4|单线/双线指令→原生过程|左→右、右→左、两线先后、竖线增长，分开汉字知识|
| G-STROKE |8|字符→完整书写原生视频|新调用0，复用P1背景；全部初始尝试分母|
| X-RECOVERY |4|显式状态/动作→诊断或同步重做|合法、Policy、Draw、不可归因；显式交错接口另验|
| 合计 |74|13个来源组|26段CPU视频，0个新模型输出、0个正式保留样本|

固定构造/列表顺序种子20261101。字为士、丑、小、以、广、刃、乞、点。汉字几何来自已保存的Make Me a Hanzi/Arphic PL Kai衍生预览目录，revision=`bddc96d41bef78427ed0e034e9f7e31d71fd1b92`，遵守Arphic Public License及原修改声明。规范文件GF0023-2020与明确的AI实例绑定分列；源数组下标、路径方向、记录顺序不能自行变成规范。继承资格`AI_reviewed_engineering_preview`，没有升级为真人逐笔金标。P1原对照使用CASIA开发路径；本次Arphic几何与其不同，不能把几何变化当独立真值或新保留来源。

## 信息接口

`model_inputs/<opaque_id>/request.json`只允许id、track、prompt、media、geometry_permission及合法当前状态字段。输入图片不带字符名、答案元数据、字幕或彩色笔号。K-CHAR prompt也不含目标汉字。H-ACTUAL不接收规范答案、事件日志、未来帧或评价路径。

`training_targets/`只存8个正例的开发接线监督，均`eligible_for_formal_training=false`；`evaluation_only/`保存目标参考、构造事件及资格。`manifest.jsonl`是审计索引，含字符/来源/评价路径，严禁把完整manifest送入模型。推理仅获取单条输入及其media。同源正确/交换/衍生记录属于同一group，不跨训练/验证/测试。

四类表示独立：规范程序、计划事件、实际RGB观察、最终评价。构造日志只说明渲染意图。汉字样本的`observed_events=null`，等待合格的独立判断；不使用日志填充。几何微任务的RGB由FFmpeg实际解码，再按明确O权限的无序空间区域测量，随后才与单独的顺序规则比较。该观察器未读取构造日志，但与构造共享简单几何设计，不能声称来源完全独立或跨真实生成域可靠。

## 像素实验与未知

10例包括正确、交换、反向、漏画、多画、整图突现、旧墨迹消失、两帧低采样、空白、两线同时增长。相同末帧异历史由持续墨迹重渲染构造，未乱序真实帧。所有视频实际编码/解码；33帧样本PTS为0…32/12秒，低采样例保留2帧，无插帧。

CPU实测：交换=顺序错误；反向=方向错误；漏/多画及空白=完整性错误；消失=历史保持错误；整图突现和两帧例的顺序/方向未知。密集视频中的两线同时增长有多帧证据，判顺序要求违反；它与低采样的同帧出现区别记录。初版把所有同时出现记unknown的不足已保留在开发失败/版本记录中，修订结果另存，未动旧P1阈值或保留预测。

像素灰度阈值128、出现占区域比1%、方向至少2个部分增长帧和位移>1像素，仅用于分离线条开发夹具。它们未在人类/模型输出域校准，不能用于正式评分。八字描画中有相交/遮挡，当前工具明确弃用此简化观察器作汉字自动裁判。

## 评价口径

`summarize`按全部实际初始尝试计联合成功下界；完成、失败、unknown和NA分别保留。未运行的授权槽位另列，不能混成已调用分母。方向/顺序/身份/完整性/历史/时间/字形分别报全部分母正确率、清晰覆盖和条件正确率；费用缺失则cost_complete=false。技术失败不自动成为笔顺错误。

无真实合格逐项审核时formal_primary_metrics=null。一般自然语言答案不经未经校准的正则打分，记unparsed/unknown；K-ORDER自由描述需合格绑定；H-ACTUAL没有独立事件答案时不替换为构造事件。G任务必须读取真实输出，并使用独立实际RGB主评。程序可验证媒体和测量契约，不负责创造规范资格。

## 运行

```bash
.venv/bin/python -m scripts.diagnostics.build --output private/diagnostic-new-development
.venv/bin/python -m scripts.diagnostics.audit --dataset private/diagnostic-new-development --output private/diagnostic-new-audit
.venv/bin/python -m scripts.diagnostics.prepare --dataset private/diagnostic-new-development --output private/diagnostic-new-proposal
.venv/bin/python -m unittest tests.test_diagnostic_benchmark -v
```

已有产物在`private/research_restart_2026-11-01/benchmark_v02`及`cpu_audit_v03`；可直接阅读，复跑须用新目录。可选`audit --predictions <JSON>`只导入`[{"id":"…","response":…}]`，没有模型调用功能。

## 正式保留集要求

目前新保留集0。下一正式比较前，应先固定检查点/训练数据/阈值/评价协议，另批授权取得无开发暴露的字×独立几何或书写者×记录来源，提供逐实例规范、方向及实际事件资格。旧640字、P0人审、144份、P1八字和本次74条全部登记暴露，不能再作为新的独立保留集。Pot1.0Test仅余两名候选作者的旧审计限制仍在，不能从同归档凑出64个独立作者。正式数量应由开发效能和人工预算决定，不能把74项包装成足量统计证据。本轮没有下载、建立或分派正式保留核验任务。

最终输入采用无损H.264 CRF0/yuv444p；8组汉字配对经实际解码，末帧逐像素相同且过程不同，见[same_final_pair_audit.json](../../../data/research/next/same_final_pair_audit.json)。初版有损编码有8/8组微小末帧差异，已保留原片与未执行包；该问题在任何新模型调用前修复。最终26段为唯一开发视频槽位，先前26段及各轮输入载体是保留的调试版本，不计独立样本。
