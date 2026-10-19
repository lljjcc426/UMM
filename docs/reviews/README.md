# 第二轮原文阅读与批判分析

以下笔记按实际阅读范围记录。相关章节核查不等于三遍完整精读；没有进行模型复现。未填完的实验条件与消融明确保留，不能计作全部完成。

[逐条完成台账](../evidence/reading_ledger_2026-10-19.md) · [理论与实验迁移](../evidence/foundations_and_transfer_2026-10-19.md)

| 编号 | 论文 | 核查范围 |
| --- | --- | --- |
| A01 | [DP-Font: Chinese Calligraphy Font Generation Using Diffusion Model and Physical Information Neural Network](A01.md) | 正式PDF Abstract/Introduction、§3.1–3.3 Eq1–11、§4.1–4.4 Tables1–3与Conclusion，Fig2/3 PDFp4及此前p7表视觉核。未取得完整训练代码/权重，核心三遍与五项书面理解检查完成，报告缺项保留。 |
| A02 | [Decoupling Layout from Glyph in Online Chinese Handwriting Generation（OLHWG）](A02.md) | 论文Abstract/§3.1–3.4 Eq1–6/Algorithms1–2、§4.1–4.3 Tables1–3、§5、AppA.2.1–4；Fig3 PDFp5视觉核。固定e1bed55 README、style_classifier.py45–93、train_ddpm指定训练段、unet_ddpm默认与layout配置已读。其余完整代码/权重未运行，核心三遍完成。 |
| A03 | [DiffInk: Glyph- and Style-Aware Latent Diffusion Transformer for Text to Online Handwriting Generation](A03.md) | v3 Abstract/Introduction/§3完整核心方法/§4 Tables1–3；AppA/B1–4/C4/D2–6；正式proceedingsPDF相同核心公式、Tables1–4及配置段复核。Fig3 v3PDFp4视觉核；固定97bc6a README、dataset初始化/掩码、trainer训练与5/20步可视化、diffusion.noise_images、VAE指定路径与配置/启动脚本。未运行模型/全部benchmark，核心三遍完成。 |
| A04 | [Stroke Modeling Enables Vectorized Character Generation with Large Vectorized Glyph Model（LVGM）](A04.md) | v1主文§3–6 Eq1–8与Tables1–3；WACV正式§3/4/5、Tables2/3及Supplement§1–3/Table1–4训练与几何公式复核；Fig4正式PDFp4/v1p5、v1p5两表视觉核。补充剩余示例图未逐图审，无模型运行，核心三遍完成。 |
| A05 | [Handwriting Trajectory Recovery with Diffusion Models](A05.md) | v1 Abstract/Introduction、§3.1–3.3 Eq1–7、§4.1–4.7 Tables1–4与§5全部核心文字；Fig3PDFp7视觉核。其他案例图只读对应分析，未独立跑基线/模型；核心三遍与五项检查完成。 |
| A06 | [Font Generation and Keypoint Ranking for Stroke Order of Chinese Characters by Deep Neural Networks](A06.md) | 出版社Abstract/正式书目信息；PDF转回订阅预览，未取得Method/Experiments全文 |
| A07 | [Complex Handwriting Trajectory Recovery: Evaluation Metrics and Algorithm（PEN-Net）](A07.md) | arXiv Abstract/§3–6主文；ACCV正式§3.1/3.2/4.3及Tables1/2配置/结论复核，supp全文三页扰动/数据统计。Fig5/6 arXivPDFp9、正式p10软min与p13消融勾选视觉核。固定03bc591 README/tree、train.py指定训练段、配置及model.py1–185核心结构/前向/解码；公开默认解码另有取整与可选骨架吸附，未取得主表实际评估调用，未运行，核心三遍完成。 |
| A08 | [Modality Conversion of Handwritten Patterns by Cross Variational Autoencoders（Cross-VAE）](A08.md) | arXivv1六页Abstract/Introduction/RelatedWork/§III–V含Eq1–9/TableI完整核心文字与Fig2PDFp3视觉核；主办ICDAR程序与作者PDF入口核。未逐图读所有示例、无训练源码/模型执行，核心三遍完成；缺失实验字段明确记未报告。 |
| A09 | [Disentangling Writer and Character Styles for Handwriting Generation（SDT）](A09.md) | Abstract、§4.1设置；完整消融与训练附录待补 |
| A10 | [Diffusion Models for Handwriting Generation](A10.md) | Abstract、§5.1、Table1及采样消融 |
| A11 | [Stroke Extraction of Chinese Character Based on Deep Structure Deformable Image Registration](A11.md) | 摘要、方法三模块、实验数据/训练、Tables2–5及Limitations；代码未运行 |
| B01 | [Calliffusion: Chinese Calligraphy Generation and Style Transfer with Diffusion Modeling](B01.md) | 方法/训练、Tables1–2及Limitation全文段落；图仅核图注，LoRA配置及原会议论文集待核 |
| B02 | [Moyun: A Diffusion-Based Model for Style-Specific Chinese Calligraphy Generation](B02.md) | Abstract、§4.1、Table1/2和用户研究说明；训练/消融未完成 |
| B03 | [InkDiffuser: High-Fidelity One-shot Chinese Calligraphy via Differentiable Morphological Optimization](B03.md) | HTML§IV公式及§V TablesI–III、结论；GitHub固定树/train.py/configs/fontdiffuser.py/dis_loss.py；PDF公式视觉核对与实际训练版本尚未完成 |
| B04 | [AnyText2: Visual Text Generation and Editing With Customizable Attributes](B04.md) | 方法框架、训练/推理配置与对比来源说明；数表待补 |
| B05 | [Kinetic Typography Diffusion Model（KineTy）](B05.md) | 数据/架构、训练设置与基线；主数表待补 |
| B06 | [Dynamic Typography: Bringing Text to Life via Video Diffusion Prior](B06.md) | 方法、数据和实现/公平比较设置；消融数表待补 |
| B07 | [Inverse Painting: Reconstructing the Painting Process](B07.md) | §1、3、4、Fig3/5；Appendix A.3、B.3/B.5/B.6 |
| B08 | [AnimatePainter（arXiv:2503.17029）](B08.md) | Abstract、§4.1/4.2、Table2；完整结构消融尚未抽全 |
| B09 | [DiffMath: Symbol- and Graph-Aware Latent Diffusion Transformer for Handwritten Mathematical Expression Generation](B09.md) | §3轨迹VAE/RelAST/DiT、Tables2–4、Appendix0.B训练和基线；更多OCR增强结果与代码未全部复核 |
| C01 | [Emerging Properties in Unified Multimodal Pretraining（BAGEL）](C01.md) | §2架构/注意力、§3数据Table1、§4训练Table3、§5–6消融与能力曲线、§7主表相关行；附录评判说明；完整硬件与所有表值未逐项核 |
| C02 | [Show-o2: Improved Native Unified Multimodal Models](C02.md) | §1/3–4完整结构与训练、Tables3–10、§5；未逐图核查、完整附录/代码/高分辨率checkpoint未审 |
| C03 | [Hyper-Bagel: A Unified Acceleration Framework for Multimodal Understanding and Generation](C03.md) | §2文字草稿与data，§3全部蒸馏阶段，§4主表/ablation相关行；配置细节和代码尚未完整复核 |
| C04 | [Flash-Unified: A Training-Free and Task-Aware Acceleration Framework for Native Unified Models（FlashU）](C04.md) | §3完整机制、§4主表/消融Table1–5，附录B Tables7–8及C敏感性；全文所有图曲线未逐图验收 |
| C05 | [UniCache: Task- and Type-Aware KV Cache Compression for Unified Multimodal Models](C05.md) | §3策略与公式、§4主表/消融Table1/3/4、实现和AppB/E；代码kernel未运行，未验收全部附表 |
| C06 | [Reconstruction Alignment Improves Unified Multimodal Models（RecA）](C06.md) | §2对齐loss与冻结、§3–4主表相关行及消融、AppB Table8超参、AppC失败与数据重叠；全部种子/表图尚未逐项核完 |
| C07 | [Learning Native Reflection in Unified Models with Interleaved Reinforcement Learning（UMM-Reflection）](C07.md) | §3–7方法、Table1–3主比较/消融/内部probe说明，AppA Table4全参组/超参；其他附录详细probe/图像案例未全部验收 |
| D01 | [HunyuanVideo 1.5 Technical Report](D01.md) | §2数据、§3架构、§4训练及Tables3/7/8；未逐项摘完所有训练规模和人评协议 |
| D02 | [LTX-2: Efficient Joint Audio-Visual Foundation Model](D02.md) | §3表示/双流、§4推理、§5数据、§6速度/评测与§7限制 |
| D03 | [VACE: All-in-One Video Creation and Editing](D03.md) | §3 VCU/adapter、§4数据及benchmark、§5对比/消融；完整大表逐数核对仍待完成 |
| D04 | [Wan-Move: Motion-controllable Video Generation via Latent Trajectory Guidance](D04.md) | §3 latentguidance/训练、§4benchmark、§5/Table4、§8.3训练与§9.4failure |
| D05 | [Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion](D05.md) | §3–5，Table1、受控消融说明，Appendix A训练细节 |
| D06 | [Self Gradient Forcing: Native Long Video Extrapolation](D06.md) | 摘要、方法两遍梯度路径、§4.1协议、§4.5/Table4及结论；长主表尚待逐项摘录 |
| D07 | [Salt: Self-Consistent Distribution Matching with Cache-Aware Training for Fast Video Generation](D07.md) | 摘要、§4.2–4.4/Tables1/2/4，AppendixB实现和动态分讨论；§3公式尚需完整推导 |
| D08 | [Wan-R1: Verifiable-Reinforcement Learning for Video Reasoning](D08.md) | 方法奖励/VideoGRPO、§4.1–4.4、主实验概述、AppendixTable4；Table2逐值与全消融待补 |
| E01 | [Mean Flows for One-step Generative Modeling](E01.md) | §4–5，Table1，实验配置及JVP消融 |
| E02 | [Improved Mean Flows: On the Challenges of Fastforward Generative Models](E02.md) | 摘要、§4.1/JVP/stopgrad、§5.1/Table1、§5.2/Table2、AppendixTable4；全部数学证明未完成 |
| E03 | [Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation](E03.md) | §I/III-A–D/IV-A–D/TablesI–X及V；未完整附录与全部训练代码；Eq2已结合正式PDF和官方采样代码核对；正式RSS PDF第3页视觉核Eq2负号，正文版本存在补充对照差异；上述commit的teacher/edm_policy.py采样循环、diffusion.py噪声映射与Euler/Heun、configs/ctmp_square.yaml相关结构/优化/训练字段只读 |
| E04 | [Discrete Flow Matching](E04.md) | 摘要、§2主要概率路径/采样概念、§3masked命题、§4实验设置与代码结果；AppendixD/G及全部证明未读完 |
| E05 | [F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching](E05.md) | §1–5核心公式/结构/数据/主表1关键行与§5.1/5.2消融解释、Conclusion/Limitations；未完整表2全部数值、附录B/C和源码/正式ACL逐页差异 |
| E06 | [Timestep Embedding Tells: It's Time to Cache for Video Diffusion Model（TeaCache）](E06.md) | 摘要、方法输入差/重标定、§4.1–4.3及限制讨论；多项式系数与代码未独立复核 |
| E07 | [clDice: A Novel Topology-Preserving Loss Function for Tubular Structure Segmentation](E07.md) | §2定义、§3定理/推论前提、§4softskeleton、§5数据/指标/Table1概述；完整证明与补充训练配置未全部复核 |
| F01 | [Differentiable Vector Graphics Rasterization for Editing and Learning（diffvg）](F01.md) | 正式15页PDF§1/3/§4开头/§5.1推导/§6.1/§6生成与Table1–2/§7/AppC；官网Errata完整；§5.2全部解析推导/全应用逐图未完成 |
| F02 | [Bézier Splatting for Fast and Differentiable Vector Graphics](F02.md) | 摘要、表示概述、§4.1–4.3和Tables1–3、限制与AppendixA/B；源码未运行 |
| F03 | [FRIDA: A Collaborative Robot Painter with a Differentiable, Real2Sim2Real Planning Environment](F03.md) | §III笔画/模拟器/规划、§IV设备、§V对比/重规划及§VI限制；官方作者页确认ICRA2023 |
| F04 | [CoFRIDA: Self-Supervised Fine-Tuning for Human-Robot Co-Painting](F04.md) | §III数据/高层微调、§IV评估、TableI、§V/限制；官方项目与HF原始README/文件清单交叉核查 |
| F05 | [Online Cursive Handwriting Generation Using Trace Transformation and Symbol-Independent Point Classification Model](F05.md) | 作者官方技术报告§1–4与references完整文字，未完整读取三个图片表及IEEE正文 |
| L001 | [Handwriting Trajectory Recovery via Autoregressive Ordered Stroke Instance Prediction，2026](L001.md) | 摘要、方法主要模块、§4.1/Table1、Tables2–4及跨语言设置；完整符号和附录仍待补核 |
| L002 | [Diff-Writer，ICONIP 2023](L002.md) | Springer正式Abstract及书目/版权/引用页、作者publicationlist；Method/实验付费正文未取得 |
| L004 | [Layout Stroke Imitation，2025](L004.md) | §3模块/公式、§4 Tables2–4及Discussion；补充材料超参、原PDF表视觉与代码待核 |
| L005 | [StrokeBank，2014](L005.md) | 作者6页PDF的方法、公式2–5、Tables1–2、数据及局限；图读取图注，正式书目和源码未核；已视觉核对PDF第3–4页部件图、DEF示意、式2–5与Table1，确认式5方向差异 |
| L006 | [Frequency-guided cross-modal diffusion for online Chinese handwriting enhancement，2026](L006.md) | ScienceDirect官方摘要和索引可读任务/模块/数据段落；正文/完整表格/代码未取得 |
| L007 | [B-BSMG，2024](L007.md) | 出版社全文§1–5、公式与实验正文、baseline和限制；表格标题及正文汇总已核，所有表格独立单元/算法图未全部核；另读官方Table1回归系数与Table4全部单元 |
| L008 | [Three-Dimensional Trajectory Planning for Robotic Chinese Calligraphy，2026](L008.md) | 出版社§3完整方法/Eqs1–10、§4.1–4.9实验/消融、§5限制与数据可用性；未核全部图与单元格，Zenodo制品未下载；另读官方Tables1/4全部单元 |
| L009 | [Video-Based Handwritten Chinese Character Recognition，2005](L009.md) | 作者8页PDF §II–V方法/纠错/实验及Conclusion；TableI细分数字与图像逐项视觉尚待核 |
| L010 | [VideoSketcher: Sequential Sketch Generation Using Video Model Priors](L010.md) | §3–7，Tables1–2，Figures2/3/7/10/12，Appendix B.3 |
| L012 | [SketchAgent，2024/2025](L012.md) | §4、§5.1–5.2、Table1/2、§6–7与官方CVPR书目信息；未完成全部交互附录 |
| L013 | [ProcessPainter，2024](L013.md) | Abstract、Table1、§4.4.2/4.5、Fig7；样本数与预算待核 |
| L014 | [Generating Past and Future in Digital Painting Processes / PaintsAlter，2025](L014.md) | 原始13页PDF§3主要框架、§3.4数据/训练、§4.2–4.7及Tables1–4；逐图视觉核对尚未全部完成 |
| L015 | [Loomis Painter，2025](L015.md) | §3–4、§5实现/Table2/3、§5.2.1PDP、§5.3消融、§7限制；附录未完整精读 |
| L016 | [StrokeNUWA，2024](L016.md) | §3.1–3.2、§4.1–4.3、§5及Tables2–4；官方PMLR书目核对 |
| L017 | [DiffSketcher，2023](L017.md) | Abstract、Appendix D/Table1、Appendix E；主方法核心目标 |
| L018 | [Diff-Font，2022 起](L018.md) | §3条件/CFG、§4.1–4.4 Tables1/2/4及跨语种表示；完整版本对齐、韩文实验与全部附录未完成 |
| L019 | [FontDiffuser，AAAI 2024](L019.md) | Method三模块/对比loss、数据/条件、Tables2–4；Table1大表全部数值及附录未逐项核完 |
| L020 | [Learning to Generate Stylized Handwritten Text via a Unified Representation of Style, Content, and Noise (InkSpire)](L020.md) | 正式PDF正文§1/3/4、Tables1–7；AppA.2–A.3/A.5.3–A.5.7及Tables10–11；Figure3第5页已渲染视觉核对。未逐图、人评Figure8百分比未读取、源码未核 |
| L021 | [Write More at Once，公开投稿版本](L021.md) | 匿名公开PDF索引Title/Abstract/Introduction；官方forum受challenge，未读Method/Experiments |
| L022 | [Stylized Handwriting Generation of Arbitrary Structures and OOV Expressions，公开投稿版本](L022.md) | 官方公开PDF索引标题、摘要、Introduction任务定义；Method/Experiments与正式决定未取得 |
| L023 | [DiffBrush，ICCV 2025](L023.md) | §3–5完整方法/主表/消融，AppB训练与结构、C指标、D人评、E中文协议、G/H拼接文字；全部附图与源码未核 |
| L024 | [Learning to Compose Stylistic Calligraphy Artwork with Emotions，ACM MM 2021](L024.md) | 原PDF9页，§3完整流程/公式、§4数据、§5主表2/消融与Table3layout及§6；未逐一视觉核验所有图或复现代码 |
| L025 | [AnyText，2023/2024](L025.md) | §3全部模块/公式、§4–6与Tables2–3；AppA.3数据过滤文字及A.2部分参数；v1.1完整新训练细节AppA.7尚未补读，未逐图/源码 |
| L027 | [UniVid，2025](L027.md) | §3完整架构/公式/Algorithm1、§4–5主表相关行；AppA.2/A.5与A.6 Tables3–4/A.7；未逐图或代码/实际split/全VBench主表逐格核查 |
| L029 | [Think in Strokes, Not Pixels，2026](L029.md) | §3完整数据与CE/RF流程，§4全部设置、Tables1–7相关行与消融/结论；未逐图/源码复现，发表录用未独立确认 |
| L030 | [Where a New Concept Must Enter，2026](L030.md) | §3–4协议与substrate相关结果、§5.1 SAR/位置汇总Table3、§6.1架构、§7完整Table6/代价及§8–9限制、AppJ；未完整读取§5.2所有sweep/代码命令 |
| L031 | [Do Unified Multimodal Models Think in One Space?，2026](L031.md) | §3–6完整流程/主表/逆向/PSP讨论，AppB.1人评表3、B.3逆向、C.6–7层/强度/位置消融及F限制；未逐图核及读取全部原始配置 |
| L032 | [UReason，2026](L032.md) | §1–5核心方法、Table2/3、AppC/E、I及K/L；主表BAGEL和全部趋势、指定人评协议；未完整所有子类/主表其余逐行/attention图/源码 |
| L033 | [Recursive Self-Improvement in Unified Multimodal Models，2026](L033.md) | §1–4完整主要机制/结果/失败、Tables1–3、AppA–D(含盲审)、Table5/6说明；决策Table4逐项/全量F分布表/可执行验证源码未全核 |
| L034 | [Tora，CVPR 2025](L034.md) | §3–5、Tables1–4，App§7–9相关数据/人评及§11/Table8；框架文字流程已读，未视觉逐图/代码/全部引用数据核查 |
| L035 | [Tora2，2025](L035.md) | §3全部公式/数据、§4与Tables1–5及结论；未逐图或源码复现，发表元数据另核 |
| L036 | [MotiMotion，ICML 2026](L036.md) | §1/3–5全部流程、Tables1–5，AppA.1–A.2/B.3/C；未完整逐图/其他附录例/源码，未独立核ICML论文集 |
| L037 | [Fluid-Gen-Zero，2026](L037.md) | §3全部方程、§4/Tables1–2/§5；App§4–5、§6.1–6.3/Tables6–8、§7人评；复杂度各子公式/全部图/代码未读 |
| L038 | [RefTok，2025](L038.md) | §3全部流程、§4–5/Tables1–3；已读框架文字与限制，HTML未见所称超参附录，未逐图/代码 |
| L039 | [MotionCtrl，2023/2024](L039.md) | §3、§4.1–4.4/Tables1–3、§5–6；附录目录/部分定量未逐项深读，框架为文字核对，代码未跑 |
| L040 | [DragNUWA，2023](L040.md) | §3全部流程/公式、§4与Table1、Figures4–6文字说明及§5；未视觉核全部图，也未核后续官方SVD实现 |
| L041 | [DragAnything，2024](L041.md) | §3–5、Tables1–3、Figure10文字限制；未逐图/源码/附录全条件复核 |
| L042 | [TextVBench，2026](L042.md) | §4–7协议、匹配/分数/采样、Tables1–2、§8–9局限结论；§3挑战与代码/原始工件未逐项核 |
| L043 | [ViTeX-Bench，2026](L043.md) | 正文§3–7/方程及Tables1–2相关指标；AppA/B/G/H/I/L/M及Table7，部分F基线适配；未逐图/源码/附录O全部身份probe，mask相关Kendall冲突待核 |
| L045 | [CalliReader / CalliBench，ICCV 2025](L045.md) | 正文§1/3–7、Tables2–8；正式CVF元信息，官方supp B/C/D.1–D.2/F.1与TablesS1–S4；未完整D.3/逐图/评审prompt/源码 |
| L046 | [AWCV100K](L046.md) | PDF§III数据、§IV特征/网络、§V设置与TablesIII–V；其他消融表/正式终版与代码待核 |
| L047 | [Recontextualizing Revitalization: A Mixed Media Approach to Reviving the Nüshu Language（NüshuVision / NüshuStrokes）](L047.md) | ACL正式元数据；10页PDF正文、实验Table1、Limitations/Ethics及AppendixA–D文字；官方仓库目录页；未逐图验收/运行代码 |
| L048 | [Tegaki](L048.md) | 官网功能、API样例、FAQ全文；源码/版本/实际字体导出与质量尚未验证 |
| L049 | [SCUT-COUCH2009-TL](L049.md) | PDF采集/标注/算法§2–5、Tables1–4；完整文件规范/授权与当前下载未核 |
| L050 | [CASIA-OHFC](L050.md) | 官方说明的数据/partition/usage/InkML格式；压缩包与配套论文实验尚未完整核查 |
| L051 | [Word-As-Image，2023](L051.md) | 正文§1/3–6、全部核心损失/权重、Table1；AppA/B/C及Figure18中文说明；没有逐图视觉复查全部SVG，代码未核 |
| L052 | [Strike a Chord! Modal Kinetic Typography，2026](L052.md) | 18页正式arXivPDF正文§1–6/全部核心方程/Tables1–2；AppA.4–A.5/A.7–A.11/部分A.12；未逐图/全部FEM附推导/源码（项目页soon） |
| L053 | [Timage: A Generative Text-in-Image Paradigm for Fine-Tuning Vision-Language Models；公开预印本版本](L053.md) | §1/3全方法公式与训练/§4.1–4.5 Tables1–3/§5 Table4效率与局限/§6；未读到supp/代码/训练数据，原文矛盾保留 |
| L054 | [BoxTuning: Directly Injecting the Object Box for Multimodal Model Fine-Tuning；公开预印本版本](L054.md) | §1–5完整方法/训练、Tables1–7和所有主要对照；未核代码/数据清单/训练步数/独立Limitations（正文未见） |
| L055 | [Online Reasoning Video Object Segmentation；公开预印本版本](L055.md) | §3–6完整任务/方法/数据/主表1–3和消融；§1–2关键背景；所有示例图/来源视频与代码未逐一核，未复现 |
| L056 | [CoT-RVS / ThinkVideo](L056.md) | §3–4任务/流程/参数、主表1–6关键结果与消融；AppC/D/F/G/H/I/J及A4/A5；提示全文A/B、Fig8数值不可读部分与各模块代码尚未逐行核 |
| L057 | [Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities](L057.md) | v6摘要、§3分类及指定段落、Tables1/2选定行、§5.4、§6/7指定讨论；34页全文/全部引用/代码未全读，未复现 |
| L058 | [Unified-IO 2: Scaling Autoregressive Multimodal Models with Vision, Language, Audio, and Action](L058.md) | §3.1–3.5、§4数据、Tables2/4、GRIT/缩放段、§5.5及AppB4相关条件；未逐项阅读全部220任务、全部附表/图，未复现 |
| L059 | [AnyGPT: Unified Multimodal LLM with Discrete Sequence Modeling](L059.md) | §3全部表示/架构、§4合成数据、§5 Tables2–6、AppA/C训练与解码条件；未逐图核验多轮示例、未运行代码 |
| L060 | [SEED-X: Multimodal Models with Unified Multi-granularity Comprehension and Generation](L060.md) | §3表示/位置/预训/指令、理解/GenEval主表、§4定性组件比较、AppendixB配置；未完整核验所有附录数据/图和代码，未复现 |
| L061 | [UniTok: A Unified Tokenizer for Visual Generation and Understanding](L061.md) | §1/3–4方法/数据、Tables1/4–9及§5；表2完整生成行、表3VQA逐行/AppendixA图/源码与正式会议版本未全部复核 |
| L062 | [Transfer between Modalities with MetaQueries](L062.md) | Introduction、§3设计/表1–3、§4训练数据、§5.1–5.6解释/表8–9、AppA/C及Table10；未逐行全部主表/全图/代码，未复现 |
| L063 | [MMaDA: Multimodal Large Diffusion Language Models](L063.md) | §2–3完整核心目标/UniGRPO/采样、§4训练和Table3、§5 Tables5/6/协同讨论、§9；官方tree3cdb8709635beb29f66e4e23cd66060872ac3996的generate.py及modeling_mmada.py对应sampling段、stage4头/检索。未通读所有理解表/全仓库RL、未复现 |
| L064 | [MANZANO: A Simple and Scalable Unified Multimodal Model with a Hybrid Vision Tokenizer](L064.md) | §3–4表示/训练、§5.1/5.2 Table1和联合对照/Fig5、§5.4–5.5讨论、结论；未逐行精读全部主表/图、未复现 |
| L065 | [Qwen3-Omni Technical Report](L065.md) | §1–3/主要模块与数据训练、Tables1/2、§6 Table16全表及结论；未逐项读取全部ASR/TTS/VLM表，未复现 |
| L066 | [Emu3.5: Native Multimodal Models are World Learners](L066.md) | §1–4架构/数据/训练/奖励/DiDA、§5部分tokenizer、§6 Tables7–9/16及§6.3–6.8解释、§7局限；未逐行核全部编辑/重建主表、未视觉核对全图、未运行模型 |
| L067 | [Beyond Accuracy: Benchmarking Cross-Task Consistency in Unified Multimodal Models](L067.md) | §3完整构造/匹配/公式、§4 Tables2–8主结果/人评/规模替换、§5–6限制；附录细类全部表和代码未核 |
| L068 | [IMUG-Bench: Benchmarking Unified Multimodal Models on Interleaved Understanding and Generation](L068.md) | §3完整构造/评分/TTS，§4主表2–4/设置/退化/消融，Conclusion；humanjudge附录及所有任务提示未完整核 |
| L069 | [Unison: Benchmarking Unified Multimodal Models via Synergistic Understanding and Generation](L069.md) | §3–5任务/构造/指标/实验，Table2judge及Table3相关行、§6–9insights/limits；源码/训练配置及所有子项未逐一核 |
| L070 | [When Does Visual Generation Help Visual Understanding in Unified Multimodal Models?](L070.md) | §3完整任务/协议、§4.2–4.4结果与Tables2–4、§6限制、AppA.3–A.4实现；完整大表所有行、图像和代码未全核 |
| L071 | [GenEval: An Object-Focused Framework for Evaluating Text-to-Image Alignment](L071.md) | §1、§3.1–3.2、§4、§5.1/5.2关键段/本作比较行、§6、AppA1/A2/Table4、C2/C3检测段；完整标注UI/AppD及全部表格未逐项核，框架图仅文字说明，未运行评价器 |
| L072 | [UniFlow: A Unified Pixel Flow Tokenizer for Visual Understanding and Generation](L072.md) | §3.1–3.2公式/流程、§4.1/4.2关键段、§5/Table6g–i、AppB1配置关键段/B2/B3/B4、AppE；repo e6322d0 README、FlowDecoder439–523及model/config关键行、HF config全文；未视觉核全部图/重训，未复现 |
| L073 | [OFA: Unifying Architectures, Tasks, and Modalities Through a Simple Sequence-to-Sequence Learning Framework](L073.md) | Introduction、§3全部、Table1/5/10/13、§4.4、AppA.1–A.3和B；其他主表未全部逐行，未逐图、未复现；另核正式PMLR PDF第3页Fig2、第9页Table9(对应HTML Table10)、第15页数据表，确认表号版本变化；未把正式Table10误作消融 |
| L074 | [Unified-IO: A Unified Model for Vision, Language, and Multi-Modal Tasks](L074.md) | §3.1–3.4全部、§4 GRIT解释、Table5全表/预算、§4.4–4.6及Table7；未逐行所有任务数据/主表、未视觉验收与复现 |
| L075 | [Versatile Diffusion: Text, Images and Variations All in One Diffusion Model](L075.md) | §3全部、§4.1–4.5/表1/Fig6文字数值、AppC清洗/训练、AppE局限；部分图未视觉读、采样细节未全核、未复现 |
| L076 | [One Transformer Fits All Distributions in Multi-Modal Diffusion at Scale](L076.md) | §3–4完整公式/表示、§6训练/表1/应用、AppD/E与H配置/效率；未逐图/全部采样伪代码验收、未复现 |
| L077 | [Emu: Generative Pretraining in Multimodality](L077.md) | §2–4完整流程/数据、§5主表2/解释/局限、AppA训练/消融表5–7、AppB1；部分图与主表1/3/4未逐行、未复现 |
| L078 | [Planting a SEED of Vision in Large Language Model](L078.md) | §1–3方法与全部Tables1–3、§4–5结论；未核全部图/代码与未披露训练参数，未复现 |
| L079 | [Unified Language-Vision Pretraining in LLM with Dynamic Discrete Visual Tokenization](L079.md) | §1、§3.1–3.3、§4.1–4.3、Table2/3、AppA、AppB Tables4–8、AppC Table9及AppE；未逐图、未核全部评价表/代码、未复现 |
| L080 | [NExT-GPT: Any-to-Any Multimodal LLM](L080.md) | §3–6核心方法、Table4/5及人评说明、AppA、AppC三阶段和Table7、AppD开头及零样本生成表；未逐一核全部QA结果、视频采样条件或代码，未复现 |
| L081 | [DreamLLM: Synergistic Multimodal Comprehension and Creation](L081.md) | §2背景/2.1动机、§3方法/三阶段、§4.2主T2I表尾与协议、§5.1 Table3、AppA Table9、AppC Table11及AppE失败；未逐图/全部主表、未复现 |
| L082 | [Making LLaMA SEE and Draw with SEED Tokenizer](L082.md) | §3/4方法、Tables1/2/4、§4.2主结果解释/4.3全部消融、AppA/B、AppC指定数据行、AppD评测与部分模板；未逐行Table3、未逐图/代码、未复现 |
| L083 | [Generative Multimodal Models are In-Context Learners](L083.md) | §2.1–2.3、§3.1–3.3、Tables3–5、AppA/B含Tables6/7、AppD含Table9、AppE示例选择/Chat协议；未逐行Tables1/2及全部图、未核代码，未复现 |
| L084 | [MM-Interleaved: Interleaved Image-Text Generative Modeling via Multi-modal Feature Synchronizer](L084.md) | §1/3全部、§4.1–4.3、Tables2/3/6–8、AppA Table9与数据、AppB Tables16/17；PDF第6页Fig4和第13页Tables6/7已渲染视觉核对。未逐行全部主表/下游SFT配置、未复现 |
| L085 | [VILA-U: a Unified Foundation Model Integrating Visual Understanding and Generation](L085.md) | §1/3–6相关方法与Tables1/4/6–9、部分GenAIbench表尾、AppA解释与AppC失败配方；官方README、pretrain.sh/sft.sh、datasets_mixture.py、inference.py已读；未逐行Tables2/3/5、未读全部底层generation实现、未复现 |
| L086 | [JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation](L086.md) | §1部分、§3.1–3.4、Table1和§4.1–4.4指定主指标、§4.5 Table6全部、§5、AppB/C/D；未逐行全部主理解表与图、未核代码，未复现 |
| L087 | [Orthus: Autoregressive Interleaved Image-Text Generation with Modality-Specific Heads](L087.md) | arXiv §4–5、Tables3–5、AppA/B/C，正式PMLR第4页Fig2与第8页Tables4/5已渲染视觉核对，正式pp8–9 Limitations已读；未逐行全部理解主表、未核代码，未复现 |
| L088 | [Liquid: Language Models are Scalable and Unified Multi-modal Generators](L088.md) | §2预备/数据/训练、§3.1–3.3、Table1、§4.1 Table3、§4.2解释、§4.3训练/变体、§4.6和§6；未逐图、未逐行全部主理解/语言表、未核代码，未复现 |
| L089 | [ILLUME: Illuminating Your LLMs to See, Draw, and Self-Enhance](L089.md) | §3全部、§4自增强、§5.1/Table5、主Table4本作行、Table2/7和§5.4、结论、AppA tokenizer训练；正式题录已核，未逐行全部主表/全部图、未核代码，未复现 |
| L090 | [MetaMorph: Multimodal Understanding and Generation via Instruction Tuning](L090.md) | §2.1–2.3、§3.1–3.4、主Table1本作行与讨论、AppA.1/A.2、AppB Table3、AppC.1组成、AppD Tables4/5；正式PDF第2页Fig1已视觉核对。未逐图、未逐行AppD Table6/7及全部主表、未复现 |
| L091 | [UGen: Unified Autoregressive Multimodal Model with Progressive Vocabulary Learning](L091.md) | §2.1–2.3及Algorithm1、§3.1–3.5、Tables1/2、AppA Table4相关行；未逐图/读取全部k曲线与附录细项、未核代码，未复现 |
| L092 | [Harmonizing Visual Representations for Unified Multimodal Understanding and Generation](L092.md) | §3.1–3.4、Table1/3、§4设置及§4.2 Tables6–8、Fig6正文解释、§5；未视觉核Fig6/完整图、未逐行全部主表/附录、未复现 |
| L093 | [X-Omni: Reinforcement Learning Makes Discrete Autoregressive Image Generative Models Great Again](L093.md) | §3.1–3.2、§4.1–4.2、Table1和§4.3.1、Tables2/3本作行及协议、§4.4正文、§5、AppA；未视觉读Fig2/6、未逐行全部理解表、未核代码，未复现 |
| L094 | [TokenFlow: Unified Image Tokenizer for Multimodal Understanding and Generation](L094.md) | §1/3–4主要方法、Table4–6、AppA/A.2/Table11、B.1/B.2/B.3/Table8解释与C；Table9逐行/全部图、优化配置和正式PDF差异未全读 |
| L095 | [QLIP: Text-Aligned Visual Tokenization Unifies Auto-Regressive Multimodal Understanding and Generation](L095.md) | §4/4.1、§5.1–5.4指定表与全部主要消融、§6、AppA表8/9；官方README与配置文件相关字段。未逐图/全部主tokenizer表或UM³代码；未复现 |
| L096 | [DualToken: Towards Unifying Visual Understanding and Generation with Dual Visual Vocabularies](L096.md) | §3.1–3.3、§4.1/4.2 Tables3/4/5(b)/6、§5、AppF4/G；官方README/run.sh/256config固定revision；主大表未逐行/正式PDF403、未核实现全部损失或复现 |
| L097 | [UniToken: Harmonizing Multimodal Understanding and Generation through Unified Visual Encoding](L097.md) | §3全部、Tables1/2/5/6、§4.1–4.4、§5与主结果叙述；官方README/TRAIN、base/AnyRes-stage2及phase2yaml已读；未逐行全部主表/逐图或全部实现，未复现 |
| L098 | [Selftok: Discrete Visual Tokens of Autoregression, by Diffusion, and for Reasoning](L098.md) | §2.1指定Eq1–5/叙述、§2.2、§2.3表2–4及指标、§3.1/3.2叙述、§4.1–4.3表7/8本作与Janus行、§5、AppA训练/Algorithm1/评估与B；42页PDF第25页Eq20交叉核。部分公式/全部大表图和代码未读，未复现 |
| L099 | [UniCode$^2$: Cascaded Large-scale Codebooks for Unified Multimodal Understanding and Generation](L099.md) | §3.1–3.6、§4.1/4.2本作行与§4.3、§5/Limitations、AppA2/A3；19页PDF第3页Eq1、第4页Fig2/Eq2–3渲染核对。未逐行全部主表/全部图或代码，未复现 |
| L100 | [TUNA: Taming Unified Visual Representations for Native Unified Multimodal Models](L100.md) | §1定义/动机、§2.1–2.3、§3.1、§3.2本作主行/叙述、Tables5/6本作行、§3.3 Table7全部、§3.4正文、§5；未逐图/全部基线或代码、完整训练协议，未复现 |
| L101 | [UniWeTok: An Unified Binary Tokenizer with Codebook Size $\mathit{2^{128}}$ for Unified Multimodal Large Language Model](L101.md) | §3、§4.1 Tables1–7、§4.2本作行与叙述、§5、App6/7叙述和Table14；未逐图/全部33张表或UMM完整协议/代码，未复现 |
| L102 | [EvoTok: A Unified Image Tokenizer via Residual Latent Evolution for Visual Understanding and Generation](L102.md) | §3.1–3.3、§4.1–4.4 Tables1/4/5及主表本作行、§5；官方README、tokenizer/生成预训/SFT脚本已读固定revision147b1b2；未逐图或全部实现/正式全文，未复现 |
| L103 | [HYDRA: Representation Harmonized Tokenization for Multimodal Generation and Understanding](L103.md) | §2.1–2.3、§3/3.1–3.2指定主行/表3/4、§4、AppD训练和D1–3；PDFp4 Fig3/Eq2–6视觉核对；官方README/配置/模型入口及ICPlan、HF卡指定段落。未逐图全部实验/实际权重，未复现 |
| L104 | [UniCom: Unified Multimodal Modeling via Compressed Continuous Semantic Representations](L104.md) | §3.1–3.3、§4.1–4.4 Tables4/5/6及主表本作行、§5、AppA/F/G；官方README、HF卡、pipeline与runtime加载/解码段落固定revision55b9001。未逐图/全部大表/完整训练代码，未复现 |
| L105 | [Tuna-2: Pixel Embeddings Beat Vision Encoders for Multimodal Understanding and Generation](L105.md) | §1、§2.1–2.3、§3.1–3.6指定主行与完整Table6、§5；未逐图/全部大表/源码或完整硬件采样协议，未复现 |
| L106 | [Representation Forcing for Bottleneck-Free Unified Multimodal Models](L106.md) | §3.1–3.3、§4.1–4.4 Tables2/3与本作主成绩、§5、Implementation/OnlineVQ附录；PDFp16超参与Algorithm1视觉核对。未逐图/完整数据/代码，未复现 |
| L107 | [HYDRA-X: Native Unified Multimodal Models with Holistic Visual Tokenizers](L107.md) | §3、§4.1/4.2 Tables1/2、§5.1–5.3 Table3、§6本作主行/叙述、AppA1–A4/E；未逐图/全部大表/源码，未复现 |
| L108 | [PixelUMM: Encoder-Free Unified Image and Video Understanding and Generation](L108.md) | §2.1–2.4、§3.1 F1/F2/F3/F4/F5/F6/F8及F7部分、§3.2主表本作行、§5；PDFp23 Tables8/9视觉核对。F3全部decoder细节/F7案例/全部图、完整源码与主采样未读，未复现 |
| L109 | [FUDOKI: Discrete Flow-based Unified Understanding and Generation via Kinetic-Optimal Velocities](L109.md) | §2、§3.1–3.4、§4.1–4.3、本作主表行/表头、AppD数据主段与类别、AppE约束、AppF；Fig5仅文字说明未视觉读曲线，完整优化配置/代码未核，未复现 |
| L110 | [Muddit: Liberating Generation Beyond Text-to-Image with a Unified Discrete Diffusion Model](L110.md) | §2.1–2.2.3、§3.1–3.5 Tables1–7本作行/消融、AppA3/E/G1；PDFp4 Fig2/Eq5/6视觉核对；官方README、train_unified掩码与loss段及sh、instruction_tuning答案掩码段，未读全部实现/正式全文，未复现 |
| L111 | [Lavida-O: Elastic Large Masked Diffusion Models for Unified Multimodal Understanding and Generation](L111.md) | §2、§3.1/3.2、§4.1–4.3本作主行及表头、AppB1/2部分/B3/B5主要结果/B6/B7、C/D；未逐图/全部附录公式/代码，未复现 |
| L112 | [Lumina-DiMOO: An Omni Diffusion Large Language Model for Multi-Modal Generation and Understanding](L112.md) | §3.1–3.3、§4.1–4.4、§5、主表本作行、§7.1–7.3/结论；官方README、image_generation_generator与generation_utils相关段，revision81344e6；ht_grpoREADME为后续工作且有正式arXiv，已识别未深读；未全表/全部源码，未复现 |
| L113 | [Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion](L113.md) | §3.1–3.4、§4.1–4.3本作行及评估叙述、AppA/B2–B4/C；未逐图、完整主表/实现/硬件配置，未复现 |
| L114 | [LLaDA2.0-Uni: Unifying Multimodal Understanding and Generation with Diffusion Large Language Model](L114.md) | §2.1–2.3、§4.1–4.4、主GenEval本作行、§5.5 Tables13/14、§6；未读全部数据细分/主大表/公式PDF/代码，未复现 |
| L115 | [FullFlow: Upgrading Text-to-Image Flow Matching Models for Bidirectional Vision--Language Generation](L115.md) | PDF§2插入loss、§3.1–3.5、§5.1–5.6、§6、AppB1–B7部分；PDFp8 Table4/主captionVQA表与课程图已视觉核对。完整评测附录/所有图/代码未读，未复现 |
| L116 | [Multimodal Flow: Unified Flow Modeling of Language and Vision in Embedding Spaces](L116.md) | §2.1–2.4、§3.1–3.5 Tables4–6/主表本作行、AppB1–B3/C1–C3；部分长公式提取只按可见作用解释，未逐图/全部主表/代码/训练超参，未复现 |
| L117 | [BLIP3-o: A Family of Fully Open Unified Multimodal Models-Architecture, Training and Dataset](L117.md) | §2.1–2.2、§3.1–3.3、§4、§5.1–5.4关键段与本作主表/表头、§6；HF8B模型卡全文、旧main README训练/codec段、NEXT README主要模块；旧训练脚本/公式PDF未核，未复现 |
| L118 | [OpenUni: A Simple Baseline for Unified Multimodal Understanding and Generation](L118.md) | §3模型与Table2、§3阶段1/2、§4.1–4.2、§5，主表自身分数/配置行；官方源码/全部采样设置与图未视觉核，未复现 |
| L119 | [UniFork: Exploring Modality Alignment for Unified Multimodal Understanding and Generation](L119.md) | §3.1–3.4、§4.1/Table1、§4.2消融、§4.3/4.4自身主表行、§4.5及Conclusion/Limitations；框架图未视觉读、代码及全部baseline未核，未复现 |
| L120 | [HunyuanImage 3.0 Technical Report](L120.md) | §2.1/2.2主要过滤/标注、§3.1.1–3.1.4、§4.1/Table1、§4.2–4.4、§5.1–5.3及§6；官方revision6e9113a README新闻/模型表/推理推荐/GSB段；SSAE/GSB图未视觉读、完整代码/配置未核，未复现 |
| L121 | [DeepGen 1.0: A Lightweight Unified Multimodal Model for Advancing Image Generation and Editing](L121.md) | §2/SCB三步、§3.1–3.3核心loss/采样、§4数据、§5.1/5.2自身结果/§5.3Tables6/7、§6、App7 Tables8/9及App8采样/奖励/配置/来源；全部基线/公式PDF/官方实现未核，未复现 |
| L122 | [Mobile-O: Unified Multimodal Understanding and Generation on Mobile Device](L122.md) | §3.1–3.4、§4.1及4.4/4.5Tables4–6、§5、App7–9/Table8及§13；PDF第4页Fig2已视觉读。官方README任务/训练段、appREADME前100行、export.py DiT/VAE/MCP/vision导出及LLM量化关键段/默认参数；未编译app/核所有Swift内存逻辑，未运行模型 |
| L123 | [InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing](L123.md) | §3.1.1–3.2.2、§4总表/4.3文字合成、§5.1Tables2/3、§5.2/5.3/5.4选定本作表行和结果段、§6；AppA动机/分类/经典OCR主要公式与MLLM定义/Mini500入口；完整专项合成/AppB和全部图表/代码未读，未复现 |
| L124 | [Mamoda2.5: Enhancing Unified Multimodal Model with DiT-MoE](L124.md) | §2.1–2.4、§3.1/3.2、§4.1/Table1/4.2/4.3、§5.1评价协议与自身结果、§6.1–6.4/Tables10–12、§8/9；官方mamoda25 README模型表/推理/结果及权重段；完整系统优化与全部附表/代码未核，未复现 |
| L125 | [SenseNova-U1: Unifying Multimodal Understanding and Generation with NEO-unify Architecture](L125.md) | §3.1–3.4核心公式/Table1/2及RL/DMD、§3.5分离服务前段、§4.1/4.2、§5.1理解协议/生成分辨率与GenEval自身结果、§5.2/Table23与曲线文字、§6入口；全部主大表/曲线坐标/源码模型卡未核，未复现 |
| L126 | [Rosetta: Composable Native Multimodal Pretraining](L126.md) | §3.1–3.3、§4.1/4.2/Table1/4.3/Table2、§5、AppA1–3/B1–2/C1–3；PDFp4Fig2、p14Eq4/5已视觉核。官方30fada7 train/maop.py32–105、TRAIN选定参数段、README主要入口及projectpage；完整训练调用链/所有采样配置未核，未复现 |
| L127 | [HermesFlow: Seamlessly Closing the Gap in Multimodal Understanding and Generation](L127.md) | arXivv2§3/4/5、AppA；PDFp4Fig3/p13推导；NeurIPS正式§4/5Tables1–5、AppA/Table6，正式PDFp9/p15视觉核。官方4997368 README指定段、train_pairdpo.py参考模型/loss路径及YAML全读；其余正式附录未全读，未复现 |
| L128 | [MindOmni: Unleashing Reasoning Generation in Vision Language Models with RGPO](L128.md) | §3.1–3.4、4.1/4.2关键段、Tables2/3本作行/5–9、AppA1/A3；PDFp7公式及WISE视觉核。正式版本/全框架图/代码与全部理解行未核齐，未复现 |
| L129 | [Co-Reinforcement Learning for Unified Multimodal Understanding and Generation](L129.md) | v3§3.1–3.3、4.1、4.4/Table3–6、5/6、AppA1/A2Table8；主表自身分数/384²行已核，所有外部行及公式PDF/代码未核，未复现 |
| L130 | [PairUni: Pairwise Training for Unified Multimodal Language Models](L130.md) | v3§1/2全方法、§3设置/关键结果/3.2Tables5/6、App6/7Tables7–10/8/9；大表指定模型/编辑行，全部图/正式版本与源码未核，未复现 |
| L131 | [UniCorn: Towards Self-Improving Unified Multimodal Models through Self-Generated Supervision](L131.md) | §3全、§4.1/4.3/4.4/Tables2–4、Limitations、AppArecipe/Table5、C全及D1；PDFp19/20理论视觉核；所有主表/图/代码未全读，未复现 |
| L132 | [Understanding vs. Generation: Navigating Optimization Dilemma in Multimodal Models](L132.md) | §2.1–2.4、3.1/3.2Tables1–5及TIIF自身行、§5、AppA3条件/ITA/VQA/Table7、A5成本；未核全部图坐标、完整理论/源码/maze实验，未复现 |
| L133 | [Learning to Generate via Understanding: Understanding-Driven Intrinsic Rewarding for Unified Multimodal Models](L133.md) | v1§3全、4.1/4.2/4.3–4.5Tables4/5、5/6；官方project、8203768 README/run_grpo.sh、entry注册和gvu_score201–230、trainer430–505的reward/advantage/policyloss段。全部图/完整模型卡/实际运行及模型卡未核，未复现 |
| L134 | [LVRPO: Language-Visual Alignment with GRPO for Multimodal Understanding and Generation](L134.md) | v1§3全、§4设置/主表指定BAGEL与本法行/4.3、AppA/B/C全及F局限；17页PDF指定理论/配置文本核；全部图、全部外部行和代码未核，未复现 |
| L135 | [Uni-Synergy: Bridging Understanding and Generation for Personalized Reasoning via Co-operative Reinforcement Learning](L135.md) | v1§3全、§4设置/主结果/消融、AppB/C/D/E/G；PDFp17/18理论视觉核、layout主表1/2/3/6；官方9ca4254根与子README指定段、grpo.py采样/筛选/奖励组合/更新/控制路径选读；完整源码/数据/图未全核，未复现 |
| L136 | [Pareto LoRA: Mitigating Modality Imbalance in Unified Multimodal Models via Pareto-Optimal Gradient Integration](L136.md) | v1§3全、§4.1–4.5、Tables1–6指定行/结论；10页PDFp4框架图/闭式解视觉核，其他定性图/完整实现未核，未复现 |
| L137 | [STBridge: Shared-Target Alignment for Bridging Understanding and Generation in UMMs](L137.md) | v1§3数据全、§4方法全、§5.1/5.2、主结果指定本法/BAGEL行、5.5Tables7–9、结论；全部图片/大表外部行/源代码未全核，未复现 |
| L138 | [Mutually Adversarial Self-Training with Evolving Data for Unified Multimodal Models](L138.md) | v1§3全、§4.1/4.2本法和基线行/4.3、结论局限、AppB算法1–3及C配置/额外消融/roundtrip；全部图片/外部大表行/发布代码尚未全核，未复现 |
| L139 | [Does Gradient Conflict Predict the Understanding--Generation Trade-off? A Controlled Audit of Conflict-Metric Validity in Unified Multimodal Models](L139.md) | §3–6全文、Tables1–3、AppendicesB/C/D及E部分结果；原CAGrad正式PDF§3/Algorithm1对照；未运行作者实现或核全图 |
| L140 | [Beyond Layers: Position-Resolved Gradient Conflict and Position-Aware Modulation for Unified Multimodal Models](L140.md) | §3–9方法/主表/消融/限制、AppendicesB–E；公式及LoRA预算独立符号核对，未取得附加实现/图像逐项验证 |
| L141 | [Do Text Edits Generalize to Visual Generation? Benchmarking Cross-Modal Knowledge Editing in UMMs](L141.md) | v1§3、§4.1–4.6指定主表/漂移段；正式PDF Table3/4及AppB/C软投影、F温度文本核。AppD传播/SVD完整推导、全部图、代码和其余附录未全核，未复现 |
| L142 | [MME-Unify: A Comprehensive Benchmark for Unified Multimodal Understanding and Generation Models](L142.md) | 旧v2§2全、§3指定分析/§4限制；正式版§2构造与评分、§3设置/Table2全行、AppH2归一及Table13文本核。其余44页图/全部附录与源码未全读，未复现 |
| L143 | [UniEval: Unified Holistic Evaluation for Unified Multimodal Understanding and Generation](L143.md) | v1§3.1–3.3、§4设置/主Table2与4.4、结论，AppC构造指定段/I局限；35页PDF主表2指定全部统一模型行文本核。全部图片/其它表和源码未核，未复现 |
| L144 | [Uni-MMMU: A Massive Multi-discipline Multimodal Unified Benchmark](L144.md) | v3§3任务/评分、§4.1–4.4主表/GT对照、人评；正式PDF主Table2全行、评分段、AppB预算及失败统计首段核。全部定性图/附录数据实例/代码未全核，未复现 |
| L145 | [GENIUS: Generative Fluid Intelligence Evaluation Suite](L145.md) | v1§2/§3设置与主Table2/§4方法理论、AppD1/D2/F/G指定完整推导段文本核；23页PDF主表与理论布局文本核。全部图/发布实现/完整参数未核，未复现 |
| L146 | [A Model-Internal Protocol for Assessing Multimodal Models as Integrated Systems](L146.md) | v2§3全/§4设置主表及阶段替换/§5，AppA/B/C2/E/F1与G指定瓶颈段；21页PDFp4Fig2及p16Eq12–22视觉核，主Table1/2/3与F1文本核。全部图片/源码/剩余附录未全核，未复现 |
| L147 | [WISE: A World Knowledge-Informed Semantic Evaluation for Text-to-Image Generation](L147.md) | v4§3全/§4设置与Tables1/2指定行；AppB/C/G/H/I/J及L限制指定段；正式PDF评分/主表交叉核。全部图/完整模板/代码未全核，未复现 |
| L148 | [ImgEdit: A Unified Image Editing Dataset and Benchmark](L148.md) | v1§3/§4.3/§5；正式§4.1–4.3、AppA4–6/B1/Table5/D Table6/E Table7/F1选读。完整图/数据/代码、其余训练配置未全核，未复现 |
| L149 | [MMIG-Bench: Towards Comprehensive and Explainable Evaluation of Multi-Modal Image Generation Models](L149.md) | v2§3/4与正式主Tables1–3、§5.1/5.2、附录aspect比例/Table4文本核；完整图/余下附录/代码和全部配置未核，未复现 |
| L150 | [KRIS-Bench: Benchmarking Next-Level Intelligent Image Editing Models](L150.md) | v1§3.1/3.4/4与AppC/D/E；正式§3.3/3.4/4.1、Table2指定行/4.3/4.4/结论局限文本核。47页全部图、human图坐标/全任务/代码未全核，未复现 |
| L151 | [CompBench: Benchmarking Complex Instruction-guided Image Editing](L151.md) | v4§3全/§4设置与§5；正式§4.1–4.2、Tables3/4全行和框架Fig3文字说明核。独立supp、全部Table2和图片/源码未全核，未复现 |
| L152 | [OneIG-Bench: Omni-dimensional Nuanced Evaluation for Image Generation](L152.md) | v3§3.2/§4.1/主Table2/文字Table5/AppA2；正式§4.1、Table2、AppA2 Table7/8、人评Table12及读字幻觉段、限制文本核；v3PDFp6公式视觉核。全部图/其余附录/代码未全核，未复现 |
| L153 | [GenExam: A Multidisciplinary Text-to-Image Exam](L153.md) | v5§3.1/§4；正式§3.2/§4设置/Table2指定行/3人评、AppC1/Table4/5及C2；PDFp5 Fig4评分流程视觉核。全部GT/图/附录分类及源码未全核，未复现 |
| L154 | [ChatUMM: Robust Context Tracking for Conversational Interleaved Generation](L154.md) | v2§2/§3 taxonomy、§4.1/4.2；正式§3三阶段说明、Tables1–3、Fig7图注/§5限制。未全审原始数据、补充材料、图或代码，未复现 |
| L155 | [How Long Can Unified Multimodal Models Generate Images Reliably? Taming Long-Horizon Interleaved Image Generation via Context Curation](L155.md) | §3.2/3.3、§4机制全、§5全、§6设置/Table1主体/§6.4/6.6、AppB/C指定部分；PDFp8Fig10及Eq3视觉核，Tables2/3。附录D/F及全部图/代码未全核，未复现 |
| L156 | [Scaling Unified Multimodal Models to Long-Horizon Interleaved Generation](L156.md) | §3方法全、§4设置/Table1/4.4Table2、AppB/C.1–2/C.4–5/D指定指标/E/F.1与Table5/图11图注。部分图、完整评价prompt/训练代码/全部附录未全核，未复现 |
| L157 | [MIO: A Foundation Model on Multimodal Tokens](L157.md) | 正式§2.1/2.2/2.3、§3Tables3–8/3.6、AppB/C超参、Table9/10、E1方法/E6指定段；完整Fig3曲线、所有附录/图/代码未全核，未复现 |
| L158 | [OmniFlow: Any-to-Any Generation with Multi-Modal Rectified Flows](L158.md) | 正式§3.1任务/Algorithm1与3.2/3.3指定段、§4、§5.1–5.4 Tables1–4/§6；补充A.1–A.7及C/D/Table7、E4指定段。部分公式排版/全部图/其他附录/代码未全核，未复现 |
| L159 | [M2-omni: Advancing Omni-MLLM for Comprehensive Modality Support with Competitive Performance](L159.md) | v3§2.1/2.2Table2/AT、§3.1/3.2/3.3、§4.1开头、§5.1指定部分/Table4/7、§5.3 Tables11/12。全部50页/细数据/公式代码/全部图未全核，未复现 |
| L160 | [Ming-Omni: A Unified Multimodal Model for Perception and Generation](L160.md) | v1§2.1/2.3多尺度/2.4、§3.2.2/3.3/3.4、§4Table5/4.3指定段、内部评价定义；原版README图生成/硬件和config全字段核。不是全部论文/全部模块代码精读；未下载权重、未执行或复现 |
| L161 | [Ming-Flash-Omni: A Sparse, Unified Architecture for Multimodal Perception and Generation](L161.md) | v3§2/§3指定数据、§4.1–4.3、Tables2–5指定行；官方README/当前HF模型卡及模态表核。全部附录/所有主表、模型执行代码未全审，未复现 |
| L162 | [LongCat-Flash-Omni Technical Report](L162.md) | §2.1–2.4.1、§3.2指定阶段、§4.1训练/4.2DPO、§6流式、Tables8/14/15；HF卡部署/模态接口。全预训优化/其余评测/代码未全审，未复现 |
| L163 | [ERNIE 5.0 Technical Report](L163.md) | §2.1/2.2视觉、§3.1/3.2、§6视觉Tables4–6、§6.4专家分析/弹性指定段；音频/完整后训练/附录及所有图未全读，未复现 |
| L164 | [MUNI: Multimodal Unified Latent Diffusion for Coherent Any-to-Any Generation](L164.md) | §2/§3/§4、§6.1–6.3/Tables2–4、AppB LemmaB1/命题B2及假设/主要证明、AppD Tables5/6、AppE指定实现/Table7和Limitations。其余附录/全部图/代码未全审，未复现 |
| L165 | [BagelVLA: Enhancing Long-Horizon Manipulation via Interleaved Vision-Language-Action Generation](L165.md) | PDF§3.1–3.5、§4 Tables1/3/4与指定分析、AppD训练/评价；28页全部图/附录/代码未全审，未复现 |
| L166 | [WorldBagel: Uncovering the Power of Unified Multimodal Models for Vision-Language-Action-World Modeling](L166.md) | §3.1–3.5、§4.1/4.4与Tables2–4；AppA1–A4指定定理/证明、PDFp24视觉核。其他附录/全部图及代码未全审，未复现；反例为本次解析分析 |
| L167 | [Vision as Unified Multimodal Generation](L167.md) | §3.1/3.2、§4、Tables1/3/5指定行、§5.6.1、§7.5发布统计；固定README/HF数据及模型卡指定段、TRAIN、PREP开头、YAML首任务/权重与launcher。其余48页、全部配置/代码未全审，未复现 |
| L168 | [Puffin-World: Scaling a Unified Multimodal Model with Native 3D World States](L168.md) | §3.1–3.3/多任务指定段、§4数据指定段、§5.1/Tables1/4/5指定行及Table6/§5.5、AppA2开头；官方Puffin树c6d9ae5e63bc79d5d01554235b7c1d3772c327c8根及World README训练说明。全部附录/配置/代码未全审，未复现 |
| L169 | [InstructPix2Pix: Learning to Follow Image Editing Instructions](L169.md) | 正式§3/§4.1/4.2/§5，PDFp3Fig2与p7Fig8/10视觉核；补充B、C1–3、D指定部分。未全审数据manifest/所有补充图/代码，未复现 |
| L170 | [Multimodal C4: An Open, Billion-scale Corpus of Images Interleaved with Text](L170.md) | §3数据获取/对齐/过滤、正式Table1/3、§4指定下游及§5；对应HTML指定方法/限制。全部图、附录、原始图片与训练代码未全审，未复现 |
| L171 | [OBELICS: An Open Web-Scale Filtered Dataset of Interleaved Image-Text Documents](L171.md) | §3.1–3.5、§4.3人工审查、§5数据混合与Table2、HTML AppA4.1–4.3/Table6/7；未全读所有附录/图或执行训练，未复现 |
| L172 | [OmniCorpus: A Unified Multimodal Corpus of 10 Billion-Level Images Interleaved with Text](L172.md) | v3 §3/§4、§5.1/5.3、§6、AppB1/B2及Tables1–4；官方README固定ce4a012c6adf7c298cd6943a7ad875ec1af1ab6b（2025-05-05）核公开CC/CW/YT及210M版本。未下数据/全审代码，未复现 |
| L173 | [CoMM: A Coherent Interleaved Image-Text Dataset for Multimodal Understanding and Generation](L173.md) | 正式§3/§4/§5、Tables1–4，PDFp4 Eq1视觉核；补充A数据split/E训练、Tables5–9及人评/Claude段落。master树/README/eval图像指标源码核，非全仓审计；未执行模型或复现 |
| L174 | [ShareGPT-4o-Image: Aligning Multimodal Models with GPT-4o-Level Image Generation](L174.md) | v1§2/3/4、Tables1–3及人评设置，官方固定README和T2I示例源码；附录B/C/D完整提示/管线及训练代码、HF实际样本未全审，未执行模型/复现 |
| L180 | [Painter: Teaching Auto-Regressive Language Models to Draw Sketches](L180.md) | §2–3完整数据/模型/loss/训练及Table3和discussion，Table1/2协议；§4相关工作，正式CVF元数据核查；全部图/实现未逐项检查 |
| L181 | [Joint optimization for attention-based generation and recognition of Chinese characters using tree position embedding](L181.md) | 正式作者PDF§3/4(含证明)/5/6/7、Tables1–3/5/7/8关键行、p6公式渲染目视核查；编码实现/全部案例图与训练未复现；官方embed.py TPE全函数、joint.py前向/IF_SIM/dual、optimizer.py和joint_config.yaml只读核对 |
| L182 | [STRIVE: Scene Text Replacement In Videos](L182.md) | CVF正式全文§1/3–5、全部主实验Tables1–2、BPN方程/训练/模拟与结论假设；未读视频/代码/补充，公式符号与OCR定义保留待核 |
| L183 | [CONSTANT: Towards High-Quality One-Shot Handwriting Generation with Patch Contrastive Enhancement and Style-Aware Quantization](L183.md) | CVF正式10页正文§1/3–5、Tables1–6和方程；官方README/DATASET/TRAINING_SAMPLING、IAM/CASIA配置、CASIAconverter、SAQ前向和完整PCE模块。代码tree快照cf31559c036b6f8d5ec64b20bff59809a66c8bfe；未读完整diffusion/pipeline/patchNCE实现/论文所称附录，未下载模型数据或复现。 |
| L184 | [Stroke-Seg: A deep learning-based framework for chinese stroke segmentation](L184.md) | 正式PDF pp4343–4354的相关工作、Figure2说明、§3–6、Tables1–4；主表文字与公式已读，PDF框架/表图未完成可视逐项验收；官方代码选定入口另见S016 |
| L185 | [Training Diffusion Models with Reinforcement Learning（DDPO）](L185.md) | §2相关工作/§3部分、§4.1–4.3、§5–7、AppA/B Table1/C/D与E/F正文；官方23页PDF已获取，未逐图视觉核对、未逐行代码/全部公式或独立复现 |
| N07 | [A stroke-level large-scale database of Chinese character handwriting and the OpenHandWrite_Toolbox for handwriting research](N07.md) | 正式Springer正文PresentStudy、ToolboxDevelopment、采集/编码/排除/结果/部分Discussion；OSF摘要工作簿字段及R指标代码见R07；Tables3–7逐系数、全部附录和原始数据未完整复核 |
| N10 | [Video Text Preservation with Synthetic Text-Rich Videos](N10.md) | 全文Abstract/§1–5(方法/评价/结论完整)；参考文献未逐项追溯，图中视频未独立播放，未定位到训练实现 |
| N11 | [CalliffusionV2: Personalized Natural Calligraphy Generation with Flexible Multi-modal Control](N11.md) | §3–5全部核心方法、数据、Tables1–3、fewshot/编辑/非汉字说明；全部图样与公开训练实现未逐项核，正式发表未确认 |
| N12 | [CalliPaint: Chinese Calligraphy Inpainting with Diffusion Model](N12.md) | 全文§1–4与AppendixA/B文字和Tables1/2完整；框架图具体层次、所有图选项及原Calliffusion训练实现未核 |
| N14 | [SteerVTE: Seamless Video Text Editing with Style and Glyph Control](N14.md) | §1/3全部方法与数据、§4 Tables1/3/4主表和消融、§5局限；§7.2/8.1/8.2完整协议；Table2仅关键行/解释，未逐图/代码/数据文件复核 |
| R01 | [Hanzi Writer（工具，不是论文）](R01.md) | 官方docs Animation/Quiz/Loading character data/Raw Character SVG/配置项；LICENSE来源另列；未核quiz匹配实现或运行浏览器 |
| R02 | [Make Me a Hanzi（数据/工程资源）](R02.md) | 官方README数据格式/来源/笔顺/坐标/下载说明与COPYING全文；没有下载全库或执行解析 |
| R03 | [CASIA-HWDB / CASIA-OLHWDB（数据）](R03.md) | 官方home采集/作者划分，Online Database全部POT/WPTT格式和统计表，Conditions of Academic Use；未下载样本或重读ICDAR2011全篇 |
| R04 | [IAM-OnDB（数据）](R04.md) | 官方主页面Overview/Characteristics/Terms索引正文，旧官网Data format字段完整索引；未读基础论文全文/实际下载样本 |
| R05 | [Mobao（Moyun配套静态书法数据）](R05.md) | Moyun v2 §4.1收集/分割细节与Introduction规模对照；B04已有模型笔记，本卡不重复统计为独立论文 |
| R06 | [通用规范汉字笔顺规范](R06.md) | 官方PDF前12页；§1–5全文及§6开头示例；8105逐项、全部索引与后部表未完成逐字核查 |
| R07 | [OpenHandWrite_Toolbox与笔画级数据](R07.md) | OSF node/files API及Data/R子目录、batch_summarise_all.R全文、batch_funcs.R定义及长度/首末点/相邻延迟函数、小xlsx全部表头和各2行样例；未运行R/全读脚本和下载完整采集包 |
| S007 | [Brush Calligraphy Stroke Segmentation Dataset (BCSS)](S007.md) | 固定HF README完整数据/加载段、两个info.csv头部样例和范围，正式论文§3–5对照；未下载全mask或逐图审查 |
| S008 | [Wuji Writing VAM TI2V-5B 30L 0522 0819](S008.md) | 固定HF revision的README、model_config.json、training_config.yaml；未下载11.54GB权重，动作统计与日志仅卡片引用，未执行模型 |
| S009 | [AnimCJK](S009.md) | 官方README目录/使用/完整“中”SVG示例与许可；长历史changelog、全部字库和生成脚本未逐项读 |
| S010 | [KanjiVG](S010.md) | 官方README全文；SVG规范关于group/path/顺序/属性与已知不一致部分；04e2d.svg全文；未逐字库核查 |
| S011 | [Qari-OCR-LoRA](S011.md) | 官方GitHub README、HF固定revision README/adapter_config.json/training_info.json与推理示例全部相关内容；未下载adapter或运行OCR |
| S012 | [CASIA-HWDB2-line (Teklia HF derivative)](S012.md) | HF固定revision README全部字段、规模/示例/许可；未下载全parquet或逐条图像核验 |
| S013 | [SceneDAPR](S013.md) | 官方README核心数据/标注/训练/许可和完整src/preprocessing.py；blob bf765c696bcd1aa95cdf8879a366b01a7f377da3；未读WWW全文及受限数据 |
| S014 | [sketch-diffusion (ark60 independent implementation)](S014.md) | notebook关键数据处理/attention/model/diffusion/trainer/config/evaluation及保存输出；未执行notebook、未下载数据权重；保存输出的运行环境和文件对应仍待核 |
| S015 | [VidSketch sketch animation implementation](S015.md) | 官方README核心/许可；candles.yaml全文、train_vidsketch.py初始化/参数选择/优化器/主损失、inference.py adapter加载段；未全读所有模块或执行；blob config cd2b32c8df4a8564a156727b86f561dc81d3c95c/train 9d459e78da5e058be84b656ddd881b12ab7f5ecc |
| S016 | [BCSS Stroke-Seg implementation](S016.md) | 官方README全部、recursive tree、FCN.py与deeplab.py全文、LabelMe01字段；未执行、未读全部子模块，未取得主表checkpoint |
| U01 | [Chameleon: Mixed-Modal Early-Fusion Foundation Models](U01.md) | §2.1–2.4，Tables1–2/7，训练稳定性曲线 |
| U02 | [Emu3: Next-Token Prediction is All You Need](U02.md) | §2数据/模型，Tables1–3/7–8及视频VBench表 |
| U03 | [Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation](U03.md) | §3训练目标/阶段，§4.1/Table1，§4.5/Table5 |
| U04 | [Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling](U04.md) | §2.1–2.3，训练Table2，§3.1及主评测表 |
| U05 | [Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model](U05.md) | §3目标/attention，§4.1，§4.3/Table5及patchsize讨论 |
| U06 | [Show-o: One Single Transformer to Unify Multimodal Understanding and Generation](U06.md) | §4.1/Table1，Table4及表示选择研究 |
| U17 | [Uncovering Understanding-Generation Synergy in Native Unified Multimodal Models: From Representation, Task to System](U17.md) | 摘要，§3/Table1与探针，Tables4–5，系统任务说明和SVG诊断附录 |
| U18 | [Transferability Between Understanding and Generation in Unified Multimodal Models](U18.md) | §3–5；Tables1/3/4/10/11/12；Appendix0.A、0.B.2、0.C、0.E |
| X01 | [InkSight: Offline-to-Online Handwriting Conversion by Teaching Vision-Language Models to Read and Write](X01.md) | §3架构/五任务/token，§4.1–4.7数据、Table2/3及限制；AppendixG尚待完整摘录 |
| N13 | [The Unwritten Benchmark: A New Challenge for Multimodal Machine Learning in Abstract Perceptual Reasoning](N13.md) | §1–5主方法、Tables1–3及§6开头；未读完整§6后段/全部附录、未审数据生成代码；无模型执行 |
| U07 | [Unified Multimodal Discrete Diffusion (UniDisc)](U07.md) | §3.1–3.4含Eq2/3、§4.1/4.2、AppB1/C/F/H1 Tables3–6；Fig2 PDFp5视觉核。完整检索/大模型训练/AppI/J与全部图未全读；未复现 |
| U08 | [Zebra-CoT: A Dataset for Interleaved Vision Language Reasoning](U08.md) | §1/§3.1、§5训练/主Table2、AppA1 Table3、Table8 Tetris指定行及脚手架定义；其余类别采集/Bagel补充结果/完整prompt与代码未全读，未复现 |
| U09 | [ThinkMorph: Emergent Properties in Multimodal Interleaved Chain-of-Thought Reasoning](U09.md) | §2/§3主表2、§5.2指定分析、AppB1–B3/B7 Tables4–6/8与§7；PDFp16视觉核。正式目录确认，OpenReview PDF403；其余形式化分析、全部案例/prompt和代码未全读 |
| U10 | [Monet: Reasoning in Latent Visual Space Beyond Images and Language](U10.md) | 正式CVPR§3.2–3.4 Eq7/8、§4 Tables2–5；arXiv§3.1–3.3及AppB/C训练Table7/8/梯度surrogate；官方README/launcher、actor135–158与300–303、runner1326–1337等指定行。全pipeline和其余附录未全审，未执行模型；arXivPDFp3 Fig1已渲染视觉核 |
| U11 | [Omni-R1: Towards the Unified Generative Paradigm for Multimodal Reasoning](U11.md) | §3/§4.1–4.2 Eq1–16、§5 Tables2–4、AppC/D Table6；其余图/协议细节和源码未全读，未复现 |
| U12 | [WEAVE: Unleashing and Benchmarking the In-Context Interleaved Comprehension and Generation](U12.md) | 正式§3方法、Tables2–4、§4.4指定段；arXivAppB2/B3训练/评分/历史及部分推理配置；固定官方README与summarize82–109核权重。全收集附录/所有分域表及judge执行未全审 |
| L178 | [Drawing and Recognizing Chinese Characters with Recurrent Neural Network](L178.md) | §II/§III核心表示与优化、§IV TablesI/II、§V生成Eq23–44、§VI实现与质量、§VII指定段；CrossRef期刊卷页日期核。2018正式全文/全部图、相关工作追引/代码未全读，未复现；arXivPDFp8 Fig5与p7 TableIII已渲染视觉核 |
| L003 | [Write Like You，2021](L003.md) | 作者公开正式PDF §2.3–5核心表示/公式/实现、Tables1–7及结论指定段；PDFp3 Fig2已视觉核；固定代码model.py默认/均值cycle与README/train部分。补充材料/完整源码及全部附图未读；未复现 |
| S002 | [TextDiffuser: Diffusion Models as Text Painters](S002.md) | 正式§3.1–3.2/§4.2/§5.1–5.2 Tables1–4、AppA/B/H指定段；PDFp4 Fig2已视觉核。固定README训练配置已读；完整数据过滤/附录/训练源码未全审；未复现 |
| S003 | [GlyphControl: Glyph Conditional Control for Visual Text Generation](S003.md) | 正式§3.2–4.2、§4.5 Table3和§5指定段、Tables1/2；固定README与主训练YAML。完整AppendixD/全部源码/框架视觉图未核，未复现 |
| U13 | [Quantifying the Gap between Understanding and Generation within Unified Multimodal Models (GapEval)](U13.md) | §2.1–2.4/§3.1–3.2 Table2、§4.1指定段、AppB1–B4/C/E部分/F2.2/F3；全文其余图表和实现未全审，无模型执行 |
| U14 | [UniG2U-Bench: Do Unified Models Advance Multimodal Understanding?](U14.md) | §3.1–3.2核心定义、§4.1指定段/Table2、§4.2–4.4协议/metrics、Table4及Table6标题；其余长附录/全部主表分域/源码未全读，未复现 |
| U15 | [RealUnify: Do Unified Models Truly Benefit from Unification? A Comprehensive Benchmark](U15.md) | §3.1指定段/§3.3数据和协议、§4.1指定主文、Tables3–5与Table2部分、AppA3/B2指定段。完整Table2底行、所有细分/配置/源码未读，未复现 |
| U16 | [Can Unified Generation and Understanding Models Maintain Semantic Equivalence Across Different Output Modalities? (VGUBench)](U16.md) | §3.1指定定义/§3.2数据/§3.3评分指定段、§3.4统计、§4.1指定协议、Tables1/2；完整prompt附录/源码/其余分析未全审，未复现 |
| U19 | [Generation Enhances Understanding in Unified Multimodal Models via Multi-Representation Generation (UniMRG)](U19.md) | §3.1核心loss及§3.2指定动机、§4.1/§4.2 Table1/2和§4.3指定消融段、AppB1–B3。Table3完整/附录其余/源码未全审，未复现 |
| U20 | [Semantic Generative Tuning for Unified Multimodal Models (SGT)](U20.md) | §3.1–3.3指定方法/动机、§4.1–4.3指定段、Tables2/3，§5；AppTable6/7/8/9及7.3指定配置。未审全部图/7.1/源码/最终recipe末段，未复现 |
| U21 | [Model Guides You How to Draw: Adaptive Visual Gating for Unified Multimodal Reasoning (AdaViG)](U21.md) | §5.1–5.3 Eq4–6、§6.1配置/Tables1–4、AppA6限制/A7部分表；完整§3/§4控制诊断与App阈值/代码未全读，未复现 |
| U22 | [UEval: A Benchmark for Unified Multimodal Generation](U22.md) | §2概述/§2.1指定来源、§2.2rubric与人审、§3.1–3.3指定段/Tables1/2、Fig7/8对应说明；完整trace实验/附录/实现未全审，未复现 |
| U23 | [Self-correction Optimization for Interleaved Multimodal Generation (SCO)](U23.md) | §3.1–3.4 Eq1–13、§4.1指定数据/§4.3–4.7指定结果/Tables1–5，AppA1视频与A3指标指定段；完整优化实现/视频数据协议及源码未全审，未复现 |
| U24 | [Unified Multimodal Autoregressive Modeling with Shared Context-Visual Tokenizer is Key to Unification (UniAR)](U24.md) | §3.1–3.3核心公式、§4.1训练/§4.2指定主表/§4.3指定组件，Tables1–3/6–9和AppA1–A4/B；全部理解表/源码/所有消融图未审，未复现 |
| U25 | [Visual Generation Unlocks Human-Like Reasoning through Multimodal World Models (VisWorld-Eval)](U25.md) | §3.1–3.4指定定义/定理、§4.1–4.2、§5.1–5.2指定段与§5结尾限制；AppA1/A2 Theorems3/4及Corollary1证明、AppB1部分/B2 Tables2–4。完整先验分析/其他证明/主图数值/全部附录与代码未审，未复现 |
| U26 | [SenseNova-U1.5: Towards Native Unified Visual Intelligence](U26.md) | §3.1–3.2主架构及五阶段/OPD，Tables1/2/8/9/11/12/21、官方README发布及training README范围指定段；完整数据§4/全部榜/消融/源码未全读，未复现 |
| U27 | [UniModel: A Visual-Only Framework for Unified Multimodal Understanding and Generation](U27.md) | §3.1–3.3、§4.1–4.5指定方法和实验/限制；未逐图核全部样例，未审代码或获得缺失训练配置，未复现 |
| U28 | [LatentUMM: Dual Latent Alignment for Unified Multimodal Models](U28.md) | §3.1–3.3 Eq1–5、§4.1/Tables1–3及4.3指定段/4.5–4.6，AppB效率/C1–C4；TorchUMM425efa19cb2a18d43278d4d222ed238b5e244546 README、stage1 model、stage2辅助脚本、bagel.py374–412及train loss聚合。全源码/消融未全审，未执行模型 |
| U29 | [Bridging Modality Disconnect in Self-Reflection via Closed-Loop Visually Grounded Verification (MIRROR)](U29.md) | §3.1–3.3及Fig2视觉核、§4.1–4.3、Tables1/2/4/6；AppA1/A2、B1–B3、D2 Table11。完整12榜实现/其他消融及代码未审，未复现 |
| U30 | [LatentUM: Unleashing the Potential of Interleaved Cross-Modal Reasoning via a Latent-Space Unified Model](U30.md) | §3.1–3.3、§4.1–4.3及导航实现段、Tables2–4；AppA1/A2/B1和Fig2PDFp4视觉核；完整导航图/所有消融/附录及代码未审，未复现 |
| U31 | [DIVA: Harnessing the Representation Divergence in Unified Multimodal Models for Mutual Reinforcement](U31.md) | §3.1–3.3 Eq4–11、Tables1–4及§4.1指定数据；AppB1/B2 Tables7/8及B3指标。完整诊断图/全部表/代码未核；GenEval数值冲突未解决，未复现 |
| L186 | [Towards Human-Like Robot Handwriting via Contour-Aware Generation](L186.md) | 正式CVF PDF§1/§3–7与Tables1–6、Fig5PDFp6已渲染核；官方CVF元数据/补充zip链接、GitHub树与README。未读supp/逐图或控制代码，未运行机器人/模型 |
| N08 | [Hierarchical offline-to-online Chinese handwriting trajectory reconstruction via dual-domain priors](N08.md) | Springer正式PDF§3.1–3.8选定公式/Algorithm1及§4.1–4.5、Tables1–7、Fig2/3PDFp5视觉核；完整Algorithm2/全部参数与用户实验/代码未审，未复现；与L006同作者不同题目和DOI独立记录 |
| R08 | [SenseNova-U1.5-8B-MoT-LoRAs：8step与V2蒸馏适配器、加载与训练配置](R08.md) | HF API文件列表与README指定头部/QuickStart/模型表/Limitations/License；GitHubREADME发布及base_vs_distill条件、utils/lora.py指定加载逻辑、trainingREADME范围；未下载权重、未运行或审全训练实现 |
| N01 | [UniCalli: A Unified Diffusion Framework for Column-Level Generation and Recognition of Chinese Calligraphy](N01.md) | 作者ICLR正式PDF§3.1–3.4/§4.1–4.3、Tables1–6、AppB/C/D/E/G及H用户研究指定段；Fig2 PDFp4视觉复核。完整代码、其余应用图及全部古文字细节未审，未复现 固定源码README、inference.generate、sampling.prepare/denoise及model.init_module_embeddings/forward指定路径已审。 |
| N02 | [Bridging Online and Offline Handwriting via Differentiable Physical Rendering (OnOff Handwriting)](N02.md) | §3.1–3.3/§4.1–4.4/§5/§6、Tables2–4，AppB/C与D1/E3指定段，Fig5 PDFp9视觉核。完整机器人映射参数、指标实现及余下附录/代码未全审，未执行模型或机器人 固定官方仓库README与文件树已核，未有完整模型源码。 |
| N03 | [DeepCalliFont: Few-shot Chinese Calligraphy Font Synthesis by Integrating Dual-modality Generative Models](N03.md) | 正式AAAI主文Introduction、Method Eq1–22、Experiments Tables1–2/消融与Limitations；Fig2 PDFp3及Table1所在p7视觉核。补充材料/完整实现未全审，未复现 固定官方README/config及train.py的optimizer/loss/rasterizer段；非全部模型/数据实现审计。 |
| N04 | [Beyond Legibility: Benchmarking Visual Text Rendering and In-Place Editing in Unified Video Generation (VidScribe)](N04.md) | v2 §3.1–3.3/§4.1–4.3、Tables1/3/4/11、AppA2/F12、B1 grounding/A1/A2/B1、C1/C2/C3指定段；Fig3 PDFp6视觉核。完整任务分表、结构检查源码/全API协议未全审；未运行模型 |
| N05 | [VTR-Bench: A Systematic Benchmark for Evaluating Visual Text Rendering in Video Generation](N05.md) | v1 §3.1–3.4/§4.1–4.5，Tables1–5/Fig7、AppB构造与C1–3指定段；Fig4 PDFp6视觉核。完整prompts/工具源码、后续分项图未审，未复现 |
| N06 | [Video models are zero-shot learners and reasoners](N06.md) | v2 §1–2/§3定性协议、§4.1–4.7/讨论、AppA Figure30、B总表/B1/B2/B5/B6与Cpromptstudy指定段。未逐读62任务全部视频、未独立审生成原片；Figure30 caption核而非完整stroke实测，未复现 |
| N09 | [Text-Animator: Controllable Visual Text Video Generation](N09.md) | v1 §3.1–3.4/§4.1–4.5、Tables1–3与Conclusion，Fig2 PDFp4视觉核。未审完整code、OCR/FID/相机配置和实际视频原片，未复现 |
| L011 | [Draw This First](L011.md) | v1 §3.1–3.4/§4.1–4.3/§5–6，Tables1–9、AppA–F指定公式/算法/协议段，Fig1 PDFp3视觉核；未逐图核所有定性样例或审全部代码，未复现 |
| S001 | [Ketaba-OCR at AR-MS NakbaNLP 2026](S001.md) | ACL正式PDF§2–6与AppA–H指定协议/全部Tables1–10，Arabic原文受文本提取字形影响，未逐字翻译判读；官方固定GitHub YAML/README及HF元数据另核。未运行模型，未独立读取隐藏GT GitHub YAML/README、train_model/preprocess_sample、ensemble.normalization/voting指定函数及HF README/adapter_config/training_info已审。 |
| L026 | [UniVideo](L026.md) | v4 §2/3.1–3.4、Tables1–7、AppD1/E/F/G1指定段；Fig2 PDFp3已视觉核；v2训练与数据表历史对照。固定代码893c9da的README/TRAINING/EVAL/hiddenyaml已读；AppG其余数据、完整test细目、所有实现仍待后续，不计完整三遍 |
| L028 | [Lance: Unified Multimodal Modeling by Multi-Task Synergy](L028.md) | v1 §3–7、Tables2–5/9/10、VBench/理解主表指定列；Fig6 PDFp9已视觉核。固定代码4baeee的README/train.md/train_dataset.md/unified数据yaml、HF7395315的配置/llm配置已读；全专家源码/GRPO实现未审，不计完整三遍 |
| L044 | [CalligraphyBench](L044.md) | 固定HFREADME/API树；datasetsserver全部88行元数据/几何长度检查；网站首页catalog/detailJS内TaskSetup/Scoring/来源与tool协议。未执行工具、未人工读全88参考图、未重评分，状态仅资源协议审查 |
| L175 | [XMP-Font: Self-Supervised Cross-Modality Pre-training for Few-Shot Font Generation](L175.md) | 正式CVPR§1/3/4/5、Tables1/2，Fig2 PDFp4已视觉核；arXivv1网络结构附录Table3–5指定段。未获取/审完补充代码及所有字体切分，不计完整三遍 |
| L176 | [Representing Online Handwriting for Recognition in Large Vision-Language Models](L176.md) | v1§1–6、Tables1–10、AppB/D/E/F指定段；Fig2/3 PDFp4已视觉核。完整采样间隔、优化器/LoRA配置和代码未核，不计完整三遍 |
| L177 | [PaintFlow: A Unified Framework for Interactive Oil Paintings Editing and Generation](L177.md) | v1主文Method/Experiments/Conclusion、Table1、supp interface/Algorithm2/ExperimentSettings/UserStudy/Table2；Fig2 PDFp3已视觉核。SBR具体版本、代码、全部结果图/物理执行未核，不计完整三遍 |
| L179 | [UM-Text: A Unified Multimodal Model for Image Understanding and Visual Text Editing](L179.md) | v1§1–5、Tables1–4；Fig3 PDFp3已视觉核；AAAI官方页面出版元数据核。正式PDF技术差异、源代码与完整UMT协议仍未审，不计完整三遍 |
| S004 | [VidSketch: Hand-drawn Sketch-Driven Video Generation with Diffusion Control](S004.md) | v1 Method/主表/ablation/AppA/B指定段，v2对应方法、Table1和AppA4；Fig3 v2PDFp3视觉核；固定ad7fcdb README、VidSketch/inference.py抽象度/参数调用、train_vidsketch.py配置默认及noise/loss段、configs/candles.yaml全文件、inference/pipelines/pipeline_VidSketch.py adapter门控/scheduler指定段。未审全部模型源码和论文实验日志，不计完整三遍 |
| H001 | [CoFRIDA-Sharpie：机器人共同绘画LoRA模型制品](H001.md) | 固定HF README/API文件树、现存H001制品卡及F04关联；未加载或运行权重，仅资源协议审查 |
| L187 | [Visual-OPSD: Cross-Modal On-Policy Self-Distillation for Efficient Unified Multimodal Reasoning](L187.md) | v6 Abstract/Introduction/Method§2含Eq1–7与AppB证明、Experiments§3/Table1–3、Conclusion；AppC/D/E/F/G/I/J/M指定配置/公式/评价及K/L正负案例文字。Fig4 PDFp5视觉核；固定32f245d README/TRAIN/EVAL和opsd_loss.py26–103核。未逐图核所有案例、未审全部trainer/harness或下载权重。三遍核心阅读和五项书面理解检查完成，复现另列。 |
| L188 | [LiveSVG: Zero-Shot SVG Animation via Video Generation](L188.md) | v1 Abstract/Introduction/§3方法Eq1–4/§4主结果与§5限制；AppA–F/H指定结构/表3–9、评分prompt、人评与优化协议，Fig3PDFp5视觉核。公开项目页入口已定位；完整实现未取得。三遍核心阅读与五项书面理解检查完成，正文/附录冲突保留。 |
| L189 | [AniClipart: Clipart Animation with Text-to-Video Priors](L189.md) | 正式IJCV PDFAbstract/Introduction、§3所有方法与Eq1–4、§4.1–4.5主表/消融/分层及§5讨论；Fig3PDFp5视觉核，部分定性样例仅读说明。固定fee58e05README和树；supp视频与完整代码未审。三遍核心阅读/五项书面理解检查完成，未独立复现。 |
| L190 | [VitaGlyph: Vitalizing Artistic Typography with Flexible Dual-branch Diffusion Models](L190.md) | 正式WACV2026主文§1/3/4/5/6、Tables1/2和Fig2PDFp2视觉核；v3补充I–III/V–X指定prompt/CFG/配置/五轮/人评/耗时/局限。固定ca7d0f8 README、docs/generation115–177及模型位置段、generation.py指定条件/融合调用、acg_attention.py1–75。旧URLCarlofk1返回404，已按正式paper链接修正为Carlofkl；未跑预训模型。三遍核心阅读/五项书面理解检查完成。 |
| R09 | [Datumwell Handwriting：10个完整模拟书写episode公开样本、动作与低频RGB对齐](R09.md) | 固定HFREADME/API74项列表、publicationstatus、meta/info、coverage、samplemanifest全部10例、qualityflags/camerareadability、featurepolicy、actionschema、loader及UJIprovenance；conversion指定时间/动作字段，首例frames全部378时间戳数值检查。未下载完整视频/轨迹、未执行模型或动作；属于资源协议审查。 |
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
