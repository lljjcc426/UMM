# CoRL：联合优势、任务分支与奖励发布审查

第一百四十批完成[L129](../reviews/L129.md)明确范围核心三遍与五项书面记录。[结构化证据](../../data/corl_joint_advantage_branch_and_reward_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），249核心/252书面含未通过项；未确认核心81论文／研究+27资源，资源另审。无目录新增、删除文件、权重下载或模型执行。

来源：[NeurIPS2025正式版](https://proceedings.neurips.cc/paper_files/paper/2025/hash/08f6f963e993ee81625adb5aaac9403c-Abstract-Conference.html)、[v3](https://arxiv.org/abs/2505.17534v3)、[固定代码](https://github.com/mm-vl/ULM-R1/tree/0c92629f9b307a32bb286ae3562809e941d1bb0b)。正式24页，实际8页交叉核，全文核心阅读以v3 HTML及正式主表/方法/附录为依据；2页旧匿名supplement单列。

## 问题定义与研究路线

统一图文AR模型能否经联合GRPO建立理解/生成基础，再经任务特定RL增强两种能力；比较独立、权重合并、交替、统一策略，并研究图文语义循环与token匹配奖励。研究为静态T2I/图像QA后训练；无连续视频、文字笔顺或真实笔触动作评价。

仅理解RL容易牺牲生成，单独CLIP奖励对细对象/关系辨别有限；共享LLM允许跨任务参数迁移和联合优势。用真实图-描述-QA对将两个任务配在同个组，视觉感知相似与caption循环约束、token级匹配加QA正确/格式形成联合奖励。无coldSFT的RL仍依赖有标注图/QA/原始caption、预训Janus及感知/语言评价器，不能写不依赖监督数据。

CoRL stageI对同个真实样本分别采G张图和G个文字推理答案，把cycle+TIM+.8*(QA+format)合成联合奖励/组内std优势，同时更新共享LLM，β0；stageII分别T2I、MC、OE用各自奖励/数据和β.02继续。循环为1−LPIPS(真实图,生成图)+SPICE(原prompt,BLIP重caption)，TIM为双向token max-cos均值；对应ULM-R1。混合QA额外合并MC/OE两个模型；所有最终结果不由同一权重得到的证据须保留。

## 模块与数据流

stageI真实图/QA→独立SigLIP语义encoder+aligner→共享AR LLM→think/answer文字；同样本原caption→同LLM+图像code embedding/head→576离散image IDs→VQ decoder成384²图。两路各采G，图像重caption及真实图比对、TIM与QA格式/正确性算reward，共享优势反馈两路LLM。stageII分支各自输入输出；没有图像帧序列、扩散去噪、显式笔画轨迹或闭环执行。图像code的raster AR顺序不等于书写时间顺序。

Janus-Pro-1B为基座，主表LLM实际列DeepSeek1.5B；原HF960ab331配置24层/hidden2048/16Q16KV/FF5632/vocab102400/context16384。理解SigLIP-large-patch16-384输出1024→2层GELU MLP2048；生成VQ-16/码本16384/8维code，24×24=576token，独立gen_embed/aligner/head和VQ图像decoder，共享language_model。当前init_trainable_parameters冻结理解vision/aligner及生成VQ/aligner/head/embed，仅训练LLM；表7 Janus1.3B全参语言训练、7B LoRA，非所有系统模块都全参。扩展同AR家族，不能证明扩散/flow UMM均适用。

## 训练数据与实验协议

pilot x2x_rft_16k与stageI x2x_rft_22k来自COCO2017 train真实图，QA/答案适配A-OKVQA和GPT-VQA；caption按答案实体覆盖选择，README约70%覆盖。HF固定卡片实数16415/22479，字段prompt/real_image/qa_problem/qa_solution/qa_type和分类/检测/coverage；卡片无独立详细构建正文。stageII T2I继续16K，MC/OE来自MCoT-Instruct，含AOKVQA/M3CoT/SQA-train/ArxivQA/TabMWP/MAVIS与GeomVerse/RCoT等。HF mcq66025/OE66617，表3ColdSFT为两个各22K子集，训练实际子集抽样/去污染和重叠未完整给出；此前将II全写各22K须修正。

生成GenEval(对象/计数/位置/颜色属性)、WISE知识合理性/审美、DPG密集指令；理解MMMU/MMStar/WeMath MC，MMVet/POPE/LogicVista OE，MathVista/MathVerse-Vision/MathVision混合格式，VLMEvalKit。LPIPS/SPICE/TIM/QA标签/格式是训练reward，不等于独立测试质量；无有序OCR/CER或笔顺事件。7%/23%可由把同类benchmark统一尺度后平均分的相对提升近似重建，约6.93%/22.98%，不能当每项提升或+7/+23个百分点。

T1生成PixArt/SD1.5/2.1/3Medium/SDXL/DALLE3/LlamaGen/SimpleAR；统一TokenFlow/Emu3/DPO/LWM/Orthus/Janus/JanusPro/ILLUME+/D-DiT/Harmon/Showo/HermesFlow。T2理解SmolVLM/SAIL/Ovis2/InternVL3/Qwen2.5VL/LMMR1及ILLUME+/Harmon/VILAU/Orthus/UniToken/SGenVL/Showo/HermesFlow/Janus。原生256/384/512/1024分辨率、模型先验/参数/数据不同；表2†部分由作者重评；不要以异协议全榜排名代替同基座消融。

8×H20 96GB/AdamW；正式T8 stageI G8/β0/batch16/lr4e-6/epoch1/最大prompt1024/completion512；stageII G16/β.02/lr1e-6/epoch1，T2I batch16/prompt256，MC/OE batch32/prompt1024/completion512。文字评测greedy，图像384²/CFG5/576AR tokens。公开统一脚本8rank×perdevice1×accum4、maxcompletion576/lr4e-6/epoch1/G8/β0，名称bs16不解释实际采样有效batch口径，不能直接当正式全配置。代码温度固定1；图像含两CFG分支；无端到端时间/总训练GPU小时、多seed区间。阶段II/权重合并完整配方和最终检查点未在所读固定入口/官方集合核到。

## 结果与消融能支持什么

T1 JanusPro1.5B GenEval.73/WISE.26/DPG82.63→ULMR1约.77/.33/83.92，消融精度Gen77.3；计数.51→.71/属性.56→.80。统一模型GenEval低于Janus7B.80；WISE.33低于Harmon.41/Emu3.39/Janus7B与Showo.35，正文second-on-WISE与表不符；计数.71仅统一组最佳，专用SD3.72更高。T2九项36.3/43.1/5.9/39.8/86.2/23.9/37.3/13.5/13.4→42.3/47.6/21.1/43.9/88.9/34.5/42.5/25.4/22.0；MMMU仍低ILLUME+44.3、MathVista42.5低SGen42.7、MMVet43.9低Janus7B50。混合题用MC/OE权重合并，不能写全部由同一生成+理解检查点同步达到。

F1 pilot生成/理解平均77.8/38.1；单T2I78.4/36.1、单理解77.1/41.0、合并78.4/39.1、交替77.9/40.1、统一79.1/41.5，无预算/方差完整隔离。T3统一S1 Gen75.9/DPG83.3/MMMU40.3/WeMath14/MMVet42.5/Logic30.2；ColdSFT72.8/82.5/41.0/18.0/42.0/27.9，统一在MMMU和WeMath更低。最终CoRL77.3/83.9/42.3/21.1/43.9/34.5较ColdSFT+RL74.5/82.8/41.8/22.5/43.7/35.9：生成更优、WeMath和Logic更低。T4 CLIP74.2/82.4、TIM74.1/83.0、cycle76.2/83.5、cycleCLIP77/83.4、cycleTIM77.3/83.9；TIM单独Gen低CLIP。T5 SSIM77.5/83.6 vsLPIPS77.3/83.9有取舍。T6 λ.7/.8同77.3/42.3，.9为77.1/43.5，非唯一最优。T7 Janus1.3B和7B各九项均升，但模型/LoRA方式改变，增益非线性。T3ColdSFT Gen72.8−73.0=−.2pp，表打印−.3待核。

## 局限与优势条件

TIM对固定token向量集合置换和重复最近匹配不敏感，无一对一/显式空间约束；上下文hidden可编码位置，不能直接说整个模型对文字顺序恒不变。真实图LPIPS把多解T2I偏向单一布局；学习中自身TIM/recaption可共同漂移。论文说cycle/TIM归一到[0,1]，所读active代码未见显式此归一；默认自身recaption+BERTScore/Jaccard+1−滑窗RMSE，与正文BLIP/SPICE/LPIPS不同。QA传qa_type列表，reward却直接与字符串MC比较，进入OE匹配/softJaccard而非逐例MC抽取；论文二值准确率与默认软分有差异。图像rollout用CFG5，但所读logps为条件分支普通logsoftmax；还对已拼接全部image IDs的最后576位置打分，可能较next-token目标晚一位，需作者版本/实际tensor位置复核，未以此推断论文结果无效。Eq6写联合输出概率比，实现为共享优势下两路token ratio各自mask均值相加；§3.3.3文字说reward替代Ai而未说明stageII归一。统计checklist明确No。无最终同权重全任务评测/完整预算控制/视频笔顺证据。

共享语言参数、配对样本实体覆盖高、QA答案和语义reward可靠时，联合优势可能让生成学到理解实体并让两任务减少遗忘；phaseI为后续专门任务RL提供较好起点。真实图感知奖励适合受限图文配对分布，开放多解生成可能损多样性；token最近cos不足保证对象关系/字序/细笔。权重分支与合并、相同家族基座及预算限制使普遍协同不能由最终主表直接推出。

## 验证方案与论文写作

固定Janus基座、unique配对样本、MC/OE子集/epoch/总rollout/GPU秒和评测模板，比较单任务/交替/联合独立优势/联合奖励、实体相关对与随机配对、共享/冻结部分LLM；同一S1与每个S2/合并权重都完整测生成和九理解项，报告双向增量/梯度冲突及Pareto。拆真实图LPIPS、caption评价器、TIM和各归一/λ，CLIP与同预算OCR/关系验证奖励对照，TIM固定裁判与动态自身对照；保留多解多样性。核CFG采样概率和teacherforcing位移，公布修订脚本/实际版本，比较token/sequence归一；多seed与误差区间。用跨字符/字体/字系和同终态异书写过程切分测有序OCR、事件顺序/接触与RGB可见性；静态图像AR不能替代视频实验。未运行。

Intro先pilot四种RL范式再提出基础-专门化两阶段，Method按reward/统一优化/任务细化，T3与T4–6分别检验范式/奖励/权衡，图中保留失败例，值得学习。Claim需限定监督来源、主表检查点/分支、相对均值7%/23%与绝对百分点，保持精确表中排名；统一RL优于ColdSFT在WeMath并不成立。Limitations除简单reward和能力差距，还应公开单权重证据、caption/真实图偏置、默认脚本差异、MC列表判别/采样概率与位置核查，避免把verifiable当完全正确的语义裁判。

## 实际阅读范围

arxiv2505.17534v3 HTML Abstract/§1–6核心全文、完整T1–8/Eq1–6与Fig1–5图注、AppA1/A2；正式24页PDF2078913bytes，实际p3/4/5/6/7/8/10/24共8页交叉核pilot柱图/架构/公式/全主表与消融/训练数据表，未逐图p9所有QA细字、逐篇参考文献和全checklist指南；统计No与资源声明选读。官方2页早期supplement A1/A2研究文字和训练表已读，引用列表不独立算精读。GH0c92629f完整2828项树/2798blob及README全文；统一启动全文、入口参数/数据映射、trainer冻结/采样/奖励汇总/优势/两token损失与logps、cycle活跃函数/默认模型/metric、TIM函数/切片、QA/format/registry；Janus联合forward与CFG采样/VQ构造、eval生成和混合评测接口选段。HF4数据卡全文和元数据/实际声明行数，未下载全部parquet；JanusPro1B960ab331配置/元数据；官方collection4数据未见模型权重条目不等于全网无权重。额外TTRL README、两个启动参数/奖励选段：投票答案只用GT作命中日志、图像自选高分参考；未读完整TTRL trainer/复现，不计独立论文完成。无权重下载、训练/推理执行或独立复现。

## 联合训练与最终检查点的区别

| 证据 | 研究判断 |
| --- | --- |
| Fig1统一RL生成79.1/理解41.5，高于baseline77.8/38.1 | 支持该pilot共享训练的双项提升，未匹配所有任务曝光/算量和误差 |
| T3 S1 UnifiedRL Gen75.9/DPG83.3/MMMU40.3/WeMath14 | 同一个S1具备双任务结果；WeMath低于ColdSFT18 |
| S2分别T2I、MC、OE，混合题又合并MC/OE | 最终主表跨分支，需每个检查点都跑完整双任务矩阵 |
| 最终CoRL WeMath21.1/Logic34.5 vs ColdSFT+RL22.5/35.9 | 不存在所有理解项一致优于有监督起点 |
| 原版GenEval .73→.773、WISE .26→.33、DPG .8263→.8392 | 统一尺度后均分相对增约6.93%，非各项+7pp |
| 九项理解均分33.27→40.91 | 相对约22.98%，非每项+23pp |
| WISE.33，Harmon.41/Emu3.39/Showo与Janus7B.35 | 正文second名次与表1不符 |
| T4 TIM Gen74.1<CLIP74.2，T5LPIPS Gen77.3<SSIM77.5 | 平均分和DPG优势要保留指标取舍 |

## 奖励和概率实现的具体边界

[统一脚本](https://github.com/mm-vl/ULM-R1/blob/0c92629f9b307a32bb286ae3562809e941d1bb0b/corl/scripts/corl_unified.sh)启动unify_reward=True、unify_advantage=False；[trainer](https://github.com/mm-vl/ULM-R1/blob/0c92629f9b307a32bb286ae3562809e941d1bb0b/corl/open_r1/trainer/grpo_trainer_unified.py)实际先将T2I奖励与.8倍理解奖励相加，再对配对组做std归一，并把同一优势用于两路token级ratio，各自按有效token数平均后求和。它保留联合奖励耦合，但没有直接实现Eq6写法中整对输出的sequence probability ratio，需说明具体近似及归一目标。当前系数.8写在trainer里，扫描λ需要改实际配置或实现；论文表6的扫描不能只改一个未连接的外部参数。

[默认参数](https://github.com/mm-vl/ULM-R1/blob/0c92629f9b307a32bb286ae3562809e941d1bb0b/corl/open_r1/grpo_janus_unify.py)使用自身caption、Jaccard+BERTScore、image_cs_metrics=mse；[cycle活跃实现](https://github.com/mm-vl/ULM-R1/blob/0c92629f9b307a32bb286ae3562809e941d1bb0b/corl/open_r1/rewards/r_t2i.py)实际上调用滑窗root-MSE而非普通全图MSE。选择LPIPS才用vgg网络和224²图；论文的BLIP/SPICE/LPIPS配方没有被当前默认启动显式选中。SPICE在另一个caption consistency函数出现，不能据此声称活跃cycle默认用SPICE。所读cycle/TIM活跃路径未见论文承诺的各自[0,1]变换，组内std不是这项变换。

[QA函数](https://github.com/mm-vl/ULM-R1/blob/0c92629f9b307a32bb286ae3562809e941d1bb0b/corl/open_r1/rewards/r_base.py)接收qa_type列表却用kwargs[qa_type]==MC这种整体比较；MC抽取分支因此未按逐例类型选择，OE还给softJaccard部分分。此处描述的是所读静态调用路径；没有执行代码或用它推断正式训练已发生何种错误。格式函数用fullmatch，可检查标记但不验证推理正确。

[Janus实现](https://github.com/mm-vl/ULM-R1/blob/0c92629f9b307a32bb286ae3562809e941d1bb0b/janus/models/modeling_vlm.py)的采样用cond/uncond CFG5，logps路径却取条件分支普通softmax；若将其视为采样分布的精确importance ratio需要额外修正或论证。另一个待核点是将全部576图像code拼接后，直接取最后576隐藏状态对同一组code打分：标准next-token teacher forcing应从最后prompt位置预测第一个code，该切片表面晚一位。需作者真实版本、位置示例及梯度检验确认，不能将当前发布版本的问题直接当已发表结果作废的证据。

TIM从当前LLM hidden固定切图像5:581、文字586之后，再做max-cos。对既定向量集合，最近匹配允许一对多、缺少顺序与位置硬约束；hidden已含位置上下文，因此不能写整个模型绝对对顺序不敏感。跨模板、不同patch长度和新文字体系需重新检验切片和裁判可信度。

## HF数据与额外TTRL制品

| 制品 | 固定版本 | 卡片声明训练行数 |
| --- | --- |
| x2x_rft_22k | f52833ce01b5657294bed87f23f27d04b92838b9 | 22479 |
| x2x_rft_16k | a25a5992543d7b97cd5561b4b0cbe57f36afb15e | 16415 |
| mcot_r1_mcq_66k | 8ddff75bea9a80e3fdb59ecd17da2d02fcca29ef | 66025 |
| mcot_r1_vqa_66k | ada4d925fd843f81d45f087435c7dbd9cfdfa065 | 66617 |

数据卡主要是schema/计数，没有完整去重、子集抽样、源许可证整合和分布分析；未下载约数十GB parquet。表3ColdSFT指定的MC/OE各22K不能作为两HF完整发布量。官方collection本次只有四数据条目，README未列最终权重；不把这一有限检索扩大为全网没有权重。固定完整源码树2828项，按相关入口/路径未核到完整stageII启动/合并配方，仍需作者补全。

README额外发布[TTRL代码](https://github.com/mm-vl/ULM-R1/tree/0c92629f9b307a32bb286ae3562809e941d1bb0b/ttrl)，记录MMMU36.3→39.8、MMStar43.1→46.9、GenEval.73→.76、UniScore.370→.455。这是测试时参数更新协议，不能混入CoRL离线主结果。理解奖励按采样答案多数投票，GT只用于所读reward函数的命中率日志，不凭GT变量名就指控标签监督泄漏；生成奖励以caption得分最高的生成图作为图像一致性参考，该函数在整个传入列表取一次max，跨提示分组方式需结合尚未全读的trainer复核。没有独立验证这些README数字，也没有完成整个TTRL源码精读，已作为额外非论文制品队列保留。

## 对后续选题的约束

可研究配对相关性、联合优势的跨任务信用分配、同一权重与专门分支的收益代价、动态自身裁判漂移；须先检索已有PairUni/UniCorn/UniSynergy等工作，不能看到一个实现问题就称有可发表新课题。下一项L130 PairUni。静态图像token预测与规范书写过程仍需要不同数据和可观测事件设计。
