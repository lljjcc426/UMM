# 交错数据、指令编辑与教师微调的证据审查

日期2026-10-20；L057、L169–L174七项存量分析。各自七字段、五个因果问题、写作学习和未读范围见[逐篇索引](../reviews/README.md)。数字均为作者报告，未执行训练/推理；本批无独立新增论文、无删除。

## 文档顺序的含义

| 工作 | 顺序的构造 | 对时序研究的证据边界 |
| --- | --- | --- |
| MMC4 | CLIP图句匹配，随机放句前/后 | 不保原DOM或真实事件时间 |
| OBELICS | DOM提取保网页结构 | 网页排版/讲解顺序未标物理时间 |
| OmniCorpus | 网页结构，另有视频关键帧+ASR故事板 | 稀疏关键帧会漏瞬时笔画，缺动作标注 |
| CoMM | 教程/故事步骤及多维coherence筛选 | 可有多种合理顺序，静态步骤不等于连续视频 |
| InstructPix2Pix/ShareGPT4o | 输入图—指令—输出图 | 编辑配对不提供帧间运动或严格增笔约束 |

MMC4正式表为571M图/101.2M文档，OBELICS引用585M/103M保留版本差；OBELICS353M图像出现次数中298M唯一。OmniCorpus8.6B也是图像出现次数。IP2P454445是生成文字三元组，每对文字筛至多4图对，不能用同一数字随意代表最终配对数。

## 量化结果保留取舍

IDEFICS80B/32shot COCO116.6高于Flamingo113.8，但VQA65.9低于67.6、Hateful ROC-AUC52.5低于70。OmniCorpus四shot聚合改善，零shot和部分单任务有下降；混合训练和更换视觉/语言骨干须拆分归因。

CoMM的DPO使SEED8B FID57.96→63.05、IRS5.27→4.69，14B也下降；文字偏好改进不能概括成全部生成质量提升。ShareGPT4o同协议JanusPro GenEval.76→.80，color.90→.88；DPG提升伴attribute下降。91K是继承JanusPro后的额外微调数据。官方README写92K但分项45K+46K仍91K，manifest未核不强行统一。

IP2P的Fig8/10为已视觉核的量化曲线，衡量源图保持与编辑方向。数据/过滤影响折中曲线，不能编造不存在的主结果表或未标注精确点值。其实际制图对selfattention替换详见补充C2，须与P2P一般crossattention介绍区分。

## CoMM公式需保留未决状态

[正式论文](https://openaccess.thecvf.com/content/CVPR2025/papers/Chen_CoMM_A_Coherent_Interleaved_Image-Text_Dataset_for_Multimodal_Understanding_and_CVPR_2025_paper.pdf)p4 Eq1第二项对全部j<i求和，系数为2/[(N−1)(N−2)]；共有N(N−1)/2个pair，因此不等于文字所称的全部pair均值。若所有相似为1，印刷式结果为−2/(N−2)，且N=2无定义。这是对印刷公式的代数检查，没有证明实际筛选使用同样的式子。

[固定公开树](https://github.com/HKUST-LongGroup/CoMM/tree/0da05d494a25af3ca03a512b9a2c74c9b0dc9421)的README与评价图像指标已读，未定位筛选实现。不能悄改求和上界或系数，再当作者方法解读；需要作者确认或找到实际执行代码。验证时长度与内容分别控制。

## 综述与版本的使用

L057综述v6截止2026-01，帮助检索分类，未新增模型实验。其笼统视频能力标签和展望需要回到每个模型原文，不作为十月的新颖性证据。OmniCorpus由官方README核ICLR2025；本次OpenReview正式PDF403，实际阅读arXivv3，不混称读过正式PDF。

剩余历史8项继续核原文，之后33条摘要/5份第一遍及全部完整三遍仍待完成。SCI一区身份须在具体年份/学科口径下核，排版和高引用不能代替分区证据。
