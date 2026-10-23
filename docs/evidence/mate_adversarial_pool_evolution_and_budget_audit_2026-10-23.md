# MATE：困难输入、数据池演化与预算审查

第一百五十一批完成[L138](../reviews/L138.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/mate_adversarial_pool_evolution_and_budget_audit_2026-10-23.json)。357目录（330论文／研究、27资源），260核心/263书面含未通过项；未确认核心70论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[arXiv版本](https://arxiv.org/abs/2609.36224)、[v1全文](https://arxiv.org/pdf/2609.36224v1)。

## 研究问题

在同一静态图UMM中，生成与描述分支能否互相提供有效困难输入，并让这些输入跨epoch演化，从有限初始数据改善生成和理解？文字→图像/图像→caption循环及数据选择问题，无新视频生成或汉字笔顺/动作模型。

## 现有不足

固定输入/合作奖励可能反复强化已会样本；作者希望有效性筛选后选择对方最难解的输出，后续池随模型变化。难例不必等于可学缺口：裁判误差、无效输出、随机波动和不可逆的信息压缩也会造成低分，需拆开检验。无单独训练的对手组件，但依赖外部冻结reward及SigLIP。

## 贡献

保持标准GRPO后训目标和优化器，把输入来源改为对向分支输出、在源一致候选中按solver平均reward最低选择，并将选中图/文本变成下一epoch对向输入池。创新在困难输入选择/跨模态池演化组合，不是新GRPO、从零无数据训练或GAN独立判别器。共享骨干潜在协同是待检假设。

## 输入、模块、输出与公式

Eq1–3以源图I为例：Uθ提Ncaption；RU(p,I)>τ筛选；每个入选p由Gθ采M图，r=RG(Ihat,p)+λCG(Ihat,I)，按均值最小选p*。同一M样本归一优势Am=(rm−rbar)/σ(Eq5)作clippedGRPO+referenceKL更新solver。反向从源文p生成N候选图，用RG准入，U写M描述，以RU(phat,I)+λCU(phat,p)打分和选图。Eq4将选中文本建下epoch文本池、选中图建图池，交替跨模态。Algo1每epoch列出两方向采样后先U再G更新；具体mini-batch rollout/oldpolicy刷新顺序未有源码核定。未选候选rollout仅估难度。若σ<1e−6跳过组更新，所选输入仍入下一池；这里是丢组阈值，非在Eq5分母直接加epsilon。

## 模型与外部裁判

Janus-Pro-1B自回归图文骨干，LM参数1.5B、全部可训2.1B，Tables1/2列UMM的LM数、generation-only总数，参数列口径不统一，不能据1.5B称所有训练参数。两路径共享θ、无额外可训perturber；solver更新共享θ也可间接改变challenger。冻结UnifiedReward-qwen-7b基于Qwen2.5-VL-7B-Instruct，RG图对文原量表1–5、RU文对图0–100，各rescale[0,1]，固定released pointwise prompt/greedy。SigLIP作CG/CU一致性；reward网络未参与官方benchmark裁判，但roundtrip编码同族。

## 数据和池更新

Align-Anything text-to-image split5000图文初始化两池，训练不使用原配对；作者称原texts未出现在生成benchmark prompts，未提供所选ID/图像语义与模板去重，不能扩大为全部数据无重叠保证。两个池每轮由已选输出替换，无原始语料锚定或旧checkpoint对手档案；多样性和稀有知识可能丢失。Roundtrip用Align-Anything test前32对图像，属于固定小子集。没有视频或笔画标注。未取得实际池/候选分数文件。

## 指标与评价协议

GenEval六类准确率均值、DPG-Bench整体，四图/prompt；生成均值为这两整体分未四舍五入前平均。理解VLMEvalKit九列：POPE overallF1、MME cognition(最高800后缩放100)、MMBench English dev accuracy、SEED image、MMStar、V*Bench、CV2D/CV3D、SEED2+，再等列均值；不同题量权重不等每题平均。Roundtrip k1/2/4/8图像cos(I0,Ik)，文本从k2比p1/pk(不比原始p0)；SigLIP-L16-384均值576patch再L2，长文分64token窗口平均embedding，描述greedy最多256token，误差棒为32样本标准误，不是多seed训练区间。主奖励UnifiedReward不参与这些benchmark，但SigLIP一致性分非完全独立。

## 对比

同JanusPro1B重实现UniRL/SUDER并共享optimizer/scorer/corpus/batch；其他生成模型SD3Medium/LlamaGen/Sana.6/1.6/Lumina2，其他UMM Janus/JanusFlow/Showo，理解LLaVAv1.5/DeepSeekVL1.3/LLaVAOV.5。外部生成分引用论文且无prompt重写，理解优先OpenVLM同toolkit可用分，缺项自行测，MMBenchENdev对所有模型测；不宜把异来源所有行当同预算实验。机制基线固定池、固定池+最高分合作、无准入、无一致、全部准入候选组；分网使用Qwen2VL2B+SimpleAR.5，底座与总参数亦变化。

## 实验条件和发布边界

§4.1/T4：N4/M8/τ.5/λ.1/σfloor1e−6，5epoch，effectivebatch48(24inputs/step)，all2.1B参数lr1e−6/clip.2/lowvarianceKL.01，6×NVIDIAB200约29小时。每源提4个候选、每准入候选8个solver样本，最多32rollouts，其他候选只估难度；同epoch/batch不等同完整候选/裁判/算力预算。主实验与消融各singletrainingrun，作者明确对小于1点谨慎。GenEval/DPG官方ELLA代码，384px/CFG5/temp1/4图每prompt；理解JanusProchattemplate+greedy。训练采样温度、optimizer具体betas/wd、max文本/策略更新次数、precision、裁判资源分配/全部基线时长/种子ID未齐。§10 reproducibility只承诺以后发scripts/config/eval/记录，全文出链与有限title+GitHub/HF检索未确认官方制品；不宣称全球不存在，未执行。

## 主结果

T1 Janus/UniRL/SUDER/MATE GenEval74.4/75.2/74.3/76.8，DPG82.1/82.1/82.0/83.8；MATE对base+2.4/+1.7pp。GenEval六类base→MATE single98.4→99.1、two84.1→87.9、count53.1→53.8、colors91.2→90.7(−.5)、position63.8→65.5、colorattr56→64。MATE非每类最好：single低SUDER99.4，colors低UniRL92，position低UniRL66.5。其DPG83.8低于外部SD3Medium84.1/Sana1.6B84.8/Lumina2 87.2。T2base→MATE POPE84.3→84.2、MMEC263.6→281.4、MMB74.5→74.7、SEED66.9→67、MMStar43.5→43.7、V*40.8→42.9、CV2D59.8→60.5、CV3D58.9→59.2、SEED2+50.9→51.2；avg56.9→57.6，UniRL55.7/SUDER56.3。提升8/9，但JanusFlow59.3平均更高，不能泛称所有UMM SOTA。

## 完整消融和循环一致

F6b(Uavg/Gavg)：base56.9/78.3，MATE57.6/80.3，固定池57.7/79.9，再合作最高分57.8/79.5，无准入57.3/79.3。生成两次差.4单run仅suggestive，理解无依赖这两机制的实验证据；未完整困难×演化2×2，缺演化池+合作。T5无一致57.5/80.5、全准入组57.5/80.6，后两生成反高于MATE，不能称一致和仅最难必要；全候选最多4倍更新组但总budget未齐。分网66.3/64.1，相对自身−.9/+2.1，2.8B总参数vsJanus2.1B且底座不同，未隔离共享。F6a第8轮图base/UniRL/SUDER/MATE .779/.758/.745/.824，文.686/.602/.709/.783；MATE图k1/2/4/8 .909/.885/.856/.824，文k2/4/8 .843/.814/.783，仍随循环下降。F3每prompt4图选1展示；F5/7每列图文来自两独立方向，未必匹配，不能当固定实体轨迹或逐帧视频。

## 局限和疑问

作者明示1B规模/5K数据/有限候选近似/额外开销，单seed.4差和SigLIP依赖也在主文承认。审查补充：无人过τ时fallback最高score可仍≤τ，准入不保证全部有效；最低均值可能选中负采样噪声，且同M组同时估难度和训练，需独立估计；低均分全错/零方差组会被跳过仍进入下池，难度不保证可学性或信息保存。共享参数收益和跨大模型/视频泛化未由当前分网对照隔离。F8号称main run pair4/epoch2完整轮，上半RU列均值(七个.95+一个.90)/8=.94375显示.944、四个.95四个.90=.925；未展示Eq3的λCU/CG，rbar图值和总奖励对应需原始记录核查，不能据图断言主训练去掉一致项。长期池无锚/弱judge可能收缩分布，32例同族embedding高相似不直接证明小字/计数/身份/时间顺序保存。

## 预期优势条件

当源候选大多有效、有限采样可辨可学缺口、外部reward精确且共享更新不损另一任务时，hard mining与动态池可提高固定数据下学习信号，尤其生成属性组合。当前限定规模单run显示生成+2.4/1.7和理解+.7，机制消融主要给生成小幅提示，理解应归于完整后训结果而不单独归因hard/池。往书写UMM迁移时要让候选严格事件/笔画/终图一致，embedding同意不能替代规范笔顺oracle。

## 可证伪实验

等所有采样/裁判/训练token及硬件时预算，对随机/最难/最高分/中等难度/全候选，和固定/演化池做完整析因；把估难M与训练M分开，增N/M并报独立difficulty排名稳定、fallback率、零方差率与丢组后池漂移。多seed、按prompt配对bootstrap，预注册最小实用差；同初始化的共享/分离/只更新一任务对照，控制总参数和冻结encoder。保留真实样本锚、稀有类别配额/回放，对judge换代/人标/独立OCR及细部属性、计数、身份测信息消失，文本同时比p0和p1。书写任务加同终图不同顺序负例/严格事件轨迹与真实执行，报告成本收益曲线。核F8分项/总reward及源码版本，未执行。

## 论文组织与Claim学习

Introduction从固定合作自训→互相出困难题→对手如何持续演化，Method按目标/单轮/池更新组织，AppA表按对方提供什么/优化任务/输入来源/困难/新增模块分维比创新，易于审查。可以学习主动标明参数口径、雷达图截轴不比面积、定性单例选取与single-run小差、分网混杂。写Claim要让实验能反驳假设：无一致/全候选稍高、理解消融不依赖hard/演化均应保留；“inverse”在caption压缩意义不构成数学双射，“valid”受fallback及judge约束。

## 实际阅读范围

v1完整20页17894933bytes，Abstract/§1–5全部正文、AIUse/Reproducibility、AppA/B/C全部研究内容，Eq1–5/T1–5/Algorithms1–3/F1–8及图注；实际查看p3/4/5/7/8/9/16/17/18/19/20共11页，覆盖所有图/表/算法。p10–15参考定位含SUDER/UniGame/SRUM/EVA等追引，未逐篇精读引用；abs版本、HTML及有限title+GitHub/HF检索，不曾取得作者待发布scripts/config/records/模型权重，未运行或独立复现。

## 三句话概括

固定数据自训可能重复已有能力，MATE尝试用另一个分支输出中的困难候选扩展训练输入。它先按源一致筛候选，再以solver平均奖励选最难，并跨epoch重建图文池，以GRPO更新。JanusPro上生成和理解平均改善；困难与演化机制对理解没有独立增益证据，生成消融的.4点差来自单run。

## 五个关键问题

1. 有限初始语料下如何选择并持续生成有学习价值的输入。
2. 固定合作方案可能重复易例；困难也可能来自噪声或无效样本，现有筛选不能保证完全排除。
3. 两方向困难输入选择和跨模态池演化是具体改动，GRPO本身沿用已有工作。
4. 候选有效、难度估计可靠、缺点可学且共享更新有益时预期受益；小模型生成组合属性是本文有限实证范围。
5. 需补困难×演化完整析因、所有采样/更新预算匹配、独立估难、多seed及真正信息保存oracle。

## 主张与证据逐项对照

| 主张 | 已有支持 | 当前限制 |
| --- | --- | --- |
| 整体后训有效 | GenEval74.4→76.8，DPG82.1→83.8，理解56.9→57.6 | 单run，颜色和POPE回退 |
| 困难与演化有益 | 固定池79.9、合作固定池79.5，对比完整80.3生成均值 | 每差.4；理解57.7/57.8略高，缺完整2×2 |
| 一致项必要 | 当前无一致57.5/80.5 | 生成反高于完整80.3，未证必要 |
| 只训最难有效率 | 全准入57.5/80.6 | 生成略高、更新组数不同，需完整成本收益 |
| 共享参数有益 | 分网相对自身理解−.9、生成+2.1 | 底座和总参数不同，未隔离共享 |
| 循环保存信息 | 32例SigLIP k8图.824、文.783 | 同族训练特征、从p1而非p0比文本，细节可能丢失 |

## 图示与算法边界

Fig8上半rbar .944和.925等于展示的RU简单均值，图未显示一致性分项；Eq3及Algo2/3使用R+λC。需作者记录确认总奖励如何对应图值，不能由此断言正式训练忽略C。Fig5/7同列图文来自两条独立方向，不能按逐帧视频或严格配对图文解释。

准入无人通过时仍保留最高分候选，可能低于阈值；σ过低只跳过训练，所选候选仍更新下一池。完整方法需要同时追踪fallback、零方差、信息丢失和稀有类保留。

## 追引与覆盖队列

SUDER(arXiv2506.07963，非本条MATE)、SRUM(2510.12784)、UniGame(CVPR2026 pp37632–37641)、SILMM、UnifiedReward、Align-Anything(2412.15838)、EVA(2411.00062)、online hard example mining(CVPR2016)、prioritized level replay(ICML2021)、replay-guided environment design(NeurIPS2021)、DAPO及零方差组处理。标题检索没有命中SUDER/UniGame/SRUM/SILMM/UnifiedReward；仍需DOI/作者/别名去重及主源完整阅读，未计精读完成。
