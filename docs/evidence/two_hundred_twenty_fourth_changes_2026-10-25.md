# 第二百二十四批逐文件变更说明

日期：2026-10-25；基线：2d61ab93。7篇核心深审仍未完成，新增A06出版社F1–8实际原图阅读。未删除文件，未执行模型。

| 文件 | 操作及原因 |
| --- | --- |
| [README.md](../../README.md) | 修改当前阅读范围，添加本批入口及保留7篇缺项的说明。 |
| [data/critical_reviews_2026-10-19.json](../../data/critical_reviews_2026-10-19.json) | 更新A06：三编码分支、FC/CE、三种字体、StrokeGAN定性比较、逐图边界及待证机制。保持first_pass_only。 |
| [data/literature.json](../../data/literature.json) | 同步A06当前方法、指标、数据、限制、两幅关键原图来源及本批阅读历史；保留历史记录。 |
| [data/literature.csv](../../data/literature.csv) | 从主数据生成A06对应行，供检索和分析使用。 |
| [data/literature_public.xlsx](../../data/literature_public.xlsx) | 用Artifact Tool修改A06在“全部记录”和“书写及相关”的两行内容及行高；保留其他记录、工作表和原有样式/原生部件。 |
| [data/remaining_source_access_and_reading_handoff_2026-10-25.json](../../data/remaining_source_access_and_reading_handoff_2026-10-25.json) | 更新7篇最新来源核查，前批结果保留为previous_batch_access_checks；核心完成数未升级。 |
| [data/seven_remaining_source_and_figure_audit_2026-10-25.json](../../data/seven_remaining_source_and_figure_audit_2026-10-25.json) | 新增本批结构化记录：8图独立URL、实际像素查看、观察/解释范围，以及7篇缺项。 |
| [docs/all_literature.md](../all_literature.md) | 生成全部目录中的A06更新。 |
| [docs/handwriting/literature.md](../handwriting/literature.md) | 生成书写目录中的A06更新。 |
| [docs/reviews/A06.md](../reviews/A06.md) | 生成A06方法与批判分析，明确已读全部原图及尚缺完整正文。 |
| [docs/reviews/README.md](../reviews/README.md) | 同步A06已读范围索引。 |
| [docs/project/STATUS.md](../project/STATUS.md) | 当前批次更新为224，记录图像阅读增量与未完成项。 |
| [docs/evidence/remaining_source_access_and_reading_handoff_2026-10-25.md](remaining_source_access_and_reading_handoff_2026-10-25.md) | 更新7篇阅读矩阵，纠正L022缓存页范围和ResearchGate全文提供方。 |
| [docs/evidence/seven_remaining_source_and_figure_audit_2026-10-25.md](seven_remaining_source_and_figure_audit_2026-10-25.md) | 新增8图分析、方法判断、待核反证和7篇所需材料。 |
| 本文件 | 新增逐文件变更说明。 |

检查范围：目录/笔记生成、仓库结构与本地链接校验、差异空白检查；Excel已核目标行取值与修改前后图像，并比较保存文件中非目标行及原生部件的保留情况。核心完成仍为326/333，五条书面记录仍为329项。没有新增模型测试或复现结果。
