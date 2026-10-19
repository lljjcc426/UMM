# 离散路径、插入流与连续块：第十四批审查

2026-10-20；新增L109–L116八份指定章节分析，累计226份。主目录332条中章节240、摘要33、历史待复核59。Muddit补五项书面检查，累计7项；完整三遍验收未完成。未运行模型，没有删除文件。

## 任务、路径与解码依赖

| 记录 | 生成状态与主要机制 | 须保留的边界 |
| --- | --- | --- |
| [FUDOKI/L109](../reviews/L109.md) | metric-induced离散CTMC，普通token间跳转 | kinetic最优对指定路径/权重；13M指适配，含内部数据和已有Janus先验 |
| [Muddit/L110](../reviews/L110.md) | 视觉先验MM-DiT，双方向maskedCE | 77token；联合图像增益伴文字任务下降；公开sh文字权重为0 |
| [LaViDa-O/L111](../reviews/L111.md) | ElasticMoT/模态展开/空间分层，框规划与反思 | 激活参数6.4B与总量10.4B分开；小字VQ重建缺陷为作者明示限制 |
| [Lumina-DiMOO/L112](../reviews/L112.md) | aMUSEdVQ/LLada8B、MLcache、SelfGRPO | cache近似且显存增加；token区域不变不保证decoder区外像素不变 |
| [Omni-Diffusion/L113](../reviews/L113.md) | Dream7B mask预测图/语音/文 | 语音输入仍是连续encoder+MLP；只有静态图生成 |
| [LLaDA2.0-Uni/L114](../reviews/L114.md) | SigLIPVQ+16BMoE blockmask+6B ZImage流decoder | 8步指最后decoder；骨干与decoder分别训练，语义码仍损细节 |
| [FullFlow/L115](../reviews/L115.md) | 连续图flow+离散插入文字，低秩适配 | 136M是可训练量；FID参考冻结teacher生成图；matchedbaseline同时改变多个配方因素 |
| [Multimodal Flow/L116](../reviews/L116.md) | 连续文/图embedding、chunkcausalFM | 文本codec用CE且块间因果；1.6B不含冻结codecs，不可仅凭并行认定更快 |

这些模型的去噪/揭示/插入顺序属于算法内部状态。把它们用于规范书写视频，需要另外定义事件、RGB时间、动作条件和评价协议。

## 公式与公开实现交叉读

[Muddit v5 PDF](https://arxiv.org/pdf/2505.23606v5)第4页已渲染核对。mask比例γ从0到1与文字monotonically decrease矛盾；Eq5又将一个密度表达式记作γ，密度允许超过1，无法直接当mask概率。[官方代码d048cf7](https://github.com/M-E-AGI-Lab/Muddit/tree/d048cf7df98609c4bd4107f3abb61ced5a1a9e70)的train_unified.py第784–808行实际使用σ均匀、cos(σπ/2)为比例，938–969行计算maskCE并除比例。sh将text_loss_weight设0，8GPU×8batch×8acc=512，与论文联合训练和部分表设置不一致。当前可确定呈现/模板需澄清，不能据此宣布实测结果错误。

[Lumina代码81344e6](https://github.com/Alpha-VLLM/Lumina-DiMOO/tree/81344e60545ae8d70f11039d3450717d974f831b)的image_generation_generator先取当前vq_mask位置，预测后只在这些位置低置信重mask；已接受token不会在本轮被选。vq_len保存初始mask数再乘cos schedule，与正文Eq4写当前L_t需对应。具体采样器的限制不能扩大到所有masked生成器。

## 主表与消融支持什么

- Muddit Table4：T2Ionly→joint GenEval59.3→61.6；I2Tonly→joint CIDEr60.1→59.9、VQA69.1→68.2。多任务正迁移依方向。Table5 32→64步GenEval61.9→61.1、VQA65.4→68.2，不支持所有任务32步后均稳定。
- LaViDa-O：基础/规划/反思GenEval.77/.85/.89；布局/计数改善伴更多推理计算。ImgEdit整体3.71→3.80，两类全局编辑下降，规划并非所有指令都适合。小字重建失败直接限制文字任务。
- FUDOKI：GenEval.77→.88用32候选选top4，MMVet38→55.5用8候选选优；提高不是同一单样本计算。给定路径的kinetic优化不能替代质量/计算因果实验。
- Omni-Diffusion：256→10步图像28.57→1.29秒，CLIP.235/.667→.226/.650；音频RTF降低同时WER3.07→4.83，需同时列质量与速度。
- LLaDA2Uni：SPRINT平均分−.6而TPS1.6×，OCR−2.3；Turbo decoder50→8步且移除CFG，延迟11.4×，GenEval.89→.87。全部pipeline另含语义码生成。
- MF-1受控Table4是重训stylebaseline，在50B+5B、匹配可训练参数下优于两种实现；冻结codecs先验、实际FLOPs尚需核。Table6 specificattention/specificFFN在GenEval/CIDEr优于所选sharedattention，所选结构PPL较好，须保留折中。

## FullFlow的参考分布与配方归因

[FullFlow PDF](https://arxiv.org/pdf/2605.20316v1)第8页Table4/主captionVQA表及课程图已视觉核查。FID/CMMD参考冻结baseSD3输出，衡量teacher分布保持；不等价于真实图像保真或优于teacher。Table4等墙钟FID62.65→31.57、CIDEr2→99.4；等step本法CIDEr13.4，说明吞吐与训练更新数解释大量文字增益。

AppB7写明：FullFlow用ind→ac课程和same-noise teacher，DualDiffLoRA用ac+普通FM，此外文本接口/冻结范围不同。虽然参数/data/optimizer匹配，这个总对照不能隔离单个接口机制。应做接口×teacher×课程析因，并同时报告等step/等时间和真图FID/teacherFID。136M可训练量不包含整个冻结SD3与T5/CLIP。

## 与绘画和笔顺研究的连接

公式/解码器分析首先要回答哪些信息能保留、在哪一阶段丢失，之后再做真实执行实验。VQ语义或重建码、连续语义与直接像素各有信息/计算条件，不能仅按统一目标或模型家族排序。对细字先测codec重建OCR/最小笔差，再测单帧生成与真实时序事件；共享训练比较必须匹配每任务曝光/整体计算。

由官方根README发现[HT-GRPO/Sketch Then Paint](https://arxiv.org/abs/2605.16842)与[dMLLM-TTS](https://arxiv.org/abs/2512.19433)，均为后续待深读候选。ht_grpo子README写代码/报告稍后发布，根README已有论文链接，不能记成无论文成果。sketch/paint标题并不能证明输出绘画过程视频。
