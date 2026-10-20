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
| 本轮逐篇阅读、理论与实验迁移 | [344份结构化笔记](docs/reviews/README.md) · [理论与迁移分析](docs/evidence/foundations_and_transfer_2026-10-19.md) · [逐条阅读台账](docs/evidence/reading_ledger_2026-10-19.md) |
| 全部文献 | [文献总表](docs/all_literature.md) · [CSV](data/literature.csv) · [Excel](data/literature_public.xlsx) |

## 主要判断

- **读写联合与中文书法统一生成已有前作。** [InkSight](https://arxiv.org/abs/2402.05804)联合识别与笔迹恢复，[UniCalli](https://arxiv.org/abs/2510.13745)统一列级书法识别与静态生成。研究贡献需要具体到过程理解及其对生成的作用。
- **笔顺条件不等于过程正确。** 静态字形、最终帧OCR和文字笔顺问答都不能独立证明实际生成顺序；需要检查具体笔画的身份、先后、方向与落笔状态。
- **轨迹、物理渲染和视频文字控制已有可比较的方法。** [OnOff](https://arxiv.org/abs/2608.03198)连接轨迹与墨迹渲染；[VidScribe](https://arxiv.org/abs/2609.36598)和[VTR-Bench](https://arxiv.org/abs/2610.01499)提供视频文字评测。它们的指标与规范笔顺验证仍有区别。
- **UMM的额外收益尚需实验确认。** 先比较过程理解与生成执行，再扩展多字、布局、风格和效率。不能仅凭一个模型同时支持理解和生成就认定二者互相促进。

## 文献与证据

主目录包含 **318项论文／研究记录、26项资源，共344条记录**。每项记录包括研究主张、方法、问题、结果、限制、原始来源、版本及核查范围。数量不代表全文精读数量；文献中的数值为作者报告。

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
