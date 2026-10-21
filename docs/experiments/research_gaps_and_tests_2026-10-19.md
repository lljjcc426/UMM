# 可证伪实验计划：严格笔顺视频、绘图智能体与过程/外观耦合

目标限定为：**具有清楚规范版本的汉字，在可观察、保留笔画身份的视觉条件下，从真实像素帧读懂已执行笔画，并继续产生可证实符合要求的书写过程。** 参考 [旧 SO 试验方案](stroke_order_pilot.md)、[新前作矩阵](../evidence/scoped_literature_matrix_2026-10-19.md)。

## 1. 理论与任务边界

记指定合法书写序列集合为 G(c,locale,script)，笔画实例为 k，实例轨迹为 p_k(u)，画布状态为 I_t。扩散/flow solver 内部时间不同于视频帧 t 和已执行笔画事件 k。对于墨迹集合并，不同事件顺序可能产生相同 I_T，故单从 I_T 无法识别实际历史。在视频原始帧里，采样不足仍可能导致历史不可识别。

考虑多个书体规范与合法集合，不能把书法家的行草写法用单一简体楷书顺序判错。需要区分规范正确、与真实记录一致、最终图可读、工具动作合法和机器人真实执行成功。

## 2. 研究疑问 → 方法 → 可反证实验

| ID | 具体已知前作 | 本项目待验证的不足 | 最小假设及反证 |
| --- | --- | --- | --- |
| SO1 实际过程识别 | VidScribe A1/A2；Calligraphy Bench Agent 笔顺评分 | 最终读对和外观形状无法唯一反演执行历史；视觉裁判输入尚不充分明确 | 同末帧合法/交换/反向视频，输入全帧 vs 最终帧；若全帧仍不能提升，则当前视觉信号/感知训练不足 |
| SO2 实例匹配 | BCSS per-stroke masks；AnimCJK 轮廓；Stroke-Seg | 交叉、同形重复笔无法由全局笔类 ID 区分 | oracle mask+事件 vs 自动 mask+事件；评估误差传播，若 oracle 即失败，优先改生成/表示 |
| SO3 动作执行 | VideoSketcher、OnOff、Wan 视频扩散 | LLM 所计划 stroke 与 RGB 实际出现顺序可能不一致 | 给完全相同的真值有序轨迹，比较 VideoSketcher 风格基线、控制视频 DiT、硬约束渲染 |
| SO4 共享收益 | InkSight、UniCalli、Lance、UniVideo | 仅把理解和生成串联不能证明联合训练收益 | 同一底座/数据/标注预算：只生成、独立理解器+同生成器、联合训练、共享特征切断；若独立方案等效，缩小 UMM 创新主张 |
| SO5 工具日志 vs 像素 | Calligraphy Bench 工具绘制 | 结构化绘图动作可以保证/记录序列，RGB 输出后难以从稀疏帧重建 | 对同一轨迹导出完整 action log、高 fps、低 fps 三条件；统计真实可观测性并给不可观测区间 |
| SO6 行草泛化 | KanjiVG、AnimCJK、书法资源 | 规范地域与连笔跨域会使单一匹配器误判 | unseen 书写者/字体/地区的开放合法集合评测；报告原规范失配 |
| SO7 效率 | DiffInk 少步样本、CausVid/VideoSketcher AR | 生成加速可能丢失短笔和抬笔 | 固定同 latent / 相同步数 / 帧率，画质量与严格顺序/显存/总延迟四指标 |
| SO8 视频-动作 | Wuji Writing VAM | 数字机器人执行示教未覆盖中文任务与严格规范 | 先比较人类参考时间配准、配动作头/不配动作头；无法拿纯视频 PSNR 代替笔顺 |

## 3. 数据构造及排除泄漏

优先用**有序矢量真值**产生可审查合法历史及控制负例。字符集覆盖二、三、王、玉、田、国、必、点折交叉包围等；选择包含同类笔多实例及易同终态误判情形。每个字存 norm_id、script、variant、允许顺序集合、实例轮廓、中心线/速度（如有）、每帧新增 ink、笔接触/抬笔、视频帧时间、渲染器参数、相机/遮挡元数据。

负例分层：两笔交换但末帧相同；单笔反向；漏笔；重复笔；两笔同时出现；先画多字后回跳；接触断续；有手遮挡与强风格、模糊/压缩噪声。**不能只生成 random permutation 当真实难度分布**；真实自由视频的失败须另外标注。

分三种数据来源且不混淆：规则 SVG（规范合成）、真实 online 原始采集（行为记录）、普通 RGB 视频（像素观测）。BCSS 的实例 mask 可以作空间监督但无真实事件序列；CASIA-HWDB2-line 静态行图不提供笔顺。Calligraphy Bench 真实 API strokes 可借作结构化参考，须审裁判口径与许可。

训练/测试拆分按字符、组件频次、书写者、字库来源、渲染引擎、地区规范和风格家族组织。测试同个字的多风格时必须明确 seen-character vs unseen-character 两种难度。所有视频生成方法至少保存 3+ seeds 的完整输出、参数/提示与原始视频；统计变异，不凭“最漂亮样本”胜出。

## 4. Baselines 对齐表

