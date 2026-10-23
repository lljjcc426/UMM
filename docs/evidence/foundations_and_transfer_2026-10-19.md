# 生成理论、视频与绘画：机制和实验迁移

本页连接[逐篇原文笔记](../reviews/README.md)与本项目的可检验问题。它不把已阅读的相关章节计为全文三遍验收，也不把通用生成性能视为规范书写能力。训练、推理与复现均未在本批运行。

## 研究范围及任务边界

| 研究层 | 本轮覆盖 | 与书写过程的连接 | 不能直接推出的结论 |
| --- | --- | --- | --- |
| 概率生成基础 | GAN、VAE、DDPM、score-SDE | 分布建模、轨迹/视频压缩、可用训练目标 | 图像质量好就具有正确笔顺 |
| 连续输送与快速采样 | FM、Rectified Flow、Consistency、DPM-Solver、MeanFlows | 路径、参数化、数值误差与少步生成 | 少NFE就减少视频帧或自动保留事件 |
| 表示与骨干 | LDM、DiT、CogVideoX、Wan | 空间/时间压缩、条件接口、时空token | 重建PSNR高就保留每一次短时落笔 |
| 序列训练 | Video Diffusion、AnimateDiff、Diffusion Forcing、Self Forcing | 图像先验、时间模块、训练/推理分布差异 | 平滑、长滚动就能准确执行指定动作 |
| 矢量/动作绘画 | sketch-rnn、Learning to Paint、Paint Transformer、StrokeFusion | 显式笔状态、可执行笔触、局部与全局表示 | 一种重绘策略等于原艺术家真实过程 |
| 视觉先验优化 | CLIPasso、DiffSketcher、Dynamic Typography | 可微渲染、语义/几何损失、单例优化 | 优化迭代可作为真实作画时间 |
| 静态与动态文字 | DP-Font、AnyText2、KineTy等 | 字形结构、文字可读性、动态排版 | 字形正确、整体文字运动等于逐笔形成 |
| 适配与效率 | LoRA、QLoRA、DoRA、rsLoRA | 训练参数/存储、量化误差、有效更新尺度 | 语言任务最佳配置直接适合视频 |
| 统一多模态 | Chameleon、Emu3、Janus/Pro、Transfusion、Show-o、U17/U18 | 表示需求、共享/分离计算、任务迁移 | 单模型支持双任务就发生正向协同 |
| 评价 | FVD、VBench、VidScribe、Calligraphy Bench | 通用质量、文字质量、工具动作与事件指标 | 单个总分覆盖真实执行与严格规范 |

基础条目为G001–G032；已存在的UMM和书写工作继续沿用原编号，避免重复计数。

## 公式究竟负责什么

以下公式用于解释作用；时间方向、参数化及记号在使用代码前须与原文对应。

**VAE（[G029](../reviews/G029.md)）**：

`ELBO = E_q[log pθ(x|z)] − KL(qφ(z|x) || p(z))`，`z=μφ(x)+σφ(x)⊙ε`。

第一项鼓励给定潜表示的重建，第二项约束潜后验与先验；重参数化让梯度通过随机变量的可微变换。轨迹VAE的抬笔状态、视频VAE的短时事件可能在压缩时丢失，须在生成器之前测重建上限。降低KL可改善重建，却可能恶化从先验采样，不能用一个重建指标替代两种目标。

**DDPM（[G001](../reviews/G001.md)）**：

`x_t=√ᾱ_t x_0+√(1−ᾱ_t)ε`，训练`E||ε−εθ(x_t,t,c)||²`。

网络学习噪声预测，逆过程把噪声转为样本。这里的`t`是噪声尺度；视频内部还有帧时间`τ`。两者是不同轴。不能将50次去噪当成50个笔画事件。

**score-SDE（[G002](../reviews/G002.md)）**：正向`dx=f dt+g dW`；逆向过程的漂移包含`f−g²∇log p_t`，并按逆时间积分；probability-flow ODE中该项系数为`1/2`。推导和实现都要同时明确积分方向。综述中的公式同样需要回查原始论文，不能因为是高水平期刊便免于核对。

**Flow Matching（[G005](../reviews/G005.md)）**：回归可采样条件路径的速度，得到边缘速度目标的相同梯度。直线路径`x_t=(1−t)x_0+t x_1`对应条件速度`x_1−x_0`，但条件路径直线不保证拟合后所有边缘流线直，更不自动构成全局最优运输。Rectified Flow的reflow进一步调整端点耦合，理想性质和有限训练经验须分别表述。

