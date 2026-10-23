# 第二轮原文复核与扩展调研：实际完成范围

本轮始于2026-10-19，更新截至2026-10-22。当前主目录357条，264项明确范围核心三遍/267项五条书面记录（含未通过项），93条尚未确认核心三遍，其中66条论文／研究、27条资源；资源另按制品与协议审查，不以论文三遍计数代表其未审。下文早期批次数量和待办保留为历史快照，当前逐条状态以[阅读台账](reading_ledger_2026-10-19.md)及后续批次为准。在main原HEAD `06210329c5667a0b0aed7a6e836417feff5a9d7f`基础上工作。研究范围覆盖统一多模态、静态/动态文字、在线轨迹、素描/绘画过程、视频基础模型、扩散/流理论、适配及评价。原档案和笔记保留，没有删除已有仓库文件。

## 已落地成果

- [334份逐篇结构化笔记](../reviews/README.md)：302份存量或新增研究/资源分析，32份基础/邻近研究；每份写问题、动机、机制、输入输出、数据、结构、指标、基线、条件、消融、局限、优势假设、可证伪实验及写作学习。329份相关章节/资源分析、5份仅第一遍；字段未核完时明确记录。
- [理论与实验迁移](foundations_and_transfer_2026-10-19.md)：解释关键公式的作用，区分噪声时间/视频时间、条件路径/边缘流、参数量/显存、文字可读性/事件正确性，并提出分层对照。
- [来源访问审计](../../data/source_access_audit_2026-10-19.json)：原281条+首轮16条+32条基础候选，共329条访问事件；同研究重复事件保留以便追溯，不能解释为329篇独立论文。只审计首选来源，未声称每条的所有外部链接均被打开。
- 首轮补录整合：16条来源映射到主目录，VideoSketcher沿用L010、Calligraphy Bench沿用L044，其余14条为S编号；代码/数据/权重按资源记录，并关联对应研究。新增32条G编号，再增加H001配套模型制品，再补STRIVE与CONSTANT两篇，再补Stroke-Seg与DDPO，以及G-HTR论文和U1.5八步LoRA资源（层级O2O沿用存量N08），主目录334条，其中311条论文/研究、23条资源。
- Markdown/CSV/JSON/Excel已同步。Excel保留原5个工作表，新增数据集、方法框架、模型结构、指标、基线、实验条件、笔记路径与阅读层级列；候选表保留。

[逐条完成台账](reading_ledger_2026-10-19.md)覆盖全部334条；[首批文件说明](second_round_changes_2026-10-19.md)及[继续复核文件说明](continued_changes_2026-10-20.md)列出每个新增/修改路径与原因。

## 纠错与证据限制

| 项目 | 复核发现 | 已采取的处理 |
| --- | --- | --- |
| Calligraphy Bench | 旧目录已经有L044，X2026-006未关联 | 补关联，不计为新发现；仍将其作为必须面对的直接前作 |
| U18 | 原先unresolved，现可读取v2 | 核方法、Tables1/4/12与条件；限制跨架构因果结论和文字增益 |
| DP-Font | 原PDF表中PSNR↓，CFG最优取决于指标 | 已视觉检查第7页，不以冲突指标认定改善 |
| VideoSketcher | 末帧辨识与作画顺序偏好不完全同向 | 分指标报告，Neither票不改写成顺序准确率 |
| DiffInk/OLHWG | 布局条件、额外标准字形输入影响比较 | 记录信息条件；表与正文速度不一致时保留差异 |
| Moyun | 数据规模叙述和IoU方向待厘清 | 不直接据此声称全部指标最优 |
| Janus/Show-o/U17 | 单任务与联合结果有升有降 | 保留负迁移和表示/先验混杂，提出匹配对照 |
| Transfusion | 图内注意力收益取决于外围编码器；消融FID样本较少 | 解释交互，不混5K/30K评估 |
| 访问成功 | arXiv转换壳、DOI跳转页可能HTTP200 | 日志区分正文候选/落地页/占位页，禁止自动升级阅读状态 |
| Write Like You | 命令行DOI403，后续Wiley元数据/摘要可读 | DOI原值经正式页面确认；已读北大作者公开正式PDF核心方法/主表/消融并核公开代码默认；补充材料未全读 |

所有数值均来自作者来源，尚无独立模型复现。论文的“最优”“首次”等表述均须检验比较范围；不能直接沿用宣传性Claim。

## 当前状态和未完成项

主目录334条：相关原文/资源章节329条、摘要5条、仅元数据0条、历史未重新核查0条（清零仅指初次相关章节核查）。原U18来源待解决项已经解除；这不表示其他条目全文已读。

334份结构化笔记中仍有完整附录、代码、逐图讲解和消融数表缺项。按用户给出的完整三遍验收，L020、L024、L073、L084、L087、L103、L110、L122、L126、L127、L136、L146、L153、L155、L169、U07、U10、L178、L003、S002、U20、U24、U29、U30、L186、N08及N01/N02/N03/N04/N05/N09/L011及L026/L028/L175/L176/L177/L179/S004五项书面检查已记录40项，尚无计时口试；其他条目未完成五项验收，没有将已写笔记自动计成读透。原文核查、三遍理解验收、代码核查和独立复现是不同工作量。

后续必须继续完成5条摘要记录、5份第一遍与已有笔记未读部分，以及其他仅摘要/元数据记录的精读和所有未验收项。以下访问问题需要定位公开替代或正式版本：

- L006出版社公开摘要、Introduction及部分section snippets已读；完整Method、公式和实验数表尚未取得。
- L021/L022 OpenReview入口受访问验证限制；另需核对投稿/撤稿/正式发表状态。第三方页面提到的撤稿标签未当作已核正式事实。
- L178已取得PDF并核核心方法/表及框架，期刊正式文与2016预印本的全量版本比对仍待完成。
- R04官方站直连证书过期/超时；已读取官方页面搜索索引中的介绍与格式。当前文件下载、协议与旧格式的一致性仍需复核，未关闭证书验证。
- G027 EDM正式主PDF的§1–6、Table1/2与算法已补读；独立补充材料的完整训练配置仍待核，不再记为仅第一遍。

引用追踪、跨语言资源及最新发布仍需持续检索。本次没有可审计的证据能保证全领域零遗漏，因此不作该声明。

## 验证范围

使用仓库目录校验器检查字段、ID、规范键、笔记路径、补录关联及内部Markdown链接；Excel检查工作表记录数、字段及筛选范围，并查看更新前后预览。未运行学习模型、未下载权重、未把外部论文PDF加入仓库。具体校验结果以提交中的结构与脚本为准。

首批历史校验结果：328条记录、193份Markdown的目录/路径/内部链接检查通过；16条补录映射检查通过。原校验器扫描了Git忽略的本地checkpoints，已改为Git跟踪文件和未忽略的新文件；没有删除或发布这些本地权重。Excel四个正式目录表分别为328/158/170/22条，原候选表保留。

## 继续复核的新增判断

[过程与执行比较](process_execution_boundaries_2026-10-19.md)补入L001严格整字笔顺、LVGM中文矢量续写、Cross-VAE双向模态、InkSight识别/书写联合等直接前作，防止选题新颖性遗漏。PaintsAlter数字编辑过程允许删除/变形，Loomis Painter的PDP与严格笔序不等价；FRIDA/CoFRIDA将仿真、语义与真实执行分层验证。

效率与训练方法覆盖HunyuanVideo1.5、LTX2、VACE、WanMove、SelfGradientForcing、Salt、WanR1、iMF、DiscreteFlowMatching、TeaCache与clDice。每项均保留未读附录/主表/训练字段，新增笔记不等于完成全部精读。CoFRIDA-Sharpie原始卡的基础模型字段冲突另立H001，不把论文分数赋给未经对齐的权重。

## 2026-10-20再次继续核查

19项原文核查升级使相关章节数达到131、历史待复核降至161，累计100份结构化笔记。见[本批清单](../../data/third_review_batch_2026-10-20.json)、[主张与跨文字审查](claims_and_cross_script_2026-10-20.md)、[文件变更说明](third_changes_2026-10-20.md)。L047正式题名补全并关联NüshuStrokes；未新增独立研究计数。InkDiffuser固定代码版本，StrokeBank式5已视觉核查，未解决的版本/公式差异仍保留。

## 第四批（2026-10-20）

新增24份来源限定笔记，相关章节记录增至150，历史待复核137；累计124份笔记。五项全文未取得的条目A06/L002/L006/L021/L022保持第一遍，与原G027共6项。L024全文、公式、主表/消融和Figure3完成核查，五项书面理解检查另行记录；无模型复现。见[本批清单](../../data/fourth_review_batch_2026-10-20.json)、[专题审查](gradient_metrics_and_resource_protocols_2026-10-20.md)及[文件说明](fourth_changes_2026-10-20.md)。前面第三批数字保留当时快照。

## 第五批（2026-10-20）

新增21份来源限定笔记，补录STRIVE（ICCV2021）与CONSTANT（WACV2026），累计330条记录与145份笔记。章节核查171条、摘要40条、元数据1条、历史待复核118条。此前批次数量保留为提交时快照。五项书面检查2项，不代表整篇附录/代码均已核完，完整三遍阅读完成数为0；修改生成脚本，避免由书面检查数量直接推算完整三遍数量。

[协议与任务审查](text_motion_and_protocol_audit_2026-10-20.md)、[本批清单](../../data/fifth_review_batch_2026-10-20.json)和[逐文件说明](fifth_changes_2026-10-20.md)记录具体范围。InkSpire、DiffVG、Strike a Chord、STRIVE与CONSTANT已取得可读取PDF；CalliReader补充材料已读指定部分。ViTeXBench版本/推理条件、CalliReader训练配置、STRIVE公式/术语及CONSTANT采样设置冲突均保留，没有自行替作者选择一个版本。

## 第六批（2026-10-20）

