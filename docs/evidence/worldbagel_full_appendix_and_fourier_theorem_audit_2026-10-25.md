# WorldBagel：完整附录与Fourier定理审查

第二百一十三批完成[L166](../reviews/L166.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/worldbagel_full_appendix_and_fourier_theorem_audit_2026-10-25.json)。358目录（331论文／研究、27资源），318核心/323书面含未通过项；待完成核心深审13篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2607.03461)、[主源2](https://arxiv.org/pdf/2607.03461v1)、[主源3](https://arxiv.org/html/2607.03461v1)、[主源4](https://github.com/Lifelong-Robot-Learning/LIBERO/tree/8f1084e3132a39270c3a13ebe37270a43ece2a01)、[主源5](https://github.com/google-research/language-table/tree/42b319d46ec408cfe382cdbf45e71b6cf4be2900)、[主源6](https://jialuo-li.github.io/)、[主源7](https://xavihart.github.io/)。

## 研究问题

在BAGEL两个专家内同时预测连续动作与动作条件未来观测，研究动作Fourier表征、任务序列组织和混合采样对VLAW的作用。

## 现有不足

离散动作可损细节、直接回归难表高频映射，单独policy与世界预测未共享语义；异构数据大小/监督不均。这些是机制动机，未以所有同预算因子证明统一架构本身必然优。

## 贡献

UND加33M FourierFeatureActionDecoder(FFAD)、GEN加FFAT动作条件；多视图历史/多步action与future的sequenceplans，数据n^α平滑+joint优先2:1。AppA四条理论中Th1给有效但保守Lipschitz界、Th2内部可逆结论可修正证明，Th3全域稳定与Th4线性通用逼近主张有反例，须分别评价。

## 输入、模块、输出与公式

视觉历史+自然语言→H步连续动作；视觉+文字+动作→未来多视图。文中动作开环执行，世界图用于预测展示/训练，并未给在线MPC选动作闭环协议。动作条件预测不等于规范书写笔顺或真实物理可执行保证。

## 模型结构

BAGEL UND/GEN专家共注意力空间各自QKV，冻结视觉/文tokenizer，更新两专家、FFAD/FFAT投影和生成decoder。逐动作维sin/cos(2^kπa),k0..K；动作FourierMSE+.1图FM(Eq1–3)。FFAD以actionanchor hidden→1024/2层4headTransformer→2blockresMLP，正文最后写输出Rd与目标2d(K+1)Fourier维未完全对齐，无代码无法定实现。Eq4归一phase，正文说低频锚解缠后均值，但Eq5书面右式没写分支整数项；若直按裸atan2算式，高频正确特征也不直接给原动作。FFAT将连续动作重新Fourier投影GEN条件。

## 数据分布与划分

LIBERO四suite/LanguageTable/IsaacSimFranka多任务；没有训练episode数、标准划分/分辨率/长度H/历史长度/每任务评测次数/数据α值及全部预处理manifest。正文把四suite合说10场景不可靠；官方LIBERO库8f1084e列130tasks(三受控suite+100)，其中100拆90+10，不能将整benchmark缩为10。LanguageTable官方42b319d关联InteractiveLanguage arxiv2210.06407，含real442226与多种sim数据；本文[32]却引用LearningLatentPlansfromPlay2020，无法仅凭该引文辨明所用子集。

## 指标与评价协议

VLA成功率与A-MSE；世界FVD/PSNR/SSIM/LPIPS；actionembedding冻结线性probe预测taskidentity、协方差effective rank/首特征值比。T3 SSIM/LPIPS数字82.41/16.33与T4 LPIPS.203量表不同未明示百分比，不能直接混算。更高rank/任务probe不自动推出因果动力学、迁移/稳定性。

## 对比方法

世界主要对RynnVLA002，policy对OpenVLAOFT/π0.5等；Table2 multitask标记与结果统一协议缺实际run资料。声称allcontinuous与tokenization的类别定义需限定；不把类型勾选当独立能力审计。排BagelVLA因当时代码缺失，本次官方页仍comingsoon支持当前不能直接复现对照。没有足够容量/预训/采样预算匹配的joint-vs-separated全因子。

## 实验条件和发布边界

AdamW2e-5/wd.01/cos/globalb32/80K/8H200，K32，joint:policy2:1，作者说所有结果5seed均值但无各seed/CI/原始run。K定义Eq0..K实际K+1频率与表称K bands也不完全一致；动作归一边界/float精度/phase规则、世界NFE及端到端延迟未给齐。扰动“varianceσ=.05”有方差/标准差记号歧义，scale.8–1.2/time±1；未说明是否重跑真实环境得到对应扰动后GT。若只改条件动作却比原帧，不能据该分数独立判断正确响应扰动。

## 主结果

T2 LIBERO98.0>Rynn97.4/OpenVLAOFT97.1，为作者均值，不据.6pp宣统计显著。T3actioncond LIBERO FVD373.1<389.5/PSNR23.88>21.74，LanguageTable392.2/22.61、Franka421.9/23.04，actionfree也优Rynn；数据来源于real不意味着新真机部署成功。T4probe68.7>FAST54.2/reg49.8，rank33.7>16.3、topmass.43<.67，只支持给定表征统计。高于基线与对自身扰动退化两个比较须分开。

## 消融及进一步实验

T4a reg.042MSE/96.3SR→FFAD.028/98.0，但reg只线性头、FFAD33M+Transformer+resMLP，容量混淆。K8/16/32/64 MSE.034/.031/.028/.029，SR96.8/97.3/98.0/97.6，非K单调。FFATPSNR23.21/23.82/23.88/23.87。噪声PSNR23.64/LPIPS.203优Rynn21.38/.274，scale23.57/.208、time23.41/.214；与T3LPIPS尺度无明确对齐。AppB只PlanA/C模板无定量sampling/ordering消融，PlanA仍列future预测与policyfocused只监督动作的描述不完全一致。

## 局限与疑问

全部25页2图4表30编号式AppA1–4/B全核。Th1πsqrt(2Σ4^k)是保守上界(可去多余sqrt2)，随K指数增，不能推出高K数值鲁棒。Th2在开区间由k0就能证明injective：Δa=2m且|Δa|<2→0；原证漏因子2且声称整数差唯一0逻辑错，结论本身内部成立。闭区间φ(−1)=φ(1)，不能全域无损。Th3未经margin/解缠正确条件的C仅依K全域界不成立：固定K取a=1−δ,b=−1+δ，令预测φhat(a)=φ(b)，特征差→0但锚解码到b后动作误差→2；需局部离branch且足够小噪声。Th4取A=[−1,1],f=1，每非零整数频率sin/cos积分0，所有wφ均积分0，sup|1−wφ|≥1，违任意ε。证明用含DC全部整数频率的代数，不能替换给定指数频率线性span；经典定理还需区间端点/周期函数空间条件。均为本仓库解析反例，非模型执行。

## 预期优势条件

动作归一在可靠内区间、phase分支可锁定且同样本世界/控制能共享特征时，Fourier表征可能改善细节拟合与多任务预测。实验优势可继续检验；错误的逼近/全域稳定定理不能担保端点动作或有限精度K32/64。

## 可证伪实验

同33M容量非线性rawhead与Fourierhead比较；扫K/float精度/端点/branch噪声，明确是否含DC/连续频谱与解缠规则。固定预训/预算做jointloss/sequenceordering/采样α/2:1因子，真实扰动环境重跑GT检验因果动作响应，报各seedCI/吞吐/闭环成功。数学修正Th2，Th3局部margin，Th4删改函数空间并证；书写额外测落抬笔/笔顺/接触与终态。未执行模型。

## 论文组织与Claim学习

研究问题与分组表组织清楚，但定理必须核实际频率集合、DC、端点和反函数分支。区分有效Lipschitz上界、可修证明、存在反例的结论；少量分数差与勾选表不支撑“统一本身”因果。AppB标题含study却缺study数字，数据引用/子集、模型发布和接受状态需准确。

## 实际阅读范围

arXiv唯一v1全25页§1–5/69条references清单及关键关联/AppA1–4全部定义定理证明/B全模板，F1–2全视觉9contact及p23–25理论/计划放大，T1–4全部(a–h)、Eq1–30逐式。官方arxivComments/作者Jialuo与Haotian页面发布线索核，无对应codecheckpoint入口；LIBERO/LanguageTable固定README来源定义补核。未取得WorldBagel实现/视频补充包，未运行模型/训练/benchmark；理论反例为解析分析。核心三遍与五书面完成，未声称复现。

## 四条理论分别评价

Th1保守Lipschitz上界有效但随K指数增加；Th2开区间可逆结论成立，原证明相位整周期漏2，直接用最低频即可修。Th3缺少局部分支margin：固定K取a=1−δ,b=−1+δ，预测特征恰取φ(b)，δ趋0时特征误差趋0而解码动作差趋2，故全域C仅依K不成立。Th4对A=[−1,1]和常数f=1，每个给定非零频率基函数积分0，任意线性组合一致误差至少1。以上是本仓库数学分析，无模型执行。

## 经验与理论

这些反例限制理论声称，未直接否定作者报告98.0%等实验分数。判定经验收益仍需同容量head、同预训练/compute联合训练因子、各seed和评测子集。扰动动作后是否重跑环境GT也需明确。

## 发布状态

官方arxivComments写RejectedbyECCV2026/ArxivPaper，PDF的ECCV样式不能作接收证据。代码与checkpoint仍承诺afteracceptance，作者页面未给对应下载。
