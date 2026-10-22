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


## 第三十批补充

第三十批读取Visual-OPSD v6、LiveSVG v1、AniClipart IJCV正式版与VitaGlyph WACV2026正式版和v3指定补充，四图视觉核；固定三项Git代码/文档并逐处保留版本冲突。Datumwell固定HF提交审74文件表、十例manifest、特征/动作/转换协议及首例378原生时间戳。未获取受限200例、未跑模型。


## 第三十一批补充

第三十一批核七项完整核心方法/表/消融和框架图；补DiffInk ICLR2026、LVGM WACV2026、PEN-Net ACCV2022正式/补充，固定三库对比配置、mask与loss实现。主表/代码歧义保留。


## 第三十二批补充

第三十二批交叉核CVPR2023 SDT正式/补充、AAAI2023 StrokeExtraction、ICCC2023 Calliffusion正式、Moyun v2与DOI登记；固定SDT/StrokeExtraction/Luhman/InkDiffuser/DiffMath源码范围。DiffMath仅README，不以目录存在当代码已发。后续待查CalliECD（S0031320326013385）、Cangjie（10.1049/ipr2.70392）须先与主目录去重，均未在本批假称精读。


## 第三十三批补充

正式ECCV2024 KineTy、ICCV2025 Dynamic Typography和InversePainting v2/supp已核，AnyText2/AnimatePainter不推定正式接收。固定四官方仓库HEAD核代码/配置/许可；用Salimans2016 §4核标准IS定义，仍未取得KineTy完整评估实现。


## 第三十四批补充

BAGEL2505.14683v3/Show-o22506.15564v3/ReCA2509.07295v4核心读，官方NeurIPS2025/ICLR2026登记核。固定ByteDance-Seed/Bagel、showlab/Show-o、HorizonWind2004/reconstruction-alignment，核训练示例/复现指南/发布TODO及selected源码，未把后续新增支持模型当全部正式实验。


## 第三十五批补充

核Hyper-Bagel2509.18824v1、FlashU2603.15271v1及CVF Findings2026pp9131–9142正式登记、UniCache2609.32831v1、Reflection2609.35767v1。固定三官方GitHub版本与Reflection HF RL/data卡，框架图/主表/消融视觉核；未把arXivPDF与accepted版当逐页已比。


## 第三十六批补充

Hunyuan2511.18870v2/LTX2601.03233v1/VACE正式ICCV2025 PDF与v1附录/WanMove2512.08765v1核心读及框架/表图视觉核；NeurIPS主会和CVF正式身份核。四GitHub固定版本、原LTX19B/WanMove模型与MoveBench/VACEBenchmark卡及配置交叉核，未下载大权重/数据。


## 第三十七批补充

D05 arXiv2506.08009v1核心PDF/NeurIPS2025官方登记；D06 2607.20368v1 HTML全文与flowchat原图，另有v2分开；D07 2604.03118v2 PDF/HTML，ECCV作者声明未升独立确认；D08 2603.27866v1 PDF表1/2蓝黄归属与Target图、消融/MF/跨任务。三个固定Git及HF卡、configs、相关梯度/loss路径已读。作者SGF README追到SGF+2610.10429v2，正在精读未新增；第三方SGF复现alphaXiv和MotionStream仅候选，未验证其结果。


## 第三十八批补充

E01 NeurIPS2025正式23页PDF；E02 arXiv2512.02012v2/官方Lyy-iiis/imeanflow；E03 RSS正式PDF核心+v2 HTML AppA–C/固定student loss路径；新D09 2610.10429v2核心全文/局部定理与固定Git/HF。各核图/主表/消融，未模型运行。SGF+ Related与MF/iMF官方README追到pMF2601.22158、AlphaFlow/DecoupledMeanFlow/CMT，以及ResamplingForcing、MaskForcing、CausalForcing++、DataForcingDistillation、OneForcing、RewardForcing、DuoMatching、VideoMirai、NextForcing、FreqForcing、MemRoPE等名称：仅追引线索，尚待逐项去重/原始身份/正文核查，不计已读或新颖性证据。


## 第三十九批补充

E04 NeurIPS2024正式41页核心/指定证明/附录配置，E05 ACL2025正式17页含B/C，E06 CVPR2025正式11页，E07 CVPR2021正式10页与arXiv HTML补A/D/E/G/H/I选段；核框架图/主表/现有消融，固定Git关键路径及F5 HF卡。CVF网页访问403，已取得正式PDF；未据摘要代替正文。Guide and Code2412.06264、SmoothCache2509.08696，以及TeaCache Related中的AdaCache/FasterCache/FORA/Δ-DiT/PAB等追引待逐项去重和正式原文，只有读取的库配置/已有论文部分计证据，未把追引名单计已读。


## 第四十批补充

