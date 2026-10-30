# 生成表征、RAE与像素空间

[专题总览](README.md) · [综合分析](synthesis.md) · [检索与停止边界](search_scope.md)

本页 6 项。每项列明实际阅读范围；单篇作者报告的结果均未在本仓库复现。

<a id="paper-2401-08740"></a>

## SiT: Exploring Flow and Diffusion-based Generative Models with Scalable Interpolant Transformers

作者：Nanye Ma、Mark Goldstein、Michael S. Albergo、Nicholas M. Boffi 等6人。标识：`2401.08740v2`。首次公开：2024-01-16；所查版本更新：2024-09-23。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[ECCV 2024（正式论文集）](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/09828.pdf)

方法：SiT 在同一 Transformer 中系统比较插值路径、预测目标和 ODE/SDE 采样，作为 DiT 到 flow 的受控桥梁。

限制与判断：表中训练步数与 NFE 固定的局部消融比跨系统榜单更有归因价值；长期大模型结果还包含其他设置变化。

片段定位：本地HTML提取文本起始行 246, 248, 256；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：ECCV 2024; Code available: https://github.com/willisma/SiT

原始来源：[来源1](https://arxiv.org/abs/2401.08740v2) · [来源2](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/09828.pdf) · [来源3](https://arxiv.org/html/2401.08740)

<a id="paper-2410-06940"></a>

## Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think

作者：Sihyun Yu、Sangkyung Kwak、Huiwon Jang、Jongheon Jeong 等7人。标识：`2410.06940v4`。首次公开：2024-10-09；所查版本更新：2025-06-18。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：[ICLR 2025（正式论文集）](https://proceedings.iclr.cc/paper_files/paper/2025/file/d9e42b4d7163931f3689d6d6fbaa11d0-Paper-Conference.pdf)；[ICLR 2025（官方目录）](https://iclr.cc/virtual/2025/poster/30467)

方法：REPA 在扩散 Transformer 中间层对齐预训练视觉表征，主要提高训练效率和生成质量。

限制与判断：对齐特征是训练监督，不自动把生成器变为可靠理解器；预训练编码器成本、特征层和细节保真需记录。

作者元数据备注（与独立核实分开）：ICLR 2025 (Oral). Project page: https://sihyun.me/REPA

原始来源：[来源1](https://arxiv.org/abs/2410.06940v4) · [来源2](https://proceedings.iclr.cc/paper_files/paper/2025/file/d9e42b4d7163931f3689d6d6fbaa11d0-Paper-Conference.pdf) · [来源3](https://iclr.cc/virtual/2025/poster/30467)

<a id="paper-2504-10483"></a>

## REPA-E: Unlocking VAE for End-to-End Tuning with Latent Diffusion Transformers

作者：Xingjian Leng、Jaskirat Singh、Yunzhong Hou、Zhenchang Xing 等6人。标识：`2504.10483v3`。首次公开：2025-04-14；所查版本更新：2025-10-22。

阅读层级：**摘要筛选**。范围：阅读原始摘要、核对问题与方法归属；未完成正文核读。

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：REPA-E 联合调整 VAE 与潜扩散生成器，尝试减轻固定重建潜空间对生成和表征的限制。

限制与判断：端到端调优增加训练变量；应单独检验重建、生成、语义对齐和细笔信息的变化。

原始来源：[来源1](https://arxiv.org/abs/2504.10483v3)

<a id="paper-2510-11690"></a>

## Diffusion Transformers with Representation Autoencoders

作者：Boyang Zheng、Nanye Ma、Shengbang Tong、Saining Xie。标识：`2510.11690v1`。首次公开：2025-10-13；所查版本更新：2025-10-13。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：[ICLR 2026（官方目录）](https://iclr.cc/virtual/2026/poster/10011890)

方法：RAE 将冻结视觉表征编码器与可训练解码器配对，在高维语义潜空间训练扩散 Transformer。

限制与判断：论文实际展示语义编码器也能良好重建，不能先验认定语义必丢细节；汉字细笔仍需专门测量。

片段定位：本地HTML提取文本起始行 31, 33, 39；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Technical Report; Project Page: https://rae-dit.github.io/

原始来源：[来源1](https://arxiv.org/abs/2510.11690v1) · [来源2](https://iclr.cc/virtual/2026/poster/10011890) · [来源3](https://arxiv.org/html/2510.11690)

<a id="paper-2511-13720"></a>

## Back to Basics: Let Denoising Generative Models Denoise

作者：Tianhong Li、Kaiming He。标识：`2511.13720v2`。首次公开：2025-11-17；所查版本更新：2026-01-07。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：JiT 以干净数据预测和适合像素空间的网络设计重审去噪模型，减少对高维噪声预测目标的依赖。

限制与判断：预测 x、噪声或速度的效果依赖数据维数和参数化；本轮没有确认其正式会议身份，不按题名推定。

片段定位：本地HTML提取文本起始行 178, 179, 193；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：Tech report. Code at https://github.com/LTH14/JiT

原始来源：[来源1](https://arxiv.org/abs/2511.13720v2) · [来源2](https://arxiv.org/html/2511.13720)

<a id="paper-2601-16208"></a>

## Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders

作者：Shengbang Tong、Boyang Zheng、Ziteng Wang、Bingda Tang 等10人。标识：`2601.16208v1`。首次公开：2026-01-22；所查版本更新：2026-01-22。

阅读层级：**正文片段选读**。范围：正文方法段落选读；行号为本地HTML提取文本定位，未覆盖全文证明和全部实验

来源归属：会议/期刊归属未由本轮官方来源确认；作者自报见下文。

方法：研究文本到图像 RAE 扩展，指出文本渲染的定向数据组成及高维表示噪声日程是关键因素。

限制与判断：摘要与正文片段支持这些设计动机；尚未核读全部规模实验。一般重建或语义指标不能替代细笔画实例和完整笔顺评价。

片段定位：本地HTML提取文本起始行 134, 135, 138；行号依赖提取版本，仅用于追踪，不能等同完整章节覆盖。

作者元数据备注（与独立核实分开）：website: https://rae-dit.github.io/scale-rae/

原始来源：[来源1](https://arxiv.org/abs/2601.16208v1) · [来源2](https://arxiv.org/html/2601.16208)
