# Batch A：同一Lance检查点24次诊断执行报告

日期：2026-11-01。分支：`exp/p1-process-diagnostic`。

**24项全部执行完成，20份理解回答与4段原生MP4均通过工程完整性检查，技术失败、阻塞、未运行、额外GPU重试和本任务训练均为0。** 模型内容存在明显错误，也出现了左到右横线增长的正面个案。当前结果支持进一步调查理解、观察与生成能力的缺口，尚不能定位唯一机制瓶颈或证明任何改进方法有效。P0/P1正式科学状态保持原样。

主记录：[实际调用与资源汇总](../../../data/research/runs/diagnostic_batch_A_2026-11-01/execution_summary.json)、[最终队列状态](../../../data/research/runs/diagnostic_batch_A_2026-11-01/state.json)、[24项AI案例分析](../../../data/research/runs/diagnostic_batch_A_2026-11-01/AI_case_analysis.json)。汇总JSON保留20份完整原始回答及逐次资源记录。

## 1. 授权、固定版本与完整分母

原[24次授权](../../../data/research/runs/diagnostic_batch_A_2026-11-01/authorization.json)和[缺缓存部署快照](batch_A_execution_2026-11-01.md)保留；用户随后明确[批准恢复固定检查点与独立环境](../../../data/research/runs/diagnostic_batch_A_2026-11-01/checkpoint_restore_approval.json)。原授权中的`allow_download=false`及待回复字段属于审批时快照，补充批准仅更新固定缓存恢复范围。

| 任务 | 冻结请求 | 实际原生调用 | 工程有效 | 技术失败 | 阻塞/未运行 |
|---|---:|---:|---:|---:|---:|
| K-CHAR 图像识字 |4|4|4|0|0/0|
| K-ORDER 文字笔画知识 |4|4|4|0|0/0|
| V-STRUCT 静态空间结构 |4|4|4|0|0/0|
| H-ACTUAL 实际视频过程 |8|8|8|0|0/0|
| G-ATOMIC 原生原子生成 |4|4|4|0|0/0|
| 合计 |24|24|24|0|0/0|

工程有效指正确输入进入原生接口并产出可读回答/视频，不能据此认定内容正确。所有质量差的产物均保留。原P1的64个生成槽位及其旧理解、codec、人审证据继续复用，没有重新生成或改写历史结果。

- 模型：`bytedance-research/Lance`，权重revision `7395315758865e6f56ab87ad06a88c7ac172f056`；源码revision `4baeee086648996f6ab12e673cbe461b0b149997`。
- 11份固定文件恢复完成；3个大权重分别只做过一次与官方LFS元信息对应的SHA-256核验。[来源记录](../../../data/research/runs/diagnostic_batch_A_2026-11-01/model_provenance.json)。
- seed 11；G0；848×480、33帧、12fps；30步、CFG 4、timestep shift 3.5、KV cache开启、提示增强关闭；原生理解上限256 tokens。未更换提示、种子、权重或生成参数。
- 全部理解通过`x2t_video`调用：K-CHAR/V-STRUCT使用静态图重复33帧；K-ORDER使用空白视频载体。其结果不能直接推广为独立图像接口或纯文本接口的能力结论。

## 2. 输入、采样和原片完整性

先逐次运行并检查前四项，再连续执行剩余20项。实际输入依次为丑、广、士、小；[前四项审计](../../../data/research/runs/diagnostic_batch_A_2026-11-01/first_four_GPU_input_audit.json)确认提示和seed正确、参考占位答案未进入conditioning，实际RGB及变换张量与预检一致，未见ENV-01“十”字fixture覆盖。

最终[20项实际输入审计](../../../data/research/runs/diagnostic_batch_A_2026-11-01/all_understanding_input_audit.json)全部匹配。每段原生读取索引为0–32；源RGB为128×128、33帧、12fps；实际ViT变换为`[3,34,588,588]`，包含原生末帧补齐。真实读取帧、变换张量、reader PTS、packed tokens及conditioning全文均已保存。预检本身没有初始化CUDA。

[五组相同终帧配对](../../../data/research/runs/diagnostic_batch_A_2026-11-01/paired_native_input_audit.json)的原生变换终帧相同，中间历史不同，采样索引一致；因此不存在仅因遗漏这些源帧而导致配对差异消失的证据。此检查没有证明模型内部一定正确使用时间信息。

4段生成均为真实原生MP4，每段33帧、848×480，源RGB和解码RGB尺寸一致，PTS为`i/12`，最后显示时刻约2.666667秒，容器时长约2.75秒。每段原片、编码前RGB、解码RGB、真实caption/packed输入、FFmpeg解码命令与日志全部保留；没有插帧、补片或重选结果。

## 3. 诊断发现及其证据边界

以下为AI案例核对与限定范围的CPU像素证据，没有代填真人判断或建立新的正式金标。

