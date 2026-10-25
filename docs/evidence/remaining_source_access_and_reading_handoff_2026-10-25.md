# 余下来源核查与本轮交接

2026-10-25，第二百二十一批。当前主目录359项：332篇论文／研究、27项资源；359份结构化笔记，325项明确范围核心三遍、328项五条书面记录（含未通过项）。本批对余下7篇做有限主源访问复查，未增加核心完成数。没有文件删除。

新增BoundInk已经另计L192，并与旧称CASHG去重。27项资源按数据/源码/模型制品协议记录，不适用论文三遍计数。[完整台账](reading_ledger_2026-10-19.md)、[状态页](../project/STATUS.md)、[结构化访问证据](../../data/remaining_source_access_and_reading_handoff_2026-10-25.json)。

## 七项未完成的明确边界

| 编号 | 研究 | 已核范围 | 当前访问结果 | 恢复后需要补齐 |
| --- | --- | --- | --- | --- |
| [A06](../reviews/A06.md) | Font Generation / Keypoint Ranking | 正式摘要与书目；方法/实验未取 | Springer PDF入口返回订阅HTML；OpenAlex无仓储全文 | 合法完整作者稿/正式全文与全部图表 |
| [L002](../reviews/L002.md) | Diff-Writer | 正式摘要与书目；方法/实验未取 | Springer订阅预览；OpenAlex无仓储全文 | 合法完整作者稿/正式全文与全部图表 |
| [L006](../reviews/L006.md) | Frequency-guided cross-modal diffusion | 原始摘要/任务模块线索；无全文 | Elsevier仅coredata，无body；2026在线、2027卷期分列 | 完整正文、主表/公式/附录与发布版本 |
| [L021](../reviews/L021.md) | Write More at Once | 官方匿名首段；无方法实验 | OpenReview PDF/API challenge；Template-Guided仅相似前史线索 | 原投稿完整版本；若主张改题，需版本身份及差异证据 |
| [L022](../reviews/L022.md) | Arbitrary Structures / OOV | 官方匿名首段；无方法实验 | OpenReview PDF/API challenge；正式接收未核 | 合法完整版本及其正式身份 |
| [F05](../reviews/F05.md) | Samsung Online Cursive | 作者说明全文及实际图表；非正式全文 | 官方program/Crossref身份已核；IEEE PDF418 | 正式完整方法/训练/实验/附录；作者报告保留 |
| [L184](../reviews/L184.md) | Stroke-Seg | 正式文字/8式/4表、F2/F8实际图；核心partial | 其余原图F1/3/4/5/6/7/9未得到可核像素 | 补齐这些实际原图；保留实现与数据口径冲突 |

## 书目与版本修正

L006的DOI含2026，此前在线原始索引也登记2026-09-10；本批Crossref及Elsevier coredata明确卷761/124136、coverDate为2027-02-05。目录保留在线与卷期两个日期，恢复无年份后缀的正式题名。Elsevier XML虽名为full-text-retrieval-response，实际只有1826字节coredata，没有方法/实验正文。L002也恢复完整正式英文题名，旧简称保留为alias。

L021与ICDAR2025 Template-Guided Cascaded Diffusion存在布局→Imitating扩散及作者线索重合；正式摘要另述latent aggregation/high-frequency loss。尚无可读完整版本证明二者等同，没有合并或重复计完成。L022第三方ICLR标签与本次正式索引检索都不足以确认录用或拒稿，保留匿名投稿身份。

## 本轮工作能支持的研究判断

已经形成问题/数据/方法/指标/基线/实验条件及五项书面分析，并追到理论与发布实现。完成阅读只对应每篇明示的固定版本及范围，不代表独立复现、所有权重/训练数据均已下载或全仓源码均逐行审查。CompBench明确完成旧v2全文及正式正文交叉审查，正式新增实验supp条件仍缺；其他论文的复现条件缺项保留在各笔记。

终态字形、笔画实例、书写方向、事件顺序、抬笔接触与连续视频分别需要证据。静态编辑/字符集OCR/单帧评分/时间均值特征，均不足以单独证明规范笔顺过程正确；联合任务比分离基线高也需要控制数据、参数、外部教师、参考条件与预算后才能解释协同机制。BoundInk的边界监督前史及重叠指标限制、MME-Unify的正式表列/发布评分差异、CompBench跨版本边界均已入库，不能把已有机制或尚未验证的疑问包装成新贡献。

本项目的中文规范笔顺视频测试集、真实模型诊断与同预算联合/分离实验仍是研究计划，尚未执行。当前授权调研阶段没有推理、训练、OCR/judge/API模型调用，也没有准确率或速度复现成绩。外部来源受限的7项已如实留缺；本轮检索不保证覆盖所有未来发布或全部相关文献。

## 下一次工作的入口

收到可读原文或原图后，按上表逐项恢复，补方法/公式/完整主表与实际图，再更新验收。访问条件未变化时，不重复同一失败入口。实验阶段直接参考[最小方案](../experiments/stroke_order_pilot.md)和[实验顺序](../project/EXPERIMENTS.md)，其中的待测项不能改写为已证实结果。

本批逐文件操作及原因见[变更说明](two_hundred_twenty_first_changes_2026-10-25.md)。
