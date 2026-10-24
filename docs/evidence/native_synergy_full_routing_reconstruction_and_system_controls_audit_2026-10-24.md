# 原生UMM协同：完整路由、重建数据与系统对照审查

第一百八十三批完成[U17](../reviews/U17.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/native_synergy_full_routing_reconstruction_and_system_controls_audit_2026-10-24.json)。358目录（331论文／研究、27资源），288核心/293书面含未通过项；待完成核心深审43篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2609.01607v1)、[主源2](https://arxiv.org/html/2609.01607v1)、[主源3](https://arxiv.org/pdf/2609.01607v1)、[主源4](https://huggingface.co/papers/2609.01607)。

## 研究问题

在不引入预训练视觉encoder/VAE先验、但保留预训练语言模型的pixel-in/pixel-out UMM中，理解与生成何时出现互助、干扰或仅共存？分别以表示层路由、几何/SVG/3D任务及推理编辑系统实验检验；无笔顺/手绘过程模型。

## 现有不足

同一接口能做两任务不等于共同训练产生收益；既有研究常混入视觉预训练、额外模块和数据变化。本文以同Qwen3初始化、单任务与联合训练、冻结probe及同源数据目标变换提高可解释性，但路线、重建数据和预算仍需进一步拆分。

## 贡献

三级干预框架：dense和modality-decoupled MoT表现相反的任务取舍；提出task-decoupled MoT，保留理解图像与语言共享、生成图像专化及shared attention，并加入重建；三类领域任务与同源Textual-Desc几何参照；同源推理编辑数据比较端到端和planner→executor。提供比跨模型相关更直接的训练证据，机制解释仍有混杂。几何只报告Gen→Und，双向验证来自SVG和3D。

## 输入、模块、输出与公式

两卷积把像素转32×32 patch tokens，随机16层pre-buffer连接Qwen3-1.7B；文本AR，生成图像连续flow matching；整体多模态序列因果，同一图内部双向，MRoPE-I位置编码。t/noise scale由MLP嵌入加入视觉输入，无外部图tokenizer/VAE，无编号目标/采样公式。图像理解→文字或SVG代码；文本/SVG/上下文图+噪声→像素图。SVG的image→code属于论文Und，code→pixel属于Gen；生成代码并渲染与直接像素生成的输出通道需区分。

## 模型结构

Dense：Text、Und-V、Gen-V全用同LLM层。Modality-decoupled MoT：Text留预训练语言支路，全部视觉token入随机视觉支路，跨支路global attention。Task-decoupled MoT：Text和干净理解/条件图token入语言支路，噪声生成token入专用生成支路；共同文本及editing跨图注意力维系语义联系。另加掩去条件图50%视觉token的重建任务，主文称训练mixture额外20%，AppA.1称在3:6:1上additional two parts，归一分母/替换关系未充分说明。它是路由+辅助重建联合设计，不能把全收益归给路由。原生专指视觉接口，语言参数有预训练。

## 数据分布与划分

SenseNova-U1定制采样：Und:T2I:Edit=3:6:1；训练210k步论文列约78M/159M/26.5M流曝光，单任务仅对应流；保持联合与单任务对应流batch相同，未给总FLOPs/完整batch/token曝光。生成只English prompt、去infographic并降低文字渲染样本权重。F7理解流占比GeneralVQA23.7/TextOnly19.8/Caption19.1/OCR11/SI9.2/ChartTable8.1/Reason4.9/GroundCount3.6/Code.7（展示舍入）。几何965K理解及MathCanvasImagen/Edit，未列生成数；SVG359K UniSVG pairs用于双向；3D生成SpatialEdit500K+ScanNet/++1.6M、Objaverse248K、VSC880K、Omni3Dlayout332K。每任务50%一般数据且移除对应域；3D另重训去SI base，缺逐项移除清单/scene级split和自建testIDs。

## 指标与评价协议

理解19项分5General/5OCR/9视觉空间类，表1类均值、T8逐项；SEED只image、MMERealworld lite、MindCube mini、PerceptionBench MCQ，temperature0。生成GenEval2 atom-level、DPG、HPSv3、aesthetic（不可互换）；1024²/CFG4/50采样步/timestep shift3。SVG用UniSVG SSIM/LPIPS/CLIP加权分，本文未给权重/执行失败处理。3DSpatialEdit VE/FE越低好，VSC PSNR/SSIM高和LPIPS低；未为另外两类3D生成任务报告独立结果。冻结probe：ImageNet全局pool+linear/LARS100epochs；ADE20K/NYUv2用3个conv-upsample头30epochs，后两者非纯linear probe。CKA为COCOval5000图文pair pooled text/gen image层特征，未干预alignment机制。

## 对比方法

Dense和modalityMoT各Und/Gen/Joint；taskMoT主表只有Joint，无其同架构单任务及去重建参照。几何Und、同源图生成数据转caption/源目标编辑描述的Textual-Desc、Und+Gen，较好控制附加数据来源，仍缺等目标token/计算和目标信息强度。SVG/3D同架构对应单任务；编辑同taskMoT checkpoint，原同一批例变三训练格式：端到端隐式请求→显式指令→目标图，planner只出显式指令，executor看源图+原隐式请求+显式指令→目标图；pipeline不是无源图/无原请求的弱设定。

## 实验条件和发布边界

T7表示训练AdamWβ.9/.95 ε1e−8、LR1e−4 constant/warmup2000、210Ksteps、WD0/clip1/EMA.9999、CE:MSE=.1:1、16Kcontext、Und256²–2048²/Gen512²–1024²，logitnormal μ−.8 σ.8、noise scale sqrt(N/64)。等步数及对应流batch不等总计算预算；未给各架构total/active params、FLOPs/GPU时、task/system微调步数/比例及完整运行seed。论文未给本研究独立代码/权重/datarelease URL；定向检索和HFpaper API未定位确认制品（linkedModels/Datasets/Spaces皆空），SenseNova模型不能替代本研究各实验checkpoint。未模型训练/推理/judge或独立复现。

## 主结果

T1 Dense三个理解均值67.82/71.96/60.72→68.69/72.12/61.77（+.87/+.16/+1.05）；生成51.16/79.11/7.05/5.12→51.03/78.12/5.92/4.94四项降，GenEval2仅−.13不泛称全部大幅。ModMoT理解64.20/66.84/59.54→61.58/62.11/57.49三项降，生成57.55/82.06/7.72/5.37→63.47/83.09/7.97/5.48四项升。TaskMoT69.02/72.09/62.38、63.96/82.31/7.90/5.50；非所有列最优：OCR略低denseJoint72.12，DPG/HPS低modJoint83.09/7.97。T2Und→TextualDesc→Joint：Geometry3K59.90/63.56/65.39，PGPS9K72.40/73.90/73.40，MathVerse60.13/59.11/63.15，MathVista71.80/73.60/74.30；Joint比Und全升但PGPS低TextualDesc.5。T3SVG80.64→81.70、80.21→86.52。T4 3DUnd均57.15→59.01，8升1降ViewSpatial58.75→58.07。T5VE.4062→.3766、FE.6564→.6297；VSC16.76→19.15、.6365→.6674、.3828→.3078。T6RISEoverall16.66→18.88，KRIS66.48→68.33；RISElogical11.76→9.41，七个非overall子项6升1降。全10表原展示数据保留结构化audit。

## 消融及进一步实验

T8–10完整逐bench/skill结果显示类均值掩盖任务冲突：dense理解19项并非全升；modGenEvalverb13.75→9.28而Overall升，DPGentity89.82→88.12。F3冻结probe早中层joint多较好但后层小差，未列raw/CI；F4四组PCA可视化只作精选例，sharedPCA无拟合split/方差详单。F5所有画出层jointCKA更高，但CKA增高和生成提高并列不足证明中介因果。F6BlindVQA Gen49.41/Und52.18/Joint58.54，基于UniSVGtest用作者记作GPT5.6luna的annotator造3000再筛base答错1370；无全3000对照、独立人审、选项频率/shortcut或跨base筛选。F6右六例一步clean预测形状较清晰，非一步最终采样分数。F8三SVG代码问齿数/箭头组合/购物车把手；F9–10各两例四任务只示输入目标，非逐模型失败率。

## 局限与疑问

路由设计与额外重建共同改变，缺taskMoT单任务/无重建因子对照，跨dense/MoT容量和总计算未对齐；等流曝光减少数据量混杂但联合训练消耗更多任务。结构原生仍含Qwen预训练知识，不能称无任何先验。知识共享是三个正向case归纳，无不相关域负对照或梯度干预证明必要条件；TextualDesc监督信息量和算力未严格等值。SVG1370选择于base错误，限制外推全体分布；可通过符号解析/统计图形实现解题，缺此baseline不能断言必须内部像素模拟。3D自建VSC为给1/2/4/5补3的双侧插帧，含未来帧，不证明纯自回归未来预测/物理动力学；split隔离和test大小缺，静态布局/多视生成未量化。系统同源samebase是实质控制，但无GT显式指令oracle、共享权重不同接口、等训练/推理预算和连续hidden→纯文字handoff拆分；两overall提升不支持普遍优于模块系统。无多seed/CI/显著性。

## 预期优势条件

对于文字/笔顺/艺术字/素描视频，可把矢量程序或轨迹→像素与图像→程序联合，分离干净条件和噪声输出路径，保留共享语言/约束注意力。优势预期在双向任务共享真实几何/笔画因果结构且有配对监督时更明显；SVG路径序列不保证合法书写笔序，插帧提升也不能外推因果落笔。若强调非汉文字，需加入非English条件和文字渲染数据，此论文特意降权此类样本。

## 可证伪实验

Q1任务路由是否独立有效：在等架构total/active参数、FLOPs和每流曝光下交叉路由dense/modality/task×重建0/20%，补taskMoTUnd/Gen，固定初始化多seed，报告19理解项与四生成项Pareto及CI；随机配对/不相关域辅助目标和无跨支路attention作负对照；若只加重建已解释收益，收缩路由归因。Q2系统/共享知识是否解释收益：同源例、同目标信息、等训练token/总算力与推理预算比较共享checkpoint单/双call、纯文字handoff、hiddenhandoff、GT显式指令executor；分开planning正确与execution保真。SVG按未见path组合/变换程序分split，保留完整3000+错题1370，符号SVGparser baseline与盲人审；3D按scene/object/trajectory隔离，自建VSC区分插帧和只见过去的预测。文字轨迹用可执行渲染核验顺序/拓扑/时间，未执行这些模型实验。

## 论文组织与Claim学习

三级问题逐层扩大、用相反方向退化引出设计、再同源目标转换和系统对照，结构值得借鉴。native先清楚定义为结构原生很必要；文字中的bidirectional覆盖范围、joint不全项提升及不确定性也应进入摘要/结论。设计+辅助数据必须因子化，equalsteps不能代替预算表；机制probe需注明诊断还是干预；自建错题筛选和插帧应明确分布/信息条件。

## 实际阅读范围

完整23页v1研究正文§1–8及AppA.1–A.5/B.1–B.2、T1–10全部主/分项结果与T7训练配置、F1–10全部（13图资产；PDF交核布局/图例/三SVG和四3D格式），无编号公式，全部内联噪声/训练配置已核。结构化表与证据边界记录；官方独立代码/模型/data未定位，未提升为制品全审或独立复现。核心三遍和五项书面完成，无独立口试。

## 识别范围

本文通过改变训练任务和架构，具备比不同模型排行榜相关性更直接的干预证据。核心三遍完成仅指论文研究内容。task-decoupled路由与辅助重建共同改变，且缺同架构单任务与明确总计算预算，收益不能完整拆给单一机制。

几何只报告生成对理解的迁移；SVG和3D有两个方向的评测。系统两项总分更高但RISE逻辑更低，未测更广planner/agent空间，不能写普遍端到端优越。3D的VSC是已见未来帧的插帧。

追引SenseNova-U1/U1.5、Transferability U18、UniSVG、MathCanvas、SpatialEdit和既有原生模型；引用关系不自动提升这些条目的阅读状态。
