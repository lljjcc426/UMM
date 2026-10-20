# 自生成历史、梯度路径、少步组合与任务奖励：核心三遍审查

本批扩展[D05 Self Forcing](../reviews/D05.md)、[D06 Self Gradient Forcing](../reviews/D06.md)、[D07 Salt](../reviews/D07.md)、[D08 Wan-R1](../reviews/D08.md)四项既有记录，完成核心方法/公式职责、框架视觉、主表与现有消融、批判阅读和各五条书面理解检查。SGF以arXiv v1 HTML及Fig2原图核读，未冒称全PDF逐页视觉检查。无独立模型运行。

## 四项工作的具体不足与优势假设

| 工作 | 针对的不足 | 干预和仍保留的近似 | 有望受益的任务条件 |
| --- | --- | --- | --- |
| Self Forcing | TF/DF真实历史与学生生成历史分布差 | 自rollout+整体分布目标；随机exit、历史KV写入detach | 少步因果流式视频，教师覆盖目标分布，首帧等待敏感 |
| SGF | futureloss无法直接训练历史tctx0 writer | 两遍局部重放重算KV保梯度；生成latent/轨迹仍detach | 历史表示漂移主导、mask/RoPE/缓存关系匹配的长时视觉稳定 |
| Salt | DMD局部更新组合不一致、不同质量cache分布 | SC端点约束、混步与reference关系对齐；reference较强为经验假设 | 2–4NFE生成，训练grid匹配且参考可靠 |
| Wan-R1 | 视觉像在解题、实际路径错误；VLM误奖励 | 任务GRPO与路径/保真奖励；机器人使用embedding代理 | 可可靠提取轨迹、GT定义清楚且SFT有成功率的特定任务 |

四者都未提供规范汉字笔顺的专门训练/完整评价。泛化视频质量、历史稳定和任务事件正确性要分别验证；已有机制的不足也需继续追引，不能直接当作新课题。

## 原文、表格与结论纠偏

### Self Forcing

