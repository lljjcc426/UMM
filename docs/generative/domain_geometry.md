# 物理、几何、医学与其他领域

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 17 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2603-05527"></a>

## Drifting to Boltzmann: Million-Fold Acceleration in Boltzmann Sampling with Force-Guided Drifting

作者：Pipi Hu。标识：`2603.05527v1`。首次公开：2026-02-26；所查版本更新：2026-02-26。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Force-Guided Drifting 用力标签替换或修正目标 score，比较坐标和距离特征中不同的力注入方式。

限制与判断：百万倍宣传对应传统分子动力学基线，不能当作相对同硬件扩散的统一加速比；力标签也有成本。

原始来源：[来源1](https://arxiv.org/abs/2603.05527v1)

<a id="paper-2603-11854"></a>

## Inverse Neural Operator for ODE Parameter Optimization

作者：Zhi-Song Liu、Wenqing Peng、Helmi Toropainen、Ammar Kheder 等8人。标识：`2603.11854v1`。首次公开：2026-03-12；所查版本更新：2026-03-12。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：INO 先用条件神经算子重建 ODE 轨迹，再以摊销漂移从观测反演参数。

限制与判断：速度比较包含预先学习代理的投入；代理误差和反问题可辨识性与参数更新稳定性分别存在。

作者元数据备注（与独立核实分开）：17 pages, 6 figures

原始来源：[来源1](https://arxiv.org/abs/2603.11854v1)

<a id="paper-2603-17579"></a>

## One-Step Sampler for Boltzmann Distributions via Drifting

作者：Wenhan Cao、Keyu Yan、Lin Zhao。标识：`2603.17579v1`。首次公开：2026-03-18；所查版本更新：2026-03-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：针对只知未归一化能量的 Boltzmann 目标，以平滑能量、重要性估计或曲率修正构造目标侧场。

限制与判断：主要为低维多峰及弯曲能量的合成验证；未知归一化常数处理不等于解决高维采样覆盖。

原始来源：[来源1](https://arxiv.org/abs/2603.17579v1)

<a id="paper-2603-28498"></a>

## MRI-to-CT synthesis using drifting models

作者：Qing Lyu、Jianxu Wang、Jeremy Hudson、Ge Wang 等5人。标识：`2603.28498v2`。首次公开：2026-03-30；所查版本更新：2026-04-06。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在盆腔 MRI 到 CT 任务中比较一步漂移、CNN、GAN 和多步扩散，评价骨界面重建。

限制与判断：任务特定图像指标与后续放疗可靠性不同；真实泛化和下游用途不能由样例清晰直接推出。

原始来源：[来源1](https://arxiv.org/abs/2603.28498v2)

<a id="paper-2604-19736"></a>

## Generative Drifting for Conditional Medical Image Generation

作者：Zirong Li、Siyuan Mei、Weiwen Wu、Andreas Maier 等6人。标识：`2604.19736v1`。首次公开：2026-04-21；所查版本更新：2026-04-21。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：GDM 以医学编码器多级特征库估计三维条件漂移，并协调分布目标和患者级保真梯度。

限制与判断：医学预训练、配对信息和梯度协调共同贡献，未证明仅换漂移损失即可保持实例细节。

原始来源：[来源1](https://arxiv.org/abs/2604.19736v1)

<a id="paper-2605-02325"></a>

## DriftDecode: One-Step Wireless Image Decoding via Drifting-Inspired Detail Recovery

作者：Jingwen Fu、Ming Xiao、Mikael Skoglund。标识：`2605.02325v1`。首次公开：2026-05-04；所查版本更新：2026-05-04。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftDecode 以空间对齐真值特征的实例纹理漂移辅助单步无线图像恢复。

限制与判断：接收信号已含粗结构，目标是受损细节恢复；不属于完整无条件分布采样的同一问题。

原始来源：[来源1](https://arxiv.org/abs/2605.02325v1)

<a id="paper-2605-06140"></a>

## SymDrift: One-Shot Generative Modeling under Symmetries

作者：Samir Darouich、Vinh Tong、Lluís Pastor-Pérez、Tanja Bien 等6人。标识：`2605.06140v3`。首次公开：2026-05-07；所查版本更新：2026-09-29。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/151782)

方法：SymDrift 对齐坐标或使用群不变嵌入，使漂移场本身适应分子等任务的全局对称性。

限制与判断：等变生成器不自动消除经验分布的对称偏差；汉字规范方向不可随意当作应消去的旋转对称。

原始来源：[来源1](https://arxiv.org/abs/2605.06140v3) · [来源2](https://neurips.cc/virtual/2026/poster/151782)

<a id="paper-2605-17188"></a>

## RDDM: A Residual-Driven Drifting Model for High-Fidelity Low-Dose CT Denoising

作者：Jianxu Wang、Qing Lyu、Ge Wang。标识：`2605.17188v1`。首次公开：2026-05-16；所查版本更新：2026-05-16。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：RDDM 在低剂量 CT 的残差上建立吸引排斥场，配合像素监督形成不同保真噪声权衡。

限制与判断：收益包含配对像素监督与残差设计；临床结论超出公开图像质量比较的证据范围。

作者元数据备注（与独立核实分开）：Code is available at: https://github.com/Jayx-Wang/RDDM

原始来源：[来源1](https://arxiv.org/abs/2605.17188v1)

<a id="paper-2605-22990"></a>

## Drift-React: One-step Generation of Reaction Pathways via SE(3) Drifting Fields

作者：Rémi Schlama、Philippe Schwaller。标识：`2605.22990v1`。首次公开：2026-05-21；所查版本更新：2026-05-21。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/154432)

方法：Drift-React 以 SE(3) 等变模型和 Sinkhorn 加权漂移从反应物、产物预测完整反应路径。

限制与判断：反应坐标上的连续路径与视频物理时间不同；能量瓶颈和几何误差不证明一般事件顺序推理。

原始来源：[来源1](https://arxiv.org/abs/2605.22990v1) · [来源2](https://neurips.cc/virtual/2026/poster/154432)

<a id="paper-2605-24841"></a>

## DriftingMol: Decoder-Coupled Drift for One-Pass Property-Conditional Molecular Generation

作者：Jiangjie Qiu、Yijun Li、Wentao Li、Xiaonan Wang。标识：`2605.24841v1`。首次公开：2026-05-24；所查版本更新：2026-05-24。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftingMol 使用冻结 SELFIES VAE 解码器隐藏特征计算漂移，通过输入梯度把表示几何传回生成器。

限制与判断：冻结解码器权重不意味着切断输入梯度；一次生成器加一次解码器的成本须同时报告。

作者元数据备注（与独立核实分开）：9 pages, 5 figures

原始来源：[来源1](https://arxiv.org/abs/2605.24841v1)

<a id="paper-2606-07481"></a>

## Drifting Models for Surrogate Flow Modeling

作者：Chris R. Jung、Markus Dörr、Natalie Jüngling、Jennifer Niessner 等6人。标识：`2606.07481v1`。首次公开：2026-06-05；所查版本更新：2026-06-05。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在 VAE 潜空间和边界标签掩码下应用条件漂移，构建单次 CFD 流场代理。

限制与判断：特定边界与几何范围内的误差比较不保证未见几何或物理守恒；CFD 的 flow 与生成 flow matching 需区分。

作者元数据备注（与独立核实分开）：Accepted to the 2nd International Symposium AI and Fluid Mechanics 2026

原始来源：[来源1](https://arxiv.org/abs/2606.07481v1)

<a id="paper-2606-27824"></a>

## Pepti-drift: Scalable Safe-Active Peptide Generation Without Inference-Time Guidance

作者：Takashi Fujiwara、Hikaru Shindo、Kaushalya Madhawa、Jun Jin Choong 等9人。标识：`2606.27824v3`。首次公开：2026-06-26；所查版本更新：2026-10-01。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Pepti-drift 以结合活性吸引和风险区域排斥做一次潜变量细化，并强调长度匹配评价。

限制与判断：预测活性安全与真实药效不同；报告单次潜细化之外还有并行解码，速度和长度混杂必须分列。

作者元数据备注（与独立核实分开）：preprint

原始来源：[来源1](https://arxiv.org/abs/2606.27824v3)

<a id="paper-2607-02428"></a>

## Self-Auditing Residual Drifting for Pathology-Preserving Accelerated Knee MRI

作者：Qing Lyu、Jianxu Wang、Mohammad Kawas、Ge Wang 等5人。标识：`2607.02428v1`。首次公开：2026-07-02；所查版本更新：2026-07-02。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：SA-RDM-DC 联合预测图像与缺失 k-space 残差，使用数据一致性、频率漂移和同次误差估计。

限制与判断：自审计分数属于模型输出，跨协议可靠性和病理保留须独立验证；不能自动升级为可信人工金标。

原始来源：[来源1](https://arxiv.org/abs/2607.02428v1)

<a id="paper-2609-26435"></a>

## One-Step Generative Surrogate Models via Block-Triangular Joint Drifting

作者：Nicholas Geissler、Shreya Jha、Ricardo Baptista、Benjamin Peherstorfer。标识：`2609.26435v1`。首次公开：2026-09-22；所查版本更新：2026-09-22。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：用块三角联合漂移学习连续状态对的联合分布，保留当前态边缘并直接生成条件下一态。

限制与判断：单对样本下的条件建模依赖结构约束；模拟轨迹统计尚不等于复杂 RGB 事件的实例绑定。

原始来源：[来源1](https://arxiv.org/abs/2609.26435v1)

<a id="paper-2610-04819"></a>

## DriftSR: One-Step Real-World Image Super-Resolution via Distribution Drifting

作者：Wei Zhu、Kai Zhang、Yu Zheng、Zhaopeng Yang 等7人。标识：`2610.04819v1`。首次公开：2026-10-03；所查版本更新：2026-10-03。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：借助冻结扩散教师的隐藏特征实施空间特征漂移，以结构调制引导约束低质输入内容，训练单步超分辨生成器。

限制与判断：空间位置作为样本形成的分布约束仍需检查局部对应；教师特征、退化配方与结构保真均构成条件，未核读全部实验。

原始来源：[来源1](https://arxiv.org/abs/2610.04819v1)

<a id="paper-2610-29106"></a>

## DriftNeRF: Cross-Ray Density Drifting for Sparse-View Neural Radiance Fields

作者：Juntang Wang、Yihan Wang、Sheng'en Li、Hao Wu 等6人。标识：`2610.29106v1`。首次公开：2026-10-21；所查版本更新：2026-10-21。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftNeRF 用跨光线邻近点的密度共识构造停止梯度正则，约束稀疏视角 NeRF 的局部三维不一致。

限制与判断：它是辐射场训练正则，未建立从随机噪声一次生成图像的采样器；不可与原生 GMD 的 1-NFE 结果合并。

作者元数据备注（与独立核实分开）：13 pages, 6 figures, 18 tables

原始来源：[来源1](https://arxiv.org/abs/2610.29106v1)

<a id="paper-2610-38953"></a>

## Guidance-Coupled Nullspace Drifting for One-Step Medical Image Reconstruction

作者：M. Tuna Alatan、Agah Server Tapan、Şaban Öztürk、Muhammad Usama Mirza 等7人。标识：`2610.38953v1`。首次公开：2026-10-28；所查版本更新：2026-10-28。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftRecon 在成像算子零空间约束下漂移生成缺失分量，并联动引导强度和核温度。

限制与判断：测量一致性来自显式物理结构；没有对应观测算子时不能直接移植零空间保证。

原始来源：[来源1](https://arxiv.org/abs/2610.38953v1)
