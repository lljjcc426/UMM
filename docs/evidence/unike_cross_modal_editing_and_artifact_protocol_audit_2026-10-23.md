# UniKE：跨模态知识编辑、条件瓶颈与发布制品协议审查

第一百五十四批完成[L141](../reviews/L141.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/unike_cross_modal_editing_and_artifact_protocol_audit_2026-10-23.json)。357目录（330论文／研究、27资源），263核心/266书面含未通过项；未确认核心67论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://proceedings.mlr.press/v306/gao26ag.html)、[主源2](https://raw.githubusercontent.com/mlresearch/v306/main/assets/gao26ag/gao26ag.pdf)、[主源3](https://arxiv.org/abs/2606.00477)、[主源4](https://arxiv.org/html/2606.00477v1)、[主源5](https://github.com/gxx27/UniKE/tree/f8331cbc43199e1fc7aec0d3b1db553d46739abd)、[主源6](https://huggingface.co/datasets/gxx27/UniKE/tree/2345d5d4d000640d22ca3f180aae06bbaf3c0fd3)。

## 研究问题

仅编辑统一多模态模型语言骨干的事实，能否迁移到答案中性的静态图像生成？文字回忆、显式推理和视觉实现在哪些环节脱节？UniKE首先是跨模态知识编辑基准与协议，附推理增强及机制诊断，无规范笔顺/书写视频生成。

## 现有不足

既有编辑多评价文字或视觉输入后的文字问答，文字侧成功不保证事实经条件接口进入图像。直接提示不显露新答案可避免把提示跟随当参数知识迁移；但首token、目标字符串包含和答案已知裁判分别只是有限代理，不能互替完整事实、绑定正确性或动态执行。

## 贡献

构造属性四stage与可视关系编辑基准，三UMM×三编辑器比较Direct/Reasoning-Augmented；软化AlphaEdit使其适配BLIP3o/OmniGen2，测语言状态和生成条件漂移，以Ovis投影SVD和五块传播诊断接口。基准/协议、编辑器适配、测试时推理及机制假设需分别评价；当前制品存在下述设置与统计边界。

## 输入、模块、输出与公式

输入(q,y,y′,pimg,tvis,qvqa)，在MLP中层累积MEMIT/PMET/AlphaEdit编辑→测q后的目标首token→Direct按pimg生成，ReasonAug先由已编辑模型自己回忆/描述再生成→Qwen3VL目标已知二值裁判。Eq1实例、Eq2–4三指标；Eq5–7状态cos/Frobenius及条件均值漂移；Eq8–15编辑约束、软投影及协方差正则；Eq16用右奇异向量子空间测编辑能量。正文ReasonAug说同prompt追加推理；生成脚本实际优先直接用reasoning_output、空时才回退pimg；诊断reasoning_conditioning.py却拼推理+原prompt，三者需原始运行配置对齐。

## 模型结构

Ovis-U1（语言Qwen3-1.7B、整体约3B）末两层concat4096→冻结linear1536→生成端；BLIP3o4B Qwen2.5VL2048经64learned queries；OmniGen2 Qwen2.5VL2048完整条件序列。Ovis编辑层4–8，另两者6–10。论文§4.6/T5统一写DiT，但公开BLIP3o generate_images.py用UNet2DConditionModel/EulerDiscreteScheduler，需明确正式实验对应实现；不能把三者全部视为同构DiT。

## 数据分布与划分

公开HF固定版本2971编辑记录=964属性+2007关系，实际2768种subject字面串；5535stage实例=3528属性+2007关系。属性material212/color287/shape198/pattern58/size209，S1–4数量959/874/858/837；Gemini3.0Flash温度1生成/过滤可视性，四stage为原子、场景、多实体、衍生使用。关系location845/occupation531/creator328/affiliation303，CounterFact/MQuAKE规则及Gemini可视性筛选/代理视觉目标。全JSON审计发现5条无S1，编辑加载器排除后2966=959+2007，保留stage总5526；另两组相同S1 prompt存在矛盾目标，顺序累积需消解规则。stage难度比较有可用样本组成变化；尺寸比较后续stage目标可变为实体名，不能都按相同形容词判。

## 指标与评价协议

