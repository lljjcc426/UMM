# MANZANO与GenEval：统一表示、任务协同和测量口径

第九十七批完成已有[L064 MANZANO](../reviews/L064.md)、[L071 GenEval](../reviews/L071.md)指定范围的核心三遍和五项书面检查。[版本与发布审查](../../data/manzano_geneval_measurement_and_release_audit_2026-10-21.json)保留原文、实际图表、代码commit和待解释差异。目录仍356条（329论文／研究、27资源），195项核心、198项五条书面含未通过项，161条尚未确认核心（含资源）。无文件删除、模型运行或独立复现。

## 版本和真实任务

[MANZANO所读2509.16197v1](https://arxiv.org/html/2509.16197v1)核心§1–6、实际F3–6和T1–3均已核读。[Apple官方研究页](https://machinelearning.apple.com/research/manzano)及[OpenReview](https://openreview.net/forum?id=FIXPFUeO9Z)确认ICLR2026书目，正式PDF403未取得。没有把v1问题直接归给未读正式修订稿。它统一静态图理解和生成：共享语义encoder、连续/离散adapter、AR语言模型及外部flow像素decoder；不包含规范汉字笔顺视频实验。

[GenEval所读2310.11513v1](https://arxiv.org/pdf/2310.11513v1)为完整21页，核心§1–7及指定AppA/C/D，实际框架p2、人评p6、结果p8、消融p14及人评UI p21均核读。[正式NeurIPS2023条目](https://papers.neurips.cc/paper_files/paper/2023/hash/a3bf71c7c63f0c3bcb7ff67c67b1e7b1-Abstract-Datasets_and_Benchmarks.html)另核身份；正式PDF未完整取得，不充当全文证据。它测静态图的对象组合对齐，无生成器和时序评价。

## MANZANO机制和条件

ViT 42×42×1024经3×3STC变14×14×9216，连续MLP给理解；离散FSQ为64K语义ID给AR图像生成。tokenizer阶段挂300M小LLM，以文字NTP随机训练两路且全参数解冻；之后弃小LLM，主LLM阶段冻结encoder/离散adapter。连续adapter未在相同冻结声明内。主LLM图像/文本CE权重.5/1，像素细节由独立Flow DiT-Air恢复，编辑再把参考图送decoder。

统一PT大多数1.6Ttokens、30B仅.8T；CPT83B。理解与生成均使用大量私有/授权及合成数据，完整去污染与精确训练配置未披露。像素decoder .9/1.75/3.52B，256²400k、512/1024/2048各100ksteps。LLM参数标签不能当全部系统参数，AR语义序列和flow decoder也不能合成“一步”。

| 证据 | 原值及边界 |
| --- | --- |
| T1 hybrid对discrete | 理解64.9/66.5/73.3高于63.3/62.2/62.3；GE77/WISE35持平，DPG79.9低于80.9 |
| T1 dual | 128² MagViT2 f8/256tokens，另分支256²；有分辨率混杂，非纯encoder分工消融 |
| F5 300M unified减specialist | 理解+.4/−2.3/−1.5；生成GE+2/DPG+.2/WISE−1 |
| F5 3B unified减specialist | 理解−.8/−.3/−.8；生成GE0/DPG−1.6/WISE0 |
| F5预算 | 匹配单任务token曝光，减专家steps；未配平总FLOPs/总steps |
| T2 30B | SEED76/RW70.1/MMB83.4/AI2D86均低于BAGEL对应78.5/72.8/85/89.2，正文“consistently”需限缩 |
| F6 decoder | 结构人评约+9.9，GE/DPG近持平，最大decoder美学下降；800prompt×3内部标注者，CI/一致性和映射不足 |
| T3 scale | ColorAttr3B.71→30B.65，不能称全部随规模上升 |
| 编辑 | 参考图同时给LLM和decoder，仅定性例；没有独立去旁路量化实验 |

这些结果可支持统一表示下的近似专家表现和某些指标扩展趋势；正协同需要逐任务基线及预算控制。将v1的强修辞逐项收窄，不把单图排行榜推到规范书写。

## GenEval的实际配置与效度

六任务553唯一prompt，分布80/99/80/94/100/100，每提示四图全部计入。Mask2Former/Swin-S在COCO80类别上检测/分割，实例crop并把背景置灰，CLIP ViT-L/14以三种文本模板的平均特征做颜色分类。默认置信.3、计数.9，位置按bbox中心/尺度margin.1。

实际自动颜色为十种，AppC1排除gray；主文十一基本色理论来源和p21人评界面十一选项（包括gray）属于不同口径。本次修正旧笔记不能将十一直接作为实际自动classifier配置。非计数默认至少达到请求数量，计数用exclude n+1实现精确计数。

人工研究1200图、6000标注（5/图）；83%是评估器对人工判断一致，非生成成功率。8605是所有标注者一致的分项子集，非8605张图。模型结果IFXL六项.97/.74/.66/.81/.13/.35/宏均.61；SDXL宏均.55，位置/绑定仍弱。

| 原文证据 | 核查 |
| --- | --- |
| F3/T5 H14比较 | GenEval总一致.834、互评.878、H14CLIP.798；twoobject .799低于H14 .828，正文“四个复杂任务更好”不覆盖该项 |
| 计数 | .823−.734=.089，即8.9百分点；正文称22点与所选H14图表不一致，待解释 |
| 位置 | .823−.682=.141，即14.1百分点；不可与计数互换 |
| T4 crop/mask | κ无两者.32/绑定.01，仅crop.37/.33，仅mask.43/.47，组合.45/.49；人互评.55/.65 |
| 阈值 | 计数.3→.9，κ.37→.65；五折agreement.823±.013，未声明95%CI |
| 错误例 | 重叠物体合并、mask孔洞混色、艺术图OOD，均为作者讨论；字体/轨迹超出任务 |

## 固定发布代码和跨论文聚合核对

[GenEval固定af4902f](https://github.com/djghosh13/geneval/tree/af4902f24d3ca90ebbb446dd9891a59e0f82725f)完整18blob树，读README/MITLICENSE、评测/汇总/提示生成程序和553行metadata；没有运行检测/生成，未下载权重和原图。

1. evaluate_images.py按置信排序选请求数量的最高分对象，不搜索更低分的可能匹配；默认每类最多16个、max_overlap1不做实际NMS。位置函数还用归一方向阈.5，须与纸面轴向公式区别记录；AppC3 above第二组不等号与前组和代码方向不一致，疑排版问题，未代改正式版。
2. summary_scores.py同时输出全图微均、至少一张成功的prompt率及六任务Overall宏均；三者不能混报。代码只汇总读到图像，不保证每任务/每提示四图齐备，必须报告样本完整性和各子项。
3. create_prompts.py默认seed43，去重后metadata553行；只解析数据，不把提示生成或静态代码审查当模型实验。

按GenEval §3.2及官方汇总代码，Overall是六任务均分。MANZANO v1 T3 3B给出.98/.91/.82/.71/.78/.71，其算术均值.818333…，却报Overall.85；仅两位小数舍入不足解释。原表值全部保留，不直接以本次算术取代作者结果；需作者逐图结果、准确prompt/rewrite、commit和聚合协议。30B六项均分.85与其Overall一致。这是条件性的表内聚合疑点，未运行任何生成评测。

## 可证伪假设、实验与写作学习

假设一：在语义覆盖充分时，连续理解/离散生成降低量化对理解的损失；固定encoder、数据、分辨率、token率，做两套等总FLOPs/等任务曝光对照，逐项分析负迁移。参考旁路与decoder容量做独立消融，报告全系统成本、各任务多seed与区间。

假设二：实例评价在已校准COCO对象组合上比整体相似度更敏感；用未见生成器、素描/艺术/字体分层做独立盲人评，先冻阈值，再报评估TP/FP/FN、κ及不确定性。对比人工框/真mask与预测框，区分测量错误和生成错误，留组合holdout防基准调优。

书写研究需要另加未见字、多语字体、字形OCR/人审、同终态异笔画事件、落抬笔/接触和RGB时间证据。语义AR或GenEval宏均均不直接验证这些能力。以上均为未执行设计。

写作学习：MANZANO按tokenizer/LLM/decoder展开Method，以专家消融和两尺度扩展支撑Claim；应保留退步、异数据和预算边界。GenEval先验证测量工具、再评生成器，Limitations给具体误测例，研究流程值得采用。阅读时逐图表核数，不能只抄Abstract或表旁结论；核心阅读完成不等于确认作者全部结论。