新增15份存量研究笔记，EDM补正式正文与实验，累计160份；相关章节186、摘要33、元数据1、历史待复核110，主目录330条。核查统一表示与实际共享、图表闭环自改进、视频文字保持/编辑、严格在线分割、静态书法和动作式素描。2023汉字双网协同前作已纳入；TPE公式与官方实现、Consistency Policy符号与官方采样器差异均定位到具体来源，未推断主表必错。来源边界与实验建议见[专题审查](unified_representation_and_causal_review_2026-10-20.md)，全部改动见[文件说明](sixth_changes_2026-10-20.md)。无文件删除，无模型复现。

## 第七批（2026-10-20）

新增14份笔记、Stroke-Seg独立论文L184，累计331条(309论文/22资源)、174份笔记；188条章节核查，33条摘要、0条仅元数据、110条历史待核。论文、加工数据与示例实现分开记；GF0023官方PDF访问限制已解决，读取定义与初始示例。配置/源码/OSF字段和具体证据差异见[专题](resource_implementation_review_2026-10-20.md)、[清单](../../data/seventh_review_batch_2026-10-20.json)、[文件说明](seventh_changes_2026-10-20.md)。此前批次数字保留当时快照。无文件删除，无模型复现。

## 第八批（2026-10-20）

核查L058/L059/L060/L063–L066共7项，累计181份笔记、195条章节核查、33条摘要与103条历史待核。没有增加独立记录。详见[任务接口/协同证据分析](unified_interfaces_and_transfer_2026-10-20.md)、[ID清单](../../data/eighth_review_batch_2026-10-20.json)和[逐文件说明](eighth_changes_2026-10-20.md)。无删除、无模型复现；完整三遍阅读尚未验收。

## 第九批（2026-10-20）

新增7份存量研究笔记，累计188份；章节202、摘要33、历史待核96，主目录331。OFA完成五项书面理解检查，累计3项；完整三遍验收0。正式与预印本表号分开；预训/下游微调、采样重排、剩余任务曝光、条件噪声近似和外部解码成本逐项记录。详见[专题](early_unification_and_distribution_review_2026-10-20.md)、[ID清单](../../data/ninth_review_batch_2026-10-20.json)与[逐文件说明](ninth_changes_2026-10-20.md)。没有删除文件，没有运行模型。

## 第十批（2026-10-20）

新增7份存量研究笔记，累计195份；章节209、摘要33、历史待核89，主目录331。MM-Interleaved框架图与消融表已渲染视觉核对，新增五项书面检查（累计4项）；完整三遍验收仍为0。对照图像采样/重排、CLIP指标对象、分离SFT变体、量化损失、遗忘和负迁移。VILA-U读取固定revision训练/推理脚本与数据注册，保留内部数据、有效batch和帧strip存储条件。详见[专题](compression_conditions_and_synergy_2026-10-20.md)、[ID清单](../../data/tenth_review_batch_2026-10-20.json)及[逐文件说明](tenth_changes_2026-10-20.md)。无文件删除，未运行模型。

## 第十一批（2026-10-20）

新增8份存量模型分析，主目录331条不变；累计203份笔记，章节217、摘要33、历史待核81。Orthus核PMLR正式版本及图表，ILLUME/MetaMorph核ICCV正式书目，MetaMorph正式图已视觉检查；Orthus补第五项五项书面检查，完整三遍仍0。JanusFlow固定曝光消融保留负迁移，Liquid额外数据消融不作固定预算协同证明，ILLUME明确GPT-4o反馈，X-Omni保留不同中文分支及表文冲突。详见[专题](curricula_feedback_and_synergy_2026-10-20.md)、[批次ID](../../data/eleventh_review_batch_2026-10-20.json)、[逐文件说明](eleventh_changes_2026-10-20.md)。未运行模型，无文件删除。

## 第十二批（2026-10-20）

L095–L100六项相关章节核查并新增DDPO/L185（ICLR2024）；目录332条=310论文/研究+22资源，笔记210份，章节224/摘要33/历史75。UniCode²第3–4页Eq1–3/Fig2视觉核对，Selftok PDF第25页Eq20交叉读取；三项官方代码固定revision核查。数学审查保留对实验与实现的独立判断，未把公式缺口称为代码失败。完整三遍验收仍0、独立复现0，未删除文件。见[专题](tokenizer_theory_and_rl_2026-10-20.md)、[批次ID](../../data/twelfth_review_batch_2026-10-20.json)、[逐文件说明](twelfth_changes_2026-10-20.md)。

## 第十三批（2026-10-20）

L101–L108八项章节审查；目录332条、笔记218份、章节232/摘要33/历史67。三项官方代码固定revision、两HF模型卡及HYDRA框架图、RF附录伪码、PixelUMM视频主表视觉核查。UniCom最终FluxVAE.decode依赖已定位；像素接口、量化轨迹与物理书写时间分别记录。HYDRA五项书面检查使累计数达6，完整三遍验收与模型复现仍0；无删除。见[专题](pixel_interfaces_and_temporal_audit_2026-10-20.md)、[ID清单](../../data/thirteenth_review_batch_2026-10-20.json)、[逐文件说明](thirteenth_changes_2026-10-20.md)。

## 第十四批（2026-10-20）

L109–L116方法、实验与指定附录审查，新增8份，累计226份；目录332条，章节240/摘要33/历史59。Muddit与FullFlow指定PDF图表视觉核对，两项目公开代码固定revision；Muddit五项书面检查累计使总数达7。完整三遍精读仍未完成，未执行模型。见[专题](discrete_paths_and_flow_audit_2026-10-20.md)、[ID清单](../../data/fourteenth_review_batch_2026-10-20.json)、[逐文件说明](fourteenth_changes_2026-10-20.md)。

## 第十五批：开放模型、评价器与移动部署

L071与L117–L122共7项存量记录完成指定章节审查，累计233份；332条中章节247、摘要33、历史待复核52。Mobile-O补五项书面检查，累计8项；完整三遍验收仍未完成。详见[专题](open_models_and_deployment_audit_2026-10-20.md)及[逐文件说明](fifteenth_changes_2026-10-20.md)。

## 第十六批：原生像素、视频MoE与梯度投影

L072、L123–L126五项，累计238份笔记；章节252、摘要33、历史待复核47。Rosetta补第9份五项书面检查，完整三遍验收仍未完成。见[专题](native_pixels_video_moe_and_projection_audit_2026-10-20.md)及[逐文件说明](sixteenth_changes_2026-10-20.md)。

## 第十七批：配对偏好、内生奖励与协同主张

L127–L133七项，累计245份笔记；章节259/摘要33/历史待复核40。HermesFlow五项书面检查使累计为10，完整三遍验收仍未完成。新增[专题](paired_preferences_self_supervision_and_claims_2026-10-20.md)和[逐文件说明](seventeenth_changes_2026-10-20.md)。正式版基线更新、理论缺口与代码实际目标分别记录。

## 第十八批：联合RL、梯度整合与共同目标

L134–L138五项，累计250份笔记；章节264/摘要33/历史待复核35。ParetoLoRA新增五项书面检查，累计11。新增[专题](joint_rl_gradient_theory_and_targets_2026-10-20.md)与[逐文件说明](eighteenth_changes_2026-10-20.md)，未运行模型。理论公式问题与经验结果、实际代码分别记述。

## 第十九批：评价构念与跨模态编辑

复核L141–L146六项，累计256份笔记；章节270/摘要33/历史待复核29。确认UniKE/ICML2026、MME-Unify/ICLR2026、Uni-MMMU/ACL2026正式原文，并区分旧arXiv与更新实验。SGU新增五项书面检查，累计12，完整三遍验收仍0。见[专题](benchmark_construct_validity_and_cross_modal_editing_2026-10-20.md)及[逐文件说明](nineteenth_changes_2026-10-20.md)。

## 第二十批：知识、复杂编辑与多语言文字度量

L147–L153七项，累计263份笔记；章节277/摘要33/历史待复核22。均定位正式论文：WISE/GenExam为ICML2026，ImgEdit/MMIG/KRIS/OneIG为NeurIPS2025 D&B，CompBench为CVPR2026。GenExam新增五项书面检查，累计13；完整三遍0。见[专题](knowledge_editing_and_multilingual_text_metrics_2026-10-20.md)和[逐文件说明](twentieth_changes_2026-10-20.md)。

## 第二十一批：长程记忆与生成路径

L154–L160七项，累计270份笔记；章节284/摘要33/历史待核15。ChatUMM为CVPR Workshop、MIO为EMNLP主会、OmniFlow为CVPR主会；其余按已核预印本记录。UniLongGen新增五项书面检查（累计14），完整三遍仍未完成。见[专题](long_horizon_memory_and_multimodal_generation_paths_2026-10-20.md)与[逐文件说明](twenty_first_changes_2026-10-20.md)。

## 第二十二批：交错数据、编辑与教师微调

L057及L169–L174七项，累计277份笔记；章节291/摘要33/历史待核8。InstructPix2Pix新增五项书面检查，主结果是曲线而非主表，已在检查中注明该差异；完整三遍仍未完成。CoMM印刷式与实现尚未解决，保留疑点。见[专题](interleaved_data_editing_and_distillation_audit_2026-10-20.md)与[逐文件说明](twenty_second_changes_2026-10-20.md)。

## 第二十三批：稀疏全模态与动作世界

L161–L168八项，累计285份笔记；章节299/摘要33/历史未重新核查0。清零只指初次相关章节核查，未完成全部全文/三遍，五项书面检查仍15。WorldBagel定理4已有印刷公式反例，不移除实验记录；SenseNova公开训练默认与论文不同。见[专题](omni_action_world_and_theory_audit_2026-10-20.md)及[逐文件说明](twenty_third_changes_2026-10-20.md)。

## 第二十四批：离散扩散、交错及潜在推理

