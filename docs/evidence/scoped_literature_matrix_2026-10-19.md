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


## 第三十一批补充

第三十一批七项接口区分：静态字图、单字后布局、直接整行、SVG轮廓续写、静图恢复。DiffInk已正式ICLR2026、LVGM已正式WACV2026；不把预印本状态/数据规模或公式解释沿用到正式版。


## 第三十二批补充

第三十二批区分字级/行级在线扩散、已知模板静态笔分割、静态书法三标签和LaTeX结构轨迹；Moyun为McGE附属workshop，资源规模不同于实际训练子集。Calliffusion已有三因素与新字符迁移；2020已有在线手写扩散。


## 第三十三批补充

AnyText2静态图、KineTy模板派生Latin RGB动效、DynamicTypography字母SVG形变、InversePainting真实粗画布AR、AnimatePainter合成先验短clip分别列界。DDC的真实参考与理论参考不同，不跨论文排名；这五项均未提供规范逐笔执行验证。


## 第三十四批补充

BAGEL双专家共享attention、Show-o2同VAE双路径、ReCA原架构后训按接口分列；BAGEL导航额外FT，Show-o2视频2B与7B不同，ReCA无动作/视频指标。统一多模态已多路线，规范事件协同需要直接新证据。


## 第三十五批补充

Hyper-Bagel蒸馏、FlashU任务剪枝与缓存、UniCache异质KV、Reflection多轮text/flow RL均已有。静态编辑链不等视频或规范笔事件；统一模型协同已有直接先例，后续创新需具体到可执行事件和等成本强基线。


## 第三十六批补充

HunyuanVideo1.5字形条件视频、LTX2联合声画、VACE统一视频编辑、WanMove点轨迹控制已有，分别不等规范笔顺。VACE正式ICCV2025、WanMove NeurIPS2025；自动均值、人评/控制/物理事件目标分开。


## 第三十七批补充

SF历史分布、SGF历史写入梯度、Salt少步组合/cache质量、WanR1任务奖励已有不同贡献；不能将长视觉一致性或embedding代理当规范笔顺/真实执行正确。WanR1 T1/T2/Target/MF有负项与表文冲突，Salt semantic/dynamic有退化；需强基线与事件级检验。


## 第三十八批补充

E01平均场一NFE图像、E02复合回归/灵活CFG、E03观测条件动作蒸馏、新D09长视频角色解耦，均为邻近机制，无规范汉字笔顺视频完整证据。iMF系统1.72含800ep/更高GF，SGF+双参数与动态下降、CP低方差跨域负例需要进入优势条件与反证实验。


## 第三十九批补充

E04离散概率流支持token/像素，不保证事件约束；E05文字到语音的对齐与采样，不提供字形或视频；E06视频生成内部残差缓存，需标定及局部事件检验；E07二值细长结构空间loss，保证受骨架条件限制，无法评价笔顺。四篇已完成核心三遍，各记录七项协议和五条检查，均无本项目模型复现。


## 第四十批补充

F01静态矢量参数梯度与栅格监督生成；F02逐图曲线/Gaussian拟合非训练视频模型；F03真实笔触可执行规划/闭环；F04模拟删笔适配IP2P再接FRIDA，是分层强基线。四项均未验证规范汉字笔顺/书写视频分布或共享UMM协同优势。各核心三遍完成，版本/未报条件/负结果保留；无独立复现。


## 第四十一批补充

G014为短在线素描VAE/AR，G015静态图→模拟笔触分解，F05英文独立字符轨迹→连笔后处理，H001图像条件共绘LoRA制品；均无直接规范汉字笔顺RGB视频证据。详见[第四十一批矩阵](sketch_sequences_painting_rl_and_lora_artifact_2026-10-20.md)。


## 第四十二批补充

补G016局部集合摊销/G017少笔语义优化/F06双路径renderer+OT逐图优化/F07黑盒RL程序。监督来源、笔触表示、数据分布、评价和预算见[第四十二批矩阵](neural_painting_sets_semantics_and_programs_2026-10-20.md)；渲染过程没有直接规范文字/真实视频证据。


