# UniCorn：自身监督、联合目标与 UniCycle 公开协议审查

第一百四十二批完成[L131](../reviews/L131.md)明确范围核心三遍与五项书面记录。[结构化证据](../../data/unicorn_selfplay_joint_objective_and_unicycle_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），251核心/254书面含未通过项；未确认核心79论文／研究+27资源，资源另审。无目录新增、文件删除或模型执行。

来源：[ACL2026正式论文](https://aclanthology.org/2026.acl-long.621/)、[正式PDF](https://aclanthology.org/2026.acl-long.621.pdf)、[旧arxiv v2](https://arxiv.org/html/2601.03193v2)、[固定训练代码](https://github.com/Hungryyan1/UniCorn/tree/e3b4518d278748773a0587a40fcbcf84858dcbd1)、[固定基准](https://github.com/shierlouz/Unicycle/tree/aa1cf81f791e9053e3623eabff0cbe989c614fbf)、[固定权重制品元数据](https://huggingface.co/CostaliyA/UniCorn/tree/5e8d1df79b8a99039a78ad6efaea1e93f7d119a5)。正式32页完整取得，全部17表/Eq1–9及指定附录已读，实际核看13个PDF页和6张旧版原始图。正式新增Eq7–8并修正Janus增益，不能沿用旧版问题作为当前未修事实。

## 问题与设计动机

强理解/评价能力能否转化为同一UMM更好静态图像生成，作者称该差距Conduction Aphasia，提出离线自身多角色采样与数据重构，并用UniCycle测文字→图像→答案的指令信息保留。框架主要提升生成、保留理解，不等于已经验证理解和生成共同显著增强；没有连续书写视频或笔画事件任务。

图像生成模型可能知道答案或识别错误却不能生成正确对象/关系，单向生成后训练可能遗忘理解。把同一预训UMM分别作为Proposer/Solver/Judge，以内部语言/视觉知识挑高分生成结果，再从原交互构造caption/评价/反射监督，降低额外大型裁判依赖。F3与GPT4o归一理解/奖励benchmark相近是动机证据，缺少逐实例知道却生成失败的定量条件统计，不能推断已证明强worldmodel或AGI理论。

阶段1：十类人工设计规则、few-shot/动态seed提示生成，5000prompt每个8候选图，改变随机种子/CFG；同UMM按任务rubric输出0–10分析+分数，最高<7组过滤后Best-of-N选优。阶段2 CPR重构G=caption→高分图、C=高分图→原prompt、J=图+prompt→原评价CoT/score、R=低分图+prompt/编辑指令→同prompt高分图，5K/5K/3K/1K混合监督微调。使用文字CE和连续图像flow速度MSE，无在线GRPO/PPO或可微judge；三个角色是同模型不同提示，不是三个新结构。UniCycle新增循环评价基准与Soft/Hard。

## 数据流与模型结构

训练合成：Proposer文本上下文→新T，Solver T→8张I，Judge(T,I)→J分析/分数→选I*和Iloser；G T→I*，C I*+caption/reconstruct指令→T，J(T,I)→评价文字，R(T,Iloser,通用修图指令)→I*。BAGEL理解SigLIP→connector→MoT语义路，生成噪声VAE latent+time/text→生成expert预测速度→积分/FLUXVAE静态RGB；Janus迁移AR/VQ。UniCycle先T→图，再每题独立给图+q→答案，外部文本裁判对照T/参考答案评；公开BAGEL每次新context、不把原生成prompt直接给VQA答案模型。无视频时间轴。

主BAGEL-7B-MoT已有理解/生成双专家与共享attention交互，Qwen2家族语言配置28L/hidden3584/28Q4KV/FF18944/vocab152064/context32768，SigLIP1152/patch14/27L，加载时ViT层数减1，连续FLUXVAE路径；CPR未发明新架构。HF元数据报告14607260128个F32参数，model文件58429204680bytes，7B不能当整个检查点总参数；AE另335304388bytes。脚本默认freeze_llm=False/freeze_vit=False/freeze_vae=True/freeze_und=False，全语言与理解侧可训练、VAE冻结；和CoRL/PairUni仅LLM更新不同。JanusPro7B为AR迁移，未给同等完整后训练配置/理解保持矩阵。

## 数据、指标和实验条件

作者正文5000自生成prompt×8=约40000候选图，训练混合G5000+C5000+J3000+R1000共14000条，5K是生成提示量，不能当全部训练记录/全部计算；过滤保留率/最终5K源ID及40K→14K具体映射未给完整日志。类别含对象/关系/世界知识/空间/时间/文字/自然科学/人像/风格/计数，模板/阈值和预训先验都是外部设计。UniCycle由TIIF+Qwen3-235B-A22B生成QA再人工标注，1401prompt/2968QA(MC1067/YN200/OE1701)，该基准不属于无外部监督数据构建。当前公开bench tiif_style实际1649/3527QA、self_built689/1087QA，text分别214/113prompt，与论文1401划分不能混算；未核发布映射。主训练数据未在树内完整发布；提示生成需seedCSV，代码明确注释使用PersonaHub，seed/persona文件来源及正式训练版本待核，不接受无条件无外部数据断言。

生成TIIF testmini短/长(Qwen2.5VL72B裁判)、WISE六世界知识/物理合理性类、OneIG-EN alignment/text/reasoning/style/diversity、T2I-CompBench八项、DPG、GenEval；理解MME-P/C、MMB、MMMUval、MMVP、MMStar；额外RISE编辑。论文AppB把WISE描述为空间布局/保真过窄，按表11世界知识任务界定。UniCycle非text每题0/1、text为正确恢复required words比例，Soft为题均分再prompt平均，Hard全部题得1；关键词回收无显式字符顺序/重复/额外词惩罚，不等于CER/OCR拓扑或笔顺。循环分同时依赖生成、VQA及裁判，不能分离两者能力或排除共同错误抵消。

SD3/FLUX/DALLE3/GPT4o/Midjourney及JanusPro/Showo2/BLIP3o/OmniGen2/TwiG/T2IR1/BAGEL/IRG/UniGen/UniRL/MetaQuery等；部分†是MLLM重写，*为直接引用他文结果，基础模型/数据/分辨率/采样器/裁判/预算不同。T10两个BAGEL71/71.8和68.06/68.78、T13两个BAGEL.78/.79显示异来源评测；不能以表内混合数字称同协议全面最强。相同基座C/J/R/G删项是核心实验，但移除数据后未同量补采/匹配模态token和总FLOPs。

8×H80080GB，主SFT600steps约7h=约56GPUh，仅训练段未含自采40K图/提示/打分和所有评测。AdamW(.9,.95,eps1e-15)/lr1e-5constant/warm50/wd0/clip1/accum4/EMA.99/CE:MSE=.1:1，maxcontext40K，生成短512长1024、理解378–980，训练tshift4。发布启动600/lr/EMA/CE/accum大体同，但samplemax20480/packedmax36864、timestep_shift默认1且脚本未指定4；反射ViT配置224–518，主VLM378–980。候选采样源码50steps/CFG3至8/seed随样本与rank变/tshift3，提示temperature.8；基准BAGEL默认768²/50steps/CFG3/tshift3/VQAgreedy64tokens，Janus默认gen_do_sample False即argmax，可手动改。无多训练seed误差/端到端总采样成本；模型/数据路径和外部seed需补配置。

## 主表与消融证据

正式T1 BAGEL→UniCorn TIIF-S71→74.7/L71.8→72.9(均73.8)、WISE50→55、OneIG36.1→42.6/text24.4→46.8、Comp82.2→88.5/数70.4→83.5/3D77.98→84.12、DPG84.03→86.83、GenEval.78→.82。六综合生成项均升，但OneIG多样性.251→.203、TIIF短reasoning76.25→73.64/长text52.40→49.77；GenEvaltwo-object.95→.94。T2理解MME-P1685→1660/C696→677/MMB84.6→84.1下降，MMMU52.8→53.8/MMVP69.3→70上升/MMStar65持平。T3Hard36.6→46.5(+9.9pp)，T17Soft58.2→66.6(+8.4pp)；额外RISE33.33→38.87。T9OneIG.426低OmniGen2.475/FLUX.434/SD3.427；T10TIIF74.70/72.94低IRG76/73.77与GPT4o84.19/84.61，长分仅与Dalle3 72.94持平；T11WISE.55低Showo2.61；T13Gen.82低IRG.85/GPT4o.84。SOTA必须限定时间/模型与协议，表15OneIG SOTA措辞与自身表9不符。

正式T2 w/oCJR生成仍72.3/74.0而MME-P311/C92/MMB24.3/MMMU23/MMVP7.1/MMStar21，支持严重理解遗忘；未测生成多样性坍塌，不能从此证明latent/modecollapse。w/oR TIIF73.8/75.9/理解MMVP71.3>完整70；w/oJ74.2/74.8/MME1542/478；w/oC74.5/76.4/MME-C701>完整677；w/oG73.4/72.3/MME-P1669>完整1660。C/J/R有互补但不是每项去掉都降。T4Janus TIIF63.2→65.9=+2.7，正式纠正旧正文+3.2；WISE35→42/OneIG26.7→31.4。外部Qwen3VL235B构数UniCorn* TIIF74.4>73.8/OneIG44.9>42.6/WISE54<55/Hard40<46.5，有取舍；未提供实际教师熵/算量/latency测量，不因自监督更便宜就证明同模型自play必要。正式F6(旧v3F7)规模1K/5K/8K/10K/20K，短约74.1/74.7/75/75/75.3，长约72.4/72.9/74.2/74.8/75.5，无拟合指数/算量控制/区间；5K长72.94未超过IRG73.77，图中双轴星标位置有误，不能照抄5K超过IRG或称普适scalinglaw。

## 批判分析和优势条件

作者Limitations明确单轮、理解无显著收益和自采额外计算，F13保留否定/多对象计数失败。自身Judge与Solver共同盲点会让错误成为G/C/J/R伪标签，C原prompt不保证真由I*支持，R高低图独立seed/布局可改变无关内容；代码R用通用修图模板而未显式输入每例原J分析，不能假定学习真实多轮反思。正式D3保留Eq6示意并新增Eq7条件期望/Eq8MC修正旧概率式；仍把单条judge最优轨迹当期望近似，未给选择偏差界。MI恒等式/概率链式法则不证明共享参数多任务梯度正迁移，四条件loss不自动组成单jointNLL；Eq9提λ但未写权重，实际flowMSE非精确图像NLL，正文guarantee超出所给推导。公开bench裁判仅yes/no、不给参考答案、无text计数字段word_count，但metrics对text要求数值/word_count→当前默认text得0；非textAPI失败被跳过，整个prompt全失败不进正常或strict分母，hard还先四位rounding再判1，需固定全分母协议。主文裁判Qwen3-235B、AppC又说sameUMM，公开默认gpt4omini，需版本/日志。F10plate右侧指令对应C却标referenceA，两个pizza-shape问题重复，是示意标注矛盾，未据此推断全部数据错误。无连续笔顺/书写真实性证据。

基座已能较可靠识别/排序候选、每prompt有正确样本、合成任务覆盖测试且图文一致时，Best-of8筛选提高监督质量，多类C/J/R在共享参数上可减遗忘并迁移评价能力。适用于静态短文字、组合关系/知识等基座可验证分布，弱计数/否定/长文本/新文字体系会因自身裁判不可靠而受限。UniCycle只测循环信息一致，不保证生成图真实正确：若生成反了左右且VQA也反读可得到正确原答案，需外部视觉真值和交叉模型理解分离；高Soft/Hard不能直接叫自我反思或一般智能。

## 可证伪实验与论文写作

固定基座、14K记录/各类uniqueprompt、总生成候选与GPU秒，比较随机候选/自身BestN/独立可靠裁判/同算量外部教师，C/J/R/G移除时补齐数据/模态token与CE:MSE，分别冻结理解或生成expert，测双任务完整矩阵和梯度冲突/人评伪标签准确率。扫描N/阈值/CFG/种子/类别比例，跨类和跨模型的OOD无泄漏切分，单轮与多轮分开，多seed与CI、全流程成本。UniCycle先固定1401IDs及QA，比较原图人审/T→图+外部VQA、真实图同题能力、不同生成×理解交叉矩阵、空图/打乱图/无图对照以估计语言偏置/错错抵消；多裁判与人评一致率，text加有序CER/词序/多余字/重复、全部prompt失败记分母并公布失败数，不能仅剔除难题。检验Eq7期望与Best轨迹偏差，actualCE/MSE/任务λ梯度对图像目标的变化。跨汉字/阿拉伯文/其他字系与同终态异轨迹书写另建时序/执行约束评价。均未执行。

Intro从能判错却难生成的具体矛盾提出自身监督，Method按采样/四模式重构/独立循环benchmark组织，T2删项+T4骨干和外部教师+数据规模回答三层假设，Limitations和失败图承认理解收益/计算/弱任务，结构可学习。ConductionAphasia为行为类比，不能当神经机制定理；模式坍塌与理解遗忘、一般智能与循环一致要严格区分。Claim须保留多样性/理解小降、外部教师部分更优、TIIF/OneIG非全榜最强与5K/14K/40K分母；正式对旧Eq6的修正应承认，不把已修问题重复写成未修。完整发布seed/PersonaHub、划分和评分代码差异比口号式zerohyperparameter更有可评审价值。

## 实际阅读范围

arxiv2601.03193v2完整HTML Abstract/§1–5/Limitations及AppA–E研究文字，全部17表(对应HTML25个含公式块)/旧Eq1–7；正式ACL32页完整27340213bytes、§1–5/Limitations、AppA目录/B实验/C相关/D1–4理论/E1–3基准/F1–3结果和全部T1–17/Eq1–9交叉阅读，实际PDFp3/5/7/8/20/21/24/25/26/27/28/31/32共13页核看。实际旧版原始F1/F4/F5/F7/F10/F13共6张核看，其他图注读、未逐图所有定性图片/全参考文献；正式F6规模图与旧F7号区别已记。主GH e3b4518d完整209项树/README全文，启动/yaml/registry/getmax/selfjudge/selfreflect全文、caption模板/转换、proposer规则/seed/persona/采样、imagegeneration/reward输入输出、trainer冻结/配置/CE-MSE和模型flow forward选段；HF5e8d1df7 README/配置/文件树/index/参数元数据，未下载权重。UniCycle GHaa1cf81f完整25项树/README全文、两JSONL全部解析计数/结构与样例、metrics全文、judge全部有效提示/参数/循环、runner入口和BAGEL输入/默认/新context、Janus采样选段；未独立逐题审注、全trainer/全部后端源码或运行API/模型。实际训练集/seedCSV/persona文件未取得，未独立复现。

## 关键主张与证据对应

| 细节／主张 | 核查结果 |
| --- | --- |
| Self-play训练形式 | 同UMM分别充当提示生成、图像生成和裁判角色；离线选优、重构四类数据后CE/MSE监督微调，没有在线GRPO/PPO |
| 5K数据、7h成本 | 5K生成prompt、40K候选图；G/C/J/R为5K/5K/3K/1K，共14K训练记录；7h仅SFT，未含全部生成和打分 |
| 无外部数据 | 公开proposer需要seedCSV，代码明确注明使用PersonaHub；正式训练具体版本/seed/persona未完整发布，应限定断言 |
| 联合目标保证正迁移 | MI/Bayes/链式法则是恒等式，不保证有限模型/不同条件数据/CE+flowMSE梯度同向 |
| 反射边缘化缺失 | 正式Eq7增加条件期望、Eq8增加MC平均，承认修正；最高置信轨迹仍不等于无偏MC平均 |
| 生成全面提升 | 六个聚合分提高，但OneIG多样性.251→.203、TIIF部分子项与GenEval两对象下降 |
| 理解保持 | MME-P1685→1660、MME-C696→677、MMB84.6→84.1；MMMU/MMVP提高，MMStar不变 |
| 丢理解即生成mode collapse | w/oCJR理解分大跌，只证明这些理解任务遗忘；没有该消融图像多样性或分布坍塌证据 |
| 5K超越IRG30K | TIIF长72.94<73.77，规模图双轴IRG星标与表数不一致；不接受全面超越说法 |
| OneIG最强 | .426低于同文表列OmniGen2 .475、FLUX .434、SD3 .427 |
| 外部教师始终较差 | 外部教师TIIF/OneIG更高，WISE/UniCycle更低；没有熵或总成本的因果测量 |
| UniCycle公开划分 | 论文1401prompt/2968QA，发布两文件合计2338/4614；缺少论文子集映射 |
| 文本计分实现 | metrics要求恢复词数/word_count，公开裁判仅输出yes/no且无word_count，默认串联使文本题得0 |
| 缺失答案与失败处理 | 裁判按min问题数/答案数循环；部分失败被过滤，全失败prompt可退出分母，需固定完整题目宇宙和覆盖率 |
| 裁判协议一致 | 正文Qwen3-235B、附录sameUMM、代码默认gpt4omini；当前代码未将参考答案传入文本裁判 |
| 权重可直接按所有脚本加载 | HF有model.safetensors，采样脚本预期ema.safetensors；索引旧总大小/文件名、rootconfig尾逗号需适配，尚未运行加载 |

## 公式的作用及可验证范围

正式D.1的互信息分解、Bayes联合概率和链式法则解释为什么caption、judge、reflection可能携带生成所需信息。它们给出目标联系，不能推出固定数据分布的互信息随训练必增，也不能保证任一有限容量模型的辅助任务梯度对生成有益。正式D.3明确把Eq6乘积作为说明，再用Eq7对中间图像条件期望、Eq8以Monte Carlo近似；旧v2缺少边缘化的问题已经得到部分修正。最高置信轨迹的Best-of-N选择依然改变分布，需要区分筛选启发式与无偏期望估计。

正式Eq9写四模式损失求和，实际连续图像侧为速度MSE，文字侧CE且有.1:1权重。数据配比、长度归一和不同任务的输入条件共同决定实际梯度，不能直接当成同一个联合分布的精确NLL。对照应在相同样本/模态token/计算量下测辅助任务是否提高图像目标，而非仅删掉若干数据后比较。

## 循环一致性的识别问题

T→生成图→VQA答案的一致分，可能同时受生成质量、识别能力、语言先验和裁判偏差影响。生成器把左右画反且VQA也把左右认反时，循环答案仍可能与T一致；因此同一个聚合分无法识别每一环真正能力。应固定题目/参考和失败分母，用生成器×识别器交叉矩阵、真实图题、外部识别、人评、空图/错配图对照分解因素。

实际Fig10的羊/盘子示例中，prompt要求right而选项A=left、C=right，标注reference却是A；这是一处图示内矛盾，不能由此推断整个基准标签均错误。公开BAGEL每次VQA初始化新context，没有直接把原T传给识别器；不能在没有证据时指控原prompt泄漏。文字恢复率尚未显式处理字词顺序、多余字、重复和连续笔画事件。

## 公开资源与实验边界

主代码209项树，基准25项树，HF配置/文件索引及两个基准JSONL已核；实际训练样本、seedCSV及PersonaHub文件未取得。HF元数据为14.607B F32参数，model文件58.429GB，7B不能当整个检查点总参数。旧索引29.55GB且指向ema文件，与当前发布文件不一致；根config尾逗号影响通用JSON解析，但自定义加载器读独立llm/vit配置，不能据此断言所有加载方式无效。未下载权重或运行模型。

该方法处理静态图像，不能作为已有严格汉字笔顺视频生成模型。对我们研究的价值是自身筛选、多模式数据重构和循环评价的已有先例；新的协同主张需要事件级可观察任务、独立裁判、跨文字体系及公平总预算验证。下一项继续L132；SRUM、UniRL、PersonaHub、AbsoluteZero、RZero和Reflexion保留追引队列，独立研究计数前去重和原文精读。
