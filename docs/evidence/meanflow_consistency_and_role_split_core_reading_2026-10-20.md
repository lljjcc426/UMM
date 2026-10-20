# 平均速度场、一致性动作与视频角色解耦：核心三遍审查

本批完成[E01 MeanFlow](../reviews/E01.md)、[E02 iMF](../reviews/E02.md)、[E03 Consistency Policy](../reviews/E03.md)三项既有记录的核心三遍审查；经官方SGF仓库追引，新增[D09 SGF+](../reviews/D09.md)并完成同层审查。四项各有五条书面理解检查，覆盖关键公式职责、方法图、主表/现有消融、负结果及相关工作边界。总目录340项，核心三遍累计82项。没有独立模型训练、视频生成、梯度诊断或机器人执行。

## 研究问题与可检验机制

| 工作 | 具体困难 | 方法干预 | 可能受益条件 | 尚不能据此推出 |
| --- | --- | --- | --- | --- |
| MeanFlow | 瞬时速度需数值积分，平均位移监督难取 | 平均速度恒等式、JVP半梯度训练 | 生成器调用延迟主导、训练分布覆盖 | 1NFE保持规范笔事件、全流程无预训练 |
| iMF | 样本条件速度进入JVP有高方差，CFG训练固定 | 预测边缘速度切向、CFG条件、incontext结构 | 边缘估计可靠且需同模型改变引导 | 1.72全部来自目标函数、等计算预算收益 |
| Consistency Policy | 机载多步动作采样反应慢 | EDM→localCTM+DSM蒸馏、初噪/mesh适配 | 低延迟控制且示教与teacher覆盖动作模式 | 机器人低方差对RGB生成同样有益 |
| SGF+ | writer/denoiser共享参数受角色更新限制 | 两套全参数、同DMD经可微KV交互 | 角色梯度差异影响长期视觉稳定 | 等参数收益、长语义或24h任务正确 |

四者均未给出规范汉字笔顺视频完整训练/评价。把生成步数减少、动作低延迟或视觉稳定直接当作事件执行正确，会丢失核心研究问题。

## MeanFlow：场定义与有限模型的边界

