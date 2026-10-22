# DeepGen 1.0：SCB、多奖励RL与基准提示独立性审查

第一百三十五批完成[L121](../reviews/L121.md)明确范围核心三遍和五项书面记录。[结构化证据](../../data/deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.json)。357目录（330论文／研究、27资源），244核心/247书面含未通过项；未确认核心86论文／研究+27资源，资源另审。无新增目录、删除文件、下载权重或独立结果复现。

来源：[v2完整21页](https://arxiv.org/pdf/2602.12205v2)、[主代码固定fbaaaf4](https://github.com/deepgenteam/deepgen/tree/fbaaaf4ae1c79450d6a34b30beb4f59840568c69)、[独立RL固定c4d5dc2](https://github.com/deepgenteam/deepgen_rl/tree/c4d5dc27d699870ddac4bcb8ceda2e240773957b)。正式会场未核，按技术报告。

## 研究问题与贡献

在较小VLM+DiT预算统一静态文本生图、图像编辑、知识推理生图/编辑和文字渲染，改善轻量条件接口的信息损失与长RL训练能力漂移。五种生成任务不等于独立验证了理解任务、中文规范笔顺或生成视频；输入参考图/输出RGB，未建模真实笔画时间和动作。

仅取VLM单层或固定query可能压缩层级语义/细节，轻量模型依赖已有强VLM/生成器仍需对齐；单一偏好奖励与持续RL可能偏离原SFT能力。作者以多层通道融合、128学习token、分阶段数据和多奖励带监督锚点缓解。总成绩同时受预训练初始化、专门数据和训练预算影响，无法从参数标签较小推出各模块单独因果或总训练成本优势。

SCB从六个VLM hidden层沿通道拼接，含128可学习think tokens，接投影和6层Transformer连接器作DiT条件。PT只训连接器/query；SFT训DiT/连接器和VLM LoRA；RL以MR-GRPO组合组内两两偏好胜率、OCR、CLIP，逐奖励组归一化→加权→批归一化，并结合CPS随机采样、参考速度约束与持续flow-matching SFT。CPS与解耦归一化为采用的同期方法，不能全归该文原创；think tokens无显式可读CoT链。

## 方法数据流及模型结构

文字/可选参考图→Qwen2.5VL embedding并在序列末尾加入128学习嵌入→一次VLM forward取六层整个上下文（包含query）→通道cat→projector_1→Transformer connector→均值池化头与序列头→SD3.5M Kontext DiT；参考图另经冻结VAE提供latent，目标高斯噪声多步速度更新→VAE解码静态RGB。输入编码、query表示、去噪步、真实视频时刻分别定义。实际p4/6–14/19–21共13页核框架、11表、RL曲线和公式。

3B Qwen2.5VL +2B SD3.5Medium（从Skywork UniPic2-SD3.5M-Kontext-2B初始化），5B是骨干近似标签，未独立列连接器预算。公开HF VLM36L/hidden2048/16Q2KV/FFN11008；选择hidden indices35,29,23,17,11,5，非仅最终query/最后一层。连接器hidden2048/6L/32heads/FFN11946，输入12288→2048单Linear，另输出pooled2048与sequence4096。论文Eq1写前置两层MLP，实际源码及HF连接器是单Linear前置加两个输出头，差异保留。DiT24L/24heads×64/16latent通道/patch2、joint4096/pooled2048。论文SigLIP表述不代表实际加载预训练SigLIP连接器，构造为随机初始化ConnectorEncoder。VAE始终冻结；SFT VLM基座冻结加LoRA r64/alpha128/drop.05，不能按正文unfreeze entire model解释全参VLM训练。

## 数据、指标、对比与条件

PT35M生成（2M/6M/10M/5M/12M五源）+6.6M编辑，后者含1.1M内部数据，SFT复用编辑6.6M并列生成11M、UniReason生成150K/编辑100K、文字560K。生成SFT含10M内部真实长短提示3:1、BLIP60K/ShareGPT45K/Echo100K/OpenGPT40K及NanoBanana50K；文字500K由Gemini2.5Pro组提示/QwenImage合成，另中文诗/海报60K。~50M为新增训练池概称，不含已预训骨干全部数据，也不等累计样本呈现次数，跨阶段去重未公开。数据HF固定revision仅README/图/.gitattributes三文件，卡称仍上传；不能记为50M数据已公开。RL YAML包括UniGenBench general/ocr、CoRE，辅助SFT含Geneval_t2i.json与banana_UniGenBench路径；实际提示交集另单列。

T1 GenEval组合遵从、DPG长提示、UniGenBench十类生成，ImgEdit和GEdit-EN编辑；T2 WISE知识推理（1000提示）/T3 CoRE八类Qwen3VL32BThinking裁判；T4 RISE327条/UniREdit2700编辑；T5 CVTG-2K英语静态文字Word Accuracy、向上NED报告值与CLIPScore。词准确率不可写成汉字/字符逐笔正确率，CLIP整体语义不替代OCR或事件顺序。原代码仅推理生成样本，最终评分转各官方基准，裁判版本/抽样与不确定性不足；本轮没执行评分。

NanoBanana/GPTImage1/Seedream4/FLUXKontext闭源与JanusPro/ShowO2/BLIP3o/MetaQuery/OmniGen2/UniWorld/BAGEL/XOmni/LuminaDiMOO/Mammoth2/LongCatImage及Edit/HunyuanImage3/ZImageTurbo/QwenImage及Edit2509/GLMImage；按各表任务和版本比较。T1/2奖牌明确排除闭源；BLIP3o等论文私有训练版本与公开checkpoint差异引用已有L117审查；不把3B+2B标签与80B MoE活跃/驻留预算直接等价。

T9 PT200K迭代/lr1e-4/batch512、SFT400K/lr5e-5/b768，均64H200、512、AdamW/.05wd/clip1/cosine/warm ratio.01，SFT动态长宽。正文两阶段各20K warmup，与T9/源码比例推算2K/4K不符；公开PT累积4、每进程batch4且推荐64进程推算1024，异于表512，需运行日志确认，SFT累积3推算768。TRAIN.md的betas32/warmup1.0等表格错位不作事实。T10 RL G8/512²/50步/CPSη1/时间步比例.6/1500更新/lr2e-6/b256/beta5e-7/clip1e-4/SFTλ1e-4/每步/ZeRO2/bf16，消融仅1000更新。公开train.sh epochs10且max_steps默认-1，不能据此称完整复现1500步。原生及diffusers推理50steps/CFG4/seed42，GenEval每提示4张。未测端到端延迟/显存或复现。

## 主结果与消融的真实范围

SFT→RL：GenEval .86→.87、DPG87.05→87.90、UniGen74.18→75.74、ImgEdit4.09→4.14、GEdit7.12→7.17、WISE.72→.73、CoRE45.7→46.5。代价：WISE Space.82→.70，RISE13.3→10.8（四子类均降），UniREdit77.5→75.7；不能写全面无退化。WISE较Hunyuan.57的28%为相对提升，UniREdit较Qwen56.5的37%取SFT77.5，不能归RL75.7。CoRE LongCat52.2更高；DPG Qwen88.32、闭源Seed88.25更高。CVTG词准确.6605→.7533/NED.8426→.8936/CLIP.8227→.8278，CLIP表内最高，但词准确低于Hunyuan.765/Qwen.8288/LongCat.8658/GLM.9116等。F5/F6训练曲线有波动，不能称每一步稳定提高；F6起点约74.7、无SFT末约74.55与T7该行74.33不完全对应，保留原图表未强配。

T6去SCB DPG87.05→85.55/GEdit7.12→6.75/WISE.72→.70/RISE13.3→12.6，但GenEval仍.86；去think WISE.68/RISE11.7下降，GenEval.87反高于完整.86。去VLM激活各任务小降；无多种等参数连接器、层数和token长度控制，不能证明latent推理机制。T7全部1000步：完整DPG87.75/GEdit7.05/Text35.06/Overall75.69；去SFT87.40/6.99/33.33/74.33，去速度约束87.32/7.02/32.47/75.07，去逐奖励归一化87.73/7.02/32.18/75.27。支持所选配置的局部贡献，无多种子CI，且完整1000步GEdit7.05低于T1 SFT7.12；不将1000步表与1500步主结果混合。

## 局限与待解决问题

公开RL general7139行/ocr2861行，与官方UniGen600测试提示经strip/空白折叠/casefold比较，有3条完全相同（test201/203/204对应general行6869/6932/6938），OCR集0条；可确认发布文件交集，最终运行是否采样这些行/对分数贡献需日志，不能把整个结果判为泄漏或宣称独立性已证。CoRE/Geneval及banana_UniGenBench原清单未齐，语义近重复未测。Eq3最大化式接Eq5最小化loss的符号不清，源码策略负号及正速度约束澄清；CPS logp省掉1/(2σ²)改变时间权重，该项在新旧残差差里不作为加性常数抵消，属代理。Eq4裸速度MSE与默认源码除2std²+1e-7的v-based约束不完全一致，不能泛称精确轨迹KL。PT批/暖启动/投影描述差异、数据未全开/私有先验、无理解保留主表/长时视频/严格笔顺评价、无等FLOPs与统计显著性限制结论。

## 优势条件、可证伪实验及论文写法

若较小冻结/LoRA VLM不同层含互补的细节与知识，多层全序列条件在充分对齐数据下可改善长提示、编辑和知识生成；强OCR奖励可优先改善静态英语词正确性；奖励归一化在不同尺度时使权重较可解释，SFT锚点可能缓解RL分布漂移。优势以初始化、训练池、提示分布、奖励裁判和预算为条件；与纯query接口的成本/容量应控制，现有消融不保证所有任务单调提高或真实视频动作可执行。

固定相同初始化/训练曝光、数据与预算，比较单层、六层等参数projector、whole-context/query-only、随机/学习128token、显式CoT并分别报告参数/FLOPs/输入长度和生成理解双指标；多种子配对CI。RL交叉奖励权重、SFT比例、KL形式与真实高斯/残差代理，在同时间采样/预算下测所有生成编辑子类和独立OCR/人工；对RISE与Space退化画Pareto曲线。先去除确认3条交集，并取得CoRE/Geneval/banana原提示，对train/test做精确和语义去重、组合/知识族独立切分和未见基准，重新训练比较，记录测试用于选模频次。数据量按unique/重复曝光/上游预训分列。中文视频先做oracleVAE细笔重建与静态OCR，再同终态多过程输入，规则SVG/VideoSketcher/强视频基线测笔画事件、可见性/持续性/顺序与执行；上述为设计，未运行。

Intro从大模型成本/小接口瓶颈到可检验模块；Method按SCB、PT/SFT/RL、数据和五任务评价逐层组织；将T6结构与T7训练消融分开、附录公开数据配方和超参值得学习。Claim必须给范围：开源对手排名、相对提升对应哪个checkpoint、词正确性和全局语义、系统能力与单机制因果分别表述。论文无独立Limitations节，笔记主动补任务权衡、训练与测试提示独立性、公式代理、图表/代码偏差、真实资源成本与时间过程未验证；不复用“全面改善”或“低成本消费卡训练”等未证主张。

## 实际阅读范围

v2完整21页5602480bytes；Abstract/§1–6全部核心与Appendix A/B全文（T8–11），T1–11所有单元/公式1–7，主框架及图注；实际p4/6/7/8/9/10/11/12/13/14/19/20/21十三页核框架/所有表/曲线/公式。GH fbaaaf4完整92项树、README介绍/新闻/配方及TRAIN/DATA/EVAL/INFERENCE、SCB/PT/SFT/数据配置；model构造/prepareinputs/llm2dit/text2image/image2image/diff_loss、GenEval/CVTG/UniGen指定推理段。独立RL c4d5dc2完整378项树，README/训练参数与YAML、训练入口默认/脚本、SFT数据配置及trainer CPS335–481/GDPO2080–2140/优化和KL3716–4042指定段、奖励evaluator来源入口；未读整310KB trainer。原生与diffusers两HF固定metadata/card/config，后者连接器/DiT/VLM/scheduler及pipeline构造/SCB/推理默认选段；数据HF仅三文件metadata/card。公开RL两提示表和UniGen官方600行测试做精确规范化交集，未做语义近重复/CoRE全交集。参考文献按需追引，未读全仓/全部附加奖励服务/原运行日志/数据/权重或独立复现。

## 主表可复核摘记

| 指标 | SFT | RL | 解释 |
| --- | ---: | ---: | --- |
| GenEval | .86 | .87 | 表内部分开源更高/并列 |
| DPG | 87.05 | 87.90 | 低于Qwen88.32、Seedream88.25 |
| UniGenBench | 74.18 | 75.74 | 需核提示交集及选模协议 |
| WISE Overall / Space | .72 / .82 | .73 / .70 | 总分提升伴空间子类下降 |
| CoRE Overall | 45.7 | 46.5 | LongCat52.2更高，逻辑/重构子类略降 |
| RISE | 13.3 | 10.8 | 四子类均降，不能写RL全面改善 |
| UniREdit | 77.5 | 75.7 | 37%相对Qwen56.5用的是SFT分数 |
| CVTG Word Accuracy | .6605 | .7533 | 英语静态词准确率，低于多种强基线 |
| CVTG NED↑ / CLIP | .8426 / .8227 | .8936 / .8278 | CLIP最佳不等文字正确率最佳 |

T6去SCB的GenEval保持.86，去think tokens的GenEval反升.87。T7为1000步消融，完整GEdit7.05低于T1的SFT7.12；其他比较须固定训练点、任务和版本。F5总体提升伴中间回落，F6文字子分上升也可同时发生总体退化。

## 公开训练提示的直接交集

核查方法：读取[固定RL general文件](https://github.com/deepgenteam/deepgen_rl/blob/c4d5dc27d699870ddac4bcb8ceda2e240773957b/assets/rl_datasets/deepgen/unigenbench_train_data_general.txt)的7139行、同revision OCR文件2861行，以及[官方固定64e57ab测试表](https://github.com/CodeGoat24/UniGenBench/blob/64e57abc52bf24bfe901cd9beb7de5f00fc0a286/data/test_prompts_en.csv)600行；仅做首尾空白清理、连续空白折叠和casefold后精确比较。两训练表各自无规范化重复。

| 官方测试index | general文件一基行号 | 匹配方式 |
| ---: | ---: | --- |
| 201 | 6869 | 规范化后完全相同 |
| 203 | 6932 | 规范化后完全相同 |
| 204 | 6938 | 规范化后完全相同 |

OCR文件与600条表的此类交集为0。此结果确认发布文件层面的3/600提示交集，不能推定剩余597条没有语义近重复，也不能证明最终训练实际使用、收益大小或所有分数失效。论文附录已明列UniGen与CoRE来源；[辅助SFT配置](https://github.com/deepgenteam/deepgen_rl/blob/c4d5dc27d699870ddac4bcb8ceda2e240773957b/deepgen_rl/sft/configs/datasets/deepgen/t2i_grpo_moretextdata.py)引用Geneval_t2i.json和banana_UniGenBench。缺完整清单、采样日志与独立留出评价，当前保留独立性疑问。训练时周期性UniGen评测还需披露选模次数与规则。

## 公式和实现如何对应

令CPS采样转移为N(mu_theta, sigma_t²I)，在相同方差下，新旧策略log概率之差仍含 `(||y-mu_old||²-||y-mu_new||²)/(2*sigma_t²)`；其中加性归一化项可消去，残差前的时间依赖系数仍存在。论文Eq7和CPS源码用负平均平方残差，属于代理，具有不同时间/维度缩放。应实测该代理带来的梯度权重和质量，不把它宣称成严格相同的高斯概率比。

Eq3写最大化策略目标，Eq5将它与最小化的SFT损失直接相加，符号语义不清；源码用max(-A*r,-A*clip(r))加正的beta约束，再以(1−lambda)与SFT最小化损失混合，解释实际方向。Eq4写裸velocity平方，默认v-based源码还除以2*std²+1e-7。裸速度距离与严格轨迹KL一般需要额外转移、协方差和步长条件；报告不足以证明它们恒等。

逐奖励组标准化后再加权/批标准化可降低量纲差；不保证奖励与真实质量一致，也不消除相关性、低方差噪声和OCR检测偏差。128学习tokens经一次前向获得表示，没有输出可检验的文字推理链；消融收益还可能来自容量、上下文长度和优化差异。

## 无论文制品、数据和训练成本边界

[原生模型](https://huggingface.co/deepgenteam/DeepGen-1.0/tree/b746f077c0b1b3128cd075cfa886edc4ea222827)有18项文件，包含11个ZIP分片和model.pt；卡说明PT/SFT/RL checkpoint组织，本轮未下载验证其内部。原生config.json只列类/库版本，不能单凭它还原架构。[diffusers发布](https://huggingface.co/deepgenteam/DeepGen-1.0-diffusers/tree/85c2ed257b9406d8531965c68e140dc7fdb81382)24项，公开组件配置及自包含pipeline可补结构核查，默认50步/CFG4、支持T2I/静态编辑；没有独立视频管线。

[数据HF](https://huggingface.co/datasets/deepgenteam/DeepGen-1.0/tree/f3d5e6879dbca83f901042f388fac241d96bc170)仅3项，卡仍写上传中；不能将50M训练池与公开数据文件混为一谈。Apache-2.0根许可/卡标签不自动改变所有上游模型与数据各自条件，本轮只记录来源，未作法律判断。

~50M是新增训练池规模概称；使用已预训练Qwen/UniPic2，有私有数据且跨阶段重复使用，不能据此宣称全生命周期只用50M或与5B训练池系统等计算量。表中64H200训练配置与消费卡可推理亦应分别记录；推理延迟必须含VLM六层特征保存、较长条件序列、connector、50次DiT和VAE。

## 与当前选题的联系和追引

把SCB用于汉字/跨文字视频是待验迁移假设。先固定同终态不同笔顺的样本，测是否能在RGB时序中观测/识别逐笔事件，再评估共享UMM是否优于规则SVG、VideoSketcher与强视频生成基线；静态OCR和CLIP无法验证这个命题。

追引CPS/FlowCPS2509.05952、GDPO2601.05242、PrefGRPO与UnifiedReward-Think、CVTG/TextCrafter、UniReason和私有数据配方；相关引用不计已完成原文精读。继续L123 InternVLU并核L122已审状态。
