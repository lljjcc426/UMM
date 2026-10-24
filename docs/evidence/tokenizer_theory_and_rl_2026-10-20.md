# 视觉tokenizer的理论、配方与RL证据审查

本批复核L095–L100，并补入[DDPO/L185](../reviews/L185.md)。方法与结果详见[逐篇笔记](../reviews/README.md)。只记录实际已读范围，没有将拿到PDF、代码或模型链接视为完成全文精读、可运行或复现。

## 需要分别回答的三个问题

1. tokenizer是否保留理解所需语义、像素细节与局部文字差异？
2. 在固定码率、初始化、数据和计算下，下游生成/理解是否改善？
3. 两任务联合是否真正互利，优势由哪个模块或训练条件带来？

QLIP Table7在同15M训练图像/LlamaGen-XL下GenEval .31→.48；它的LLaVA默认使用量化前倒数第二层连续特征。统一UM³的COCO gFID44.1弱于相近视觉曝光LlamaGen33.4。三组实验支持的对象不同。

DualToken使用同塔浅层pixel与深层semantic双码；embedding维拼接不增加空间位置数，但残差深度与两个depthhead仍有额外计算。Table4双码平均更好，VQAv2/MMMU仍低于原SigLIP。UniToken Table6联合GenEval49.4低于生成only51.1，TextRead49.5低于理解only50.1，支持缓解干扰。

Tuna Table7 row3→12的MME1386→1361下降，其他所列理解/生成指标改善，正文全项互利表述需收窄。Tuna7B未视频训练；视频理解49帧、Show-o2 32帧，不能省略条件。1.5B视频VBench Quality84.32和Semantic83.04未检验规范笔顺或真实抬笔。

## UniCode²：数学论证的具体缺口

已视觉核对arXiv:2506.20214 PDF第3–4页Eq1–3及Fig2。以下推导为本仓库数学分析，与作者报告的实测成绩分开。

Eq1正λ项为Σ||c_k-c̄||²。在最小化中，它的梯度为2λ(c_k-c̄)，梯度下降会把中心拉向总体均值；该项自身不能支持正文“促进码本展开、防止坍缩”的解释。它也没有直接约束样本分配频率。

Eq2称期望量化误差≥各簇方差的无权平均。一般情况下，以簇概率q_k、条件均值μ_k和码中心c_k表示，精确分解为：

E||e-c_Q(e)||² = Σ_k q_k[Var(e|k)+||μ_k-c_k||²]。

若中心等于条件均值、两个簇概率.99/.01、方差0/100，则左侧为1，无权平均为50。可取数据质量.99在0、.005在90、.005在110，码本{0,100}，最近邻分配满足这些条件。因此原文下界缺少分配等条件，不能一般成立。

AppA3 Eq12给出q加权形式，Eq14改用失真−βH(q)，这与Eq1的中心收缩项不同；论文未给等价证明。Eq17的高分辨量化叙述仍需源分布、尺度和正则性假设。不能从普通Kmeans或验证集98.7%码被使用过，推出频率均匀或熵最大。

经验部分仍应按表报告：500K聚类理解平均77.4、coverage98.7%，级联优于所列单码变体；这些结果不依赖接受上述不充分理论。Table3 VQGAN10K三分数63.1/56.2/63.1的均值60.8与原列64.1不一致。未核代码，当前没有据此断言实现失败。

## Selftok：生成策略的MDP与数据编码关系

Selftok实测GenEval .74→.95、DPG81.80→85.57，值得纳入后训练对照。其§4.1却称空间token不能满足Bellman、无法RL，该必要性结论不能由所给编码依赖推出。

一个直接构造是：状态s_k含提示及已生成空间token前缀，行动为下一位置的码，转移追加该码，完成后解码整图并给终端奖励。把k纳入状态即可形成有限时域MDP；未来行动不会改写已采样的前缀。静态encoder的感受野或自然图像各部分的相关性，不妨碍定义这个生成决策过程。

