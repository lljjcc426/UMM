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
| G027 | [Elucidating the Design Space of Diffusion-Based Generative Models](G027.md) | 原始摘要及设计空间概述；实验表尚未读完 |
| G028 | [Generative Adversarial Nets](G028.md) | minimax目标与理论假设，§5/Table1，指标限制 |
| G029 | [Auto-Encoding Variational Bayes](G029.md) | ELBO/重参数化推导，§5实验设置与学习算法比较 |
| G030 | [Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion](G030.md) | 逐token噪声方法，§4.1同架构视频比较，规划任务区分 |
| G031 | [VBench: Comprehensive Benchmark Suite for Video Generative Models](G031.md) | §3.1–3.3，Table1，§4，人工配对协议 |
| G032 | [Towards Accurate Generative Models of Video: A New Metric & Challenges](G032.md) | 度量与特征设计，§4.1噪声，§4.3/Table1及人工协议 |
