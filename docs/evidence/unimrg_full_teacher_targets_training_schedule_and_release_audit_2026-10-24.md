# UniMRG：完整教师目标、训练计步与发布制品审查

第一百八十五批完成[U19](../reviews/U19.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/unimrg_full_teacher_targets_training_schedule_and_release_audit_2026-10-24.json)。358目录（331论文／研究、27资源），290核心/295书面含未通过项；待完成核心深审41篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2601.21406v3)、[主源2](https://arxiv.org/html/2601.21406v3)、[主源3](https://arxiv.org/pdf/2601.21406v3)、[主源4](https://zihan-su.github.io/UniMRG-Project/)、[主源5](https://icml.cc/Downloads/2026)、[主源6](https://github.com/Zihan-Su/UniMRG/tree/0493c6dd3661d6d8bc1fde143fef91238eef2777)、[主源7](https://modelscope.cn/datasets/Sugewud/LLaVA-Instruct-150K-UniMRG)。

## 研究问题

对已有UMM进行四任务联合后训练，生成RGB重建、相对深度和对象边界能否增强理解，并维持图像生成？重点是额外稠密教师目标通过共享参数带来的理解收益，推理理解直接回答，不要求先生成深度或分割图。

## 现有不足

RGB重建偏纹理颜色，对几何与结构约束弱；仅理解SFT可能遗忘图像生成。DepthAnythingV2与SAM提供几何/边界监督，作者尝试用原生成头学习它们而不加推理模块。尚需区分教师知识蒸馏、额外训练量和使用生成目标本身的独立作用。

## 贡献

架构通用的后训练配方：理解CE加pixel/depth/seg三种生成目标，沿用各骨干原生成loss；在Harmon/OpenUni/Show-o三个模型上比较baseline/SFT/RecA，逐步累加目标消融，1K合成图教师一致性测试。无新tokenizer/基础生成理论/推理模块；已公开Harmon实现、预处理数据入口及评测适配，未提供三骨干完整对应实现。

## 输入、模块、输出与公式

输入RGB经理解encoder得h，拼任务prompt→文字答案、原RGB、DepthAnythingV2相对深度三通道图或SAM白边黑底图。Eq1理解CE，Eq2–4对应三图目标原骨干loss，Eq5四lambda均1。推理与原UMM一致，无必须额外生成的理解开销。Eq6–8 AR/MaskGIT、9–13DDPM、14–17FM、18–19MAR是预备知识；FM独立noise/data线性路径称OTpath，未证明全局最优传输耦合。Eq20逐图minmax归一化为0–255，不是米制深度。

## 模型结构

Harmon1.5B共享MAR视觉表示，文本AR+连续latent的maskedautoregression/小diffusionhead，paper384²；OpenUni3.6B=InternVL3-2B与SANA1.6B经query/connector桥接，512²，理解视觉encoder冻结；Show-o1.3B CLIPvariant、VQ4096codebook，文本因果AR而图像maskedprediction，512²，不能简写成纯因果AR图生成。论文称冻结VQ-VAE及textencoder/decoder，图3textdecoder冻结图示与实际LLM边界需澄清：公开Harmon配方freeze_llm=False，MARencoder/decoder和proj全部False即可训练，VAE冻结且no_grad编码；配置注释decoderfrozen与布尔值相反，按执行值记录。

## 数据分布与划分

论文使用LLaVAMix665K与LLaVANextData理解数据，未充分说明各骨干精确混比/去重/留出。公开Harmon仅配置llava_v1_5_mix665k.json；depth/recon/mask从有image字段的每条QA条目取图，不去重，重复图随条目再采。DepthAnythingV2ViTL生成相对深度，论文518²cubic后resize回原图/bilinear、minmax、复制三通道。SAMViTH自动1024点、IoU.88/stability.95/NMS.7生成无类别mask，最终只存白边黑底，不能当语义类别/实例ID图。代码run_mask用Canny100/200并取边缘并集，maxsize2048后最近邻回原尺寸；外部教师仓库/checkpoint版本未全pin。ModelScope API确认公开数据仓、README列JSON/RGB/depth/mask四项，StorageSize约134.7GB，未下载全量检查样本/许可证传播。

## 指标与评价协议

理解MMBenchEnglishdev、MMVP、HallusionBench、RealWorldQA、VSR，VLMEvalKit；公开README明确MMBench_DEV_EN与VSR-zeroshot。图生成GenEval与DPG，T4含GenEval六分项。OOD随机1KMidjourneyV6，以1−MAE比DepthAnythingV2教师图，测教师一致性及合成分布迁移，非独立真实深度GT/米制几何准确率；minmax影响尺度解释，缺常数图/简单边缘/教师以外GT对照。未给多seed/CI或全部judge版本、采样与checkpoint选择依据。

## 对比方法

每骨干Base、仅UndSFT、Und+RGB的RecA、UniMRG；T2列相近LLM参数量的理解/UMM模型，但总参数、预训练、视觉分辨率不等，且BAGEL3B行缺具体checkpoint，不能当常见7B版或受控架构结论。缺同教师目标的轻量直接预测头/表征回归、等数据等计算重复RGB、错配或简化教师目标、四loss全因子。OpenUni另加pixelonly阶段需各对照保持一致后归因。

## 实验条件和发布边界

论文8H20：HarmonAdamW1e−5、每GPU每任务16/四任务共64、acc4、4000steps约5h；OpenUni1e−5、每任务4/共16、acc4、2000steps，再冻理解pixelonly3000steps约30min，总约3h；Show-o1e−6、每任务2/共8、acc5、2500steps约8h，teacher预处理成本是否计入未明。公开Harmon HEAD0493c6d树66项/40blob，37文本文件下载，重点训练/模型/数据/预处理/评测路径审读：默认512²、max_iters10000、batch16、repeat[1,1,1,1]，sampler轮流发四个同任务微batch，CollateConcat每次一任务、accumulative_counts4累积；不能把四任务64和acc4再直接相乘套给代码。TrainLoop来自xtuner0.1.23，未运行计步，记录loaderiter与optimizerstep口径待对齐。四losscoeff1但grad_scale默认.1缩理解和干净条件zenc梯度，maskedtarget路径并非完全相同scale；同权不等各模块同梯度。AdamWbeta.9/.95、WD.02、clip1、bf16、1%warmup+cosine、seed42非deterministic、每500iter保存且save_best=None。公开训练与论文384²/4000步差别不等于历史跑错。

## 主结果

T1三骨干UniMRG相对Base七指标全升。顺序MMBench/MMVP/Hallusion/RWQA/VSR/GenEval/DPG：HarmonBase50.43/60/46.69/46.67/60.88/71.37/80.52→52.23/62.67/49.32/51.90/61.21/85.26/85.27；OpenUni81.19/71.67/60.88/65.23/66.69/61.13/79.41→81.44/74.67/64.56/66.01/73.90/68/81.78；Show-o47.85/50/46.06/38.17/54.26/67.32/81.94→48.11/51.33/47/39.87/54.42/71.40/84.55。HarmonSFTGenEval.30/DPG2.85显示该设置严重遗忘；不能推所有理解训练必塌。RecAHarmonGenEval83.86/DPG86.61，纠正旧笔记把86.61当GenEval的列错读；UniMRGDPG低RecA1.34。OpenUniRecAGenEval70.07→68，Show-o71.52→71.40；并非所有指标优于RecA。T2OpenUni版在所列五理解指标均优各有分数对照，但预训练/总容量未控。

## 消融及进一步实验

T3累加Und→+pixel→+depth→+seg，并非全部组合因子；+depth50.60/62/48.26/50.46/60.39/85.15/84.96，full52.23/62.67/49.32/51.90/61.21/85.26/85.27。VSR从RecA59→60.39仍低Base60.88，full仅较Base+.33；论文not harminggen同时给DPG86.61→85.27，须报告下降。F5仅SFT噪声、SFT+D偏灰、SFT+S边界、SFT+D+S+P恢复自然图，两例说明RGB保留作用但缺量化全组合与预算控制。F6教师一致性Harmon.623→.822/OpenUni.617→.834/Show-o.637→.664。F7四例Show-o后训练输出全黑；codebook4096限制属作者解释，未做同模型codebook容量干预，不能因果确认。T4HarmonRecA→Ours六GenEval项3升3降，colors92.82→89.63；OpenUni仅count55→55.94升、其余5降，position36.08→29.42；Show-o4升2降，two90.82→90.07/attr55.08→52。

## 局限与疑问

额外teacher训练知识与generation共享目标机制未分离，联合四目标有效不证明深度/分割是必要充分条件；固定训练步也未确保同总tokens/FLOPs。公开代码仅Harmon，训练分辨率/步数/冻结说明/提示词与论文不完全齐：depth5模板、mask15、recon364，对论文depth/seg各10。Und使用灰色padding保比例，depth/recon/mask默认cropFalse先方形拉伸，故不同任务同源图几何预处理不一致。recon unconditional.1只换通用文字prompt，仍保留源图条件，不是真正无图条件。生成入口默认GenEval每prompt12图/DPG4、64MARiterations、CFG3、temperature1、512²，README默认checkpoint均指base，须显式替换finetuned；GenEvalmetadata需外部准备、评分委托外部RecA/GenEval/DPG仓，未pin完整评测栈。模型HFpaperAPI关联制品为空、repo无finetuned权重且README仅base下载，不能称已核UniMRG线上权重；公开预处理数据已确认。无原始逐题分数/多seed/CI，无法判断.16/.25pp小增益显著性。边界图无类别、深度teacheragreement非真实几何，Show-o容量解释与生成中介作用未证。

## 预期优势条件

已有UMM兼具强连续图生成器、能分出独立辅助任务且有稠密teacher时，可在不加推理架构的情况下联合学习几何/结构并缓解遗忘。向书写迁移可用骨架/部件/笔画实例或有时间的轨迹教师，但白色轮廓缺笔顺与交叉笔归属；深度在平面文字未必有用。艺术字可考虑结构骨架与RGB风格互补，素描视频应另给prefix状态/下一笔和时间监督，不从静态边界推断动态因果。

## 可证伪实验

Q1理解提升来自教师额外知识还是生成机制：同初始化、同图/QA、同教师数据，比较原生成头多目标、轻量depth/edge预测头、特征回归、等计算额外RGB、无关/打乱教师目标；统一padding/resize与可训练参数，报训练FLOPs/teacher成本及梯度scale，做Und/P/D/S全因子并用独立validation选checkpoint。若直接头相当，主张收缩为辅助稠密蒸馏。Q2几何与容量解释能否成立：用真实独立depth/实例边界GT，报尺度不变误差/相对深度排序及edgeF1、常数黑图和梯度边缘基线，锁定1K清单与原始预测；同Show-o替换codebook容量而控预算/目标频率，检验黑图是否随容量改善，分开稀疏背景与语义结构。多seed按题/图clusterCI，OpenUni额外pixel阶段各对照相同并报分阶段指标，生成所有分项及退化；书写另测笔画连接/笔序/时序可执行性。均为建议，未执行模型。

## 论文组织与Claim学习

先用无法按指令生成depth/edge和错误理解例引出问题，再四目标统一公式、三骨干主表、累加消融、OOD和失败例，结构清楚。增益相对Base与相对RecA应分开，DPG下降不能被not harming概括遮盖；教师输出应称pseudoGT并说明知识来源。架构无推理新增不代表训练零开销，容量瓶颈假说需单因子实验；公开配置与论文计步/分辨率/冻结及采样协议应一表对齐。

## 实际阅读范围

完整v3研究正文§1–5、Impact、AppA.1–A.3/B.1–B.4/C共16页；T1–4所有行/分项、F1–7全部视觉、Eq1–20及任务/预处理/提示模板已读。固定官方HEAD66tree/40blob，37文本文件下载，完整README及Harmon训练config/model/HarmonDev默认loss、sampler/collator、LLaVA任务数据、SAM边缘生成、visualization和VLMEvalKitHarmon适配，训练入口/parallelGenEval关键路径审读；未称所有vendoreddiffusion文件完整审计。ModelScope元数据/README和HFpaper关联API已核，未下载134.7GB数据/运行训练或评分。核心三遍与五项书面完成，非口试/独立复现。

## 主张与可复现范围

旧笔记将Harmon RecA的DPG86.61读成GenEval，本批纠正为GenEval83.86/DPG86.61。三骨干UniMRG相对Base均提升，不能据此写成相对RecA所有生成指标提升。

公开实现可检查Harmon训练与推理路径，预处理数据有官方发布入口；OpenUni/Show-o对应训练代码和UniMRG微调权重未定位。当前配置与论文的分辨率、计步、冻结文字和prompt数量需作者对齐。本批不以源码差别指控历史实验，也不把元数据核验当134.7GB数据逐样本验证。

深度与边界teacher引入了额外先验。下一步需要直接稠密预测/表征回归对照以识别生成机制，追引RecA、ROSS、DIVA、DepthAnythingV2、SAM、Harmon、OpenUni、Show-o和书写结构任务；未自动改变追引条目验收状态。