[NeurIPS2025官方论文集](https://proceedings.neurips.cc/paper_files/paper/2025/hash/6d13e085b79d454da5910e4ca82a3d9d-Abstract-Conference.html)确认正式身份，本批读正式23页PDF。u是沿marginal ODE characteristic的平均速度；即使训练conditional插值为直线，marginal轨迹仍可弯曲。r固定下u+(t−r)du/dt=v，JVP切向按(z,r,t)为(v,0,1)，换成(t,t−r)输入时要保链式导数。

理想场恒等式可在边界/连续性条件下恢复积分关系；用网络、条件速度、stopgrad与自适应权重训练，尚无全局收敛保证。推理1NFE不等训练一次forward，也不含VAE解码。ImageNet模型从头训练指生成网络，预训练VAE仍属于系统。

主表XL/240epoch 1NFE FID3.43、2NFE2.93；2NFE2.20属于1000epoch XL+。B4/80epoch消融的61.06不能与B2主表6.17或公开B4 guided checkpoint11.4合并。CFGω3 FID15.53、ω5反降20.75；CIFAR2.92仍略差iCT2.83。正式checklist承认单次FID无方差，Limitations答No；笔记中的有限误差和薄笔画疑问是本仓库分析。

[固定实现](https://github.com/Gsunshine/meanflow/tree/d70cb55d298ee03c53bf6da67bec281082e4e2d9)确认JVP、stopgrad、采样和配置。正文c=1e−3是示例，代码norm_eps=.01，不据此推全部原实验固定值。README中的paper/repo数值是作者发布记录，未独立复测。

## iMF：等价重写与实际改动分开

读[arXiv2512.02012v2](https://arxiv.org/pdf/2512.02012v2)。把原MF改写为V=u+(t−r)sg(JVP)回归v，与原目标代数等价；实际改动在JVP切向由vc换成预测vθ。辅助v头共享主体、最后8层独立，需单独FM loss，推理丢弃。JVP仍停梯度，原MF也不因此被判为数学无效。

概念推导写r/t，但Table4和[固定官方实现](https://github.com/Lyy-iiis/imeanflow/tree/bf60cd7cb653f6628e59d48034b333c5eba445e2)只显式嵌入h=t−r：class8、h/ω/tmin/tmax各4，共24条件tokens。__call__接收t但不直接送入网络。该细节应与概念公式分列，不能按条件变量个数推断实现。

Table1同B2/240epoch目标项6.17→5.97/5.68；无CFG时boundary29.42优aux30.76。后续Ω条件4.57→incontext4.09→blocks3.82→长训3.39，分别有贡献。系统XL1.72同时将训练240增至800epoch，推理119增至174.6GFLOPs；参数676→610M不意味着计算也减少。训练ω最高8，eval对M/L推荐10.5，需检验条件外推与搜索偏差。

[固定HF文件目录](https://huggingface.co/Lyy0725/iMF/tree/fbc11eb6687c5b6cff9beec1e6bb28fd2be46adb)含JAX/full/PyTorch checkpoint及两套FID统计；当次API无README/modelcard/license字段。代码MIT许可不替代权重许可核查。发布FID与论文小差、TPU/JAX和GPU/PyTorch统计不同均明确记录。

## Consistency Policy：调用数、端到端延迟和控制频率

正式[RSS2024 PDF](https://www.roboticsproceedings.org/rss20/p071.pdf)核心与[v2 AppA–C](https://arxiv.org/html/2405.07503v2)分版本阅读。四视觉Robomimic各200示教，PushT200、Kitchen566。实机首两任务随机起点、Microwave固定，trial10/20/10。项目页仍称两实机、v2及正式核心有三实机，不能把项目摘要当最新完整实验。

TableI/II 27/9为ParaDiGMS引用速度折算的等效NFE；TableIII实际串行100/15/1/3NFE及P5000毫秒是另一协议。3070Ti端到端Trash192→21ms，网络179→13.5ms、encoder均6ms；总9倍与网络13.3倍分开。Franka底层1kHz、waypoint15Hz，生成21ms不等机器人以1kHz闭环决策。Microwave成功.5→.4，不能把结论“无损”推广全任务。

低方差/mesh/dropout消融在Square/ToolHang有益；教师质量只试有限范围，DSM还给真实动作监督。AppB未收敛CIFAR低方差灰块只作启发，流形维度解释为假设。ODE确定性传输同样可表示多模态，动作偏单侧还需分离初方差/损失/容量。

正式Eq2负号与前文时间约定/官方Euler-Heun正号不一致，已保留符号问题；不推断实际实验采用负号。[固定student代码](https://github.com/Aaditya-Prasad/Consistency-Policy/blob/eed0c465d3c1aa6dcf22f10e784df07dec06beac/consistency_policy/student/ctm_policy.py)冻结teacher/EMA参数，但s→0仍对prediction输入求导；shared观测条件也可能回传编码器。冻结参数、detach输出与torch.no_grad需分别解释。

## SGF+：局部理论支持什么

读[v2全文关键章节及附录](https://arxiv.org/pdf/2610.10429v2)，[固定Git](https://github.com/Zihan-Su/Self_Gradient_Forcing_Plus/tree/7a7734f592f1bdb51edd28f1c42ca95b9f652453)与[固定HF卡](https://huggingface.co/ZihanSu/Self_Gradient_Forcing_Plus/tree/784c07876a43fb924a2e96095b33a5675282225b)交叉核对。writer/denoiser是两套全参数，paper1.4B→2.8B；双LoRA是建议，不是主表已验证版本。README补充64GPU无累积、frame1900/chunk700参考steps，配置max2000不等实际所有训练时长。SGF诊断指南每worker约110GB需求不代表论文计时硬件。

AppG固定Pass2重放/监督/随机性，在共享点和同乘积空间位移预算下，独立更新与共享更新的最大一阶下降平方差为r²‖gC−gD‖²/2。梯度不等便可能产生共享限制，负对齐非必要。这个预算未匹配参数/算力；同lr时位移预算不同，充分小步且聚合内积负才支持该形式的split优势。样本/模块负余弦与全batch全参数梯度需分开。局部Lipschitz条件下的一步结论不证明AdamW全局收敛。

T1 frame60s SGF→SGF+主体98.26→99.08，动态71.19→55.38、imaging71.52→71.11；240s动态65.68→53.96。T4短视频frameAction96→94.4也下降。T3每step11.79→12.76s、推理24.85→27.96GB，不能与另篇SGF的每5steps计时混用。24h四定性场景缺全程semantic/运动/事件量化；不能仅凭少数示例排除低运动换稳定。

## 对本研究的可证伪设计

1. 固定VAE/teacher/初始化、总训练FLOPs与验证集CFG搜索，比较MF/iMF/Shortcut/FM多步，分离目标、辅助头、结构和训练时长；报告FID与短笔漏失、OrderAcc、RGB事件可观测性。
2. 同参数/算力比较SGF+、加宽shared、双LoRA、梯度投影，测模块及全batch角色梯度、动态/长期语义，不能只看identity稳定。
3. 动作执行比较CP1/3步与真实DDIM/轻量BC，分开encoder/网络/通信/执行时间，低方差×CTM/DSM×dropout×mesh做因子对照；测合法多模式/接触/漏笔。
4. 所有方案先审查已有直接前作，局限只提供待检验假设；尚未进行模型实验，不提出已成立的新颖性结论。