## 第四十三批补充

G001噪声链/G002连续score与PC/ODE/G005条件速度回归/G006rectification-reflow-distill，按静态数据、接口、理论假设、NLL/FID与预算分列。详见[第四十三批](diffusion_score_flow_and_rectification_2026-10-20.md)。以上没有直接规范笔顺/真实动作视频证据。


## 第四十四批补充

G003感知压缩与条件潜扩散／G004类条件latent Transformer／G007端点一致CD-CT／G008固定checkpoint数值采样／R10decoder-only资源，按输入输出、数据／预训练、参数预算与评价分列。见[第四十四批](latent_transformer_consistency_and_solver_audit_2026-10-20.md)；没有规范书写时序／动作的直接实验。


## 第四十五批补充

G009像素整块扩散/条件重建引导；G010逐帧E潜扩散+时间D/分层插值；G011兼容SD共享motion/domain空间LoRA/时间MotionLoRA。按数据/条件/版本/成本及静态与时间指标分列；见[第四十五批](video_diffusion_temporal_transfer_and_motion_adapters_2026-10-20.md)。三项均未验证规范笔顺过程。


## 第四十六批补充

G012 3D VAE/Expert AdaLN/full attention/Frame Pack/数据筛选及EUS，R11工程微调/卡config单列；35M视频+2B图像与用户少样本微调不同。过滤Text Dominated、caption2秒采帧、公开原版与1.5帧率/时长等差异见[第四十六批](cogvideox_video_compression_data_and_finetuning_2026-10-20.md)。


## 第四十七批补充

G013 Wan2.1：通用OCR过滤＋专用中英文字图/视频分支，3fps密集caption，C16/时间4因果VAE、共享调制full-attention DiT/FM。WanBench无独立笔顺/OCR过程指标。I2V/VACE/个性化/相机/Streamer/V2A各任务输入、数据与训练边界分开；详[第四十七批](wan_visual_text_flow_training_and_evaluation_audit_2026-10-20.md)。


## 第四十八批补充

G018–G021分别对应更新表示、冻结权重存储、模长/方向参数化、rank缩放；语言/视觉理解/SDXL静态实验不直接验证书写视频事件。四者方法、训练/数据/主结果/消融、优势条件与反例见[第四十八批](parameter_efficient_adaptation_rank_quantization_and_weight_decomposition_2026-10-20.md)。


## 第四十九批补充

G025为静态二维条件图像，G026为类条件ImageNet引导；均没有规范书写时间监督。原图/条件提取/hint/VAE与真实事件分列，成本按两支计算和可训练对象；详[第四十九批](spatial_control_classifier_free_guidance_and_protocol_gaps_2026-10-20.md)。


## 第五十批补充

G028/G029均历史静态图任务，GAN快采样/对抗反馈与VAE摊销推断/表示学习不同；原主结果的估计器、样本SEM/fold SEM及学习曲线范围分别记录。理论不直接保证视频细线/事件，详[第五十批](gan_vae_theory_estimation_and_video_representation_boundaries_2026-10-20.md)。


## 第五十一批补充

G031评价16维、G032评价视频分布＋SCV可控任务，均非新书写生成器。官方源码snapshot、arXiv/正式表差异、人评model排行/样本能力、固定端点总分/雷达重标分列。详[第五十一批](video_evaluation_vbench_fvd_protocol_and_scope_2026-10-20.md)。


## 第五十二批补充

新增G033评价分析/嵌入替换与工程制品，不新增视频生成器；数据六既有集，四生成器仅诊断，原T3百分比纠错与真实分数分列。详[第五十二批](content_bias_fvd_temporal_sensitivity_and_resampling_2026-10-20.md)，core120/written122。


## 第五十三批补充

G034为I2V/可信评价、ImageSuite及Long工程关联；G031原VBench和后继2.0分开。输入图默认比例选择、整图DINO/DreamSim、camera启发式与事件真值边界见[第五十三批](vbench_plus_i2v_trustworthiness_protocol_and_implementation_2026-10-20.md)。


