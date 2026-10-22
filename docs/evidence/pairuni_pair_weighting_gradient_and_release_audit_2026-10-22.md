# PairUni：配对权重、梯度解释与公开实现审查

第一百四十一批完成[L130](../reviews/L130.md)明确范围核心三遍与五项书面记录。[结构化证据](../../data/pairuni_pair_weighting_gradient_and_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），250核心/253书面含未通过项；未确认核心80论文／研究+27资源，资源另审。无目录新增、文件删除或模型执行。

来源：[v3全文](https://arxiv.org/html/2510.25682v3)、[元数据](https://arxiv.org/abs/2510.25682v3)、[固定代码](https://github.com/Haochen-Wang409/PairUni/tree/0097f4197c7c4b564ffefacb8cbf09b03b61e735)、[作者主页](https://haochen-wang409.github.io/)。完整HTML、10表/Eq1–4、实际7张原始图为本次依据；PDF只有3.06/36.24MB，未声称完整PDF阅读。正式会场尚未独立核实，撤回旧主页ICLR标签断言。

## 问题与方法逻辑

在共享统一图文模型的理解和生成后训练中，数据语义不相关会否加剧性能取舍，能否用同图补全与跨图检索构造配对数据，并在独立任务GRPO优势之后以配对相似度加权，改善双任务结果。任务是静态图像QA/文生图及迁移静态编辑，不含视频或严格笔顺。

常规混合任务RL未显式利用理解/生成样本语义对应，两个任务可能更新不一致；同图合成注释质量/数量受限，跨图视觉近邻可扩规模。作者把弱相似称梯度冲突，但所示六种梯度余弦中位数均为正；低正余弦只说明较弱同向性，负梯度频率/层别/时间统计尚缺。

PairUG-16k构造：理解Orsta约47K用GPT-o3补生成caption，生成BLIP3o约60K用GPT-4o补QA；联合ResNet50归一特征MiniBatchKMeans选离中心最近实际样本形成同图aligned，剩余跨源图greedy top-n余弦检索/阈值δ=.6配对，每图仅用一次。PairGRPO对每任务各自prompt的G个reward先std归一，再乘共享pair权重aligned=1/retrieved=sqrt(similarity)；理解Acc、生成HPSv2。两路独立优势通过共享LLM联合更新，并非CoRL将图像/QA reward合成同一优势。

## 输入输出与模型结构

理解图+问题→Janus独立语义视觉encoder/aligner→共享LLM→文字答案；生成caption→同LLM+图像embedding/head→576离散code→VQ decoder静态图。配对字段保存两路输入及similarity，分别采G个答案/图像，独立reward与组内std，std后乘pair权重再联合梯度。Lumina-DiMOO换离散扩散骨干，文字2步/图像35步；BAGEL只做1:1理解/生成SFT。没有帧间生成器、笔画接触事件或文字书写时间轴。

主Janus-Pro-1B/7B，理解SigLIP与生成VQ分支解耦、共享AR语言骨干；1B基座语言配置可参L129已核HF960ab331的24L/2048/16QKV、16384码本及384²/576codes。固定PairUni代码冻结vision/genVQ、两路aligner和gen_head/gen_embed，仅更新language_model，主入口peft_config=None；不能说整个系统全参更新。根configs/config.json为LLaVA-OneVision/Qwen2-7B遗留配置，主入口通过Janus路径加载，不据该文件把模型误定为LLaVA。Lumina离散diffusion与BAGEL流匹配+AR为迁移，后者未验证PairGRPO。

## 数据与实验条件

Orsta47K排除原检测/grounding QA，BLIP3o60K；PairUG实际16320=4971aligned(3043生成源+1928理解源)+11349retrieved。Aligned17类、Math646/gesture602/puzzle402/count65，retrievedJourneyDB2476/GenEval1787/gesture1387/object1 1232/text2 1193/text1 992等；分布长尾。GenEval1787训练类需要来源/原始提示及与553测试模板/语义实体去重核查，未证明已泄漏。README示例towel+zebra不在本地553官方测试提示中，仅一个示例不证明全体清洁。预训无重叠为作者未独立验证声明。当前固定代码无JSONL/parquet/模型权重文件、HF数据/模型链接comingsoon，未取得完整PairUG或合成日志。

理解MMMU/MMStar/MME Perception/POPE，生成GenEval六类和均分、WISE六知识类；迁移Lumina含ImgEdit add/replace/remove/style，BAGEL另GenEval S/L与编辑综合。GenEval主要测组合指令遵循，不应笼统只称视觉保真；HPS偏好不是逐字OCR/笔顺指标。梯度余弦中位数、前200step reward曲线为机制相关证据，未给跨seed区间/完整梯度分布或因果中介识别。

主理解比较Janus系列/CoRL ULM-R1 S1†、专用Qwen2.5VL/InternVL/MiniCPM等；生成含SD3/DALLE3/SDXL/JanusProR1/Harmon/TokenFlow/Showo/Emu3等。主表ULM-R1 40.3为S1，CoRL最终分支42.3不同协议，不能说PairUni在同最终模型条件胜出。WISE所列局部组不能外推当代SOTA，MindOmni原版.60/HQ.71等不在该表。原始基座预训、数据规模、分辨率、RL算量/检查点不同；同基座随机配对/无配对和相似度消融优先于跨系统排行榜。

8×H100；7B Gtext=Gimage=4/max1200steps/perdevice2/global16/lr1e-6/CFG5/β0/temperature1；1B G8其余按正文。默认ResNet50无分类头、L2特征、MiniBatchKMeans，δ.6，K与top-n完整数值及合成API预算未核到。公开train.sh为Janus1B/G8/perdevice1/accum2/max8000/maxprompt512/图像576，节点/rank变量需外部配置，与正文7B配方不同。文字实际采样512token/temperature1并EOS mask；图像CFG5采样但logps只算条件softmax。Lumina G2/文字2步图35步；BAGEL SFT 1:1与512²/default其余配置，不代表RL。未给完整端到端GPU时/多seed误差或最终检查点；未执行训练推理。

## 主结果和完整消融

T1 Janus1B MMMU36.3/MME1444/POPE86.2→40.4/MMStar46.4/MME1483.2/POPE86.4，7B41.1/46.5/1567.1/87.4→47/49.5/1597.7/88；MMStar主表46.4对消融46.1未解释。T2 WISE 1B.23→.38、7B.35→.45；1B Janus/JanusPro标签与CoRL基座.26不完全一致，不能强行同协议。T3 GenEval1B.73→.79，但count.48→.44、color.90→.75、single.99→.98；7B.79→.85但two-object.88→.75，JanusProR1.86更高。T4当前v3 Lumina基座58.6/52.4/.88/编辑3.82/3.83/2.76/4.18→61.3/52.6/.89/3.84/3.94/2.78/4.22，所有所列编辑项均升；纠正旧笔记不是全部高于原基座的过时表述。BAGEL配对SFT MMMU54/POPE89.21/GenS84.6/GenL87.2/Img3.51高于作者复现52.8/87.37/77.9/86.1/3.38，但MMMU<原报告55.3、GenL<88；仅数据配对SFT迁移证据。

T5 Uonly38.2/43.7/.75、Gonly36.4/41.9/.74、unpair38.4/44.4/.71、random38.4/44.3/.73、aligned39.2/44.6/.76、retrieved40.1/44.9/.77、Pair7.5K39.6/43.7/.76、full40.4/46.1/.79，数据量/选样/总曝光需进一步配平。T6加权1B MME1469.87→1483.18/MMMU40→40.4/MMStar45.1→46.1但Gen.79不变；7B1554.91→1597.71/47不变/47.7→49.5但Gen.85不变。T7线性40.3/46/.79 vs平方根40.4/46.1/.79，仅小理解差无区间；T8δ.5/.6/.7 Gen.76/.79/.72同时改数据量，未隔离阈值纯效应；T9随机38.4/44/.73 vs聚类40.4/46.1/.79。T10PE40.1/45.5/.77、DINOv340.4/46/.79、ResNet40.4/46.1/.79，不足因果证明视觉相似优于语义抽象。F9六类梯度中位数Pair.120/retrieved.102/unpair.091/Uonly.082/Gonly.059/random.059，均正且仅单柱无分布/误差。F4仅200steps reward .234附近起，Pair约.254、random约.219，无误差/EMA系数，不能冒充1200/8000全程收敛证明。

## 批判阅读与优势条件

平方根对s∈[.6,1]满足sqrt(s)≥s但导数≤.646，两高分绝对差/比值差压缩；论文放大相对差异解释错误。单对两梯度乘同一正权重保持夹角不变，不能单靠标量宣称消除该对冲突；跨样本加权可改变总梯度，需另测。图8retrieved直方图实际含.2–.6而正文δ.6，尚未解释统计阶段/score定义；正文严格语义绑定/自验证未有质量量化，实际F11/F12只显示给图(和类)同时生成QA+caption，没有显式既有QA或caption输入和自验证指令，且§11路径图号与标题错位，不能代替所声称pipeline的完整证据。公开reward为SequenceMatcher字符串软相似、数字相对误差，而非通用二值Acc；HPSv2.1权重与正文v2名称须辨。实际损失exp(logp−detach(logp))*A、无oldpolicy保存/PPOclip；前向ratio=1仍有score-function梯度，并非无训练信号。两路所有completion tokens共分母导致576图像tokens与答案长度隐式权重；图像采样CFG和conditional logps不同。图像teacherforcing本实现已正确前移、补零返回后切片，不沿用CoRL待核位移问题。没有显式Limitations章节、公开全数据/最终权重或直接视频笔顺证据。

同图QA与caption覆盖同一实体、自动标注可靠且视觉近邻确实对应相同学习技能时，选样与同批两任务可减低无关梯度，std后权重可改变跨样本贡献。若把同pair正标量乘到reward后再std会抵消，本文放在优势后具有实际作用。高相似近邻也可能标签/空间关系不同；相似图像不自动意味着兼容梯度，合成数据质量与任务难度可能才是收益来源。HPS适配自然图偏好不保证计数/文字/精细线条，主表已有计数颜色下降。

## 可证伪实验和写作学习

固定基座、unique原始图/QA/caption与总rollout/GPU秒，按sameimage补全/高相似检索/随机配对×统一或独立batch×1/linear/sqrt/梯度手术全因子，匹配类分布/难度/数据量和模态有效token归一；独立测梯度负余弦比例、范数/层别和协方差、多seed置信区间，检验配对→梯度→泛化中介。发布完整PairUG索引、GenEval1787原始提示/源ID/实体模板去重和预训交叠说明，独立人审合成QA/答案/caption及验证失败率；校对δ.6与直方图分布。用同一检查点完整测六类GenEval/WISE/四理解项；按论文clippedoldpolicy对照当前scorefunction、CFG真实采样logps和conditional近似，隔离长度归一。迁移BAGEL同预算SFT与RL分列，Lumina公开扩散概率/PPO估计。跨字体/字系/细笔有序OCR、同终态不同轨迹的事件/RGB可见性评价需另建数据；均未执行。

Intro将数据语义对应与共享训练取舍联系，Method先同图补全/检索构造再独立任务GRPO和std后加权，数据/权重/阈值/encoder消融逐项对应，路线可学习。Claim需限定六类退步、BAGEL为SFT、梯度仅中位数相关与平方根压缩效应；不能把模板中的普通联合标注写成已展示自验证，或把低正余弦叫严格冲突。完整Limitations应给公共实现差异/缺少模型数据、版本日期、阈值分布矛盾与评测污染审计。旧记录作者主页ICLR断言与Lumina部分编辑不升本次明确更正，避免继承历史判断。

## 实际阅读边界

完整arxiv2510.25682v3 HTML Abstract/§1Introduction/§2Method/§3Experiments/§4Conclusion、App5Related/6Data/7Ablations/8Gradient/9Generalization/10Cases说明/11Prompts说明，10表与Eq1–4全部读；全部12图图注(含伪代码)，实际原始F1data_pipeline/F3GRPO/F4reward_curve/F8data_analysis/F9intro/F11generate_prompt/F12understand_prompt共7图核看，未逐图读其他定性例图细字或独立读全引用。PDF3,061,431/36,237,881byte部分下载无完整可读PDF，未声称22页PDF阅读。GH0097f419完整187项树/166blob与README全文，train.sh/入口grpo.py/dataset.py/两reward/utils/config全文，trainer冻结、文本图像输入/采样、teacherforcing、reward组内归一和std后相似度、合并token损失/β默认选段；未逐文件全库、完整第三方HPS或Lumina/BAGEL训练。HF链接comingsoon、树无数据/权重文件；未下载完整PairUG、权重、模型执行或独立复现。作者当前主页/正式场地检索仅能撤回旧未经证实会场断言，不能推断录用或拒稿。

## 核心主张与实际证据对应

| 主张／细节 | 已读证据与判断 |
| --- | --- |
| 两任务共享优化 | PairGRPO每任务独立标准化优势，再乘相同pair权重；CoRL把两任务奖励相加后共享优势，必须区分 |
| 平方根放大相对差异 | 对s∈[.6,1]平方根增大数值、压缩差距；该文字解释不成立 |
| 单对梯度冲突被相似度权重消除 | 同一正标量保持两梯度夹角；跨pair重加权可能改变总梯度，需要额外证据 |
| 梯度机制 | Fig9六个中位数均为正，仅Pair.120与random.059等柱值，没有负余弦比例/层别/误差 |
| 检索阈值.6 | Fig8直方图覆盖约.2到1，有低于.6样本；统计阶段/分数变换未解释 |
| 原QA/caption约束+自验证模板 | Fig11/12显示给图与类别联合产出caption/QA，没有展示原有QA/caption字段或自验证指令 |
| 1B GenEval .73→.79 | 计数.48→.44、颜色.90→.75，不能概括为全部组合能力改善 |
| 7B GenEval .79→.85 | 两对象.88→.75，JanusProR1总.86更高 |
| 相似度加权改善生成 | T6两规模GenEval .79/.85均不变，主要理解项改善 |
| BAGEL迁移 | PairUG SFT，证明范围为配对数据迁移，未检验PairGRPO RL |
| Lumina编辑结果 | 当前v3 add/replace/remove/style均高于原基座，旧笔记的不一致结论更正 |
| Acc与clippedGRPO | 发布reward软文本相似，loss无oldpolicy ratio/clip，不能声称已按正文完全复现 |

## 数学和损失计算

若0<s1<s2≤1，则sqrt(s2)−sqrt(s1)=(s2−s1)/(sqrt(s2)+sqrt(s1))；阈值.6以上分母>1，差值被压缩，比例sqrt(s2/s1)也更接近1。该设计可作为温和下调低分pair的启发式，表7的小幅理解增益不能证明更强的区分或普遍稳健性。对非零gU、gG及w>0，cos(wgU,wgG)=cos(gU,gG)，因此要把数据挑选的效果、不同pair加权的效果与单对梯度冲突处理分开。

[trainer实际实现](https://github.com/Haochen-Wang409/PairUni/blob/0097f4197c7c4b564ffefacb8cbf09b03b61e735/open_r1/trainer/grpo_trainer.py)先每任务reward组内减均值除std+1e-4，再乘sqrt(similarity)；aligned需要输入similarity=1。若在组内标准化之前把同一正权重乘所有reward，其作用将被标准化抵消，因此放置位置具有实际意义。当前实现使用exp(logp−logp.detach())乘advantage，没有保存oldpolicy概率或PPOclip；前向ratio恒1但反向有scorefunction梯度，不能误说没有学习信号。两模态按所有completion token共同归一，图像576token与文字答案长度成为隐式任务权重。

图像teacher forcing取最后577个hidden、去掉最后logit、前插dummy后移去首ID，再补零对齐整序列，首imagecode由最后prompt位置预测；这个实现不具备上一项CoRL公开切片的同一待核位移。CFG5采样与普通条件logps仍需要概率目标论证。理解reward采用SequenceMatcher和数字相对误差，MC单字答案可退化为0/1，但其他输出未必；不能将其统称严格二值Acc。

## 提示模板与数据制品

F11标题generation，实际输入image+class同时输出question/choices/answer/detail_prompt；F12标题understand，输入image同时生成同类四字段。正文§11把F11称理解→生成且声称有原QA约束，把F12称生成→理解且声称有caption约束，实际模板均未显式展示这些条件；也没有所声称自验证步骤。不能由正文的strictly语气推断合成标签已被可靠验证，需补实际API请求、校验流程和抽样准确率。

固定187项树中166文件，未见JSONL/parquet或权重文件；README模型/数据HF入口标comingsoon，示例引用仍为YourName/arxivXXXX/2024占位。全树路径未标出Lumina/BAGEL或clustering构建入口，所读启动、dataset仅加载相似度字段，未核到完整数据合成/检索流水线。README一个towel+zebra示例不在官方553测试提示，不足证明含GenEval1787类的全训练集无污染；也不足认定污染，需全体样本源ID/模板及实体去重。

## 对研究路线的约束

数据语义相近、同图注释补全、独立优势加权已是明确相关工作；后续想研究书写过程中的共享理解/生成收益，需要更细的事件与观测定义，并匹配数据量、奖励裁判、模态token归一和总算量。平方根加权、正余弦柱图或只提高综合分都不能直接支持严格笔顺协同。下一项继续L131 UniCorn，追引Orsta/DSR、UniRL/JanusProR1、合成数据去污染与梯度冲突研究，未独立精读的工作继续标队列。
