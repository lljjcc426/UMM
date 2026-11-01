# UMM科研启动 D0–D5 执行报告

日期2026-11-01，分支`exp/p1-process-diagnostic`。本轮状态为**research_kickoff_prepared**。已完成获准的资料审计、小型CPU数据/评测开发、测试与下一批精确申请准备；没有新模型运行、训练、性能提升或正式阶段切换。

## 实际交付

| 项目 | 实际结果 | 证据/入口 |
|---|---|---|
| D0 | 核对64生成（63有效、1失败）、28理解、8codec、8CPU；私有4类样例各解码33帧；原采样可访问 |[接续报告](p1_evidence_intake.md)、[机器清单](../../../data/research/next/p1_evidence_intake.json)|
| D1 | 8轨道74样本、13来源组，26段CPU视频实际编码/解码，种子20261101；正式新保留样本0 |[Benchmark](diagnostic_benchmark_v0_1.md)、[清单](../../../data/research/next/stimulus_manifest.jsonl)|
| D2 | 8个具体模型/配置登记，锁代码/权重revision及许可/资源限制；官方接口与既往实测分开 |[矩阵](model_feasibility_matrix.md)、[注册表](../../../data/research/next/model_registry.json)|
| SC-CoIT | 21页全文＋关键图/掩码/算法视觉核对；Policy/Draw、CE/FM mask、same-step、回放和定义张力留证 |[方法审计](SC_COIT_method_audit.md)|
| D3 | CPU RGB观察/多维全分母评价、mock和准备适配器、原离线审核导入/版本/分歧检查、可运行CLI |`scripts/diagnostics/`、`tests/test_diagnostic_benchmark.py`、[CPU审计](../../../data/research/next/CPU_audit_summary.json)|
| D4 | 24次精确未执行请求及实际输入；普通SFT/LoRA/课程/恢复的公平对照与阻塞项 |[GPU申请](gpu_pilot_request.md)、[逐请求JSON](../../../data/research/next/gpu_pilot_manifest.json)、[训练对照](../../../configs/research/next/training_comparison.json)|
| D5 | 本报告、独立实验登记、版本/授权/失败记录及本地提交 |[登记](../../../data/research/next/experiments.json)、[版本](../../../data/research/next/source_and_version_record.json)|

## P1状态和双人审核

P0有限结项有效。P1在本地`ed92bd8a`已有用户批准的有限负结果结项；维持`closed_with_negative_results`，EVAL-02为`completed_with_limitations`，原科学指标未通过。启动包按旧`9c206155`写的pending未覆盖新状态。最终结项报告审阅和main合并仍未批准；本轮未伪填批准。

两位真人已看过各71段可播放视频（另1缺片槽位），用户转述一致结果已归档，8个粗筛正例全是CPU对照，UMM可接受集合0/63。没有七维逐笔导出、校准或单独的P1独立条件证明；正式细分指标null。没有把“未收到逐项JSON”写成“真人没看过”，也没有重新分派142项人审。新导入器只验证原格式/身份代号/理由/版本，不造审核者或结论，任何未来真实独立性声明应单独归档。

## CPU诊断结果与实测范围

26段CPU视频包括16段汉字正确/交换过程、10段几何微任务。33帧例保留真实PTS；稀疏例只有2帧，没有插帧。八字几何沿用Arphic工程目录，规范与逐笔绑定仍为AI开发资格，不能用程序生成或旧整体通过补成金标。

10个微任务中：正确例的顺序/方向/完整性/保持通过；交换、反向、漏/多画、旧墨迹消失均被相应分项识别；整图突现和低采样顺序/方向未知。多帧明确同时增长判要求违反，保持与低采样歧义区分。该简化观察器有明确几何特权，只适用于分离线条，尚未在真实生成域校准；没有给63段UMM旧原片重新自动打正式分。

实际观察只读取解码像素和无序空间区域，判断阶段再读取规则；不读取构造事件。共同几何来源限制仍存在。汉字H-ACTUAL的独立观察答案null；K-ORDER自然描述尚缺合格语义/几何绑定。原生模型的自然语言答案不通过随意正则变为正确分，当前未解析/未核准项如实unknown。

开发中三个真实问题已保留：DEV-01初版把可确认的同时增长也记unknown，修订输出另存v02；DEV-02未执行T2V包最初套用交错JSON，经冻结P1原schema核对改为id→prompt，另存`gpu_batch_A_v03`。DEV-03另外检出8组源末帧相同、解码后有损压缩微差，最终改为无损输入，8/8解码末帧完全相同且历史不同，证据见[same-final审计](../../../data/research/next/same_final_pair_audit.json)。最终26段与先前26段调试版本分列，不计独立样本。原目录都保留，GPU调用均0。另有猜错Zebra仓库名的404，已按模型卡改正并记录。详见[开发失败和版本差异](../../../data/research/next/development_failures_and_revisions.json)。没有调旧正式阈值或利用新保留集反复调分。