**一致性与平均速度**：Consistency学习同一概率流轨迹上的共同端点；MeanFlows学习区间平均速度，利用包含导数的identity训练。两者都可追求少步，但监督目标、教师依赖、训练成本不同。1NFE只计网络评估，不能与“一个视频帧”“一次笔尖控制”相互换算。

**GAN（[G028](../reviews/G028.md)）**：理想判别器与无限容量下的分布均衡结论，不能推出有限网络交替梯度一定收敛。视频对抗蒸馏需要另查模式覆盖、长尾文字和多种训练种子。

**CFG（[G026](../reviews/G026.md)）**：可统一记作`ε̂=ε_uncond+s(ε_cond−ε_uncond)`。有的论文用`s=1+w`，抄参数时先换算；条件/空条件预测的计算也要计入。强引导可能提升对齐并损害多样性，需展示曲线。

**LoRA/rsLoRA/DoRA（[G018](../reviews/G018.md)、[G020](../reviews/G020.md)、[G021](../reviews/G021.md)）**：`W=W0+γBA`；普通LoRA常用`γ=α/r`，rsLoRA用`α/√r`，DoRA进一步分解方向与模长。改变rank也改变更新尺度，不能把同alpha不同rank的结果全部解释成容量差异。QLoRA的NF4是基础权重存储格式，计算精度、激活内存和optimizer峰值仍须分别记录。

## 直接影响结论的原文发现

| 工作 | 复核发现 | 对本项目的约束 |
| --- | --- | --- |
| DP-Font | PDF Table3的PSNR标↓；Table2的CFG=.8 FID22.19优于=.6的22.34 | 不声称PSNR改善或所有指标都以.6最佳；静态笔顺条件不验证过程 |
| OLHWG | 同表SDT在部分几何/内容/风格指标更强 | 以方法分组和条件解释优势，避免写总冠军 |
| DiffInk | Table1速度58.47与正文58.82不一致；基线还接入统一布局 | 保留冲突，选择表值并注明；不给布局条件不同的方法直接排序 |
| Moyun | 原始/加工数据规模叙述不同，表中IoU标↓ | 数据口径与IoU定义未清楚前不据此判优 |
| VideoSketcher | 全模型最终分类Top1 .82低于naive Wan .92；序列偏好含Neither | 最终物体辨识与作画次序分开；偏好比例不称严格笔顺率 |
| Paint Transformer | 像素误差有RL基线更优，速度优势更明显 | 精确描述质量—效率折中 |
| Chameleon | tokenizer重建密集文字存在限制；few-shot/SFT各异 | 先检查文字表示瓶颈与比较条件 |
| Janus | 联合与单任务在不同理解指标有升有降 | 不把结构解耦、预训练先验和任务协同混为一个因果结论 |
| Transfusion | 双向注意力对linear编码器FID61.3→20.3，对U-Net16.8→16.7 | 结构贡献依赖外围模块；5K消融FID与30K主评估分开 |
| U17/U18 | 协同依赖任务/架构，存在负迁移、选样/检测覆盖与预训练混杂 | 共享收益需要匹配训练、数据、检测失败率和外部pipeline |
| FVD/VBench | 样本量、特征、帧采样影响FVD；高平滑可能对应低动态 | 通用视频指标与笔画事件指标并列，先做受控扰动校准 |

## 五问驱动的研究假设

下面是本仓库推导的实验，不是已发表的新颖性结论；每一项都要继续追引。

