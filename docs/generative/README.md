# 扩散、Flow与Drifting生成模型专题

检索截止：2026-10-30。用户已撤销数量上限。本轮以Drifting机制和关联生成路线为边界，按引用、标题、摘要及官方会议来源扩展，新增 **142项** 去重补充记录。

**[综合分析：机制、理论、实验与UMM](synthesis.md)** · **[检索与停止边界](search_scope.md)** · [本轮文件变更](changes_2026-10-30.md)

142项中，10项完成重点章节核读，31项完成正文片段选读，101项完成摘要筛选。这里没有将142项计为全文精读完成。原目录360条、327篇核心完成及6篇停止追取的状态维持原记录；旧论文通过链接复用。

## 阅读覆盖

| 范围 | 数量 | 支持的结论 |
| --- | ---: | --- |
| 重点章节核读 | 10 | 可对指定公式、假设、实验与反例作讨论；未宣称全文逐行复核 |
| 正文片段选读 | 31 | 支持具体片段的方法判断；证明及全部实验仍可能未覆盖 |
| 摘要筛选 | 101 | 支持问题归类和初步方法概括；数值及理论为作者声明 |

## 按问题阅读

| 主题 | 新增项数 |
| --- | ---: |
| [扩散、score与采样](diffusion.md) | 10 |
| [Flow Matching、Rectified Flow、Consistency与Flow Map](flow_consistency.md) | 27 |
| [生成表征、RAE与像素空间](representation.md) | 6 |
| [蒸馏、分布匹配与偏好对齐](distillation_alignment.md) | 11 |
| [Drifting原理、理论与前史](drifting_theory.md) | 24 |
| [Drifting训练方法与算力分配](drifting_methods.md) | 10 |
| [视频、世界模型与机器人策略](video_policy.md) | 23 |
| [离散语言、语音与音频](language_audio.md) | 14 |
| [物理、几何、医学与其他领域](domain_geometry.md) | 17 |

## 六个优先会议的来源入口

新增记录中，47项定位到官方目录或正式论文集，其中12项直接定位正式论文集页/PDF。其余官方目录记录未据此自动认定主会轨道、报告形式或奖项。作者在arXiv备注中的接收声明另存；未确认的会议归属保持未确认。

