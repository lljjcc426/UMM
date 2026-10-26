# 当前研究与阅读状态

更新于2026-10-25。当前重点：整理已分析论文，优先梳理CVPR、ICCV、ECCV、NeurIPS、ICLR、ICML的研究脉络。入口为[阅读总览](../reading/README.md)与[20篇核心对照](../reading/synthesis.md)。

## 阅读范围

| 项目 | 当前数量与含义 |
| --- | --- |
| 主目录 | 360条：333篇论文／研究，27项资源 |
| 论文核心阅读完成 | 327篇；具体正文、附录、代码及版本范围见单篇笔记 |
| 资料未齐、停止跟进 | 6篇：A06、F05、L002、L006、L021、L022；未计入完成 |
| 当前未完成阅读队列 | 0篇；6篇已按用户要求退出队列 |
| 资源公开协议审查 | 27项完成；实际数据、权重等制品缺项另列 |
| 已有本地实验 | 受控像素过程与事件指标检查；尚无模型训练、推理或独立模型复现 |

本次整理没有新增论文阅读；同步远端7cb7a17b已有的L184完成记录，验收源数据相应更新。停止跟进决定见[范围说明](../reading/scope.md)；逐项完成证据见[验收台账](../evidence/reading_ledger_2026-10-19.md)，结构化状态见[阅读进度](../../data/reading_progress_2026-10-19.json)。

## 已读研究的主要路线

1. **架构与视觉表示：**Janus、Transfusion、Show-o2比较接口与目标；Harmon、TokenFlow、TUNA、ReCA比较共享表示、细节保留与对齐。先测表示能否保存关键事件，再测主干能否利用。
2. **协同与联合评价：**DIVA、R3、Unison、MME-Unify区分同一模型支持两种任务、条件链条有效及共享训练的额外收益。需控制数据、信息和全链路计算。
3. **书写直接前作：**DiffInk、UniCalli、XMP-Font与轮廓感知机器人书写分别覆盖在线轨迹、静态读写、笔画先验与可执行轨迹，限定宽泛新颖性主张。
4. **历史与实际执行：**Diffusion Forcing、History-Guided Video Diffusion、Self Forcing、Tora、DragAnything提供历史条件和运动控制参照；规范笔画身份、接触与严格先后仍需独立验证。

每条路线的方法、证据限制和实验用途见[跨论文分析](../reading/synthesis.md)。[六会议索引](../reading/README.md)区分会议正式归属、作者声明和其他轨道；七个主题索引覆盖全部327篇已完成论文。

## 接下来应验证的研究问题

| 问题 | 主要对照 | 判断依据 |
| --- | --- | --- |
| 是否读取实际历史？ | 同末帧不同历史、交换与遮蔽历史、同信息外部VLM | 判断随相关过程干预而改变，能绑定实例并定位首错 |
| 理解是否改善实际执行？ | 固定生成器，分别提供真值、模型与错误状态／规划 | 状态与决策改善传递到事件级执行和整字过程成功率 |
| 共享训练是否有额外收益？ | 共享、分离及流水线系统；匹配数据曝光与计算 | 多任务收益、泛化及全链路成本，连同退步项报告 |

这些是由文献提出的待验证问题。实施方案见[最小研究方案](../experiments/stroke_order_pilot.md)、[实验计划](EXPERIMENTS.md)与[研究判断](DECISIONS.md)。新实验尚未执行。

## 维护与历史

- [当前阅读与复核规则](../evidence/survey_queue_2026-10-19.md)：按研究问题定向回查，停止缺失资料追取。
- [主题与会议配置](../../data/reading_guide_2026-10-25.json)及[组织结果](../../data/reading_organization_2026-10-25.json)。
- [资源公开协议与制品边界](../evidence/resource_protocol_completion_and_source_limits_2026-10-25.md)。
- [本次逐文件说明](../evidence/repository_organization_changes_2026-10-25.md)。
- [整理前状态全文](history/status_before_focus_2026-10-25.md)及[批次历史](history/reading_updates_2026-10-19_to_25.md)。历史中的阶段性计数和旧待办保留用于追溯。
