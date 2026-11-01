# 模型接口与资源可行性矩阵

2026-11-01。代码/模型卡版本见[机器注册表](../../../data/research/next/model_registry.json)，任务映射见[配置](../../../configs/research/next/model_task_matrix.json)。本轮只读取官方元信息、README、许可证及选定接口代码，没有下载模型/数据载荷、执行新模型或声称汉字能力提升。

`verified_supported`表示已核到发布接口，不能解释为字形、笔顺或过程准确率经过验证。既往真实运行另记。`unsupported_by_released_interface`仅限审计的发布接口；`not_verified`表示证据不足，不能外推模型理论能力。

| 固定制品 | 已核接口 / 状态输出 | 既往实际证据 | 参数与资源边界 | 下一步限制 |
|---|---|---|---|---|
| Lance_3B_Video `73953157`，code `4baeee08` |原生T2V/I2V、视频问答|P0/P1真实执行，质量负结果保留|主权重7,105,548,336元素含ViT/位置表，另VAE；3B为active标签；P1整卡采样峰37283MiB，RSS约33.79GB|当前Mac无官方运行证明；全参AdamW曾OOM；新24调用需授权|
| BAGEL-7B-MoT `5019f57d`，code `a2fa77dd` |图像理解、生成、交错图像；发布接口无稠密T2V|本项目未运行|作者7B active/14B total，HF元素14.691B含组件；标准app指导32GB+，不能保证长轨迹显存|Apache2，需新权重与任务峰值核验|
| Bagel-Zebra-CoT `ebce3241`，code `bbf53c32` |`infz_bf16.py`交替文本/图像并回灌；无原生稠密视频接口|未运行；与上传SC-CoIT基座一致|继承BAGEL架构，准确制品参数数/任务峰值未知|Apache2；同step重画/RedX需要额外实现和实测，不能直接宣称已有SC-CoIT|
| UniVideo hidden `c84ceb49`，code `893c9da0` |同hidden制品有图像/视频理解、T2I/T2V/I2V|未运行|Qwen2.5-VL7B＋HunyuanVideo13B，完整元素/峰值未知|hidden与queries分开；训练MLLM/VAE冻结，官方全Transformer AdamW不适单80GB；子权重许可分别核|
| PixelUMM S8-F22-R05 `4bb3ce9a`，code `e19e91aa` |同F22支持图像/视频理解和生成|未运行|作者15,199,672,064参数；README T2V=320×176/96帧/24fps/35步；单卡峰值未知|权重非商业研究/评价许可；CUDA13开发环境、FlashAttention、TorchCodec共享FFmpeg；默认guardrail另有访问要求；toy训练7×≥48GiB|
| InternVL-U `f012d760`，code `018a59c1` |图像理解、生成、编辑、text_image；当前接口无稠密视频|未运行|作者4B；完整计数、Mac/MPS和任务显存未知|实际HF权重LICENSE为MIT；4B名称不能保证16GiB本机可运行|
| SenseNova-U1.5 final `9feeeab8`，code锁`feat/u1.5`的commit |图像理解、生成/编辑；无已核原生视频|未运行|HF存储参数17,532,854,464；8B-MoT名称不能当总驻留8B|Apache2；最终U1.5与U1.5Preview训练指南不能混用；CUDA12.8环境未部署|
| LTX2B distilled `8984fa25`，code `4b2d0530` |生成专用T2V/I2V，缺统一理解接口|本机既往2有效低清33帧视频，均无合格逐笔过程|transformer约1.923B、VAE约1.247B，T5另计；既往MPS驱动视频峰约7.17GiB、文本编码约10.16GiB，不能相加|LTXV Open Weights License；作为生成模块对照，不能与同权重UMM理解成绩合并|

Lance本次24请求统一使用已实测视频检查点/视频入口。K-CHAR、V-STRUCT把同一静态图重复为33帧载体，K-ORDER使用空白视频载体；明确记录该适配，未把图像权重接口能力拼给视频权重。静态重复不构成视频输出过程证据。

BAGEL/Zebra将多张状态图保存到目录，即使另行编码为MP4，原生输出仍登记interleaved_images，不能通过任意插帧变成33帧native_video。PixelUMM F18-R01不支持视频理解，禁止把F18生成与F22理解拼在一条结果上。UniVideo冻结理解模块的统一系统也不提供“共享联合更新收益”的证据。

普通G-only SFT/PEFT是必需的强基线，LoRA接入和确切参数名尚未验证，不能写成可直接运行训练。[VideoSketcher作者论文](https://arxiv.org/abs/2602.15819v2)以合成结构学习时序、再用少量手绘例学习风格，支持设置同数据等曝光课程对照；本项目不借用其报告数值，不将“借鉴课程”写成精确复现。后续恢复对照见[训练配置](../../../configs/research/next/training_comparison.json)。

一手核验入口：[Lance](https://github.com/bytedance/Lance/tree/4baeee086648996f6ab12e673cbe461b0b149997)、[BAGEL](https://github.com/ByteDance-Seed/Bagel/tree/a2fa77dd8caeefc41e6607ae0ec17408d3f4ee9f)、[Zebra](https://github.com/multimodal-reasoning-lab/Bagel-Zebra-CoT/tree/bbf53c327889a1764d27989d117d1a6b73ffdd3f)、[UniVideo](https://github.com/KlingAIResearch/UniVideo/tree/893c9da04b87fdf5099e8e0e9ef164bca6753327)、[PixelUMM](https://github.com/nv-tlabs/PixelUMM/tree/e19e91aabb99784f7b5524268ed42ec59c1ad660)、[InternVL-U](https://github.com/OpenGVLab/InternVL-U/tree/018a59c1b69690a33698234128aa04e9b3f46c71)、[SenseNova-U1.5](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT/tree/9feeeab8a2792514d109cd34589342a2cc1d4ab2)。链接和本地只读快照逐项列在注册表，能力表不作为性能排名。
