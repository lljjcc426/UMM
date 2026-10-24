# LongCat-Flash-Omni：阶段取舍、首包时钟与服务身份

第一百七十四批完成[L162](../reviews/L162.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/longcat_flash_omni_stage_tradeoffs_latency_and_service_identity_audit_2026-10-24.json)。358目录（331论文／研究、27资源），280核心/285书面含未通过项；待完成核心深审51篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2511.00279v2)、[主源2](https://arxiv.org/html/2511.00279v2)、[主源3](https://arxiv.org/pdf/2511.00279v2)、[主源4](https://github.com/meituan-longcat/LongCat-Flash-Omni/tree/f6f1f0fbe40da06b25d08033bd8c6d27f352dff0)、[主源5](https://huggingface.co/meituan-longcat/LongCat-Flash-Omni/tree/f65b9038a559d3624d5e52fad28bbe083eb2341e)、[主源6](https://github.com/XiaoBin1992/sglang/blob/06a2f9b6105fbdbbac1abd0a0e642531ab255d3e/python/sglang/srt/models/longcat_flash_omni.py)。

## 研究问题

560B稀疏底座如何同时处理T/I/V/A理解与字—声输出，保持语言能力，并在VAD/网络/视觉压缩约束下提供可打断的多轮视听对话？核心是离线与流式输入融合及语音合成，没有图像/视频生成头或笔画轨迹输出。

## 现有不足

声学序列比文字密、视觉空间与视频时序异质，简单一起训练可能产生模态干扰；离线视频QA不能直接支持持续prefill、轮次检测和低首包交互。作者由语言→离散语音→图像→视频→长窗→连续音频对齐逐步引入难度，用MDP缓解不同模态负载与显存不均。论文关于无单模态退化的表述需受分项实验限制。

## 贡献

沿用LongCat-Flash的MLA/shortcut-MoE/零计算expert；637M原生分辨率ViT、连续FSMN音编码、16.67Hz四码本直接code2wav，文字/语音共享LLM；分阶段earlyfusion与音—视chunk交错；联合多头DPO；模态解耦HSDP+PP/CP/EP与chunk ModalityBridge；稀疏/密集采帧、推测prefill→decode和回滚/打断；UNO及真人交互协议。均需与前作codec/ViT/Optimus及服务工程分开归功。

## 输入、模块、输出与公式

图/帧→nativeViT→projector/后压缩，声→16kHz/80维Fbank、10ms步长、拼接stride8即12.5Hz连续feature→FSMN→projector，与字embedding及时间戳交错送LLM。LLM输出文字及1语义+3声学码本，16.67Hz每步四码；语义与声学有一步delay，发布postprocess用当前semantic和下一步三acoustic反移后扣32偏移→24kHz codecdecoder。SGLang实际四head在同一LLM步内逐头加入前一head的embedding，并非四个互相独立的分类器。输出字/声，无像素视频/图像或在线笔顺。

## 模型结构

论文560B总、18.6–31.3B激活/均27B；HF根28层h6144/64heads/MLA qrank1536、kvrank512、512非零expert+256identity零expert，top12跨两类选择，零expert不做MLP但仍有路由/加权。HF参考router用softmax+correctionbias选topk，权重取原score再norm/scale6。视觉32层h1280/16heads/patch14、2DRoPE/SwiGLU/QKnorm，训练patch576–5832、尺寸112整除；视频temporalpatch2/默认2FPS/至少16帧，再按token预算插值压缩。发布VisionProjector按width两patch合并到2h，经MLP投6144，不能擅自当常见2×2四patch归并。音FSMN22层/proj1536/FFNh6144，最后6层各一帧lookahead，输入拼接另有左右7帧，不能把一层lookahead称全系统仅80ms。audioencoder与decoder约600M级，未独立重数总参数。

## 数据分布与划分

§3.1称多模态语料>2.5T tokens；各阶段消费另有文字重用，不能把语料和训练token当唯一去重数。语音原始数千万小时，经VAD、双私有ASR一致性、强制对齐/长度比0.5–99.5百分位、10秒间隔合并及按标点交错；长窗阶段用>10M小时中英处理音。图文SigLIP/重caption/聚类及200K中文词汇均衡，交错原始集删约74%；教育视频ASR/OCR提图文。OCR含手写/数学/多页2–6页，bbox归一0–1000、GUI动作与状态预测；STEM15M图文对。图SFT约3M，视频3M池/48能力标签→约700K，视声QA和合成语音及真人修订跨轮视频对话；声优录情绪/方言→专TTS→合成对话。DPO每prompt6rollouts，人工+模型评分，无完整偏好量/去重/源实体隔离清单。UNO1880人工题/44task/98%跨模态；CMMLU声续写1200合成题1shot，非全CMMLU文本测试。

## 指标与评价协议

T1结构、T2计算TFLOPs分布、T3–4显存GB；T5图像VQA/OCR/文档错误率↓/bbox grounding与GUI，RefCOCO-avg为RefCOCO/COCO+定位平均，不能与生成mask IoU横比；T6视频正确率，无字幕、with/without audio且所有视频最大32Kcontext。T7ASR/TTS中CER英WER，TTS是给定文字teacherforcing+speechprompt后ASR回译误差，不是自然对话质量；T8声入文/声出CMMLU准确率受TTS/ASR影响。T9识别CER/WER与翻译BLEU，T10–11声理解/QA/安全/指令混合量纲；T12–13文本acc/F1/pass@1/AIMEavg@10/GraphWalksprecision，未拼成一个平均。T14OmniBench内部修正评分版。T15每模型200段约3分钟、四场景各50段，10对话员、250用户每录像3标，0–3自然流畅分/95%CI；T16专家六维goodcase百分比，CI计算/按对话与评分员聚类未给。

## 对比方法

图/视频用Qwen3Omni、Qwen3VL235B、Qwen2.5VL72B、Gemini2.5Pro thinkingbudget128/Flashnonthinking、Seed1.6/GPT4o1120；星号引他报告。声另KimiAudio/StepAudio2mini/GPT4oAudio。文本比同系列LongCatFlash及DeepSeekV3.1/KimiK2/Qwen235B等，按对应模式限制但非同训练token/算力。真人对比Doubao/GPT4o/iFlytek/StepFun/GLM/Qwen2.5/3各产品服务；PDFp31中标为GPT4o的URL是chat.chatbot.app/?model=gpt-4o，非OpenAI域，尽管正文称官方平台，服务提供者及后端版本身份需进一步证据，不能直接视作官方ChatGPT。评测日期为2025年8–9月，不作为当前产品能力排名。

## 实验条件和发布边界

PT0约16T纯文/恒LR；PT1约5.1T、text:audio2:1，L=1.75Ltext+.25Laudio+1.5Laudiotext+.1Lfirstsemantic；PT2>3T、text:vision:speech2:1:1、ViT/projector/LLM联合训、visionloss.25；PT3 .33T退火+PPLgap动态采样；PT4 100B扩32K/RoPE1M→5M，再20B扩128K/10M，加入25%longcontextdata并保2:1:1；PT5冻结LLM训练连续audioencoder/projector。SFT冻结audioencoder其余更新，1epoch/b1024/AdamW(.9,.95)/wd.1/peak1e-5/warm4%+cosine；DPO1epoch/b256/peak1e-6/warm3%/KL.1，公式L=αLtext+βΣ四Laudio、α:β1:1；无1/4归一，不能将该比例解释为文本与全部音头总loss五五分，训练代码未核。HFf65b9038a559d3624d5e52fad28bbe083eb2341e 104files/80主shard及声/视觉/codec元数据与5组配置已核；GHf6f1f0fbe40da06b25d08033bd8c6d27f352dff0 43树项/36blob/1codec子模块，相关源码选读，未下载权重。外部SGLang开发分支固定06a2f9b6105fbdbbac1abd0a0e642531ab255d3e，音head与状态/输入相关段已读。demo seq_length34816/max_new4096/max_frames128/maxvision28672/声上限120s配置，与模型128K支持和论文32Kbenchmark分开；README FP8≥8H20-141G/BF16≥16H80080G为部署建议。

## 主结果

全部16表逐行收录。T2音/视觉/LLM平均3.29/89.85/3531.32TFLOPs每microbatch，分布长尾；T4累积显存137→134.1→89.4→80.1→73.6→69.1GB，是顺序组合收益。T5 Muir77.1/Mantis84.8/Refbbox93.9强，MMVet69<Gemini80.7、DocVQA91.8<Qwen3Omni95.7、OCR84.9<85.5，GUI亦非全胜；GHREADMERefCOCO92.3与论文93.9、Androidhigh75.6仅README，版本/协议映射未说明。T6短视频75.2/86.2/82.2均最高，但w/audio78.2<Gemini80.6/78.5，无音76.2<QwenVL79.2，STEM67.1/67.5低于Gemini75.6/79.4；正文VideoMME最好omni措辞需限定。T7/8阶段非单调：PT1→2英TTS4.72→8.64退，PT3→128K英TTS3.68→7.38、声续写text92.8→90.4/audio92→90.4退，伴数据/步数/窗口变化不能单归新模态。T9十个ASR子项对Qwen3Omni仅AISHELL1 .63<.84，一胜九负；中英Fleurs3.99/5.02>2.20/2.72、CommonVoice4.98/13.59>4.31/6.05，正文持续优于对手不受表支持。T10 TUT65.43最佳，MMAU75.90<Qwen77.50、MELD54.60<Kimi59.13；T11强项Alpaca4.94/Adv100/IFEval77.99但其它QA非全胜。T12比纯文18项11升7降；T13比纯文17项13升4降，其中IFEval82.44<89.65、COLLIE45.69<57.10、Meeseeks39.05<43.03，三项指令全退，Zebra86<89.30，绝对无退化措辞不成立且增训预算混杂。T14对Qwen3四项全好，GeminiPro只Daily82.38>80.61，其余61.38<66.80、60.89<63.96、49.90<64.48；UNO也低于Flash54.30。T15真人1.37[1.30,1.44]列第三，低Doubao1.92/GPT4o标签1.79、高Qwen3 .81；与iFlytek1.25CI重叠，未经配对检验不全称显著。T16旁语言91.5最高、memory94.5较强，但准确36<多数对手且<Qwen3 40；实时49.5/类人62.5有差距，作者已承认抢话/语音瑕疵/文字数字识别弱及过度附和。

## 消融及进一步实验

受控证据主要是T4累积显存消融与F10在8K下CP/EP的MoEGEMM曲线（选择EP32/CP2），非所有设置减少CP都对每算子严格更优。约75%为groupedGEMM算子MFU，FusedRoPE3×、detFA约非确定版.8×、MDP>90%纯文throughput均为作者指定条件报告，未完整硬件/全系统tokens每秒置信区间，不能把75%写成端到端MFU。T7/8是不同阶段checkpoint，非同token组件开关消融。无同预算课程顺序/earlylatefusion、连续离散音、PPL采样、零专家、长窗、jointDPO vs分训、各音head权重、VAD阈值/推测切换/回滚/打断代价分项表。§3.2.6文字称单独projector预训差异很小，未给独立数字；承认文字试验但不升级受控量化。

## 局限与疑问

1) 字/声输出统一不能支持视觉生成或笔顺监督迁移已成功；默认2FPS+temporal2+token压缩与回话时.5FPS可能漏快速书写和短暂遮挡，timestamp不能补未采帧。2) 感知改为连续feature后音encoder冻结SFT，课程阶段还变数据/LR/步数；语言与声退化反驳绝对Claim，不能反推多模态必然有害。3) 100ms是600–700ms VAD判定之后，F11画的首包箭头从用户停说开始，需分清clock起点；缺网络/客户端/尾延迟/并发/回滚成本。4) 根demo一次性预处理、async_generate(stream=False)及整段codecdecode，没有展示论文服务的实时VAD/推测rollback；外部SGLang提供音head/状态机制，不代表商业服务全链已开源。5) 内部修正OmniBench需发评分diff，UNO人工新建不能单独保证训练无污染；真人产品脚注身份、不同日期/网络/对话员应控制。6) GHREADME与PDF分数差异、当前资源配置/论文采帧/128K与32K评测映射需说明，未跑模型不能给速度/可用性实测结论。

