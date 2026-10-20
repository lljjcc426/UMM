# 第二轮原文复核与扩展调研：实际完成范围

本轮始于2026-10-19，更新截至2026-10-20。在main原HEAD `06210329c5667a0b0aed7a6e836417feff5a9d7f`基础上工作。研究范围覆盖统一多模态、静态/动态文字、在线轨迹、素描/绘画过程、视频基础模型、扩散/流理论、适配及评价。原档案和笔记保留，没有删除已有仓库文件。

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
