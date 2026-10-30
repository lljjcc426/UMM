# ENV-01 最小训练与独立重载验证

2026-10-27；分支 `research/p0-stroke-video-foundation`。本轮按用户批准的部分参数方案执行，沿用同一台A100 80GB、相同代码/权重revision和Python3.11/PyTorch2.5.1+cu124环境。

**结论：ENV-01在本次批准的最小环境验证范围内通过。** 前轮三项原生推理接口已有成功输出；本轮完成真实CE与视频flow-matching前反传、AdamW更新、保存和独立进程重载，并与未中断续训逐张量比较一致。Decord警告在已验证的读帧路径上为非阻塞打包元数据问题。该结论不支持默认全参训练容量、训练收敛、笔顺准确率或共享收益；P0仍须完成DATA-01、EVAL-01并另行验收。

## 授权与证据层级

用户批准本轮方案，并指出“官方默认训练状态预算超过单卡容量”仍需验证。此前88.55GiB数值保留为FP32持久参数、全量相关梯度和AdamW状态等假设下的静态估算；没有执行默认全参训练，没有实测其OOM，不能把估算写成实际容量失败。本轮实测仅对应以下配方。

代码固定为 `bytedance/Lance@4baeee086648996f6ab12e673cbe461b0b149997`，权重固定为 `bytedance-research/Lance@7395315758865e6f56ab87ad06a88c7ac172f056`。[前轮原生接口报告](env01_native_interface_report_2026-10-27.md)保留其当时的未完成状态；本报告补充训练与重载结果，不覆盖历史失败。

## 实际训练配方

- 全模型参数元素数7,105,548,336；本轮可训练324,479,024个元素、13个张量。[实际参数名单](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt03/parameters_train.json)。原计划采用“实际最后一层”策略，固定模型有36层，实际为第35层（从0计数）。
- 可训练集合：同一词嵌入、最后一层UND与GEN各自的Q投影，以及生成输入/输出投影和时间嵌入。其余参数冻结；ViT、VAE仅作原生编码。冻结模型BF16，目标参数及AdamW状态FP32；词嵌入输出通过保留autograd的hook转为BF16，以匹配视觉特征。
- AdamW：lr=1e-4、betas=(0.9,0.95)、eps=1e-8、weight_decay=0、foreach=false；梯度裁剪1.0；StepLR每步乘0.9。seed=20261027，实际训练RNG在模型构造后设为seed+1。
- 使用前轮已批准原创RGB视频的一条本地字节样本，分别走原生本地parquet、视频采样/变换和PackedDataset。CE实际为6帧56×140（5帧加末帧重复以满足ViT偶数帧）；生成实际为5帧96×176。每类一条，packed有效长度71/196，FlexAttention填充到1024。[组批元数据](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt03/batch_metadata.json)。这些仅为环境夹具，未启动DATA-01或正式数据集建设。
- 每个优化器步依次执行原生理解CE和视频FM前向、分别反传并记录，再累积梯度更新；权重为0.25/1.0。视频目标经过真实Wan VAE编码，使用原生噪声、时间步和FM目标。没有用虚构loss或随机潜变量替代RGB训练链路。

本轮采用单进程验证脚本，复用原生组批、编码器和`Lance.forward`，以及等价的单卡CE/FM均值归一化。未验证官方完整FSDP启动器、分片checkpoint、分布式恢复或正式训练配方。

## 梯度、更新与显存

| 执行 | CE原始loss | FM原始loss | 两任务共享词嵌入梯度范数（加权后） | allocated / reserved峰值GiB | 步骤墙钟s |
| --- | ---: | ---: | --- | ---: | ---: |
| 初始step1 | 2.3199303150 | 0.2071461082 | 19.24296379 / 1.30313945 | 21.14 / 22.95 | 15.66 |
| 未中断参考step2 | 2.3713848591 | 0.1668888032 | 32.07517242 / 0.55156130 | 22.04 / 23.05 | 3.45 |
| 独立恢复step2 | 2.3713848591 | 0.1668888032 | 32.07517242 / 0.55156130 | 22.04 / 23.05 | 7.51 |

共享词嵌入确为同一模型中的同一参数，分别获得两个任务的有限、非零梯度。初始CE的UND Q权重梯度范数0.04690547；FM的GEN Q、时间嵌入、VAE输入/输出投影也均非零。未参与相应任务的目标张量记录为零或无梯度，不伪报全部参数被两任务同时训练。[完整step1梯度与更新](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt03/initial_step1.json)。

AdamW初始更新最大绝对变化约1.00136e-4，下一步约9.00328e-5；全部指定的目标权重实际改变，冻结参数版本计数保持不变。MoT两侧Transformer QKV/MLP/norm具有独立参数，共享词嵌入获得梯度不证明理解与生成正迁移。单步loss变化也不作收敛或质量判断。