## 预期优势条件

在中英语音输出、跨轮视听理解与高并发大集群，四码本低频AR+直接GANdecoder、增量prefill和模块分离可能改善首包吞吐与表达；earlyfusion+多图/视频数据可能促进部分推理/知识任务，具体指标支持有条件互利。与汉字任务相关可迁移点是时间戳、流式观测、遮挡记忆、动作—声解释和多任务负载；要生成合法笔画需额外轨迹/图像输出、笔画身份与顺序监督，书写帧采样提高并量化成本。

## 可证伪实验

Q1课程/联合DPO是否带来互利：同早期textcheckpoint匹配增训token/FLOPs/数据质量，平衡声/图课程与混训/反序，分开固定textonly续训及多模态，保T12/13各项尤其三指令基准；jointDPO按显示逐头和、按1/N归一、分头优化对照，共享偏好pairs并测文本—声一致性/发音/韵律。若收益可由额外文本预算解释或指令持续退，收缩互利Claim。Q2首包改善是否跨服务可迁移：同硬件/网络固定VAD阈值，开关增量prefill/推测切换并以停说/VAD/服务发包/客户端播放四时钟报p50/p95、错抢话率/rollbackFLOPs和并发吞吐；同录像回放盲序产品评测、核GPT4o脚注服务身份、按对话/评分员cluster bootstrap。书写视频做不同FPS/temporalmerge/压缩等预算对照，测短动作/笔画漏检和遮挡后顺序，而非只问文字内容。上述均为拟议实验，未执行。

