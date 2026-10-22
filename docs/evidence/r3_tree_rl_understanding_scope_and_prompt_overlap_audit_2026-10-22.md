# R3：Tree-RL、理解提升范围与发布数据重合审查

第一百四十三批完成[L132](../reviews/L132.md)明确范围核心三遍与五项书面记录。[结构化证据及370条重合提示](../../data/r3_tree_rl_understanding_scope_and_prompt_overlap_audit_2026-10-22.json)。357目录（330论文／研究、27资源），252核心/255书面含未通过项；未确认核心78论文／研究+27资源，资源另审。无目录新增、文件删除、权重下载或模型执行。

来源：[正式ICLR2026条目](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2aadf45de754077d823b3d5d275bebf2-Abstract-Conference.html)、[正式24页PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/2aadf45de754077d823b3d5d275bebf2-Paper-Conference.pdf)、[arxiv v2](https://arxiv.org/html/2602.15772v2)、[固定源码](https://github.com/sen-ye/R3/tree/761b0b0713352a52128cbd39a004dc383bd082bd)。正式核心与附录、全部9表/Eq1–3及附录公式、12个实际PDF页已核。

## 问题和动机

统一模型单独后训练生成或理解时，另一任务可能退步；把理解作为生成中的反思与编辑条件，能否在同一BAGEL上改善静态组合图像生成及与生成内容相关的理解。任务是文本→计划+初图→多轮图像问答式自评/编辑指令+修图，不是连续书写视频、笔顺预测或普适理解基准。

F1计数子集：初始Gen47.5/Und80.4，单Gen57.5/79.8，单Und32.5/82.4，朴素混合50/80.7，R3 80/85.9，说明该配置存在取舍并支持研究任务耦合；未测梯度夹角/容量饱和、优化多seed或普遍不可兼得定理，不能由性能变化唯一识别根因是参数竞争。F1数值不同于T1/T3的计数行，不能混为同一配置。作者假设反思理解对生成有功能用途能改善协同。

R3分Reason(文字CoT计划+初图)、Reflect(图+原目标→错误分析/一句编辑指令或停止)、Refine(图+编辑指令→新图)，迭代自停。Tree-RL将完整链拆阶段，上一阶段图/分数缓冲，按完美/不完美状态重采后各阶段单独分组rollout与优化。文字GRPO、连续图MixGRPO(部分SDE其余ODE)，主训练Reason+1RR、默认推理Reason+最多4RR。无新tokenizer或新的基础MoT骨干。

## 数据流与模型结构

c→AR文字t1→flow初图I1；(c,Ii)→AR反思ti+1与编辑ei+1，若停止保留原图，否则(Ii,ei+1)→flow新图。Eq1为交错序列分布，Reason联合概率可按链式法则分解；Markov假设仅保留当前图/指令/目标，不能当有任意长历史保证。训练外部Qwen或GenEval检测器判分，反思文本不直接监督VQA正确答案，通过后续图奖励与格式奖励学。Maze扩展先随机轨迹SFT学图像状态转移再RL生成行动/图状态，只有定性12×10迷宫示例，无成功率表。

沿用BAGEL-7B-MoT：文字AR语言路径，SigLIP语义图输入经投影供理解，FLUX-VAE连续latent及t条件供flow生成/编辑，理解和生成专家通过统一attention交互；该7B名称不能自动作为全MoT总参数。公开构建从llm/vit配置载入、指定Qwen2MoTDecoderLayer；当前启动freeze_vit=True/freeze_vae=True/freeze_llm=False/freeze_und=False，语言/理解侧并非全冻结，VAE/ViT冻结；未给新的网络层/额外学习式反思模型。

## 数据和实验协议

论文GenEval与GenEval++随机重组官方模板并声称排除测试prompt；TIIF用官方train、测short testmini。正式理解集固定使用基线BAGEL根据GenEval++测试prompt生成图，结构metadata生成yes/no题，Gemini2.5Flash给VQA/ITA标签并人工一致性检查，未报告该检查抽样量/标注误差/完整理解集制品。固定发布七JSONL全部解析：train GenEval12359、GenEval++18134、TIIF2261(2260不同short)；test GenEval2212(553prompt各重复4次)、test_geneval_553为553、GenEval++280、TIIF277。GenEval发布训练与两测试文件均有370不同prompt完全重合，按553测试tag为single80/two99/count80/colors92/position18/color_attr1；与正文严格排除测试提示声明不一致。该May6公开版本不自动证明正式训练使用相同样本，缺原实验清单/日志；GenEval++及TIIF对应发布文件字面交集均0，同模板仍不等于组合OOD。

生成GenEval检测器组合正确率、GenEval++ GPT4.1评估全约束正确率、TIIFshort testmini Qwen2.5VL72B逐题率/分组均分；文字渲染仅TIIF text和例图，没有CER/字符序/笔画时序指标。理解VQA为与Gemini标签yes/no一致率，ITA为整图对提示的判断一致率，都是固定BAGEL生成图上的任务分布，不等一般MME/MMMU理解或真值无误人评。F4训练reward不是生成测试分，F7左为Qwen reward、右为VQA；T4GenEval++为validation reward，不能和T1 GPT4.1测试分直接比较。推理报告最大轮数、自停轮数分布与单H20时延，无端到端训练/评测总GPUh。

T1 GPT4o/FLUXKontext/FLUXdev/JanusPro/T2IR1/Echo4o/BAGEL与只Reason；T6另FLUXPro/BAGELselfCoT；T8QwenImageRL/FlowGRPO。模型大小/预训/监督数据/教师/推理轮数与算量未全匹配。核心对照有同R3推理下未RL BAGEL、Reason-only、1/2RR训练、不同最大轮推理、Tree与fulltrajectory训练reward、单类别→其他类别理解。缺同总NFE/延迟Best-of-N、固定外部反思编辑器、反思打乱/空图/冻结理解模块及参数容量对照，不能只因缺对照否定已观测收益。

正式T7 lr5e-6/batch16/group16；GenEval/GenEval++/TIIF分别400/300/200steps，CE:MSE权重1:2，文字temperature.9、CFGtext4/image1.5、KLtext.0005/image.005，初图10/15/15更新、编辑20。Reason SDE a.7、edit1，256候选取16且约20%完美；主训练一Reason+一RR。推理H20单卡/b1/512²，初图20–25s、每RR25–35s(反思5–10/修图20–25)，45%零RR/26%一/14%二/15%三以上，零RR仍需判停反思的具体计时需说明。当前公开启动默认8进程/PG4=2promptgroups×16=32候选，不是正文16×16；1000steps/KLtext=image.001/warm10/AdamW.9,.95 eps1e-8/wd0/clip1，未等同正式配置。脚本num_timesteps16/21为网格点，实际减一得到15/20更新，与GenEval++正文一致，不能误标步数冲突。

## 主表、消融和图证据

正式T1 GenEval++ BAGEL.371→Reason.593→R3.689，相对Reason+9.6pp、相对BAGEL+31.8pp；高于Echo4o.679但低于GPT4o.739。R3 color/count.575及pos/size.575低于Reason两项.600；非全部子项改善。T2ITA60.60→61.76→73.37(+12.77pp)，T3VQA86.48→86.72→89.63(+3.15pp)，全R3对基座七子项均提高；只Reason的count79.30→76.12下降。T6TIIF70.97→82.02、text40.72→72.40，但整体低于GPT4o84.19、text低于92.76，attribute+relation76.96低于selfCoT77.65。T8另GenEval模型总体表.96、F6/正文.962，position.98低于FlowGRPO.99。三个不同数据/步数的训练配置不能拼成单checkpoint全面成绩；TIIF重新训练不能直接证明GenEval++训练模型的跨数据零样本泛化。

正式T4训练Reason/1RR/2RR：GenEval++ validation reward .654/.729/.732，ITA62.83/74.49/74.76，后一RR边际小，未等训练FLOPs。T5单类计数/颜色/位置大小的对角ITA提高，位置训练计数62.71→60、颜色60.63→60，颜色训练计数62.71→62.50，跨类不普遍保持。T9同推理BAGELvsR3：Reason.399/.593，1RR.432/.675，2RR.436/.689，3RR.439/.682，4RR.439/.689；有对未RL多轮基座控制，收益不能全部归为额外轮数。实际F6 GenEval.944/.956/.955/.956/.962，GenEval++.593/.675/.689/.682/.689，TIIF75.9/81.2/81.9/82.6/82.0，均非单调。F7 VQA约75–100step已明显上升，不支持正文前150步几乎不变、150后才启动的严格时间描述；关联曲线不能证明理解提升因果推动生成。F4Tree reward更高，有未说明统计定义的阴影，未给梯度方差实测或等walltime曲线。

## 局限与优势条件

正文无独立Limitations节，但§3.2承认理解收益依训练领域，AppA5成本与实际F11拼写错误后误停是明确限制。未核到多训练seed/CI、一般理解保持矩阵、完整ITA/VQA标注及正式checkpoint/训练清单。公开GenEval370测试prompt重合与论文不一致，需要解决版本归因；不能以当前文件直接判正式结果无效。缓冲按奖励重采是状态课程，未给对完整轨迹原分布的状态importance权重；可优化条件课程目标，不应无依据称RL无效。公开优势无std、格式门控、15%完美、默认globalbatch/steps/KL与论文差异；图像log概率按维度平均、KL是等方差真KL的2倍均值尺度。文字保存raw概率、训练也读raw，但实际采样temperature.9/top-p.9，基础policy目标与探索分布需说明。静态多轮编辑/迷宫状态序列不保证持续视频一致/笔顺正确。

推断：基座已会定位错误并能条件编辑、外部reward能可靠区分局部修正、提示包含计数/颜色/空间等可验证约束且允许额外推理预算时，分阶段组内相对奖励有望降低长链信用分配难度、提高对应内容判断。训练1RR而推理多轮可复用编辑策略；这不构成所有任务理解与生成梯度必同向的理论保证。若裁判错、图不可编辑、错误在细笔画/字符顺序/执行物理约束上不可见，可能早停或反复修错。领域外理解、文本长串/多语种、长视频需新证据。

## 实验假设和写作学习

先固定正式train/testID和checkpoint，去除已核370提示及近模板泄漏，分别报告熟悉模板/新实体组合/跨类别/跨图像域，多训练seed与人评。同基座同数据/更新/总生成NFE/裁判调用/总GPUh比较Reason、Fulltrajectory、Tree、BestN与独立外部反思器；RL有无×反思有无×结构化格式有无×语义反思打乱/无图/冻结理解分支。验证状态采样完美比0/.15/.2/自然分布与按原状态分布加权；组内中心化/标准化及KL尺度、格式加和/门控分开消融。固定同批真实与合成图问答、均衡yes/no、防语言先验，测独立标注一致率及MME/MMMU等保持。绘制真实gradient余弦/方差/训练时间和每实例改好/改坏、停止精确率/召回率/校准、成本质量Pareto。书写另测有序OCR、笔画事件与RGB可观察性；均未执行。

Intro从单任务取舍实验引出任务重组，Method按Reason/Reflect/Refine、Tree训练与阶段reward组织，T4/5/9分别问长度、域迁移和训练贡献，AppA5报告成本、F11保留失败，结构可学习。Rootcause/ensures/preventing等强词应降为指定配置支持的假设；没有梯度/容量/干预证据时，不能由F1或F7关联判因果。说明ITA/VQA构建与裁判标签边界，承认跨类退步、非单调轮数和单独训练配置；论文分数/validationreward/正式发布data要分别可追溯。发布训练提示重合是需解决的可复核问题，不能被仅排exacttest的文字声明覆盖。

## 实际阅读边界

正式ICLR24页完整PDF、Abstract/§1–5、全部T1–9/Eq1–3、AppA1/A2.1–2所有GRPO/flow/SDE/MixGRPO公式与A3.1–3/A4/A5/A7全文，A6全部图注及选择性图；arxivv2完整HTML研究文字交叉。实际PDFp2/3/4/5/6/7/8/9/16/17/20/24共12页核看，覆盖F1–7、全部9表、F10/11及mazeF16；其他定性图未逐图核、参考文献未逐篇独立精读。固定GH761b0b0713352a52128cbd39a004dc383bd082bd完整72项树/README/tutorial全文、启动全文、train/data_utils及reward_func全部任务提示和分数、sde_sampler全文；online_rl缓冲/采样/奖励/优势/文本与图概率/KL/冻结/数据/评估选段、train_utils优势实现、rollout格式/终止/图CFG/pack与BAGEL MixSDE/文字采样选段；七JSONL全文解析计数与字面prompt交叉、metadata样例，未逐条语义审注。未独立读全模型/训练源码、部署外部rewardserver、下载权重、执行训练/推理或复现；未核正式实验实际训练清单。

## 主张与证据对应

| 研究主张／细节 | 实际证据与可支持范围 |
| --- | --- |
| 理解和生成冲突来自容量竞争 | F1是计数域五种后训练配置的性能取舍；没有直接梯度、容量或控制其他变量的根因检验 |
| 理解整体增强 | 固定BAGEL生成图+Gemini标签的ITA/VQA提高；T5跨类别下降，未给MME/MMMU等保持矩阵 |
| 反思解决全部生成约束 | T1 .371→.689，但比GPT4o .739低；相对Reason-only两个子项下降 |
| 泛化到TIIF | TIIF用其train单独200步训练，支持方法能适配另一任务；没有证明GenEval++权重零样本跨域 |
| 多轮收益仅由额外推理引起 | T9同R3推理下未RL BAGEL最高.439、RL模型.689，有重要同轮数对照；仍需等总NFE/时延其他强策略 |
| 多轮持续提升 | F6/T9非单调，TIIF三轮82.6→四轮82.0；GenEval++二轮.689→三轮.682→四轮.689 |
| 150步后理解才增强 | F7右图约75–100步已有明确上升，不能按文字叙事给出严格150步因果转折 |
| 正式排除GenEval测试prompt | 当前发布train与553官方test有370字面重合；无法据此替代正式实验使用版本的证据 |
| GenEval++/TIIF无重合 | 对当前文件确认为0字面交集，仍需模板/语义组合与预训污染边界 |
| 标准GRPO设置 | 代码优势只减组均值，无std；有行为概率/clip，和PairUni无oldpolicyclip的实现不同 |
| 反射奖励仅加格式 | 代码对质量/改进乘格式门控；格式错误时正文加和与代码行为不同 |
| 图编辑奖励写Vnew未减Vold即错误 | 同组固定Vold在减组均值后消掉，非停止分支可等效；应单独审停止与格式门控 |
| 16/21与15/20步矛盾 | 源码16/21是时间网格点，去末端形成15/20次更新，不能误判 |
| 迷宫证明长期视觉规划/视频 | 附录随机轨迹SFT+RL和一个12×10迷宫定性序列，未有成功率或连续视频评价 |

## 可复核的提示重合

在固定761b0b07版本读取七个完整JSONL，以训练加载器实际使用的prompt或short_description字段取字符串并strip，比较集合。该过程检查发布数据声明，未执行模型或测试代码。

| 发布文件 | 行数 | 不同提示 | 与相应发布测试的不同提示交集 |
| --- | ---: | ---: | ---: |
| train_geneval.jsonl | 12359 | 12359 | 370/553 |
| train_geneval++.jsonl | 18134 | 18134 | 0/280 |
| train_TIIF.jsonl | 2261 | 2260 | 0/277 |
| test_geneval.jsonl | 2212 | 553，每提示4行 | — |
| test_geneval_553.jsonl | 553 | 553 | — |
| test_geneval++.jsonl | 280 | 280 | — |
| test_TIIF.jsonl | 277 | 277 | — |

370条按553测试类别分为single_object80、two_object99、counting80、colors92、position18、color_attr1；例如a photo of a backpack、a photo of a baseball bat and a bear。完整提示列表和源文件路径已写入结构化证据，便于逐项复核。当前发布制品与正式声称严格排除测试提示不一致，需要正式训练manifest/日志解释。没有证据确认正式报告训练直接使用该May6文件，不能把未知版本差异升级为已证明的正式实验污染。

## 公式及实现的等效与差异

Eq2对缺陷图给Vnew−Vold、完美图给正确停止指示，Eq3文字反思加格式奖励、图像refine用改进量。公开代码文字reward实际为format×quality或format×improvement再加格式；该门控改变不合格式样本的学习信号。图像reward列表存Vnew，之后按同初始图的一组候选减均值：因Vold在组内固定，(Vnew−Vold)−mean(Vnew−Vold)=Vnew−mean(Vnew)，所以不能仅看没减Vold就认定编辑目标实现错误；停止mask及完美图分支另有不同处理。

附录按reward减均值除std，当前实现first_divide_std=False。缓冲完美率默认.15、正文约.2；它是对状态分布的课程采样。新编辑候选仍由当前条件策略采出，但该过程不等价于未改状态分布的完整链无偏梯度。需要说明训练所优化的目标，无须因无状态IS权重直接判条件RL失效。

代码保存文字raw policy概率、训练也计算raw logp；实际rollout有temperature和top-p探索，需解释基础策略目标与采样分布关系。图像采样与loss包含CFG重算并用行为oldlogp进行clip；Gaussian logp按维度平均后取exp差，得到几何平均概率比而非高维联合概率比。等方差kl_divergence实现mean((mu−mu_ref)^2/sigma²)，相对常见每维真KL差1/2因子，系数标注与推导应保持尺度一致。不能把上述有oldpolicy/clip的代码误写成PairUni式无clip。

## 对书写视频选题和实验的影响

R3已有多轮文字规划、视觉反思、静态图修正以及迷宫状态生成的先例，选题不能只把这些模块重新命名。严格书写研究需要可观察的笔画事件、时间顺序和可执行轨迹，并区分最终图正确与过程正确。其停错例图F11在CLUB拼写错误时结束，提示需要独立文字/事件检查与停止校准；这是一处有依据的限制，不代表全部反思均无效。

进一步追引GenEval++/Echo4o、MixGRPO、FlowGRPO及多任务梯度/可解释反思/自停校准；独立精读前不把队列计为完成。下一项继续L133。
