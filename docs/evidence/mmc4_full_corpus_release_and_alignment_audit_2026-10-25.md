# MMC4：全附录、图句分配与恢复版本审查

第二百零五批完成[L170](../reviews/L170.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/mmc4_full_corpus_release_and_alignment_audit_2026-10-25.json)。358目录（331论文／研究、27资源），310核心/315书面含未通过项；待完成核心深审21篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2304.06939v3)、[主源2](https://arxiv.org/html/2304.06939v3)、[主源3](https://arxiv.org/pdf/2304.06939v3)、[主源4](https://github.com/allenai/mmc4/tree/5304ddd7a608c88d8f4ee1a6b3a4356104215517)、[主源5](https://github.com/allenai/mmc4/blob/5304ddd7a608c88d8f4ee1a6b3a4356104215517/README.md)、[主源6](https://github.com/allenai/mmc4/blob/5304ddd7a608c88d8f4ee1a6b3a4356104215517/scripts/compute_assignments.py)、[主源7](https://huggingface.co/datasets/jmhessel/mmc4-ff/tree/14f546ce6ed4c627eaf314b6c6cba59d726bebe6)、[主源8](https://huggingface.co/datasets/jmhessel/mmc4-core-ff/tree/26e19bbe7abb37f695ad7dc12924bf6a6d498fe5)。

## 研究问题

公开构建大规模多图文档，使视觉语言模型可利用交错上下文做少样本图像描述；同时检验图句匹配、过滤及质量。本文下游实测为COCO描述，VQA为相关背景，不能混作本实验结果。

## 现有不足

单图caption缺跨图上下文；Flamingo类训练数据不可获得。C4虽有文字和网页来源，已丢完整DOM位置，不能直接恢复原网页图文排列。

## 贡献

从C4网页下载图片、过滤并用CLIP匹配图片与句子，形成MMC4及core/fewer-faces变体；以OpenFlamingo早期训练验证上下文学习价值。

## 输入、模块、输出与公式

C4文字/原页面图片URL→交错图文文档；用于图输入的文字生成/问答，不是直接生成图片或视频。

## 模型结构

C4已去DOM，回溯CommonCrawl页面提取图片URL；CLIP ViT-L/14对页内全部图句余弦匹配，linear assignment最大总相似度、至多一图一句，图多于句的未分配图回退各自argmax。固定公开compute_assignments/linear_assignment源码一致，负相似度最小化+dummy padding；不运行求解器或模型。匹配句前后随机放图属于下游序列构造，不能恢复网页原位置。OpenFlamingo3B用OPT1.3B+CLIP和跨注意力生成文字，不生成图像/视频。无新编号公式/算法。

## 数据分布与划分

T1完整MMC4 571M图/101.2M文档/43Btoken，ff375M/77.7M/33B，core29.9M/7.3M/2.4B，coreff22.4M/5.5M/1.8B；这些图条目并未证明全局唯一。C4源CC2019-18，图片2022中后期下载；初1.37B图/115M文档。页内pHash阈值5，抽60K常见图频次>10过滤；NSFWCLIP4层MLP p>.1去约10%，不保证零有害内容。ff分类器由60K RetinaFace伪标签训练80/20，95%召回是对检测器标签；保留约65%，人工912图仍23有脸(2.5%)、6可辨识。core4–40句/2–15图，pHash10，至少75%匹配CLIP>25(×100)。域名6M文本/4.9M图，前10%域占77%文档/89%图，集中明显。

## 指标与评价协议

T2文档内多图检索AUC/p@1，MSCOCO、Story-DII/SIS/DIIStress、RecipeQA/DIY；T3人工200文档836图的主题/匹配句相关性、脸/水印/标志/广告/重复比例；F7 COCO CIDEr 4/8shot。无新VQA成绩、动作顺序/跨图因果或图像生成评价。人工836图具有页内相关，不当836独立文档；无标注一致性/置信区间。

## 对比方法

T2 CLIP对Faghri、Li、MulSupTrans等文档检索算法，不是MMC4训练模型对全部VLM。F7 caption-only LAION5M/10M/15M与对应增加core2.5M/5M/7.5M序列；序列额外图/token曝光，不是同曝光的交错结构单因子。

## 实验条件和发布边界

下载png/jpg/jpeg，URL排logo/button/icon/plugin/widget，最大边800/最小边150，aspect .5–2；图句CLIP≥.15。下游早期corev1，公开v1.1有bugfix；256token连续子序列、≤5图、CLIP20过滤、丢无图并随机丢单图，固定4/8shot评COCO。本文未给完整学习率/GPU/优化器/精确训练步，不能从通用OpenFlamingo配方补成已核实验。静态代码/README固定5304ddd7a608c88d8f4ee1a6b3a4356104215517(2025-03-19)，HF元数据公开无gate；不下载语料/权重或运行模型。

## 主结果

T3主题相关87.7%/句相关80.4%，脸28.3/水印1.6/标志3.9/广告3.2/重复.7%。3700样本未发现NSFW不是全库零风险。T2 CLIP各AUC/p@1：COCO99.4/95.7、DII92.8/93.9、SIS79.1/73.3、DIIStress98.7/93、RQA80.7/70.7、DIY74/57.6；COCO p@1低于Li97.6，不能说全指标最优。F7混入序列普遍提高COCO，正文概括20–30CIDEr；实际8shot有差距超过30的柱，柱无精确数标，保留视觉趋势/近似范围，不造逐柱精确值。作者结论主动追问是否学会跨图推理还是分别描述的上下文学习。

## 消融及进一步实验

F4 linear assignment平均相似24低于简单max24.5，但不同句覆盖34%高于22%，说明覆盖与局部最大相似权衡。F5图轴统计图数mean5.7/median2、句数mean24.3/median13，正文却把计数类别/meanmedian错写；印出的Spearman rho10.3超[-1,1]，可能省略尺度但无依据直接补成.103。F6/附录T4以22K文档LDA30类、GPT4据top20词命名，最大Personal7.96%，属于文本主题概览，非人口/所有语料无偏检验。F8/9及T7/8定性文档和context-dependent广告判定全核，不能据图句相关宣称真实事件顺序。

## 局限与疑问

17页全研究内容与8图8表完成。C4丢DOM、CLIP重排、随机句前后不能作笔顺/事件时序监督；英语网页、集中域、识别器伪标签与去重残差，亦未独立证明跨图推理。发布README说明原AI2副本2025-02误删，当前仅恢复ff/coreff，完整MMC4/core和图像CLIPfeatures仍缺；HFff有5zip、coreff1zip可见，未实际下载验证其内容。14个长期缺shard已在原论文统计/实验排除，不与2025事故混作新增缺失；could_have_url_duplicate约3%，严格去重需另按flag处理。原始图仅URL需重下，失效和内容变更会改变实际可用集。MIT代码与DATA_LICENSE ODC-BY数据库/新增对齐权利分开，不能覆盖各原始网页/图版权；AppA外链DATASET_CARD.md在当前树缺失。

## 预期优势条件

公开多图文字上下文能改善以示例条件化的描述；若要证明结构带来的跨图推理收益，必须控制图文/token曝光并让答案依赖多图关系。按CLIP语义构造的交错资料可以支持场景主题组织，无法单独提供实际绘画时序。

## 可证伪实验

同一图/文/token和训练步，caption-only、CLIP匹配、可恢复DOM顺序、随机图句/随机页顺序、人工真实步骤对照；设计单图不可解的跨图关系题与互换图干预，分测相关匹配、事实依赖、动作顺序及少样本描述。另记录版本/成功重下比例、长期缺shard/可能URL重复flag分母，完整与ff版本分开。以上仅实验设计，未执行。

## 论文组织与Claim学习

数据流水线+人工质量+早期下游实验构成明确证据链；结论主动保留跨图推理疑问可借鉴。规模/可用性/唯一性/时序保真分写，表中基线不能概括全项最优，图轴统计与正文均值/中位数及rho尺度需一致；2025恢复状态必须在资源表同步。

## 实际阅读范围

v3正式17页§1–6与AppA–D全部研究内容；实际F1/2/4/5/6/7/8/9共8图(无F3)、T1–8全部含30topic/两套各50域名及文档示例，17页contact全看并放大F5/F7及示例页；无新编号公式/算法。37条references清单/关键引文，不宣称37原文全部读。固定repoREADME、两个assignment脚本全文、DATA_LICENSE重点条款/CODE_LICENSE、当前tree与两HF版本元数据/ff卡；AppA独立外链卡缺失，未全依赖/训练code审计，未运行模型/下载数据。核心三遍与五书面完成。

## 论文规模与当前获取

Table1完整版本571M图/101.2M文档为论文版本统计。固定公开README报告原AI2副本2025年2月被误删，目前仅ff与coreff恢复到HF，full/core与CLIP图像features仍缺。两HF元数据可见5与1个zip，此处未下载验证内容。图片仍经外部URL重下；14个长期缺shard已从原统计/实验排除，和后续误删不同。

## 图表及主张边界

F5图轴为每页图数mean5.7/median2、句数mean24.3/median13，正文写法不一致；rho10.3也未标量表。F7仅少样本COCO描述且增加序列曝光；不能据此单独确认跨图推理。CLIP重新分配和随机句前后位置不恢复原网页/实际动作顺序。
