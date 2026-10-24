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


第一百二十三批（2026-10-22）完成L108 PixelUMM固定v1核心/九表八组实验与十页实际PDF，补官方代码/模型卡，记录15.2B总参、F7十一项图像退步、F8条件分层及linearhead发布边界。357目录，232核心/235书面含未通过项，125条未确认核心（含资源）。见[审查](docs/evidence/pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_third_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十四批（2026-10-22）完成L109 FUDOKI正式NeurIPS2025核心/五表/AppA–F及八页实际PDF，补固定GH/HF源码与配置，记录3.86M/3.71M、L2/四次方、32/128/50步差异与纠错对照限制。357目录，233核心/236书面，未确认核心97论文／研究+27资源（资源单独审查）。见[审查](docs/evidence/fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_fourth_changes_2026-10-22.md)。没有删除文件或执行模型。


第一百二十五批（2026-10-22）完成L111 LaViDa-O正式ICLR2026核心/16表/AppA–F及12页实际PDF，补固定GH/HF制品，记录Eq7区间冲突、16/17层边界、ground数据DPG退步和反思质量-延迟条件。357目录，234核心/237书面；未确认核心96论文／研究+27资源（资源单独审）。见[审查](docs/evidence/lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_fifth_changes_2026-10-22.md)。没有删除文件或执行模型。


第一百二十六批（2026-10-22）完成L112 Lumina-DiMOO全核心/十表与十一页实际PDF，补固定GH/HF及cache/SelfGRPO/局部编辑协议，纠正32倍重复相乘、任务全优和保留码等于RGB保持的误述。357目录，235核心/238书面；未确认核心95论文／研究+27资源（资源单独审）。见[审查](docs/evidence/lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_sixth_changes_2026-10-22.md)。无删除或执行模型。


第一百二十七批（2026-10-22）完成L113 Omni-Diffusion正式核心、全部八表与八实际PDF页，核对arxivv2及固定GH/HF。明确连续语音输入、两版WER/CLIP/RTF、位置缩放/预填与源码差异。357目录，236核心/239书面；未确认核心94论文／研究+27资源（资源单独审）。见[审查](docs/evidence/omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_seventh_changes_2026-10-22.md)。无删除或执行模型。


第一百二十八批（2026-10-22）完成L114 LLaDA2.0-Uni完整核心、十四表/Eq1–8与十三实际PDF页，核固定GH/HF的MoE、decoder与SPRINT。记录文字渲染差距、T4正文/表冲突、缓存剪枝及质量-速度折中。357目录，237核心/240书面；未确认核心93论文／研究+27资源（资源单独审）。见[审查](docs/evidence/llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_eighth_changes_2026-10-22.md)。无删除或执行模型。


第一百二十九批（2026-10-22）完成L115 FullFlow完整核心、十表与十五实际PDF页，核双时间RF/插入、输出梯度理论、先验保留评价及网页制品树。保留T4/T9数值、T8反例、T5/T6预算与算术冲突。357目录，238核心/241书面；未确认核心92论文／研究+27资源（资源另审）。见[审查](docs/evidence/fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_twenty_ninth_changes_2026-10-22.md)。无删除或执行模型。


第一百三十批（2026-10-22）完成L116 Multimodal Flow完整核心/附录研究、十表/Eq1–12及九实际PDF页，核固定GH/HF连续codec、块因果、预算和采样。记录oneobjective范围、等参数与等计算区别、数据/默认配置差异及生成-理解取舍。357目录，239核心/242书面；未确认核心91论文／研究+27资源。见[审查](docs/evidence/multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirtieth_changes_2026-10-22.md)。无删除或执行模型。


第一百三十一批（2026-10-22）完成L117 BLIP3-o v1完整核心/两主表/AppA与七实际PDF页，核原GH与HF模型/数据卡。分开公开8B与私有论文8B、原版与NEXT，记录语义flow公式勘误、64query单次前向和缺少joint/AI数据因果对照。357目录，240核心/243书面；未确认核心90论文／研究+27资源。见[审查](docs/evidence/blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_first_changes_2026-10-22.md)。无删除或执行模型。


第一百三十二批（2026-10-22）完成L118 OpenUni v3全部核心/六表与五实际PDF页，核固定GH训练/模型/评测和HF模型/数据元数据。记录轻连接器、GenEval模板分布、生成器解冻混杂、L512型号矛盾及公开/许可边界。357目录，241核心/244书面；未确认核心89论文／研究+27资源。见[审查](docs/evidence/openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_second_changes_2026-10-22.md)。无删除或执行模型。


第一百三十三批（2026-10-22）完成L119 UniFork v1全部核心/五表与八实际PDF页，核固定GH分支、冻结、RQ头和训练/采样。记录mutual-kNN观察的因果边界、T4聚合矛盾、专家残余差距及参数/分辨率/发布脚本差异。357目录，242核心/245书面；未确认核心88论文／研究+27资源。见[审查](docs/evidence/unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_third_changes_2026-10-22.md)。无删除或模型执行。


第一百三十四批（2026-10-22）完成L120 HunyuanImage3.0 v3全部核心/训练表和六实际PDF页，核固定GH及三HF模型配置/采样/权重索引。记录GSB绝对四格与净差、SSAE宏微平均、无受控消融、MoE观察及Base/Instruct/Distil/TMP边界。357目录，243核心/246书面；未确认核心87论文／研究+27资源。见[审查](docs/evidence/hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_fourth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十五批（2026-10-22）完成L121 DeepGen1 v2全部核心/附录11表与13实际PDF页，核主仓、独立RL和三类HF制品。记录SCB全上下文、投影/超参差异、RL任务退化、概率代理及公开UniGen训练提示与600测试提示的3条精确交集，未推定最终运行使用。357目录，244核心/247书面；未确认核心86论文／研究+27资源。见[审查](docs/evidence/deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_fifth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十六批（2026-10-22）完成L123 InternVL-U v1全部核心/附录、24表、17实际PDF页与固定模型/代码/TextEdit/EvalKit指定实现。记录理解5/7退化、CoT子类权衡及CFG混杂、RISE原表聚合疑问、TextEdit报告与发布指标差异、LongText无序召回边界。357目录，245核心/248书面；未确认核心85论文／研究+27资源。见[审查](docs/evidence/internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_sixth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十七批（2026-10-22）完成L124 Mamoda2.5 v1全部核心/附录13表、11实际PDF页与固定八文件推理制品指定源码。补核视频/字幕真实任务、25B/A3B口径、DiT计时95.9倍与实测7.5倍、Reco/理解负例、曲线标注与发布48Top5对报告128Top8差异。357目录，246核心/249书面；未确认核心84论文／研究+27资源。见[审查](docs/evidence/mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_seventh_changes_2026-10-22.md)。无删除或模型执行。


第一百三十八批（2026-10-22）完成L125 SenseNova-U1全部核心23表/Eq1–7与固定发布配置/指定源码。明确像素MoT真实任务、17.55B/38.74B索引参数、噪声能量解释、LongText计数召回、理解/OneIG退步、协同对照缺口及U1.5版本边界。357目录，247核心/250书面；未确认核心83论文／研究+27资源。见[审查](docs/evidence/sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_eighth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十九批（2026-10-22）完成L128 MindOmni正式NeurIPS2025核心9表/Eq1–7、9实际PDF页及固定代码/模型配置审查。区分原版WISE.60与追加HQ版.71，记录RGPO仅文字policy ratio、特征KL方向/优势归一化/启动任务名差异和CoT不单调。357目录，248核心/251书面；未确认核心82论文／研究+27资源。见[审查](docs/evidence/mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_thirty_ninth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十批（2026-10-22）完成L129 CoRL核心三遍、正式8表/Eq1–6及固定联合RL/数据卡审查。明确S1双任务提升与S2任务分支/合并边界、7%/23%相对均值、WISE排名、监督数据和公开reward默认/QA类型/概率位置待核差异。357目录，249核心/252书面；未确认核心81论文／研究+27资源。见[审查](docs/evidence/corl_joint_advantage_branch_and_reward_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_fortieth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十一批（2026-10-22）完成L130 PairUni完整HTML核心与附录、10表/Eq1–4和7实际原始图，核独立优势/std后权重、平方根与梯度解释、模板和阈值矛盾、主表退步与公开损失差异。更正旧会场断言及Lumina编辑表述。357目录，250核心/253书面；未确认核心80论文／研究+27资源。见[审查](docs/evidence/pairuni_pair_weighting_gradient_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_forty_first_changes_2026-10-22.md)。无删除或模型执行。


第一百四十二批（2026-10-22）完成L131 UniCorn正式ACL32页核心、17表/Eq1–9、指定附录及13实际PDF页；交叉核固定自身采样/SFT、HF和UniCycle完整评分代码。承认正式理论修正，记录外部persona、指标退步、裁判/词数接口和分母差异。357目录，251核心/254书面；未确认核心79论文／研究+27资源。见[审查](docs/evidence/unicorn_selfplay_joint_objective_and_unicycle_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_forty_second_changes_2026-10-22.md)。无删除或模型执行。


第一百四十三批（2026-10-22）完成L132 R3正式ICLR24页核心/指定附录、9表/Eq1–3及附录公式、12实际PDF页、固定Tree训练与七JSONL协议。发现发布GenEval训练与553测试有370字面提示重合，正式训练版本仍待核；记录理解范围、非单调轮数与代码配置边界。357目录，252核心/255书面；未确认核心78论文／研究+27资源。见[审查](docs/evidence/r3_tree_rl_understanding_scope_and_prompt_overlap_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_forty_third_changes_2026-10-22.md)。无删除或模型执行。


第一百四十四批（2026-10-22）完成L133 GvU正式CVPR11页全文/6表/Eq1–8、7实际PDF页、固定奖励/PEFT上下文/策略loss及评测协议。纠正表号、计数和理解负结果、曲线幅度；记录活动教师与论文clip差异及写实评测边界。357目录，253核心/256书面；未确认核心77论文／研究+27资源。见[审查](docs/evidence/gvu_intrinsic_probability_reward_and_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_forty_fourth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十五批（2026-10-22）完成L134 LVRPO完整17页核心/全部附录、7表/Eq1–16/Algo1、12实际PDF页。记录Eq16归一缺口、MI/梯度/W2论证边界、F3/F5与主表配置差异及公开制品待核。357目录，254核心/257书面；未确认核心76论文／研究+27资源。见[审查](docs/evidence/lvrpo_theory_reward_and_protocol_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_forty_fifth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十六批（2026-10-22）完成L135 Uni-Synergy完整23页核心/全部研究附录、6表/Eq1–34、17实际PDF页与固定官方cleaned源码/原HF卡片。保留主表收益，记录截断正态/SNR/控制器证明缺口、正式与公开奖励/loss差异、DGS接口问题及归档内部待核。357目录，255核心/258书面；未确认核心75论文／研究+27资源。见[审查](docs/evidence/uni_synergy_dgs_theory_and_personalization_release_audit_2026-10-22.md)、[逐文件说明](docs/evidence/one_hundred_forty_sixth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十七批（2026-10-23）完成L181正式11页全部研究正文/8表/Eq1–24/11图、10实际PDF页及固定官方源码。记录汉字部件联合学习的已有贡献、遮挡负迁移、TPE纸面/实现/几何证明差异及公开joint未完成边界。357目录，256核心/259书面；未确认核心74论文／研究+27资源。见[审查](docs/evidence/chinese_radical_joint_tpe_geometry_and_negative_transfer_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_forty_seventh_changes_2026-10-23.md)。无删除或模型执行。


第一百四十八批（2026-10-23）完成L182 STRIVE正式研究正文/2表/4式/10图、8实际PDF页和固定五文件发布审查；区分已有视频编辑、时序proxy与书写过程，核到Eq2符号/OCR口径和多副本速度条件。357目录，257核心/260书面；未确认核心73论文／研究+27资源。见[审查](docs/evidence/strive_video_text_replacement_and_propagation_protocol_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_forty_eighth_changes_2026-10-23.md)。无删除或模型执行。


第一百四十九批（2026-10-23）完成L183 CONSTANT正式10页正文+8页supp全部研究内容/12表/8式/20图、15实际PDF页及固定代码审查。补齐WER迁移协议/写者分类/越文切分，记录IV-U HWD、SCE FID局部退化、K/CFG/配权及公开评测差别。357目录，258核心/261书面；未确认核心72论文／研究+27资源。见[审查](docs/evidence/constant_multilingual_style_quantization_and_evaluation_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_forty_ninth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十批（2026-10-23）完成L137 STBridge v1全部研究正文/10式9表16图、20实际PDF页及有限官方发布检索。明确独立双路径一致评价与训练caption条件链、softgate代数边界及局部能力回退。357目录，259核心/262书面；未确认核心71论文／研究+27资源。见[审查](docs/evidence/stbridge_shared_target_alignment_and_causal_controls_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fiftieth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十一批（2026-10-23）完成L138 MATE全部正文/附录研究内容、5表5式3算法8图及11实际PDF页。补齐B200预算、零方差/准入fallback、全候选/分网消融及Fig8分项对应边界。357目录，260核心/263书面；未确认核心70论文／研究+27资源。见[审查](docs/evidence/mate_adversarial_pool_evolution_and_budget_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_first_changes_2026-10-23.md)。无删除或模型执行。


第一百五十二批（2026-10-23）：完成L139全部研究正文/AppA–E、5表2编号式10图及11实际PDF页；逐项审查CAGrad、代理指标方向、置信区间估计对象与投影混淆。357目录，261核心/264书面；未确认核心69论文／研究+27资源。见[审查](docs/evidence/gradient_conflict_metric_validity_and_causal_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_second_changes_2026-10-23.md)。无删除或模型执行。


第一百五十三批（2026-10-23）：完成L140全部研究正文/AppA–F、6表4式10图/10实际PDF页及源码包目录；核Show-o masked生成、调用/损失归因、参数数与选桶索引等差异。357目录，262核心/265书面；未确认核心68论文／研究+27资源。见[审查](docs/evidence/position_gradient_attribution_and_lora_budget_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_third_changes_2026-10-23.md)。无删除或模型执行。


第一百五十四批（2026-10-23）：完成L141正式全部研究正文/AppA–F、16式8表6图/10实际PDF页，核固定代码与2971条HF数据；记录缺stage、矛盾请求、推理拼接与条件机制边界。357目录，263核心/266书面；未确认核心67论文／研究+27资源。见[审查](docs/evidence/unike_cross_modal_editing_and_artifact_protocol_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_fourth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十五批（2026-10-23）：完成L143全部研究正文/AppA–J及1式7表28图，29实际PDF页；核1234提示/4231题和固定核心代码，得到恒A层级基线.351及自评混淆边界。357目录，264核心/267书面；未确认核心66论文／研究+27资源。见[审查](docs/evidence/unieval_self_evaluation_identifiability_and_answer_bias_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_fifth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十六批（2026-10-23）：完成L144 ACL2026正式17页全部研究正文/AppA–C及4表10图、12实际PDF页；核固定评价代码、八文件制品与HF卡，区分指标升降、已知k和原生/外部编排。357目录，265核心/268书面；未确认核心65论文／研究+27资源。见[审查](docs/evidence/unimmmu_state_parsing_oracle_length_and_synergy_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_sixth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十七批（2026-10-23）：L145完整23页/全部附录、3表12图37式及17实际PDF页；全部评测源码、510标注和五viewer静态核，区分裁判重复/生成重复、AQ下降、理论恒等式和实际性能保证。357目录，266核心/269书面；未确认核心64论文／研究+27资源。见[审查](docs/evidence/genius_contextual_rules_attention_theory_and_metric_tradeoffs_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_seventh_changes_2026-10-23.md)。无删除或模型执行。


第一百五十八批（2026-10-23）：L147正式21页全部研究正文/AppA–L、1式11表7图及8实际PDF页；固定源码及两版1000题结构/定向事实核，分清金标准重写、三项旧分与维护版二值分，未删文件。357目录，267核心/270书面；未确认核心63论文／研究+27资源。见[审查](docs/evidence/wise_gold_explanation_verified_protocol_and_knowledge_validity_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_eighth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十九批（2026-10-23）：L148正式31页全部研究正文/AppA–G、7表11图/16实际PDF页，纠正正式五次/早期三次，核737basic/47UGE和Judge独立制品；训练对与未完整tar未冒充全量核，未删文件。357目录，268核心/271书面；未确认核心62论文／研究+27资源。见[审查](docs/evidence/imgedit_dataset_versions_score_gating_and_pipeline_reproducibility_audit_2026-10-23.md)、[逐文件说明](docs/evidence/one_hundred_fifty_ninth_changes_2026-10-23.md)。无删除或模型执行。


第一百六十批（2026-10-24）：L150正式研究正文/AppA–F、3表36图图注及17实际图页/接触图，核固定五评价入口和GH/HF各1267标注。纠正hint对IF的负项，记录异常模板分支和空知识提示边界。357目录，269核心/272书面；未确认核心61论文／研究+27资源。见[审查](docs/evidence/kris_knowledge_hint_calibration_and_released_protocol_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixtieth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十一批（2026-10-24）：L149按arXiv v2完成核心三遍，读4表/Eq1/全部研究附录及实际图；核公开zip两清单和1692图片索引，记录缺QA/评分代码、相关估计单位未决及身份-语义取舍。正式PDF未完整，未当正式版通读。357目录，270核心/273书面；未确认核心60论文／研究+27资源。见[审查](docs/evidence/mmig_ams_estimand_and_public_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_first_changes_2026-10-24.md)。无删除或模型执行。


第一百六十二批（2026-10-24）：完整取得L149正式38页并读全部研究核心/附录、4表与公式；T2较v2新增UNO/RealCustom/OmniGen，表并集20与摘要17/官网18分列。核心条目仍270，未重复计数。357目录，270核心/273书面；未确认核心60论文／研究+27资源。见[审查](docs/evidence/mmig_formal_version_delta_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_second_changes_2026-10-24.md)。无删除或模型执行。


第一百六十三批（2026-10-24）：L142核7JSON共4101条、固定视频/迷宫等评分函数和HF路径。记录时间均值特征的顺序盲点、90迷宫终止图缺项与405/720步数分母；正式全文仍缺，五项书面保留未通过，核心数不增。357目录，270核心/274书面；未确认核心60论文／研究+27资源。见[审查](docs/evidence/mme_unify_temporal_metric_and_terminal_step_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_third_changes_2026-10-24.md)。无删除或模型执行。


第一百六十四批（2026-10-24）：L151补读正式研究正文、四表六图、公开评分及数据卡；核37表列/BAGEL18项最佳、16配置第二轮背景指标下降、全幅掩码PSNR面积偏置。独立补充未取得，五项书面保留未通过，核心数不增。357目录，270核心/275书面；未确认核心60论文／研究+27资源。见[审查](docs/evidence/compbench_region_metrics_and_released_protocol_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_fourth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十五批（2026-10-24）：L152完成正式36页研究正文/附录核心三遍与五项书面，核全主表及固定评分和2440提示。记录词序错误仍满分的公式反例、430/421人评计数、RC缺项、黑图分母和表内汇总差异。357目录，271核心/276书面；未确认核心59论文／研究+27资源。见[审查](docs/evidence/oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_fifth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十六批（2026-10-24）：L154完成正式主文与独立补充全部研究文字/表图核心三遍和五项书面。核静态编辑提升及理解/T2I取舍；长程能力仅有选例，未见距离分层成功率或组件消融。357目录，272核心/277书面；未确认核心58论文／研究+27资源。见[审查](docs/evidence/chatumm_context_tracking_and_claim_boundary_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_sixth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十七批（2026-10-24）：L156补齐完整HTML/附录A–G、全部15公式/五表/11原图核心三遍与五项书面；给出LR首次距离不足保证越过近期窗口的反例，明确UniLongGen*同权重和文字0分/字段汇总边界。357目录，273核心/278书面；未确认核心57论文／研究+27资源。见[审查](docs/evidence/long_horizon_memory_revisit_definition_and_scaling_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_seventh_changes_2026-10-24.md)。无删除或模型执行。


第一百六十八批（2026-10-24）：L157补齐完整v4正文/附录、16表/六图及固定公开推理入口；保留SFT后ASR退步和direct-s2s劣势，纠正Fig3为样例，并分列人评分母、视频关键帧和解码配置边界。357目录，274核心/279书面；未确认核心56论文／研究+27资源。见[审查](docs/evidence/mio_tokenization_modality_tradeoffs_and_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_eighth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十九批（2026-10-24）：L158完成正式正文+补充22页、12公式/九表14图；核实Eq11符号与scheduler不同、多输入入口受六任务断言限制，准确保留作者已讨论的triplet必要性及文本实体重建失真。357目录，275核心/280书面；未确认核心55论文／研究+27资源。见[审查](docs/evidence/omniflow_guidance_formula_and_released_task_coverage_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_sixty_ninth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十批（2026-10-24）：L159完成v3完整50页、11公式23表及全部图，给出动态权重非单调反例，修正两套对话评测与消融并列口径，核官方推理包/9B配置及缺失训练与生成接线。357目录，276核心/281书面；未确认核心54论文／研究+27资源。见[审查](docs/evidence/m2omni_dynamic_weight_formula_and_release_scope_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventieth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十一批（2026-10-24）：L160完成v1完整28页/15表八图，修正128帧与SANM执行分支，保留上下文语音WER退化，核三router共用专家池及仅最终尺度采样；配套Ming-Lite-Uni另排追引。357目录，277核心/282书面；未确认核心53论文／研究+27资源。见[审查](docs/evidence/mingomni_multiscale_bridge_and_context_tradeoff_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_first_changes_2026-10-24.md)。无删除或模型执行。


第一百七十二批（2026-10-24）：补录L191配套前作，完成v3研究全文/三表七实际图/四式；承认MSE文字收益但保留受控消融缺项，纠正文称.62超过.67，核M2论文与Qwen发布物、三次采样只返末图。358目录，278核心/283书面；未确认核心53论文／研究+27资源。见[审查](docs/evidence/ming_lite_uni_companion_multiscale_and_release_alignment_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_second_changes_2026-10-24.md)。无删除或模型执行。


第一百七十三批（2026-10-24）：L161完成v3全部研究正文/附录、11表五图；核T8混合macro与WER折中、T11完整性退化及正文冲突，固定Flash2.0实际单尺度和负条件参数未用，保留声/图指标退步。358目录，279核心/284书面；待完成核心深审52篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/ming_flash_omni_frozen_synergy_context_metric_and_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_third_changes_2026-10-24.md)。无删除或模型执行。


第一百七十四批（2026-10-24）：L162完成v2研究全文/16表12图两式；核文本18项11升7降及指令三项全退、ASR对Qwen1胜9负、100ms在VAD后和GPT4o第三方脚注，区分demo与服务链。358目录，280核心/285书面；待完成核心深审51篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/longcat_flash_omni_stage_tradeoffs_latency_and_service_identity_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_fourth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十五批（2026-10-24）：L184补核作者原图F2/F8、正式T2全部勾选行，纠正公开代码全固定六类的过宽说法；其余图版缺口保留未通过，不增加核心三遍数。358目录，280核心/285书面；待完成核心深审51篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/stroke_seg_author_figure_checkbox_and_sample_code_recheck_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_fifth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十六批（2026-10-24）：U09完成v3研究全文/全部附录prompts、8表24图，核成本比较矛盾、单任务/最终/hybrid配置与非单调采样；固定训练/评测/HF发布，保留图像因果及保真证据边界。358目录，281核心/286书面；待完成核心深审50篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/thinkmorph_full_reasoning_modes_cost_protocol_and_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_sixth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十七批（2026-10-24）：U11完成arXivv2正文/全部附录、7表9图及FindingsACL2026正式版补核；区分Zero791条SFT、800样本加权、TV平滑与功能正确性，记录默认min/多分支及输入图接线等发布缺口。358目录，282核心/287书面；待完成核心深审49篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/omni_r1_full_perception_reward_protocol_and_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_seventh_changes_2026-10-24.md)。无删除或模型执行。


第一百七十八批（2026-10-24）：U12完成arXivv1全部研究正文/附录、10表39图和公开评测/推理源码；核ACC缺失切公式、Zebra分母、同生成公式Logic下降及数学/迷宫等现行标注错误，区分论文图示与发布版本。358目录，283核心/288书面；待完成核心深审48篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/weave_full_interleaved_benchmark_scoring_and_annotation_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_eighth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十九批（2026-10-24）：U13完成v2全部研究正文/附录、13表10图16式；核622发布题与646差异、两侧答案信息不对称、联合成功越界及图judge改按错误文本的一致性。公开锚定已补，修正旧实现待核结论；fit统计单位/λ仍与论文不同。358目录，284核心/289书面；待完成核心深审47篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/gapeval_full_bidirectional_information_scoring_and_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_seventy_ninth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十批（2026-10-24）：U14完成v1全部研究正文/附录、14表24图及公式prompts；区分GtA相对Base和Direct、复算MIO25项差值、核动作词匹配与完整成功差别，以及当前limit1/多图wrapper入口边界。358目录，285核心/290书面；待完成核心深审46篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/unig2u_full_generation_to_understanding_budget_and_scoring_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eightieth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十一批（2026-10-24）：U15补齐v2完整19页研究正文附录、13表12图和公开两评分器；确认CVPR2026接收，区分UEG重写增益/GEU图替换，核2000行配对元数据及MT字段、坏核对项、当前聚合阻断。358目录，286核心/291书面；待完成核心深审45篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/realunify_full_bidirectional_stepwise_and_conjunctive_judging_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eighty_first_changes_2026-10-24.md)。无删除或模型执行。


第一百八十二批（2026-10-24）：U16完成v1完整18页研究正文/附录、两表六图八式和全部20推理/三组judgeprompt；核Eq5缺平均项、文本图像额外内容规则差异、Render地板/复用与两处r/p冲突。358目录，287核心/292书面；待完成核心深审44篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/vgubench_full_typographic_answer_and_correlation_identifiability_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eighty_second_changes_2026-10-24.md)。无删除或模型执行。


第一百八十三批（2026-10-24）：U17完成23页v1、10表10图；核任务解耦额外重建与预算混杂、几何单向/SVG和3D双向边界，以及同源端到端编辑对照。358目录，288核心/293书面；待完成核心深审43篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/native_synergy_full_routing_reconstruction_and_system_controls_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eighty_third_changes_2026-10-24.md)。无删除或模型执行。


第一百八十四批（2026-10-24）：U18完成ECCV2026 v2完整42页、13表13图及100空间prompt；核计数GTfallback、空间检出排除、文字样式差异与FID语义，官方HEAD仅README。358目录，289核心/294书面；待完成核心深审42篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/transferability_full_parser_coverage_and_distribution_shift_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eighty_fourth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十五批（2026-10-24）：U19完成ICML2026 v3完整16页4表7图20式；核三骨干对Base七指标全升及对RecA例外、Harmon公开512²/10K配置、四任务微batch/梯度scale、无类别边界与teacheragreement。358目录，290核心/295书面；待完成核心深审41篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/unimrg_full_teacher_targets_training_schedule_and_release_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eighty_fifth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十六批（2026-10-24）：U21完成v1完整17页8表15图7式算法1；核trace四象限/两同源骨干、AND对照、阈值重叠差别、91%图FLOPs与Eq7口径，保留实测延迟证据。358目录，291核心/296书面；待完成核心深审40篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/adavig_full_counterfactual_denominators_and_early_abort_cost_audit_2026-10-24.md)、[逐文件说明](docs/evidence/one_hundred_eighty_sixth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十七批（2026-10-25）：U22完成22页5表14图、固定官方评估/生成入口及1000条元数据核查；区分标准与题/任务/模态汇总，记录单模型人评/裁判与单例trace的证据边界。358目录，292核心/297书面；待完成核心深审39篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/ueval_full_rubric_aggregation_and_release_protocol_audit_2026-10-25.md)、[逐文件说明](docs/evidence/one_hundred_eighty_seventh_changes_2026-10-25.md)。无删除或模型执行。


第一百八十八批（2026-10-25）：U23完成完整HTML正文/附录、5表10图18式；核二维框对偶与软硬约束、四分支成本、rewrite/视频物理残余失败及完整反例。358目录，293核心/298书面；待完成核心深审38篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/sco_full_soft_constraint_solver_and_video_protocol_audit_2026-10-25.md)、[逐文件说明](docs/evidence/one_hundred_eighty_eighth_changes_2026-10-25.md)。无删除或模型执行。


第一百八十九批（2026-10-25）：U25完整34页/5表17图15式与所有证明；核局部Lipschitz证明范围、MMSI全522条六关系、评分/模型阶段差异及固定revision评测骨架。358目录，294核心/299书面；待完成核心深审37篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/visworld_full_theory_comparability_and_release_protocol_audit_2026-10-25.md)、[逐文件说明](docs/evidence/one_hundred_eighty_ninth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十批（2026-10-25）：U26完整35页、23表5图10式与五阶段训练；核文字计数指标的顺序盲区、外部PE和UniMMMU下降，固定公开训练范围/最终HF配置。358目录，295核心/300书面；待完成核心深审36篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.md)、[逐文件说明](docs/evidence/one_hundred_ninetieth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十一批（2026-10-25）：U27完整13页6图及三式，核latent扩散/共享视觉encoder、F2标签倒置与F5身份变化；无量化主表/消融/完整recipe，Claim限双向示例可行性。358目录，296核心/301书面；待完成核心深审35篇论文／研究；27项资源按制品协议另审。见[审查](docs/evidence/unimodel_full_visual_only_cycle_and_evidence_scope_audit_2026-10-25.md)、[逐文件说明](docs/evidence/one_hundred_ninety_first_changes_2026-10-25.md)。无删除或模型执行。