## 第五十四批补充

G035已覆盖两动作顺序、动态状态、运动后果、实例保持和通用/专用异常专家；严格笔事件须建立局部时间/轨迹真值及新任务增益，不能再把以上概念整体当空白。见[第五十四批](vbench2_intrinsic_faithfulness_events_and_conditional_scores_2026-10-20.md)。


## 第五十五批补充

U01统一AR与U05混合CE/连续diffusion均为静态图文共享模型，已有组件/预算消融；负迁移较小不等正迁移，规范书写需细字/事件与时序mask新证据。见[第五十五批](chameleon_transfusion_shared_model_cost_and_claim_audit_2026-10-20.md)。


## 第五十六批补充

Janus解耦encoder/共享AR骨干与Show-o混合NTP/MTP均已有，不能据统一称普遍正迁移。Show-o GenHowTo关键帧微调/8fps短视频tokenizer必须计入相关先例，但只有定性证据。见[第五十六批](janus_showo_representation_video_and_math_audit_2026-10-20.md)。


## 第五十七批补充

InkSight从静态照片输出数字墨迹，VideoSketcher直接生成RGB渐进绘画且已有多笔帧19.58%/36.96%量化。规范事件/执行验证要在现有任务及局限上明确增量；原始轨迹、合理历史和规范顺序需分开。见[第五十七批](inksight_videosketcher_trajectory_events_and_resource_audit_2026-10-20.md)。


## 第五十八批补充

SketchAgent已有显式有序stroke/语义ID/协作，并正式测试字母串复杂度和网格；ProcessPainter已有文本/终图/半成图到绘画关键帧、艺术家过程适配。新颖性需要具体落在严格事件/真实执行和可验证收益。见[第五十八批](sketchagent_processpainter_protocol_and_claim_audit_2026-10-20.md)。


## 第五十九批补充

PaintsAlter已经处理多源多query/过去未来/非连续绘画状态，StrokeNUWA已压缩矢量命令并AR生成；规范笔画/真实执行须额外事件监督和独立评价，不能靠任务简称判断。见[第五十九批](paintsalter_strokenuwa_query_representation_and_metrics_audit_2026-10-20.md)。


## 第六十批补充

DiffSketcher已有文本→可微矢量素描；Diff-Font已有中/韩计数条件静态字体扩散。前者整体参数迭代，后者类型计数；均需额外有序事件与真实执行证据才能支持规范笔顺视频。见[第六十批](diffsketcher_difffont_condition_process_and_configuration_audit_2026-10-20.md)。


## 第六十一批补充（2026-10-21）

FontDiffuser已有unseen-font/unseen-character静态生成；DiffBrush已有英/中文整行生成与行/词判别。静态文字空间顺序和真实落笔时序分别建模，不以3D层或diffusion称视频。见[第六十一批](fontdiffuser_diffbrush_generalization_metrics_and_release_audit_2026-10-21.md)。


## 第六十二批补充（2026-10-21）

Emu3正式扩展已覆盖交错生成、空间变序/修复与CALVIN动作，但并无规范书写视频/真实机器人笔顺评价；Janus-Pro已有数据/训练/规模扩展，不能把继承Janus结构计新贡献。见[第六十二批](emu3_januspro_versions_training_and_causal_audit_2026-10-21.md)。


## 第六十三批补充（2026-10-21）

AnyText静态指定字形/位置/编辑与OCR感知，v1.1多更新未独立归因；UniVid一般视频生成/问答与外部LLM检索，不含规范书写事件评价。四组UniVid同名工作按作者/编号区分，见[第六十三批](anytext_univid_protocol_code_and_namesake_audit_2026-10-21.md)。


## 第六十四批补充（2026-10-21）

N10已有合成文字视频监督路线但协议和定量证据不足，其无既有工作主张须纳入2024N09；N11静态双模式骨架控制/跨字符形状和N12静态修复均是先例，无严格事件/笔顺结果。见[第六十四批](calligraphy_inpainting_and_video_text_evidence_audit_2026-10-21.md)。


