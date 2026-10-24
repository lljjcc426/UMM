# CoT-RVS v4：完整在线协议、格式失败与发布实现审查

第二百零二批完成[L056](../reviews/L056.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/cot_rvs_v4_full_online_and_release_audit_2026-10-25.json)。358目录（331论文／研究、27资源），307核心/312书面含未通过项；待完成核心深审24篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2505.18561v4)、[主源2](https://arxiv.org/html/2505.18561v4)、[主源3](https://arxiv.org/pdf/2505.18561v4)、[主源4](https://danielshkao.github.io/cot-rvs.html)、[主源5](https://github.com/DanielSHKao/CoT-RVS/tree/91b39c3a199e6badb06ff2f355530f3748506c98)、[主源6](https://github.com/DanielSHKao/CoT-RVS/blob/91b39c3a199e6badb06ff2f355530f3748506c98/T-ReasonVOS/meta_expressions_temp.json)。

## 研究问题

隐式/时间敏感自然语言query定位视频对象，输出逐帧mask；离线允许全clip挑keyframe，online扩展只逐帧更新当前key并前向传播。新式onlineVIS/目标身份切换主要定性展示，传统onlineVOS有量化表，二者须分清。属于理解/分割，叠加mask的视频可视化不构成视频生成或手写生成。

## 现有不足

单帧隐式推理或只按出现首帧定位，容易选错依赖动作/事件的对象；MLLM先描述逐帧证据再选对象/时间，专业图像分割和视频传播各司其职。无需为本任务额外训练，但SegZero/SAM2/MLLM已有预训练与任务训练，不能写成所有模块从未训练。

## 贡献

Fkey从候选帧网格和query产生{object_index,keyframe,object_description}列表，Fseg从选定图像/描述得初始mask，Fvid传播到全clip；加入online版本和180query的T-ReasonVOS。模块化三个模型，多agent是论文的模型编排术语，非单体统一理解生成模型。

## 输入、模块、输出与公式

Eq1–4 q+按时间排列候选帧→逐帧QA/分析与对象列表→keyframe mask→前后双向传播；候选最多8，ξ=floor((T−1)/8)+1。Eq5–6多个mask按既有object顺序互斥后处理，先列对象有优先权，基准评价多对象union。Eq7–8定义online前向流程，Eq9 Fkey仅看q和当前图像给二元是否可定位；Eq10–11 Yes更换key，No沿用旧key，首个key前为空；Eq12原q及当前图像给Fseg，再SAM2向前。不回改过去预测；未有事件状态机、跨帧MLLM记忆或新旧key质量比较。

## 模型结构

offline selector GPT-4o或Gemma3-27B；online LLaVA-1.6-7B为主，可换Qwen2.5VL3B/GPT4o；SegZero7B预测一bbox+两个正point，SAM2image predictor选最高分mask，SAM2video predictor跟踪。online No不显式清除旧target，二元是否可见不保证语义消失即停mask。某些复数群组被单bbox/单object接口压成一个鹅，论文A5示例失败。

## 数据分布与划分

ReasonVOS91video458query（MeViS18/MOSE26/BURST37/VIPSeg10）；T-ReasonVOS人工筛时间敏感子集180query45video（8/18/16/3）。固定repo实际JSON逐条核45video180唯一exp_text，query按来源MeViS49/MOSE83/BURST40/VIPSeg8；is_sent字段True75/False105，README未指定以此滤样本，不擅自只统计75。query手工避免歧义，仍有冷时hoodie/blanket都合理案例；未给多人一致性/按来源完整分层。其余RefDAVIS17、MeViS、ReVOS测试；继承预训练数据的交集未视频级审计。

## 指标与评价协议

J regionIoU、F boundaryF，J&F均值%；多目标按union评价，未报告VIS AP/IDswitch或事件切换延迟。格式有效率单列于A4；公开脚本仅演示、无总评测/失败分母，不能确认无效列表在主表计0或排除。A4ReasonVOS两种失败模型分母写785，与该集458不符，保留原表错误，不能照抄当样本数。

## 对比方法

MeViS/RefDAVIS/ReasonVOS/ReVOS比较传统RVOS和reasoning法如SAMWISE/GLUS/HyperSeg/VideoLISA/VISA；T-ReasonVOS对LISA、ThinkFirst+SAM2、VideoLISA-OTSA。模型大小、闭源API/训练集及推理预算不统一。A5用同Gemma selector交叉LISA13B/SegZero7B与Cutie/SAM2，隔离部分模块效应；online selector消融只有固定传统基准，动态referent新setting无专门量化集。

## 实验条件和发布边界

论文无本任务finetune；候选8，GPT4o温度.5,max2500；online论文ξ4。模块时间/内存RTX4090，8帧网格且帧324规格，API服务器时间依赖服务。固定公开commit91b39c3a199e6badb06ff2f355530f3748506c98（2026-03-17），读15个文本/源码文件含requirements与metadata；README/demo online默认ξ10，API源码max2500但省略temperature，LLaVA温度0/beam1/max512、Gemma greedymax2048，grid最大维3200。requirements仅sam2未锁版本，未独立审其内部未来访问。未调用模型/API/OCR/训练。

## 主结果

全部11编号表核：MeViS J&F online45.9/Gemma44.2/GPT52.2，对GLUS51.3、SAMWISE49.5；online不领先SAMWISE。RefDAVIS73.9/74.6/79.1，对HyperSeg71.2。ReasonVOS52/50.7/65.5，对GLUS49.9。ReVOS46.2/47.1/55.9，对HyperSeg55.7；GPT优势仅.2pp且无CI。T-ReasonVOS LISA31/ThinkFirst33.6/VideoLISA37.4/Gemma50.2/GPT55.5。A4有效列表MeViS Gemma715/78591.1%（分割52.6）、GPT761/78596.8%（60.1）；ReasonVOS Gemma273/45859.6%（50.7）、GPT444/45896.9%（65.5），LLaVA/Qwen网格离线0有效。不可由有效率推断已解决所有失败。

## 消融及进一步实验

T6 GPT候选4/8/16的ReasonVOS J&F66.2/65.5/60；选8兼顾覆盖/成本，并非最高得分；帧数与grid像素同时变化，不纯粹测推理容量。F8是CoT/无CoT/随机key定性图，没有数值可补，已纠正旧记录“图8数字不可读”。无CoT源码仍沿用chain-of-thought systemprompt，用户prompt才删显式分步要求，不能当严格去除所有CoT控制。A5同Gemma：LISA+Cutie68.8、LISA+SAM271.1、SegZero+Cutie72.1、SegZero+SAM274.6。A1模块秒/GB GPT12.01/API$.012；LLaVA1.71/15.6；Gemma63.95/24.8；SegZero4.57/18.1；SAM2 .04/2.6。A2端到端Gemma69.79s/GPT17.85s vsVideoLISA3.46s；A3online selector Qwen72.5/.18s、LLaVA73.9/.24、GPT73.2/.27。不同计时范围与API条件，.24s不可直接推广所有视频端到端FPS。

## 局限与疑问

online demo init_state预载完整frame目录(offloadCPU/async)，保留original_imgs/seg_imgs/video_segments随T增，不证明实时输入或固定总存储；是否SAM2内部无未来泄漏须锁依赖后另查，不能只凭预载就判定用了未来。每ξ帧当前图freshconv，LLaVA parser仅最后5字符含Yes.且按This is because切分，格式可改变更新决定。offline ast.literal_eval无失败评测处理，A4大量无效时总体分母不明。未给模型/数据全部version、seedCI、在线新setting的数值/标注，贪心替换无跨帧推理状态，No仍追旧mask。源code Apache2；TReasonVOS明确非商业研究并承接来源许可，代码license不覆盖数据许可。

## 预期优势条件

当可定位证据稀疏且后续mask易跟踪，先全局挑有信息帧再分割可改善隐式query；当未来不可见且referent会变，当前帧判断+重置mask能适配部分变化，缺历史语义状态时仍可能误更新/滞留。对手写只能迁移关键动作证据选择和追踪模块，mask几何及逐帧描述不验证规范笔顺。

## 可证伪实验

Q1CoT与key选择是否独立有效：同candidate/frame像素、selector与tokenbudget，移除所有system/user分步引导、直接列表/随机/首帧，预声明parse失败计0并报有效率和条件分数；按时间敏感/静态query拆解，检测依赖帧间信息与像素容量。Q2online真满足prefix/切换吗：锁SAM2依赖，同prefix改future检查当前mask不变，实测流式输入/内存，明确No时语义停用策略，报告switchdelay/早判/ID错误/空mask。手写用相同终态不同落笔顺序/接触状态，key选择、轨迹跟踪与规范规则各自留出评价。仅设计未模型执行。

## 论文组织与Claim学习

表明offline/online各自可用信息和输出是否可修订；把传统固定对象量化与新动态referent定性分开。关键帧数量应同时写grid分辨率和token预算。格式有效率需和主分数分母联立，清楚区分未finetune与模块预训练。图8无量化数值，不能虚构缺失数字；代码演示的预加载、ξ10、温度省略与论文ξ4/.5差异应披露。

## 实际阅读范围

v4全24页§1–5、AppA–K、Eq1–12、T1–6+A1–A5所有单元，F1–8+A1–A7共15图及全页实际视觉；references页清单/关键引文核，未声称逐篇读引文。固定commit15个源码/说明/metadata文本核读，JSON确定性计数；未下载/检查全部原视频或运行模型/API，未独立复现。核心三遍与五书面完成。

## 发布标注与论文的对应

固定commit中的T-ReasonVOS共45视频、180条唯一查询；MeViS/MOSE/BURST/VIPSeg视频8/18/16/3，查询49/83/40/8。is_sent字段True75/False105，使用说明只要求替换原metadata，未要求过滤该字段。

## 图表与评测边界

图8只有定性样例，旧记录对不可读数字的要求已撤销。A4提供格式有效率，但演示代码未提供全基准失败分母处理。因此当前材料不足以确认主表是否把解析失败记为零分。在线固定目标基准有量化；动态目标切换新设置主要定性。
