# MUNI：完整附录与成对数据可识别性审查

第二百一十一批完成[L164](../reviews/L164.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/muni_full_appendix_and_pairwise_identifiability_audit_2026-10-25.json)。358目录（331论文／研究、27资源），316核心/321书面含未通过项；待完成核心深审15篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2606.16408)、[主源2](https://arxiv.org/pdf/2606.16408v1)、[主源3](https://arxiv.org/html/2606.16408v1)、[主源4](https://muni-proj.github.io/)。

## 研究问题

共享随机latent如何同时支持任意子集条件生成与无条件图文音联合采样，并保留跨模态依赖、避免把私有细节全塞进共享表示？

## 现有不足

单专家混合可忽略部分输入；对所有小子集latent训练prior可能丢失缺失模态之间的相关；自重建会鼓励私有信息。作者用三项信息条件指导路由，理论仅在额外可实现/优化/排序假设下成立。

## 贡献

在UL联合训练latent框架上扩展多模态，用非混合PoE/Hellinger、目标expert stop-gradient及full/leave-one-out prior路由。定义coherence TC=0、predictivity条件互信息=0、minimality最小I；AppB给条件性命题与证明。聚合规则本身沿用已有方法，贡献重点在联合目标和路由设计。

## 输入、模块、输出与公式

图/文/音任意观测子集→缺失模态，空集→三模态共生成；另Poly三图+digit/quadrant共5模态、Gaussian3模态。没有视频、字符笔画、接触事件或规范笔顺监督。

## 模型结构

Eq1–12定义factorized stochastic decoders及subset posterior。Eq11目标expert在forward保留、backward detached，其他expert仍接收该目标梯度；Eq12 prior仅|A|≥M−1。图文音实际在预训练CLIP/CLAP/EmbeddingGemma语义空间上学习MLP enc/prior/heads，StableUnCLIP/AudioLDM负责后续图音，Gemma3-1B LoRA r16/α32/drop.05解码文字。引言不依赖text-aligned space应按框架能力理解，实际实验确用了CLIP/CLAP，不能写成完全无文字对齐先验或全部像素端到端从零训练。Poly latent32/ResNet/NCSN++；toy latent48，MMVAE+额外24/Poly额外32私有维，容量并非逐参数完全相等。

## 数据分布与划分

Poly220Ktrain/10Ktest，对齐三图digit/quadrant。toy1e6随机64成分Gaussian混合，7独立因子：全共享10、三个pair各10、三个private各20，每模态50维。真实训练仅272K图文(242KLAIONCOCO aesthetic>5+30KFlickr)、91KAudioCapsv2文音、184KVGGSound音图，无真实triplet；多条件test以AudioCaps测试文音经FLUX1dev造图。独立pair边缘一般不唯一确定高阶joint，例如三二元变量偶校验与独立分布有相同两两边缘；这是本仓库数学反例，未运行模型。AppB总体完整joint风险到pair训练的可识别性未另证。

## 指标与评价协议

Poly full10K冻结verifier标签正确/多标签同时正确，uncond三图与两标签严格一致；toy N20K/task、128投影SWD边缘保真+共享坐标MSE一致。真实图FID/音FAD/文CIDEr，CLIP/CLAP/AIS两两嵌入相似；两两score不等于三元分布或文字精确性正确。真实task样本数/全部prior与音频NFE未全给，缺CI/多seed。

## 对比方法

同backbone与预算重训MVAE/MMVAE/MoPoE/HELVAE，toy和Poly加MMVAE+/ShaLa(改flowdecoder)；图文音排除需完整triplet的MVAE/HELVAE。CoDi/OmniFlow/FlowBind为异构generalist；UnifiedIO2L灰色reference不支持A↔I，六专用模型为reference，不属等预训/总compute比较。

## 实验条件和发布边界

T7 AdamWβ.9/.95/wd0/clip1/constantLR+5epochwarm/EMA.999；toy4e-3/200epoch/b4000/约10min，Poly6e-4/300/b1024/约3h，真实4e-4/200/b1024/约3h，单RTXPRO6000均作者报告，不含继承底座预训/完整调参。encoderpriorγ .1/.1/.01，ShaLa toy.01。toy prior/decoder各50步，Poly prior50/decoder25；真实图Euler25/CFG4、文greedy。真实text CE仅有效batch1024首64例、权重.05并加768维表示alignment，imageFM/audioMSE，cross:prior路线3:2。Eq12β与独立wA完整数值/实际pair缺失路由细节未充分列；γ与β不可直接同名。

## 主结果

T2/6 Poly joint .9346>MoPoE.9283/uncond.4841>HELVAE.4246、扩展ShaLa.4539；digit .9131低于HELVAE.9297/MMVAE+.9368。T3六项由MUNI与†合并取best，单一模型未全胜；MoPoE(I+A)→T CLIP27.81>MUNI†27.60/(T+I)→A CLAP30.96>30.16，主文best限定generalists。T4†26.74/24.83/82.80 vs Omni21.17/14.23/50.95，MUNI自身TI26.76略优†。T8†FID14.40好于FlowBind20.13，但ITCIDEr58.31<Unified91.36/MoPoE59.74，AT47.38<Flow54.41/MoPoE50.34；T9TI29.92<Omni30.76、AT39.45<44.74，IA90.11<MoPoE90.82。所有为作者数。

## 消融及进一步实验

T5可控共享private结构MUNI2→1MSE.0414、SWD.1300、uncondMSE.0394最好，但1→1.0508差于MMVAE.0267；T6增加private与强prior基线支持机制比较，非聚合×detach×priorroute独立全因子消融。MUNI/†只对比聚合；未给β/γ/3:2/首64text抽样/MLP容量或noise多样性充分扫参。T7参数差异与多个目标同时改动，不能把全部差距单因果归stopgrad。

## 局限与疑问

29页11图9表57编号式AppA–F全读。LemmaB1以条件MI与链式TC成立；B2依赖总体风险/理想可优化/可实现最小latent、任何ρ>0有可行降损更新、充分小β以及Eq29先验成本随保留I严格排序。Eq30最大似然示例还需H(Z|X)固定；flow情形把排序作为假设，未普证，不推出实际非凸有限样本保证。各route单独充分也未充分证明所有subset aggregated latent分布与唯一共享prior一致；pair训练没有看到完整三元风险。定性F1–11已实际看过，音频只核波形与caption/接口，未独立聆听/评审原始音质，不以图证明声音一致。项目页无code/model下载链接，未取得对应实现。

## 预期优势条件

在跨模态依赖可由共享随机表示解释、private可由强随机decoder承担、成对语义足够识别任务结构时，目标路由可能改善联合一致和多条件融合。精确字符串、异步时序/笔顺，以及只有高阶依赖的分布不由现有图音语义分数保证。

## 可证伪实验

固定预训/数据/预算做aggregation×detach×priorroute因子，扫β/γ和text CE抽样，报质量/多样性/校准CI。构造相同两两边缘不同三元joint(偶校验/独立)及少量真tripletheldout，检验pair可识别边界；公布真实三元专家盲评/高阶关系测试，比较每route latent marginal与prior。数值检验Eq29而非预设；书写场景加可识别却笔顺错、缺笔或文字精确条件。未执行。

## 论文组织与Claim学习

三项准则→失败模式→路由→可控实验结构清楚；定理需把假设与经验分开，框架能力与实际CLIPCLAP空间、总体joint与pair训练写明。合并两个变体的best应显式标注，generalist/同骨干VAE/专用参考各自排序范围清楚，3h不能解释总预训成本。

## 实际阅读范围

arXivv1唯一版本全部29页§1–7、57条references清单及关键关联、SocietalImpacts/Limitations、AppA/A1/B LemmaB1+PropositionB2逐假设逐步/C全部loss推导/D/E1–2/F；Eq1–57、T1–9逐项、F1–11全部视觉，10contact全看并p3框架/p21配置/p22全主辅表放大。官方项目页方法/结果/样例/链接核，无code/model链接；未听原始音频、未运行模型/训练/API/基准。核心三遍五项书面完成，未声称独立复现。

## 理论适用范围

AppB B2证明依赖总体风险、理想容量/优化、可实现的最小latent、充分小β，以及Eq29先验最优成本与保留互信息严格同序。flow损失下该排序被假设；不能扩为有限数据训练保证。

## 数据与评测

图文音只用pair训练，测试triplet的图由FLUX1dev根据AudioCaps文字生成。一般pair边缘不能唯一识别三元joint；偶校验与独立三比特分布具有相同两两边缘，是本仓库给出的数学反例。模型实际使用CLIP/CLAP语义空间，训练约3h不含所有继承底座。

## 结果口径

T3六项最佳由两个聚合变体合并，且限generalist；同骨干MoPoE若干指标更高。T8/9补充了文字CIDEr及部分对齐弱项，保留这些结果才能判断联合一致收益和单向任务代价。
