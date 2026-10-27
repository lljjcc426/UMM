# ENV-01：资源与代码可行性盘点

日期：2026-10-27。协议：`stroke-video-v2`。研究分支：`research/p0-stroke-video-foundation`。

## 本轮结论与授权范围

**Lance_3B_Video 具备进入单卡云端推理验证的代码与公开制品条件；推荐先用 A100 80GB。官方默认覆盖理解、生成两侧的大范围训练配置，按下述精度及优化器状态假设的静态估算，存在超过单卡容量的高风险；实际默认训练峰值尚未测量。** 这项判断来自源码与文件头；本报告为当时的静态盘点快照，后续实测另见运行报告。2026-10-27用户指出容量结论仍待验证，本处据此澄清证据层级，不把静态估算当作实测失败。

用户批准的任务为资源和代码可行性盘点，优先形成底座可用性结论；允许轻量本地工作，较重模型运行限云服务器。当前没有模型、数据或已租用实例。GPU 数量最多为 1，可等待其他型号；GPU 主机 CPU/内存档位最高为 16 核/48GB。GPU 小时、总费用、实例访问和升级配置价格尚未批准。本轮没有租赁、完整权重下载、模型执行、数据集下载、训练、提交或推送。

本轮已完成：只读资源检查、官方源码下载与静态检查、固定版本的权重元数据/配置/两份 safetensors 文件头读取、资源目录和失败记录、报告及登记。权重 HTTP 请求限定在文件头字节范围，没有下载张量数据。运行记录见 [audit_record.json](../../../data/research/audits/env01_static_2026-10-27/audit_record.json)，全部操作及失败见 [operations.json](../../../data/research/audits/env01_static_2026-10-27/operations.json)。

## 固定制品与依赖

