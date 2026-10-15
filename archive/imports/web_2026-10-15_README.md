> 网页版历史README；原计数与403为当时状态。链接已适配归档位置。

# UMM × 中文书写过程生成研究库

**从统一理解与生成，到笔顺、笔迹、艺术字书写视频及效率优化。**

整理日期：**2026-10-15**。本包已在本地完成；本次 GitHub 写入返回403，**没有成功提交到远端**。导入方式见 [PUBLISH_TO_GITHUB.md](../../PUBLISH_TO_GITHUB.md)。

## 从哪里开始

| 想了解什么 | 入口 |
|---|---|
| 这轮新增研究如何改变选题？ | **[重点调研与修订](../../docs/handwriting/01_focused_update_2026-10-15.md)** |
| UMM是什么、如何统一、怎样做科研？ | [UMM总览](../../docs/umm/00_overview.md) |
| UMM架构、推理、协同和效率文献 | [UMM文献表](../../docs/umm/literature.md) |
| 中文笔顺、轨迹、艺术字、视频和相关机制 | [书写专题文献表](../../docs/handwriting/literature.md) |
| 本轮新增的13项直接/邻近前作 | [新增文献表](../../docs/handwriting/new_literature.md) |
| 全部公开记录，按六字段整理 | [文献总表](../../docs/all_literature.md) |
| 四篇指定论文精读 | [DP-Font / DiffInk / HTR / Inverse Painting](../../docs/handwriting/papers/README.md) |
| 当前能力到哪里、哪些尚未证明？ | [能力矩阵](../../docs/handwriting/02_capability_matrix.md) |
| 规范、数据与标注 | [数据与标准](../../docs/handwriting/03_data_and_standards.md) |
| 如何设置强基线、效率与UMM归因？ | [模型与效率](../../docs/handwriting/04_baselines_and_efficiency.md) |
| 准备开展什么实验？ | [评测协议](../../docs/experiments/benchmark_protocol.md) / [研究假设](../../docs/experiments/research_hypotheses.md) / [五个决定性实验](../../docs/experiments/minimum_experiments.md) |

## 包含的记录

- **92项公开论文/研究记录、7项资源**，共99行。
- 其中48项论文继承2026-10-14公开记录；31项补全更早UMM主题；13项为本轮重点新增。
- 另有4项原匿名稿件保留私有占位，不公开标题、原稿、截图或结果。
- [JSON](../../data/literature.json)、[CSV](../../data/literature.csv)、[Excel](../../data/literature_public.xlsx)提供可检索版本。
- [历史目录](../../archive/README.md)保留两版公开安全笔记和原Excel八张表的CSV；不是静默覆盖历史。

## 本轮最重要的修订

“UMM+中文书法”并非空白：[UniCalli](https://arxiv.org/abs/2510.13745)已有列级识别/生成联合模型。
“轨迹+接触+累计墨迹+外观增强”并非空白：[OnOff](https://arxiv.org/abs/2608.03198)已建立物理渲染桥接。
视频文字并非没有专门评测：[VidScribe](https://arxiv.org/abs/2609.36598)、[VTR-Bench](https://arxiv.org/abs/2610.01499)已有多因素研究，前者包含手写演化。
但这些不等于已经证明中文指定规范的逐笔身份、顺序、方向、接触及长程状态全部正确。

因此候选贡献应落到**具体过程正确性、实际执行、少步事件保持、任务相关缓存或低监督泛化**，并与规则渲染、专门模型和外部VLM比较，而不是预设UMM一定最好。

## 阅读与证据规则

所有文献按 **研究论文—声明—方法—针对问题—结论—缺口** 组织，并增加来源、版本和核查状态。
历史记录、本轮摘要阅读、本轮方法/实验阅读分别标记；数值是作者报告，不是本次复现。
没有统一评测不等于模型一定失败；未查到前作不等于确证新颖性。
详见 [核查口径](../../docs/evidence/method_and_status.md)、[更新日志](../../docs/evidence/updates_2026-10-15.md)、[搜索记录](../../docs/evidence/search_log.md)。

## 验证整理文件

在本目录运行（Python 3.10+，仅使用标准库）：

```bash
python scripts/validate_catalog.py
python -m unittest discover -s tests -v
python scripts/stroke_metrics.py examples/toy_events.json
```

最后一条只是手工标注事件ID的玩具测试，不会从视频提取笔画，不代表任何模型成绩。真实模型结果模板在 `data/experiment_template.csv`，尚未填写。

## 发布与材料边界

本包不含字体文件、受限数据、模型权重、论文PDF和匿名投稿原稿。第三方来源遵守各自许可；本库笔记不授予第三方素材的再分发权。详细说明见 [PRIVATE_MATERIALS](../../docs/PRIVATE_MATERIALS.md)。

后续维护建议：新增来源先登记核查层级，记录模型/论文版本，保留失败访问与观点修订，再更新研究假设；不要只增加方法名称。
