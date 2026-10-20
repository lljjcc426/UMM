# CogVideoX：时空压缩、数据与微调协议，第四十六批

深化[CogVideoX G012](../reviews/G012.md)，新增[官方Diffusers微调与检查点配置资源组R11](../reviews/R11.md)。目录344项＝318论文／研究＋26资源；核心三遍108、五条书面检查110。实际读[2408.06072v3](https://arxiv.org/html/2408.06072v3)，[ICLR2025条目](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ce31378e9f41d8907e97dab172b6c559-Abstract-Conference.html)核正式身份；未通读正式PDF全部差异，也未训练／推理／独立复现。无文件删除。

## 问题与设计的对应关系

| 困难 | 机制 | 能验证的对象 | 边界 |
| --- | --- | --- | --- |
| 视频token多／逐帧D闪烁 | 3D因果VAE，空间8×8／时间4 | 重建PSNR、相邻帧变化、token与成本 | 因果卷积不等物理执行因果性 |
| 文本／视频特征域不同 | 模态特定Expert AdaLN，共享full attention／FFN | FVD／CLIP4Clip与loss消融 | expert未采用稀疏MoE路由 |
| 跨位置大运动需间接传递 | 全时空注意 | 对同配置factorized的训练稳定与生成 | 更贵，不普遍否定全部因子化模型 |
| 多形状／时长与高分预算 | Frame Pack与渐进训练 | 数据利用／吞吐／分布表现 | 不等免费增加分辨率／时长 |
| 噪声时刻覆盖波动 | 跨rank Explicit Uniform Sampling | 各时刻验证loss、全局梯度方差 | 所测收敛证据与普适定理分开 |
| 原caption短／数据杂 | 过滤＋密集重描述 | 语义与运动质量 | 文字书写域覆盖和亚秒事件需专测 |

原Fig3／4／5／6／8与10d已视觉核；前三阶段结构和文字／视频潜图接口逐篇说明。生成骨干用整段full attention和v-prediction，VAE的“因果”描述不能转写成逐笔因果执行模型。I2V额外拼图像latent，训练图像条件加噪；AppI的V2V先把原视频变成caption再T2V，语义瓶颈不会自动保留原轨迹／时序细节。

## 几何压缩、token与元素数量要分开

T1的SDXL2D基线为8×8×1下采样、4通道；采用的3D B为8×8×4、16通道。按RGB三通道、忽略首帧边界、同数值精度计算，潜元素压缩比为：

\[R_{2D}=3\cdot8\cdot8/4=48,\qquad R_B=3\cdot8\cdot8\cdot4/16=48.\]

这是依据表中尺寸的自行计算。3D B把时间位置减少约4倍，同时channel增加4倍；不能将token节约直接写成同倍latent元素／字节节约。真实图Fig4是(4f+1)→(f+1)，短片还需计边界。Transformer固定hidden维度时，token数变化仍影响注意成本，压缩收益要按完整输入投影／激活／时延测。

| VAE T1 | PSNR↑ | 相邻帧L1↓ |
| --- | --- | --- |
| SDXL2D，C4 | 28.4 | 93.2 |
| 3D B，C16 | 28.7 | 86.3 |
| 3D C，C32 | 30.5 | 87.7 |

加channel提高PSNR但邻帧指标未同步变好。邻帧L1还随真实运动大小变化，需加入GT运动差分误差、静止复制和细线/OCR重建，不能以最小变化作为所有视频任务目标。极压缩16×16×8／C128难收敛是作者实测边界。

## 数据过滤和描述会改变研究对象

过滤后35M单镜头片平均约6秒，另有2B筛选图像；6个Video-LLaMA筛选器基于20K标注，负类含 **Text Dominated**。因此要测文字主导／手写／屏幕书写视频的筛选保留率；当前没有证据证明全部被滤掉，也不能假定通用训练已充分覆盖该任务。

密集caption先Panda70M短描述、每2秒抽帧CogVLM图像描述、GPT4总结；50K样本训Llama2加速汇总，再训CogVLM2-Caption。描述细节较多不等快速落笔／离纸／笔画顺序已被观察；需对照更密集时间采样与显式事件标签。推理prompt upsampling还可能添加动作或改写字面字符串，应分别评估原提示和改写提示。

最后20%高质量子集FT减少字幕／水印并改善视觉，作者同时承认语义略退化；不能只保留正结果。

## 主结果、消融与成本

主评是选取的VBench五维、Dynamic Quality、GPT4o-MTScore，未给全VBench总分。5B Dynamic Degree62.22低于2B66.39；Scene55.44略低T2V-Turbo55.58，AppearStyle24.44低于VideoCrafter25.13。2B／5B除参数也变位置编码和训练因素，不能当纯参数规模的因果证据。

Fig8把等参数MMDiT1与同层双参数MMDiT2分开，专家调制在后期表现较好，但多参数MMDiT2早期也有优势。factorized在所测配置崩溃不能推出该类模型普遍无效。T8 H800最高分辨率单forward full attention9.60秒、2D+1D4.17秒，质量收益有时间代价。

EUS可理解为噪声时刻分层抽样：等长区间、各rank等权且各区间内均匀时，全局边际仍均匀，减少区间覆盖随机性。T9 40K训练的t100 loss .216对iid .222，t900 .157对.161；图10d更稳定。是否带来不同域、rank和预算下的最终生成收益仍需重复实验。

T5阶段batch2000／1000／250／100、steps400K／220K／120K／10K，分辨率与时长递增；序列25K／75K／700K与T6 max82K的关系未充分解释。不能自行把700K改成70K。T6也未给足各阶段lr／总GPU时。T7 H800／50steps时延113秒等为指定BF16规格，不能套到卡片offload／INT8下限。

人评100自拟prompt对Kling2024.7，正文四维0／.5／1，AppJ写总分0–5及指令门槛；T4总分也不等四维均值简单求和（Cog2.74对2.596，Kling2.17对2.234）。现有说明不足以重建聚合，人数、CI与盲法信息也不全；保留作者报告，不猜造规则，物理观感不当真实执行成功率。

## R11：固定工程协议并保留实际默认

固定[GitHub7a1af71](https://github.com/THUDM/CogVideo/tree/7a1af7154511e0ce4e4be8d62faa8c5e5a3532d2)微调说明／shell／关键实现，以及三个HF固定版本卡与VAE／Transformer config：

| 制品 | 原版2B | 原版5B | 1.5-5B |
| --- | --- | --- | --- |
| HF固定commit前缀 | 1137dac | 8fc5b28 | fdc5267 |
| 默认公开规格 | 49帧／480×720／8fps | 同左 | 81帧／768×1360／16fps |
| Transformer | 30层／30heads／sinusoidal | 42层／48heads／RoPE | 42层／48heads／RoPE，temporal patch2 |
| VAE scale | 1.15258426 | .7 | .7，invert_scale_latents=true |
| 卡推荐精度 | FP16 | BF16 | BF16 |

时间压缩4、latent C16类名相同，不足以证明checkpoint可直接换E-D。训练encode段只见乘scale，未处理invert分支，完整依赖pipeline尺度语义还需进一步核对，不宣布已验证兼容。论文T6的2B32heads、timeembed256和BF16与卡/config的30heads、512、FP16分别保留。

实际默认LoRA r128／alpha64，Q/K/V/out投影；AdamW lr2e−5、β.9/.95、wd1e−4、100warmup+constant、clip1。shell以1.5／81×768×1360、b1、10epochs、seed42、bf16为例，validation=false。冻结VAE／T5和base，仅训adapter；SFT则训Transformer。当前trainer用每样本iid randint，未实现论文跨rank EUS；固定1.5 scheduler config为v_prediction／zero-SNR／1000步；loss变量名predicted_noise不能直接解释成ε目标，代码还有scheduler变换与按1／(1−alphabar)加权latent误差。依赖让用户安装Diffusers main而未锁commit，不能称配方已完整可复现。

数据为逐行prompt／video，I2V可选image。固定resize会改变长宽比，抽帧会影响事件可观测性；缓存和预编码成本需计入。文档基于70段视频的经验建议没有充分定量消融，rank／alpha不能照单称最优。旧HF卡LoRA47／63GB与后续guide16／24GB来源配置不同；guide某SFT行称每卡42GB／4090，与[NVIDIA标准4090的24GB](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/)不一致，设备／单位需澄清，不能按该行配置实验。INT8和offload低显存亦可能更慢，未在本设备测量。

该资源无独立方法论文定位，作为同一工程资源组关联G012；三个卡不增加三篇论文。代码/2B与5B模型许可字段分别记录，未推导额外法律结论。未下载模型权重。

## 可证伪实验与写作学习

先测同域外域VAE重建：压缩×channel固定元素预算、重建OCR／细线拓扑／GT差分／事件时标；再测生成。full/factorized×等参数/等计算、Expert/MMDiT×等参数/等层、EUS×rank/seed分别控制。过滤器对书写样本的保留率和caption亚秒覆盖单列；prompt改写需保持目标字面与先后约束。微调LoRA rank×alpha/r对SFT用等样本／墙钟与独立字形/作者split，记录训练/验证峰值、latent-cache和整个推理开销。以上未执行。

Introduction的问题需对应压缩、融合和数据机制；Method明确每个时间变量、冻结/可训对象、训练阶段和实际默认；实验负指标、边界与超参差异保留。Claim限定版本／任务／指标，Limitations把代理指标与事件能力、论文与制品差异、未公开配方区分。后续MAGVIT2、视频tokenizer、Frame Pack相关原始研究与CogKit需去重独立读，出现链接不计完成。
