# UMM × 中文书写过程生成研究库

**从统一理解与生成，到笔顺、笔迹、艺术字书写视频及效率优化。**

整理日期：**2026-10-15**。本仓库是本次研究的持续记录与跟进仓库，已整合网页版目录包和本地历轮调查。网页版连接曾返回403；本地已改用拥有仓库权限的 Git 登录进行导入。实际同步记录见 [交付状态](reports/delivery_status.json)，历史与当前方式见 [发布说明](PUBLISH_TO_GITHUB.md)。

## 从哪里开始

| 想了解什么 | 入口 |
|---|---|
| 当前做到哪里，接下来做什么？ | **[项目状态](docs/project/STATUS.md)** / [研究决策](docs/project/DECISIONS.md) / [实验跟进](docs/project/EXPERIMENTS.md) |
| 两套资料整合后怎样判断方向？ | **[综合研究地图](docs/RESEARCH_MAP.md)** |
| UMM有没有专门做笔顺，我们具体如何做？ | **[笔顺专项研究方案](docs/handwriting/05_stroke_order_umm.md)** / [原文证据核查](docs/handwriting/06_stroke_order_evidence.md) |
| 这轮新增研究如何改变选题？ | **[重点调研与修订](docs/handwriting/01_focused_update_2026-10-15.md)** |
| UMM是什么、如何统一、怎样做科研？ | [UMM总览](docs/umm/00_overview.md) |
| UMM架构、推理、协同和效率文献 | [UMM文献表](docs/umm/literature.md) |
| 中文笔顺、轨迹、艺术字、视频和相关机制 | [书写专题文献表](docs/handwriting/literature.md) |
| 网页版新增的13项直接/邻近前作 | [网页重点文献表](docs/handwriting/new_literature.md) |
| 本地历轮调查补入的研究 | [本地补充文献视图](docs/local_additions.md) / [历轮笔记](archive/local/README.md) |
| 全部公开记录，按六字段整理 | [文献总表](docs/all_literature.md) |
| 网页版四篇指定论文精读 | [DP-Font / DiffInk / HTR / Inverse Painting](docs/handwriting/papers/README.md) |
| 本地附件对应的可公开研究 | [Timage / BoxTuning / ORVOS 公开预印本分析](docs/evidence/public_preprint_reviews.md) |
| 当前能力到哪里、哪些尚未证明？ | [能力矩阵](docs/handwriting/02_capability_matrix.md) |
| 规范、数据与标注 | [数据与标准](docs/handwriting/03_data_and_standards.md) |
| 如何设置强基线、效率与UMM归因？ | [模型与效率](docs/handwriting/04_baselines_and_efficiency.md) |
| 准备开展什么实验？ | [评测协议](docs/experiments/benchmark_protocol.md) / [研究假设](docs/experiments/research_hypotheses.md) / [五个决定性实验](docs/experiments/minimum_experiments.md) |

## 包含的记录

- **269项公开论文／研究记录、11项资源，共280条主记录**。包括预印本、基准及相邻研究，不是280篇全文精读或280个原生UMM。
- 原始网页版99条记录、本地116条可公开专题记录、143条通用UMM记录和7条专项补充形成365条来源记录，经论文标识与资源实体去重归并。
- 另存 **573条arXiv检索元数据、200条综述仓库候选**，二者有重叠，不相加作为已读论文数；1条撤回记录单列，不作结论依据。
- 四份原附件及未公开材料保留本地。三项已核对公开预印本，公开笔记只依公开版本；其余继续保留私有占位。
- [JSON](data/literature.json)、[CSV](data/literature.csv)、[Excel](data/literature_public.xlsx)提供可检索版本。
- [历史目录](archive/README.md)保留两版公开安全笔记和原Excel八张表的CSV；不是静默覆盖历史。
- [整合说明](docs/evidence/integration_2026-10-15.md)记录去重、版本、修订和文件变更；[历史编号映射](data/record_aliases.json)连接365条来源记录与主目录。

## 本轮最重要的修订

“UMM+中文书法”并非空白：[UniCalli](https://arxiv.org/abs/2510.13745)已有列级识别/生成联合模型。
“轨迹+接触+累计墨迹+外观增强”并非空白：[OnOff](https://arxiv.org/abs/2608.03198)已建立物理渲染桥接。
视频文字并非没有专门评测：[VidScribe](https://arxiv.org/abs/2609.36598)、[VTR-Bench](https://arxiv.org/abs/2610.01499)已有多因素研究，前者包含手写演化。
但这些不等于已经证明中文指定规范的逐笔身份、顺序、方向、接触及长程状态全部正确。

因此候选贡献应落到**具体过程正确性、实际执行、少步事件保持、任务相关缓存或低监督泛化**，并与规则渲染、专门模型和外部VLM比较，而不是预设UMM一定最好。

按当前用户重点，**实际笔顺正确性与UMM归因是主线，效率是第二阶段问题**。InkSight已有含中文的读写联合训练，XMP-Font已有静态笔顺预测损失，LVGM已有逐笔矢量生成。需证明实际过程理解能改善生成执行，而不只是认字、背规则或提高最终帧OCR。

层级双域HTR的91.2%是起点、笔画数与总长度的综合分，不能解释为严格笔顺正确率。更多结论修订见[研究决策](docs/project/DECISIONS.md)。

## 阅读与证据规则

所有文献按 **研究论文—声明—方法—针对问题—结论—缺口** 组织，并增加来源、版本和核查状态。
历史记录、本轮摘要阅读、本轮方法/实验阅读分别标记；数值是作者报告，不是本次复现。
没有统一评测不等于模型一定失败；未查到前作不等于确证新颖性。
详见 [核查口径](docs/evidence/method_and_status.md)、[更新日志](docs/evidence/updates_2026-10-15.md)、[搜索记录](docs/evidence/search_log.md)。

## 验证整理文件

在本目录运行（Python 3.10+；检查与事件指标使用标准库）：

```bash
python scripts/validate_catalog.py
python -m unittest discover -s tests -v
python scripts/stroke_metrics.py examples/toy_events.json
```

最后一条只是手工标注事件ID的玩具测试，不会从视频提取笔画，不代表任何模型成绩。真实模型结果模板在 `data/experiment_template.csv`，尚未填写。

## 发布与材料边界

本包不含字体文件、受限数据、模型权重、论文PDF和匿名投稿原稿。第三方来源遵守各自许可；本库笔记不授予第三方素材的再分发权。详细说明见 [PRIVATE_MATERIALS](docs/PRIVATE_MATERIALS.md)。

后续维护建议：新增来源先登记核查层级，记录模型/论文版本，保留失败访问与观点修订，再更新研究假设；不要只增加方法名称。

更新 `data/literature.json` 后，安装 `requirements.txt` 中的 openpyxl，运行 `python scripts/render_catalog.py` 同步Markdown、CSV和Excel。候选数据放在 `data/discovery/`。每次实质工作同步项目状态及变更日志；具体约定见 [AGENTS.md](AGENTS.md)。
