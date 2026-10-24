# SCO：完整软约束求解与视频协议审查

第一百八十八批完成[U23](../reviews/U23.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/sco_full_soft_constraint_solver_and_video_protocol_audit_2026-10-25.json)。358目录（331论文／研究、27资源），293核心/298书面含未通过项；待完成核心深审38篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2610.10400v1)、[主源2](https://arxiv.org/html/2610.10400v1)、[主源3](https://arxiv.org/pdf/2610.10400v1)、[主源4](https://api.github.com/search/repositories?q=%22self-correction%22+%22interleaved%22)。

## 研究问题

交错生成每一轮如何同时落实新事件、保留此前主体/布局/风格，并避免历史图像惯性和逐轮漂移？提出冻结生成器的采样更新修正，目标是图序列与视频的变化/保持取舍；未生成或约束书写笔轨迹。

## 现有不足

普通CFG将历史与当前事件混合在一个条件方向和一个scale，强化当前动作可能改动应保持内容，过度保持又可能抑制合法变化。额外训练/数据成本较高，作者用四个条件预测在推理时构造两个代理方向；两差分能否对应真实语义因素仍需检验。

## 贡献

full/counter/eventonly/unconditional四分支，构造new-event和state-preserving方向，在二维Gram耦合下做有预算的最小修正；无模型参数或task-specific训练。七图文生成器×两基准、CFG方法比较、两约束消融/五超参扫，三视频生成器和IRASim定性扩展。新意是变化/保持的联合控制协议与软约束化；未给代码或独立证明语义分解/物理正确性。

## 输入、模块、输出与公式

Eq1历史H与事件e→当前图并append回历史；δref=ω(vfull−vu)。Eq2–4counter保同H但把e改成事件发生前e∅，anew=vfull−vcounter，要求anewᵀδ≥λnew||anew||。Eq5–6eventonly删除H保e，astate=vfull−vevent，同样半空间。Eq7λnew=α0在τ≤τend内启用，λstate=sstateλnew；τ是从采样开始计的归一进程。Eq8δ*=δref+μnewanew+μstateastate，v*=vu+δ*；Eq9无预算的欧氏投影，Eq10–11Gram对角范数/非对角夹角，Eq12 0≤μi≤Mi；Eq13加入非负slack的二次目标加Miξi。负cos表示两个更新方向局部竞争，不足以证明不可行，最终residual=[ci−aiᵀδ*]+判断未满足程度。

## 模型结构

外接冻结采样层，v可为noise/score/velocity，需各底座支持相同latent上的四条件预测。MiniGPT5/MMInterleaved模块化与BAGEL/SenseNova/LLaDA/DuoGen等按各自原架构，不能据表分类把Showo2概括为所有意义的模块化。二维系数小不等额外backboneforward便宜。视频Eq14 GPT5planner把目标F帧分K事件并分配nk，Eq15–17对同一联合spatiotemporallatent四分支的第t帧分量求方向/μ，保留视频网络原有跨帧attention；各帧分量条件差不独立隔离局部因果或物理动力学。

## 数据分布与划分

OpenING5400人标条目/23meta-topic/56tasks；ISGBench1150/8场景/21subtasks与interleavedscenegraph，正文与AppA2称用officialprompts/protocol，但主表FID/CLIPI/GPT等自定组合与原benchmark全部官方维度不相同，实际题ID/过滤/输出图对GT对齐/失败处理未全披。手工VideoCraftBench五任务约9.5Kclips/7小时为数据源总规模，主实验手工subset实际测试数未给；InterleavedXEmbodiment约210K轨迹为母集，手物subset实际分割/测试数未给。LanguageTable在AppA2另述followingIRASim的初始观察+短动作轨迹条件视频，仅F6定性，无T5独立量化行，不能把母集规模当本文评测数。

## 指标与评价协议

图文表FID↓、CLIPI/T↑、GPTJ1↑、主体Cs/背景Cb↑、GPTJ2↑；Eq18FID的Inception均值/协方差距离。Cs为连续帧主体区域DINOv2cos，Cb背景CLIPcos，主体/背景分割获取与tracking未给；CLIP本身为语义表征，Cb不等低层几何/静止像素一致。GPTJ1逐帧promptfidelity/factual，J2holistic事实/物理0–1，均称GPT5.6sol固定采样，但无完整prompt/snapshot/具体采样值/人评校准。视频FVD/LPIPS↓，LPIPS条目至2.487，缺骨干/归一/逐帧和多帧聚合，不能由>1单独判非法，也不能直接与标准实现跨论文比。DINO/CLIP平稳与LM评分不等接触/守恒/机器人执行成功。

## 对比方法

MiniGPT5、Showo2、MMInterleaved、BAGEL、LLaDA2.0Uni、SenseNovaU1、DuoGen各original/+SCO。T3SenseNova在OpenING比较InterleavedCFG/CFG++/TCFG；T4MMInterleavedOpenING与SenseNovaISG的stateonly/newonly/both。未有等总NFE或walltime的更长采样/多次采样/多条件线性组合对照，也未有联合Gram对sequential/去交叉项对照。视频VideoWorld2/Cosmos2.5/Cosmos3及F6IRASim。未统一记录各模型revision、基本CFGscale/步数/分辨率/conditionaldrop实现。

## 实验条件和发布边界

PyTorch、2×NVIDIAH100，冻结θ、无训练；SenseNova在OpenING扫α0=.25/.5/1/2/4，sstate=.3/.5/.7/.9/1.1，Mnew=2/4/6/8/10，Mstate=3/5/10/15/20，τend=0/.25/.5/.75/1；最佳区域α1/Mnew6、sstate.7–.9/Mstate10、τend.5。未声明独立校准集或最终全模型固定值/多seed与CI。每个选中采样步除baselinefull/u再算counter/eventonly；若N步有比例f启用且同单分支成本，预测次数从2N变(2+2f)N、比例1+f，半数步时约1.5倍仅分析近似，τend.5不必正好半数非均匀步。未报告总NFE/延迟/峰值显存或planner+rewriteAPI成本。视频GPT5planner是必需阶段，F7又用commercialmodels改写历史/事件，具体模型/prompt/缓存和错误率未披。论文/arXiv无官方code/project链接，GitHub组合词检索0、HFpaperAPI404；有限范围未定位实现/权重/原始评分日志。无模型或API执行。

## 主结果

T1 ISG全七底座各项均升：FIDMini91.3→88.5、Showo83.6→79.7、MM76.2→73.6、BAGEL83.2→78.3、LLaDA95.8→91.7、SenseNova52.1→49.7、DuoGen45.7→41.4；DuoGenCLIPI.413→.445/CLIPT.531→.560/J1.692→.735/Cs.39→.41/Cb.43→.47/J2.621→.659。T2OpenINGFIDMini90.4→89.9、Showo88.5→84、MM94.1→81.3、BAGEL87.2→83.7、LLaDA118.6→108.4、Sense67.2→55.9、Duo53.6→50.1。SenseCLIPI.325→.376/T.471→.507/J1.658→.694/Cs.29→.35/Cb.37→.40/J2.574→.602；DuoCLIPI.382→.405/T.505→.539/J2.603→.637。Mini另外六项全退CLIPI.149→.138/T.257→.247/J1.445→.423/Cs.18→.17/Cb.23→.21/J2.344→.319；LLaDAJ1.237→.234/Cb.11→.10也退。故generalimprovement有底座与指标限制。T1captionISG/T2OpenING，§4.3首句顺序写反；本批按caption及数字分配。全部行见结构化数据。

## 消融及进一步实验

T3SenseOpenING InterleavedCFG/CFG++/TCFG/SCO的FID62.7/60.4/59.2/55.9，CLIPI.343/.358/.349/.376，CLIPT.485/.481/.484/.507，J2.589/.577/.583/.602；SCO在四项均最高，但分支数/预算未对齐。T4MMbase/state/new/both的FID94.1/85.6/89.4/81.3，CLIPI.140/.149/.153/.164，J1.432/.445/.440/.450，Cs.15/.18/.13/.17，J2.327/.320/.362/.369；SenseFID52.1/51.1/50.6/49.7，CLIPI.385/.393/.397/.409，J1.677/.689/.686/.695，Cs.36/.39/.34/.38，J2.591/.620/.563/.624。stateonlyCs优both但MMJ2低base；newonlySenseJ2低base。T5VideoWorldFVD178→146.3/LPIPS2.487→1.708/Cs.26→.30/Cb.38→.41/J2.527→.562；Cosmos2.5167.2→142.3/1.729→1.337/.37→.41/.48→.52/.583→.640；Cosmos3138.9→119.3/1.174→1.026/.49→.53/.56→.59/.651→.705。F3五超参中等区域较优，F4τ1噪声严重、τ.5保布局但效果方向仍需实测；F1/F2/F5/F8–10为选例，无统一成功率。

## 局限与疑问

求解语义需明确：Eq13软primal可消去slack为二次项+加权hinge，其对偶应为min_{0≤μ≤M} .5μᵀGμ−dᵀμ，d_i=c_i−aiᵀδref，δ*=δref+Aᵀμ。该框内对偶始终允许残差；把Eq9硬半空间再直接加Eq12系数上限可能无可行解，二者不能无说明混用。正文称解Eq9+12但同时给正确软形式，缺实际solver/活跃集/数值协议，记录为实现歧义，不据此判定实际算法错误。方向是冻结模型对prompt改写/删历史的响应，未与独立event/stateGT校准；F7历史红裙白上衣被full/counter文字改成红shirt，显示改写可失真。F8newonly行文字本身写变浅/ivorywhite，若作图条件则颜色改变受条件混杂，若是生成文字则需分离planner与图采样贡献；caption角色未明，不把全变色归于方向。单位缩放v→kv时投影左侧k²/阈值k，固定λ不自动跨noise/score/velocity或尺度保持等效；μbudget亦受范数。视频四分支各自改全帧条件，perframeμ不提供物理约束。F6IRASim+SCO选例仍标no-contact/not-target-place/offset，证明残余接触与终点问题，无法从T5J2提升推导已验证真实动力学。

## 预期优势条件

底座能可靠理解事件/历史且有可访问采样分支时，变化与保持两方向的受控折中可能改善长图序列。SCO更依赖分支可分性与准确rewrite；Mini失败表明弱生成器/错误条件下无保证。迁移书写与素描应把state设为已完成笔画/字符拓扑，将new设为当前合法笔或增墨；抬笔、擦除、遮挡或艺术风格变更需要允许变化的mask/语义范围。现有Cs/Cb不验证细笔画、笔顺或轨迹可执行性，也不能撤销已落纸动作。

## 可证伪实验

Q1联合校正到底实现了什么：公开每步四branch/原始方向、G/μ/投影残差，按Eq13对偶与active-set给可复算低维例；同输出参数化/normalized方向，比较原CFG、固定线性四分支、单方向、顺序校正/无交叉项和joint，按实际总NFE/延迟/显存对齐。独立校准集固定超参、多seedpairedCI，同时报告event实现与应保持/允许改变区域的pixel/结构指标；加入oracle/模型生成/错误rewrite，若消融提示词质量即可解释收益，收缩优化机制主张。Q2视频物理与书写是否获益：同一planner/同事件分帧与相同初始状态/动作轨迹，控制无planner/错误planner并计预处理API，列出实际视频IDs/fps/长度/分辨率/失败分母；报接触连续性、穿透/物体持久性、目标到达和闭环sim执行成功，分别测有必要大变化/遮挡场景。书写加prefix墨迹保留/新增定位、细笔与字符拓扑、DTW笔序及手笔接触，和复制前帧/静止高一致基线并列。均建议，未执行。

## 论文组织与Claim学习

以event/state矛盾导出双条件、Gram交叉作用和softslack，理论与消融对应，正文承认Mini失败和保持/变化取舍有价值。应把真正优化的对偶目标和boundedcoeff含义写清，供读者重建solver；训练free与推理额外forward成本分列。数据母集规模不能代替测试清单，GPT物理评分与真实接触/执行应分开命名；F7rewrite错误及F8caption条件应交代，避免选例含义超出可控变量。

## 实际阅读范围

完整v1HTML正文§1–5、AppA1–A5全部（20页PDF版对应范围），T1–5全部行、F1–10全原始PNG视觉、Eq1–18；补核F3五扫参/F6残余物理问题/F7rewrite/F8文字条件。PDF下载多次超时未完整，网页PDFmetadata确认20页；全文阅读依据完整HTML和图assets，无本地完整PDF阅读声明。论文无官方repo链接、有限组合检索0/HF404；未找到SCO实现，未审各底座原repo为SCO实现。核心三遍/五项书面完成，无生成/judge/速度复现。

## 低维优化解释（本仓库推导）

令A的两行为aᵢᵀ，d=c−Aδref。从Eq13消去ξ，可写成 .5||δ−δref||² + ΣᵢMᵢ[cᵢ−aᵢᵀδ]₊。其对偶是框内凸二次目标 min .5μᵀGμ−dᵀμ，0≤μ≤M，恢复δ*=δref+Aᵀμ。这说明预算M是slack的线性惩罚所对应的对偶上限，并不保证最终硬条件全满足。论文给了软primal却未明写此对偶目标，正文Eq9+12的求解表述需要实现澄清。

这项推导审查不涉及模型运行，也未为第三方补写一个冒充官方的实现。四预测的近似NFE记账仅在明确的同成本假设下成立，不能代替实际GPUwalltime。

追引CFG/CFG++/TCFG/UniversalGuidance、SenseNova/DuoGen、OpenING/ISGBench、VideoWorld2/Cosmos/IRASim及书写prefix研究；物理评分提高与真实机器人执行成功保持不同证据层级。