Eff仅目标答案首token与argmax下一token相同，非完整事实成功；Reason为归一目标字符串包含（代码对size另有辅助匹配），非正确绑定/肯定事实保证。VQA由Qwen3-VL-235B-A22B-Instruct读图、问题、目标criterion给matches_target，未核人标一致性。当前代码长边缩512/JPEG88，出错/skipped不进VQA分母，畸形JSON还可用true与matches字串回退，需报告覆盖率和解析错误。附录裁判温度.1，代码0；两者均不能独立保证绝对确定。未给主结果CI/多seed重复。VQA/Eff边际比不等P(VQA成功|Eff成功)，主表不能证明已成功编辑子集的精确迁移率。

## 对比方法

Ovis-U1/BLIP3o4B/OmniGen2×MEMIT/PMET/AlphaEdit，Direct与ReasonAug；AlphaEdit在后两模型的软化版带星号。属性四stage、PMET100例漂移、Ovis三编辑器100例SVD、AlphaEdit100例t=.5五块传播。缺完整未编辑基准量化、等长中性/错误/oracle caption、实际生成路径的对齐条件、图像分支直接编辑及同预算原版/软化版locality对比。

## 实验条件和发布边界

九份JSON已读：共同value梯度25步/lr.1/weightdecay.001/KL.0625/clamp4/mom2权重15000，Wikipedia100K float32二阶矩；Ovis v_loss_layer27、另两者35。Alpha L2=10/null阈.02，Ovisα1/ε0，BLIPα.7/ε.01/max更新Frob比.5，Omniα.6/ε.015/比.4；代码比值基准INITIAL_WEIGHT_NORMS，论文文字似当前W，需对齐。run_edit默认100条每块，evaluate.py累积更新并只在最终全编辑模型上评价；不是每块重置。代码生图默认seed42/1024²/50步：OvisCFG5，Omni文本CFG4/图CFG2，BLIPUNet硬编码CFG3/50步；Reason vLLM greedy/temp0/top_p1/top_k−1/maxnew512/seed42/maxlen4096。README≥48GB是运行要求，非已确认实验硬件；torch2.4/Py3.10及bf16等工程设置不补成正式训练日志。正式完整硬件/耗时/多seed和逐run manifest未提供。官方GH固定f8331cbc43199e1fc7aec0d3b1db553d46739abd目录221成员，下载35选择性源码/配置文件，阅读本文涉及函数；HF固定2345d5d4d000640d22ca3f180aae06bbaf3c0fd3全文JSON/卡。未下载权重/缓存矩阵，未执行作者脚本或复现。

## 主结果

T3各模型/编辑器总体Eff；VQA Direct→ReasonAug；Reason：Ovis MEMIT59.84；8.70→24.41；43.59，PMET72.18；9.71→28.32；53.57，Alpha64.73；7.42→20.67；44.47。BLIP MEMIT68.88；15.17→16.32；45.52，PMET76.30；18.51→19.29；53.20，Alpha*77.88；16.12→17.33；61.67。Omni MEMIT58.29；8.73→12.17；44.64，PMET76.20；11.43→16.01；51.96，Alpha*76.37；11.50→17.90；58.93。OvisPMET总体增18.61pp符合摘要18.6；约92%是OmniAlpha关系Eff91.93%，非总体。每组合总体VQA提高，但BLIPPMET关系20.98→20.78下降.20pp，不能声称全部子域提高。OvisPMET主表可由959属性/2007关系重构：Eff529/959、1612/2007、总2141/2966=72.18%；VQA83/959、205/2007、总288/2966=9.71%，仅为整数一致性分析，不替代正式原始run证据。

## 消融及进一步实验

T4 PMET100例按语言cos漂移/语言相对Frob/Direct条件/Reason条件：Ovis.003/.078/.018/.154，BLIP.139/.527/.031/.064，Omni.038/.262/.018/.092；条件漂移放大8.56/2.06/5.11倍，prompt内容/长度不同，不能当语义因果。T6投影1536×4096，k1/10/100/500/1000/1536保留.01/.18/1.99/10.62/21.60/34.82%，各向同性参照.02/.24/2.44/12.21/24.41/37.50%。T7 Alpha/MEMIT/PMET的原δ范数2810.5/4134.8/2930.6、投影范数585.0/973.3/669.6、子空间ρ34.2/31.9/34.8%；ρ是行空间投影比例，非含Σ的实际Wδ能量比例。代码原δ用全序列Frob、投影用均值δ，范数不可直接相比。T8 Alpha100例t=.5：txt-in7273/1.000，block0–4 7243/.996、7238/.995、7187/.988、7225/.993、7398/1.017；relative实际以7273为分母，列名RelativeBlock0需核。五块范数近常数不能证明整个生成器线性或唯一瓶颈；传播脚本存在捕获块异常后pass/保留原状态的路径，需成功forward日志，不能据此断言正式表运行失败。F5分stage归一不同可用子集；F6所标Stage2孔雀花园对应当前HF row12 stage3，需版本映射。