## 第六十五批补充（2026-10-21）

G036是静态无mask再训练采样器，G037是线性恢复理论/二维toy；均不生成规范笔事件。RePaint已有同预算往返vs放慢对照，书法修复需强对照及已知错笔条件；理论Th8局部反例与两状态收缩分开。见[审计](repaint_sampling_and_linear_theory_audit_2026-10-21.md)。


## 第六十六批补充（2026-10-21）

N06通用视频符号分笔是先例但无规范事件评价，N07真实200Hz/压力/hover测量与N13无墨迹反推都约束可观测性选题；三者识别/测量/生成任务不同。见[审查](video_reasoning_and_handwriting_observability_audit_2026-10-21.md)。


## 第六十七批补充（2026-10-21）

U08跨领域交错推理数据覆盖科学/2D/3D/逻辑；Anole主表提升与BAGEL负面报告并存。静态辅助图不提供视频事件监督；GT图文前缀收益也不等于自主生成收益。见[审查](zebra_cot_negative_results_and_artifact_audit_2026-10-21.md)。


## 第六十八批补充（2026-10-21）

G030独立噪声RNN用于视频/规划/模仿/时序，不能把规划主表当视频量化或无限滚动证明；main注意力与paper原RNN分开，GT已生成历史的可靠性是跨域可检验变量。见[审查](diffusion_forcing_theory_protocol_and_versions_2026-10-21.md)。


## 第六十九批补充（2026-10-21）

G038：K600/RE10K/动作MC与果实交换；视频v目标、机器人x0；K16帧50K、长64帧1024、MC125生成帧1024的FVD不能横比。HG-f部分噪声可损坏细笔画，需字符/事件留出；同预算比较生成质量、动态正确性与真实执行。见[审查](history_guided_video_diffusion_audit_2026-10-21.md)。


## 第七十批补充（2026-10-21）

L086/L092为文字回答与静态图像，RF积分/空间mask次序均无真实书写动作语义；语义教师/LLM增强、VAE压缩和重caption成本纳入条件，终态/语义/严格事件/执行分层。见[审查](janusflow_harmon_shared_representation_audit_2026-10-21.md)。


## 第七十一批补充（2026-10-21）

G027是静态32/64²U-Net扩散设计空间，不含书写事件或视频。数值时间、FID/NFE摘要、训练/搜索曝光与任务事件分列，原ADM与新ImageNet参考资料差异保留。


## 第七十二批补充（2026-10-21）

L185静态图像在线RL，噪声动作并无真实笔语义；JPEG/美学/VLM代理与严格时序事件分列，TPU主全UNet、GPU后续LoRA及HF公开不同轮次制品分版本。


## 第七十三批补充（2026-10-21）

L001静态字图→轨迹、English已见类别/Tamil适配，L004style+text+boxes→offset/pen；二者均不作为已解决真实RGB规范笔顺视频或共享UMM协同证据。布局检测、采样密度、方向量表与版本缺项分列。


## 第七十四批补充（2026-10-21）

L180文本/画布动作六任务、生成仅qual；G024多数据各自重训、无序矢量静态草图。明确ICCV Workshop/AAAI主会身份，表中FID与PR反例、运行/metric实现和各自预算缺项。


## 第七十五批补充（2026-10-21）

L005 IAAI2014静态字/2风格/20读者；L015固定v3 80/10/10、3骨干/人评/效率，原2025题名/90%/PDP不直接拼接，WACV2027作者声明未当正式论文集核实。


## 第七十六批补充（2026-10-21）

L063正式NeurIPS/T3 WISE(Natural)非文化、完整语言/理解反例；L029固定v3主表.77→.83/WISE.70→.76及退步，数据62213/混合teacher/131NFE的条件分别记录。


## 第七十七批补充（2026-10-21）

L047单字体500句/单书家397字不同模态，日志CER.6735/位置准确.2352，公开树无MP4；L184外部300/未知150 TSR.831，与验证.982/后续6类加工资源分别记录。


