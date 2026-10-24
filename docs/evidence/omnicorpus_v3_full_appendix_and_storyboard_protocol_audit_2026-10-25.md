# OmniCorpus：v3完整附录、故事板与评测协议审查

第二百零七批完成[L172](../reviews/L172.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/omnicorpus_v3_full_appendix_and_storyboard_protocol_audit_2026-10-25.json)。358目录（331论文／研究、27资源），312核心/317书面含未通过项；待完成核心深审19篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2406.08418v3)、[主源2](https://arxiv.org/pdf/2406.08418v3)、[主源3](https://arxiv.org/html/2406.08418v3)、[主源4](https://openreview.net/forum?id=kwqhn2VuG4)、[主源5](https://github.com/OpenGVLab/OmniCorpus/tree/ce4a012c6adf7c298cd6943a7ad875ec1af1ab6b)、[主源6](https://huggingface.co/datasets/OpenGVLab/OmniCorpus-CC/blob/8038991c62db064e5469a8a509261d8f4e85fd61/README.md)、[主源7](https://huggingface.co/datasets/OpenGVLab/OmniCorpus-YT/blob/1a35a3e6d1614aead05c11d6f1aae83f7b893c1c/README.md)、[主源8](https://huggingface.co/datasets/OpenGVLab/OmniCorpus-CC-210M/tree/39c856327b0c18a89915fa4c94ae870d94e18601)。

## 研究问题

如何高效构建多源、多语言、大规模交错数据，并以可扩展筛选获得对MLLM有用的子集？

## 现有不足

英语网页占优、下载成本高，单一CLIP/规则过滤难控制多维质量；数据规模和下游价值不必单调。

## 贡献

增强正文提取→前置文字过滤/去重→图片下载过滤→多维文字过滤；人工反馈设计英/中规则和BERT评价；网页及视频关键帧/转录统一故事板。

## 输入、模块、输出与公式

网页HTML/视频与ASR→带元信息的交错文档；下游LLaVA式模型输出文字，视频故事板没有提供逐帧连续运动或笔画标注。

## 模型结构

增强Trafilatura正文/DOM密度补充、保留text/image/code/header/detail/quote/video/audio/table/list标签，chunk按上下左右线性化；前置粗文本过滤和MinHash.8去重，后图片下载/过滤与五BERT分数(广告/政治/毒性/NSFW/流畅)。human-feedback为作者找问题→写/测试规则迭代的Alg1，无reward/PPO/RLHF训练。基础LLaVA1.5 CLIPViTL336+已caption预对齐双层MLP+Vicuna1.5 7B，损失仅文本token，冻视觉训MLP/LLM。T5换InternViT300M448+InternLM2 7B，T7SFT再全模型训练；图片/帧输入文字输出，无像素或视频生成接口。

## 数据分布与划分

T1总8.6B图出现/1696Btoken/2.2B文档；CC3.3B/748B/988M(2013–2023-11/12)、CW3.2B/940B/1196M、YT2.1B/7.7B/10M。非100亿唯一图证明。T1 CW平均写2图/330token但3.2B÷1196M≈2.68、940B÷1196M≈786；总平均写574token但1696B÷2.2B≈771，无法单靠舍入解释，保留原数与冲突不擅自修哪一列。D4声称CC16M域/每域137文档、14M图域/615图，对应总量约2.19B/8.61B更接近全量而非CC，口径未说明。三个来源各100K文档LDA20topic/T15–17，T-SNE分离不等于真实分布/人口代表性。YT来源YTTemporal1B/HDVILA/HowTo/InternVid关键帧+转录。

## 指标与评价协议

T2/3/4两VQAaccuracy+两captionCIDEr的算术平均，不能称统一准确率；B1消融RICES检索示例、TextVQA明确提供OCRtokens且不后处理。T5改OpenFlamingo随机示例、TextVQA不含OCR，0*含两个无图文字priming。T7另12benchmark含不同尺度MME1602.3，不能横项平均。人工仅200个CC文档405图，图相关88.4/水印8/logo4/广告.2/字32.1/结构字22.7%，未评中文和YT全库。F4用自身审美/NSFW与文本广告/NSFW/流畅平均代理分数，非独立人工质量验证或真实运动指标。

## 对比方法

同基础骨干对MMC4/Core/OBELICS/OmniCC/YT，每组从不同池随机1M文档，未匹配图/token/FLOPs且无多seedCI。自然vsCLIP重排与全AR/crossattention(F6)交互；T5同时换两骨干并加LAION/纯文，T7约3.3MSFT混多种OCR/VQA/科学/纯文，不能把SOTA差全部归到交错语料或筛选。

## 实验条件和发布边界

图边≥150/aspect.5–2、aesthetic≥3.7/NSFW≤.8、pHash/dHash跨页>10去，粗文本过滤80%、MinHash去90%，BERT维度分层。B2仅给1M文档、16A10080G约1天，论文未给完整LR/优化器/batch/epoch/序列长/各runseed；Checklist“结果稳定”无误差条证据。T4 YT每例均匀六帧，其余帧丢弃。T2 common SFT LLaVA665K，interleaved SFT将caption/VQA拼成评测fewshot格式；T7另3.3M指令/全模型，不与T2同条件。C1假设10000CPU/1000GPU/3Gbps/每文2.97图，T9速度/过滤率作成本模型，不是实际跑完所有次序；T10最快①②④③2.31h，实际为保留多样文档选①②(③④)5.95h，不能写实际流程全局最快。

## 主结果

T3筛选池988M/600M/200M/40M/8M/2.5M四shot平均54.5/55.1/58.7/57.6/56/58.2，每次实际训1M；严格过滤收益不单调，非训练量规模曲线。T4 OmniCC4shot58.7vsOB58.2但0shot28.3<31.3/Flickr54.3<54.7。YT零shotOKVQA16.5/TextVQA22.9最高，但4shot40.1/41低于CC41.1/42，不能泛称所有VQA最好；4shotcaption83.8/36最低。CW接相同SFT MMBenchCN59.8→62.5/CMMMU23.6→24.9为小实验，不代表全面中文字形能力。T2 MMLU48.7/49.9→预训47.1/48.6，commonSFT50.4/51.2、交错SFT50.8/51.3；预训始终保持语言能力主张过强。T5 7B8shotVQAv264.7/TextVQA45.6/VizWiz52.2，对IDEFICS56.4/27.5/40.4有优势，OKVQA46.6<47.7，非全任务胜。

## 消融及进一步实验

F6全AR自然位优于检索，crossattention检索略优，图无逐点精确标读趋势；机制“阅读习惯/相关上下文”是解释假设。T2 commonSFT 0shot76.5/four73.9，交错SFT0shot74.5/four77.9，fewshot保留与zero tradeoff；高质SFT相同任务模板也需隔离。T7 OursScienceQA91.8*明确见过train图、MME1602.3/MMB76.5/MMBCN75.4较强，但GQA61.7/POPE85.4/MMVet41.3非最佳，额外3.3MSFT与骨干变化非交错单因子。T11 1000文档估FPR，英不完整句16.7%/引文6%/短段8.3%，中文去来源10%；部分零误杀不推出零总体误杀或高召回，missrate未给完整结果。正文近30英/40中规则，T11只列29英/15中，未称40条均可核。F7被修改或过滤比例约.82–.94，不等于删掉82–94%。

## 局限与疑问

v3全部39页10图17表/Alg1和A–E完成，2025正式PDF仍无法获取。规模/均值/域统计口径有冲突，来源更多/筛分数更高未独立证明全语言/唯一/事实质量；人审仅CC、无多seedCI、过滤因果作者§6亦认未解。视频时间戳保留弱时序线索，但六帧静态评测无连续运动/笔尖接触/规范顺序，不验证视频生成。公开CC为图片URL/文本，YT为视频ID+帧时间戳+转录，需要重取媒体，无长期稳定保证。HF210M目前auto gate，匿名raw卡401，CC/YT无gate元数据可见；未下载数据/权重或执行代码。v3datasheetQ43限非商用、Q48/49称metadataApache，AppE却CCBY；当前README/CC/YT卡区分数据CCBY4.0+ToU/代码Apache，原图权利另属来源；保留版本冲突，非法律结论。

## 预期优势条件

前置去重和多资源并行可省下载/过滤成本，多源长文与筛选子集能改善特定fewshot文字理解；自然序收益依接口/训练任务。若迁移手写/绘画，应从带时间戳视频另采密集事件，稀疏故事板可供语义步骤条件而不能当规范笔顺。

## 可证伪实验

同骨干/图/token/计算分别匹配，五评分维度×来源/语言×顺序因子，单独评每项和置信区间；先分开RICES+OCRtokens与random无OCR两个协议。加无交错预训而相同3.3MSFT对照，分离视觉/语言骨干。YT原时间戳密集/六帧/乱序对照，按笔画接触/遗漏/规范事件真值测；规则报告每条触发分母/误杀/漏检，成本保留假设和实测吞吐。仅设计未执行。

## 论文组织与Claim学习

数据工程账目与双语/视频来源动机明确；规模单位和表内比值须算术自洽，基准平均不能统称accuracy。把OCR提示/抽样/冻训切换写进主结果，前置过滤成本模型和实际选用次序分开。datasheet许可/非商用表述、§6无明显风险与A2承认残留/偏差需同步，当前发布卡和预印本分版本引用。

## 实际阅读范围

最新v3全39页§1–6、Checklist、A1全部59问/A2、B1–3、C1–2、D1–4、E；F1–10全部实际视觉、T1–17全部含T6提示/T9–10成本/T11所有44规则/T12–14五示例/T15–17各20topic，Alg1全部伪代码；39页13contact全看并F6/成本/域图原页放大。135条references清单/关键引文，非全引文原文。固定repoce4a012README全文，CC/YT版本卡正文/字段与三HF元数据；CC卡大YAML未逐行读，210Mraw401、OpenReview403明确保留。未全审代码/模型/数据、未运行推理/ASR/OCR/过滤API/训练；核心v3三遍及五书面完成。

## 预印本与当前发布

完整读到最新arXiv v3的39页，官方README确认ICLR2025接受；OpenReview页面需验证且API403，因此不把预印本等同已核2025正式修订。CC/YT公开卡分别提供URL和视频ID/关键帧时间戳/文字，未分发原媒体；210M当前有auto gate，匿名raw卡401。

## 评测和成本的可比性

消融采用RICES且TextVQA提供OCRtokens，T5换随机示例/无OCR，0*含文字priming。最终又换视觉和语言骨干并混纯文/LAION，补充SFT再加约3.3M样本，不可都归为筛选效应。C1成本模型最快①②④③2.31小时，作者实际为保留更多文档选择①②(③④)5.95小时。

T1 CW与总token均值无法由同表总量/文档数推得；资源表保留原数和算术不一致，避免擅自修正其中任一列。
