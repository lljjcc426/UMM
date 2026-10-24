# 第一百九十二批逐文件变更说明

基础2b2fd5d。358目录（331论文／研究、27资源），297核心/302书面含未通过项；待完成核心深审34篇论文／研究；27项资源按制品协议另审。完成U28：2605.17766v1完整27页/HTML正文§1–5，AppA/B/C1–7/D1–2/E1–2/F/G，10张表全部行列、F1–9全部视觉、E2六个未编号科学QA图、8条编号公式及成本/配置未编号式；追引BAGEL/JanusPro/Harmon、RecA/UniGame/UniCoT、UEval/UnifiedBench/RealUnify、CLIP/SigLIP/Gemini Embedding/DPO。固定公开commit的17个下载文件中，重点逐段核Stage1 model/train、stage2代理、BAGEL aux/pretrain、两stageYAML/README/script与MathVista scorer；其余仅相关位置，不声称全2783文件完整阅读。五项书面记录与核心三遍完成；全部结果为论文/代码审查，未独立运行模型。。无文件删除。

| 文件 | 操作及原因 |
| --- | --- |
| [README.md](../../README.md) | 修改：追加本批范围、结论与专题入口 |
| [data/critical_reviews_2026-10-19.json](../../data/critical_reviews_2026-10-19.json) | 修改：U28完整原文问题/方法/实验/局限/思考 |
| [data/latentumm_full_dual_alignment_gradient_and_rollout_protocol_audit_2026-10-25.json](../../data/latentumm_full_dual_alignment_gradient_and_rollout_protocol_audit_2026-10-25.json) | 新增：本批原文证据、阅读范围和技术发现 |
| [data/literature.csv](../../data/literature.csv) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/literature.json](../../data/literature.json) | 修改：U28七协议、任务定位与原文来源 |
| [data/literature_public.xlsx](../../data/literature_public.xlsx) | 修改：经artifact工具同步变更行，保留五表和原格式并核看预览 |
| [data/one_hundred_ninety_second_review_batch_2026-10-25.json](../../data/one_hundred_ninety_second_review_batch_2026-10-25.json) | 新增：本批基准commit、完成ID和目录统计 |
| [data/reading_acceptance_2026-10-20.json](../../data/reading_acceptance_2026-10-20.json) | 修改：U28五项书面验收及实际阅读边界 |
| [data/reading_progress_2026-10-19.json](../../data/reading_progress_2026-10-19.json) | 修改：同步核心和书面验收进度 |
| [data/umm.csv](../../data/umm.csv) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/umm.json](../../data/umm.json) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/all_literature.md](../../docs/all_literature.md) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/foundations_and_transfer_2026-10-19.md](../../docs/evidence/foundations_and_transfer_2026-10-19.md) | 修改：补充方法假设、理论边界和迁移条件 |
| [docs/evidence/knowledge_gaps_2026-10-20.md](../../docs/evidence/knowledge_gaps_2026-10-20.md) | 修改：记录原文/制品/实验协议未决项 |
| [docs/evidence/latentumm_full_dual_alignment_gradient_and_rollout_protocol_audit_2026-10-25.md](../../docs/evidence/latentumm_full_dual_alignment_gradient_and_rollout_protocol_audit_2026-10-25.md) | 新增：完整方法、结果、批判问题和写作学习专题 |
| [docs/evidence/one_hundred_ninety_second_changes_2026-10-25.md](../../docs/evidence/one_hundred_ninety_second_changes_2026-10-25.md) | 新增：逐文件列出本批新增/修改的原因 |
| [docs/evidence/reading_ledger_2026-10-19.md](../../docs/evidence/reading_ledger_2026-10-19.md) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/scoped_literature_matrix_2026-10-19.md](../../docs/evidence/scoped_literature_matrix_2026-10-19.md) | 修改：更新实际任务、输入输出和方法适用范围 |
| [docs/evidence/search_log.md](../../docs/evidence/search_log.md) | 修改：记录主源版本、图表公式和实际查看范围 |
| [docs/evidence/second_round_audit_2026-10-19.md](../../docs/evidence/second_round_audit_2026-10-19.md) | 修改：区分未确认核心论文与按制品另审资源 |
| [docs/evidence/survey_queue_2026-10-19.md](../../docs/evidence/survey_queue_2026-10-19.md) | 修改：追加本批追引和未决核查队列 |
| [docs/evidence/tokenizer_theory_and_rl_2026-10-20.md](../../docs/evidence/tokenizer_theory_and_rl_2026-10-20.md) | 修改：补充表示/优化/后训机制的精确边界 |
| [docs/experiments/research_gaps_and_tests_2026-10-19.md](../../docs/experiments/research_gaps_and_tests_2026-10-19.md) | 修改：记录等预算、消融、反事实和可证伪方案，未执行 |
| [docs/project/STATUS.md](../../docs/project/STATUS.md) | 修改：更新本批及剩余论文/资源数量 |
| [docs/resources/nonpaper_research_2026-10-19.md](../../docs/resources/nonpaper_research_2026-10-19.md) | 修改：记录官方模型/源码/配置/数据发布与可访问范围 |
| [docs/reviews/README.md](../../docs/reviews/README.md) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/reviews/U28.md](../../docs/reviews/U28.md) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/umm/literature.md](../../docs/umm/literature.md) | 修改：同步U28结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
