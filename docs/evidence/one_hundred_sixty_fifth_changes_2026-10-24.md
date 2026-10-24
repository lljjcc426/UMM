# 第一百六十五批逐文件变更说明

基础b7c2d11。357目录（330论文／研究、27资源），271核心/276书面含未通过项；未确认核心59论文／研究+27资源。完成L152：正式完整36页已取得；§1–5和AppA1–A7全部研究正文、T1–14及T15/续页极坐标图、Algo1/Eq1–4，F1–13实际图/图注核读，图中生成选例做定性观察，未逐像素OCR或重建全部极坐标值；参考文献只追引相关条目，NeurIPS行政checklist不作为研究正文精读。与v3指定内容分版。固定GH完整45文件列表，五个评分主脚本、text_utils、inference、utils及生成入口、总体调用、fine_grained风格分组核读；未逐行审完依赖LLM2Vec内部或运行权重。GH两CSV/HF两JSON、7 Q/D、两文字参考/两知识参考计数核查。三遍指定位/方法与图表/批判书面范围，无独立模型复现、口试或人评。。无文件删除。

| 文件 | 操作及原因 |
| --- | --- |
| [README.md](../../README.md) | 修改：追加本批范围、结论与专题入口 |
| [data/critical_reviews_2026-10-19.json](../../data/critical_reviews_2026-10-19.json) | 修改：L152完整原文问题/方法/实验/局限/思考 |
| [data/literature.csv](../../data/literature.csv) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/literature.json](../../data/literature.json) | 修改：L152七协议、任务定位与原文来源 |
| [data/literature_public.xlsx](../../data/literature_public.xlsx) | 修改：经artifact工具同步变更行，保留五表和原格式并核看预览 |
| [data/local_additions.csv](../../data/local_additions.csv) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/local_additions.json](../../data/local_additions.json) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/one_hundred_sixty_fifth_review_batch_2026-10-24.json](../../data/one_hundred_sixty_fifth_review_batch_2026-10-24.json) | 新增：本批基准commit、完成ID和目录统计 |
| [data/oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.json](../../data/oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.json) | 新增：本批原文证据、阅读范围和技术发现 |
| [data/reading_acceptance_2026-10-20.json](../../data/reading_acceptance_2026-10-20.json) | 修改：L152五项书面验收及实际阅读边界 |
| [data/reading_progress_2026-10-19.json](../../data/reading_progress_2026-10-19.json) | 修改：同步核心和书面验收进度 |
| [data/umm.csv](../../data/umm.csv) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/umm.json](../../data/umm.json) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/all_literature.md](../../docs/all_literature.md) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/foundations_and_transfer_2026-10-19.md](../../docs/evidence/foundations_and_transfer_2026-10-19.md) | 修改：补充方法假设、理论边界和迁移条件 |
| [docs/evidence/knowledge_gaps_2026-10-20.md](../../docs/evidence/knowledge_gaps_2026-10-20.md) | 修改：记录原文/制品/实验协议未决项 |
| [docs/evidence/one_hundred_sixty_fifth_changes_2026-10-24.md](../../docs/evidence/one_hundred_sixty_fifth_changes_2026-10-24.md) | 新增：逐文件列出本批新增/修改的原因 |
| [docs/evidence/oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.md](../../docs/evidence/oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.md) | 新增：完整方法、结果、批判问题和写作学习专题 |
| [docs/evidence/reading_ledger_2026-10-19.md](../../docs/evidence/reading_ledger_2026-10-19.md) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/scoped_literature_matrix_2026-10-19.md](../../docs/evidence/scoped_literature_matrix_2026-10-19.md) | 修改：更新实际任务、输入输出和方法适用范围 |
| [docs/evidence/search_log.md](../../docs/evidence/search_log.md) | 修改：记录主源版本、图表公式和实际查看范围 |
| [docs/evidence/second_round_audit_2026-10-19.md](../../docs/evidence/second_round_audit_2026-10-19.md) | 修改：区分未确认核心论文与按制品另审资源 |
| [docs/evidence/survey_queue_2026-10-19.md](../../docs/evidence/survey_queue_2026-10-19.md) | 修改：追加本批追引和未决核查队列 |
| [docs/experiments/research_gaps_and_tests_2026-10-19.md](../../docs/experiments/research_gaps_and_tests_2026-10-19.md) | 修改：记录等预算、消融、反事实和可证伪方案，未执行 |
| [docs/local_additions.md](../../docs/local_additions.md) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/project/STATUS.md](../../docs/project/STATUS.md) | 修改：更新本批及剩余论文/资源数量 |
| [docs/resources/nonpaper_research_2026-10-19.md](../../docs/resources/nonpaper_research_2026-10-19.md) | 修改：记录官方模型/源码/配置/数据发布与可访问范围 |
| [docs/reviews/L152.md](../../docs/reviews/L152.md) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/reviews/README.md](../../docs/reviews/README.md) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/umm/literature.md](../../docs/umm/literature.md) | 修改：同步L152结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
