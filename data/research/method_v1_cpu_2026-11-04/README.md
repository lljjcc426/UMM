# CPU方法接入产物

- `attachment/`：用户附件原始文档、2条合成样本、3个程序及原CPU视频/日志，按原内容保留。原文中的运行声明是附件制作时的记录。
- `integration_v1/`：本仓库对真实192条训练导出执行的新检查，含配对与划分、RGB/目标输入、SVG重建、四种随机模块特征/梯度及共享执行器的3个CPU视频和解码联系图。

原始压缩包仍位于用户Downloads；完整解包来源保存在本机`private/method_research_cpu_2026-11-04/original/`。接入代码位于`method_v1/`，与附件相比的修改见[报告](../../../docs/research/paired_strokes_v1/method_cpu_integration_2026-11-04.md)。

真实训练样本为原S0–S1的192字/1752笔，PNG仍从原数据目录读取，未复制或重写。静态SVG核对仅用于渲染一致性，不授予独立逐笔资格。相关来源/许可仍见[原数据许可](../paired_strokes_v1/source_licenses.csv)。三个新MP4的程序均由附件提供，无模型生成或训练。