| 具体不足 | 预期优势的任务与分布 | 必须包含的对照 | 支持或推翻的证据 |
| --- | --- | --- | --- |
| 时间压缩遗漏短笔画 | 极短事件、相邻交叉笔画、小字 | 同生成器不同VAE，先做GT重建 | 事件召回/边界误差；若重建已经丢失，生成头不能独自解决 |
| 静态字形监督不区分历史 | 同终态、不同顺序/方向的视频 | 末帧复制、合法/非法排列、规则SVG | RGB观察器对事件变化敏感，且与人工事件标注一致 |
| 历史误差累积 | 长字串、错误前缀续写 | teacher forcing、独立token噪声、self rollout | 按长度/错误类型报告条件成功率和漂移曲线 |
| 共享模型负迁移 | 需要检查已写过程并修正下一笔 | 专用理解/生成、外部planner、共享/分离路径 | 等数据/active参数/总计算下联合成功率；单任务收益不能替代 |
| 图像奖励忽略执行 | 同终态的多种动作轨迹 | 神经绘画、轨迹扩散、规则渲染、原生视频 | 实际落笔/抬笔与视觉出现一致性，真实工具回放 |
| 高秩适配未有效学习 | 小数据跨字体/书写者适配 | alpha/r、alpha/√r、初始更新尺度匹配 | 梯度/验证损失/事件精度，同时记忆与泛化均测 |
| 量化损伤细字/时间 | 低显存部署、长序列 | BF16-LoRA与NF4-QLoRA相同adapter | 同质量门槛显存/时间和错笔分布；记录预处理/解码成本 |
| 通用裁判对笔顺失明 | 未见字体、语言规范及跨地区字形 | 独立检测器、人工、工具动作真值 | 报告漏检、拒判、条件准确率和全体覆盖率，禁止静默删失败样本 |

所有方案至少按字符/书写者/字体/规范与数据源拆分，避免同字形或同模板泄漏；验证集选参数，测试集锁定。多个合法序列用明确的可接受集合或偏序表示；书写规范与数据中实际发生的历史分别评价。

## 学习研究组织方式

Introduction应按应用/任务→可测失败→现有机制为何不足→有条件假设→本文贡献展开。Method先定义输入、输出和监督，再画出数据流，随后解释每一模块及核心公式。没有训练数据、条件接口、目标函数和推理协议的框架名不构成完整方法。

实验围绕假设组织：主比较回答有没有收益，消融回答来源，分布外划分回答适用边界，失败案例回答什么未解决，计算账回答是否值得。只删除模块会同时改变参数量和计算，必要时补等容量替代。评价器本身先用已知正反例验证，避免以不敏感指标证实过程正确。

Claim写成“在指定数据/输入/预算/指标中，相比明确对照提高某能力”；Limitations分别写数据覆盖、观测不可辨识、上游误差、计算代价和未验证任务。发现局限以后先检索已有解决方法，再谈选题。

## 知识盲区与补读清单

| 概念 | 当前掌握/未完成处 | 对应原始阅读与验收 |
| --- | --- | --- |
| ELBO与重参数化 | 可解释目标作用；尚未对所有轨迹VAE逐式核对 | G029，手推Gaussian KL并检查padding/mask |
| SDE与ODE等价 | 能区别漂移系数/积分方向；数值条件需进一步推导 | G002，推导边缘连续性方程 |
| CFM梯度等价 | 条件期望与可微/可积条件须逐项检查 | G005，解释条件OT不等于全局OT |
| 数值积分误差 | NFE与阶数概念已分开，具体模型转换待代码核查 | G008/G027；EDM完整实验表仍未完成 |
| MeanFlow identity/JVP | 已记录作用，需逐符号推导目标与停止梯度 | E01笔记，再核实现 |
| 时空VAE混叠 | 已提出可观测性实验，尚未测真实笔画 | G003/G012/G013，先测重建事件 |
| rsLoRA稳定性 | 已读定理假设与实验，不扩张为任意任务保证 | G021，复述矩条件及学习率耦合 |
| 评价统计 | 已核样本数/参考分布差异，尚未运行自举置信区间 | G031/G032与项目事件协议 |
| 区域笔顺与动作物理 | 工具资料已纳入，尚缺全规范/真实执行审计 | AnimCJK/KanjiVG/Wuji等资源卡 |

CCF会议类别、正式接收状态和SCI分区属于不同信息。此处记录已核来源中的会议/期刊与年份；SCI分区未独立取得对应年度官方信息，暂不武断标为一区。经典来源用于理解机制，最新记录用于检查现有能力，二者都不能代替原始实验审查。


## 第六十八批补充（2026-10-21）

G030正式理论p20存在log比值/KL负号错误，p16/17相关正KL/正MSE式不能直接引用为已核保证；完整修正证明未完成。独立噪声/历史可靠性/MCG的经验与理想表达条件分列；视频长滚动为有限场景定性，maze reward/CRPS不代替严格笔顺。见[审查](diffusion_forcing_theory_protocol_and_versions_2026-10-21.md)。


## 第六十九批补充（2026-10-21）

G038独立噪声无状态非因果DFoT与HG-v/f/t将可变历史、可靠性及动态折中落到具体算法，补完G030后续。正式证明KL方向/符号与路径一致性问题保留；动作/相机历史任务不等文字笔顺或UMM协同。见[审查](history_guided_video_diffusion_audit_2026-10-21.md)。