## 局限与疑问

作者归因生成条件接口、有限架构/编辑器/可视知识，未覆盖视频/笔顺。独立审查：(1) 2971记录与编辑2966分母、5无S1样本后续生成是否仍参与、两组矛盾prompt须给run级名单/冲突规则；原JSON审计有证据，但其对整体结果影响未量化。(2) 首token/字符串及目标已知VQA不能代替完整知识、实体绑定、细字/标志准确；stage不齐、错误排除和边际分数妨碍因果解释。(3) ReasonAug原prompt保留方式在正文、生图与诊断代码不一致；BLIPUNet与DiT描述不一致，温度亦不同。(4) SVD34%依赖实际δ方向，不是维度必然上限；行空间能量与真实W范数区别、全序列/均值δ统计单位需统一。(5) 五块norm保持不证明线性，异常吞掉可伪造稳定性，原始日志未得；诊断raw-token conditioning与真实chat/blank-image生成路径尚未同一化，工具limit取前100非随机抽样。(6) 无主表多seed CI、条件成功联合表、完整locality/未编辑保留及多编辑冲突分析；软化约束提高编辑能力的代价待测。未执行模型，代码风险不能写成正式实验已发生错误。

## 预期优势条件

当编辑确实写入可视事实、模型可准确回忆、条件接口通常漏传该事实而生成分支有相应表达能力时，显式回忆有望提高静态视觉符合率。若回忆错误、目标不可视、标志细节超出生成器能力或严格动态事件受限，较大条件漂移不保证成功。写作/笔顺研究可迁移“文字知道→渲染知道→事件正确”分层检验，但本论文未验证这些动态能力。

## 可证伪实验

冻结版本公布2966/2971逐case/stage集合、冲突去重/最终真值与所有错误分母；重算完整答案/事实绑定并给Eff×VQA联合表。未编辑/仅prompt/正确与错误回忆/oracle/等长中性caption在同seed同预算配对；统一原prompt拼接和真实生成接口，补人标/独立OCR/标志裁判。主表按主体聚类CI和多seed、stage共同可用子集。分别改变投影/子空间方向/生成分支，以δ同一统计单位和实际Wδ验证机制；强制每块forward成功、匹配latent/timestep/conditioning，测输出对定向干预响应。原/软Alpha同预算测locality与累积保持、冲突请求单独分层。严格书写再测离散事件顺序、细笔RGB可观测与执行约束，均为方案未运行。

## 论文组织与Claim学习

用可观察的文字—图像脱节提出任务，先界定答案中性测试，再拆文字编辑/回忆/视觉验证、以架构接口诊断解释，Introduction与Method主线清楚。学习分指标分阶段呈现；Claim须把约92%的关系首token与总体视觉分数标明口径，较大漂移是诊断证据，不能等同唯一因果。Limitations应写数据缺stage/冲突、解析分母、协议实现差异和人标缺口；正式图表与发布版本需可回溯。

## 实际阅读范围

正式PMLR24页2816417bytes，Abstract/§1–5全部研究正文、AppA–F全部研究内容/提示、Eq1–16/T1–8/F1–6及全部图注；实际看p2/3/4/5/6/7/8/15/16/17共10页，参考p10–12仅定位未逐篇读。arXiv v1指定部分与正式版对照。官方GH固定commit目录221成员、下载35选择性文件；读数据加载/九配置/evaluate累积与eff/生图/Reason与judge关键函数、SVD/DiT传播/condition提取/推理条件分解，非221成员逐行读；官方HF固定版本完整2971行JSON及模型卡。下载元数据和源码不计训练执行；无权重、作者模型推理或独立复现。

## 数据制品静态审计

