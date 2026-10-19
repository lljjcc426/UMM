# 生成代理、早期gate、共享token与世界模型

2026-10-20，六项存量U20–U25；七字段、五个研究问题及写作分析见[逐篇目录](../reviews/README.md)。SGT与UniAR新增五项书面检查。相关章节核查不等全文附录/代码完成，无新增独立记录、无删除、无模型执行。

## 机制比较

| 工作 | 改动发生在哪 | 已核条件/限制 |
| --- | --- | --- |
| SGT | 训练：生成分割等辅助目标 | 190K SAM+约500K VQA；纯代理损部分OCR/知识 |
| AdaViG | 推理：第5扩散步决定是否继续画辅助图 | 两个BAGEL数学变体；304题调阈值，仍先付部分生成成本 |
| UEval | 数据/评价：题级图文rubric | 含art步骤图；部分模型各模态独立调用两次 |
| SCO | 推理：四条件分支估计变化/保持方向，约束修正CFG | 视频须GPT5事件规划，额外分支/NFE成本待核 |
| UniAR | 共享离散bit上下文+AR+独立条件FM像素解码 | 不重编码可读bit，但实际像素可能与bit细节不同 |
| VisWorld-Eval | 理论/基准及三类CoT后训练 | oracle信息上界，非所有任务视觉优越定理 |

## 结果、输入与成本

[SGT v2](https://arxiv.org/pdf/2605.18714v2) Table3多数感知和GenEval提升，BAGEL SIBench分割50.18低重建50.59，OmniGen2 Hallusion64.25低重建65.19。AppTable6纯panoptic时OCR81→79.3；AppTable7 OmniGen2 depth GenEval79.9高分割78.9。分割是所测理解任务较好代理，不能扩成每项生成最优。12随机seed指生成采样平均，未证明12次独立训练。与UniMRG均存在结构监督，需同数据/teacher/预算比较。

[AdaViG v1](https://arxiv.org/pdf/2607.10004v1) Table1 Zebra平均43.9→47.0、图生成FLOPs−57%；Canvas47.1→50.5、−32%。Table2实测整链延迟降幅另报，例如Canvas13.2→9.4s。两信号都弱才中止优于任一弱：后者drop61%，MathVista75.1低原77.9；双弱drop43%达81.3。attention是可预测代理，不能直接命名真实认知意图；需等drop率对照和跨骨干迁移。省图不适合直接跳过必须完整呈现的书写笔事件。

[UEval v1](https://arxiv.org/pdf/2601.22155v1) 有1000题/10417rubric，art/life/tech/exercise明确包含步骤图。这一前史必须纳入绘画过程评价相关工作，仍无规范笔顺或连续视频评价保证。Table2 GPT5Thinking文字83.8高Instant77.7，图49.1却低52.8；不能把reasoning改进概括各模态。参考答案图87.8/文96.8未满分，人评仅对Thinking输出分层10%，约90%agreement/r.88不证明对所有模型无偏。单模态分别调用两次与原生joint的预算/一致性分开。

[SCO v1](https://arxiv.org/pdf/2610.10400v1) Eq3/5的两方向分别由full−counterevent、full−eventonly估计。投影方向可竞争，有界修正产生slack；Gram项不能丢。AppA1明确视频须规划事件并分配帧条件，不能写成只插一个无外部阶段的算子。每作用步有四条件分支；训练免费不等推理免费。Table2 MiniGPT5多数指标下降；Table4单state Cs.18高Both.17但总体GPTJ2低，体现保持/变化取舍。Table5LPIPS原值可>1，具体聚合/缩放未核，保留原分而不擅自与其他论文.2等值比较。视频FVD不直接证明动作可执行或接触物理正确。

[UniAR v2](https://arxiv.org/pdf/2606.18249v2) 64bit的2^64表示理论组合数；多层/2×2并行减少AR步数，最后依然条件FM DiT产像素。Table9及AppA4明示不含decoder、A100无CFG；质量评价用CFG2.5或2.0。13s不是端到端1024图生成延迟。Table7 35.4→24.5s/iter对应时间降30.8%、吞吐比约1.445。OneIGEN.873/LongTextEN.917并非高于表中所有模型，QwenImage.891/.943，GPT4o长文.956。应评共享bit所含细节与最终像素是否一致，不能仅以省一次重编码作为理解图的可靠性保证。

## VisWorld理论的成立范围

[VisWorld v1](https://arxiv.org/pdf/2601.19834v1) AppA把观测设为state的确定函数，并假定不同模态共享oracle推理。答案KL≤联合CoT/答案KL来自边缘化数据处理，链式分解分成reasoning和worldmodel项。该不等式不直接比较两种模型的答案准确率，也不保证减小某项会降低实际错误率。

条件熵下降=条件互信息≥0针对oracle真分布。实际辅助图会错，其生成误差也进入联合KL；视觉通道更细可能有更多有用信息，同时更难预测。信息论给的是条件性上界和取舍，不能推出视觉必胜。AppCorollary1完全观测且确定状态迁移时，显式状态无新增信息；这不排除有限算力模型因显式表示方便而受益。

AppTable2七任务35935训练/3946测试；五任务各480，球反射1024，MMSI522。后训练Fig4与zero-shot Table1不同；MMSI仅cameraobject/cameraregion观察稳定收益，不能概括所有空间题。SFT三模式给的监督格式和图生成loss不同，仍需匹配训练/推理compute。约4倍样本效率来自折纸曲线，不是全领域保证。RL只优化文字，图是reference正则，不能称完整图文联合RLVR。

## 后续可证伪设计

分割/深度/边缘/重建同源图、同更新、同梯度预算，加入错配/随机目标和判别辅助head；报告知识/OCR负迁移。Gate等drop率、SCO等NFE，完整计规划API与attention/decoder/CFG成本。对原图、规则渲染GT状态、错误状态、模型图逐一干预，分任务可观测性与真实动力学检验；书写要按真实笔事件标签判序，去噪/推理索引均不可充当笔画时间。
