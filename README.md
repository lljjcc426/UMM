# UMM 与中文书写过程生成

研究统一多模态模型（Unified Multimodal Model，UMM）如何结合理解与生成，重点关注中文书写视频中的笔画顺序、实际执行和艺术风格控制。

核心问题是：模型能否根据已经发生的书写过程，判断下一笔并正确生成？在相同数据、输入和计算预算下，统一训练是否优于规则渲染、专门轨迹模型或外部视觉语言模型指导？

## 阅读导航

| 内容 | 入口 |
|---|---|
| 研究范围、主要发现与开放问题 | [综合分析](docs/RESEARCH_MAP.md) |
| 中文笔顺生成的直接前作、方法与实验设计 | [笔顺专项](docs/handwriting/05_stroke_order_umm.md) · [证据核查](docs/handwriting/06_stroke_order_evidence.md) |
| UMM架构、理解与生成协同 | [UMM综述](docs/umm/00_overview.md) · [相关文献](docs/umm/literature.md) |
| 书写轨迹、艺术字与视频生成 | [能力与问题](docs/handwriting/02_capability_matrix.md) · [相关文献](docs/handwriting/literature.md) |
| 重点论文的方法、结果与限制 | [论文精读](docs/handwriting/papers/README.md) · [四篇指定论文精读](docs/evidence/attachment_reviews.md) · [公开版本对照](docs/evidence/public_preprint_reviews.md) |
| 数据、标准与评价 | [数据与标准](docs/handwriting/03_data_and_standards.md) · [评测协议](docs/experiments/benchmark_protocol.md) |
| 研究进展与后续实验 | [研究进展](docs/project/STATUS.md) · [结论依据](docs/project/DECISIONS.md) · [实验计划](docs/project/EXPERIMENTS.md) · [最小研究方案](docs/experiments/stroke_order_pilot.md) |
| 本轮逐篇阅读、理论与实验迁移 | [357份结构化笔记](docs/reviews/README.md) · [理论与迁移分析](docs/evidence/foundations_and_transfer_2026-10-19.md) · [逐条阅读台账](docs/evidence/reading_ledger_2026-10-19.md) |
| 全部文献 | [文献总表](docs/all_literature.md) · [CSV](data/literature.csv) · [Excel](data/literature_public.xlsx) |

## 主要判断