上述步骤计时包括CPU参数前后快照和梯度记录，不能作为纯GPU吞吐。训练进程含加载与保存99.05秒，恢复进程109.05秒。加载allocated峰值28.38GiB、reserved28.70GiB；完整进程每秒采样的整卡峰值29,163MiB（约28.48GiB），可能漏过短峰。训练阶段allocated最高22.04GiB、reserved23.05GiB；两者不相加。主存进程峰值约31.3GiB。

## Checkpoint闭环

step1 checkpoint保存全部13个可训练张量、AdamW动量/二阶矩与step、StepLR、全局步数、固定batch进度、Python/NumPy/Torch CPU/CUDA随机状态、完整配方与冻结底座revision。冻结参数从固定原始权重和同一初始化种子重建，因此该checkpoint依赖所注明底座，不能单独当作完整模型发布。

独立进程重新构造底座后恢复：[逐项恢复检查](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt03/reload_exact_comparison.json)全部为true。两次底座加载只缺少有意重建的固定位置表，无其他missing或unexpected键。

恢复后的下一步与未中断参考比较：[续训比较](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt03/continuation_comparison.json)显示所有目标参数逐张量完全相等，最大差异0；优化器、调度器和RNG也完全一致，两个loss数值相同。事先记录的数值容差未放宽。

共执行3次优化器更新：初始step1、未中断参考step2、恢复step2；后两次用于验证同一步的恢复一致性，不当作3个独立训练样本。两份原始checkpoint各约3.894GB，云端原件保留；压缩备份、运行环境与本地归档位置见[制品清单](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/artifact_inventory.json)。大制品放在本地private备份，不加入Git；运行配方、原始日志、状态与比较证据进入研究分支。

## Decord原因与正确性核查

官方发布wheel文件名为`py3-none`，包内WHEEL标注`cp36-cp36m`；pip据此报平台不支持。当前库通过ctypes加载原生解码库，包内标签不一致能够解释安装检查警告；未修改标签或隐藏pip失败。

对原创输入与两段前轮生成视频共99帧，以独立FFmpeg进程解码RGB，与Decord逐帧比较：帧数、形状一致，全部像素差异为0；逐帧时间戳最大差异3.3731e-6秒，在事先1e-5秒容差内。原生训练的字节读取方法与直接Decord索引读取一致，本轮原生parquet读取、采样、时间填充、ViT/VAE及训练均实际执行。[完整核查](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt02/decord_audit.json)。

据此将警告登记为**当前固定环境及已验证数据路径上的已知非阻塞问题**。未发现帧损坏、顺序改变或由该警告引发的训练错误；该结论不覆盖所有编码格式和任意未来输入。

## 失败、成本与收尾

1. attempt01核查脚本要求系统ffprobe，但镜像未安装；在模型启动前失败。改用已有独立FFmpeg的showinfo读取PTS，未新增软件或放宽检查。
2. attempt02解码/组批成功，首次模型前向因FP32词嵌入输出和BF16视觉特征indexed assignment冲突失败，没有完成loss/backward/step。保留日志，在验证脚本加入保留梯度的输出类型转换；未改上游模型源。
3. attempt03复用已通过的核查与原始packed batch，完成训练和独立恢复，未重复生成视频或下载权重。
4. 本地首轮证据解包使用了当前系统Python不支持的tarfile filter参数，触发TypeError；改用已由本任务生成的可信归档的普通解包，模型结果不受影响。

所有失败均保留。费用授权延续“不设上限”，实际账单仍为null；阶段进程墙钟和GPU采样、环境冻结、归档记录完整保留。进程耗时不能直接相加代替平台租用账单，模型结束后的归档/等待也计入租用占用范围。[任务及变更记录](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/task_record.json)记录最终收尾状态。

本地目录、v1/v2结构及P0开发门禁检查通过，50项回归测试通过。首轮有一项既有门禁测试默认实际清单永远没有证据、ENV-01永远未完成；现已将该负例夹具显式设为“无证据、未完成”，保留原失败并重跑测试通过。门禁实现及科研验收要求未放宽。[首轮测试日志](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/checks/unit_tests.log)与[修复后日志](../../../data/research/runs/env01_training_reload_a10080_2026-10-27/checks/unit_tests_attempt02.log)均保存。未推送或触发GitHub CI。

本轮完成后停止模型计算，不启动新研究任务。平台实例仍需用户选择停机保盘或后续使用，SSH连接成功和模型进程结束均不等同于平台停止计费。完整P0保持进行中，不提出面向main的PR。

后续独立任务：[官方默认训练策略容量实测](env01_default_capacity_report_2026-10-27.md)已在A10080上完成真实联合前反传，首次AdamW状态初始化OOM；本报告的部分参数训练/重载结果与当时边界保留。