N13/U07–U12/L178八条摘要升级相关章节；累计293笔记，章节307/摘要25，书面五项检查18。正式CVPR/ICLR版本与公开实现补核，纠正成本/百分比/任务接口。无新增独立记录、无文件删除或模型执行。见[专题](interleaved_reasoning_cost_and_latent_policy_audit_2026-10-20.md)及[逐文件说明](twenty_fourth_changes_2026-10-20.md)。

## 第二十五批：字形条件、成对评价与结构监督

L003/S002/S003/U13–U16/U19八条升级相关章节，累计301笔记、章节315/摘要17，五项书面检查20。核论文与配置差异、参数可识别性和生成指标取舍。见[专题](glyph_conditions_paired_benchmarks_and_structural_targets_2026-10-20.md)及[逐文件说明](twenty_fifth_changes_2026-10-20.md)。无独立记录新增、无删除、未运行模型；附录/实现缺项继续保留。

## 第二十六批：生成代理、gate和世界模型

U20–U25六项升级相关章节，累计307笔记、章节321/摘要11。U20/U24五项书面检查新增2项，累计22。生成代理负迁移、推理成本口径、SCO视频规划和信息论假设见[专题](generative_targets_gating_shared_tokens_and_world_models_2026-10-20.md)及[逐文件说明](twenty_sixth_changes_2026-10-20.md)。无新增独立记录、无删除、无模型执行；完整三遍仍待补。

## 第二十七批：原生像素、潜空间代理与机器人书写

U26–U31六项升级章节；新增正式CVPR2026 G-HTR/CHTR-110K（L186），补读存量Springer层级O2O（N08），新增无独立论文的U1.5八步LoRA资源（R08，关联U26）。累计334条/316笔记，章节329/摘要5；四项五条书面检查使累计26，完整三遍仍0。任务接口、公开代码计算路径和表间冲突见[专题](native_pixels_latent_proxies_and_robot_handwriting_2026-10-20.md)及[逐文件说明](twenty_seventh_changes_2026-10-20.md)。没有删除、模型执行或机器人实验。

## 第二十八批：原有九项补齐独立分析

N01/N02/N03/N04/N05/N06/N09/L011/S001重新核正式或固定版本PDF、选定图/表/附录与可取得的指定代码。新增九份本轮结构化分析，累计325份；七项五条书面理解检查新增，累计33。主目录仍334条（311研究/23资源），329章节/5摘要；当前仅9条尚无本轮独立结构化笔记，详见[台账](reading_ledger_2026-10-19.md)。这不代表其余325条完整三遍或代码复核全部结束。见[专题](calligraphy_video_text_order_and_ocr_protocols_2026-10-20.md)与[逐文件说明](twenty_eighth_changes_2026-10-20.md)。没有删除已有文件。

## 第二十九批：当前主目录的独立分析补齐

L026/L028/L044/L175/L176/L177/L179/S004/H001九项新增本轮独立17字段分析，累计334份，当前目录每条均有对应笔记；其中五条受全文访问限制，仅第一遍。七篇新增五项书面理解检查，累计40。完整三遍尚未完成，代码/全部附录/追引仍需继续，不能据模板齐全宣称调研完成或零遗漏。新增Calligraphy Bench全部88行的精简元数据审计；统一视频、静态文字、草图动画、画布编辑和机器人资源按真实输入输出区分。见[专题](unified_video_static_text_sketch_and_resource_mismatches_2026-10-20.md)与[逐文件说明](twenty_ninth_changes_2026-10-20.md)。无删除，无模型运行。


第三十批补四篇视觉蒸馏/矢量动画/艺术字论文和一个模拟书写资源（尚未找到对应独立论文）。当前339条/339笔记，334项原文章节或资源协议、5项摘要；44项五条书面检查，其中4篇完成核心三遍阅读。计时口试、全部代码与独立复现单列，不额外作为核心阅读门槛；此前40项仍逐篇待核定。见[专题](visual_distillation_svg_animation_and_causal_robot_rgb_2026-10-20.md)及[逐文件说明](thirtieth_changes_2026-10-20.md)。无删除，无模型执行。


第三十一批完成A01/A02/A03/A04/A05/A07/A08七项核心三遍与五条书面检查；另将此前40项已有证据逐项按统一口径确认，属于状态校正。当前339目录/339笔记、334章节或协议/5摘要、51核心三遍；未模型复现。见[中文墨迹生成与恢复专题](chinese_ink_generation_and_recovery_core_reading_2026-10-20.md)及[逐文件说明](thirty_first_changes_2026-10-20.md)。无删除。


第三十二批完成A09/A10/A11/B01/B02/B03/B09七项核心三遍与五条书面检查。当前339目录/339笔记、334章节或协议/5摘要、58核心三遍，未模型复现。见[手写风格/书法/数学审查](handwriting_style_diffusion_and_math_core_reading_2026-10-20.md)及[逐文件说明](thirty_second_changes_2026-10-20.md)。无删除。


第三十三批完成B04–B08五项核心三遍、五条书面检查及公开实现交叉核。当前339目录/339笔记、334章节或协议/5摘要、63核心三遍；未模型执行。见[动态文字与绘画过程审查](dynamic_text_and_painting_process_core_reading_2026-10-20.md)和[逐文件说明](thirty_third_changes_2026-10-20.md)。无删除。


第三十四批完成C01/C02/C06核心三遍及各五条书面检查，核Show-o2 NeurIPS2025/ReCA ICLR2026身份和最新已读版本、固定公开代码。339目录/339笔记、334章节或协议/5摘要、66核心三遍；未模型运行。见[统一主干与重建审查](unified_backbones_and_reconstruction_core_reading_2026-10-20.md)和[逐文件说明](thirty_fourth_changes_2026-10-20.md)。无删除。


第三十五批完成C03/C04/C05/C07核心三遍及各五条书面检查，核NFE/延迟/managedKV分母、参考与物理后端差异、整轨迹协同及协议缺项。339目录/339笔记、334章节或协议/5摘要、70核心三遍；未独立模型运行。见[加速缓存与反思审查](acceleration_cache_and_reflection_core_reading_2026-10-20.md)和[逐文件说明](thirty_fifth_changes_2026-10-20.md)。无删除。


第三十六批完成D01–D04核心三遍及各五条书面检查，核视频/声画/条件编辑/轨迹控制、原文与固定实现差异、负结果及训练适配配置。339目录/339笔记、334章节或协议/5摘要、74核心三遍；未独立模型运行。见[视频骨干与运动控制审查](video_backbones_and_motion_core_reading_2026-10-20.md)和[逐文件说明](thirty_sixth_changes_2026-10-20.md)。无删除。


第三十七批扩展D05–D08核心三遍和五项书面检查：核自生成历史、cache梯度、少步组合、任务RL；记录Wan-R1表文冲突、Salt负项及固定代码/HF配置。339目录/339笔记、334章节或协议/5摘要、78核心三遍；无独立模型运行。见[自回归训练与视频RL审查](autoregressive_training_and_video_rl_core_reading_2026-10-20.md)和[逐文件说明](thirty_seventh_changes_2026-10-20.md)。无删除。


第三十八批完成E01–E03核心三遍并新增D09 SGF+同层审查：核平均场/JVP、CFG条件与训练预算、一致性动作计时、视频角色局部梯度理论及负项。主目录340项/340笔记、335章节或协议/5摘要，核心三遍82项；全部三遍仍未完成，无独立模型运行。见[平均场、一致性与角色解耦审查](meanflow_consistency_and_role_split_core_reading_2026-10-20.md)和[逐文件说明](thirty_eighth_changes_2026-10-20.md)。无删除。


第三十九批完成E04–E07核心三遍与各五项书面检查：核离散FM概率/任务指标与采样精度、F5语音对齐/solver与CFG开销、TeaCache残差/校准和多卡分母、clDice条件定理/空间指标边界。主目录340项，核心三遍86项；其余三遍继续保留未完成状态。见[离散流、语音、缓存与拓扑审查](discrete_flow_speech_cache_topology_core_reading_2026-10-20.md)和[逐文件说明](thirty_ninth_changes_2026-10-20.md)。无模型运行/文件删除。


第四十批完成F01–F04核心三遍与各五项书面检查：可微矢量渲染、Gaussian曲线表示、真实笔触规划与共绘模型适配，核作者勘误/版本/预算/模拟代理。主目录340项，核心三遍90项；其余仍待逐项完成。见[矢量与机器人绘画审查](differentiable_vectors_robot_painting_core_reading_2026-10-20.md)和[逐文件说明](fortieth_changes_2026-10-20.md)。F02实际读v4HTML，正式PDF不完整未计；F03/F04预印本版本明确，无模型运行/文件删除。


第四十一批补完sketch-rnn与Learning to Paint核心三遍（累计92项），深化英文连笔作者报告及CoFRIDA-Sharpie制品协议（四项五检查，累计94项）。HF权重rank256/cross768与卡片SDXL及当前rank32脚本不对齐，未运行；F05 IEEE正文仍缺。主目录340项，剩余任务继续逐项处理。见[素描/RL/LoRA审查](sketch_sequences_painting_rl_and_lora_artifact_2026-10-20.md)与[逐文件说明](forty_first_changes_2026-10-20.md)。无文件删除。


第四十二批补完Paint Transformer/CLIPasso并追引补录Stylized Neural Painting/SPIRAL，新增四项核心三遍（累计96）和书面五检查（累计98）。主目录342项；当前Paint Transformer采色版、CLIPasso评价/参与者差异、SPIRAL奖励与符号边界均单独记录。见[神经绘画审查](neural_painting_sets_semantics_and_programs_2026-10-20.md)及[逐文件说明](forty_second_changes_2026-10-20.md)。无训练/推理或文件删除，扩散/Flow Matching/视频基础及剩余候选继续处理。


第四十三批深化DDPM/Score-SDE/Flow Matching/Rectified Flow，新增四项核心三遍（累计100）与五条书面检查（累计102），342项目录不增删。记录质量—似然取舍、等NFE/检查点差异、条件OT边界和RF高步负结果。见[扩散与流审查](diffusion_score_flow_and_rectification_2026-10-20.md)及[逐文件说明](forty_third_changes_2026-10-20.md)。未训练/推理；LDM/DiT/consistency/求解器和视频等剩余复核继续。


