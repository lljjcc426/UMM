# 视频、世界模型与机器人策略

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 23 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2412-07772"></a>

## From Slow Bidirectional to Fast Autoregressive Video Diffusion Models

作者：Tianwei Yin、Qiang Zhang、Richard Zhang、William T. Freeman 等7人。标识：`2412.07772v4`。首次公开：2024-12-10；所查版本更新：2025-09-23。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[CVPR 2025（正式论文集）](https://openaccess.thecvf.com/content/CVPR2025/papers/Yin_From_Slow_Bidirectional_to_Fast_Autoregressive_Video_Diffusion_Models_CVPR_2025_paper.pdf)

方法：CausVid 用分布匹配蒸馏把双向视频教师转换为因果少步学生，并利用缓存支持低延迟生成。

限制与判断：因果滚动与去噪步数是两条成本轴；蒸馏教师和训练推理输入分布差异仍可能造成长期误差。

片段定位：本地HTML提取文本起始行 102, 103, 106；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：CVPR 2025. Project Page: https://causvid.github.io/

原始来源：[来源1](https://arxiv.org/abs/2412.07772v4) · [来源2](https://openaccess.thecvf.com/content/CVPR2025/papers/Yin_From_Slow_Bidirectional_to_Fast_Autoregressive_Video_Diffusion_Models_CVPR_2025_paper.pdf) · [来源3](https://arxiv.org/html/2412.07772)

<a id="paper-2412-15689"></a>

## DOLLAR: Few-Step Video Generation via Distillation and Latent Reward Optimization

作者：Zihan Ding、Chi Jin、Difan Liu、Haitian Zheng 等9人。标识：`2412.15689v2`。首次公开：2024-12-20；所查版本更新：2026-05-06。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICCV 2025（正式论文集）](https://openaccess.thecvf.com/content/ICCV2025/html/Ding_DOLLAR_Few-Step_Video_Generation_via_Distillation_and_Latent_Reward_Optimization_ICCV_2025_paper.html)

方法：DOLLAR 结合变分 score 蒸馏、一致性蒸馏和潜奖励优化，研究少步视频的质量与多样性。

限制与判断：VBench 和人类偏好未覆盖笔画规范；1步最高加速与4步质量对照口径不同，不能拼接成一个系统成绩。

原始来源：[来源1](https://arxiv.org/abs/2412.15689v2) · [来源2](https://openaccess.thecvf.com/content/ICCV2025/html/Ding_DOLLAR_Few-Step_Video_Generation_via_Distillation_and_Latent_Reward_Optimization_ICCV_2025_paper.html)

<a id="paper-2504-12626"></a>

## Frame Context Packing and Drift Prevention in Next-Frame-Prediction Video Diffusion Models

作者：Lvmin Zhang、Shengqu Cai、Muyang Li、Gordon Wetzstein 等5人。标识：`2504.12626v3`。首次公开：2025-04-17；所查版本更新：2025-10-14。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：FramePack 按历史帧重要性压缩上下文，并研究下一帧视频生成中的长期漂移抑制。

限制与判断：这里的 drift 是长视频误差累积；不属于 GMD 核场机制，视频时序与生成采样时间须分开。

片段定位：本地HTML提取文本起始行 48, 49, 51；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：https://github.com/lllyasviel/FramePack

原始来源：[来源1](https://arxiv.org/abs/2504.12626v3) · [来源2](https://arxiv.org/html/2504.12626)

<a id="paper-2509-22622"></a>

## LongLive: Real-time Interactive Long Video Generation

作者：Shuai Yang、Wei Huang、Ruihang Chu、Yicheng Xiao 等12人。标识：`2509.22622v2`。首次公开：2025-09-26；所查版本更新：2025-10-13。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10007501)

方法：LongLive 通过因果流式生成、训练分布和记忆管理支持实时交互长视频。

限制与判断：实时性依赖具体分辨率、硬件和缓存设定；长时视觉稳定并未验证规范书写中的离散事件顺序。

片段定位：本地HTML提取文本起始行 48, 50, 52；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Code, model, and demos are available at https://github.com/NVlabs/LongLive

原始来源：[来源1](https://arxiv.org/abs/2509.22622v2) · [来源2](https://iclr.cc/virtual/2026/poster/10007501) · [来源3](https://arxiv.org/html/2509.22622)

<a id="paper-2603-11984"></a>

## Ada3Drift: Adaptive Training-Time Drifting for One-Step 3D Visuomotor Robotic Manipulation

作者：Chongyang Xu、Yixian Zou、Tianyu Yang、Fanman Meng 等7人。标识：`2603.11984v2`。首次公开：2026-03-12；所查版本更新：2026-09-20。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Ada3Drift 先用配对回归建立观测动作对应，再逐步增加批量漂移正则，单次生成三维控制动作块。

限制与判断：配对监督、课程调度和几何输入共同影响结果；不能把收益全部归于替换生成目标。

原始来源：[来源1](https://arxiv.org/abs/2603.11984v2)

<a id="paper-2603-14056"></a>

## Amortizing Trajectory Diffusion with Keyed Drift Fields

作者：Gokul Puthumanaillam、Melkior Ornik。标识：`2603.14056v1`。首次公开：2026-03-14；所查版本更新：2026-03-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Keyed Drifting 在反映当前条件的紧凑 key 空间检索邻域，在完整轨迹空间施加漂移。

限制与判断：无条件未来维度可能淹没当前状态并造成近静止输出；key 的信息权限和同条件样本覆盖决定迁移合理性。

原始来源：[来源1](https://arxiv.org/abs/2603.14056v1)

<a id="paper-2604-03540"></a>

## Drift-Based Policy Optimization: Native One-Step Policy Learning for Online Robot Control

作者：Yuxuan Gao、Yedong Shen、Shiqi Zhang、Wenhao Yu 等9人。标识：`2604.03540v4`。首次公开：2026-04-04；所查版本更新：2026-08-29。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DBP 单步生成多模态动作块；DBPO 增加随机接口提供 PPO 风格的条件 rollout 似然用于在线优化。

限制与判断：训练随机接口与部署生成器应区分；真实任务成功率不能跨数据、硬件和演示预算直接比较。

作者元数据备注（与独立核实分开）：Accepted at the 34th ACM International Conference on Multimedia

原始来源：[来源1](https://arxiv.org/abs/2604.03540v4)

<a id="paper-2604-04528"></a>

## Receding-Horizon Control via Drifting Models

作者：Daniele Foffano、Alessio Russo、Alexandre Proutiere。标识：`2604.04528v1`。首次公开：2026-04-06；所查版本更新：2026-04-06。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Drifting MPC 将离线行为先验和期望代价联合成条件轨迹目标，用单步生成支持滚动控制。

限制与判断：未知动力学下仍受离线支持限制；规划目标最优与真实闭环安全、可执行性需分别测量。

原始来源：[来源1](https://arxiv.org/abs/2604.04528v1)

<a id="paper-2604-16519"></a>

## Positive-Only Drifting Policy Optimization

作者：Qi Zhang。标识：`2604.16519v1`。首次公开：2026-04-15；所查版本更新：2026-04-15。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：PODPO 用正优势样本驱动局部对比漂移，探索无策略密度的在线策略改进。

限制与判断：正样本选择并未自动证明全局优化或主动防错；摘要中的机制主张还需正文和公平闭环证据支持。

作者元数据备注（与独立核实分开）：12 pages, 6 figures

原始来源：[来源1](https://arxiv.org/abs/2604.16519v1)

<a id="paper-2604-21489"></a>

## MISTY: High-Throughput Motion Planning via Mixer-based Single-step Drifting

作者：Yining Xing、Zehong Ke、Yiqian Tu、Zhiyuan Liu 等6人。标识：`2604.21489v1`。首次公开：2026-04-23；所查版本更新：2026-04-23。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：MISTY 以 mixer 结构和单步漂移生成轨迹，强调高吞吐运动规划。

限制与判断：规划生成头的吞吐与端到端碰撞检查、可行性和控制闭环成本不同；本轮未复核全部设置和运行代码。

作者元数据备注（与独立核实分开）：8 pages, 4 figures, 3 tables. Submitted to IEEE Robotics and Automation Letters (RA-L)

原始来源：[来源1](https://arxiv.org/abs/2604.21489v1)

<a id="paper-2605-07727"></a>

## Drifting Field Policy: A One-Step Generative Policy via Wasserstein Gradient Flow

作者：Juil Koo、Mingue Park、Jiwon Choi、Yunhong Min 等5人。标识：`2605.07727v1`。首次公开：2026-05-08；所查版本更新：2026-05-08。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DFP 把价值提升与锚策略约束分解为动作空间场，并用 top-K 价值选择构造可训练代理。

限制与判断：Q 函数误差、行为支持与代理偏差会影响结果；会议目录改题条目未在本轮强行合并为同一正式版本。

原始来源：[来源1](https://arxiv.org/abs/2605.07727v1)

<a id="paper-2606-01098"></a>

## Implicit Drifting Policy: One-Step Action Generation via Conditional Expert Geometry

作者：Zemin Yang、Yaoyu He、Yiming Zhong、Yuhao Zhang 等8人。标识：`2606.01098v1`。首次公开：2026-05-31；所查版本更新：2026-05-31。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/153972)

方法：IDP 用观测相似演示的局部专家几何和全局参考几何构造标量势，避免显式估计极稀疏条件场。

限制与判断：该方法改变了直接核场估计；邻域是否共享合法动作语义和终端约束是 UMM 迁移时的关键。

原始来源：[来源1](https://arxiv.org/abs/2606.01098v1) · [来源2](https://neurips.cc/virtual/2026/poster/153972)

<a id="paper-2606-13795"></a>

## DiPOD: Diffusion Policy Optimization without Drifting Apart

作者：Haozhe Jiang、Haiwen Feng、Pieter Abbeel、Jiantao Jiao 等6人。标识：`2606.13795v2`。首次公开：2026-06-11；所查版本更新：2026-06-17。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DiPOD 通过自蒸馏和在策略 ELBO 正则，减轻扩散策略似然代理与真实策略梯度的双重偏移。

限制与判断：题名 drifting apart 指目标偏移，机制属于扩散策略优化；不归为 GMD 漂移模型。

作者元数据备注（与独立核实分开）：Project page: astro-eric.github.io/blogs/dipod/ Code: https://github.com/Astro-Eric/DiPOD-release

原始来源：[来源1](https://arxiv.org/abs/2606.13795v2)

<a id="paper-2607-14507"></a>

## DRIFT: Drift and Aggregation for Motion Planning

作者：Yining Xing、Zhiyuan Liu、Zehong Ke、Wenhao Yu 等5人。标识：`2607.14507v1`。首次公开：2026-07-16；所查版本更新：2026-07-16。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DRIFT 批量生成多条紧凑轨迹提议，再用场景感知聚合头形成最终驾驶计划。

限制与判断：提议头 10.82ms 与完整模型 66.43ms 的口径不同；单个最终计划仍包含多候选和聚合计算。

作者元数据备注（与独立核实分开）：8 pages, 3 figures, 4 tables. Under review at IEEE RAL

原始来源：[来源1](https://arxiv.org/abs/2607.14507v1)

<a id="paper-2607-15065"></a>

## DriftWorld: Fast World Modeling through Drifting

作者：Susie Lu、Haonan Chen、Weirui Ye、Yilun Du。标识：`2607.15065v3`。首次公开：2026-07-16；所查版本更新：2026-10-02。

阅读层级：**重点章节核读**。范围：§III-C单正样本条件场；§IV-A数据与时间窗；§IV-B TableI、讨论及自回归范围。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftWorld 在历史帧与动作条件下用单正例和多个生成负例训练未来观测生成器，并做自回归展开。

限制与判断：真实场景的一次调用通常预测一帧，长视频仍需多次调用；PSNR/FVD 和机器人场景不构成汉字笔顺正确证据。

本轮核读所得：单次生成未来块随后自回归滚动；头部一步不等于完整长视频一步，PushT同UNet对照支持该场景的目标函数收益。

作者元数据备注（与独立核实分开）：Website at https://susie-lu.github.io/driftworld/

原始来源：[来源1](https://arxiv.org/abs/2607.15065v3) · [来源2](https://arxiv.org/html/2607.15065v3)

<a id="paper-2608-23939"></a>

## CoDrift: Compositional Drifting for Offline Reinforcement Learning

作者：Xiewei Ni、Ruofeng Mei、Xiangyu Xu。标识：`2608.23939v1`。首次公开：2026-08-25；所查版本更新：2026-08-25。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：CoDrift 组合条件行为场、跨状态边缘场与价值场，应对离线 RL 的单正例和多目标问题。

限制与判断：边缘稳定性与状态条件保持可能冲突；需要匹配 critic、数据和调参预算才能归因。

原始来源：[来源1](https://arxiv.org/abs/2608.23939v1)

<a id="paper-2608-29749"></a>

## DriftingVLA: Native One-Step Vision-Language-Action Generation via Per-Dimension Temporal Drifting

作者：Yuxuan Gao、Shiqi Zhang、Yedong Shen、Yifan Duan 等9人。标识：`2608.29749v1`。首次公开：2026-08-30；所查版本更新：2026-08-30。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftingVLA 以每个动作维度的完整时间曲线组织漂移，模型仍联合生成所有维度，并后训练 VLM 与动作头。

限制与判断：单维训练几何不等于推理中各维独立；动作专家单步也不等于整个 VLM 加控制回路只做一次轻量计算。

片段定位：本地HTML提取文本起始行 51, 56, 76；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2608.29749v1) · [来源2](https://arxiv.org/html/2608.29749)

<a id="paper-2609-06923"></a>

## DriftParking: Trajectory Modeling via Drifting Field for End-to-End Automated Parking

作者：Ziyan Wang、Dong Li、Weibo Wang、Yinyin Lu 等7人。标识：`2609.06923v1`。首次公开：2026-09-07；所查版本更新：2026-09-07。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftParking 使用配对轨迹的一对一吸引、专家中心排斥及端点残差表示，强调停车终点精度。

限制与判断：吸引项已转为条件配对监督；不可把该设定直接等同于总体分布匹配理论或自由多模态采样。

原始来源：[来源1](https://arxiv.org/abs/2609.06923v1)

<a id="paper-2609-18108"></a>

## Technical Report: One-Step Drifting Action Heads for GR00T N1.7

作者：Xihe Shao。标识：`2609.18108v1`。首次公开：2026-09-16；所查版本更新：2026-09-16。

阅读层级：**重点章节核读**。范围：方法、同步与异步范围；§IV-A TablesI/II/III、评测覆盖及缺失项。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：GR00T 技术报告记录单步漂移动作头的速度和多种子闭环成功率，明确披露成功率下降。

限制与判断：延迟只含骨干加动作头；对照种子并非各项完全齐全，Object 缺结果，异步重叠路径未被同步 LIBERO 测试。

本轮核读所得：GR00T头部45.3→5.0ms，backbone+head70.0→30.6ms；LIBERO三个已测套件成功率下降，异步扩展未在该基准验证。

作者元数据备注（与独立核实分开）：For code and test result, see https://github.com/RealManShao/lerobot/tree/feat/drif-ov. For trained checkpoint, see https://huggingface.co/Xihe666/models

原始来源：[来源1](https://arxiv.org/abs/2609.18108v1) · [来源2](https://arxiv.org/html/2609.18108v1)

<a id="paper-2609-23305"></a>

## Shared Execution-Clock Drifting Policy for Dynamic Precision Manipulation

作者：Zhenchen Dong、Qingran Wu、Jinna Fu、Jiaming Wu 等7人。标识：`2609.23305v1`。首次公开：2026-09-20；所查版本更新：2026-09-20。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：SECD 同时生成进度索引动作曲线与共享单调执行时钟，通过解码动作上的漂移和演示对齐联合训练。

限制与判断：块内进度不等于完整任务进度；执行时钟、采样积分时间和优化迭代应分开。

片段定位：本地HTML提取文本起始行 42, 44, 45；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：8 pages. Project page: https://secd-anonymous-ewn.pages.dev/

原始来源：[来源1](https://arxiv.org/abs/2609.23305v1) · [来源2](https://arxiv.org/html/2609.23305)

<a id="paper-2610-15662"></a>

## Drift, Then Spread: Learning One-Step Generative Policies for Online Reinforcement Learning

作者：Chunyu Luo、Hongyu Zhao、Guangyi Ni、Yue Song 等5人。标识：`2610.15662v1`。首次公开：2026-10-11；所查版本更新：2026-10-11。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftSpread 在同一 actor 中交替吸收 critic 引导漂移与熵扩散，用于无显式密度的最大熵 RL。

限制与判断：Boltzmann 收敛结论要求固定 critic、精确拟合及先小步后长时间极限，不能直接保证有限在线训练。

原始来源：[来源1](https://arxiv.org/abs/2610.15662v1)

<a id="paper-2610-19883"></a>

## Occupancy Modeling via Drifting: One-Step Generation Enables Direct Policy Extraction

作者：Robin Uhrich、Marco Bagatella、Núria Armengol Urpí、Pavel Kolev 等5人。标识：`2610.19883v1`。首次公开：2026-10-14；所查版本更新：2026-10-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：用漂移建模折扣状态占据，通过单步生成器直接微分提取策略，减少额外 critic 蒸馏。

限制与判断：占据建模、多模态覆盖和策略提取各影响结果；无标签预训练仍依赖覆盖合适行为的数据。

原始来源：[来源1](https://arxiv.org/abs/2610.19883v1)

<a id="paper-2610-20190"></a>

## Value-Guided Repulsion for Offline Reinforcement Learning

作者：Yixue Hao、Jiahao Zhang、Jiesong Lian、Xufei Guo 等8人。标识：`2610.20190v1`。首次公开：2026-10-14；所查版本更新：2026-10-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：VRQL 用归一化价值修改生成动作间排斥强度，同时保留对行为动作的吸引。

限制与判断：局部场的价值偏置依赖 critic 准确性；较高离线平均成绩不自动说明更强的分布覆盖。

原始来源：[来源1](https://arxiv.org/abs/2610.20190v1)
