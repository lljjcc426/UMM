# Drifting原理、理论与前史

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 24 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-1502-02761"></a>

## Generative Moment Matching Networks

作者：Yujia Li、Kevin Swersky、Richard Zemel。标识：`1502.02761v1`。首次公开：2015-02-10；所查版本更新：2015-02-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：GMMN 以核矩或 MMD 匹配训练直接生成器，提供无逐样本重建配对的分布学习先例。

限制与判断：核选择与高维批量估计限制仍在；其未归一化矩梯度与现代归一化漂移场不完全相同。

原始来源：[来源1](https://arxiv.org/abs/1502.02761v1)

<a id="paper-1608-04471"></a>

## Stein Variational Gradient Descent: A General Purpose Bayesian Inference Algorithm

作者：Qiang Liu、Dilin Wang。标识：`1608.04471v3`。首次公开：2016-08-16；所查版本更新：2019-09-09。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2016（官方目录）](https://neurips.cc/virtual/2016/poster/7009)

方法：SVGD 通过 score 与核排斥组合移动粒子，是样本变分推断和后续摊销对齐的重要基础。

限制与判断：它本身并非已训练的单步生成器；粒子推断、参数摊销和高维核退化问题需要区分。

作者元数据备注（与独立核实分开）：To appear in NIPS 2016

原始来源：[来源1](https://arxiv.org/abs/1608.04471v3) · [来源2](https://neurips.cc/virtual/2016/poster/7009)

<a id="paper-2304-12906"></a>

## The Score-Difference Flow for Implicit Generative Modeling

作者：Romann M. Weber。标识：`2304.12906v5`。首次公开：2023-04-25；所查版本更新：2026-05-20。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：SD-Flow 早在 2023 年研究平滑分布的 score 差运输与参数生成器，是漂移机制的重要先行研究。

限制与判断：TMLR 原文与后续更新分列；理论的密度及最优判别器条件不直接覆盖现代全部实际归一化实现。

作者元数据备注（与独立核实分开）：25 pages, 5 figures, 4 tables. Updated final version of a paper originally published in Transactions on Machine Learning Research (TMLR), including minor typographical corrections and post-publication commentary connecting the SD flow to drifting models；Transactions on Machine Learning Research (7/2023)

原始来源：[来源1](https://arxiv.org/abs/2304.12906v5) · [来源2](https://studios.disneyresearch.com/2023/08/31/the-score-difference-flow/) · [来源3](https://openreview.net/forum?id=dpGSNLUCzu)

<a id="paper-2602-04770"></a>

## Generative Modeling via Drifting

作者：Mingyang Deng、He Li、Tianhong Li、Yilun Du 等5人。标识：`2602.04770v2`。首次公开：2026-02-04；所查版本更新：2026-02-06。

阅读层级：**重点章节核读**。范围：§3.2 Eq6；§5.2 Tables1/2与特征消融；§5.3 Table7；Appendix C.1有限基条件。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/154240)

方法：以吸引真实样本、排斥生成样本的核场构造停止梯度目标，把分布演化放到训练，部署直接生成。

限制与判断：反对称性只直接给出分布相同则场为零；原附录的逆向结论依赖有限基、探针交互独立等条件。特征预训练和大参考批量仍有成本。

本轮核读所得：单步 ImageNet256 FID1.54/1.61为作者报告；参考池大小和表征显著影响质量；机器人结果并非全部优于 Diffusion Policy。

作者元数据备注（与独立核实分开）：Project page: https://lambertae.github.io/projects/drifting/

原始来源：[来源1](https://arxiv.org/abs/2602.04770v2) · [来源2](https://neurips.cc/virtual/2026/poster/154240) · [来源3](https://arxiv.org/html/2602.04770v2)

<a id="paper-2602-20463"></a>

## A Long-Short Flow-Map Perspective for Drifting Models

作者：Zhiqi Li、Bo Zhu。标识：`2602.20463v1`。首次公开：2026-02-24；所查版本更新：2026-02-24。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：用满足半群一致性的长程映射与短程终端映射重新解释漂移，并引出密度学习及保守冲量项。

限制与判断：终端区间趋零及近似阶数有明确前提；不能把流映射分解称为所有实现和优化过程完全等价。

作者元数据备注（与独立核实分开）：25 pages, 7 figures

原始来源：[来源1](https://arxiv.org/abs/2602.20463v1)

<a id="paper-2603-07514"></a>

## A Unified View of Score-Based and Drifting Models

作者：Chieh-Hsin Lai、Bac Nguyen、Naoki Murata、Yuhta Takida 等8人。标识：`2603.07514v3`。首次公开：2026-03-08；所查版本更新：2026-05-15。

阅读层级：**重点章节核读**。范围：§3.3 Theorem3及假设；§4.2 CIFAR与ImageNet诊断；§5.1 SD-flow联系；PDF第2页Fig1视觉核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Gaussian 核的总体均值位移精确对应平滑 score 差；一般径向核分解为预条件 score 项与残差。

限制与判断：Laplace 的高维近似依赖壳集中、内积和矩条件；有限池、双轴归一化及特征空间实现另有偏差项。

本轮核读所得：Gaussian总体归一化均值位移等于平滑score差乘方差；一般径向核保留残差，Laplace近似另需集中条件。

原始来源：[来源1](https://arxiv.org/abs/2603.07514v3) · [来源2](https://arxiv.org/html/2603.07514v3)

<a id="paper-2603-09936"></a>

## Generative Drifting is Secretly Score Matching: a Spectral and Variational Perspective

作者：Erkan Turan、Nicolas Dufour、Maks Ovsjanikov。标识：`2603.09936v2`。首次公开：2026-03-10；所查版本更新：2026-05-29。

阅读层级：**重点章节核读**。范围：§5.6冻结场理想拟合命题；§6线性化谱速率、退火与ImageNet消融；Appendix D.4仅核读证明路线。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：从谱与变分角度研究 Gaussian 漂移、频率收敛瓶颈和带宽退火，并连接冻结场回归与 JKO 近似。

限制与判断：谱速率有线性化设定；完美拟合冻结目标与一次 SGD 更新有差距，不能推出实际大网络全局收敛。

本轮核读所得：score联系不等于所有核和有限批量实现精确等价；8.36的退火结果属于该文受控消融。

原始来源：[来源1](https://arxiv.org/abs/2603.09936v2) · [来源2](https://arxiv.org/html/2603.09936v2)

<a id="paper-2603-10592"></a>

## Gradient Flow Drifting: Generative Modeling via Wasserstein Gradient Flows of KDE-Approximated Divergences

作者：Jiarui Cao、Zixuan Wei、Yuxin Liu。标识：`2603.10592v1`。首次公开：2026-03-11；所查版本更新：2026-03-11。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：以 KDE 近似散度的 Wasserstein 梯度流组织漂移，探讨 KL、χ² 混合与流形扩展。

限制与判断：主要为框架与合成实验；Gaussian score 恒等式的条件、散度方向和实际归一化须分别核对。

原始来源：[来源1](https://arxiv.org/abs/2603.10592v1)

<a id="paper-2603-12366"></a>

## Sinkhorn-Drifting Generative Models

作者：Ping He、Om Khangaonkar、Hamed Pirsiavash、Yikun Bai 等5人。标识：`2603.12366v2`。首次公开：2026-03-12；所查版本更新：2026-03-26。

阅读层级：**重点章节核读**。范围：§3.4 Propositions3.7–3.11与有限粒子开放问题；§4成本；§5.1温度扫描。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：以双边 Sinkhorn 缩放替换局部归一化，通过交叉运输减自运输构造场，研究温度稳定性。

限制与判断：正文区分光滑正密度总体结论和有限粒子结论；正则化且粒子数至少三时的通用零粒子场可辨识性仍未解决。

本轮核读所得：连续正密度情形的可辨识结论有条件；n≥3有限正则经验测度的零场逆向结论仍未解决。

原始来源：[来源1](https://arxiv.org/abs/2603.12366v2) · [来源2](https://arxiv.org/html/2603.12366v2)

<a id="paper-2603-25182"></a>

## Learning Monge maps with constrained drifting models

作者：Théo Dumont、Théo Lacombe、François-Xavier Vialard。标识：`2603.25182v3`。首次公开：2026-03-26；所查版本更新：2026-04-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在最优运输映射的凸约束集合上定义散度梯度流，以凸性受限网络和自然梯度近似 Monge 映射。

限制与判断：目标对数凹及相应凸性条件限制定理范围；任意复杂图像分布和普通生成器不直接满足。

原始来源：[来源1](https://arxiv.org/abs/2603.25182v3)

<a id="paper-2604-06333"></a>

## Drifting Fields are not Conservative

作者：Leonard T. Franz、Sebastian Hoffmann、Tim Weiland、Bernhard Schölkopf 等5人。标识：`2604.06333v3`。首次公开：2026-04-07；所查版本更新：2026-05-08。

阅读层级：**重点章节核读**。范围：§3.1至§4场与归一化公式、Propositions6/7及引言；未全面复核ImageNet实验。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/155051)

方法：指出位置相关归一化通常产生非保守位移场，Gaussian 为径向核中的例外；sharp 归一化恢复势函数。

限制与判断：非保守性、零场可辨识性和训练收敛属于不同命题；新归一化的实验可比性不能充当原实现的统一收敛证明。

本轮核读所得：标准归一化漂移场一般非保守；该性质不能单独推出分布不可辨识。

原始来源：[来源1](https://arxiv.org/abs/2604.06333v3) · [来源2](https://neurips.cc/virtual/2026/poster/155051) · [来源3](https://arxiv.org/html/2604.06333v3)

<a id="paper-2604-24196"></a>

## Identifiability and Stability of Generative Drifting in the Companion-Elliptic Kernel Family

作者：HakGeun Lee、Hyonho Chun。标识：`2604.24196v4`。首次公开：2026-04-27；所查版本更新：2026-08-13。

阅读层级：**重点章节核读**。范围：Theorem3.7证明；Counterexample4.1证明；Theorems4.5/4.8/4.10陈述及4.10证明。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在含 Laplace 的 companion-elliptic 核类证明总体零场可辨识，并研究局部残差、尾质量和反卷积稳定性。

限制与判断：局部小场无法排除质量逃逸；定量界含尾项，Matérn 另需导数残差。该定理没有保证有限批量网络训练到达零场。

本轮核读所得：总体全空间零场可辨识，与质量逃逸下局部小场失效同时成立；Gaussian反卷积和Matérn稳定性条件不同。

作者元数据备注（与独立核实分开）：40 pages, 0 figures

原始来源：[来源1](https://arxiv.org/abs/2604.24196v4) · [来源2](https://arxiv.org/html/2604.24196v4)

<a id="paper-2604-27239"></a>

## Analytical Correction for Subsampling Bias in Drifting Models

作者：Jiaru Zhang、Zeyun Deng、Juanwu Lu、Ziran Wang 等5人。标识：`2604.27239v1`。首次公开：2026-04-29；所查版本更新：2026-04-29。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验；另核读§4.1构造、Theorem4.1及凸包讨论。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/155602)

方法：分析 softmax 自归一化质心的有限样本偏差，给出利用批内统计的 ABC 修正。

限制与判断：O(1/n) 到 O(1/n²) 的结论依赖权重、矩和相应估计条件；不能宣称消除所有高维估计与优化误差。

片段定位：本地HTML提取文本起始行 68, 75, 78；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2604.27239v1) · [来源2](https://neurips.cc/virtual/2026/poster/155602) · [来源3](https://arxiv.org/html/2604.27239)

<a id="paper-2605-05118"></a>

## On the Wasserstein Gradient Flow Interpretation of Drifting Models

作者：Arthur Gretton、Li Kevin Wenliang、Alexandre Galashov、James Thornton 等6人。标识：`2605.05118v2`。首次公开：2026-05-06；所查版本更新：2026-05-21。

阅读层级：**重点章节核读**。范围：§3.1 Algorithm1对照；§3.2 Proposition2与Theorem3有限加权测度条件；Appendix B.5仅核读陈述。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：区分原论文概念算法的 KDE-score 场与实际双轴权重算法，并构造更接近 Sinkhorn 的代理。

限制与判断：代理的 Gaussian 总体一致性要求加权测度有限；作者明确指出代理通常也不是真正的 Wasserstein 梯度流。

本轮核读所得：需逐项区分论文定义的KDE散度梯度流与原始启发式漂移场；有限测度结论不可泛化成任意SGD全局收敛。

原始来源：[来源1](https://arxiv.org/abs/2605.05118v2) · [来源2](https://arxiv.org/html/2605.05118v2)

<a id="paper-2605-10727"></a>

## Kernel-Gradient Drifting Models

作者：Maria Esteban-Casadevall、Jorge Carrasco-Pollo、Max Welling、Jan-Willem van de Meent 等6人。标识：`2605.10727v1`。首次公开：2026-05-11；所查版本更新：2026-05-11。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/151352)

方法：以核本身的梯度代替固定欧氏位移，得到一般核的平滑 score 差，并扩展到流形与概率单纯形。

限制与判断：这是修改后的场；characteristic 核及相应正则性结论不能直接套到原 Laplace 位移场和离散大语言模型。

原始来源：[来源1](https://arxiv.org/abs/2605.10727v1) · [来源2](https://neurips.cc/virtual/2026/poster/151352)

<a id="paper-2605-11755"></a>

## One-Step Generative Modeling via Wasserstein Gradient Flows

作者：Jiaqi Han、Puheng Li、Qiushan Guo、Renyuan Xu 等6人。标识：`2605.11755v2`。首次公开：2026-05-12；所查版本更新：2026-05-26。

阅读层级：**重点章节核读**。范围：§3.3 Theorem3.1；Appendix B.1假设、B.3有界支持局部化；作者项目页方法与结果；未逐行验算全证明。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：W-Flow 用 Sinkhorn 能量的 Wasserstein 场训练单步运输生成器，交叉运输减独立批次自运输改善分布覆盖。

限制与判断：有限粒子向总体动力学逼近的定理在有限时间、正则性和相应有界支持下成立；不等于有限 SGD 达到全局数据分布。

本轮核读所得：有限粒子小步长在有限时间逼近总体PDE，受Lipschitz、增长及Sinkhorn局部化条件限制。

作者元数据备注（与独立核实分开）：40 pages, 14 figures

原始来源：[来源1](https://arxiv.org/abs/2605.11755v2) · [来源2](https://arxiv.org/html/2605.11755v2)

<a id="paper-2605-22795"></a>

## Finite-Particle Convergence Rates for Conservative and Non-Conservative Drifting Models

作者：Krishnakumar Balasubramanian。标识：`2605.22795v3`。首次公开：2026-05-21；所查版本更新：2026-09-21。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：研究保守和原 Laplace 场的有限粒子熵耗散、局部占据与残差速率，显式保留带宽依赖。

限制与判断：逆 KDE 矩可在缩带宽下发散；所述 N 的速率依赖均匀正则性、求积及尺度对齐，维数代价明显。

片段定位：本地HTML提取文本起始行 85, 103, 104；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2605.22795v3) · [来源2](https://arxiv.org/html/2605.22795)

<a id="paper-2608-01547"></a>

## Finite-Probe Total-Variation Certificates for Finite-Basis Drifting Models

作者：Sam Andersson、Ricky Molén。标识：`2608.01547v1`。首次公开：2026-08-03；所查版本更新：2026-08-03。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在声明的有限密度基中，利用独立探针的未归一化场分子和可观测性边际构造 TV 条件证书。

限制与判断：需独立噪声界、算子误差与外部残差半径；退化时弃判。不能从任意训练小损失给出通用分布证书。

作者元数据备注（与独立核实分开）：39 pages, 8 figures. Reproducibility code and numerical outputs: https://github.com/SamAndersson-C/finite-drift-certification

原始来源：[来源1](https://arxiv.org/abs/2608.01547v1)

<a id="paper-2609-15193"></a>

## Convergence rates for generative drifting flows: fixed-scale obstructions and multihead acceleration

作者：Arthur Stéphanovitch、Eddie Aamari。标识：`2609.15193v2`。首次公开：2026-09-14；所查版本更新：2026-10-13。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：研究理想漂移动力学的固定尺度障碍，以连续多尺度头改善参考分布附近的收敛率。

限制与判断：指数收敛位于规定参考分布的邻域与理想条件；有限数据、有限尺度、网络拟合和真实图像训练另待验证。

原始来源：[来源1](https://arxiv.org/abs/2609.15193v2)

<a id="paper-2609-32708"></a>

## One-Step Generative Modeling via Unbalanced Optimal Transport

作者：Yirong Shen、Mengfei Xia、Junpeng Jing、Lu Gan 等5人。标识：`2609.32708v1`。首次公开：2026-09-26；所查版本更新：2026-09-26。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：UOT-GF 保持生成侧边缘固定，只松弛真实侧质量，以缓解有限批次的强制匹配偏差。

限制与判断：与双侧松弛存在不同目标和失配风险；报告同配置改进也不证明所有不平衡任务上都优于平衡运输。

原始来源：[来源1](https://arxiv.org/abs/2609.32708v1)

<a id="paper-2610-01355"></a>

## Discrete Wasserstein Flows for One-Step Generative Modeling

作者：Alessandro Micheli、Andrea Zerio、Samir Bhatt。标识：`2610.01355v1`。首次公开：2026-10-01；所查版本更新：2026-10-01。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在离散状态空间以概率流与占据权重学习单步采样器，连接离散 Wasserstein 演化。

限制与判断：主要是有限状态可控设定；不能据此宣称已解决大词表文本生成或长序列语义一致性。

原始来源：[来源1](https://arxiv.org/abs/2610.01355v1)

<a id="paper-2610-04454"></a>

## One-Step Generation via Riemannian Wasserstein Gradient Flows

作者：David Li、Chanhyuk Lee、Jaehoon Yoo、Nikita Gushchin 等10人。标识：`2610.04454v1`。首次公开：2026-10-03；所查版本更新：2026-10-03。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在共同训练框架下比较多个几何感知 Wasserstein 场，避免加性欧氏更新越出约束空间。

限制与判断：不同任务的最佳场不同；尚无一个能量对全部几何和数据域普遍最优的证据。

原始来源：[来源1](https://arxiv.org/abs/2610.04454v1)

<a id="paper-2610-18552"></a>

## Unbalanced W-Flow: Unbalanced Wasserstein Drifting under Finite-Batch Marginal Fluctuations

作者：Jongwook Jeon、Mingue Park、Jiwon Choi、Jaihoon Kim 等6人。标识：`2610.18552v1`。首次公开：2026-10-13；所查版本更新：2026-10-13。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：UW-Flow 从去偏不平衡 Sinkhorn 能量推导漂移，分析批次质量波动与模态间隔对速度误差的影响。

限制与判断：与仅松弛真实侧的 UOT-GF 为不同论文；需注明质量松弛参数、平衡极限及可辨识假设。

作者元数据备注（与独立核实分开）：31 pages, 9 figures, 9 tables

原始来源：[来源1](https://arxiv.org/abs/2610.18552v1)

<a id="paper-pmlr-v306-ouyang26c"></a>

## Primal-Spectral Generative Modeling: Fast Analytical Generation via Pseudoinverse Lévy Inversion

作者：Zhiyuan Ouyang、Simei Huang、Zuokai Wen、Xiangyun Zhang 等5人。标识：`pmlr-v306-ouyang26c`。首次公开：2026；所查版本更新：未提供。

阅读层级：**摘要筛选**。范围：正式PMLR摘要筛选；未核读正文。

来源归属：[ICML 2026（正式论文集）](https://proceedings.mlr.press/v306/ouyang26c.html)

方法：以可学习谱密度与伪逆Lévy反演连接原始域和谱域，构建PriSpecNet/PiLI的一步解析生成路线。

限制与判断：仅核读正式摘要；ImageNet256 FID1.66及26GFLOPs为作者报告，反演正则、数据和完整模型成本尚未逐项复核。

原始来源：[来源1](https://proceedings.mlr.press/v306/ouyang26c.html)