| 项目 | 核查结果 |
| --- | --- |
| 官方代码 | [bytedance/Lance](https://github.com/bytedance/Lance/tree/4baeee086648996f6ab12e673cbe461b0b149997)，commit `4baeee086648996f6ab12e673cbe461b0b149997` |
| 权重仓库 | [bytedance-research/Lance](https://huggingface.co/bytedance-research/Lance/tree/7395315758865e6f56ab87ad06a88c7ac172f056)，revision `7395315758865e6f56ab87ad06a88c7ac172f056`；API 返回 public、非 gated、非 disabled |
| 许可证据 | 源码 LICENSE 为 Apache-2.0，模型卡 `license: apache-2.0`；未替第三方数据或全部传递依赖作授权结论 |
| 视频模型文件 | `Lance_3B_Video/model.safetensors`：14,211,277,144 bytes，约 14.21GB/13.24GiB |
| 初始化所需视觉编码器文件 | `Qwen2.5-VL-ViT/vit.safetensors`：1,337,407,560 bytes |
| VAE 文件 | `Wan2.2_VAE.pth`：2,818,839,170 bytes；仅核查元数据，未读取 pickle/张量内容 |
| 选定下载集合 | 视频目录、ViT 目录、VAE 及根配置共 18,379,012,935 bytes，约 18.38GB/17.12GiB；不含图像模型、示例媒体、训练数据和软件 |
| 原生环境 | Linux/CUDA 路径，Python 3.11；官方列出 PyTorch 2.8.0/cu126 + flash-attn 2.8.3 和 PyTorch 2.5.1/cu124 + flash-attn 2.6.3 的 A100 测试组合 |
| 依赖边界 | 官方 requirements 固定了 transformers 4.49.0、accelerate 1.13.0、pyarrow 11.0.0 等，wandb 未固定版本；本轮未安装或验证该 CUDA 环境，实际环境锁定待云端安装后记录 |

公开访问及文件大小以[原始模型元数据](../../../data/research/audits/env01_static_2026-10-27/assets/model_metadata.json)为证。下载时只选择上述目录与 VAE，避免 README 中全仓模式额外拉取图像检查点和展示媒体。文件大小与元数据中的 LFS 标识仅用于版本和下载规划，没有进行重复 hash 扫描。

## 接口与训练代码审查

下列“存在”仅指固定版本包含代码入口。43 个带行号片段保存在 [source_excerpts.json](../../../data/research/audits/env01_static_2026-10-27/source_excerpts.json)，下载的目录结构保存在 [source_tree.txt](../../../data/research/audits/env01_static_2026-10-27/source_tree.txt)。

| 能力 | 静态证据 | 可支持的判断与缺项 |
| --- | --- | --- |
| 文本生成视频 | `inference_lance.py:61–115` 定义 `t2v`，调用生成方法 | 有官方入口；生成效果、显存和耗时待实测 |
| 视频理解 | 同处定义 `x2t_video`，模型提供 `validation_video_to_text` 和理解 KV cache 路径 | 有官方入口；尚未验证本研究的笔画事件理解 |
| 图像条件生成视频 | 同处定义 `i2v`，提供示例 JSON | 可以用实际最后帧作为候选条件路径；不预先承诺任意多帧前缀冻结 |
| 视频编辑/条件 | 同处定义 `video_edit`；训练包含 v2v parquet 配置 | 视频条件与前缀续写语义不同，需要后续按 P 协议独立验证 |
| 首帧/首末帧训练 | `dataset_x2v_interleave.py:59–64` 将 `ff2v` 映射到 `[0]`，`flf2v` 映射到 `[0,-1]` | 首末帧条件含未来信息，不能直接放入 T/P；必要时只采用合法已发生条件 |
| 单任务与混合训练 | `sft_lance_{understand,generation,unified}.sh` → `train/unified_train.py` | 有反传、优化器和模型/优化器保存入口；梯度与重载一致性均未实测 |
| 损失 | `Lance.forward` 分别计算文本 CE 和视频 flow matching 的 MSE | 支持现有理解/生成目标；本项目事件 adapter、执行损失和自由滚动管线尚未实现 |
| 冻结与节省显存 | `freeze_model_components` 提供 LLM、词嵌入/输出头、UND 参数、ViT 的冻结；有激活重计算和 CPU offload 配置 | 部分冻结有代码基础；已审查训练入口没有现成 LoRA/PEFT 接入，接入和梯度检查需要后续任务 |
| 模型重载 | `train/fsdp_utils.py` 保存模型及优化器；`train_utils.py` 有初始化与恢复路径 | `strict=False` 的加载报告需要实际审阅预期/非预期差异；本轮未证明可重载 |

训练数据读取本地 parquet：t2v 为 `caption + video_bytes`；v2t 为 `video_bytes + caption_i/q/a`；视频编辑另含条件和目标字节字段。官方 t2v 示例混合 `t2v/ff2v`，不能把默认配方当作已固定的 T 协议。官方局部配置包含高分辨率、最长数秒视频和 65,536 packed token 上限，不能在单卡上直接视作轻量排错配置。

默认训练脚本中的 `FREEZE_LLM`、`FREEZE_UND_PARAMS`、`USE_EMA` 等采用脚本内直接赋值；仅在启动前设置同名环境变量不会改变这些值。后续若批准调整，应明确修改脚本或通过受控启动器传参。`ARNOLD_WORKER_GPU`、`NUM_SHARD`、部分数据配置及 `NUM_WORKERS` 支持环境覆盖。官方训练验证逻辑关闭，需要单独的离线推理与评价步骤。

推理默认 `ENHANCE_PROMPT=false`；后续保持关闭，可避免引入额外模型/服务及改变原始提示的混杂因素。模型主程序显式检查 CUDA，并使用 NCCL、BF16、FlashAttention/FlexAttention，当前 M5/16GB macOS 不作为官方模型运行目标。

### 理解与生成参数共享的具体限制

`ModelArguments.layer_module` 默认 `Qwen2MoTDecoderLayer`。`qwen2_navit.py` 的理解/生成两侧具有分别命名的 QKV/O 投影、MLP 和归一化参数，生成侧后缀为 `moe_gen`。共同的模型容器和交错 attention 提供统一处理路径，但不能直接据此认定全部 Transformer 权重共享。后续 H3 必须列出实际共享参数路径，再设计共享/分离对照。本轮没有改变研究假设或模型架构。

## 参数与单卡内存预算

文件头包含 1,411 个 BF16 张量，共 7,105,548,336 个元素，已包括 ViT 与固定位置表。独立 ViT 文件供初始化读取，**不能再次计入主模型常驻参数总数**。具体分组与公式见 [static_assessment.json](../../../data/research/audits/env01_static_2026-10-27/static_assessment.json)。固定位置表不参与训练；头信息元素数也不能直接写成可训练参数数。

| 组成 | 张量元素数 |
| --- | ---: |
| 理解侧 Transformer 参数 | 2,774,782,976 |
| 生成侧 Transformer 参数 | 2,774,782,976 |
| 词嵌入与语言输出头 | 622,329,856 |
| ViT（包含在主检查点中） | 668,684,288 |
| 固定三维位置表 | 260,046,848 |
| 生成投影与时间嵌入 | 4,921,392 |

按脚本默认冻结 ViT、词嵌入、语言输出头和固定位置表，覆盖两侧训练的可训练规模估计为 5,554,487,344；若冻结理解侧，仅生成侧与生成头约 2,779,704,368。此处以检查点形状和冻结规则推算，没有构建模型或测量 `requires_grad` 后的实际名单。

官方训练直接构造模型，未在 FSDP 包装前把持久参数转为 BF16。FSDP 的 `param_dtype=bf16` 控制前向/反向计算，默认保留全精度参数及优化器使用的全精度梯度；参考 [PyTorch 2.8 MixedPrecision](https://docs.pytorch.org/docs/2.8/fsdp.html#torch.distributed.fsdp.MixedPrecision)。因此以 FP32 参数、梯度与 AdamW 两个状态估算，单卡无法从分片获得容量收益：

`状态字节数 ≈ 4 × 全模型元素数 + (4 + 8) × 可训练元素数`

| 配置 | FP32 模型 | 梯度 | AdamW 两状态 | 状态合计 |
| --- | ---: | ---: | ---: | ---: |
| 默认覆盖两侧 | 26.47GiB | 20.69GiB | 41.38GiB | **88.55GiB** |
| 冻结理解侧的估计 | 26.47GiB | 10.36GiB | 20.71GiB | **57.54GiB** |

以上是静态预算，假设相关可训练参数都获得梯度，忽略 tokenizer 扩容、FSDP 填充/低精度副本、VAE、视频激活、CUDA 工作区及优化器临时张量。它不提供实测峰值、单步速度或特定分辨率保证。默认 EMA 在启动脚本中关闭，无需为一个原本不存在的默认 EMA 副本再计费。

据此建议先做获准的小输入、部分参数训练验证。上述88.55GiB与57.54GiB仅是所列假设下的状态估算；实际峰值取决于持久精度、参与损失的参数、优化器实现及卸载策略，默认配置在本实例上能否运行仍待实测。普通CPU offload也存在主存压力。部分冻结配置的实测只能支持其对应范围，不能外推至全参训练。用户已另行批准ENV-01部分参数训练与保存重载验证。

## 当前平台资源与选择

资源目录来自用户截图和后续文字，包含 16 种 GPU。价格与空闲状态是截图时点、指定 CPU/内存组合的信息，未登录平台验证；网页公开访问发生超时。完整目录见 [cloud_resources.json](../../../data/research/audits/env01_static_2026-10-27/cloud_resources.json)。

| GPU | 当前角色 |
| --- | --- |
| A100-SXM4-80GB（80G） | 首选单卡推理验证；具有最大的后训练探索余量，仍不保证默认大范围训练可用 |
| A100-SXM4-40GB、A800-SXM4-40GB（各40G） | 满足官方推理显存起点的备选；具体样例、启动峰值和生成长度待实测 |
| A40、RTX A6000（各48G） | 推理备选；实际价格、速度和目标视频显存待实测，不据显存大小推定性价比 |
| RTX 4090PLUS（平台标48G） | 条件性推理备选；型号属于平台标称变体，租赁前确认单卡可见显存及实际设备信息 |
| RTX 5090（32G） | 低于官方40GB起点，且 Blackwell 需匹配编译环境；不作为本轮原生底座验证首选 |
| RTX 4090、RTX 3090、A30、RTX A5000（各24G）；RTX 3080（10G） | 低于官方40GB起点；本轮不承诺通过卸载/量化即可运行 |
| V100-32GB、V100-16GB、GTX1080Ti（11G）、RTX2080Ti（11G） | 显存不足且不适配当前原生 BF16/FlashAttention-2 路径，不推荐为该底座租用 |

硬件架构依据 [NVIDIA 当前 GPU 表](https://developer.nvidia.com/cuda/gpus)和[旧 GPU 表](https://developer.nvidia.com/cuda/gpus/legacy)；默认注意力库范围依据 [FlashAttention-2 官方说明](https://github.com/Dao-AILab/flash-attention#nvidia-cuda-support)。Blackwell 能否使用当前固定版本还需实机编译/运行验证；本轮未为此切换依赖。

GPU 主机档位：8核/16GB、8核/24GB、16核/32GB、16核/48GB。建议首次模型加载选 **1×A100 80GB + 16核/48GB**；48GB 主存给初始化、CPU checkpoint 读取及数据处理留下更多空间，仍需观测实际启动和保存峰值。先把数据 worker 从默认8降到2。磁盘建议预留约150GB，作为18.38GB模型资产、环境、缓存、日志和少量重载检查产物的规划空间；这是建议值，未获平台配额或实测下限确认。

截图中的 **¥8/小时对应1×A100 80GB + 8核/16GB**；提高 CPU/内存后的价格未知，不能沿用¥8作为最终报价。RTX5090截图为¥3.16/小时且该时点已满。CPU-only `ecs.c1.base` 有2核/2GB、4核/4GB、4核/8GB、8核/16GB，可用于轻量数据工作；本地已可承担当前静态盘点，无需另租CPU实例。

## 下一任务的建议与完成边界

本轮静态盘点子任务已完成。完整 ENV-01 的必需接口、梯度、重载及实测预算仍缺证据，17项实验保持 `planned`，P0发布清单保持 `in_progress`，没有面向main的PR或提交。

建议下一项单独审批为 **A100 80GB 云端最小接口验证**：先固定实际实例和环境，选择已审查的权重子集，分别验证一条视频理解、文本生成视频和合法图像条件输入，记录加载/生成显存、时间、失败及原始媒体。先检查推理结果与资源，再决定单步训练的冻结范围或PEFT方案；不直接把默认65,536 token混合训练脚本交给单卡执行。

后续需确认该16核/48GB配置的实际租价、费用/时长上限、磁盘容量和实例访问方式。本轮只提出这些后续条件，没有租赁或开始新实验。工程检查见证据目录下 `validation.json`；通过结构检查不构成模型能力证据。

后续实测：[官方默认训练策略单卡容量](env01_default_capacity_report_2026-10-27.md)在A10080小型联合批次首次AdamW状态初始化时OOM。该实际结果与本文静态估算分别记录，未将估算替换成实测峰值。
