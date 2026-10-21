# MotiMotion与Fluid-Gen-Zero：运动控制、物理参照及发布协议审查

第一百零七批完成已有[L036 MotiMotion](../reviews/L036.md)、[L037 Fluid-Gen-Zero](../reviews/L037.md)固定核心三遍、实际框架/主表/消融与五条书面检查，补全两项正式题名。[结构化来源与范围](../../data/motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.json)。356目录（329论文／研究、27资源），215核心/218书面含未通过项，141条未确认核心（含资源）。无文件删除、权重/图片或视频下载、模型/仿真执行或原结果复现；MotiBench仅读取文本标注/来源表与发布元数据。

两项是相关的视频生成研究，提供外部规划/仿真与生成器的模块路线。MotiMotion侧重欠指定用户动作的后果推断，Fluid-Gen-Zero侧重对单图重建仿真的遵循。两种目标与规范笔顺、共享UMM协同训练均需分别验证。

| 工作 | 一手身份与固定阅读版本 | 实际图表 |
| --- | --- | --- |
| MotiMotion | [正式ICML2026/PMLR306:44433–44451](https://proceedings.mlr.press/v306/hsin-ying26a.html)，完整19页PDF取得并交叉对应表/配置；完整核心/附A–C阅读固定[2605.22818v1](https://arxiv.org/html/2605.22818v1)，2026-05-21 | F2、完整T1/T4；全部现有T1–9文字协议 |
| Fluid-Gen-Zero | 固定[2610.10984v1](https://arxiv.org/html/2610.10984v1)，2026-10-07；正式会议/期刊未确认，核心§1–5/Eq1–5、附1–7/T1–8 | F2/F4、完整T1/T8 |

## MotiMotion：允许重定时的运动规划及二档软控制

VLM读取原图、叠加轨迹、归一坐标和可选文字，生成详细叙述、修正用户轨迹并补从动或静止锚点；轨迹高斯图复制三通道，经Wan VAE与noisy/reference latent按channel拼接。Wan2.2 I2V-A14B扩初始tokenization层，并微调该层及全部self-attention，其他冻结；FM预测x1−x0。新增权重零初始化。

外部reasoner不训练，视频控制器却训练5K+3K步，故“training-free”只适用于reasoner。OpenVid/CoTracker3 64×64提点，阶段I采1–500轨迹，阶段II采1–20，50%样本作仿射/降采样/平滑退化。实际confidence为用户1、VLM预测.5，通过高斯峰值sG缩放；并无已验证的连续置信概率校准。

固定公开提示词要求100–150词叙述、20点/5秒4FPS归一坐标；空间形状和静点应保留，遇物理冲突可改路径，速度可重定时。这一任务定义适合表达粗意图。规范笔顺若已给合法真值，需要限制模型的改动权限并另测指令保持。

| 证据 | 原始结果 | 解释边界 |
| --- | --- | --- |
| 正式T1 | 物理.302>Magic.157/WanMove.218；语义.665>.343/.511；Photo.520<Magic.550 | 表题“全项最高”与数值不符，保留观感反例 |
| T2偏好 | 自动overall78/73.8，人类97.9/81.4 | slight/moderate/strong权1/2/3、tie0，SA/(SA+SB)为决定性偏好点份额，不能按普通胜率解释 |
| T4同控制器 | 物理.166→prompt.237→motion.285→confidence.302；语义.337→.544→.641→.665 | 支持该配置组件链，不证明真实参数级物理推理或任意分布都改善 |
| T3迁移 | Magic加reasoning物理.157→.199，但Photo.550→.528 | 规划收益有指标取舍 |
| AppT9阶段 | 两阶段物理.319高于一阶段.302，Photo.503<.520、语义.654<.665 | 一阶段减少额外生成/推理调用，效果与成本共同决定选择 |
| AppT7跟随 | 4轨迹FVD724.4/EPE8.28；16轨迹712.8/7.89 | 跟随协议与MotiBench欠指定后果任务分开，跨底座/训练量非严格因果控制 |

Gemini3.1Pro同时做规划与自动judge，相关偏差需要独立judge/人评检验。12人各30随机题共360次比较，未提供每场景等频、raw win/tie/强度分布及聚类置信区间。公开2AFC prompt要求避免tie，进一步说明原始判断分布应公开。迭代纠错仅展示钟表一例，未用于其他实验。

训练Adam/lr1e-5/b16/warm100/constant/wd.03；低档I~U[.1,1]、旋转±5°I/scale±.2I/trans±30Ipx、最少10%点重插值、SG阶2。作者报告完整reasoning约50s/10Ktoken/.07USD、prompt-only15s/3K/.02，仅代表当时reasoner成本；视频生成NFE、分辨率、硬件和总延迟未核齐。

### MotiBench公开标注与论文统计的具体差异

[固定GH](https://github.com/motimotion/motimotion/tree/b3baf01615279b2912d2dee1c91924139de9db38)完整5blob：README、method图、reason/eval/eval-2afc三指令文件。已有规划与评价提示词，可研究其规则；未确认完整控制器训练/采样代码或权重发布。

[HF固定revision4b3f3bf83e2d6b062873af12f910c8d5d9ed6ff6](https://huggingface.co/datasets/shinying/motibench/tree/4b3f3bf83e2d6b062873af12f910c8d5d9ed6ff6)读取卡、API目录、`test.jsonl`、`licenses.csv`，未下载图像。

| 项目 | 论文/卡 | 固定标注实际统计 |
| --- | --- | --- |
| 总量 | 62 | 62行、目录62图、来源表62行/文件名相对应 |
| 五类 | Collision9/Constraint17/Tool8/Flow9/Common19 | Collision9/Constraint17/Tool9/Flow8/Common19 |
| 输入轨迹 | 粗轨迹，推理指令输出20点归一坐标 | 98条原始轨迹，每图1–5条、每轨迹1–20点，坐标范围14–1483，为像素量级 |
| 来源 | 生成/网络或真实照片混合 | Generated16、Pexels23、Unsplash23 |

Flow与Tool计数相差一条，当前不能判哪条标签应改，也不据此断言主实验用了错误数据。应保留论文统计与发布统计的不同版本证据。原始长度不一的像素轨迹需要归一/插值，推理20点schema是输出约束，不能假定原始文件已经满足；完整预处理脚本未核到。

HF卡CC-BY4适用于作者轨迹/prompt，照片另按Pexels/Unsplash来源许可。不能用顶层单一元数据覆盖所有图片，也不重复计该论文的配套数据为新增独立论文。

## Fluid-Gen-Zero：仿真参照如何进入长视频

规则parser给材料/力，VLM判物体、流体类型、尺度与事件；DINO/SAM2.1分割、MoGe2 pointmap和SAM3D物体mesh，液面法向定义世界重力方向。Genesis将刚体或弹性MPM与液体MPM耦合，生成粒子轨迹、投影flow/mask、预览和代理参照。该仿真决定粗运动，冻结VFM恢复外观。

参照视频的实现定义需要说清：附1.3是FLUX补背景后，将原图物体图层按仿真centroid位移平移、alpha合成。它没有完整渲染物体旋转/弹性或流体表面推进；native flow/轨迹条件和生成器承担其他运动/细节。不能把参照直接解读为真实RGB物理视频。

规划把物理粒子变化、投影flow/mask变化和VLM事件风险融合，p5/p95归一，各族默认(.4,.4,.2)与VLM权重等权。按复杂度选择13/41/81目标长度，在1mod4合法候选上贪心最小化局部复杂度、长度差、事件边缘奖励和保护惩罚。阈值.45/.72、importance.75、λu10。若存在未受保护候选，该大惩罚优先避开保护区；若全部候选受保护，仍未保证硬可行，不能宣称绝不切事件。

latent参照按原scheduler加噪初始化：FM用γ=1−σ，Tora用sqrt αbar。object早期二值mask/β1硬替换，fluid平滑mask/β从.8线性衰减，k0=8、kobj11、kfl10，之后释放。clip末帧作下段首帧锚，去重复帧。原生VACE denseflow、Tora/WanMove sparse轨迹同时保留。

| 证据 | 数值/协议 | 解释边界 |
| --- | --- | --- |
| T1仿真对齐 | Tora对象133.20→24.61、fEPE3.950→.843；WanMove92.93→23.08、5.180→.827；VACE56.02→41.06、6.445→2.070 | 同条件与同参照对齐改善；不等于已测真实动力学正确 |
| T1质量反例 | WanMove审美.528→.500、图质.677→.665、PhysR.518→.486；overall.593→.597 | 多指标存在取舍，不能只摘对齐改善 |
| AppT6/7/8 | planning-only128.12/3.221，latent-only24.79/.812，full24.61/.843 | planner同时改caption与边界；full fluid误差略劣latent-only、subject.906<.912，未实现所有指标单调增益 |
| T8区域 | 去region30.40/1.026，去fluid28.06/.937，full24.61/.843 | 区域设计改善所测对齐；去fluid flicker.998>full.995，去region图质.657>.656 |
| T2人评 | 同底座overall55.1–74.4%，对PhysGen3D94.2/WonderPlay90.4 | 仅8图/13人/442pairs，不当43场景全体成功率；人评看同一仿真preview |

对象误差是逐帧centroid L1像素，fEPE以仿真投影flow为参照。物理参数和重建若错，忠实遵循会继承错误；仍需真实录像或传感数据。VideoPhy2/flicker可能偏好稳定少动，原文提出GPT judge更敏感，但GPT亦须用错时/冻结/外观好且运动错的对照校准，不能默认其判断是真值。

43策展场景、10主流体类别、401帧为仿真，不是401帧真实录像。Genesis dt1e-3/30substeps/g9.8；FLUX补背景24步固定seed；gpt5.4-mini-2026-03-17做三类调用，每5帧采样，gpt5.5作judge。无生成器微调仍有多预训练模型、VLM、仿真及多clip计算；完整NFE/分辨率/硬件/卡时和独立调参集未核齐。

[作者项目](https://hongh0.github.io/Fluid-Gen-Zero/)所链[GH](https://github.com/hongh0/Fluid-Gen-Zero)本次HEAD API404；论文写upon acceptance。只能记录当前未确认公开实现/数据，不能称原代码已读、完整系统已复现或网络绝无其他制品。

## 可证伪实验及待追引工作

对MotiMotion，将正确完整、欠指定、故意违规输入分层，同时测指令保持与事件合理性；固定调用/生成预算，对比长prompt、不同reasoner、随机规划、标准控制器。公开raw win/tie/强度分布并按场景/被试聚类统计；二档confidence与真正校准不确定度分开。严格书写场景禁止任意添笔/改序，测可见事件与真实接触。

对Fluid-Gen-Zero，固定prompt仅动边界、固定边界仅动prompt，比较初始化/区域/时间表与等NFE控制；以真实物理数据校准尺度/材料、留未见物性，测试超长保护事件。评人同时有无simulation preview，报告端到端成本、质量/对齐Pareto。书写可借鉴笔尖/旧墨迹的不同锚定，但需刷毛/墨迹标定和独立顺序监督。上述均未执行。

本批追引中识别出主目录及现有候选题名未覆盖的相关路线：MagicMotion、Motion Prompting、MotionCraft、PhysGen3D、WonderPlay、RealWonder、PerpetualWonder、PhysAnimator；另有前批检索发现的Rosetta Stone for Unified MLLMs与VQRAE。现列为待核队列，引用关系/名称不充作这些原文已读或正式录用证据。需核定一手版本、去重、阅读原文与资源，再判断当前局限是否已有解法。

写作上，问题定义先说明何时允许修正输入、何种参照代表成功；Method展示每层表示与接口；实验把主效果、机制、代价及反例分别呈现。Claim明确加权偏好/相对下降、策展分布/真实物理、冻结参数/完整成本；Limitations落到重建误差、judge耦合、代码与标注版本的具体缺口。
