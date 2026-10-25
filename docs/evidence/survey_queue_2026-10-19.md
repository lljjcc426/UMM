# 当前阅读与定向复核规则

范围更新于2026-10-25。此前的持续补读队列已结束；当前任务是把已分析论文整理为可比较的研究路线，优先CVPR、ICCV、ECCV、NeurIPS、ICLR、ICML。原队列全文保存在[历史快照](../project/history/queue_before_focus_2026-10-25.md)。

## 当前队列

327篇论文已完成所记录范围的核心阅读。其余6篇资料未齐，按用户要求停止追取，退出当前队列，保留既有分析和缺项，详见[范围决定](../reading/scope.md)。当前未完成阅读队列为0；完成数量仍为327/333。

27项资源的公开协议审查已完成。实际受限或未发布的制品继续按原报告记录，不作为新增阅读待办，见[资源审查](resource_protocol_completion_and_source_limits_2026-10-25.md)。

## 现有论文怎么读

先看[跨论文分析与20篇核心对照](../reading/synthesis.md)，再按具体问题进入[会议／主题总览](../reading/README.md)。会议主表、作者录用声明和Workshop／Findings／Demo分别列出，投稿模板或他文引用不作为正式录用依据。

| 需要回答的问题 | 优先回查的已读论文 | 回查目的 |
| --- | --- | --- |
| 哪些表示保留语义和细部？ | Janus、Transfusion、Show-o2、Harmon、TokenFlow、TUNA、ReCA | 比较共享粒度、目标与码率；确认短笔及接触状态的信息上限 |
| 理解如何影响生成？ | DIVA、R3、CoRL、GvU、Unison、MME-Unify | 区分诊断、规划、执行、自评和共享训练收益 |
| 已有书写前作覆盖到哪里？ | DiffInk、UniCalli、XMP-Font、SDT、OLHWG、机器人书写 | 列清静态读写、轨迹、规范笔画与RGB过程各自真值 |
| 怎样使用与控制实际历史？ | Diffusion Forcing、History-Guided Video Diffusion、Self Forcing、Tora、DragAnything | 设计前缀干预、错误累积与事件身份对照 |
| 指标是否能识别目标错误？ | VBench、FVD内容偏置、clDice及本库过程指标说明 | 校准同终态错序、逆向、漏笔／重复和抬笔状态 |

这些是研究实施时的定向复核线索，不表示论文阅读未完成。需要核对具体公式、表格或代码版本时，沿用单篇笔记的原始来源。

## 后续选文标准

- 优先六会议中直接改变研究设计、基线或评价的工作。
- 直接中文书写前作、必要理论及高相关预印本保留，不因会场排序丢弃已有证据。
- 先判断新材料是否补充尚缺的机制证据；重复目录与二手摘要不扩大阅读任务。
- 论文身份、已读版本、完成范围和独立复现分别记载。

当前入口：[研究状态](../project/STATUS.md) · [研究判断](../project/DECISIONS.md) · [最小方案](../experiments/stroke_order_pilot.md)。
