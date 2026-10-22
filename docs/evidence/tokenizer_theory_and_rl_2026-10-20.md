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
