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
