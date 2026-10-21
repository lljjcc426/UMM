# Lumina-DiMOO：缓存误差、自反馈与局部编辑的证据边界

第一百二十六批完成[L112](../reviews/L112.md)明确范围核心三遍/五项书面记录。[结构化证据](../../data/lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），235核心/238书面含未通过项；未确认核心95论文／研究+27资源。资源按制品协议另审。本批没有新增目录、删除文件、下载权重、执行模型或独立复现。

## 来源、问题与定位

以[arXiv2510.06308v1](https://arxiv.org/abs/2510.06308v1)的[完整33页PDF](https://arxiv.org/pdf/2510.06308v1)为准。Abstract/§1–8、Eq1–8、T1–10、F1–13图注全部核心研究文字已读，实际看p4/8/10/12/13/14/17/18/22/23/24十一页。未逐图核全部定性展示或逐篇参考文献。正式会场接收尚未独立核明；官方README的CVPR2026消息指向后续dMLLM-TTS，不能归给本作。

本作研究AR视觉采样慢、统一dLLM任务覆盖不足，以及双向注意力反复计算的成本。作者在LLaDA8B上扩视觉词表，结合四阶段多任务、并行mask采样、最大logit缓存和Self-GRPO。GenEval基础.88/自反馈后.91、DPG86.04等作者结果支持特定静态任务性能，同时存在任务退步、缓存误差与原协议缺项。

“Omni”在本版覆盖静态图文理解、T2I、多类I2I和局部重绘。视频/音频列为Conclusion未来工作，尚无规范笔画、真实绘画轨迹或文字书写视频的任务/指标。“Sketch Then Paint”是后续HT-GRPO对token学习层次的隐喻，不能归为已实现绘画视频。

## 模型、公式与运行过程

图像统一用aMUSEd-VQ：8192码、stride16；1024²图像4096原视觉码，另有64行末及prompt/边界。理解也读该VQ码，未并用SigLIP语义encoder。作者承认codec语义不足，依更多理解数据适配。LLaDA32层/4096hidden/12288FFN、32QKVheads、RMSNorm/1DRoPE；原文字126345加8192视觉及11新词条，发布vocab134548/视觉offset126356。[HF固定f014549e](https://huggingface.co/Alpha-VLLM/Lumina-DiMOO/tree/f014549e17679e41b119959754cdd9320af9bdc8)元数据8,081,805,312 BF16参数，不能视为含VQ的整个系统总参数。

行末符号保留宽高网格，对扁平1D序列显式编码行边界；“任意分辨率”仍受训练分布、长度、显存和stride约束。不能理解为任意大图无成本、原始像素信息无损。I阶段同时mask图文，II/III只mask目标；CE忽略条件位置。发布SFT用随机cosine比例、至少一处mask、masked-label平均CE及10%文字drop作为CFG训练。

图像全局mask，逐轮只对当前masked位置预测、采样和保留低置信mask，已提交位置保留。文字块内并行、块间依次，具有半AR依赖。正文Eq4使用当前mask数量L′t及ceil，公开generator用固定初始vq_len及floor，不能假定完全同协议。正文对已提交码置信设−∞的说法须结合选择域，源码在当前mask集合重mask，因此不会因此重新遮掉全部已提交位置。

ML-Cache选高最大logit位置复用K/V及输出logits，低值位置重算；有warmup与refresh。它明确是有损近似，F4单例logitscosine>.99不证明图像质量无损。最大rawlogit也非校准概率：每位置logits整体加常数不改变softmax，却能改变maxlogit排序。这一数学性质说明代理依赖表示标度；未证明所训练模型中该代理失效，需用质量-速度实验检验。

Self-GRPO从当前策略采G图，用提示提取的QA检验图像语义，再对生成轨迹选定时间步及理解答案loglikelihood加权，另加KL reference。式（6）\(w_g=\mathrm{softmax}_g(\alpha(r_g-\bar r))=\mathrm{softmax}_g(\alpha r_g)\)：公共均值严格抵消，所有权重非负；不能把该式叙述成零均值、带负优势的标准clipped GRPO。论文保留采样轨迹但只对所选步反传，式（7）的时间前缀对应采样轨迹，不能改写成图像raster AR目标。G、问题数N、alpha/beta和选步策略缺完整可复建细节；无oldpolicy不等于无reference/无采样开销。

## 数据、训练与全部主表

I约80M图文含公共重描述30M及先前Lumina数据50M；II增加3M图表/数学/UI，Qwen2.5VL重描述并混编辑/条件图；III理解15M/生成15M（含内部合成），另VisualCloze各200K、UniWorld编辑500K等。低层任务200K后作者仍报告效果差。IV用GenRef子集、近GenEval模板，DSG抽三元组制单选QA和近义干扰项。不能把II的Qwen描述自动写成IV全部QA教师；完整原样本/去重/划分尚未取得。

T2前三stage64A800，lr2e-4/2e-4/2e-5、b1024/512/512、AdamW(.9,.95)、constant/wd.1/clip1；RL8H20/b48/lr3e-6/AdamW(.9,.99)，固定1024且arbitraryres勾选为否。I256→512，II/IIIT2I1024、I2I512、理解动态512–1024。没有充分阶段总步数/天数/总GPUh，不能从数据量擅填训练曝光。采样CFG/NFE/精度须与各表协议分别核对。

| 证据 | 支持与边界 |
| --- | --- |
| T3 GenEval | .88→Self-GRPO .91；two .94→.96/count .85→.87/color .89→.95/attr .76→.82，position .85不变。基础two低OmniGen2 .95/color低GPT4o .92；正文FLUX .82与表.66冲突，可能协议不同但原文未解释 |
| T4 DPG | overall86.04、entity92.08/relation94.31强；global81.46/attribute88.98/other82低于多基线。不能由overall最高概括每个维度全胜 |
| T5 UniGenBench | overall71.12为该历史快照；text25.57低SD3.5 32.76/FLUX32.18。不能引用历史排名为当前全域SOTA |
| T6 OneIG-EN | 作者把overall定义五维平均，.455/text.551优所列，style.400低SANA .401/diversity.232低多方法；与T5文字分数评价尺度不同 |
| T7 TIIFmini | overall短71.27高FLUX71.09、长68.53低71.78；“第二名”需保留短长差异，Basic/Advanced/Designer各类互有胜负 |
| T8 Graph控制 | CannyF1 .38低mGPT2 .49/Omini .47/OmniGen .43/OneDiff .39，FID30.35差Omini29.58，SSIM .65高；DepthRMSE8.31/FID34.38强，但MANIQA .40低.49。图像质量/结构控制并非一个指标 |
| T9 style/subject/edit | style文本.32对Instant .27、风格.53对.60是+.05/−.07绝对差。subjectDINO80.57/CLIPI89.36强，CLIPT34.72低OneDiff34.80。edit Add3.82与UniWorld平、Replace3.83高；Remove2.76低UniWorld3.24、Style4.18低BAGEL4.49/OmniGen4.19 |
| T10 理解 | POPE87.4与JanusPro平，MMMU58.6与UniWorld平，SEED83.1强；MMEP1534.2/MMB84.5低BAGEL1687/85。所列MMaDA五项均低本作，但继承数据/预算不同，不能唯一归架构 |
| F12 cache | 图45→22s≈2.05倍，文字31.7→17≈1.87倍；显存38.9→45.9GB（+7GB）。AR mGPT710→22≈32.3倍已包含缓存，不能再乘2。AR图分辨率768²/720²、其他1024²；文字统一1024token，GPU/计时边界和质量同时约束仍需更充分公开 |
| §7.2 初始化 | 相同5Mgen+5Mund/256直接SFT，LLaDA-SFT对随机失败仅给定性观察，无曲线/数值/训练时长。主模型§3.2写Base，消融写SFT，必须区分。固定一种优化设置失败不证明所有预算下随机训练不可能 |

Self-GRPO只有T3完整前后对照，尚未显示理解同时改善、模板外泛化和选轨迹/QA奖励的独立收益。StageIV不支持arbitraryres，不能直接把基础模型全部能力视为已验证RL后仍保持。各表主要为作者报告，未独立复现。T6 BAGEL“AR”标签需按[C01](../reviews/C01.md)视觉连续flow纠正，不能传抄为全AR。

## 发布模型、配置与实际可复现性

[GH固定81344e6](https://github.com/Alpha-VLLM/Lumina-DiMOO/tree/81344e60545ae8d70f11039d3450717d974f831b)741项完整树、README/config/公开SFT训练与指定推理/cache代码已读，范围详L112；HF卡/config/VQconfig已核，Apache2标识已核，未作法律条文审读。未下载权重或运行。

公开T2I例64步/temp1/CFG4，源码为5cond−4uncond、每轮两前向；I2I cfgtext2.5/img4为三前向。cache .9/warm .3/refresh5示例在1536×768、A800报告58.2→32.2约1.81倍，不能混写F12的2.05倍。通用文字函数将steps按块数均分；README128token/32block与论文测速1024token/block256不同，不能混作同一延迟。

SFT yaml为用户数据路径占位，公开shell2epochs/clip4与T2clip1有差异，属于微调入口，尚不足恢复四阶段原训练；完整Self-GRPO训练入口未定位。训练代码中宽高变量赋值互换需与预提码格式核明，未据此断言原论文评测错误。

普通MMU generator早停判断HF eos126081，与正文“当前块完成并检测answer结束”未完全对齐，返回语句引用该模块未定义input_p_len/rows；所读作用域下触发存在问题，但未运行该分支。它也未接cache，不能声称发布默认MMU路径复现了1.87倍。另VLMEval wrapper已独立读全：预填answer_end和padding，只留一个答案mask，是选择题答案协议；不含普通generator的早停分支，也不能当1024token开放文本测速。不能将一个入口问题扩大为所有基准分数失效。

## 区域保持、写作学习与实验假设

正文“区域外100%保持”缺充分条件。令z=E(I)，只固定区域外码可令z′外=z外；一般不能推出D(z′)外=I外，因为D(z)本来就可能有VQ重建误差，局部改码还通过decoder感受野影响邻区。发布inpainting将中心矩形或反转区域映到latent格，未mask码保留，随后整图decode；画布paste只是前后并排展示，没有将原RGB外区贴回输出。严格RGB保持应测误差，或显式pixelcomposite并另评接缝/语义一致性。已有[RePaint/G036](../reviews/G036.md)也支持局部条件采样，不能把局部编辑本身直接当未解决的新课题。

Introduction按速度/统一任务覆盖切入，Method先codec/接口后目标、采样/cache，Training和Data分开，值得借鉴。Claim应把历史排名、近似cache、仅定性初始化和绝对分差写清；Limitations散在低层任务与结论未来方向，尚需集中说明局部保持、QA模板偏置和缓存误差。读者不能沿用“所有维度领先/100%”概括。

可证伪设计：同checkpoint/种子/分辨率/CFG/NFE与硬件扫cache参数，对比maxlogit/熵/margin/随机同复用量，测显存/时间/组合/细字OCR与错提交。RL用等曝光SFT、仅T2I/仅MMU/联合、同模型或外部judge、等预算BestN及选步消融；GenRef去重后测模板/词汇/组合OOD、理解前后与校准、训练多seedCI。局部编辑分别比较VQ重建、局部改码、全decode与pixelcomposite的外区maxL1、零变化率、边界和文字拓扑。初始化对齐总预训资源与可调优化参数，避免只对齐最后SFT步。均为未执行实验建议。

后续dMLLM-TTS（2512.19433）、HT-GRPO（2605.16842）、aMUSEd/Meissonic与相关cache原工作需按原始ID去重后独立读；本批只核官方链接/HTREADME，未把它们的论文结果计入完成。