[NeurIPS2025官方论文集](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f4823f831af67a3ef15e41a85434422a-Abstract-Conference.html)已确认主会身份，技术分析读[arXiv v1](https://arxiv.org/pdf/2506.08009v1)。Table1单H100 chunk17FPS/.69s，对Wan.78FPS/103s；约150倍是首帧等待比，吞吐约22倍。SF total84.31略高Wan84.26，但quality85.07低85.30，未给统计CI。frame8.9FPS/.45s不应与chunk17FPS拼成同一配置。

Table1 CausVid脚注为同Wan1.3B官方实现81.20；Table2作者同框架DF+DMD82.76与SF84.31是另一比较协议。SiD的quality85.52优DMD85.07，semantic78.24低81.28。不同目标有权衡。rolling10s重算4.6FPS到16.1FPS；长于5s、尤其30s退化仍是项目明确限制。

随机exit使每块只在选中forward反传，历史写入no_grad；共享参数仍受其他路径更新。DMD/SiD不需视频仅限这一后训练阶段：预训练、教师、16K ODE初始化pair与扩写prompt均有成本。GAN的70K“real”训练视频由教师合成，不能写成70K真实世界视频。

### SGF

[v1核心方法](https://arxiv.org/html/2607.20368v1)与[Fig2](https://arxiv.org/html/2607.20368v1/flowchat.png)明确：Pass1无梯度生成并记录，Pass2对stopgrad历史重编码KV，让未来损失回到writer。它是局部surrogate，没有更新生成历史本身或恢复全部denoising decisions的梯度。24prompts×4exits的前向recovery RelL2约1.41%、cos.999886；将其与bf16epsilon比较只是数值尺度参考，不能当梯度精确证明。

frame训练全5s/21latent无FIFO淘汰，推理sink4+FIFO16+current1；chunk训练/推理sink3+FIFO6+current3。不能概括两者都在训练时做同样streaming淘汰。Table1 frameODE60s subject.928→.971，但dynamic.867→.566；Table2 chunkCD240s imaging.671→.667下降。长表缺semantic项，不能由稳定指标推长期指令正确。

人评GSB是净差，frame60s ODE/CD/TF分别29.6/36.8/45.1%，非获胜概率。Table4峰值79.01→87.01GB、稳态79.01→63.73GB、每5steps10.39→11.71s，硬件型号未明确。不能将87GB结果套成80GB单卡保证。DirectKVgrad OOM仅描述本实验实现；有限memory丢失的历史也无法靠writer梯度恢复。

### Salt

[v2](https://arxiv.org/pdf/2604.03118v2)Eq6–10借精确ODE flow的半群性质约束Euler近似端点；Euler单步一般不精确满足半群，约束并不提供全局误差或逻辑正确保证。Table4同8点训练grid DMD82.54，SC83.36，高于4点DMD82.78；支持组合约束超出单纯加密grid。Table5 CausalForcing加naiveSC由84.62降83.83，mixed+SC85.02、full85.08，缺mixed-only，不能单独归因混步或SC的净贡献。

SF接Salt total84.20→84.47而semantic82.05→81.28；30sCF quality82.57→82.15、dynamic76.95→54.02。VideoAlign为学习型评价代理；两例光流图不足排除总体少动偏差。AppA局部defect.0135→.0111是机制诊断，不能替代长rollout评价。α额外adversarial结果单列，PCM行实际8NFE，不能按表caption统一4NFE。

§4.2 I2V8H200与AppB非AR16H200有硬件描述冲突；AppB非AR关闭backward simulation，AR默认开启。官方GitREADME非AR4NFE表83.19/84.42/78.30，v2表83.36/84.76/77.77，保留不同来源，不选优拼接。arXiv作者Comments与HF称ECCV2026录用，本批官方accepted页未定位标题，按作者声明记录，未冒充正式论文集独立核定。

### Wan-R1

[v1](https://arxiv.org/pdf/2603.27866v1)Table1对SFT：regular/trap/3D EM有提高，但irregular56.9→47.9下降；SokoSD10.2→16.9变差。摘要29.1与51.4分别为3D/trap EM绝对百分点提升。表最后Δ行对base，不能说对SFT。PR为PrecisionRate正确前缀，SD为StepDeviation，纠正旧笔记的PathRatio/StepDistance写法。

Table2颜色标注蓝SFT/黄R1已核：irregularHard PR68.4→51.6，正文将68.4归给R1，存在归属矛盾。3DHard96.2对15.2是base对照，SFT58.7要另列。TargetFig3总体分R1略高SFT，但ADE/FDE/MR/AC有落后项，caption全项更好不受图支持；无数字表，不猜精确小数。

Table7 SokoMF94.1→73.0下降21.1pp，不能概括无画质损失。Table8 PR+EM相对EM提升EM58.3→61.1，但PR79.3→78.6/SD4.4→5.2退化，MF分项未消融；无SFT失败只证当前稀疏奖励配置的bootstrap依赖。跨任务与纹理均有退化项。

maze奖惩对单GT最优路径，可能误罚另一合法解；提取器/像素阈值/失败处理缺详细协议。Target默认DINO/CLIP embedding、时间位移profile与端点相似，VGGTtrajectory reward权重默认0；代理相似度不认证物理正确。结果是离线生成视频，无真实机器人闭环执行。LNCS模板不证明录用，未定位作者官方代码/模型入口。

## 固定代码、模型卡和调参入口

- SF [33593df代码](https://github.com/guandeh17/Self-Forcing/tree/33593df3e81fa3ec10239271dd2c100facac6de1)：四步shift5，gen2e−6/critic4e−7、fake:gen5:1、globalbatch64、EMA.99；600iter<2h/64H100为作者实测口径，8H100<16h为预估。HF [2f8b779卡](https://huggingface.co/gdhe17/Self-Forcing/tree/2f8b779212da279d212c22a509b66ad6552f350e)Apache2，提供ODE/不同目标checkpoint与prompts。4090可运行和H10017FPS分别界定。
- SGF [79be9ac](https://github.com/zhuang2002/Self_Gradient_Forcing/tree/79be9acbd874c9be050944a6b1de6693e988a171)：公开globalbatch8、frame1500/chunk1200steps、同gen/critic学习率；默认per-rank exit配置继续步列表但写exit x0，不全等于提前break。HF [ffaf490](https://huggingface.co/JunhaoZhuang/Self_Gradient_Forcing/tree/ffaf49017e4558fe02319b931f458ea2379bf606)分别发布frame/chunk模型、初始化与prompts，不能把公开配方默认为每个论文run原配置。
- Salt [5fbb513](https://github.com/XingtongGe/Salt/tree/5fbb513543ac7cd335522d72fd70232a2ed4ab54)：SCλ.2、TRDmargin.1/weight.1、CF对齐start700对论文示例600。pipeline_sc_training.py608–631将composedtarget分支stopgrad，Eq8未显式标sg。HF [07877f3](https://huggingface.co/domiso/Salt/tree/07877f3acb5ef36f353cb0b226f6bdc1b5b8ce05)license other，CF用EMA、LongLive用regular generator；LongLive部分文件CCBYNCSA4与顶层Apache2分开。

只读卡、配置和有关计算路径，未下载/运行权重，无全源码审计。论文配套模型制品关联已有ID，未重复计为独立研究。

## 研究思路与可证伪实验

先区分历史分布、梯度路径、时间步组合、任务奖励四类机制，再做同teacher/初始化/prompt/总FLOPs的对照。SF×cachegrad×exit设置，SGF前向恢复外补梯度夹角，Salt做mixed-only与SC/TRD全因子；同时报告短长semantic、动态幅度、identity和置信区间，避免少动提高稳定分。

任务RL需合法多解oracle、轨迹提取人工审查、背景篡改对抗例和reward每分项/权重对照。Target分代理分数、几何轨迹和实际执行；bestK固定总预算、公开选择器。书写补规范事件、抬落笔、墨迹单调增长、漏重笔和方向，规则SVG/强视频基线/共享UMM比较应匹配输入信息与资源。

Introduction可学习如何由具体失败定义可检验问题；Method把计算图与公式职责相连；实验主表和受控消融分别承担性能与归因。Claim限定分母、版本、指标与人评净差，Limitations写已观察负项和缺失协议。SGF+ [2610.10429v2](https://arxiv.org/abs/2610.10429v2)已从作者仓库追到，正在精读，尚未计主目录新增；24h连续生成主张仍需区分示例与全程定量证据。

本批后339目录/339笔记、78核心三遍及五项书面检查；剩余精读、候选去重追引和五项全文阻塞仍继续。无文件删除。
