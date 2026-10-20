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

截至2026-10-21第六十二批，主目录347条（321论文／研究、26资源），347份结构化笔记，138项明确范围的核心三遍与140项五条书面检查。历史未重新核查标记已清零，5项仍受全文访问限制；其余记录的核心三遍逐项继续。未完成全部深审，未训练、推理或独立复现。下方按批保留历史状态。具体范围见[本轮审查](../evidence/second_round_audit_2026-10-19.md)与[逐条台账](../evidence/reading_ledger_2026-10-19.md)。

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


第三十三批完成B04–B08五项核心三遍、五条书面检查及公开实现交叉核。当前339目录/339笔记、334章节或协议/5摘要、63核心三遍；未模型执行。见[动态文字与绘画过程审查](../evidence/dynamic_text_and_painting_process_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_third_changes_2026-10-20.md)。无删除。


第三十四批完成C01/C02/C06核心三遍及各五条书面检查，核Show-o2 NeurIPS2025/ReCA ICLR2026身份和最新已读版本、固定公开代码。339目录/339笔记、334章节或协议/5摘要、66核心三遍；未模型运行。见[统一主干与重建审查](../evidence/unified_backbones_and_reconstruction_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_fourth_changes_2026-10-20.md)。无删除。


第三十五批完成C03/C04/C05/C07核心三遍及各五条书面检查，核NFE/延迟/managedKV分母、参考与物理后端差异、整轨迹协同及协议缺项。339目录/339笔记、334章节或协议/5摘要、70核心三遍；未独立模型运行。见[加速缓存与反思审查](../evidence/acceleration_cache_and_reflection_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_fifth_changes_2026-10-20.md)。无删除。


第三十六批完成D01–D04核心三遍及各五条书面检查，核视频/声画/条件编辑/轨迹控制、原文与固定实现差异、负结果及训练适配配置。339目录/339笔记、334章节或协议/5摘要、74核心三遍；未独立模型运行。见[视频骨干与运动控制审查](../evidence/video_backbones_and_motion_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_sixth_changes_2026-10-20.md)。无删除。


第三十七批扩展D05–D08核心三遍和五项书面检查：核自生成历史、cache梯度、少步组合、任务RL；记录Wan-R1表文冲突、Salt负项及固定代码/HF配置。339目录/339笔记、334章节或协议/5摘要、78核心三遍；无独立模型运行。见[自回归训练与视频RL审查](../evidence/autoregressive_training_and_video_rl_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_seventh_changes_2026-10-20.md)。无删除。


第三十八批完成E01–E03核心三遍并新增D09 SGF+同层审查：核平均场/JVP、CFG条件与训练预算、一致性动作计时、视频角色局部梯度理论及负项。主目录340项/340笔记、335章节或协议/5摘要，核心三遍82项；全部三遍仍未完成，无独立模型运行。见[平均场、一致性与角色解耦审查](../evidence/meanflow_consistency_and_role_split_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_eighth_changes_2026-10-20.md)。无删除。


第三十九批完成E04–E07核心三遍与各五项书面检查：核离散FM概率/任务指标与采样精度、F5语音对齐/solver与CFG开销、TeaCache残差/校准和多卡分母、clDice条件定理/空间指标边界。主目录340项，核心三遍86项；其余三遍继续保留未完成状态。见[离散流、语音、缓存与拓扑审查](../evidence/discrete_flow_speech_cache_topology_core_reading_2026-10-20.md)和[逐文件说明](../evidence/thirty_ninth_changes_2026-10-20.md)。无模型运行/文件删除。


第四十批完成F01–F04核心三遍与各五项书面检查：可微矢量渲染、Gaussian曲线表示、真实笔触规划与共绘模型适配，核作者勘误/版本/预算/模拟代理。主目录340项，核心三遍90项；其余仍待逐项完成。见[矢量与机器人绘画审查](../evidence/differentiable_vectors_robot_painting_core_reading_2026-10-20.md)和[逐文件说明](../evidence/fortieth_changes_2026-10-20.md)。F02实际读v4HTML，正式PDF不完整未计；F03/F04预印本版本明确，无模型运行/文件删除。


