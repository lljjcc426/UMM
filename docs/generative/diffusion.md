# 扩散、score与采样

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 10 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-1503-03585"></a>

## Deep Unsupervised Learning using Nonequilibrium Thermodynamics

作者：Jascha Sohl-Dickstein、Eric A. Weiss、Niru Maheswaranathan、Surya Ganguli。标识：`1503.03585v8`。首次公开：2015-03-12；所查版本更新：2015-11-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICML 2015（正式论文集）](https://proceedings.mlr.press/v37/sohl-dickstein15.html)

方法：以逐步扰动与可学习逆过程建立扩散概率生成框架，把非平衡过程连接到可计算学习目标。

限制与判断：奠定形式框架，不能把后续现代图像质量、Transformer 扩展或少步能力归给该早期实验。

原始来源：[来源1](https://arxiv.org/abs/1503.03585v8) · [来源2](https://proceedings.mlr.press/v37/sohl-dickstein15.html)

<a id="paper-1907-05600"></a>

## Generative Modeling by Estimating Gradients of the Data Distribution

作者：Yang Song、Stefano Ermon。标识：`1907.05600v3`。首次公开：2019-07-12；所查版本更新：2020-10-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2019（官方目录）](https://neurips.cc/virtual/2019/poster/13242)

方法：用多噪声水平的 denoising score matching 学习 score，再以退火 Langevin 动力学生成。

限制与判断：多尺度 score 估计与采样链质量均重要；它是 DDPM 之前的关键支线，采样成本应包含各噪声水平的多次更新。

作者元数据备注（与独立核实分开）：NeurIPS 2019 (Oral)

原始来源：[来源1](https://arxiv.org/abs/1907.05600v3) · [来源2](https://neurips.cc/virtual/2019/poster/13242)

<a id="paper-2010-02502"></a>

## Denoising Diffusion Implicit Models

作者：Jiaming Song、Chenlin Meng、Stefano Ermon。标识：`2010.02502v4`。首次公开：2020-10-06；所查版本更新：2022-10-05。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2021（官方目录）](https://iclr.cc/virtual/2021/poster/2804)

方法：DDIM 保持训练边缘的同时改变非马尔可夫生成过程，支持确定性路径和跳步采样。

限制与判断：确定性不代表任意大步都准确；同一训练目标可配不同采样器，不能据采样方式反推训练范式。

作者元数据备注（与独立核实分开）：ICLR 2021; updated connections with ODEs at page 6, fixed some typos in the proof

原始来源：[来源1](https://arxiv.org/abs/2010.02502v4) · [来源2](https://iclr.cc/virtual/2021/poster/2804)

<a id="paper-2102-09672"></a>

## Improved Denoising Diffusion Probabilistic Models

作者：Alex Nichol、Prafulla Dhariwal。标识：`2102.09672v1`。首次公开：2021-02-18；所查版本更新：2021-02-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICML 2021（官方目录）](https://icml.cc/virtual/2021/poster/9531)

方法：Improved DDPM 研究方差学习、混合目标与噪声调度，以改善似然和减少采样步。

限制与判断：少步收益依赖具体方差参数化与训练设定；似然改善和感知质量不能相互替代。

原始来源：[来源1](https://arxiv.org/abs/2102.09672v1) · [来源2](https://icml.cc/virtual/2021/poster/9531)

<a id="paper-2105-05233"></a>

## Diffusion Models Beat GANs on Image Synthesis

作者：Prafulla Dhariwal、Alex Nichol。标识：`2105.05233v4`。首次公开：2021-05-11；所查版本更新：2021-06-01。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2021（官方目录）](https://neurips.cc/virtual/2021/poster/28362)

方法：ADM 系统改进扩散网络与训练，并用分类器梯度引导图像质量和覆盖的权衡。

限制与判断：分类器预训练、引导计算和数据权限需计入，FID 改善可能伴随召回下降。

作者元数据备注（与独立核实分开）：Added compute requirements, ImageNet 256$\times$256 upsampling FID and samples, DDIM guided sampler, fixed typos

原始来源：[来源1](https://arxiv.org/abs/2105.05233v4) · [来源2](https://neurips.cc/virtual/2021/poster/28362)

<a id="paper-2107-00630"></a>

## Variational Diffusion Models

作者：Diederik P. Kingma、Tim Salimans、Ben Poole、Jonathan Ho。标识：`2107.00630v6`。首次公开：2021-07-01；所查版本更新：2023-04-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2021（官方目录）](https://neurips.cc/virtual/2021/poster/27712)

方法：VDM 以连续时间变分界组织扩散，并研究信噪比参数化、调度学习和密度建模。

限制与判断：变分似然目标和有限步生成误差属于不同评价；连续时间的理论等价依赖具体参数化。

作者元数据备注（与独立核实分开）：Published at NeurIPS'21

原始来源：[来源1](https://arxiv.org/abs/2107.00630v6) · [来源2](https://neurips.cc/virtual/2021/poster/27712)

<a id="paper-2107-03006"></a>

## Structured Denoising Diffusion Models in Discrete State-Spaces

作者：Jacob Austin、Daniel D. Johnson、Jonathan Ho、Daniel Tarlow 等5人。标识：`2107.03006v3`。首次公开：2021-07-07；所查版本更新：2023-02-22。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2021（官方目录）](https://neurips.cc/virtual/2021/poster/27623)

方法：D3PM 将扩散扩展到离散状态，用结构化转移矩阵和辅助交叉熵建模序列及图像。

限制与判断：离散跃迁与连续 Gaussian 加噪的生成空间不同；矩阵结构、词表规模与步数共同决定成本。

作者元数据备注（与独立核实分开）：10 pages plus references and appendices. First two authors contributed equally

原始来源：[来源1](https://arxiv.org/abs/2107.03006v3) · [来源2](https://neurips.cc/virtual/2021/poster/27623)

<a id="paper-2211-01095"></a>

## DPM-Solver++: Fast Solver for Guided Sampling of Diffusion Probabilistic Models

作者：Cheng Lu、Yuhao Zhou、Fan Bao、Jianfei Chen 等6人。标识：`2211.01095v3`。首次公开：2022-11-02；所查版本更新：2025-05-19。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DPM-Solver++ 面向引导采样，用数据预测形式与多步高阶积分提高少步稳定性。

限制与判断：属于采样器设计，仍使用预训练多步模型；强引导、阶数和 NFE 的对照需要同一底座。

作者元数据备注（与独立核实分开）：Machine Intelligence Research

原始来源：[来源1](https://arxiv.org/abs/2211.01095v3)

<a id="paper-2501-09732"></a>

## Inference-Time Scaling for Diffusion Models beyond Scaling Denoising Steps

作者：Nanye Ma、Shangyuan Tong、Haolin Jia、Hexiang Hu 等11人。标识：`2501.09732v1`。首次公开：2025-01-16；所查版本更新：2025-01-16。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[CVPR 2025（正式论文集）](https://openaccess.thecvf.com/content/CVPR2025/papers/Ma_Scaling_Inference_Time_Compute_for_Diffusion_Models_CVPR_2025_paper.pdf)

方法：除增加去噪步数外，通过 verifier 和搜索寻找更好的初始噪声，研究扩散推理时计算扩展。

限制与判断：正式 CVPR 题名与 arXiv 题名不同；搜索候选数、奖励调用和选择偏差须计入，不能只报单候选 NFE。

原始来源：[来源1](https://arxiv.org/abs/2501.09732v1) · [来源2](https://openaccess.thecvf.com/content/CVPR2025/papers/Ma_Scaling_Inference_Time_Compute_for_Diffusion_Models_CVPR_2025_paper.pdf)

<a id="paper-2603-17671"></a>

## Few-Step Diffusion Sampling Through Instance-Aware Discretizations

作者：Liangyu Yuan、Ruoyu Wang、Tong Zhao、Dingwen Fu 等7人。标识：`2603.17671v1`。首次公开：2026-03-18；所查版本更新：2026-03-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[CVPR 2026（正式论文集）](https://openaccess.thecvf.com/content/CVPR2026/papers/Yuan_Few-Step_Diffusion_Sampling_Through_Instance-Aware_Discretizations_CVPR_2026_paper.pdf)

方法：学习由输入先验决定的实例自适应时间离散，为不同扩散或 flow 轨迹分配不同积分步。

限制与判断：存在离散策略调优成本；按样本自适应可能改变推理预算分布，比较应报告完整开销。

作者元数据备注（与独立核实分开）：24 pages, 20 figures. code: https://github.com/851695e35/INDIS

原始来源：[来源1](https://arxiv.org/abs/2603.17671v1) · [来源2](https://openaccess.thecvf.com/content/CVPR2026/papers/Yuan_Few-Step_Diffusion_Sampling_Through_Instance-Aware_Discretizations_CVPR_2026_paper.pdf)