| 基线 | 实际获得的输入 | 输出 | 哪些指标可直接算 | 不可以拿什么硬比较 |
| --- | --- | --- | --- | --- |
| Rule SVG（AnimCJK/Hanzi Writer） | 字+SVG 真值+样式 | 确定性笔画动画 | 规范顺序全对与渲染缺失 | 不能把它当自由高保真艺术生成 |
| VideoSketcher（计划+视频） | 文本/步骤及其笔刷条件 | RGB 逐步绘画视频 | 视频真实事件/观测率、视觉质量 | 不可借内部计划当真实输出 |
| 受控视频 DiT | 真实有序笔画 mask/trajectory | RGB 视频 | 执行遵循度 | 与文本-only baseline 同表前应区分 oracle 信息 |
| Calligraphy Bench Agent | 参考图+stroke API | 有序工具路径+最终画面 | 工具动作顺序、几何、时间 | 与没有工具的 RGB 视频同名指标未校准 |
| 专门在线轨迹模型 DiffInk/OLHWG | 文本/风格/布局 | 轨迹+笔状态 | 轨迹事件及样式 | 直接宣称其生成了写实像素视频 |
| Ketaba/Qari OCR | 静态书写图 | Unicode 文本 | CER/WER | 笔顺率、视频延迟 |
| Wuji VAM | 人视频+机器人 proprio + 三视图 | 机器人多视图+54维动作 | 动作误差、预测视觉 | 0–9 数字机器人指标充当中文字模型效果 |

## 5. 最低可复核指标：定义分母和弃权

- Strict whole-character order：笔画实例匹配一一对应、规定合法序列、方向与 pen-state 均正确的整字样本数 / 全部评测字样本数。另报告不含 pen-state 的 order-only 版本，避免改变门限偷换名称。
- Matched-stroke order fraction：匹配成功的笔画中正确位次的比例。它和 strict whole-character order 不可互换，须列对分母、匹配失败率；适用于和 Calligraphy Bench 对照口径讨论。
- First-error accuracy 与 prefix-state Jaccard：模型识别真实首错位置和真实已写实例集合。合法规则建议和“实际观察到了什么”分开标注。
- Direction accuracy / Contact F1 / Completion recall：针对实例方向、接触事件和新墨迹覆盖度。
- Observability：因抽帧/遮挡/伪影不能确定顺序的比例；同时报告可观测子集上的准确率和**全样本中可确认正确比例**。不可观测情况不自动记为正确。
- 漂移与破坏：已完成区域像素保持、意外新墨迹、字体/颜色匹配；FID、CLIP、OCR/CER、VBench 或 VidScribe 因素分数作为辅助指标。
- 计算公平性：硬件/GPU时、NFE、每帧采样、重试、VLM/规则/渲染器调用、编码器/检测器耗时和总显存峰值。偏好选最优多样本应与同样总采样数对照。

## 6. 实验阶梯与最小可发表主张

**E0 评价器合法性：**构造 64 字×多个正负序列及相同最终像素对；人工二次标注并对不同 fps 做混淆矩阵。先证明评价体系对反例有效，且独立人工标注的一致性可接受。64 字只是 pilot，正式测量另做统计效能评估。

**E1 识别：**full video、sparse frames、final frame、oracle event stream、shuffled frames，固定理解器以排除顺序记忆。随机标签负控确保模型无法从视频外目标字线索作弊。

**E2 执行：**给 oracle 动作控制，严格复核输出的 RGB ink diff；测规划信息丢失与低帧率假错。若规则执行器能覆盖需求，则选择简单方案，不预设生成模型优势。

**E3 联合训练：**共享 UMM vs 强连接器 vs 专门轨迹加渲染，固定真实前缀、训练数据、总计算、推理预算，做跨任务有无损协同分析；报告准确率差与显著性而非笼统提升。

**E4 失败案例：**依据漏笔、错序、短笔、重复横、连笔、交叉、密集、多字等聚类；只有存在稳定拖累因素且已查竞争方法仍不足时，才设计新机制。例如跨帧结构化笔事件记忆与可控视觉执行回读，需切断事件状态/切断回读两项消融以说明作用。

## 7. 写作要求与完成条件

每个 claim 对应原文表格或本项目复现实验；方法未测的机制写为**假设**单列，避免在摘要中将“理论上”表达为既成事实。Introduction 采用现象（严格可观察）→强基线具体失败→为何既有信号缺失→目标→方法→可复现实验。Method 在给模型组件之前定义状态、条件信息和控制是否 oracle。Experiments 展示主要匹配预算对比、困难分层、统计变异、真实耗时、错误修复案例和至少两项机制消融。Limitations 简洁列不可观测样本、规范约束和算力，不反复插入空泛免责声明。

**阶段判定**：至少两个任务维度和三种基线输入协议跑通之后，再决定是否需要发明新 UMM 机制；当前实验结果尚未产生。

## 历史状态与匹配计算

新增对照：densehistory、recentwindow、UniLongGen分层筛块、scene路由/持久anchor、oracle任务状态。对逐笔过程保留必须累积的状态，按远程回访/细节大小/错误历史分层；原生规划与固定文字分协议。所有probe、anchor、外部planner、CFG、prefill和生成步计总成本；同时报告状态/字符/事件正确与静态视觉质量。

## 顺序来源与状态监督

固定图文内容和曝光，比较CLIP匹配重排、DOM顺序、随机序、教程步骤及真实笔画事件时间。理解/图序列/连续RGB/动作分开评价。编辑对照保留源图—改动Pareto曲线、局部OCR/状态检查；DPO同时报告文字和图像退步，打乱负例允许多种有效顺序。

## 动作与世界对照的补充

书写应比较动作only、文字计划、正确/预测/打乱未来帧、相机几何和共享训练；同动作/数据/compute并记录观测刷新率。对高频动作表示扫频带/精度/端点；几何camera自评加独立标定，重力锚不替代接触动力学。公开脚本与论文超参各自记录，先复原匹配协议再谈改进。