经典[DDPO](https://proceedings.iclr.cc/paper_files/paper/2024/hash/14f75513f0f1ca01de1e826b52e6b840-Abstract-Conference.html)也以(prompt,t,x_t)为状态、x_(t−1)为行动，对随机扩散转移计算logdensity并优化终端奖励。这支持非离散AR路径的RL构造；确定性ODE是否能使用相同密度估计则需另证。

Selftok PDF第25页Eq20只显式写−A+KL，未显示logπ或importance因子。若采样优势作为常量，该式不足以给出奖励的策略梯度；这是公式呈现的待澄清项，实际实现未读。DDPO的推导可作为对照，不能用理论疑点抹去实测收益。

## 奖励正确性与文字捷径

DDPO附录A已展示VLM计数奖励被图中数字文字欺骗，以及不可压缩奖励导向高频噪声；作者还说明定性样例手选退化前checkpoint。Selftok的程序/VQA奖励与GenEval/DPG评价相近，更需要独立评价器和域外提示检验。

文字/绘画/视频实验应分别测奖励值、独立OCR、真实事件、任务完成、多样性和人评。训练与测试提示去重只能处理一种泄漏；共享识别器弱点、语义模板重复、字体/字形近重复还要分别审查。

## 公开代码和无独立论文制品

| 制品及已读revision | 已核内容 | 尚未支持的结论 |
| --- | --- | --- |
| [QLIP cf86fcc](https://github.com/NVlabs/QLIP/tree/cf86fcc5131c2bb008c349fe9456ccbd1e0e1619) | README、配置相关字段；三个HF tokenizer入口与bits/压缩指标定义 | README论文链接仍占位，不能由tokenizer模型表认定完整UM³训练公开可复现 |
| [DualToken499e5b1](https://github.com/songweii/DualToken/tree/499e5b1d716bb72f5e5e2a91eae78ab53cf2ef3d) | README、run.sh、256配置；浅/深层、shortcut与双RQ；训练示例8进程 | MLLM代码/权重仍写未来发布，HF按钮空；示例CC12M配方不代表完整论文数据 |
| [UniToken9181c61](https://github.com/SxJyJay/UniToken/tree/9181c61367baf44e67f08984cac8347c1d5a1626) | README/TRAIN、base与AnyRes-stage2、phase2混合yaml | 两stage2均指phase1 caption配置，accum_iter需外部提供；III配方/制品未对应，未运行 |

这些是论文关联的工程制品，未重复增加独立论文计数。HF链接可见性、完整权重、训练数据、代码与实际重现实验分别记录。

## 对研究设计与写作的迁移

先测tokenizer重建与最小笔形差上限，再测联合模型。固定有效bits、位置数、残差深度和decoder，并把语义教师初始化纳入预算；连续旁路、分层双码、非空间query和VAE潜空间encoder是不同对照。

研究笔顺时要另定义可观察的笔画身份/先后/方向/抬笔和执行约束。非空间渐进重建、去噪时间、AR光栅次序和训练课程都不能直接作为真实笔画时间。

Introduction提出具体缺口，Method说明可检验机制，实验区分表示保真、单任务与联合收益。Claim写清分布、预算和对照；Limitations保留数表冲突、理论假设、公开制品缺项及域外失败。


第一百一十五批（2026-10-22）：UniCode²核心全读更新：Eq12含条件偏差、H高不保证I、分布缩放限制Eq17；实际PDF T4参数单位GB、T6训练超参，旧位置已修正。见[审查](unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[L099](../reviews/L099.md)。


第一百一十七批（2026-10-22）：UniWeTok的位置数、组合码本、有限usage和bits口径；T3前/后蒸馏需追读出位置，不据T2不同SigLu设置直接判错。见[审查](uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[L101](../reviews/L101.md)。


第一百一十八批（2026-10-22）：残差层级分配、独立码本槽位和256位置×4depthhead成本；F5曲线受监督位置和decoder影响。见[审查](evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[L102](../reviews/L102.md)。


第一百一十九批（2026-10-22）：OCR19.40点下降、原特征拼接成本，连续通道瓶颈与空间压缩需等资源比较。见[审查](unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[L104](../reviews/L104.md)。


第一百二十批（2026-10-22）：像素patch非自动无损、加权MSE与分母截断、mask后标签可辨性及额外预训成本。见[审查](tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[L105](../reviews/L105.md)。


第一百二十一批（2026-10-22）：SK软边际/硬argmax、跨batch指派与AR曝光误差；VLM-only五降保留。见[审查](representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[L106](../reviews/L106.md)。


第一百二十二批（2026-10-22）：17帧→5时间位置、动态度/平滑退步，因果mask不推出规范笔顺。见[审查](hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[L107](../reviews/L107.md)。


第一百二十三批（2026-10-22）：3072→4096可单射，四帧tubelet不自动推出信息损失；边界平滑需控制模糊。见[审查](pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[L108](../reviews/L108.md)。


第一百二十四批（2026-10-22）：动能最优限制与非mask回访；BestN外部judge选择不等已实施RL，L2四次方代码差异。见[审查](fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[L109](../reviews/L109.md)。


第一百二十五批（2026-10-22）：4096原VQ码→1024压缩位置，分层采样不等笔顺，反思非单调/无RL执行。见[审查](lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[L111](../reviews/L111.md)。


第一百二十六批（2026-10-22）：SelfGRPO权重均值抵消/无old但有reference；离散局部码固定不推出RGB不变。见[审查](lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[L112](../reviews/L112.md)。


第一百二十七批（2026-10-22）：语音codec接口非全离散；负熵选择和采样温度并非规范笔画顺序。见[审查](omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[L113](../reviews/L113.md)。


第一百二十八批（2026-10-22）：语义码损细节、主干CE/decoderFM分别优化，RL为未来方向，互补mask不等独立数据翻倍。见[审查](llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[L114](../reviews/L114.md)。


第一百二十九批（2026-10-22）：T5删除子词可decode/re-tokenize冻结CLIP但不保证语法；两阶段调度反例及Poisson非零门协议。见[审查](fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[L115](../reviews/L115.md)。


第一百三十批（2026-10-22）：连续语义码仍可丢信息；主干FM与独立CE decoder、512/1152维权重及T6取舍。见[审查](multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[L116](../reviews/L116.md)。


第一百三十一批（2026-10-22）：64×1792语义码可能丢细笔；native Qwen与EVA编码分支不同，NEXT GRPO不回填原版。见[审查](blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[L117](../reviews/L117.md)。


第一百三十二批（2026-10-22）：256query条件不等256AR输出，DC-AE32倍压缩的细笔上限及GenEval蒸馏/RL/rewrite区别。见[审查](openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[L118](../reviews/L118.md)。


第一百三十三批（2026-10-22）：VILA-U RQ四深度与逐空间生成、CFG/top-p/top-k、256原生与384错配；不等规范笔顺。见[审查](unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[L119](../reviews/L119.md)。


第一百三十四批（2026-10-22）：16倍32通道VAE与双表示、MixGRPO/SRPO/ReDA/MeanFlow说明的实证边界，80B蒸馏与20B剪枝分开。见[审查](hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[L120](../reviews/L120.md)。


第一百三十五批（2026-10-22）：CPS残差代理logp、带方差速度约束、MR-GRPO/GDPO/持续SFT、静态生成与真实笔画时间区分。见[审查](deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[L121](../reviews/L121.md)。


第一百三十六批（2026-10-22）：AR显式CoT与连续latent flow分工、16通道与2×2 patch64维、VAE细笔和文字无序计数局限；本工作不作为新RL算法归类。见[审查](internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[L123](../reviews/L123.md)。


第一百三十七批（2026-10-22）：4×16×16视频VAE细文字代价、AR条件与非视觉AR、DMD/NFT复合奖励及评价独立性。见[审查](mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[L124](../reviews/L124.md)。


第一百三十八批（2026-10-22）：像素2048/3072瓶颈、x预测v损失夹分母、多重集合IoU对召回差异、FlowGRPO与后蒸馏机制。见[审查](sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[L125](../reviews/L125.md)。


第一百三十九批（2026-10-22）：RGPO文字token ratio、图像CLIP及随机latent层特征正则；公式和代码KL方向/std分母不一致。见[审查](mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.md)、[L128](../reviews/L128.md)。


第一百四十批（2026-10-22）：共享优势两路token ratio、固定视觉头/LLM更新、TIM裁判与CFG/teacherforcing位置核查。见[审查](corl_joint_advantage_branch_and_reward_release_audit_2026-10-22.md)、[L129](../reviews/L129.md)。


第一百四十一批（2026-10-22）：独立task优势std后sqrt、无oldpolicyclip的scorefunction、模态token总分母和CFG概率边界。见[审查](pairuni_pair_weighting_gradient_and_release_audit_2026-10-22.md)、[L130](../reviews/L130.md)。


第一百四十二批（2026-10-22）：UniCorn离线选优CE+flowMSE，未用在线GRPO；固定数据MI与学习交叉熵不可混同，拒绝采样代价纳入。见[审查](unicorn_selfplay_joint_objective_and_unicycle_protocol_audit_2026-10-22.md)、[L131](../reviews/L131.md)。


第一百四十三批（2026-10-22）：Tree阶段课程、组中心化无std/格式门控、行为clip、图像几何概率比及KL因子；时间网格16/21为15/20更新。见[审查](r3_tree_rl_understanding_scope_and_prompt_overlap_audit_2026-10-22.md)、[L132](../reviews/L132.md)。


第一百四十四批（2026-10-22）：每图聚合文本概率的AR图码RL；FLUX还接原文本，公开scorefunction+KL未用oldpolicyclip，no_grad不等跨步固定教师。见[审查](gvu_intrinsic_probability_reward_and_release_audit_2026-10-22.md)、[L133](../reviews/L133.md)。


第一百四十五批（2026-10-22）：组相对baseline/除std、KL梯度与下界、dense max复用patch、缺归一flow重加权和稀疏路由非正交保证。见[审查](lvrpo_theory_reward_and_protocol_audit_2026-10-22.md)、[L134](../reviews/L134.md)。


第一百四十六批（2026-10-22）：固定MaskGIT位置logp与真正采样动作概率区分；DrGRPO去std/响应长度归一为既有方法；同组随机baseline协方差、DGS选择偏差、TIER维数界和控制误差符号。见[审查](uni_synergy_dgs_theory_and_personalization_release_audit_2026-10-22.md)、[L135](../reviews/L135.md)。


第一百四十七批（2026-10-23）：部件树位置与书写时序分开；TPE纸面频率/源码路径均值/原始内积反例；InfoNCE/dual为监督联合机制，未使用策略强化学习。见[审查](chinese_radical_joint_tpe_geometry_and_negative_transfer_audit_2026-10-23.md)、[L181](../reviews/L181.md)。


第一百四十八批（2026-10-23）：STTN为SpatialTransformer几何，不属自注意力UMM；BPN合成参数监督再真实重构自监督，无策略强化学习或笔画事件token。见[审查](strive_video_text_replacement_and_propagation_protocol_audit_2026-10-23.md)、[L182](../reviews/L182.md)。


第一百四十九批（2026-10-23）：风格VQ混连续条件，SCE/PCE与噪声MSE监督；当前梯度标准差配权不等正式固定α，无策略RL/统一理解生成。见[审查](constant_multilingual_style_quantization_and_evaluation_audit_2026-10-23.md)、[L183](../reviews/L183.md)。


第一百五十批（2026-10-23）：CE+FM SFT后captionGRPO和图像MixGRPO，caption阶段不rollout图像且使用离线GT差分；共享冻结与reward细节需实现核对。见[审查](stbridge_shared_target_alignment_and_causal_controls_audit_2026-10-23.md)、[L137](../reviews/L137.md)。


第一百五十一批（2026-10-23）：GRPO同组标准化、σfloor丢组但保留到下池、fallback可能低于τ；固定外部reward与共享更新的间接影响。见[审查](mate_adversarial_pool_evolution_and_budget_audit_2026-10-23.md)、[L138](../reviews/L138.md)。


第一百五十二批（2026-10-23）：全部共享小decoder的任务梯度诊断不等真实信息转移；全平行投影改梯度模长和任务比，论文CAGrad文字与原约束对偶不同。见[审查](gradient_conflict_metric_validity_and_causal_audit_2026-10-23.md)、[L139](../reviews/L139.md)。


第一百五十三批（2026-10-23）：raster索引是空间顺序，原Show-o mask迭代非左到右AR；PAM只对选桶与缓存EMA去负分量，不保证当前总梯度或AdamW更新无冲突。见[审查](position_gradient_attribution_and_lora_budget_audit_2026-10-23.md)、[L140](../reviews/L140.md)。


第一百五十四批（2026-10-23）：语言知识编辑→条件表示→视觉实现是不同测量环节；Reason提示拼接在正文/生成/诊断脚本不同，需固定路径，行空间软化须同时检查知识保持代价。见[审查](unike_cross_modal_editing_and_artifact_protocol_audit_2026-10-23.md)、[L141](../reviews/L141.md)。


第一百五十五批（2026-10-23）：自评奖励可能提高猜目标b而非看图a，需独立校准与负例；生成/理解/答题格式分开，低分/大CV不能单独证明更有效基准。见[审查](unieval_self_evaluation_identifiability_and_answer_bias_audit_2026-10-23.md)、[L143](../reviews/L143.md)。


第一百五十六批（2026-10-23）：状态表征可作外部记忆，拓扑真错与解析阈值失败分开；GT中间态改善提供空间不证明自身图因果，未知长度和预算需一致。见[审查](unimmmu_state_parsing_oracle_length_and_synergy_audit_2026-10-23.md)、[L144](../reviews/L144.md)。


第一百五十七批（2026-10-23）：GENIUS两定理限固定向量和冻结系数；Eq5–8补偿方向/归一与Eq28/33不一致。有限logit偏置不保证噪声贡献为0，需任务损失与因果消融。见[审查](genius_contextual_rules_attention_theory_and_metric_tradeoffs_audit_2026-10-23.md)、[L145](../reviews/L145.md)。


第一百五十八批（2026-10-23）：WISE架构组不是受控结构消融，QwenImage等语言条件扩散不意味着AR视觉token；需固定底座/预算再检验CoT知识到生成的因果接口。见[审查](wise_gold_explanation_verified_protocol_and_knowledge_validity_audit_2026-10-23.md)、[L147](../reviews/L147.md)。


第一百五十九批（2026-10-23）：ImgEdit将Qwen语义与SigLIP视觉投影为FLUX文字支条件；训练50K/10Kstep/Prodigy batch128，不提供共享UMM协同因果或RL效果。见[审查](imgedit_dataset_versions_score_gating_and_pipeline_reproducibility_audit_2026-10-23.md)、[L148](../reviews/L148.md)。


第一百七十七批（2026-10-24）：组std>0只要求复合reward有差，不保证同组答案有对有错；Eq16单样本logratio不等同非负KL估计，完整RL未发布。代码min与论文mean、MSE/2D/1D分支和fallback需明确主表配置。见[审查](omni_r1_full_perception_reward_protocol_and_release_audit_2026-10-24.md)、[U11](../reviews/U11.md)。


第一百七十八批（2026-10-24）：BAGEL继承MoT/AR+flow，公开每轮独立inferencer，多图取回不等持久KV记忆；单轮重编图号与长程内状态归因需干预。见[审查](weave_full_interleaved_benchmark_scoring_and_annotation_audit_2026-10-24.md)、[U12](../reviews/U12.md)。


第一百七十九批（2026-10-24）：Gapfit论文按模型i/代码每模型四任务行，totalcount1000、λ2.7/1.05 vs2/2；共现修正在logit事后而非MAPloss；BAGEL混标准数据的干预不可称纯单侧。见[审查](gapeval_full_bidirectional_information_scoring_and_release_audit_2026-10-24.md)、[U13](../reviews/U13.md)。


第一百八十批（2026-10-24）：Emu3/MIO分类与原始token机制不齐；统一接口/共享参数分层，纠正错误引文ID；GtA额外NFE图数与文本token缺compute匹配。见[审查](unig2u_full_generation_to_understanding_budget_and_scoring_audit_2026-10-24.md)、[U14](../reviews/U14.md)。


第一百八十一批（2026-10-24）：无新训练/tokenizer/扩散方程；外部Gemini/GPTImage组合72.7是工程参照，非同compute理论oracle。见[审查](realunify_full_bidirectional_stepwise_and_conjunctive_judging_audit_2026-10-24.md)、[U15](../reviews/U15.md)。


第一百八十二批（2026-10-24）：本文无新训练/扩散公式；Showo移除autoencoder概述及BAGEL综述引文不宜沿用覆盖既有准确架构。见[审查](vgubench_full_typographic_answer_and_correlation_identifiability_audit_2026-10-24.md)、[U16](../reviews/U16.md)。


第一百八十三批（2026-10-24）：无预训练视觉encoder/VAE，32patch+16prebuffer/文本AR图flow；两支路共享attention，路由与重建需因子化而非全归模块。见[审查](native_synergy_full_routing_reconstruction_and_system_controls_audit_2026-10-24.md)、[U17](../reviews/U17.md)。


第一百八十四批（2026-10-24）：LoRA只调QKV/MLP、encoder/head冻结；离散diffusion/AR/连续路差异未控，F10attention不同阶段且Janusmask索引需澄清。见[审查](transferability_full_parser_coverage_and_distribution_shift_audit_2026-10-24.md)、[U18](../reviews/U18.md)。


第一百八十五批（2026-10-24）：Show-o图像maskedprediction；4096codebook瓶颈缺容量干预。Harmon四loss权重1并有条件梯度scale.1，冻结按实际布尔值。见[审查](unimrg_full_teacher_targets_training_schedule_and_release_audit_2026-10-24.md)、[U19](../reviews/U19.md)。


第一百八十六批（2026-10-24）：I文本/原图相对mass、F原图ViTabs、双弱AND；无训练更新、RLreward仅展望，层/CFG/attentionkernel聚合待释。见[审查](adavig_full_counterfactual_denominators_and_early_abort_cost_audit_2026-10-24.md)、[U21](../reviews/U21.md)。


第一百八十七批（2026-10-25）：无新tokenizer或训练loss；参考生成/模型草拟rubric与同源judge需校准，不能将单模型人评直接升级为通用RLreward证据。见[审查](ueval_full_rubric_aggregation_and_release_protocol_audit_2026-10-25.md)、[U22](../reviews/U22.md)。


第一百八十八批（2026-10-25）：SCO无训练loss/tokenizer/RL，投影是测试时采样控制；四分支同latent，planner与promptrewrite质量为前提，不能当语义因果分解保证。见[审查](sco_full_soft_constraint_solver_and_video_protocol_audit_2026-10-25.md)、[U23](../reviews/U23.md)。


第一百八十九批（2026-10-25）：BAGEL CE+FM、Eq6时间/速度目标符号需实现约定；GRPO只文字policy项，视觉ref为velocityMSE，未直接证明densityKL。见[审查](visworld_full_theory_comparability_and_release_protocol_audit_2026-10-25.md)、[U25](../reviews/U25.md)。


第一百九十批（2026-10-25）：Encoder/VAE-free仍有学习patch投影和空间ConvDecoder；42层8.2B双分支，最终config确认pixel head/noise embedding/max16，8B不等全参数总量。见[审查](sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.md)、[U26](../reviews/U26.md)。


第一百九十一批（2026-10-25）：z(t)=(1−t)z0+t z1、target z1−z0符号一致；两taskembedding/等概率双向，同一MSE仍有任务梯度/尺度差异，无实测冲突消除。见[审查](unimodel_full_visual_only_cycle_and_evidence_scope_audit_2026-10-25.md)、[U27](../reviews/U27.md)。


第一百九十二批（2026-10-25）：−logsigmoid(best−worst)可通过降低worst减损，无reference ratio，不能继承DPO或平均鲁棒性保证；K1无排序梯度。见[审查](latentumm_full_dual_alignment_gradient_and_rollout_protocol_audit_2026-10-25.md)、[U28](../reviews/U28.md)。


第一百九十三批（2026-10-25）：双向stopgrad InfoNCE与unique NCECLUB依critic条件；公开工具GaussianCLUB/无内部detach，完整调用方未发布，不能认定历史实现。见[审查](diva_full_information_factorization_and_release_protocol_audit_2026-10-25.md)、[U31](../reviews/U31.md)。


第一百九十四批（2026-10-25）：传统二值骨架/EF/ARG无学习型tokenizer或RL；3×3逆查和POL窗口不同，T0=k0w/T1=(T0+w²)/2保具体假设。见[审查](video_based_chinese_recognition_2005_full_temporal_recovery_audit_2026-10-25.md)、[L009](../reviews/L009.md)。


第一百九十五批（2026-10-25）：图2RealFake/Agent不能当实际GAN/RL证据；正文仅MSE/Adam代理监督，低维控制参数与笔序token分开。见[审查](bbsmg_full_calibrated_neural_brush_renderer_audit_2026-10-25.md)、[L007](../reviews/L007.md)。


第一百九十六批（2026-10-25）：本文为解析/规则规划，GAN/RL是比较对象；空间/时间/压深动作接口可迁移，缺笔顺监督和closed-loop证据。见[审查](calligraphy_3d_full_quintic_constraints_and_public_release_audit_2026-10-25.md)、[L008](../reviews/L008.md)。


第一百九十七批（2026-10-25）：伪词1–3subword，首token评分因果mask控制patch捷径；MLP和共享rank对照、激活/权重编辑的计算位置与优化机制分开。见[审查](entry_point_umm_full_causal_interface_and_compute_audit_2026-10-25.md)、[L030](../reviews/L030.md)。


第一百九十八批（2026-10-25）：答案text vs VAE pool监督/位置不对称；L030名字单层地址patch与本篇全层VAE属性steering不同，Janus差异不构成直接矛盾。见[审查](one_space_full_directional_steering_and_architecture_claim_audit_2026-10-25.md)、[L031](../reviews/L031.md)。


第一百九十九批（2026-10-25）：文本推理93.4与图像执行17.8测不同变量；清空缓存Rp执行无需训练，未证明视频/结构化动作执行迁移。见[审查](ureason_v3_full_context_intervention_and_release_audit_2026-10-25.md)、[L032](../reviews/L032.md)。


第二百批（2026-10-25）：U/C共理解expert、G独立expert，两更新从同Mt独立合并；先期14000生成updates与模型课程成本不能隐去。见[审查](recursive_self_improvement_full_rules_and_native_error_audit_2026-10-25.md)、[L033](../reviews/L033.md)。


第二百零一批（2026-10-25）：Algo1N32在n33集合仅25位置，n34又需要先前未留的旧索引；若存全B可抽样但总存储不bounded，需实现澄清。见[审查](orvos_full_causal_protocol_and_bounded_memory_audit_2026-10-25.md)、[L055](../reviews/L055.md)。


第二百零二批（2026-10-25）：4/8/16帧66.2/65.5/60与grid像素混杂；无CoT代码system仍要求chain-of-thought，机制消融范围有限。见[审查](cot_rvs_v4_full_online_and_release_audit_2026-10-25.md)、[L056](../reviews/L056.md)。


第二百零三批（2026-10-25）：5背景式不能统摄离散flow；semantic可兼重建，query为接口结构，统一tokenizer仍需事件/规则监督。见[审查](umm_survey_v6_full_taxonomy_and_scope_audit_2026-10-25.md)、[L057](../reviews/L057.md)。


第二百零四批（2026-10-25）：小字控制受字高/数据过滤/latent重建等共同影响，未有VAE单因子消融；F2随机初始化与正文copy说明有出入。见[审查](glyphcontrol_full_appendix_and_ocr_denominator_audit_2026-10-25.md)、[S003](../reviews/S003.md)。


第二百零五批（2026-10-25）：OpenFlamingo文字next-token与图像输入；交错预训练不直接赋予图像/视频输出，论文主动保留跨图推理疑问。见[审查](mmc4_full_corpus_release_and_alignment_audit_2026-10-25.md)、[L170](../reviews/L170.md)。


第二百零六批（2026-10-25）：NTP+内联zloss；十倍按图aggregate，不是token/GPU统一十倍。主模型73.85%OBtoken并非纯OB。见[审查](obelics_full_supplement_and_data_mixture_audit_2026-10-25.md)、[L171](../reviews/L171.md)。
