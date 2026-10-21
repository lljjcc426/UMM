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