第七十八批（2026-10-21）：VD .11的文生图FID改善与variation大幅改善、文字定性分开；Emu按base/I与star、shot分行，保留NExT/OKVQA及MMVet OCR/空间/数学退步。见[审查](versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)和[单篇L075](../reviews/L075.md)、[L077](../reviews/L077.md)。


第七十九批（2026-10-21）：LaVIT COCO FID7.4含四选一；MMLU仍降1.5；正式LLaMA1与公开LLaMA2-v1/v2分组，v2多项理解下降。见[审查](lavit_dynamic_tokens_and_version_audit_2026-10-21.md)和[单篇L079](../reviews/L079.md)。


第八十批（2026-10-21）：UniFlow平均差6.05分、MMEP退步、有CFG生成退步、不同下游tokenizer/模型版本；一步decoder与256AR分别计。见[审查](uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)和[单篇L072](../reviews/L072.md)。


第八十一批（2026-10-21）：TokenFlow共享索引/独立LLM、相对7.2%与教师差距，TQA/重建和采样反例。见[审查](tokenflow_shared_indices_and_claim_audit_2026-10-21.md)和[单篇L094](../reviews/L094.md)。


第八十二批（2026-10-21）：MetaMorph连续视觉响应/SD1.5可视化、低T2I数据但非低总数据、负迁移/重复行。见[审查](metamorph_synergy_and_data_budget_audit_2026-10-21.md)和[单篇L090](../reviews/L090.md)。


第八十三批（2026-10-21）：扩散三框架与14任务节、四轴分类、无统一实测的综述边界。见[审查](diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)和[单篇G022](../reviews/G022.md)。


第八十四批（2026-10-21）：架构/训练/采样/部署全流程成本、表格NFE/条件与正式版边界。见[审查](diffusion_efficiency_full_pipeline_audit_2026-10-21.md)和[单篇G023](../reviews/G023.md)。


