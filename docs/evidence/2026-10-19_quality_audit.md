# 2026-10-19 第一轮调研审计（历史快照）

此页的281条/221待核是第一轮快照。最新状态见[第二轮审查](second_round_audit_2026-10-19.md)与[逐条台账](reading_ledger_2026-10-19.md)；补录已同步主目录和表格。

## 本次实际审计了哪些内容？

- 读取仓库 main 分支目录（初始 155 个路径）、README、研究地图、数据主目录、证据说明、指定论文解读、已有 UMM/书写专项、实验协议与目录生成/验证脚本。
- 主目录 data/literature.json 共有 281 项，270 条研究或论文、11 条资源。按照现存 verification 字段计数：
  - historical_record_not_rechecked **221** 条；
  - historical_record_unresolved **1** 条；
  - primary_abstract_read **37** 条；
  - primary_sections_read **21** 条；
  - primary_metadata_only **1** 条。
- 这些数字描述**档案状态**，不等于 21 篇已经按所要求的七字段+三遍流程读透，也不等于其他条目全不准确。不能把“正式编入文献表”和“完成逐篇原文验证”画等号。
- 本轮原始来源重点读到 VidScribe 全文相关节、Ketaba 论文/PDF/代码、VideoSketcher 代码和研究任务、Calligraphy Bench、BCSS、Wuji VAM 等模型卡与数据卡；其他拓展研究按来源级别标记。

## 任务分类：提交前必须先通过

| 任务类别 | 输入 → 输出 | 关键标准 | 正确的研究连接 |
| --- | --- | --- | --- |
| 视频中文字质量评测 | 文字/参考/原视频 + 生成视频 → 指标 | OCR、字形结构、跨帧稳定、编辑残留 | VidScribe、VTR-Bench |
| 静态文字图像生成 | 文字/位置/字体 → 一张文字图 | 字形、文字准确率、FID | TextDiffuser、GlyphControl、AnyText2 |
| 在线笔迹生成/恢复 | 字形/文本/风格 → 有序轨迹与笔状态 | 顺序、几何、抬笔/起笔、文本识别 | DiffInk、OLHWG；Inverse Painting属于RGB绘画过程复原，未输出笔尖轨迹 |
| 序列绘画视频 | 草图指令/几何计划 → 渐进绘制视频 | 顺序执行、内容覆盖、连续性 | VideoSketcher |
| 草图驱动视频动画 | **给定草图序列** + 文本 → 动画视频 | 运动与草图对齐 | VidSketch；不可同“从空白画出来”混用 |
| 中文书法 Agent 绘制 | 参考书法图 + 绘图工具 → 笔画命令/画布 | 笔画召回、顺序、最终画面 | Calligraphy Bench |
| 手写 OCR/HTR | 静态行图 → 文本 | CER、WER | Ketaba、Qari、CASIA-HWDB2-line |
| 笔画实例分割 | 单字图像 → 多个笔画 mask | IoU、实例匹配等需核原文 | BCSS |
| 机器人示教书写 | 人类参考视频+机器人状态 → 动作与多视角预测 | 动作误差、回放视频误差 | Wuji Writing VAM |
| 确定性字形工具 | 字符+SVG/规范 → 逐笔动画 | 规则匹配、覆盖、地区标准 | AnimCJK、Hanzi Writer、KanjiVG |

**典型失误：**将“stroke weight”“glyph stroke correctness”“stroke sequence”“robot action trajectory”“diffusion steps”归为同一种笔顺指标。这五项物理/统计对象不同。VidScribe 的 A2 评价轮廓拓扑，Calligraphy Bench 才有明确称为 stroke order 的评价，但任务依赖绘图工具且为视觉裁判的匹配笔比例；后者也不能代替生成视频的严格全事件准确率。

## 影响新颖性的直接前作（补充关联已纠正）

Calligraphy Bench在第一轮之前已存在主目录L044；首轮X2026-006是同一资源的再核查，不能计为新发现。第二轮已加入明确关联。