第四十一批补完sketch-rnn与Learning to Paint核心三遍（累计92项），深化英文连笔作者报告及CoFRIDA-Sharpie制品协议（四项五检查，累计94项）。HF权重rank256/cross768与卡片SDXL及当前rank32脚本不对齐，未运行；F05 IEEE正文仍缺。主目录340项，剩余任务继续逐项处理。见[素描/RL/LoRA审查](../evidence/sketch_sequences_painting_rl_and_lora_artifact_2026-10-20.md)与[逐文件说明](../evidence/forty_first_changes_2026-10-20.md)。无文件删除。


第四十二批补完Paint Transformer/CLIPasso并追引补录Stylized Neural Painting/SPIRAL，新增四项核心三遍（累计96）和书面五检查（累计98）。主目录342项；当前Paint Transformer采色版、CLIPasso评价/参与者差异、SPIRAL奖励与符号边界均单独记录。见[神经绘画审查](../evidence/neural_painting_sets_semantics_and_programs_2026-10-20.md)及[逐文件说明](../evidence/forty_second_changes_2026-10-20.md)。无训练/推理或文件删除，扩散/Flow Matching/视频基础及剩余候选继续处理。


第四十三批深化DDPM/Score-SDE/Flow Matching/Rectified Flow，新增四项核心三遍（累计100）与五条书面检查（累计102），342项目录不增删。记录质量—似然取舍、等NFE/检查点差异、条件OT边界和RF高步负结果。见[扩散与流审查](../evidence/diffusion_score_flow_and_rectification_2026-10-20.md)及[逐文件说明](../evidence/forty_third_changes_2026-10-20.md)。未训练/推理；LDM/DiT/consistency/求解器和视频等剩余复核继续。


第四十四批深化LDM／DiT／Consistency Models／DPM-Solver并补HF VAE资源组R10；343项（318研究／25资源），核心三遍104、书面五检查106。核查decoder／CFG、CT例子初始化与超参、原DPM与++默认差异及负指标；见[本批审查](../evidence/latent_transformer_consistency_and_solver_audit_2026-10-20.md)和[逐文件说明](../evidence/forty_fourth_changes_2026-10-20.md)。全部剩余三遍与视频等领域继续，未训练或推理。


第四十五批深化VDM／VideoLDM／AnimateDiff；343项，核心三遍107、五条书面检查109。分清C3D-FID／I3D-FVD、条件抽样协议、时序／静态质量取舍与论文／示例／后继版本；见[本批审查](../evidence/video_diffusion_temporal_transfer_and_motion_adapters_2026-10-20.md)及[逐文件说明](../evidence/forty_fifth_changes_2026-10-20.md)。AnimateDiff原补充训练／评价协议仍待补，全部剩余三遍继续，未训练、推理或复现。


第四十六批深化CogVideoX并补R11微调／检查点配置资源组；344项（318研究／26资源），核心三遍108、五条书面检查110。核文字主导视频过滤、时空token／元素压缩、负指标、人评聚合与公开版本／默认值差异；见[本批审查](../evidence/cogvideox_video_compression_data_and_finetuning_2026-10-20.md)及[逐文件说明](../evidence/forty_sixth_changes_2026-10-20.md)。全部剩余深审继续，未训练／推理／复现。


第四十七批深化Wan2.1：344项目录，核心三遍109、五条书面检查111。核专门中英视觉文字数据、流式VAE/采样缓存/蒸馏分支差异、负指标与gap/步数/帧率矛盾，并固定代码默认及负提示。见[本批审查](../evidence/wan_visual_text_flow_training_and_evaluation_audit_2026-10-20.md)、[逐文件说明](../evidence/forty_seventh_changes_2026-10-20.md)。全部剩余审查继续；无模型训练、推理或独立复现。