## 论文组织与Claim学习

系统报告按结构→数据课程→SFT/DPO→基础设施→服务→离线/真人多层评测组织可学；冻结关系F5、输出头时间错位F6、服务时钟F11和逐维失误讨论有信息量。表12/13下降、表9识别退步与无退化/持续领先措辞冲突，应逐项限定；图1截断纵轴仅作概览，不能把柱差当绝对误差改善。逐头loss求和需明确归一，benchmark版本、脚注服务身份、产品日期/采样上下文与延迟起点要一并列。作者已报告过度附和等局限，后续工作不将这些重新包装为从未提出的缺口。

## 实际阅读范围

v2完整HTML研究§1–8全部文字、16表全部行、两显示目标式；F1–12全部实际图视觉阅读（10位图含F3/4子图，F6/F9用完整40页PDF第13/20页，F10另第21页；第30/31页交叉核T13–16与产品脚注）。贡献名单仅核范围，参考相关追引；未称PDF40页逐页视觉检查。GH43树/36blob/1固定codec子模块元数据；README全文、demo全文、audioadaptor全文、交错converter全文、postprocessor全文、视觉projector与native相关段、HFrouter相关段、datautils的视频采样、FeatureProcessor/拼接配置与audioframe计数相关段选读；SGLang固定开发分支audiohead/生成状态接口相关段，未称全仓逐行。HF104文件清单/80shards与根、声、视觉、预处理、codec五组配置核；子模块实现、全SGLang/trainer/权重未读或执行。核心三遍与五项书面完成，未独立口试、训练/推理/复现。

## 证据边界

16张原表和两显示公式以结构化证据保留。完整研究内容与服务代码可得范围分别记录；100ms为VAD判定后口径，公开demo调用stream=False。GPT4o脚注域名及表格分项均核到完整PDF，避免把HTML转换问题归给作者。

## 追引

LongCat-ViT、LongCat-Audio-Codec、UNO-Bench及Optimus/MDP为配套与机制追引，尚未作为本批新论文全文验收。
