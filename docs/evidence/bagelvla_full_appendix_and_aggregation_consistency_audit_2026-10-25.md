# BagelVLA：完整附录与表格汇总一致性审查

第二百一十二批完成[L165](../reviews/L165.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/bagelvla_full_appendix_and_aggregation_consistency_audit_2026-10-25.json)。358目录（331论文／研究、27资源），317核心/322书面含未通过项；待完成核心深审14篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2602.09849)、[主源2](https://arxiv.org/pdf/2602.09849v2)、[主源3](https://cladernyjorn.github.io/BagelVLA.github.io/)。

## 研究问题

让机器人根据全局指令和当前多视图观测，显式生成子任务文字、未来关键帧表示及动作块；在长程操作中提高计划与控制且减视觉预测延迟。

## 现有不足

语言规划与视觉预测通常分开，完整先预测图再逆动力学动作延迟高且预测误差/OOD图影响控制。作者用统一MoT与分阶段学习接入动作，RFG给当前图结构先验；并未证明所有真实场景都受此机制支配。

## 贡献

BAGEL理解/生成专家加2B动作专家，完整/联合/初始一步三种双FM交互；RFG从N(vt,I)而非N(0,I)起并缓存初始图特征供动作。两阶段跨模态规划/预测预训和有动作下游微调，启发式控制方案，无形式因果或全局最优保证。

## 输入、模块、输出与公式

全局指令L+多视图当前图+部分实验本体状态→子任务lt/未来keyframe与连续actionchunk；真正执行依靠初始视觉KV即可，不要求先解码完未来像素。关键帧预测不等于持续视频、落笔/抬笔/接触力或标准笔顺。

## 模型结构

BAGEL两个Qwen2.5-7B式专家+2B action，28层/hidden3584，语言/图FFN18944、动作3584，ViT SigLIP2+FLUXVAE/256²。语言CE，图/动作FM速度MSE；§3.1 logp乘积写法与§3.2负logp是概念建模，未精确likelihood求解。图t~LogitNormal0,1、动作Beta1.5,1；τ0noise/1target。F7完整方案动作读GT clean target(训练)/生成target(推理)，joint读同期noise；single与RFG只读τ0KV且mask禁止读GT target。RFG初态均值为当前VAE；不据其单步特征证明已准确预测完整图。

## 数据分布与划分

正文§3.5 GeneralVQA2.98M、人手310K、公开robot146K规划+297K动态、自采75K；AppC1改成2.56M/310K/382K/4.5K，T6明确558K+2M=2.558M，公开120K+80K+99K+55K+27.5K=381.5K，自采4.5K。保留冲突不任挑一版作精确实际训练。Stage2 CALVINABC、RoboTwin50任务×50clean=2500、Aloha basic3K+long1.5K。C2长程只列视觉动作但正文和T3有语言规划，标注名称也未完全同步。Seed1.5VLthinking仅数据标注，F12子任务+帧界JSON/F13全局句子，筛选标准/错误率/划分manifest未公布。

## 指标与评价协议

CALVIN D上1000条5任务链平均完成长度与各阈值完成率；不能因单个技能短就把整评测称单步。RoboTwin每50任务100次Clean/Random/unseen指令平均成功；真机各任务/难度20次。planning accuracy为20个中间状态的correct motion trend，非精确完整轨迹正确率。F6有errorbars但定义/seed/CI来源未交代；未独立复跑。

## 对比方法

π0/RDT/UPVLA/VPP，以及去keyframe/去text/RFG/预训。真实动作数据称相同但总体预训练与模型容量不同；未见与全部基线匹配总compute/teacher标注预算，不能全归统一架构。

## 实验条件和发布边界

全局LR1e-5/FSDPpacked，预训64A800/b~1600/20K；CALVIN8卡b192/30K/chunk10/no proprio/2view预测第3，RoboTwin8卡b128/60K/chunk16隔3步有效48、3view预测primary；真机32卡b512/50K/chunk24/3view。正文速度RTX5090 chunk48/1.2s→40Hz是动作吞吐，与AppD真机chunk24条件分开；async只更新本体、低频更新视觉KV→72Hz，未给最大观测陈旧/完整控制延迟分布。训练随机换更早帧适应async。

## 主结果

T1 CALVIN4.405>VPP4.329，但T8整5步完成.741<VPP.769；前四阈值优势累积提高平均，不能说每长度都赢。RoboTwin作者表75.26clean/20.87random，泛化绝对率仍低，多个任务random0、OpenMicrowaveclean0；T7去keyframe clean行均值46.72却汇总56.72，Bagelrandom行均值20.48却汇总20.87，π0random16.36却汇总16.34。已按PDF50行12列重算列均值并视觉核表，未知原始runs或何处错，未擅改作者headline。T2平均75.5优π65/VPP59.5，但vase35<40/50、drawer95<100，非全任务最好。T3stack73.3/算式63.3、plan95/85，细动作成功低于计划；每难度20，尚无显著性推断。

## 消融及进一步实验

T4限定单view/10Ksteps/A800延迟20次：complete6.04s/2.480、joint2.90/2.038、naive single1.23/3.345、RFG1.23/3.600；图50动作10，主表多view30K4.405不能混。F6 naive single在PourFries25<无预训40，RFGfull45，作者正面收益也有任务差。F5/11显示5/10/20步视觉样例，未给FID/预测校准或构图变化分层；没有同compute真/生成/打乱/纯噪关键帧检验未来语义必要性。语义/OOD/背景解释为机制假设，非因果隔离。

## 局限与疑问

28页AppA–I/13图8表/3编号式及未编号目标全核。正文与附录recipe/表聚合存在实质冲突；原始run数/样本名单与代码缺失无法定正。官方页Code is coming soon链接仅github首页，无可用项目代码/checkpoint。F12示例以字面看含省略对象大括号等非严格JSON，未见parser代码/失败率不能直接保证标注可解析。I的LLM solely grammar应限定稿件写作阶段，§3.4仍用teacher标注。未进行视频逐帧真机复验，demo精选帧不证明全失败分布/鲁棒安全或动态书写能力。

## 预期优势条件

背景多保留、子任务可语言分解且动作需快于完整图采样时，当前图初始化/初始KV预测特征可能改善控制；大运动、新对象或背景突变会削弱先验，需独立验证。

## 可证伪实验

统一数据版本及全部50任务原始runs，确认T7聚合；匹配总compute做动作only/textplan/真实或生成或打乱或纯噪keyframe/RFG因子。固定视角与训练步数，分报完整5步、meanlength、每任务CI和plan/action错误。测视觉更新时间、KV陈旧、端到端延迟、动作吞吐及async失败；写字加落抬笔、接触力、笔顺事件和字符终态独立评判。未执行。

## 论文组织与Claim学习

方案依赖结构→mask→延迟/成功率消融组织清楚；meanlength与全部五步成功应同时报，数据recipe/小表汇总须同步。显著/证明/必然语句需统计或因果证据；40/72Hz附硬件/chunk/视觉更新口径，稿件LLM润色声明限定范围。

## 实际阅读范围

最新v2全部28页§1–6/53条references清单及关键关联/AppA–I、T1–8全表含RoboTwin50行12列简单均值复核、F1–13全视觉含10contact、p5架构/p11消融/p22mask/p23表/p27–28prompt放大；Eq1–3和所有未编号logp/FM目标逐项。官方项目页/链接核：codecomingsoon仅github首页；无实现可审。未运行teacher/模型/训练/控制/API，仅来源阅读与表格算术；核心三遍与五书面完成，非独立复现。

## 数据量冲突

正文VQA2.98M、公开robot146K+297K、自采75K；附录VQA2.56M、公开robot约382K、自采4.5K。Table6分项支持附录近似数，仍无法独立认定实际run使用哪版。

## 汇总与完整链

Table7共50行12列的简单均值：去keyframe Clean46.72而作者汇总56.72，BagelVLA Random20.48而作者汇总20.87，π0 Random16.36而汇总16.34。正文headline暂保留为作者报告并标记，未声称已用隐藏GT重评。CALVIN平均完成长4.405提高，但完整五步成功.741低于VPP.769。

## 频率与条件

40Hz来自chunk48/1.2s，72Hz异步可复用较旧视觉KV；AppD真机训练chunk24。Table4单视图10K与主表多视图30K条件不同，比较需要各自标记。