F01正式15页+项目勘误，F02正式NeurIPS身份及arXiv2503.16424v4 HTML核心/附录A–E重点+Fig2/6原图，F03 arXiv2210.00664v1 PDF9页含AppA–C，F04 arXiv2402.13442v1 PDF7页；核框架/主表或主结果图/现有消融。F02正式PDF传输中断，完整旧v2仅版本对照，未把不完整正式文件列已读。Git分别固定diffvg85802a7、Bezier9612a22、FRIDA v1.0.0 df3f06f和CoFRIDA v2.0.0 1bf0205；Frida当前f42fa618只记身份。F02 Related/补充中的LIVSS、SGLIVE、O&R、GaussianImage、区域渐变/隐式色场、SVGFormer等需逐项去重续读；Frida train_lora.py与HF配套模型卡本批未深读，不能计完成。


## 第四十一批补充

G014实际读arXiv1704.03477v2及AppA，GoogleResearch核ICLR2018，OpenReview PDF403未取得；G015正式CVF PDF核心/Fig2/8/9、官方615c070代码选段。F05 Samsung全文及Fig1/T1–3，ICASSP13860，ViewManuscript正常跳转IEEE11463098未得正文。H001固定58d397f卡/API/512KiB ZIP元数据，原IP2P31519b5与SDXL-IP2P06653d4 config及Frida f42fa618加载/LoRA选段；未执行pickle或模型。CASHG arXiv2604.02103仅引文/检索线索，尚未精读；G016正式下载超时，官方Paddle与非官方PyTorch复现应区分。


## 第四十二批补充

G016实际读arXiv2108.03798v2，CVF正式下载不完整；官方a5ceece五维形状+grid_sample采色。G017作者项目34页正文/补充及92262f7配置/损失选段。F06读2011.08114v1及附录/CVF身份，正式PDF不完整；官方e7a66b2 README。F07 PMLR10页正文+2页补充、5ee538c公开无条件模型说明/网络选段。框架/主表或曲线/消融原图均已核，未运行。AttentionPainter2410.16418、Interactive Neural Painting2307.16441及其他追引尚需去重/全文，不计新增完成。


## 第四十三批补充

G001实际读2006.11239v2，G0022011.13456v2，G0052210.02747v2，G0062209.03003v1完整HTML核心与所列附录。DDPM/Score官方身份页、ICLR2023目录核venue；正式PDF不完整/403未计已读。固定DDPM1e0dceb/ScoreJAX0acb9e0/RF5a1fd4d官方代码选段，框架/曲线原图核；G005 diffusion图文件不可读不计视觉核，OT条件图可读。NeuralODE/经典score与反向扩散、stochastic interpolants/OT RF后续仍需去重追引，未计新增完成。


## 第四十四批补充

实际阅读G0032112.10752v2／G0042212.09748v2／G0072303.01469v2／G0082206.00927v3完整HTML核心与列明附录，核CVF／PMLR／NeurIPS身份；原框架视觉核范围见逐篇。固定代码LDM a506df5／DiT ed81ce2／CM e32b69e／DPMS52bc3fb，选段核对而非全代码审计。R10读取两个固定HF卡/API/config，不下载权重。队列追加Improved CT2310.14189、DPM++2211.01095、RDM2204.11824，当前仅交叉引用线索，尚未独立完成全文深审。


## 第四十五批补充

核心阅读G0092204.03458v2／G0102304.08818v2／G0112307.04725v2；G009另交叉核NeurIPS正式§4.1 C3D-FID/10K与§4.2抽样。Fig与附录范围逐篇注明，AD e92bd56训练说明/三配置/冻结与时间attention实现选段已核。原补充未取得，不将ICLR2026检索命中训练参数误配原AD；视频未播放。后续RaMViD/SparseCtrl/VideoFusion/VideoCrafter/LongVideoGAN待去重独立读。


## 第四十六批补充

实际读G0122408.06072v3核心及AppA/B/D–G/I/J/K，原Fig3/4/5/6/8与10d完整图已视觉核，ICLR2025身份确认。R11固定GitHub7a1af71的说明/配置/关键trainer和HF三个版本API/config/卡选段；NVIDIA官方标准4090 24GB核文档42GB行。全部例视频/正式PDF/源码未通读。CogKit/MAGVIT2/视频tokenizer与Frame Pack原研究仅追引线索，待去重独立读。


## 第四十七批补充

G013实际读2503.20314v2核心/扩展机制/限制、主T1–8与已有消融，原Fig5/6/7/9/10/16/17视觉核；未观看全视频/扩展图。Wan2.1固定9737cba的三配置全读、采样/调制/VAE关键段与README模型/部署选段；会议身份未获正式证据。VACE/TheMatrix独立原文、Wan2.2/2.6及衍生LoRA/数据资源继续去重核查，出现链接不计完成。


## 第四十八批补充

