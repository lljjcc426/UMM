# 已分析论文：会议索引与研究脉络

当前重点为CVPR、ICCV、ECCV、NeurIPS、ICLR、ICML。先用研究问题比较方法，再按会议查找具体论文。

主目录333篇论文／研究，327篇已完成所记录范围的核心阅读。其余6篇已按用户要求停止跟进；未计作完成。27项资源公开协议审查另列。

**先看[跨论文分析与20篇核心对照](synthesis.md)**，再进入会议或主题索引。所有单篇分析均可从下表点击到达。

## 六个会议

| 会议 | 已核会议论文／官方接收 | 作者声明录用 | Workshop／Findings／Demo等 |
| --- | ---: | ---: | ---: |
| [CVPR](cvpr.md) | 28 | 1 | 5 |
| [ICCV](iccv.md) | 15 | 0 | 1 |
| [ECCV](eccv.md) | 3 | 3 | 0 |
| [NeurIPS](neurips.md) | 33 | 2 | 2 |
| [ICLR](iclr.md) | 35 | 0 | 1 |
| [ICML](icml.md) | 17 | 0 | 0 |

已核会议归属共131篇；该列包含NeurIPS Datasets and Benchmarks及已核官方接收条目，具体类型逐条列出。ECCV2026的EvoTok为官方初步名单，出版检查仍保留。正式会议身份不表示本库读过其所有终版差异。

## 按研究问题查阅

| 主题 | 已完成论文 | 研究用途 |
| --- | ---: | --- |
| [汉字、字体与在线书写](handwriting.md) | 50 | 字形、风格、布局、轨迹恢复与识别生成联合；确定直接前作和强基线。 |
| [笔画、矢量与绘画过程](drawing.md) | 27 | 笔画表示、顺序生成、可微渲染、机器人绘画；区分矢量命令与真实书写事件。 |
| [UMM接口、架构与视觉表示](architecture.md) | 99 | 视觉编码、共享主干、AR/扩散/flow目标、跨模态接口；解释统一发生在哪里。 |
| [协同、推理与联合优化](synergy.md) | 38 | 正负迁移、交错推理、反馈与RL；用对照实验判断共享的实际收益。 |
| [视频理解、历史与运动控制](video.md) | 39 | 时序表示、历史条件、自生成前缀、轨迹控制及动态文字；连接过程建模。 |
| [评价、基准与训练数据](evaluation_data.md) | 43 | 任务定义、评判器、联合能力、图文交错数据与过程真值；检查指标实际测量什么。 |
| [生成基础、适配与效率](foundations_efficiency.md) | 31 | 扩散/flow理论、少步生成、缓存、LoRA与控制；在正确性约束下讨论成本。 |

七个主分类合计覆盖全部已完成论文；其他期刊、会议和预印本作为直接前作或机制背景保留。会议筛选服务阅读优先级，研究结论仍依据方法和实验。

## 当前范围与维护

- [停止跟进的6篇及原因](scope.md)：A06、F05、L002、L006、L021、L022。
- [全部逐篇笔记](../reviews/README.md)与[论文／资源验收台账](../evidence/reading_ledger_2026-10-19.md)。
- [研究进展](../project/STATUS.md)、[研究判断](../project/DECISIONS.md)与[实验计划](../project/EXPERIMENTS.md)。
- [历史批次](../project/history/reading_updates_2026-10-19_to_25.md)保存原来的阅读流水，不作为当前待办。
- 配置为[data/reading_guide_2026-10-25.json](../../data/reading_guide_2026-10-25.json)；执行`python scripts/render_reading_guide.py`更新索引。

## 会议归属容易混淆的记录

以下论文保留原有研究分析，未因模板、相关前作或二手标签而放进六会议主表。

