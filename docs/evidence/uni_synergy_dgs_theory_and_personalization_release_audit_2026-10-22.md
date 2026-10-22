# Uni-Synergy／Sync-R1：DGS理论、个性化协议与公开实现审查

第一百四十六批完成[L135](../reviews/L135.md)明确范围核心三遍及五项书面记录。[结构化证据](../../data/uni_synergy_dgs_theory_and_personalization_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），255核心/258书面含未通过项；未确认核心75论文／研究+27资源，资源另按制品审查。无目录新增、文件删除、权重下载或模型执行。

来源：[v1](https://arxiv.org/html/2605.10445v1)、[23页PDF](https://arxiv.org/pdf/2605.10445v1)、[固定官方源码](https://github.com/arctanxarc/UniCTokens/tree/9ca4254c4e94dce82f0fe0e131f27632f89424a2)、[HF固定数据卡与树](https://huggingface.co/datasets/HankYang428/unictokens_data/tree/332df6e7d6d26f2a577f1a7e85874c92ab0cd963)。NeurIPS2025属于前作UniCTokens，本篇正式会场未核。

## 研究问题

少样本人、动物、物体的个性化统一理解与静态图像生成：在已学习用户概念及额外属性后，能否回答/推断隐含属性，并生成身份、上下文和密集提示都相符的图像。输入图像+问题或概念额外信息+推理提示，输出中间文字推理及静态RGB图。Dense文本指提示信息密集，不指图内长文本渲染；没有视频、轨迹、汉字笔顺或机器人动作任务。

## 现有不足及动机

作者将已有统一个性化方法的问题定位为理解与生成缺少显式联合推理反馈，密集语义/隐含属性易丢失，完整多候选图像RL昂贵；因此对文字推理→生成的轨迹施复合奖励，并尝试在去掩码早期筛掉低潜力样本。动机与少样本概念记忆/语义对齐有关；尚未排除提示改写、奖励专家和额外训练本身解释收益，也未证明标准SFT不能实现同等收益。

## 贡献与方法

Sync-GRPO在Show-o个性化初始化上，将Visual Instruct Reasoning和Text Attribute Reasoning两路按1:1混合，用Dr.GRPO式去组std/去响应长度归一，正文Eq2与附录Eq9对文字及图像token加权的old-policy clipped surrogate+参考KL。DGS在50步中的第10步解码代理评分，拒绝低分候选，保留G个候选再完成剩余步骤；扩展UnifyBench++覆盖Reasoning/Dense Reasoning及生成。四奖励为ERNIE3语义向量、BLIP2文图、DINOv2身份及人脸FaceNet；这些是论文设计，公开cleaned代码采用替代评分且缺少文字动作的直接policy loss，不能混为已实现的同一协议。

## 输入、模块、输出和公式作用

视觉路I,Q→Show-o自回归IRvis→basic concept prompt+IRvis→MaskGIT图码→VQ解码RGB；文字路extra_info/inference prompt→IRtxt→inference prompt+IRtxt→同生成器。Eq1将每步每位置图码概率连乘；Eq2、9按αtext=.4/αimage=.6对轨迹token加权，A=R−组均值，无std。DGS代理Rtilde和阈值T决定接受后续算，PR目标.25；Eq7为带趋势项的幂次阈值控制。Eq30–34规定奖励及域权重。标准MaskGIT中已确定位置未重新采样，对所有固定位置重复计logp是额外surrogate；完整采样路径概率与最终图像边缘概率也需区别，不能把连乘直接当严格最终图像似然。

## 模型结构

Show-o1.3B/Phi1.5文本AR+MAGVITv2离散图像去掩码，512²、1024图码；公开config codebook8192/llm_vocab50295/10special/total58498，加入每概念25个token（概念名1+K16+M8）。前两阶段各15epochs，理解b4/生成b1，然后100步RL。αtext/image=.4/.6是损失权重（T4），另有奖励理解/生成4:6与动物(.4,.3,.3,0)/人(.4,.2,.2,.2)，三者不能混淆。公开训练器还使用CLIP、FaceNet/face_recognition及GLM/Gemini，外部LLM抽取/改写IR后才作生成条件；主要image-only轨迹损失会经共享网络间接影响理解，未出现对所采文字IR的logp更新项。

## 数据与划分

论文以UnifyBench扩充UnifyBench++，新增extra_info、Reasoning、Dense Reasoning、Dense Generation、Reasoning Generation、Dense Reasoning Generation；AppB/F6说明斜体extra_info/推理提示用于训练、非斜体用于评估，同一概念的属性分割不能自动视为新概念OOD。未给全部++条目数量/机器可核split清单。HF HankYang428/unictokens_data固定332df6e为2025原UniCTokens发布，数据卡20概念（10人/5动物/5物体）、每概念约10–15图、100随机负例及困难负例；这些是卡片报告，不能充作2026++实测统计。tree仅README/.gitattributes/1.620GB zip；本轮HTTP Range归档内部读取长度不符而停止，未声称读到内部JSON/图像。代码读取concept/test/t2i_conditions.json的前int((n+1)*.5)条用于训练；文件夹叫test不足以判泄漏，需与论文斜体split及实际评测清单逐条对照。HF卡头MIT、正文CC-BY-NC4.0存在许可表述冲突，按冲突记录不自行选定。

## 实验指标

T1个性化Recognition加权分、Reasoning BLEU、Dense Reasoning GPT4o、VQA/QA的BLEU及GPT；PureGen用CLIP-T/CLIP-I，DenseGen/DenseReaGen用分句GPT有效率+CLIP-I，ReaGen用CLIP-T/CLIP-I。Rea BLEU与GT extra_info文本比；ReaGen CLIP-T先将抽象占位替换为GT属性作评测参考，这不等于模型输入也拿到GT。Dense分按标点切片后GPT4o判图中是否实现并平均，存在拆句/裁判版本与校准依赖。T5另YoLLaVA/MC-LLaVA理解、DreamBench/YoLLaVA生成；MC-LLaVA仅单概念子集。无字符CER、笔画事件顺序、视频一致/真实性、执行成功或严格分布外识别；CLIP-I不是身份判别准确率，语义相似奖励不是形式逻辑验证器。

## 比较方法

主要匹配前作UniCTokens1.3B；统一Chameleon+TP/IP7B、Show-o+TP1.3B、YoChameleon7B；理解YoLLaVA13B/Phi1.5、MC-LLaVA13B、RAP-MLLM13B、Qwen2.5VL3B；生成Textual Inversion/DreamBoothSD1B，GPT4o+TP/IP作作者经验参照。YoChameleon每概念1K图，DreamBooth10/3000图条件另列，未等模型/预训/外部裁判和总预算。T1的GPT4o200B没有官方参数规模证据，保留为表中作者标记且不用于效率比；upper bound为经验参照，部分专用模型分数更高，并非理论上界。缺同基座等预算SFT/最佳N、外部改写单独控制、冻结推理/仅imageRL、同终态不同事件过程和独立奖励验证。

## 实验条件

论文8×H100/Show-o1.3B512²；两阶段个性化SFT各15epochs/K16/M8/理解b4生成b1；RL G9/b1/100steps/lr1e-6/β.01/CFG5/gradnorm1/αtext.4/αimage.6/TPR.25/μ.12/η.8/eps0=2，两路1:1；代码50图像步/10步代理点、AdamW(.9,.999)/wd1e-3/eps1e-8，PPOepsilon.2且logratio截[-10,10]。代码DGS mask重采样噪声温度1.8，对照默认1.0；这不是logits softmax温度，配置差异仍需控制。公开README默认3GPU/G9、另1GPU/G3；其分组要求G可被卡数整除，不能直接套论文8GPU/G9。GPUh/完整seed/训练重复和CI、全部++split/裁判快照、实际正式训练版本及完整奖励专家待补；本轮未执行训练或模型推理。

## 主结果

实际T1 UniCTokens→Sync：Rec .792→.859，Rea BLEU .238→.250，DenseRea .385→.503；VQA BLEU/GPT .505/.521→.592/.606，QA .546/.601→.604/.652。PureGen CLIP-T/I .280/.750→.308/.765；DenseGen GPT/I .298/.639→.337/.645；ReaGen T/I .282/.762→.324/.801；DenseReaGen GPT/I .317/.712→.353/.756。这是该前作配置的点估计改进；YoLLaVA/MC/RAP等专用模型在若干理解列更高。T5 DreamBench .788/.299→.808/.323，YoLLaVA CLIP-I .806→.822；YoChameleon DreamBench .807，3000图DreamBooth .815，不能称所有基线全面更优。正文14.1%/10.0%/8.8%等汇总未说明与具体列的聚合关系；逐列报告原分，避免照抄。F5左横轴wallclock分钟，达到无DGS基线峰值98%约1.9x更快，图为reward非外部测试质量；红曲线后段回落，未给完整计时分项/多seed数，不能当每步吞吐2x或全训练任务加速保证。

## 消融和实际图

T2 full多数列胜去理解环/视觉路/文字路/无DGS，但无DGS QA-BLEU .607高于full .604、PureGen CLIP-I .766高于.765；去视觉路PureGen .759，去文字路.757。T6全四奖励Rea BLEU .250低于去FER三奖励.252，TIER+DER VQA-BLEU .593高于full.592，因此总体最好须明确聚合/统计。T3 Joint→Joint+Sync-GRPO Rec .712→.789/DenseRea .387→.468/DenseReaGenGPT .288→.322，但低于正式初始化Sync .859/.503/.353，且Joint+RL CLIP-I PureGen .695显著低于UniCTokens.750；可支持不同个性化初始化上RL有益，不能支持完全免SFT冷启动或任意初始化均SOTA。F1/4/6/7/8为静态概念属性和密集提示例图，未有视频/笔顺证据；F5右阈值约.5→.65，PR接近.25，经验曲线不解决公式和源码控制规则差异。

## 局限、理论及源码问题

论文未单列Limitations，主要边界需主动补齐。理论D1把组内随机均值当常数，iid下Var(Ri−Rbar)=(1−1/G)σ²，且组内协方差/score与A独立等假设未实证；D2声称top-p正态截断Var≤p对所有p≤.5不成立（p=.1精确约.169135>.1；默认.25约.241636仍小于.25，不能反过来说默认点已被反例否定）。D3奖励均值增大不推出梯度均值范数增大，SNR严格提升未由此证得。D4忽略趋势项的幂控制线性化漏lnT*，0<T*<1时局部系数大于1；完整带eps0=2切换趋势系统需另行分析，不能从简化式推出稳定或断言完整系统总发散。公开代码CLIP评分器名称/参数/方法接口与grpo导入调用不匹配；DGS接受后的续算遗漏必填input_ids，且保存preview时将所有位置填满而未保留正常remask状态，无法直接视为等价续算；这些是静态源码证据，未运行复现错误。四奖励未完整发布、外部API抽取和评分、单卡示例的src1广播、G/卡数整除和split版本均限制可复现性；没有seed区间，无法以小差异证明普适协同。 Eq30另称||s−y||₂≤2，但未限制属性段数及余弦向量范数，例如5维s=0、y=1时范数√5>2、R=1−√5/2<0；不能保证TIER始终落[0,1]。修正可按实际维数和允许范围归一或裁剪，但会改变奖励，需重新验证；本轮未擅自替作者改公式。

## 优势成立的条件

已有少样本概念身份与额外知识、隐含属性需要转换成显式生成条件、早期代理与终端真实质量正相关时，联合反馈与选择性完成可能提高个性化属性实现率。在联合正态/固定阈值等假设下，选中reward方差可由精确截断式降低；要推出梯度SNR还需score分布和协方差不变/受控，而筛选通常改变它们。固定接受G、过检率p、代理占步比f的期望生成前向成本为GT[1+f(1/p−1)]，p=.25/f=.2为1.6GT，尚未算奖励；固定提议N相比全做完则比值f+(1−f)p=.4，两个预算口径不同。1.9x达到目标时间可以与前者并存，但需更少优化步等证据；不能宣称筛选在等G下天然节省采样FLOPs。静态语义/身份收益对多语文字、细笔拓扑和时序书写无直接外推保证。

## 可证伪验证

先锁正式++split/奖励专家/初始化、修复并报告公开接口和DGS续算；同基座等数据/外部API/总GPUh做SFT、image-only RL、文字-only RL、真正jointIR+image、改写器、BestN及DGS析因，两路1:1及α与奖励权重分开。DGS同时给等G、等N、等总时间三口径，逐项计代理/奖励/拒绝/续算/反传时间，控制mask温度，报告ρ、每类false reject、校准和外部测试/身份/多样性曲线；验证真实梯度均值/协方差而非仅reward方差。固定规范终图配正序/反序/重复漏笔RGB视频，加入多语言细笔和遮挡、字符/事件/执行oracle；比较规则SVG、强分离生成识别和共享UMM。理论用精确截断正态式及含score协方差推导；控制器用完整含趋势的分段系统与同阈值反事实，不用reward均值替代梯度。以上为待执行方案。

## 研究组织与写作学习

可学习Introduction从个性化隐含知识失败→显式推理桥→联合奖励→候选成本与DGS逐步建立需求，Method按轨迹概率/目标/筛选组织，AppB用具体斜体示例说明训练评测。Claim应分别写前作匹配点估计、跨预算经验加速与未充分证明的机制；Dense指语义密集，fewshot/persona不等书写时序。Limitations应补身份/属性分布、原++发布、裁判误差、初始化及正式-公开实现差异。Dr.GRPO原文2503.20783v2§3.1–3.2已定向追读，去std和响应长度归一属于既有方法，其固定MAX_TOKENS只是全局尺度，不等于没有任何归一；该论文尚未全篇三遍，不新增核心完成数。

## 实际阅读范围

arxiv2605.10445v1完整23页4098853bytes；Abstract/§1–5全文、AppA–G全部研究文字、T1–6/Eq1–34/F1–8及图注；实际PDFp2/3/4/5/6/7/8/9/14/15/17/18/19/20/21/22/23共17页核看全部框架/结果表/消融/主要理论与定性。参考文献用于定位追引，未逐篇独立读。官方GH9ca4254完整122项树、root/sync README、完整grpo训练控制路径和train入口/初始化/优化、config、clip_eval接口与utils BLEU，pdata/ref_model/requirements按依赖定向读；未声称底层全库逐行读。当前固定版本grpo/train已重新获取，确认此前缓存文本一致。HF332df6e卡片/元数据/树已核，zip内部Range长度异常停止，未读内部数据/下载权重。DrGRPOv2§3.1–3.2定向原文追读，不计全篇。未训练/推理/独立复现。

## 理论核算：限定结论

令p为固定阈值事件的真实通过概率，z=Φ⁻¹(1−p)、λ=φ(z)/p，标准正态尾部的精确方差为v(p)=1+zλ−λ²。在正文联合正态假设下，Var(R|Rtilde>T)=σ²[(1−ρ²)+ρ²v(p)]。p=.1时v=.1691351693>.1，足以否定“所有p≤.5均有v≤p”；p=.25时v=.2416369622<.25，不能据此否定默认点的数值界。随机停止下的G/N是通过率估计，不能无条件替代固定事件概率。

如果组均值来自同一批iid奖励，Var(Ri−Rbar)=(1−1/G)σ²，i≠j时Cov(Ai,Aj)=−σ²/G。逐token求和的总梯度还依赖不同token/样本间协方差与策略score，而DGS会改变这些分布。奖励提高或奖励方差降低均不足以单独证明其声明的梯度SNR界。

忽略趋势切换项、设x=lnT−lnT*，正确一阶项为x_next≈[1−μ f(T*)T*lnT*]x。对0<T*<1和μf>0，其系数大于1；原Eq29漏掉lnT*。完整Eq7包含μ−eps0·indicator与趋势状态，eps0=2大于μ=.12，切换可反号，需完整分段系统分析。公开代码采用TPR−PR、每次±.005且小于阈值差时不更新，未实现该趋势系统。

Eq30的奖励范围同样需要维数条件；没有该条件时，不能直接假定所有专家的加权总分处于[0,1]。这些是公式审查与闭式计算，未进行模型实验。

## 公开代码对照

| 位置（固定9ca4254） | 可核事实 | 影响及边界 |
| --- | --- | --- |
| grpo.py:21、430；clip_eval.py:122、125、142 | 导入/调用SHOWO_P_CLIPEvaluator；文件实际导出SHOWOConceptClipEvaluator，构造和评分方法也已变更 | 当前cleaned文件接口不一致；未运行或声称复现错误日志 |
| grpo.py:256、758–763 | _run_maskgit_rollout的input_ids为必填，接受后的state续算调用未传该参数 | 公开DGS路径有静态调用错误 |
| grpo.py:332–345 | 将preview所有图码位置填满后存为续算input_ids；未保留正常remask状态 | 即使补参数，也不能直接称与未中断MaskGIT等价 |
| grpo.py:809–815、1090–1138 | old/current/ref轨迹logp仅收集图像去掩码步；clip和参考KL存在 | 缺直接IR文字动作loss；共享参数仍可间接受影响，不能称理解参数完全不更新 |
| grpo.py:1016、1068；README单卡示例 | 无条件从rank1广播；分组要求G可整除卡数 | 单卡示例及论文8GPU/G9不能按当前默认直接复现 |
| grpo.py:490–492 | 从test目录提示前半选训练条目 | 按具体条目匹配论文斜体split；目录名不足以判数据泄漏 |
| README§7及实际奖励段 | 完整专家部署仍待发布；cleaned路径CLIP/人脸/API/BLEU | 不能把替代评分实现记录为已发布四专家正式协议 |

以上只审查公开版本，无法据此断言作者实际用于论文表格的私有训练代码采用相同错误。

## 与书写、绘画及下一步调研的关系

可迁移的问题是：隐含个性化属性如何变成显式条件、早期代理怎样影响候选分布、如何证实共享模型比强分离基线更有效。CLIP/人脸与静态GPT分不能判定汉字笔顺、绘画事件或真实执行；还需同终图反序、漏笔、形近字及多语种等独立控制。

本篇反向追引定位UniCTokens2505.14671、YoChameleon2504.20998、PEARL2603.20422和DrGRPO2503.20783；后者本轮仅定向读§3.1–3.2，其余未全篇读，不计核心完成。后续补前作正式版本及数据构建，再继续未完成的STBridge、SUDER、基准/语料与中文笔画记录。既有扩散/flow/视频/绘画与非论文资源审查继续保留并按公开协议补缺。
