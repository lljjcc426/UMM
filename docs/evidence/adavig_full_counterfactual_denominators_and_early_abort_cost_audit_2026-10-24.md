# AdaViG：完整反事实分母、早期中止与成本记账审查

第一百八十六批完成[U21](../reviews/U21.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/adavig_full_counterfactual_denominators_and_early_abort_cost_audit_2026-10-24.json)。358目录（331论文／研究、27资源），291核心/296书面含未通过项；待完成核心深审40篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2607.10004v1)、[主源2](https://arxiv.org/html/2607.10004v1)、[主源3](https://arxiv.org/pdf/2607.10004v1)、[主源4](https://api.github.com/search/repositories?q=AdaViG)。

## 研究问题

BAGEL式交错数学推理触发图像后，能否在扩散早期根据内部信号中止可能有害的图，提升最终答案并节约推理成本？门控控制是否继续一次已触发生成，不重新训练生成器，也不生成书写轨迹。

## 现有不足

原方法按nextactiontoken启动图像，没有显式估计图对答案的效用；错误/冗余图可能吸引后续推理并浪费计算。作者用有图与全程纯文字分支诊断utilitygap，再设计早期attention统计。图多不必更准确，但可用性和因果解释需区别检验。

## 贡献

冻结模型的双attention统计与AND中止规则，t*=5/50步做早期决策；在两个同BAGEL骨干CoT变体、五数学benchmark报告准确率/实测延迟提升，另有单信号/OR、随机中止、文本only、DAPICoT、步数/tokenbudget/阈值对照。无新训练目标/tokenizer/视频架构，attention作为SFT筛选或RL奖励仅未来建议，本文未做训练验证。

## 输入、模块、输出与公式

输入数学题q和图Iin→共享MoT文字/图交错推理→最后文字答案。Eq1–2链与img_start路由；Eq3对所有VAEquery平均、对指定key段求和的head平均softmaxmass m。Eq4 I=m(text)/(m(text)+m(inputViT+inputVAE))，度量两个来源相对占比；Eq5 F=m(inputViT)绝对mass；Eq6仅I<τI且F<τF中止。算法1：非图正常decode；图先执行5step，双弱丢partialVAE并resettextnode，否则完成余45步并append图。Eq7估计ΔFLOPs=r(1−t*/T)=.9r，r定义为abort比例。

## 模型结构

BAGEL7B MoT理解/生成expert共享attention，文字causal、图像bidirectional；BAGELZebraCoT与MathCanvas的BAGELCanvas两种后训练检查点。每图既有ViT也有VAE表示，取正在去噪的VAEquery对之前text/原图key的注意力。只明确headaverage，未明确哪层/跨层聚合、CFG分支、prompt段/已有生成图token归属和实际attentionkernel；segmentmass未按key数归一化，受文字长度/图token数/softmax竞争影响。I高不能直接证明存在正确plan、F高不能保证几何faithful，必须独立校准。

## 数据分布与划分

诊断与阈值调参MathVisiontestmini304题，不是全程零数据选择；16独立采样trace/题分析标签变化。主测试五集DynaMath、WeMath、MathVersetestmini、MathVistatestmini的GPS类、OlympiadBenchMath子集，未充分给每集实际题清单/语言与过滤数；MathVision未列入主表五集，因此不能据调参直接称主表测试泄漏。未新增训练数据或更新模型。

## 指标与评价协议

主指标最终答案准确率%、五任务Avg；imagegenerationFLOPs为扩散步数近似，非系统总FLOPs；单H200每题端到端实测秒，另图像数和KVcache。F4helpful=有图对/文字错、harmful=有图错/文字对、neutral正文仅定义两者都对；F3实际图例另列Bothwrong，但F4三类pie合计100%未交代bothwrong如何计或分母，不能把26.3%直接当全体单次生成有害率。全链有图vs所有节点强制文字的counterfactual同时改变多个决策和后续随机轨迹，未隔离单个视觉步骤的平均因果效应。

## 对比方法

一般MLLM GPT4o/Gemini2.5Pro/Qwen2.5VL7B/InternVL3-8B与UMMEmu3/JanusPro/MUSE/BAGEL为外部能力参考；受控方法比较同ZebraCoT/Canvas加gate、Ionly/Fonly/OR、random25/50%、textonly100%、适配DAPICoT。原BAGELCoT与ICoT不等于Zebra/Canvas只关闭门控；跨不同后训练权重不能将到Canvas的分数差归给专门数学训练单因子。random未匹配AdaViG43/57%中止率，需同预算随机和learnedqueryonly/长度等简单信号基线。

## 实验条件和发布边界

无参数更新，H200141GB；t*=5，总T50。Zebra阈值(.5,.04)、Canvas(.6,.01)，MathVision304选。单H200报告walltime，但maxcontext/采样温度/topP/seed/重复次数、主表答题parser/judge版本、实际checkpointrevision与cache/attention实现未齐。F10约.8–4.5Ktokenbudget；F9比较t*=1/3/5/7/9，5步折中、7/9准确率更高但成本更高。正文/附录和arXiv未给官方code/project链接；GitHubAPI AdaViG检索13repo均无此论文相关项，HFpaperAPI404，有限范围内未定位官方独立实现/权重/原始逐题日志，不笼统断言不存在。未执行推理/速度测试。

## 主结果

T1按Dyna/We/MathVerse/MathVistaGPS/Olympiad顺序，Zebra39/34.5/48.2/81/16.7→43.5/38.1/51.3/83.4/18.9，Avg43.9→47，图FLOPs称−45/91/75/34/40%、Avg57%；Canvas42.3/35.3/55.8/77.9/24→48/38.8/58.4/81.3/26.2，Avg47.1→50.5，称−75/27/25/26/37%、Avg32%。5.7是Dyna准确率百分点，非相对5.7%。T2Zebra37.4/41.6/53.2/52.7/24.9s→25.7/22.6/31.7/39.8/17.6s，−24.5%至45.6%；Canvas13.2/13.1/11.5/10.4/5.72→9.4/10.8/9.7/8.8/3.96，−15.4%至30.8%。系统延迟改善有单独报告，不把图FLOPs节省直接当整机加速。

## 消融及进一步实验

T3CanvasIonly/Fonly/OR/ANDdrop55/31/61/43%，三测试AND81.3/38.8/48均最高，OR75.1/32.7/41.2均低base。T4random25%78.2/34.6/44.1，50%77.4/35.6/42.9，text76.9/34.1/42.7，DAP78.4/35.4/44.3；正文泛称random和text都低base不逐项成立，Dyna随机/text均高42.3。T5ZebraI/F/OR/ANDdrop64/61/76/57%，AND83.4/38.1/43.5最佳；T6random25%78.2/34.3/38.9、50%80.4/34.3/37.7、text77.1/32.5/37.5、DAP81/34.5/39.3。T7固定F.02扫I.5/.6/.7，Canvas80.6/81.2/81、Zebra83.2/82.3/82.1；T8固定I.6扫F.01/.02/.04，Canvas81.1/80.7/80.3、Zebra82.4/82.7/83.1。相同(.6,.02)两表80.7vs81.2、82.7vs82.3，可能采样差异但未给seed/CI解释。F4Canvashelpful28.2/harmful26.3/neutral45.5，Zebra29.6/32.3/38.1；16trace90.1%题出现≥2类，40.5%有helpful与harmful。F10实画WeMath/MathVista；正文不同tokenbudget提Dyna不能代替图中MathVista。

## 局限与疑问

FLOPs记账需澄清：Eq7固定候选数且r≤1时最多省90%，T1ZebraWeMath91%无法由该式直接给出；F8完整生成图数降幅和T1数值一致，可能混计完整图数或门控改变未来触发，需每链attempt/abort/complete及已执行步数核。若完成图C/触发A/base图B，等每步成本近似savings=1−[50C+5(A−C)]/(50B)，仅完整图减少比例会漏5步。Canvas五逐集比例算术均值38%，表Avg32%可能加权但权重未给，准确率Avg和成本Avg分母需分开。F4三类标签与F3Bothwrong处理未齐，tracelevel不等每图因果效用；输入级方法能否预测风险未被90.1%随机trace异质性排除。Attentionmass可预测不等因果中介，F11全样本平均生成图注意力更高，也可能recency/段长度效应，缺helpful/harmful分层和attention干预。F12两图色标不同（约1e−3与1e−4），不能只比颜色。两个模型同BAGEL族、只有数学任务，阈值跨架构/书写迁移未证；会丢必要但低attention图，也不修复保留图的质量。F13与F15同一题同I/F非三独立成功例。

## 预期优势条件

有可访问attention的原生交错生成器，生成触发频繁且存在可预测错误图时，简单earlyabort有望兼顾最终答案与实际延迟；低频触发收益受限。书写/素描可借鉴在落笔前决定是否执行或继续一段可撤销latent，但已落纸/已提交帧不能靠丢latent撤销；还需保留prefix、笔序与最小必要结构，不以attention总量替代小笔画正确性。

## 可证伪实验

Q1双attention是否识别单步视觉效用：对每次触发保存同prefix/seed，比较keep/abort并继续同策略，完整记录四种最终正确组合与多次续写分布；把queryonly、length/recency、entropy、自图attention和等drop随机作为对照，报风险预测AUC/PR、校准、误删必要图与分任务CI。扰动key段长度/图resolution、层/head/path屏蔽验证语义plan/faithfulness解释；若简单长度信号相当则收缩机制主张。Q2精度与成本能否共同复现：锁定模型/采样/attentionkernel，记录attempt/abort/complete/T/NFE/token/cache逐链日志，含被丢5步和callback开销，按题报完整FLOPs与H200walltime，明确macro/weighted分母；分开固定候选和链后续触发改变。校准集独立冻结阈值，跨模型/领域/文字长度复核，随机与gate按同NFE/延迟预算，多seedpairedCI；书写另测不可逆执行与必要细笔漏删。均建议，未运行模型。

## 论文组织与Claim学习

先给有害图的反事实例和链随机性诊断，再以两种故障动机导出两个易计算统计，规则/算法简洁、主表同时给准确率与真实walltime，值得借鉴。诊断标签应完整四象限并说明分母，attention名称不自动构成语义机制；random有正增益的单项不能被概括忽略。图数、估计FLOPs、端到端延迟需独立命名和记账，阈值表重叠点差异应有采样说明；RL奖励和减少数学训练依赖仍属展望。

## 实际阅读范围

完整v1 17页正文§1–7、AppA.1–A.8，T1–8所有行、F1–15全部视觉（15assets，F7/8与F9/10各合并排版）、Eq1–7及算法1；PDF核四象限legend、主表/阈值重叠、FLOPs公式与case重复。论文及arXiv未提供官方repo，GitHub有限检索无相关独立实现、HFpaperAPI404；未独立检查BAGEL原repo为AdaViG实现。核心三遍/五项书面完成，未运行模型或独立复现。

## 诊断与实现边界

F3明确画Bothwrong，正文F4仅定义helpful/harmful/两者都正确neutral，pie三类又合计100%。因此本批记录为标签归一协议未充分说明，并未认定作者完全没有bothwrong样本。

Eq7与主表91%的不一致针对论文给出的固定候选数近似。门控若改变后续生成触发，整链总成本可以产生不同降幅；需要原始日志解释，不能据此否定已单独报告的H200延迟改善。Canvas主表Avg32%与逐集算术平均38%也保留可能加权的解释。

追引MathCanvas、ZebraCoT、BAGEL、DAPICoT、UniMRG及视觉思维/书写执行研究；无模型训练或APIjudge执行，未将注意力推荐为已验证RLreward。
