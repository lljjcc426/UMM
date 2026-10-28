# P0 规范候选与受控RGB数据 v1

生成于2026-10-27 UTC（北京时间任务跨至2026-10-28）。**工程制品已构建，独立人工核验尚未完成，不能当作已审定的规范笔顺金标准或完整跨字体数据集。**

640个不同字符与来源字形组：观察器开发64、观察器保留64、模型训练320、模型验证64、模型字符保留128。后512字与观察器用字完全隔离。按2–5、6–8、9–12、13–20笔四层等额分配，随机种子20261027。范围限GF0023—2020索引中前3500一级字与固定源的交集，实际所选字清单见 [splits.json](splits.json)。

## 来源、许可和修改

来源：[Make Me a Hanzi graphics](https://github.com/skishore/makemeahanzi/blob/bddc96d41bef78427ed0e034e9f7e31d71fd1b92/graphics.txt)，固定revision `bddc96d41bef78427ed0e034e9f7e31d71fd1b92`。完整来源文件30,778,076字节、9,574行；本目录只保留640字所需几何。

图形继承 **Arphic Public License**，版权归Arphic Technology Co., Ltd.等原权利人；[上游COPYING](licenses/COPYING)与[未改动的许可全文](licenses/ARPHICPL.TXT)随包保留。修改日期2026-10-27：抽取子集，增加稳定ID、角色划分、合成时序及两种栅格过程；修改说明置于模板文件、manifest记录和媒体元数据。衍生几何/媒体按APL分发，无担保。未引入另受LGPL约束的dictionary数据，也未分发字体文件。

[官方GF0023—2020规范](https://www.moe.gov.cn/jyb_sjzl/ziliao/A19/202103/W020210318300204215237.pdf)只供核对，完整PDF保留在本地参考缓存，未随数据发布。索引中的字符、序号和页码已核；源几何的逐笔顺序及方向尚待独立比较，`allowed_orders_candidate`不能自动升为正式规范允许集。

## 文件与媒体

- [templates.json](templates.json)：源轮廓、medians、稳定笔画身份、规范索引与待核状态。
- `manifest_observer_dev.jsonl`、`manifest_observer_holdout.jsonl`：704与1,408份受控RGB媒体，分别含64与128份静态空白对照。
- `manifest_model_train.jsonl`、`manifest_model_validation.jsonl`、`manifest_model_character_test.jsonl`：320、64与256段正例候选；最后128个字符各有两种渲染方法。
- 共 **2,752份**无损RGB媒体：**2,560份动态APNG＋192份单帧空白PNG**。全部实际RGB另存于随研究分支保留的[rgb_media.tar.gz](rgb_media.tar.gz)，媒体原件仍在本机 `private/p0_data_eval_2026-10-27/media/`；逐文件路径、大小以运行登记为准，manifest保留一次生成时的SHA256。本轮全量解码141,423帧与清单一致，动态时序异常0。
- APNG合并连续重复帧，故帧间隔可变；以`frame_timestamps`与`frame_durations`为准。192份静态空白未编码时长，不构成时序证据；本轮不补帧重建。原始合成网格为83ms（名义12fps经整数毫秒量化），没有真实笔压/接触/速度传感数据。
- [人工核验页面](review/index.html)、[旧标注文件](human_annotations.json)：原640项规范＋2,112项RGB队列收到38条全局试标（规范6、RGB32），原文保留。其后全量AI审核包为640字＋2,752份媒体；默认真人队列已减量，12张首审＋6张第二位复核均完成，六段获双人整体过程正确判断，完整分项金标未推定。当前剩余卡片0，未重新启用全量人工队列。
- [受控小样例](../../../../examples/p0_data_eval/examples.json)可随Git查看；完整媒体已随分支打包，原始来源及第二份完整迁移归档仍保留本地private。

## 数据权限与隔离

`model_inputs`只含字符与指令。T从空白生成，不读目标图、源轮廓、事件边界或构造日志；P适配器仅允许prefix_end及之前的帧。训练目标路径与评价用事件、规范引用、错误构造标签独立存放。RGB观察器仅获得解码像素与G1静态参考几何，观察完成后才关联构造标签计算指标。

同一来源字形的所有换序、反向、速度/外观及渲染变体保持在同一角色，不跨训练/验证/保留集。已覆盖字符保留及字符＋合成渲染方法变化；独立同字字体/书写者、真实记录ID保留尚无素材，不用笔宽变化冒充这些格子。基础模型预训练是否见过这些字未知。

## 复现与核验

新检出本分支后可先运行 `tar -xzf data/research/datasets/p0_stroke_synthetic_v1/rgb_media.tar.gz -C .` 恢复manifest所引用的媒体及许可，无需重新生成或重新评分。

重建研究须使用隔离检出并保留旧记录，不能直接覆盖当前候选、冻结文件或保留集预测。在仓库根目录使用具备NumPy与Pillow的Python运行 `python -m scripts.p0.build_data prepare --norm-text <本地规范提取文本>`，再按角色运行 `media --role <role>`；已有媒体目录会保留，重建使用独立工作目录。源获取命令及失败恢复见运行登记。

观察器先执行 `python -m scripts.p0.evaluate calibrate`，冻结开发集选择的阈值，再执行 `evaluate`。已有保留集预测文件时拒绝覆盖。结果属于固定相机、已知参考几何和受控合成域；不证明真实生成视频或任意书体可自动评分。

**当前入口**：[最终固定人工包](http://127.0.0.1:8770/)，启动 `python -m scripts.p0.final_review_server --port 8770`。[新报告](../../../../docs/research/v2/p0_final_human_package_2026-10-28.md)列出每位真人64字规范＋144份RGB＋8份独立记录核验＝216项，两人共432提交，涉及72个不同字。此包使用单列的CASIA扩展，未替换本数据集640字/2,752媒体。原12＋6卡片仍在8768按原口径保存；下方旧队列说明仅为历史，不另加任务。

人工页面可直接打开本地HTML，动画与规范候选可查看；逐帧滑块建议通过本地HTTP运行：`python -m http.server 8765 --bind 127.0.0.1`。旧页面仅保留历史进度。正式审核使用 `python -m scripts.p0.review_server --port 8766` 与 http://127.0.0.1:8766/ ，先查看示意并完成犬、怀、热、蔽的非保留集练习。提交记录追加保存在本机private，导出v2 JSON用于入库；测试标签与科研记录隔离。

[本轮报告](../../../../docs/research/v2/p0_data_eval_report_2026-10-28.md) · [执行登记](../../runs/p0_data_eval_2026-10-27/task_record.json)。

历史[审核准备与工作量](../../../../docs/research/v2/p0_human_review_preparation_2026-10-28.md)保留当时全量方案、顺序及保存方法，当前人工量以上述减量批次为准。旧试标不预填正式任务，不计入前瞻校准统计。