## 第七十批补充（2026-10-21）

L086解耦+REPA与L092共享MAR的正式证据各有取舍；JanusFlow生成only可优于联合，Harmon实际Fig6提示理解监督对生成的特定方向收益，缺完整预算/seed条件。不能把共享或解耦本身当普适答案。见[审查](janusflow_harmon_shared_representation_audit_2026-10-21.md)。


## 第七十一批补充（2026-10-21）

G027补完固定网络采样→训练模块的正式审查：ρ/随机性依分布，预条件单项有FID退步，图像FID与笔事件数值误差分开。见[审查](edm_numerics_training_and_selection_audit_2026-10-21.md)。


## 第七十二批补充（2026-10-21）

L185正式/代码审查补扩散随机轨迹策略梯度、PPO近似、按维密度缩放；终端黑盒奖励与物理落笔事件仍有目标缺口。见[审查](ddpo_policy_surrogate_rewards_and_artifacts_2026-10-21.md)。


## 第七十三批补充（2026-10-21）

L001联合实例/顺序与跨阶段起点是直接强基线，L004布局条件英文轨迹是相关生成工作；静态多解、记录序/规范序、笔间顺序/笔内方向/可见视频事件应分开。见[审查](ordered_recovery_and_layout_strokes_audit_2026-10-21.md)。


## 第七十四批补充（2026-10-21）

Painter L180是LLM→笔触/渲染反馈的重要前作，StrokeFusion G024是局部几何+布局无序扩散；两者不能直接当已验证规范笔顺/真实视频。见[审查](painter_and_strokefusion_feedback_geometry_audit_2026-10-21.md)。


## 第七十五批补充（2026-10-21）

L005经典少样本部件检索保连笔，L015新版终图条件逆序视频/跨媒介；静态无向部件、已知终图流程和严格在线事件是不同可观测任务。见[审查](strokebank_and_loomis_painter_version_audit_2026-10-21.md)。


## 第七十六批补充（2026-10-21）

MMaDA共享masked CE主体/不同tokenizer与采样；Think in Strokes整图多轮RF/AR交错。联合训练共同上升非因果协同，中间可擦除语义编辑非严格书写事件。见[审查](mmada_and_think_in_strokes_protocol_audit_2026-10-21.md)。


## 第七十七批补充（2026-10-21）

女书静态字体OCR/动态记录分开，未训练视频生成；Stroke-Seg静态重叠类mask不确定唯一动作历史，非汉字应先定义本书写系统规范事件。见[审查](nushu_and_stroke_seg_data_protocol_audit_2026-10-21.md)。


第七十八批（2026-10-21）：VD模块路由/连续文本潜空间与Emu交错连续视觉预测是两种统一设计；全图语义causal表征没有真实笔事件时间含义。见[审查](versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)和[单篇L075](../reviews/L075.md)、[L077](../reviews/L077.md)。


第七十九批（2026-10-21）：动态语义token的连续理解输入/离散监督分开；全图causal merger不等同物理笔事件时序。见[审查](lavit_dynamic_tokens_and_version_audit_2026-10-21.md)和[单篇L079](../reviews/L079.md)。


第八十批（2026-10-21）：UniFlow层级蒸馏、pixel flow与GTB，重建/生成Pareto和原生输入信息量分开。见[审查](uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)和[单篇L072](../reviews/L072.md)。


第八十一批（2026-10-21）：共享离散索引不等同共享LLM协同，K/采样/decoder需控制。见[审查](tokenflow_shared_indices_and_claim_audit_2026-10-21.md)和[单篇L094](../reviews/L094.md)。


第八十二批（2026-10-21）：协同主张需控制数据身份、优化步数和外部decoder；相关性不独立识别因果。见[审查](metamorph_synergy_and_data_budget_audit_2026-10-21.md)和[单篇L090](../reviews/L090.md)。


第八十三批（2026-10-21）：DDPM/DSM/SDE、变分上下界与表示/条件/采样的瓶颈分解。见[审查](diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)和[单篇G022](../reviews/G022.md)。


第八十四批（2026-10-21）：逆SDE漂移、非线性近似、KL/VQ与训练/推理全成本。见[审查](diffusion_efficiency_full_pipeline_audit_2026-10-21.md)和[单篇G023](../reviews/G023.md)。


