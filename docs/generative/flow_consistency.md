# Flow Matching、Rectified Flow、Consistency与Flow Map

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 27 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2302-00482"></a>

## Improving and generalizing flow-based generative models with minibatch optimal transport

作者：Alexander Tong、Kilian Fatras、Nikolay Malkin、Guillaume Huguet 等8人。标识：`2302.00482v4`。首次公开：2023-02-01；所查版本更新：2024-03-11。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：以小批量最优运输耦合改善条件 flow matching，统一处理噪声到数据路径的配对方式。

限制与判断：批内最优不等于总体最优运输；批大小和匹配开销是轨迹直度、质量与效率的共同变量。

作者元数据备注（与独立核实分开）：TMLR. Code: https://github.com/atong01/conditional-flow-matching

原始来源：[来源1](https://arxiv.org/abs/2302.00482v4)

<a id="paper-2303-08797"></a>

## Stochastic Interpolants: A Unifying Framework for Flows and Diffusions

作者：Michael S. Albergo、Nicholas M. Boffi、Eric Vanden-Eijnden。标识：`2303.08797v4`。首次公开：2023-03-15；所查版本更新：2025-10-09。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Stochastic Interpolants 用连接端点的随机插值组织速度和 score 回归，统一 ODE 与 SDE 生成。

限制与判断：统一框架不代表所有目标、数值误差和训练成本相同；不同噪声项与耦合仍形成不同算法。

作者元数据备注（与独立核实分开）：JMLR Version

原始来源：[来源1](https://arxiv.org/abs/2303.08797v4)

<a id="paper-2309-06380"></a>

## InstaFlow: One Step is Enough for High-Quality Diffusion-Based Text-to-Image Generation

作者：Xingchao Liu、Xiwen Zhang、Jianzhu Ma、Jian Peng 等5人。标识：`2309.06380v2`。首次公开：2023-09-12；所查版本更新：2024-03-23。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/19575)

方法：InstaFlow 用 reflow 改善噪声到图像耦合，再把 Stable Diffusion 运输压成一步文生图。

限制与判断：耦合再生成、教师与大规模训练成本应合计；旧 COCO 子集和后续 COCO 全量指标不可直接排名。

作者元数据备注（与独立核实分开）：ICLR 2024

原始来源：[来源1](https://arxiv.org/abs/2309.06380v2) · [来源2](https://iclr.cc/virtual/2024/poster/19575)

<a id="paper-2310-02279"></a>

## Consistency Trajectory Models: Learning Probability Flow ODE Trajectory of Diffusion

作者：Dongjun Kim、Chieh-Hsin Lai、Wei-Hsiang Liao、Naoki Murata 等9人。标识：`2310.02279v3`。首次公开：2023-10-01；所查版本更新：2024-03-30。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/17404)

方法：CTM 学习概率流 ODE 的任意时间间映射，结合轨迹一致性、蒸馏和感知目标。

限制与判断：任意时间跳转依赖对应训练；附加判别或感知组件的效果不能统一归于一致性条件本身。

作者元数据备注（与独立核实分开）：International Conference on Learning Representations

原始来源：[来源1](https://arxiv.org/abs/2310.02279v3) · [来源2](https://iclr.cc/virtual/2024/poster/17404)

<a id="paper-2310-04378"></a>

## Latent Consistency Models: Synthesizing High-Resolution Images with Few-Step Inference

作者：Simian Luo、Yiqin Tan、Longbo Huang、Jian Li 等5人。标识：`2310.04378v1`。首次公开：2023-10-06；所查版本更新：2023-10-06。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：LCM 在潜空间直接预测带引导概率流 ODE 的解，将预训练文生图蒸馏为少步模型。

限制与判断：前置 LDM、蒸馏与解码器均为依赖；2到4步主要设置不能概括为所有任务一步高质量。

原始来源：[来源1](https://arxiv.org/abs/2310.04378v1)

<a id="paper-2310-14189"></a>

## Improved Techniques for Training Consistency Models

作者：Yang Song、Prafulla Dhariwal。标识：`2310.14189v1`。首次公开：2023-10-22；所查版本更新：2023-10-22。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/18479)

方法：改进一致性训练的噪声离散、损失、时间采样与参数设计，提高从零学习少步生成的稳定性。

限制与判断：少步模型的训练资源不可由推理 NFE 推断；具体离散计划与网络缩放应随版本保留。

原始来源：[来源1](https://arxiv.org/abs/2310.14189v1) · [来源2](https://iclr.cc/virtual/2024/poster/18479)

<a id="paper-2311-01462"></a>

## Idempotent Generative Network

作者：Assaf Shocher、Amil Dravid、Yossi Gandelsman、Inbar Mosseri 等6人。标识：`2311.01462v1`。首次公开：2023-11-02；所查版本更新：2023-11-02。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/18455)

方法：IGN 同时约束真实样本重建和 f(f(z))=f(z) 幂等性，学习一次投影式生成。

限制与判断：幂等固定点集合与分布权重匹配不同；理想条件的收敛不能省略支持、损失与优化假设。

原始来源：[来源1](https://arxiv.org/abs/2311.01462v1) · [来源2](https://iclr.cc/virtual/2024/poster/18455)

<a id="paper-2311-05556"></a>

## LCM-LoRA: A Universal Stable-Diffusion Acceleration Module

作者：Simian Luo、Yiqin Tan、Suraj Patil、Daniel Gu 等9人。标识：`2311.05556v1`。首次公开：2023-11-09；所查版本更新：2023-11-09。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：LCM-LoRA 用低秩一致性蒸馏得到可与兼容微调模型组合的少步加速模块。

限制与判断：跨底座和任意 LoRA 的普适性不能超出测试范围；合并后仍需检验条件、风格与细节保持。

作者元数据备注（与独立核实分开）：Technical Report

原始来源：[来源1](https://arxiv.org/abs/2311.05556v1)

<a id="paper-2402-19159"></a>

## Trajectory Consistency Distillation: Improved Latent Consistency Distillation by Semi-Linear Consistency Function with Trajectory Mapping

作者：Jianbin Zheng、Minghui Hu、Zhongyi Fan、Chaoyue Wang 等7人。标识：`2402.19159v2`。首次公开：2024-02-29；所查版本更新：2024-04-15。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：TCD 用半线性轨迹一致性函数与策略性随机采样，改进潜一致性模型细节和多步误差。

限制与判断：蒸馏路径、参数化与随机采样共同贡献；较多 NFE 的细节提升不能标成一步结果。

作者元数据备注（与独立核实分开）：Project Page: https://mhh0318.github.io/tcd

原始来源：[来源1](https://arxiv.org/abs/2402.19159v2)

<a id="paper-2403-03206"></a>

## Scaling Rectified Flow Transformers for High-Resolution Image Synthesis

作者：Patrick Esser、Sumith Kulal、Andreas Blattmann、Rahim Entezari 等17人。标识：`2403.03206v1`。首次公开：2024-03-05；所查版本更新：2024-03-05。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICML 2024（官方目录）](https://icml.cc/virtual/2024/poster/34535)

方法：SD3 研究高分辨率 rectified flow、噪声采样和多模态 Transformer，用扩展训练提高文本图像合成。

限制与判断：大数据、模型规模和文本编码器参与收益；不能把系统结果单因归给 flow 目标或假定可单步无损。

原始来源：[来源1](https://arxiv.org/abs/2403.03206v1) · [来源2](https://icml.cc/virtual/2024/poster/34535)

<a id="paper-2405-07510"></a>

## PeRFlow: Piecewise Rectified Flow as Universal Plug-and-Play Accelerator

作者：Hanshu Yan、Xingchao Liu、Jiachun Pan、Jun Hao Liew 等6人。标识：`2405.07510v5`。首次公开：2024-05-13；所查版本更新：2024-09-02。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：PeRFlow 把运输分成若干窗口，在每个窗口 reflow，使潜扩散模型获得分段直化和少步部署。

限制与判断：需计入预训练教师及窗口轨迹构建；可插拔兼容性以论文测试模型和适配方式为限。

原始来源：[来源1](https://arxiv.org/abs/2405.07510v5)

<a id="paper-2406-07507"></a>

## Flow map matching with stochastic interpolants: A mathematical framework for consistency models

作者：Nicholas M. Boffi、Michael S. Albergo、Eric Vanden-Eijnden。标识：`2406.07507v2`。首次公开：2024-06-11；所查版本更新：2025-06-03。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Flow Map Matching 从随机插值构造两时刻映射，连接一致性、Eulerian 与 Lagrangian 形式。

限制与判断：流映射的固定点、解存在性和参数训练收敛分别需要条件；不能把任意 flow 当作已学成的直接运输图。

片段定位：本地HTML提取文本起始行 80, 91, 108；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2406.07507v2) · [来源2](https://arxiv.org/html/2406.07507)

<a id="paper-2406-14548"></a>

## Consistency Models Made Easy

作者：Zhengyang Geng、Ashwini Pokle、William Luo、Justin Lin 等5人。标识：`2406.14548v2`。首次公开：2024-06-20；所查版本更新：2024-10-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/27780)

方法：ECT 从已有扩散模型逐步收紧一致性条件，降低训练高质量一致性模型的附加成本。

限制与判断：所报快速微调以前置预训练为条件；微调 GPU 小时不能与从零总训练成本直接相比。

原始来源：[来源1](https://arxiv.org/abs/2406.14548v2) · [来源2](https://iclr.cc/virtual/2025/poster/27780)

<a id="paper-2407-02398"></a>

## Consistency Flow Matching: Defining Straight Flows with Velocity Consistency

作者：Ling Yang、Zixiang Zhang、Zhilong Zhang、Xingchao Liu 等9人。标识：`2407.02398v1`。首次公开：2024-07-02；所查版本更新：2024-07-02。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Consistency Flow Matching 在速度一致性上约束流，尝试直接训练更直的生成路径。

限制与判断：路径直度有助于积分但不充分保证全局正确耦合；不得与所有同名 consistency 模型合并。

作者元数据备注（与独立核实分开）：Code: https://github.com/YangLing0818/consistency_flow_matching

原始来源：[来源1](https://arxiv.org/abs/2407.02398v1)

<a id="paper-2410-07303"></a>

## Rectified Diffusion: Straightness Is Not Your Need in Rectified Flow

作者：Fu-Yun Wang、Ling Yang、Zhaoyang Huang、Mengdi Wang 等5人。标识：`2410.07303v2`。首次公开：2024-10-09；所查版本更新：2024-10-11。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/28415)

方法：Rectified Diffusion 分离 reflow 的关键训练条件，检验直线性在少步收益中的实际作用。

限制与判断：同标题的否定性结论针对特定机制比较；不能理解成所有路径几何对数值采样都无影响。

片段定位：本地HTML提取文本起始行 125, 127, 129；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2410.07303v2) · [来源2](https://iclr.cc/virtual/2025/poster/28415) · [来源3](https://arxiv.org/html/2410.07303)

<a id="paper-2410-11081"></a>

## Simplifying, Stabilizing and Scaling Continuous-Time Consistency Models

作者：Cheng Lu、Yang Song。标识：`2410.11081v2`。首次公开：2024-10-14；所查版本更新：2025-03-01。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/29963)

方法：sCM 重新设计连续时间一致性参数化、损失和训练稳定化，扩展少步一致性训练。

限制与判断：连续极限中的目标性质不等于有限网络稳定性；训练精度、归一化与导数计算开销需匹配。

片段定位：本地HTML提取文本起始行 46, 47, 49；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：ICLR 2025 Oral

原始来源：[来源1](https://arxiv.org/abs/2410.11081v2) · [来源2](https://iclr.cc/virtual/2025/poster/29963) · [来源3](https://arxiv.org/html/2410.11081)

<a id="paper-2410-12557"></a>

## One Step Diffusion via Shortcut Models

作者：Kevin Frans、Danijar Hafner、Sergey Levine、Pieter Abbeel。标识：`2410.12557v3`。首次公开：2024-10-16；所查版本更新：2025-06-23。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/29802)

方法：Shortcut Models 同时条件于当前时间和步长，用小步监督及两步自举学习可变跨度跳转。

限制与判断：自举误差和训练步长分布影响大跳转；一步与多步表现均应报告，不能只展示最优预算点。

片段定位：本地HTML提取文本起始行 61, 67, 69；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2410.12557v3) · [来源2](https://iclr.cc/virtual/2025/poster/29802) · [来源3](https://arxiv.org/html/2410.12557)

<a id="paper-2412-06264"></a>

## Flow Matching Guide and Code

作者：Yaron Lipman、Marton Havasi、Peter Holderrieth、Neta Shaul 等10人。标识：`2412.06264v1`。首次公开：2024-12-09；所查版本更新：2024-12-09。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Flow Matching Guide and Code 系统整理连续和离散 flow matching 的路径、目标、条件生成及公开实现。

限制与判断：属于方法指南和代码资料，内部多个配置不构成新的独立实证论文成绩；本轮未运行其代码。

原始来源：[来源1](https://arxiv.org/abs/2412.06264v1)

<a id="paper-2503-07565"></a>

## Inductive Moment Matching

作者：Linqi Zhou、Stefano Ermon、Jiaming Song。标识：`2503.07565v7`。首次公开：2025-03-10；所查版本更新：2025-05-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICML 2025（正式论文集）](https://proceedings.mlr.press/v267/zhou25c.html)；[ICML 2025（官方目录）](https://icml.cc/virtual/2025/poster/43977)

方法：IMM 通过归纳式分布矩匹配学习少步生成；ICML 正式条目与后续 arXiv 版本分别留档。

限制与判断：正式标题仍为 Inductive Moment Matching，部分摘要使用 MMSD；新版本数值不可回填为正式论文原成绩。

原始来源：[来源1](https://arxiv.org/abs/2503.07565v7) · [来源2](https://proceedings.mlr.press/v267/zhou25c.html) · [来源3](https://icml.cc/virtual/2025/poster/43977)

<a id="paper-2509-24526"></a>

## CMT: Mid-Training for Efficient Learning of Consistency, Mean Flow, and Flow Map Models

作者：Zheyuan Hu、Chieh-Hsin Lai、Yuki Mitsufuji、Stefano Ermon。标识：`2509.24526v2`。首次公开：2025-09-29；所查版本更新：2026-02-22。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10011770)

方法：CMT 在预训练与最终 flow map 训练之间插入轨迹到干净端点的中训练，改善初始化和后续稳定性。

限制与判断：中训练和教师轨迹的成本要与最终微调合计；不同分辨率、数据量的节省不可混用。

作者元数据备注（与独立核实分开）：ICLR 2026. Code available at https://github.com/sony/cmt

原始来源：[来源1](https://arxiv.org/abs/2509.24526v2) · [来源2](https://iclr.cc/virtual/2026/poster/10011770)

<a id="paper-2510-24474"></a>

## Decoupled MeanFlow: Turning Flow Models into Flow Maps for Accelerated Sampling

作者：Kyungmin Lee、Sihyun Yu、Jinwoo Shin。标识：`2510.24474v1`。首次公开：2025-10-28；所查版本更新：2025-10-28。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2026（正式论文集）](https://proceedings.iclr.cc/paper_files/paper/2026/hash/699124f548e4cb86674b20eae0fd8619-Abstract-Conference.html)；[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10009715)

方法：Decoupled MeanFlow 仅在末段网络引入目标时间条件，把预训练 flow Transformer 转成平均速度流映射。

限制与判断：先训练 flow 再转换的优势包含完整两阶段预算；可转换接口与具体 UMM 主干仍需核实。

原始来源：[来源1](https://arxiv.org/abs/2510.24474v1) · [来源2](https://proceedings.iclr.cc/paper_files/paper/2026/hash/699124f548e4cb86674b20eae0fd8619-Abstract-Conference.html) · [来源3](https://iclr.cc/virtual/2026/poster/10009715)

<a id="paper-2511-18834"></a>

## FlowSteer: Guiding Few-Step Image Synthesis with Authentic Trajectories

作者：Lei Ke、Hubery Yin、Gongye Liu、Zhengyao Lv 等9人。标识：`2511.18834v1`。首次公开：2025-11-24；所查版本更新：2025-11-24。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[CVPR 2026（官方目录）](https://openaccess.thecvf.com/CVPR2026?day=2026-06-07)

方法：FlowSteer 在分段 reflow 中对齐在线轨迹，并加入轨迹对抗约束，修正训练采样失配。

限制与判断：教师轨迹、对抗损失和 scheduler 修复共同影响少步结果；不能把全部增益归因于直化。

作者元数据备注（与独立核实分开）：Few-Step Image Synthesis

原始来源：[来源1](https://arxiv.org/abs/2511.18834v1) · [来源2](https://openaccess.thecvf.com/CVPR2026?day=2026-06-07)

<a id="paper-2511-22688"></a>

## Test-time scaling of diffusions with flow maps

作者：Amirmojtaba Sabour、Michael S. Albergo、Carles Domingo-Enrich、Nicholas M. Boffi 等7人。标识：`2511.22688v1`。首次公开：2025-11-27；所查版本更新：2025-11-27。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/154289)

方法：FMTT 用 flow map 将最终数据上的奖励连接到中间状态，做轨迹倾斜、重要性采样或搜索。

限制与判断：精确采样与局部奖励最大化是不同目标；理论收益依赖映射及权重条件，验证器误差仍会影响实际选择。

原始来源：[来源1](https://arxiv.org/abs/2511.22688v1) · [来源2](https://neurips.cc/virtual/2026/poster/154289)

<a id="paper-2512-11831"></a>

## On the Design of One-step Diffusion via Shortcutting Flow Paths

作者：Haitao Lin、Peiyan Hu、Minsi Ren、Zhifeng Gao 等8人。标识：`2512.11831v5`。首次公开：2025-12-03；所查版本更新：2026-02-01。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10007823)

方法：统一 shortcut 路径的设计空间，分离参数化、时间采样与损失，以受控比较改进从零一步训练。

限制与判断：同表单步质量仍依赖引导与训练步数；新版本结果需绑定所读版本，不能归给所有 shortcut 变体。

作者元数据备注（与独立核实分开）：10 pages of main body, conference paper

原始来源：[来源1](https://arxiv.org/abs/2512.11831v5) · [来源2](https://iclr.cc/virtual/2026/poster/10007823)

<a id="paper-2607-26398"></a>

## Flow Map Learning via Nongradient Vector Flow

作者：Mark Goldstein、Anshuk Uppal、Raghav Singhal、Aahlad Puli 等5人。标识：`2607.26398v1`。首次公开：2026-07-29；所查版本更新：2026-07-29。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10010892)

方法：SGFlow 通过非保守、停止梯度的向量动态学习 ODE 流映射，避免模型逆与迭代调用反传。

限制与判断：其固定点性质与有限神经网络 SGD 收敛有差别；论文也未宣称在全部采样步数上 FID 最优。

作者元数据备注（与独立核实分开）：ICLR 2026

原始来源：[来源1](https://arxiv.org/abs/2607.26398v1) · [来源2](https://iclr.cc/virtual/2026/poster/10010892)

<a id="paper-2609-16222"></a>

## How I learned to stop worrying and love StopGrads: Stationarity, Convergence, and a case study on Flow Map Learning

作者：Max W. Shen、Mark Goldstein、Zichu Wang、Aahlad Puli 等5人。标识：`2609.16222v1`。首次公开：2026-09-14；所查版本更新：2026-09-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/149145)

方法：用停止梯度回归原则刻画固定点和函数半梯度动力学，分析 MeanFlow 等映射并改动梯度放置降低内存。

限制与判断：函数空间唯一驻点和解析动力学有规定假设；不能直接推导实际模型对任意初始化、有限优化的全局收敛。

原始来源：[来源1](https://arxiv.org/abs/2609.16222v1) · [来源2](https://neurips.cc/virtual/2026/poster/149145)

<a id="paper-pmlr-v306-zhang26do"></a>

## Contrastive Flow Map Matching

作者：Junyu Zhang、Daochang Liu、Younghyun Kim、Jong Hwan Ko 等7人。标识：`pmlr-v306-zhang26do`。首次公开：2026；所查版本更新：未提供。

阅读层级：**摘要筛选**。范围：正式PMLR摘要筛选；未核读正文。

来源归属：[ICML 2026（正式论文集）](https://proceedings.mlr.press/v306/zhang26do.html)

方法：在平均速度回归中加入与采样路径对齐的InfoNCE；作者从联合KL分解解释对比学习项，以训练期插件改善flow map。

限制与判断：仅核读正式论文集摘要；未独立复核联合KL推导及全部算力匹配，不能据摘要断言所有MeanFlow变体普遍改善。

原始来源：[来源1](https://proceedings.mlr.press/v306/zhang26do.html)