## 交错中间状态的因果验证

对生成图/latent进行保留、移除、随机、GT替换，固定文字前后文与预算；配同内容文字及规则渲染对照。图token、NFE、latency和多候选选择成本完整计算。绘画/文字以真实事件时间标签测结果，不能用去mask顺序或回答正确率替代笔顺。

## 结构监督和条件信息对齐

同标准内容轨迹/字形框/参考作者给各基线，明确附加输入；结构目标用正确/错配/随机teacher全因子并固定总更新/数据曝光，计伪标和额外训练成本。同终态不同笔序的反事实检查静态识字与规范事件是否可辨；分别测轨迹/终态/RGB过程。配对基准加GT/移除/打乱中间图，固定真实计算预算，近似base不当严格因果对照。

## 生成帮助的四种替代解释

结构teacher监督、更多后训练、额外中间图信息、更多测试计算应逐项控制。按同源图/同曝光/同更新比较seg/depth/edge/pixel；按同dropgate和同总NFE比较AdaViG/SCO。对共享bit与最终像素分别提问，检查decoder改变细节；笔事件时序与推理索引严格分开。

## 新直接前史下的强基线

L186图拓扑/宽度/机器人执行和N08分层O2O/书写动力学均已有研究，新增笔顺或运动prior本身不足以建立创新。比较适配宽度的TrajFormer、GHTR、层级O2O、规则SVG及视频模型，固定控制链与信息输入；笔序/方向/接触/时间误差独立于静态OCR/FID。latent闭环另测最终RGB，以独立encoder/judge验证，防止自洽代理替代真实任务。

## 已有同图改序控制与指标冲突

[L011 Draw This First](../reviews/L011.md)已经固定图像/seed、改caption来检验order，区域τ.838、part.461、pass.444，withinunit较低，必须作为直接前史。下一实验应细到strokeID/方向/抬笔并同时统计碎片/漏笔，不能只复做粗区域顺序。OnOff的CVL图像FID改善同时CER变差；文字/字形/顺序/执行分别评，报告Pareto。VidScribe A2为空间字形拓扑，VTR最清楚出现的WER没有覆盖完整时序，加入终态同形换序/反向/重画反例。[专题](../evidence/calligraphy_video_text_order_and_ocr_protocols_2026-10-20.md)列已有实验与待验证的真正增量。

## 统一接口、自适应控制与指标分母

UniVideo冻结MLLM的理解成绩不能证明联合训练改善理解；Lance图像OCR GRPO不能直接证明视频逐帧持字改进。共享/分离模型需固定数据/总参/compute、prompt改写与采样预算，分别报告理解、生成、笔画事件和执行指标。VidSketch公开入口固定adapter强度，新增固定、论文阈值、实际自适应三组对照前先补完整版本。Calligraphy Bench笔顺分母为匹配笔画X，漏笔可能不受该项惩罚，应同时报N、X、Y和全目标归一Y/N；39行count差异先逐项追源，不能直接把现有评分判错。


## 第三十批补充

视觉OPSD需同初始化SFT/直接关闭生成/真实cropteacher，分离特权信息与生成分支来源。SVG动画对照需固定输入版本和候选总预算；正反loop不能做不可逆墨迹强基线。机器人RGB需比较真50Hz与3Hz因果保持，计划action与测量state分开评价。


## 第三十一批补充

新增同几何仅换顺序/方向与同顺序变宽/采样率两个隔离实验；真实目标prefix与独立同作者reference分开；VAE重建与下游扩散生成双诊断。闭合轮廓转中心线误差需独立报告。


## 第三十二批补充

区分新字符、新作者、新script少样本迁移；风格测试critic用测试作者监督需多critic校准。合成增强对齐样本数/优化steps/新表达分布；模板index置乱实验检继承顺序。软形态先验证极限/梯度并比较硬minmax和简单edge正则。


## 第三十三批补充

动态文字/绘画加入静止终图、淡入、逆擦除和随机顺序基线；真实时间统一标定，终帧外观/曲线/有序区域/笔事件分开。共同数据/预算/信息比较，GT与预测条件干预，ε与x0 glyph目标及DF×layering独立消融，loss权重Pareto和cluster人评CI。


## 第三十四批补充

比较UMM和独立双模型按同active FLOPs/同total参数分别配平；固定阶段因素追规模曲线。ReCA类后训用相同输入token数/算力语义与随机特征干预，测复制与跨任务迁移；共享模型I2T曝光保持一致，罕见字符/计数/事件单独评。


## 第三十五批补充

同physical engine联立画质/managedKV/peakVRAM/延迟；同byte预算策略与动态预算消融。反思固定root/image/renderer/noise换文字，text/flow更新2×2、多seed/独立judge，独立critic+renderer按同总FLOPs配平，repair/damage/stop均报。


## 第三十六批补充

同预算比SSTA AND/OR、Glyph、联合/顺序AV和register、VCU adapter/全参、轨迹坐标/random/latent/ControlNet；测控制误差与全管线时延/显存。轨迹输入sample/average、数量和冲突seed配平，换跟踪器/人工GT分离条件误差；规范书写补墨迹增长与pen-contact/事件。


## 第三十七批补充

同初始化/teacher/prompt/kernel/总FLOPs测TF/DF/SF×exit×cachegrad；SGF加梯度夹角和writer冻结，Salt混步×SC×TRD完整因子、reference可靠性/700vs600warmup。同步测长语义、动态/identity和事件CI，任务RL补奖励各项、合法多解、提取器人工核/删墙攻击；bestK披露选择器及总预算，Target代理/几何/执行分列。