| 记录 | 本次组织规则 |
| --- | --- |
| [B04 · AnyText2: Visual Text Generation and Editing With Customizable Attributes](../reviews/B04.md) | AnyText2未核接收，AnyText1的ICLR身份不移植。 |
| [U01 · Chameleon: Mixed-Modal Early-Fusion Foundation Models](../reviews/U01.md) | Chameleon为所读技术报告，未核正式ICLR身份。 |
| [U16 · Can Unified Generation and Understanding Models Maintain Semantic Equivalence Across Different Output Modalities? (VGUBench)](../reviews/U16.md) | VGUBench中的ICML模板/关键词不构成接收证明。 |
| [L021 · Write More at Once，公开投稿版本](../reviews/L021.md) | 公开投稿稿，未核录用；用户停止跟进。 |
| [L022 · Stylized Handwriting Generation of Arbitrary Structures and OOV Expressions，公开投稿版本](../reviews/L022.md) | 公开投稿稿，未核录用；用户停止跟进。 |
| [L053 · Timage: A Generative Text-in-Image Paradigm for Fine-Tuning Vision-Language Models；公开预印本版本](../reviews/L053.md) | Timage的arXiv comments只写ECCV，未独立确认录用。 |
| [L055 · Online Reasoning Video Object Segmentation；公开预印本版本](../reviews/L055.md) | ORVOS只有第三方ECCV标签，主源未确认。 |
| [L078 · Planting a SEED of Vision in Large Language Model](../reviews/L078.md) | 原SEED报告与后续ICLR SEED-LLaMA分别记录。 |
| [L091 · UGen: Unified Autoregressive Multimodal Model with Progressive Vocabulary Learning](../reviews/L091.md) | UGen被ICLR论文引用，未核其自身接收。 |
| [L098 · Selftok: Discrete Visual Tokens of Autoregression, by Diffusion, and for Reasoning](../reviews/L098.md) | Selftok是DDT-LLaMA扩展，前身CVPR身份不移植。 |
| [L101 · UniWeTok: An Unified Binary Tokenizer with Codebook Size $\mathit{2^{128}}$ for Unified Multimodal Large Language Model](../reviews/L101.md) | UniWeTok与同仓库BitDance为不同论文。 |
| [L112 · Lumina-DiMOO: An Omni Diffusion Large Language Model for Multi-Modal Generation and Understanding](../reviews/L112.md) | Lumina-DiMOO与后续dMLLM-TTS为不同论文。 |
| [L119 · UniFork: Exploring Modality Alignment for Unified Multimodal Understanding and Generation](../reviews/L119.md) | UniFork有under-review线索，未核正式接收。 |
| [L130 · PairUni: Pairwise Training for Unified Multimodal Language Models](../reviews/L130.md) | PairUni旧录用断言已撤回，正式会场未确认。 |
| [L134 · LVRPO: Language-Visual Alignment with GRPO for Multimodal Understanding and Generation](../reviews/L134.md) | LVRPO的ICML模板/关键词不构成接收证明。 |
| [L135 · Uni-Synergy: Bridging Understanding and Generation for Personalized Reasoning via Co-operative Reinforcement Learning](../reviews/L135.md) | Uni-Synergy不能继承前作UniCTokens的NeurIPS身份。 |
| [L140 · Beyond Layers: Position-Resolved Gradient Conflict and Position-Aware Modulation for Unified Multimodal Models](../reviews/L140.md) | Beyond Layers的ICLR格式不构成接收证明。 |
| [L145 · GENIUS: Generative Fluid Intelligence Evaluation Suite](../reviews/L145.md) | GENIUS的聚合站会场标签未由一手来源确认。 |
| [L166 · WorldBagel: Uncovering the Power of Unified Multimodal Models for Vision-Language-Action-World Modeling](../reviews/L166.md) | WorldBagel的arXiv当前注明Rejected by ECCV2026。 |
| [L168 · Puffin-World: Scaling a Unified Multimodal Model with Native 3D World States](../reviews/L168.md) | Puffin-World不继承早期Puffin的ICLR身份。 |
| [S004 · VidSketch: Hand-drawn Sketch-Driven Video Generation with Diffusion Control](../reviews/S004.md) | VidSketch仅ICML格式，未核PMLR条目。 |
| [L189 · AniClipart: Clipart Animation with Text-to-Video Priors](../reviews/L189.md) | AniClipart是IJCV期刊论文，未计作CVPR2025。 |
| [L193 · Towards Grand Unification of Multi-Human Activity Recognition](../reviews/L193.md) | 用户扩展稿与其ECCV2022前身是不同版本，未转移会议身份。 |
