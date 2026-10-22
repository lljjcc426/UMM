# SenseNova-U1：原生像素接口、MoT协同与发布制品审查

第一百三十八批完成[L125](../reviews/L125.md)明确范围核心三遍与五项书面记录。[结构化证据](../../data/sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），247核心/250书面含未通过项；未确认核心83论文／研究+27资源，资源另审。无目录新增、删除文件、权重下载或独立复现。

来源：[v1](https://arxiv.org/abs/2605.12500v1)、[固定发布仓](https://github.com/OpenSenseNova/SenseNova-U1/tree/c35c83b58ef6e238a08b986aa58f3b73303aa42f)。后续U1.5、LoRA、Infographic与Interleaved单列版本队列，不将其结果倒填本论文。

## 问题与贡献

使理解、文字及图像生成/编辑、交错图文推理在原生像素接口与MoT内联合训练，缓解预训视觉encoder/VAE割裂、细文字损失和理解/生成目标冲突。视频用作理解与交错图像数据，机器人展示为稀疏视频动作解释和图像状态预测；未量化连续视频生成、机器人闭环执行或规范汉字笔顺。

语义视觉编码压缩细粒像素，VAE增加独立表征与迁移接口；理解AR偏因果、生成flow需双向图像上下文，直接共享全部参数可能干扰。用浅层像素patch接口、分支独立参数/共同attention、分阶段联合与OCR/风格RL分别处理。没有预训VE/VAE仍继承NEO/LLM先验和大规模数据，不能归零基础训练。

RGB两层卷积patchify和MLP像素输出替代独立深VE/VAE；NEO原生分时空RoPE与MoT双分支，理解clean不能看noise而生成可看clean前缀与图像双向token；先理解warmup/生成PT，再联合mid/SFT，FlowGRPO交替文字-风格与美学奖励，DMD2/PhasedDMD后蒸至8NFE；LightLLM与LightX2V分离推理。FlowGRPO/DMD等是采用机制，原生接口和训练整合的增益须相应受控实验。

## 数据流与结构

输入文字/参考RGB图或稀疏视频帧→理解分支原生patch+文字token，AR可输出文字/显式CoT/图像起始符；生成分支将同分辨率高斯噪声RGB重新patchify并加t与噪声尺度embedding，共享attention读缓存cleanKV→MLP预测clean RGB patch xhat→v=(xhat−z)/(1−t)数值积分→重组图像；生成图与文字可继续入前缀形成交错序列。参考/噪声视觉输入均非固定外部VAE latent；图像推理多步与文字AR代价分别统计。

T1 8B-MoT理解/生成各8.2B，42L/hidden4096/Q32KV8/head128按T64H32W32，PreBuffer有；A3B理解30.0B/128专家、生成8.2B/32专家各Top8，48L/hidden2048/Q32KV4/无PreBuffer。分开QKVO/LN/FFN但attention联合，非所有权重共用。HF索引total_parameters分别17552340992/38737986560，total_size35104681984/77475973120bytes，是发布元数据非实测显存/活跃算量。pixel16卷积3→1024/GELU、2×2卷积→LLM维/等效32patch；发布代码在第一层embed用2D RoPE，末头hidden→4096→3072，use_pixel_head=false。A3B2048<3072且GELU，不保证一般RGB的可逆无损；T23支持有限分布经验重建。HF A3B rope_theta10000000与正文时间轴5000000不同，最终评测配置待核。

## 数据和评价协议

理解warmup图文配对32/caption17/infographic14/纯文字37%；joint理解内部SenseNovaV6.5通用39.2/agent空间22.3/知识推理19.3/文字19.2%，CLIP聚类均衡与答案重生成/拒绝筛选。SFT空间15/通用13/推理12/NLP11/OCR11/agent10/长文8/code6/对话4/组合4/其余6%。生成Nature40.5/People26.7/Design20.7/其余合成，编辑为过滤网络对/合成，明确变与不变条件。交错生活44/信息图29/视频19/推理8%，视频来源不能当原生连续视频训练输出。表2累计3.45T训练tokens，不含所有上游预训、非唯一样本；<80M仅正文joint近收敛片段。完整内部样本/去重与所有评测语义去污染证据未开放；680MB训练样例仅覆盖接口和任务，不是原始训练集。

理解EvalScope llm_recall/gpt-4o-mini-2024-07-18，MMMU/Pro/MathVista/Vision/MMBench/MMStar/InfoVQA/OCRBench-v1-v2/AI2D/Hallusion/BabyVision/TiR及空间VSI/ViewSpatial/MindCube/3DSR；文本MMLU/IFEval/IFBench/Tau2/Claw。生成GenEval、DPG、OneIG EN/ZH、TIIF短长、CVTG-2K NED/CLIP/word、LongText EN/ZH、IGen问题/图级、BizGen hard/easy、WISE；ImgEdit/GEdit/RISE，OpenING、VBVR-Image Preview、UniMMMU GaU、RealUnify UEG/GEU。T23PSNR/SSIM。LongText当前代码Qwen2.5VL7B OCR，清标点/大小写及限定字符集，EN词/ZH字符Counter交集除GT总量的micro召回，不敏感顺序/多余文字，且过滤多种非中英字系；不等于有序CER/跨文字全面正确。

理解Qwen3VL8B/30BA3B、Qwen3.5-9B/35BA3B、Gemma4/LongCat；生成Tuna/Tuna2/NEO-unify/OneCAT/Mogao/Lumina/QwenImage/ZImage/BAGEL/Janus/BLIP3o/InternVLU/Emu3.5和闭源GPTImage/Seedream/NanoBanana等；编辑含QwenEdit2511/LongCatImage/FLUXKontext/OmniGen2/Step1X；交错SEEDX/VILAU/Showo/NExTGPT及组合pipeline，VBVR专训版本；重建SDXL/SD3/FLUX VAE/RAE/UniFlow/UAE。参数列常仅分支且预训/原生分辨率和评测设置不同，榜单不能代替同预算架构消融。

T2 warm120K lr2e-5/.75T；生成PT120K2e-4/.25T/256–512→60K1e-4/.25T/512–2048→120Kcos1e-4至2e-5/.88T；joint84K2e-5/1.19T与SFT9Kcos2e-5至0/.13T。AdamW(.9,.95,1e-8)/wd0/clip1，genEMA.9999/joint.999；joint理解/生图/编辑/交错.33/.37/.24/.06、CE:FM=.1:1，context32768。z_t=t x+(1−t)sigma eps；sigma=sqrt(N/64)上限8；代码v分母clamp t_eps=.05。FlowGRPO每轮48提示×16图=768/10步/CFG4/噪声.7/lr1e-5/KL.01，文字600轮/分辨率warm200；交替奖励8B1600轮/A3B200，冻结under和最后3生成层/头。DMD fake:G更新5:1/G2e-6/F4e-7，AdamW(0,.999)/wd.01，8NFE无CFG对基准50步CFG(100NFE)。正文评测temp.6/top_p.95/top_k20/reppen1/max40960/timeout600；当前yaml却1.05/32768/300，需原日志。VSI32帧而Qwen128；生成2K后缩1K不使原生输入/推理成本相同。部署每步5090.415s/L40S.443s使用TP2+CFG2，不是单卡/端到端耗时。

## 结果与消融

T3相对Qwen3VL8B推理与多数空间项提升，但InfoVQA86→82.46/OCRBench-v2 61.55→61.30；A3B InfoVQA86→83.04、VSI56.9低于8B62.66，非各项单调保留。GenEval两型.91；DPG8B87.78/A3B88.14低于Qwen88.32；OneIG-EN8B.549低于Emu.564，Text.969<.994；ZH8B.535/A3B.540低于Qwen.548。TIIF短89.74/长89.17为表中8B整体最佳但子项非全胜。CVTG8B.940/A3B.881、LongText8B.979/.962；IGen问题.51但图级全正确仅.04；BizGen8B hard39.7/easy61.7，知识3.5/17.9仍弱。ImgEdit8B3.90/A3B3.91低于QwenEdit2511的4.51；GEdit7.47/7.32低于7.88。SFT CoT使WISE8B.69→.78/A3B.74→.81，RISE23.9→26.9/25.3→30.0，但A3B temporal25.9→24.7退。OpenING9.07/9.16；VBVR-Image Preview68.8/68.9仅此子集。GaU35.0/32.6，Sliding8B0、几何24.2低于BAGEL32.8；RealUnify52.4/50.5：GEU为单次交错流程、UEG为T2I推理，仍只是跨模型比较，缺各自无生成/无理解条件，不能据此算双向协同增量。

T23用先前NEO-unify2B、90K重建MSCOCO2017，512下PSNR31.56与FLUX VAE相同但SSIM.85<.93，其他256设置不完全可比；不是U1全模型像素可逆证明。2B冻结理解/60K公开混合数据ImgEdit3.32，支持指定条件保留信息。F12为MT前后柱状图，MM平均72.1→73.2、文本77.7→77.8、DPG84.7→86.5、GEdit69.1→69.9（归一化0–100）；无同预算仅生成/仅理解的对应对照，不能隔离架构内在无冲突。F13横轴Train Tokens至约2.5T，DPG512其余1024；DPG约1.1→1.4T、GEdit约1.3→1.9T、RISE约1.9→2.2T有回落，无误差带/其他架构同预算曲线，不能写严格单调或由此证明更高样本效率。CoT有同SFT两配置比较但输出长度/额外计算也改变；RL三reward描述与冻结策略缺完整独立因子/多seed；DMD定性少步对照不等全部基准相同质量。

## 局限和条件化假设

没有严格笔画事件/同终态异轨迹/视频字幕时序生成或闭环动作执行评价；VLA仅四帧动作描述，worldmodel仅图像+指令→结果的定性示例。无VE/VAE不保证无压缩损失或无先验；A3B2048瓶颈、重建SSIM差异、细字与网格错误要量化。§3.1正文称近似常数per-token噪声能量，但独立单位高斯且固定patch维d时E||sigma eps||²=d sigma²随N增长；该式独立不能证明这句，需额外SNR/归一化定义。OCR奖励为文本Counter多重集合IoU，顺序失明；LongText又是不罚额外文字的召回，清洗还屏蔽其他字系。InfoVQA等退步、榜单参数口径/2K预算、代码评测默认差异和有限重建/协同对照必须保留。RISE引用InternVLU 1.8/overall9.4的不一致沿用原表，136批已记未解决，不当正常数据背书。原始数据/RL蒸馏全流程未核到公开完整实现。

在相同上游先验、训练token和可驻留成本下，当细文字/布局需要像素空间保真、理解上下文能提供近充分语义而分支独立容量足以缓解优化冲突，原生32patch+MoT可能较语义压缩接口改善OCR和复杂指令；短规划CoT可能有利WISE/逻辑编辑，少步蒸馏适合延迟约束但须质量Pareto。高分辨率细笔、非中英/超长/新字体、同图异过程、实际笔触接触及长视频不自动获益；DMD/奖励上升不保证这些分布泛化。

## 验证设计与科研写法

固定LLM/上游训练/unique数据/总tokens与实测GPU秒，像素接口对VE/VAE、共享/双分支、RoPE/PreBuffer、sigma固定/平方根且含/不含embedding全因子或有针对性消融；按驻留参数/活跃FLOPs/attention与通信单列。原生1K/2K与2K缩1K作信息和计算双对齐，报告端到端含CoT/KV/OCR/解码及误差。联合/仅理解/仅生成同预算与关闭生成辅助/关闭CoT，测双向增量及梯度冲突，RealUnify/GaU榜单不能替代。OCR IoU/有序CER/空间region对齐/错误增字、换行重排、细笔和多字系留出测试；RL奖励组与冻结末层因子、DMD8/50步同种子全基准盲评。用规则SVG、VideoSketcher和强视频模型在同终态异过程/跨字符字体作者切分，测笔画事件顺序、可见性/持续性/接触和真实执行。上述实验未运行。

Intro将表征接口/理解生成目标冲突/推理系统三个问题连到设计，Method分原生架构、flow、分阶段训练/RL蒸馏、部署，数据与结果分开；表2公开阶段比空泛数据量更可审查。学习将Claim绑定版本/原生输入预算/任务和完整表；“near-lossless”“minimal intrinsic conflict”“synergy”应分别补重建误差、同预算冲突对照与模型内增量，不能只由好看的输出或跨模型排名推出。结论谈世界抽象/具身未来是展望；Limitations应写实际混排长字、网格/背景偏差、内部数据与发布默认差异，以及尚无连续视频/严格笔顺验证。

## 实际读取范围

arxiv v1 HTML全部研究正文Abstract/§1–6（含完整Method/data/deployment/23表与消融、VLA/worldmodel解释）、贡献列表和F1–15图注、Eq1–7作用；参考条目不逐篇计精读。完整43页PDF26140491bytes，实际p6/7/8/10/16/20/22/23/27/29/30/31/32/33共14页核框架、结构/训练/理解/文字/推理表、重建、MT柱状/TrainTokens曲线及机器人状态图；其余定性页未逐图。固定GH c35c83b完整735项树/603blob；README新闻/原U1发布与局限相关段，当前U1.5其他图文未全读；NEOChat构造170–251、v输出599–640、编辑1550–1687、生图1780–1857，VisionEmbeddings/NEOVisionModel全逻辑，MoE路由构造/双分支说明，trainingREADME169–245及两型配置选段/8B启动全文，evaluation说明与under yaml全文/生图文档全文、LongText清洗/计数/汇总核心、distill用法与issues。HF两型元数据/完整配置/权重索引；卡片未全文、无权重下载/运行/独立复现；未把后续U1.5与Infographic新版本计此论文三遍。

## 逐项收窄研究结论

| 原证据 | 对研究判断的约束 |
| --- | --- |
| HF索引8B 17,552,340,992、A3B 38,737,986,560参数 | 名称、分支参数、整模型驻留和活跃FLOPs各自记录 |
| 两层卷积/GELU/32patch，A3B隐藏2048对RGB patch3072维 | near-lossless是有限分布重建经验；没有一般可逆性证明 |
| T23 NEO-unify2B512重建31.56/.85，FLUX VAE31.56/.93 | PSNR相同、SSIM仍有差距；非完整U1大模型受控消融 |
| sigma=sqrt(N/64)，单位高斯固定patch维d | 每token噪声二阶矩d*sigma²随N增，额外常能量定义待核 |
| 2K生成再缩到1K评分 | 与原生1K推理在输入信息和成本上不同 |
| InfoVQA 8B 82.46<Qwen3VL86；OCRv2 61.30<61.55 | 理解能力不能写全保留或全提高 |
| OneIG-EN Text .969<Emu.994；ZH整体.535/.540<Qwen.548 | 保留具体基准优势，避免全面领先 |
| IGen Q-ACC .51/I-ACC .04 | 问题平均和整图全部约束正确度不同 |
| RISE A3B CoT整体25.3→30但Temporal25.9→24.7 | CoT有分项取舍及额外计算成本 |
| GaU/RealUnify给跨模型分数 | 还需本模型关闭图像/理解辅助时的对照才能估因果增量 |
| 机器人四帧解释/图像状态预测 | 未证明动作执行、连续世界动态和规范笔顺 |

## 评分机制与跨文字盲区

[LongText固定实现](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/evaluation/gen/longtext/eval_images_longtext.py)默认用Qwen2.5-VL-7B-Instruct OCR。英文以词、中文以字符计数交集，汇总为GT总量加权召回；当前清洗允许中英字母、数字和列明的部分拉丁重音字符，剔除标点、限定范围以外字符，英文小写。顺序颠倒、多余文字、其他书写体系不能充分反映。此前136批核的InternVL-EvalKit为32B OCR：不能假定两仓所有已发表分数都被同一工具重测。

论文OCR训练奖励为多重集合IoU，会通过union惩罚额外计数，但仍不感知顺序；不能把它和LongText召回混为同一个指标。CVTG当前词准确实现逐GT检查是否出现在预测词列表，同一预测可满足重复GT，没有一对一消耗；NED以difflib选近邻后算字符Levenshtein相似度。它还报告CLIP与多region词准确率，须保持各指标定义及裁判版本。严格笔顺需要有序OCR、区域文字与事件级顺序/持续性、笔触接触等单独测量。

## 配置、训练和少步资源

[当前理解yaml](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/evaluation/understanding/config.yaml)的repetition_penalty1.05/max32768/timeout300与正文1.00/40960/600不同。生图说明的CVTG默认CFG7、shift1、2048，部分其他基准CFG4、shift3、50步；SFT示例检查点也不能直接当所有主表最终RL检查点。结果复核需锁实际命令与原日志。

[8B训练启动](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/training/shell/train_u1/8B.sh)为示例，lr2e-4/20万步/seq28672/生成256–512，和表2SFT9K/lr2e-5/seq32768不是同一配方。代码可用来学习混任务packing/分布式训练接口，不能据此声称复现原始完整训练；680MB HF样例只用于覆盖任务/数据格式，原内部大训练集不随样例发布。完整树只有base_vs_distill文档命中grpo/reward/dmd/distill相关路径检索，未核到完整RL/蒸馏trainer；该检索边界不推断所有其他函数不存在。

[v1推理](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/src/sensenova_u1/models/neo_unify/modeling_neo_chat.py)在img_cfg=1时仅计算图像条件与完整条件两分支，避免把公式三个项误算为总需三次前向；50步CFG对应100NFE，蒸馏8步无CFG对应8NFE。代码将分母1−t夹至配置t_eps=.05。全局CFG归一化与默认值要连同结果记录；算NFE比不等于端到端加速比。

[少步文档](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/docs/base_vs_distill.md)明确原U1 LoRA可能网格伪影、Infographic LoRA可能重复文字/白背景；当前U1.5 LoRA还规定训练基础SFT与兼容最终base/不兼容Preview。它们是重要无独立论文资源，需要逐版本记录来源、配置、局限，不能拿兼容性说明当完成训练或质量测量。本批只审发布说明和用法/局限，不将所有新制品计为完整独立审查。

## 后续追引与实验

按重复研究关联追NEO-unify官方博客、U1.5独立报告及其后LoRA/Infographic/Interleaved/GGUF/Training-Sample资源；兼顾FlowGRPO/DMD2/PhasedDMD、LightLLM/LightX2V、CVTG/LongText/IGen/BizGen/VBVR-Image/RealUnify。引文或资源链接被识别不代表这些来源已独立精读。继续L128 MindOmni及现有未完成队列。