## 第三十八批补充

同VAE/teacher/backbone/总FLOPs比较MF/iMF/Shortcut/FM，目标×辅助v×weight×结构×长训独立消融，CFG只在独立验证集选并披露搜索预算/训练ω外推。SGF+同参数加宽shared/双LoRA/梯度投影对照，补长semantic/动态/薄笔事件与聚合角色梯度。CP低方差×CTM/DSM×dropout×mesh和实际encoder/通信/执行计时，规范多模式和接触/漏笔独立评价。


## 第三十九批补充

离散FM同tokens/FLOPs/precision报PPL+entropy+代码或事件成功及延迟/吞吐；F5启发对齐需固定实际场评估数、参考条件、solver/CFG/vocoder，Sway不作物理时间控制。TeaCache独立70prompt校准及ROI/全局proxy、等延迟solver/cache对照，记录总成本和短笔漏失。clDice补同mask不同笔序、桥接/断连/交叉/多组件，固定实际k/α验证选择，全图+patch拓扑与时序事件共同评估。


## 第四十批补充

F01–F04补静态渲染器×剪增×opacity×逐层因子，固定实际参数/时间并分列单步与整图开销；标准SVG导出前后边界/透明度/层次检验；真实/理想renderer与闭环开环在同工具/动作/时间预算比较。CoFRIDA模拟差需真实执行检验，补风格同量FT/能力FT/分层/共享UMM，按真人中间画布/材料留出，统一语义差并保留neither/both。相同最终图不同合法/非法笔顺是空间指标反证，需事件方向/接触/短笔Recall共同测。


## 第四十一批补充

补G014统一Nmax/EOS mask的KL因子与长序列/画者留出；G015固定renderer/奖励密度/总笔/FLOPs拆modelbased×bundle×WGAN；F05固定上游测试外观—识别权衡与全链路CPU时延、正式偏好界值；H001先恢复版本/alpha再做无LoRA/fullFT/LoRA与真实执行，不能据结构兼容宣布性能。


## 第四十二批补充

同renderer/笔数/算力预算比RL、逐图优化、集合与自回归；拆采色vs颜色学习、全局/patch、image/L1/W/BCE、OT分辨率/迭代与过程奖励。分别报单笔/终图/结构/事件/物理执行、训练摊销/推理，乱序同终图检验评价。CLIP评价需独立识别/人类；重复测量采用参与者聚类统计。


## 第四十三批补充

同数据/架构/吞吐/算力拆mean/ε、目标权重、VE/VP/subVP/OT路径、solver/NFE；固定checkpoint，多训练seed与多采样重复分开，报NLL定义/MC误差/去量化K、FID参考和墙钟。RF拆reflow次数×端点对量×L2/LPIPS×蒸馏，计teacher数据/存储并完整画高低步曲线。文字视频分t/τ，增加事件/近形字/乱序同终图反例；尚未运行。


## 第四十四批补充

固定E-D与latent／noise seed，拆f×潜通道、DiTblock×patch、CTscratch／teacher-init×LPIPS／L2、DPM／++×ε／映射／NFE；等样本／墙钟／质量分列，teacher与decoder／LPIPS预训练及τ／ε搜索计成本。报告rFID／FID／PSNR／sFID／recall及独立OCR／拓扑／真实笔事件，反例保持同终帧。未运行。


## 第四十五批补充

固定E-D/SD/CLIP、参考统计/样本数/fps，拆joint独立帧比例×等样本/墙钟、replacement/重建引导×含corrector反传成本、时间层/时间D/插值×全参/冻结、共享motion/domain/LoRA×兼容域。负指标与重建/生成分列，加静止复制/同终图乱序/瞬时出现、OCR/细线拓扑/运动幅度/事件可观测性；未执行。


## 第四十六批补充

固定潜元素预算控制空间/时间压缩×channel，先重建OCR/拓扑/GT差分与事件可见性，再生成。full/factorized×参数/计算、Expert/MMDiT×等参数/等层、EUS×rank/seed；筛选器书写保留率、caption时间密度与字面保真、LoRA rank×alpha/r对SFT按等样本/墙钟控制。记录预编码/cache与训练/验证峰值、全推理成本。未执行。


## 第四十七批补充

Wan实验须保存默认负提示（空值会回填“字幕/画作/静止”等）与重写原文，控制专门文字数据和一般OCR过滤的域保留率。原RGB→3fps采帧→VAE重建逐级测OCR/细线/笔事件；原版50步、缓存/FP8、四步Streamer分设条件。偏好校准和独立任务/模型heldout分开，以静止/乱序/反播等相同末帧反例测代理指标；未执行。


## 第四十八批补充

适配实验固定版本/模块/数据与验证搜索预算，rank×γ×lr及等参数/等墙钟双控制。DoRA加m-only/direction-only、norm完整导数/detach；QLoRA分BF16/NF4/DQ/paged。测实际更新/梯度、GPU/CPU/迁移/时延以及独立OCR/细线/笔事件和跨作者泛化；异常低分先核解码/提取/稳定性。语言训练PPL或SDXL静态例图不替代过程评价；未执行。


## 第四十九批补充

ControlNet结构×prompt完整/缺失/冲突×control单/双支×实际RW分开，真值/提取条件控制上游误差。CFG引导×步数/求解器、训练dropout独立；记录NFE/墙钟/峰值、OCR/事件/多样性和稀有文字覆盖，验证选Pareto后锁test。原二维条件无法区分顺序，需要相同末帧反例和时间接口；未执行。


