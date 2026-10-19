# 尚需精读与原始来源追引：可操作队列

本队列维护“文献/研究找到了”与“已完整精读”之间的差别；不表示后台任务正在执行。2026-10-19 保存到 GitHub 便于逐次人工/模型核验。

## 优先级 P0｜威胁研究新颖性的直接前作

| 原始研究 | 已知可靠范围 | 下一次精读动作 |
| --- | --- | --- |
| [Calligraphy Bench](https://github.com/haizelabs/calligraphy) | 88 字中文书法 tool-agent、order 指标，HF 有 SVG/medians | 获取 judge 实现或联系作者；验证相同终态不同动作是否可识别；查合法地区书体 |
| [VideoSketcher](https://github.com/rhfeiyang/VideoSketcher) | Wan2.1 + two-stage LoRA + AR，官方脚本 | 阅读原文图、全部结果表/统计、train.py loss、AR distillation；固定 commit |
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
