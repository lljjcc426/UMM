# 文献检索记录

日期：2026-10-15。按检索方向归档，非搜索引擎结果穷尽清单。原论文相关部分阅读不等于代码运行。

| 检索链 | 代表查询/种子 | 获得的原始来源 | 核查范围 |
|---|---|---|---|
| UMM基础 | Chameleon / Janus / Transfusion / Show-o / UniDisc | arXiv原始摘要 | 补全U01—U07，摘要层级 |
| 交错推理 | Zebra-CoT / ThinkMorph / Monet / Omni-R1 / WEAVE | arXiv原始摘要 | U08—U12，避免泛称所有工作是视频模型 |
| 协同与评价 | GapEval / RealUnify / UniG2U / VGUBench / UEval | arXiv原始页 | U13—U16、U22 |
| 原生协同 | Uncovering Understanding–Generation Synergy / Transferability | arXiv及标题检索 | 前者来源重新定位成功；后者本轮正文失败，U18保留待核 |
| 书法统一 | Chinese calligraphy unified recognition generation | [UniCalli](https://arxiv.org/html/2510.13745v2) | 方法/实验/限制；大PDF访问失败，未虚称看过PDF图 |
| 在线—离线桥接 | differentiable physical rendering handwriting | [OnOff](https://arxiv.org/html/2608.03198v1) | 方法、简化物理和渲染PDF相关页 |
| 双模态字形 | dual modality Chinese calligraphy | [DeepCalliFont](https://arxiv.org/html/2312.10314v1) | 核查图像—轨迹与书体区别 |
| 视频文字系统评价 | handwriting stroke / text rendering video benchmark | [VidScribe](https://arxiv.org/html/2609.36598v2)、[VTR](https://arxiv.org/html/2610.01499v1) | 方法/因素/结果口径，不能当笔顺排名 |
| 视频逐笔能力 | stroke-by-stroke video reasoning | [Video models zero-shot](https://arxiv.org/html/2509.20328v2) | Fig.30局部任务，限制外推 |
| 结构和运动先验 | hierarchical offline-to-online Chinese trajectory | [双域HTR](https://link.springer.com/article/10.1007/s44443-026-01050-5) | 原文结构/顺序/向量/运动先验 |
| 动态文字机制 | Text-Animator / Video Text Preservation | [2024](https://arxiv.org/html/2406.17777v1)、[2025](https://arxiv.org/abs/2511.05573) | 前者方法概览，后者摘要级 |
| 局部书法/个性化 | CalliPaint / CalliffusionV2 | [CalliPaint](https://arxiv.org/abs/2312.01536)、[V2](https://arxiv.org/abs/2410.03787) | 摘要级跟踪，不捏造时序指标 |
| 真实过程数据 | OpenHandWrite / stroke-level Chinese database | [出版方原文](https://link.springer.com/article/10.3758/s13428-026-03001-4) | 采集与用途，不下载数据，不推定许可 |
| 规范 | 通用规范汉字笔顺规范 / 8105 / 教育部 | [官方PDF](https://www.moe.gov.cn/jyb_sjzl/ziliao/A19/202103/W020210318300204215237.pdf) | 官方搜索索引可见，直接PDF失败；不编造规范编号/页码 |
| 无墨迹过程识别 | The Unwritten Benchmark | [原始摘要](https://arxiv.org/abs/2608.14558)、[作者发表页](https://nilayyilmaz.dev/publications/) | 作为邻近评测，不用异常索引日期推定首发 |
| 出版信息更新 | LVGM WACV | CVF WACV2026 PDF索引 | 新版元数据线索，PDF未完整读取 |
| 进一步待查 | G-HTR、Benchmarking High-Fidelity Video Scene Text Editing、Reels-RSI | 参考文献及摘要线索 | 未纳入已完成核心表，不借相邻论文代替原文 |

## 访问失败的含义

部分PDF及出版页面未能获取；相关条目仅采用已取得的摘要、元数据或HTML证据，并保留待核状态。

## 2026-10-19 增量检索与原始资料交叉核对

| 搜索渠道 | 命中并核查的原始资料 | 来源等级与待补部分 |
| --- | --- | --- |
| arXiv 正文 | VidScribe 2609.36598，VidSketch 2502.01101 | 前者正文§3/4及结果；后者方法与部分实验待补主表 |
| ACL Anthology + GitHub + HF | Ketaba NakbaNLP 2026、官方 train.yaml / inference.py、HassanB4 adapter | 论文/代码核对完成，adapter 默认路径与官方名存在差异，未本地推理 |
| GitHub 论文官方资源 | VideoSketcher、Haize Calligraphy Bench、BCSS、SceneDAPR、MoSketch、SketchEdit | VideoSketcher 仓库配置可核，完整定量主表待核；Calligraphy Bench judge 实现细节不详 |
| Hugging Face 无论文发布物 | Wuji Writing VAM、Qari-OCR-LoRA、BCSS 数据子集、CASIA-HWDB2-line | 主要模型卡/数据卡，未取权重和受限数据；写字数字与汉字分布区别 |
| CJK 工程与文图控制 | AnimCJK、KanjiVG、TextDiffuser、GlyphControl | 前两个工程README，后两个 NeurIPS2023 官方摘要；SVG区域规范和静态/动态分别记录 |
| 历史目录精度审计 | 281 项 main 主目录 verification 状态 | 221 历史未重新核、1 未解决、37 摘要、21 章节、1 元数据；统计方式见新质量审计 |

详见 [增量研究矩阵](scoped_literature_matrix_2026-10-19.md)、[新资料原始来源登记](../../data/research_additions_2026-10-19.json) 和 [精读队列](survey_queue_2026-10-19.md)。候选数量不能作为已阅读全文数量；无独立实验复现成果。


## 2026-10-19 第二轮

- 对281主目录+16补录的首选来源，以及32条基础文献分别访问，329条事件明细见[访问记录](../../data/source_access_audit_2026-10-19.json)。同一工作可产生多条事件；原文候选与落地页分开。
- 扩展路径：DDPM→score-SDE→LDM/DiT→FM/RF/Consistency/数值求解；Video Diffusion→AnimateDiff/CogVideoX/Wan→Diffusion Forcing/Self Forcing；sketch-rnn→神经绘画/CLIPasso/StrokeFusion；LoRA→QLoRA/DoRA/rsLoRA；FVD/VBench→书写事件校准。
- 直接纠错：Calligraphy Bench与L044重复关联；U18已重新定位原文；DP-Font PSNR及CFG多指标冲突；VideoSketcher分类与顺序偏好分开；UMM联合与单任务结果存在权衡。
- 当前阅读范围与未完成量见[第二轮审查](second_round_audit_2026-10-19.md)，不能将本检索日志当成全部三遍精读完成证明。

## 2026-10-19至20：继续复核存量与前后向追引

- 23项存量研究的原文相关章节已复核：[批次ID与范围](../../data/continued_review_batch_2026-10-19.json)。重点是静态轨迹恢复、矢量动作、交互绘画、数字/物理媒介、视频控制、缓存/蒸馏、离散flow与拓扑约束。
- 官方CVF/PMLR/NeurIPS及作者页核对SketchAgent、StrokeNUWA、VACE、TeaCache、clDice、FRIDA/CoFRIDA发表信息；L001来源版本核为v1，未附会正式会议。
- 通过CoFRIDA官方项目追引HF原始README和文件清单，发现基础模型标识冲突，资源H001单列关联F04。
- 继续发现Edit Flows、Discrete Guidance Matching、Disney2026线稿矢量化、Windfoil，保留为待读候选，未计作已经精读的独立论文。
- DiffVG两个官方PDF入口直接下载未完成；官方项目页/勘误可读，原有F01仍待正文复核。本次未靠访问状态填充全文技术字段。
