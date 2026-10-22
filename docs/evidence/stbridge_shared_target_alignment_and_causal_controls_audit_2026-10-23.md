# STBridge：共享目标、差分奖励与因果对照

第一百五十批完成[L137](../reviews/L137.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/stbridge_shared_target_alignment_and_causal_controls_audit_2026-10-23.json)。357目录（330论文／研究、27资源），259核心/262书面含未通过项；未确认核心71论文／研究+27资源，资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[arXiv版本](https://arxiv.org/abs/2607.17140)、[v1完整PDF](https://arxiv.org/pdf/2607.17140v1)。

## 研究问题

源图Is和编辑指令x输入同一UMM后，文字分支描述的目标状态与图像分支真正编辑的状态能否一致，并改善静态图理解/生成/编辑？编辑图It同时作目标图及其caption的语义锚；未直接验证写字视频/动作时序。RISE Temporal为静态未来状态编辑。

## 现有不足

共享架构不自动保证文字描述与生成视觉内容对齐：可出现描述新增自行车但图中未加、图已水彩化但描述漏风格、caption太稀疏。直接全图caption-image相似可能被不变背景主导，局部编辑信息不充分。共享目标、差分奖励和顺序优化分别针对配对关系、局部变化、两路径训练。例图诊断不能独自证明共享目标是全部协同瓶颈。

## 贡献

把目标caption和编辑目标图组织成同一目标状态的两种表达，BAGEL上三阶段后训：共享目标CE+FM监督；仅caption GRPO以源图相对目标差分为reward；固定caption策略后以多维编辑reward训练图像MixGRPO。主要新增是目标表示和后训接口/奖励设计，不是新视频模型或已证通用架构定理。

## 输入、模块、输出和公式

Stage1：Qwen3.5-35B-A3B仅看真实It生成c*t，模型由Is,x预测caption(CE Eq2)，由Is,x,c*t预测目标图(FM Eq3)，两loss相加Eq4。Stage2：Is,x→K个ĉ，不rollout图像；VLM(Is,ĉ)推断隐含编辑差分Δhat，与由Is,It离线制备的Δ*对齐，GRPO只更新理解分支Eq5–6。Stage3：冻结caption策略预测ĉ，图像策略在Is,x,ĉ下采样编辑图；裁判看Is、生成图、指令，给编辑/细节/保留/质量/偏好五个0–4分，MixGRPO更新图像分支。Eq7–10 b=Σs/20、g=.1+.9(sedit+spreserve)/8、R=b*g；裁判图未明确以ĉ或真实It作为输入。最终部署/独立两路径评测须区分。

## 结构与冻结范围

初始化BAGEL checkpoint并用其codebase，保留AR目标文字与连续latent flow图像两路径；正文未另报新层/参数数或精确共享参数冻结掩码。Stage1CE teacher forcing目标caption，再FM条件图像；Stage2图像冻结，Stage3文字冻结，若共享attention/embedding如何分组冻结需发布实现核定。不能把后训流程重命名为全新统一骨干。没有视频时间维/笔画token/执行器。

## 数据来源、选择与分布

SFT直接用PickNano-250K SFT split257730，无额外过滤/重采样/类别分层，目标图teacher caption。Fig8实际SFT全局风格43%、对象26.6%、场景构图18.5%、人物7.8%、文字编辑4.1%。Fig10/12却称示例Pico-Banana-400K并同引39，两名称和split派生映射未明确；ref39为Pico-Banana。RL15349=8000理解转编辑+7349ThinkEdit-RL多轮子集(EditThinker)。前者QA→标绿近点/灰远点、裁框、对应绿勾、网格(+5,−8)平移；四粗类各25%，Fig11称示例Flickr30k但完整QA来源/切分未列，不能据此确认泄漏。后者按编辑类型分层，保留首轮3≤score<7，用选定turn源图/指令/改进目标；Fig8对象44.7%、人物26.4%、场景10.2%、文字8%、全局6%、其他4.6%。两轮RL均用全15349混池。400对alignment评价池来源/split未齐。

## 指标和裁判角色

BLINK14类、CVBench2D/3D、VisPuzzle、MMVet、MMVP、OddGrid、WISE、ImgEdit、RISE共9个命名benchmark；结论写seven与列表不齐。理解准确/子项，WISE世界知识生成评分，ImgEdit/5和RISE编辑分；不构成视频/字符笔顺指标。WISE裁判Qwen3.5-35B-A3B/vLLM，RL裁判122B-A10B，alignment裁判Gemini-3.1-Flash-Image-Preview，三者角色须分清。§5.5 400对上分别由Is,x调用caption分支和直接图像编辑分支，未写将本次caption喂图像分支；裁判对比二者global与五项fine(实体/属性/部件/空间/交互属性)。Fine为五项均值、Overall=(global+fine)/2，即global占50%，每fine占10%。.9000是加权一致分，不能当90%独立任务成功；两输出可一致地错，需额外目标oracle。

## 基线与缺失对照

主要BAGEL原模型/SFT/RL同初始化比较；RISE另列GPT-Image1/1mini/1.5/2、Gemini2.5-FlashImage、NanoBananaPro、Qwen-ImageEdit2511。商业版本/自身跑或引用口径、完整推理预算不齐，无法自动算同条件SOTA。SFT消融SourceCaptionOnly、TargetCaptionOnly、SharedTarget；reward消融DirectCaptionTargetAlignment对DiffReward。没有等图像监督量image-only、错配/不配对caption、同预算separate/shared模型、顺序/联合/逆序和stage3-only析因。

## 实验条件

64GPU=8节点×8/FSDP用于三阶段，GPU型号未给。SFT500step/perGPUb1/global64、lr2e−5余弦min1e−6、EMA.995、sample/globaltokenlimit35000；不能据500×64断言看遍257730，因为packing细节不足。CaptionRL300步、GenRL150步，lr5e−6、512²、max32768tokens，裁判Qwen3.5-122B-A10B/vLLM。K、采样温度、GRPO clip/KL、MixGRPO窗口/噪声、NFE/CFG、各stage token/GPU时/judge开销、seed/CI未齐；35Bteacher与122Bjudge也需成本计入。ref40实为Qwen3技术报告，不能代替3.5精确checkpoint配置。无官方code/model/data发布链接在论文和有限title+GitHub/HF检索得到核实；此为检索范围，不断言全球不存在。未运行。

## 主结果与局部回退

T1BLINK BAGEL60.88→SFT63.85→RL66.03(+5.15pp)，计数74.17→75.83→73.33、拼图83.33→83.33→82.67、IQ30.67→33.33→30均低于base；forensic37.88→43.18→37.88。T2 CV2D78.01→77.98→79.20，count71.83→70.18→70.56仍低；CV3D81.08→81.75→83；VisPuzzle34.75→35.25→35.50、MMVet63.3→63.9→64.6、MMVP69.3→71.33→72。T3OddGrid36.57→39.21→41.71，各五类均升。T4WISE62.8→63.3→64，但文化78→68→69、时间63.33→63.33→63回退。T5ImgEdit3.42→3.57→3.88，style4.51→3.88→4.39、compose2.67→2.48→2.36、action4.25→4.12→4.10低于base。T6RISE15.8→32.9→36.8(+21pp)，逻辑1.2→1.1→1.9仍极低；STBridge低于GPTImage1.5/2/NanoPro51.4/49.4/48.3，高于Gemini2.5Flash33.9。总体改善不意味着所有能力/子类改善。

## 对齐及消融

T7alignment base/SFT/RL：global.6190/.7985/.9418；presence.6648/.7558/.9275、attr.5374/.6819/.8534、part.3857/.5998/.7618、spatial.6080/.7613/.9153、interattr.4489/.6721/.8330；fineavg.5290/.6942/.8582，overall.5740/.7464/.9000。未给人审/裁判重复/区间。T8BLINK base60.88/SourceCaption57.20/TargetCaption56.27/Shared63.85：caption-only不足，shared同时多了图像FM/条件/监督，不能唯一归因为正确配对。T9base60.88/SFT63.85/Direct63.88/Diff66.03，Diff比Direct+2.15pp，但count/jigsaw/reflection/forensic/IQ反而低于Direct。Diff行全部14列与T1最终RL行相同，而该节称TargetExpression优化，是否均含后续imageRL需stage-checkpoint对应。没有阶段独立表、等预算随机/错误pair、门控及teacher消融。

## 局限和公式审查

target caption训练与预测caption条件存在exposure gap；差分裁判依赖外部VLM和离线真实目标，不能称完全无监督。Align高分不保证编辑正确/不丢小字、稀有实体，caption覆盖率/长度和同族judge偏差需控制。Eq10门控是软权重：五分(edit,detail,preserve,quality,pref)=(0,4,4,4,4)得b.8×g.55=.44，高于全2分的.5×.55=.275；这是公式反例说明未硬性要求编辑与保留均成功，不是实际rollout失败率。400对协议分别生成，训练caption条件链的推断行为未由此直接测出。数据split/源、成本、冻结分组和最终stage身份不齐；没有显式Limitations节，仅结论未来跨模型/数据/超越编辑，上述边界为本审查分析。局部回退与9vs7、PickNano/Pico命名不应被总分掩盖。

## 预期优势条件

在源图和指令可确定清晰目标、目标caption足够覆盖编辑/保留、teacher和reward能识别局部变化且算力足够时，共享监督与差分相对背景占优的全图reward预期提高细粒度编辑和两个独立路径一致分。现有单BAGEL静态图实验支持限定点估计，未证明共享骨干本身、顺序机制或所有UMM皆受益；对规范笔顺/视频要建立独立时序目标和oracle。

## 可证伪实验

在同底座/图文监督量/总token与所有judge+rollout预算下，SharedPair对image-only、等量未配对、随机错配和caption直接prompt增强；SFT×captionRL×imageRL全析因，联合/正序/逆序及独立对shared参数。分别测试独立双路径、预测caption条件链、GTcaption条件链，报告一致与目标正确二维表/细节覆盖。固定高背景相似但局部OCR/数量/位置相反的反事实集，对差分VLM/直接分数/人标oracle、caption长度控制和弱teacher。门控与硬阈值/几何均值等同预算比较，观察edit0仍获高分的实际频率。公开QA去重split/400pool、3seed分层区间、holdout新裁判；视频扩展用同终图不同笔顺/事件轨迹真值，单列RGB可观测性、动作可执行与文字识别，未执行。

## 写作逻辑和Claim

Introduction用架构共享仍语义不一致→三类可见失败→共享目标概念组织；Data先统一QA/编辑接口，再Method三阶段及奖励，最后总体/对齐/消融，假设到证据较清楚。学习其把任务输出和训练接口画全；写Claim须限定总体/子项与所用裁判，说明训练caption条件链和独立评测两种调用。consistency不等correctness，softgate不等硬保证，“seven”/数据别名/引用checkpoint须内部统一；未专列Limitations时也应单独写局部退化、成本和依赖。

## 实际阅读范围

v1完整28页PDF20807281bytes，Abstract/§1–6完整研究正文(p1–24)、Eq1–10/T1–9/F1–16及全部图注；实际查看p1/2/3/4/5/7/8/10/11/12/13/14/15/16/19/20/21/22/23/24共20页，包括全部框架/数据/奖励/定性/主表消融，其他正文文字全读。p25–28参考定位追引不等逐篇精读。abs版本/HTML核对，论文出链及title+GitHub/HF有限检索未确认官方发布，未读不存在于已取得资料的训练配置/权重/源实现，未下载权重/运行/复现。

## 三句话概括

架构共享后，描述的编辑目标和生成图仍可能不一致，背景还会主导全图相似分。STBridge用同一目标图派生caption作监督，再顺序优化caption差分和图像编辑奖励。BAGEL上多项总体分及独立双路径一致分提高，同时计数、文化和部分编辑子项回退，机制归因仍需等预算析因。

## 五个关键问题

1. 当前问题是静态编辑的目标表达和视觉实现不一致。
2. 作者认为共享架构/独立任务监督及全图相似无法显式约束局部目标，例图和有限reward消融提供支持。
3. 共享目标监督补配对接口，DiffReward聚焦源图相对变化，顺序RL尝试先表达后实现。
4. 目标caption覆盖充分、编辑可观测、裁判可靠的静态任务下预期受益；视频/笔顺不在已证范围。
5. T8共享训练同时多了FM监督，T9阶段身份需澄清，T7测独立输出一致；应按上文任务正确×一致矩阵及预算析因验证。

## 一致评价的协议边界

训练阶段明确有目标caption条件链。§5.5却分别从同一源图和指令调用文字与图像分支，没有明确写把本次文字输出喂给图像分支。该实验支持两个输出的裁判一致分改善；不能代替完整预测caption→编辑链的成功率，也不能说明二者共同满足外部真值。

## 软门控的可检查例子

Eq10中编辑0、其余4分时奖励.44；五项全2分时奖励.275。公式允许前者排序更高。它仍会软惩罚编辑和保留，是否抑制实际reward hacking需要记录分项分布、零分高奖励频次和人审，不能只用名称“gate”推断硬约束。

## 追引队列

Pico-Banana-400K/PickNano-250K派生、EditThinker/ThinkEdit-RL(arXiv2512.05965)、MixGRPO(2507.21802)、EditReward(2509.26346)、ThinkRL-Edit(2601.03467)、EditR1/Leveraging verifier-based RL in image editing(CVPR2026 pp34343–34352)、Steering visual generation with understanding supervision(2605.05781)。先按作者/DOI/别名去重再补读；此次仅定位参考，没有把这些项计成完成精读。