**Calligraphy Bench（Haize Labs，2026）**已在 88 个汉字书法样本上要求智能体通过 tldraw 绘制笔画，并报告逐笔顺序、笔画召回、最终外观。这说明“已有研究完全没有针对中文书法的笔顺生成评测”过宽。该工作没有完整原生 RGB 视频生成比较，也未见公开严格事件序列标注和人工逐事件验证协议。其“stroke order 82%”不能移植为视频模型严格整字笔顺率。资料：[HF dataset](https://huggingface.co/datasets/haizelabs/calligraphy-bench)、[GitHub](https://github.com/haizelabs/calligraphy)。

**BCSS（Brush Calligraphy Stroke Segmentation）**已有单图对应多个笔画 mask 的数据；证明从静态墨迹中提取笔画实例已有前作。但单张图实例 mask 无法唯一确定实际书写顺序。原完整集合与 HF 可直接加载 subset 数量不同，见[资源笔记](../resources/nonpaper_research_2026-10-19.md)。

**Wuji Writing VAM**已发布 Wan2.2 视频 DiT 与动作预测联合权重，以人类第一视角写字参考、机器人观察图和 54-D 状态预测多视角视频及 54-D 动作，训练的字是 0–9 数字。它是非论文工业/研究模型卡，证明“视频+动作共同生成”已有人直接做书写相关研究。没有证据其支持中文书法规范笔画评测。来源：[官方模型卡](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819)。

## 检索审计规则（防遗漏）

1. **同义语串**：Chinese handwriting, stroke-order, brush writing, calligraphy, stroke mask, raster-to-vector, online/offline HTR；drawing process, sequential sketch, painting time-lapse, inverse painting；text in video, video scene text, video text editing；UMM, native unified image-video generation, flow matching, action-conditioned video；Arabic script, kanji stroke data, CJK SVG。
2. **多源并行**：正式会议/期刊索引（CVF、NeurIPS/ICLR、ACL、Springer、IEEE、IJCAI）、arXiv 原文、作者 GitHub、HF 模型卡/数据卡/adapter_config、作者实验日志及实例。
3. **追引**：阅读 Introduction 的“为什么”、Related Work 分类与边界、失败案例、消融表、附录协议、代码配置，逐项写对应失效假设。
4. **去重**：以 arXiv base ID / DOI / 论文正式题名合并论文；权重/adapter/数据子集按独立制品另立资源卡，明确“同一研究的发布物”，避免重复计算为新论文。
5. **可复核性**：每条包含来源链接、核查日期、已读范围、核实数值的表号、未见证据；项目与仓库保持版本，外部 live 页面不意味着本次运行成功。
6. **状态升级**：metadata → abstract → method+experiments+appendix → code audit → reproduction；不得在未运行时打 reproduction 标签；未见字段写“待核”，不得自动补全。

## CCF-A / SCI 一区与经典理论的检索地位

- TextDiffuser、GlyphControl 的 [NeurIPS 2023](https://papers.neurips.cc/) 正式出版页面直接确认会议主会；适合学习问题定义、条件设计与指标，但均为**静态图像生成**。
- UMM 的 Transfusion / Chameleon / Janus / BAGEL / Show-o2 等以正式来源及版本逐项审阅架构；“模型统一”必须分别明确共享 token、主干、目标和输入输出。
- 经典 diffusion、latent diffusion、flow matching、LoRA / DoRA、矢量 SVG 渲染属于方法工具箱，不因移植汉字视频自然构成新颖性。
- **会议/期刊档次不构成技术内容的代替证据。** 期刊分区随年份/学科体系变化，未查官方索引不得武断标注 SCI 一区；WACV 2027 尚属未来会议，当前仅记录作者宣布接收。

## 仍没有完成的工作

- 尚未逐篇重新打开 281 条旧文献的所有原文、全部附录与每个代码仓库，也无法证明“世界全部相关论文零遗漏”。保留 221 条历史未复核和 1 条 unresolved 的明确状态。
- 未在本次执行生成模型/笔顺/机器人动作推理、训练或计算成本测试；所有分数都是作者声称或旧档案记载。
- 项目自有跨模型汉字严格笔顺真实样本成绩仍空缺。
- data/research_additions_2026-10-19.json 是**本轮来源可追溯增量目录**；旧主目录及其生成视图未在本轮重新导出。正式统计时两个目录需去重并显式区分，不能把增量数量伪装成旧主目录已同步。

研究方向只有在明确比较对象、分布、观测量、对照和可证伪假设以后才进入选题列表，详见[实验设计](../experiments/research_gaps_and_tests_2026-10-19.md)。
