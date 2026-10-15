# 文献与研究数据

`literature.json` 是当前主数据：280条记录，包括269条研究、11条资源。记录按来源标识归并，保留六字段、核查层级、版本、历史别名和 `evidence_history`。不能把整合记录数量当作全文精读数量。

- `literature.csv`、`literature_public.xlsx` 与 Markdown 表由 `scripts/render_catalog.py` 同步生成。
- `umm.*`、`resources.*`、`new_handwriting.*`、`local_additions.*` 是不同阅读视图，不与主表相加计数。
- `historical_public.*` 保留网页版原始2026-10-14的53条公开记录，不用新结论改写历史。
- `record_aliases.json` 对应365条来源记录及当前编号。
- `local_work_inventory.json` 记录20份本地研究文档的公开去向。
- `excluded_records.json` 保存1条已撤回研究及排除原因，不作为研究证据。
- `discovery/` 是检索候选层，与主目录有重叠，不作已读文献计数。
- `withheld_private_records.json` 记录原始附件的处理状态；原稿保留本地。
- `experiment_template.csv` 是未填写的实验记录模板，不是实验结果。

原记录把问题与方法合写时，当前表会保留此关系并指向完整历史笔记，不通过自动补全制造未核读内容。外部来源的可用性按各轮记录保留；本次结构检查没有重新访问全部外链。
