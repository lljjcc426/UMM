# 无独立论文项目、模型卡与数据集：2026-10-19 核查补录

**发现规则**：arXiv/会议之外，同时查 Hugging Face Models/Datasets/Spaces、GitHub、原作者网页、训练 YAML、权重 adapter_config、评测提交和数据许可。记录单元为“实际发布的资源/版本”，即使该资源后来被论文引用，也要保存独立资源卡；切忌以 README 营销性表述替代测量。

| 资源 | 证据入口 | 实际输入→输出 | 与书写视频的关系 | 本次阅读层级 |
| --- | --- | --- | --- | --- |
| AnimCJK | [GitHub README](https://github.com/parsimonhi/animCJK) | Unicode CJK 字→语言/地区版本的 SVG 逐笔动画 | 规范化/方言对照及确定性渲染基线；没有学习型视频生成器 | 官方 README / SVG 示例 |
| KanjiVG | [GitHub README](https://github.com/KanjiVG/kanjivg)、[规范](https://kanjivg.tagaini.net/) | 日本汉字 SVG 路径、结构属性 | 日本标准约定下顺序/组件参考；跨语种必须核对顺序差异 | README、SVG格式规范与中SVG已核，见S010 |
| Qari-OCR-LoRA | [GitHub](https://github.com/HasanBGit/QARI-OCR-LoRA)、[HF](https://huggingface.co/HassanB4/Qari-OCR-LoRA) | 阿拉伯语手稿图→转录文本 | 低参数、多模型基座对照，**未提供视频生成** | HF固定配置/训练信息与README已核，见S011 |
| CASIA-HWDB2-line 的 HF 衍生版 | [HF 数据集](https://huggingface.co/datasets/Teklia/CASIA-HWDB2-line) | 离线汉字手写**行图像＋文本** | 静态 OCR/数据增强；公开衍生字段不能直接当在线笔尖序列 | 固定revision的image/text字段与split已核，见S012 |
| Hanzi Writer | [官方文档](https://hanziwriter.org/docs.html) | 汉字及笔画形状→预设顺序动画/练习 | 制作无生成学习成本的强规则基线 | 继承主目录 R01 |
| Make Me a Hanzi | [原始仓库](https://github.com/skishore/makemeahanzi) | 字符→有序 stroke 轮廓、medians | 生成事件标注、可控 SVG 渲染；中心线不等于真实压力轨迹 | 继承主目录 R02 |
| Ketaba-OCR-LoRA | [HF 适配器](https://huggingface.co/HassanB4/Ketaba-OCR-LoRA)、[代码](https://github.com/HasanBGit/Ketaba-OCR-LoRA) | 阿拉伯语手稿行图→识别串 | 论文现已在 NakbaNLP 2026 发表；模型卡继续作为独立可执行制品核查 | 论文+代码实核，见 [精读](../handwriting/papers/ketaba_ocr_lora.md) |

## AnimCJK：为什么必须有这个工程基线？

README 明确区分 svgsZhHans（简体中国用字）、svgsZhHant（台湾繁体）、svgsJa、svgsKo 等 SVG 目录，并提供 clipPath + CSS 动画示例。所读 README 中简体目录约 8,244 个、繁体目录约 1,513 个、日文目录约 7,336 个字形（项目持续更新，复现时冻结版本）。**同一 Unicode 在语言/地区间可以具有不同笔顺、方向甚至笔画数**：作者举例马偏旁与草字头在不同目录的差异。

- 数据用途：将标准动画转为 event timeline；按语言/规范层设置可接受序列；合成合法、交换笔顺、反画方向、同时落墨反例。
- 不可推断：SVG 动画有顺序，不代表轨迹来自真人手写；不能用其中某地区写法判另一地区“错误”。
- 需要审计：每一 SVG 是否有可导出的中心线与落笔/抬笔标注、矢量曲线的生成时长；仓库及生成 SVG 的许可证分别确认。
- 建议实验：把同一字在 svgsZhHans/Ja/Hant 的可用序列当交叉规范条件，测模型在指明地区时能否按给定序列执行。

## KanjiVG：日本汉字形体与结构的对照

KanjiVG README 标注 CC BY-SA 3.0；SVG 含 stroke/radical/element 等自定义属性，方便事件实例与部件对应。它为日本字形与部件研究提供可控数据，但**它的默认字形和简体汉字并不自然等价**，需分别保存书写规范、字符变体及地区标签。高价值变量是偏旁结构和形态复杂度，用于设计 unseen-component / repeated-stroke 测试切分。

## Qari-OCR-LoRA：同团队的非主模型制品

- 实际基座 NAMAA-Space/Qari-OCR-v0.3-VL-2B-Instruct；Qwen2-VL-2B 路线，官方称约 2.2B 参数。
- LoRA/DoRA/RSLoRA 适配器；作者 README 称约 37.6M 可训练参数（1.67%）。
- 原始 README 报告 blind CER=0.2635、WER=0.5521；这是作者提交中的辅助实验模型。Ketaba 论文也提到此对照，因此不可泛称“从未出现在论文中”。
- 核对事项：实际适配器配置、训练 split、tokenizer、重现 CER 的数据规范化流程；本文未本地跑模型。对汉字笔顺只迁移比较 PEFT 技术，不能作为视频生成 baseline。

## HF 离线/在线字段错配：CASIA 衍生版是反例

HF 名称中 HWDB2-line 易使人误认资源“有时序笔划”。这个衍生页面公开的是行图/对应文字，无证据表明每条包含 ordered (x,y,pen_state) 轨迹；研究汉字笔顺应另查原始 **CASIA-OLHWDB 在线数据**与采集许可、设备和时间字段。离线数据可作为识别监督、字体分布或纹理素材，不能直接造出真实历史。不要把无法从最终图像唯一反推的顺序假设标成真值。

## 资源复现卡必填字段

资源名+作者、精确版本/commit+HF revision、链接、输入输出接口、底座和适配器依赖、公开权重与否、数据集/字段/许可、训练脚本和默认超参、作者指标及统计口径、环境/VRAM、已测试/未测试、已知命名差异、可迁移机制及负面结果；新资源先登记，再进入“论文/工程项目”分类。

## 检索漏项的技术原因及修复

只搜论文标题会漏掉 HF LoRA/adapter、数据子集、API-only 产品、CJK 字形引擎和伴随模型。建议同时查：
- Hugging Face：handwriting、OCR、stroke、trajectory、calligraphy、Arabic manuscript、LoRA、video text 等 model/dataset/space 标签。
- GitHub：stroke animation SVG、brush drawing sequence、text video edit、writing video diffusion、dataset card、workflow YAML。
- 跨语种：Chinese Hanzi、Japanese kanji、Korean Hanja、Arabic calligraphy、Latin cursive、Indic script、Omniglot symbols；分开按语言对应笔顺标准。
- 逆向参考：视频文字论文 Related Work、工具被引用的论文、论文 GitHub Issues 与 model card 的 base_model、数据卡 license/字段。
候选若只有名称或镜像，保留为“待确认真实来源”，不补虚构配置。只用该轮公开可访问信息，未下载受限数据或权重。

## 追加：高相关性的“正式论文之外”资料

### Calligraphy Bench｜直接影响汉字笔顺新颖性的基准

[Haize Labs 项目](https://github.com/haizelabs/calligraphy) 和 [Hugging Face 88 条测试样本](https://huggingface.co/datasets/haizelabs/calligraphy-bench) 展示了智能体用 tldraw stroke API 描绘参考书法，报告笔画召回、正确顺序、1–5 风格相似度及成对偏好分数。**它评估书法绘图动作，不能用其 77–82% order 分数表达整段 RGB 视频规范书写准确率。** HF Viewer 另显示 strokes_svg / medians 字段，待审计这些字段与评分器之间的信息通路。详情请看 [逐项研究笔记](../handwriting/papers/calligraphy_bench.md)。

### BCSS｜静态笔画 mask，与时序真值隔开

[BCSS 官方仓库](https://github.com/Rvosuke/BCSS) 与 [HF 衍生包](https://huggingface.co/datasets/Rvosuke/BCSS) 的来源关系已核对：作者 README 描述完整数据 **1,322 图、10,653 笔画**，但正式论文Table1分组数相加为14,766，差异未解决（训练/验证 1,022，外部测试 300）；HF 发布说明此处可加载的加工子集约 **1,212 图**，由 1,082 训练/验证和 130 外部测试图组成。两种规模必须带上各自版本，不要将 HF subset 误报为全文数据。HF实际是固定六类重叠mask，论文为十类；主要用于墨迹类别/重叠分割与视觉结构约束，单图 mask **不含真实笔尖的时间方向**。衍生数据许可证与源数据许可须分开核实。

### Wuji Writing VAM｜公开 video+action 联合写字权重

[Wuji Writing HF model card](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819) 清楚列明 Wan2.2-TI2V-5B 视频权重与 action_dit 动作流同时输出，输入人类头视角写字示范、机器人三视角图、54D proprio 与指令；输出短期三视角视频及 54D 动作。当前训练资源是**0–9 数字、487 teleop episodes、896 个人类参考视频 episodes**，发布 step-12500 训练日志只作当前快照。视频和动作的同步协同已有工程探索，仍缺中文字体规范/真实机器执行对照。详见 [单独模型卡](../handwriting/papers/wuji_vam_modelcard.md)。

### SceneDAPR 与 Quick, Draw!：真实素描过程先验

[SceneDAPR 官方仓库](https://github.com/DSAIL-SKKU/SceneDAPR) 报告场景素描与 stroke order、绘制时间等注释，数值为 1,399 场景画与 6,420 个物体级标注；可研究同一画面内多对象绘制顺序的事件边界，需要读取实际字段确认时间单位、实例归属和许可。Google [Quick Draw! Dataset](https://github.com/googlecreativelab/quickdraw-dataset) 提供用户画笔的时序矢量墨迹，尤其适合建构**在线轨迹基线与时序错误注入**，其物体类别绘制顺序不能直接当中文汉字规范。另有 [ark60/sketch-diffusion](https://github.com/ark60/sketch-diffusion) 个人 notebook 发布 8 层 transformer + 1000 步 DDPM/Quick Draw 子集生成序列素描及 GIF；需核 Notebook 的 train/test 分割、运行日志、FID/KID 数值，不能将 README 中示意输出当作已复现成绩。

### 额外的“看似相关、任务却不同”的工程与研究

- [VidSketch](https://github.com/CSfufu/VidSketch)：由用户**给定**不同时间的手绘草图和提示，生成场景动画。它处理“草图约束下场景动起来”，与“白纸上新增每一笔”训练标签不同。
- [MoSketch](https://github.com/jyliu-98/MoSketch)：静态多物体素描经实例/运动分解实现动画；所述 stroke assignment 是移动物体/线条控制，不证明汉字笔顺。
- [SketchEdit](https://github.com/CMACH508/SketchEdit)：自由手绘矢量 stroke 级的图像编辑；适合研究局部笔画身份与不误伤，尚不具备规范书写视频结果。
- [DiffStroke](https://github.com/CMACH508/DiffStroke)：稀疏草图引导的局部图像修改，与逐笔生成历史不同。
- [KAIST 课程 Sequential Sketch Stroke Generation](https://github.com/KAIST-Visual-AI-Group/Diffusion-Project-Drawing)：基于 Quick Draw 时序数据的公开教学任务和评价结构。适合作为实现学习材料，不可计为独立同行评审新方法。

上述各项均需进一步固定仓库版本、数据许可与实际训练协议。是否配套有正式论文请检查仓库指向并按 DOI/arXiv 合并研究，避免将模型卡、课程代码和同论文训练附件重复统计为多篇成果。

## 2026-10-20实际配置与源码追加

本页保留首轮发现过程；当前结论以[资源实现审查](../evidence/resource_implementation_review_2026-10-20.md)及[S007](../reviews/S007.md)/[S008](../reviews/S008.md)/[S009](../reviews/S009.md)/[S010](../reviews/S010.md)/[S011](../reviews/S011.md)/[S012](../reviews/S012.md)/[S013](../reviews/S013.md)/[S014](../reviews/S014.md)/[S015](../reviews/S015.md)/[S016](../reviews/S016.md)为准。已读取实际HF配置/字段、选定源码和保存输出；Qari多指标得失、VidSketch训练目标、sketch-diffusion编码/反向公式及测试索引复用均明确记录。资源关联论文不重复计数；本轮补独立Stroke-Seg论文[L184](../reviews/L184.md)。
