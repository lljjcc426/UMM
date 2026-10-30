# Drifting训练方法与算力分配

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 10 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2605-04060"></a>

## Lookahead Drifting Model

作者：Guoqiang Zhang、Kenta Niwa、W. Bastiaan Kleijn。标识：`2605.04060v1`。首次公开：2026-04-10；所查版本更新：2026-04-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：训练时顺序构造多个前瞻漂移方向并加权合成，尝试吸收更高阶校正而保留一次部署调用。

限制与判断：额外场计算留在训练；现有玩具与 CIFAR 证据不能直接支撑高分辨率视频优势。

原始来源：[来源1](https://arxiv.org/abs/2605.04060v1)

<a id="paper-2604-18194"></a>

## Friction-Augmented Drifting Models for Resource-Efficient Domain Translation

作者：Arkadii Kazanskii、Tatiana Petrova、Andrey Ustyuzhanin、Konstantin Bagrianskii 等6人。标识：`2604.18194v2`。首次公开：2026-04-20；所查版本更新：2026-08-14。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DMF 通过随训练变化的摩擦系数缩放漂移，分析双粒子代理的局部排斥与有限时域收缩。

限制与判断：两粒子代理不足以证明一般分布收敛；二维矩匹配与 Wasserstein 指标、FFHQ 域迁移应分开理解。

原始来源：[来源1](https://arxiv.org/abs/2604.18194v2)

<a id="paper-2605-12183"></a>

## DriftXpress: Faster Drifting Models via Projected RKHS Fields

作者：Ali Falahati、Elliot Creager、Gautam Kamath、Shubhankar Mohapatra。标识：`2605.12183v2`。首次公开：2026-05-12；所查版本更新：2026-07-23。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftXpress 在低秩 RKHS 特征中近似核场，降低参考交互的训练开销。

限制与判断：需同时报告近似秩、场误差、训练墙钟和质量；推理单步与训练节省是两个独立比较。

原始来源：[来源1](https://arxiv.org/abs/2605.12183v2)

<a id="paper-2605-17244"></a>

## Drift Flow Matching

作者：Chenrui Ma、Xi Xiao、Lin Zhao、Tianyang Wang 等6人。标识：`2605.17244v1`。首次公开：2026-05-17；所查版本更新：2026-05-17。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[NeurIPS 2026（官方目录）](https://neurips.cc/virtual/2026/poster/155776)

方法：Drift Flow Matching 将直接运输与流式迭代连接，使漂移生成器支持可选的多步质量提升。

限制与判断：多次调用需要对应训练机制；简单重复调用普通单步生成器不自动获得同样效果。

原始来源：[来源1](https://arxiv.org/abs/2605.17244v1) · [来源2](https://neurips.cc/virtual/2026/poster/155776)

<a id="paper-2607-18198"></a>

## Three-Body Scattering for Generative Modeling

作者：Peng Sun、Zhenglin Cheng、Deyuan Liu、Jun Xie 等6人。标识：`2607.18198v1`。首次公开：2026-07-20；所查版本更新：2026-07-20。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：TBSM 将能量距离转成每个样本只与一真一假源交互的三体散射，以 O(B) 样本损失训练一步生成器。

限制与判断：线性交互计数不包含特征编码器和生成器成本；同条件单参考及跟踪估计仍有统计误差。

作者元数据备注（与独立核实分开）：31 pages, 5 figures, and 4 tables. Code: https://github.com/sp12138/TBSM

原始来源：[来源1](https://arxiv.org/abs/2607.18198v1)

<a id="paper-2608-07924"></a>

## Second Order Drifting Models

作者：Drake Brown、Yuhao Huang、Shih-Hsin Wang、Bao Wang。标识：`2608.07924v1`。首次公开：2026-08-08；所查版本更新：2026-08-08。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：在相空间加入人工速度变量，利用二阶动力学缓解核平滑带来的谱刚性，并给出半隐式训练。

限制与判断：加速分析围绕线性化频率动力学；人工训练速度变量不能解释为视频的真实物体速度。

片段定位：本地HTML提取文本起始行 73, 105, 107；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：20 pages, 4 figures

原始来源：[来源1](https://arxiv.org/abs/2608.07924v1) · [来源2](https://arxiv.org/html/2608.07924)

<a id="paper-2609-32298"></a>

## Refresh or Realize? Compute Allocation in Drifting Models

作者：Sipeng Chen、Xu Zheng、Shibo Li。标识：`2609.32298v1`。首次公开：2026-09-26；所查版本更新：2026-09-26。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：固定目标重复拟合，测量实际网络位移与指定场的差距，并比较更新场和深入拟合的预算分配。

限制与判断：两种训练种子的同墙钟结果支持该设定下优先刷新；不能由更低固定目标误差推出更好最终 FID。

片段定位：本地HTML提取文本起始行 183, 204, 580；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：20pages

原始来源：[来源1](https://arxiv.org/abs/2609.32298v1) · [来源2](https://arxiv.org/html/2609.32298)

<a id="paper-2610-03626"></a>

## Depth as Time in One-Step Generative Models

作者：Arnold Caleb Asiimwe、William Yang、Sanghyuk Chun、Esin Tureci 等5人。标识：`2610.03626v1`。首次公开：2026-10-02；所查版本更新：2026-10-02。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：以中间层输出头探测单步模型的深度计算，发现流映射模型可呈现逐层去噪及再加噪现象。

限制与判断：层探测是经验观察，原生漂移模型未呈现同样模式；不能把所有单步网络都解释成隐藏扩散轨迹。

原始来源：[来源1](https://arxiv.org/abs/2610.03626v1)

<a id="paper-2610-04703"></a>

## Learning Discriminative Geometry for Drifting Models

作者：Doudou Zhang、Wenwen Hou、Yilin Chen、Qi Chen。标识：`2610.04703v1`。首次公开：2026-10-03；所查版本更新：2026-10-03。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：交替学习编码器的判别几何和生成器，以当前批次重建 KDE，并裁剪特征速度。

限制与判断：生成器更新仍需经冻结编码器对输入反传；引入判别几何训练的依赖与计算须单独计入。

片段定位：本地HTML提取文本起始行 249, 278, 331；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2610.04703v1) · [来源2](https://arxiv.org/html/2610.04703)

<a id="paper-2610-10989"></a>

## Multi-Bandwidth Distribution Matching Distillation: On the Equivalence of Distribution Matching Distillation and Drifting Models

作者：Jialin Zhu、Xing Liu、Feixiang He、He Wang。标识：`2610.10989v1`。首次公开：2026-10-07；所查版本更新：2026-10-07。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：把预训练扩散或 flow 的信号改写为漂移吸引场，联系 DMD，并提出多带宽 DMD。

限制与判断：等价性取决于教师场、排斥估计和参数化；有教师的蒸馏与原生无教师训练应分列。

片段定位：本地HTML提取文本起始行 72, 73, 74；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2610.10989v1) · [来源2](https://arxiv.org/html/2610.10989)
