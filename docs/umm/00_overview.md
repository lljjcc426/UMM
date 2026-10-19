# UMM 总览与研究地图

[返回仓库首页](../../README.md) · [UMM文献表](literature.md)

## 1. 这里研究的UMM是什么

视觉语境中的统一多模态模型把视觉理解与视觉生成放入同一可训练框架。实际统一可以发生在tokenizer、参数、注意力上下文、训练目标或推理过程，不能要求所有组件完全相同。

[Janus](https://arxiv.org/abs/2410.13848)分开理解与生成的视觉编码；[Transfusion](https://arxiv.org/abs/2408.11039)结合文字自回归和图像扩散；[BAGEL](https://arxiv.org/abs/2505.14683)使用专门计算路径和共同上下文；[Show-o2](https://arxiv.org/abs/2506.15564)将视觉生成扩展到时空建模。它们的能力集合不同。

本库采用三个分析层次（不是官方分类）：

| 层次 | 要求 | 不能替代的检验 |
|---|---|---|
| 功能统一 | 同一模型会看图、会画图 | 两种能力分别可用 |
| 学习协同 | 训练一侧可改善另一侧 | 控制数据/计算后的迁移 |
| 推理协同 | 一个任务中观察、生成、检查相互促进 | 正确视觉证据确实改变后续推理 |

[GapEval](https://arxiv.org/abs/2602.02140)、[RealUnify](https://arxiv.org/abs/2509.24897)和[UniG2U](https://arxiv.org/abs/2603.03241)分别从知识、联合任务与生成辅助理解角度说明：第一层不能自动推出后两层。

## 2. 与VLM、视频模型、世界模型的关系

- VLM可主要输出文字、掩码或坐标；有视觉输入不等于能够原生生成图像。
- 视频模型能生成运动，不等于具有可用的视觉问答或错误诊断接口。VACE的“统一创建与编辑”和LTX-2的“音视频统一”不能直接当作理解—生成统一。
- 世界模型强调条件状态转移及其对规划/行动的作用。图文交错答对一题，不等于获得机器人闭环执行能力。
- 模型生成的图片是其预测或构造，不是新的真实观测。自洽也可能是持续保持同一个错误。

## 3. 研究分支

1. 表示与架构：共享什么，分开什么；语义与细节是否冲突。
2. 生成式视觉推理：什么时候画、画什么、画完是否真正被使用。
3. 后训练与恢复：错误检测、有效反馈、执行修复、避免误改。
4. 持续状态：对象身份、关系、动作和多轮历史。
5. 效率：少步、跳层、缓存、局部执行、按需理解、标注和训练成本。
6. 评测：任务联合、输出等价性、因果干预、可验证过程。

## 4. 与中文书写的连接

中文书写提供了离散事件和连续几何并存的试验对象。静态认识一个字，与辨认实际写了哪一笔、生成正确下一笔，是不同能力。

但“读写联合”已有[InkSight](https://arxiv.org/abs/2402.05804)，“列级书法识别生成统一”已有[UniCalli](https://arxiv.org/html/2510.13745v2)。因此，UMM在本专题的贡献必须具体到过程、效率、泛化或新的可解释协同，不可只靠模型名称。

## 5. 学习顺序

Janus/Transfusion（表示及目标）→ BAGEL/Show-o2（具体基座）→ Zebra-CoT/ThinkMorph（交错推理）→ GapEval/UniG2U/VGUBench（协同是否有效）→ UMM-Reflection/UniCache（恢复和效率）→ UniCalli/InkSight/OnOff（书写直接前作）。

阅读顺序不是研究质量或录用概率排名。每篇核查层级见文献表，未逐篇复现。

## 从 VLM 和生成模型理解 UMM

[LLaVA](https://arxiv.org/abs/2304.08485) 式 VLM 将视觉编码经连接器送入语言模型，常以文字交叉熵学习回答。它能描述图像，但没有因此自动获得像素解码器。视觉语义编码倾向保留“是什么”，逐笔生成还需要精细的“在哪里、怎样变化”。

生成模型大致有两种常见训练方式。[Chameleon](https://arxiv.org/abs/2405.09818)、[Emu3](https://arxiv.org/abs/2409.18869) 将视觉离散化并建模后续 token；[潜空间扩散](https://arxiv.org/abs/2112.10752)学习从噪声恢复视觉潜变量。[Flow Matching](https://arxiv.org/abs/2210.02747) 则回归连接噪声与数据的向量场，积分得到图像或视频。

设数据潜变量为 z、噪声为 ε，一种简化的 flow matching 写法为：

\[
z_\tau=(1-\tau)\epsilon+\tau z,\qquad
\mathcal L_{FM}=\mathbb E\|v_\theta(z_\tau,\tau,c)-(z-\epsilon)\|^2.
\]

这里 τ 是生成求解时间；视频帧 t 是被生成内容的时间；第 k 笔又是离散事件索引。三者不能互换。逐步去噪不等于逐笔书写，生成整段视频也不意味着必须按物理帧顺序进行去噪。

UMM 将文字任务和视觉生成放进一个可训练系统，例如共享上下文后分别用 CE 和 FM。共享程度是一项设计选择：Janus 分开视觉编码，BAGEL 区分理解/生成专家，Show-o2 融合语义与低层视觉路径。视觉编码、tokenizer、主干和训练数据是否共享，应逐项说明，不能仅凭“统一”二字判断。

对汉字研究，可共享的是实例身份、局部几何和历史进度；可保留独立的是高分辨率渲染路径。若先压缩时序时已经丢了短笔，再强的文字推理也无法从相同观测中恢复唯一历史。

## 视频底座的论文能力与公开能力

2026-10-16 核查：BAGEL 适合图文交错与关键帧编辑；Show-o2 论文包含视频生成，但官方仍将 T2V/I2V 权重发布列为 TODO。[Lance](https://github.com/bytedance/Lance) 已提供视频检查点与联合微调入口，是原生视频 UMM 的可执行候选。[UniVideo](https://arxiv.org/html/2510.08377v2) 则连接冻结 MLLM 和视频 DiT，适合作为组装式对照。具体接口及硬件边界见[最小研究方案](../experiments/stroke_order_pilot.md)。

## 四篇附件如何帮助理解这条路线

[附件精读](../evidence/attachment_reviews.md)分别拆解 Timage 的输入覆盖层、ORVOS 的因果历史、SC-CoIT 的跨模态恢复与 BoxTuning 的对象提示。只有 SC-CoIT 直接检验 UMM 的理解—生成恢复；其检测强、立即修复弱的结果说明，共享语义和正确诊断还不能取代执行监督。

## 任务接口与协同实验的原文补充（2026-10-20）

[本批审查](../evidence/unified_interfaces_and_transfer_2026-10-20.md)逐项区分输出与外部解码成本。Qwen3-Omni处理视频输入但输出文字/语音；SEED-X的Edit/PPT/Story/Try-on是专门微调版本。Qwen3-Omni受控对照报告部分视觉增益、部分单项下降，并明确无可测语言增益；Manzano近似保持任务性能的对照按任务token匹配，未固定总FLOPs。Emu3.5的操作评价是子任务/关键帧自动评审，尚不证明机器人闭环执行。

## 早期前作与负迁移（2026-10-20）

[OFA](../reviews/L073.md)的统一预训后仍按任务微调；图像分数含24选1。[Unified-IO](../reviews/L074.md)评估单一联合模型，其消融按剩余任务曝光缩短步数，显示图像合成对关键点的帮助以及文字任务对部分视觉任务的干扰。[UniDiffuser](../reviews/L076.md)独立噪声时间统一条件/联合/边缘分布，有限T为近似边缘化；[MetaQueries](../reviews/L062.md)冻结MLLM是强组合基线，保留理解尚不代表生成训练提高理解。详见[历史机制与实验迁移](../evidence/early_unification_and_distribution_review_2026-10-20.md)。

## 压缩与条件解码的边界（2026-10-20）

[LaVIT](../reviews/L079.md)理解连续/监督离散且混纯文仍有遗忘；[NExT-GPT](../reviews/L080.md)用四模态专家decoder做语义条件连接；[DreamLLM](../reviews/L081.md)让冻结扩散loss回传LLM；[SEED-LLaMA](../reviews/L082.md)改用unCLIP图像条件。[Emu2](../reviews/L083.md)主体保真与文字对齐存在取舍；[MM-Interleaved](../reviews/L084.md)通过细节旁路改善空间访问；[VILA-U](../reviews/L085.md)无需扩散decoder，但作者尚未观察到理解生成显著协同。详见[机制与实验条件](../evidence/compression_conditions_and_synergy_2026-10-20.md)。

## 联合训练与外部反馈（2026-10-20）

[JanusFlow](../reviews/L086.md)固定任务曝光的消融仍有FID/POPE下降；[Orthus](../reviews/L087.md)软量化与条件扩散头有低成本转换证据；[Liquid](../reviews/L088.md)增数据的改善伴计算改变。[ILLUME](../reviews/L089.md)用GPT-4o评估自生成图，[X-Omni](../reviews/L093.md)采用OCR/VLM奖励和中文分支，均须记教师成本。[MetaMorph](../reviews/L090.md)少量T2I之外仍有其他生成监督，[UGen](../reviews/L091.md)渐进词表不能消除全部单任务差距，[Harmon](../reviews/L092.md)MAR表示理解/生成仍有取舍。见[跨方法审查](../evidence/curricula_feedback_and_synergy_2026-10-20.md)。

## 视觉码的实验与理论边界（2026-10-20）

[QLIP](../reviews/L095.md)独立LLaVA用连续倒数第二层，统一UM³生成仍弱于其对照；[DualToken](../reviews/L096.md)同塔双码可保留外观/语义但不在每项理解指标更优；[UniToken](../reviews/L097.md)连续旁路缓解干扰，联合仍有退化。[Selftok](../reviews/L098.md)实测RL增益与其“空间码不可RL”理论需分别评价；[DDPO](../reviews/L185.md)早已对扩散定义去噪MDP。[UniCode²](../reviews/L099.md)大码本覆盖率不等于均匀entropy，[Tuna](../reviews/L100.md)1.5B视频与7B静态能力需分开。见[数学、配方与迁移审查](../evidence/tokenizer_theory_and_rl_2026-10-20.md)。

最新表示审查补充：UniCom主模型预测压缩语义特征，公开最终decoder仍调用Flux VAE；Tuna-2/PixelUMM可直接像素预测，RF仍保留理解encoder。EvoTok残差深度与去噪时间都不对应真实笔画事件。具体七字段、退化指标及实验条件见[像素/时间接口专题](../evidence/pixel_interfaces_and_temporal_audit_2026-10-20.md)。

## 离散/连续建模的进一步区分

FUDOKI是非吸收metricCTMC，可修改普通token；Muddit/LaViDa-O/Lumina的mask路径及采样器另有不同。FullFlow连续图像+离散插入文本，LLaDA2Uni离散骨干+连续图像decoder，MultimodalFlow连续embedding骨干+离散文字decoder。统一目标要指出作用模块；采样迭代、空间揭示及块间因果都不直接对应物理书写时间。见[机制与实验审查](../evidence/discrete_paths_and_flow_audit_2026-10-20.md)。

## 开放模型与移动系统的成本口径

BLIP3o8B公开权重与含私有数据论文版分数不同；OpenUni冻结VLM的理解成绩为继承；UniFork小消融在部分指标仍逊单任务专家。DeepGen约5B仍用64H200做两阶段训练；Mobile-O的.5B是语言骨干口径，total约1.6B，导出精度和内存测量需对齐。见[条件与部署审查](../evidence/open_models_and_deployment_audit_2026-10-20.md)。

## 原生像素与共享路由

UniFlow是一阶段语义codec重建/理解，并非凭零样本视频重建即可称文字生成视频；SenseNova-U1原生像素和Mamoda2.5额外编码器的依赖不同。Rosetta早任务分数仍有下降；梯度投影相对动量，不能推出任意旧任务都不遗忘。见[条件审查](../evidence/native_pixels_video_moe_and_projection_audit_2026-10-20.md)。

## 后训练协同的归因

本批区分语义配对、自采样SFT、双DPO、GRPO与多轮编辑。HermesFlow正式.64→.69且genDPO.70更高；UniCorn/GvU均有理解子项下降；R3理解增益限相关域。PairUni BAGEL扩展实际为SFT。见[原文/理论/实现审查](../evidence/paired_preferences_self_supervision_and_claims_2026-10-20.md)。

## 联合训练需要分清保证与观测

[第十八批](../evidence/joint_rl_gradient_theory_and_targets_2026-10-20.md)分析rewardGRPO、个性化双路径、局部梯度整合、共同编辑目标及动态困难池。ParetoLoRA视觉指标提高伴Task4文字下降；STBridge一致性与外部正确需分测；MATE理解收益未依赖困难/演化消融，单seed小差异不能作强因果结论。

## 评价对象与协同归因

[第十九批](../evidence/benchmark_construct_validity_and_cross_modal_editing_2026-10-20.md)区分自生成QA、原图重建后QA、任务中间视觉状态、新规则适应与文字知识编辑迁移。评价链可诊断接口失真；证明共享参数收益仍需同数据/信息/计算的流水线与单分支对照。

## 知识与复杂图像编辑的观察

[第二十批](../evidence/knowledge_editing_and_multilingual_text_metrics_2026-10-20.md)显示知识线索、静态图执行、背景保留和文字渲染各有瓶颈。BAGELCoT在WISE总分提高，但OneIG文字分下降；KRIS程序类也退步，协同Claim必须限定任务/指标和计算。

## 长程生成及接口审查

[第二十一批](../evidence/long_horizon_memory_and_multimodal_generation_paths_2026-10-20.md)区分固定文字的图像续写、原生故事规划、语义全历史与稠密生成记忆；MIO离散码后接扩散、OmniFlow连续潜流后文字AR解码、M2omni文字接口接独立SD3、Ming冻结感知后训桥接，不能只凭统一名称推断共享机制或双向收益。

## 交错文档及教师数据

[第二十二批](../evidence/interleaved_data_editing_and_distillation_audit_2026-10-20.md)区分MMC4相似度分配、OBELICS网页结构、OmniCorpus关键帧故事板、CoMM连贯步骤及合成编辑数据。以上顺序均需与真实动作时间标注分别定义；可生成图序列的任务不能直接改称书写视频生成。

## 全模态及动作世界接口

[第二十三批](../evidence/omni_action_world_and_theory_audit_2026-10-20.md)区分Ming/LongCat的video输入、ERNIE视觉AR+扩散refiner、BagelVLA第三动作专家、WorldBagel两专家动作表示、SenseNova视觉标签生成以及Puffin相机几何。共享名称、专家重叠或“physics”一词不能代替任务接口和因果实验。

## 交错推理与视频过程的边界

[第二十四批](../evidence/interleaved_reasoning_cost_and_latent_policy_audit_2026-10-20.md)区分图文mask联合恢复、辅助图thought、连续hidden思考、多轮静态编辑和真实轨迹生成。去噪迭代、推理图序列和画笔物理时间不能互换；交错训练带来的准确率收益还需干预视觉thought来验证因果作用。