本节仅使用发布JSON的标准库解析，未执行作者模型代码。

| 对象 | 原始发布 | 编辑加载器要求S1后 |
| --- | ---: | ---: |
| 编辑记录 | 2971 | 2966 |
| 属性记录 | 964 | 959 |
| 关系记录 | 2007 | 2007 |
| S1总实例 | 2966 | 2966 |
| S2属性 | 874 | 872 |
| S3属性 | 858 | 856 |
| S4属性 | 837 | 832 |
| 全stage实例 | 5535 | 5526 |

无S1的0基原JSON索引/主体为210 Red Blood Cell、521 Teardrop、2276 Bridge、2929 Pear、2938 Santa Suit；后续生成脚本直接枚举原JSON，需明确是否对这五条同样排除。2971是编辑记录数，实际subject字面串2768种；重复主体的不同属性/关系可合理存在，不能一概当错误重复。

两组精确prompt冲突：170/2492的“iOS 8 was developed by”分别目标Sega/Microsoft；295/1800的“Triple H is employed by”分别Valve Corporation/BBC。默认代码累积全部编辑后再评价；相同确定性下一token提示不能同时符合两种不同目标，应定义冲突消解/有序最终真值。这两组不足以解释整体低视觉成功率。

## 条件诊断与实际生成的区别

`interpretability/reasoning_conditioning.py:51`构造“推理+Based on the above, generate an image:+原prompt”；`scripts/generate_images.py:500`直接优先取reasoning_output。因此诊断表的prompt路径与公开生成脚本尚未相同化。`interpretability/utils.py`又从原tokenizer文本提取条件，而Ovis实际生成有chat/空图等包装。需要正式命令及逐case输出确认其对应关系。

`bottleneck_analysis.py`对原δ用全序列Frob、投影用均值δ；`dit_propagation.py`使用合成latent、t=.5、缺失/省略位置编码路径及异常后pass的处理。未取得正式运行日志，所述均为实现风险和统计单位差异，不能写成作者正式实验已经失败。

## 理论边界

设W=UΣVᵀ，论文ρ(k)=||V_kᵀδ||²/||δ||²只反映δ在右奇异子空间中的比例；实际||Wδ||²=Σ_j σ_j²(v_jᵀδ)²还依赖奇异值。1536/4096=37.5%只在各向同性方向等条件下给期望参照，无法推出任意编辑至少丢失62.5%。将δ对齐行空间即可改变保留率。序列Frob与均值δ也应分开报告。

令A为完整文字事实成功、B为图像事实成功，应直接统计P(B|A)及联合混淆表；分别报告的P(A)、P(B)不能恢复该条件概率，P(B)/P(A)只有额外假设B⊆A时才相等。现有Eff本身仅是首token代理，还需先改进A的定义。

## 五个关键问题与写作学习

1. 问题：已编辑语言知识能否在答案中性提示下进入静态生成？
2. 难点：回忆、条件接口、图像表达及裁判均可能失效，既有文字编辑分数未区分这些环节。
3. 针对不足：用UniKE、Direct/ReasonAug、软Alpha和接口探针逐层测量；这四项的证据均限于本文静态任务，各自单独评估。
4. 优势条件：可视事实已被完整写入并准确回忆，生成器具备表达能力，且原条件未带出事实时，显式描述可能提高VQA；需排除长度/内容混杂。
5. 验证：同版本同样本同seed配对、完整事实联合表、oracle/错误/中性提示、接口干预、强制forward成功日志、locality与多编辑保持及人标校准。

Introduction把“文字—图像脱节”变为可观察任务；Method依次定义数据、协议、编辑适配、诊断；实验将主性能、stage及机制分层。Claim须保留子域/分母、首token代理、边际与条件概率、相关与因果的边界。图6阶段标记与当前HF数据不对应应交代发布版本；Limitations应同时说明数据/评价与代码对应缺口。

## 追引和适用范围

TIME/ReFACT/Diff-QuickFix/TMKE与ROME/MEMIT/AlphaEdit/MQuAKE/ZsRE进入去重追引队列，本文引用或定向核查不计它们已独立精读。向严格书写的迁移只形成分层检验思路：文字回忆、终图字符、RGB笔画事件和实际执行分别设oracle/裁判；动态有效性尚待实验。
