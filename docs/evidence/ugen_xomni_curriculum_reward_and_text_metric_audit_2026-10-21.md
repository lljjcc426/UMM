# UGen与X-Omni：视觉词表课程、图像奖励及文字指标复核

第一百零五批完成已有[L091 UGen](../reviews/L091.md)、[L093 X-Omni](../reviews/L093.md)固定预印本核心三遍、实际框架/主表与已有消融、五条书面检查。[结构化来源与范围](../../data/ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.json)。目录356（329论文／研究、27资源），211核心/214书面含未通过项，145条未确认核心（含资源）。无文件删除、权重/图像数据下载、模型推理训练或原表复现。

两篇研究均涉及文本与静态图像。UGen研究渐进激活离散视觉ID；X-Omni以GRPO优化离散AR输出，随后仍用FLUX扩散生成像素，并提出英文/中文长文字图像基准。通用图像生成和文字渲染与规范书写过程的任务定义分开。

| 工作 | 主要来源 | 实际核看图表 |
| --- | --- | --- |
| UGen | [2503.21193v1](https://arxiv.org/html/2503.21193v1)，唯一列出版本，完整13页PDF交叉、§1–5/Alg1/Eq1–5/T1–5 | F2框架、完整T2、PDFp8 F6/F7/F8；HTML部分SVG对象空白后改读完整PDF，未把空白图标已读 |
| X-Omni | [2507.22058v1](https://arxiv.org/html/2507.22058v1)，§1–5/GRPO公式/T1–4/附录A；[作者项目](https://x-omni-team.github.io/)与固定GH/HF | F3框架、F2 RL流程/BoN曲线、完整T1 |

两项正式会议/期刊身份未由一手出版材料确认，按预印本记录。检索结果中的ICLR论文仅引用UGen，不能作为UGen录用证据。

## UGen：课程收益与未解决的协议问题

TinyLlama1.1B/32K文本词表/context4096，加MoVQGAN67M/16384视觉词表；256²图变32²=1024码，三类序列均通过共享decoder、全序列等权CE。仍复用预训练文本模型和视觉codec。Alg1激活集初始只有文本ID，每k步随机从未激活视觉词表取一个ID，其他视觉位置替换为MASK；全部激活后继续训练。预训三类数据3:2:5，SFT2:6:2。

预训30M文本与30M图文（生成为同图文反向，不能再计30M独立图像）；CogVLM重描述、内部1M图文。SFT又包含内部文本/理解/生成各1M及公开数据。部分SFT来源与被测语言基准同名，未给精确train/test清单，需补划分和去重证据，当前不能判定测试泄漏或声称完全无相关监督。

| 证据 | 结果/问题 | 解释边界 |
| --- | --- | --- |
| T2主控制 | Vanilla文字42.1/理解61.0/生成42.5→UGen46.1/66.0/52.1 | 分别+4.0/+5.0/+9.6百分点，支持所测课程改进；作者13.3%为综合相对说法，非每项+13.3或13.3百分点 |
| 单任务/原始基座 | 单任务48.8/66.4/55.9，原TinyLlama文字52.9 | 仍有退化；不能把缩小混训差距写成共享模型超过全部专用模型 |
| T4–5分项 | GQA58.2高于单任务54.9，但VQA70<73.1/MME55.5<56.4/POPE80.4<81.2；计数33.7<45/位置26<35 | 有利分项与反例共同限定Claim；GenEval总52.1低于Show-o53/Emu3Gen54/SDXL55/Janus61 |
| F6 PPL | UGen曲线比vanilla低 | 逐步MASK改变目标熵/可预测性；需同一未mask验证集、固定词表、分模态PPL才可解释优化差异，不能单独证明“融合/冲突消失” |
| F7课程速度 | k3/6/9/∞，至600K；k9约200K最高、k6约500K最高、600K略降 | 最佳k依赖预算；主T1仅500K、未明主表默认k/随机顺序；不外推普遍最优 |
| F8随机初始化 | 文字39.8→43.8、理解60.4→65.1、生成38.2→42.0 | 所测scratch设置也有收益；无多seed/置信区间，未隔离词频、mask课程与目标熵 |

算法与图注有直接待核点：F7称k=∞等同Vanilla Unified AR，但按Alg1初始仅文本激活、每k步新增视觉ID，∞会使视觉位置持续MASK；这与“全部视觉ID直接混合”的vanilla定义不一致。没有原代码或作者澄清，不替作者猜测修正。

语言正文列8基准含SIQA，附T3仅BoolQ/PIQA/HellaSwag/WinoGrande/OpenBookQA/ARC-e/ARC-c共7项，显示Avg与七项平均相符；应标记“正文8项与附表7项不一致”。理解平均前MME按/20归一，例如1110→55.5。主T2 Janus/Show-o语言41.0/36.1，附T3 40.7/36.0亦有差异，不能交叉择数。

训练T1为预训AdamW/lr1e-4/cosine/wd.01/clip1/b256/warm5000/500K，SFT lr3e-5/b128/warm1000/10K，推理CFG5。同数据/基座/配置的对照优于跨模型大表推因果，但仍需核单任务vs混合的每任务暴露、三专用模型总计算及完整训练日志。所选一手链接/定向检索未确认官方完整代码/权重或硬件成本，不代表网络上绝无其他制品。

## X-Omni：RL优化的是含扩散解码的完整图像奖励

SigLIP2-g-patch16语义encoder与VQ先在Qwen1.5B理解任务中训练，再冻结；码本16384、维2048。Qwen2.5-7B原28层前后各加4视觉block，共36层及视觉embedding/head。理解监督文字，生成监督视觉码；视觉码经线性条件接FLUX.1-dev扩散decoder，后者恢复像素。所谓统一离散AR针对中间序列，系统仍含独立视觉codec、扩散和外部奖励模型。

PT约200M图/600Btoken与59M理解/100Btoken；三阶段42B/629B/42B训练token，先新视觉参数再全部AR、最后退火。SFT1.5B，RL180Kprompt。GRPO每prompt16rollout，冻结decoder成图后加权HPSv2、UnifiedReward、Qwen2.5VL32B对齐、GOT-OCR2与PaddleOCR奖励，组归一优势/clip/KLβ.01，lr1e-6/200step/b512。精确奖励权重、clipε和完整codec/decoder训练成本未公开齐全。

| 主表/分析 | 结果 | 限制 |
| --- | --- | --- |
| T1文字 | OneIG EN.901/CN.895；LongText EN.900/CN.814 | CN LongText低于Seedream3 .878，EN低于GPT4o .956；正文“中文超过全部”与表及官方HF榜不符 |
| T2 DPG | 87.65高于表中Show-o2 86.14/GPT4o86.23 | global84.8低于DALLE90.97，other84.2低于Show-o2 91.64；GPT4o仅每prompt1图且拒绝prompt被剔除，评估子集不完全一致 |
| T3 GenEval | .83，采用prompt rewriting | 低于Mogao.89/BAGEL.88/OmniGen2.86/BLIP3o.84，不能全称最优；GPT4o数来自外部报告 |
| T4理解 | POPE89.3/GQA62.8/MMB74.8/SEED74.1/Doc88.6/OCR704 | MMB低于JanusPro79.2/Show-o2 79.3，OCR低于MiniCPM725；没有RL前后多seed理解对照来证明双向协同 |
| F2奖励 | 约.416→.577，SFT BoN8=.513、BoN16=.529 | 当前训练奖励优化证据；缺独立heldout/同总成本SFT拒绝采样/逐奖励消融，不能证明任意N/数据分布上RL都更好 |
| CFG | 定性显示AR在CFG1仍可生成 | 公共FLUXdecoder28步、true_cfg1.5、条件/无条件双分支；AR无CFG不等于整流程无CFG、无扩散或已有端到端提速实测 |

误差累积和token-decoder分布差是合理动机，但没有单独测GT/预测码解码误差、各rollout位置偏移或干预实验。奖励提高可有多种解释，不能直接确认为两种机制均被解决。

### LongText-Bench度量的实际语义

附录与[固定GH](https://github.com/X-Omni-Team/X-Omni/tree/2b8237bb3789638c290eeda3e83ed81bd3652c3b)交叉：英文、中文各160条，8场景各20，short/long各80；ID范围0–199但不连续，不能按最大ID推200条。每prompt生成4图，Qwen2.5-VL-7B做OCR；英文short多10–30词、long30–50词，中文short20–40字、long多>60字。该覆盖不代表任意文字体系。

`summary_scores.py`对英文词/中文字符建立Counter，以多重集交集数量除以GT数量，最终为全部匹配数/全部GT数。故为长度加权的无序内容召回，不罚OCR多余文字，英文小写、去大部分标点。静态公式推导GT“甲乙”、预测“乙甲丙”可得1；GT英文“red car”、预测“car red extra”亦可得1。未运行作者生成或OCR，也未据此断言原表分数错误。该指标应与有序CER/WER、precision、整串exact、布局和人工核对并列，无法验证合法书写顺序。

原论文因OCR片段顺序不稳而弃Edit Distance是明确设计取舍，但真实布局与顺序正确性因此未被测到。识别器输出也可能漏字/幻觉；训练OCR奖励与测试OCR不同能减少部分直接同模型耦合，仍需人工和独立OCR证据。

### 固定发布制品及可复现边界

| 制品 | revision | 已核范围 |
| --- | --- | --- |
| GH | 2b8237bb3789638c290eeda3e83ed81bd3652c3b | 完整10blob树、README/生成/聊天/两语prompt与三个评价脚本；无原PT/SFT/GRPO完整训练入口 |
| [X-Omni-En](https://huggingface.co/X-Omni/X-Omni-En/tree/db70091623513f616c6da7a049773ec5934be88e) | db700916 | 卡/config/指定modeling与decoder片段，apache-2.0卡元数据 |
| [X-Omni-Zh](https://huggingface.co/X-Omni/X-Omni-Zh/tree/9ec2a05d820a845e881fdb5a74486260407edd5f) | 9ec2a05d | 单独中文模型目录/元数据，不能将En/Zh当同checkpoint同时能力 |
| [PT](https://huggingface.co/X-Omni/X-Omni-PT/tree/51a5d872fcc0cd1ed251030fad194fbde0b09f7f) / [SFT](https://huggingface.co/X-Omni/X-Omni-SFT/tree/6c1b96fad2c9619e4826a21eb51a107d274ccdaf) | 51a5d872 / 6c1b96fa | 发布元数据/目录；存在checkpoint不等于完整训练和原实验已复现 |
| [LongText-Bench](https://huggingface.co/datasets/X-Omni/LongText-Bench/tree/429e30e9c1e0dea535038ae4238ea6ec42823098) | 429e30e9 | 卡/目录；实际prompt统计读取固定GH两文件，不假定HF文件逐字同版 |

公开生成默认1152²、downsample16→72²=5184 AR码，temp1/minp.03/topp1/seed1234、ARCFG1，然后28步扩散。HF config maxpos8192与论文训练16384不同，尚未验证长上下文能力边界。视觉block输出用mask保留文字，但代码仍计算层后再where，不能称文本完全不增加计算。

当前入口有直接可见的适配点：中文README用`--model_path`而parser要求`--model_name_or_path`；`eval.sh`合并写`results.jsonl`但最后传`results.json`；所读HF forward labels分支按文本vocab reshape，而logits维度包含mm词表，不能将它当已确认可直接复用的完整训练代码。以上为静态阅读，未运行模型验证，也未擅改外部仓库。

## 能检验的机制与写作思路

UGen需比较全激活、固定随机mask、渐进mask率、按词频/语义激活、新embedding预热和梯度隔离，固定token/FLOPs/曝光，在共同未mask验证集报告分模态CE与下游指标，多seed扫k/预算。X-Omni需逐奖励移除、随机奖励、同调用预算BoN/拒绝采样SFT或DPO，测GT码/生成码与rollout位置误差，用独立人评和有序文字指标评估奖励泛化。均未执行。

对书写视频，先确定真实顺序、笔画身份、抬落笔和RGB逐帧可见性，再讨论课程或RL；只有可识别内容奖励容易忽视顺序/多余字。规则SVG/纯轨迹渲染、专用生成器与独立识别组合应作为强对照。

可学习的Introduction写法是从可观察失败提出局部机制假设，Method按表示/优化接口组织，实验分别检验主效果与各机制。Claim需区分绝对百分点/相对聚合、奖励/独立质量、静态内容/真实顺序；Limitations明确协议矛盾、评价取舍、商业API子集、En/Zh变体、外部教师与完整成本。