第八十五批（2026-10-21）：条件噪声均值总体最优、有限端点近似与随机边缘分支。见[审查](unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[单篇L076](../reviews/L076.md)。


第八十六批（2026-10-21）：时空压缩、残差identity调制、三方绑定与两向跨模态InfoNCE。见[审查](tora_motion_binding_and_process_boundary_audit_2026-10-21.md)、[L034](../reviews/L034.md)/[L035](../reviews/L035.md)。


第八十七批（2026-10-21）：条件flow端点、区域loss混杂、二维差分噪声/真实时标及alpha/r缩放。见[审查](tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)、[G039](../reviews/G039.md)/[R12](../reviews/R12.md)。


第八十八批（2026-10-21）：时空注入、顺序适配、dense/sparse条件偏移、零位移信息不可辨。见[审查](motionctrl_camera_object_and_observability_audit_2026-10-21.md)、[L039](../reviews/L039.md)。


第八十九批（2026-10-21）：离散MoD/mask泄漏、模态边缘对齐不能确定联合耦合、codec上限。见[审查](unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)、[L058](../reviews/L058.md)/[L059](../reviews/L059.md)。


第九十批（2026-10-21）：重建上限/可学性/任务能力分开；MCQ实际条目/组合数/码率与RQ参数条件。见[审查](seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[L060](../reviews/L060.md)/[L061](../reviews/L061.md)/[G040](../reviews/G040.md)。


第九十一批（2026-10-21）：有限元空间基/周期时间基、线性旋转、tanh高频/DC解析反例与参数分离定义。见[审查](semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[L051](../reviews/L051.md)/[L052](../reviews/L052.md)。


第九十二批（2026-10-21）：冻结VAE/BERT、噪声MSE和latent对抗分布约束不保证逐样本字形/事件。见[审查](dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[G041](../reviews/G041.md)。


第九十三批（2026-10-21）：零梯度与AdamW衰减、argmin码量化、剩余曝光/总FLOPs两种控制。见[审查](metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[L062](../reviews/L062.md)、[L074](../reviews/L074.md)。


第九十四批（2026-10-21）：链式分解不要求encoder causal；格式稳定、语义保真和可执行真实过程分开验证。见[审查](seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[L078](../reviews/L078.md)、[L082](../reviews/L082.md)。


第九十五批（2026-10-21）：估计mask可行性不保证准确率，FM与SB路径目标需对应；固定权重均值差值界及polyline时序信息限制。见[审查](timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[L053](../reviews/L053.md)、[L054](../reviews/L054.md)。


第九十六批（2026-10-21）：评价代理/人类效度、答案选项信息、显式坐标与有限预算对齐；既有画框负结果进入选题新颖性。见[审查](autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[G042](../reviews/G042.md)、[G043](../reviews/G043.md)。


第九十七批（2026-10-21）：连续理解/离散生成的量化取舍、任务曝光与总FLOPs、实例级测量效度和六任务宏均。见[审查](manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)、[L064](../reviews/L064.md)、[L071](../reviews/L071.md)。


第九十八批（2026-10-21）：共享任务非劣性与曝光/FLOPs、低码率多码本流式、AR到离散双向去噪、外部像素/视频decoder与时序可辨。见[审查](qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[L065](../reviews/L065.md)、[L066](../reviews/L066.md)。


第九十九批（2026-10-21）：二元AW等于联合正确、共同事件锚/动态实际历史与规范目标；错误同分不保证同内容，家族均值不足因果归因。见[审查](xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[L067](../reviews/L067.md)、[L068](../reviews/L068.md)。


第一百批（2026-10-21）：GGU差值代数、双正确与潜在表征因果分开，oracle受控参考和stopprobe改变任务；迁移到事件GT/真实执行状态。见[审查](unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[L069](../reviews/L069.md)、[L070](../reviews/L070.md)。


第一百零一批（2026-10-21）：冻结专家参数/条件梯度/真实训练成本分开，KL最优专家假设和T3局部协同对照，交错数据非指令数据。见[审查](nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[L080](../reviews/L080.md)、[L081](../reviews/L081.md)。


第一百零二批（2026-10-21）：视觉压缩/重建上限、RICES与格式、量化depth成本及对齐/重建取舍；统一接口非协同证据。见[审查](emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[L083](../reviews/L083.md)、[L085](../reviews/L085.md)。


第一百零三批（2026-10-21）：视觉-文字embedding对齐及语言先验；无序内容F1与NED，轨迹片段GAT不等于规范笔画；不从识别推出生成能力。见[审查](callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[L045](../reviews/L045.md)、[L046](../reviews/L046.md)。


第一百零四批（2026-10-21）：经验规模趋势与评价饱和、原基座/文本继续控制、教师引导SFT和历史预训成本；局部联合增益与严格共享协同分开。见[审查](liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[L088](../reviews/L088.md)、[L089](../reviews/L089.md)。


第一百零五批（2026-10-21）：masked目标熵/PPL、课程速度预算、奖励泛化与分布差因果；无序Counter召回/长度加权与有序过程区分。见[审查](ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[L091](../reviews/L091.md)、[L093](../reviews/L093.md)。


第一百零六批（2026-10-21）：固定loss尺度与梯度冲突、语义层级/量化瓶颈、rFID/PSNR/码率Pareto；序列长度不变与额外残差预测成本区分。见[审查](qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[L095](../reviews/L095.md)、[L096](../reviews/L096.md)。


第一百零七批（2026-10-21）：二档source-confidence/校准、偏好点份额/胜率、仿真条件与评估参照、有限保护惩罚/可行性、代理RGB参照。见[审查](motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[L036](../reviews/L036.md)、[L037](../reviews/L037.md)。


第一百零八批（2026-10-21）：参考side information与条件熵动机、实际总码率/名义token比、完整因果隔离/目标内部上下文、PSNR与混合百分比。见[审查](reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[L038](../reviews/L038.md)。


第一百零九批（2026-10-21）：dense→sparse课程、anchor后仍按强度采样、空间身份pool与位置Gaussian、点加权均值和26/12百分点。见[审查](dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[L040](../reviews/L040.md)、[L041](../reviews/L041.md)。


第一百一十批（2026-10-21）：先对应再字符计分、S/T分离、每视频调和后平均；条件观测和字符加权影响测量对象。见[审查](textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[L042](../reviews/L042.md)。


第一百一十一批（2026-10-22）：fitting子串/可读support/Pareto反例，glyph推理消融与训练归因、池化时序可识别性需实验。见[审查](vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[L043](../reviews/L043.md)。


第一百一十二批（2026-10-22）：单任务/联合干扰减轻仍有负迁移；输入连续支路不等于T2I输出连续码，额外先验/成本需对齐。见[审查](unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[L097](../reviews/L097.md)。


第一百一十三批（2026-10-22）：空间码前缀MDP反例、entropy不等于因果、IV假设与Eq20梯度；关联已读L185DDPO。见[审查](selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[L098](../reviews/L098.md)。


第一百一十四批（2026-10-22）：排列/文本perplexity与协同因果边界，前缀渐进非物理时间；名义相同比特仍需同数据/decoder预算。见[审查](ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[G044](../reviews/G044.md)、[L098](../reviews/L098.md)。


第一百一十五批（2026-10-22）：Eq1中心梯度、Eq2不平衡簇反例、H上界与语义信息差别、Eq17分布/尺度条件。见[审查](unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[L099](../reviews/L099.md)。


第一百一十六批（2026-10-22）：连续Transfusion分类纠正；CKNNA相关与因果、VAE时空压缩对短事件的边界。见[审查](tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[L100](../reviews/L100.md)。


第一百一十七批（2026-10-22）：名义bits/位置token/曝光/完整算力分开；SigLu有界不证明entropy/commitment函数等价。见[审查](uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[L101](../reviews/L101.md)。


第一百一十八批（2026-10-22）：shared前缀不等于各层绑码本；EMA与commitment作用不同；残差深度不等于物理时间。见[审查](evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[L102](../reviews/L102.md)。


第一百一十九批（2026-10-22）：Eq1条件分解需充分性；低维/连续不保证无损，18倍维数不等于上下文或完整bits/FLOPs。见[审查](unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[L104](../reviews/L104.md)。


第一百二十批（2026-10-22）：x预测速度MSE对应时间加权clean误差；flow噪声时间不等于真实书写时间。见[审查](tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[L105](../reviews/L105.md)。


第一百二十一批（2026-10-22）：固定VAE重建误差不直接给GenEval上界，EMA/硬VQ联合训练非全路径连续反传。见[审查](representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[L106](../reviews/L106.md)。


第一百二十二批（2026-10-22）：2位置mask的层级感受野、fs与总码率、无交互边与统计独立区分。见[审查](hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[L107](../reviews/L107.md)。


第一百二十三批（2026-10-22）：patchify重排与线性单射条件，跨空间loss不可比、步数不等FLOPs收益。见[审查](pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[L108](../reviews/L108.md)。


第一百二十四批（2026-10-22）：给定路径/权重动能最优及负对角条件，概率时间与书写执行时间分清。见[审查](fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[L109](../reviews/L109.md)。


第一百二十五批（2026-10-22）：maskedCE归一/条件独立近似、exp时间方向与codec小字上限。见[审查](lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[L111](../reviews/L111.md)。


第一百二十六批（2026-10-22）：最大rawlogit标度/softmax公共baseline抵消、码保持与RGB保持区别。见[审查](lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[L112](../reviews/L112.md)。


第一百二十七批（2026-10-22）：负熵提交、统一缩放与依正负logit变换、mask揭示时间不等物理时间。见[审查](omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[L113](../reviews/L113.md)。


第一百二十八批（2026-10-22）：语义充分性、独立连续decoder、key范数与注意力贡献及逆sqrt长度折中。见[审查](llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[L114](../reviews/L114.md)。


第一百二十九批（2026-10-22）：MSE/CE输出梯度界到共享参数须Jacobian条件；二维时间路径不保证路径无关质量。见[审查](fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[L115](../reviews/L115.md)。


第一百三十批（2026-10-22）：chunk因果分解、端点FM时间权重、SDE backstep方差与前缀分布偏差。见[审查](multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[L116](../reviews/L116.md)。


第一百三十一批（2026-10-22）：条件均值回归与随机latentflow、双扩散噪声、端点下标勘误及时间换元。见[审查](blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[L117](../reviews/L117.md)。


第一百三十二批（2026-10-22）：确定query连接器与随机CLIPflow区别、latentflow目标和冻结反传成本。见[审查](openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[L118](../reviews/L118.md)。


第一百三十三批（2026-10-22）：mutual-kNN跨样本几何一致性不等梯度冲突；总体曲线非严格单调，CE均值归一化与任务曝光需核。见[审查](unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[L119](../reviews/L119.md)。


第一百三十四批（2026-10-22）：共享MoE路由观察与人工分叉区分，Euler速度推理与未公开训练目标区分，SSAE宏微平均和GSB净差。见[审查](hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[L120](../reviews/L120.md)。


第一百三十五批（2026-10-22）：六层全上下文特征、一次前向学习query与显式CoT区分，概率比中加性常数与方差系数，组标准化的作用条件。见[审查](deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[L121](../reviews/L121.md)。


第一百三十六批（2026-10-22）：两层上下文通道融合、双流联合注意、RMSNorm二阶矩、3CFG成本及分类均值凸组合一致性。见[审查](internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[L123](../reviews/L123.md)。


第一百三十七批（2026-10-22）：MoE活跃与驻留、注意二次成本、dense窄专家upcycling、ByT5字节预算、收敛步数与耗时区分。见[审查](mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[L124](../reviews/L124.md)。


第一百三十八批（2026-10-22）：near-lossless经验与可逆性区别、sigma平方根的二阶矩、活跃/驻留参数、CFG前向次数与端到端耗时。见[审查](sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[L125](../reviews/L125.md)。


第一百三十九批（2026-10-22）：组内std/variance、反向KL、特征分布代理与准确图像概率、文字policy gradient和可微冻结生成器。见[审查](mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.md)、[L128](../reviews/L128.md)。


第一百四十批（2026-10-22）：双向max-cos的集合不变性与上下文位置、联合sequence和token surrogate、CFG采样与概率匹配。见[审查](corl_joint_advantage_branch_and_reward_release_audit_2026-10-22.md)、[L129](../reviews/L129.md)。


第一百四十一批（2026-10-22）：平方根压缩高分差距、同正标量保持pair梯度夹角，std前后权重不等效。见[审查](pairuni_pair_weighting_gradient_and_release_audit_2026-10-22.md)、[L130](../reviews/L130.md)。


第一百四十二批（2026-10-22）：正式Eq7–8补条件期望/MC，MI/Bayes恒等式不保证有限容量CE+MSE正迁移；Best轨迹与无偏MC区分。见[审查](unicorn_selfplay_joint_objective_and_unicycle_protocol_audit_2026-10-22.md)、[L131](../reviews/L131.md)。


第一百四十三批（2026-10-22）：把性能取舍与梯度/容量根因区分；同组固定Vold减均值后消掉，不因公开存Vnew误判reward错误。见[审查](r3_tree_rl_understanding_scope_and_prompt_overlap_audit_2026-10-22.md)、[L132](../reviews/L132.md)。


第一百四十四批（2026-10-22）：固定提示的文本先验常数不能反转组内排序；几何长度归一保排序但非线性改变优势，检验视觉敏感性与活动教师漂移。见[审查](gvu_intrinsic_probability_reward_and_release_audit_2026-10-22.md)、[L133](../reviews/L133.md)。


第一百四十五批（2026-10-22）：Eq16缺partition常数，常数奖励平移即反例；条件均值速度不等终态均图，MI降条件熵需边缘和下界条件。见[审查](lvrpo_theory_reward_and_protocol_audit_2026-10-22.md)、[L134](../reviews/L134.md)。


第一百四十六批（2026-10-22）：选择性采样改变目标/score分布，精确截断正态方差不满足通用≤p界；奖励均值不等梯度信号，阈值局部线性化需lnT*。见[审查](uni_synergy_dgs_theory_and_personalization_release_audit_2026-10-22.md)、[L135](../reviews/L135.md)。


第一百四十七批（2026-10-23）：祖先路径均值的原始点积有深度偏置；纸面Root=L1与源码独立基区分，双向一致性不保证外部语义正确。见[审查](chinese_radical_joint_tpe_geometry_and_negative_transfer_audit_2026-10-23.md)、[L181](../reviews/L181.md)。


第一百四十八批（2026-10-23）：Eq2负w高斯模糊/正w反遮罩锐化与文字相反；同族算子模拟不等真实核泛化，角度不可辨和时间平滑不等正确运动。见[审查](strive_video_text_replacement_and_propagation_protocol_audit_2026-10-23.md)、[L182](../reviews/L182.md)。


第一百四十九批（2026-10-23）：VQ+连续旁路不证明风格因子可识别，InfoNCE同坐标负样本/重复部件假设；生成噪声预测代数恢复z0供PCE。见[审查](constant_multilingual_style_quantization_and_evaluation_audit_2026-10-23.md)、[L183](../reviews/L183.md)。


第一百五十批（2026-10-23）：一致与正确分离，独立路径与caption条件链分离；软乘积门控允许edit0奖励.44，全2分.275，不能推硬保证。见[审查](stbridge_shared_target_alignment_and_causal_controls_audit_2026-10-23.md)、[L137](../reviews/L137.md)。


第一百五十一批（2026-10-23）：有限样本最低均值可能吸收负噪声，低reward不等可学缺口；caption循环非双射，一致不保证原信息保存。见[审查](mate_adversarial_pool_evolution_and_budget_audit_2026-10-23.md)、[L138](../reviews/L138.md)。


第一百五十二批（2026-10-23）：诊断效度区分预测/并发/因果；统一冲突严重度方向后cos/rate/energy符号不矛盾，CAGrad对称正交分量可抵消。见[审查](gradient_conflict_metric_validity_and_causal_audit_2026-10-23.md)、[L139](../reviews/L139.md)。


第一百五十三批（2026-10-23）：调用位置梯度精确分解不等loss项梯度；归一后eta保留率不等因果方差分解，组合增益不等简单相加。见[审查](position_gradient_attribution_and_lora_budget_audit_2026-10-23.md)、[L140](../reviews/L140.md)。


第一百五十四批（2026-10-23）：SVD行空间保留比例不等实际Wδ能量，维度比需各向同性；条件漂移和五块范数保持不足证明唯一瓶颈或线性，边际分数比不等条件成功率。见[审查](unike_cross_modal_editing_and_artifact_protocol_audit_2026-10-23.md)、[L141](../reviews/L141.md)。


第一百五十五批（2026-10-23）：S=g a+(1−g)b同时含生成真符合、真阳性和误答目标，Δ自评−外裁不能识别绝对理解；层级macro与池化micro、选项偏差、簇相关需区分。见[审查](unieval_self_evaluation_identifiability_and_answer_bias_audit_2026-10-23.md)、[L143](../reviews/L143.md)。


第一百五十六批（2026-10-23）：强制中间图流程不推出逻辑必需；step宏平均/整题exact、感知距离/准确率及κ边际需区分，同预算干预才能定位协同。见[审查](unimmmu_state_parsing_oracle_length_and_synergy_audit_2026-10-23.md)、[L144](../reviews/L144.md)。
