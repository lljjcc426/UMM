# 当前实验入口：stroke-video-v2

更新于2026-10-27。**17个实验均planned，无新数据、模型运行或评分器校准结果。**

[完整实验对照、交付和停止规则](../research/v2/experiments.md) · [机器登记v2](../../data/research/experiments_v2.json) · [阶段路线](ROADMAP.md)。

保留v1实验语义，并新增ADAPT-01、EVAL-02、CAUSAL-01：

| 阶段 | 实验ID |
| --- | --- |
| P0 | ENV-01、DATA-01、EVAL-01 |
| P1 | SO-00、BASE-01、EVAL-02、SO-01 |
| P2 | FIT-01、ADAPT-01、SO-02 |
| P3 | SO-03A、SO-03B、CAUSAL-01、SO-03C |
| P4可选 | REC-01 |
| P5 | SO-04 |
| P6可选 | EF-01 |

关键改动：EVAL-01不再依赖GPU环境；EVAL-02覆盖实际生成域；同数据领域适配先于新机制；共享与反馈各自归因；REC-01不阻塞正式生成泛化验证。依赖表示前置实验完成并记录结论，不表示必须取得正结果。

运行使用[模板v2](../../templates/research_run_v2.json)，固定T/P/O及G0/G1、源权限、状态/历史来源、codec和窗口、共享参数、全部尝试和独立评价。完成必须有运行记录及结果制品，不能用文档/CI填模型成绩。

已有[PX-01](../experiments/process_probe.md)只是8个受控像素案例。历史[登记v1](../../data/research/experiments_v1.json)及[原实验页](../../archive/research_v1_2026-10-27/EXPERIMENTS.md.txt)保留，不得将v1计划视为已运行结果。
