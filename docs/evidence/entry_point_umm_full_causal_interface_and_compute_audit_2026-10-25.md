# UMM概念入口：完整行为、因果位置与公开计算路径审查

第一百九十七批完成[L030](../reviews/L030.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/entry_point_umm_full_causal_interface_and_compute_audit_2026-10-25.json)。358目录（331论文／研究、27资源），302核心/307书面含未通过项；待完成核心深审29篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2608.17564v1)、[主源2](https://arxiv.org/html/2608.17564v1)、[主源3](https://arxiv.org/pdf/2608.17564v1)、[主源4](https://github.com/Zane-ZYQiu/entry-point-umm/tree/8a0a9893d8f307cdc457b093c0d3ffaa31e32a7f)。

## 研究问题

单方向把新伪词绑定到视觉实体后，未训练方向能否使用该概念；名字—图像表示相似与实际识别/命名/绘制是否一致；绑定进入共享计算的位置如何限制跨任务使用。采用控制注入研究UMM机制，非新通用生成骨干或笔顺生成方法。

## 现有不足

联合训练的理解/生成数据重叠使跨任务增益难归因；只看候选匹配会混淆识别与主动命名，只看表征对齐会混淆可读出与后续可用。用单向监督、固定模型激活干预和分层位置扫描分解这些问题。

## 贡献

BAGEL单向G/U概念注入；区分4选名字匹配、无候选上下文的名字似然排序、另行开放命名、生成图像检索；centered semantic-address retrieval（SAR）与层位置干预；Semantic Anchoring冻结图像地址、只优化名字hidden对齐；同目标闭式激活edit冻结全部权重，与LoRA权重edit比较；7组发现/确认、同类sibling、第二视觉encoder、4架构与通用生成遗忘控制。

## 输入、模块、输出与公式

Eq1 TransferRate=(Across−Abase)/(Adirect−Abase)，须在同一个评价任务中用其直接学习上界/底座校正。SAR将K名字/视觉向量各去概念均值再cosine检索求MRR，是诊断不构成行为因果保证。Eq2 InfoNCE CE(tc@vc.T/τ)，τ=.07；视觉地址为每概念8张训练图固定编码均值，名字hidden在6短模板取同层平均。Eq3/4闭式δk=tbar+||tc_k|| vc_k/||vc_k||−tk，保留相对原中心的名字模长并转向视觉地址；最大化旧中心下对角cosine项，不等于含负样本耦合的整体InfoNCE全局最小。修改后均值=tbar+mean(||tc_k||vhat_k)，通常不等于原tbar，论文附录承认有限precision/重中心/负项差异。缓存8×3584=28672标量不代表总计算为零。

## 模型结构

BAGEL28 decoder blocks、d3584、MoT共享理解/文本qkvo+MLP与私有generation *_moe_gen，7B/专家、14.1B总量；U只走共享，G走两者。r32 LoRA含attention与MLP，固定预算实验分配shared/private rank和为32、80.74M。frozen activation patch按伪词完整subword输入embedding序列定位，指定层后加每概念δ到其全部token残差；修改权重的方案可改变注入层以前的映射，静态δ方案仅改该处状态，两曲线差异不能仅归因深度。理解的name评分首subword logits受因果mask保护，不会被本词后续hidden patch直接自匹配。

## 数据分布与划分

主研究56 Objaverse资产=7组×8，每实体60训练视图20heldout，方位/背景/光照划分；伪词1–3subword经冻结底座行为筛查，不能证明预训练从未见实体。24项检索bank=本组+循环后2组；同类细粒度另12对=24概念、3组，每组8。AppH末段“24 sibling pairs”与主体12pairs/24concept不一致，按T16及设计记录12对。跨架构Janus-Pro-1B（Llama总1.5B）、Lumina-DiMOO-8B（LLaDA8B）、Omni-Diffusion-7B（Dream7B/Qwen2.5）三个新增架构各12概念/12bank；BAGEL曲线采用7组汇总，T13列每次8概念/24bank，§6.1泛称各模型12项与T13细项不完全一致，按明确协议分开。

## 指标与评价协议

4way名称匹配chance.25、反向图匹配.25；所谓context-free production逐一teacher-force8个名字，以logP(name|image,prompt)−logP(name|prompt) PMI总subword/首subwordargmax，chance.125，属于无候选提示的候选评分。另T18实际free decoding原问题/禁止真实类别/伪词对类别2选控制，不可忽略。DINOv2 24way top1生成identity chance1/24，不能等同规范事件或完美实例还原；CLIP独立encoder交叉核对，depth均值Pearson.997，概念层.821、MAE.165、46/56同在底座以上，不能称所有实例判断完全一致。GenEval553prompt×2图（官方通常4），检测器替换为OWLv2，绝对分不能与官方Mask2Former分数直接比。

## 对比方法

冻结base；G-flow/U-LMCE单向、shared attention/MLP/private、embedding-only与final-norm anchor；G+anchor、anchor-only、closed-form frozen patch、wrong-address derangement、幅度缩小、rank容量分配/同shared rank对照、same-category siblings、下游block删除、joint/U→G recipes。跨架构Janus语义SigLIP、BAGEL语义ViT有窗口；Lumina-DiMOO/Omni-Diffusion VQ/codebook无明确visual窗口，word-target阳性对照验证hook可用。encoder/规模/训练目标协变，不是语义格式必要性的单变量证明。

## 实验条件和发布边界

主7组各480steps、r32 alpha64 dropout.05、AdamW lr1e−4 betas(.9,.95) wd0、20step线性warmup后常数、clip1、bf16，expected/max packedtokens4096/8192、训练/生成512²、seed42；生成30steps CFGtext4。统计按7group bootstrap配对，g0发现、g1–6确认；配置相关，36config SARρ=.68[.37,.88]不是36独立模型实验。源码scale anchor-only direction=gen/task_weight0仍构建gen数据、VAE encode、model(**data)得flow loss后乘0，再附加name anchor forward/backward；无flow更新成立，但“每步只做约80token一次前反传”的总算力描述不由当前公开loop支持，未测运行耗时/推定历史版本。closed-form max_steps−1跳过优化仍需地址读取、计算δ及生成。官方repo1203树节点/1159文件，公开脚本与结果JSON静态核对，未下载权重/启动模型。

## 主结果

T1 7组匹配/identity：base .243/.039；Gboth .520/.653；GMLP .620/.717；Uboth .989/.360；Uattention .984/.078；UMLP .991/.339；anchorL14 .898/.808；finalnorm .332/.103；G+anchor .946/.907。TransferRate G→U .36[.23,.49]、U→G .54[.41,.67]，差.17[−.05,.40]，方向rate差未确立。T2单组Uall全词/首词PMI .938/.922，G .141/.125、base .141/.125，说明G匹配提升不等于命名评分可用。T18独立8概念×6held图：U自由命名1.000，G/base0；禁真实类别后同为1/0/0；伪词对真实类别2选U1、G.0833、base.0208，原文JSON有逐回答，G和base常答Axe等类别，单组不能扩所有任务。T4七组activation DINO sites0/3/7/10/14/17/21/24/25/26/27/norm=.323/.528/.584/.366/.040/.047/.033/.038/.040/.037/.039/.039；CLIP=.269/.433/.512/.281/.054/.051/.048/.056/.051/.056/.051/.051。weight sites3/7/10/14/21/24/26/27/norm=.602/.769/.800/.808/.352/.271/.202/.115/.103，未测点不补0。T5跨架构base→峰值BAGEL .036→.584，Janus .052→.583（wordtarget.625），Lumina-DiMOO .104→.167（word.656），Omni-Diffusion .250→.250（word.500）。T6单组按相近identity匹配：base GenEval.681/identity.036；patchL3 .681/.930；anchor480 .680/.930；UMLP1600 .680/.445；U→G1760含160flow .680/.891；anchor+480flow .638/.953；joint640含640flow .692/.820；G960 .401/.922。不得把.930与7组.808/.584混用，或称所有flow必损通用能力。全部18表逐单元另存结构化证据，区间/组SD保留原表。

## 消融及进一步实验

F3 readout intervention SAR .583→1，identity .562→.492（delta−.070）；只说明对齐提升未带来额外export，不能把最终identity写成−.07或绝对0。T7四预注册主要对照6/6确认：L14vsnorm identity+.672[.59,.74]、matching+.554[.50,.60]；anchorvsG matching+.381[.27,.49]；UMLPvsattn identity+.219[.14,.31]。两次要结果未重现而撤回：anchorvsG identity+.135[−.04,.29]5/6；GMLPvsdefault+.049[−.06,.17]2/6。T9单组patchL3 .930/L7 .828/L14 .016，不能代七组峰L7.584。T10固定rank32转私有时Gdirect .773/.883/.781/.531/.102，cross .575/.700/.525/.412/.138，整体负趋势不严格单调；Udirect1/1/1/1/.138、cross .531/.445/.398/.242/.016，末点U梯度不达adapter为退化检查。T11从patchL7删除下游2/4/6块identity .742/.102/.016，CLIP漂移−.0065/−.0832/−.1084；上游删除均0但漂移更大，损伤不匹配，作者撤回单独因果归因。T12/13 hooked路径且有gradient的共享度BAGEL .5、Janus.873，grad-only BAGEL.961明显高估；参数总量/路径节点均单列。T14Janus embedding .240也高于base.052，不能以BAGEL embedding失败概括所有模型。T15同hook wordtarget有效控制后两模型visual null，但只限所测概念/层。T16同类24bank coarse/fine/sibling：base .047/.031/.484；G .906/.724/.758，降.182[.09,.29]；U .424/.344/.706；anchor+flow .966/.888/.914；anchor .802/.747/.878；patch7 .323/.307/.690，类别shortcut确有影响。T17错地址L3为0对真.930，四分之一幅patchL7 .086、L24 .031，幅度/概念特异性分开。

## 局限与疑问

因果结论限选定模型与干预：位置、可用下游计算、表示读出和权重更新机制不能压成一个普适必要定律。语义vision与窗口跨四模型关联，需同骨干控encoder/目标/算量。开放命名仅单组，主production为有限候选排序；gallery仍可见细节变形。小概念量与单seed主注入、不同baseline任务/随机底座/饱和上界影响TransferRate，不能假定SAR≈行为性能。T6通用性553prompt但仅1个8concept注入组且匹配identity未匹配steps，joint是明显反例，41%下降限G960配方。论文称Janus/BAGEL获得93%/80%trained gain用.583/.625与.584/.724原始比，非baseline校正gain。闭式方向对齐不优化整体InfoNCE；weight与activation峰值差不能消除函数改动与静态向量的混杂。当前源码anchor-only仍有零加权flow前向，需实测/改loop才能支持总算力的短序列成本主张。

## 预期优势条件

若理解路径已给视觉实体有用语义地址，早/中层共享计算可能把名字绑定交给已有生成器使用，以少量地址参数或无flow梯度保留通用生成。证据支持BAGEL/Janus的有限概念控制实验；映射到笔顺需新规则事件、时序表示及真实执行检查，静态类别检索不足以证实。

## 可证伪实验

Q1窗口与语义格式是否必要：同一UMM固定参数/训练/数据，分别换semantic encoder与codebook及可控投影，扫描同幅/同预算激活与权重edit，明确free naming/候选PMI/实例检索/组合/通用遗忘；同损伤控制下游删除，并按concept/group/seed报CI。Q2是否能迁移书写过程：将新笔画规则或新字事件序列只教理解侧或动作侧，去重笔画/部件/字体、分布外顺序与长度；测自由说明、笔序合法率/pen-up/down/轨迹和视频时间一致性，候选识别分开；与静态概念及显式轨迹token对照。用真正跳过flow前向的anchor loop分别报完整地址读取/优化/生成walltime及峰显存、等steps/等walltime结果。均为研究设计，未执行模型。

## 论文组织与Claim学习

按识别→命名→生成和readout→usable分解claim，发现/确认分组、撤回CI跨0的次要结果和承认下游删除混杂值得采用。正文/附录18表把单组/七组、原始分数/校正率和不同检测器分开。关于“入口门控”的标题应对应具体模型/概念范围；低成本要以实际执行路径计入全成本，零loss权重不能充当省掉forward的证据。

## 实际阅读范围

arXivv1全部27页§1–9、AppA–J及引用、全部4编号公式和SAR/闭式推导、F1–10原页实际视觉、T1–18全部单元；官方固定commit README/REPRODUCIBILITY、anchor.py/hidden_ti.py、ctxfree naming/understanding/generation/open-naming probe完整静态阅读，trainer训练/闭式初始化、matrix scale/entry/recipe、GenEval及容量统计的相关入口/条件阅读；3份开放命名JSON逐协议与示例、5份GenEval聚合JSON核对。未声称逐行读全1159文件、未加载模型/执行训练推理或独立复现。核心三遍及五项书面验收完成。

## 单组与七组的边界

七组activation峰L7 identity .584；单组L3 .930，不能用单组高分替代56概念汇总。T6通用生成匹配identity、非等steps，OWLv2检测分只在相同harness内部解释。T18单组48held图有真实自由解码证据：U全部产伪词、G/base均无；主T2 production仍为候选PMI排序。

当前trainer在`task_weight=0`时仍执行`model(**data)`及可能的VAE编码，之后乘零；anchor另计算短名字序列。无flow梯度和省去flow计算须分开验证，此为公开版本代码事实，不推定作者历史运行。

结构化专题保留全部18表原始单元及实际视觉图号。
