# 第一百六十九批逐文件变更说明

基础34d22c6。357目录（330论文／研究、27资源），275核心/280书面含未通过项；未确认核心55论文／研究+27资源。完成L158：CVPR2025正式main11p（pp13178–13188）与官方supp11p全部研究内容：§1–8、AppA1–8/B1–2/C/D/E1–4/F/G1/H/I，Algorithm1、Eq1–12、T1–9每行/F1–14所有实际PDF图（含F13失败/F14十六样例）；F4仅视觉趋势未数字化曲线。arXivv2HTML交叉抽数值T1–7，原版PDF逐表核。GH固定README/training.md/configdata和scriptsconfig全文；pipeline load_pretrained/__call__参数/任务门控/条件预处理/采样循环与输出、train噪声/缺模态/compute_loss、scheduler构造/step、TextVAE encode/connect/mean相关段，未称全文读完2500行train或全部代码。HF v0.5/v0.9/数据集元数据pin；未下载权重/大包，未执行模型。三遍核心阅读及五项书面，无独立口试/复现。。无文件删除。

| 文件 | 操作及原因 |
| --- | --- |
| [README.md](../../README.md) | 修改：追加本批范围、结论与专题入口 |
| [data/critical_reviews_2026-10-19.json](../../data/critical_reviews_2026-10-19.json) | 修改：L158完整原文问题/方法/实验/局限/思考 |
| [data/literature.csv](../../data/literature.csv) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/literature.json](../../data/literature.json) | 修改：L158七协议、任务定位与原文来源 |
| [data/literature_public.xlsx](../../data/literature_public.xlsx) | 修改：经artifact工具同步变更行，保留五表和原格式并核看预览 |
| [data/local_additions.csv](../../data/local_additions.csv) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/local_additions.json](../../data/local_additions.json) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/omniflow_guidance_formula_and_released_task_coverage_audit_2026-10-24.json](../../data/omniflow_guidance_formula_and_released_task_coverage_audit_2026-10-24.json) | 新增：本批原文证据、阅读范围和技术发现 |
| [data/one_hundred_sixty_ninth_review_batch_2026-10-24.json](../../data/one_hundred_sixty_ninth_review_batch_2026-10-24.json) | 新增：本批基准commit、完成ID和目录统计 |
| [data/reading_acceptance_2026-10-20.json](../../data/reading_acceptance_2026-10-20.json) | 修改：L158五项书面验收及实际阅读边界 |
| [data/reading_progress_2026-10-19.json](../../data/reading_progress_2026-10-19.json) | 修改：同步核心和书面验收进度 |
| [data/umm.csv](../../data/umm.csv) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [data/umm.json](../../data/umm.json) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/all_literature.md](../../docs/all_literature.md) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/foundations_and_transfer_2026-10-19.md](../../docs/evidence/foundations_and_transfer_2026-10-19.md) | 修改：补充方法假设、理论边界和迁移条件 |
| [docs/evidence/knowledge_gaps_2026-10-20.md](../../docs/evidence/knowledge_gaps_2026-10-20.md) | 修改：记录原文/制品/实验协议未决项 |
| [docs/evidence/omniflow_guidance_formula_and_released_task_coverage_audit_2026-10-24.md](../../docs/evidence/omniflow_guidance_formula_and_released_task_coverage_audit_2026-10-24.md) | 新增：完整方法、结果、批判问题和写作学习专题 |
| [docs/evidence/one_hundred_sixty_ninth_changes_2026-10-24.md](../../docs/evidence/one_hundred_sixty_ninth_changes_2026-10-24.md) | 新增：逐文件列出本批新增/修改的原因 |
| [docs/evidence/reading_ledger_2026-10-19.md](../../docs/evidence/reading_ledger_2026-10-19.md) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/evidence/scoped_literature_matrix_2026-10-19.md](../../docs/evidence/scoped_literature_matrix_2026-10-19.md) | 修改：更新实际任务、输入输出和方法适用范围 |
| [docs/evidence/search_log.md](../../docs/evidence/search_log.md) | 修改：记录主源版本、图表公式和实际查看范围 |
| [docs/evidence/second_round_audit_2026-10-19.md](../../docs/evidence/second_round_audit_2026-10-19.md) | 修改：区分未确认核心论文与按制品另审资源 |
| [docs/evidence/survey_queue_2026-10-19.md](../../docs/evidence/survey_queue_2026-10-19.md) | 修改：追加本批追引和未决核查队列 |
| [docs/experiments/research_gaps_and_tests_2026-10-19.md](../../docs/experiments/research_gaps_and_tests_2026-10-19.md) | 修改：记录等预算、消融、反事实和可证伪方案，未执行 |
| [docs/local_additions.md](../../docs/local_additions.md) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/project/STATUS.md](../../docs/project/STATUS.md) | 修改：更新本批及剩余论文/资源数量 |
| [docs/reviews/L158.md](../../docs/reviews/L158.md) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/reviews/README.md](../../docs/reviews/README.md) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
| [docs/umm/literature.md](../../docs/umm/literature.md) | 修改：同步L158结构化笔记、阅读索引、分类Markdown/CSV/JSON，保留历史 |