G018 2106.09685v2、G019 2305.14314v1、G020 2402.09353v6、G021 2312.03732v1指定核心/附录、原主结果/消融与所列图视觉核。LoRA Microsoft作者页确认ICLR2022，QLoRA NeurIPS2023、DoRA PMLR ICML2024身份核；rsLoRA未确认正式venue。OpenReview浏览器验证未通读正式LoRA，未将搜索摘要作为全文。现代PEFT/bitsandbytes/QDoRA-FSDP实现及视频适配资源仍须独立版本核。


## 第四十九批补充

G025 2302.05543v3主文、原Fig2/3/5/8视觉，G026 2207.12598v1核心/Algorithm1/2/T1/2/Fig2/4/5。CVF ControlNet ICCV2023身份条目已取得；正式supp下载未完整不计。固定ed85cd1官方cldm关键段、scribble demo/FAQ/训练和数据教程；未读全卡/源码。T2I-Adapter2302.08453、ControlNet++2404.07987、CFG++2406.08070、EVCtrl2508.10963只检索标题/摘要，入追引去重队列不计完成。


## 第五十批补充

G028 1406.2661v1核心/Algorithm1/Proposition1/2与Theorem1完整证明、T1/2、Fig1四幅；正式NIPS2014身份条目核。G029 1312.6114v11核心/Algorithm1/Eq1–12/AppB–E与F指定段、Fig1/2/3视觉；作者与ICLR官方历史身份核，2022为版本日期。GAN样本图、VAE AppA及全代码未核；Rezende同期Stochastic Backpropagation须独立追读，不能据当前两篇忽略其贡献。


## 第五十一批补充

G031 arXiv2311.17982v1核心/G–M指定段与T1/A5、Fig2/5/A11；正式CVPR PDF Fig1/T1/Fig5caption，CogVideo背景95.42→96.20差异。G032 arXiv1812.01717v2核心/AppA/B/C/Fig3–6、正式关联workshop身份/摘要。固定VBench fd18b3d及GoogleFVD 3ef52111指定源码。追引++2411.13503/2.0 2503.21755/ContentBias2404.12391仅原摘要与README，待全文入库，不算完成。


## 第五十二批补充

G033精读2404.12391v1核心/Eq1/2/T1–7/AppA/B说明，CVPR2024正式身份与PDF Fig2/3/4/6/7/9、T2/3视觉，项目因子部分图/T2/T3。固定a1e037ab源码范围详笔记；T3绝对分差误标百分比在三来源一致，按原分重算。未检查全部动画/依赖/权重。++/2.0全文待精读，不算完成。


## 第五十三批补充

G034精读2411.13503v1全部核心/主表TI–IVb、Fig1/5/9/10视觉；Crossref出版商登记48(3):3268–3285、2026-03，仓库TPAMI2025录用口径分开。指定fd18b3d新增评分/crop/聚合源码及README段；Long仅文档、2.0仍待读。


## 第五十四批补充

G035：2503.21755v2核心I–VI/TI–IV、Eq1/2、Fig1/3/11视觉；固定代码指定评分、人体README/配置/聚合、实例test/split、metadata计数/样例、mechanics原始/改写首例与HF人体卡。正式会刊未确认。


## 第五十五批补充

U01 v2核心§1–7/TI–VII/AppB TXI–XIV、框架/稳定/胜平负实际图；U05 v1核心§1–6/Eq1–4/TI–IX/AppA、框架/mask/FID/CIDEr图，ICLR正式归属元数据。Chameleon官方README全文，HF卡401未读；Janus/Show-o仅取原文，未验收。


## 第五十六批补充

U03 arXiv v1核心/五表/AppA及实际框架/训练/语义encoder图，CVPR正式§4.4/4.5/TV选读；U06 v7核心/五表/AppA–F/I/J/K和实际架构/attention/diffusion图。原Janus README选段；原Show-o固定45a5a2d构造/forward/t2i及四配置全文/README选段。未读范围见专题。


## 第五十七批补充

X01 v4核心/三表及AppC–M文字/表，实际Fig2/3/4/8；官方TMLR归属、README/HF两卡/dataset.md/TF工具。L010 v1核心/三表及AppA/B–E文字，实际Fig2/3/7；79067883脚本/代码选段和HF API，仅元数据无zip/权重。WACV2026同名VideoSketcher（视频素描转换）待独立筛查；SketchAgent v1已获取未验收。


## 第五十八批补充

SketchAgent v1核心/补充文字与D提示选段，正式PDF方法/实验及p6/p8实际图表；固定14c4043生成/拟合选段。ProcessPainter v1核心/Eq1–5/TI–II、v2变更/方法数据实验补读，实际v1Fig2/7；ffeaa2c README/ARN配置全文及优化器/采样选段，HF仅许可卡；不是全部代码/附录全读。


## 第五十九批补充