第四十八批深化LoRA/QLoRA/DoRA/rsLoRA：344项目录，113核心三遍、115五条书面检查。区分低秩表示、量化存储、模长/方向和rank缩放，保留主表负项、配方冲突与语言证据迁移边界。见[本批审查](../evidence/parameter_efficient_adaptation_rank_quantization_and_weight_decomposition_2026-10-20.md)与[逐文件说明](../evidence/forty_eighth_changes_2026-10-20.md)。全部剩余工作继续；无训练、推理或独立复现。


第四十九批深化ControlNet/CFG：344项目录，115核心三遍、117五条书面检查。修正CFG分辨率训练步数，保留FID文字/表图冲突与等速度负结果；核ControlNet初始零残差、代码/hint/RW差异和二维到时序边界。见[本批审查](../evidence/spatial_control_classifier_free_guidance_and_protocol_gaps_2026-10-20.md)与[逐文件说明](../evidence/forty_ninth_changes_2026-10-20.md)。无训练、推理或独立复现；剩余深读继续。


第五十批深化GAN/VAE原始理论与实验：344项目录，117核心三遍、119五条书面检查。区分理想分布均衡/有限网络、ELBO/似然/Parzen与重建/生成，保留TFD和小数据test反例。见[本批审查](../evidence/gan_vae_theory_estimation_and_video_representation_boundaries_2026-10-20.md)与[逐文件说明](../evidence/fiftieth_changes_2026-10-20.md)。无训练、推理或独立复现；剩余工作继续。


第五十一批深化VBench/FVD核心、既有验证与固定官方评价代码：344项目录，119核心三遍、121五条书面检查。保留VBench版本/相关系数名称差异、FVD样本偏差及非全胜结果；++/2.0和ContentBias继续追读。见[本批审查](../evidence/video_evaluation_vbench_fvd_protocol_and_scope_2026-10-20.md)与[逐文件说明](../evidence/fifty_first_changes_2026-10-20.md)。无训练、推理或独立复现；剩余工作继续。


第五十二批新增并精读Content Bias G033：345项目录（319研究／26资源），核心三遍120、五条书面检查122。核同空间质量扰动、冻结重采样、长视频反例与固定实现，纠正T3把分差标百分比的错误；见[本批审查](../evidence/content_bias_fvd_temporal_sensitivity_and_resampling_2026-10-20.md)和[逐文件说明](../evidence/fifty_second_changes_2026-10-20.md)。未删除文件、训练、推理或独立复现，全部剩余工作继续。


第五十三批新增并精读VBench++ G034：346项（320研究／26资源），核心三遍121、书面检查123。核I2V裁图/专家、可信人评与固定评分实现，记录2026正式卷期、肤色归一化/安全阈值/背景特征差异及有效样本分母。见[本批审查](../evidence/vbench_plus_i2v_trustworthiness_protocol_and_implementation_2026-10-20.md)、[逐文件说明](../evidence/fifty_third_changes_2026-10-20.md)。无删除、训练、推理或复现；全部剩余工作继续。


第五十四批新增VBench-2.0 G035并完成核心精读：347项（321研究／26资源），核心三遍122、书面检查124。核18维事件/物理评价、人体异常训练资源和指定固定代码；记录条件分母、预筛失败计分、无人检测满分及MotionOrder相关名称疑问。见[本批审查](../evidence/vbench2_intrinsic_faithfulness_events_and_conditional_scores_2026-10-20.md)、[逐文件说明](../evidence/fifty_fourth_changes_2026-10-20.md)。无删除或模型复现；原有剩余研究继续。


第五十五批补完原记录Chameleon/U01、Transfusion/U05核心三遍：目录347项不变，核心124、书面126。修订训练token口径、Chameleon总体/子集胜率、稳定性曲线表述和Transfusion共享代价/FLOP估计、patch暴露混杂。见[原文审查](../evidence/chameleon_transfusion_shared_model_cost_and_claim_audit_2026-10-20.md)、[逐文件说明](../evidence/fifty_fifth_changes_2026-10-20.md)。无删除/模型复现；Janus/Show-o及其他剩余继续。