第四十四批深化LDM／DiT／Consistency Models／DPM-Solver并补HF VAE资源组R10；343项（318研究／25资源），核心三遍104、书面五检查106。核查decoder／CFG、CT例子初始化与超参、原DPM与++默认差异及负指标；见[本批审查](latent_transformer_consistency_and_solver_audit_2026-10-20.md)和[逐文件说明](forty_fourth_changes_2026-10-20.md)。全部剩余三遍与视频等领域继续，未训练或推理。


第四十五批深化VDM／VideoLDM／AnimateDiff；343项，核心三遍107、五条书面检查109。分清C3D-FID／I3D-FVD、条件抽样协议、时序／静态质量取舍与论文／示例／后继版本；见[本批审查](video_diffusion_temporal_transfer_and_motion_adapters_2026-10-20.md)及[逐文件说明](forty_fifth_changes_2026-10-20.md)。AnimateDiff原补充训练／评价协议仍待补，全部剩余三遍继续，未训练、推理或复现。


第四十六批深化CogVideoX并补R11微调／检查点配置资源组；344项（318研究／26资源），核心三遍108、五条书面检查110。核文字主导视频过滤、时空token／元素压缩、负指标、人评聚合与公开版本／默认值差异；见[本批审查](cogvideox_video_compression_data_and_finetuning_2026-10-20.md)及[逐文件说明](forty_sixth_changes_2026-10-20.md)。全部剩余深审继续，未训练／推理／复现。


第四十七批深化Wan2.1：344项目录，核心三遍109、五条书面检查111。核专门中英视觉文字数据、流式VAE/采样缓存/蒸馏分支差异、负指标与gap/步数/帧率矛盾，并固定代码默认及负提示。见[本批审查](wan_visual_text_flow_training_and_evaluation_audit_2026-10-20.md)、[逐文件说明](forty_seventh_changes_2026-10-20.md)。全部剩余审查继续；无模型训练、推理或独立复现。


第四十八批深化LoRA/QLoRA/DoRA/rsLoRA：344项目录，113核心三遍、115五条书面检查。区分低秩表示、量化存储、模长/方向和rank缩放，保留主表负项、配方冲突与语言证据迁移边界。见[本批审查](parameter_efficient_adaptation_rank_quantization_and_weight_decomposition_2026-10-20.md)与[逐文件说明](forty_eighth_changes_2026-10-20.md)。全部剩余工作继续；无训练、推理或独立复现。


第四十九批深化ControlNet/CFG：344项目录，115核心三遍、117五条书面检查。修正CFG分辨率训练步数，保留FID文字/表图冲突与等速度负结果；核ControlNet初始零残差、代码/hint/RW差异和二维到时序边界。见[本批审查](spatial_control_classifier_free_guidance_and_protocol_gaps_2026-10-20.md)与[逐文件说明](forty_ninth_changes_2026-10-20.md)。无训练、推理或独立复现；剩余深读继续。


第五十批深化GAN/VAE原始理论与实验：344项目录，117核心三遍、119五条书面检查。区分理想分布均衡/有限网络、ELBO/似然/Parzen与重建/生成，保留TFD和小数据test反例。见[本批审查](gan_vae_theory_estimation_and_video_representation_boundaries_2026-10-20.md)与[逐文件说明](fiftieth_changes_2026-10-20.md)。无训练、推理或独立复现；剩余工作继续。


第五十一批深化VBench/FVD核心、既有验证与固定官方评价代码：344项目录，119核心三遍、121五条书面检查。保留VBench版本/相关系数名称差异、FVD样本偏差及非全胜结果；++/2.0和ContentBias继续追读。见[本批审查](video_evaluation_vbench_fvd_protocol_and_scope_2026-10-20.md)与[逐文件说明](fifty_first_changes_2026-10-20.md)。无训练、推理或独立复现；剩余工作继续。


第五十二批新增并精读Content Bias G033：345项目录（319研究／26资源），核心三遍120、五条书面检查122。核同空间质量扰动、冻结重采样、长视频反例与固定实现，纠正T3把分差标百分比的错误；见[本批审查](content_bias_fvd_temporal_sensitivity_and_resampling_2026-10-20.md)和[逐文件说明](fifty_second_changes_2026-10-20.md)。未删除文件、训练、推理或独立复现，全部剩余工作继续。


第五十三批新增并精读VBench++ G034：346项（320研究／26资源），核心三遍121、书面检查123。核I2V裁图/专家、可信人评与固定评分实现，记录2026正式卷期、肤色归一化/安全阈值/背景特征差异及有效样本分母。见[本批审查](vbench_plus_i2v_trustworthiness_protocol_and_implementation_2026-10-20.md)、[逐文件说明](fifty_third_changes_2026-10-20.md)。无删除、训练、推理或复现；全部剩余工作继续。


第五十四批新增VBench-2.0 G035并完成核心精读：347项（321研究／26资源），核心三遍122、书面检查124。核18维事件/物理评价、人体异常训练资源和指定固定代码；记录条件分母、预筛失败计分、无人检测满分及MotionOrder相关名称疑问。见[本批审查](vbench2_intrinsic_faithfulness_events_and_conditional_scores_2026-10-20.md)、[逐文件说明](fifty_fourth_changes_2026-10-20.md)。无删除或模型复现；原有剩余研究继续。


第五十五批补完原记录Chameleon/U01、Transfusion/U05核心三遍：目录347项不变，核心124、书面126。修订训练token口径、Chameleon总体/子集胜率、稳定性曲线表述和Transfusion共享代价/FLOP估计、patch暴露混杂。见[原文审查](chameleon_transfusion_shared_model_cost_and_claim_audit_2026-10-20.md)、[逐文件说明](fifty_fifth_changes_2026-10-20.md)。无删除/模型复现；Janus/Show-o及其他剩余继续。


第五十六批补完原Janus/U03、Show-o/U06核心精读：347目录不变、126核心/128书面。修订解耦/共享收益、版本/指标、CFG与采样成本；纳入Show-o视频扩展，并限定附录公式问题的适用范围。见[原文审查](janus_showo_representation_video_and_math_audit_2026-10-20.md)、[逐文件说明](fifty_sixth_changes_2026-10-20.md)。无删除/训练复现，剩余精读继续。


第五十七批补完InkSight/X01、VideoSketcher/L010核心精读：347目录不变，128核心/130书面。补齐配方、主表/消融、并笔率/统计口径、TF版本与HF制品访问，纠正合理轨迹/规范笔序及偏好/准确率混用。见[原文审查](inksight_videosketcher_trajectory_events_and_resource_audit_2026-10-20.md)、[逐文件说明](fifty_seventh_changes_2026-10-20.md)。无删除/模型复现；SketchAgent及剩余继续。


第五十八批补完SketchAgent/L012与ProcessPainter/L013核心：347目录不变，130核心/132书面。记录正式新增字母串/网格实验、协作边界、关键帧与末帧重建评价，以及公开代码与论文的配置差异。见[原文审查](sketchagent_processpainter_protocol_and_claim_audit_2026-10-20.md)、[逐文件说明](fifty_eighth_changes_2026-10-20.md)。无删除/训练或独立复现；剩余继续。


第五十九批补完PaintsAlter/L014、StrokeNUWA/L016核心：347目录保持，132核心/134书面。补齐非连续查询、数字编辑/规范事件差别、矢量压缩质量取舍、指标方向冲突及公开示例配置。见[原文审查](paintsalter_strokenuwa_query_representation_and_metrics_audit_2026-10-20.md)、[逐文件说明](fifty_ninth_changes_2026-10-20.md)。无删除或独立复现；DiffSketcher新版与剩余继续。


第六十批补完DiffSketcher/L017、Diff-Font/L018明示版本核心：347目录保持，134核心/136书面，213项未确认核心三遍（含资源）。明确优化过程与真实书写、笔画计数与顺序、版本及guidance指标取舍，核对公开warmup/batch/embedding差异。见[原文审查](diffsketcher_difffont_condition_process_and_configuration_audit_2026-10-20.md)、[逐文件说明](sixtieth_changes_2026-10-20.md)。无删除或独立复现；剩余继续。


第六十一批（2026-10-21）补完FontDiffuser/L019、DiffBrush/L023核心：347目录、136核心/138书面，211项尚未确认核心三遍（含资源）。区分未见内容/字体/作者、静态行与真实事件、下游OCR指标，补齐模块tradeoff及公开推理/文章配方差异。见[原文审查](fontdiffuser_diffbrush_generalization_metrics_and_release_audit_2026-10-21.md)、[逐文件说明](sixty_first_changes_2026-10-21.md)。无删除或独立复现；剩余继续。


第六十二批（2026-10-21）补完Emu3/U02、Janus-Pro/U04核心：347目录、138核心/140书面，209项尚未确认核心三遍（含资源）。Emu3 Nature正式扩展与2024v1分列，补重写/后处理、tokenizer/配方消融和CALVIN模拟边界；Janus-Pro缺少逐因素消融，明确记录归因限制。见[原文审查](emu3_januspro_versions_training_and_causal_audit_2026-10-21.md)、[逐文件说明](sixty_second_changes_2026-10-21.md)。无删除或独立复现；剩余继续。


第六十三批（2026-10-21）补完AnyText/L025、UniVid/L027核心：347目录、140核心/142书面，207项尚未确认核心三遍（含资源）。AnyText v1/v1.1多因素更新、区域OCR指标与社区底模分列；UniVid论文/代码差异、VBench命名和ActivityNetQA规模问题明确保留。见[原文/实现审查](anytext_univid_protocol_code_and_namesake_audit_2026-10-21.md)、[逐文件说明](sixty_third_changes_2026-10-21.md)。无删除/独立复现；同名新线索与剩余记录继续。


