# 2026-10-19 补录研究矩阵：研究对象、方法、比较边界

来源均链接原始论文/发表页或所有者制品；字段中“待核”具有实质含义。深度逐项见 [增量 JSON](../../data/research_additions_2026-10-19.json)、[质量审计](2026-10-19_quality_audit.md)、[精读索引](../handwriting/papers/README.md)。

## 任务与数据/训练/指标矩阵

| 研究（原始来源） | 研究问题与输入→输出 | 数据/分布 | 方法/架构 | 指标与基线 | 实验条件/证据深度 |
| --- | --- | --- | --- | --- | --- |
| [VidScribe](https://arxiv.org/abs/2609.36598) | 视频中文字质量评测：T2V/R2V/I2V/V2V 视频→评分 | 803，英语68%中文32%，12 因素 | OCR 轨迹+三路混合判定 | A1/A2/B/C/D，V2V E1/E2；7 商业 + 4 任务开源 | 原文 §3–4 和表，非笔顺事件 |
| [Calligraphy Bench](https://huggingface.co/datasets/haizelabs/calligraphy-bench) | 书法 Agent：参考图→tldraw 笔画 | 88 样本，20 书法家 | Tool agent + vision judge | recall/order/fidelity/preference；4 Agent | API 工具、完整裁判事件输入待核 |
| [VideoSketcher](https://github.com/rhfeiyang/VideoSketcher) | ordered drawing steps→逐步绘制视频 | 合成图形+7 真实艺术画样本 | LLM 计划 + Wan2.1-14B LoRA，1.3B AR | 精确主表及消融待核 | README：480p/81f/50steps；两路线非同一模型 |
| [VidSketch](https://arxiv.org/abs/2502.01101) | 已给草图序列+文本→动画视频 | 每动作约 8–12 视频，作者报告 | VDM+inflated T2I adapter+TempSpatial Attention | 量化主表待核 | arXiv 方法已读；与从空白绘制任务不同 |
| [TextDiffuser](https://papers.neurips.cc/paper_files/paper/2023/hash/1df4afb0b4ebf492a41218ce16b6d8df-Abstract-Conference.html) | prompt→静态有字图 | MARIO-10M、MARIO-Eval | Layout Transformer→diffusion | OCR+视觉，人评；表待核 | NeurIPS 2023 正式摘要 |
| [GlyphControl](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8951bbdcf234132bcce680825e7cb354-Abstract-Conference.html) | glyph+文本→静态有字图 | LAION-Glyph | SD + glyph conditioning | OCR/CLIP/FID vs DeepFloyd IF，表待核 | NeurIPS 2023 正式摘要 |
| [AnyText2](https://github.com/tyxsspa/AnyText2) | 文本/排版条件→静态文字图 | 需读完整原文 | 字形表示+条件控制 | 原文表待核 | 主目录 B04 已有 |
| [DiffInk](https://arxiv.org/abs/2509.23624) | 文本、风格→在线书写行轨迹 | CASIA 相关线上轨迹 | InkVAE + InkDiT + GMM | 内容识别 AR；DDIM 1/2/5/10 步 | 现有详细笔记；AR 非规范顺序 |
| [OLHWG](https://arxiv.org/abs/2410.02309) | 文本行→排版+轨迹 | CASIA online | AR Layout + 1D Diffusion | 内容/风格，具体原文表待核 | ICLR 2025 前作 |
| [UniCalli](https://arxiv.org/abs/2510.13745) | 书法列图↔静态风格字形 | 多字书法裁剪及合成 | 双向噪声/扩散共享表征 | 静态识别/生成指标 | 无实际书写视频时序 |
| [OnOff](https://arxiv.org/abs/2608.03198) | 在线笔迹/参数→毛笔墨迹图 | 真实轨迹和渲染资源，详见旧卡 | contact + render + optional enhancement | 外观/渲染，详见原文 | 不能把增强后无错序当作已证 |
| [BCSS](../reviews/S007.md) | 静态字图→六类mask | HF1212图；论文1322图/十类，笔画总数冲突见笔记 | 类别多标签资源 | HF外部130图无GTmask，不能套论文分数 | 重叠类别mask，无实例时间身份 |
| [Wuji VAM](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819) | 人参考视频+机器人状态→未来视频+54维动作 | 487 teleop / 896 ego，数字0–9 | Wan2.2视频DiT + ActionMoT | snapshot MAE/SSIM，未见真实笔顺率 | 模型卡，无完整任务对比 |
| [Ketaba-OCR](https://aclanthology.org/2026.nakbanlp-1.21/) | 阿语手稿行图→文本 | 18057 final train、2671 blind | QLoRA/DoRA/RSLoRA HTR+6模型集成 | CER/WER，基线+辅助 HTR | 正式 workshop 论文+源代码 |
| [Qari-OCR-LoRA](https://github.com/HasanBGit/QARI-OCR-LoRA) | 阿语行图→文本 | 同团队阿文记忆录 | Qwen2-VL 2B LoRA/DoRA/RSLoRA | blind CER .2635/WER .5521 | 附属适配器，不具有视频输出 |
| [AnimCJK](https://github.com/parsimonhi/animCJK) | Unicode/地区→SVG 逐笔动画 | CJK 多地区 SVG | path/clip reveal，无学习模型 | 顺序约定/覆盖范围 | 跨地区笔顺不能强行混并 |
| [KanjiVG](https://github.com/KanjiVG/kanjivg) | Japanese Kanji→SVG paths | KanjiVG | 矢量实例/部件属性 | 数据工具，不适用 FID 排名 | CC BY-SA 3.0，地区约定 |
| [SceneDAPR](https://github.com/DSAIL-SKKU/SceneDAPR) | 真实场景素描→带顺序注释 | 1399 幅场景，6420 物体标注，官方 README | 真实 stroke sequence 与分割 | 具体基准表待核 | 非中文字，需要审计原始时间字段 |
| [sketch-diffusion](https://github.com/ark60/sketch-diffusion) | Quick Draw 轨迹→轨迹/GIF | cat/bus/rabbit，作者 README | Transformer DDPM，1000 步，8 层 | FID/KID（实际独立结果待跑） | 无同行评审发表确认，仅 notebook |
| [SketchEdit](https://github.com/CMACH508/SketchEdit) | stroke sketch + edit condition→矢量编辑图 | QuickDraw 类，数据配置待核 | VAE/UNet diffusion；具体论文待读 | 待核 | IJCAI 2024 作者 README，尚未核会议正式页 |
| [MoSketch](https://github.com/jyliu-98/MoSketch) | 静态多对象草图→对象动画 | 60+500 草图处理资产，仓库 README | 分解、笔画对象分配、运动计划 | 完整指标待核 | ICCV2025 仓库声明，非逐笔从空白 |
| [Stroke-Seg论文L184](../reviews/L184.md) | 静态书法+先验→十类mask | 872训练/150验证/300外部 | PKV+multi-label+BCE/Dice | TSR验证.982/外部.897，未知字.831 | 数据/代码S007/S016另记，未给时间过程 |

## 如何从这些前作推导“可以做”的方向

**交集更有区分力**：VideoSketcher 已有逐步画出来的视频；Calligraphy Bench 已有中文逐笔动作与笔顺评分；BCSS 有静态笔画类别/重叠分割；VidScribe 有视频文字多维判定；Wuji VAM 有视频加动作的工程权重。新工作要拿出一个当前相邻方法**不能在同输入条件下一步解决**的实证问题，例如：

- 在保持每帧终态/最终 OCR 完全相同的反例中，从原始 RGB 时序识别已发生的具体笔画与首错事件。
- 把笔画规范区域、实际生成像素、行动计划一致地约束为一个可检验闭环；并说明对 VideoSketcher+规则 oracle 与可编辑渲染器的增益。
- 当模型生成极短/密集/交叉笔画时，量化时间采样不可识别率，和显式动作表示是否真正提升可观测信息。
- 同等数据、调用与训练 FLOPs 下，独立 VLM+视频生成器与共享 UMM 是否有额外协同收益；若没有就如实选择最简单方案。

这些全是**假设**，现阶段没有独立实验支持“已成功”。从失败子集/related work 重复限制获得候选，然后先查有无已经覆盖的方法，再设计反证。

## 第二十七批接口补充

| 工作 | 输入→输出 | 必须区分的评价 |
| --- | --- | --- |
| L186 G-HTR | 静态字图→含宽度/penstate轨迹→外部机器人控制 | 轮廓/DTW与真实笔序、压力/时间 |
| N08 HierarchicalO2O | 静态字图+先验→M/L参数轨迹 | Sw三项与全序，速度统计与时间真值 |
| U29 MIRROR | 原图+问题→工具标记原图→答案修订 | 定位/理解与场景生成 |
| U30 LatentUM | 文字/图→语义码/文字→可选RGB | 语义码正确与decoder像素正确 |
| R08 U1.5 LoRA | 基础权重+适配器→8步图/编辑 | 基础模型榜分与适配器实际质量 |

## 第二十八批任务与评价补充

| 工作 | 输入→输出 | 必须区分的协议 |
| --- | --- | --- |
| N01 UniCalli | 标准字/书法/框latent双向→静态书法/字库识别 | 全论文模型与无pred_box公开base、分布内与外部识别 |
| N02 OnOff | 文字+参考→轨迹/brush参数→静态图/robot | 渲染代理与传感物理，FID与CER |
| N03 DeepCalliFont | 参考图/轨迹→目标图/轨迹 | 草书与常规FID，伪连笔与真实时序 |
| N04 VidScribe | 4类视频文字任务→11指标+2编辑probe | 空间字形拓扑与时间规范笔事件 |
| N05 VTRBench | 多载体prompt→video→CoQ/有界WER | 最清楚一次与全帧，单次与Agent成本 |
| N06 Videozero-shot | 首帧+prompt→黑盒video | APIrewriter、pass1、oraclebestframe/pass10 |
| N09 TextAnimator | glyph/position/camera→场景文字video | 完整字符串动画与逐笔生成 |
| L011 DrawThisFirst | 图/文指令→有序polyline | 区域/部件/笔粒度，弧长与时间/碎片 |
| S001 Ketaba | 历史稿行图→Unicode转录 | 正式论文/模型制品、官方corpus与按行CER、PseudoGT |

## 第二十九批：补齐九项真实任务接口

| 工作 | 输入→输出 | 关键协议边界 |
| --- | --- | --- |
| L026 UniVideo | 多模态语义/视觉参考→视频；冻结MLLM理解 | v4与旧版、prompt改写、frozen理解和joint收益 |
| L028 Lance | 交错文字/图/视频→文字或视觉latent | active/总参数、图像RL/视频、训练比例 |
| L044 Calligraphy Bench | 参考书法+MCP工具→可编辑stroke画布→评分 | canonical几何/书家图像、匹配分母、计数差异 |
| L175 XMPFont | 参考字图+类别序列预训→静态字体 | 类别顺序/真实时空、训练字体数 |
| L176 LVLM在线识别 | 已知轨迹→坐标串/RGB→转录 | 识别/生成、重采样与时间信息丢失 |
| L177 PaintFlow | 当前画布/mask/sketch/ref→新画布 | 静态局部编辑/真实绘制过程 |
| L179 UMText | 多模态设计请求→布局条件→静态设计图 | 全pipeline域外、RCI实现、共同Planner |
| S004 VidSketch | 草图关键帧+首帧→自然动画 | 草图动画/画草图过程、论文/硬编码入口 |
| H001 CoFRIDA-Sharpie | 模型卡描述→编辑权重制品 | 基础模型字段冲突、实际机器人完整链未给 |


## 第三十批补充

第三十批：L187是条件差异分布蒸馏，student保原图但不生成新图；L188显式I2V目标拟合已有SVG；L189低维轨迹/ARAP视频SDS；L190静态艺术字双区域扩散，I2V仅应用；R09为模拟动作与低频RGB对齐资源。均已按实际输入/输出、成本和指标与规范笔顺任务区分。
