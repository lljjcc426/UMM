# 仓库维护与科研证据规范

更新2026-10-27；当前协议stroke-video-v2。

| 位置 | 职责 |
| --- | --- |
| data/literature.json | 文献主数据；题录、方法、证据和版本 |
| data/reading_guide_2026-10-25.json | 会议、主题与停止跟进范围 |
| docs/reviews、docs/reading | 单篇和生成索引；改前核对应生成脚本 |
| data/discovery/generative_*.json | 生成模型补充题录、阅读范围与检索审计；与主目录独立登记 |
| docs/generative | 扩散、Flow、Drifting专题；总览、主题卡及预印本索引由补充JSON生成，综合分析与边界手工维护 |
| docs/research/v2 | 当前科学目标、信息契约、方法、数据评价与实验 |
| docs/project | 当前阶段导航与真实状态 |
| data/research/experiments_v2.json | 当前实验ID、依赖、状态及证据 |
| configs/research/stroke_video_v2.json | 计划参数、核心对照和资源前提，不是第三方训练配置 |
| templates/research_run_v2.json | 空白运行记录，性能字段初始null |
| docs/evidence、archive、docs/project/history | 来源核查和历史；不得当当前实验完成情况 |

v1文件保留，完整冻结状态见[199646c](https://github.com/lljjcc426/UMM/tree/199646c6960677f656594b3c542c8eb8aaf890f9)。当前入口由[研究工作区](docs/research/README.md)指定，运行记录必须固定协议版本；禁止把旧结果重命名为新协议。

## 证据层级

作者报告、原文核读、代码静态审查、确定性单元测试、模型实测、未验证假设分别标注。数据卡可见不等于取得数据或获再分发许可。任何completed实验需要run及原始结果路径；planned记录不应带虚构成绩。ready须有必要环境/输入清单和预算，blocked/stopped保留原因。

指标、合法序列、split、裁判、预算或采样策略改变时增加版本和原因；正式测试不参与选择最佳seed/阈值/基线。生成计划与RGB实际事件分开，三态观测、所有失败及重试保留。

每次运行记录代码/权重/数据revision、T/P/O与G0/G1输入权限、源组划分、训练与推理seed、共享/冻结参数、曝光/计算、硬件、完整命令、全部媒体、人工/自动标签、失败/未知与端到端成本。

不提交私有稿件、字体、未许可数据、模型权重、凭据和原始个人笔迹；已有匿名稿过滤保持。维护权威源数据后再生成导出，不以重渲染覆盖手工证据。新发现的摘要级来源先登记阅读范围，不能自动计为全文完成。

## 生成模型补充专题的维护

先修改 `data/discovery/generative_models_2026-10-30.json`，再运行 `python scripts/render_generative_survey.py`，更新专题README、9个主题页及预印本索引。`docs/generative/synthesis.md`、`search_scope.md`、`changes_2026-10-30.md` 手工维护，不由渲染器覆盖。

阅读层级分别为重点章节核读、正文片段选读和摘要筛选；正式论文集、官方目录与作者自报身份分别保存。补充记录不自动写入 `data/literature.json`、CSV、Excel或原核心阅读完成计数；后续整合须去重并保留实际覆盖。论文全文与下载缓存放在仓库外，公开交付保留来源URL、版本和中文分析。

## 检查命令

```bash
python scripts/validate_research_v2.py
python -m unittest tests.test_research_v2 -v
python scripts/validate_research_plan.py
python -m unittest tests.test_research_plan tests.test_stroke_metrics -v
python scripts/validate_catalog.py
```

有相应本地依赖时再运行全部测试。检查不验证外部链接、实际授权、模型性能或科学正确性。提交前重新读HEAD；使用期望SHA防并发覆盖，禁止force更新。
