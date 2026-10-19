# 尚需精读与原始来源追引：可操作队列

第二轮已补VideoSketcher方法/主表/消融、DiffInk及部分UMM和基础理论，见[124份笔记](../reviews/README.md)。截至2026-10-20全部328条的逐条缺项以[阅读台账](reading_ledger_2026-10-19.md)为准；下表保留专题追引和代码复核任务。

本队列维护“文献/研究找到了”与“已完整精读”之间的差别；不表示后台任务正在执行。2026-10-19 保存到 GitHub 便于逐次人工/模型核验。

## 优先级 P0｜威胁研究新颖性的直接前作

| 原始研究 | 已知可靠范围 | 下一次精读动作 |
| --- | --- | --- |
| [Calligraphy Bench](https://github.com/haizelabs/calligraphy) | 88 字中文书法 tool-agent、order 指标，HF 有 SVG/medians | 获取 judge 实现或联系作者；验证相同终态不同动作是否可识别；查合法地区书体 |
| [VideoSketcher](https://github.com/rhfeiyang/VideoSketcher) | Wan2.1 + two-stage LoRA + AR，官方脚本 | 主表/方法/消融已读，见L010新笔记；仍需逐图、完整附录训练条件、train.py及AR实现核查 |
| [BCSS / Stroke-Seg](https://github.com/Rvosuke/BCSS) | 静态 per-stroke mask 与规模，HF subset 与论文规模不同 | 核对出版社全文、实例数、交叉笔分割 IoU；解码 mask 与顺序是否被标注 |
| [Wuji Writing VAM](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819) | 数字机器人多视角视频+动作，配置/日志 | 校核训练配置/模型结构；动作流如何编码书写轨迹；独立部署真值/许可证 |
| [VidScribe](https://arxiv.org/abs/2609.36598) | 803 条视频文字基准，A1/A2 与 T2V/R2V/I2V/V2V | 审计评判器与混淆矩阵；设计 strict temporal order 反例 |
| [VTR-Bench](https://arxiv.org/abs/2610.01499) | 视频中文字 OCR/条件评价与多候选反馈 | 精核视频采样、WER 计算、预算控制及流程成本 |
| [OnOff Handwriting](https://arxiv.org/abs/2608.03198) | 轨迹+接触+近似物理墨迹渲染 | 增强是否改变原始 stroke 实例；跨风格规范与逐笔定量 |
| [DiffInk](https://arxiv.org/abs/2509.23624) | InkVAE/InkDiT、少步生成曲线 | 固定采样+评测协议，重查数据切分和额外控制变量 |

## P1｜跨领域生成/理解方法与强基线

- [TextDiffuser—NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/1df4afb0b4ebf492a41218ce16b6d8df-Abstract-Conference.html)、[GlyphControl—NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8951bbdcf234132bcce680825e7cb354-Abstract-Conference.html)：须全文阅读结构图、数据集、对比表及消融，理解显式 glyph/layout 约束在新任务内可能消失的收益。
- [VidSketch](https://arxiv.org/abs/2502.01101)、[MoSketch (ICCV2025)](https://github.com/jyliu-98/MoSketch)、[SketchEdit (IJCAI2024)](https://github.com/CMACH508/SketchEdit)、[DiffStroke](https://github.com/CMACH508/DiffStroke)：前三类分别是草图条件视频、对象动画、笔画编辑，不可都叫“笔顺视频”；逐篇抽表再做机理迁移。
- [SceneDAPR](https://github.com/DSAIL-SKKU/SceneDAPR)、[Quick Draw dataset](https://github.com/googlecreativelab/quickdraw-dataset)、[ark60 Sketch Diffusion](https://github.com/ark60/sketch-diffusion)：确认真实 stroke event 和 timestamp 与模型生成时间的区别。
- UMM 架构组：Transfusion、Janus、Chameleon、BAGEL、Lance、UniVideo、Show-o2；逐项核参数共享、视觉 tokenizer、损失/训练策略、官方可用视频生成接口及显存需求。研究问题核心是**协同有无**, 不能以同一程序调用多模型代替可证协同。
- 经典理论：DDPM（Ho 等）、latent diffusion（Rombach 等）、Flow Matching（Lipman 等）、rectified flow、LoRA、DoRA、RSLoRA；讲解服务具体公式与控制训练，而非无限扩展阅读偏题。

## P2｜语言/地域、训练工程与无论文材料

- [Ketaba](https://github.com/HasanBGit/Ketaba-OCR-LoRA)、[Qari](https://github.com/HasanBGit/QARI-OCR-LoRA) 与 [HF CASIA-HWDB2-line](https://huggingface.co/datasets/Teklia/CASIA-HWDB2-line)：核模型标识、任务接口、实际数据、CER 定义及领域泛化；OCR 不能为视频执行作直接 baseline。
- [AnimCJK](https://github.com/parsimonhi/animCJK)、[KanjiVG](https://github.com/KanjiVG/kanjivg)、[Make Me a Hanzi](https://github.com/skishore/makemeahanzi)：逐规范比较简体/繁体/日文有序笔画、许可和字形对应。
- 继续检查 Hugging Face 上“writing, brush, handwriting, stroke, calligraphy, pen trajectory, LoRA, I2V, robotic writing”，将找到的模型按语料/模型类型/可复现性建卡，并定期排除空模型卡和被重命名复制的条目。

## 所有逐篇笔记的最低完成门槛

(1) 研究问题和动机两分钟讲清；(2) 画出输入→主要模块→输出并解释公式与新组件；(3) 原表复现主指标口径并列至少一个实际 baseline；(4) 至少一组消融支持某个 claim；(5) 至少两个源自数据/失败样本/Related Work 的可检验质疑。数据集、模型结构、训练条件、优化器、NFE/seed、硬件、预算、限制必须分字段记录。不满足的字段标为待核，严禁填经验推测。

**停止/排除规则：**与目标无直接因果连接的研究可作领域背景；正式增量目录登记时区分 paper、benchmark、dataset、model_card 和 code_release；同论文多制品可保留多卡，但不能将它们计为多个独立论文。

## 本批存量复核后的追引补充

已完成相关章节阅读的23项是A04/A08/A11、L001/X01、L012/L014/L015/L016、F02/F03/F04、D01–D04/D06–D08、E02/E04/E06/E07；完整验收缺项仍见各笔记。

检索时又发现以下直接来源，登记为**候选，尚未完成原文精读**，本批不放进正式独立论文计数：

| 来源 | 相关性与下一步 |
| --- | --- |
| [Edit Flows，NeurIPS2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cb43f46154e750746602faaffd65fbbb-Abstract-Conference.html) | 可变长度离散序列编辑；对笔画增删和事件长度建模相关，需核方法/采样/实验 |
| [Discrete Guidance Matching，ICLR2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f0470962fc538827f3130757fb707b71-Abstract-Conference.html) | 离散flow指导率；追查与E04及多模态离散生成的关系，不能仅用题名推导效果 |
| [2D Gaussian Splatting for Bézier Spline Line Art Vectorization，Disney Research2026](https://studios.disneyresearch.com/2026/07/16/2d-gaussian-splatting-for-bezier-spline-line-art-vectorization/) | 与F02相关的最新矢量化工作；核工具/表示/复杂交叉线与时间事件适用性 |
| [Windfoil，arXiv2610.02468](https://arxiv.org/abs/2610.02468) | 可微矢量覆盖与渲染效率；需核与DiffVG/F02的比较条件及闭合/开放曲线限制 |

[CoFRIDA-Sharpie模型制品](../resources/cofrida_sharpie_card.md)已单独登记H001并关联F04，基础模型字段冲突待官方配置/代码进一步解决。DiffVG主PDF约17 MB，本批两次直接下载未完成，保留项目页可读事实，不将其升级为全文已读。

## 第三批之后的具体缺项

本批再读19项：B01/B03/B09、L004/L005/L009/L018/L019/L046–L050、C01/C03–C07。仍需完成各笔记标注的附录、图像、版本和代码核对，不能从相关章节阅读升级成完整三遍精读。

- InkDiffuser：取得完整PDF视觉核对、作者实际训练配置与缺导入模块解释；代码快照已记录。
- DiffMath：确认正文/附录冲突的VAE与DiT参数；核轨迹顺序、测试词表与独立OCR。
- 女书：核视频制品及其是否为Smartpen回放，字符表覆盖和字体/作者泛化；397字录制未被论文用于生成器训练。
- UMM：继续L057–L174的架构、tokenizer、协同训练与评价，优先L139/L140受控梯度研究及L067–L070跨任务协同基准。

## 第四批之后

本批新增L139/L140、L067–L070、R01–R05、F05、L007/L008、L023/L024、L029–L031及5项仅第一遍A06/L002/L006/L021/L022。主目录仍有137条历史原文待复核，40条摘要记录中也有需要精读的条目。

待取得的全文包括A06机器人笔顺恢复、DiffWriter(L002)、Frequency-Guided(L006)和两篇OpenReview投稿L021/L022。不能用后续论文对它们的转述填成原文已读。L020正式ICLR论文PDF下载中。

新增追引线索（尚未完成全文阅读）：
- *A survey of handwriting synthesis from 2019 to 2024: A comprehensive review*，Pattern Recognition162(2025)111357；需核出版社原文、参考文献与本目录差集。
- *From pixels to strokes: A survey on generative handwriting*，IJDAR2026，DOI10.1007/s10032-026-00609-2；需核任务分类及参考列表。
- *Hierarchical offline-to-online Chinese handwriting trajectory reconstruction via dual-domain priors*，DOI10.1007/s44443-026-01050-5；需核与L006的任务、数据和方法关系。
- *Template-Guided Cascaded Diffusion…*，ICDAR2025，DOI10.1007/978-3-032-04614-7_9；是否与L021投稿有版本关系待查，暂不合并。
- [CursiveTransformer作者实现介绍](https://greydanus.github.io/2025/03/30/cursive-transformer/)；需读取训练代码、数据、采样配置和授权。
- [Inkspire作者项目](https://dlin.org/inkspire)，arXiv:2501.18588：草图协作交互线索，须与同名手写生成工作区分。
