# 第二百二十三批逐文件变更说明

基础提交cea09604。360目录（333论文／研究、27资源），326论文核心完成；329项历史五条书面记录中328论文、1资源，包含未通过项。本批补审27资源共135项，七篇论文全文/原图补访未解决；实际原始包/未发布流程等缺项逐项保留。无文件删除、模型训练/推理/judge或独立复现。

已执行检查：目录字段与内部链接、资源ID/五项回答/边界覆盖；Excel更新前后预览与主表值核对，5工作表及无关内容/样式/原生部分保留。确定性数据解析的范围见本批报告，不以此代替模型评测。校验器另外更新本地忽略文件`reports/validation.json`，该运行产物不提交。

| 文件 | 操作及原因 |
| --- | --- |
| [README.md](../../README.md) | 修改：更新333论文/27资源/360总数和导航；增加资源审查、七篇访问缺项与本批入口 |
| [data/critical_reviews_2026-10-19.json](../../data/critical_reviews_2026-10-19.json) | 修改：27项资源补实际文件/源码/图像阅读，修正过期范围及未发布流程；不升级论文核心数 |
| [data/literature.csv](../../data/literature.csv) | 修改：由主目录重新生成对应分类视图，同步27项资源；不增删研究记录 |
| [data/literature.json](../../data/literature.json) | 修改：27资源主记录补范围、版本、来源、字段、结论及制品验收路径，旧结论保留在review_history |
| [data/literature_public.xlsx](../../data/literature_public.xlsx) | 修改：artifact工具同步27资源/81行出现位置；保留5工作表、其它单元格、样式、筛选与原生部分，核看前后预览 |
| [data/local_additions.csv](../../data/local_additions.csv) | 修改：由主目录重新生成对应分类视图，同步27项资源；不增删研究记录 |
| [data/local_additions.json](../../data/local_additions.json) | 修改：由主目录重新生成对应分类视图，同步27项资源；不增删研究记录 |
| [data/reading_progress_2026-10-19.json](../../data/reading_progress_2026-10-19.json) | 修改：单列326/333论文核心、328论文书面记录、1历史资源记录和27资源/135项协议回答 |
| [data/remaining_source_access_and_reading_handoff_2026-10-25.json](../../data/remaining_source_access_and_reading_handoff_2026-10-25.json) | 修改：更新360/326统计及七篇本批补访结果；前批来源检查保留previous_batch_access_checks |
| [data/resource_acceptance_2026-10-25.json](../../data/resource_acceptance_2026-10-25.json) | 新增：新增27资源逐项五问、版本/来源、22项实际制品检查及4项原包待取/1项发布未确认的边界 |
| [data/resource_artifact_observations_2026-10-25.json](../../data/resource_artifact_observations_2026-10-25.json) | 新增：新增字典、规范索引、OSF工作表、样图、54维统计与10个parquet的确定性审查摘要 |
| [data/resources.csv](../../data/resources.csv) | 修改：由主目录重新生成对应分类视图，同步27项资源；不增删研究记录 |
| [data/resources.json](../../data/resources.json) | 修改：由主目录重新生成对应分类视图，同步27项资源；不增删研究记录 |
| [data/two_hundred_twenty_third_review_batch_2026-10-25.json](../../data/two_hundred_twenty_third_review_batch_2026-10-25.json) | 新增：记录基础commit、34个补访/补审ID、27资源完成范围和7篇仍缺原文的状态 |
| [docs/all_literature.md](../../docs/all_literature.md) | 修改：由主目录生成分类Markdown，反映资源新来源、证据与剩余制品缺项 |
| [docs/evidence/knowledge_gaps_2026-10-20.md](../../docs/evidence/knowledge_gaps_2026-10-20.md) | 修改：追加资源发布/原包与七篇全文/原图的剩余缺项 |
| [docs/evidence/reading_ledger_2026-10-19.md](../../docs/evidence/reading_ledger_2026-10-19.md) | 修改：资源单列协议完成和制品缺项，移除资源不适用的论文三遍未完成标签 |
| [docs/evidence/remaining_source_access_and_reading_handoff_2026-10-25.md](../../docs/evidence/remaining_source_access_and_reading_handoff_2026-10-25.md) | 修改：更新当前七项来源矩阵，逐项说明访问响应与仍需全文/实际图 |
| [docs/evidence/resource_protocol_completion_and_source_limits_2026-10-25.md](../../docs/evidence/resource_protocol_completion_and_source_limits_2026-10-25.md) | 新增：新增27项协议结论、实际新增证据、七篇访问缺项及对研究方案的影响 |
| [docs/evidence/search_log.md](../../docs/evidence/search_log.md) | 修改：记录主源版本与实际文件/图像/源码范围，区分失败响应和原文 |
| [docs/evidence/second_round_audit_2026-10-19.md](../../docs/evidence/second_round_audit_2026-10-19.md) | 修改：修正当前进度口径并追加本批，旧批次快照保留 |
| [docs/evidence/survey_queue_2026-10-19.md](../../docs/evidence/survey_queue_2026-10-19.md) | 修改：追加本批完成与下一步所需的具体来源 |
| [docs/evidence/two_hundred_twenty_third_changes_2026-10-25.md](../../docs/evidence/two_hundred_twenty_third_changes_2026-10-25.md) | 新增：逐项列出本批所有新增/修改文件及原因；无文件删除 |
| [docs/handwriting/literature.md](../../docs/handwriting/literature.md) | 修改：由主目录生成分类Markdown，反映资源新来源、证据与剩余制品缺项 |
| [docs/local_additions.md](../../docs/local_additions.md) | 修改：由主目录生成分类Markdown，反映资源新来源、证据与剩余制品缺项 |
| [docs/project/STATUS.md](../../docs/project/STATUS.md) | 修改：更新当前326/333论文核心和27资源协议状态，保留历史批次 |
| [docs/resources/nonpaper_research_2026-10-19.md](../../docs/resources/nonpaper_research_2026-10-19.md) | 修改：追加27项资源协议的当前审查与未发布/不可取得制品边界 |
| [docs/reviews/H001.md](../../docs/reviews/H001.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/L044.md](../../docs/reviews/L044.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/L048.md](../../docs/reviews/L048.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/L049.md](../../docs/reviews/L049.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/L050.md](../../docs/reviews/L050.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R01.md](../../docs/reviews/R01.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R02.md](../../docs/reviews/R02.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R03.md](../../docs/reviews/R03.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R04.md](../../docs/reviews/R04.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R05.md](../../docs/reviews/R05.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R06.md](../../docs/reviews/R06.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R07.md](../../docs/reviews/R07.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R08.md](../../docs/reviews/R08.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R09.md](../../docs/reviews/R09.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R10.md](../../docs/reviews/R10.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R11.md](../../docs/reviews/R11.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/R12.md](../../docs/reviews/R12.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/README.md](../../docs/reviews/README.md) | 修改：更新27项实际阅读范围，说明论文与资源的验收模板差异 |
| [docs/reviews/S007.md](../../docs/reviews/S007.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S008.md](../../docs/reviews/S008.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S009.md](../../docs/reviews/S009.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S010.md](../../docs/reviews/S010.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S011.md](../../docs/reviews/S011.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S012.md](../../docs/reviews/S012.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S013.md](../../docs/reviews/S013.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S014.md](../../docs/reviews/S014.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S015.md](../../docs/reviews/S015.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [docs/reviews/S016.md](../../docs/reviews/S016.md) | 修改：该资源补实际制品/源码证据、字段/版本/适用范围及五项协议审查；保留未取得与未执行项 |
| [scripts/render_reviews.py](../../scripts/render_reviews.py) | 修改：增加资源专用模板/五项验收、资源台账和进度，保留论文三遍标准 |
| [scripts/validate_catalog.py](../../scripts/validate_catalog.py) | 修改：校验资源验收ID与主表一致、每项有5条实质回答及具体制品边界 |
