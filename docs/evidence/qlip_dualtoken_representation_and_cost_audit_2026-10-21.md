# QLIP与DualToken：量化接口、任务收益及完整成本审查

第一百零六批完成已有[L095 QLIP](../reviews/L095.md)、[L096 DualToken](../reviews/L096.md)固定版本核心三遍、实际框架/主表/消融与五条书面检查。[结构化来源与范围](../../data/qlip_dualtoken_representation_and_cost_audit_2026-10-21.json)。356条目录（329论文／研究、27资源），213核心/216书面含未通过项，143条未确认核心（含资源）。无文件删除、权重/图像数据下载、模型训练推理或原结果复现。

两项都研究静态图像与文本。共同问题是语义对齐与像素重建需要怎样的表示和训练接口，尚未验证规范书写视频或逐帧笔画事件。判断“统一”需逐项检查主干、码本、输入表示、输出头及优化目标。

| 工作 | 固定一手来源与身份 | 实际图表/阅读范围 |
| --- | --- | --- |
| QLIP | [2502.05178v1](https://arxiv.org/html/2502.05178v1)，2025-02-07；[作者项目](https://nvlabs.github.io/QLIP/)/arXiv标Tech report，正式会议/期刊未确认 | 核心§1–6/Eq1–9、附A–D/T8–14；实际F2/T2/T3a/T6 |
| DualToken | [2503.14324v3](https://arxiv.org/html/2503.14324v3)，2026-04-20；[正式ICLR2026 Conference](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0dbc636d5667a522cbfd92e7401ab704-Abstract-Conference.html) | 固定v3核心§1–5/Eq1–7/T1–6、附A–G/T7–14；实际F2/F4/T3/T5a/T11/T13；正式PDF下载不完整排除，未称正式全文已读 |

## QLIP：同tokenizer、不同下游接口

图像patch经ViT：CLS用于与文本全局特征对比，patch经MLP降维、球面归一和28bit BSQ，再经MLP/视觉decoder重建。阶段I重建/量化/对比联合；阶段II冻结视觉encoder、移除文本encoder，仅调量化瓶颈/decoder，加LPIPS/GAN。这样可将大batch对比与昂贵感知重建分阶段安排，但初始化仍复用MIM/EVA-CLIP等历史训练。

摘要称动态平衡，正文§4明确选post-hoc固定比例：先分别训练两个单目标，按收敛loss反比设置权重，实验αr:αa=1000:1；作者明确放弃在线adaptive梯度方法以减少额外反向成本。观察梯度量级差异可支持动机，固定loss值比例不保证梯度方向冲突消失。

下游分成三套实验，不能将它们的最佳成绩拼成同一模型：LLaVA主要使用倒数第二层连续特征；LlamaGen学习离散视觉码；UM3才以冻结tokenizer混合图文序列训练共享AR，且文本/视觉分别softmax。公开模型的BSQ `group_size=1`属于量化实现设置；没有完整UM3训练代码核实28bit隐式码如何映射到其有限视觉词表，不补写两个14bit分组等未证实细节。

| 原表证据 | 观察 | 对Claim的约束 |
| --- | --- | --- |
| T2 B16 | zero74.3/rFID3.21；BSQ rFID3.81，但QLIP PSNR23.16<24.12、SSIM.6286<.6638 | rFID改善与逐像素/结构指标存在取舍 |
| T2 L392 | zero79.1>VILA78，名义CR168为21的8倍；rFID1.46>1.25 | 高压缩比没有同时支配全部指标；骨干/分辨率/历史数据不同 |
| T3a比例 | αa:αr从1:0到1:1000，zero75.7→74.3、rFID367.8→35.3；1:10000时zero35.4 | 支持所测局部平衡，不支持任意权重均兼容 |
| T3c阶段II | rFID35.3→3.21，PSNR24.49→23.16 | 感知与像素保真目标应分开解释 |
| T6理解接口 | 倒二层量化前GQA61.2/POPE86.1/MME1398.7；最后层量化后40.4/50.6/677.17 | 语义层选择与量化都有影响；连续LLaVA成绩不能证明全离散理解无损 |
| T7生成 | LlamaGen-QLIP GenEval.48/DPG78.17；BSQ .31/34.03 | 支持该生成任务改善；VQGAN50M与QLIP/BSQ15M不构成完全同数据对照 |
| T5 UM3 | 五项语言均低于原Llama3.2；Wino54.22<61.48；gFID44.1劣于LlamaGen33.4 | 统一模型可行性已展示，正向协同/全面无损尚未证明 |

CR公式24*p²/bit是固定宽度名义压缩比，不代表实际文件大小或熵编码率；连续VAE位宽假设也影响比较。rFID评估重建，gFID评估采样生成；不将两者混用。

协议需保留差异：T1 LAION-COCO4M，正文/附录5M；加SA11M为16M，但T7列15M。UM3正文约18M，表中CC6M+SA11M约17M，过滤/舍入口径未完全说明。附T8是B8配置，阶段I120K×65536约7.86B曝光，与概述4B不能自动合并为同一设置；T3是2B短预算。附T9给UM3 b512/context4096/600K/AdamW1e-4及10K步混合退火60:1:3→12:1:3，不能据这些数字推完整历史训练成本。

## DualToken：双码本共享主干及其受控对照

浅第6层pixel RVQ支持重建，深第26层semantic RVQ对固定初始SigLIP蒸馏。两种量化特征按embedding维拼接，projector映到固定LLM宽度，故空间序列长度保持不变。生成使用两个独立的3层depth Transformer，各沿残差深度D预测，再用pixel decoder成像；需要2×D套残差预测，序列不加长并不代表计算免费。

256²为256位置/D4，384²为729位置/D8；VILA-U384用D16。语义teacher为初始视觉模型；训练实现还包含量化语义特征及pooler的MSE/负cos。论文Eq2将commitment下标重复写为Lc1+Lc1，固定代码实际把pixel与semantic两loss相加。这是原文公式与实现的区别，不能据排版推断程序训练了重复目标。

| 证据 | 观察 | 可支持及未支持的解释 |
| --- | --- | --- |
| T3层/目标 | 最后26层Recon+Sem zero72.3/rFID3.86；浅6重建+深26语义82/.25 | 层级分离在此配置明显更好；仍共享浅层，未证明梯度完全解耦 |
| T3指标反例 | 浅6重建SSIM.745，双目标.744；初始SigLIP zero83.2/量化后82.4，双目标82 | 没有所有指标无损支配 |
| T4相同LLaVA | 连续52.8、VILA48.1、sem-only52.2、dual53.9 | dual对VILA平均+5.8、对sem-only+1.7；VQA77<77.6/MMMU30.2<30.3，分项仍有退化 |
| T5b GenAI | 3B dual.68，受控VILA3B .60、pixel-only.55 | .60→.68为约13.3%相对、.08绝对；不能称13个百分点 |
| T6 MJHQ | 3B7.88优于VILA3B15.12，劣于Liquid5.47/Playground4.48/PixArt6.14 | 限定比较集合、分辨率/数据条件 |
| AppC同ViTamin | UniTok .38/78.6→DualRVQ .39/80.3→DualMCQ .25/82.2 | 量化器也影响收益，RVQ对UniTok rFID略劣；不可把全部差异归浅深层 |
| AppB多骨干 | RVQ8/16384码/2M样本，6种骨干约前1/4层优于中/后层，邻近层变化小 | 支持已测模型/数据上的经验规则，尚非任意架构最优层定理 |
| AppD实际成本 | 参数额外约276.1M；显存73.8→78.2G、生成11.42→12.97s、单forward328.98→337.20GFLOPs | 约+6%/+13.6%/+2.5%，三种测量范围不同，不能用单forward增长替代完整生成延迟 |

双独立encoder基线已有较强控制：AppF4将SigLIP-L冻结再学RVQ4，将SBER-MoVQGAN270M下采样/上采样从8改16并换RVQ4；匹配分辨率、16×16长度、embedding、LLM/head和训练数据。必须承认这些控制；后续仍可进一步匹配总参数、预训练成本及端到端延迟。不能把该基线误记为未适配、未训练的原始MoVQ。

T4 MME等已处于归一标度，原文所读范围未给完整换算，不与T5的原始MME分数直接相加。主要统一模型3B/7B采用Qwen2.5，T4控制采用LLaMA2-7B；不能将两组实验合为同一基座结果。附T12 GenEval .72/.75低于JanusPro.80；主表BAGEL等理解成绩更高，保留这些反例。

## 发布制品和训练条件的证据范围

| 制品 | 固定revision | 已核与缺口 |
| --- | --- | --- |
| [QLIP GH](https://github.com/NVlabs/QLIP/tree/cf86fcc5131c2bb008c349fe9456ccbd1e0e1619) | cf86fcc5131c2bb008c349fe9456ccbd1e0e1619 | 完整7blob树；README、BSQ group/index、视觉forward/decoder片段、example代码cell及许可证；未见完整原tokenizer/LLaVA/LlamaGen/UM3训练流程 |
| [QLIP-B16 HF](https://huggingface.co/nvidia/QLIP-B-16-256/tree/fbe07ff2d8c8798ca9f2f5c0699608bcc3da48a0) | fbe07ff2d8c8798ca9f2f5c0699608bcc3da48a0 | 卡/config/processor；28bit/group1；卡CC-BY-NC4，GH为Nvidia Source Code License-NC，按制品分别记录 |
| [DualToken GH](https://github.com/songweii/DualToken/tree/499e5b1d716bb72f5e5e2a91eae78ab53cf2ef3d) | 499e5b1d716bb72f5e5e2a91eae78ab53cf2ef3d | 完整241blob树、README/run.sh/256config、指定视觉core/tower与train stage1 loss；tokenizer训练/推理代码已发；统一MLLM完整代码/权重仍为will release，HF空链接不能证明已发布 |

DualToken附T13 tokenizer AdamW/lr7.2e-5/b64；MLLM I projector1e-3/b64、II projector/LLM2e-5/b256、III生成projector/head1e-4/b128，IV-1/IV-2全projector/head/LLM1e-5、b512/256。当前`run.sh`则8卡每卡32、10M样本、20epoch、β.5/.9、wd1e-4、warm10000、gan从0。实际脚本是可研究资源，是否等同最终主表协议尚未确认，不能擅自替论文选一个数。

Tokenizer约ImageNet1K+CC12M+LAION50M，MLLM又用内部2M VQA、审美/IFT及公开多数据源。所谓10%数据不包含继承SigLIP预训练；完整去重、总步数与混合比例尚未齐全。未下载检查点、媒体数据或运行训练，静态源码解读不冒充复现。

## 可检验假设及研究写作

QLIP假设是通过预算可承受的训练安排获得语义/重建折中，需固定历史初始化、码率与token/FLOPs，比较单目标、固定/在线权重、阶段冻结，并报告梯度方向和任务Pareto曲线；连续与离散理解接口必须分别测试。DualToken假设是浅层外观与深层语义互补，需同层/浅深、单/双码、等容量head、打乱语义目标、两encoder等预算控制，区分层级、额外监督与容量贡献。

两者均需测试小字/细笔画/未见文字体系、OCR与有序CER、语言回退、同延迟/显存质量。书写视频另建笔画身份、抬落笔、时间可见性和执行约束真值，保留规则SVG与专用模型强对照。以上为设计，尚未执行。

可学习的Introduction以观察到的表示/资源冲突提出局部机制，Method明确接口与优化阶段，实验分别支持主效果与机制。Claim用比较集合、绝对/相对增益、量化前后及成本范围限定；Limitations保留负结果、内部数据、初始化历史和未公开训练细节。当前研究证据支持若干静态任务改进，规范时序能力需要独立验证。
