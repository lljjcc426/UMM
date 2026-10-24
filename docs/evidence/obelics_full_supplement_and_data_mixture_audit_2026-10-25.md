# OBELICS：完整补充、数据混合与评测协议审查

第二百零六批完成[L171](../reviews/L171.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/obelics_full_supplement_and_data_mixture_audit_2026-10-25.json)。358目录（331论文／研究、27资源），311核心/316书面含未通过项；待完成核心深审20篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://proceedings.neurips.cc/paper_files/paper/2023/hash/e2cfb719f58585f779d0a4f9f07bd618-Abstract.html)、[主源2](https://proceedings.neurips.cc/paper_files/paper/2023/file/e2cfb719f58585f779d0a4f9f07bd618-Paper-Datasets_and_Benchmarks.pdf)、[主源3](https://proceedings.neurips.cc/paper_files/paper/2023/file/e2cfb719f58585f779d0a4f9f07bd618-Supplemental-Datasets_and_Benchmarks.pdf)、[主源4](https://arxiv.org/pdf/2306.16527v2)、[主源5](https://github.com/huggingface/OBELICS/tree/c50923f346abda02aa35fb48872266ac5dc8d896)、[主源6](https://huggingface.co/datasets/HuggingFaceM4/OBELICS/blob/08b7dca61ec09bacd68234ba6c388209b126d31c/README.md)、[主源7](https://github.com/huggingface/OBELICS/blob/c50923f346abda02aa35fb48872266ac5dc8d896/obelics/configs/config_filter_web_documents.yaml)。

## 研究问题

如何保留网页原生多图文字结构，开放构建可训练大规模视觉语言上下文学习模型的数据？

## 现有不足

单图caption缺自然跨图联系，MMC4依CLIP再分配图句；高规模网页仍有广告、重复和低质量内容。

## 贡献

DOM简化提取自然交错顺序，逐节点/段落/文档过滤与去重，开放OBELICS；IDEFICS验证与caption语料的互补。

## 输入、模块、输出与公式

网页HTML→英语交错文档；IDEFICS接图文上下文输出文字。图片为输入，论文没有由IDEFICS生成RGB图或视频。

## 模型结构

DOM清理/unwrap/去空嵌套，删除li/table/header及特定div/导航/日期，保留简化后文本图片节点顺序和换行；more-link替为EOS标记。保存的是经过删改的DOM遍历序，未模拟CSS/JS全部视觉渲染、更不等同动作时间。IDEFICS冻结LLaMA7B/65B+OpenCLIPViTH14 630M，6层/64latent/16head×96dim Perceiver126M，每4层加crossattention1.4B/13.9B；新增tokenembedding可训，9B/80B中trainable1.5B/14B。Q/K RMSNorm稳定训练；文字NTP+zloss=1e−3 log²Z，无新编号理论式/算法，无图像/视频输出。

## 数据分布与划分

25个CC2020-02至2023-01/02，41.2B候选，FastText去63.6%非英，MinHash16hash/5gram及LR质量>.5得1.1B；3.6B图URL下载55%约2B，筛至365M文档1.4B图，再去重最终141M文档/353M图出现/298M唯一(84.3%)/115Btokens。图URL频次>10去除而低频重复保留；同URL/同图集留最新，域内同段≥3次去15%文字。T1引用MMC4旧585M/103M与L170新版571M/101.2M分开。T5/6 LDA100K随机文档20/200topic，非人口分布。HF原版141047697、修正版opt_out_docs_removed_2023_07_12为134648855；原仅去退出图片却漏退出整篇文档，卡称约4.25%，元数据两计数差约4.54%，口径/版本未解释，不强行同值。

## 指标与评价协议

T2八任务：COCO/FlickrCIDEr、四种VQAaccuracy、VisDialNDCG、HatefulMemesROC-AUC；F11另IIIT5K rank-classification准确率。F6为aggregate4shot双横轴tokens/images，非统一原生准确率，也非直接GPU耗时。人工250文档的相关/脸/文字/残留等比例，各类别可重叠；90%为文档所有图相关，不与MMC4按836图的80.4%句相关直接比。KenLM Wikipedia100K文档perplexity只量类似Wikipedia程度，非事实正确性/普适质量。

## 对比方法

9B OBELICS-only/LAION-only/50:50-token混合，冻结同backbone且三组有效batch一致，图数/文本密度/域分布不同；DOM保留、长文、过滤和数据本身未被单因素分离。IDEFICS9/80B对Flamingo同规模/OpenFlamingov2 9B，底座、数据和算力并非同条件。作者56.5vs55.8 aggregate是每任务从不同shot挑最好，不代表固定32shot或单prompt全面领先。

## 实验条件和发布边界

