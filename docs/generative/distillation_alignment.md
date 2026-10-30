# 蒸馏、分布匹配与偏好对齐

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 11 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2202-00512"></a>

## Progressive Distillation for Fast Sampling of Diffusion Models

作者：Tim Salimans、Jonathan Ho。标识：`2202.00512v2`。首次公开：2022-02-01；所查版本更新：2022-06-07。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2022（官方目录）](https://iclr.cc/virtual/2022/poster/6537)

方法：Progressive Distillation 逐次将教师的两步确定性采样映射压为一步，逐级缩短部署链。

限制与判断：每一级蒸馏和教师生成都有训练成本；压缩轨迹映射并不保证保留全部模式或过程语义。

作者元数据备注（与独立核实分开）：Published as a conference paper at ICLR 2022

原始来源：[来源1](https://arxiv.org/abs/2202.00512v2) · [来源2](https://iclr.cc/virtual/2022/poster/6537)

<a id="paper-2311-17042"></a>

## Adversarial Diffusion Distillation

作者：Axel Sauer、Dominik Lorenz、Andreas Blattmann、Robin Rombach。标识：`2311.17042v1`。首次公开：2023-11-28；所查版本更新：2023-11-28。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：ADD 将扩散教师蒸馏与对抗目标结合，实现一到少步高分辨率图像生成。

限制与判断：判别器特征、教师、真实数据及优化稳定性都属于依赖；不能与无教师原生方法只按步数比较。

原始来源：[来源1](https://arxiv.org/abs/2311.17042v1)

<a id="paper-2311-18828"></a>

## One-step Diffusion with Distribution Matching Distillation

作者：Tianwei Yin、Michaël Gharbi、Richard Zhang、Eli Shechtman 等7人。标识：`2311.18828v4`。首次公开：2023-11-30；所查版本更新：2024-10-04。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DMD 以教师和学生分布的 score 差训练单步学生，并用配对回归稳定早期学习。

限制与判断：教师 score 与持续拟合的 fake score 都有误差；原版配对噪声图像集包含多步教师成本。

片段定位：本地HTML提取文本起始行 81, 83, 93；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：CVPR 2024, Project page: https://tianweiy.github.io/dmd/；Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2024

原始来源：[来源1](https://arxiv.org/abs/2311.18828v4) · [来源2](https://arxiv.org/html/2311.18828)

<a id="paper-2403-12015"></a>

## Fast High-Resolution Image Synthesis with Latent Adversarial Diffusion Distillation

作者：Axel Sauer、Frederic Boesel、Tim Dockhorn、Andreas Blattmann 等6人。标识：`2403.12015v1`。首次公开：2024-03-18；所查版本更新：2024-03-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：LADD 把对抗蒸馏放到潜扩散特征中，用于 SD3-Turbo 等少步高分辨率生成。

限制与判断：减少像素级判别开销仍需教师表示和对抗训练；4步无引导与1步性能应明确分列。

原始来源：[来源1](https://arxiv.org/abs/2403.12015v1)

<a id="paper-2404-04057"></a>

## Score identity Distillation: Exponentially Fast Distillation of Pretrained Diffusion Models for One-Step Generation

作者：Mingyuan Zhou、Huangjie Zheng、Zhendong Wang、Mingzhang Yin 等5人。标识：`2404.04057v3`。首次公开：2024-04-05；所查版本更新：2024-05-24。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICML 2024（官方目录）](https://icml.cc/virtual/2024/poster/34068)

方法：SiD 利用 score 恒等式以自身合成样本蒸馏预训练扩散，无需真实训练集或多步教师配对数据。

限制与判断：data-free 描述蒸馏阶段，教师仍已学习数据；辅助 score 拟合和训练成本不因无真实样本而消失。

作者元数据备注（与独立核实分开）：ICML 2024, PyTorch implementation: https://github.com/mingyuanzhou/SiD

原始来源：[来源1](https://arxiv.org/abs/2404.04057v3) · [来源2](https://icml.cc/virtual/2024/poster/34068)

<a id="paper-2405-14867"></a>

## Improved Distribution Matching Distillation for Fast Image Synthesis

作者：Tianwei Yin、Michaël Gharbi、Taesung Park、Richard Zhang 等7人。标识：`2405.14867v2`。首次公开：2024-05-23；所查版本更新：2024-05-24。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[NeurIPS 2024（正式论文集）](https://papers.nips.cc/paper_files/paper/2024/hash/54dcf25318f9de5a7a01f0a4125c541e-Abstract-Conference.html)

方法：DMD2 去除原版配对回归，采用快慢更新的 fake critic、真实数据对抗损失和推理分布模拟。

限制与判断：减少配对数据构建仍保留教师、辅助网络和真实数据；ImageNet-64 与 256 的 FID 不直接比较。

片段定位：本地HTML提取文本起始行 97, 102, 110；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Code, model, and dataset are available at https://tianweiy.github.io/dmd2

原始来源：[来源1](https://arxiv.org/abs/2405.14867v2) · [来源2](https://papers.nips.cc/paper_files/paper/2024/hash/54dcf25318f9de5a7a01f0a4125c541e-Abstract-Conference.html) · [来源3](https://arxiv.org/html/2405.14867)

<a id="paper-2605-07327"></a>

## Teacher-Feature Drifting: One-Step Diffusion Distillation with Pretrained Diffusion Representations

作者：Yuan Zhang、Chenyi Li、Haodong Yu、Guoqing Ma 等11人。标识：`2605.07327v2`。首次公开：2026-05-08；所查版本更新：2026-08-07。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Teacher-Feature Drifting 直接用扩散教师隐藏特征计算漂移，并加覆盖约束，减少额外表征网络。

限制与判断：仍依赖预训练教师及其特征计算；ImageNet-64 的 FID 与原论文 ImageNet-256 不可直接排总榜。

片段定位：本地HTML提取文本起始行 92, 114, 121；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2605.07327v2) · [来源2](https://arxiv.org/html/2605.07327)

<a id="paper-2605-26552"></a>

## Aligning Few-Step Generative Models by Amortizing Sample-based Variational Inference

作者：Jaewoo Lee、Hyeongyu Kang、Dohyun Kim、Kyuil Sim 等12人。标识：`2605.26552v2`。首次公开：2026-05-26；所查版本更新：2026-05-27。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：FAV 把参考分布上的奖励倾斜写成样本变分推断，以 SVGD 粒子更新和固定点回归适配多类少步生成器。

限制与判断：需要明确参考采样、奖励评价与特征选择成本；模型无似然要求不等于没有分布假设。

作者元数据备注（与独立核实分开）：Under review

原始来源：[来源1](https://arxiv.org/abs/2605.26552v2)

<a id="paper-2606-02521"></a>

## Drifting Preference Optimization for One-Step Generative Models

作者：Zhou Jiang、Yandong Wen、Zhen Liu。标识：`2606.02521v3`。首次公开：2026-06-01；所查版本更新：2026-06-03。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DrPO 用黑箱奖励排序正负候选，以偏好偶极场加参考漂移形成停止梯度更新，保持单步部署。

限制与判断：省去奖励反传不等于省去奖励查询和候选生成；目标奖励的提升仍可能伴随偏好过拟合。

片段定位：本地HTML提取文本起始行 35, 53, 65；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：24 pages, 9 figures

原始来源：[来源1](https://arxiv.org/abs/2606.02521v3) · [来源2](https://arxiv.org/html/2606.02521)

<a id="paper-2606-15553"></a>

## Distilling Drifting Transformers with Representation Autoencoders

作者：Jiawei Zhang、Mengfei Xia、Gen Li、Yuantao Gu。标识：`2606.15553v2`。首次公开：2026-06-14；所查版本更新：2026-08-03。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Drift-RAE 以语义丰富的 RAE 表示做漂移蒸馏，研究各向异性潜空间和引导设计。

限制与判断：报告短程蒸馏成本不含完整教师和 RAE 预训练；ImageNet 结果尚不能保证汉字细笔重建与过程正确。

片段定位：本地HTML提取文本起始行 96, 100, 133；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2606.15553v2) · [来源2](https://arxiv.org/html/2606.15553)

<a id="paper-2610-02188"></a>

## DMAD: Distribution Matching as Adversarial Distillation for Fast Visual Generation

作者：Zhengming Yu、Junkun Yuan、Haotian Yang、Gordon Guocheng Qian 等11人。标识：`2610.02188v2`。首次公开：2026-10-01；所查版本更新：2026-10-13。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DMAD 以共享骨干上的真假分类头估计密度比，将 DMD 的 score 分布匹配改写为对抗蒸馏。

限制与判断：等价梯度依赖判别器最优等条件；真实数据、教师样本和大骨干训练仍有成本，视频榜单不证明过程正确。

作者元数据备注（与独立核实分开）：28 pages, 15 figures. Project page: https://yzmblog.github.io/projects/DMAD

原始来源：[来源1](https://arxiv.org/abs/2610.02188v2)
