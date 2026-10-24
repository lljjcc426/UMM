# SenseNova-U1.5：原生像素、文字指标与专家蒸馏完整审查

第一百九十批完成[U26](../reviews/U26.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.json)。358目录（331论文／研究、27资源），295核心/300书面含未通过项；待完成核心深审36篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2609.11929v1)、[主源2](https://arxiv.org/html/2609.11929v1)、[主源3](https://arxiv.org/pdf/2609.11929v1)、[主源4](https://github.com/OpenSenseNova/SenseNova-U1/tree/c35c83b58ef6e238a08b986aa58f3b73303aa42f)、[主源5](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT/tree/9feeeab8a2792514d109cd34589342a2cc1d4ab2)、[主源6](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT-LoRAs/tree/f33b8fe0216e6f10e5aed58ebbfdd05f02826732)。

## 研究问题

在原生理解/生成统一模型中，如何同时提高细节、双语长文字、复杂布局、多参考编辑和交错视觉推理，并维持理解能力？研究对象是最终图像与交错图文输出，无在线手写轨迹、笔顺或书写视频任务。

## 现有不足

外接视觉encoder/VAE存在表示接口与重建瓶颈；原有逐patch MLP头欠缺相邻patch空间交互，高分辨率噪声尺度与训练分布也需适配。多个RL目标可能互相干扰，因此先分专家优化再聚合。以上是设计动机；报告同时改变数据/计算/解码器/后训练，未把每个因素的独立因果贡献分离。

## 贡献

在NEO-unify的encoder-free/VAE-free像素接口上加入空间卷积PixelShuffle解码头、分辨率噪声条件，扩展至4K数据和结构化任务；五阶段训练依次为生成预训练、统一mid-training、统一SFT、四专家RL/DPO、multi-expert on-policy distillation。主要证据是完整系统在多类生成编辑基准的改善及部分退化；原生统一促进能力交互仍需匹配消融，不能由架构命名直接证明。

## 输入、模块、输出与公式

输入文字token及清晰/含噪图像，输出文字AR或图像flow。每32×32RGB patch经两级卷积投影（16再2）+GELU成为4096维token，带2D位置与原生时空RoPE，<img>边界/PreBuffer；是学习投影并有空间压缩，未证明可逆/近无损，4096维大于RGB3072维也不能据维数直接断言必丢信息。Eq1文字CE；Eq2 z_t=t·x+(1−t)σ_Rε；Eq3 x-prediction转换v=(xhat−z_t)/(1−t)，GT同式，在线性路径下为x−σ_Rε；Eq4速度MSE等于endpoint MSE/(1−t)^2（t<1），高t有不同权重；Eq5 LPIPS，Eq6加权CE+FM+感知损失。Eq7–10及未编号式给OCR/编辑奖励与专家蒸馏；四专家在同一student当前状态/时间/条件给velocity目标，student状态stop-gradient，损失未穿过整段生成轨迹。Beta(2+3n/N,5−3n/N)查询时间随训练从早期高噪声偏向后期低噪声，30步ODE仅跑到查询点、无suffix。

## 模型结构

42层MoT，Q/KV heads32/8，head T/H/W64/32/32，hidden4096；表1理解/生成各8.2B，模态分支有不同QKVO/norm/FFN、共享attention交互，8B命名不等整个模型只有8B参数。官方参数文档17.552B例子属于U1，未把其精确总量直接移植U1.5。clean上下文不可见未来noisy图，noisy块内双向并读过去clean，文字因果。F3 PixelShuffle2→3×3 conv1024→1024/GELU→PixelShuffle2→conv256→192→PixelShuffle8→RGB，跨patch做空间重建。固定repo中ConvDecoder对应此结构，modeling_neo_chat以use_pixel_head替换FM头；HF最终config use_pixel_head=true、resolution noise、noise_scale=1、base64token、max16、NSEmb=true、4K面积上限，42/4096/32/8与论文相符。σ_R随图token数平方根缩放并clip16，noise embedding除σmax。移除独立VE/VAE不等移除所有可学习视觉模块。

## 数据分布与划分

相比U1新增59M图文对、78来源，未声称全训练集只有59M；有效训练volume中88.2%高于1024²、64.4%高于2048²，volume分母未充分解释，不能当唯一图片计数。38M编辑样本：general42.93%/infographic41.67%/reference15.40%，最多10参考，含spatial marker/box及结构化PE/CoT目标。交错数据以lifestyle43.83%、infographic29.24%、video19.22%、reasoning7.69%为主，报告未给其全量；图文/视频转换及teacher筛选不等实际笔过程监督。RL美学280K先滤弱reward方差、OCR60K（短20K+长改写40K）、编辑120K（local80%/global20%）经三轮筛选、info120K DPO对。来源/筛选分布、完整license清单、与全部评测的去重和预训练污染证据不足；数据量与模态监督差异是与前代比较的混杂。

## 指标与评价协议

文字/视觉理解accuracy及指令following；生成QwenImageBench、GenEval/2、OneIG EN/ZH、DPG、CVTG、LongText、IGen、BizGen、WISE；编辑ImgEdit/GEdit/WeEdit/OmniRef；交错RISE/OpenING/VBVR，生成辅助理解UniMMMU/RealUnify。CVTG官方当前代码：accuracy按GT词计数micro，不等2–5区块均值；每GT词只判断是否存在预测词（不consume），重复GT可复用同一预测，近似NED逐词选best match，均忽略全局词序/区域绑定且不直接罚额外词；CLIP按图片平均。LongText当前代码英词/中文字符Counter交集÷GT总量，最后按GT量micro，是多重集召回率；保留重复数但忽略顺序/位置且无多写惩罚，区别于RL的min/max Jaccard奖励。论文T12高分不能据此推出逐字符顺序/版式/无幻字。OpenING当前scorer默认gpt-4o、六维先逐维均值再宏均值，缺失/null任一必要维会整条滤掉，需同时报有效样本与失败率；不能据代码默认断言历史T21实际judge就是该版本。RealUnify当前汇总为样本micro，<answer>内或response首个A–D解析，无边界fallback可能误取普通单词字母；UniMMMU脚本只是外部image_text_agent scorer包装。未执行judge/API、OCR模型或基准重跑。

## 对比方法

同系列U1/SFT/CoT及BAGEL、UniWorld、OmniGen2、QwenImage/2512、ZImage、LLaDA、ERNIE、Emu3.5、FireRed、FLUX等开源，与GPTImage2、NanoBananaPro、Seedream、Gemini等闭源作报告内比较。同为Qwen3初始化不能对齐完整视觉预训练、数据量/算力、CFG/NFE、prompt改写及模型发布时间；T3有些外部行引用原报告，#Params主要标生成分支，不构成统一总参数成本。wPE必须区分裸prompt，wCoT区分直接输出；未用终态文字/图像分数代替过程准确率。

## 实验条件和发布边界

表2 Stage1三期180K/100K/185Ksteps，lr2e−4/1e−4/1e−4→2e−5，seq8196/20480/20480，256²–1024²→512²–4096²，前两期T2I，三期T2I/edit/interleave=.6/.3/.1；冻结理解分支。Stage2双分支80K lr2e−5 seq32768 mix.3/.4/.2/.1；Stage3 10.5K lr2e−5→0 seq32768，表中mix.3/.4/.3/.1合计1.1，原样记录、未擅自归一。两统一stage CE:FM:Perc=.1:1:.1，AdamWβ.9/.95 eps1e−8。美学/OCR专家16候选、30steps、CFG4、shift3，从最初10步采连续5步；美学epoch分别route HPSv3++/PaddleOCR，CPSη.7 lr2e−5 KL.01；OCR Preciseη1.5+GRPOGuard KL.02，两者冻结最后gen block/head/outnorm。编辑lr4e−5 KL.01、24步、η.7及EMA，论文称避开SDE但未完整给替代logpolicy推导；5维VLM归一min聚合，execution未改时0，文字项按任务启用。info先额外midtraining→OCRGRPO→120K对DPO(lr5e−6 β10、查询1–20某一步)→路由GRPO，额外资源不同。MOPD硬domain路由四teacher，800steps×globalbatch128=102400exposures，与每域25600一致；AdamW2e−5 β.9/.999 wd1e−4 gradclip1 BF16，冻理解/末3gen层/head；T2I CFG4、编辑CFG1，5种area1K²–4K²/9种比例对齐32，编辑跟源尺寸。

## 主结果

全部23表逐行已核，结构化保留原值。T3理解有下降：MMMU74.78→73.86、MMMUPro67.69→66.47、MathVision75.82→73.55、MMStar78.27→77.53、OCRv2 61.30→59.07、MMLURedux87.61→86.33、SuperGPQA49.67→49.55；MathVista84.2→85.85、CEval84.4→90.41等改善。T4/5 QwenImageBench EN48.28→52.82→PE60.22，ZH45.99→52.43→PE60.13；T7GenEval2 .43→.55→PE.71，GPTImage2 .81。T8/9 OneIG EN.549→.552、ZH.535→.536，分别仍低Emu.564/Qwen.548且多样性.166→.159/.176→.165。T10DPG87.78→88.11仍低Qwen88.32，global/attr/other分项下降。T11CVTG avg.940→.948、NED.972→.977、CLIP.825→.819，2/3区文字accuracy下降，4/5区上升；avg不可用四个区域均值复算。T12LongTextEN.979→.988、ZH.962→.989，按上述召回协议解释。T13IGen Q/I .51/.04→.62/.08→PE.76/.17，距Nano.90/.49仍大；T14BizGen hard/easy39.7/61.7→51.4/70.2→PE72.2/88.4，其中Knowledge4.8/23.4→PE72.0/87.9提示外部规划贡献。T15WISE.69→.70、CoT.78→.81，化学CoT.77→.76。T16ImgEdit3.90→4.59；T17GEdit EN/CN7.47/7.70→8.26/8.24，闭源仍更强。T18WeEdit均值7.46中translation IA/TC/BP2.19/4.16/8.11、reason1.84/4.17/7.94，保留背景高分未能保证正确执行。T19OmniRef wPE objective.68/MLLM8.15低Nano.70/8.50。T20RISE33.6→CoT38.6，但spatial49→42、VP95.2→94.8；T21OpenING9.07→9.18，completeness9.14→9.13。T22VBVR总体68.2/ID67.6/OOD68.9，但OOD abstract69.8低Nano75.1，knowledge/perception也非全最优。T23UniMMMU35.0→29.6：jigsaw87.3→86、maze28.6→17.3、sliding0→0、geometry24.2→15；RealUnify47.5→56.3、MR36→38/MT63→84/AF51不变/CN40→52。

## 消融及进一步实验

PE和CoT开关有同模型结果，说明额外规划/中间生成在部分任务有效，但也有RISE空间下降；PE不是单一内部架构改动。未提供U1.5同数据/步数/预算的MLP vs PixelShuffle、4K/noise embedding/LPIPS、四expert前后与MOPD前后逐项对照，也无同U1.5禁用生成的UniMMMU/RealUnify比较。T3理解退化与T23GaU退化必须保留，不能用RealUnify提升声称所有理解均维持。F1/2选例展示图像细节/多参考编辑，F3解码头、F4五阶段、F5数据饼图；示例无抽样分母和独立人评，静态例不证明书写过程或所有分布可靠。前代/闭源排名与整体配方比较不替代模块消融。

## 局限与疑问

完整系统多因素共同变化，近无损/能力交互/四专家无损聚合缺直接隔离证据。OCRRL multiset Jaccard对词/字符排列不变，长期文字eval甚至只测召回，无法约束句序、拓扑、版式绑定或笔画时序；高NED/CLIP也不等笔顺。PE可由外部LLM产生约1100–1500token RenderJSON，当前helper默认gpt-5.6-terra并可选web_search、编辑PE默认gpt-5.5，外部知识和成本须记入系统；这些当前默认不证明历史实验所用版本。U1.5知识类PE涨幅不能全归原生模型记忆。未给跨表完整同budget/seed/CI、全量eval rawoutputs/去重。发布固定repo735tree603blob中未见RL/DPO/MOPD训练实现路径，训练README仅U1+U1.5Preview生成PT，示例launcher200K/8192/≤1024²与报告多stage不等；样本数据/路径占位需自备，不能声称完整训练已复现。HF最终checkpoint与8步LoRA存在不等四专家训练流程已发布。报告/README已指出编辑过改、指令遗漏、多图长上下文和强CFG细节/色彩不稳，经验建议不替代系统统计。

## 预期优势条件

可学习pixel接口与空间重建可能在高分辨率细笔、密集双语文字、跨patch连续结构上有帮助；分专家优化可能缓和reward冲突，OPD在student访问状态追随对应teacher可减少teacher轨迹分布偏移。但需要数据/算力匹配、结构与过程指标验证。迁移中文艺术字过程时可研究局部墨迹连续性/细线保持和中间图回读；原模型仅静态/交错图，无笔接触/增墨约束/规范笔序标签，不宜直接当笔顺解决方案。

## 可证伪实验

Q1空间头与4K数据谁贡献细笔/文字收益：固定底座、训练图/分辨率/steps、LPIPS/noise/推理NFE/CFG，做MLP/ConvDecoder×数据分辨率、NSEmb开关的必要因子对照，测独立OCR+顺序CER/WER、区域绑定、细线断连/拓扑、人评/CI与吞吐，不只bag词召回；若对齐后无增益，收窄空间头主张。Q2四专家聚合是否保留能力并促进推理：同学生/总训练exposures比混合reward、四专家、无OPD和OPD，逐domain报Pareto/回归、teacher routing、hard样本与未训练任务，并在U1.5同预算比较无图/交错图/GT图/错误或随机图回读。PE固定外部planner/知识访问/长度/总时间，保留裸prompt；对生成文字做交换词序/增加幻字/改布局的指标一致性审查。书写另报prefix只增墨、笔序/方向/接触/速度和终态字形，同终态换序对照。均为提案，无模型执行。

## 论文组织与Claim学习

文章从原生接口局限→空间头与4K→五阶段专家→理解/生成/编辑/交错全表，方法组织易于按阶段复述；报告保留很多前代下降项，值得学习。Claim需与表一致：VBVR按总体/OOD平均领先不等每子类领先，UniMMMU“competitive”应同时给−5.4pp，generation helps需同模型禁用生成对照。参数口径、PE外部planner、平均分分母和代码发布范围应在主结果旁清楚标示，不能只用摘要/雷达图概括。

## 实际阅读范围

完整2609.11929v1 PDF35页/HTML正文§1–6、§7contributors与参考追引，无附录；10编号式及未编号OPD/Beta表达、T1–23全部行、F1–5全部视觉及首页总览。固定repo735tree603blob结构，下载27个选定text文件；人工重点审README/训练NOTICE及说明、launcher/配置、ConvDecoder及模型选择/噪声片段、生成/交错评测说明、CVTG/LongText/RealUnify/UniMMMU/OpenING评分段、PE脚本与参数文档。未宣称完整逐行审603blob或27文件；HF最终/LoRA API文件清单、最终config已核，无权重下载/模型推理/训练/judgeAPI/基准重跑。核心三遍与五项书面检查完成，独立模型复现仍false。

## 两种文字指标不能混写

报告OCR专家使用多重集Jaccard，分子为各token计数min之和、分母max之和，会惩罚多写但排列不变。当前LongText评测使用Counter交集除GT数，额外文字不进入分母；英文按词、中文按字符，因此GT中字符不变时的换序仍可得到满分。当前CVTG则逐GT词判断是否出现在预测词列表，不消耗匹配，同一预测词可能覆盖重复GT。上述为公式/代码结构分析，未调用OCR/生成模型，也未推断历史所有成绩有误。

CVTG avg按所有GT词计数汇总；表11四个区域分数的算术均值不是其总体分母。表2SFT任务比例合计1.1保留为原文疑点，不自行修正。表23UniMMMU平均35.0→29.6与RealUnify47.5→56.3同时保留。OpenING缺失评分过滤应报分母；未用当前默认judge反推历史实验身份。

论文相关追引覆盖NEO-unify/U1、Qwen3、flow matching/pixel diffusion、GRPO/Precise/CPS、DPO与on-policy distillation及所有23表的benchmark引用；相关目录已有工作的复用不记为新增全文三遍。没有公开证据的笔顺能力或完整RL开源，不补写成已完成。