PaintsAlter正式13页核心§1–5/Eq1–6/TI–IV，实际Fig3/9/10及TIII/IV；项目页和作者名仓库检索边界。StrokeNUWA正式ICML核心/补充A–C文字/TV，实际Fig3/TII/III/Fig7；固定a52e1cc README/两训练例/训练主体。DiffSketcher v2核心已读，v5（2026-04）取得待补全；正式PDF下载未完不作为全文证据。


## 第六十批补充

DiffSketcher v2/v5核心及v5补充A–I文字、T1与实际Fig3/4/8；2023正式PDF未完整不计全文。Diff-Font v3核心及T1–6/实际图，Springer卷页/日期/DOI核定但期刊全文未读；两固定代码的配置/关键条件路径，非全仓复现。


## 第六十一批补充（2026-10-21）

FontDiffuser v1全部核心/附录文字/T1–10及实际Fig2/6，AAAI元数据核、正式PDF不完整不计全文；DiffBrush正式PDF/含附录PDF完整取得，v1核心/B–N文字及实际p3/7/8/14。两固定代码选定配方/条件路径，非全实现或运行。


## 第六十二批补充（2026-10-21）

Emu3 Nature正式核心HTML、T1/实际EDT1–7与Fig1/3/4，完整38页补PDF选读训练/评测/消融并看p13 FigS9，v1方法/主表/评测交叉；Janus-Pro v1全部核心/T1–5/实际Fig3，缺独立消融。两固定GitHub发布与官方HF卡/config或SFT脚本交叉，未运行。


## 第六十三批补充（2026-10-21）

AnyText v5核心/实际Fig2/T2–4、A1–3/A7 T7–8，固定3d4a260选择代码与RealisticVision卡；UniVid v2核心/实际Fig2/T1–4/A2/A4–7 Eq6–16，固定98b5c425选择路径、HF固定a9398c3元数据；ActivityNetQA作者README/原摘要。新增2509.21760、2603.13739、2606.05748同名待精读线索，未混计已读/573候选。正式OpenReview最终PDF尚未逐页核。


## 第六十四批补充（2026-10-21）

N10 arXivv1全部核心/References书目，实际Fig1失败静帧，核2024N09先例/原Wan书目；N11 v1核心Eq1–4/T1–3与实际Fig2a/2b/4/6a；N12官方Workshop接收项14、完整5页正式PDF核心/附录文本及p1实际图，arXiv同核心/T1–2/AppB四选图交叉。未审完整训练实现/原视频或复现。RePaint完整原文/官方scheduler列待补。


## 第六十五批补充（2026-10-21）

G036正式CVF书目、v2全部核心/T1–4/实际Fig2与Fig6指定行、正式supp指定章节/表、固定8e2a055 README/示例/采样路径；主会最终PDF未完整取得。G037 v1核心/AppB/实际p3/11/12/22–24及选择证明段；总体矩反例独立记录，未读完全部30页证明或核正式出版。


## 第六十六批补充（2026-10-21）

N06 v2核心§1–5、全部B任务协议/C及实际p8/p23图；N07正式全文核心与独立T3–7全部系数、实际Fig3/10；N13 v1剩余讨论/结论及AppA全文、实际Fig1/T2/3，作者项目全部静态文本/HF卡全文。CVF限定检索未核N13 Findings正式记录；WritingHacker2016为待全文追引，不重复计入已读。


## 第六十七批补充（2026-10-21）

U08 v2核心与A/C–H核读，实际p4/p9；官方GitHub固定bbf53c3，HF数据f6d1defc/Anole a93d8850/BAGEL ebce3241公开卡全文、18配置元数据与指定训练/推理路径。ICLR2026作者引用/正式PDF索引交叉，OpenReview正文/decision浏览器验证，未读终稿不覆盖v2。


## 第六十八批补充（2026-10-21）

G030正式NeurIPS2024 PDF核心§1–5、A–F正文与指定实际图表；AppA完整证明阅读定位p20 log比值/KL符号，解析高斯检查。paper dd65516/main475e0bc固定代码配置/研究README与指定训练/指标路径。arXiv页当前v4/2024-12-10，未将终版修改状态补猜；History-Guided Video Diffusion正式PMLR267/song25b已定位，尚未阅读全文。


## 第六十九批补充（2026-10-21）

G038正式ICML2025 PMLR267/song25b全文核心、AppA–D理论/协议文字与现有消融；实际p3–6/p13/15图表公式。固定GitHub530f8bf、HF模型0959def/Space9077cb7，模型卡/目录/指定分数组合代码与配置。与G030独立论文、制品不另计；补完第六十八批待精读项。


## 第七十批补充（2026-10-21）

L086 CVPR2025正式全文核心/独立supp A–E、真实Fig2/T4/5；L092 ICCV2025正式核心/supp S1–4/T S1/S2、真实Fig4/6/T5–7。固定Janus1daa72f/HFba75944、Harmon4eb6087/HF4cc9763，公开README/FINETUNE/配置与指定采样代码。仅decoder BLIP3o60K后续.85制品独立记录，不回填正式.76。