第六十四批（2026-10-21）补完N10视频文字保持、N11 CalliffusionV2、N12 CalliPaint核心：347目录、143核心/145书面，204项尚未确认核心三遍（含资源）。明确无量化/消融、额外参考信息和四选人评证据限制；确认CalliPaint为NeurIPS2023 Workshop。见[审查](calligraphy_inpainting_and_video_text_evidence_audit_2026-10-21.md)、[逐文件说明](sixty_fourth_changes_2026-10-21.md)。无删除/独立复现；RePaint原始方法与剩余条目继续。


第六十五批（2026-10-21）补录G036原RePaint与G037线性理论：349目录、145核心/147书面，204项尚未确认核心三遍（含资源）。核同预算消融/固定实现差异及有效mask条件，记录Th8的局部总体矩反例，未模型复现。见[审计](repaint_sampling_and_linear_theory_audit_2026-10-21.md)、[逐文件说明](sixty_fifth_changes_2026-10-21.md)。无删除，旧条目/跨领域覆盖继续。


第六十六批（2026-10-21）补完N06 Veo零样本、N07真实多层手写数据库、N13 Unwritten核心/书面检查；349目录、148核心/150书面，201项尚未确认核心三遍（含资源）。核oracle/无效评价、正式回归T3–7、融合与拼接证据及门控卡边界。见[审查](video_reasoning_and_handwriting_observability_audit_2026-10-21.md)、[逐文件说明](sixty_sixth_changes_2026-10-21.md)。无新增独立论文、无删除/复现。


第六十七批（2026-10-21）补完U08 Zebra-CoT v2核心/书面检查与固定版本模型卡/数据卡/代码审查；349目录、149核心/151书面，200项尚未确认核心三遍（含资源）。补入BAGEL负面结果、主附表/采样数差异、GT前缀信息与代码配置边界；正式终稿访问受限单列。见[审查](zebra_cot_negative_results_and_artifact_audit_2026-10-21.md)、[逐文件说明](sixty_seventh_changes_2026-10-21.md)。无重复论文新增、无删除/模型复现。


第六十八批（2026-10-21）补完G030 Diffusion Forcing正式核心/书面检查；349目录、150核心/152书面，199项尚未确认核心三遍（含资源）。核实正式理论p20 KL符号问题、主表反例/任务指标及paper/main代码版本差异。见[审查](diffusion_forcing_theory_protocol_and_versions_2026-10-21.md)、[逐文件说明](sixty_eighth_changes_2026-10-21.md)。无新增独立论文/删除/模型复现。


第六十九批（2026-10-21）补入G038 History-Guided Video Diffusion正式核心/五条书面检查；350目录、151核心/153书面，199项尚未确认核心三遍（含资源）。审查HG-v/f/t、ELBO及路径一致性条件、主表反例/尺度/EMA/机器人与人工长导航，关联固定代码与HF制品。见[审查](history_guided_video_diffusion_audit_2026-10-21.md)、[逐文件说明](sixty_ninth_changes_2026-10-21.md)。新增1项论文，无删除或模型复现。


第七十批（2026-10-21）补完L086 JanusFlow（CVPR2025）/L092 Harmon（ICCV2025）正式核心与书面检查，350目录、153核心/155书面，197项尚未确认核心三遍（含资源）。补正式表号/反例、实际框架与协同图、VAE/采样成本及HF后续decoder微调制品，见[审查](janusflow_harmon_shared_representation_audit_2026-10-21.md)、[逐文件说明](seventieth_changes_2026-10-21.md)。无新增独立论文/删除/模型复现。


第七十一批（2026-10-21）补完G027 EDM正式核心，350目录、154核心/156书面，196条未确认核心三遍（含资源）。修订NFE/FID摘要、最低三次/检查点选择统计、数值/训练因果与书写增广条件，见[审查](edm_numerics_training_and_selection_audit_2026-10-21.md)、[逐文件说明](seventy_first_changes_2026-10-21.md)。无删除或模型复现。


第七十二批（2026-10-21）补完L185 DDPO正式核心，350目录、155核心/157书面，195条未确认核心三遍（含资源）。补实际奖励/消融图、策略代理/按维密度缩放、奖励漏洞与GPU/LoRA/HF制品，见[审查](ddpo_policy_surrogate_rewards_and_artifacts_2026-10-21.md)、[逐文件说明](seventy_second_changes_2026-10-21.md)。无删除或模型复现。


第七十三批（2026-10-21）补完L001有序轨迹恢复/L004布局笔迹核心，350目录、157核心/159书面，193条未确认核心三遍（含资源）。核严格OrderAcc边界/方向与密度、原始消融冲突及源包缺supp，见[审查](ordered_recovery_and_layout_strokes_audit_2026-10-21.md)、[逐文件说明](seventy_third_changes_2026-10-21.md)。无删除或模型复现。


第七十四批（2026-10-21）补完Painter L180/StrokeFusion G024正式核心、实际表图及固定代码/HF；350目录、159核心/161书面，191条未确认核心三遍（含资源）。核反馈缺失消融、集合等变/笔顺边界、主表反例与PR实现差异，见[审查](painter_and_strokefusion_feedback_geometry_audit_2026-10-21.md)、[逐文件说明](seventy_fourth_changes_2026-10-21.md)。无删除或模型复现。


第七十五批（2026-10-21）补完StrokeBank L005正式IAAI核心和Loomis Painter L015最新v3/附录/指定制品；350目录、161核心/163书面，189条未确认核心三遍（含资源）。校正会场/题名、旧版指标/划分与最新反例/人评/制品可用性，见[审查](strokebank_and_loomis_painter_version_audit_2026-10-21.md)、[逐文件说明](seventy_fifth_changes_2026-10-21.md)。无删除或模型复现。


第七十六批（2026-10-21）补完MMaDA L063正式NeurIPS核心/指定补充与Think in Strokes L029固定v3核心；350目录、163核心/165书面，187条未确认核心三遍（含资源）。纠正主表/子集/涨幅和版本，补官方关联RL实现及其与原论文差异。见[审查](mmada_and_think_in_strokes_protocol_audit_2026-10-21.md)、[逐文件说明](seventy_sixth_changes_2026-10-21.md)。无删除或模型复现。


第七十七批（2026-10-21）补完L047女书正式核心/固定代码与CSV统计，重审L184 Stroke-Seg正式全文；L184实际图表视觉待核，保留未完成。350目录、164核心/167项五条书面记录（含未通过项），186条未确认核心三遍（含资源）。见[审查](nushu_and_stroke_seg_data_protocol_audit_2026-10-21.md)、[逐文件说明](seventy_seventh_changes_2026-10-21.md)。无删除或模型复现。


第七十八批（2026-10-21）补完L075 Versatile Diffusion与L077 Emu正式核心/指定补充，核对实际框架主表及固定代码/HF。350目录、166核心/169项五条书面（含未通过项），184条未确认核心三遍（含资源）。见[证据审查](versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)、[逐文件说明](seventy_eighth_changes_2026-10-21.md)。无删除或模型复现。


第七十九批（2026-10-21）补完LaVIT L079正式核心/指定附录及实际图表，核固定代码/HF后续LLaMA2-v2模型。350目录、167核心/170项五条书面（含未通过项），183条未确认核心三遍（含资源）。见[审查](lavit_dynamic_tokens_and_version_audit_2026-10-21.md)、[逐文件说明](seventy_ninth_changes_2026-10-21.md)。无删除或模型复现。


第八十批（2026-10-21）补完UniFlow L072正式ICLR核心/指定附录、实际图表及固定推理制品。350目录、168核心/171项五条书面（含未通过项），182条尚未确认核心三遍（含资源）。见[审查](uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)、[逐文件说明](eightieth_changes_2026-10-21.md)。无删除或模型复现。


第八十一批（2026-10-21）补完TokenFlow L094正式CVPR核心/官方supp和实际框架主表消融，核固定代码/HF。350目录、169核心/172项五条书面（含未通过项），181条尚未确认核心三遍（含资源）。见[审查](tokenflow_shared_indices_and_claim_audit_2026-10-21.md)、[逐文件说明](eighty_first_changes_2026-10-21.md)。无删除或模型复现。


第八十二批（2026-10-21）补完MetaMorph L090正式核心/supp及固定代码；核对重复200K行、逐任务负迁移、相关性混杂与条件丢弃参数。350目录、170核心/173项五条书面（含未通过项），180条尚未确认核心三遍（含资源）。见[审查](metamorph_synergy_and_data_budget_audit_2026-10-21.md)、[逐文件说明](eighty_second_changes_2026-10-21.md)。无删除或模型复现。


第八十三批（2026-10-21）补完扩散视觉综述G022固定v5研究核心，核三框架/分类表、变分界与Ramesh/Avrahami归属。350目录、171核心/174项五条书面（含未通过项），179条尚未确认核心三遍（含资源）。见[审查](diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)、[逐文件说明](eighty_third_changes_2026-10-21.md)。无删除或模型复现。


第八十四批（2026-10-21）补完效率综述G023固定v2研究核心；更正逆SDE/NFE/模型组件归属，201项新增发现层候选未计精读。350目录、172核心/175项五条书面（含未通过项），178条尚未确认核心三遍（含资源）。见[审查](diffusion_efficiency_full_pipeline_audit_2026-10-21.md)、[逐文件说明](eighty_fourth_changes_2026-10-21.md)。正式终版待读，无删除或模型复现。


