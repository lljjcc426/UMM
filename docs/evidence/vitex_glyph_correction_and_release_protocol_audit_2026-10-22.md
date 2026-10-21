# ViTeX：glyph结果纠正、三轴评价与当前制品审查

第一百一十一批完成已有[L043](../reviews/L043.md)固定核心三遍与五项书面记录，补全题名。[结构化证据及公开数字汇总](../../data/vitex_glyph_correction_and_release_protocol_audit_2026-10-22.json)。目录356条（329论文／研究、27资源），220核心/223书面含未通过项，136条未确认核心（含资源）。没有新增独立论文/资源、删除本仓库文件、下载权重/图片视频数据、执行模型或独立复现。下述统计仅使用公开文本清单及已报告数字。

## 来源与任务

固定[2609.40356v2](https://arxiv.org/html/2609.40356v2)，2026-10-11；已读Abstract/§1–8、Eq1–9、AppA–O全部研究文字和T1–13，实际核F3原框架、完整T2主表/T7消融。其他定性图只读图注，参考文献未逐篇读。PDF120秒仅取得1.77MB/6.99MB，不完整文件排除。

arXiv comments、作者GH/HF称NeurIPS2026 Evaluations and Datasets Track录用；有限官方会务/OpenReview检索未另确认，保留作者声明层级。[abs摘要](https://arxiv.org/abs/2609.40356v2)仍为旧CharAcc.688，核心HTML和当前完整glyph结果.714，需区分来源。

任务是给定源视频V、逐帧maskM、源串src和目标串tgt，在场景表面替换文字，同时保持时间质量和编辑局部性。Benchmark是主要贡献，ViTeX-Edit-14B是配套参考编辑器。规范逐笔出墨、空白起笔及共享理解生成UMM均未定义。手写文字外观的数据比例无法说明采集了手写动作过程。

最近旧工作STRIVE已在[L182](../reviews/L182.md)，关联而不重复计数。参考文献另提GlyphMastero和VidTextPres，尚需核原文和别名/目录去重；本批不将引用条目直接计为新精读工作。

## 数据与方法

387个真实源视频，720p/120帧/24fps；230训练配对、157冻结评价不提供编辑参考。Panda70M628/4322和InternVid200/3768经筛选再选387。SAM3交互mask经25²膨胀3次；Qwen3VL32B读取/提出近长度目标，Gemini3ProImage编辑首帧，removal1.3B去字，静态alpha或PISCO14B插入产生审核配对。230训练中56alpha/174PISCO；这与约25%静态/75%动态的分类口径不同，静态也可选PISCO。配对编辑是模型辅助参考，不是唯一正确外观。初期未保存逐条重试/拒绝统计。

eval150Latin/4中文/1日文/2Cyrillic；全387为印刷23%/手写44%/艺术33%。七个nonLatin例只能做小样本诊断，AnyText2 Seq.168/Char.295、其他Char<.19，不能推广各文字体系表现。

ViTeX-Edit冻结40层5120维Wan2.1-VACE14B DiT、uMT5和WanVAE；训练8VACE块、glyphencoder和条件attention，约4.02B参数。目标串通过uMT5，V/M通过96ch VCU。字体选择、EasyOCR四边形和CoTracker3构造目标glyph视频，按源运动做homography，VAElatent经stride(1,2,2)patch、64learnedqueries池化，再由各VACE块hidden读glyph并残差注入。

训练glyph仅检测/跟踪；纠正评价前增加mask有效性校验，149片跟踪（14片部分fallback）/8片全mask放置。训练两阶段：49帧720p、5epoch、repeat10、AdamW5e-5/wd.01；121帧2epoch、1e-5；有效batch64、8H10080GB/bf16/FM，约22+50小时=576GPUh。未包含基础模型预训和配对构造总费用。推理50step/CFG5/seed42、121帧去末帧。

当前glyphencoder在flatten后以learnedqueries汇聚全部时空latent，所核代码没有显式位置/逐帧索引。VAElatent可能已编码局部时序，不能据此断言全无运动信息；但“对齐glyph如何保持时间对应”需要错时glyph、VAE后token置换及有位置/逐帧条件的受控实验。

## 三轴指标的实际含义

| 轴 | 指标与边界 |
| --- | --- |
| 正确性 | PP-OCRv5按源脚本路由，置信.30；NFKC/upper后只保留Unicode L/N。SeqAcc要求目标作为预测子串完全匹配，CharAcc为fitting相似度，前后额外字符不罚，符号/标点/空白/组合mark会被移除 |
| 支持集 | 源OCR对src相似≥.5才入D；Seq/Char仅D，TTS只相邻帧均在D。5/157无D排除，152片贡献文字均值；稳定错字也可能高TTS |
| 视觉/时间 | full/crop各Flicker、源RAFT流Warp、MUSIQ；crop为整片mask并集固定窗口，cropMUSIQ只D，时间指标用完整片。平滑或静止可能低误差，不保证编辑成功 |
| 局部性 | mask内预测替回源，然后在全帧算PSNR/SSIM/LPIPS/DreamSim；它与单独在mask外像素平均不同，也受mask面积和编码影响 |
| 比较 | SeqAcc↑/Warp-c↓/DreamSim-loc↓作Pareto，无跨轴总分。SeqAcc0也可非支配，必须看编辑是否成功 |

八基线分四族：AnyText2/TextCtrl/FLUX-Text/RS-STE逐帧；TextCtrl+AnyV2V；WanVACE/VideoPainter；Kling3Omni。TextCtrl256²/RS32×128是bbox编辑贴回，其他多为全帧重建，不同接口带来局部性结构差异。VideoPainter源下采8fps、pad到49、去pad再线性插24fps，四项时间分标†并排除排名。

## 结果与消融：分别看均值、区间和配置

| T2主要行 | SeqAcc | CharAcc | TTS | Warp-c↓ | DreamSim-loc↓ |
| --- | --- | --- | --- | --- | --- |
| Source | .000 | .317 | .760 | 1.27 | .000 |
| FLUX-Text | .528 | .737 | .326 | 13.01 | .012 |
| TextCtrl | .475 | .734 | .511 | 2.09 | .004 |
| VideoPainter | .364 | .619 | .606 | 3.35† | .024 |
| ViTeX完整glyph | .363 | .714 | .658 | 1.62 | .020 |
| ViTeX text-only | .339 | .688 | .653 | 1.55 | .023 |
| ViTeX Composite | .361 | .718 | .664 | 1.61 | .003 |

完整glyph Char比VideoPainter高.095，但Seq略低；逐帧FLUX/TextCtrl文字准确均值更高。Kling最高MUSIQ仍Seq0。旧提交因加载器重初始化glyph/清零条件输出，生成实际无glyph；v2修正并将旧配置单列text-only，训练权重本身未被判损坏。

T7只在同权重推理时关glyph，未做重新训练的no-glyph模型。

| glyph开启减关闭 | 均值差 | paired95%CI | 可支持结论 |
| --- | --- | --- | --- |
| SeqAcc | +.024 | [−.025,+.079] | 区间跨0 |
| CharAcc | +.026 | [−.003,+.056] | 区间跨0 |
| Warp-c↓ | +.07 | [.05,.10] | 时间误差增加 |
| Flicker-c↓ | +.14 | [.09,.19] | 相邻差增加 |
| MUSIQ-c↑ | +2.39 | [1.94,2.93] | 所测感知分改善 |

未拆glyph运动/字体/池化、两阶段或训练规模。不能将推理消融概括为训练机制均有效。

Composite使用41²外环LAB统计、4px羽化、源像素恢复和CRF18编码。参考编辑器PSNR29.70→42.67dB、DreamSim.020→.003，Seq.363→.361；其他基线PSNR也趋约43，主要是共享后处理的源还原。全基线只报告支持的fullFlicker/PSNR，未完整重算文字/crop时间，不能另做Composite全指标Pareto。

## 校准、独立性与剩余冲突

源OCR校准exact.851/Char.966/TTS.760只是当前可读support背景，非所有target的上界。训练生成参考OCRexact.585/Char.790，人类读回Char.917/97%可读，仍有识别与渲染缺陷。

方法盲转录351crop由一位作者完成，排除9个nonLatin crop，catch32/36正确，方法级人/OCR Char排名ρ.95；三名非作者评70输出，三轴ordinalα.87/.80/.37，与Seq/Warp-c/DreamSim相关+.71/−.40/−.53。两个人评都早于修正、使用旧glyphinactive输出，不能直接验证修正模型的人类收益。locality一致性偏低需保留。

12片独立复标采用同SAM管线，IoU.95/Dice.98/cropIoU.94；主文DreamSim排名Kendallτ.94，AppL写.89，Warp均1.00，未自行选一值覆盖冲突。bootstrap只量化现有分布采样误差，不弥补脚本/极端运动覆盖。AppO ArcFace在131可检测脸源片上ViTeX.87，低于TextCtrl.99、RS.97、FLUX和Wan.96，说明背景稳定仍可能改身份。

## 固定公开制品：读到哪里、计算了什么

[GH bbbd2585](https://github.com/taco-group/ViTeX-Bench/tree/bbbd258512b1c6920c2088e7c1821145ddab23cf)完整126树项；读README、指定协议/发布段、完整文字指标/evaluate、OCR/RAFT/locality核心、glyph/attention/加载与训练接口/shell。vendored框架未全读。

[模型HF b3abf44f](https://huggingface.co/ViTeX-Bench/ViTeX-Edit-14B/tree/b3abf44f166d3936905b0430ef1e9d7560b19a62)卡明确旧推理脚本问题、adapter约8GB/基础约75GB，未下载。当前加载代码按缺失key条件初始化新模块，并从adapter替换VACE；静态代码核查不替代真实加载和条件敏感性运行。[数据HF c5e4fe16](https://huggingface.co/datasets/ViTeX-Bench/ViTeX-Dataset/tree/c5e4fe16a6c8dd532fd8c48118c9cd4969f78fa2)实际文本清单230/157、ID无交集、训练全部有edited路径、eval全部无。卡记录2026-09-29修正三进三出，当前有157条；未检查视频内容/媒体去重。

发布`eval_all.json`含13变体×157=2041逐片数字，文字指标均有152支持；源平均可读帧覆盖.894904。由这些已报数字重算完整glyph Seq.363101/Char.713691/Warp-c1.616526，与显示精度一致；这是数字汇总，未跑OCR/生成器，也不独立验证精度。

| 来源差异 | 直接证据及影响 |
| --- | --- |
| 裁剪边距 | AppE写固定16px；`union_mask_bbox`及调用实际pad_ratio=.1，相对10%可能改变crop分数 |
| Source PSNR | 正文/表为数学∞；代码clamp100，发布Source157条全100。需区分理论展示与实现截断 |
| OCR原串 | resultsREADME称保留；实际全部2041条均无source_ocr/pred_ocr，不能单靠包重算fitting/normalizer。当前evaluate代码会保存串，说明文档、发布包和当前输出不同 |
| 新提交完整性 | evaluate跳过缺OCR/文件，按最短视频/mask截帧；发布各行有157不受已知漏片影响，但新提交须报漏片/短片与support，不能只报均值 |
| 归一/插值 | 代码仅L/N且upper、空间resize为OpenCV默认；文档宣称Lanczos等细节需对齐，未据此断定原表错误 |

代码/adapter为Apache说明与数据CC-BY-NC4.0、上游Panda/InternVid限制分开，HF单个language=en标签不覆盖实际四脚本清单。

## 下一步可证伪实验与写作学习

固定Wan、训练对、参数与预算，训练无glyph/静态/对齐/错时glyph，做VAE后token置换与显式位置/逐帧token对照；按视频多seed pairedCI测文字、几何、时间、身份和成本。注入角点/跟踪/字体/mask误差，定位上游限制。统一源复制/编码/后处理接口，先设文字成功门槛，再读时间与Pareto，防止源复制/平滑获得假成功。

补严格整串、额外字、符号/变音、可读覆盖和瞬时失败，扩大非Latin/曲面/遮挡分布并让独立多人评correctedglyph。书写/绘画过程另用时变墨迹、接触抬笔和笔画事件GT，同终态不同顺序作对照。以上未执行，研究缺口还需系统查新。

可学习其从输入/任务三要求到指标三轴，再用反例/校准/局部性control组织实验；也应学习公开纠错对受影响结果逐一划界。Claim须写均值/区间/具体配置，Limitations列覆盖、测量和构造provenance，不能把旧人评或推理消融提升为新训练机制的普遍因果证据。