T3段/文word4–1000/10–2000；字符重复.1/.1、词重复.1/.2、special.3/.275、stopword≥.3/.35、flagged≤.01、punctuation≥.001/.03、spam≤.12、common≥.8/.9、langscore≥.8、PPL≤1500；图150–20000px、aspect .5–2、jpg/png/webp，文档1–30图。公开过滤YAML同阈值但段级lang/PPL开关False、文档级True，模板不证明完整生产路径关闭这些步骤。T8 seq1024、200Kmax、AdamW正文/表Adam(.9,.999)、wd.1、clip1、warm2K、linearLR80B5e−5→3e−5/9B1e−5→6e−6，bf16ZeRO3；batch3.67M/1.31M tokens。主IDEFICS token混合OB73.85/Wiki6.15/LAION17.18/PMD2.82%，后两高质小集Wiki/PMD各repeat3。80B512A10080G、9B128约14天，三数据对照单源32卡/混合64卡约6天。IDEFICS80B及9B混合各恰3次loss-spike重启，回滚shuffle/可降LR。

## 主结果

T2 80B32shotCOCO116.6vsFlamingo113.8/Flickr81.1vs75.4/OKVQA57.8平/VizWiz50vs49.8；VQAv2 65.9<67.6、TextVQA36.7<37.9、Hateful52.5<70，VisDial未报；作者八任务四更好或平不能解释缺失为持平。9B32shotCOCO98vsOpenFlamingo99.5，Hateful49.8vs53.8；9B0shotCOCO46/Flickr27.3偏低，fewshot大改。人工250文档照片80%/图形29%/全部相关90%/字30%/结构文本5%/过滤遗漏7%/脸46%/水印3%/logo2%，零发现NSFW/明显PII不代表全库零，A3明确残留色情/暴力cluster并讨论偏差。

## 消融及进一步实验

F6交错长文按图量可约少一个数量级达到类似aggregate4shot，按tokens图并无十倍统一优势；混合总体强。F11逐任务VQAv2/OKVQA LAIONonly后期下降，caption-only部分caption较好，不能凭训练loss下降推出VQA提高。作者概括LAION在分类/OCR稍优，但F11 IIIT5K后期LAIONonly约.8而OBELICS约.95，不能称全程/所有OCR胜出；Hateful曲线波动大无多seedCI。A4.4零shot实为2个无图文字priming；prompt由5中间checkpoint的独立validation选；greedy+人工stopwords，LAIONonly VQA额外保首词，caption提示也不同。OCR/Hateful为候选rank；Hateful提示直接提供图上文字context，不是仅测视觉OCR。

## 局限与疑问

正式主20+supp31全部研究内容/11图11表和checklist完成，HF卡/README/两YAML静态核。保留DOM同时去li/table及日期会丢步骤列表/表格和部分时间线索，无动作/笔顺真值；高质量LR“人工写”只是由curated来源代理，低PPL相似Wikipedia不能当科学正确。250文档人审无一致性CI，已披露7%噪声与有害cluster/性别种族关联，过滤覆盖非完美；退出整页的修正版需显式选。HF字段只图URL，图片重下会衰退，未下载数据验证内容；CCBY4.0+训练使用披露ToU不能代替原内容授权。无多seed、强训练重启/同token与同图/同算力均不能同时等价；未隔离结构因果，未独立复现。

## 预期优势条件

长文交错与caption混合可改善需要语言上下文的少样本问答，按图数更省源于每图关联文本更丰富等联合因素；若要将收益归到原生顺序，须同源重排消融。保留简化DOM可供多图主题连贯研究，时间/接触/规范顺序仍需真值。

## 可证伪实验

固定同源图文、冻结骨干、token/图/计算分别对齐，DOM/CLIP匹配/随机序×长短文×caption比例，单图不可解的多图题及换序干预；OCR/图上结构文本/真实步骤列表分层。各模型同选prompt预算并同时报原答案与首词截断，Hateful给/不给context，0shot标明文字priming。记录3次重启/LR与多seed，按原/退出整页修正版和图片可下载率报告分母；此处未执行。

## 论文组织与Claim学习

完整多层过滤阈值、token/image双横轴和人审残留公开有用；十倍明确限定图量与aggregate，逐任务/提示截断/数据混合/重启要一起给。源网页可见与取得同意分开，过滤成功样本不能覆盖已知残留；HTML自动编号漂移时引用PDF实际编号。

## 实际阅读范围

NeurIPS正式20页+31页Supplement与v2合并51页对照；§1–6、Checklist、A1–A5全研究内容，PDFF1–11实际视觉/T1–11全部，T4全100域、T5全20topic、T6全200topic及词列；51页contact全部看、F11原页放大。references清单和关键引文，非全部引文原文。无新编号式/算法，zloss内联读。固定c50923f仓库README/两配置全文与HF08b7dca卡/元数据；未审全代码/依赖、下载语料权重、运行模型/过滤API。核心三遍和五书面完成。

## 版本与评测口径

正式20页主文件及31页补充与arXiv合并51页对照，PDF实际11图11表；HTML将统计表列为figure而使编号偏移。数据卡明确原始过滤漏掉退出整篇文档，另有修正版配置134648855条；原配置141047697条，均仅提供图片URL。

十倍指按图量达到类似aggregate4shot表现，不等于所有任务/token/GPU耗时十倍。零shot含两个无图文字示例，LAIONonly的首词截断与caption提示另有选择；训练IDEFICS80B及9B混合各三次重启，不能用默认模板掩盖这些协议。
