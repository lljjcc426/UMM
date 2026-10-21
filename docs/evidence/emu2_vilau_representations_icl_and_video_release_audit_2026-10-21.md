# Emu2与VILA-U：视觉表示、上下文学习及视频发布协议

第一百零二批完成已有[L083 Emu2](../reviews/L083.md)、[L085 VILA-U](../reviews/L085.md)指定范围核心三遍、实际框架/主表/现有消融和缺失说明、五条书面检查。356目录（329论文／研究、27资源）、205核心/208书面含未通过项，151条未确认核心（含资源）。[结构化审查](../../data/emu2_vilau_representation_and_video_protocol_audit_2026-10-21.json)保留版本、制品及边界。无文件删除、权重/数据媒体下载或模型训练/推理/原表复现。

| 工作 | 已核正文与身份 | 核心贡献 |
| --- | --- | --- |
| Emu2 | [CVPR2024正式14398–14409](https://openaccess.thecvf.com/content/CVPR2024/html/Sun_Generative_Multimodal_Models_are_In-Context_Learners_CVPR_2024_paper.html)，完整12页PDF交叉核Abstract/方法及实际F2/T1/T4–5；完整核心与AppA–E据固定[2312.13286v2](https://arxiv.org/html/2312.13286v2) | 37B连续视觉AR、独立训练图像/视频decoder、base/Chat/Gen三种权重与上下文适配 |
| VILA-U | [ICLR2025正式条目](https://proceedings.iclr.cc/paper_files/paper/2025/hash/e9e140df6de01afb672cb859d203c307-Abstract-Conference.html)确认；完整核心/T1–9/AppA,C据固定[2409.04429v3](https://arxiv.org/html/2409.04429v3) | 语义/重建双目标RQ视觉塔、空间LLM与depth Transformer、原生离散帧生成 |

Emu2正式补充PDF、VILA-U正式PDF均部分下载，未作为已读全文；不是所有附录例图都实际看过，单篇笔记列范围。两工作有视频研究内容，均未建立规范汉字笔顺、抬落笔或逐笔绘画事件体系。通用视频能力与严格书写过程能力分开。

## Emu2：需要按权重与监督阶段解释

EVA02-CLIP-E-plus将图像平均池化成64连续视觉位置，经linear接LLaMA33B；文本预测分类、视觉预测连续embedding，后接独立训练的SDXL图像decoder。StageI只做caption文本监督，224²转448²；StageII冻结视觉encoder并加入视觉回归。Chat静态图改256位置，以答案CE训练；Gen以文本、参考图和bbox黑底定位图条件，只监督末图embedding。这些训练阶段和两类SFT权重不能合并为同checkpoint已验证双向协同。

图像decoder只更新SDXL UNet，encoder/VAE冻结，448²→1024²。其autoencoding训练不需要每步调用LLM，区别于原Emu的条件路径。视频decoder则从SD2.1增加时间卷积/时空attention；v2 F10图注明确视频生成定性示例，但没有对应视频生成主量化表。本批未实际完整核F10图像；当前已核GH/HF主要提供图像解码路径，未确认独立视频decoder发布，不否定论文中的训练与展示。

| 证据 | 观察 | 限制 |
| --- | --- | --- |
| T1 base | VQA0/4/8/16shot33.5/67/67.8/68.8；16shot OK57.1、Hateful66 | OK低于Flamingo57.8、Hateful低于70；0*为文字2shot/图像0shot，与真0shot不同 |
| T2 Chat | VQA84.9*/MSVD49/MSRVTT31.4/MMVet48.5 | 星号任务训练集已见，MMVet是5次judge评分均值；GPT4V67.7仍有差距 |
| T3 grounding | Emu2优于所列多个generalist | CogVLM灰色行全部更高，作者据specialist分类排除；Emu2也用了grounding训练，不能省略 |
| T4 Gen | CLIP-I.686高于SDXL.674/GILL.684；CLIP-T.297低于SDXL.310/SD1.5.302/DALLE3.320 | 正文声称两指标SOTA与表不合；DALLE项CLIP-T只4096样本，其余30K |
| T5 Gen | DINO.766/CLIP-I.850/CLIP-T.287 | 对KosmosG前两项改善、CLIP-T同.287且低于SuTI.304，主体保持与文字遵循分开 |

RICES用于few-shot选择，zero-shot另改输出格式提示，不能把0→4shot差全归视觉推理。T1可说明现有示例数对照，F3和重建CLIP-I.907可说明autoencoder，但**没有同数据/预算的模型尺度、均值/CFormer、目标或decoder严格消融**；不补造消融结论。

正文/附录仍有三处协议差异：语言token3.8B/3.6B，decoder warmup2000/2500步，Gen warmup100步/T9 ratio0。T9分text-to-image/grounded/editing的batch4096/3584/2048及QFT2048/1024/2048，不概括为全阶段同batch。评测Euler50步/CFG3，DreamBench单参考与KosmosG一致、4图/prompt共3000，部分prompt重写；Chat beam5/视频16帧，均应与指标绑定。

## VILA-U：重建与语义取舍有直接证据

视觉塔用SigLIP先验、冻结文本encoder，视觉encoder/RQ/decoder以对比与重建权1:1训练；共享16384码本逐层量化残差。Llama2-7B预测空间位置h，depth Transformer再顺序预测D个码并累加解码。256版16×16×4，384版27×27×16；后者同时换SO400M骨干、分辨率与量化深度，不能只归因分辨率。

| 原文 | 支持的结论 | 不支持的概括 |
| --- | --- | --- |
| T1/T8 | 同码形RQVAE rFID1.30对统一塔1.80；1.3B T2I FID12.0对13.2 | 对齐目标同时改善所有重建/生成指标 |
| T7 | 同SigLIP/25M，加对比使VQA57.7→68.0、MMVet15.3→20.8 | 该下游只用理解数据，无法证明理解/生成联合互益；700M行还混合数据扩大 |
| T4/T5 | 256/384 FID12.81/7.69，但GenAI-Bench基本总分.76/.73、高级.64/.61 | 提高分辨率导致全面质量提升 |
| T6 | 视频74.01/76.26/65.04，对OpenSora75.91/78.82/64.28、CogVideoX81.61/82.75/77.04 | 所有维度超OpenSora或整体优于CogVideoX |
| T9/AppC | CFG3在选定值最好；四种失败训练recipe有经验解释 | 不同数据/架构下同一配方必然失败，或冻结语义特征理论上绝不能重建 |

结论明确“尚未观察到显著理解/生成协同”，本仓库按此保留。多模态预训[image,text]/[text,image]/[text,video]只监督后项，交错只文字、video→text留SFT；框架图“all tokens involved”的概括不能替代实际loss mask。T2把LaVIT标Continuous，与AppA及已核[L079](../reviews/L079.md)的语义量化分类不合，不据此误改原工作。

## 固定代码、checkpoint及时间协议

[Emu GHd9f12f43](https://github.com/baaivision/Emu/tree/d9f12f431a4ea8219bd80ed2aa3173b7fa26fb12)完整184blob，Emu2下未见训练路径；读取root/Emu2 README及6指定文件中的native图像编码/AR/扩散采样/聊天核心。native图像生成逐64位置重算完整前缀，未见KV复用，不能将此当HF远程实现或实测全链路速度。[HF base fa835ec1](https://huggingface.co/BAAI/Emu2/tree/fa835ec101e52da5e081695107e1ddd3c7c4d88a)、[Chat20ea30b0](https://huggingface.co/BAAI/Emu2-Chat/tree/20ea30b04f8fee599cf97535e655c200df728501)、[Gena41a2dcd](https://huggingface.co/BAAI/Emu2-Gen/tree/a41a2dcd777a68225dddc72c7213b064ee06f4a0)元数据/卡与对应config已核，base/Gen64位置、Chat静态256/视频64；Gen是diffusers目录，config在multimodal_encoder下，root config404不能写成缺模型。

[VILA-U GH4ea42ead](https://github.com/mit-han-lab/vila-u/tree/4ea42ead2ce22b035ee74c7966eed245bca3e927)完整91blob，读8指定路径中的MM训练/推理/RQ和架构核心及constants。视频函数固定8帧，256版为2048个高层LLM视觉位置、每位置4残差码；depth循环仍顺序采样，CFG条件/无条件两分支。当前depth采样temperature1/top_p.96/top_k900，不由LLM config文本do_samplefalse推断视觉确定性。`inference.save_video`横向PNG帧条，无fps/MP4；模型能生成帧序列，真实视频时间协议需要另给。

pretrain/SFT默认lr5e-5/1e-4、1epoch/warm.03/context8192。脚本变量global_bs512除节点/acc却未除每节点8进程，在常规DDP和默认整除下预期有效4096；未运行确认、未把它当原表训练batch。README8节点×8GPU/4h为资源申请，不能当实测训练耗时。内部15M和完整视觉塔训练/日志仍限制复现。

官方[HF collection](https://huggingface.co/collections/mit-han-lab/vila-u-7b-6716f7dd5331e4bdf944ffa6)只列[256版91f97e4b](https://huggingface.co/mit-han-lab/vila-u-7b-256/tree/91f97e4b4746e6c2a27a168726ff5a2b9fe0d850)。卡/root/vision/LLM配置确认8视频输入帧、shared RQ/EMA.99、6层depth Transformer/hidden2560/40heads。猜测384仓库路径401不证明其存在或私有；未核到384制品，保留论文实验与发布覆盖的区别。模型制品关联原研究，未重复计论文数。

## 对研究问题和写作的启发

两篇都要求把表征的重建/理解能力、上下文可用性和完整生成能力分开。书写场景先测细笔画/局部帧差能否在64连续位置或RQ码中保留，再固定decoder/encoder、相同样本/FLOPs分别干预压缩、目标、规模和检索。报告OCR/位置计数、事件身份/规范顺序、RGB可观测状态及完整AR+decoder延迟，规则SVG和外部分离组合为强基线。上述均为待执行方案。

Emu2按base/Chat/Gen组织方法和实验便于解释权重，VILA-U先视觉塔再多模态AR、提供取舍消融并坦陈无协同，均可学习。Claim需写具体指标与训练/测试分布、完整预训和选择预算；Limitations应保留失败与反例，论文中的概括性SOTA或速度形容词需要逐表与代码核查。