第八十五批（2026-10-21）：图文五种分布、CFG调用和同预算因果边界，非书写视频。见[审查](unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[单篇L076](../reviews/L076.md)。


第八十六批（2026-10-21）：轨迹中心/实体身份/事件接触和留墨分别定义，OpenSora/Cog及主表/消融协议分开。见[审查](tora_motion_binding_and_process_boundary_audit_2026-10-21.md)、[L034](../reviews/L034.md)/[L035](../reviews/L035.md)。


第八十七批（2026-10-21）：首图轨迹→视听联合、外观变形资源、绘画事件与UMM协同分别界定。见[审查](tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)、[G039](../reviews/G039.md)/[R12](../reviews/R12.md)。


第八十八批（2026-10-21）：相机407/对象283组合、独立轨迹数量与UMM/书写任务边界。见[审查](motionctrl_camera_object_and_observability_audit_2026-10-21.md)、[L039](../reviews/L039.md)。


第八十九批（2026-10-21）：四模态离散接口与视频/书写事件区分；base/chat和训练阶段独立。见[审查](unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)、[L058](../reviews/L058.md)/[L059](../reviews/L059.md)。


第九十批（2026-10-21）：静态图像表示/编辑与连续书写过程、分版本模型及flat/history区别。见[审查](seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[L060](../reviews/L060.md)/[L061](../reviews/L061.md)/[G040](../reviews/G040.md)。


第九十一批（2026-10-21）：静态轮廓设计、优化迭代MP4、循环字体动画和书写事件四者区分。见[审查](semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[L051](../reviews/L051.md)/[L052](../reviews/L052.md)。


第九十二批（2026-10-21）：静态单字/多字/非Latin栅格艺术字，逐例微调与通用Express分开。见[审查](dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[G041](../reviews/G041.md)。


第九十三批（2026-10-21）：知识条件单向迁移、连续patch/离散输出和任务移除正负效果。见[审查](metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[L062](../reviews/L062.md)、[L074](../reviews/L074.md)。


第九十四批（2026-10-21）：离散语义码/图像条件静态解码、抽帧视频理解，多图序列不外推连续视频或笔顺。见[审查](seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[L078](../reviews/L078.md)、[L082](../reviews/L082.md)。


第九十五批（2026-10-21）：静态query排版服务VQA与已观测轨迹服务视频QA，未做视频/笔顺生成；分表示与额外信息。见[审查](timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[L053](../reviews/L053.md)、[L054](../reviews/L054.md)。


第九十六批（2026-10-21）：MC基准造题与视频坐标理解单列，六QA含原3D姿态，不归为视频/笔顺生成。见[审查](autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[G042](../reviews/G042.md)、[G043](../reviews/G043.md)。


第九十七批（2026-10-21）：静态图理解/AR语义加flow像素生成，与对象组合评价分列；均无视频/规范笔顺实验。见[审查](manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)、[L064](../reviews/L064.md)、[L071](../reviews/L071.md)。


第九十八批（2026-10-21）：Qwen输入视听输出文字/语音；Emu图文关键帧/DiDA/SD3.5像素解码/Wan视频解码分开，具身无低层动作或执行成功率。见[审查](qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[L065](../reviews/L065.md)、[L066](../reviews/L066.md)。


第九十九批（2026-10-21）：两项静态图文/交错评测，非新视频生成模型；正确性对称、内容一致、实际状态理解、目标完成与内部机制分别定义。见[审查](xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[L067](../reviews/L067.md)、[L068](../reviews/L068.md)。


第一百批（2026-10-21）：两项协同/规划Benchmark，均无规范书写视频模型；直接回答、有辅助回答、联合质量与成本分开。见[审查](unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[L069](../reviews/L069.md)、[L070](../reviews/L070.md)。


第一百零一批（2026-10-21）：四模态接口与图文交错联合学习分开；视频CLIPSIM/FID、图像FID/理解指标不能替代笔顺事件。见[审查](nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[L080](../reviews/L080.md)、[L081](../reviews/L081.md)。


第一百零二批（2026-10-21）：连续AR+独立扩散器与离散RQ空间/深度AR、base/Chat/Gen权重、视频展示与视频主量化分开。见[审查](emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[L083](../reviews/L083.md)、[L085](../reviews/L085.md)。


第一百零三批（2026-10-21）：CalliBench识别/文化VQA与L044 Calligraphy Bench区分；字符阅读顺序、空中轨迹、规范字内笔顺分开。见[审查](callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[L045](../reviews/L045.md)、[L046](../reviews/L046.md)。


第一百零四批（2026-10-21）：静态图像的离散统一decoder、连续输入/离散输出和扩散detokenizer；交错例图/未来方向不等同书写视频。ILLUME+/X发现池候选待精读。见[审查](liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[L088](../reviews/L088.md)、[L089](../reviews/L089.md)。


第一百零五批（2026-10-21）：渐进视觉词表、图像级GRPO、语义AR+FLUX与长文字图像基准；静态文字覆盖不等同布局/顺序或视频笔顺。见[审查](ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[L091](../reviews/L091.md)、[L093](../reviews/L093.md)。


第一百零六批（2026-10-21）：联合训练tokenizer、连续理解接口与双RVQ离散理解/生成；共享视觉主干、双词表和双输出head分别辨明，静态能力不推笔顺。见[审查](qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[L095](../reviews/L095.md)、[L096](../reviews/L096.md)。


第一百零七批（2026-10-21）：欠指定触发运动推断与仿真对齐长视频；允许改轨迹、区域latent锚定和规范笔顺任务分开。见[审查](motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[L036](../reviews/L036.md)、[L037](../reviews/L037.md)。


第一百零八批（2026-10-21）：参考条件离散表示、视频重建/未来预测/外观编辑分开；已有字保真不代表新文字/笔顺生成。见[审查](reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[L038](../reviews/L038.md)。


第一百零九批（2026-10-21）：开放域文字/图像/轨迹与额外mask实体运动；艺术绘画外观不等于逐笔过程，二维实体控制不保证接触/旧墨迹/笔顺。见[审查](dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[L040](../reviews/L040.md)、[L041](../reviews/L041.md)。


第一百一十批（2026-10-21）：持续文字T2V/Ref2V评价；动态/渐进书写为需新GT的扩展，无新生成器/UMM。见[审查](textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[L042](../reviews/L042.md)。


第一百一十一批（2026-10-22）：视频局部文字替换Benchmark+参考编辑器；手写外观与笔画过程区分，关联已录L182 STRIVE，GlyphMastero/VidTextPres待原文/别名核验。见[审查](vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[L043](../reviews/L043.md)。


第一百一十二批（2026-10-22）：双输入共享AR静态理解/生成；workshop与主会区分，OCR读取与指定字/时序生成分开。见[审查](unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[L097](../reviews/L097.md)。


第一百一十三批（2026-10-22）：扩散渐进码/静态纯AR与视觉RL；前身正式版关联，视频物理/笔顺为后续非本作已完成能力。见[审查](selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[L098](../reviews/L098.md)。


第一百一十四批（2026-10-22）：480码递归表示/静态共享AR，关联L098同家族版本；非真实笔顺或已完成视频生成。见[审查](ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[G044](../reviews/G044.md)、[L098](../reviews/L098.md)。


第一百一十五批（2026-10-22）：固定SigLIP索引与适配embedding、静态AR→扩散；外部decoder/大词表成本，未验证文字视频或笔顺。见[审查](unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[L099](../reviews/L099.md)。


第一百一十六批（2026-10-22）：连续VAE→SigLIP2共享表示、图文/视频任务；静态文字与VBench不提供笔顺GT。见[审查](tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[L100](../reviews/L100.md)。


第一百一十七批（2026-10-22）：隐式128bit×64位置tokenizer，Gen/Edit/Chat分别SFT，无文字视频或笔顺评价。见[审查](uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[L101](../reviews/L101.md)。


第一百一十八批（2026-10-22）：4/16残差前缀静态表示；理解/生成分别入口，没有书写时序或单checkpoint正协同证据。见[审查](evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[L102](../reviews/L102.md)。


第一百一十九批（2026-10-22）：通道连续压缩、理解原特征/编辑压缩条件、FLUX/VAE两级解码，未测视频。见[审查](unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[L104](../reviews/L104.md)。


第一百二十批（2026-10-22）：直接像素理解/图像生成/编辑，不能把原TUNA VAE视频归Tuna2。见[审查](tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[L105](../reviews/L105.md)。


第一百二十一批（2026-10-22）：保留联合DINO理解encoder、AR表示前缀→像素flow，静态生成非书写过程。见[审查](representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[L106](../reviews/L106.md)。


第一百二十二批（2026-10-22）：图像/视频ViT时间压缩、双教师、Sem内编辑交互，17帧视频不等逐笔过程。见[审查](hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[L107](../reviews/L107.md)。


第一百二十三批（2026-10-22）：原始像素图像/视频MoT，4秒T2V和额外条件微调，未测笔顺。见[审查](pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[L108](../reviews/L108.md)。


第一百二十四批（2026-10-22）：静态I2T/T2I离散DFM，理解连续SigLIP路径仍保留，非笔顺视频。见[审查](fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[L109](../reviews/L109.md)。


第一百二十五批（2026-10-22）：静态理解/ground/编辑/1024²T2I，空间分层揭示与真实书写事件区分。见[审查](lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[L111](../reviews/L111.md)。


第一百二十六批（2026-10-22）：静态离散图文，视频/音频仍未来方向，后续sketch隐喻需独立核。见[审查](lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[L112](../reviews/L112.md)。


第一百二十七批（2026-10-22）：静态图文+语音、连续输入/离散输出；未覆盖真实书写视频和规范事件。见[审查](omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[L113](../reviews/L113.md)。


第一百二十八批（2026-10-22）：静态文字渲染和稀疏交错生成覆盖，未验证真实笔顺视频。见[审查](llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[L114](../reviews/L114.md)。