**识字与笔画知识。** 4个识字回答分别为`a squint`、类似小写`l'`的符号、`water`的一个stroke、`J`，均未识别出对应输入字。四个文字笔顺回答未形成可执行的完整逐笔计划；例如“丑”回答转为人物、车辆移动，“广/小”回答复述问题并声称视频6秒。它们均正常EOS结束，未触及长度上限。不能将此四字个案写成总体汉字准确率，也没有依据将旧整体人审升级为逐笔规范金标。

**空间结构与实际过程。** 四份静态结构回答没有给出足以核验的逐笔几何绑定。“士”正常过程回答013部分提到了横后出现中央竖线，说明不能把所有过程信息都记为完全缺失；但方向、下横身份和时长仍不充分或有误。交换顺序的014被描述为人形向右行走；015声称“小”解体、碎片脱落。

[实际像素证据](../../../data/research/runs/diagnostic_batch_A_2026-11-01/micro_actual_pixel_audit.json)基于原生读取RGB，8段过程输入均从空白开始，固定阈值128下历史墨迹消失像素总数均为0，直接反驳015的墨迹脱落描述。简单双线的观察器只获得评估侧固定几何区域，未读取渲染事件日志，区域信息未提供给模型；该观察器仅适用于这些不相交黑白线段。

- 017实际为上横右到左、下横左到右；回答已输出部分将二者方向说反。
- 018实际只有两条横线；回答虚构第三至第十一条等多条线。
- 019实际两条线一次出现后位置固定；回答虚构上下移动。
- 020反复描述额外小线，未给出清晰的实际先后和生长方向。

017、018、020达到256-token上限，其余17份回答正常EOS。三份原始token和截断标记保留，没有延长回答或再次调用。截断部分不补写结论，已输出的明确错误也不抹除。

**原生生成包含正反两类证据。** 全部33帧联系图和关键原尺寸帧已回看；[中性像素记录](../../../data/research/runs/diagnostic_batch_A_2026-11-01/generation_pixel_evidence.json)仅作辅助，不充当通用评分器。

| 请求 | 冻结目标 | 实际RGB现象 | 可支持的判断 |
|---|---|---|---|
|021|水平线从右到左增长|由小变大的弯折曲线，累计14829个阈值墨迹消失像素|存在可见形成/变形；水平直线形状不符，不能简单归为方向全对或全错|
|022|竖线从上到下增长|首帧已有完整贯穿高度竖线，黑色掩膜33帧不变|最终竖线可见；缺少生长过程，书写方向不可判|
|023|水平线从左到右增长|近水平线由左向右延长；黑色范围从`x=160…193`扩至`x=160…687`|核心原子指令有正面RGB证据；不能由此推广为复杂汉字生成通过|
|024|先上横再下横，保留旧墨迹|首帧已有短弯曲箭头状线段，未出现双线顺序|缺少要求的第二条线与顺序过程|

023首帧已有210个阈值黑像素，整段累计仅6个阈值墨迹消失像素；该提示没有明确要求首帧完全空白，不能事后增加此条件将其改判失败。小规模阈值变化也不足以证明保墨失败。本文不发布“0/4原子成功”或正式笔顺准确率。

**尚不能成立的结论。** 数据来自4个暴露汉字和受控微任务，只有一个检查点、一个seed，没有新的独立保留集、完整规范金标、训练对照或因果干预。原生提示没有要求JSON；叙述未满足结构化比较器，不能直接算作笔顺错误。正式规范指标仍未评分，AI个案意见独立保存。当前没有显式动作状态，SC-CoIT的Policy Error/Draw Error均记为`unattributed`；不能从一段错误描述或弯曲线直接判定具体模块根因。

## 4. 环境、资源与技术问题

独立目录：`/mnt/data/umm-diagnostic-batch-a-20261101`。Python 3.11.18、Torch 2.5.1+cu124、Transformers 4.49.0、FlashAttention 2.6.3、Decord 0.6.0、NumPy 1.23.5；完整[环境版本](../../../data/research/runs/diagnostic_batch_A_2026-11-01/isolated_environment.json)与[pip freeze](../../../data/research/runs/diagnostic_batch_A_2026-11-01/isolated_pip_freeze.txt)已保存。

| 资源 | 实测 |
|---|---|
| 首次开始—末次结束 UTC |13:30:23.515185—14:20:44.133957|
| 调度跨度，包含前四项AI工程检查等待 |3020.62秒，50.34分钟|
| 24个worker累计墙钟，含加载 |2561.51秒，42.69分钟|
| PyTorch单进程峰值分配 |30,471,729,152 bytes，28.379GiB|
| PyTorch单进程峰值预留 |38,507,905,024 bytes，35.863GiB|
| 单进程主存RSS峰值 |33,783,074,816 bytes，31.463GiB|
| 1秒整卡采样峰值 |60633MiB，含其他任务；不能算作Lance独占显存|
| 启动时有其他GPU进程的调用 |6次|
| 账单金额/纯GPU内核时间 |未核对/未单独计量，不填造金额或将加载时间伪称为内核时间|

