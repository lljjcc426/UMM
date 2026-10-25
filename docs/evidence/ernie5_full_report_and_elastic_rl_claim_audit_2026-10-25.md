# ERNIE 5.0：完整报告、弹性实验与RL主张审查

第二百一十七批完成[L163](../reviews/L163.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/ernie5_full_report_and_elastic_rl_claim_audit_2026-10-25.json)。358目录（331论文／研究、27资源），322核心/327书面含未通过项；待完成核心深审9篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2602.04705)、[主源2](https://arxiv.org/pdf/2602.04705v1)、[主源3](https://github.com/PaddlePaddle/ERNIE)、[主源4](https://huggingface.co/baidu/models)、[主源5](https://huggingface.co/api/models?author=baidu&search=ERNIE-5&limit=100)。

## 研究问题

怎样以共享超稀疏MoE和统一分组自回归目标支持文字、图像、视频、音频的理解与生成，并从一次预训练得到不同深度/专家数/激活稀疏度的模型？

## 现有不足

异质模态有不同序列长度、注意力和生成粒度；分开训练/压缩多尺寸模型成本高，异步RL的长尾rollout、训练推理数值偏差、熵塌缩与零奖励难题影响吞吐和优化。

## 贡献

万亿级/激活<3%的模态无关共享MoE，NGTP统一NTP/MTP文字、NFSP视觉、NCP音频；弹性depth/width/sparsity子网共同预训练；SFT+UMRL，U-RB异步缓冲、MISC混合粒度重要性采样、WPSM软降权及AHRL提示。统一主要指共享AR骨干和目标，视觉终端仍有独立训练的diffusionrefiner。

## 输入、模块、输出与公式

文字离散token；图/视频由CNN+ViT与patchmerger提语义，再bitwise progressive多尺度量化，图K4、视频K16含4frame压缩；同尺度视觉bidirectional、跨尺度/帧causal，图视单帧视频；AR生成低分辨视觉后独立级联扩散细化。音频12.5HzRVQ首层蒸馏Whisper语义、残差codec声学；理解把同帧各级embedding相加，生成头按级预测再feedback，speakerembedding控音色。完整媒体结果未执行或播放。

## 模型结构

路由依统一token表征而无模态ID/专门专家手工分配；总层数/宽度/专家N与topk/精确总参数未披露。视觉tokenizer bit数/尺度序列和audio级数/vocab未完整给出。NGTP不等于每种模态同一token粒度；音频NCP在顶层附加heads，不把所有codec展平。全模态fromscratch骨干与外部Whisper语义教师并存。

## 数据分布与划分

预训练trillion级文本token与多模态instances，清洗/去重/安全/配比动态调整有说明，无逐来源完整名单、模态token量/比例与测试去污明细。SFT覆盖文字/视觉/语音多任务，verifier含rule/model；RL题数、奖励权重、hint来源/长度配置和训练预算不足以独立复现。不可由全模态概述推出具有实际汉字逐笔轨迹监督。

## 指标与评价协议

T1–2文本语言知识/逻辑/数学/代码/工具/联网，T3–4视觉STEM/document/general/video与base，T5GenEval、T6VBench质量/语义/overall，T7ASR WER及voice/audio理解，T8TTS WER；指标的文本正确率/音频WER不替代画面审美、说话人相似/MOS或因果笔顺。F8专家频率/F9top25%专家IoU/F10归一化熵属于描述性路由统计，未提供干预迁移因果结论。

## 对比方法

文本base对DeepSeekV3/Qwen3/Llama4/KimiK2，post对DSV3.2/Gemini2.5Pro/GPT5/Gemini3Pro；视觉对Qwen2.5VL/GLM4.5V/GPT4.1/Gemini2.5；图像HiDream/Flux/QwenImage，视频Veo3等；ASR/TTS对Qwen3Omni/KimiAudio/CosyVoice等。各项分数依作者表，训练数据/推理预算/闭源版本未严格同配；无同预算全模态联合vs分离模型消融。

## 实验条件和发布边界

8K预训练WSDwarm2K/peakLR1e-4/batch14M→56Mtokens/RoPE1M，32K/128K扩展cos1e-4→1e-5，routerbias1e-4→1e-5/MTP.3→.1。§3.3深度full75%/reduced25%，宽度/稀疏度各80/20；§6.4.2小实验深度80/20却称一致，报告内差异。Paddle4TP/12PP/64EP/ZeRO1/contextparallel/FP8/tokenizers独立nodes、FlashMask；>200%kernel/>20%e2e及>15%decode提升缺完整硬件/负载/计时表。

## 主结果

T1多数base强但C-Eval91.98<Kimi92.49、CMMLU89.69<90.61、MBPP79.10<79.36；T2SimpleQA74.01/Chinese86.03及MultiChallenge65.98等优势，HMMT79.58与AIME89.06仍落后若干参照。T5GenEval88.4→90.1<Qwen91；T6overall83.78→84.20<Veo85.06，即使semantic83.40>Veo82.49。T3CharXivDQ90.35→89.05；T7CommonEval4.39→3.74/SDQA86.44→77.58/Alpaca4.65→4.62/MMAU80.80→80.40/VocalSound91.48→90.73，后训练收益非逐任务一致。AISHELL1.75→.31最好，Wenet7.27/7.36仍逊Qwen4.69/5.89；T8TTS1.35zh/1.54en，en逊Cosy1.45。未独立复现。

## 消融及进一步实验

小MoE3.2B/active454M/64experts/topk8/250Btokens：T9base16layer1.945→elastic16 1.941、12layer2.137，仅.004差无seedCI，且无独立训练12层同预算baseline；T10base64 1.957/elastic64 1.964、32 2.218；T11basek8 1.945/elastic8 1.969、4 1.971、2 2.003、1 2.175。T12为另训ERNIE5.0-Exp：Full七项均75.55、ES25%74.43(-1.12)、EA35.8%75.17(-.38)；EA总参35.8%/激活53.7%不能当FLOPs比，抽取base后另有mid/posttraining，同策略不等于无需后续训练。F6mixedratio熵/accuracy改善无独立seedCI，WPSM/AHRL无完整独立因子结果。

## 局限与疑问

U-RB保留预设querygroup顺序、异步预发后续组/长尾partialrollout，unbiased指减轻快慢query抽样偏差，未给无偏梯度证明与完整staleness校正。Eq3将token级train-old/infer-old截断mask与GSPO序列比结合，j聚合符号未明；WPSM Eq4依组平均acc与单response低entropy降权，条件无逐条答对判断。AHRL Eq5 p=p_initial*exp(-gamma*t*pass_initial)：pass_initial为SFT固定pass@k；等于0时p永不衰减、接近0时极慢，正文逐步移除提示需条件，未披露边界处理。参数/代码/权重/全数据不足；PaddleERNIE README为4.5、官方baidu模型目录与ERNIE-5查询未找到5.0权重，不能拿4.5工具包当本报告可复现实现。

## 预期优势条件

sharedMoE可按token条件分享容量，NFSP/分组音频缓解长度；弹性可能减少重复预训练成本，提示可给零奖励难题初始路径。但需同输入数据/算力对照；路由IoU与平均分不能证明理解直接改善实际笔顺生成。动态笔画需因果动作和可见前缀定义。

## 可证伪实验

固定数据/总FLOPs比较共享MoE与分离专家及分离模型，测正负迁移；弹性各抽取尺寸对同参同预算独立训练/常规裁剪，分开pre/mid/post成本并报真实延迟。RL对U-RB/MISC/WPSM/AHRL析因，报告延迟分布/样本比/有效token和多seed，追踪初始pass=0组的hint比例及无提示测试。笔顺用同终态不同序、方向、回跳与风格泛化，单列执行视频和终态识别，未执行模型。

## 论文组织与Claim学习

报告从token组/共享路由到弹性训练、RL稳定与基础设施串联完整；适合学习按瓶颈组织机制。主张需分开AR骨干与扩散refiner、主模型与Exp、参数比例与FLOPs、后训练改善与个别下降；unbiased和collaboration应明确证据等级，公式退火需说明零边界。

## 实际阅读范围

唯一v1完整36页：正文§1–7全读、contributors和reference清单核，报告没有独立附录；10图全12张contacts视觉核，F7/Eq3–4p14、Eq5p15、F8–9p24、F10/T9p25、T12p27放大；12表全行及Eq1–5、未编号熵式核。核官方PaddleERNIE develop README与HFbaidu目录/ERNIE-5查询，未将4.5发布当5.0；未运行/训练/调用模型或下载权重。核心三遍和五书面完成，未做独立复现。

## 关键公式与实验边界

AHRL Eq5使用SFT初始pass@k固定量：p(t)=p_initial exp(-gamma t pass_initial)。若pass_initial=0，则任何t都有p(t)=p_initial。报告未交代该组的撤提示规则；这是一条公式边界，未据此推断实际训练失败。WPSM Eq4降权条件由query组平均正确率和当前response熵构成，缺逐条正确性的显式条件。

ERNIE5.0-Exp是独立实验版。T12 EA总参数35.8%、激活53.7%，抽取预训练base后仍有相同策略的mid/posttraining；激活参数比例不直接等于实际FLOPs/延迟。ES25%与EA结果及额外成本分开。

## 描述性分析与因果主张

专家IoU和归一化熵展示自发分工；理解/生成专家重叠较低，不能仅据共享池证明协同。归一化熵需要专家概率和为1，topk的token比例需明确归一化。视觉末端扩散细化、外部Whisper语义教师与共享AR骨干分开；主表也保留CharXiv/音频后训练负项。