- **读写联合与中文书法统一生成已有前作。** [InkSight](https://arxiv.org/abs/2402.05804)联合识别与笔迹恢复，[UniCalli](https://arxiv.org/abs/2510.13745)统一列级书法识别与静态生成。研究贡献需要具体到过程理解及其对生成的作用。
- **笔顺条件不等于过程正确。** 静态字形、最终帧OCR和文字笔顺问答都不能独立证明实际生成顺序；需要检查具体笔画的身份、先后、方向与落笔状态。
- **轨迹、物理渲染和视频文字控制已有可比较的方法。** [OnOff](https://arxiv.org/abs/2608.03198)连接轨迹与墨迹渲染；[VidScribe](https://arxiv.org/abs/2609.36598)和[VTR-Bench](https://arxiv.org/abs/2610.01499)提供视频文字评测。它们的指标与规范笔顺验证仍有区别。
- **UMM的额外收益尚需实验确认。** 先比较过程理解与生成执行，再扩展多字、布局、风格和效率。不能仅凭一个模型同时支持理解和生成就认定二者互相促进。

## 文献与证据

主目录包含 **330项论文／研究记录、27项资源，共357条记录**。每项记录包括研究主张、方法、问题、结果、限制、原始来源、版本及核查范围。数量不代表全文精读数量；文献中的数值为作者报告。

[候选目录](data/discovery/README.md)另含573条arXiv检索记录和200条综述目录候选，两者有重叠，也与主目录重叠。详细记录规则见[核查方法](docs/evidence/method_and_status.md)，早期分析见[研究档案](archive/README.md)。

## 数据维护

`data/literature.json` 为文献主数据。安装依赖后生成Markdown、CSV和Excel视图，并检查记录及仓库内链接：

```bash
python -m pip install -r requirements.txt
python scripts/render_catalog.py
python scripts/validate_catalog.py
```

`scripts/stroke_metrics.py` 提供已标注事件序列的指标示例，不负责从视频识别笔画。[像素过程小实验](docs/experiments/process_probe.md)已运行，验证同终态反例和模板辅助的顺序/方向观测；可用 `python scripts/process_probe.py` 复现并查看[动画](examples/process_probe/comparison.gif)。它不是模型评测，当前尚无模型训练或推理实验结果。

## 2026-10-19：新增来源核查与文献补录

首轮补录现已整合进主目录：[补录映射](data/research_additions_2026-10-19.json)保留16条来源记录，VideoSketcher关联L010、Calligraphy Bench关联L044，其余14条使用S编号；关联代码作为资源记录。新增32条G编号基础/邻近领域文献。主目录、CSV、Markdown及Excel已同步，禁止再将16条补录全部加到主目录计数。

- [补录研究矩阵](docs/evidence/scoped_literature_matrix_2026-10-19.md)：按任务、数据、结构、指标、比较方法与实验条件区分直接前作和可迁移机制。
- [VidScribe 精读](docs/handwriting/papers/vidscribe.md)、[Calligraphy Bench](docs/handwriting/papers/calligraphy_bench.md)、[VideoSketcher 精读](docs/handwriting/papers/videosketcher_deep_review.md)：分别对应视频文字评测、书法工具绘制、逐步素描视频生成；三者的笔顺与生成任务不等价。
- [Ketaba OCR 论文/代码核查](docs/handwriting/papers/ketaba_ocr_lora.md)、[Wuji 视频动作权重](docs/handwriting/papers/wuji_vam_modelcard.md)、[无论文模型及数据资源](docs/resources/nonpaper_research_2026-10-19.md)。
- [NeurIPS 静态文字扩散前作](docs/handwriting/papers/static_text_neurips_baselines.md)、[可证伪实验设计](docs/experiments/research_gaps_and_tests_2026-10-19.md)、[下一批精读核查队列](docs/evidence/survey_queue_2026-10-19.md)。

**关键新颖性纠偏：**中文书法逐笔 Agent 评价已有 Calligraphy Bench，严格笔顺视频问题仍需证明其独有的像素历史可观测性/时间执行与共享 UMM 收益；VidScribe 评字形拓扑，Calligraphy Bench 评工具笔顺，均不可直接套用为模型生成汉字规范笔顺视频正确率。

## 第二轮：原文重读、实验审查与广泛领域补充

[本轮审查记录](docs/evidence/second_round_audit_2026-10-19.md)说明实际完成范围和纠错；[修改文件说明](docs/evidence/second_round_changes_2026-10-19.md)记录首批新增与修改文件；[继续复核文件说明](docs/evidence/continued_changes_2026-10-20.md)记录后续修改，无文件删除。

截至2026-10-20，累计形成340份逐篇结构化笔记，其中335份核查相关章节或资源协议，5份仅完成第一遍；包含数据、结构、指标、基线、实验条件、消融、可证伪假设及写作学习。并对原281条、首轮16条补录和32条基础候选的首选来源执行访问审计，得到329条访问事件；这些事件有同研究重复，且**访问成功不等于阅读完成**。

当前340条目录中：335条已读相关原文或资源章节、5条已核摘要、0条仅元数据、0条历史原文待复核（仅指初次章节核查标记）。U18原始来源已解决。**核心三遍阅读与五项书面检查已逐项确认90篇，全部文献的三遍精读尚未完成。独立模型复现为0；不能声称达成零遗漏。** 每一条当前状态见[完成台账](docs/evidence/reading_ledger_2026-10-19.md)。

继续复核覆盖23项存量研究：[过程、评价与执行边界](docs/evidence/process_execution_boundaries_2026-10-19.md)比较轨迹恢复、绘画过程与机器人执行；[CoFRIDA-Sharpie资源卡](docs/resources/cofrida_sharpie_card.md)明确模型元数据冲突及论文/权重版本边界。

第三批再补19项存量研究：[实验主张与跨文字过程审查](docs/evidence/claims_and_cross_script_2026-10-20.md)定位InkDiffuser公式/代码、DiffMath训练条件、Layout Stroke Imitation消融与StrokeBank式5等待澄清问题；补充女书、空中书写、在线流程图、字体动画及UMM协同/压缩的证据边界。[本批文件说明](docs/evidence/third_changes_2026-10-20.md)列出全部改动。

第四批新增24项存量研究/资源笔记：[梯度、指标和数据协议审查](docs/evidence/gradient_metrics_and_resource_protocols_2026-10-20.md)核对多任务梯度定义、一致性分数、静态草稿与笔画过程、字体/手写库授权与实际字段。5项全文尚未取得，只完成第一遍，未升级章节精读。L024另有[五项书面理解检查](data/reading_acceptance_2026-10-20.json)，未进行计时口试或模型复现。[本批文件说明](docs/evidence/fourth_changes_2026-10-20.md)。

第五批新增21份笔记，并补入STRIVE（ICCV2021）和CONSTANT（WACV2026）两项遗漏前作：[文字、运动与协议审查](docs/evidence/text_motion_and_protocol_audit_2026-10-20.md)核对静态手写、视频文字评价/编辑、可微矢量渲染与运动控制的实际任务，记录版本、公式及配置差异。L020增加五项书面理解检查；统计脚本不再把这类检查自动计为完整三遍阅读完成。[本批文件说明](docs/evidence/fifth_changes_2026-10-20.md)。

第六批新增15份存量研究笔记并升级EDM：[统一表示、因果过程与协同证据](docs/evidence/unified_representation_and_causal_review_2026-10-20.md)审查Show-o2/UniTok/TokenFlow、UReason/RSI、在线分割、视频文字编辑、Painter及2023汉字生成识别前作。新增[知识盲区清单](docs/evidence/knowledge_gaps_2026-10-20.md)，记录ODE多模态、噪声时间与事件时间、码率公平性及公式/实现差异。[本批文件说明](docs/evidence/sixth_changes_2026-10-20.md)。

第七批新增14份规范/资源/论文笔记，并从BCSS追引补录Stroke-Seg正式论文：[资源配置与实现审查](docs/evidence/resource_implementation_review_2026-10-20.md)核对六类/十类标签、验证/外部测试分数、素描扩散编码与公式、HF适配器/训练配置及OSF统计字段。官方笔顺规范PDF已读取定义和初始示例。[逐文件说明](docs/evidence/seventh_changes_2026-10-20.md)。

第十批新增7项：LaVIT/NExT-GPT/DreamLLM/SEED-LLaMA/Emu2/MM-Interleaved/VILA-U，核查动态压缩、条件解码与真实协同证据，并读取VILA-U训练/推理配置：[机制与条件分析](docs/evidence/compression_conditions_and_synergy_2026-10-20.md)、[逐文件说明](docs/evidence/tenth_changes_2026-10-20.md)。

第十一批新增8项：JanusFlow/Orthus/Liquid/ILLUME/MetaMorph/UGen/Harmon/X-Omni，区分固定任务曝光、额外数据、外部教师与中文分支。详见[训练课程、反馈与协同](docs/evidence/curricula_feedback_and_synergy_2026-10-20.md)、[逐文件说明](docs/evidence/eleventh_changes_2026-10-20.md)。

第十二批完成QLIP/DualToken/UniToken/Selftok/UniCode²/Tuna的指定章节审查，补入经典DDPO（ICLR2024），核查三项官方代码配方并记录理论反例：[tokenizer与RL审查](docs/evidence/tokenizer_theory_and_rl_2026-10-20.md)、[逐文件说明](docs/evidence/twelfth_changes_2026-10-20.md)。

第十三批完成L101–L108指定章节审查，核对EvoTok/HYDRA/UniCom官方代码及两项HF模型卡，记录像素/视频接口、时间压缩、负迁移和实际VAE依赖：[像素接口与时序审查](docs/evidence/pixel_interfaces_and_temporal_audit_2026-10-20.md)、[逐文件说明](docs/evidence/thirteenth_changes_2026-10-20.md)。

第十四批完成L109–L116指定章节审查，新增8份笔记，并核Muddit训练掩码/损失与Lumina-DiMOO采样代码。见[离散路径与连续流审查](docs/evidence/discrete_paths_and_flow_audit_2026-10-20.md)、[逐文件说明](docs/evidence/fourteenth_changes_2026-10-20.md)。


第三十批补四篇视觉蒸馏/矢量动画/艺术字论文和一个模拟书写资源（尚未找到对应独立论文）。当前339条/339笔记，334项原文章节或资源协议、5项摘要；44项五条书面检查，其中4篇完成核心三遍阅读。计时口试、全部代码与独立复现单列，不额外作为核心阅读门槛；此前40项仍逐篇待核定。见[专题](docs/evidence/visual_distillation_svg_animation_and_causal_robot_rgb_2026-10-20.md)及[逐文件说明](docs/evidence/thirtieth_changes_2026-10-20.md)。无删除，无模型执行。


第三十一批完成A01/A02/A03/A04/A05/A07/A08七项核心三遍与五条书面检查；另将此前40项已有证据逐项按统一口径确认，属于状态校正。当前339目录/339笔记、334章节或协议/5摘要、51核心三遍；未模型复现。见[中文墨迹生成与恢复专题](docs/evidence/chinese_ink_generation_and_recovery_core_reading_2026-10-20.md)及[逐文件说明](docs/evidence/thirty_first_changes_2026-10-20.md)。无删除。


第三十二批完成A09/A10/A11/B01/B02/B03/B09七项核心三遍与五条书面检查。当前339目录/339笔记、334章节或协议/5摘要、58核心三遍，未模型复现。见[手写风格/书法/数学审查](docs/evidence/handwriting_style_diffusion_and_math_core_reading_2026-10-20.md)及[逐文件说明](docs/evidence/thirty_second_changes_2026-10-20.md)。无删除。


第三十三批完成B04–B08五项核心三遍、五条书面检查及公开实现交叉核。当前339目录/339笔记、334章节或协议/5摘要、63核心三遍；未模型执行。见[动态文字与绘画过程审查](docs/evidence/dynamic_text_and_painting_process_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_third_changes_2026-10-20.md)。无删除。


第三十四批完成C01/C02/C06核心三遍及各五条书面检查，核Show-o2 NeurIPS2025/ReCA ICLR2026身份和最新已读版本、固定公开代码。339目录/339笔记、334章节或协议/5摘要、66核心三遍；未模型运行。见[统一主干与重建审查](docs/evidence/unified_backbones_and_reconstruction_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_fourth_changes_2026-10-20.md)。无删除。


第三十五批完成C03/C04/C05/C07核心三遍及各五条书面检查，核NFE/延迟/managedKV分母、参考与物理后端差异、整轨迹协同及协议缺项。339目录/339笔记、334章节或协议/5摘要、70核心三遍；未独立模型运行。见[加速缓存与反思审查](docs/evidence/acceleration_cache_and_reflection_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_fifth_changes_2026-10-20.md)。无删除。


第三十六批完成D01–D04核心三遍及各五条书面检查，核视频/声画/条件编辑/轨迹控制、原文与固定实现差异、负结果及训练适配配置。339目录/339笔记、334章节或协议/5摘要、74核心三遍；未独立模型运行。见[视频骨干与运动控制审查](docs/evidence/video_backbones_and_motion_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_sixth_changes_2026-10-20.md)。无删除。


第三十七批扩展D05–D08核心三遍和五项书面检查：核自生成历史、cache梯度、少步组合、任务RL；记录Wan-R1表文冲突、Salt负项及固定代码/HF配置。339目录/339笔记、334章节或协议/5摘要、78核心三遍；无独立模型运行。见[自回归训练与视频RL审查](docs/evidence/autoregressive_training_and_video_rl_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_seventh_changes_2026-10-20.md)。无删除。


第三十八批完成E01–E03核心三遍并新增D09 SGF+同层审查：核平均场/JVP、CFG条件与训练预算、一致性动作计时、视频角色局部梯度理论及负项。主目录340项/340笔记、335章节或协议/5摘要，核心三遍82项；全部三遍仍未完成，无独立模型运行。见[平均场、一致性与角色解耦审查](docs/evidence/meanflow_consistency_and_role_split_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_eighth_changes_2026-10-20.md)。无删除。


第三十九批完成E04–E07核心三遍与各五项书面检查：核离散FM概率/任务指标与采样精度、F5语音对齐/solver与CFG开销、TeaCache残差/校准和多卡分母、clDice条件定理/空间指标边界。主目录340项，核心三遍86项；其余三遍继续保留未完成状态。见[离散流、语音、缓存与拓扑审查](docs/evidence/discrete_flow_speech_cache_topology_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/thirty_ninth_changes_2026-10-20.md)。无模型运行/文件删除。


第四十批完成F01–F04核心三遍与各五项书面检查：可微矢量渲染、Gaussian曲线表示、真实笔触规划与共绘模型适配，核作者勘误/版本/预算/模拟代理。主目录340项，核心三遍90项；其余仍待逐项完成。见[矢量与机器人绘画审查](docs/evidence/differentiable_vectors_robot_painting_core_reading_2026-10-20.md)和[逐文件说明](docs/evidence/fortieth_changes_2026-10-20.md)。F02实际读v4HTML，正式PDF不完整未计；F03/F04预印本版本明确，无模型运行/文件删除。


第四十一批补完sketch-rnn与Learning to Paint核心三遍（累计92项），深化英文连笔作者报告及CoFRIDA-Sharpie制品协议（四项五检查，累计94项）。HF权重rank256/cross768与卡片SDXL及当前rank32脚本不对齐，未运行；F05 IEEE正文仍缺。主目录340项，剩余任务继续逐项处理。见[素描/RL/LoRA审查](docs/evidence/sketch_sequences_painting_rl_and_lora_artifact_2026-10-20.md)与[逐文件说明](docs/evidence/forty_first_changes_2026-10-20.md)。无文件删除。


第四十二批补完Paint Transformer/CLIPasso并追引补录Stylized Neural Painting/SPIRAL，新增四项核心三遍（累计96）和书面五检查（累计98）。主目录342项；当前Paint Transformer采色版、CLIPasso评价/参与者差异、SPIRAL奖励与符号边界均单独记录。见[神经绘画审查](docs/evidence/neural_painting_sets_semantics_and_programs_2026-10-20.md)及[逐文件说明](docs/evidence/forty_second_changes_2026-10-20.md)。无训练/推理或文件删除，扩散/Flow Matching/视频基础及剩余候选继续处理。


第四十三批深化DDPM/Score-SDE/Flow Matching/Rectified Flow，新增四项核心三遍（累计100）与五条书面检查（累计102），342项目录不增删。记录质量—似然取舍、等NFE/检查点差异、条件OT边界和RF高步负结果。见[扩散与流审查](docs/evidence/diffusion_score_flow_and_rectification_2026-10-20.md)及[逐文件说明](docs/evidence/forty_third_changes_2026-10-20.md)。未训练/推理；LDM/DiT/consistency/求解器和视频等剩余复核继续。


第四十四批深化LDM／DiT／Consistency Models／DPM-Solver并补HF VAE资源组R10；343项（318研究／25资源），核心三遍104、书面五检查106。核查decoder／CFG、CT例子初始化与超参、原DPM与++默认差异及负指标；见[本批审查](docs/evidence/latent_transformer_consistency_and_solver_audit_2026-10-20.md)和[逐文件说明](docs/evidence/forty_fourth_changes_2026-10-20.md)。全部剩余三遍与视频等领域继续，未训练或推理。


第四十五批深化VDM／VideoLDM／AnimateDiff；343项，核心三遍107、五条书面检查109。分清C3D-FID／I3D-FVD、条件抽样协议、时序／静态质量取舍与论文／示例／后继版本；见[本批审查](docs/evidence/video_diffusion_temporal_transfer_and_motion_adapters_2026-10-20.md)及[逐文件说明](docs/evidence/forty_fifth_changes_2026-10-20.md)。AnimateDiff原补充训练／评价协议仍待补，全部剩余三遍继续，未训练、推理或复现。


第四十六批深化CogVideoX并补R11微调／检查点配置资源组；344项（318研究／26资源），核心三遍108、五条书面检查110。核文字主导视频过滤、时空token／元素压缩、负指标、人评聚合与公开版本／默认值差异；见[本批审查](docs/evidence/cogvideox_video_compression_data_and_finetuning_2026-10-20.md)及[逐文件说明](docs/evidence/forty_sixth_changes_2026-10-20.md)。全部剩余深审继续，未训练／推理／复现。


第四十七批深化Wan2.1：344项目录，核心三遍109、五条书面检查111。核专门中英视觉文字数据、流式VAE/采样缓存/蒸馏分支差异、负指标与gap/步数/帧率矛盾，并固定代码默认及负提示。见[本批审查](docs/evidence/wan_visual_text_flow_training_and_evaluation_audit_2026-10-20.md)、[逐文件说明](docs/evidence/forty_seventh_changes_2026-10-20.md)。全部剩余审查继续；无模型训练、推理或独立复现。


第四十八批深化LoRA/QLoRA/DoRA/rsLoRA：344项目录，113核心三遍、115五条书面检查。区分低秩表示、量化存储、模长/方向和rank缩放，保留主表负项、配方冲突与语言证据迁移边界。见[本批审查](docs/evidence/parameter_efficient_adaptation_rank_quantization_and_weight_decomposition_2026-10-20.md)与[逐文件说明](docs/evidence/forty_eighth_changes_2026-10-20.md)。全部剩余工作继续；无训练、推理或独立复现。


第四十九批深化ControlNet/CFG：344项目录，115核心三遍、117五条书面检查。修正CFG分辨率训练步数，保留FID文字/表图冲突与等速度负结果；核ControlNet初始零残差、代码/hint/RW差异和二维到时序边界。见[本批审查](docs/evidence/spatial_control_classifier_free_guidance_and_protocol_gaps_2026-10-20.md)与[逐文件说明](docs/evidence/forty_ninth_changes_2026-10-20.md)。无训练、推理或独立复现；剩余深读继续。


第五十批深化GAN/VAE原始理论与实验：344项目录，117核心三遍、119五条书面检查。区分理想分布均衡/有限网络、ELBO/似然/Parzen与重建/生成，保留TFD和小数据test反例。见[本批审查](docs/evidence/gan_vae_theory_estimation_and_video_representation_boundaries_2026-10-20.md)与[逐文件说明](docs/evidence/fiftieth_changes_2026-10-20.md)。无训练、推理或独立复现；剩余工作继续。


第五十一批深化VBench/FVD核心、既有验证与固定官方评价代码：344项目录，119核心三遍、121五条书面检查。保留VBench版本/相关系数名称差异、FVD样本偏差及非全胜结果；++/2.0和ContentBias继续追读。见[本批审查](docs/evidence/video_evaluation_vbench_fvd_protocol_and_scope_2026-10-20.md)与[逐文件说明](docs/evidence/fifty_first_changes_2026-10-20.md)。无训练、推理或独立复现；剩余工作继续。


第五十二批新增并精读Content Bias G033：345项目录（319研究／26资源），核心三遍120、五条书面检查122。核同空间质量扰动、冻结重采样、长视频反例与固定实现，纠正T3把分差标百分比的错误；见[本批审查](docs/evidence/content_bias_fvd_temporal_sensitivity_and_resampling_2026-10-20.md)和[逐文件说明](docs/evidence/fifty_second_changes_2026-10-20.md)。未删除文件、训练、推理或独立复现，全部剩余工作继续。


第五十三批新增并精读VBench++ G034：346项（320研究／26资源），核心三遍121、书面检查123。核I2V裁图/专家、可信人评与固定评分实现，记录2026正式卷期、肤色归一化/安全阈值/背景特征差异及有效样本分母。见[本批审查](docs/evidence/vbench_plus_i2v_trustworthiness_protocol_and_implementation_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_third_changes_2026-10-20.md)。无删除、训练、推理或复现；全部剩余工作继续。


第五十四批新增VBench-2.0 G035并完成核心精读：347项（321研究／26资源），核心三遍122、书面检查124。核18维事件/物理评价、人体异常训练资源和指定固定代码；记录条件分母、预筛失败计分、无人检测满分及MotionOrder相关名称疑问。见[本批审查](docs/evidence/vbench2_intrinsic_faithfulness_events_and_conditional_scores_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_fourth_changes_2026-10-20.md)。无删除或模型复现；原有剩余研究继续。


第五十五批补完原记录Chameleon/U01、Transfusion/U05核心三遍：目录347项不变，核心124、书面126。修订训练token口径、Chameleon总体/子集胜率、稳定性曲线表述和Transfusion共享代价/FLOP估计、patch暴露混杂。见[原文审查](docs/evidence/chameleon_transfusion_shared_model_cost_and_claim_audit_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_fifth_changes_2026-10-20.md)。无删除/模型复现；Janus/Show-o及其他剩余继续。


第五十六批补完原Janus/U03、Show-o/U06核心精读：347目录不变、126核心/128书面。修订解耦/共享收益、版本/指标、CFG与采样成本；纳入Show-o视频扩展，并限定附录公式问题的适用范围。见[原文审查](docs/evidence/janus_showo_representation_video_and_math_audit_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_sixth_changes_2026-10-20.md)。无删除/训练复现，剩余精读继续。


第五十七批补完InkSight/X01、VideoSketcher/L010核心精读：347目录不变，128核心/130书面。补齐配方、主表/消融、并笔率/统计口径、TF版本与HF制品访问，纠正合理轨迹/规范笔序及偏好/准确率混用。见[原文审查](docs/evidence/inksight_videosketcher_trajectory_events_and_resource_audit_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_seventh_changes_2026-10-20.md)。无删除/模型复现；SketchAgent及剩余继续。


第五十八批补完SketchAgent/L012与ProcessPainter/L013核心：347目录不变，130核心/132书面。记录正式新增字母串/网格实验、协作边界、关键帧与末帧重建评价，以及公开代码与论文的配置差异。见[原文审查](docs/evidence/sketchagent_processpainter_protocol_and_claim_audit_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_eighth_changes_2026-10-20.md)。无删除/训练或独立复现；剩余继续。


第五十九批补完PaintsAlter/L014、StrokeNUWA/L016核心：347目录保持，132核心/134书面。补齐非连续查询、数字编辑/规范事件差别、矢量压缩质量取舍、指标方向冲突及公开示例配置。见[原文审查](docs/evidence/paintsalter_strokenuwa_query_representation_and_metrics_audit_2026-10-20.md)、[逐文件说明](docs/evidence/fifty_ninth_changes_2026-10-20.md)。无删除或独立复现；DiffSketcher新版与剩余继续。


第六十批补完DiffSketcher/L017、Diff-Font/L018明示版本核心：347目录保持，134核心/136书面，213项未确认核心三遍（含资源）。明确优化过程与真实书写、笔画计数与顺序、版本及guidance指标取舍，核对公开warmup/batch/embedding差异。见[原文审查](docs/evidence/diffsketcher_difffont_condition_process_and_configuration_audit_2026-10-20.md)、[逐文件说明](docs/evidence/sixtieth_changes_2026-10-20.md)。无删除或独立复现；剩余继续。


第六十一批（2026-10-21）补完FontDiffuser/L019、DiffBrush/L023核心：347目录、136核心/138书面，211项尚未确认核心三遍（含资源）。区分未见内容/字体/作者、静态行与真实事件、下游OCR指标，补齐模块tradeoff及公开推理/文章配方差异。见[原文审查](docs/evidence/fontdiffuser_diffbrush_generalization_metrics_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_first_changes_2026-10-21.md)。无删除或独立复现；剩余继续。


第六十二批（2026-10-21）补完Emu3/U02、Janus-Pro/U04核心：347目录、138核心/140书面，209项尚未确认核心三遍（含资源）。Emu3 Nature正式扩展与2024v1分列，补重写/后处理、tokenizer/配方消融和CALVIN模拟边界；Janus-Pro缺少逐因素消融，明确记录归因限制。见[原文审查](docs/evidence/emu3_januspro_versions_training_and_causal_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_second_changes_2026-10-21.md)。无删除或独立复现；剩余继续。


第六十三批（2026-10-21）补完AnyText/L025、UniVid/L027核心：347目录、140核心/142书面，207项尚未确认核心三遍（含资源）。AnyText v1/v1.1多因素更新、区域OCR指标与社区底模分列；UniVid论文/代码差异、VBench命名和ActivityNetQA规模问题明确保留。见[原文/实现审查](docs/evidence/anytext_univid_protocol_code_and_namesake_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_third_changes_2026-10-21.md)。无删除/独立复现；同名新线索与剩余记录继续。


第六十四批（2026-10-21）补完N10视频文字保持、N11 CalliffusionV2、N12 CalliPaint核心：347目录、143核心/145书面，204项尚未确认核心三遍（含资源）。明确无量化/消融、额外参考信息和四选人评证据限制；确认CalliPaint为NeurIPS2023 Workshop。见[审查](docs/evidence/calligraphy_inpainting_and_video_text_evidence_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_fourth_changes_2026-10-21.md)。无删除/独立复现；RePaint原始方法与剩余条目继续。


第六十五批（2026-10-21）补录G036原RePaint与G037线性理论：349目录、145核心/147书面，204项尚未确认核心三遍（含资源）。核同预算消融/固定实现差异及有效mask条件，记录Th8的局部总体矩反例，未模型复现。见[审计](docs/evidence/repaint_sampling_and_linear_theory_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_fifth_changes_2026-10-21.md)。无删除，旧条目/跨领域覆盖继续。


第六十六批（2026-10-21）补完N06 Veo零样本、N07真实多层手写数据库、N13 Unwritten核心/书面检查；349目录、148核心/150书面，201项尚未确认核心三遍（含资源）。核oracle/无效评价、正式回归T3–7、融合与拼接证据及门控卡边界。见[审查](docs/evidence/video_reasoning_and_handwriting_observability_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_sixth_changes_2026-10-21.md)。无新增独立论文、无删除/复现。


第六十七批（2026-10-21）补完U08 Zebra-CoT v2核心/书面检查与固定版本模型卡/数据卡/代码审查；349目录、149核心/151书面，200项尚未确认核心三遍（含资源）。补入BAGEL负面结果、主附表/采样数差异、GT前缀信息与代码配置边界；正式终稿访问受限单列。见[审查](docs/evidence/zebra_cot_negative_results_and_artifact_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_seventh_changes_2026-10-21.md)。无重复论文新增、无删除/模型复现。


第六十八批（2026-10-21）补完G030 Diffusion Forcing正式核心/书面检查；349目录、150核心/152书面，199项尚未确认核心三遍（含资源）。核实正式理论p20 KL符号问题、主表反例/任务指标及paper/main代码版本差异。见[审查](docs/evidence/diffusion_forcing_theory_protocol_and_versions_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_eighth_changes_2026-10-21.md)。无新增独立论文/删除/模型复现。


第六十九批（2026-10-21）补入G038 History-Guided Video Diffusion正式核心/五条书面检查；350目录、151核心/153书面，199项尚未确认核心三遍（含资源）。审查HG-v/f/t、ELBO及路径一致性条件、主表反例/尺度/EMA/机器人与人工长导航，关联固定代码与HF制品。见[审查](docs/evidence/history_guided_video_diffusion_audit_2026-10-21.md)、[逐文件说明](docs/evidence/sixty_ninth_changes_2026-10-21.md)。新增1项论文，无删除或模型复现。


第七十批（2026-10-21）补完L086 JanusFlow（CVPR2025）/L092 Harmon（ICCV2025）正式核心与书面检查，350目录、153核心/155书面，197项尚未确认核心三遍（含资源）。补正式表号/反例、实际框架与协同图、VAE/采样成本及HF后续decoder微调制品，见[审查](docs/evidence/janusflow_harmon_shared_representation_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventieth_changes_2026-10-21.md)。无新增独立论文/删除/模型复现。


第七十一批（2026-10-21）补完G027 EDM正式核心，350目录、154核心/156书面，196条未确认核心三遍（含资源）。修订NFE/FID摘要、最低三次/检查点选择统计、数值/训练因果与书写增广条件，见[审查](docs/evidence/edm_numerics_training_and_selection_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_first_changes_2026-10-21.md)。无删除或模型复现。


第七十二批（2026-10-21）补完L185 DDPO正式核心，350目录、155核心/157书面，195条未确认核心三遍（含资源）。补实际奖励/消融图、策略代理/按维密度缩放、奖励漏洞与GPU/LoRA/HF制品，见[审查](docs/evidence/ddpo_policy_surrogate_rewards_and_artifacts_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_second_changes_2026-10-21.md)。无删除或模型复现。


第七十三批（2026-10-21）补完L001有序轨迹恢复/L004布局笔迹核心，350目录、157核心/159书面，193条未确认核心三遍（含资源）。核严格OrderAcc边界/方向与密度、原始消融冲突及源包缺supp，见[审查](docs/evidence/ordered_recovery_and_layout_strokes_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_third_changes_2026-10-21.md)。无删除或模型复现。


第七十四批（2026-10-21）补完Painter L180/StrokeFusion G024正式核心、实际表图及固定代码/HF；350目录、159核心/161书面，191条未确认核心三遍（含资源）。核反馈缺失消融、集合等变/笔顺边界、主表反例与PR实现差异，见[审查](docs/evidence/painter_and_strokefusion_feedback_geometry_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_fourth_changes_2026-10-21.md)。无删除或模型复现。


第七十五批（2026-10-21）补完StrokeBank L005正式IAAI核心和Loomis Painter L015最新v3/附录/指定制品；350目录、161核心/163书面，189条未确认核心三遍（含资源）。校正会场/题名、旧版指标/划分与最新反例/人评/制品可用性，见[审查](docs/evidence/strokebank_and_loomis_painter_version_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_fifth_changes_2026-10-21.md)。无删除或模型复现。


第七十六批（2026-10-21）补完MMaDA L063正式NeurIPS核心/指定补充与Think in Strokes L029固定v3核心；350目录、163核心/165书面，187条未确认核心三遍（含资源）。纠正主表/子集/涨幅和版本，补官方关联RL实现及其与原论文差异。见[审查](docs/evidence/mmada_and_think_in_strokes_protocol_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_sixth_changes_2026-10-21.md)。无删除或模型复现。


第七十七批（2026-10-21）补完L047女书正式核心/固定代码与CSV统计，重审L184 Stroke-Seg正式全文；L184实际图表视觉待核，保留未完成。350目录、164核心/167项五条书面记录（含未通过项），186条未确认核心三遍（含资源）。见[审查](docs/evidence/nushu_and_stroke_seg_data_protocol_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_seventh_changes_2026-10-21.md)。无删除或模型复现。


第七十八批（2026-10-21）补完L075 Versatile Diffusion与L077 Emu正式核心/指定补充，核对实际框架主表及固定代码/HF。350目录、166核心/169项五条书面（含未通过项），184条未确认核心三遍（含资源）。见[证据审查](docs/evidence/versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_eighth_changes_2026-10-21.md)。无删除或模型复现。


第七十九批（2026-10-21）补完LaVIT L079正式核心/指定附录及实际图表，核固定代码/HF后续LLaMA2-v2模型。350目录、167核心/170项五条书面（含未通过项），183条未确认核心三遍（含资源）。见[审查](docs/evidence/lavit_dynamic_tokens_and_version_audit_2026-10-21.md)、[逐文件说明](docs/evidence/seventy_ninth_changes_2026-10-21.md)。无删除或模型复现。


第八十批（2026-10-21）补完UniFlow L072正式ICLR核心/指定附录、实际图表及固定推理制品。350目录、168核心/171项五条书面（含未通过项），182条尚未确认核心三遍（含资源）。见[审查](docs/evidence/uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)、[逐文件说明](docs/evidence/eightieth_changes_2026-10-21.md)。无删除或模型复现。


第八十一批（2026-10-21）补完TokenFlow L094正式CVPR核心/官方supp和实际框架主表消融，核固定代码/HF。350目录、169核心/172项五条书面（含未通过项），181条尚未确认核心三遍（含资源）。见[审查](docs/evidence/tokenflow_shared_indices_and_claim_audit_2026-10-21.md)、[逐文件说明](docs/evidence/eighty_first_changes_2026-10-21.md)。无删除或模型复现。


第八十二批（2026-10-21）补完MetaMorph L090正式核心/supp及固定代码；核对重复200K行、逐任务负迁移、相关性混杂与条件丢弃参数。350目录、170核心/173项五条书面（含未通过项），180条尚未确认核心三遍（含资源）。见[审查](docs/evidence/metamorph_synergy_and_data_budget_audit_2026-10-21.md)、[逐文件说明](docs/evidence/eighty_second_changes_2026-10-21.md)。无删除或模型复现。


第八十三批（2026-10-21）补完扩散视觉综述G022固定v5研究核心，核三框架/分类表、变分界与Ramesh/Avrahami归属。350目录、171核心/174项五条书面（含未通过项），179条尚未确认核心三遍（含资源）。见[审查](docs/evidence/diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)、[逐文件说明](docs/evidence/eighty_third_changes_2026-10-21.md)。无删除或模型复现。


第八十四批（2026-10-21）补完效率综述G023固定v2研究核心；更正逆SDE/NFE/模型组件归属，201项新增发现层候选未计精读。350目录、172核心/175项五条书面（含未通过项），178条尚未确认核心三遍（含资源）。见[审查](docs/evidence/diffusion_efficiency_full_pipeline_audit_2026-10-21.md)、[逐文件说明](docs/evidence/eighty_fourth_changes_2026-10-21.md)。正式终版待读，无删除或模型复现。


第八十五批（2026-10-21）补完UniDiffuser L076正式研究核心与固定制品审查。350目录、173核心/176项五条书面（含未通过项），177条未确认核心三遍（含资源）。CFG额外调用、文字codec与v1内部续训已明确。见[审查](docs/evidence/unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[逐文件说明](docs/evidence/eighty_fifth_changes_2026-10-21.md)。无删除或模型复现。


第八十六批（2026-10-21）补完Tora L034正式版和Tora2 L035固定v2研究核心/制品边界。350目录、175核心/178项五条书面（含未通过项），175条未确认核心三遍（含资源）。见[审查](docs/evidence/tora_motion_binding_and_process_boundary_audit_2026-10-21.md)与[逐文件说明](docs/evidence/eighty_sixth_changes_2026-10-21.md)。Tora3和Wan玩偶LoRA只进入追查，无删除/模型复现。


第八十七批（2026-10-21）新增Tora3 G039固定v3核心精读和Wan玩偶LoRA R12非论文资源协议审查。352目录、176核心/179项五条书面（含未通过项），176条未确认核心三遍（含资源）。见[审查](docs/evidence/tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)与[逐文件说明](docs/evidence/eighty_seventh_changes_2026-10-21.md)。资源审查不计论文完成；无删除/模型复现。


第八十八批（2026-10-21）补完MotionCtrl L039明确v2核心/补充与固定发布审查。352目录、177核心/180项五条书面（含未通过项），175条未确认核心三遍（含资源）。见[审查](docs/evidence/motionctrl_camera_object_and_observability_audit_2026-10-21.md)与[逐文件说明](docs/evidence/eighty_eighth_changes_2026-10-21.md)。保留联合复杂运动低成功率与HF链接/采样配置未决，无删除/模型复现。


第八十九批（2026-10-21）补完Unified-IO 2 L058、AnyGPT L059正式核心/指定补充与固定发布审查。352目录、179核心/182项五条书面（含未通过项），173条未确认核心三遍（含资源）。见[审查](docs/evidence/unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)与[逐文件说明](docs/evidence/eighty_ninth_changes_2026-10-21.md)。AnyGPT正式音乐词表冲突解除；保留图像择优/真实音频history、缺机制消融及配置口径，无删除/模型复现。


第九十批（2026-10-21）补完SEED-X L060固定v2HTML核心/实际来源图、UniTok L061正式核心/指定附录，补录SEED-Data-Edit G040报告/固定标注样本。353目录、182核心/185书面含未通过项，171条未确认核心。保留CFG反例、缺定量消融/多轮拆单轮与有限样本来源映射未决。见[审查](docs/evidence/seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninetieth_changes_2026-10-21.md)。无删除/模型复现。


第九十一批（2026-10-21）补完Word-As-Image L051、Strike a Chord L052固定核心/指定附录与实际框架/主表/消融，核静态优化video输出及论文/发布差异。353目录、184核心/187书面含未通过项，169条未确认核心。见[审查](docs/evidence/semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_first_changes_2026-10-21.md)。DS-Fusion已定位ICCV2023来源待下一批，不计本批已读。无删除/模型复现。


第九十二批（2026-10-21）完成前批待补DS-Fusion：新增G041正式核心/实际图表/指定supp和固定代码/HF Express制品。354目录、185核心/188书面含未通过项，169条未确认核心。见[审查](docs/evidence/dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_second_changes_2026-10-21.md)。保留SF/MF取舍、胜出与Equal区别及epoch/step/风格图/默认首字符等发布条件，无删除/模型复现。


第九十三批（2026-10-21）补完L062 MetaQueries/L074 Unified-IO固定核心三遍/实际图表与指定发布。354目录、187核心/190书面含未通过项，167条未确认核心。见[审查](docs/evidence/metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_third_changes_2026-10-21.md)。记录单向迁移、任务干扰、embedding梯度/decay与数据构造差异；无删除/模型复现。


第九十四批（2026-10-21）补完L078初版SEED/L082 SEED-LLaMA指定版本核心三遍、实际框架/表格及发布。354目录、189核心/192书面含未通过项，165条未确认核心。见[审查](docs/evidence/seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_fourth_changes_2026-10-21.md)。区分77文字/1图像条件、格式成功/语义质量、原始论文/发布配方；无删除/模型复现。


第九十五批（2026-10-21）补完L053 Timage/L054 BoxTuning公开v1核心三遍、实际框架/主表/消融和指定发布。354目录、191核心/194书面含未通过项，163条未确认核心。见[审查](docs/evidence/timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_fifth_changes_2026-10-21.md)。Timage训练/样本/聚合矛盾和Box正式书目/README效率分别记录，核心阅读完成不表示结论确证；无删除/模型复现。


第九十六批（2026-10-21）追引新增G042 AutoConverter/VMCBench和G043 ObjectMLLM正式核心/指定附录、实际图表与固定发布，补正L053的9450筛查前含义、L054的既有画框/标注实验边界。356目录、193核心/196书面含未通过项，163条未确认核心。见[审查](docs/evidence/autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_sixth_changes_2026-10-21.md)。无删除/模型复现。


第九十七批（2026-10-21）完成L064 MANZANO/L071 GenEval固定v1核心、实际图表/指定附录与选定代码；校正颜色候选、任务协同范围、表文及GenEval聚合疑点。356目录、195核心/198书面含未通过项、161条未确认核心。见[审查](docs/evidence/manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)和[逐文件说明](docs/evidence/ninety_seventh_changes_2026-10-21.md)。无删除/模型复现。


第九十八批（2026-10-21）完成L065 Qwen3-Omni/L066 Emu3.5固定v1核心、主表/实际图表、选定GH/HF发布；区分真实生成模态、受控Base与后训练、三种扩散/负迁移、未发布DiDA和自动具身评价。356目录、197核心/200书面含未通过项，159条未确认核心。见[审查](docs/evidence/qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_eighth_changes_2026-10-21.md)。无删除/模型复现。


第九十九批（2026-10-21）完成L067 XTC-Bench/L068 IMUG-Bench固定v1核心、实际图表及固定代码/文本元数据审查；记录正确性对称与内容一致性、BLIP3o误分PureAR、MCQ连续多选解析缺陷/37条真值、动态history/几何评分差异。356目录、199核心/202书面含未通过项，157条未确认核心。见[审查](docs/evidence/xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[逐文件说明](docs/evidence/ninety_ninth_changes_2026-10-21.md)。无删除/模型复现。


第一百批（2026-10-21）完成L069 Unison正式ICML2026核心与L070 VGAU-Diag v2核心、实际框架主表/协议对照及固定代码文本审查；澄清GGU直接/带图评分、ME累计检出与终态、rho含义、oracle与停止probe预算。356目录、201核心/204书面含未通过项，155条未确认核心。见[审查](docs/evidence/unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundredth_changes_2026-10-21.md)。无删除/模型复现。


第一百零一批（2026-10-21）完成L080 NExT-GPT正式核心和L081 DreamLLM固定v2核心、实际图表/消融及GH/HF配置审查，纠正155M参数归属与ID含义，保留表间冲突/发布配方差异。356目录、203核心/206书面含未通过项，153条未确认核心。见[审查](docs/evidence/nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_first_changes_2026-10-21.md)。无删除/模型复现。


第一百零二批（2026-10-21）完成L083 Emu2固定v2与L085 VILA-U固定v3核心、实际指定框架/主表/现有消融及GH/HF发布审查；分开base/Chat/Gen、0*、表征取舍、空间/深度AR和8帧PNG协议。356目录、205核心/208书面含未通过项，151条未确认核心。见[审查](docs/evidence/emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_second_changes_2026-10-21.md)。无删除/模型复现。


第一百零三批（2026-10-21）完成L045 CalliReader/CalliBench与L046 AWCV-100K/VCRec核心、实际图表及固定GH/HF发布审查；区分阅读顺序、空中书写识别与规范笔顺生成，记录无序F1、发布数据行数、参数/解码协议和英文反例。356目录、207核心/210书面含未通过项，149条未确认核心。见[审查](docs/evidence/callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_third_changes_2026-10-21.md)。无删除/模型复现。


第一百零四批（2026-10-21）完成L088 Liquid/L089 ILLUME指定版本核心、实际图表及发布范围；纠正Liquid语言对照缺失的旧说法，区分规模趋势、额外数据收益与协同，明确ILLUME教师及15M成本口径/版本差异。356目录、209核心/212书面含未通过项，147条未确认核心；ILLUME+/X留后续审查。见[审查](docs/evidence/liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_fourth_changes_2026-10-21.md)。无删除/模型复现。


第一百零五批（2026-10-21）完成L091 UGen/L093 X-Omni固定核心、实际框架/主表/已有消融及指定制品；核课程mask与PPL、7/8基准和k∞差异，纠正中文长文本全优说法，明确无序加权召回、En/Zh与扩散CFG。356目录、211核心/214书面含未通过项，145条未确认核心。见[审查](docs/evidence/ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_fifth_changes_2026-10-21.md)。无删除/模型复现。


第一百零六批（2026-10-21）完成L095 QLIP/L096 DualToken固定核心、实际框架/主表/消融与指定代码；核量化前后理解、固定loss比例、双码head与完整成本、受控双encoder及脚本/论文差异。356目录、213核心/216书面含未通过项，143条未确认核心。见[审查](docs/evidence/qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_sixth_changes_2026-10-21.md)。无删除/模型复现。


第一百零七批（2026-10-21）完成L036 MotiMotion/L037 Fluid-Gen-Zero固定核心、实际框架/主表/消融，确认正式ICML身份并审查公开指令/HF标注；区分加权偏好、仿真参照与真实物理，记录Flow/Tool类别差异及质量退步。356目录、215核心/218书面含未通过项，141条未确认核心。见[审查](docs/evidence/motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_seventh_changes_2026-10-21.md)。无删除/模型复现。


第一百零八批（2026-10-21）完成L038 RefTok固定核心/实际F2和完整T1–3，补全题名并区分参考side information、名义压缩和新文字生成；L184新图2下载入口仍403，保留未验收。356目录，216核心/219书面含未通过项，140条未确认核心（含资源）。见[审查](docs/evidence/reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_eighth_changes_2026-10-21.md)。无删除/模型复现。


第一百零九批（2026-10-21）完成L040 DragNUWA/L041 DragAnything固定核心和实际图表，确认ECCV身份，审查当前发布、ObjMC和343JSON/4367轨迹；区分原LD/HD与SVD、额外mask、26/12百分点与正式评测输入。356目录，218核心/221书面含未通过项，138条未确认核心（含资源）。见[审查](docs/evidence/dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_ninth_changes_2026-10-21.md)。无删除/模型复现。


第一百一十批（2026-10-21）完成L042 TextVBench核心/实际F2/T1/T2/F5：持续文字双轨评价，extra未进H、归一移除标点空白、活跃路由/批划分/采样和诊断混杂；渐进书写需时变GT。356目录，219核心/222书面含未通过项，137条未确认核心（含资源）。见[审查](docs/evidence/textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[逐文件说明](docs/evidence/one_hundred_tenth_changes_2026-10-21.md)。无删除/模型复现。


第一百一十一批（2026-10-22）完成L043 ViTeX固定v2核心/AppA–O/实际F3-T2-T7，区分glyph加载纠正、CI跨0/时间取舍与旧人评；审查固定GH/HF/230+157清单和2041逐片已报数字，记录margin/PSNR/OCR串发布差异。356目录，220核心/223书面含未通过项，136条未确认核心（含资源）。见[审查](docs/evidence/vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_eleventh_changes_2026-10-22.md)。无删除/模型复现。


第一百一十二批（2026-10-22）完成L097 UniToken正式workshop核心/实际p3–6，并核arXiv更新表、固定GH/HF和改写prompt。纠正两阶段/三阶段、负迁移与指标退步，保留当前配置/评测协议缺口。356目录，221核心/224书面含未通过项，135条未确认核心（含资源）。见[审查](docs/evidence/unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twelfth_changes_2026-10-22.md)。无删除/模型复现。


第一百一十三批（2026-10-22）完成L098 Selftok固定v3核心/AppA/B与六页实际图表公式，补编辑总数据及负例，给出空间码前缀MDP反例、保留Eq20实现待核；核GH/HF发布和EMA/码序，前身DDT正式文献入全文队列。356目录，222核心/225书面含未通过项，134条未确认核心（含资源）。见[审查](docs/evidence/selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirteenth_changes_2026-10-22.md)。无删除/模型复现。


第一百一十四批（2026-10-22）补录G044 DDT-LLaMA正式CVPR2025核心/完整supp研究说明及实际图表，关联L098前身/扩展而不作独立重复创新；分别记录480码/GenEval.66、文本perplexity与人评案例、发布跳转范围。357目录，223核心/226书面含未通过项，134条未确认核心（含资源）。见[审查](docs/evidence/ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_fourteenth_changes_2026-10-22.md)。无删除/模型复现。


第一百一十五批（2026-10-22）完成L099 UniCode²固定v2核心、T1–6/AppA研究文字与七页实际图表公式，纠正T4参数单位位置，补全部主表/消融和量化反例；未定位对应版本公开代码/权重。357目录，224核心/227书面含未通过项，133条未确认核心（含资源）。见[审查](docs/evidence/unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_fifteenth_changes_2026-10-22.md)。没有文件删除或模型复现。


第一百一十六批（2026-10-22）完成L100 TUNA正式CVPR正文、官方附录、固定v1和公开原版实现选读；记录联合训练MME下降、正文/附录学习率冲突、公开配方/发布边界及clean/noisy条件分支待测试。357目录，225核心/228书面含未通过项，132条未确认核心（含资源）。见[审查](docs/evidence/tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_sixteenth_changes_2026-10-22.md)。没有文件删除或模型复现。


第一百一十七批（2026-10-22）完成L101 UniWeTok固定v3核心/Eq1–9/33表和七页实际图表，核查BitDance共用代码与HF相关tokenizer制品；区分64位置/128bit、33B位置token/全成本及三个独立SFT变体。357目录，226核心/229书面含未通过项，131条未确认核心（含资源）。见[审查](docs/evidence/uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_seventeenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百一十八批（2026-10-22）完成L102 EvoTok固定v1核心/Eq1–11/五表和六页实际图表，核GH独立码本/EMA与训练入口及ECCV官方接收列表；保留表示深度、三项并列与主表/公开配方差异。357目录，227核心/230书面含未通过项，130条未确认核心（含资源）。见[审查](docs/evidence/evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_eighteenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百一十九批（2026-10-22）完成L104 UniCom固定v1核心/全部七表和七页实际图表，补原始特征旁路、OCR下降、VAEdecoder与WorldEdit文字/表格冲突；核GH/HF配置和理解入口shape待核项。357目录，228核心/231书面含未通过项，129条未确认核心（含资源）。见[审查](docs/evidence/unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_nineteenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十批（2026-10-22）完成L105 Tuna-2固定v2核心/全部六表及八页实际图表，补任务退步、重建额外微调、偏好90.1%和mask/噪声公开默认差异。357目录，229核心/232书面含未通过项，128条未确认核心（含资源）。见[审查](docs/evidence/tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twentieth_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十一批（2026-10-22）完成L106 Representation Forcing固定v4核心/三表含五子消融、AppA–C与六页实际PDF；核VLM-only反例、量化伪代码及AR完整成本。357目录，230核心/233书面含未通过项，127条未确认核心（含资源）。见[审查](docs/evidence/representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_first_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十二批（2026-10-22）完成L107 HYDRA-X固定v1核心/十三表、AppA–G与十页实际PDF，补视频运动反例、时间压缩/编辑/解码接口和训练比例边界；官方核L107及L103的NeurIPS2026身份。357目录，231核心/234书面含未通过项，126条未确认核心（含资源）。见[审查](docs/evidence/hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_second_changes_2026-10-22.md)。没有删除或模型复现。
