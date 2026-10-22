# Mamoda2.5：MoE视频、少步后训练和发布制品审查

第一百三十七批完成[L124](../reviews/L124.md)明确范围核心三遍和五项书面记录。[结构化证据](../../data/mamoda25_moe_video_distillation_and_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），246核心/249书面含未通过项；未确认核心84论文／研究+27资源，资源另审。无新增目录、删除文件、下载权重或独立结果复现。

来源：[v1完整38页](https://arxiv.org/pdf/2605.02641v1)、[固定主仓mamoda25目录](https://github.com/bytedance/mammothmoda/tree/ba41c0b90a2a0b626a21a4f36139275e9700e0c3/mamoda25)。正式会场未核，按技术报告。

## 问题与贡献

在统一AR–Diffusion系统内支持文字生图/视频、静态/视频编辑和多模态理解，缓解视频长时空token/大DiT计算、成对编辑数据不足及多步CFG延迟。确有视频任务与字幕编辑评价；字幕/标牌的静态或跨帧渲染正确不等于汉字逐笔动作/规范顺序，未评价真实绘画执行。

视频token随帧数和像素数增长，dense DiT及全局attention昂贵，编辑还需参考视频条件；固定初始噪声但不同提示会在去噪中漂移，难合成结构一致的前后视频对；蒸馏与RL顺序执行可能损质量/采样多样性。作者分别用细粒MoE与高压缩VAE、共享早期去噪合成、DMD+DiffusionNFT联合后训应对。MoE减少FFN活跃计算不消除注意二次复杂度，优劣须连同VAE/编码器/初始化和工程成本评估。

DiT-MoE128路由专家Top8+1共享专家，sigmoid原始亲和分、Expert Bias只改TopK选择，入选原分再归一化。Wan2.2-5B dense自注意/LN迁移，专家从14336中间神经元各随机抽1024，路由随机，避免窄专家直接复制。Qwen3VL8B/MetaQueries gen-expert条件、ByT5文字字节条件和参考VAE latent与噪声沿序列拼接，统一生成/编辑。视频对共享早期去噪→VLM重caption/筛选/反向成对；DMD与DiffusionNFT同时优化，先DMD冷启动再混奖励，将编辑30步CFG蒸到4步无CFG。引用的MoE/MetaQueries/ByT5/DMD/NFT为采用的既有机制；系统整合与上采样设计需区分独立原创。

## 方法与结构

报告框架F3：文字/参考图视频→Qwen3VL8B+学习MetaQueries激活AR内gen experts提供语义条件；引号目标文字→ByT5；参考图视频→3D因果VAE；上述条件/refiner与待去噪目标latent拼接→DiT-MoE联合selfattention/FFN专家→flow迭代→VAE解码RGB视频或单帧。AR此版不逐视觉token自回归生成，MetaQueries也不等于输出显式CoT链。训练可同时NTP与flow，推理有生成、Edit、Edit-Distill三个阶段checkpoint标签，不能把所有表都归4步。公开pipeline仅核到普通文字hidden→refiner与引号ByT5，并在DiT内接参考视频latent；完整MetaQueries/AR视觉条件实现未在指定入口核到。

25B总/3B活跃指DiT-MoE生成骨干，另有Qwen3VL8B、gen experts、ByT5/refiner/VAE，不能写整系统仅3B计算或3B驻留。报告E128A8、expert宽1024/shared1，注意仍dense；Wan2.2 3D causalVAE压缩4×16×16，相比4×8×8同输入少4倍空间token，不保证细文字重建或全部计算4倍加速。固定代码按num_heads12选32专家Top4无共享，否则选48专家Top5/hidden3072/expert1920/shared2048，异于报告128/8/1024；类默认40L/40heads是默认非实测权重配置。refiner默认2层双向Transformer/4096，文字上限512；ByT5输入1472映射4096，选引号文本最多256token，与Qwen实际序列接后截512，跨语言字节预算应测。sigmoid分独立后仍有TopK竞争/权重归一化，不能称完全无专家竞争。

## 数据、基线与协议

T1低分辨T2I50M；T2V/T2I低分辨20M/20M、高分辨10M/15M；联合SFT T2V/T2I/理解10M/15M/1M；I2I10M、联合I2I/V2V10M/10M；DMD+RL视频编辑128K。理解Honey1M子集覆盖OCR/General/Chart/Caption/STEM/Document/GroundingCounting，内部改CoT；T2I/I2I继承Mamoda2，T2V内部真实+合成。视频编辑add/remove/replace用LLM提示对、强T2V共享早期去噪、VLM重caption/过滤并交换方向；style采用公开资源，subtitle内部合成。没有所有上游骨干数据/跨阶段去重、teacher型号/早期共享步数与筛选阈值/完整采样日志，不能将各阶段简单相加当独立数据或把反向对算新独立场景。

VBench2.0五维Creativity/CommonSense/Controllability/Human/Physics；OpenVE431对/八类中只测spatially-aligned七类、MLLM指令/保真/稳定；FiVE100视频（74真26合成）/420对象提示对，YN/MC/并/交/Acc；Reco480视频指令对四类/三方面及九细项，主表Gemini2.5Pro重评，附表Flash原协议。GenEval六类静态组合遵从，ImgEdit/GEditEN编辑，理解MMVet/MMMU/MathVista/Hallusion/AI2D/OCRBench/MMStar；速度T2仅DiT去噪。训练混合奖励含编辑VLM、逐帧视觉质量、非编辑区域SSIM（遮文字）、OCR Levenshtein+VLM，优化奖励曲线不等独立泛化/人工质量。无笔画事件/严格汉字顺序/动作执行指标。

VBench Sora480/Kling1.6/ViduQ1/Seedance1Pro/Veo3与HunyuanVideo/Wan2.1/LongCat；速度另Wan2.2A14B/Hunyuan1.5/LongCat、VInO/OmniVideo2。OpenVE KlingO1/PixVerse/匿名proprietary与VACE/InsViE/Lucy/ICVE/Ditto/OpenVEEdit/Kiwi/UniVideo/OmniWeaving/VInO；缺类星号overall不能与全七类无条件同口径。FiVE TokenFlow视频编辑（非同名统一tokenizer）、DMT/VidToMe/AnyV2V/VideoGrain/WanEdit/OmniVideo2/Omni。图像SANA/FLUX/SDXL/DALLE/SD3/HiDream/Janus/Mogao/Mamoda2/Qwen/Seedream，GenEval匕首行有prompt rewrite；理解对Qwen3VL8B及Mamoda2，初始化/额外理解SFT不同，非严格联合正迁移因果。

T1低分T2I480/1epoch/lr1e-4；低分视频480/12fps/1ep/4e-5，高分720/24fps/1ep/2e-5；联合SFT720/24fps/2ep/1e-5。编辑先480/5ep/b8×128，再480→720/49–121帧/视频5ep/lr1e-5，图像b8×512、视频b1×512、采样1:9；表两类均写5ep与混采的具体曝光口径待日志。DMD+RL720/24fps/128K/1ep/1e-5，未给C/两lambda/奖励权重、更新步/精确分布。MoE消融64xPU/b512/AdamW固定5e-5/wd.01/clip1/最大像素407040，正文最多80K而F13横轴100K；主要T2I、早期T2V提前停止，无完整视频消融。速度均称单xPU/无额外所列工程优化，型号/精度/实际CFG/时钟及多次测量不全；T2明确排除文字与VAE。发布CLI默认93帧/50步/CFG4.5/bf16/VAЕfp32/24fps/seedNone、CPU文本offload与tiling；编辑README30步/CFG3。未运行。

## 主表与消融分析

T3 VBench61.64低于LongCat62.11/Veo66.72，Human84.56但Creativity53.81低于Wan55.25/LongCat54.73；不能全开源第一。T4 OpenVE overall3.86高于匿名3.73/Kling3.69/VInO3.21，但Add3.24低于匿名3.38/Kling3.32、Text3.99<匿名4.03、Style4.05<Kling/VInO4.34、Background3.31<Kling3.38、Creative3.87<匿名3.94。T5 FiVE-Acc87.41 vsOmniVideo2 73.53，各子项表内最高。Reco Pro Add8.83>VInO8.70但编辑准确9.02<9.29/质量9.13<9.30，Style9.44<9.52；正文四类overall皆最佳不成立。Flash附T13 Add8.80<VInO8.85、Style8.99<VInO9.10/ReCo9.17。GenEval.83低于Mogao.89/Mamoda2/Qwen.87；ImgEdit4.22/GEdit7.05，Compose3.28<VInO4.36、Action4.41<4.51。理解相对Qwen3：MMVet74.1→74.5/MMMU66.8→68.1/Math77→77.8/Hall59.2→59.5，但AI2D85.5→85.3/OCR912→897/MMStar71.7→70.7。T2 Edit69s/Distill9.2s实测7.5倍，vsVInO882s为95.9；T2V50步110s vsWan40步1366s。均只DiT耗时。

F13 Dense1.35B与E16A2/E32A4/E64A8在相同active标签下loss收敛有优势，2.2倍取横轴训练步而非实测时间；非最终25B系统全规模视频控制。F14固定最终模型初始化比较scratch70.79/78.17→Attn81.81/82.15→ExpertAttn83.26/82.27；加Drop82.66/82.30，DPG略高故非全面劣。~5倍是达到特定loss的步数，图例橙ExpertAttn+Drop实际最低而图注/正文称无Drop最低，需原日志解标注矛盾。T10四组合：umT5cross67.30/77.08，incontext67.93/77.76；Qwen cross65.52/76.44，incontext68.50/78.84，有交互效应；fromscratch指DiT设置，不证明移除编码器预训成本/参数差。T11图编辑Wan2.87→4.05但Action4.11→3.89；T12自合成对Reco在三类全指标提高，未固定unique量/teacher/曝光，不能只归共享早期轨迹。F15四步混奖励约百步超过teacher线，缺独立全基准与DMD-only/RL-only/两顺序同预算实验。

## 局限与优势条件

论文速度只DiT去噪且不同步骤/VAE/token/编码器，~15倍为30/4×CFG2前向估算，表列69/9.2仅7.5倍，不能互代。25B/3B不含AR等组件，内存须驻留全部专家。固定8文件推理代码48Top5/32Top4与128Top8冲突，README权重ComingSoon、无实际权重下载链接和完整trainer/合成/评测配置；普通last_hidden_state提示入口未核MetaQueries/gen-expert/参考视觉AR机制，不能作报告架构完整复现。F13最多80K/图100K、F14图例和正文最低曲线矛盾；全视频消融缺失，多seed/CI/硬件型号/原输出评分未给。Pro与Flash裁判能改变Add相对排名、匿名闭源版本限制复核；内部98%未给样本量/成功定义/人工盲评/CI。ByT5收益无移除控制，UTF8多字节预算、VAE高压缩对细笔影响未评。无音视频联合（列future）、严格笔顺或真实绘画数据，学术新颖性需与已存绘画/视频/文字基准比较。

在高质量图/视频配对、大吞吐硬件与可负载平衡的长序列上，稀疏FFN增加容量且不线性增加活跃FFN算量，dense先验上采样可能减少重新学习步数；高压缩VAE减少token，代价可能是细文字/小运动细节。共享早期轨迹合成倾向保大结构，适合局部add/remove/replace；也可能限制大结构变化。DMD约束teacher输出分布、NFT按复合奖励偏好微调可在少步速度与编辑质量间折中，但高训练reward不能保证独立质量，字幕正确也不保证逐笔事件。优势受分布/teacher/奖励与真实硬件所限。

## 可证伪实验和研究写法

固定上游初始化、unique对/帧曝光、VAE码率和数据，比较dense与MoE同active/同总参数/同实测FLOPs三套条件，报告路由负载、通信、显存及端到端延迟。对4×8×8/4×16×16做oracle重建与细笔/文字CER、时序一致，量化速度质量Pareto。共享初噪/早期k步/完整独立×数据量/去重/teacher因子实验，按动作/镜头/场景族留出。DMD-only/NFT-only/先后两序/联合在同rollout与训练GPU秒比较，锁C/lambda/reward、同独立裁判/盲评并测每类CI，重评四步所有benchmark，不能仅混奖励曲线。ByT5移除/字符或字节条件、引号/长UTF8截断/大小写/多语言、逐帧和逐事件OCR分开。严格笔顺用同终态异轨迹视频、规则SVG/VideoSketcher和强视频基线，测笔画事件顺序/可见性/持续性与真实执行；上述未运行。

Intro按视频算量、编辑对数据、少步后训三个具体瓶颈建立贡献对应；Method先AR/DiT/VAE再路由/上采样/条件，随后数据和五阶段训练、工程与多任务评价，组织清楚。四格条件注入实验展示交互、多judge附表展示协议敏感性值得学习；Claim须限制表内/对齐场景/子类及checkpoint，保留Style/理解退步，收敛步数与时间/总成本区分。FutureWork明确音视频、理解生成深度协同尚待解决；当前共用管线不自动证明双向协同。Limitations要补代码/报告不一致、裁判依赖/匿名基线、全视频消融和端到端实测，避免把广告98%当公开普适成功率。

## 实际阅读范围

v1完整38页PDF29710835bytes与HTML核心；Abstract/§1–9全部研究文字（含系统优化）、AppA1/A2全部文字与F1–24图注，T1–13全部单元和图14表、Eq1–3/NTP+flow作用；实际p5/6/11/14/15/19/21/22/23/25/34共11页核框架、路由、训练、速度/主要表、收敛/上采样/奖励曲线和Flash附表。未逐看全部定性视频帧/参考文献，HTML非标准span表另解析并对关键PDF表核看。GH ba41c0b完整66项树/55blob，mamoda25八文件清单、README全文、config全文、infer128–181/220–312/默认片段，MoE1–242主要前向/路由，transformer135–216/285–367/382–616/627–664，pipeline构造/引号提取/ByT5/文字编码/CFG调用指定段，refiner构造和层片段；根Apache2标识已核，未声称全文逐条法律解读。未全读repo的Mamoda2其他目录/实际权重、完整底层核、trainer/原日志/所有标注与模型执行；无独立复现。

## 参数、耗时与质量分别解释

| 项目 | 原证据 | 允许的结论 |
| --- | --- | --- |
| 参数 | 25B/A3B生成骨干，另Qwen3VL8B/ByT5等 | 不能写整系统3B或只需3B驻留 |
| VAE | 4×16×16对4×8×8 | 同输入空间token少4倍，细文字重建需另测 |
| T2视频编辑 | VInO40步882s，Edit30步69s，Distill4步9.2s | 表内DiT耗时95.9倍与7.5倍，排除文字/VAE |
| 正文约15倍 | 30/4×额外CFG前向2 | 理论前向次数估算，不等表中实测耗时比 |
| T2视频生成 | Mamoda50步110s，Wan40步1366s | 不把生成速度写成30步配置 |
| T3 VBench | 61.64，LongCat62.11/Veo66.72 | 表内较强，整体非最优 |
| T4 OpenVE | overall3.86，Kling3.69 | 只对齐七类；Add/Style/背景等未全胜 |
| Reco Pro Style | Mamoda9.44，VInO9.52 | 正文四类总分皆最佳与表不符 |
| Reco Flash Add/Style | 8.80/8.99，VInO8.85/9.10 | 换裁判会影响比较，保留原协议 |
| T9理解 | AI2D−.2、OCR−15、MMStar−1.0 | 不能写全部保留或全面正迁移 |

## 结构与初始化消融的真实范围

F13主要是在T2I、Dense1.35B及等active标签E16A2/E32A4/E64A8上比较训练loss，约2.2倍为达到所选loss的步数比。正文最多80K、图轴100K不一致，原训练日志待核；同active不自动等墙钟/总参数/通信与上游预训成本。最后E128A8完整视频消融未做。

F14随机取窄专家相对只迁移attention，GenEval81.81→83.26、DPG82.15→82.27；scratch70.79/78.17。Drop版本GenEval82.66稍低、DPG82.30反高。图例把橙色最低曲线标成ExpertAttn+Drop，正文/图注却称无Drop最低；保留标注疑问，不擅自改图或确定哪条训练轨迹。约5倍也是训练步数比，既有Wan预训练成本需单列。随机抽取不能保证精确保持dense函数。

T10四格条件×注入实验显示交互：Qwen在cross-attention下65.52/76.44低于umT5的67.30/77.08，配in-context后68.50/78.84高于umT5的67.93/77.76。它支持特定组合，不能说明任何VLM编码器都会独立优于文本encoder。T12本数据在三类所有分项优于Reco-Data，但unique量/teacher/曝光未完全对齐，不能只归共享早期去噪。

F15优化的混合奖励过百步超过teacher，缺DMD-only/NFT-only/两种顺序同预算结果和四步模型全部独立benchmark。教师分布可约束偏移；“强于KL”和“成本低一个数量级”仍需单独比较。

## 无独立论文制品的发布边界

主仓完整66项树/55个blob，mamoda25八个文件中有推理入口、MoE/refiner/DiT/pipeline。README权重表写Coming Soon，未给可直接下载的权重链接，未看到完整训练/合成/评分运行配置。提供使用示例不等于已发布完整报告模型。

[生成器固定源码](https://github.com/bytedance/mammothmoda/blob/ba41c0b90a2a0b626a21a4f36139275e9700e0c3/mamoda25/src/transformer_mammothmoda.py)按head数选32专家Top4或48专家Top5，与报告128专家Top8不同。代码类默认40层/40heads、命名20B或6B配置都不能当最终权重事实。未下载或执行模型，无据断言这些差异已影响正式实验。

[发布pipeline](https://github.com/bytedance/mammothmoda/blob/ba41c0b90a2a0b626a21a4f36139275e9700e0c3/mamoda25/src/pipeline_mammothmoda.py)核到普通文字last_hidden_state、refiner和引号ByT5；没有在所读入口核到完整MetaQueries/gen-expert与参考视觉进入AR的流程，参考视频VAE条件则进入DiT。ByT5对引号文本设256token预算，合并Qwen条件后总截512；UTF8多字节文字和长提示必须补截断测量。

根Apache2标识只说明当前代码根许可，未作所有上游模型与数据统一许可判断。训练/推理工程优化如FSDP2、USP、GroupedGEMM/SSTA/cache分别记来源；发布MoE朴素逐专家循环不能直接当生产优化核的性能证明。

## 对中文笔顺、跨文字和绘画视频的启示

本工作确实研究生成视频、视频编辑与字幕编辑；它扩展当前调研的视频部分。但字幕替换、静态词正确和帧间一致不提供规范笔画事件的直接证据。高压缩VAE可能丢失细笔/接触点，先做oracle重建；共享早期轨迹合成适合保持大结构，也可能限制应改变结构/运动的编辑，需按变形程度测试。

建立同终态不同过程的独立切分，与规则SVG、VideoSketcher及强视频模型对比；除OCR/VBench外，测笔画事件、可见性/持续性、接触与动作可执行。共享UMM收益还须固定生成/理解训练预算检验双向协同，Future Work本身承认更深协同有待探索。

追引DiT-MoE/RaceDiT/DiffMoE、ExpertBias/DropUpcycling、DMD/DiffusionNFT、OpenVE/FiVE/Reco、VInO/OmniVideo2、Wan高压缩VAE和视频编辑合成资源；引用不计这些工作独立精读。下一项L125 SenseNova-U1；保留完整未完成队列。