## 第五十批补充

对抗视频/绘画目标需多seed稳定/覆盖和D/G协调控制、真假指标独立事件反例。VAE按同码率/潜维比较，分posterior重建/prior/骨干生成及均值/采样，测细线与事件时标，分别控制KL/感知/对抗和q族/推断预算；不以重建loss或ELBO单项替过程。未执行。


## 第五十一批补充

过程评估以同终图错序/反播/漏笔/同时增墨/静止匹配反例，分局部墨迹与背景相机运动。固定fps/长度/分辨率/压缩、评价特征/层/预处理/N/裁片及context，分训练seed和子集CI；人评按prompt/作者/模型留出，报可评覆盖率与事件真值，不以通用总分代笔顺。未执行。


## 第五十二批补充

ContentBias已有时序敏感性/冻结重采样研究，不能直接当新颖缺口。对同终图错笔序的局部事件测试，加入I3D/VideoMAE与独立人类校准；匹配空间扰动、背景/镜头、帧率/片长/压缩和唯一样本数。开发参考调选择，独立参考测试并报权重有效样本量；不能只以同评价参考下降证明生成改善。未执行。


## 第五十三批补充

按默认/统一输入像素与比例两种设置、同预算/提示优化记录比较；构造单帧保真后漂移、错序、闭环镜头和短事件。对代理face/外观分类报告覆盖NA与有效N，按prompt/模型层次CI；开发集调阈值、独立人类/事件真值校准。未执行。


## 第五十四批补充

对通用事件评价加入原始/改写×同预算因子、条件/全体成绩和coverage；同终图错序、逆向、伪接触、只运动不留墨，独立事件真值，按文字/作者/生成器留出和高fps局部评价。未执行。


## 第五十五批补充

共享/分离/部分共享×单多任务在相同样本暴露与实测总计算两种控制下比较；patch×图像数×外围等参、噪声×loss权重，报各任务Pareto、重建细字上限、跨字/作者/文字体系泛化及人评计数/CI。未执行。


## 第五十六批补充

encoder共享/解耦×骨干共享/分离×单/多任务，固定上游预训与实际预算，保留语义蒸馏及单任务强基线并报Pareto/CI；AR/掩码/连续diffusion对齐CFG实际强度和图码数，测真实延迟而非轮数。视频加入GenHowTo/规则SVG/渐进绘画及错序同终图负例。未执行。


## 第五十七批补充

同终图多历史/可接受集合，检测oracle×文字条件×跨脚本，保留空输出fallback覆盖/成本；几何/真实样本等预算消融，fps/时长/有效帧规则与阈值敏感性，LLM评委目标词汇/顺序交换及人工事件时间校准。均未执行。


## 第五十八批补充

同LLM预算比较表示并单报解析coverage；协作等信息/笔画控制和跨概念/起笔者分层。ProcessPainter合成/真实样本/两阶段消融、ARN×逆噪2×2和配置对齐；末帧、风格、密集stroke事件分别评价，全部未执行。


## 第五十九批补充

按原视频/艺术家分组留出、固定后端partition×step投影和跨查询一致性；依据允许的数字编辑分层，不泛用单调增墨。矢量表示同预算、Fixer修补代价、等价SVG与跨prompt独立指标，全部未执行。


## 第六十批补充

保持count不变重排事件构造反例；静态感知/OCR与事件顺序分列。先对齐warmup/lr/batch/维度，再同预算多seed消融；guidance在validation择参、test冻结，盲评固定素材，全部未执行。


## 第六十一批补充（2026-10-21）

同预算全因子/独立validation、多seed；直接生成图OCR、纯生成训OCR、混合数据增益分开；独立content-probe、行长/语言/作者分层、cluster人评，公开精确推理/样本量与预训成本。尚未执行。


## 第六十二批补充（2026-10-21）

同最终checkpoint与等总预算专门/双模型比较；控制分词器、prompt重写/后处理/分辨率，数据×策略因子与同stageIII步数的规模对照。书写域测OCR/motion过滤保留率、4×时间压缩短事件重建、顺序/方向/RGB可观测性与真实执行。仅方案未执行。


## 第六十三批补充（2026-10-21）

AnyText固定数据/底模做标注×mask×感知loss×社区模型因子，测全图额外字与未见语言/字符；UniVid核split/VBench版本后做同总API/帧/token预算的选帧/反思、保序/缓存、score/feature-gain与真实scheduler步对照，加入短笔画事件和校准。仅方案未运行。


## 第六十四批补充（2026-10-21）

合成教师/含text提示与同Wan配对、全视频逐帧文字及过滤率；双模式loss/ID因子与LoRA/full-ft同预算、字符×作者/作品/style留出；相同mask/NFE强修复对照、已知错误区与可纠错冲突、专门等效检验。方案未执行。


## 第六十五批补充（2026-10-21）

图像修复按实际NFE/延迟匹配往返vs slow，mask面积/细线/已知错笔分层，缺失正确/已知保持与纠错/整字合法/真实感分列；可控线性模型扫描lambda与误差地板。仅Th8总体矩局部数学审计已运行，其他训练/推理/实验未执行。


## 第六十六批补充（2026-10-21）

Veo固定rewriter与帧干预、同预算selector/oracle、无效类比严格计错；N07层交互CI/混合模型和错误修订单列；N13同文件人机/词长先验/轨迹oracle、音画偏移/FPS与合成实录配对等效。全部方案未运行。


## 第六十七批补充（2026-10-21）

