# ENV-01：官方默认训练策略的单卡容量实测

2026-10-27，分支 `research/p0-stroke-video-foundation`。用户提出“默认全参训练容量实测一下”，并明确批准先测小型真实联合批次、通过后再测65,536 token的执行方案。[批准方案](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/approved_plan.json)、[任务登记](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/task_record.json)、[机器可读结果](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/summary.json)。

**实测结论：在当前1×A100 80GB上，固定版本的官方默认冻结/FSDP/BF16/AdamW策略未能完成首次优化器步骤。** 真实CE＋视频flow-matching的forward、loss、backward与梯度裁剪完成；AdamW初始化二阶矩状态时发生CUDA OOM。此次结论来自实际执行，先前88.55GiB静态估算仍单独保留为带假设的预算数值，不充当实测峰值。

## 配方与适用范围

- 源码 `bytedance/Lance@4baeee086648996f6ab12e673cbe461b0b149997`；权重 `bytedance-research/Lance@7395315758865e6f56ab87ad06a88c7ac172f056`。沿用已下载制品、既有Conda环境和原生代码，未修改上游源码或下载新数据。
- “默认全参”按官方 `scripts/sft_lance_unified.sh` 的默认冻结规则定义：冻结ViT、词嵌入与语言输出头，UND/GEN Transformer专家和连接模块可训练。实际可训练 **5,554,487,344** 个元素、**1,018** 个张量；冻结 **1,551,060,992** 个元素。全部持久参数实测为FP32。[参数名单](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/parameters_before_fsdp.json)。
- 直接调用原生组件构造、checkpoint载入、冻结、FSDP包装、NO_REENTRANT激活检查点、视频编码和损失函数。官方HYBRID_SHARD的1×1设备网格被PyTorch自动切为 **NO_SHARD**，未启用CPU offload。FSDP配置的参数计算/归约/buffer类型为BF16；实测持久参数、反传后梯度和已分配AdamW矩状态为FP32。本次没有逐算子计算精度追踪。[实际FSDP配置](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/fsdp_configuration.json)。
- AdamW保持官方默认 `betas=(0.9,0.95), eps=1e-15, weight_decay=0, foreach=None, fused=None`；LR=1e-4、constant调度、warmup=500。初始实际LR为0，调用真实 `optimizer.step()` 仍会分配矩状态；此次在更新前OOM，完成更新数为0。没有设置低精度优化器、减少训练参数或改用offload规避容量问题。
- 使用此前获准的自制 `observed_strokes.mp4`，经原生parquet读帧和组批。小批次含一个tv2t和一个t2v样本，同一次forward计算两项损失。理解输入6帧56×140（含ViT时序补齐），生成输入5帧96×176；实际序列 **267 token**，flex注意力预算补齐至 **1,024**。CE监督14 token，FM监督132 latent token。与官方多数据集训练内容不同；小批次有意缩小图像、帧率和token预算以测训练状态容量。[输入元数据](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/batch_metadata.json)。
- 沿用16核、主存50,470,645,760字节、Ubuntu22.04、Python3.11.18、torch2.5.1+cu124、FlashAttention2.6.3、驱动550.127.05、CUDA12.4。关闭W&B上传、定期验证与checkpoint写出，以边界日志替代完整accelerate启动器的记录功能；训练操作顺序保留原生zero_grad→backward→clip_grad_norm→optimizer.step→scheduler.step。[完整运行环境](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/environment_snapshot.txt)、[解析后训练参数](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/resolved_arguments.json)。

## 实际结果与分母

一次进程启动、一次真实联合forward/backward、一次优化器步骤尝试；软件错误0次、CUDA OOM 1次、完成优化器更新0次。随机种子2026。checkpoint载入匹配1,410项，仅缺少原生有意重建的固定 `latent_pos_embed.pos_embed`，无unexpected key。

| 项目 | 实测 |
| --- | --- |
| CE / FM / 联合损失 | 2.3295228481 / 0.1230806410 / 0.7054613829；联合=0.25×CE＋FM |
| 反传梯度 | 1,018/1,018可训练张量均有FP32梯度；全部有限，范数全部非零 |
| 裁剪前全局梯度范数 | 10.239189148 |
| backward完成时allocated | 53.31GiB；此时尚未创建AdamW矩状态 |
| 全进程allocated / reserved峰值 | **77.8277 / 78.0176GiB**；两个量不可相加 |
| 每秒整卡采样峰值 | **80,977MiB＝79.0791GiB**，包含非PyTorch开销；采样可能遗漏短峰 |
| 主存RSS峰值 | **38.9874GiB** |
| worker / 含启动退出的控制器耗时 | 112.029 / 122.255秒，未将本轮准备、归档及空闲时间当作免费时段 |

[原始指标与完整traceback](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/metrics.json)、[逐张量梯度](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/gradients_step0.json)、[原始进程日志](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/process.log)、[整卡采样](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/gpu_samples.csv)全部保留。

失败位于 `torch.optim.adamw.AdamW._init_group` 的 `state["exp_avg_sq"] = torch.zeros_like(...)`，请求额外86MiB，CUDA当时只剩61.25MiB；allocator已分配77.83GiB，未分配缓存约152.44MiB。分配器在失败前已尝试回收缓存，现有记录支持实际状态容量不足，未观察到数据损坏或纯软件接口错误。

失败时只有608个参数条目开始创建状态，FP32一阶矩已分配3,301,213,184元素，二阶矩3,278,668,800元素，仍未覆盖全部5,554,487,344可训练元素。不能把失败时的部分状态数量当作完整优化器预算。[失败时状态库存](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/optimizer_at_failure.json)、[allocator明细](../../../data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/allocator_at_failure.json)。

按批准的停止条件，未重复相同OOM配置，跳过65,536 token及第二个稳态步骤；没有产生新训练checkpoint。此次直接证明的是上述默认策略在本机小型联合批次上失败；它没有测量65,536 token的实际峰值，也没有排除其他精度、优化器、冻结范围或offload方案。先前已通过的[部分参数训练与独立重载](env01_training_reload_report_2026-10-27.md)仍为独立证据。

## 记录、费用与下一步边界

本次脚本、配置、原始输入parquet、实际packed batch、参数与梯度清单、异常、显存采样、解析后参数及环境信息已回收到本地研究分支；云端原件保留。本轮没有删除或覆盖既有运行、权重、环境或checkpoint。新增与修改文件逐项说明见任务登记；本地工程检查见该run的 `checks/`。

本地v1/v2协议、P0开发状态门禁和50项回归测试通过。初次目录检查发现前轮两份已入库的 `.pt` 组批输入被旧权重扩展名规则拒绝，已为三份明确路径的自制输入建立白名单，权重排除规则保留；修正后目录检查与全部50项回归通过。初次失败日志保留。原始nvidia-smi文本含尾部空格，保持原样；维护代码、配置与文档的空白检查单独执行。

云端训练进程已退出，回收时GPU为14MiB、0%利用率、无compute进程。实例租约仍在持续，操作系统空闲不代表停止计费；平台实际账单未知，金额保持null。本轮执行及归档时间线保留，前轮checkpoint与FlashAttention编译wheel已有本地private备份。用户可在平台停止实例并选择保留磁盘，后续需要复用环境时再开机。

ENV-01保留“原生接口＋批准的部分参数训练/重载通过”的边界，新增“默认策略单卡容量失败”的实测结论。DATA-01、EVAL-01仍为planned，完整P0尚未验收。本轮结束后停止额外GPU实验，后续配方调整或新阶段须重新确认和批准；不推送、不提交main、不提出合并PR。
