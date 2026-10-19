# 研究进展

## 研究问题

共享的多模态过程理解，能否帮助生成器在艺术风格变化和不完整前缀下，持续执行正确的汉字笔画顺序？

研究对象是实际生成过程。首先研究保留可辨笔画结构的中文艺术字，再扩展多字、布局、速度、颜色和自由行草。

## 已有工作

- 文献目录覆盖UMM架构、理解与生成协同、笔迹生成与恢复、书写视频和相关控制方法。
- 已梳理笔顺生成的任务定义、直接前作、可检验机制、数据方案、对照与指标。
- 对VidScribe中8段公开生成样例进行了定性核查，记录了笔顺、方向、文字增生及多字结构等问题，也保留了较好的生成结果。样例数量不足以估计模型总体错误率。
- 四份指定PDF已完成正文、实验及附录阅读；[精读分析](../evidence/attachment_reviews.md)区分版本和各自证据边界。
- [最小研究方案](../experiments/stroke_order_pilot.md)明确状态、动作、执行三层评价及BAGEL/Lance等底座的公开可用性。
- [像素过程小实验](../experiments/process_probe.md)已完成：8个同终态案例区分正常、换序、反向、跨字回跳和不可观察情形。它是模板辅助的确定性验证，不是学习模型成绩。
- [结论依据](DECISIONS.md)记录了指标解释和研究范围的修订。

## 尚待验证

- 建立具有独立标注的中文规范笔顺视频测试集。
- 测试模型能否区分最终字形相同、实际顺序不同的过程。
- 比较规则渲染、专门轨迹模型、物理渲染、外部VLM指导和联合UMM。
- 检验过程理解的提升是否转化为实际生成收益，并测量计算成本。

目前尚无本项目的模型训练、准确率、速度或显存对照结果。

## 实验顺序

1. SO-01：实际笔顺理解诊断。
2. SO-02：正确轨迹或掩码条件下的生成执行。
3. SO-03：相同数据、输入与预算下的联合、分离和专门模型对照。
4. SO-04：多字与风格泛化。
5. EF-01：过程信息在少步生成和缓存压缩中的保持。

详细设计见[实验计划](EXPERIMENTS.md)与[笔顺专项](../handwriting/05_stroke_order_umm.md)。

## 第二轮调研更新（2026-10-19）

截至2026-10-20，主目录334条，首轮补录已关联并同步表格；新增334份结构化阅读笔记和基础/邻近领域分析，以及CoFRIDA-Sharpie资源卡。历史未重新核查标记已清零，5条摘要和全部完整三遍验收仍待完成，完整三遍验收与模型复现均未完成。具体范围见[本轮审查](../evidence/second_round_audit_2026-10-19.md)与[逐条台账](../evidence/reading_ledger_2026-10-19.md)。

第四批：150条章节核查、40条摘要核查；L024已记录五项书面理解检查，其他逐篇验收继续进行。全文无法访问的5项只记第一遍。

第五批：累计171条章节核查、145份结构化笔记；补入STRIVE和CONSTANT。L020与L024记录五项书面理解检查，共2项；完整三遍阅读完成数仍为0。版本与实际配置差异见[本批审查](../evidence/text_motion_and_protocol_audit_2026-10-20.md)。

第六批：累计186条章节核查、160份结构化笔记；EDM已补正式正文/主表，第一遍笔记余5项。新增15份存量研究的协议与机制审查，详见[本批分析](../evidence/unified_representation_and_causal_review_2026-10-20.md)。完整三遍验收仍未完成，无模型复现。

第七批：174份笔记，188条章节核查、33条摘要、0条仅元数据、110条历史待复核。新增Stroke-Seg正式论文L184，其HF数据与代码仍为独立资源记录；共331条(309论文/22资源)。重点差异见[资源实现审查](../evidence/resource_implementation_review_2026-10-20.md)。全部三遍验收和模型复现仍未完成。

第八批：新增7份UMM技术审查，累计181份笔记、195条章节核查、33条摘要及103条历史待核。Qwen3-Omni仅输出文字/语音；SEED-X专门版本、AnyGPT/Manzano外部解码、MMaDA采样代码与Emu3.5关键帧/执行边界见[本批分析](../evidence/unified_interfaces_and_transfer_2026-10-20.md)。完整三遍验收和复现仍未完成。

第九批：OFA/Unified-IO/VersatileDiffusion/UniDiffuser/Emu/SEED及MetaQueries共7项，累计188份笔记、202条章节核查、33条摘要、96条历史待核。OFA新增正式框架图/消融视觉核对与五项书面理解检查(累计3项)；完整三遍验收仍为0。详见[早期统一与分布审查](../evidence/early_unification_and_distribution_review_2026-10-20.md)。

第十批：新增7份存量模型分析，累计195份笔记，209条章节核查、33条摘要、89条历史待核。MM-Interleaved补框架图/消融视觉核查及五项书面检查（共4项）；完整三遍验收0。详见[压缩、条件与协同](../evidence/compression_conditions_and_synergy_2026-10-20.md)。

第十一批新增8份存量模型分析，累计203份笔记；217条相关章节核查、33条摘要、81条历史待核。Orthus正式框架图/消融表与MetaMorph正式框架图已视觉核对；五项书面检查累计5，完整三遍验收0。见[专题](../evidence/curricula_feedback_and_synergy_2026-10-20.md)。

第十二批：6项历史记录升级相关章节核查，新增DDPO论文L185，目录332条；累计210份笔记，224条章节、33条摘要、75条历史待核，三遍验收0。核查QLIP/DualToken/UniToken公开代码，UniCode²公式/框架图已视觉核对；见[理论与配方审查](../evidence/tokenizer_theory_and_rl_2026-10-20.md)。

