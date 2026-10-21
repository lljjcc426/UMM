# Timage与BoxTuning：输入视觉标记、证据冲突与实际发布

第九十五批补完[L053](../reviews/L053.md)、[L054](../reviews/L054.md)指定公开版本核心三遍及五项书面检查。目录354条（327论文／研究、27资源），191项核心/194项书面含未通过项，163条尚未确认核心（含资源）。[结构化证据](../../data/timage_boxtuning_protocol_and_release_audit_2026-10-21.json)区分完整原文、正式书目、发布声明和本次推论。未删除文件、下载模型权重/数据媒体或执行模型。

## 版本、任务与阅读范围

[Timage v1](https://arxiv.org/pdf/2606.19944v1)16页，读Abstract/§1–6、Eq1–8/T1–4与图注；实际p5F2/p7Eq5–7/p9T1/p10T2/p11T3/F3/p12T4/F4–5。arXiv comments写ECCV，本次未独立确认正式会议，保留预印身份。所谓Langevin补充不在已取得PDF/HTML中。

[BoxTuning v1](https://arxiv.org/pdf/2604.11136v1)17页，读Abstract/§1–5、Eq1–4/T1–7，实际p7F2/p8F3/p12T2–3/p13T4/p14T5–7。已核[NeurIPS2026官方poster149433](https://neurips.cc/virtual/2026/poster/149433)与Downloads，正式题名改为“Object-Aware Visual Prompting for Multimodal Model Fine-Tuning”；其OpenReview q6gwQDgllS PDF403未取得。正式录用书目与已读旧版分开，不把旧版问题自动归给未读修订版。

Timage生成的是静态图中的query排版，以理解准确率为目标；BoxTuning把已观测物体框/轨迹叠在视频帧上，输出QA答案。两者均不提供文字生成视频、规范汉字笔顺或机器人动作生成实验。视觉标记可以参考到我们的过程理解研究，实际贡献需按输入/输出/指标界定。

## Timage：方法可解释，但关键实验结论仍待核

输入image/query后，从冻结VLM抽Hq，从实例分割/显著图建candidate mask。区域能量−∫αHq拉向相关位置，supportα限制在mask；样式能量用ink预算/平滑调字大小。条件drift经投影Euler–Maruyama采样区域/外观；训练用Langevin伪目标的直线velocity MSE和冻结MLLM任务NLL，STE越过离散投影，K5候选投票。

这些公式分别描述相关性、估计几何约束、候选生成和任务监督。投影相对估计mask可行，并不保证真实前景全部无遮挡，更不保证下游答案正确；核心没有给所用FM目标等价entropic-SB路径KL最优解的证明。drift网络结构、噪声/步数、λ/γ、热图层/heads、渲染器和字体、Eq8标准条件概率与反传实现尚缺。不能仅凭“cSB”名称补齐理论保证。

| 原文可核事实 | 审查结论/仍需证据 |
| --- | --- |
| §3.4模块100epochs/16H20/b128/AdamWlr1e-4/wd.01/cosine；§4称training-free，T2 TrainingNo | MLLM冻结有依据；整方法无需训练与该训练段冲突，训练数据/拆分也未交代 |
| Timage称VMCBench9450题；所引[CVPR2025 AutoConverter官方入口](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_Automated_Generation_of_Challenging_Multiple-Choice_Questions_for_Vision_Language_Model_CVPR_2025_paper.html)报告9018题 | 第九十六批原文追引已明确9450为筛查前、9018为最终发布；仍待Timage使用阶段、样本ID与清洗/隔离协议，不能据此认定新增432题 |
| T1 Base79.1→87.7；四类差值5.7/7.6/3.2/6.1 | 若Overall为同层四类分数固定非负权重均值，差值须≤7.6，8.6不满足；不同层级聚合需明确脚本/权重，暂不判定成因 |
| T2 FullFT Reasoning75.1，本作75.8 | 差.7个百分点，正文1.6不对应此对照；后者对应LoRA74.2 |
| T3 79.1→81.6→84.6→86→87.7 | semantic2.5/mask3/style1.4/ensemble1.7；文字最后2.2有误，style1.4与表一致 |
| T3 RandomBase79.1，T2 RandomOverlay79.8 | 需配置/取样差异说明，不能当同一已匹配基线 |
| T4五骨干均提升，主K5；F4效率曲线 | 是否每骨干另训、各baseline投票次数及测量条件未给足；小参数不等低总成本 |

因此保留“作者报告87.7及各表数字”，不把跨大模型/全参SOTA写为已确证研究事实。顺序添加消融也不能隔离semantic×mask交互或生成框架特异作用；需要同Hq/mask的简单网格/梯度/Langevin排版、投影FM、作者cSB及等K对照。

§5作者真正写的局限是字形不完整和低对比/透明度，声称少影响答案却未给比例。本次额外指出训练free、数据版本、聚合/差值、外部先验和计算预算问题；来源层级分别标注。GitHub同名检索79项未确认本作实现，不能据此宣称全网无代码。

## BoxTuning：表示与信息增量分别分析

YOLOWorld-L按benchmark类别词表检测（conf.3/NMS.5），SAM2跨原始帧传播mask并取tightbox，多关键帧检测补新目标（IoU>.5去重）。给物体分32色，16个MLLM关键帧绘box3px/trail2px，图例约9token/对象；CLIPViTL14冻结，STC全调，Mistral7B q/v LoRA r128/alpha256/drop.05，Answer nexttoken CE。四A10080GB/b16/AdamWlr2e-4/wd.01/cosine/warm100，epochs/steps及部分预处理/上下文条件未披露。

T2对象文字均值1000→88，作者报减少90.8%；这是object text开销，未包括全部视觉token和检测/跟踪。T3比ObjectMLLM五集均提高：78.5/67.2/67.7/79.7/76.5，对方77.6/66.6/67.2/78.5/75.5；相对基础67.9/66/66.5/79.8/76.7，NExT和Intent仍低.1/.2。baseline数值来自[31]，未当成本作同机全量重跑。T4只列LLaVA-NeXT-Video、VideoLLaMA2、SeViLA、ViLA、ObjectMLLM与本作，并有zero-shot/外部复现脚注，不能把RelatedWork中的其他模型当主实验对照。

T5加legend在NExT/Intent仅+.1，正文+.2–.4未涵盖全部列；加trail两集+.3。T6 adaptiveL比L30在CLEVRER/Perc分别+.3/.2，限两集无方差。T7最佳box3/trail2均78.5，宽8降77.1/76.8，支持可见性/遮挡取舍，缺物体数量/密度和检测错误分层。

框与trail利用稠密原帧tracks，MLLM仍只看16帧。其收益包含表示媒介与额外中间运动信息两部分；等信息量和等context预算回答不同问题，应分别设计。Eq2列历史t−L…t−1，正文却说覆盖到下一关键帧gap，需render代码澄清边界。轨迹线可含方向/速度代理，但未证明能恢复逐帧时间、遮挡/形变和所有运动历史；“lossless temporal resolution”需收窄。相同栅格路径可对应不同速度/访问历史，尤其有重叠往返时。

**v1没有独立Limitations，也未见上游检测/密集多框已被作者列为局限的段落。** 此处将漏检、SAM2漂移/ID-switch、32色容量和多标记干扰作为本次问题；线宽消融是已有相关证据。不能把讨论示例变成作者原文事实，正式修订版的处理仍待取得全文。

## 无论文制品式证据：官方README新增效率报告

固定[zekunqian/BoxTuning b722eb7](https://github.com/zekunqian/BoxTuning/tree/b722eb7d571e9f1a5e3ef02b3314b117d4c11e91)完整树只有README一文件，code/camera-ready列TODO。README报告ObjectMLLM .5250→Box .3465秒/样本（1.52×，延迟−34%），FLOPs−30.2%、动态峰显存−37.8%，称包含render overhead。它们不在旧v1中，GPU/batch/输入输出长度/检测跟踪计时边界和原日志未发布，单列作者报告，不自行当全pipeline独立实测。CCBY4徽标也不代表已审核未来全部源码/权重/数据许可。

## 可检验设计与写作学习

Timage先公开训练/测试ID、所有方法逐题输出与聚合，核总分和差值，再匹配K1/5、辅助模型/数据与总成本。加入乱字/语义错配/无文字、相同mask/Hq不同优化器，检可读语义而非标记或先验是否带来特异收益。BoxTuning匹配dense tracks比较紧凑坐标、时间戳点/箭头/衰减trail、ROI，做轨迹反转/置换、错ID/错legend与同终态异时序；按miss/ID-switch/密度分层，换强底座、多seed，实际检查context截断并分段计时。均未运行。

Timage的where/how→energy→dynamics、BoxTuning的获取→渲染→图例→训练组织方式清楚。科研写作应使每个Claim对应具体分布/指标/预算，算力包含外部模块，理论可行性与经验优势分别证明。表文矛盾、少量负迁移与原配方未知项直接保留，不能为叙事完整而补造。

本批追引确认了尚需完整纳入的两项原始工作：[AutoConverter/VMCBench（CVPR2025）](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_Automated_Generation_of_Challenging_Multiple-Choice_Questions_for_Vision_Language_Model_CVPR_2025_paper.html)、[ObjectMLLM（ICCV2025）](https://openaccess.thecvf.com/content/ICCV2025/html/Tang_How_Can_Objects_Help_Video-Language_Understanding_ICCV_2025_paper.html)。本批仅核其官方摘要/书目和关联，不宣称完成它们的原文精读。


第九十六批订正：原VMCBench正式§5已说明9450为转换/清洗前、9018为最终保留（dev1000/test8018），因此前文数量疑点现收窄为Timage使用阶段、题目ID和清洗/隔离协议，不能断言新加432题。ObjectMLLM正式suppD/F已有标注框重训对照、固定颜色画框负尝试，BoxTuning新颖性需据此界定。详见[追引审查](autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)。
