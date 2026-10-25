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


第一百一十七批（2026-10-22）完成L101 UniWeTok固定v3核心/Eq1–9/33表和七页实际图表，核查BitDance共用代码与HF相关tokenizer制品；区分64位置/128bit、33B位置token/全成本及三个独立SFT变体。357目录，226核心/229书面含未通过项，131条未确认核心（含资源）。见[审查](uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_seventeenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百一十八批（2026-10-22）完成L102 EvoTok固定v1核心/Eq1–11/五表和六页实际图表，核GH独立码本/EMA与训练入口及ECCV官方接收列表；保留表示深度、三项并列与主表/公开配方差异。357目录，227核心/230书面含未通过项，130条未确认核心（含资源）。见[审查](evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_eighteenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百一十九批（2026-10-22）完成L104 UniCom固定v1核心/全部七表和七页实际图表，补原始特征旁路、OCR下降、VAEdecoder与WorldEdit文字/表格冲突；核GH/HF配置和理解入口shape待核项。357目录，228核心/231书面含未通过项，129条未确认核心（含资源）。见[审查](unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[逐文件说明](one_hundred_nineteenth_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十批（2026-10-22）完成L105 Tuna-2固定v2核心/全部六表及八页实际图表，补任务退步、重建额外微调、偏好90.1%和mask/噪声公开默认差异。357目录，229核心/232书面含未通过项，128条未确认核心（含资源）。见[审查](tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_twentieth_changes_2026-10-22.md)。没有删除或模型复现。


第一百二十一批（2026-10-22）完成L106 Representation Forcing固定v4核心/三表含五子消融、AppA–C与六页实际PDF；核VLM-only反例、量化伪代码及AR完整成本。357目录，230核心/233书面含未通过项，127条未确认核心（含资源）。见[审查](representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_first_changes_2026-10-22.md)。没有删除或模型复现。

追引未完成项：Latent Forcing（2602.11401）、REPA、DINOv3（2508.10104）和SwAV。已在本作参考文献/算法关联中定位；除SwAV归一化函数对照外，未作独立完整精读，不计验收数。BitDance/WeTok等既有追引队列保留。


第一百二十二批（2026-10-22）完成L107 HYDRA-X固定v1核心/十三表、AppA–G与十页实际PDF，补视频运动反例、时间压缩/编辑/解码接口和训练比例边界；官方核L107及L103的NeurIPS2026身份。357目录，231核心/234书面含未通过项，126条未确认核心（含资源）。见[审查](hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_second_changes_2026-10-22.md)。没有删除或模型复现。

本批追引定位：AToken（2509.14476）、OmniTokenizer（NeurIPS2024，37:28281–28295）、Beyond Language Modeling（2603.03276，本文简称TransNext）。需用正式标题/ID去重再独立精读，当前不增验收。HYDRA-X OpenReview3mwm6O3FZt及HYDRA sNTc0XTEDc正式版本未对读；已有BitDance/WeTok和RF追引队列保留。


第一百二十三批（2026-10-22）完成L108 PixelUMM固定v1核心/九表八组实验与十页实际PDF，补官方代码/模型卡，记录15.2B总参、F7十一项图像退步、F8条件分层及linearhead发布边界。357目录，232核心/235书面含未通过项，125条未确认核心（含资源）。见[审查](pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_third_changes_2026-10-22.md)。没有删除或模型复现。

本批追引：SenseNova-U1/U1.5、MiniT2I、JiT、PixelDiT、NEO及Cosmos3需按正式标题/ID与现有目录去重后补独立阅读；ViPE2508.10934目前仅核本作参考条目，未独立精读。PixelUMM主生成来源/完整训练预算、F18/F19/F21检查点能力与F7完整编辑定量评测仍待；已有AToken/OmniTokenizer/TransNext等追引保留。


第一百二十四批（2026-10-22）完成L109 FUDOKI正式NeurIPS2025核心/五表/AppA–F及八页实际PDF，补固定GH/HF源码与配置，记录3.86M/3.71M、L2/四次方、32/128/50步差异与纠错对照限制。357目录，233核心/236书面，未确认核心97论文／研究+27资源（资源单独审查）。见[审查](fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_fourth_changes_2026-10-22.md)。没有删除文件或执行模型。

本批追引：[38]Flow Matching with General Discrete Paths（ICLR2025/2412.03487）正式源已定位，D-DiT（CVPR2025/2501.00289）仅核§3纠错，NeuralODE（NeurIPS2018/1806.07366）仅核摘要起源。需去重后独立全篇与制品审查；FUDOKI原训练数据计数、距离/步数版本、GPU与完整配方、judge和maze定量/额外训练仍待。LaViDa-O/LuminaDiMOO等原队列继续。


第一百二十五批（2026-10-22）完成L111 LaViDa-O正式ICLR2026核心/16表/AppA–F及12页实际PDF，补固定GH/HF制品，记录Eq7区间冲突、16/17层边界、ground数据DPG退步和反思质量-延迟条件。357目录，234核心/237书面；未确认核心96论文／研究+27资源（资源单独审）。见[审查](lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_fifth_changes_2026-10-22.md)。没有删除文件或执行模型。

本批追引：LaViDa原理解模型、Sparse-LaViDa（官方CVPR2026代码入口）、LaViDa-R1、Meissonic、Besnier2025/Haltonmask需按正式ID去重后独立阅读。当前仅定位，不算已精读。LaViDa-O Eq7/时间方向、发布16/17层、完整exp实现、T6投影、原训练样本/配方及缺eval_hd.yaml继续待核。原LuminaDiMOO/OmniDiff队列保留。


第一百二十六批（2026-10-22）完成L112 Lumina-DiMOO全核心/十表与十一页实际PDF，补固定GH/HF及cache/SelfGRPO/局部编辑协议，纠正32倍重复相乘、任务全优和保留码等于RGB保持的误述。357目录，235核心/238书面；未确认核心95论文／研究+27资源（资源单独审）。见[审查](lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_sixth_changes_2026-10-22.md)。无删除或执行模型。

继续：L113 OmniDiff及L114–116，保留dMLLM-TTS/HT-GRPO/aMUSEd/Meissonic与cache理论追引；HTGRPO有arxiv2605.16842，非无论文资源，尚未计核心完成。L112待补完整原RL/数据与cache质量协议，未将推理源码选读等同全系统复现。


第一百二十七批（2026-10-22）完成L113 Omni-Diffusion正式核心、全部八表与八实际PDF页，核对arxivv2及固定GH/HF。明确连续语音输入、两版WER/CLIP/RTF、位置缩放/预填与源码差异。357目录，236核心/239书面；未确认核心94论文／研究+27资源（资源单独审）。见[审查](omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_seventh_changes_2026-10-22.md)。无删除或执行模型。

继续L114 LLaDA2.0-Uni、L115 FullFlow和L116 MultimodalFlow；语音/视觉codecs原论文按ID去重追引。保留L184原PDF图证及封闭来源项，未降低验收范围。


第一百二十八批（2026-10-22）完成L114 LLaDA2.0-Uni完整核心、十四表/Eq1–8与十三实际PDF页，核固定GH/HF的MoE、decoder与SPRINT。记录文字渲染差距、T4正文/表冲突、缓存剪枝及质量-速度折中。357目录，237核心/240书面；未确认核心93论文／研究+27资源（资源单独审）。见[审查](llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_eighth_changes_2026-10-22.md)。无删除或执行模型。

继续L115 FullFlow、L116 MultimodalFlow及L117后统一模型；新增追引BlockDiffusion/LLaDA2mini/ZImage/UCGM/CVTG和dFactory，逐原始ID去重。本批未将这些引用或外部SGLang/FP8视为已深读。


第一百二十九批（2026-10-22）完成L115 FullFlow完整核心、十表与十五实际PDF页，核双时间RF/插入、输出梯度理论、先验保留评价及网页制品树。保留T4/T9数值、T8反例、T5/T6预算与算术冲突。357目录，238核心/241书面；未确认核心92论文／研究+27资源（资源另审）。见[审查](fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[逐文件说明](one_hundred_twenty_ninth_changes_2026-10-22.md)。无删除或执行模型。

继续L116 MultimodalFlow及L117后统一模型；FullFlow追引OneFlow/EditFlows/DualDiffusion及关联硕士论文需按原ID去重。网页仓库不构成原训练代码覆盖。


第一百三十批（2026-10-22）完成L116 Multimodal Flow完整核心/附录研究、十表/Eq1–12及九实际PDF页，核固定GH/HF连续codec、块因果、预算和采样。记录oneobjective范围、等参数与等计算区别、数据/默认配置差异及生成-理解取舍。357目录，239核心/242书面；未确认核心91论文／研究+27资源。见[审查](multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirtieth_changes_2026-10-22.md)。无删除或执行模型。

继续L117 BLIP3o及后续统一模型；新增追引ELF2605.10938、ScaleRAE2601.16208、GPIC2605.30341和minit2i/RAE制品，按原ID去重。本篇引用与接口核查不等独立精读完成。


第一百三十一批（2026-10-22）完成L117 BLIP3-o v1完整核心/两主表/AppA与七实际PDF页，核原GH与HF模型/数据卡。分开公开8B与私有论文8B、原版与NEXT，记录语义flow公式勘误、64query单次前向和缺少joint/AI数据因果对照。357目录，240核心/243书面；未确认核心90论文／研究+27资源。见[审查](blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_first_changes_2026-10-22.md)。无删除或执行模型。

继续L118 OpenUni及后续统一模型；BLIP3o-NEXT2510.15857按原ID去重、原OpenReview9aI6XUDYLX后版全文/录用未核、公开检查点完整训练日志和数据去重留队列。


第一百三十二批（2026-10-22）完成L118 OpenUni v3全部核心/六表与五实际PDF页，核固定GH训练/模型/评测和HF模型/数据元数据。记录轻连接器、GenEval模板分布、生成器解冻混杂、L512型号矛盾及公开/许可边界。357目录，241核心/244书面；未确认核心89论文／研究+27资源。见[审查](openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_second_changes_2026-10-22.md)。无删除或执行模型。

继续L119 UniFork及后续模型；追引FlowGRPO（先核原ID）、SANA/DC-AE正式版与重caption资源，按题名/原ID去重。OpenUni资源元数据与架构接口核查不等这些工作精读完成。


第一百三十三批（2026-10-22）完成L119 UniFork v1全部核心/五表与八实际PDF页，核固定GH分支、冻结、RQ头和训练/采样。记录mutual-kNN观察的因果边界、T4聚合矛盾、专家残余差距及参数/分辨率/发布脚本差异。357目录，242核心/245书面；未确认核心88论文／研究+27资源。见[审查](unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_third_changes_2026-10-22.md)。无删除或模型执行。

继续L120 HunyuanImage3.0与后续模型；追引Huh等mutual-kNN原文和任务梯度/参数分叉工作，按原ID/题名去重。UniFork OR挑战访问、原checkpoint/配方矛盾留待有新证据再解，不重复失败抓取。


第一百三十四批（2026-10-22）完成L120 HunyuanImage3.0 v3全部核心/训练表和六实际PDF页，核固定GH及三HF模型配置/采样/权重索引。记录GSB绝对四格与净差、SSAE宏微平均、无受控消融、MoE观察及Base/Instruct/Distil/TMP边界。357目录，243核心/246书面；未确认核心87论文／研究+27资源。见[审查](hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_fourth_changes_2026-10-22.md)。无删除或模型执行。

继续L121 DeepGen1；追引MixGRPO2507.21802/SRPO2509.06942/TMP/ReDA，MeanFlow已有E01/E02去重关联。参考文献与报告概述不计各原工作精读，未公开制品/原评测保留缺口。


第一百三十五批（2026-10-22）完成L121 DeepGen1 v2全部核心/附录11表与13实际PDF页，核主仓、独立RL和三类HF制品。记录SCB全上下文、投影/超参差异、RL任务退化、概率代理及公开UniGen训练提示与600测试提示的3条精确交集，未推定最终运行使用。357目录，244核心/247书面；未确认核心86论文／研究+27资源。见[审查](deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_fifth_changes_2026-10-22.md)。无删除或模型执行。

继续L123 InternVLU；追引CPS2509.05952/GDPO2601.05242/PrefGRPO、UniReason/CVTG。相关引用与制品读取不计各原工作独立精读。保留3条公开提示交集的实际训练使用及近重复边界。


第一百三十六批（2026-10-22）完成L123 InternVL-U v1全部核心/附录、24表、17实际PDF页与固定模型/代码/TextEdit/EvalKit指定实现。记录理解5/7退化、CoT子类权衡及CFG混杂、RISE原表聚合疑问、TextEdit报告与发布指标差异、LongText无序召回边界。357目录，245核心/248书面；未确认核心85论文／研究+27资源。见[审查](internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_sixth_changes_2026-10-22.md)。无删除或模型执行。

继续L124 Mamoda2.5；追引门控/MSRoPE、FluxText/FluxReason、GenExam/LongText/CVTG、GeoGebra/Graphviz/PubChem。引用不计原文独立精读，RISE与TextEdit原运行版本问题继续保留。


第一百三十七批（2026-10-22）完成L124 Mamoda2.5 v1全部核心/附录13表、11实际PDF页与固定八文件推理制品指定源码。补核视频/字幕真实任务、25B/A3B口径、DiT计时95.9倍与实测7.5倍、Reco/理解负例、曲线标注与发布48Top5对报告128Top8差异。357目录，246核心/249书面；未确认核心84论文／研究+27资源。见[审查](mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_seventh_changes_2026-10-22.md)。无删除或模型执行。

继续L125 SenseNova-U1；追引DiTMoE/RaceDiT/DiffMoE、DMD/NFT/ExpertBias、OpenVE/FiVE/Reco/VInO/OmniVideo2及视频数据合成。相关引用不计原文独立精读；完整视频消融、发布权重与曲线标注疑问保留。


第一百三十八批（2026-10-22）完成L125 SenseNova-U1全部核心23表/Eq1–7与固定发布配置/指定源码。明确像素MoT真实任务、17.55B/38.74B索引参数、噪声能量解释、LongText计数召回、理解/OneIG退步、协同对照缺口及U1.5版本边界。357目录，247核心/250书面；未确认核心83论文／研究+27资源。见[审查](sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[逐文件说明](one_hundred_thirty_eighth_changes_2026-10-22.md)。无删除或模型执行。

继续L128 MindOmni；NEO-unify博客/U1.5报告/LoRA/Infographic/Interleaved/GGUF/Training-Sample逐版本追引。FlowGRPO/DMD2/PhasedDMD及LightLLM/LightX2V、CVTG/LongText/RealUnify另审，不能由引用计完成。


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


第一百五十六批（2026-10-23）：完成L144 ACL2026正式17页全部研究正文/AppA–C及4表10图、12实际PDF页；核固定评价代码、八文件制品与HF卡，区分指标升降、已知k和原生/外部编排。357目录，265核心/268书面；未确认核心65论文／研究+27资源。见[审查](unimmmu_state_parsing_oracle_length_and_synergy_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_sixth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十七批（2026-10-23）：L145完整23页/全部附录、3表12图37式及17实际PDF页；全部评测源码、510标注和五viewer静态核，区分裁判重复/生成重复、AQ下降、理论恒等式和实际性能保证。357目录，266核心/269书面；未确认核心64论文／研究+27资源。见[审查](genius_contextual_rules_attention_theory_and_metric_tradeoffs_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_seventh_changes_2026-10-23.md)。无删除或模型执行。


第一百五十八批（2026-10-23）：L147正式21页全部研究正文/AppA–L、1式11表7图及8实际PDF页；固定源码及两版1000题结构/定向事实核，分清金标准重写、三项旧分与维护版二值分，未删文件。357目录，267核心/270书面；未确认核心63论文／研究+27资源。见[审查](wise_gold_explanation_verified_protocol_and_knowledge_validity_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_eighth_changes_2026-10-23.md)。无删除或模型执行。


第一百五十九批（2026-10-23）：L148正式31页全部研究正文/AppA–G、7表11图/16实际PDF页，纠正正式五次/早期三次，核737basic/47UGE和Judge独立制品；训练对与未完整tar未冒充全量核，未删文件。357目录，268核心/271书面；未确认核心62论文／研究+27资源。见[审查](imgedit_dataset_versions_score_gating_and_pipeline_reproducibility_audit_2026-10-23.md)、[逐文件说明](one_hundred_fifty_ninth_changes_2026-10-23.md)。无删除或模型执行。


第一百六十批（2026-10-24）：L150正式研究正文/AppA–F、3表36图图注及17实际图页/接触图，核固定五评价入口和GH/HF各1267标注。纠正hint对IF的负项，记录异常模板分支和空知识提示边界。357目录，269核心/272书面；未确认核心61论文／研究+27资源。见[审查](kris_knowledge_hint_calibration_and_released_protocol_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixtieth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十一批（2026-10-24）：L149按arXiv v2完成核心三遍，读4表/Eq1/全部研究附录及实际图；核公开zip两清单和1692图片索引，记录缺QA/评分代码、相关估计单位未决及身份-语义取舍。正式PDF未完整，未当正式版通读。357目录，270核心/273书面；未确认核心60论文／研究+27资源。见[审查](mmig_ams_estimand_and_public_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_first_changes_2026-10-24.md)。无删除或模型执行。


第一百六十二批（2026-10-24）：完整取得L149正式38页并读全部研究核心/附录、4表与公式；T2较v2新增UNO/RealCustom/OmniGen，表并集20与摘要17/官网18分列。核心条目仍270，未重复计数。357目录，270核心/273书面；未确认核心60论文／研究+27资源。见[审查](mmig_formal_version_delta_2026-10-24.md)、[逐文件说明](one_hundred_sixty_second_changes_2026-10-24.md)。无删除或模型执行。


第一百六十三批（2026-10-24）：L142核7JSON共4101条、固定视频/迷宫等评分函数和HF路径。记录时间均值特征的顺序盲点、90迷宫终止图缺项与405/720步数分母；正式全文仍缺，五项书面保留未通过，核心数不增。357目录，270核心/274书面；未确认核心60论文／研究+27资源。见[审查](mme_unify_temporal_metric_and_terminal_step_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_third_changes_2026-10-24.md)。无删除或模型执行。


第一百六十四批（2026-10-24）：L151补读正式研究正文、四表六图、公开评分及数据卡；核37表列/BAGEL18项最佳、16配置第二轮背景指标下降、全幅掩码PSNR面积偏置。独立补充未取得，五项书面保留未通过，核心数不增。357目录，270核心/275书面；未确认核心60论文／研究+27资源。见[审查](compbench_region_metrics_and_released_protocol_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_fourth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十五批（2026-10-24）：L152完成正式36页研究正文/附录核心三遍与五项书面，核全主表及固定评分和2440提示。记录词序错误仍满分的公式反例、430/421人评计数、RC缺项、黑图分母和表内汇总差异。357目录，271核心/276书面；未确认核心59论文／研究+27资源。见[审查](oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_fifth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十六批（2026-10-24）：L154完成正式主文与独立补充全部研究文字/表图核心三遍和五项书面。核静态编辑提升及理解/T2I取舍；长程能力仅有选例，未见距离分层成功率或组件消融。357目录，272核心/277书面；未确认核心58论文／研究+27资源。见[审查](chatumm_context_tracking_and_claim_boundary_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_sixth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十七批（2026-10-24）：L156补齐完整HTML/附录A–G、全部15公式/五表/11原图核心三遍与五项书面；给出LR首次距离不足保证越过近期窗口的反例，明确UniLongGen*同权重和文字0分/字段汇总边界。357目录，273核心/278书面；未确认核心57论文／研究+27资源。见[审查](long_horizon_memory_revisit_definition_and_scaling_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_seventh_changes_2026-10-24.md)。无删除或模型执行。


第一百六十八批（2026-10-24）：L157补齐完整v4正文/附录、16表/六图及固定公开推理入口；保留SFT后ASR退步和direct-s2s劣势，纠正Fig3为样例，并分列人评分母、视频关键帧和解码配置边界。357目录，274核心/279书面；未确认核心56论文／研究+27资源。见[审查](mio_tokenization_modality_tradeoffs_and_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_eighth_changes_2026-10-24.md)。无删除或模型执行。


第一百六十九批（2026-10-24）：L158完成正式正文+补充22页、12公式/九表14图；核实Eq11符号与scheduler不同、多输入入口受六任务断言限制，准确保留作者已讨论的triplet必要性及文本实体重建失真。357目录，275核心/280书面；未确认核心55论文／研究+27资源。见[审查](omniflow_guidance_formula_and_released_task_coverage_audit_2026-10-24.md)、[逐文件说明](one_hundred_sixty_ninth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十批（2026-10-24）：L159完成v3完整50页、11公式23表及全部图，给出动态权重非单调反例，修正两套对话评测与消融并列口径，核官方推理包/9B配置及缺失训练与生成接线。357目录，276核心/281书面；未确认核心54论文／研究+27资源。见[审查](m2omni_dynamic_weight_formula_and_release_scope_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventieth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十一批（2026-10-24）：L160完成v1完整28页/15表八图，修正128帧与SANM执行分支，保留上下文语音WER退化，核三router共用专家池及仅最终尺度采样；配套Ming-Lite-Uni另排追引。357目录，277核心/282书面；未确认核心53论文／研究+27资源。见[审查](mingomni_multiscale_bridge_and_context_tradeoff_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_first_changes_2026-10-24.md)。无删除或模型执行。


第一百七十二批（2026-10-24）：补录L191配套前作，完成v3研究全文/三表七实际图/四式；承认MSE文字收益但保留受控消融缺项，纠正文称.62超过.67，核M2论文与Qwen发布物、三次采样只返末图。358目录，278核心/283书面；未确认核心53论文／研究+27资源。见[审查](ming_lite_uni_companion_multiscale_and_release_alignment_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_second_changes_2026-10-24.md)。无删除或模型执行。


第一百七十三批（2026-10-24）：L161完成v3全部研究正文/附录、11表五图；核T8混合macro与WER折中、T11完整性退化及正文冲突，固定Flash2.0实际单尺度和负条件参数未用，保留声/图指标退步。358目录，279核心/284书面；待完成核心深审52篇论文／研究；27项资源按制品协议另审。见[审查](ming_flash_omni_frozen_synergy_context_metric_and_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_third_changes_2026-10-24.md)。无删除或模型执行。


第一百七十四批（2026-10-24）：L162完成v2研究全文/16表12图两式；核文本18项11升7降及指令三项全退、ASR对Qwen1胜9负、100ms在VAD后和GPT4o第三方脚注，区分demo与服务链。358目录，280核心/285书面；待完成核心深审51篇论文／研究；27项资源按制品协议另审。见[审查](longcat_flash_omni_stage_tradeoffs_latency_and_service_identity_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_fourth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十五批（2026-10-24）：L184补核作者原图F2/F8、正式T2全部勾选行，纠正公开代码全固定六类的过宽说法；其余图版缺口保留未通过，不增加核心三遍数。358目录，280核心/285书面；待完成核心深审51篇论文／研究；27项资源按制品协议另审。见[审查](stroke_seg_author_figure_checkbox_and_sample_code_recheck_2026-10-24.md)、[逐文件说明](one_hundred_seventy_fifth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十六批（2026-10-24）：U09完成v3研究全文/全部附录prompts、8表24图，核成本比较矛盾、单任务/最终/hybrid配置与非单调采样；固定训练/评测/HF发布，保留图像因果及保真证据边界。358目录，281核心/286书面；待完成核心深审50篇论文／研究；27项资源按制品协议另审。见[审查](thinkmorph_full_reasoning_modes_cost_protocol_and_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_sixth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十七批（2026-10-24）：U11完成arXivv2正文/全部附录、7表9图及FindingsACL2026正式版补核；区分Zero791条SFT、800样本加权、TV平滑与功能正确性，记录默认min/多分支及输入图接线等发布缺口。358目录，282核心/287书面；待完成核心深审49篇论文／研究；27项资源按制品协议另审。见[审查](omni_r1_full_perception_reward_protocol_and_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_seventh_changes_2026-10-24.md)。无删除或模型执行。


第一百七十八批（2026-10-24）：U12完成arXivv1全部研究正文/附录、10表39图和公开评测/推理源码；核ACC缺失切公式、Zebra分母、同生成公式Logic下降及数学/迷宫等现行标注错误，区分论文图示与发布版本。358目录，283核心/288书面；待完成核心深审48篇论文／研究；27项资源按制品协议另审。见[审查](weave_full_interleaved_benchmark_scoring_and_annotation_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_eighth_changes_2026-10-24.md)。无删除或模型执行。


第一百七十九批（2026-10-24）：U13完成v2全部研究正文/附录、13表10图16式；核622发布题与646差异、两侧答案信息不对称、联合成功越界及图judge改按错误文本的一致性。公开锚定已补，修正旧实现待核结论；fit统计单位/λ仍与论文不同。358目录，284核心/289书面；待完成核心深审47篇论文／研究；27项资源按制品协议另审。见[审查](gapeval_full_bidirectional_information_scoring_and_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_seventy_ninth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十批（2026-10-24）：U14完成v1全部研究正文/附录、14表24图及公式prompts；区分GtA相对Base和Direct、复算MIO25项差值、核动作词匹配与完整成功差别，以及当前limit1/多图wrapper入口边界。358目录，285核心/290书面；待完成核心深审46篇论文／研究；27项资源按制品协议另审。见[审查](unig2u_full_generation_to_understanding_budget_and_scoring_audit_2026-10-24.md)、[逐文件说明](one_hundred_eightieth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十一批（2026-10-24）：U15补齐v2完整19页研究正文附录、13表12图和公开两评分器；确认CVPR2026接收，区分UEG重写增益/GEU图替换，核2000行配对元数据及MT字段、坏核对项、当前聚合阻断。358目录，286核心/291书面；待完成核心深审45篇论文／研究；27项资源按制品协议另审。见[审查](realunify_full_bidirectional_stepwise_and_conjunctive_judging_audit_2026-10-24.md)、[逐文件说明](one_hundred_eighty_first_changes_2026-10-24.md)。无删除或模型执行。


第一百八十二批（2026-10-24）：U16完成v1完整18页研究正文/附录、两表六图八式和全部20推理/三组judgeprompt；核Eq5缺平均项、文本图像额外内容规则差异、Render地板/复用与两处r/p冲突。358目录，287核心/292书面；待完成核心深审44篇论文／研究；27项资源按制品协议另审。见[审查](vgubench_full_typographic_answer_and_correlation_identifiability_audit_2026-10-24.md)、[逐文件说明](one_hundred_eighty_second_changes_2026-10-24.md)。无删除或模型执行。


第一百八十三批（2026-10-24）：U17完成23页v1、10表10图；核任务解耦额外重建与预算混杂、几何单向/SVG和3D双向边界，以及同源端到端编辑对照。358目录，288核心/293书面；待完成核心深审43篇论文／研究；27项资源按制品协议另审。见[审查](native_synergy_full_routing_reconstruction_and_system_controls_audit_2026-10-24.md)、[逐文件说明](one_hundred_eighty_third_changes_2026-10-24.md)。无删除或模型执行。


第一百八十四批（2026-10-24）：U18完成ECCV2026 v2完整42页、13表13图及100空间prompt；核计数GTfallback、空间检出排除、文字样式差异与FID语义，官方HEAD仅README。358目录，289核心/294书面；待完成核心深审42篇论文／研究；27项资源按制品协议另审。见[审查](transferability_full_parser_coverage_and_distribution_shift_audit_2026-10-24.md)、[逐文件说明](one_hundred_eighty_fourth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十五批（2026-10-24）：U19完成ICML2026 v3完整16页4表7图20式；核三骨干对Base七指标全升及对RecA例外、Harmon公开512²/10K配置、四任务微batch/梯度scale、无类别边界与teacheragreement。358目录，290核心/295书面；待完成核心深审41篇论文／研究；27项资源按制品协议另审。见[审查](unimrg_full_teacher_targets_training_schedule_and_release_audit_2026-10-24.md)、[逐文件说明](one_hundred_eighty_fifth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十六批（2026-10-24）：U21完成v1完整17页8表15图7式算法1；核trace四象限/两同源骨干、AND对照、阈值重叠差别、91%图FLOPs与Eq7口径，保留实测延迟证据。358目录，291核心/296书面；待完成核心深审40篇论文／研究；27项资源按制品协议另审。见[审查](adavig_full_counterfactual_denominators_and_early_abort_cost_audit_2026-10-24.md)、[逐文件说明](one_hundred_eighty_sixth_changes_2026-10-24.md)。无删除或模型执行。


第一百八十七批（2026-10-25）：U22完成22页5表14图、固定官方评估/生成入口及1000条元数据核查；区分标准与题/任务/模态汇总，记录单模型人评/裁判与单例trace的证据边界。358目录，292核心/297书面；待完成核心深审39篇论文／研究；27项资源按制品协议另审。见[审查](ueval_full_rubric_aggregation_and_release_protocol_audit_2026-10-25.md)、[逐文件说明](one_hundred_eighty_seventh_changes_2026-10-25.md)。无删除或模型执行。


第一百八十八批（2026-10-25）：U23完成完整HTML正文/附录、5表10图18式；核二维框对偶与软硬约束、四分支成本、rewrite/视频物理残余失败及完整反例。358目录，293核心/298书面；待完成核心深审38篇论文／研究；27项资源按制品协议另审。见[审查](sco_full_soft_constraint_solver_and_video_protocol_audit_2026-10-25.md)、[逐文件说明](one_hundred_eighty_eighth_changes_2026-10-25.md)。无删除或模型执行。


第一百八十九批（2026-10-25）：U25完整34页/5表17图15式与所有证明；核局部Lipschitz证明范围、MMSI全522条六关系、评分/模型阶段差异及固定revision评测骨架。358目录，294核心/299书面；待完成核心深审37篇论文／研究；27项资源按制品协议另审。见[审查](visworld_full_theory_comparability_and_release_protocol_audit_2026-10-25.md)、[逐文件说明](one_hundred_eighty_ninth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十批（2026-10-25）：U26完整35页、23表5图10式与五阶段训练；核文字计数指标的顺序盲区、外部PE和UniMMMU下降，固定公开训练范围/最终HF配置。358目录，295核心/300书面；待完成核心深审36篇论文／研究；27项资源按制品协议另审。见[审查](sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninetieth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十一批（2026-10-25）：U27完整13页6图及三式，核latent扩散/共享视觉encoder、F2标签倒置与F5身份变化；无量化主表/消融/完整recipe，Claim限双向示例可行性。358目录，296核心/301书面；待完成核心深审35篇论文／研究；27项资源按制品协议另审。见[审查](unimodel_full_visual_only_cycle_and_evidence_scope_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_first_changes_2026-10-25.md)。无删除或模型执行。


第一百九十二批（2026-10-25）：U28完整27页10表9图/6QA及8式，核固定输入modal式无UMM梯度、max−min偏好可降低worst、代理/真实循环和公开配置差异，保留各类增益与负结果。358目录，297核心/302书面；待完成核心深审34篇论文／研究；27项资源按制品协议另审。见[审查](latentumm_full_dual_alignment_gradient_and_rollout_protocol_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_second_changes_2026-10-25.md)。无删除或模型执行。


第一百九十三批（2026-10-25）：U31完整18页10表7图13式并核PMLR正式版；确认ICML2026，保留Showo GenEval两套数、Liquid及编辑负项，核有限工具代码与MI/stopgrad实现边界。358目录，298核心/303书面；待完成核心深审33篇论文／研究；27项资源按制品协议另审。见[审查](diva_full_information_factorization_and_release_protocol_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_third_changes_2026-10-25.md)。无删除或模型执行。


第一百九十四批（2026-10-25）：L009完整8页11图2表/EF算法，核1251实例8117笔画、490笔画错误及top1/5 88.41/96.16%；末帧回溯恢复与规范笔顺判断分开记录。358目录，299核心/304书面；待完成核心深审32篇论文／研究；27项资源按制品协议另审。见[审查](video_based_chinese_recognition_2005_full_temporal_recovery_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_fourth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十五批（2026-10-25）：L007正式17页19图5表10式完成；区分静态footprint与序列，核mm/px、deg/rad及回归比例疑点，静态CSIM/SSIM和重校准两笔结果限条件解释。358目录，300核心/305书面；待完成核心深审31篇论文／研究；27项资源按制品协议另审。见[审查](bbsmg_full_calibrated_neural_brush_renderer_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_fifth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十六批（2026-10-25）：L008完成正式21页17图5表10式2算法，核局部时间/OLS单调性/恒速图与公式边界；Zenodo公开49图及规划脚本，三维函数默认三次样条，完整数据仍须申请。358目录，301核心/306书面；待完成核心深审30篇论文／研究；27项资源按制品协议另审。见[审查](calligraphy_3d_full_quintic_constraints_and_public_release_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_sixth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十七批（2026-10-25）：L030完成27页10图18表4式及关键代码/结果JSON；区分有限候选评分与单组自由命名，限定激活/权重峰值和跨架构必要性结论，核anchor-only仍执行零加权flow前向。358目录，302核心/307书面；待完成核心深审29篇论文／研究；27项资源按制品协议另审。见[审查](entry_point_umm_full_causal_interface_and_compute_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_seventh_changes_2026-10-25.md)。无删除或模型执行。


第一百九十八批（2026-10-25）：L031完成31页18图8表13式；核51名义概念与逐项图47标签、逆向QA干预的含义和非单调强度曲线，采用AppB.4对架构归因的明确限制。358目录，303核心/308书面；待完成核心深审28篇论文／研究；27项资源按制品协议另审。见[审查](one_space_full_directional_steering_and_architecture_claim_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_eighth_changes_2026-10-25.md)。无删除或模型执行。


第一百九十九批（2026-10-25）：L032完成v3全41页26图16表6式及固定代码/数据；分清固定Rp干预与注意力关联，实核仓库500题和论文2000题发布差、计划提取回退与judge默认配置差。358目录，304核心/309书面；待完成核心深审27篇论文／研究；27项资源按制品协议另审。见[审查](ureason_v3_full_context_intervention_and_release_audit_2026-10-25.md)、[逐文件说明](one_hundred_ninety_ninth_changes_2026-10-25.md)。无删除或模型执行。


第二百批（2026-10-25）：L033全16页7图6表4式完成；补T4阈值、T6双分母、AppF研究途中规则变更，保留真实native错误漏报未改善及外部复杂图表/通用理解限制。358目录，305核心/310书面；待完成核心深审26篇论文／研究；27项资源按制品协议另审。见[审查](recursive_self_improvement_full_rules_and_native_error_audit_2026-10-25.md)、[逐文件说明](two_hundredth_changes_2026-10-25.md)。无删除或模型执行。


第二百零一批（2026-10-25）：L055全19页4图3表11式及Algo1完成；核32次采样去重/旧token重新请求问题、实际空仓库，补CoT-RVS既有online工作与平均J&F的事件评价缺口。358目录，306核心/311书面；待完成核心深审25篇论文／研究；27项资源按制品协议另审。见[审查](orvos_full_causal_protocol_and_bounded_memory_audit_2026-10-25.md)、[逐文件说明](two_hundred_first_changes_2026-10-25.md)。无删除或模型执行。


第二百零二批（2026-10-25）：L056全24页15图11表12式完成；核在线当前帧策略、预载/存储范围、180条真实metadata与代码默认配置，纠正图8为纯定性图。358目录，307核心/312书面；待完成核心深审24篇论文／研究；27项资源按制品协议另审。见[审查](cot_rvs_v4_full_online_and_release_audit_2026-10-25.md)、[逐文件说明](two_hundred_second_changes_2026-10-25.md)。无删除或模型执行。


第二百零三批（2026-10-25）：L057全34页研究正文5图4表5式完成；补分类轴重叠、方法纳入规则缺失、数据单位和GenEval规模错误，区分任意模态标签与具体生成接口。358目录，308核心/313书面；待完成核心深审23篇论文／研究；27项资源按制品协议另审。见[审查](umm_survey_v6_full_taxonomy_and_scope_audit_2026-10-25.md)、[逐文件说明](two_hundred_third_changes_2026-10-25.md)。无删除或模型执行。


第二百零四批（2026-10-25）：S003全17页12图4表完成；补TextCaps起点/冻结和场景融合权衡，查明LD排除无OCR结果、目标任一框命中及公开训练loader问题。358目录，309核心/314书面；待完成核心深审22篇论文／研究；27项资源按制品协议另审。见[审查](glyphcontrol_full_appendix_and_ocr_denominator_audit_2026-10-25.md)、[逐文件说明](two_hundred_fourth_changes_2026-10-25.md)。无删除或模型执行。


第二百零五批（2026-10-25）：L170全17页8图8表完成；CLIP构造位置与真实时序分开，校正图轴统计和检索最优边界，核2025误删后仅ff/coreff恢复。358目录，310核心/315书面；待完成核心深审21篇论文／研究；27项资源按制品协议另审。见[审查](mmc4_full_corpus_release_and_alignment_audit_2026-10-25.md)、[逐文件说明](two_hundred_fifth_changes_2026-10-25.md)。无删除或模型执行。


第二百零六批（2026-10-25）：L171正式20+31页全部完成；十倍限按图量aggregate，补逐任务/提示截断/重启条件及退出整篇文档修正版。358目录，311核心/316书面；待完成核心深审20篇论文／研究；27项资源按制品协议另审。见[审查](obelics_full_supplement_and_data_mixture_audit_2026-10-25.md)、[逐文件说明](two_hundred_sixth_changes_2026-10-25.md)。无删除或模型执行。


第二百零七批（2026-10-25）：L172最新预印本39页完整核；补OCR/RICES协议差、语言能力先降后升、最快成本模型与实际次序、时间戳释放格式和表内规模矛盾。358目录，312核心/317书面；待完成核心深审19篇论文／研究；27项资源按制品协议另审。见[审查](omnicorpus_v3_full_appendix_and_storyboard_protocol_audit_2026-10-25.md)、[逐文件说明](two_hundred_seventh_changes_2026-10-25.md)。无删除或模型执行。


第二百零八批（2026-10-25）：L173正式10+13页全部；补DPO图像退化、人机评分局部反序、全配对PSNR/SSIM与Task2 IRS见图，区分可证数学/源码问题和未复现结论。358目录，313核心/318书面；待完成核心深审18篇论文／研究；27项资源按制品协议另审。见[审查](comm_full_supplement_and_sequence_metric_audit_2026-10-25.md)、[逐文件说明](two_hundred_eighth_changes_2026-10-25.md)。无删除或模型执行。


第二百零九批（2026-10-25）：L174 v1全19页补齐，公开两JSON精确92256条；核真实图来源矛盾、整块mask、batch口径与训练入口缺调用。358目录，314核心/319书面；待完成核心深审17篇论文／研究；27项资源按制品协议另审。见[审查](sharegpt4o_full_appendix_manifest_and_training_audit_2026-10-25.md)、[逐文件说明](two_hundred_ninth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十批（2026-10-25）：S001正式11页完整；公开源码确认CodaBench提交分数定权与30命名配置重复，补同底座适配收益/排行榜聚合/伪GT限制。358目录，315核心/320书面；待完成核心深审16篇论文／研究；27项资源按制品协议另审。见[审查](ketaba_ocr_full_appendix_and_blind_weight_selection_audit_2026-10-25.md)、[逐文件说明](two_hundred_tenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十一批（2026-10-25）：L164完成29页全部证明/附录/图表；补总体joint理论到pair训练的缺口、真实预训练空间和附录结果边界。358目录，316核心/321书面；待完成核心深审15篇论文／研究；27项资源按制品协议另审。见[审查](muni_full_appendix_and_pairwise_identifiability_audit_2026-10-25.md)、[逐文件说明](two_hundred_eleventh_changes_2026-10-25.md)。无删除或模型执行。


第二百一十二批（2026-10-25）：L165完成28页全图表附录；补正文与附录训练量冲突、RoboTwin50行均值差异及CALVIN完整5步弱项。358目录，317核心/322书面；待完成核心深审14篇论文／研究；27项资源按制品协议另审。见[审查](bagelvla_full_appendix_and_aggregation_consistency_audit_2026-10-25.md)、[逐文件说明](two_hundred_twelfth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十三批（2026-10-25）：L166完成25页；解析区分四条理论有效范围，补phase全域稳定反例与数据来源、表量纲和容量对照限制。358目录，318核心/323书面；待完成核心深审13篇论文／研究；27项资源按制品协议另审。见[审查](worldbagel_full_appendix_and_fourier_theorem_audit_2026-10-25.md)、[逐文件说明](two_hundred_thirteenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十四批（2026-10-25）：L167完成48页22图19表；补齐失败案例、人工caption边界、相机评测跳过路径与depth对齐条件。358目录，319核心/324书面；待完成核心深审12篇论文／研究；27项资源按制品协议另审。见[审查](sensenova_vision_full_appendix_and_decoder_protocol_audit_2026-10-25.md)、[逐文件说明](two_hundred_fourteenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十五批（2026-10-25）：L168完成32页17图8表；核对首帧预标注传播、规则自校准与点云尺度后处理，补公开数据与训练条件。358目录，320核心/325书面；待完成核心深审11篇论文／研究；27项资源按制品协议另审。见[审查](puffin_world_full_appendix_and_propagation_protocol_audit_2026-10-25.md)、[逐文件说明](two_hundred_fifteenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十六批（2026-10-25）：N14完成23页12图5表，核对单第20帧/PPv3默认评测、集合字符指标与首16帧FVD，分开论文协议与发布入口。358目录，321核心/326书面；待完成核心深审10篇论文／研究；27项资源按制品协议另审。见[审查](steervte_full_appendix_and_evaluation_release_audit_2026-10-25.md)、[逐文件说明](two_hundred_sixteenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十七批（2026-10-25）：L163补全36页10图12表；区分共享AR与终端扩散、弹性抽取与额外训练，记录RL公式边界及主表负项。358目录，322核心/327书面；待完成核心深审9篇论文／研究；27项资源按制品协议另审。见[审查](ernie5_full_report_and_elastic_rl_claim_audit_2026-10-25.md)、[逐文件说明](two_hundred_seventeenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十八批（2026-10-25）：L142完整取得44页正式版并读齐AppA–H/F1–25/T1–13；补稳定/相关/人类校准，同时保留表列与公开评分协议冲突。358目录，323核心/327书面；待完成核心深审8篇论文／研究；27项资源按制品协议另审。见[审查](mme_unify_formal_full_appendix_and_consistency_audit_2026-10-25.md)、[逐文件说明](two_hundred_eighteenth_changes_2026-10-25.md)。无删除或模型执行。


第二百一十九批（2026-10-25）：L151找到25页arXivv2并补齐AppA–F/19图6表，完成v2完整与正式正文阅读；不把旧GPT4o配置挪用到正式新增模型和人评。358目录，324核心/327书面；待完成核心深审7篇论文／研究；27项资源按制品协议另审。见[审查](compbench_early_full_appendix_and_cross_version_protocol_audit_2026-10-25.md)、[逐文件说明](two_hundred_nineteenth_changes_2026-10-25.md)。无删除或模型执行。