第五十六批补完原Janus/U03、Show-o/U06核心精读：347目录不变、126核心/128书面。修订解耦/共享收益、版本/指标、CFG与采样成本；纳入Show-o视频扩展，并限定附录公式问题的适用范围。见[原文审查](../evidence/janus_showo_representation_video_and_math_audit_2026-10-20.md)、[逐文件说明](../evidence/fifty_sixth_changes_2026-10-20.md)。无删除/训练复现，剩余精读继续。


第五十七批补完InkSight/X01、VideoSketcher/L010核心精读：347目录不变，128核心/130书面。补齐配方、主表/消融、并笔率/统计口径、TF版本与HF制品访问，纠正合理轨迹/规范笔序及偏好/准确率混用。见[原文审查](../evidence/inksight_videosketcher_trajectory_events_and_resource_audit_2026-10-20.md)、[逐文件说明](../evidence/fifty_seventh_changes_2026-10-20.md)。无删除/模型复现；SketchAgent及剩余继续。


第五十八批补完SketchAgent/L012与ProcessPainter/L013核心：347目录不变，130核心/132书面。记录正式新增字母串/网格实验、协作边界、关键帧与末帧重建评价，以及公开代码与论文的配置差异。见[原文审查](../evidence/sketchagent_processpainter_protocol_and_claim_audit_2026-10-20.md)、[逐文件说明](../evidence/fifty_eighth_changes_2026-10-20.md)。无删除/训练或独立复现；剩余继续。


第五十九批补完PaintsAlter/L014、StrokeNUWA/L016核心：347目录保持，132核心/134书面。补齐非连续查询、数字编辑/规范事件差别、矢量压缩质量取舍、指标方向冲突及公开示例配置。见[原文审查](../evidence/paintsalter_strokenuwa_query_representation_and_metrics_audit_2026-10-20.md)、[逐文件说明](../evidence/fifty_ninth_changes_2026-10-20.md)。无删除或独立复现；DiffSketcher新版与剩余继续。


第六十批补完DiffSketcher/L017、Diff-Font/L018明示版本核心：347目录保持，134核心/136书面，213项未确认核心三遍（含资源）。明确优化过程与真实书写、笔画计数与顺序、版本及guidance指标取舍，核对公开warmup/batch/embedding差异。见[原文审查](../evidence/diffsketcher_difffont_condition_process_and_configuration_audit_2026-10-20.md)、[逐文件说明](../evidence/sixtieth_changes_2026-10-20.md)。无删除或独立复现；剩余继续。


第六十一批（2026-10-21）补完FontDiffuser/L019、DiffBrush/L023核心：347目录、136核心/138书面，211项尚未确认核心三遍（含资源）。区分未见内容/字体/作者、静态行与真实事件、下游OCR指标，补齐模块tradeoff及公开推理/文章配方差异。见[原文审查](../evidence/fontdiffuser_diffbrush_generalization_metrics_and_release_audit_2026-10-21.md)、[逐文件说明](../evidence/sixty_first_changes_2026-10-21.md)。无删除或独立复现；剩余继续。


第六十二批（2026-10-21）补完Emu3/U02、Janus-Pro/U04核心：347目录、138核心/140书面，209项尚未确认核心三遍（含资源）。Emu3 Nature正式扩展与2024v1分列，补重写/后处理、tokenizer/配方消融和CALVIN模拟边界；Janus-Pro缺少逐因素消融，明确记录归因限制。见[原文审查](../evidence/emu3_januspro_versions_training_and_causal_audit_2026-10-21.md)、[逐文件说明](../evidence/sixty_second_changes_2026-10-21.md)。无删除或独立复现；剩余继续。