## 第七十一批补充（2026-10-21）

G027 NeurIPS2022正式核心全文、独立supp B2–6/C3.4/D/E/F，实际Alg1/T2/F5及supp T3/4；固定NVlabs/edm008a4e5 README/loss/EDMPrecond/指定sampler与Adam/train配置。最低三次FID、选检查点与两栏摘要核查，无权重或执行。


## 第七十二批补充（2026-10-21）

L185 ICLR2024正式核心§1–7/AppA–F，实际F2/3/4/7/10/11/12与T1。固定JAXf0b6ca7/torch1958463指定scheduler/策略目标/config/README、HF美学3941662与对齐23c5dc4全文卡/元数据及对齐scheduler。按维mean logdensity静态代数分析，不等模型运行。


## 第七十三批补充（2026-10-21）

L001 2609.02251v1核心§1–5/七表/数据可用声明，实际p8框架/p14主表/p15/16/17对照；L0042509.15678v1核心§1–5，实际p7框架/p12主表/p15消融/时长；arXiv源包清单/指定TeX确认未含所引supp。未发现已确认正式会场/公开实现，不声称全网不存在。


## 第七十四批补充（2026-10-21）

Painter ICCV2023W/MMFM正式10页全部核心、实际p307框架/p308流程主表；StrokeFusion AAAI2026正式9页全部核心、实际p13658/61/62，固定GitHub4fddf5d及HF abe809b卡/清单、训练/模型/metric/预处理指定代码；追引NeurIPS2019§2Eq1并集PR，不计引文全篇精读。


## 第七十五批补充（2026-10-21）

L005官方IAAI Emerging Application Papers元数据/正式6页全部核心，实际p3027–29公式/表/失败例；L0152511.17344v3 2026-10-18核心§1–7/附录§8/9、T1–9与实际PDFp3/4/7/12–14，固定e53bfd6c代码/README和HF14B8787142/5B7d85f81卡/清单。WACV2027仅作者标识，未查到正式CVF条目。


## 第七十六批补充（2026-10-21）

L063 NeurIPS2025正式页/41页PDF/官方Supplemental ZIP，完整核心§1–6/正式T1–6、附录B–E、实际p4/p6/p21；官方关联dLLM-RL固定10b4fd1c指定配置/目标/奖励。L029固定2604.04746v3 16页核心§1–5/T1–7及实际p4/7/8/10，日期Apr9与此前HTML不同，表内基线.77纠正。


## 第七十七批补充（2026-10-21）

L047正式EMNLP10页核心/研究附录与实际p12420 F2/p12421T1，固定GitHub94f2a059指定代码/notebook/log/完整CSV；L184 Wiley正式15页核心文本/公式/T1–4数值/图注，实际图表视觉仍未验，不计核心三遍；下载403/截图超时不反复重试。


第七十八批（2026-10-21）：采用ICCV2023正文/正式supplement、ICLR2024 Emu正式全文核心与AppA–D，核实际框架/结果/消融；固定官方代码及HF元数据，只读未执行。见[审查](versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)和[单篇L075](../reviews/L075.md)、[L077](../reviews/L077.md)。


第七十九批（2026-10-21）：LaVIT ICLR2024正式核心/AppA/B/D/E与实际框架主表，固定官方GH/HF静态核查；未执行模型。见[审查](lavit_dynamic_tokens_and_version_audit_2026-10-21.md)和[单篇L079](../reviews/L079.md)。


第八十批（2026-10-21）：UniFlow正式ICLR2026、32页核心与指定附录、实际图表、固定GH/HF和quick_start代码。见[审查](uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)和[单篇L072](../reviews/L072.md)。


第八十一批（2026-10-21）：TokenFlow正式主文11p+supp10p、核心/指定图表与官方固定GH/HF/训练采样代码。见[审查](tokenflow_shared_indices_and_claim_audit_2026-10-21.md)和[单篇L094](../reviews/L094.md)。


第八十二批（2026-10-21）：MetaMorph ICCV正式主文12p/supp8p、指定实际图表与固定官方仓库，权重和原始MetaCLIP仍受公开状态限制。见[审查](metamorph_synergy_and_data_budget_audit_2026-10-21.md)和[单篇L090](../reviews/L090.md)。


第八十三批（2026-10-21）：固定2209.04747v5、25页研究核心/关键附录及实际框架/主表，原始元数据与DDPM架构交叉核查。见[审查](diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)和[单篇G022](../reviews/G022.md)。


第八十四批（2026-10-21）：固定效率综述v2全文研究核心及实际框架/主表/公式，Crossref正式书目、固定官方代码和201项发现候选。见[审查](diffusion_efficiency_full_pipeline_audit_2026-10-21.md)和[单篇G023](../reviews/G023.md)。


