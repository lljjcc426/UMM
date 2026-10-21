# 尚需精读与原始来源追引：可操作队列

第二轮已补VideoSketcher方法/主表/消融、DiffInk及部分UMM和基础理论，见[334份笔记](../reviews/README.md)。截至2026-10-20全部334条的逐条缺项以[阅读台账](reading_ledger_2026-10-19.md)为准；下表保留专题追引和代码复核任务。

本队列维护“文献/研究找到了”与“已完整精读”之间的差别；不表示后台任务正在执行。2026-10-19 保存到 GitHub 便于逐次人工/模型核验。

## 优先级 P0｜威胁研究新颖性的直接前作

| 原始研究 | 已知可靠范围 | 下一次精读动作 |
| --- | --- | --- |
| [Calligraphy Bench](https://github.com/haizelabs/calligraphy) | 88 字中文书法 tool-agent、order 指标，HF 有 SVG/medians | 获取 judge 实现或联系作者；验证相同终态不同动作是否可识别；查合法地区书体 |
| [VideoSketcher](https://github.com/rhfeiyang/VideoSketcher) | Wan2.1 + two-stage LoRA + AR，官方脚本 | 主表/方法/消融已读，见L010新笔记；仍需逐图、完整附录训练条件、train.py及AR实现核查 |
| [BCSS / Stroke-Seg](https://github.com/Rvosuke/BCSS) | 静态 per-stroke mask 与规模，HF subset 与论文规模不同 | 出版社方法/主表与HF及示例源码已复核，见L184/S007/S016；保留10类vs6类、14766 vs10653笔画等差异。后续取样解码和完整训练协议复核 |
| [Wuji Writing VAM](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819) | 数字机器人多视角视频+动作，配置/日志 | 校核训练配置/模型结构；动作流如何编码书写轨迹；独立部署真值/许可证 |
| [VidScribe](https://arxiv.org/abs/2609.36598) | 803 条视频文字基准，A1/A2 与 T2V/R2V/I2V/V2V | 审计评判器与混淆矩阵；设计 strict temporal order 反例 |
| [VTR-Bench](https://arxiv.org/abs/2610.01499) | 视频中文字 OCR/条件评价与多候选反馈 | 精核视频采样、WER 计算、预算控制及流程成本 |
| [OnOff Handwriting](https://arxiv.org/abs/2608.03198) | 轨迹+接触+近似物理墨迹渲染 | 增强是否改变原始 stroke 实例；跨风格规范与逐笔定量 |
| [DiffInk](https://arxiv.org/abs/2509.23624) | InkVAE/InkDiT、少步生成曲线 | 固定采样+评测协议，重查数据切分和额外控制变量 |

## P1｜跨领域生成/理解方法与强基线

- [TextDiffuser—NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/1df4afb0b4ebf492a41218ce16b6d8df-Abstract-Conference.html)、[GlyphControl—NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8951bbdcf234132bcce680825e7cb354-Abstract-Conference.html)：须全文阅读结构图、数据集、对比表及消融，理解显式 glyph/layout 约束在新任务内可能消失的收益。
- [VidSketch](https://arxiv.org/abs/2502.01101)、[MoSketch (ICCV2025)](https://github.com/jyliu-98/MoSketch)、[SketchEdit (IJCAI2024)](https://github.com/CMACH508/SketchEdit)、[DiffStroke](https://github.com/CMACH508/DiffStroke)：前三类分别是草图条件视频、对象动画、笔画编辑，不可都叫“笔顺视频”；逐篇抽表再做机理迁移。
- [SceneDAPR](https://github.com/DSAIL-SKKU/SceneDAPR)、[Quick Draw dataset](https://github.com/googlecreativelab/quickdraw-dataset)、[ark60 Sketch Diffusion](https://github.com/ark60/sketch-diffusion)：确认真实 stroke event 和 timestamp 与模型生成时间的区别。
- UMM 架构组：Transfusion、Janus、Chameleon、BAGEL、Lance、UniVideo、Show-o2；逐项核参数共享、视觉 tokenizer、损失/训练策略、官方可用视频生成接口及显存需求。研究问题核心是**协同有无**, 不能以同一程序调用多模型代替可证协同。
- 经典理论：DDPM（Ho 等）、latent diffusion（Rombach 等）、Flow Matching（Lipman 等）、rectified flow、LoRA、DoRA、RSLoRA；讲解服务具体公式与控制训练，而非无限扩展阅读偏题。

## P2｜语言/地域、训练工程与无论文材料

- [Ketaba](https://github.com/HasanBGit/Ketaba-OCR-LoRA)、[Qari](https://github.com/HasanBGit/QARI-OCR-LoRA) 与 [HF CASIA-HWDB2-line](https://huggingface.co/datasets/Teklia/CASIA-HWDB2-line)：核模型标识、任务接口、实际数据、CER 定义及领域泛化；OCR 不能为视频执行作直接 baseline。
- [AnimCJK](https://github.com/parsimonhi/animCJK)、[KanjiVG](https://github.com/KanjiVG/kanjivg)、[Make Me a Hanzi](https://github.com/skishore/makemeahanzi)：逐规范比较简体/繁体/日文有序笔画、许可和字形对应。
- 继续检查 Hugging Face 上“writing, brush, handwriting, stroke, calligraphy, pen trajectory, LoRA, I2V, robotic writing”，将找到的模型按语料/模型类型/可复现性建卡，并定期排除空模型卡和被重命名复制的条目。

## 所有逐篇笔记的最低完成门槛

(1) 研究问题和动机两分钟讲清；(2) 画出输入→主要模块→输出并解释公式与新组件；(3) 原表复现主指标口径并列至少一个实际 baseline；(4) 至少一组消融支持某个 claim；(5) 至少两个源自数据/失败样本/Related Work 的可检验质疑。数据集、模型结构、训练条件、优化器、NFE/seed、硬件、预算、限制必须分字段记录。不满足的字段标为待核，严禁填经验推测。

**停止/排除规则：**与目标无直接因果连接的研究可作领域背景；正式增量目录登记时区分 paper、benchmark、dataset、model_card 和 code_release；同论文多制品可保留多卡，但不能将它们计为多个独立论文。

## 本批存量复核后的追引补充

已完成相关章节阅读的23项是A04/A08/A11、L001/X01、L012/L014/L015/L016、F02/F03/F04、D01–D04/D06–D08、E02/E04/E06/E07；完整验收缺项仍见各笔记。

检索时又发现以下直接来源，登记为**候选，尚未完成原文精读**，本批不放进正式独立论文计数：

| 来源 | 相关性与下一步 |
| --- | --- |
| [Edit Flows，NeurIPS2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cb43f46154e750746602faaffd65fbbb-Abstract-Conference.html) | 可变长度离散序列编辑；对笔画增删和事件长度建模相关，需核方法/采样/实验 |
| [Discrete Guidance Matching，ICLR2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f0470962fc538827f3130757fb707b71-Abstract-Conference.html) | 离散flow指导率；追查与E04及多模态离散生成的关系，不能仅用题名推导效果 |
| [2D Gaussian Splatting for Bézier Spline Line Art Vectorization，Disney Research2026](https://studios.disneyresearch.com/2026/07/16/2d-gaussian-splatting-for-bezier-spline-line-art-vectorization/) | 与F02相关的最新矢量化工作；核工具/表示/复杂交叉线与时间事件适用性 |
| [Windfoil，arXiv2610.02468](https://arxiv.org/abs/2610.02468) | 可微矢量覆盖与渲染效率；需核与DiffVG/F02的比较条件及闭合/开放曲线限制 |

[CoFRIDA-Sharpie模型制品](../resources/cofrida_sharpie_card.md)已单独登记H001并关联F04，基础模型字段冲突待官方配置/代码进一步解决。DiffVG主PDF约17 MB，本批两次直接下载未完成，保留项目页可读事实，不将其升级为全文已读。

## 第三批之后的具体缺项

本批再读19项：B01/B03/B09、L004/L005/L009/L018/L019/L046–L050、C01/C03–C07。仍需完成各笔记标注的附录、图像、版本和代码核对，不能从相关章节阅读升级成完整三遍精读。

- InkDiffuser：取得完整PDF视觉核对、作者实际训练配置与缺导入模块解释；代码快照已记录。
- DiffMath：确认正文/附录冲突的VAE与DiT参数；核轨迹顺序、测试词表与独立OCR。
- 女书：核视频制品及其是否为Smartpen回放，字符表覆盖和字体/作者泛化；397字录制未被论文用于生成器训练。
- UMM：继续L057–L174的架构、tokenizer、协同训练与评价，优先L139/L140受控梯度研究及L067–L070跨任务协同基准。

## 第四批之后

本批新增L139/L140、L067–L070、R01–R05、F05、L007/L008、L023/L024、L029–L031及5项仅第一遍A06/L002/L006/L021/L022。主目录仍有137条历史原文待复核，40条摘要记录中也有需要精读的条目。

待取得的全文包括A06机器人笔顺恢复、DiffWriter(L002)、Frequency-Guided(L006)和两篇OpenReview投稿L021/L022。不能用后续论文对它们的转述填成原文已读。L020正式ICLR论文PDF下载中。

新增追引线索（尚未完成全文阅读）：
- *A survey of handwriting synthesis from 2019 to 2024: A comprehensive review*，Pattern Recognition162(2025)111357；需核出版社原文、参考文献与本目录差集。
- *From pixels to strokes: A survey on generative handwriting*，IJDAR2026，DOI10.1007/s10032-026-00609-2；需核任务分类及参考列表。
- *Hierarchical offline-to-online Chinese handwriting trajectory reconstruction via dual-domain priors*，DOI10.1007/s44443-026-01050-5；需核与L006的任务、数据和方法关系。
- *Template-Guided Cascaded Diffusion…*，ICDAR2025，DOI10.1007/978-3-032-04614-7_9；是否与L021投稿有版本关系待查，暂不合并。
- [CursiveTransformer作者实现介绍](https://greydanus.github.io/2025/03/30/cursive-transformer/)；需读取训练代码、数据、采样配置和授权。
- [Inkspire作者项目](https://dlin.org/inkspire)，arXiv:2501.18588：草图协作交互线索，须与同名手写生成工作区分。

## 第五批之后

新增F01、L020/L025/L027、L034–L043、L045、L051–L054、L182/L183共21份笔记。DiffVG、InkSpire全文下载问题已解决，前面日志保留当时访问快照。L020已核正式ICLR2026正文、指定附录、框架图及五项书面检查；代码和未读附录仍列缺项。主目录330条，历史原文待复核118条。完整三遍验收继续进行。

新增引文追踪线索，以下仍为待读候选，未计入正式独立论文数：

| 来源 | 下一步 |
| --- | --- |
| AniClipart（CVPR2025） | 从L052参考文献追查；读取动态矢量目标、骨骼/ARAP约束、SDS优化预算，检查与固定字形运动基线的信息条件 |
| [LiveSVG](https://levymsn.github.io/LiveSVG/)，arXiv2605.30174 | 原始SVG拟合视频教师的两阶段动画；核拓扑、遮挡、可编辑性与运动评价 |
| [VitaGlyph](https://arxiv.org/abs/2410.01738)，WACV2026 | 核“双分支”的实际输入输出及静态/动画属性，不能由Vitalizing题名推断时间生成 |
| DSFusion；Differentiable Variable Fonts | 来自艺术字体相关工作；定位正式论文及数据/实现，去重后再登记，不能从他文比较结果补成原文已读 |

## 第六批之后

C02/L032/L033/L055/L056/L061/L094/N10/N11/N12/N14/E03/E05/L180/L181已新增结构化章节分析，G027已补正式正文/实验；其余未读附录/完整代码仍以笔记为准。优先继续L057–L174其余统一架构、离散/连续扩散、数据、协同训练和综合评价，以及S资源的模型卡/配置/数据实际字段。

新追引候选（未完成全文，不计新增正式论文）：[Evaluating the design space of diffusion-based generative models，NeurIPS2024/arXiv2406.12839](https://arxiv.org/abs/2406.12839)、[Boosting Continuous Control with Consistency Policy，AAMAS2024](https://aamas.csc.liv.ac.uk/Proceedings/aamas2024/pdfs/p334.pdf)。前者可检验EDM设计选择的适用条件；后者与RSS Consistency Policy题名相近但属另一工作，禁止混合实验。L181的Related Work另有2020双向读写/RCN/TAN等，应继续逐项去重追引。

## 第七批之后

R06/R07/N07、S007–S016与新补L184已写结构化笔记。剩余110条历史和33条摘要、此前全部未读附录/代码/三遍检查继续执行；资源查证不自动减少论文历史积压。S002/S003静态文字扩散、S004论文(不混S015实现)与S001 Ketaba正式论文需继续补齐；SceneDAPR对应WWW论文需正式去重和全文精读。BCSS论文十类/11维和HF六类/七值、14766与10653计数冲突需取得加工映射或勘误；暂不替作者选择。OpenHandWrite原始采集包/第二大表与全部统计附录尚未读完。

第九批已读早期架构及MetaQueries；剩余96条历史及33条摘要仍按逐条台账继续，已有相关章节分析的记录也需逐图、未读表格/附录和完整理解验收，不能只按记录数结项。

第十批完成L079–L085相关章节分析；余89条历史、33条摘要及全部未读图表/附录/代码/三遍验收继续。新候选追引：unCLIP/Prior、residual quantization与deformable attention的原始理论需与已有基础笔记去重；冻结扩散loss与score蒸馏等价条件需进一步推导，不能只照抄论文KL解释。

第十一批完成L086–L093指定章节；余81条历史、33条摘要和全部未读图表/附录/代码/三遍验收继续。MetaMorph AppD两行重复200K标记、JanusFlow阶段分布、UGen k极限解释和Harmon去mask数量的符号需核实现/正式补充；不提前定性代码错误。

第十二批完成L095–L100及新增DDPO/L185，余75条历史、33条摘要和未完成图表/附录/代码/三遍验收继续。追引需覆盖DPOK、D3PO、DDPO后续偏好优化与真实轨迹RL；先按arXiv/正式题录去重再核原文。QLIP下游UM³的实际视觉码词表/分解head、DualToken正式全文403和UniToken最终StageIII对应公开制品仍待核。

## 第十三批之后

L101–L108已读指定章节并保留未核字段，新增8份笔记，累计218份。历史待复核67条，摘要33条，全部附录/逐图/代码及完整验收继续按逐条台账完成。EvoTok残差深度不作为书写时间，UniCom最终解码依赖VAE；新候选需先去重与读取原文。

## 第十四批后队列

L109–L116已形成指定章节分析；历史待复核59条、摘要33条、5份笔记仅第一遍，剩余字段以台账为准。新增追引候选：[HT-GRPO/Sketch Then Paint](https://arxiv.org/abs/2605.16842)、[dMLLM-TTS](https://arxiv.org/abs/2512.19433)，由Lumina官方README发现。ht_grpo子目录写code/report soon，但根README已链接正式arXiv，不能归类无论文，也不能把sketch/paint隐喻认作真实绘画视频；原文尚待读取/去重入主目录。

## 第十五批后续

当前历史待复核52条，摘要级33条、5份firstpass和其余笔记图/公式/全部条件也需继续补。BLIP3o-NEXT2510.15857已有主目录关联则沿用ID；TMP2606.27089已有论文，不能归无论文资源；Mobile-O导出精度/内存口径待实际Swift/CoreML复核。下一组L123–L126开放模型/长视频训练，随后协同优化、基准、交错图文与数据。

## 第十六批后续

历史待复核47条；下一组协同优化与RL的L127–L138，随后评价基准、交错多模态和训练数据。33条摘要级和5份firstpass尚需升级，全部笔记也需继续补完整图表/附录/验收。UniFlow正文/附录batch冲突、InternVL-U数据交叉、Mamoda2.5权重发布、SenseNova OCR奖励粒度、Rosetta实际旧任务梯度/内存协议均保留待核。

## 第十七批后续

历史待复核40条；继续L134–L138协同优化，再评价、全模态、具身与交错数据。HermesFlow正式版25页仅指定主文/表/推导已核；PairUni BAGEL为SFT，Lumina为初步RL实现，不能混为全架构PairGRPO。GvU环境锁PEFT0.17.1及上下文定义已核，裸调用不进入禁用上下文，仍需完整实际运行链核查；UniCorn理论缺边缘化，需补其代码/完整附录。33条摘要级及完整验收仍待完成。

## 第十八批后续

历史待复核35条。继续L141–L156评价/数据/长序列、L157–L174全模态/具身/交错数据及L057综述；33条摘要级、5条第一遍笔记和全部完整三遍验收仍待完成。LVRPO架构/算法口径、ParetoLoRA实际系数与阈值、STBridge数据来源/共享参数冻结范围、SyncR1完整奖励和rollout似然继续审查。

## 第十九批后续

历史待复核29条：L057、L147–L174。继续评价/数据/交错长序列、全模态和具身；另33条摘要级、5条第一遍及完整三遍验收仍待完成。UniKE全答案与locality、MME-Unify跨表计数/归一实际实现、GENIUS干预配置、SGU不同接口和理论条件继续核。

## 第二十批后续

历史待复核22条：L057、L154–L174。随后须升级33条摘要和5条第一遍，并继续完整三遍验收。资源侧需要实际发布数据计数、ImgEdit混合judge/训练权重、OneIG文字清洗/分词/并列秩规则及编码器训练配置；不能因有论文就省略发布制品核查。GenExam/GRADE/DisciplineGen需追引去重后扩展。

## 第二十一批后续

历史待核15项：L057、L161–L174；随后补33条摘要及5份第一遍，继续全部三遍验收。需核UniLongGen裁判版本/全historyprobe成本、长程新作训练超参与scene预算、ChatUMM专门多轮量化、Ming-Lite-Uni和MingFlash各版本制品；候选先去重再增。

## 第二十二批后续

剩余历史待核L161–L168八项；其后继续33条摘要、5份第一遍及全体三遍验收。CoMM图像coherence印刷公式的归一与实现、ShareGPT4o 91K/92K及原图比例、OmniCorpus评测OCR输入和分语言质量继续待核。新候选CI-VID/OpenING/COHERENCE需去重，不凭搜索标题写分析。

## 第二十三批后续

历史未重新核查标记清零；下一步逐项补33条摘要和5份第一遍，再补各笔记sections_read明确的未读段与5项检查。核心问题：WorldBagel定理4与相位分支，MUNI总体风险/先验排序假设与pair数据，SenseNova50K/200K配置，Puffin自评camera偏差。新增候选继续去重，不以完成存量初核声称全领域覆盖完成。

## 第二十四批后续

剩25条摘要：A06/L002/L003/L006/L021/L022/U13–U16/U19–U31/S002/S003；其中5份第一遍继续补合法全文。WriteLikeYou已找到并下载北大作者公开PDF，待读。新候选Visual-OPSD（2606.18974）质疑ThinkMorph视觉thought的因果作用，需读原文和源码、查同任务/版本后再关联，不能直接将其结论当本次确认。继续补每份笔记的未读章节与书面检查。

## 第二十五批后续

剩17条摘要：A06/L002/L006/L021/L022和U20–U31。其中五份仍第一遍，L003取得合法作者全文并核核心，补充材料待读；前述北大稿“待读”的历史描述以本批为准。U20–31已定位固定版本，下载不计阅读。新增待去重/全文候选：CVPR2026 Qin等Towards Human-Like Robot Handwriting via Contour-Aware Generation（31597–31607）；Wang等Hierarchical offline-to-online Chinese handwriting trajectory reconstruction via dual-domain priors，DOI10.1007/s44443-026-01050-5，正式页2026-08-21。已看后者摘要及所示方法/数据段，主表和完整公式待审，未加正式计数或宣称创新已排除。继续补301笔记未读范围和其余书面验收。

## 第二十六批后续

剩11条摘要：A06/L002/L006/L021/L022和U26–U31。六篇可用PDF已下载，待读；其余五份合法全文仍受限。U20/U24补五项书面检查，但各笔记明确未全读附录/代码；完整三遍未计完成。GHTR和HierarchicalO2O两候选正在取得原文，先去重再补主目录；UEval的art属于步骤图生成评测，后续绘画检索需关联这一明确前史。

## 第二十七批后续

剩五条摘要A06/L002/L006/L021/L022均涉及全文访问限制，不能用相关新论文替代它们。316笔记中的完整附录/代码/理解验收还需逐项补。新增L186补充zip/机器人控制链与发布数据尚未核，GitHub固定树只有README；N08时间采样/先验bank隔离和全部训练λ待核。U28论文公式与可训练代码代理要做完整路径比对，U31表间分数冲突、U26 SFT比例含义待核。R08已核HF卡、文件与加载逻辑，未读权重tensor，不把基础模型分数赋给适配器。

## 第二十八批后的继续队列

本轮尚无独立17字段笔记的九项为L026 UniVideo、L028 Lance、L044 Calligraphy Bench、L175 XMP-Font、L176 LVLM在线笔迹表示、L177 PaintFlow、L179 UMText、S004 VidSketch、H001 CoFRIDA-Sharpie。五条受全文访问约束的摘要仍为A06/L002/L006/L021/L022。其余325份笔记未完成的附录/图/代码/全部三遍验收也继续；新候选发现和无论文资源检索尚需扩展，不能把统一模板补齐等同调研零遗漏。

## 第二十九批后的继续队列

九份缺失的独立笔记已补，当前334条均有笔记。五条摘要仍为A06/L002/L006/L021/L022。下一阶段按各笔记明确列出的缺项补读图表/附录/训练和评价源码、核版本差异并做五项理解检查，继续扩展新文献和真正无独立论文的资源。UniVideo v4训练数据/算力细项、Lance总参数及完整训练路径、UMText正式PDF技术差异与RCI梯度、PaintFlow正式接收/实际lambda训练、VidSketch论文实验所用自适应入口、Calligraphy Bench计数差异对judge的具体影响仍待，不将待测问题写成已证实错误。


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


第九十五批追引待精读：AutoConverter/VMCBench（CVPR2025，官方摘要9018题）及ObjectMLLM（ICCV2025，六视频QA/有公开代码模型），见本批审查末尾的官方入口。已确认主目录尚无这两标题；待完整原文/制品核查后补录，不算已完成核心。


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
