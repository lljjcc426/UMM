# 无独立论文项目、模型卡与数据集：2026-10-19 核查补录

**发现规则**：arXiv/会议之外，同时查 Hugging Face Models/Datasets/Spaces、GitHub、原作者网页、训练 YAML、权重 adapter_config、评测提交和数据许可。记录单元为“实际发布的资源/版本”，即使该资源后来被论文引用，也要保存独立资源卡；切忌以 README 营销性表述替代测量。

| 资源 | 证据入口 | 实际输入→输出 | 与书写视频的关系 | 本次阅读层级 |
| --- | --- | --- | --- | --- |
| AnimCJK | [GitHub README](https://github.com/parsimonhi/animCJK) | Unicode CJK 字→语言/地区版本的 SVG 逐笔动画 | 规范化/方言对照及确定性渲染基线；没有学习型视频生成器 | 官方 README / SVG 示例 |
| KanjiVG | [GitHub README](https://github.com/KanjiVG/kanjivg)、[规范](https://kanjivg.tagaini.net/) | 日本汉字 SVG 路径、结构属性 | 日本标准约定下顺序/组件参考；跨语种必须核对顺序差异 | 官方 README |
| Qari-OCR-LoRA | [GitHub](https://github.com/HasanBGit/QARI-OCR-LoRA)、[HF](https://huggingface.co/HassanB4/Qari-OCR-LoRA) | 阿拉伯语手稿图→转录文本 | 低参数、多模型基座对照，**未提供视频生成** | 官方 README/示例 |
| CASIA-HWDB2-line 的 HF 衍生版 | [HF 数据集](https://huggingface.co/datasets/Teklia/CASIA-HWDB2-line) | 离线汉字手写**行图像＋文本** | 静态 OCR/数据增强；公开衍生字段不能直接当在线笔尖序列 | HF 目录和卡片级 |
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
