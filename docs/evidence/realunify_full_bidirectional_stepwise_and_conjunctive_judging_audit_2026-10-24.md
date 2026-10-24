# RealUnify：完整双向分步骤与全部核对项判分审查

第一百八十一批完成[U15](../reviews/U15.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/realunify_full_bidirectional_stepwise_and_conjunctive_judging_audit_2026-10-24.json)。358目录（331论文／研究、27资源），286核心/291书面含未通过项；待完成核心深审45篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2509.24897v2)、[主源2](https://arxiv.org/html/2509.24897v2)、[主源3](https://arxiv.org/pdf/2509.24897v2)、[主源4](https://github.com/FrankYang-17/RealUnify/tree/0b76a109589e7e9b36fa6c6640fdc396db2ecd2a)、[主源5](https://huggingface.co/datasets/DogNeverSleep/RealUnify/tree/0b3609a3f5dbc460a341e78d833fe6272693c855)。

## 研究问题

统一模型能否用理解知识/推理改善图像生成（UEG），以及用生成的重构/变换图改善选择题理解（GEU）？两方向的端到端与分步骤协议用于定位系统瓶颈，尚不能凭任务名称证明每题必须使用显式图生成，或严格测得共享参数的因果协同。

## 现有不足

分别测理解和图生成易掩盖知识虽会回答却不能画出、或辅助图反而损失信息。作者设计需要世界知识、计算、状态更新与空间变换的任务并拆成两阶段诊断，区别基础能力不足与整合困难。更强的因果归因还需额外预算、重写提示、图信息损失和专用系统强度控制。

## 贡献

1000题、10大类32子任务；UEG600与GEU400，每大类100，direct/stepwise双协议、图核对问题polling与专用模型组合。评12统一系统和6专用模型，UEG分步骤普遍提高、可测GEU分步骤总体下降，提示方向不对称。贡献是任务与诊断设计，无新UMM训练、扩散求解器或在线笔顺模型。

## 输入、模块、输出与公式

UEGdirect：含隐式知识/数学/逻辑/code的文本→目标RGB。UEGstep：同问题→先用理解模块输出简单明确的重写prompt→同系统生成图→对人工question_list逐项yes/no。GEUdirect：图+题+四选项→A/B/C/D；GEUstep：原图+恢复/改色/突出区域/标路线指令→编辑辅助图→基于辅助图回答选择题。公开README使用edit_image作为第二阶段输入，未说明一定同时保留原图；这与原图+辅助图的工具增强需分开。仅静态RGB与文字，无笔画事件、落抬笔或连续时序。

## 模型结构

直接使用BAGEL、OmniGen2、OvisU1、UniWorld、UniPic2、OneCAT、MIO、ILLUME+、Showo2、JanusPro、BLIP3o和NanoBanana的原架构与推荐推理，无共同训练或固定骨干的新结构。理解→生成及生成→理解的串联是推理协议；Gemini2.5Pro与GPTImage1组成的外部系统不等同单模型共享表征或参数上界。论文无编号方法方程，公开评分实现可形式化为UEG每题∏k1[judge_k=GT_k]、GEU每题1[parsed_letter=GT]。

## 数据分布与划分

1000同题在direct/step各保一份，并非2000独立新题。UEG10位AI专业高年级本科/博士设计prompt和核对题，三名博士独立审正确性/客观性/答案唯一且全同意保留；GEU脚本造重构/多步改色/迷宫，地图GoogleSearch，attention来自BLINK/HRBench，人审。F4细分32：world7、commonsense4、math5（数值计算分单/多步）、logic4、science4、code1、reconstruction1、tracking1、attention3、navigation2，逐细分样本数未完整公开于T6，T6仅10类各100。HF固定912文件，四JSON全解析600/600/400/400、按(task,index)唯一且两协议ID/GT配对，无全图像像素审；GEU400题仅385不同input_image路径，CI宜按原图分组。

## 指标与评价协议

UEG公开实现每题所有核对问题同时正确才1，非逐核对题均值；600题1546核对项，长度1/2/3/4/5/6分别141/192/125/66/74/2，复杂度和judge累积误差随核对数变化。1434yes/110no，另同一code题有空标签和空dict两坏项；499题全yes，常数yes的解析诊断可达499/600（83.17%），这是偏置敏感性说明，未执行judge/模型且不声称Gemini实际恒答yes。GEU四选一acc，GT A96/B106/C101/D97，均匀猜测25%，恒B26.5%；MT类最高频B33%，部分21/19等低于机会参考。总体按十类等量即UEG.6+GEU.4。图像指标主要检验约束，不评价美学或轨迹执行；缺置信区间/多seed与失败覆盖率。

## 对比方法

12统一=11开源+1 NanoBanana（gemini-2.5-flash-image-preview），6专用=GPTImage1/QwenImage/FLUX1Kontext与Gemini2.5Pro/GPT4.1/Qwen2.5VL7B。T3为按方向direct挑top3统一模型后对照，非全部系统平均。T5组合强专用系统可作当前工程参照，不能视作理论oracle或同compute能力上限；模型年代、训练数据/规模、图输出接口不匹配。JanusPro/Showo2/BLIP3o不支持相应编辑，GEUstep缺测，Nano全部step缺测；缺项不计零且不能用少任务总分与完整榜公平比较。

## 实验条件和发布边界

AppB只说明开源officialdefault/recommended，闭源Nano preview与judge gemini-2.5-pro；未固定各模型SHA/图尺寸/seed/NFE/CFG/token预算/总时间与API历史快照。Direct一次、step额外一次理解或图编辑，未等预算文字CoT/规则工具对照，无训练超参可填。固定GH 0b76a109589e7e9b36fa6c6640fdc396db2ecd2a共13树项/10blob，README及全部两份eval源码全文审；缺模型推理wrapper、完整依赖/历史rawoutputs和配置。eval_generation中judge函数TODO/pass，需自行接入；task_correct_num初始化条件写task_type not in task_dic，对合法六类从不初始化，随后累加或打印会KeyError，阻断当前汇总。异常/None样本也无完整历史处理定义；这些说明当前入口不可直接复现，不推断历史论文运行必然使用该代码。未调用外部judge、模型或训练。

## 主结果

T1–13全部（T3a/b分别）、F1–12实际图和全部附录prompts已核。T2：11开源UEGdirect→step MIO14.5→18.3、Janus25→25.2、ILLUME29.7→32.3、Showo28→29.5、Omni30.3→32.5、UniPic37.5→40.5、UniWorld35→35.2、Ovis31.2→39.3、BLIP33→36、OneCAT37.5→39、BAGEL32.7→47.7；每组展示均升，但.2pp等需配对统计。可测8组GEU均降：MIO25.8→20.3、ILLUME27.8→27.5、Omni32.5→30.8、UniPic24→23.8、UniWorld32.3→28.5、Ovis39→29.5、OneCAT31.3→29.3、BAGEL39.3→35.8。T2 BAGEL总35.3→42.9受UEG权重主导，不能概括双向都升。类别例BAGELcode7→40，而GEUattention50→52/MT31→25/navigation39→28。NanoUEG63/GEU31.8/总50.5。T3专用UEG GPT62.2/Qwen52.2/FLUX40，GEU Gemini54.8/GPT38.5/Qwen34.5；BAGEL39.3高于后两者但低于Gemini，不能归因统一胜过专用。

## 消融及进一步实验

T4 Gemini/Qwen/四人专家对四系统七个direct/step条件均分：BAGEL32.7/47.7对人31.5/44.2；本次按七条件复算Gemini与人aggregateMAE2.1286pp，Qwen7.2429pp。说明该展示范围均分较接近，未提供逐题混淆、κ、评者一致性和CI，不能当全任务judge可靠性证明。T5 Gemini→GPTImage UEG72.7超过Nano63，其中code91，而GPTImage→Gemini GEU31.8低于BAGEL39.3与Gemini自身54.8，可能含图编辑损失及输入替换。F5 lightsaber与玩具车提供成功例，F6给GT中间内容才能改正猎豹/人数，展示中间步骤错误的作用；仅两例不能定量定位全部瓶颈。F7–10共示例，F11–12各16幅失败图展示属性缠绕/数量/奥运环/位置/手指/物理/文字/雌狮错误；无各类失败发生率及随机抽样说明。

## 局限与疑问

需要协同的任务不自动证明显式生成必需：改色可以符号状态更新，注意聚焦可裁剪/标框，重构计数或局部识别可能存在无需完整复原的解法；无这些受控消融时，不以GtA下降证明模型忽视生成或基础生成能力已经充足。UEG重写改善同时改变prompt信息显式性与调用预算；step可能把题解直接传给生成器，不能唯一归因为共享参数协同。当前GEUstep的100个MT记录question已缩成变换后读数，evaluation_prompt仍含完整原始变换命令；若在已编辑图上沿用后者，可能再次要求变换，实际推理调用哪字段无wrapper/历史日志可核。UEGlogical17 direct写adjacent erasers，step误为adjacent birds；code2的question_list含一空question/answer和一空dict，影响当前打分。GEUstep400条保留作者机器绝对路径，需映射到发布相对路径。主表历史是否修正这些项未知，未将发布缺陷外推全部数值。

## 预期优势条件

双向、同题、显式中间内容有助区分“能说出字形规则”与“能画对结构”，以及用草图/布局改善理解。可迁移到题解→轨迹→RGB三侧，但要求真实笔序/落抬笔监督、独立正确性和等预算对照；静态图重构与字形文本判对不能证明生成了合法书写过程。GT中间状态是有价值的上限诊断，需要全题统计而非个例说明机制。

## 可证伪实验

Q1 step收益是否来自协同：同骨干/训练数据/固定总调用、图采样和token，比较direct、自动重写、人工/规则重写、等预算文字CoT、外部专用组合，UEG保存重写答案正确性与图约束满足；GEU原图+辅助图、只辅助图、GT图、裁剪/规则图、打乱或错误图控制。若人工提示显式化或纯文本同预算解释收益，收缩统一协同归因。Q2分步骤下降是否为生成能力不足：修正MT最终question字段、eraser/bird和code2坏核对项，接入固定judge并修计数，按真实处理数和失败率汇总；GEU保留25%/按类别频率机会基线，按385原图分组配对bootstrap。UEG按核对数分层，双向yes/no对称题、人逐项复核与all-check/partial-credit并列；报告原始judge与人混淆和CI。全题GT辅助状态、生成图替换/移除实验定位中间错误，若输入纠正即恢复GEU，不将原下降解释成内部能力无法整合。均为建议，未执行神经推理或独立复现。

## 论文组织与Claim学习

从双向问题到任务设计、direct/step诊断与GT中间状态案例的论文结构清晰。应将额外调用、提示重写、原图替换和共享参数效应分开；“上界”“必需”“充分基础能力”“真正协同”需要受控统计支撑。更新会议状态、明确all-check评分与题数、修正表号T3a/b交叉引用，公开字段/路径和可运行评分器需与主文协议一致。

## 实际阅读范围

完整v2研究§1–5及AppA–C全部末级小节，编号T1–13全部行（T3a/b分表）及F1–12全部实际图/28图引用（26唯一asset）；全部推理/judgeprompt，无编号方法公式。PDF19页取得并与HTML研究内容核对。固定GH13树10blob中README和两份全部eval源码；HF912文件清单及四JSON全量2000行元数据/ID/GT/核对项解析，指定语义差异逐条核，非全部600长prompt或图像像素逐字审。核心三遍/五项书面完成，无独立口试/模型/judge/训练复现。

## 发布与历史实验的区别

本次未运行模型或judge，不提交上游代码修复，不把目录验收视为数值复现。公开当前评分器的计数初始化条件可由控制流直接判定；其与论文历史运行的对应关系未公开。MT同题的最终question字段已经去掉变换，但evaluation_prompt仍保留，复现实验必须明确选择，不能默认历史执行了二次变换。

HF数据的README指定研究使用限制；本批保留元数据计数、必要缺陷定位和短示例，不将四份完整数据或全部图像复制入仓库。GH源码LICENSE与数据使用条款分开记录。

追引现有MMEUnify、UniEval、WISE、T2ICoRe、UniG2U、VGUBench及BAGEL/OneCAT/UniWorld等目录；待审条目仍独立核主源。