第十三批：8项历史记录升级章节核查，累计218份笔记，232条章节、33条摘要、67条历史待核；主目录332条。HYDRA补框架图与五项书面理解检查（累计6项），完整三遍验收0。另视觉核对RF伪码与PixelUMM的VBench全表；见[像素接口与时序审查](../evidence/pixel_interfaces_and_temporal_audit_2026-10-20.md)。

第十四批：L109–L116八项存量研究新增分析，累计226份笔记；主目录332条，240条章节/33条摘要/59条历史待核。Muddit新增指定框架图和五项书面检查，累计7项；完整三遍验收仍0。FullFlow主表已视觉核对，正式ICLR2026 Muddit来源已定位；未运行模型、无删除。见[离散路径专题](../evidence/discrete_paths_and_flow_audit_2026-10-20.md)。

第二十一批：七项长程生成/多模态框架，累计270份笔记、284条章节/33条摘要/15条历史待核。UniLongGen五项书面检查累计14；完整三遍和复现未完成。原版MingREADME/config已定位历史提交，未执行模型；见[专题](../evidence/long_horizon_memory_and_multimodal_generation_paths_2026-10-20.md)。

第二十二批新增7份存量分析，累计277份，章节291/摘要33/历史8；IP2P五项书面检查累计15，全部三遍验收仍0。无模型执行；逐文件说明及疑点见[专题](../evidence/interleaved_data_editing_and_distillation_audit_2026-10-20.md)。

第二十三批八项存量初核，累计285份，相关章节299/摘要33/历史未重新核查0；全部完整三遍仍未完成、未执行模型。WorldBagel理论反例和SenseNova公开配置差异见[专题](../evidence/omni_action_world_and_theory_audit_2026-10-20.md)。

第二十四批补8条摘要为章节分析，累计293笔记，章节307/摘要25；U07/U10/L178增加五项书面检查，累计18。全文/附录缺项保留；无模型执行。见[成本、latent策略与历史轨迹专题](../evidence/interleaved_reasoning_cost_and_latent_policy_audit_2026-10-20.md)。

第二十五批补8条，累计301份笔记；章节315/摘要17，新增L003/S002书面检查，累计20。WriteLikeYou模型默认与论文差异、GapEval公式条件和UniMRG取舍见[专题](../evidence/glyph_conditions_paired_benchmarks_and_structural_targets_2026-10-20.md)。无模型执行、无文件删除，完整三遍仍待完成。

第二十六批补U20–U25，累计307笔记；章节321/摘要11，五项书面检查22。生成代理/推理gate/视觉tokenizer/世界模型假设见[专题](../evidence/generative_targets_gating_shared_tokens_and_world_models_2026-10-20.md)。无训练推理和文件删除。

第二十七批补U26–U31，新增L186/R08并补N08，累计334条（311研究/23资源）、316笔记；章节329/摘要5，五项书面检查26。原生像素、潜空间代理及机器人/动力学前史见[专题](../evidence/native_pixels_latent_proxies_and_robot_handwriting_2026-10-20.md)；无文件删除，无模型执行，完整三遍尚未完成。

第二十八批重新精读原有九项的指定方法/实验/附录，累计325份笔记和33项五条书面理解检查，目录仍334条。新增[书法、视频文字、画序及OCR协议专题](../evidence/calligraphy_video_text_order_and_ocr_protocols_2026-10-20.md)；同图改序对照、FID/CER权衡和公开base/源码范围均已记录。没有删除文件，未运行新模型。

第二十九批补当前目录最后九份独立分析，累计334条/334笔记，329章节/5摘要，40项五条书面理解检查。新增[统一视频与文字/草图/资源差异专题](../evidence/unified_video_static_text_sketch_and_resource_mismatches_2026-10-20.md)及88行Calligraphy Bench元数据审计。全部三遍、未读附录/源码及扩展追引仍继续。无删除，无模型运行。


第三十批补四篇视觉蒸馏/矢量动画/艺术字论文和一个模拟书写资源（尚未找到对应独立论文）。当前339条/339笔记，334项原文章节或资源协议、5项摘要；44项五条书面检查，其中4篇完成核心三遍阅读。计时口试、全部代码与独立复现单列，不额外作为核心阅读门槛；此前40项仍逐篇待核定。见[专题](../evidence/visual_distillation_svg_animation_and_causal_robot_rgb_2026-10-20.md)及[逐文件说明](../evidence/thirtieth_changes_2026-10-20.md)。无删除，无模型执行。


第三十一批完成A01/A02/A03/A04/A05/A07/A08七项核心三遍与五条书面检查；另将此前40项已有证据逐项按统一口径确认，属于状态校正。当前339目录/339笔记、334章节或协议/5摘要、51核心三遍；未模型复现。见[中文墨迹生成与恢复专题](../evidence/chinese_ink_generation_and_recovery_core_reading_2026-10-20.md)及[逐文件说明](../evidence/thirty_first_changes_2026-10-20.md)。无删除。


第三十二批完成A09/A10/A11/B01/B02/B03/B09七项核心三遍与五条书面检查。当前339目录/339笔记、334章节或协议/5摘要、58核心三遍，未模型复现。见[手写风格/书法/数学审查](../evidence/handwriting_style_diffusion_and_math_core_reading_2026-10-20.md)及[逐文件说明](../evidence/thirty_second_changes_2026-10-20.md)。无删除。