第八十五批（2026-10-21）：PMLR正式26页、实际图表算法、固定官方采样/结构/codec与HF两版本元数据。见[审查](unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[单篇L076](../reviews/L076.md)。


第八十六批（2026-10-21）：正式Tora11+supp7页、Tora2v2/Crossref正式MM题录、固定代码配置与HF元数据；Tora3/玩偶LoRA后续发现。见[审查](tora_motion_binding_and_process_boundary_audit_2026-10-21.md)、[L034](../reviews/L034.md)/[L035](../reviews/L035.md)。


第八十七批（2026-10-21）：从Tora作者共享README追引Tora3 v3与Wan玩偶LoRA，固定论文/项目/源码与HF配置，核Diffusers0.33.1默认50步。见[审查](tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)、[G039](../reviews/G039.md)/[R12](../reviews/R12.md)。


第八十八批（2026-10-21）：作者22页v2/补充A–E、正式Crossref题录，固定主代码/配置/HF，未全审其他分支。见[审查](motionctrl_camera_object_and_observability_audit_2026-10-21.md)、[L039](../reviews/L039.md)。


第八十九批（2026-10-21）：CVPR/ACL正式PDF及指定补充、固定源码/训练脚本/模型与数据卡。见[审查](unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)、[L058](../reviews/L058.md)/[L059](../reviews/L059.md)。


第九十批（2026-10-21）：固定arXiv HTML/报告、NeurIPS正式PDF与指定源码/模型卡/分包标注。见[审查](seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[L060](../reviews/L060.md)/[L061](../reviews/L061.md)/[G040](../reviews/G040.md)。


第九十一批（2026-10-21）：固定预印本PDF/实际图表、TOG书目/DOI、Word-As-Image固定源码及Code(soon)状态；DS-Fusion正式来源待补读。见[审查](semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[L051](../reviews/L051.md)/[L052](../reviews/L052.md)。


第九十二批（2026-10-21）：ICCV2023正式PDF/作者supp、固定源码根/ldm子树和HF Express关联补漏。见[审查](dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[G041](../reviews/G041.md)。


第九十三批（2026-10-21）：固定MetaQueries v1HTML/UnifiedIO v2PDF与正式书目、实际图表、固定代码/HF数据卡。见[审查](metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[L062](../reviews/L062.md)、[L074](../reviews/L074.md)。


第九十四批（2026-10-21）：固定初版v2PDF/后续v1HTML，ICLR2024正式书目、实际图表、共享代码与HF模型卡追引；正式PDF下载未完成排除。见[审查](seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[L078](../reviews/L078.md)、[L082](../reviews/L082.md)。


第九十五批（2026-10-21）：固定两v1完整PDF、实际框架/主表/消融，BoxNeurIPS官方149433/固定GH及两项基准追引。见[审查](timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[L053](../reviews/L053.md)、[L054](../reviews/L054.md)。


第九十六批（2026-10-21）：由Timage/BoxTuning直接基准追引CVPR2025 AutoConverter及ICCV2025 ObjectMLLM；正式PDF/supp均完整取得，Web工具CVF403由curl读取；固定GH/HF，不下载大数据。见[审查](autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[G042](../reviews/G042.md)、[G043](../reviews/G043.md)。


第九十七批（2026-10-21）：MANZANO v1/Apple和ICLR正式书目分开；GenEval完整arXiv v1、NeurIPS书目和固定18blob发布。正式PDF403/不完整均未作正文证据，实际核框架/结果/消融/人评UI。见[审查](manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)、[L064](../reviews/L064.md)、[L071](../reviews/L071.md)。


第九十八批（2026-10-21）：固定v1提交表、GH28/72blob与HF小配置；实际框架/主表/控制对照，Emu F9初次空图排除后直接原SVG核读，不取模型媒体/权重。见[审查](qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[L065](../reviews/L065.md)、[L066](../reviews/L066.md)。


第九十九批（2026-10-21）：固定v1完整核心及指定附录；XTC GH500blob/HF清单，IMUG GH1060blob/HF卡及完整12.9MB文本metadata；实际框架/主表/TTS、人评，原BLIP3o摘要交叉核分组；少量纯函数反例。见[审查](xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[L067](../reviews/L067.md)、[L068](../reviews/L068.md)。


第一百批（2026-10-21）：PMLR正式11页、arXivv1/v2、两GH固定树59/718blob、HF固定卡/全部指定文本；核作者录用声明与正式出版层级，未找到VGAU对应正式页。见[审查](unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[L069](../reviews/L069.md)、[L070](../reviews/L070.md)。


第一百零一批（2026-10-21）：正式ICML32页/v3与DreamLLM固定v2、ICLR身份、实际框架/表格、固定GH307/295blob及HF元数据配置；正式DreamPDF部分下载排除。见[审查](nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[L080](../reviews/L080.md)、[L081](../reviews/L081.md)。


第一百零二批（2026-10-21）：CVPR完整12页交叉及固定v2完整核心/附录、VILA-U固定v3/ICLR身份、实际图表，GH184/91blob和固定HF卡配置；部分PDF与猜测384地址排除。见[审查](emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[L083](../reviews/L083.md)、[L085](../reviews/L085.md)。


第一百零三批（2026-10-21）：CalliReader正式11页+补充10页、固定v2，AWCV作者accepted13页与DOI卷期页；实际框架/实验，GH830/265blob、HF三个固定revision/当前规模API。见[审查](callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[L045](../reviews/L045.md)、[L046](../reviews/L046.md)。


第一百零四批（2026-10-21）：Liquid固定v4与正式IJCV身份，ILLUME完整正式11页/旧v1附录A；实际框架/主表/消融，Liquid固定GH76blob/HF卡与配置；期刊全文/正式supp边界明确。见[审查](liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[L088](../reviews/L088.md)、[L089](../reviews/L089.md)。


第一百零五批（2026-10-21）：UGen唯一v1完整13页/HTML及实际p8，X-Omni固定v1核心/附A、实际框架/主表/RL曲线，GH10blob/HF五项固定revision与两语prompt统计。见[审查](ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[L091](../reviews/L091.md)、[L093](../reviews/L093.md)。


第一百零六批（2026-10-21）：QLIP唯一v1核心/附A–D/实际图表、7blob与HF固定配置；DualToken正式ICLR身份、v3核心/附A–G/实际图表、241blob树/训练loss，正式PDF部分下载排除。见[审查](qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[L095](../reviews/L095.md)、[L096](../reviews/L096.md)。


第一百零七批（2026-10-21）：MotiMotion正式ICML/PMLR19p、固定v1/实际图表、GH5blob四文本与HF固定62行/来源表；Fluid-Gen-Zero v1核心/附1–7/实际图表及作者项目/GH404。见[审查](motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[L036](../reviews/L036.md)、[L037](../reviews/L037.md)。


第一百零八批（2026-10-21）：固定RefTokv1核心、F2/T1–3及arXiv身份，PDF不完整/正文所指附录未取得；有限官方实现/录用检索未确认。Stroke-Seg新精确F2下载入口403，保留未验收。见[审查](reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[L038](../reviews/L038.md)。


第一百零九批（2026-10-21）：固定两项v1/v3核心与实际图表、正式ECCV身份；DN当前唯一README/svd404，DA固定代码/HF与343JSON文本统计。见[审查](dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[L040](../reviews/L040.md)、[L041](../reviews/L041.md)。


第一百一十批（2026-10-21）：固定v1核心/实际框架主表失败表难度图，有限主源未确认正式venue/官方制品；不把released声明当代码核验。见[审查](textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[L042](../reviews/L042.md)。


第一百一十一批（2026-10-22）：固定v2完整核心/AppA–O/实际框架主表消融；GH/HF及已报逐片数字核查，NeurIPS为作者声明未独立确认。见[审查](vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[L043](../reviews/L043.md)。


第一百一十二批（2026-10-22）：正式CVF完整11页核心/实际p3–6；固定arXiv方法/更新表、GH/HF及prompt文本核查。见[审查](unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[L097](../reviews/L097.md)。


第一百一十三批（2026-10-22）：固定v3核心/AppA/B和六页实际图表，GH/HF；前身DDT-LLaMA正式CVPR身份新查，尚待独立全文。见[审查](selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[L098](../reviews/L098.md)。


第一百一十四批（2026-10-22）：Selftok追引补正式CVPR2025前身G044，正式11页与supp11页完整核心/实际图表，code/HF跳转映射。见[审查](ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[G044](../reviews/G044.md)、[L098](../reviews/L098.md)。


第一百一十五批（2026-10-22）：固定v2/arXiv元数据和HF论文页、定向GH/HF/原始发表源检索；未定位对应代码/权重不等于证明未发布。见[审查](unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[L099](../reviews/L099.md)。


第一百一十六批（2026-10-22）：正式CVPR全索引/正文/官方zip内PDF、arXivv1及固定GH原版TUNA路径；未播放zip视频。见[审查](tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[L100](../reviews/L100.md)。


第一百一十七批（2026-10-22）：固定v3全文/全部33表、GH59f56e67树与README、HF2d4e8863卡与配置；UniWeTok collection404，不把BitDance会场或权重直接移植。见[审查](uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[L101](../reviews/L101.md)。


第一百一十八批（2026-10-22）：固定v1全部核心/五表，六页实际图表；GH147b1b2选读，ECCV官方接收列表注明preliminary，正式出版待核。见[审查](evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[L102](../reviews/L102.md)。


第一百一十九批（2026-10-22）：固定v1全部七表/AppA–G、七页实际图表，GH55b9001/HF78e43059固定制品；正式会场未核。见[审查](unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[L104](../reviews/L104.md)。


第一百二十批（2026-10-22）：固定v2六表与八页实际图表、GH b53594e3选读；正式会场与可验证官方权重链接未核。见[审查](tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[L105](../reviews/L105.md)。


第一百二十一批（2026-10-22）：固定v4/实际PDFAppA–C、项目页外链与SwAV函数选读；会场/运行代码未核。见[审查](representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[L106](../reviews/L106.md)。


第一百二十二批（2026-10-22）：固定v1十三表/实际PDF与NeurIPS官方155676/149164；OpenReview API403、正式全文未对读。见[审查](hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[L107](../reviews/L107.md)。


第一百二十三批（2026-10-22）：固定2609.38597v1、官方GH e19e91a/HF4bb3ce9与完整九表；未核正式会场。见[审查](pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[L108](../reviews/L108.md)。


第一百二十四批（2026-10-22）：NeurIPS2025正式39页、GHffcfc8e/HF6827760；D-DiT原作方法段与NeuralODE2018摘要仅核特定纠错。见[审查](fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[L109](../reviews/L109.md)。


第一百二十五批（2026-10-22）：ICLR2026正式33页、GHe3a80df4/HF8e805608，全部16表/12实际页。见[审查](lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[L111](../reviews/L111.md)。


第一百二十六批（2026-10-22）：arxivv1完整33页/GH81344e6/HFf014549e与11实际PDF页。见[审查](lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[L112](../reviews/L112.md)。


第一百二十七批（2026-10-22）：ICML PMLR306正式15页、arxivv2、GHc4f4625/HF2233ee1；八实际PDF页与全部正式八表。见[审查](omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[L113](../reviews/L113.md)。


第一百二十八批（2026-10-22）：arxivv1完整25页/GHee9dfd5/HFdc2cde4；全部14表/Eq1–8及13实际PDF页。见[审查](llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[L114](../reviews/L114.md)。


第一百二十九批（2026-10-22）：arxivv1完整36页/全部十表/十五实际PDF页，G H网页树9a04534共192项，关联thesis未读。见[审查](fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[L115](../reviews/L115.md)。


第一百三十批（2026-10-22）：arxivv1完整18页/十表/九实际PDF页，GHc84caf5完整182项树、HF13818c6九文件元数据与指定配置源码。见[审查](multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[L116](../reviews/L116.md)。


第一百三十一批（2026-10-22）：v1完整17页/两表/七实际PDF页，固定原GH2042项树与指定源码、HF模型/数据元数据与卡；fixedrevision认证错误和ORchallenge明确未读。见[审查](blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[L117](../reviews/L117.md)。


第一百三十二批（2026-10-22）：v3完整13页/六表/五实际PDF页，GHd1703fc完整123项树和指定方法/训练/评测，HF42f2472与五数据API元数据。见[审查](openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[L118](../reviews/L118.md)。


第一百三十三批（2026-10-22）：v1完整15页/五表/八实际PDF页，GH2c5b757完整111项树及指定源码；Qwen配置/指定HF查询，OR挑战版未读。见[审查](unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[L119](../reviews/L119.md)。


第一百三十四批（2026-10-22）：v3完整17页/一训练表/六实际PDF页，GH6e9113a完整77项树指定段，三HF固定配置/采样/index元数据；GenEval原工作纠偏。见[审查](hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[L120](../reviews/L120.md)。


第一百三十五批（2026-10-22）：v2完整21页/11表/13实际PDF页、固定主仓92项与RL378项树的指定源码、三HF制品元数据，以及固定UniGen600提示对公开RL两提示文件交集。见[审查](deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[L121](../reviews/L121.md)。


第一百三十六批（2026-10-22）：v1完整61页全部核心/附录24表、17实际PDF页，固定GH32项/HF23项、TextEdit50blob与EvalKit3640blob树及指定指标代码；仅元数据不算数据逐例读取。见[审查](internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[L123](../reviews/L123.md)。


第一百三十七批（2026-10-22）：v1完整38页、13表/三公式/11实际PDF页、固定66项树与八文件推理目录的指定代码，权重ComingSoon；未全读上代其他目录。见[审查](mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[L124](../reviews/L124.md)。


第一百三十八批（2026-10-22）：v1全核心23表/Eq1–7、实际PDF页及固定GH735项树/603blob、两HF配置/权重索引、指定推理/训练/评价源码。见[审查](sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[L125](../reviews/L125.md)。


第一百三十九批（2026-10-22）：NeurIPS正式25页核心9表/Eq1–7/9实际PDF页、指定附录与固定GH171项树/137blob、HF25项文件/组合配置。见[审查](mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.md)、[L128](../reviews/L128.md)。