第八十五批（2026-10-21）补完UniDiffuser L076正式研究核心与固定制品审查。350目录、173核心/176项五条书面（含未通过项），177条未确认核心三遍（含资源）。CFG额外调用、文字codec与v1内部续训已明确。见[审查](unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[逐文件说明](eighty_fifth_changes_2026-10-21.md)。无删除或模型复现。


第八十六批（2026-10-21）补完Tora L034正式版和Tora2 L035固定v2研究核心/制品边界。350目录、175核心/178项五条书面（含未通过项），175条未确认核心三遍（含资源）。见[审查](tora_motion_binding_and_process_boundary_audit_2026-10-21.md)与[逐文件说明](eighty_sixth_changes_2026-10-21.md)。Tora3和Wan玩偶LoRA只进入追查，无删除/模型复现。


第八十七批（2026-10-21）新增Tora3 G039固定v3核心精读和Wan玩偶LoRA R12非论文资源协议审查。352目录、176核心/179项五条书面（含未通过项），176条未确认核心三遍（含资源）。见[审查](tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)与[逐文件说明](eighty_seventh_changes_2026-10-21.md)。资源审查不计论文完成；无删除/模型复现。


第八十八批（2026-10-21）补完MotionCtrl L039明确v2核心/补充与固定发布审查。352目录、177核心/180项五条书面（含未通过项），175条未确认核心三遍（含资源）。见[审查](motionctrl_camera_object_and_observability_audit_2026-10-21.md)与[逐文件说明](eighty_eighth_changes_2026-10-21.md)。保留联合复杂运动低成功率与HF链接/采样配置未决，无删除/模型复现。


第八十九批（2026-10-21）补完Unified-IO 2 L058、AnyGPT L059正式核心/指定补充与固定发布审查。352目录、179核心/182项五条书面（含未通过项），173条未确认核心三遍（含资源）。见[审查](unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)与[逐文件说明](eighty_ninth_changes_2026-10-21.md)。AnyGPT正式音乐词表冲突解除；保留图像择优/真实音频history、缺机制消融及配置口径，无删除/模型复现。


第九十批（2026-10-21）补完SEED-X L060固定v2HTML核心/实际来源图、UniTok L061正式核心/指定附录，补录SEED-Data-Edit G040报告/固定标注样本。353目录、182核心/185书面含未通过项，171条未确认核心。保留CFG反例、缺定量消融/多轮拆单轮与有限样本来源映射未决。见[审查](seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[逐文件说明](ninetieth_changes_2026-10-21.md)。无删除/模型复现。


第九十一批（2026-10-21）补完Word-As-Image L051、Strike a Chord L052固定核心/指定附录与实际框架/主表/消融，核静态优化video输出及论文/发布差异。353目录、184核心/187书面含未通过项，169条未确认核心。见[审查](semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[逐文件说明](ninety_first_changes_2026-10-21.md)。DS-Fusion已定位ICCV2023来源待下一批，不计本批已读。无删除/模型复现。


第九十二批（2026-10-21）完成前批待补DS-Fusion：新增G041正式核心/实际图表/指定supp和固定代码/HF Express制品。354目录、185核心/188书面含未通过项，169条未确认核心。见[审查](dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[逐文件说明](ninety_second_changes_2026-10-21.md)。保留SF/MF取舍、胜出与Equal区别及epoch/step/风格图/默认首字符等发布条件，无删除/模型复现。


第九十三批（2026-10-21）补完L062 MetaQueries/L074 Unified-IO固定核心三遍/实际图表与指定发布。354目录、187核心/190书面含未通过项，167条未确认核心。见[审查](metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[逐文件说明](ninety_third_changes_2026-10-21.md)。记录单向迁移、任务干扰、embedding梯度/decay与数据构造差异；无删除/模型复现。


第九十四批（2026-10-21）补完L078初版SEED/L082 SEED-LLaMA指定版本核心三遍、实际框架/表格及发布。354目录、189核心/192书面含未通过项，165条未确认核心。见[审查](seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[逐文件说明](ninety_fourth_changes_2026-10-21.md)。区分77文字/1图像条件、格式成功/语义质量、原始论文/发布配方；无删除/模型复现。


第九十五批（2026-10-21）补完L053 Timage/L054 BoxTuning公开v1核心三遍、实际框架/主表/消融和指定发布。354目录、191核心/194书面含未通过项，163条未确认核心。见[审查](timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[逐文件说明](ninety_fifth_changes_2026-10-21.md)。Timage训练/样本/聚合矛盾和Box正式书目/README效率分别记录，核心阅读完成不表示结论确证；无删除/模型复现。


第九十六批（2026-10-21）追引新增G042 AutoConverter/VMCBench和G043 ObjectMLLM正式核心/指定附录、实际图表与固定发布，补正L053的9450筛查前含义、L054的既有画框/标注实验边界。356目录、193核心/196书面含未通过项，163条未确认核心。见[审查](autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[逐文件说明](ninety_sixth_changes_2026-10-21.md)。无删除/模型复现。


第九十七批（2026-10-21）完成L064 MANZANO/L071 GenEval固定v1核心、实际图表/指定附录与选定代码；校正颜色候选、任务协同范围、表文及GenEval聚合疑点。356目录、195核心/198书面含未通过项、161条未确认核心。见[审查](manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)和[逐文件说明](ninety_seventh_changes_2026-10-21.md)。无删除/模型复现。


第九十八批（2026-10-21）完成L065 Qwen3-Omni/L066 Emu3.5固定v1核心、主表/实际图表、选定GH/HF发布；区分真实生成模态、受控Base与后训练、三种扩散/负迁移、未发布DiDA和自动具身评价。356目录、197核心/200书面含未通过项，159条未确认核心。见[审查](qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[逐文件说明](ninety_eighth_changes_2026-10-21.md)。无删除/模型复现。


第九十九批（2026-10-21）完成L067 XTC-Bench/L068 IMUG-Bench固定v1核心、实际图表及固定代码/文本元数据审查；记录正确性对称与内容一致性、BLIP3o误分PureAR、MCQ连续多选解析缺陷/37条真值、动态history/几何评分差异。356目录、199核心/202书面含未通过项，157条未确认核心。见[审查](xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[逐文件说明](ninety_ninth_changes_2026-10-21.md)。无删除/模型复现。


第一百批（2026-10-21）完成L069 Unison正式ICML2026核心与L070 VGAU-Diag v2核心、实际框架主表/协议对照及固定代码文本审查；澄清GGU直接/带图评分、ME累计检出与终态、rho含义、oracle与停止probe预算。356目录、201核心/204书面含未通过项，155条未确认核心。见[审查](unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[逐文件说明](one_hundredth_changes_2026-10-21.md)。无删除/模型复现。


第一百零一批（2026-10-21）完成L080 NExT-GPT正式核心和L081 DreamLLM固定v2核心、实际图表/消融及GH/HF配置审查，纠正155M参数归属与ID含义，保留表间冲突/发布配方差异。356目录、203核心/206书面含未通过项，153条未确认核心。见[审查](nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[逐文件说明](one_hundred_first_changes_2026-10-21.md)。无删除/模型复现。


第一百零二批（2026-10-21）完成L083 Emu2固定v2与L085 VILA-U固定v3核心、实际指定框架/主表/现有消融及GH/HF发布审查；分开base/Chat/Gen、0*、表征取舍、空间/深度AR和8帧PNG协议。356目录、205核心/208书面含未通过项，151条未确认核心。见[审查](emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[逐文件说明](one_hundred_second_changes_2026-10-21.md)。无删除/模型复现。


第一百零三批（2026-10-21）完成L045 CalliReader/CalliBench与L046 AWCV-100K/VCRec核心、实际图表及固定GH/HF发布审查；区分阅读顺序、空中书写识别与规范笔顺生成，记录无序F1、发布数据行数、参数/解码协议和英文反例。356目录、207核心/210书面含未通过项，149条未确认核心。见[审查](callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[逐文件说明](one_hundred_third_changes_2026-10-21.md)。无删除/模型复现。


第一百零四批（2026-10-21）完成L088 Liquid/L089 ILLUME指定版本核心、实际图表及发布范围；纠正Liquid语言对照缺失的旧说法，区分规模趋势、额外数据收益与协同，明确ILLUME教师及15M成本口径/版本差异。356目录、209核心/212书面含未通过项，147条未确认核心；ILLUME+/X留后续审查。见[审查](liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[逐文件说明](one_hundred_fourth_changes_2026-10-21.md)。无删除/模型复现。


第一百零五批（2026-10-21）完成L091 UGen/L093 X-Omni固定核心、实际框架/主表/已有消融及指定制品；核课程mask与PPL、7/8基准和k∞差异，纠正中文长文本全优说法，明确无序加权召回、En/Zh与扩散CFG。356目录、211核心/214书面含未通过项，145条未确认核心。见[审查](ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[逐文件说明](one_hundred_fifth_changes_2026-10-21.md)。无删除/模型复现。


第一百零六批（2026-10-21）完成L095 QLIP/L096 DualToken固定核心、实际框架/主表/消融与指定代码；核量化前后理解、固定loss比例、双码head与完整成本、受控双encoder及脚本/论文差异。356目录、213核心/216书面含未通过项，143条未确认核心。见[审查](qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[逐文件说明](one_hundred_sixth_changes_2026-10-21.md)。无删除/模型复现。


第一百零七批（2026-10-21）完成L036 MotiMotion/L037 Fluid-Gen-Zero固定核心、实际框架/主表/消融，确认正式ICML身份并审查公开指令/HF标注；区分加权偏好、仿真参照与真实物理，记录Flow/Tool类别差异及质量退步。356目录、215核心/218书面含未通过项，141条未确认核心。见[审查](motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[逐文件说明](one_hundred_seventh_changes_2026-10-21.md)。无删除/模型复现。


第一百零八批（2026-10-21）完成L038 RefTok固定核心/实际F2和完整T1–3，补全题名并区分参考side information、名义压缩和新文字生成；L184新图2下载入口仍403，保留未验收。356目录，216核心/219书面含未通过项，140条未确认核心（含资源）。见[审查](reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[逐文件说明](one_hundred_eighth_changes_2026-10-21.md)。无删除/模型复现。


第一百零九批（2026-10-21）完成L040 DragNUWA/L041 DragAnything固定核心和实际图表，确认ECCV身份，审查当前发布、ObjMC和343JSON/4367轨迹；区分原LD/HD与SVD、额外mask、26/12百分点与正式评测输入。356目录，218核心/221书面含未通过项，138条未确认核心（含资源）。见[审查](dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[逐文件说明](one_hundred_ninth_changes_2026-10-21.md)。无删除/模型复现。


第一百一十批（2026-10-21）完成L042 TextVBench核心/实际F2/T1/T2/F5：持续文字双轨评价，extra未进H、归一移除标点空白、活跃路由/批划分/采样和诊断混杂；渐进书写需时变GT。356目录，219核心/222书面含未通过项，137条未确认核心（含资源）。见[审查](textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[逐文件说明](one_hundred_tenth_changes_2026-10-21.md)。无删除/模型复现。


第一百一十一批（2026-10-22）完成L043 ViTeX固定v2核心/AppA–O/实际F3-T2-T7，区分glyph加载纠正、CI跨0/时间取舍与旧人评；审查固定GH/HF/230+157清单和2041逐片已报数字，记录margin/PSNR/OCR串发布差异。356目录，220核心/223书面含未通过项，136条未确认核心（含资源）。见[审查](vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_eleventh_changes_2026-10-22.md)。无删除/模型复现。


第一百一十二批（2026-10-22）完成L097 UniToken正式workshop核心/实际p3–6，并核arXiv更新表、固定GH/HF和改写prompt。纠正两阶段/三阶段、负迁移与指标退步，保留当前配置/评测协议缺口。356目录，221核心/224书面含未通过项，135条未确认核心（含资源）。见[审查](unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twelfth_changes_2026-10-22.md)。无删除/模型复现。


第一百一十三批（2026-10-22）完成L098 Selftok固定v3核心/AppA/B与六页实际图表公式，补编辑总数据及负例，给出空间码前缀MDP反例、保留Eq20实现待核；核GH/HF发布和EMA/码序，前身DDT正式文献入全文队列。356目录，222核心/225书面含未通过项，134条未确认核心（含资源）。见[审查](selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirteenth_changes_2026-10-22.md)。无删除/模型复现。


第一百一十四批（2026-10-22）补录G044 DDT-LLaMA正式CVPR2025核心/完整supp研究说明及实际图表，关联L098前身/扩展而不作独立重复创新；分别记录480码/GenEval.66、文本perplexity与人评案例、发布跳转范围。357目录，223核心/226书面含未通过项，134条未确认核心（含资源）。见[审查](ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_fourteenth_changes_2026-10-22.md)。无删除/模型复现。


第一百一十五批（2026-10-22）完成L099 UniCode²固定v2核心、T1–6/AppA研究文字与七页实际图表公式，纠正T4参数单位位置，补全部主表/消融和量化反例；未定位对应版本公开代码/权重。357目录，224核心/227书面含未通过项，133条未确认核心（含资源）。见[审查](unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_fifteenth_changes_2026-10-22.md)。没有文件删除或模型复现。


第一百一十六批（2026-10-22）完成L100 TUNA正式CVPR正文、官方附录、固定v1和公开原版实现选读；记录联合训练MME下降、正文/附录学习率冲突、公开配方/发布边界及clean/noisy条件分支待测试。357目录，225核心/228书面含未通过项，132条未确认核心（含资源）。见[审查](tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_sixteenth_changes_2026-10-22.md)。没有文件删除或模型复现。


第一百一十七批（2026-10-22）完成L101 UniWeTok固定v3核心/Eq1–9/33表和七页实际图表，核查BitDance共用代码与HF相关tokenizer制品；区分64位置/128bit、33B位置token/全成本及三个独立SFT变体。357目录，226核心/229书面含未通过项，131条未确认核心（含资源）。见[审查](uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_seventeenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百一十八批（2026-10-22）完成L102 EvoTok固定v1核心/Eq1–11/五表和六页实际图表，核GH独立码本/EMA与训练入口及ECCV官方接收列表；保留表示深度、三项并列与主表/公开配方差异。357目录，227核心/230书面含未通过项，130条未确认核心（含资源）。见[审查](evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_eighteenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百一十九批（2026-10-22）完成L104 UniCom固定v1核心/全部七表和七页实际图表，补原始特征旁路、OCR下降、VAEdecoder与WorldEdit文字/表格冲突；核GH/HF配置和理解入口shape待核项。357目录，228核心/231书面含未通过项，129条未确认核心（含资源）。见[审查](unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[逐文件说明](one_hundred_nineteenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十批（2026-10-22）完成L105 Tuna-2固定v2核心/全部六表及八页实际图表，补任务退步、重建额外微调、偏好90.1%和mask/噪声公开默认差异。357目录，229核心/232书面含未通过项，128条未确认核心（含资源）。见[审查](tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_twentieth_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十一批（2026-10-22）完成L106 Representation Forcing固定v4核心/三表含五子消融、AppA–C与六页实际PDF；核VLM-only反例、量化伪代码及AR完整成本。357目录，230核心/233书面含未通过项，127条未确认核心（含资源）。见[审查](representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_first_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十二批（2026-10-22）完成L107 HYDRA-X固定v1核心/十三表、AppA–G与十页实际PDF，补视频运动反例、时间压缩/编辑/解码接口和训练比例边界；官方核L107及L103的NeurIPS2026身份。357目录，231核心/234书面含未通过项，126条未确认核心（含资源）。见[审查](hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_second_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十三批（2026-10-22）完成L108 PixelUMM固定v1核心/九表八组实验与十页实际PDF，补官方代码/模型卡，记录15.2B总参、F7十一项图像退步、F8条件分层及linearhead发布边界。357目录，232核心/235书面含未通过项，125条未确认核心（含资源）。见[审查](pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_third_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十四批（2026-10-22）完成L109 FUDOKI正式NeurIPS2025核心/五表/AppA–F及八页实际PDF，补固定GH/HF源码与配置，记录3.86M/3.71M、L2/四次方、32/128/50步差异与纠错对照限制。357目录，233核心/236书面，未确认核心97论文／研究+27资源（资源单独审查）。见[审查](fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_fourth_changes_2026-10-22.md)。没有删除文件或执行模型。


第一百二十五批（2026-10-22）完成L111 LaViDa-O正式ICLR2026核心/16表/AppA–F及12页实际PDF，补固定GH/HF制品，记录Eq7区间冲突、16/17层边界、ground数据DPG退步和反思质量-延迟条件。357目录，234核心/237书面；未确认核心96论文／研究+27资源（资源单独审）。见[审查](lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_fifth_changes_2026-10-22.md)。没有删除文件或执行模型。


第一百二十六批（2026-10-22）完成L112 Lumina-DiMOO全核心/十表与十一页实际PDF，补固定GH/HF及cache/SelfGRPO/局部编辑协议，纠正32倍重复相乘、任务全优和保留码等于RGB保持的误述。357目录，235核心/238书面；未确认核心95论文／研究+27资源（资源单独审）。见[审查](lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_sixth_changes_2026-10-22.md)。无删除或执行模型。


第一百二十七批（2026-10-22）完成L113 Omni-Diffusion正式核心、全部八表与八实际PDF页，核对arxivv2及固定GH/HF。明确连续语音输入、两版WER/CLIP/RTF、位置缩放/预填与源码差异。357目录，236核心/239书面；未确认核心94论文／研究+27资源（资源单独审）。见[审查](omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_seventh_changes_2026-10-22.md)。无删除或执行模型。


第一百二十八批（2026-10-22）完成L114 LLaDA2.0-Uni完整核心、十四表/Eq1–8与十三实际PDF页，核固定GH/HF的MoE、decoder与SPRINT。记录文字渲染差距、T4正文/表冲突、缓存剪枝及质量-速度折中。357目录，237核心/240书面；未确认核心93论文／研究+27资源（资源单独审）。见[审查](llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_eighth_changes_2026-10-22.md)。无删除或执行模型。


第一百二十九批（2026-10-22）完成L115 FullFlow完整核心、十表与十五实际PDF页，核双时间RF/插入、输出梯度理论、先验保留评价及网页制品树。保留T4/T9数值、T8反例、T5/T6预算与算术冲突。357目录，238核心/241书面；未确认核心92论文／研究+27资源（资源另审）。见[审查](fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_ninth_changes_2026-10-22.md)。无删除或执行模型。


第一百三十批（2026-10-22）完成L116 Multimodal Flow完整核心/附录研究、十表/Eq1–12及九实际PDF页，核固定GH/HF连续codec、块因果、预算和采样。记录oneobjective范围、等参数与等计算区别、数据/默认配置差异及生成-理解取舍。357目录，239核心/242书面；未确认核心91论文／研究+27资源。见[审查](multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirtieth_changes_2026-10-22.md)。无删除或执行模型。


第一百三十一批（2026-10-22）完成L117 BLIP3-o v1完整核心/两主表/AppA与七实际PDF页，核原GH与HF模型/数据卡。分开公开8B与私有论文8B、原版与NEXT，记录语义flow公式勘误、64query单次前向和缺少joint/AI数据因果对照。357目录，240核心/243书面；未确认核心90论文／研究+27资源。见[审查](blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_first_changes_2026-10-22.md)。无删除或执行模型。


第一百三十二批（2026-10-22）完成L118 OpenUni v3全部核心/六表与五实际PDF页，核固定GH训练/模型/评测和HF模型/数据元数据。记录轻连接器、GenEval模板分布、生成器解冻混杂、L512型号矛盾及公开/许可边界。357目录，241核心/244书面；未确认核心89论文／研究+27资源。见[审查](openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_second_changes_2026-10-22.md)。无删除或执行模型。


第一百三十三批（2026-10-22）完成L119 UniFork v1全部核心/五表与八实际PDF页，核固定GH分支、冻结、RQ头和训练/采样。记录mutual-kNN观察的因果边界、T4聚合矛盾、专家残余差距及参数/分辨率/发布脚本差异。357目录，242核心/245书面；未确认核心88论文／研究+27资源。见[审查](unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_third_changes_2026-10-22.md)。无删除或模型执行。


第一百三十四批（2026-10-22）完成L120 HunyuanImage3.0 v3全部核心/训练表和六实际PDF页，核固定GH及三HF模型配置/采样/权重索引。记录GSB绝对四格与净差、SSAE宏微平均、无受控消融、MoE观察及Base/Instruct/Distil/TMP边界。357目录，243核心/246书面；未确认核心87论文／研究+27资源。见[审查](hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_fourth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十五批（2026-10-22）完成L121 DeepGen1 v2全部核心/附录11表与13实际PDF页，核主仓、独立RL和三类HF制品。记录SCB全上下文、投影/超参差异、RL任务退化、概率代理及公开UniGen训练提示与600测试提示的3条精确交集，未推定最终运行使用。357目录，244核心/247书面；未确认核心86论文／研究+27资源。见[审查](deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_fifth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十六批（2026-10-22）完成L123 InternVL-U v1全部核心/附录、24表、17实际PDF页与固定模型/代码/TextEdit/EvalKit指定实现。记录理解5/7退化、CoT子类权衡及CFG混杂、RISE原表聚合疑问、TextEdit报告与发布指标差异、LongText无序召回边界。357目录，245核心/248书面；未确认核心85论文／研究+27资源。见[审查](internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_sixth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十七批（2026-10-22）完成L124 Mamoda2.5 v1全部核心/附录13表、11实际PDF页与固定八文件推理制品指定源码。补核视频/字幕真实任务、25B/A3B口径、DiT计时95.9倍与实测7.5倍、Reco/理解负例、曲线标注与发布48Top5对报告128Top8差异。357目录，246核心/249书面；未确认核心84论文／研究+27资源。见[审查](mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_seventh_changes_2026-10-22.md)。无删除或模型执行。


第一百三十八批（2026-10-22）完成L125 SenseNova-U1全部核心23表/Eq1–7与固定发布配置/指定源码。明确像素MoT真实任务、17.55B/38.74B索引参数、噪声能量解释、LongText计数召回、理解/OneIG退步、协同对照缺口及U1.5版本边界。357目录，247核心/250书面；未确认核心83论文／研究+27资源。见[审查](sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_eighth_changes_2026-10-22.md)。无删除或模型执行。


第一百三十九批（2026-10-22）完成L128 MindOmni正式NeurIPS2025核心9表/Eq1–7、9实际PDF页及固定代码/模型配置审查。区分原版WISE.60与追加HQ版.71，记录RGPO仅文字policy ratio、特征KL方向/优势归一化/启动任务名差异和CoT不单调。357目录，248核心/251书面；未确认核心82论文／研究+27资源。见[审查](mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_ninth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十批（2026-10-22）完成L129 CoRL核心三遍、正式8表/Eq1–6及固定联合RL/数据卡审查。明确S1双任务提升与S2任务分支/合并边界、7%/23%相对均值、WISE排名、监督数据和公开reward默认/QA类型/概率位置待核差异。357目录，249核心/252书面；未确认核心81论文／研究+27资源。见[审查](corl_joint_advantage_branch_and_reward_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_fortieth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十一批（2026-10-22）完成L130 PairUni完整HTML核心与附录、10表/Eq1–4和7实际原始图，核独立优势/std后权重、平方根与梯度解释、模板和阈值矛盾、主表退步与公开损失差异。更正旧会场断言及Lumina编辑表述。357目录，250核心/253书面；未确认核心80论文／研究+27资源。见[审查](pairuni_pair_weighting_gradient_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_forty_first_changes_2026-10-22.md)。无删除或模型执行。


第一百四十二批（2026-10-22）完成L131 UniCorn正式ACL32页核心、17表/Eq1–9、指定附录及13实际PDF页；交叉核固定自身采样/SFT、HF和UniCycle完整评分代码。承认正式理论修正，记录外部persona、指标退步、裁判/词数接口和分母差异。357目录，251核心/254书面；未确认核心79论文／研究+27资源。见[审查](unicorn_selfplay_joint_objective_and_unicycle_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_forty_second_changes_2026-10-22.md)。无删除或模型执行。


第一百四十三批（2026-10-22）完成L132 R3正式ICLR24页核心/指定附录、9表/Eq1–3及附录公式、12实际PDF页、固定Tree训练与七JSONL协议。发现发布GenEval训练与553测试有370字面提示重合，正式训练版本仍待核；记录理解范围、非单调轮数与代码配置边界。357目录，252核心/255书面；未确认核心78论文／研究+27资源。见[审查](r3_tree_rl_understanding_scope_and_prompt_overlap_audit_2026-10-22.md)、[逐文件说明](one_hundred_forty_third_changes_2026-10-22.md)。无删除或模型执行。


第一百四十四批（2026-10-22）完成L133 GvU正式CVPR11页全文/6表/Eq1–8、7实际PDF页、固定奖励/PEFT上下文/策略loss及评测协议。纠正表号、计数和理解负结果、曲线幅度；记录活动教师与论文clip差异及写实评测边界。357目录，253核心/256书面；未确认核心77论文／研究+27资源。见[审查](gvu_intrinsic_probability_reward_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_forty_fourth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十五批（2026-10-22）完成L134 LVRPO完整17页核心/全部附录、7表/Eq1–16/Algo1、12实际PDF页。记录Eq16归一缺口、MI/梯度/W2论证边界、F3/F5与主表配置差异及公开制品待核。357目录，254核心/257书面；未确认核心76论文／研究+27资源。见[审查](lvrpo_theory_reward_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_forty_fifth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十六批（2026-10-22）完成L135 Uni-Synergy完整23页核心/全部研究附录、6表/Eq1–34、17实际PDF页与固定官方cleaned源码/原HF卡片。保留主表收益，记录截断正态/SNR/控制器证明缺口、正式与公开奖励/loss差异、DGS接口问题及归档内部待核。357目录，255核心/258书面；未确认核心75论文／研究+27资源。见[审查](uni_synergy_dgs_theory_and_personalization_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_forty_sixth_changes_2026-10-22.md)。无删除或模型执行。


第一百四十七批（2026-10-23）完成L181正式11页全部研究正文/8表/Eq1–24/11图、10实际PDF页及固定官方源码。记录汉字部件联合学习的已有贡献、遮挡负迁移、TPE纸面/实现/几何证明差异及公开joint未完成边界。357目录，256核心/259书面；未确认核心74论文／研究+27资源。见[审查](chinese_radical_joint_tpe_geometry_and_negative_transfer_audit_2026-10-23.md)、[逐文件说明](one_hundred_forty_seventh_changes_2026-10-23.md)。无删除或模型执行。


第一百四十八批（2026-10-23）完成L182 STRIVE正式研究正文/2表/4式/10图、8实际PDF页和固定五文件发布审查；区分已有视频编辑、时序proxy与书写过程，核到Eq2符号/OCR口径和多副本速度条件。357目录，257核心/260书面；未确认核心73论文／研究+27资源。见[审查](strive_video_text_replacement_and_propagation_protocol_audit_2026-10-23.md)、[逐文件说明](one_hundred_forty_eighth_changes_2026-10-23.md)。无删除或模型执行。


第一百四十九批（2026-10-23）完成L183 CONSTANT正式10页正文+8页supp全部研究内容/12表/8式/20图、15实际PDF页及固定代码审查。补齐WER迁移协议/写者分类/越文切分，记录IV-U HWD、SCE FID局部退化、K/CFG/配权及公开评测差别。357目录，258核心/261书面；未确认核心72论文／研究+27资源。见[审查](constant_multilingual_style_quantization_and_evaluation_audit_2026-10-23.md)、[逐文件说明](one_hundred_forty_ninth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十批（2026-10-23）完成L137 STBridge v1全部研究正文/10式9表16图、20实际PDF页及有限官方发布检索。明确独立双路径一致评价与训练caption条件链、softgate代数边界及局部能力回退。357目录，259核心/262书面；未确认核心71论文／研究+27资源。见[审查](stbridge_shared_target_alignment_and_causal_controls_audit_2026-10-23.md)、[逐文件说明](one_hundred_fiftieth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十一批（2026-10-23）完成L138 MATE全部正文/附录研究内容、5表5式3算法8图及11实际PDF页。补齐B200预算、零方差/准入fallback、全候选/分网消融及Fig8分项对应边界。357目录，260核心/263书面；未确认核心70论文／研究+27资源。见[审查](mate_adversarial_pool_evolution_and_budget_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_first_changes_2026-10-23.md)。无删除或模型执行。


第一百五十二批（2026-10-23）：完成L139全部研究正文/AppA–E、5表2编号式10图及11实际PDF页；逐项审查CAGrad、代理指标方向、置信区间估计对象与投影混淆。357目录，261核心/264书面；未确认核心69论文／研究+27资源。见[审查](gradient_conflict_metric_validity_and_causal_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_second_changes_2026-10-23.md)。无删除或模型执行。


第一百五十三批（2026-10-23）：完成L140全部研究正文/AppA–F、6表4式10图/10实际PDF页及源码包目录；核Show-o masked生成、调用/损失归因、参数数与选桶索引等差异。357目录，262核心/265书面；未确认核心68论文／研究+27资源。见[审查](position_gradient_attribution_and_lora_budget_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_third_changes_2026-10-23.md)。无删除或模型执行。


第一百五十四批（2026-10-23）：完成L141正式全部研究正文/AppA–F、16式8表6图/10实际PDF页，核固定代码与2971条HF数据；记录缺stage、矛盾请求、推理拼接与条件机制边界。357目录，263核心/266书面；未确认核心67论文／研究+27资源。见[审查](unike_cross_modal_editing_and_artifact_protocol_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_fourth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十五批（2026-10-23）：完成L143全部研究正文/AppA–J及1式7表28图，29实际PDF页；核1234提示/4231题和固定核心代码，得到恒A层级基线.351及自评混淆边界。357目录，264核心/267书面；未确认核心66论文／研究+27资源。见[审查](unieval_self_evaluation_identifiability_and_answer_bias_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_fifth_changes_2026-10-23.md)。无删除或模型执行。