共享策略使用实测显存/内存余量，单次PyTorch分配上限42GiB；没有停止或修改其他实验。每次调用均低于900秒，全批跨度低于两小时保护。权重下载和依赖恢复先于首次模型调用，耗时与失败保留在setup日志中，未计为模型调用或GPU重试。[退出检查](../../../data/research/runs/diagnostic_batch_A_2026-11-01/process_exit_check.json)确认本任务GPU进程为空；实例与磁盘保留。

[恢复记录](../../../data/research/runs/diagnostic_batch_A_2026-11-01/runtime_restore_record.json)保留以下问题：固定权重普通传输过慢后调整传输工具；独立FFmpeg下载截断；固定FlashAttention缺少匹配预编译包，源码构建从2个并发恢复为4个并发；驱动缺少`libcuda.so`链接名，仅在本任务目录创建兼容链接。没有改动系统驱动或其他实验环境。

自带FFmpeg 4.2.2不支持原运行器的`-fps_mode`，在生成前CPU验证时发现，解码改为等效`-vsync 0`。服务器33帧解码和全部4段原片审计随后通过。原失败日志保留，没有因此增加GPU调用。

## 5. 测试、归档与复现

完整CPU回归182项通过，最终7.716秒，其中运行器8项测试；覆盖精确授权、真实输入归档、共享资源、仅终止自身子进程、失败不重试及完整分母。目录、v2协议、P1开发结项检查通过；后者继续报告`original_scientific_gates_met=false`、`merge_authorized=false`。[验证记录](../../../data/research/runs/diagnostic_batch_A_2026-11-01/runner_validation.json)。无需因仅追加文档再次运行完整模型或重复权重核验。

服务器原件保留在独立目录的`inputs/`、`bundles/<请求ID>/runs/<UTC>/`、`CPU_native_loader_preflight/`与`AI_generation_contacts/`。原片固定相对路径为`<native_run>/t2v/outputs/000001.mp4`，20份原答位于`<native_run>/x2t_video/outputs/result.json`，具体`native_run`见最终state。

服务器归档：`/mnt/data/umm-diagnostic-batch-a-20261101/backups/batch_A_evidence_20261101T143532877061Z.tar.gz`，242,763,262 bytes，724份普通文件，252项必要证据无缺失，含原片、全部回答/token、源/解码RGB、采样、输入、命令、日志、环境元信息和编译后的FlashAttention wheel。SHA-256：`850bec8ecd2c5e69453f6e0f458f7449d08f23ff0c12a3bd9ce1f1a98355c7fd`。

本地副本已回传至`private/diagnostic_batch_A_2026-11-01/server_backup/`，大小及SHA-256与服务器一致；已解包至`private/diagnostic_batch_A_2026-11-01/server_artifacts/`，4段原片、20份原答均可直接访问。[备份回执](../../../data/research/runs/diagnostic_batch_A_2026-11-01/backup_receipt.json)。权重、已安装环境、大型缓存及慢速下载残片仍保留在服务器，未重复打包；精确版本、三项大权重核验、pip freeze及必要构建产物已随证据包保存。没有公开上传大文件或凭据。

复现入口：

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m scripts.diagnostics.summarize_batch \
  --root /path/to/extracted/server_artifacts --output /tmp/batch_A_summary.json
```

服务器执行器入口为`runtime/bin/python -m scripts.diagnostics.execute --root ...`；最终state已全部完成，按该state再次调用不会重跑已调用槽位。新GPU请求、重试或训练仍需独立批准，不通过清空state复跑。

## 6. 后续建议与文件变更

优先准备Batch B的普通领域适配目标与独立验证方案：识字/几何绑定、可执行的逐笔表示，以及基于真实RGB的事件顺序和方向。正式训练目标须使用核准的规范或明确的几何微任务监督；当前错误回答不能直接充当自纠错金标。相同数据、预算和验收下建立普通SFT/LoRA基线，再评估纠错机制的额外收益。若需排除视频载体/指令格式的影响，可另行申请小规模原生正控；本批没有擅自追加。

Batch C继续等待可观察错误、显式可恢复状态、可靠错误标签和公平基线。023的正面结果支持保留原生生成路线，但没有证明理解端改进必然带来完整汉字视频改进。Batch B/C未执行，本轮在报告和本地保存后停止。

实际文件变化：

- 修改`scripts/diagnostics/execute.py`：资源余量与自身显存上限、原始回答token采证、真实解码审计、最终完整计数；`media.py`增加解码证据和FFmpeg兼容选项；`tests/test_diagnostic_execution.py`补充分母和零重试恢复检查。
- 新增`restore_runtime.sh`、`preflight_lance.py`、`summarize_batch.py`，分别用于固定恢复、原生CPU输入预检、实际运行汇总。
- 更新`AGENTS.md`、`docs/project/STATUS.md`、`data/research/next/experiments.json`及本批`state.json`，记录补充授权和实际完成；原state另存快照，原部署报告保留当时阻塞事实并追加进展说明。
- 新增本报告及本批证据JSON/测试日志；原片、数组、构建产物和传输失败现场私有保存。没有删除文件，没有改写P0/P1原片、人审、阈值、发布结论，没有推送或合并main。
