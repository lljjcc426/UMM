# AnyText / UniVid：实验协议、实现与同名工作审查（第六十三批）

[L025](../reviews/L025.md)、[L027](../reviews/L027.md)补完明确版本核心阅读和五条书面检查。目录347条保持，140项核心阅读、142项书面检查；207项尚未确认核心三遍（包括资源等层级）。没有删除文件、训练、推理或独立复现。以下结果均为原文报告，代码部分为静态选择路径审查。

## 版本、任务与同名区分

| 工作 | 核查版本 | 实际任务与边界 |
| --- | --- | --- |
| AnyText | [2311.03054v5](https://arxiv.org/html/2311.03054v5)，2024-02-21，含A7 v1.1；官方作者仓库/OpenReview交叉为ICLR2024 Spotlight | 指定多语言字符串、位置/可选图像→静态图像生成/编辑。OCR中的stroke为视觉字形特征，无有序笔画/视频事件。正式OpenReview最终PDF尚未逐页比对 |
| UniVid（Luo等） | [2509.24200v2](https://arxiv.org/html/2509.24200v2)，2025-09-30 | BAGEL+Wan adapter耦合，一般视频生成/问答，未验证笔顺任务；最终会议接收未确认 |

AnyText已看实际Fig2，读核心§1–6/Eq1–5/主T2–4与AppA1–3/A7；UniVid已看实际Fig2，读核心§1–5/Algorithm1/主T1–2以及AppA2/A4–7/T3–4/Eq6–16。其它定性样例、引用追读与完整实现尚未全部审查。阅读范围分别写入笔记与验收JSON，未把无运行静态阅读称为复现。

同名研究另列待精读，不移植到L027：

| 研究 | 原始来源与目前证据 | 后续处理 |
| --- | --- | --- |
| Chen / Gu / Mao，UniVid: Unifying Vision Tasks with Pre-trained Video Generation Models | [2509.21760](https://arxiv.org/abs/2509.21760)，作者摘要和[CUC-MIPG代码入口](https://github.com/CUC-MIPG/UniVid)；用视觉句子组织任务 | 当前仅摘要/入口，作者仓库称WACV2026，正式论文集及实验仍待核 |
| Xiao等，UniVid: Pyramid Diffusion Model for High Quality Video Generation | [2603.13739](https://arxiv.org/abs/2603.13739)，2026-03-14，元数据与摘要已读；时空金字塔和双流交叉注意力 | 尚未读核心方法/主表/消融 |
| Yang等，UNIVID: Unified Vision-Language Model for Video Moderation | [2606.05748](https://arxiv.org/abs/2606.05748)，[ACL Industry正式PDF入口](https://aclanthology.org/2026.acl-industry.32.pdf) | 视频审核，当前仅标题/原始入口；全文、架构和正式元数据尚未核 |

这些新线索进入检索/后续队列，未计作新增已精读记录，也未混入573条原有arXiv候选统计。缩写相同不足以认定同一研究或同一模型。

## AnyText：模块与损失

glyph/position/masked-image VAE latent融合为辅助za；TextControlNet接zt+za控制冻结SD1.5。每行字形经冻结PP-OCRv3提取中间特征，线性投影替换CLIP的星号占位，保留其余caption语义。文字感知损失在预测x0解码后的指定区域与真图区域之间比较OCR特征MSE，按区域大小归一并乘alpha_bar_t。它没有直接优化有序笔画事件或OCR分类交叉熵。

训练OCR与测试DuGuang不同，有助减少同一识别器闭环，但不能消除共同OCR偏差。Sen.ACC在给定区域裁图上评价，不能检出所有框外多余字；需另测全图检测、人工字符审核与布局。中英各1000图benchmark的证据不能推广为全部文字体系同等有效。

### 数据与主要结果

v1 AnyWord3034486图、>9M行；约1.6M中文、1.39M英文、10K其他。Wukong/LAION400M及多个OCR集经PP-OCRv3伪标、BLIP2重caption，筛图尺寸/比例、文字面积、行数、行高和置信。训练最多5行×20字符，限制需要单列。每语言1000holdout×4生成；DDIM20/CFG9/seed100/b4。

| T2 | 英文Sen.ACC / NED / FID | 中文Sen.ACC / NED / FID |
| --- | --- | --- |
| ControlNet | .5837 / .8015 / 45.41 | .3620 / .6227 / 41.86 |
| TextDiffuser | .5921 / .7951 / 41.31 | .0605 / .1262 / 53.37 |
| AnyText v1 | .6588 / .8568 / 35.87 | .6634 / .8264 / 28.46 |
| AnyText v1.1 | .7239 / .8760 / 33.54 | .6923 / .8396 / 31.58 |

NED在该文为越高越好的相似度，FID越低越好。v1.1中文FID变差，不能写成全部质量指标改善。GlyphControl不同预训/微调版本另见L025，模型训练分布不同，主表并未隔离架构因果收益。

v1 8A100/AdamW2e−5/b48/10epoch：5生成、3编辑概率.5、2感知λ.01。T3消融另为200K图/160K中文、15epoch/8V100约60h；感知组由Exp5第13epoch继续，不能说各组从零用同一loss训满15epoch。README全量约312h与200K约60h分别记录。

| T3（Sen.ACC / NED） | 数值 | 审查 |
| --- | --- | --- |
| 编辑on / off，无OCR embedding | .1552/.4070 → .2024/.4649 | 编辑任务与纯生成指标有权衡 |
| CLIP视觉 / 卷积 / OCR embedding | .1416/.3809；.1864/.4402；.4595/.7072 | OCR对无embedding off组+25.71个百分点 |
| 去position | .4472/.6974 | 有一定下降，未报告seedCI |
| λ=.003 / .01 / .03 | .4848/.7353；.4996/.7457；.4659/.7286 | .01相对OCR组+4.01pp；不单调，选择是否使用独立validation待核 |

A2单TeslaV100/b4参数1426.7M→1431.6M，3476→3512ms/图。此约1.04%时延差没有方差，不能推出全量训练也同成本。

### v1.1同时变化的因素

A7抽查中文/英文标错率11.8%/2.4%，样本N与CI未公开。中文重标换PP-OCRv4，英文换MARIO-LAION；T7全量3.03M→3.53M，中英趋1:1，去watermark后2.95M。低置信/太小/未选入最多5行的区域加入inv_mask，在噪声回归时抑制。

v1继续5epoch，最后2epoch筛watermark并用λ.003；训练后还用社区RealisticVision V5.0 noVAE替换SD1.5底模。标注、数据、遮罩、loss和基模同时变动，A7未给正交因子，不能将v1.1收益全部归给inv_mask。T8使用私有模型/数据，伪文本119%等超过100，定义分母未充分披露，不将其写作发生概率。

[固定3d4a260代码](https://github.com/tyxsspa/AnyText/tree/3d4a260c67d92c0e27d6e18ed69990e19a40de6d)：当前train.py是200K/15epoch/mask_ratio0/no-perloss的快速实验配置。perloss.yaml给λ.003/CTC系数0；ddpm.py对无效mask后的噪声误差仍取所有像素mean，没有按有效面积重归一。由此推断有效面积不同会改变样本权重，但尚未运行对照验证。README注明重组并对齐各方法配置后数值可有变化，不能假设当前发布与原表完全逐位一致。

### 社区模型作为实际研究资源

[Realistic_Vision_V5.0_noVAE模型卡](https://huggingface.co/SG161222/Realistic_Vision_V5.0_noVAE)全文已读，本次未固定HF revision。元数据creativeml-openrail-m，建议外置SD VAE、EulerA或DPM++2M Karras、CFG3.5–7与超分/denoise范围；缺完整训练数据与可隔离文字收益的量化证据。它是AnyText v1.1实际依赖，已在资源目录和L025记录，未重复计为另一篇论文。

模型卡photoreal负提示包含text/sketch/drawing，若照搬到文字/绘画任务，可能与任务目标冲突；这是需要固定模型做有无负提示实验的假设，未进行推理。代码、数据标注器、VAE、社区底模、训练脚本和采样设置都应进入实验协议。

## UniVid：架构、主结果和可归因范围

BAGEL7B与Wan2.2 TI2V5B通过adapter耦合。StageI只调adapter/DiT交叉注意力LoRA；II用20K ActivityNetQA/4epoch调connector及ViT最后2块，LLM冻结；III交替flow matching与assistant-token CE。完整训练lr/batch/LoRA秩/GPU/联合步数未给，当前推理配置不能代填。默认121帧/24fps、1280×704、50steps、CFG5，约5秒。

| 主结果 | 数值与限定 |
| --- | --- |
| T1生成 | total85.27、quality86.44、semantic80.58；EasyAnimate83.42，+1.85分/相对+2.22%，非2.2pp |
| T1子项 | dynamic61.83、aesthetic64.21；Hunyuan dynamic70.83、EasyAnimate aesthetic69.48更高，并非全子项最佳 |
| T2 QA | MSVD80.1/4.2、MSRVTT61.4/3.4、TGIF75.0/4.1、Activity58.8/3.6；SF-LLaVA对应79.1/4.1、65.8/3.6、78.7/4.2、55.5/3.4 |
| T3生成消融total | base76.25、woMLLM77.82、woTMA80.42、full85.27 |
| T4理解消融（MSVD / MSRVTT / TGIF / Activity Acc） | base64.1/48.9/54.2/39.8；woFT71.1/52.2/63.5/46.5；woReflection73.1/55/64.6/52；full80.1/61.4/75/58.8 |

表支持作者报告系统中的增益，缺全部因子、外部API/帧数/重训预算控制。7B为LLM标签，完整系统还包含DiT/ViT/VAE、检索与外部评估/反思服务，不能解释为单7B系统等预算比较。MSVD与Activity提升是1.0/3.3个百分点，其他两个QA数据集低于SF-LLaVA，无CI。

### 评测协议仍待核的问题

§4.1称VBench，§4.3与结论称VBench-Long，默认时长约5s；具体版本、长时长评测列表和脚本尚未确定。暂按原文分别记录，不能从total分数直接推断长视频证据。

§4.1把58K问答/5800视频称为ActivityNetQA test；[数据作者README](https://github.com/MILVLG/activitynet-qa)和[原论文摘要](https://arxiv.org/abs/1906.02467)说明该数为全库。实际eval split仍待样本文件复核，当前未发现足以证明训练测试泄漏的证据。外部裁判版本/提示与内部confidence校准也未给出可完整复建的协议。

### 公式与公开实现交叉

读取[固定98b5c425源码](https://github.com/AIGeeksGroup/UniVid/tree/98b5c425a15275c4d8b3dc1aaa788134ed6c55f7)的指定路径，差异可能来自发布演进，不能反推原始实验一定用了当前实现。

| 项目 | 论文 | 所读公开路径 | 含义 |
| --- | --- | --- | --- |
| TMA | Eq2–5乘attention score，含text/image时序增益 | model_pipeline hook乘context前段特征，Wan K有归一化，独立cross-attn | 两操作一般不等价；文字softmax总质量仍为1，需核实际注意力池 |
| 进度 | 采样流时间/step | 调度计DiT.forward调用 | CFG条件/无条件若额外调用可能改变边界，须实际trace确认 |
| 外部服务 | DeepSeek v3.1评估/路由，Qwen-plus反思 | BAGEL eval为Qwen评估/汇总/路由、DeepSeek反思 | 当前实现与论文分工反转，均计系统预算 |
| 检索缓存 | 64帧SigLIP2 feature一次缓存后复用 | rank_frames重复emb_imgs，动态64→32重算 | 当前路径不能支持只编码一次的效率主张 |
| 顺序 | 保持帧时间顺序 | 静态selected.extend检索序、动态MMR序，所读路径无显式重排 | 不能假定输入保留时间序；细微动作/笔顺需专项验证 |
| 发布 | 公开系统 | [HF固定a9398c3](https://huggingface.co/AIGeeksGroup/UniVid/tree/a9398c3a9ad197c8f05f46d7b86c4b8f230418fa)只有adapter_model.safetensors、training_state.pt及.gitattributes | 无完整backbone/模型卡/配置，需另组BAGEL/Wan与环境；未下载或加载权重 |

README TODO与实际源码不同步，源码含训练/推理函数，不能写成“没有代码”。根推理导入路径、README理解命令路径/必填id参数还需环境组装验证，静态差异不等已经运行失败。外部Evaluator所读路径用question、全局caption和候选答案评分，未读到输入GT；可能的caption锚定与置信未校准需要实验检验，不能臆称GT泄漏。

AppA5 Eq10–16借随机策略梯度解释query改善。真实代码是离散字符串反思+确定性topk/MMR，没有权重RL更新，也未实际计算所列∇logπ与baseline。Eq15依赖代理目标与真实reward正梯度对齐；从该假设到现实反思效果尚缺独立验证。作为有条件的解释可以记录，不能提升为无条件收敛证明。

## 可证伪设计与论文写作学习

AnyText固定数据量/预算与底模，做OCR标注×无效mask×感知loss×社区底模因子；独立validation择参，测有效面积归一、有无photoreal负提示、框外额外字、多语言/未见字符/作者留出。通用文字成图→逐笔视频还需事件与帧观测监督、规则渲染/静态逐帧/视频条件强baseline。这些实验未执行。

UniVid先核split、评测版本和当前实现，再做同帧数/总token/外部API预算的均匀、相关、MMR、反思对照；外部caption扰动/置信校准、缓存/保序、实际scheduler步与score/feature-gain对照。书写域需测短暂笔画事件、方向和时序，普通视频total不足替代。全部为研究方案。

学习AnyText用编码/控制/监督三个缺口组织Intro，并以模块替代/权重扫描检验；学习UniVid将生成条件与理解检索分问题组织。但Claim必须保留版本、各子项、外部模型和预算，理论假设需对应实际操作，Limitations写出静态/短片/细微时序、标注噪声、评测与发布边界。发现缺口后继续查后续工作，不能直接宣布新颖课题。
