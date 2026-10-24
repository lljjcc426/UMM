# VisWorld-Eval：完整理论、比较条件与发布协议审查

第一百八十九批完成[U25](../reviews/U25.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/visworld_full_theory_comparability_and_release_protocol_audit_2026-10-25.json)。358目录（331论文／研究、27资源），294核心/299书面含未通过项；待完成核心深审37篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2601.19834v1)、[主源2](https://arxiv.org/html/2601.19834v1)、[主源3](https://arxiv.org/pdf/2601.19834v1)、[主源4](https://manchery.github.io/Reasoning-Visual-World/)、[主源5](https://github.com/thuml/Reasoning-Visual-World/tree/4ee920ca9b65bdee124bae8c36e336998243cdda)、[主源6](https://huggingface.co/datasets/thuml/VisWorld-Eval/tree/1ac6c2bd6e045510cc6f06b43831358ee9145063)、[主源7](https://datasets-server.huggingface.co/size?dataset=thuml%2FVisWorld-Eval)。

## 研究问题

统一多模态模型生成中间图像，何时能帮助物理/空间推理，何时仅增加错误与计算？以世界重建/模拟区分任务，对同一BAGEL底座的隐式、显式文字、交错图文CoT做任务级后训练比较。人类认知是动机，未有参与者/心理实验验证human-like认知机制。

## 现有不足

语言状态描述可能遗漏几何细节，部分视觉知识难从文字监督学习；但视觉生成也可能模糊、变色并积累状态错误。需把观察的信息性、预训练先验和生成保真度与推理能力分开。本文有明确负例：简单5×5迷宫显式图像无益，MMSI多类关系仍退化。

## 贡献

以MOMDP观测视角定义world reconstruction/simulation，将CoT拆成逻辑r与观测o，给KL误差分解/条件互信息界及迁移学习假设界；构造七任务VisWorld-Eval和三种CoT监督，用SFT/RL、训练样本量/难度/表示探针分析视觉收益。核心贡献是条件化的研究框架与受控任务证据；视觉优越性仍属假说，定理未证明视觉对文字的普遍信息排序。

## 输入、模块、输出与公式

Eq1有限视图→新视图，Eq2历史观测/动作→未来观测，Eq3 R=((r1,o1),…,(rH,oH))→A；implicit令o空、verbal输出矩阵/坐标/文字状态、visual输出中间图并继续读图。AppA先由modality-agnostic slice f抽状态、g按模态render，并假设各模态共用oracle逻辑过程和固定H。Eq4/9利用KL数据处理/链式法则，将答案KL上界拆为oracle分布下逻辑条件KL与观测条件KL之和，未提供free-running误差保证。Eq5/10条件熵差为非负CMI且受状态信息与任务所需信息上界；非负只说明oracle conditioning不增加熵，不能直接推出学习模型答案准确率提高。

## 模型结构

实验底座BAGEL-7B-MoT，文本自回归CE+视觉flow matching；本文未设计新的图像tokenizer/统一骨干。Eq6 CE含所有文字步骤/答案，加中间图速度MSE；表3权重1:10。原文z_t=t·o+(1−t)ε但MSE目标ε−o，与该线性插值正向导数o−ε符号相反，需要实际时间/速度/积分器约定说明，未发布训练实现所以仅记公式约定疑问。Eq7 GRPO只对文字token做ratio/clipping/advantage，视觉项是相对SFTref的速度MSE，文中称KL但未给生成分布KL等价或路径界；不把它直接当已证明的density KL。共享参数/上下文仍可影响图像，不等所有视觉参数被冻结；r_i是推理步骤，优势A才属reward估计。

## 数据分布与划分

T2训练/测试：fold2357/480、multi2000/480、ball2254/1024、maze8448/480、soko7715/480、cube2500/480、MMSI10661/522，总训练35935/测试3946（各task-specific训练集样本数相加）。fold网格3–8/1–4折、测试8/4，规则CoT+Gemini2.5Pro重写，文字为轮廓/孔形两矩阵；multiBlender/CLEVR3–6物/1–5操作、唯一颜色形状组合；ball点质量理想弹性镜面反射/4–8孔、测试至少一次反射，Seed1.6解释相邻帧。maze固定5×5，soko6–10单箱，最优搜索+随机绕行/碰墙反思，文字删渲染、implicit再mask坐标。cube3–5网格、双颜色，iso+两正交→新视图，潜在遮挡用第三色标注，文字字符矩阵，另测OOD6。MMSI训练通过visual-CoT+SFTBAGEL新视图工具后Gemini过滤重写。HF固定revision 1ac6c2bd6e045510cc6f06b43831358ee9145063七split计3946、schema6列；人工读各split首条文字/schema，未读图像字节，另结构化统计MMSI全部522条extra_info。实际六关系93/94/81/86/85/83，AppB1声称聚焦CamObj/CamReg却不符发布全部六类；主图只展示该两类，T5完整六类总体与实际样本权重相容。未称人工逐条深读3946题或验证全部GT。

## 指标与评价协议

七任务答案accuracy，T1overall5/7为task等权平均、不是按3946样本micro；MMSI内部T5按六类型样本权重可由四舍五入数近似复算34.7803/38.3736→34.8/38.4。官方verifier按任务不同：fold最后行整数、cube/MMSI最后行选项，解析失败转LM；multi非选项始终LM语义判；ball最后boxed精确字符串；maze归一坐标×512、像素线避墙/起终点邻近且wall_judge==1才成功；soko从bbox方向模拟单箱终点==goal。LMfallback固定prompt语义等价，模型/端点留TODO，full_resp精确等于Yes、不strip，未给历史judge版本/温度/校准。故不能把所有答案评分写成纯确定规则。F6b world-model fidelity：文字string pattern、视觉Gemini3Pro图像判，仅形状忽略颜色；模型checkpoint为SFT而同图答案accuracy为RL，不能据此证明同模型fidelity→accuracy因果。F6c两层4096MLP预测x/y各5分类，报坐标均值，随机机会20%（非联合坐标4%）。

## 对比方法

同BAGEL初始权重的implicit/verbal/visual task-specific SFT；ball/multi显式verbal因坐标算术困难被省略，仅implicit作对照，未提供最优结构化状态/工具执行基线。Qwen2.5VL与BAGEL共享Qwen2.5LM来源但完整视觉/预训练不同，F7只说明几个task的SFT文字分数接近，不能排除所有先验/预算混杂。T1七zero-shot VLM含Gemini3Flash/Pro、Seed1.8、GPT5.1、o3、Qwen3VL8BThinking、BAGEL，无中间图生成；与图4任务后训练模型分开报告，不当同训练预算排名。没有同总token/NFE/walltime、图像数量/分辨率与等信息完整文字状态的比较。

## 实验条件和发布边界

SFT8GPU/8rank，AdamW3e−5恒定lr、warm200、4000steps、每rank32K，CE:MSE1:10；genresolution表为fold/cube(256,1024)、multi(240,1024)、其余(256,512)，understanding(224,980)，不擅自解释tuple精确语义。RL64GPU/verl，lr1e−5、batch128、mini32、group16，视觉ref系数.1文字KL0。QwenSFTLLaMAFactory、RLverl。未披精确GPU型号/总GPUh、各CoT训练token/图像NFE/CFG/延迟、推理采样版本seed/CI。F6a500/1000训练子集与全2357相同4000steps意味着重复/epochs不同，4×sample efficiency仅该fold任务设定，非4×计算节省。官方repo固定4ee920ca9b65bdee124bae8c36e336998243cdda递归10entries/8blobs，核7个textblob（README/gitignore/eval5py），asset概念图非源码未下载；只含评测，未含SFT/RL、三类CoT训练集、后训练checkpoint、probe/fidelity实现。evaluate.py GET_CLINET/GET_RESPONSE/API为None，load_dataset("VisWorld-Eval",split="ballgame")固定且未namespaced，--task只改评分/输出，跨任务需手工改数据加载；README指定thuml数据。model_apis.py端点/模型TODO、max_tokens32768，无显式温度/seed，OpenAI兼容payload用input_image/input_text需后端适配。根目录未有license文件，HFcard未显式license字段，不从公开下载推断任意授权。未运行API/模型/训练。

## 主结果

F4 implicit/verbal/visual分别：fold21.1/27.4/39.2、multi40.0/缺/66.6、ball40.7/缺/57.6、cube63.7/60.2/76.8、MMSICamObj46.5/缺/60.9、CamReg37.3/缺/54.4、maze77.0/73.1/70.6、soko29.6/36.8/39.3。视觉对implicit提升fold18.1/multi26.6/ball16.9/cube13.1，但maze下降6.4，soko仅比verbal高2.5且无CI。T5完整MMSI implicit/visual：CamCam33.1/29.6、ObjObj31.2/29.5、RegReg31.8/31.6、CamObj46.5/60.9、ObjReg29.1/25.8、CamReg37.3/54.4，六类四降，总体34.8→38.4。T1zero-shot taskmacro5/7：Flash50/60.5、Pro49.8/53.2、Seed38.3/49.1、GPT40.8/38.2、o3 37.6/32、Qwen25.4/18.9、BAGEL23.2/16.6；全部单项见结构化表。项目页posttrainedoverall55.7/55.5为视觉行任务均值，含MMSI38.4，非joint模型全任务统一训练能力。

## 消融及进一步实验

F6a fold500/1000/full样本、Normal/Hard对比，视觉样本效率更好但单任务、相同步数与额外图像监督；F6b cube3–6难度视觉fidelity更高但文字格式判/视觉LM判、SFTfidelity/RLaccuracy错位且忽略颜色。F6c迷宫masked坐标MLP probe：随机约.2、PT中层约.55、SFT中层约.97（图读近似），8:2按不同CoT分，未明确maze identity独立切分；可解码不等因果使用世界状态，未做干预或低容量/跨任务probe。F7Qwenimplicit/verbal fold21.5/28.8、multi37.5/缺、cube60.0/58.8，BAGEL21.1/27.4、40.0/缺、63.7/60.2。F8 RL三task所有CoT多有提升，视觉差距仍在；曲线不同结束步数/成本，未量化统一预算收敛或统计显著性，未把图上近似值当精确表。F9/10–14成功与训练选例，F15视觉仍左右方向错，F16正确中间图伴随错误文字、两种CoT均最终−1，F17b错误形状可仍选正确答案、c颜色推断错误、d细形状缺失仍答案正确；说明accuracy与中间statefidelity需分开。F17caption误称paperfold，按实际Cube内容记录。

## 局限与疑问

理论：Thm1只给上界，加入观测既可能降低逻辑KL也新增生成KL；未证明上界紧或视觉风险必低。Thm2依赖oracle共同逻辑、deterministic observation/条件独立，未证明图像必比充分文字信息更多。Cor1全观察+确定转移下CMI为0，有限模型仍可能从外部工作区/先验获益，不能外推任何确定环境显式图无用。同输入/固定参数自产图不等外部新测量，有限算力表示优势需另验证。迁移界：boundedloss[0,1]、总体最优、P局部二次增长区域包含Q最优、球内ERM/UC；Assumption2仅要求θ,θ′∈Θr局部Lipschitz，但Thm5证明在Q最优位于球外时把Lipschitz用于θr与θQ*跨球两点，假设范围不够，需扩展至该端点/连接区域；Thm6继承此bias项前提。Rademacher项归一未定义，UC被直接假设，不称已验证标准rate；无TV/复杂度实测或视觉/文字分布排序。实验：同底座不能消除模态特有oracle监督、序列长度/图像计算与teacher筛选差异；两个任务无verbalWM、F6metric/checkpoint不齐、MMSI四类下降，限制“superiority”。发布代码是可改造评测骨架，未能据此复现训练/图4等历史分数，未据stub推断论文实际实验使用错误数据。

## 预期优势条件

当任务状态有难以稳定文字化的连续几何/反射/视角变换，且视觉生成先验/保真度足够时，显式图可提供适合有限计算模型的状态工作区；简单离散可完整编码状态未必获益。迁移书写/素描可把前缀墨迹与下一笔状态作为o，检查拓扑、细线和时序，比较同信息轨迹/符号状态与渲染图；本文没有笔轨迹/接触/书写执行证据，高维图的信息量和图像答案准确率不能代替笔顺可执行性。

## 可证伪实验

Q1收益来自视觉表示还是额外oracle信息/预算：同任务实例/完整状态GT/teacher与初始权重，对齐训练token/steps与推理总NFE/时间，把同一状态编码成完整符号矩阵/自然语言/渲染图，加入文字+执行器、随机/错误/GT中间图、无回读图与caption条件；各模态用同一结构解析/独立人校准judge，在同SFT及同RLcheckpoint分别测答案与中间state、逐步错误/CI，若等信息/等成本后优势消失，应缩小视觉优越主张。Q2可解码状态是否用于推理及何时失败：按maze身份/拓扑独立划probe集，比较低容量probe并对表示做状态一致干预、交换/遮盖图与坐标，检验下游决策是否随状态改变；扩到大maze/多箱/遮挡/OODcube与全部六MMSI关系，独立报颜色/拓扑和方向。修正Thm5的Lipschitz范围并区分oracle条件熵与自生成观察的有限计算增益；书写加精确细笔/prefix合法增墨/DTW笔序，同成本比较符号轨迹与图像。均建议，未执行模型实验。

## 论文组织与Claim学习

世界重建/模拟→三种CoT→理论tradeoff→七任务→负例与probe，组织有清楚研究问题；作者公开保留maze负例、视觉幻觉/错色和全MMSI表，值得学习。理论标题应显式区分一般KL/CMI性质、额外假设与视觉specific假说；证明中局部假设需覆盖所有用到的点。结果应同时展示六关系、metric/checkpoint/训练预算/teacher监督，避免只用两类成功主图概括整体。源码范围、完整数据子类与paper描述要对齐；准确最终答案和忠实推理分开验收。

## 实际阅读范围

完整2601.19834v1 PDF34页/HTML正文§1–6、AppA1/A2全部证明与B1–3/C1–2（HTML§7–9），Eq1–15、6个Theorem编号（3/4为1/2重述）、3Lemma/2Assumption/1Corollary，T1–5全部行、F1–17全部视觉。固定repo10tree/8blob，审7textblob含5个evalpy；HFschema/七split3946计数与7首条文字、MMSI全522条metadata子类分布，未读全部图片或全部3946题语义。项目页/README核发布及聚合；OpenReview页面验证/API403未核接收。核心三遍/五项书面验收完成，未模型推理、judgeAPI、训练、probe或历史原始分数复现。

## 证明范围和数据范围的独立核对

Thm5在Q最优点位于半径r球外时，比较边界投影θr与θQ*的风险差。Assumption2只在球内两点给Lipschitz，不能直接覆盖球外端点。扩展假设至相关连接区域后，论文的投影距离界才得到所用风险差控制。该问题限定于给定证明与假设范围，不构成否定实验分数的证据。

HF当前固定revision的MMSI全部522条metadata含CamCam93、ObjObj94、RegReg81、CamObj86、ObjReg85、CamReg83。由表5四舍五入子类分数及这些计数复算隐式34.7803、视觉38.3736，与34.8/38.4相容。正文称聚焦CamObj/CamReg需要与实际全六类发布区分；本批未下载这些图片，也未声称逐题验证GT。

评测代码审查定位到任务入口/parse/fallback范围，并未运行任何模型或API，也未将官方未发布的训练实现自行补成可复现实验。追引MOMDP/mental models、BAGEL、dual coding、SpatialViz/RBenchV/MMSI/ZebraCoT及implicitworldmodel相关研究，本文的条件信息理论不能直接外推笔顺控制。
