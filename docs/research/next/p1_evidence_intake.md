# P1证据接续与范围校正

2026-11-01。本轮在`exp/p1-process-diagnostic`准备研究重启，父提交`d40d7647`包含尚未推送的P1结项和工程成果。只读查询并fetch了远端：main=`ce2bc8a8`，P1=`9c206155`；main新增两项生成模型文献整理提交，与本地历史分叉，未合并或重置。新工作不宣称正式进入P2，不修改P0/P1契约、发布清单、原始结果或阈值。

## 实际历史分母

| 条件 | 初始尝试 | 有效原片 | 技术失败 | 权限 |
|---|---:|---:|---:|---|
| 普通文本 |24|24|0|G0|
| 顺序文本 |24|24|0|G0|
| 全白i2v |8|7|1|G0|
| 空间模板文本 |8|8|0|G1|
| 合计 |64|63|1|分表|

另有28次理解、8次codec、8段CPU对照。失败槽位为`N076-T_G0_blank_i2v-s11`，采证包装器对list调用`.numel()`，未重试；不能删除分母，也不能记作笔顺错误。

两位真人已经看过压缩包，用户转述结果一致：8段可识别且大致合适的视频全部对应CPU对照，63段UMM有效原片未进入可接受集合。另1槽位缺片。七维逐视频JSON提交为0；没有将聊天粗筛补成逐笔记录，也没有沿用P0的独立性确认替P1作证明。0/63是本批粗筛未发现可接受UMM视频，不能换算为可观察笔顺准确率0%。新人工任务为0，无需重新打开旧页面或重做142项。

## 启动包与当前状态的差异

启动包按`9c206155`的服务器交付快照描述P1 pending；本地`ed92bd8a`已按用户批准作有限负结果结项。当前正式状态保持`closed_with_negative_results`，BASE-01 `completed_negative`，SO-00/EVAL-02/SO-01 `completed_with_limitations`。原科学指标未达标、最终报告审阅和main合并未批准。旧文件内pending字段保留为历史快照。正式细分成功率继续为null；该null不抹去已有双人粗筛。

## 本次独立抽检

实际解码以下4项各33帧并检查单调PTS、尺寸；含原生T2V、原生全白I2V、确定性CPU对照、codec重建：

- `private/p1_native_pilot_issue3_2026-10-30/requests/N076-T_G0_native_simple-s11/`
- `private/p1_full_server_2026-10-30/requests/N019-T_G0_blank_i2v-s11/`
- `private/p1_full_server_2026-10-30/diagnostics/controls/O-N076/`
- `private/p1_full_server_2026-10-30/requests/SO00-codec-N076/`

理解样例`SO01-C-N076-full_prefix`的实际采样记录和RGB数组可访问；公共28项原答/采样记录、20配对和8项字面时长冲突继续引用旧证据。本轮没有重新作真人内容判断。历史2192份逐文件SHA核对属于原P1执行，本次未重复全量校验。

机器清单：[p1_evidence_intake.json](../../../data/research/next/p1_evidence_intake.json)。私有映射与原片均未发布。八字旧数据、工程Arphic几何、同源扰动只能进入开发/回归；它们不构成新保留集。

## 原审核工具的复用

保留`scripts/p1/export_review.py`及两份原离线包，新增`scripts.diagnostics.reviews`离线导入验证器。验证原schema、单人原始代号、七维独立选项、unknown/NA理由、缺片不能填写、修改/重复版本保留、current与末版本一致。双包比较仅报告分歧，不自动仲裁；不同代号不证明不同真人或审核独立。映射在私有输入参数中，不放入盲审包。

本次对两个真实cards.js分别运行空导入契约检查，每包72槽位、71可播放、1缺片；空对象是程序测试，并非实际人审提交。35项新单测中的模拟身份均明确为TEST_ONLY，未写入P1目录。无真实新导出时正式指标null，不凭空制造“已导入”记录。
