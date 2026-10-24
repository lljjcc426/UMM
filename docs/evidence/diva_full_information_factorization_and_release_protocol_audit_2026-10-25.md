# DIVA：正式版本、信息分解与公开制品完整审查

第一百九十三批完成[U31](../reviews/U31.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/diva_full_information_factorization_and_release_protocol_audit_2026-10-25.json)。358目录（331论文／研究、27资源），298核心/303书面含未通过项；待完成核心深审33篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2605.25328v1)、[主源2](https://arxiv.org/html/2605.25328v1)、[主源3](https://proceedings.mlr.press/v306/lu26as.html)、[主源4](https://raw.githubusercontent.com/mlresearch/v306/main/assets/lu26as/lu26as.pdf)、[主源5](https://github.com/Jayyy-H/DIVA/tree/8891120fe9f6e42fac7470e7a5f05f6a668abe37)。

## 研究问题

同backbone理解/生成有不同归纳偏置，能否把中层表示分成跨flow共享与任务独有因子，在保留独有信息的同时促进双任务？对象是图像理解/生成/编辑后训练，无video/笔顺/交错输出实测，作者列为未来方向。

## 现有不足

理解倾向语义不变性，重建生成需局部细节；同样本构造caption与masked inpainting有共同语义锚。F2浅深层梯度冲突较大、中层几何分离与频谱差异，是设计动机而非全部失败的因果证明。图中gradient conflicts均为正量，未充分定义究竟是负cos转化率/强度等，不自动当梯度cos。谱分析缺FFT轴/patch排列/频带阈值/样本及误差带定义，不能由feature高频直接等同图像细节或笔顺时序。

## 贡献

DIVA两stage：冻结骨干，用跨flow shared+自身unique的低秩logit偏置和正交约束预热分解encoder；冻结encoder后微调选定骨干层，以双向stopgrad InfoNCE对齐shared、NCE-CLUB式压unique跨flow依赖并保留原任务loss。三base/多任务主表有提升，消融支持模块在所测配置有用；MI估计和相似度可视化不能作为语义因子唯一可识别或信息完整保留的证明。

## 输入、模块、输出与公式

给同一(I,T)，理解flow输入原图+详细caption提示，目标对应caption；生成flow以T和mask比例r∈[.2,.6]的I⊙(1−M)做inpainting。抽中层image tokens HU/HG∈RN×d，Pool为h；三层GELU MLP、sigmoid gate及LN得shared/unique(Eq5/13)。Eq2残差||G−ΠUG||²/||G||²、Eq3合并flow effective rank增量用于诊断，PCA秩/ER定义与估计细节不完整。Eq4把I(X1,X2;Y)写作shared+两unique+noise是建模假设，未证明完整PID/可识别性，synergy不能默认为已被独立量化。Eq6shared对比目标/7unique正负critic差，边界依赖负样本/optimal critic条件。Eq8低秩读出把另一flow shared和自身unique加至logit，Eq9正交，Eq10双向stopgrad、Eq11与原native loss合并，Eq12秩r=24。冻结encoder参数仍应保留对其输入/骨干的梯度；无完整训练入口验证实际stopgrad/EMA/critic更新次序。

## 模型结构

NexusGen7B、ShowO1.5B、Liquid7B为实际后训练对象；同一图文样本双flow，中层池化后四个分解encoder。Stage1四个rank24读出跨所选层共享，shared-only→shared+unique预热；Stage2微调Nexus/Showo层8–18、Liquid9–22，encoder固定。论文叙述unfreeze backbone需结合T8的selected layers，不能误写所有层全训。Stage1 logit偏置按样本广播，原骨干仍提供token/空间信息；单个全局因子本身不提供完整逐patch对齐。无需把两个训练flow当额外独立生成backbone或推理循环。

## 数据分布与划分

200K=60K CapsFusion/InfinityMM筛选图文+70KJourneyDB+70KMidjourneyV6；60K caption refinement及MJ图生caption用Qwen2.5VL32B，保原pair。后训练配对没有全靠模型自生成，self-improved不等无外部数据/teacher。T3提供rawJourneyDB70K、mixed70K/200K来源对照；过滤阈值、数据ID、holdout与decontamination及重写recipe当前未完整发布，不能依据数据规模断言零污染或均衡覆盖。

## 指标与评价协议

T1五种理解MMMU/MME/MMBench/MMVet/POPE，§4.2列MMVP却未见该结果，保留文字/表差异。生成GenEval553prompts、DPG1065、WISE1000/25subdomain按论文描述；T9六GenEval子项，T10六WISE大类。T5 ImgEdit九类/Ovr及GEditEN SC/PQ/O，模型judge版本/prompt/统计CI不足。T1星号称8random seeds reproduced，未说明是生成seed还是8次独立完整训练，无std/CI。F5 tSNE十类×四对只是投影与anchor可分性，未独立证实unique保留或shared纯语义。

## 对比方法

T1单任务LLaVA/Qwen2.5VL/InstructBLIP/SDXL/QwenImage/SD3/Infinity和多种UMM仅上下文；因果重点三base各自+DIVA、Showo同数据SFT、去Iuni/stopgrad、层区间/encoder/mask、数据规模、λuni。T6 RecA1134.8MME/75.7POPE/.63GenEval vsDIVA1206.1/79.1/.64；UAE无同协议结果，空值不当0或落败。未充分给两stage与SFT/RecA总update/双flow算力匹配，不能完全排除额外优化预算。

## 实验条件和发布边界

T7按Nexus/Showo/Liquid：Stage1 steps3K/2K/5K，lr2e−4/2e−4/1.5e−4，acc5/5/8，每GPU6，warmup300/200/500，native权重1、orth .2。T8 Stage2 steps15K/12K/20K，lr5e−5/3e−5/2e−5，acc10/12/18，warmup1000/800/1300，λsha/uni 0→.6；均AdamW/EMA(.99,.999)/wd.01/cosine。8RTX4090(24GB)：Nexus512²/ZeRO3约74h，Showo256²/ZeRO2约46h，Liquid512²/ZeRO2约89h；正文却称Showo8B与T1/9 1.5B冲突，不能擅纠正。完整训练脚本缺失，batch两flow计量/EMA双decay用法/τ/critic优化等未重建。未运行训练/推理/模型judge。

## 主结果

T1 Nexus MMMU43.5→49.4/MME1279.1→1355.3/POPE83.6→87.4/GenEval.77→.83/DPG81.30→87.87/WISE.39→.45；Showo MMMU26.3→32.4/MME1097.7→1206.1/GenEval.57→.64/DPG69.81→76.03/WISE.29→.34；Liquid MMMU30.2→34/MME1321.7→1434.9/GenEval.70→.81/DPG80.63→83.47/WISE.41→.44。10表全行原值另存。T2/4 Showo Base/SFT/DIVA GenEval .69/.67/.75，与T1/3/6/9的base.57/ours.64不一致，正式PMLR PDF仍未改，当前README也两套并列；不合并或挑高。T9 Liquidoverall.82而T1.81，且.82旁增益仍+.11，原样记疑。T10 Liquid Time.47→.45退化，NexusCulture.35持平，ShowoTime.35持平；“各方面均提升”须收窄。

## 消融及进一步实验

T2同数据SFT MMMU26.8/POPE74.5/DPG70.75，DIVA32.4/79.1/76.03；w/oIuni为28.3/75.8/71.58，w/oSG31.7/78.2/74.92，支持实测模块作用，不等严格信息分解证明。8–18总体较好但7–19 MMMU32.5更高、TransformerPOPE79.2高于79.1，默认未全指标最优。contiguous mask MMMU24.7/POPE69.6/DPG68.22低于base，证明mask选择有明显失败风险。T3 rawJourney70K→mixed70K→200K MMMU31.7/31.9/32.4，GenEval.62/.62/.64，来源/规模有贡献。T4 λ.4/.6/.8邻域较稳，但仅三点不能保证更大范围稳定。T5 ImgEdit2.98→3.35、GEdit4.61→4.92；GEdit仍低于Flux6.01/Bagel6.64/GPT7.53，ImgEdit低于Flux3.48，部分细类也低于其他方法，§4.2 across all tasks主张过宽。

## 局限与疑问

独有表示常量化也可令跨flow MI低，正交仅线性去相关，非独立或task sufficiency证明；native监督/Stage1有缓解作用，无理论保证。InfoNCE lower/CLUB upper依critic/样本估计条件，不能把近似优化等同真实MI测量。当前官方repo commit8891120fe9f6e42fac7470e7a5f05f6a668abe37共21树项/17blob，无完整trainer、dataset recipe、eval、模型checkpoint；README明说showcase/计划发布。已读diva_utils190行：GatedMLP为两Linear+SiLU乘门，无论文三层GELU+sigmoid+LN；info_nce_loss是普通双向CE，无内部detach（调用方可外置，未发布）；unique为Gaussian CLUB，非所写NCEoptimal critic；LowRankReadout默认64而paper24，orth默认.1而paper.2，可被调用方覆盖，不能断言历史实验错误。无调度/critic/EMA集成代码确认。

## 预期优势条件

同样本双任务含可迁移语义及足够不同细节、预热学到有用因子、原任务监督避免unique丢信息时，shared对齐+unique去依赖有机会减冲突；适用中小单backbone三base经验。书写可分内容语义与轨迹/风格，但时间合法性可能需要两者协同；强行低MI可能抹去字符约束笔序的必要依赖，需测实际任务信息和过程质量。

## 可证伪实验

Q1分解是否保留有用信息：固定data/teacher/optimizer步数与双flow FLOPs，比SFT、只有shared、只有unique、random frozen encoder、Stage1-only及完整；用独立probe测shared内容/unique细节与task互预测，追unique variance/collapse，比较线性正交与真正非线性依赖。Q2所谓低/高频是否因果：明确token二维网格/FFT频带并加入patch重排、图像低高通/遮罩同ratio对照，重测全维残差/ER及实际重建/理解；MI批量大小/负样本/critic收敛与teacherEMA/SG分别消融，给8独立训练seed CI。确认GenEval两套protocol、checkpoint、sample seed与分母，匹配总训练预算；书写增加同终态异笔序、prefix/动作合法性任务，不用终态语义分数代替时间证据。均未运行。

## 论文组织与Claim学习

F2梯度/几何/谱诊断→双flow假设→两stage→主表/消融/robustness形成清晰主线；信息论符号的语义需给可检验定义与估计条件，谨慎用prove/strictly preserve等词。低分项、dataset teacher成本、mask失败与制品未完成应进边界。正式PDF未修数表冲突，仓库README也重复两套数字，说明投稿/正式/代码表应维护统一配置映射。F6坐标既称能力又标validation loss，明确越低越好及实际loss定义后才解释前沿。

## 实际阅读范围

arXiv2605.25328v1完整18页及正式PMLR18页文本对应检查（主要排版差异，表/方法疑点仍在），正文§1–5、Acknowledgements/Impact、AppA1–2/B1–3/C1–2；10表全行列、F1–7全部视觉、Eq1–13及未编号读出式。F4六成对选例/F7十六图与全部prompt核对；追引CLUB/FactorizedContrastiveLearning/BYOL、RecA/UAE/Showo/Nexus/Liquid与各benchmark。固定repo完整21项树、下载6文件，全文读README/diva_utils/配置，phi/modeling_utils仅定点搜索，未声称完整代码读通或全模型复现。核心三遍和五项书面记录完成。

## 图示与结果范围

F4六组成对生成选例显示数量、关系或布局改善；未给随机选例分母/匹配seed，不能据其估计成功率。F7十六个生成图中第15prompt要求白色牌上黑字DIVA，输出为偏棕牌且增加Welcome和图形；第14要求snowboards，图中板具细节也需独立评判。选例本身仍有未严格满足约束的情况，不支持所有prompt精确完成。

F5十类各四对的tSNE表示配对邻近，但投影/样本语义本身不能验证unique信息完备。F6图例ours为圆点、baseline三角，两个轴写validation loss；按loss越低越好解释前沿移动，实际VQA loss/分母/误差条待补。

正式PMLR页已提供可核会议卷页，本批更新此前venue未确认记录。未把正式收录当所有方法或数字无误的依据；全部原数保留，未运行任何模型。