U08提出同信息文字/GT图文/自生成/纠错/跳过回读的同预算因子实验；按源/题/模板去污染和跨任务留出，逐轮状态错误、最终答案、无效覆盖、成本/CI分列。BAGEL错图回读解释需受控干预，严格笔顺再另测事件。全部未执行，既有视觉推理纠错方法仍需查新。


## 第六十八批补充（2026-10-21）

G030同骨干交叉独立噪声/teacher forcing/self rollout、fused-SNR/stack/历史噪声，固定NFE/墙钟比较MCG与多未来基线；测字符事件漂移与视觉/执行，maze补first-hit/碰墙。理论先修正KL符号与明确表达条件。全部未运行；D05/D06及History-Guided后续须查新。


## 第六十九批补充（2026-10-21）

G038补足可变历史引导前作：同骨干/训练预算做SD/BD/DF/reduced，历史长短/自生成误差与噪声分层；同NFE/显存/墙钟对比HG-v/f/t与额外采样。严格笔事件、身份、方向、执行与视觉质量共报，动态量不代替正确动作；人工选路/插值与自主成功率分开。均未运行。


## 第七十批补充（2026-10-21）

L086/L092共享收益检验需固定预训/teacher，分别匹配每任务曝光与总FLOPs，加入同任务额外数据/计算对照及多seed；先测VAE重建上限，再测书写身份/顺序/方向/执行。同一接口与单幅GenEval不替代过程收益；实验均未运行。


## 第七十一批补充（2026-10-21）

G027迁移先固定checkpoint/初噪比较等NFE和墙钟的积分器，报身份/事件/方向与FID完整重复值；高NFE参考隔离数值误差。训练预条件×噪声×权重×增广全因子及同预算搜索，字符变换跟踪身份与坐标。未运行。


## 第七十二批补充（2026-10-21）

L185后续须同rollout/FLOPs/teacher墙钟比较优化器，因子化更数/交替频率、sum-vs-mean密度/clip、KL与earlystop；训练奖励外独立人评/OCR/事件及数字文字欺骗测试，保留同终态错序/反向/罕见字。未运行。


## 第七十三批补充（2026-10-21）

L001同骨干联合/后排序×起点来源、匹配复杂度/点密度并测方向/contact；L004 layout×MS四格、真/预测/扰动框，直接测CER/WER/词距/漏词与pen事件。两者同终态错序/反向、多seed，视频GT不能由静态恢复器自证。未运行。


## 第七十四批补充（2026-10-21）

Painter同预算开环/反馈/残差/事件、注入漏笔测恢复、Pile×规模控制；StrokeFusion norm×box×视觉输入×image loss，保长尾/匹配复杂度，统一FIDweights/PR球并集/k/RDP，再测合法顺序器/AR/规则SVG及反向事件。方案未运行。


## 第七十五批补充（2026-10-21）

部件库同人工预算/未见部件连通结构留出；逆序视频同骨干预算/首末锚定剥离、原始笔事件vsmedian、艺术家/channel留出、人评参与者×作品层级统计与明确test-as-val映射。transfer单/双模型含teacher总成本；未运行。


## 第七十六批补充（2026-10-21）

同teacher/数据曝光/训练与搜索总FLOPs分离joint-vs-separate、终图/多轮/双critique，反馈屏蔽与错误critique干预、正确未完成vs错误标注、质量-NFE/token/秒数曲线与理解遗忘；严格事件禁擦除，实际规范次序/方向/停笔。方案未运行。


## 第七十七批补充（2026-10-21）

女书同源句/书页去重固定split、真实字体/书家留出、原始CER/EM和轨迹事件监督对照；Stroke-Seg ID重编号/gold-pred-noisy识别、count/ID拆分、class/multilabel/loss全因子及同类相交实例，公开一对一匹配/阈值与总识别成本。未运行。


第七十八批（2026-10-21）：补等额外2.4K步的时序/字幕干预、同数据预算共享消融、同prompt/RICES/后处理和全部退步分项；加笔事件与RGB指标，方案未运行。见[审查](../evidence/versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)和[单篇L075](../reviews/L075.md)、[L077](../reviews/L077.md)。


第七十九批（2026-10-21）：补同码率细笔/OCR、单样本/四选一、Gumbel多seed、版本/额外数据和继续训练控制；测语言保持及事件时序，未运行。见[审查](../evidence/lavit_dynamic_tokens_and_version_audit_2026-10-21.md)和[单篇L079](../reviews/L079.md)。


第八十批（2026-10-21）：补等teacher/分辨率/码率/计算的tokenizer因子实验、细字/OCR与完整采样成本；未运行。见[审查](../evidence/uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)和[单篇L072](../reviews/L072.md)。


第八十一批（2026-10-21）：补共享索引全因子、等调用/等延迟与真实联合LLM正负迁移；未运行。见[审查](../evidence/tokenflow_shared_indices_and_claim_audit_2026-10-21.md)和[单篇L094](../reviews/L094.md)。


第八十二批（2026-10-21）：补等数据/等算力联合迁移、余弦与梯度、跨集近图去重及同终态异轨迹对照；未运行。见[审查](../evidence/metamorph_synergy_and_data_budget_audit_2026-10-21.md)和[单篇L090](../reviews/L090.md)。


第八十三批（2026-10-21）：补同checkpoint数值对照、同骨干文字/glyph及同终态异事件分层验证，未运行。见[审查](../evidence/diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)和[单篇G022](../reviews/G022.md)。


第八十四批（2026-10-21）：等预算全成本、teacher/蒸馏、VAE短事件上界与LoRA配置对照，未运行。见[审查](../evidence/diffusion_efficiency_full_pipeline_audit_2026-10-21.md)和[单篇G023](../reviews/G023.md)。