| 论文 | 官方来源 | 本轮阅读 |
| --- | --- | --- |
| [From Slow Bidirectional to Fast Autoregressive Video Diffusion Models](video_policy.md#paper-2412-07772) | [CVPR 2025（正式论文集）](https://openaccess.thecvf.com/content/CVPR2025/papers/Yin_From_Slow_Bidirectional_to_Fast_Autoregressive_Video_Diffusion_Models_CVPR_2025_paper.pdf) | 正文片段选读 |
| [Inference-Time Scaling for Diffusion Models beyond Scaling Denoising Steps](diffusion.md#paper-2501-09732) | [CVPR 2025（正式论文集）](https://openaccess.thecvf.com/content/CVPR2025/papers/Ma_Scaling_Inference_Time_Compute_for_Diffusion_Models_CVPR_2025_paper.pdf) | 摘要筛选 |
| [FlowSteer: Guiding Few-Step Image Synthesis with Authentic Trajectories](flow_consistency.md#paper-2511-18834) | [CVPR 2026（官方目录）](https://openaccess.thecvf.com/CVPR2026?day=2026-06-07) | 摘要筛选 |
| [Few-Step Diffusion Sampling Through Instance-Aware Discretizations](diffusion.md#paper-2603-17671) | [CVPR 2026（正式论文集）](https://openaccess.thecvf.com/content/CVPR2026/papers/Yuan_Few-Step_Diffusion_Sampling_Through_Instance-Aware_Discretizations_CVPR_2026_paper.pdf) | 摘要筛选 |
| [DOLLAR: Few-Step Video Generation via Distillation and Latent Reward Optimization](video_policy.md#paper-2412-15689) | [ICCV 2025（正式论文集）](https://openaccess.thecvf.com/content/ICCV2025/html/Ding_DOLLAR_Few-Step_Video_Generation_via_Distillation_and_Latent_Reward_Optimization_ICCV_2025_paper.html) | 摘要筛选 |
| [SiT: Exploring Flow and Diffusion-based Generative Models with Scalable Interpolant Transformers](representation.md#paper-2401-08740) | [ECCV 2024（正式论文集）](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/09828.pdf) | 正文片段选读 |
| [Stein Variational Gradient Descent: A General Purpose Bayesian Inference Algorithm](drifting_theory.md#paper-1608-04471) | [NeurIPS 2016（官方目录）](https://neurips.cc/virtual/2016/poster/7009) | 摘要筛选 |
| [Generative Modeling by Estimating Gradients of the Data Distribution](diffusion.md#paper-1907-05600) | [NeurIPS 2019（官方目录）](https://neurips.cc/virtual/2019/poster/13242) | 摘要筛选 |
| [Diffusion Models Beat GANs on Image Synthesis](diffusion.md#paper-2105-05233) | [NeurIPS 2021（官方目录）](https://neurips.cc/virtual/2021/poster/28362) | 摘要筛选 |
| [Variational Diffusion Models](diffusion.md#paper-2107-00630) | [NeurIPS 2021（官方目录）](https://neurips.cc/virtual/2021/poster/27712) | 摘要筛选 |
| [Structured Denoising Diffusion Models in Discrete State-Spaces](diffusion.md#paper-2107-03006) | [NeurIPS 2021（官方目录）](https://neurips.cc/virtual/2021/poster/27623) | 摘要筛选 |
| [Improved Distribution Matching Distillation for Fast Image Synthesis](distillation_alignment.md#paper-2405-14867) | [NeurIPS 2024（正式论文集）](https://papers.nips.cc/paper_files/paper/2024/hash/54dcf25318f9de5a7a01f0a4125c541e-Abstract-Conference.html) | 正文片段选读 |
| [Test-time scaling of diffusions with flow maps](flow_consistency.md#paper-2511-22688) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/154289) | 摘要筛选 |
| [Generative Modeling via Drifting](drifting_theory.md#paper-2602-04770) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/154240) | 重点章节核读 |
| [Drifting Fields are not Conservative](drifting_theory.md#paper-2604-06333) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/155051) | 重点章节核读 |
| [Analytical Correction for Subsampling Bias in Drifting Models](drifting_theory.md#paper-2604-27239) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/155602) | 正文片段选读 |
| [SymDrift: One-Shot Generative Modeling under Symmetries](domain_geometry.md#paper-2605-06140) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/151782) | 摘要筛选 |
| [Kernel-Gradient Drifting Models](drifting_theory.md#paper-2605-10727) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/151352) | 摘要筛选 |
| [Drift Flow Matching](drifting_methods.md#paper-2605-17244) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/155776) | 摘要筛选 |
| [Drift-React: One-step Generation of Reaction Pathways via SE(3) Drifting Fields](domain_geometry.md#paper-2605-22990) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/154432) | 摘要筛选 |
| [Implicit Drifting Policy: One-Step Action Generation via Conditional Expert Geometry](video_policy.md#paper-2606-01098) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/153972) | 摘要筛选 |
| [How I learned to stop worrying and love StopGrads: Stationarity, Convergence, and a case study on Flow Map Learning](flow_consistency.md#paper-2609-16222) | [NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/149145) | 摘要筛选 |
| [Denoising Diffusion Implicit Models](diffusion.md#paper-2010-02502) | [ICLR 2021（官方目录）](https://iclr.cc/virtual/2021/poster/2804) | 摘要筛选 |
| [Progressive Distillation for Fast Sampling of Diffusion Models](distillation_alignment.md#paper-2202-00512) | [ICLR 2022（官方目录）](https://iclr.cc/virtual/2022/poster/6537) | 摘要筛选 |
| [InstaFlow: One Step is Enough for High-Quality Diffusion-Based Text-to-Image Generation](flow_consistency.md#paper-2309-06380) | [ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/19575) | 摘要筛选 |
| [Consistency Trajectory Models: Learning Probability Flow ODE Trajectory of Diffusion](flow_consistency.md#paper-2310-02279) | [ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/17404) | 摘要筛选 |
| [Improved Techniques for Training Consistency Models](flow_consistency.md#paper-2310-14189) | [ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/18479) | 摘要筛选 |
| [Idempotent Generative Network](flow_consistency.md#paper-2311-01462) | [ICLR 2024（官方目录）](https://iclr.cc/virtual/2024/poster/18455) | 摘要筛选 |
| [Consistency Models Made Easy](flow_consistency.md#paper-2406-14548) | [ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/27780) | 摘要筛选 |
| [Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think](representation.md#paper-2410-06940) | [ICLR 2025（正式论文集）](https://proceedings.iclr.cc/paper_files/paper/2025/file/d9e42b4d7163931f3689d6d6fbaa11d0-Paper-Conference.pdf)；[ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/30467) | 摘要筛选 |
| [Rectified Diffusion: Straightness Is Not Your Need in Rectified Flow](flow_consistency.md#paper-2410-07303) | [ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/28415) | 正文片段选读 |
| [Simplifying, Stabilizing and Scaling Continuous-Time Consistency Models](flow_consistency.md#paper-2410-11081) | [ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/29963) | 正文片段选读 |
| [One Step Diffusion via Shortcut Models](flow_consistency.md#paper-2410-12557) | [ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/29802) | 正文片段选读 |
| [LongLive: Real-time Interactive Long Video Generation](video_policy.md#paper-2509-22622) | [ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10007501) | 正文片段选读 |
| [CMT: Mid-Training for Efficient Learning of Consistency, Mean Flow, and Flow Map Models](flow_consistency.md#paper-2509-24526) | [ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10011770) | 摘要筛选 |
| [Diffusion Transformers with Representation Autoencoders](representation.md#paper-2510-11690) | [ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10011890) | 正文片段选读 |
| [Decoupled MeanFlow: Turning Flow Models into Flow Maps for Accelerated Sampling](flow_consistency.md#paper-2510-24474) | [ICLR 2026（正式论文集）](https://proceedings.iclr.cc/paper_files/paper/2026/hash/699124f548e4cb86674b20eae0fd8619-Abstract-Conference.html)；[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10009715) | 摘要筛选 |
| [On the Design of One-step Diffusion via Shortcutting Flow Paths](flow_consistency.md#paper-2512-11831) | [ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10007823) | 摘要筛选 |
| [Flow Map Learning via Nongradient Vector Flow](flow_consistency.md#paper-2607-26398) | [ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10010892) | 摘要筛选 |
| [Deep Unsupervised Learning using Nonequilibrium Thermodynamics](diffusion.md#paper-1503-03585) | [ICML 2015（正式论文集）](https://proceedings.mlr.press/v37/sohl-dickstein15.html) | 摘要筛选 |
| [Improved Denoising Diffusion Probabilistic Models](diffusion.md#paper-2102-09672) | [ICML 2021（官方目录）](https://icml.cc/virtual/2021/poster/9531) | 摘要筛选 |
| [Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution](language_audio.md#paper-2310-16834) | [ICML 2024（官方目录）](https://icml.cc/virtual/2024/poster/34686) | 摘要筛选 |
| [Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](flow_consistency.md#paper-2403-03206) | [ICML 2024（官方目录）](https://icml.cc/virtual/2024/poster/34535) | 摘要筛选 |
| [Score identity Distillation: Exponentially Fast Distillation of Pretrained Diffusion Models for One-Step Generation](distillation_alignment.md#paper-2404-04057) | [ICML 2024（官方目录）](https://icml.cc/virtual/2024/poster/34068) | 摘要筛选 |
| [Inductive Moment Matching](flow_consistency.md#paper-2503-07565) | [ICML 2025（正式论文集）](https://proceedings.mlr.press/v267/zhou25c.html)；[ICML 2025（官方目录）](https://icml.cc/virtual/2025/poster/43977) | 摘要筛选 |
| [Contrastive Flow Map Matching](flow_consistency.md#paper-pmlr-v306-zhang26do) | [ICML 2026（正式论文集）](https://proceedings.mlr.press/v306/zhang26do.html) | 摘要筛选 |
| [Primal-Spectral Generative Modeling: Fast Analytical Generation via Pseudoinverse Lévy Inversion](drifting_theory.md#paper-pmlr-v306-ouyang26c) | [ICML 2026（正式论文集）](https://proceedings.mlr.press/v306/ouyang26c.html) | 摘要筛选 |

## 预印本与尚未核实的会议身份

重要预印本单列于[预印本及未核实身份索引](preprints.md)，包括W-Flow、score联系、Companion-Elliptic、DriftWorld、GR00T技术报告等。未找到本轮官方证据表示身份未确认，不能推断已经证明未被接收；作者自报期刊另列。

## 复用原目录中的基础文献

下列卡片为此前已有阅读；本轮复用，未重新累计为新增或重新宣称完成全篇核读。CFG的workshop归属须与主会区分。

| 文献 | 已有记录 |
| --- | --- |
| DDPM、Score SDE、LDM、DiT | [G001](../reviews/G001.md) · [G002](../reviews/G002.md) · [G003](../reviews/G003.md) · [G004](../reviews/G004.md) |
| Flow Matching、Rectified Flow、Consistency、DPM-Solver | [G005](../reviews/G005.md) · [G006](../reviews/G006.md) · [G007](../reviews/G007.md) · [G008](../reviews/G008.md) |
| CFG、EDM | [G026](../reviews/G026.md) · [G027](../reviews/G027.md) |
| MeanFlow、Improved MeanFlow | [E01](../reviews/E01.md) · [E02](../reviews/E02.md) |
| Diffusion Forcing、Self Forcing、Consistency Policy、Discrete Flow Matching | [G030](../reviews/G030.md) · [D05](../reviews/D05.md) · [E03](../reviews/E03.md) · [E04](../reviews/E04.md) |

## 数据与维护

[机器可读清单](../../data/discovery/generative_models_2026-10-30.json) · [检索审计](../../data/discovery/generative_search_2026-10-30.json) · [渲染脚本](../../scripts/render_generative_survey.py)

本目录README、9个主题页和预印本索引由补充JSON生成；综合分析、检索边界与变更说明手工维护。运行 `python scripts/render_generative_survey.py` 只更新本专题生成页。

文献调研的费用与GPU使用为0，没有训练、推理或数据集下载。文献中的分数和速度均为作者报告。2026-10-30用户另行批准发布到GitHub main，按仓库PR流程交付；见[发布与文件变更记录](changes_2026-10-30.md)。专题不改变P0有限结项及P1实验授权。
