# 离散语言、语音与音频

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 14 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2205-14217"></a>

## Diffusion-LM Improves Controllable Text Generation

作者：Xiang Lisa Li、John Thickstun、Ishaan Gulrajani、Percy Liang 等5人。标识：`2205.14217v1`。首次公开：2022-05-27；所查版本更新：2022-05-27。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Diffusion-LM 在连续词嵌入上去噪，并利用梯度实现可控文本生成。

限制与判断：离散化、嵌入到 token 的映射和多步控制成本均须计入；文本属性控制不等于严格逻辑推理。

原始来源：[来源1](https://arxiv.org/abs/2205.14217v1)

<a id="paper-2310-16834"></a>

## Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution

作者：Aaron Lou、Chenlin Meng、Stefano Ermon。标识：`2310.16834v3`。首次公开：2023-10-25；所查版本更新：2024-06-06。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICML 2024（官方目录）](https://icml.cc/virtual/2024/poster/34686)

方法：SEDD 用离散分布比率与 score entropy 目标建立离散扩散，支持文本建模与生成。

限制与判断：离散比率估计和连续 score 恒等式不同；困惑度、似然界和少步质量须按相同设置评价。

作者元数据备注（与独立核实分开）：ICML 2024 Oral. Code at https://github.com/louaaron/Score-Entropy-Discrete-Diffusion

原始来源：[来源1](https://arxiv.org/abs/2310.16834v3) · [来源2](https://icml.cc/virtual/2024/poster/34686)

<a id="paper-2406-07524"></a>

## Simple and Effective Masked Diffusion Language Models

作者：Subham Sekhar Sahoo、Marianne Arriola、Yair Schiff、Aaron Gokaslan 等8人。标识：`2406.07524v2`。首次公开：2024-06-11；所查版本更新：2024-11-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：MDLM 通过掩码离散扩散和简化参数化提升文本密度建模及采样。

限制与判断：掩码恢复的并行预测仍可需要多轮；困惑度、吞吐和生成连贯性应分列。

作者元数据备注（与独立核实分开）：NeurIPS 2024. We provide the code at https://github.com/kuleshov-group/mdlm

原始来源：[来源1](https://arxiv.org/abs/2406.07524v2)

<a id="paper-2502-09992"></a>

## Large Language Diffusion Models

作者：Shen Nie、Fengqi Zhu、Zebin You、Xiaolu Zhang 等10人。标识：`2502.09992v3`。首次公开：2025-02-14；所查版本更新：2025-10-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：LLaDA 以掩码扩散完成语言预训练与指令适配，检验扩散语言模型的规模化能力。

限制与判断：双向建模不直接证明胜过同预算 AR；采样步数、重掩码和生成长度影响吞吐与指标。

原始来源：[来源1](https://arxiv.org/abs/2502.09992v3)

<a id="paper-2603-28049"></a>

## Drift-AR: Single-Step Visual Autoregressive Generation via Anti-Symmetric Drifting

作者：Zhen Zou、Xiaoxiao Ma、Mingde Yao、Jie Huang 等6人。标识：`2603.28049v3`。首次公开：2026-03-30；所查版本更新：2026-06-29。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Drift-AR 把漂移用于连续视觉 AR 的扩散解码，并配合连续特征的提议与验证加速。

限制与判断：单步解码器与自回归前缀、提议验证、整图端到端调用次数须分列。

片段定位：本地HTML提取文本起始行 64, 66, 72；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2603.28049v3) · [来源2](https://arxiv.org/html/2603.28049)

<a id="paper-2604-24199"></a>

## Speech Enhancement Based on Drifting Models

作者：Liang Xu、Diego Caviedes-Nozal、W. Bastiaan Kleijn、Longfei Felix Yan 等5人。标识：`2604.24199v4`。首次公开：2026-04-27；所查版本更新：2026-06-06。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：较早的 DriftSE 将语音增强写成分布平衡，比较从噪声观测直接映射和条件随机生成。

限制与判断：无配对边缘匹配不保证保留输入说话者和语义；需结合后续带条件的反例分析。

作者元数据备注（与独立核实分开）：6 pages, 2 figures

原始来源：[来源1](https://arxiv.org/abs/2604.24199v4)

<a id="paper-2605-19470"></a>

## Drifting Objectives for Refining Discrete Diffusion Language Models

作者：Daisuke Oba、Hiroki Furuta、Naoaki Okazaki。标识：`2605.19470v1`。首次公开：2026-05-19；所查版本更新：2026-05-19。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：TokenDrift 将离散扩散预测提升为软 token 特征，在冻结语义空间增加吸引排斥目标。

限制与判断：它是离散扩散的细化目标，所报设置包含多次调用；不能标为从噪声原生一步生成全文。

片段定位：本地HTML提取文本起始行 81, 93, 182；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Project page: https://daioba.github.io/tokendrift/

原始来源：[来源1](https://arxiv.org/abs/2605.19470v1) · [来源2](https://arxiv.org/html/2605.19470)

<a id="paper-2609-12252"></a>

## DriftSE: Speech Enhancement with Generative Drifting

作者：Liang Xu、Diego Caviedes-Nozal、W. Bastiaan Kleijn、Longfei Felix Yan 等5人。标识：`2609.12252v1`。首次公开：2026-09-10；所查版本更新：2026-09-10。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：新 DriftSE 在语义与声学双潜空间同时漂移，尝试兼顾内容清晰度和物理声学保真。

限制与判断：与 2604.24199 同名但不同论文；语义与声学目标的权衡不能外推为书写细节无损。

作者元数据备注（与独立核实分开）：11 pages, 3 figures

原始来源：[来源1](https://arxiv.org/abs/2609.12252v1)

<a id="paper-2609-27598"></a>

## DriftAudio: Marginal Drifting for Distributional Post-Training of One-Step Text-to-Audio Generators

作者：Xingyu Chen、Fei Ma、Sipei Zhao。标识：`2609.27598v1`。首次公开：2026-09-23；所查版本更新：2026-09-23。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftAudio 对已有单步文生音频做跨文本边缘分布后训练，用冻结音频特征与滚动生成样本库估计场。

限制与判断：边缘分布改进与文本条件保持分别评估；不同底座的 CLAP、IS 有取舍，不能仅凭 FAD 宣称全面改善。

片段定位：本地HTML提取文本起始行 105, 116, 304；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Submitted to IEEE ICASSP 2027

原始来源：[来源1](https://arxiv.org/abs/2609.27598v1) · [来源2](https://arxiv.org/html/2609.27598)

<a id="paper-2609-34662"></a>

## Unsupervised Speech Enhancement via Drifting

作者：Diego Caviedes-Nozal、Liang Xu、Rasmus Kongsgaard Olsson、W. Bastiaan Kleijn。标识：`2609.34662v1`。首次公开：2026-09-28；所查版本更新：2026-09-28。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：揭示无配对边缘漂移会丢失内容与说话者，使用输入 anchor 与 key 重加权重新绑定条件。

限制与判断：内容和渲染质量可分别变化；正文在统一重评分流水线比较，不能混用不同实现的非侵入指标。

片段定位：本地HTML提取文本起始行 108, 115, 118；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：5 pages, 2 figures. Submitted to ICASSP 2027

原始来源：[来源1](https://arxiv.org/abs/2609.34662v1) · [来源2](https://arxiv.org/html/2609.34662)

<a id="paper-2610-12879"></a>

## One-Step Text Generation by Seq-Drifting

作者：Jiayu Liu、Ruizhi Zhao、Tianyun Ji、Yee Whye Teh 等6人。标识：`2610.12879v1`。首次公开：2026-10-09；所查版本更新：2026-10-09。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：Seq-Drifting 在连续 token 表示上形成上下文相关吸引和跨样本、序列内排斥，一次并行输出文本。

限制与判断：训练使用支持模型构造上下文候选；不应把推理不需支持模型写成完全没有教师或外部知识成本。

片段定位：本地HTML提取文本起始行 64, 84, 142；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2610.12879v1) · [来源2](https://arxiv.org/html/2610.12879)

<a id="paper-2610-22960"></a>

## DriftTTS: One-stage Single Step Text-to-Speech via Generative Drifting

作者：Jaehyun Ahn、Dohyun Kim、Heeseung Kim。标识：`2610.22960v1`。首次公开：2026-10-16；所查版本更新：2026-10-16。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：DriftTTS 在时长预测与单调对齐形成的先验上做分段漂移，一次解码 mel 频谱。

限制与判断：单次 decoder 不包含文本编码、时长模型和声码器全链路；分段与时长对齐是重要条件信息。

片段定位：本地HTML提取文本起始行 47, 48, 49；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Project page: https://drifttts.github.io/

原始来源：[来源1](https://arxiv.org/abs/2610.22960v1) · [来源2](https://arxiv.org/html/2610.22960)

<a id="paper-2610-23225"></a>

## ReLaDrift: Recurrent Language Generation via Drifting for Test-Time Scaling

作者：Yuki Otsuka、Daisuke Oba、Naoaki Okazaki。标识：`2610.23225v1`。首次公开：2026-10-16；所查版本更新：2026-10-16。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：ReLaDrift 共享生成器反复修订草稿，只对随机抽到的末轮反传，使测试计算可随轮数扩展。

限制与判断：推理 N 轮就是 N 次生成器调用；该方法超出了原生单步，不可统一标为所有结果 1-NFE。

片段定位：本地HTML提取文本起始行 93, 95, 103；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

原始来源：[来源1](https://arxiv.org/abs/2610.23225v1) · [来源2](https://arxiv.org/html/2610.23225)

<a id="paper-2610-32870"></a>

## Noisy Target Training Meets Drifting for Weakly-Supervised Speech Enhancement

作者：Yoshiki Masuyama、Dominik Klement、Christoph Boeddeker、Julius Richter 等8人。标识：`2610.32870v1`。首次公开：2026-10-23；所查版本更新：2026-10-23。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：把 noisy-target 训练与未配对干净语音的 Sinkhorn 漂移相结合，修正残留噪声。

限制与判断：仍需额外干净语料分布，且噪声域和内容保持需检查；弱监督不等于无数据依赖。

作者元数据备注（与独立核实分开）：Submitted to ICASSP 2027

原始来源：[来源1](https://arxiv.org/abs/2610.32870v1)