第八十五批（2026-10-21）：等预算共享/专家、噪声端点和联合一致性、非汉字与事件检验；未运行。见[审查](../evidence/unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[单篇L076](../reviews/L076.md)。


第八十六批（2026-10-21）：等预算编码/融合/课程、绑定负对照和同终态异过程/接触留墨检验，未运行。见[审查](../evidence/tora_motion_binding_and_process_boundary_audit_2026-10-21.md)、[L034](../reviews/L034.md)/[L035](../reviews/L035.md)。


第八十七批（2026-10-21）：2×2路径×loss、独立事件标注/同轨迹不同声音、等预算adapter与offload主机成本方案，未运行。见[审查](../evidence/tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)、[G039](../reviews/G039.md)/[R12](../reviews/R12.md)。


第八十八批（2026-10-21）：等40K步课程、相机×对象全因子、静止/接触/留墨与独立提取器方案，未运行。见[审查](../evidence/motionctrl_camera_object_and_observability_audit_2026-10-21.md)、[L039](../reviews/L039.md)。


第八十九批（2026-10-21）：共享正负迁移、同候选成本、真实/生成音频history和open/closed-loop对照，未运行。见[审查](../evidence/unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)、[L058](../reviews/L058.md)/[L059](../reviews/L059.md)。


第九十批（2026-10-21）：同码率/总预算/CFG/源图旁路、数据成分及flat/history可证伪对照，未运行。见[审查](../evidence/seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[L060](../reviews/L060.md)/[L061](../reviews/L061.md)/[G040](../reviews/G040.md)。


第九十一批（2026-10-21）：全样本自由识别、等参数平滑基/drive/部件/静止区域/DC与非周期书写对照，未运行。见[审查](../evidence/semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[L051](../reviews/L051.md)/[L052](../reviews/L052.md)。


第九十二批（2026-10-21）：等底座预算/候选、D/显式OCR、style量/字体混合及heldout组合和过程评价，未运行。见[审查](../evidence/dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[G041](../reviews/G041.md)。


第九十三批（2026-10-21）：接口/显式问答对照，等FLOPs/曝光两组，codec/后处理与同终态异事件；未运行。见[审查](../evidence/metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[L062](../reviews/L062.md)、[L074](../reviews/L074.md)。


第九十四批（2026-10-21）：causal/bidirectional×自由/强制32码，等追加LoRA/全参预算、同生成条件蒸馏、跨文字codec；未运行。见[审查](../evidence/seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[L078](../reviews/L078.md)、[L082](../reviews/L082.md)。


第九十五批（2026-10-21）：等K/辅助先验排版对照、等信息与等context轨迹对照，motion反事实/上游误差及强底座多seed；未运行。见[审查](../evidence/timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[L053](../reviews/L053.md)、[L054](../reviews/L054.md)。


第九十六批（2026-10-21）：等调用/独立盲审造题；同感知和曝光的坐标/投影/画框/legend/轨迹，ID时序与漏检干预、总成本；未运行。见[审查](../evidence/autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[G042](../reviews/G042.md)、[G043](../reviews/G043.md)。


第九十七批（2026-10-21）：等分辨率/token率/两套预算的hybrid对照及旁路消融；跨生成器/艺术/字体独立校准评价、完整样本和逐图结果，笔顺另加事件真值；未执行。见[审查](../evidence/manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)、[L064](../reviews/L064.md)、[L071](../reviews/L071.md)。


第九十八批（2026-10-21）：分阶段等预算非劣/模态对齐；等decoder交错/RL消融、质量延迟曲线、独立人评和状态/事件/接触干预；未执行。见[审查](../evidence/qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[L065](../reviews/L065.md)、[L066](../reviews/L066.md)。


第九十九批（2026-10-21）：同内容/异内容同错事件配对；oracle/生成/注错history和同题/分辨率/预算、多seed，人评双真值；原评分与修复版分开，模型实验未执行。见[审查](../evidence/xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[L067](../reviews/L067.md)、[L068](../reviews/L068.md)。


第一百批（2026-10-21）：固定同题直接/辅助回答、oracle/预测框、GT/自判停止2×2、逐轮初值Δ和预算；书写事件规范与状态可见性独立测量。未执行模型实验。见[审查](../evidence/unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[L069](../reviews/L069.md)、[L070](../reviews/L070.md)。


第一百零一批（2026-10-21）：相同专家/数据/FLOPs的caption/连续接口和单目标/联合、冻结UNet停止梯度对照；书写事件/可见状态双标注。未运行模型。见[审查](../evidence/nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[L080](../reviews/L080.md)、[L081](../reviews/L081.md)。


第一百零二批（2026-10-21）：固定encoder/decoder/FLOPs分离规模、压缩/目标、检索与同格式示例；细笔画可重建性、事件状态与完整采样成本。未运行模型。见[审查](../evidence/emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[L083](../reviews/L083.md)、[L085](../reviews/L085.md)。


第一百零三批（2026-10-21）：反事实诗词/改字/遮挡与作者内容互斥；oracle轨迹、降fps/噪声和设备外域、同预算强基线；书写事件另行标注。未运行模型。见[审查](../evidence/callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[L045](../reviews/L045.md)、[L046](../reviews/L046.md)。


第一百零四批（2026-10-21）：同基座/codec/token/FLOPs的共享/独立/增普通数据控制；50K匹配教师调用、去评价/改图/推理及多seed细粒度分项，尚未执行。见[审查](../evidence/liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[L088](../reviews/L088.md)、[L089](../reviews/L089.md)。


第一百零五批（2026-10-21）：同目标/预算课程与恒定mask、逐奖励和BoN/拒绝采样SFT、GT/预测码与有序文字/布局评价，多seed待执行。见[审查](../evidence/ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[L091](../reviews/L091.md)、[L093](../reviews/L093.md)。


第一百零六批（2026-10-21）：同码率/初始化/预算连续与离散接口、固定/在线权重、单/双码/双encoder/等容量head控制、梯度与细字/时序评价，多seed待执行。见[审查](../evidence/qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[L095](../reviews/L095.md)、[L096](../reviews/L096.md)。


第一百零七批（2026-10-21）：正确/欠指定/违规输入、独立judge/raw偏好、多seed；边界与prompt分离、同NFE、真实物理及preview控制、笔尖/旧墨迹锚定，未执行。见[审查](../evidence/motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[L036](../reviews/L036.md)、[L037](../reviews/L037.md)。


第一百零八批（2026-10-21）：等总bit/同骨干的无/量化/连续/打乱参考，重建与预测分开；空白起笔/已有字/新显露与静态复制/错时、终态参考泄漏控制，未执行。见[审查](../evidence/reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[L038](../reviews/L038.md)。


第一百零九批（2026-10-21）：同mask/同数据预算的区域/常量/随机/DINO/CLIP/DIFT，课程与Gaussian拆分、分割/轨迹误差、背景/物理/笔画事件独立评价；未执行。见[审查](../evidence/dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[L040](../reviews/L040.md)、[L041](../reviews/L041.md)。


第一百一十批（2026-10-21）：oracleOCR/关联/路由分解、受控错误/批顺序/采样密度、配对多seed与可见覆盖率，书写时变墨迹/事件GT；未执行。见[审查](../evidence/textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[L042](../reviews/L042.md)。


第一百一十一批（2026-10-22）：同预算无/静态/错时glyph与位置token、Oracle上游/误差注入、严格整串与可读覆盖、corrected人评；书写事件另建GT，未执行。见[审查](../evidence/vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[L043](../reviews/L043.md)。


第一百一十二批（2026-10-22）：同SigLIP先验/长度/FLOPs表示对照、固定曝光比例、统一prompt交叉与多seed双任务Pareto，未执行。见[审查](../evidence/unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[L097](../reviews/L097.md)。


第一百一十三批（2026-10-22）：同码率/LLM/数据/renderer和FLOPs的RL替换、独立奖励评价器及真实书写事件；仅理论反例，未运行模型实验。见[审查](../evidence/selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[L098](../reviews/L098.md)。


第一百一十四批（2026-10-22）：同LLM/曝光/码率/FLOPs空间-query×mask对照、独立文本集和盲人评；全部未执行。见[审查](../evidence/ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[G044](../reviews/G044.md)、[L098](../reviews/L098.md)。


第一百一十五批（2026-10-22）：等词表成本/码率/数据级联对照、真实q/H和训练曲线、独立OCR与同终图异过程GT；未执行。见[审查](../evidence/unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[L099](../reviews/L099.md)。


第一百一十六批（2026-10-22）：等总FLOPs与等任务曝光共享对照、多seedPareto、短接触/抬笔事件GT；未执行。见[审查](../evidence/tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[L100](../reviews/L100.md)。


第一百一十七批（2026-10-22）：等bits/FLOPs与等曝光的因子消融、多seed/真实联合熵、独立OCR/事件GT；未运行。见[审查](../evidence/uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[L101](../reviews/L101.md)。


第一百一十八批（2026-10-22）：等bits/容量/FLOPs的4/4与4/16和16/4、多任务Pareto、教师/decoder干预与事件GT；未运行。见[审查](../evidence/evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[L102](../reviews/L102.md)。


第一百一十九批（2026-10-22）：等Nd/FLOPs/上下文预算、PathI/II冻结与容量控制、细字OCR/未改区/完整两级成本；未运行。见[审查](../evidence/unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[L104](../reviews/L104.md)。


第一百二十批（2026-10-22）：等全部预训/FLOPs、mask×预算/规模、重建额外微调、偏好原票与attention干预，未运行。见[审查](../evidence/tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[L105](../reviews/L105.md)。


第一百二十一批（2026-10-22）：对VLM-only、匹配容量辅助任务、R条件与共享梯度的等成本协同检验，未执行。见[审查](../evidence/representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[L106](../reviews/L106.md)。


第一百二十二批（2026-10-22）：mask×压缩全因子、teacher预算、STI与LLM容量替代及书写事件/FPS测试，未执行。见[审查](../evidence/hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[L107](../reviews/L107.md)。


第一百二十三批（2026-10-22）：p×τ×head×CFG、等15K继续训练和F8目标子集/事件对照，未执行。见[审查](../evidence/pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[L108](../reviews/L108.md)。


第一百二十四批（2026-10-22）：同初始/数据/墙钟的mask-remask、距离、AR编辑及错对转移，多seed；事件与RGB顺序对照未执行。见[审查](../evidence/fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[L109](../reviews/L109.md)。


第一百二十五批（2026-10-22）：M×width全因子、ground等token替补、反思等墙钟/BestN和VQ文字重建上限，未执行。见[审查](../evidence/lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[L111](../reviews/L111.md)。


第一百二十六批（2026-10-22）：cache质量-时间-显存Pareto、等曝光RL与模板OOD、区域RGB误差/复合基线，未执行。见[审查](../evidence/lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[L112](../reviews/L112.md)。