## 公平对照与当前研究判断

| 假设 | 当前证据 | 判断/下一步 |
|---|---|---|
| H-K 汉字知识不足 |P1未直接测可靠识字/规范知识，LTX单字分词失败不代表Lance知识 |unverified；先K-CHAR/K-ORDER|
| H-V 基础过程生成不足 |P1粗筛无合格书写；无法单独归因知识或生成接口 |unverified；G-ATOMIC排除汉字知识混淆|
| H-U 实际历史理解不足 |28份原答存在字面时长冲突、部分干预回答相同；没有完整事件准确率 |unverified；同终态异历史H-ACTUAL及可见方向反例|
| H-UE 理解与生成协同可改善 |尚无本任务同数据普通适配、联合/分离对照 |unverified；先FIT、G-only/课程，再普通混合和参数等价对照|
| H-R 恢复训练能改善 |SC-CoIT作者在交错状态任务有效，汉字视频接口尚不对齐 |unverified；只有可见错误、合法恢复和同预算对照成立后研究|

[公平对照配置](../../../configs/research/next/training_comparison.json)包含G-only普通SFT、LoRA候选、同预算课程、U-only、普通U+G、仅诊断文字、Policy/Draw独立与组合、固定/迭代错误集及等预算随机重试。共享参数不等于所有权重共享；额外监督量、训练曝光、教师挖错和重试成本都单列。LoRA模块/rank尚未接入，训练数据资格和容量未达ready，恢复dropout的完整配对替换与真实梯度验证也未执行。这些限制没有包装成已能训练或已完成方法复现。

## 下一批建议与明确阻塞

推荐先只批准Batch A：同一Lance检查点24次，20理解＋4无汉字基础过程生成，seed11、零额外重试；建议单A10080、16核/48GiB，2小时及120元硬上限，单调用900秒。价格和实际费用未知，上限属于申请值，不是账单。P1旧64次不重复。当前完整ID、提示、静态输入适配、MP4、校验和及原生参数已材料化，所有请求保持unexecuted。

Batch A执行尚缺新的GPU批准、可用实例/固定缓存和新的获准执行接线；旧P1 runner的批准不能复用。如缓存不可用，应另申请固定权重恢复/下载。A2新模型、B训练、C恢复的预算/数据/接口尚不确定，以blocked和null显式登记，未填无限预算。暂不申请正式人工任务。

正式科学比较仍需独立保留来源和逐笔规范/实际RGB资格；现有作者资源限制未解决。本轮没有建立新保留集。普通SFT若已解决需求，应停止多余机制；G-ATOMIC也失败时，增强汉字知识本身不足以解释/解决过程生成。会诊断但不会改画时，不能声称自纠错有效。

## 可运行入口、检查和本地保存

CPU构造/评价/准备命令见[Benchmark说明](diagnostic_benchmark_v0_1.md)。实际数据在`private/research_restart_2026-11-01/benchmark_v02`，26段解码审计在`cpu_audit_v03`，24请求最终输入在`gpu_batch_A_v03`。原论文、解压材料、官方只读快照、初版失败都在同一私有根。旧P1原片、审核包和映射仍在原私有目录。本轮没有重新全量校验2192份；原报告的备份检查保持历史引用。

本轮检查实际命令、退出码、全量日志已记入`data/research/next/checks/check_results.json`，包括原目录/v1/v2验证、P1开发门禁、P0历史门禁、完整CPU单测。最终完整CPU回归174项通过（新增35项），耗时7.794秒；目录/v1/v2、P1开发与P0历史检查均退出0。严格P1 main合并门禁按预期拒绝缺少最终报告与合并批准；该拒绝是权限契约预期，不能关闭门禁换绿。

修改说明：`AGENTS.md`、`docs/project/STATUS.md`、`docs/project/BRANCH_WORKFLOW.md`仅新增本轮授权/当前入口及分支说明，历史正文保留。新增`scripts/diagnostics/`、一份测试文件、`configs/research/next/`、`data/research/next/`及本组报告。没有删除文件；未改旧P0/P1登记、预测、人审、原片、阈值或main，未推送。版本、完整变更列表和本地提交由最终登记记录。

```json
{"status":"research_kickoff_prepared","D0_D5_CPU_preparation":"completed","new_GPU_calls":0,"new_MPS_model_calls":0,"training_runs":0,"new_weight_or_dataset_downloads":0,"new_human_tasks":0,"remote_pushes":0,"main_merges":0,"formal_model_metrics":null,"formal_P1_state_changed":false,"next_proposed_GPU_calls":24,"next_GPU_authorized":false,"method_validated":false}
```
