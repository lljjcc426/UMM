# 第一百九十批逐文件变更说明

基础707f06e。358目录（331论文／研究、27资源），295核心/300书面含未通过项；待完成核心深审36篇论文／研究；27项资源按制品协议另审。完成U26：完整2609.11929v1 PDF35页/HTML正文§1–6、§7contributors与参考追引，无附录；10编号式及未编号OPD/Beta表达、T1–23全部行、F1–5全部视觉及首页总览。固定repo735tree603blob结构，下载27个选定text文件；人工重点审README/训练NOTICE及说明、launcher/配置、ConvDecoder及模型选择/噪声片段、生成/交错评测说明、CVTG/LongText/RealUnify/UniMMMU/OpenING评分段、PE脚本与参数文档。未宣称完整逐行审603blob或27文件；HF最终/LoRA API文件清单、最终config已核，无权重下载/模型推理/训练/judgeAPI/基准重跑。核心三遍与五项书面检查完成，独立模型复现仍false。。无文件删除。

| 文件 | 操作及原因 |
| --- | --- |
| [README.md](../../README.md) | 修改：追加本批范围、结论与专题入口 |
| [data/critical_reviews_2026-10-19.json](../../data/critical_reviews_2026-10-19.json) | 修改：U26完整原文问题/方法/实验/局限/思考 |
| [data/literature.csv](../../data/literature.csv) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/literature.json](../../data/literature.json) | 修改：U26七协议、任务定位与原文来源 |
| [data/literature_public.xlsx](../../data/literature_public.xlsx) | 修改：经artifact工具同步变更行，保留五表和原格式并核看预览 |
| [data/one_hundred_ninetieth_review_batch_2026-10-25.json](../../data/one_hundred_ninetieth_review_batch_2026-10-25.json) | 新增：本批基准commit、完成ID和目录统计 |
| [data/reading_acceptance_2026-10-20.json](../../data/reading_acceptance_2026-10-20.json) | 修改：U26五项书面验收及实际阅读边界 |
| [data/reading_progress_2026-10-19.json](../../data/reading_progress_2026-10-19.json) | 修改：同步核心和书面验收进度 |
| [data/sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.json](../../data/sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.json) | 新增：本批原文证据、阅读范围和技术发现 |
| [data/umm.csv](../../data/umm.csv) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/umm.json](../../data/umm.json) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/all_literature.md](../../docs/all_literature.md) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/foundations_and_transfer_2026-10-19.md](../../docs/evidence/foundations_and_transfer_2026-10-19.md) | 修改：补充方法假设、理论边界和迁移条件 |
| [docs/evidence/knowledge_gaps_2026-10-20.md](../../docs/evidence/knowledge_gaps_2026-10-20.md) | 修改：记录原文/制品/实验协议未决项 |
| [docs/evidence/one_hundred_ninetieth_changes_2026-10-25.md](../../docs/evidence/one_hundred_ninetieth_changes_2026-10-25.md) | 新增：逐文件列出本批新增/修改的原因 |
| [docs/evidence/reading_ledger_2026-10-19.md](../../docs/evidence/reading_ledger_2026-10-19.md) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/scoped_literature_matrix_2026-10-19.md](../../docs/evidence/scoped_literature_matrix_2026-10-19.md) | 修改：更新实际任务、输入输出和方法适用范围 |
| [docs/evidence/search_log.md](../../docs/evidence/search_log.md) | 修改：记录主源版本、图表公式和实际查看范围 |
| [docs/evidence/second_round_audit_2026-10-19.md](../../docs/evidence/second_round_audit_2026-10-19.md) | 修改：区分未确认核心论文与按制品另审资源 |
| [docs/evidence/sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.md](../../docs/evidence/sensenova_u1_5_full_native_pixel_metrics_and_expert_distillation_audit_2026-10-25.md) | 新增：完整方法、结果、批判问题和写作学习专题 |
| [docs/evidence/survey_queue_2026-10-19.md](../../docs/evidence/survey_queue_2026-10-19.md) | 修改：追加本批追引和未决核查队列 |
| [docs/evidence/tokenizer_theory_and_rl_2026-10-20.md](../../docs/evidence/tokenizer_theory_and_rl_2026-10-20.md) | 修改：补充表示/优化/后训机制的精确边界 |
| [docs/experiments/research_gaps_and_tests_2026-10-19.md](../../docs/experiments/research_gaps_and_tests_2026-10-19.md) | 修改：记录等预算、消融、反事实和可证伪方案，未执行 |
| [docs/project/STATUS.md](../../docs/project/STATUS.md) | 修改：更新本批及剩余论文/资源数量 |
| [docs/resources/nonpaper_research_2026-10-19.md](../../docs/resources/nonpaper_research_2026-10-19.md) | 修改：记录官方模型/源码/配置/数据发布与可访问范围 |
| [docs/reviews/README.md](../../docs/reviews/README.md) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/reviews/U26.md](../../docs/reviews/U26.md) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/umm/literature.md](../../docs/umm/literature.md) | 修改：同步U26结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
