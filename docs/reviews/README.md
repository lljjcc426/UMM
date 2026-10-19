# 第二轮原文阅读与批判分析

以下笔记按实际阅读范围记录。相关章节核查不等于三遍完整精读；没有进行模型复现。未填完的实验条件与消融明确保留，不能计作全部完成。

[逐条完成台账](../evidence/reading_ledger_2026-10-19.md) · [理论与实验迁移](../evidence/foundations_and_transfer_2026-10-19.md)

| 编号 | 论文 | 核查范围 |
| --- | --- | --- |
| U18 | [Transferability Between Understanding and Generation in Unified Multimodal Models](U18.md) | §3–5；Tables1/3/4/10/11/12；Appendix0.A、0.B.2、0.C、0.E |
| L010 | [VideoSketcher: Sequential Sketch Generation Using Video Model Priors](L010.md) | §3–7，Tables1–2，Figures2/3/7/10/12，Appendix B.3 |
| A03 | [DiffInk: Glyph- and Style-Aware Latent Diffusion Transformer for Text to Online Handwriting Generation](A03.md) | §3–4；Table1/2；Appendix A、B.3/B.4 |
| A02 | [Decoupling Layout from Glyph in Online Chinese Handwriting Generation（OLHWG）](A02.md) | Abstract、§4.1–4.3、Table1/2、对比损失消融；附录参数未完整转录 |
| A05 | [Handwriting Trajectory Recovery with Diffusion Models](A05.md) | Abstract、§4.1/4.2、Table1；完整消融待读 |
| A07 | [Complex Handwriting Trajectory Recovery: Evaluation Metrics and Algorithm（PEN-Net）](A07.md) | Abstract、§5.1–5.3、Table1协议；结构消融待补 |
| A09 | [Disentangling Writer and Character Styles for Handwriting Generation（SDT）](A09.md) | Abstract、§4.1设置；完整消融与训练附录待补 |
| A10 | [Diffusion Models for Handwriting Generation](A10.md) | Abstract、§5.1、Table1及采样消融 |
| B02 | [Moyun: A Diffusion-Based Model for Style-Specific Chinese Calligraphy Generation](B02.md) | Abstract、§4.1、Table1/2和用户研究说明；训练/消融未完成 |
| B07 | [Inverse Painting: Reconstructing the Painting Process](B07.md) | §1、3、4、Fig3/5；Appendix A.3、B.3/B.5/B.6 |
| B08 | [AnimatePainter（arXiv:2503.17029）](B08.md) | Abstract、§4.1/4.2、Table2；完整结构消融尚未抽全 |
| L013 | [ProcessPainter，2024](L013.md) | Abstract、Table1、§4.4.2/4.5、Fig7；样本数与预算待核 |
| L017 | [DiffSketcher，2023](L017.md) | Abstract、Appendix D/Table1、Appendix E；主方法核心目标 |
| D05 | [Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion](D05.md) | §3–5，Table1、受控消融说明，Appendix A训练细节 |
| E01 | [Mean Flows for One-step Generative Modeling](E01.md) | §4–5，Table1，实验配置及JVP消融 |
| U01 | [Chameleon: Mixed-Modal Early-Fusion Foundation Models](U01.md) | §2.1–2.4，Tables1–2/7，训练稳定性曲线 |
| U02 | [Emu3: Next-Token Prediction is All You Need](U02.md) | §2数据/模型，Tables1–3/7–8及视频VBench表 |
| U03 | [Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation](U03.md) | §3训练目标/阶段，§4.1/Table1，§4.5/Table5 |
| U04 | [Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling](U04.md) | §2.1–2.3，训练Table2，§3.1及主评测表 |
| U05 | [Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model](U05.md) | §3目标/attention，§4.1，§4.3/Table5及patchsize讨论 |
| U06 | [Show-o: One Single Transformer to Unify Multimodal Understanding and Generation](U06.md) | §4.1/Table1，Table4及表示选择研究 |
| U17 | [Uncovering Understanding-Generation Synergy in Native Unified Multimodal Models: From Representation, Task to System](U17.md) | 摘要，§3/Table1与探针，Tables4–5，系统任务说明和SVG诊断附录 |
| A01 | [DP-Font: Chinese Calligraphy Font Generation Using Diffusion Model and Physical Information Neural Network](A01.md) | 原始PDF方法、§4.1/4.4，第7页Tables2–3/Fig6视觉核对 |
| B04 | [AnyText2: Visual Text Generation and Editing With Customizable Attributes](B04.md) | 方法框架、训练/推理配置与对比来源说明；数表待补 |
| B05 | [Kinetic Typography Diffusion Model（KineTy）](B05.md) | 数据/架构、训练设置与基线；主数表待补 |
| B06 | [Dynamic Typography: Bringing Text to Life via Video Diffusion Prior](B06.md) | 方法、数据和实现/公平比较设置；消融数表待补 |
| A04 | [Stroke Modeling Enables Vectorized Character Generation with Large Vectorized Glyph Model（LVGM）](A04.md) | 摘要、§3数据、§4两阶段表示、§5.1–5.5及§6限制；Table2/3文字，未逐图视觉验收 |
| A08 | [Modality Conversion of Handwritten Patterns by Cross Variational Autoencoders（Cross-VAE）](A08.md) | 摘要、§II–III空间共享损失、§IV-A至D含TableI；未完成所有图像视觉核查 |
| A11 | [Stroke Extraction of Chinese Character Based on Deep Structure Deformable Image Registration](A11.md) | 摘要、方法三模块、实验数据/训练、Tables2–5及Limitations；代码未运行 |
| L001 | [Handwriting Trajectory Recovery via Autoregressive Ordered Stroke Instance Prediction，2026](L001.md) | 摘要、方法主要模块、§4.1/Table1、Tables2–4及跨语言设置；完整符号和附录仍待补核 |
| X01 | [InkSight: Offline-to-Online Handwriting Conversion by Teaching Vision-Language Models to Read and Write](X01.md) | §3架构/五任务/token，§4.1–4.7数据、Table2/3及限制；AppendixG尚待完整摘录 |
| L012 | [SketchAgent，2024/2025](L012.md) | §4、§5.1–5.2、Table1/2、§6–7与官方CVPR书目信息；未完成全部交互附录 |
| L014 | [Generating Past and Future in Digital Painting Processes / PaintsAlter，2025](L014.md) | 原始13页PDF§3主要框架、§3.4数据/训练、§4.2–4.7及Tables1–4；逐图视觉核对尚未全部完成 |
| L015 | [Loomis Painter，2025](L015.md) | §3–4、§5实现/Table2/3、§5.2.1PDP、§5.3消融、§7限制；附录未完整精读 |
| L016 | [StrokeNUWA，2024](L016.md) | §3.1–3.2、§4.1–4.3、§5及Tables2–4；官方PMLR书目核对 |
| F02 | [Bézier Splatting for Fast and Differentiable Vector Graphics](F02.md) | 摘要、表示概述、§4.1–4.3和Tables1–3、限制与AppendixA/B；源码未运行 |
| F03 | [FRIDA: A Collaborative Robot Painter with a Differentiable, Real2Sim2Real Planning Environment](F03.md) | §III笔画/模拟器/规划、§IV设备、§V对比/重规划及§VI限制；官方作者页确认ICRA2023 |
| F04 | [CoFRIDA: Self-Supervised Fine-Tuning for Human-Robot Co-Painting](F04.md) | §III数据/高层微调、§IV评估、TableI、§V/限制；官方项目与HF原始README/文件清单交叉核查 |
| D01 | [HunyuanVideo 1.5 Technical Report](D01.md) | §2数据、§3架构、§4训练及Tables3/7/8；未逐项摘完所有训练规模和人评协议 |
| D02 | [LTX-2: Efficient Joint Audio-Visual Foundation Model](D02.md) | §3表示/双流、§4推理、§5数据、§6速度/评测与§7限制 |
| D03 | [VACE: All-in-One Video Creation and Editing](D03.md) | §3 VCU/adapter、§4数据及benchmark、§5对比/消融；完整大表逐数核对仍待完成 |
| D04 | [Wan-Move: Motion-controllable Video Generation via Latent Trajectory Guidance](D04.md) | §3 latentguidance/训练、§4benchmark、§5/Table4、§8.3训练与§9.4failure |
| D06 | [Self Gradient Forcing: Native Long Video Extrapolation](D06.md) | 摘要、方法两遍梯度路径、§4.1协议、§4.5/Table4及结论；长主表尚待逐项摘录 |
| D07 | [Salt: Self-Consistent Distribution Matching with Cache-Aware Training for Fast Video Generation](D07.md) | 摘要、§4.2–4.4/Tables1/2/4，AppendixB实现和动态分讨论；§3公式尚需完整推导 |
| D08 | [Wan-R1: Verifiable-Reinforcement Learning for Video Reasoning](D08.md) | 方法奖励/VideoGRPO、§4.1–4.4、主实验概述、AppendixTable4；Table2逐值与全消融待补 |
| E02 | [Improved Mean Flows: On the Challenges of Fastforward Generative Models](E02.md) | 摘要、§4.1/JVP/stopgrad、§5.1/Table1、§5.2/Table2、AppendixTable4；全部数学证明未完成 |
| E04 | [Discrete Flow Matching](E04.md) | 摘要、§2主要概率路径/采样概念、§3masked命题、§4实验设置与代码结果；AppendixD/G及全部证明未读完 |
| E06 | [Timestep Embedding Tells: It's Time to Cache for Video Diffusion Model（TeaCache）](E06.md) | 摘要、方法输入差/重标定、§4.1–4.3及限制讨论；多项式系数与代码未独立复核 |
| E07 | [clDice: A Novel Topology-Preserving Loss Function for Tubular Structure Segmentation](E07.md) | §2定义、§3定理/推论前提、§4softskeleton、§5数据/指标/Table1概述；完整证明与补充训练配置未全部复核 |
| B01 | [Calliffusion: Chinese Calligraphy Generation and Style Transfer with Diffusion Modeling](B01.md) | 方法/训练、Tables1–2及Limitation全文段落；图仅核图注，LoRA配置及原会议论文集待核 |
| B03 | [InkDiffuser: High-Fidelity One-shot Chinese Calligraphy via Differentiable Morphological Optimization](B03.md) | HTML§IV公式及§V TablesI–III、结论；GitHub固定树/train.py/configs/fontdiffuser.py/dis_loss.py；PDF公式视觉核对与实际训练版本尚未完成 |
| B09 | [DiffMath: Symbol- and Graph-Aware Latent Diffusion Transformer for Handwritten Mathematical Expression Generation](B09.md) | §3轨迹VAE/RelAST/DiT、Tables2–4、Appendix0.B训练和基线；更多OCR增强结果与代码未全部复核 |
| L004 | [Layout Stroke Imitation，2025](L004.md) | §3模块/公式、§4 Tables2–4及Discussion；补充材料超参、原PDF表视觉与代码待核 |
| L005 | [StrokeBank，2014](L005.md) | 作者6页PDF的方法、公式2–5、Tables1–2、数据及局限；图读取图注，正式书目和源码未核；已视觉核对PDF第3–4页部件图、DEF示意、式2–5与Table1，确认式5方向差异 |
| L009 | [Video-Based Handwritten Chinese Character Recognition，2005](L009.md) | 作者8页PDF §II–V方法/纠错/实验及Conclusion；TableI细分数字与图像逐项视觉尚待核 |
| L018 | [Diff-Font，2022 起](L018.md) | §3条件/CFG、§4.1–4.4 Tables1/2/4及跨语种表示；完整版本对齐、韩文实验与全部附录未完成 |
| L019 | [FontDiffuser，AAAI 2024](L019.md) | Method三模块/对比loss、数据/条件、Tables2–4；Table1大表全部数值及附录未逐项核完 |
| L046 | [AWCV100K](L046.md) | PDF§III数据、§IV特征/网络、§V设置与TablesIII–V；其他消融表/正式终版与代码待核 |
| L049 | [SCUT-COUCH2009-TL](L049.md) | PDF采集/标注/算法§2–5、Tables1–4；完整文件规范/授权与当前下载未核 |
| L048 | [Tegaki](L048.md) | 官网功能、API样例、FAQ全文；源码/版本/实际字体导出与质量尚未验证 |
| L050 | [CASIA-OHFC](L050.md) | 官方说明的数据/partition/usage/InkML格式；压缩包与配套论文实验尚未完整核查 |
| L047 | [Recontextualizing Revitalization: A Mixed Media Approach to Reviving the Nüshu Language（NüshuVision / NüshuStrokes）](L047.md) | ACL正式元数据；10页PDF正文、实验Table1、Limitations/Ethics及AppendixA–D文字；官方仓库目录页；未逐图验收/运行代码 |
| C01 | [Emerging Properties in Unified Multimodal Pretraining（BAGEL）](C01.md) | §2架构/注意力、§3数据Table1、§4训练Table3、§5–6消融与能力曲线、§7主表相关行；附录评判说明；完整硬件与所有表值未逐项核 |
| C03 | [Hyper-Bagel: A Unified Acceleration Framework for Multimodal Understanding and Generation](C03.md) | §2文字草稿与data，§3全部蒸馏阶段，§4主表/ablation相关行；配置细节和代码尚未完整复核 |
| C04 | [Flash-Unified: A Training-Free and Task-Aware Acceleration Framework for Native Unified Models（FlashU）](C04.md) | §3完整机制、§4主表/消融Table1–5，附录B Tables7–8及C敏感性；全文所有图曲线未逐图验收 |
| C05 | [UniCache: Task- and Type-Aware KV Cache Compression for Unified Multimodal Models](C05.md) | §3策略与公式、§4主表/消融Table1/3/4、实现和AppB/E；代码kernel未运行，未验收全部附表 |
| C06 | [Reconstruction Alignment Improves Unified Multimodal Models（RecA）](C06.md) | §2对齐loss与冻结、§3–4主表相关行及消融、AppB Table8超参、AppC失败与数据重叠；全部种子/表图尚未逐项核完 |
| C07 | [Learning Native Reflection in Unified Models with Interleaved Reinforcement Learning（UMM-Reflection）](C07.md) | §3–7方法、Table1–3主比较/消融/内部probe说明，AppA Table4全参组/超参；其他附录详细probe/图像案例未全部验收 |
| L139 | [Does Gradient Conflict Predict the Understanding--Generation Trade-off? A Controlled Audit of Conflict-Metric Validity in Unified Multimodal Models](L139.md) | §3–6全文、Tables1–3、AppendicesB/C/D及E部分结果；原CAGrad正式PDF§3/Algorithm1对照；未运行作者实现或核全图 |
| L140 | [Beyond Layers: Position-Resolved Gradient Conflict and Position-Aware Modulation for Unified Multimodal Models](L140.md) | §3–9方法/主表/消融/限制、AppendicesB–E；公式及LoRA预算独立符号核对，未取得附加实现/图像逐项验证 |
| L067 | [Beyond Accuracy: Benchmarking Cross-Task Consistency in Unified Multimodal Models](L067.md) | §3完整构造/匹配/公式、§4 Tables2–8主结果/人评/规模替换、§5–6限制；附录细类全部表和代码未核 |
| L068 | [IMUG-Bench: Benchmarking Unified Multimodal Models on Interleaved Understanding and Generation](L068.md) | §3完整构造/评分/TTS，§4主表2–4/设置/退化/消融，Conclusion；humanjudge附录及所有任务提示未完整核 |
| L069 | [Unison: Benchmarking Unified Multimodal Models via Synergistic Understanding and Generation](L069.md) | §3–5任务/构造/指标/实验，Table2judge及Table3相关行、§6–9insights/limits；源码/训练配置及所有子项未逐一核 |
| L070 | [When Does Visual Generation Help Visual Understanding in Unified Multimodal Models?](L070.md) | §3完整任务/协议、§4.2–4.4结果与Tables2–4、§6限制、AppA.3–A.4实现；完整大表所有行、图像和代码未全核 |
| R01 | [Hanzi Writer（工具，不是论文）](R01.md) | 官方docs Animation/Quiz/Loading character data/Raw Character SVG/配置项；LICENSE来源另列；未核quiz匹配实现或运行浏览器 |
| R02 | [Make Me a Hanzi（数据/工程资源）](R02.md) | 官方README数据格式/来源/笔顺/坐标/下载说明与COPYING全文；没有下载全库或执行解析 |
| R03 | [CASIA-HWDB / CASIA-OLHWDB（数据）](R03.md) | 官方home采集/作者划分，Online Database全部POT/WPTT格式和统计表，Conditions of Academic Use；未下载样本或重读ICDAR2011全篇 |
| R05 | [Mobao（Moyun配套静态书法数据）](R05.md) | Moyun v2 §4.1收集/分割细节与Introduction规模对照；B04已有模型笔记，本卡不重复统计为独立论文 |
| F05 | [Online Cursive Handwriting Generation Using Trace Transformation and Symbol-Independent Point Classification Model](F05.md) | 作者官方技术报告§1–4与references完整文字，未完整读取三个图片表及IEEE正文 |
| L007 | [B-BSMG，2024](L007.md) | 出版社全文§1–5、公式与实验正文、baseline和限制；表格标题及正文汇总已核，所有表格独立单元/算法图未全部核；另读官方Table1回归系数与Table4全部单元 |
| L008 | [Three-Dimensional Trajectory Planning for Robotic Chinese Calligraphy，2026](L008.md) | 出版社§3完整方法/Eqs1–10、§4.1–4.9实验/消融、§5限制与数据可用性；未核全部图与单元格，Zenodo制品未下载；另读官方Tables1/4全部单元 |
| L023 | [DiffBrush，ICCV 2025](L023.md) | §3–5完整方法/主表/消融，AppB训练与结构、C指标、D人评、E中文协议、G/H拼接文字；全部附图与源码未核 |
| L029 | [Think in Strokes, Not Pixels，2026](L029.md) | §3完整数据与CE/RF流程，§4全部设置、Tables1–7相关行与消融/结论；未逐图/源码复现，发表录用未独立确认 |
| L030 | [Where a New Concept Must Enter，2026](L030.md) | §3–4协议与substrate相关结果、§5.1 SAR/位置汇总Table3、§6.1架构、§7完整Table6/代价及§8–9限制、AppJ；未完整读取§5.2所有sweep/代码命令 |
| L031 | [Do Unified Multimodal Models Think in One Space?，2026](L031.md) | §3–6完整流程/主表/逆向/PSP讨论，AppB.1人评表3、B.3逆向、C.6–7层/强度/位置消融及F限制；未逐图核及读取全部原始配置 |
| R04 | [IAM-OnDB（数据）](R04.md) | 官方主页面Overview/Characteristics/Terms索引正文，旧官网Data format字段完整索引；未读基础论文全文/实际下载样本 |
| L024 | [Learning to Compose Stylistic Calligraphy Artwork with Emotions，ACM MM 2021](L024.md) | 原PDF9页，§3完整流程/公式、§4数据、§5主表2/消融与Table3layout及§6；未逐一视觉核验所有图或复现代码 |
| A06 | [Font Generation and Keypoint Ranking for Stroke Order of Chinese Characters by Deep Neural Networks](A06.md) | 出版社Abstract/正式书目信息；PDF转回订阅预览，未取得Method/Experiments全文 |
| L002 | [Diff-Writer，ICONIP 2023](L002.md) | Springer正式Abstract及书目/版权/引用页、作者publicationlist；Method/实验付费正文未取得 |
| L006 | [Frequency-guided cross-modal diffusion for online Chinese handwriting enhancement，2026](L006.md) | ScienceDirect官方摘要和索引可读任务/模块/数据段落；正文/完整表格/代码未取得 |
| L021 | [Write More at Once，公开投稿版本](L021.md) | 匿名公开PDF索引Title/Abstract/Introduction；官方forum受challenge，未读Method/Experiments |
| L022 | [Stylized Handwriting Generation of Arbitrary Structures and OOV Expressions，公开投稿版本](L022.md) | 官方公开PDF索引标题、摘要、Introduction任务定义；Method/Experiments与正式决定未取得 |
| L034 | [Tora，CVPR 2025](L034.md) | §3–5、Tables1–4，App§7–9相关数据/人评及§11/Table8；框架文字流程已读，未视觉逐图/代码/全部引用数据核查 |
| L035 | [Tora2，2025](L035.md) | §3全部公式/数据、§4与Tables1–5及结论；未逐图或源码复现，发表元数据另核 |
| L039 | [MotionCtrl，2023/2024](L039.md) | §3、§4.1–4.4/Tables1–3、§5–6；附录目录/部分定量未逐项深读，框架为文字核对，代码未跑 |
| L040 | [DragNUWA，2023](L040.md) | §3全部流程/公式、§4与Table1、Figures4–6文字说明及§5；未视觉核全部图，也未核后续官方SVD实现 |
| L041 | [DragAnything，2024](L041.md) | §3–5、Tables1–3、Figure10文字限制；未逐图/源码/附录全条件复核 |
| L025 | [AnyText，2023/2024](L025.md) | §3全部模块/公式、§4–6与Tables2–3；AppA.3数据过滤文字及A.2部分参数；v1.1完整新训练细节AppA.7尚未补读，未逐图/源码 |
| L036 | [MotiMotion，ICML 2026](L036.md) | §1/3–5全部流程、Tables1–5，AppA.1–A.2/B.3/C；未完整逐图/其他附录例/源码，未独立核ICML论文集 |
| L037 | [Fluid-Gen-Zero，2026](L037.md) | §3全部方程、§4/Tables1–2/§5；App§4–5、§6.1–6.3/Tables6–8、§7人评；复杂度各子公式/全部图/代码未读 |
| L038 | [RefTok，2025](L038.md) | §3全部流程、§4–5/Tables1–3；已读框架文字与限制，HTML未见所称超参附录，未逐图/代码 |
| L027 | [UniVid，2025](L027.md) | §3完整架构/公式/Algorithm1、§4–5主表相关行；AppA.2/A.5与A.6 Tables3–4/A.7；未逐图或代码/实际split/全VBench主表逐格核查 |
| L020 | [Learning to Generate Stylized Handwritten Text via a Unified Representation of Style, Content, and Noise (InkSpire)](L020.md) | 正式PDF正文§1/3/4、Tables1–7；AppA.2–A.3/A.5.3–A.5.7及Tables10–11；Figure3第5页已渲染视觉核对。未逐图、人评Figure8百分比未读取、源码未核 |
| L042 | [TextVBench，2026](L042.md) | §4–7协议、匹配/分数/采样、Tables1–2、§8–9局限结论；§3挑战与代码/原始工件未逐项核 |
| L043 | [ViTeX-Bench，2026](L043.md) | 正文§3–7/方程及Tables1–2相关指标；AppA/B/G/H/I/L/M及Table7，部分F基线适配；未逐图/源码/附录O全部身份probe，mask相关Kendall冲突待核 |
| L045 | [CalliReader / CalliBench，ICCV 2025](L045.md) | 正文§1/3–7、Tables2–8；正式CVF元信息，官方supp B/C/D.1–D.2/F.1与TablesS1–S4；未完整D.3/逐图/评审prompt/源码 |
| L051 | [Word-As-Image，2023](L051.md) | 正文§1/3–6、全部核心损失/权重、Table1；AppA/B/C及Figure18中文说明；没有逐图视觉复查全部SVG，代码未核 |
| F01 | [Differentiable Vector Graphics Rasterization for Editing and Learning（diffvg）](F01.md) | 正式15页PDF§1/3/§4开头/§5.1推导/§6.1/§6生成与Table1–2/§7/AppC；官网Errata完整；§5.2全部解析推导/全应用逐图未完成 |
| L053 | [Timage: A Generative Text-in-Image Paradigm for Fine-Tuning Vision-Language Models；公开预印本版本](L053.md) | §1/3全方法公式与训练/§4.1–4.5 Tables1–3/§5 Table4效率与局限/§6；未读到supp/代码/训练数据，原文矛盾保留 |
| L054 | [BoxTuning: Directly Injecting the Object Box for Multimodal Model Fine-Tuning；公开预印本版本](L054.md) | §1–5完整方法/训练、Tables1–7和所有主要对照；未核代码/数据清单/训练步数/独立Limitations（正文未见） |
| L052 | [Strike a Chord! Modal Kinetic Typography，2026](L052.md) | 18页正式arXivPDF正文§1–6/全部核心方程/Tables1–2；AppA.4–A.5/A.7–A.11/部分A.12；未逐图/全部FEM附推导/源码（项目页soon） |
| L182 | [STRIVE: Scene Text Replacement In Videos](L182.md) | CVF正式全文§1/3–5、全部主实验Tables1–2、BPN方程/训练/模拟与结论假设；未读视频/代码/补充，公式符号与OCR定义保留待核 |
| L183 | [CONSTANT: Towards High-Quality One-Shot Handwriting Generation with Patch Contrastive Enhancement and Style-Aware Quantization](L183.md) | CVF正式10页正文§1/3–5、Tables1–6和方程；官方README/DATASET/TRAINING_SAMPLING、IAM/CASIA配置、CASIAconverter、SAQ前向和完整PCE模块。代码tree快照cf31559c036b6f8d5ec64b20bff59809a66c8bfe；未读完整diffusion/pipeline/patchNCE实现/论文所称附录，未下载模型数据或复现。 |
| C02 | [Show-o2: Improved Native Unified Multimodal Models](C02.md) | §1/3–4完整结构与训练、Tables3–10、§5；未逐图核查、完整附录/代码/高分辨率checkpoint未审 |
| L061 | [UniTok: A Unified Tokenizer for Visual Generation and Understanding](L061.md) | §1/3–4方法/数据、Tables1/4–9及§5；表2完整生成行、表3VQA逐行/AppendixA图/源码与正式会议版本未全部复核 |
| L094 | [TokenFlow: Unified Image Tokenizer for Multimodal Understanding and Generation](L094.md) | §1/3–4主要方法、Table4–6、AppA/A.2/Table11、B.1/B.2/B.3/Table8解释与C；Table9逐行/全部图、优化配置和正式PDF差异未全读 |
| L032 | [UReason，2026](L032.md) | §1–5核心方法、Table2/3、AppC/E、I及K/L；主表BAGEL和全部趋势、指定人评协议；未完整所有子类/主表其余逐行/attention图/源码 |
| L033 | [Recursive Self-Improvement in Unified Multimodal Models，2026](L033.md) | §1–4完整主要机制/结果/失败、Tables1–3、AppA–D(含盲审)、Table5/6说明；决策Table4逐项/全量F分布表/可执行验证源码未全核 |
| E03 | [Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation](E03.md) | §I/III-A–D/IV-A–D/TablesI–X及V；未完整附录与全部训练代码；Eq2已结合正式PDF和官方采样代码核对；正式RSS PDF第3页视觉核Eq2负号，正文版本存在补充对照差异；上述commit的teacher/edm_policy.py采样循环、diffusion.py噪声映射与Euler/Heun、configs/ctmp_square.yaml相关结构/优化/训练字段只读 |
| E05 | [F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching](E05.md) | §1–5核心公式/结构/数据/主表1关键行与§5.1/5.2消融解释、Conclusion/Limitations；未完整表2全部数值、附录B/C和源码/正式ACL逐页差异 |
| N10 | [Video Text Preservation with Synthetic Text-Rich Videos](N10.md) | 全文Abstract/§1–5(方法/评价/结论完整)；参考文献未逐项追溯，图中视频未独立播放，未定位到训练实现 |
| N14 | [SteerVTE: Seamless Video Text Editing with Style and Glyph Control](N14.md) | §1/3全部方法与数据、§4 Tables1/3/4主表和消融、§5局限；§7.2/8.1/8.2完整协议；Table2仅关键行/解释，未逐图/代码/数据文件复核 |
| L055 | [Online Reasoning Video Object Segmentation；公开预印本版本](L055.md) | §3–6完整任务/方法/数据/主表1–3和消融；§1–2关键背景；所有示例图/来源视频与代码未逐一核，未复现 |
| L056 | [CoT-RVS / ThinkVideo](L056.md) | §3–4任务/流程/参数、主表1–6关键结果与消融；AppC/D/F/G/H/I/J及A4/A5；提示全文A/B、Fig8数值不可读部分与各模块代码尚未逐行核 |
| N11 | [CalliffusionV2: Personalized Natural Calligraphy Generation with Flexible Multi-modal Control](N11.md) | §3–5全部核心方法、数据、Tables1–3、fewshot/编辑/非汉字说明；全部图样与公开训练实现未逐项核，正式发表未确认 |
| N12 | [CalliPaint: Chinese Calligraphy Inpainting with Diffusion Model](N12.md) | 全文§1–4与AppendixA/B文字和Tables1/2完整；框架图具体层次、所有图选项及原Calliffusion训练实现未核 |
| L180 | [Painter: Teaching Auto-Regressive Language Models to Draw Sketches](L180.md) | §2–3完整数据/模型/loss/训练及Table3和discussion，Table1/2协议；§4相关工作，正式CVF元数据核查；全部图/实现未逐项检查 |
| L181 | [Joint optimization for attention-based generation and recognition of Chinese characters using tree position embedding](L181.md) | 正式作者PDF§3/4(含证明)/5/6/7、Tables1–3/5/7/8关键行、p6公式渲染目视核查；编码实现/全部案例图与训练未复现；官方embed.py TPE全函数、joint.py前向/IF_SIM/dual、optimizer.py和joint_config.yaml只读核对 |
| R06 | [通用规范汉字笔顺规范](R06.md) | 官方PDF前12页；§1–5全文及§6开头示例；8105逐项、全部索引与后部表未完成逐字核查 |
| S008 | [Wuji Writing VAM TI2V-5B 30L 0522 0819](S008.md) | 固定HF revision的README、model_config.json、training_config.yaml；未下载11.54GB权重，动作统计与日志仅卡片引用，未执行模型 |
| S011 | [Qari-OCR-LoRA](S011.md) | 官方GitHub README、HF固定revision README/adapter_config.json/training_info.json与推理示例全部相关内容；未下载adapter或运行OCR |
| S012 | [CASIA-HWDB2-line (Teklia HF derivative)](S012.md) | HF固定revision README全部字段、规模/示例/许可；未下载全parquet或逐条图像核验 |
| S009 | [AnimCJK](S009.md) | 官方README目录/使用/完整“中”SVG示例与许可；长历史changelog、全部字库和生成脚本未逐项读 |
| S010 | [KanjiVG](S010.md) | 官方README全文；SVG规范关于group/path/顺序/属性与已知不一致部分；04e2d.svg全文；未逐字库核查 |
| S013 | [SceneDAPR](S013.md) | 官方README核心数据/标注/训练/许可和完整src/preprocessing.py；blob bf765c696bcd1aa95cdf8879a366b01a7f377da3；未读WWW全文及受限数据 |
| S014 | [sketch-diffusion (ark60 independent implementation)](S014.md) | notebook关键数据处理/attention/model/diffusion/trainer/config/evaluation及保存输出；未执行notebook、未下载数据权重；保存输出的运行环境和文件对应仍待核 |
| S015 | [VidSketch sketch animation implementation](S015.md) | 官方README核心/许可；candles.yaml全文、train_vidsketch.py初始化/参数选择/优化器/主损失、inference.py adapter加载段；未全读所有模块或执行；blob config cd2b32c8df4a8564a156727b86f561dc81d3c95c/train 9d459e78da5e058be84b656ddd881b12ab7f5ecc |
| S007 | [Brush Calligraphy Stroke Segmentation Dataset (BCSS)](S007.md) | 固定HF README完整数据/加载段、两个info.csv头部样例和范围，正式论文§3–5对照；未下载全mask或逐图审查 |
| S016 | [BCSS Stroke-Seg implementation](S016.md) | 官方README全部、recursive tree、FCN.py与deeplab.py全文、LabelMe01字段；未执行、未读全部子模块，未取得主表checkpoint |
| L184 | [Stroke-Seg: A deep learning-based framework for chinese stroke segmentation](L184.md) | 正式PDF pp4343–4354的相关工作、Figure2说明、§3–6、Tables1–4；主表文字与公式已读，PDF框架/表图未完成可视逐项验收；官方代码选定入口另见S016 |
| N07 | [A stroke-level large-scale database of Chinese character handwriting and the OpenHandWrite_Toolbox for handwriting research](N07.md) | 正式Springer正文PresentStudy、ToolboxDevelopment、采集/编码/排除/结果/部分Discussion；OSF摘要工作簿字段及R指标代码见R07；Tables3–7逐系数、全部附录和原始数据未完整复核 |
| R07 | [OpenHandWrite_Toolbox与笔画级数据](R07.md) | OSF node/files API及Data/R子目录、batch_summarise_all.R全文、batch_funcs.R定义及长度/首末点/相邻延迟函数、小xlsx全部表头和各2行样例；未运行R/全读脚本和下载完整采集包 |
| L058 | [Unified-IO 2: Scaling Autoregressive Multimodal Models with Vision, Language, Audio, and Action](L058.md) | §3.1–3.5、§4数据、Tables2/4、GRIT/缩放段、§5.5及AppB4相关条件；未逐项阅读全部220任务、全部附表/图，未复现 |
| L059 | [AnyGPT: Unified Multimodal LLM with Discrete Sequence Modeling](L059.md) | §3全部表示/架构、§4合成数据、§5 Tables2–6、AppA/C训练与解码条件；未逐图核验多轮示例、未运行代码 |
| L060 | [SEED-X: Multimodal Models with Unified Multi-granularity Comprehension and Generation](L060.md) | §3表示/位置/预训/指令、理解/GenEval主表、§4定性组件比较、AppendixB配置；未完整核验所有附录数据/图和代码，未复现 |
| L063 | [MMaDA: Multimodal Large Diffusion Language Models](L063.md) | §2–3完整核心目标/UniGRPO/采样、§4训练和Table3、§5 Tables5/6/协同讨论、§9；官方tree3cdb8709635beb29f66e4e23cd66060872ac3996的generate.py及modeling_mmada.py对应sampling段、stage4头/检索。未通读所有理解表/全仓库RL、未复现 |
| L064 | [MANZANO: A Simple and Scalable Unified Multimodal Model with a Hybrid Vision Tokenizer](L064.md) | §3–4表示/训练、§5.1/5.2 Table1和联合对照/Fig5、§5.4–5.5讨论、结论；未逐行精读全部主表/图、未复现 |
| L065 | [Qwen3-Omni Technical Report](L065.md) | §1–3/主要模块与数据训练、Tables1/2、§6 Table16全表及结论；未逐项读取全部ASR/TTS/VLM表，未复现 |
| L066 | [Emu3.5: Native Multimodal Models are World Learners](L066.md) | §1–4架构/数据/训练/奖励/DiDA、§5部分tokenizer、§6 Tables7–9/16及§6.3–6.8解释、§7局限；未逐行核全部编辑/重建主表、未视觉核对全图、未运行模型 |
| L073 | [OFA: Unifying Architectures, Tasks, and Modalities Through a Simple Sequence-to-Sequence Learning Framework](L073.md) | Introduction、§3全部、Table1/5/10/13、§4.4、AppA.1–A.3和B；其他主表未全部逐行，未逐图、未复现；另核正式PMLR PDF第3页Fig2、第9页Table9(对应HTML Table10)、第15页数据表，确认表号版本变化；未把正式Table10误作消融 |
| L074 | [Unified-IO: A Unified Model for Vision, Language, and Multi-Modal Tasks](L074.md) | §3.1–3.4全部、§4 GRIT解释、Table5全表/预算、§4.4–4.6及Table7；未逐行所有任务数据/主表、未视觉验收与复现 |
| L075 | [Versatile Diffusion: Text, Images and Variations All in One Diffusion Model](L075.md) | §3全部、§4.1–4.5/表1/Fig6文字数值、AppC清洗/训练、AppE局限；部分图未视觉读、采样细节未全核、未复现 |
| L076 | [One Transformer Fits All Distributions in Multi-Modal Diffusion at Scale](L076.md) | §3–4完整公式/表示、§6训练/表1/应用、AppD/E与H配置/效率；未逐图/全部采样伪代码验收、未复现 |
| L077 | [Emu: Generative Pretraining in Multimodality](L077.md) | §2–4完整流程/数据、§5主表2/解释/局限、AppA训练/消融表5–7、AppB1；部分图与主表1/3/4未逐行、未复现 |
| L078 | [Planting a SEED of Vision in Large Language Model](L078.md) | §1–3方法与全部Tables1–3、§4–5结论；未核全部图/代码与未披露训练参数，未复现 |
| L062 | [Transfer between Modalities with MetaQueries](L062.md) | Introduction、§3设计/表1–3、§4训练数据、§5.1–5.6解释/表8–9、AppA/C及Table10；未逐行全部主表/全图/代码，未复现 |
| L079 | [Unified Language-Vision Pretraining in LLM with Dynamic Discrete Visual Tokenization](L079.md) | §1、§3.1–3.3、§4.1–4.3、Table2/3、AppA、AppB Tables4–8、AppC Table9及AppE；未逐图、未核全部评价表/代码、未复现 |
| L080 | [NExT-GPT: Any-to-Any Multimodal LLM](L080.md) | §3–6核心方法、Table4/5及人评说明、AppA、AppC三阶段和Table7、AppD开头及零样本生成表；未逐一核全部QA结果、视频采样条件或代码，未复现 |
| L081 | [DreamLLM: Synergistic Multimodal Comprehension and Creation](L081.md) | §2背景/2.1动机、§3方法/三阶段、§4.2主T2I表尾与协议、§5.1 Table3、AppA Table9、AppC Table11及AppE失败；未逐图/全部主表、未复现 |
| L082 | [Making LLaMA SEE and Draw with SEED Tokenizer](L082.md) | §3/4方法、Tables1/2/4、§4.2主结果解释/4.3全部消融、AppA/B、AppC指定数据行、AppD评测与部分模板；未逐行Table3、未逐图/代码、未复现 |
| L083 | [Generative Multimodal Models are In-Context Learners](L083.md) | §2.1–2.3、§3.1–3.3、Tables3–5、AppA/B含Tables6/7、AppD含Table9、AppE示例选择/Chat协议；未逐行Tables1/2及全部图、未核代码，未复现 |
| L084 | [MM-Interleaved: Interleaved Image-Text Generative Modeling via Multi-modal Feature Synchronizer](L084.md) | §1/3全部、§4.1–4.3、Tables2/3/6–8、AppA Table9与数据、AppB Tables16/17；PDF第6页Fig4和第13页Tables6/7已渲染视觉核对。未逐行全部主表/下游SFT配置、未复现 |
| L085 | [VILA-U: a Unified Foundation Model Integrating Visual Understanding and Generation](L085.md) | §1/3–6相关方法与Tables1/4/6–9、部分GenAIbench表尾、AppA解释与AppC失败配方；官方README、pretrain.sh/sft.sh、datasets_mixture.py、inference.py已读；未逐行Tables2/3/5、未读全部底层generation实现、未复现 |
| G001 | [Denoising Diffusion Probabilistic Models](G001.md) | §2–4，Algorithms 1–2，Eq.14，Tables 1–2 |
| G002 | [Score-Based Generative Modeling through Stochastic Differential Equations](G002.md) | 摘要，SDE/ODE方法，§4采样，Table 1 |
| G003 | [High-Resolution Image Synthesis with Latent Diffusion Models](G003.md) | §3–4，压缩因子实验，Figs.6–7 |
| G004 | [Scalable Diffusion Models with Transformers](G004.md) | 模型结构、条件模块和扩展实验；主结果及结构消融 |
| G005 | [Flow Matching for Generative Modeling](G005.md) | §3，条件向量场推导，Eqs.20–23，实验Table 1 |
| G006 | [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](G006.md) | 直线回归与reflow方法，理论性质，CIFAR-10实验 |
| G007 | [Consistency Models](G007.md) | 一致性函数、CD/CT算法，Fig.3及主实验 |
| G008 | [DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps](G008.md) | 扩散ODE推导、高阶算法、主比较实验 |
| G009 | [Video Diffusion Models](G009.md) | 时空网络和联合训练方法，BAIR/Kinetics评估设置 |
| G010 | [Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models](G010.md) | 摘要、架构与数据部分、主实验设置；消融数表待补 |
| G011 | [AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning](G011.md) | 模块设计、Table 1及域/运动适配消融 |
| G012 | [CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](G012.md) | 3D VAE、Transformer结构、训练组织及Fig.8相关实验 |
| G013 | [Wan: Open and Advanced Large-Scale Video Generative Models](G013.md) | §4.5提示对齐，§4.7及Table 2，VAE/DiT总体结构 |
| G014 | [A Neural Representation of Sketch Drawings](G014.md) | 原始PDF§3表示/训练、§4实验设置、Table1与Fig8；完整附录未全部读完 |
| G015 | [Learning to Paint With Model-based Deep Reinforcement Learning](G015.md) | 方法、训练设置、Fig.8及速度比较 |
| G016 | [Paint Transformer: Feed Forward Neural Painting with Stroke Prediction](G016.md) | 框架、训练/评估条件、Tables 1–2 |
| G017 | [CLIPasso: Semantically-Aware Object Sketching](G017.md) | §3方法，§4.3/Tables2–3，Appendix A/D/E；其余实验尚有未逐项摘录字段 |
| G018 | [LoRA: Low-Rank Adaptation of Large Language Models](G018.md) | 低秩更新定义、初始化、秩及模块消融 |
| G019 | [QLoRA: Efficient Finetuning of Quantized LLMs](G019.md) | 方法三组成、适配模块研究、评测协议与限制 |
| G020 | [DoRA: Weight-Decomposed Low-Rank Adaptation](G020.md) | 分解方法、常识推理表、rank与参数量对照 |
| G021 | [A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA](G021.md) | §3稳定性定义及Theorem3.2，Figs.2–3与实验设置 |
| G022 | [Diffusion Models in Vision: A Survey](G022.md) | 摘要，三框架分类及生成范式关系；参考文献逐项阅读未完成 |
| G023 | [Efficient Diffusion Models: A Comprehensive Survey from Principles to Practices](G023.md) | 摘要，§3 VAE，§5.1采样，效率对照表及Limitations |
| G024 | [StrokeFusion: Vector Sketch Generation via Joint Stroke-UDF Encoding and Latent Sequence Diffusion](G024.md) | 方法、数据/指标、Tables1–3，Fig.6和Limitations；正式会议元数据 |
| G025 | [Adding Conditional Control to Text-to-Image Diffusion Models](G025.md) | §3训练与结构，§4.2，ADE20K Table2及提示消融 |
| G026 | [Classifier-Free Diffusion Guidance](G026.md) | §4.1–4.3及Tables1–2，训练条件dropout定义 |
| G027 | [Elucidating the Design Space of Diffusion-Based Generative Models](G027.md) | 正式NeurIPS主PDF§1–6/Algorithms1–2/Table1–2/Fig2–5文字解释，原公式已推核；未视觉核全部图，附录B–F在独立supp未读，训练源码未全核 |
| G028 | [Generative Adversarial Nets](G028.md) | minimax目标与理论假设，§5/Table1，指标限制 |
| G029 | [Auto-Encoding Variational Bayes](G029.md) | ELBO/重参数化推导，§5实验设置与学习算法比较 |
| G030 | [Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion](G030.md) | 逐token噪声方法，§4.1同架构视频比较，规划任务区分 |
| G031 | [VBench: Comprehensive Benchmark Suite for Video Generative Models](G031.md) | §3.1–3.3，Table1，§4，人工配对协议 |
| G032 | [Towards Accurate Generative Models of Video: A New Metric & Challenges](G032.md) | 度量与特征设计，§4.1噪声，§4.3/Table1及人工协议 |
