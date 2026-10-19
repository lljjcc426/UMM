# 文献检索记录

日期：2026-10-15。按检索方向归档，非搜索引擎结果穷尽清单。原论文相关部分阅读不等于代码运行。

| 检索链 | 代表查询/种子 | 获得的原始来源 | 核查范围 |
|---|---|---|---|
| UMM基础 | Chameleon / Janus / Transfusion / Show-o / UniDisc | arXiv原始摘要 | 补全U01—U07，摘要层级 |
| 交错推理 | Zebra-CoT / ThinkMorph / Monet / Omni-R1 / WEAVE | arXiv原始摘要 | U08—U12，避免泛称所有工作是视频模型 |
| 协同与评价 | GapEval / RealUnify / UniG2U / VGUBench / UEval | arXiv原始页 | U13—U16、U22 |
| 原生协同 | Uncovering Understanding–Generation Synergy / Transferability | arXiv及标题检索 | 前者来源重新定位成功；后者本轮正文失败，U18保留待核 |
| 书法统一 | Chinese calligraphy unified recognition generation | [UniCalli](https://arxiv.org/html/2510.13745v2) | 方法/实验/限制；大PDF访问失败，未虚称看过PDF图 |
| 在线—离线桥接 | differentiable physical rendering handwriting | [OnOff](https://arxiv.org/html/2608.03198v1) | 方法、简化物理和渲染PDF相关页 |
| 双模态字形 | dual modality Chinese calligraphy | [DeepCalliFont](https://arxiv.org/html/2312.10314v1) | 核查图像—轨迹与书体区别 |
| 视频文字系统评价 | handwriting stroke / text rendering video benchmark | [VidScribe](https://arxiv.org/html/2609.36598v2)、[VTR](https://arxiv.org/html/2610.01499v1) | 方法/因素/结果口径，不能当笔顺排名 |
| 视频逐笔能力 | stroke-by-stroke video reasoning | [Video models zero-shot](https://arxiv.org/html/2509.20328v2) | Fig.30局部任务，限制外推 |
| 结构和运动先验 | hierarchical offline-to-online Chinese trajectory | [双域HTR](https://link.springer.com/article/10.1007/s44443-026-01050-5) | 原文结构/顺序/向量/运动先验 |
| 动态文字机制 | Text-Animator / Video Text Preservation | [2024](https://arxiv.org/html/2406.17777v1)、[2025](https://arxiv.org/abs/2511.05573) | 前者方法概览，后者摘要级 |
| 局部书法/个性化 | CalliPaint / CalliffusionV2 | [CalliPaint](https://arxiv.org/abs/2312.01536)、[V2](https://arxiv.org/abs/2410.03787) | 摘要级跟踪，不捏造时序指标 |
| 真实过程数据 | OpenHandWrite / stroke-level Chinese database | [出版方原文](https://link.springer.com/article/10.3758/s13428-026-03001-4) | 采集与用途，不下载数据，不推定许可 |
| 规范 | 通用规范汉字笔顺规范 / 8105 / 教育部 | [官方PDF](https://www.moe.gov.cn/jyb_sjzl/ziliao/A19/202103/W020210318300204215237.pdf) | 官方搜索索引可见，直接PDF失败；不编造规范编号/页码 |
| 无墨迹过程识别 | The Unwritten Benchmark | [原始摘要](https://arxiv.org/abs/2608.14558)、[作者发表页](https://nilayyilmaz.dev/publications/) | 作为邻近评测，不用异常索引日期推定首发 |
| 出版信息更新 | LVGM WACV | CVF WACV2026 PDF索引 | 新版元数据线索，PDF未完整读取 |
| 进一步待查 | G-HTR、Benchmarking High-Fidelity Video Scene Text Editing、Reels-RSI | 参考文献及摘要线索 | 未纳入已完成核心表，不借相邻论文代替原文 |

## 访问失败的含义

部分PDF及出版页面未能获取；相关条目仅采用已取得的摘要、元数据或HTML证据，并保留待核状态。

## 2026-10-19 增量检索与原始资料交叉核对

| 搜索渠道 | 命中并核查的原始资料 | 来源等级与待补部分 |
| --- | --- | --- |
| arXiv 正文 | VidScribe 2609.36598，VidSketch 2502.01101 | 前者正文§3/4及结果；后者方法与部分实验待补主表 |
| ACL Anthology + GitHub + HF | Ketaba NakbaNLP 2026、官方 train.yaml / inference.py、HassanB4 adapter | 论文/代码核对完成，adapter 默认路径与官方名存在差异，未本地推理 |
| GitHub 论文官方资源 | VideoSketcher、Haize Calligraphy Bench、BCSS、SceneDAPR、MoSketch、SketchEdit | VideoSketcher 仓库配置可核，完整定量主表待核；Calligraphy Bench judge 实现细节不详 |
| Hugging Face 无论文发布物 | Wuji Writing VAM、Qari-OCR-LoRA、BCSS 数据子集、CASIA-HWDB2-line | 主要模型卡/数据卡，未取权重和受限数据；写字数字与汉字分布区别 |
| CJK 工程与文图控制 | AnimCJK、KanjiVG、TextDiffuser、GlyphControl | 前两个工程README，后两个 NeurIPS2023 官方摘要；SVG区域规范和静态/动态分别记录 |
| 历史目录精度审计 | 281 项 main 主目录 verification 状态 | 221 历史未重新核、1 未解决、37 摘要、21 章节、1 元数据；统计方式见新质量审计 |

详见 [增量研究矩阵](scoped_literature_matrix_2026-10-19.md)、[新资料原始来源登记](../../data/research_additions_2026-10-19.json) 和 [精读队列](survey_queue_2026-10-19.md)。候选数量不能作为已阅读全文数量；无独立实验复现成果。


## 2026-10-19 第二轮

- 对281主目录+16补录的首选来源，以及32条基础文献分别访问，329条事件明细见[访问记录](../../data/source_access_audit_2026-10-19.json)。同一工作可产生多条事件；原文候选与落地页分开。
- 扩展路径：DDPM→score-SDE→LDM/DiT→FM/RF/Consistency/数值求解；Video Diffusion→AnimateDiff/CogVideoX/Wan→Diffusion Forcing/Self Forcing；sketch-rnn→神经绘画/CLIPasso/StrokeFusion；LoRA→QLoRA/DoRA/rsLoRA；FVD/VBench→书写事件校准。
- 直接纠错：Calligraphy Bench与L044重复关联；U18已重新定位原文；DP-Font PSNR及CFG多指标冲突；VideoSketcher分类与顺序偏好分开；UMM联合与单任务结果存在权衡。
- 当前阅读范围与未完成量见[第二轮审查](second_round_audit_2026-10-19.md)，不能将本检索日志当成全部三遍精读完成证明。

## 2026-10-19至20：继续复核存量与前后向追引

- 23项存量研究的原文相关章节已复核：[批次ID与范围](../../data/continued_review_batch_2026-10-19.json)。重点是静态轨迹恢复、矢量动作、交互绘画、数字/物理媒介、视频控制、缓存/蒸馏、离散flow与拓扑约束。
- 官方CVF/PMLR/NeurIPS及作者页核对SketchAgent、StrokeNUWA、VACE、TeaCache、clDice、FRIDA/CoFRIDA发表信息；L001来源版本核为v1，未附会正式会议。
- 通过CoFRIDA官方项目追引HF原始README和文件清单，发现基础模型标识冲突，资源H001单列关联F04。
- 继续发现Edit Flows、Discrete Guidance Matching、Disney2026线稿矢量化、Windfoil，保留为待读候选，未计作已经精读的独立论文。
- DiffVG两个官方PDF入口直接下载未完成；官方项目页/勘误可读，原有F01仍待正文复核。本次未靠访问状态填充全文技术字段。

## 2026-10-20 · 第三批存量原文与公开实现核查

读取19项原始方法/实验章节，ID见[data/third_review_batch_2026-10-20.json](../../data/third_review_batch_2026-10-20.json)。来源包含arXiv版本页、作者PDF、ACL正式论文集、TCSVT作者接收版、官方数据页和工程文档；读取范围逐篇记录。InkDiffuser额外检查固定GitHub树4d9f6c1aef2a13ac1b4779aa090389c0d609e227及三个源文件，未运行训练。女书官方仓库仅核文件列表。StrokeBank PDF第3–4页视觉检查确认式5方向差异。未成功完整下载的PDF未作为本地全文阅读证据，女书全文经Web PDF读取。首批来源访问审计保留为当时快照，不用其HTTP结果代替本批阅读。

## 2026-10-20 · 第四批

24项ID见[第四批清单](../../data/fourth_review_batch_2026-10-20.json)。读取梯度审计/位置级梯度及4项统一评测的原始方法、表格和指定附录；交叉检查原CAGrad算法；读取DiffBrush和3项语义/过程研究，保留不同注入协议的边界。资源方面读取Hanzi Writer文档及LICENSE、Make Me a Hanzi的README/COPYING、CASIA在线格式/条件、IAM-OnDB官方页面的搜索索引、Mobao论文数据章节和Samsung作者技术报告。Springer机器人2篇的Table1/4单独读取，L024完整作者PDF与第4页框架图核查。A06/L002全文受限，L006出版社直连受限，L021/L022只取得可读取摘要/引言，均保持第一遍。搜索索引、作者报告、论文正文、代码与实际数据文件各自注明，未下载模型或运行训练。

## 2026-10-20 · 第五批

21项ID及来源见[本批清单](../../data/fifth_review_batch_2026-10-20.json)。读取Tora/Tora2、MotionCtrl、DragNUWA/DragAnything、MotiMotion、FluidGenZero、RefTok、UniVid的指定方法与实验；读取AnyText、TextVBench、ViTeXBench并分开版本、数据和指标口径。取得InkSpire正式ICLR PDF并查看框架图，补读DiffVG正文/勘误、CalliReader补充材料、Word-As-Image、Strike a Chord、Timage和BoxTuning。前向/后向追引补入STRIVE及CONSTANT，核CONSTANT的官方固定代码树、数据说明和IAM/CASIA配置；未运行源码或下载权重。新增LiveSVG/VitaGlyph等候选只登记线索。各篇未读章节/代码仍在笔记中明示。

## 2026-10-20 第六批来源与精读

新增笔记ID见[data/sixth_review_batch_2026-10-20.json](../../data/sixth_review_batch_2026-10-20.json)。读取对应arXiv全文核心方法/数据/主表与指定附录，额外取得EDM NeurIPS正式主PDF、Consistency Policy RSS正式PDF、L181作者正式PDF，并核对Painter ICCV Workshop/TokenFlow CVPR/F5-TTS ACL的正式元数据。

补充只读来源：Consistency Policy官方仓库commit eed0c465d3c1aa6dcf22f10e784df07dec06beac的teacher采样循环、diffusion Euler/Heun/噪声映射与Square配置；SPRATeam-USTC/G-R-Joint-Optimization commit03b07e7156cf96da6420ee9b794aa75a72256c44的TPE、joint前向/对比、优化器与joint配置。固定版本用于追溯，不是文件hash完整性扫描。L181 PDF p6已目视核公式。未运行外部代码，无新模型权重。

检索词包括CalliffusionV2/CalliPaint/Painter+venue、L181完整题名、Consistency Policy+RSS+GitHub、EDM+NeurIPS2022正式全文。新候选及区分相近题名见[追引队列](survey_queue_2026-10-19.md)。仅访问/搜索摘要不升级章节状态；15份新笔记+1份升级均由实际章节阅读后人工记录。

## 2026-10-20 第七批：从制品反查原文与执行协议

实际读取Wuji/Qari/CASIA/BCSS固定HF revision的配置、README与字段；GitHub selected source blobs见各笔记。Stroke-Seg Wiley HTML后续访问超时，但正式epdf可读§3–6及Tables1–4，新增L184；记录论文/代码/加工版差异。KanjiVG规范与实际中SVG、AnimCJK示例已核。GF0023官方PDF已成功取得581页，本次读前12页定义和初始表，解决首轮索引级限制。OSF rn2ck API确认公开Data/R目录，读取小xlsx表头/样例及R指标相关函数；未取得全部原始轨迹，未运行模型/R脚本。

## 2026-10-20 第八批：任务接口、训练干扰与输出边界

读取Unified-IO2、AnyGPT、SEED-X、MMaDA、Manzano、Qwen3-Omni、Emu3.5原文的模型/数据/训练/选定主表/消融与局限。MMaDA官方tree3cdb8709635beb29f66e4e23cd66060872ac3996，generate.py及modeling_mmada.py按topk高置信解除mask，澄清正文采样措辞；完整UniGRPO ratio实现未取得，不把公式疑点当代码已证错误。Emu3.5 Table3为tokens，未把150B误记样本；LongText中文单项与DiDA质量退化均保留。没有运行外部训练代码或模型。

## 2026-10-20 第九批：早期统一架构与联合扩散

读取L073–L078和L062的方法/训练/主表/消融/限制。通过PMLR与CVF核对OFA(ICML2022)、UniDiffuser(ICML2023)、VersatileDiffusion(ICCV2023)。OFA正式PDF Fig2与Table9渲染视觉核对，公开HTML对应消融Table10；正式Table10为数据统计，表号不能跨版本互引。UniDiffuser正式Fig4已视觉核对。保留OFA正文ImageNet增益与表中差、UniDiffuser文本decoder目标缺负号疑点(未核实际代码)、MetaQuery指令标注模型版本差异；没有把公式疑点当作实现已证错误。

## 2026-10-20 第十批：压缩、条件与协同

LaVIT arXiv2309.04669v3、NExT-GPT2309.05519v3、DreamLLM2309.11499、SEED-LLaMA2310.01218、Emu2 2312.13286v2、MM-Interleaved2401.10208v2、VILA-U2409.04429。读取各自方法、指定主表/消融/附录，范围逐篇列出，未把全文获取等同全文已读。MM-Interleaved v2 PDF共35页，与题录评论20页不一致；第6页Fig4、第13页Table6/7已视觉核查。VILA-U官方仓库revision 4ea42ead2ce22b035ee74c7966eed245bca3e927读取README、pretrain.sh、sft.sh、datasets_mixture.py、inference.py；没有下载模型权重。保留Emu2主文双CLIP领先与表4冲突、decoder warmup差异，NExT signal数量一位差，未核实现处不定性代码bug。

## 2026-10-20 第十一批：训练课程与反馈

JanusFlow2411.07975、Orthus2412.00127、Liquid2412.04332、ILLUME2412.06673、MetaMorph2412.14164、UGen2503.21193、Harmon2503.21979、X-Omni2507.22058。读取范围逐篇记录，含训练配方、关键主表与指定消融/附录。Orthus正式PMLR267:31619–31633，官方15页PDF第4页Fig2及第8页Table4/5渲染视觉核对，Limitations读第8–9页；MetaMorph正式ICCV PDF第2页Fig1视觉核对。ILLUME与MetaMorph官方CVF书目确认ICCV2025，页码分别21612–21622及17001–17012。X-Omni Table2表头Global/Entity/Attribute/Relation/Other/Overall已核，87.65为Overall；表1中文LongText自身.814低于Seedream3 .878，保留与正文声称冲突。Harmon Fig6和X-Omni RL/CFG图只读正文解释，未读精确曲线；不赋予未看过的数值或预算控制。

## 2026-10-20 第十二批：tokenizer理论与公开配方

QLIP2502.05178、DualToken2503.14324、UniToken2504.04423、Selftok2505.07538v3、UniCode²2506.20214、Tuna2512.02014。读取范围逐篇记录；UniCode²19页PDF第3–4页渲染核Eq1–3/Fig2；Selftok42页PDF第25页Eq20交叉核。DDPO2305.13301v4与ICLR2024官方proceedings查重后新增L185，方法、奖励、实验、局限及AppA–F指定部分已读，正式PDF23页获取未逐图。DualToken OpenReview匹配标题/ICLR2026 PDF搜索摘要，但直取403，保留正式全文未对读；UniToken CVF搜索命中CVPR2025W/MMFM，主会/Workshop明确分开。代码revision：NVlabs/QLIP cf86fcc5131c2bb008c349fe9456ccbd1e0e1619；songweii/DualToken499e5b1d716bb72f5e5e2a91eae78ab53cf2ef3d；SxJyJay/UniToken9181c61367baf44e67f08984cac8347c1d5a1626，已读各README及指定配置/脚本，未下载权重或运行。

## 2026-10-20：第十三批连续/离散与像素视频接口

读取arXiv2602.14178v3、2603.12108v1、2603.15228v3、2603.10702v1、2604.24763v2、2605.31604v4、2606.13289v1、2609.38597v1的指定方法/实验/附录。arXiv版本页实时核查前四项。官方GitHub EvoTok147b1b2、HYDRAca3e71d、UniCom55b9001与两项HF卡交叉；仅下载源码/配置/卡片/PDF，无模型权重。HYDRAp4、RFp16、PixelUMMp23已渲染核对；正式会场依作者声明和proceedings核查分开。详见[pixel_interfaces_and_temporal_audit_2026-10-20.md](pixel_interfaces_and_temporal_audit_2026-10-20.md)。

## 2026-10-20：离散流/掩码/连续块路径

阅读L109–L116指定方法、主表本作行/消融/附录；FullFlow由abstract入口补PDF36页，Muddit v5 PDF27页、LaViDa-O PDF33页，下载页数不算全文阅读。视觉查看Muddit p4与FullFlow p8，记录实际范围；代码Muddit d048cf7、Lumina81344e6。ICLR正式proceedings确认Muddit会场；根README交叉发现HT-GRPO有论文，未误计无论文资源。

## 2026-10-20 第十五批来源与版本

读取GenEval及BLIP3o/OpenUni/UniFork/HunyuanImage3/DeepGen/Mobile-O指定正文与配置/消融；Mobile-O v2 PDF18页，仅第4页Fig2视觉核查，下载页数不算全读。BLIP3o默认NEXT分支d0b0a1c与旧main418fc44分别核；HF8B公开模型卡与私有论文分数分开。Hunyuan当前README6e9113a区分Base/Instruct/Distil。Mobile-O91c2550的export.py确认LLM默认4bit、visionFP16与论文描述不一致；未部署。

## 2026-10-20 第十六批

UniFlow v2、InternVL-U v1、Mamoda2.5 v1、SenseNova-U1 v1、Rosetta v1读取指定正文/表/公式。UniFlow代码e6322d0与HF配置交叉核一步采样；Mamoda2.5官方ba41c0b README仍列权重Coming Soon；Rosetta代码30fada7核每tensor投影与float临时副本，PDF第4/14页框架/证明视觉核对。下载/访问未算全文阅读。

## 2026-10-20 第十七批

读HermesFlow/MindOmni/CoRL/PairUni/UniCorn/R3/GvU指定方法与实验。HermesFlow NeurIPS正式PDF25页，p9/p15视觉核对，arXiv14页p4/p13另核；正式Show-o基线.64与v2.53不同，代码4997368实际两DPO加权和。MindOmni PDFp7方差分母视觉核，UniCorn30页PDFp19/20理论视觉核。GvU8203768入口/奖励/训练配置交叉读取，未运行。

## 2026-10-20 第十八批

核对LVRPO/Uni-Synergy/ParetoLoRA/STBridge/MATE的arXivv1及指定方法/实验/附录。PDF下载17/23/10页仅用于来源核对，不计全文精读；ParetoLoRA第4页、SyncR1第17/18页视觉核数学；标准正态上尾p=.1的条件方差解析计算.169135，反驳其普遍≤p命题。官方UniCTokens9ca4254 sync_r1_grpo的README/采样/筛选/更新/阈值路径选读，实际负反馈方向与论文式不同。

## 2026-10-20 第十九批

核对六篇arXiv指定版本；取得UniKE的PMLR306正式24页、MME-Unify的ICLR2026正式44页、Uni-MMMU的ACL2026正式17页PDF，选读方法/主表/指定附录，不以下载算全文阅读。UniEval35页/GENIUS23页/SGU21页PDF仅指定文本范围；SGU p4框架和p16证明视觉核。OpenReview访问受限后改用ICLR正式论文页，无绕过证书或身份。

## 2026-10-20 第二十批

取得并选读七篇正式PDF（WISE21/ImgEdit31/MMIG38/KRIS47/CompBench11/OneIG36/GenExam32页），与arXivv4/v1/v2/v1/v4/v3/v5比对指定数据/方法/主表/附录。未把PDF页数计为完整阅读。GenExam正式p5评分图与OneIGv3p6文字公式视觉核；OneIG正式文本确认同公式。SciPy官方kendalltau说明tau-b处理ties，不能沿用“有并列所以全部秩相关不可用”的推断。

## 2026-10-20 第二十一批

下载L154–L160指定arXiv/正式PDF，选读方法/主表/指定附录；MIO正式23页，OmniFlow正式11+补充11页，不以页数计完成阅读。UniLongGenp8框架图视觉核。GitHub当前Ming为Flash2.0，经官方commits定位2025-06-12提交75fb7ec，读取原README/config；一个假定test_infer_imagegen.py路径返回404，未声称读过此文件，也未运行代码。

## 2026-10-20 第二十二批

读取L057及L169–L174指定PDF/HTML方法、实验、附录；IP2P正式p3框架/p7结果和消融、CoMM正式p4 Eq1视觉核。CoMM默认master，最初假定main返回404，随后读取master目录、README和图像指标代码，未找到数据筛选实现，不称全仓没有。OmniCorpus官方README核ICLR2025接收与CC/CW/YT资源；OpenReview验证页/正式PDF403未读。ShareGPT4o按论文给出的FreedomIntelligence地址定位官方固定提交，最初猜测组织地址404，不影响实际源已定位。

## 2026-10-20 第二十三批

读L161–L168固定版本方法/主表/指定附录，下载30/40/36/29/28/25/48/32页只表来源体量，不计全文完成。MUNI AppB假设/命题与WorldBagel AppA理论进一步核；WorldBagelp24视觉核后给常数函数积分反例。读取Ming/LongCat/SenseNova固定HF卡、SenseNovaTRAIN/YAML/launcher指定段、PuffinWorld发布README。未下载权重、未执行源码；PyYAML模块缺失后直接读取配置文本，没有安装依赖或增加测试。

## 2026-10-20 第二十四批

取得N13/U07–U12/L178固定PDF；PDF页数14/33/37/42/40（Monet以实际文件为准）/20/51/14不计作全文完成。Monet pypdf因surrogate编码失败，改用pdftotext读取，保留原文件；WEAVE CVPR正式11页和Monet正式PDF指定主文另核，ThinkMorph OpenReviewPDF403、正式ICLR目录和arXiv带接收版本交叉。读取Monet固定actor/runner与训练脚本、WEAVE固定README和summarize；未执行代码。L178 DOI经CrossRef确认40(4):849–862/2018年，预印本2016分开。Zebra猜测仓库路径404未当官方资源；WriteLikeYou北大作者PDF成功取得，留待阅读。

## 2026-10-20 第二十五批

读取WriteLikeYou北大作者正式PDF、NeurIPS2023 TextDiffuser/GlyphControl正式PDF和U13/14/15/16/19固定v2/v1/v2/v1/v3。U14 pypdf输出surrogate失败改pdftotext；页数不计阅读完成。固定WriteLikeYou a334b02f、GlyphControl5891d9b、unilm31c5b904的默认/README/训练YAML指定段。再次尝试OpenReview L021/L022 PDF及API均403，浏览解析页有challenge；A06/L002 SpringerPDF返回订阅HTML，无全文，不再按URL后缀当PDF。L006出版社公开摘要/Introduction/片段可读，方法表未取得。CVF正式目录确认机器人书写题目/页码；Springer新O2O正式页开放，留待全文。

## 2026-10-20 第二十六批

U20–U25固定PDF版本v2/v1/v1/v1/v2/v1。读取选定方法、公式、实验/消融及配置，U20PDFp6/U24p4框架渲染核。pdftotext含巨大空白/图中符号时本地压缩连续空白便于阅读，保留原PDF和layout；没有据清洗文本自动修定公式。理论按VisWorld AppA1/A2假设和证明读取，未把条件信息上界当视觉无条件优势。SCO主表/附录规划和GPTjudge原值保留，数值未独立复算模型。

## 2026-10-20 第二十七批

U26–U31读取固定版本PDF方法/选定结果与附录，U29p3/U30p4方法图视觉核。原文追引定位CVF2026正式G-HTR全文及Springer DOI10.1007/s44443-026-01050-5，标题/DOI去重补入L186并深读已有N08，两者p6/p5方法图已视觉核。TorchUMM固定425efa19cb2a18d43278d4d222ed238b5e244546审指定对齐/代理计算；SenseNova固定c35c83b58ef6e238a08b986aa58f3b73303aa42f，HF LoRAs固定f33b8fe0216e6f10e5aed58ebbfdd05f02826732，GHTR固定98e6b16756dc61d70e2c3e6c9c6097b206b1eb70。首次由不完整显示名尝试的单独GitHub/HF地址未找到，已跟随PDF/README真实链接纠正，失败地址不计发布缺失证据；无下载大权重或训练。

## 2026-10-20 第二十八批

重新取得N01作者正式ICLR PDF、N03正式AAAI PDF、S001正式ACL workshop PDF及N02/N04/N05/N06/N09/L011固定arXiv PDF。七篇方法图视觉核，DeepCalliFont消融勾选另外核图。按作者页面链接读取UniCalli固定8f0b42d95e7a374e992c08736a9a3cda79743f7c、OnOff ca3f8d6f7c76d142c95d6a86f97410249d0e5f7c、DeepCalliFont 5b0efdc5c1d688997fae5dabebd5b059c29b9721、Ketaba f1aefa8317edda0d7f064c2ae1731cdb4186b076指定README/配置/函数。KetabaHF固定7f55602e5e83041c4af6ff007c7ccd1dc3e23202，VidScribeHF文件树固定dc7ad43c6bca768250b6d3471a145e1f89504b45；未下载权重或完整视频。OnOff作者称ECCV2026，主办接受页检索/解析未定位对应行，保持作者声明与独立主办核查分开。

## 2026-10-20 第二十九批

七篇PDF对照读取，发现UniVideo当前v4需替换v2为当前主来源，XMPFont读取正式CVPR2022PDF，UMText独立核AAAI2026DOI元数据但技术分析注明arXivv1。七篇方法图视觉核。固定代码UniVideo893c9da04b87fdf5099e8e0e9ef164bca6753327、Lance4baeee086648996f6ab12e673cbe461b0b149997、VidSketchad7fcdb8099e39d253364275711a992febb91eb4及HF Lance7395315758865e6f56ab87ad06a88c7ac172f056/CoFRIDA58d397f81bd0bf64eb43d85ee8bd5191acd9824d。Calligraphy卡固定d3f189f76568729def5e845569543ba9786c317e，datasets-server一次返回全部88行；另读官方SPA公开任务/评分说明及来源描述。仅存行ID/标签/计数，未存完整图片或几何。VidSketch核实际candles.yaml、训练首帧与loss、推理抽象度入口和adapter门控。没有运行模型。
