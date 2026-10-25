# 七项缺失原文最终来源核验｜2026-10-25

当前范围更新：本页L184已完成工作保留，并同步至验收源数据；其余6篇按用户要求停止跟进，不再要求获取PDF或人工验证。见[当前范围](../reading/scope.md)。

## 本轮结论

在此前 333 项研究中，**L184 / Stroke-Seg 的原始 15 页全图 PDF 已实际定位并打开**；此前缺失的 Figure 3/4/5/6/7/9 像素已逐图检查，旧核查的 Figure 2/8 同样得到可见图版。**Figure 1 在这份正式 PDF 内有原图和图注**（论文 p.4342），本次单独调用该页截图返回缓存错误，因此其具体细节仅按正文/图注描述，没有声称独立像素核实。

6 篇 **A06、F05、L002、L006、L021、L022** 仍未取得对应版本的可读取完整 PDF。逐篇链接/当前访问状态/缺失内容见下表。未将作者博客、摘要、搜索引擎缓存、相似论文或出版方付款预览计作“原文全文”。

| ID | 对应正式来源 | 本次已核的最大范围 | 完整原文获得情况 |
| --- | --- | --- | --- |
| A06 | [Springer SN Computer Science](https://link.springer.com/article/10.1007/s42979-021-00717-2) | Springer 全8张原始插图已核；论文正文仍付费预览，训练、表及消融缺 | **未获得** |
| F05 | [ICASSP 2026 / IEEE 11463098](https://ieeexplore.ieee.org/document/11463098/) | [Samsung作者技术说明](https://research.samsung.com/blog/Online-Cursive-Handwriting-Generation-Using-Trace-Transformation-and-Symbol-Independent-Point-Classification-Model)中图1和表1–3，正式稿 PDF 未取得 | **未获得** |
| L002 | [ICONIP 2023 章 DOI](https://link.springer.com/chapter/10.1007/978-981-99-8141-0_7) | 官方摘要、版本/页码；pp.86–100全部图表/方法缺 | **未获得** |
| L006 | [Information Sciences](https://www.sciencedirect.com/science/article/pii/S0020025526010674) | 官方摘要/引言、§小节摘录；公开API仅 coredata，非论文 body | **未获得** |
| L021 | [OpenReview 正文 PDF](https://openreview.net/pdf?id=VdDtRu7RTf) | 官方索引的摘要/引言；PDF触发 browser verification。无官方接受/撤稿结论 | **未获得** |
| L022 | [OpenReview 正文 PDF](https://openreview.net/pdf?id=SuLp0J2uan) | 官方索引的摘要与少量缓存页；当前PDF页触发浏览器验证 | **未获得** |
| L184 | [IET Image Processing 官方](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.13255) / [含九幅原图的15页 PDF](https://www.researchgate.net/journal/IET-Image-Processing-1751-9667/publication/385042124_Stroke-Seg_A_deep_learning-based_framework_for_chinese_stroke_segmentation/links/671295a0069cb92a811b531e/Stroke-Seg-A-deep-learning-based-framework-for-chinese-stroke-segmentation.pdf) | 正文 §1–6、公式1–8、Tables1–4 及 F2–F9 实际图像；F1有原图、图注及正文引用，截图服务不能单页呈现 | **完整 PDF 已获得可读的公开链接** |

## L184：逐幅核对原始 Figure 1–9

**正式原始文件**：[research article PDF](https://www.researchgate.net/journal/IET-Image-Processing-1751-9667/publication/385042124_Stroke-Seg_A_deep_learning-based_framework_for_chinese_stroke_segmentation/links/671295a0069cb92a811b531e/Stroke-Seg-A-deep-learning-based-framework-for-chinese-stroke-segmentation.pdf)；IET Image Processing 18(13):4341–4355，DOI 10.1049/ipr2.13255，15 页；正文版权信息表明 **CC BY-NC-ND 4.0**。研究对象为**静态毛笔汉字笔画类别多标签分割**，其输出不包含笔画的实际时间先后、落笔方向或唯一笔实例 ID。

| 图 | PDF页面/期刊页 | 核查证据与理解 |
| --- | --- | --- |
| F1 | 2 / 4342 | 完整原图包含于PDF。图注讲解交叉处错误截断及楷体与毛笔字交叉点差异。**单页像素截图失败，只确认正文/图注和完整PDF承载，不夸大图像核查。** |
| F2 | 4 / 4344 | 已核原图：识别字符并查11维笔画先验，原图与先验融合送分割骨干、十通道多标签输出。 |
| F3 | 5 / 4345 | 已核原图：对3,755字的26种传统笔形做出现频次统计，并比较重新归并的10类分布；体现类别稀疏问题。 |
| F4 | 5 / 4345 | 已核原图：十类笔形层次及形状样例；类合并减少类别数，同时同类多实例身份难由单类别通道分离。 |
| F5 | 6 / 4346 | 已核原图：“德”分解到字类型ID和10类笔形数；零值代表该类缺失。先验来自识字/字典，并非从原图恢复真实写字顺序。 |
| F6 | 8 / 4348 | 已核原图：BCSS多个来源书法字及每笔彩色mask，包含复杂交叉；不同颜色只是分割标注。 |
| F7 | 11 / 4351 | 已核原图：Ground Truth、SSGAN、CCSE、DeepStroke 与 Stroke-Seg 几种分割定性输出。结合T3才可讨论 TSR/FSR，不靠单图数错误率。 |
| F8 | 12 / 4352 | 已核原图：已见/未见字的彩色分割效果，部分交叉或连笔处仍留下模糊区域。 |
| F9 | 13 / 4353 | 已核原图：错误实例与正确示例成对显示。§5.4明确举出未见复杂笔画ShuZheZheGou被拆分、Pie误识为Dian、无法分类/分入多类等。 |

### 方法—数据—结果重新对齐

- **输入/模型/输出**：400×400单字灰度图 + character ID、10类笔画个数组成的11D PKV；PKV 上采样后与图像拼接；不同FCN/U-Net/DeepLab v3+/TransUNet/TransDeepLab/Mask2Former/OneFormer分割骨干，多标签十类通道经阈值0.6输出。BDLoss=0.5·BCE+0.5·Dice（各类求和）。预测结果是类别 mask；同类型多笔实例、笔尖物理轨迹与合法顺序仍需额外算法。
- **数据**：正式论文T1报告1,322图；训练/验证1,022图内分872训练、150验证，另300张外部测试；总计笔画需按原 T1 分项求和1,322图、14,766笔画，而历史GitHub/HF公开包报10,653笔画，来源和范围必须并列，不能合并数字。
- **主实验 T3**：TransUNet TSR=.982、FSR=.018、FLOPs79.0G；DeepStroke .935/.068，54.1G；FCN .961/.045，39.9G。指标为IoU>0.8的匹配笔画分割率，**不能解释为笔顺准确率**。
- **严格消融 T2**：U-Net 的 Dice/no-prior TSR=.681；Dice/prior=.880（+19.9个百分点）；BDLoss/prior=.955（相对初始 +27.4个百分点）。论文摘要“19.9%”的具体比较基线须按行注明，不把这些视为跨全模型统一增幅。
- **分布外 T4**：300独立外部图中的已见字150例 TSR=.962、FSR=.065；未见字150例 TSR=.831、FSR=.140；总计 .897/.103，未见字降低13.1个百分点。报告双指标时均使用原表定义；TSR、FSR由于分母与匹配方式不必互补到1。
- **具体局限**：10个类通道不唯一追踪同类多笔；PKV由识别系统/人工维护字典供给；风格、未见字和复杂交叉明显拖累分割；作者公开FCN样例实现与正式论文全模型/全损失训练脚本及评价流程不完全一致。
- **可证伪问题**：若在未知字输入错误character ID/PKV噪声下，先验收益是否保留？当同类笔多实例重叠时，语义类TSR提高是否仍能恢复严格逐笔身份及顺序？下一阶段应做gold/pred/noisy ID+stroke-count拆分及相同信息量对照，额外测 instance matching、方向/事件，与最终画面IoU分开。

### 三遍阅读的5项独立证据

1. 问题/动机：单标签与截断交叉导致笔画缺失；类频次不平衡，跨书体结构差异（§1–2，F1/3）。
2. 框架：11D PKV→灰度/先验双通道→分割骨干→10个重叠类 mask（§3，F2/4/5）。
3. 核心创新：Stroke Class、PKV、multi-label、BDLoss，区分既有BCE+Dice和真正贡献（§3，Eq1–8）。
4. 主表与消融：T3主比较、T2原始六设置和T4域外分组均已核，指标口径见上。
5. 至少两项有依据疑问：同类实例不可辨识与PKV字身份泄漏；另对F9错误模式和真实时序差异提出检验。

**结论**：L184 按本仓库“核心三遍/五条书面核查”标准可升级完成；**完整训练与评测代码/权重、独立模型复现及F1单页额外截图依然未执行**。原始 PDF 在外部作者/出版社发布页面，仓库记录其可核链接与阅读范围，避免改变 CC BY-NC-ND 原文件与放入未许可的二次编辑 PDF。

## 其他6篇收尾检索核验

- A06 的Springer订阅下载实际返回HTML预览；F1–8出版方静态原图已经阅读。缺少实验总表与训练协议时不可把NDCG平均0.9667等同完整正确笔顺率。
- F05 三个作者说明主表仅支持“英文独立字符轨迹→连笔后处理”的模型分析；正式ICASS​​P公式/附录缺，不以相关的 Samsung 旧对齐工作替代。
- L002 正式书章仍受订阅，相关OLHWG是独立论文；L006 Elsevier摘要/开头给出了wavelet CMSE、PE-CSP，完整消融数字仍需全文。
- L021/L022 必须取得**精确 OpenReview submission ID 对应版本**；机器搜索索引有首段但浏览器当前验证跳转，不能据第三方“撤稿”字符串作官方发表决议。

论文获取途径：出版方机构订阅或作者许可的accepted manuscript；OpenReview两个条目可在已认证账户的实际浏览器打开并下载。上传/提供时应保留DOI、版本、PDF页数、原图与附录对应关系。本次在连接的Drive检索标题未发现这六篇原文，也未在 GitHub 中找到对应PDF；因此核心完成数应明确保持六篇待原文。出版方受限文件没有被冒充成完整下载。

[逐条结构化JSON](../../data/seven_missing_full_pdfs_latest_2026-10-25.json) · [L184单篇笔记](../reviews/L184.md) · [原七条历史核查](remaining_source_access_and_reading_handoff_2026-10-25.md)
