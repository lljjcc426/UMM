# 静态文字、字形动画与绘画过程：核心三遍审查

本批对[AnyText2](../reviews/B04.md)、[KineTy](../reviews/B05.md)、[Dynamic Typography](../reviews/B06.md)、[Inverse Painting](../reviews/B07.md)、[AnimatePainter](../reviews/B08.md)完成核心问题/动机、公式作用、框架图视觉核、主表与现有消融、批判阅读及各五条书面检查。逐篇保留七个实验协议字段和五个因果分析问题；未运行模型。

## 输出和时间的含义

| 研究 | 输出/时间 | 主证据及范围 |
| --- | --- | --- |
| AnyText2 | 静态文字图；扩散step | 文本行OCR与外观/控制/延迟，不证明视频 |
| KineTy，ECCV2024 | Latin字串动效RGB、24帧 | 专业模板派生数据；测试共享模板 |
| Dynamic Typography，ICCV2025 | 单字母SVG形变动画、24帧 | 每prompt优化；无规范笔事件 |
| Inverse Painting，SIGGRAPH Asia2024 Conference Papers | 约20秒物理间隔的画布关键帧 | 真实视频去手/工具/细变化；合理粗历史 |
| AnimatePainter，2025预印本 | 合成先验的RGB短过程 | 测试静态图无GT过程，终帧指标为主 |

RGB动效、画布更新、可执行笔尖事件、历史识别和规范书写是不同输出。各自已有先例，创新需要明确输入信息与约束。视频扩散的去噪时间不等物理绘制时间；整clip联合采样也仍可多步去噪。

## 指标可支持到哪里

[KineTy正式论文](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05000.pdf)Table2/4把IS标↓，但[IS原始定义§4](https://arxiv.org/html/1606.03498v1#S4)是exp(E KL(p(y|x)||p(y)))，以低条件熵/高边缘熵为目标。未取得KineTy完整评估实现，先保留方向冲突，不擅自解释为逆IS。其FVD125.90较低，但OCR .76低于TextDiffuser+SparseCtrl .90；full IS1.77即按论文↓也劣无字条件1.74。

[Dynamic Typography正式论文](https://openaccess.thecvf.com/content/ICCV2025/papers/Liu_Dynamic_Typography_Bringing_Text_to_Life_via_Video_Diffusion_Prior_ICCV_2025_paper.pdf)的相邻CLIP .9963低于DynamiCrafter .9979；去可读性loss的warp .0156优于full .0165但字形相似下降。应评运动幅度/静止率/字形可读的Pareto，不能只用相邻相似度判动效成功。

[Inverse Painting v2](https://arxiv.org/pdf/2409.20556v2)的mask IoU跨真实全时刻取最大，忽略顺序；DDC对真实目标距离曲线做DTW，baseline时间间隔有人工标定。人评宣传的1.9×等来自逐题四法评分归一，raw评分4.21对SVD2.96，不能写成原始评分比或胜率。

[AnimatePainter v1](https://arxiv.org/pdf/2503.17029v1)测试1000张静态LAION-art，没有GT过程；其DDC使用未充分定义的理论曲线，与Inverse Painting不能跨论文按数值排名。SSIM .524仍低于Timecraft .550；−DL文字描述同时去掉DF和layer，未独立隔离layering。

## 实现、数据和主表的对应

[AnyText2固定代码](https://github.com/tyxsspa/AnyText2/tree/b06c583a583818f3679665ef67b51363f107853c)默认train.py用200K/15epochs/mask_ratio0；主文8A100/10epochs/globalb48/50%编辑mask。每卡b3×accum2×8可吻合48，不能误列batch冲突。速度5.85→4.69s等于延迟−19.8%、吞吐+24.7%，两者分母不同。颜色/长caption/WriteNet消融的准确率退化均已记录。

[KineTy固定代码](https://github.com/SeonmiP/KineTy/tree/a83f29ce072ae23ac8b7c1986adf208492139f0b)train.py目标是ε，但glyph分支直接VAEdecode ε，末帧masked像素L1；论文Eq8则加权噪声MSE。静态差异需要实际训练版本和受控实验解决，不能推定主表无效。584模板×1000=584000样本；模板IP限制完整数据再分发，需许可模板、AfterEffects和Nexrender重新构建。

[Dynamic Typography固定代码](https://github.com/zliucz/animate-your-word/tree/8e092aeea908a6f2b77f14b0df05b1dbc6662c63)补足hidden128/multires6、默认perceptual/angles各1000及transition20000。作者README说明加transition会减运动幅度。角度实现边长加.1、三角过滤首轮廓且未显式holes，需针对多轮廓/内洞与方向翻转另测；它不构成严格拓扑保持证明。

[Inverse Painting固定代码](https://github.com/ArmastusChen/inverse_painting/tree/3a27592d5eab6fa46f7a434ae93df0db32b2d6fd)两个默认yaml均600Ksteps，论文mask80K、renderer200K。公开样例与[模型权重](https://huggingface.co/boweiche/inverse_painting)分别记录，完整294视频发布清单未在已核README找到。主图与补充的拼图左右顺序不同，已读预处理为[current,target]；不能把一张框架图当全部实现事实。

## 可证伪研究设计与写作学习

1. 共同训练数据/总预算/相同输入与采样次数比较静态后动画、wholeclip、AR及显式stroke强基线；按模板、作者、题材、字体和新字符分别留出。
2. 建立静止终图、线性淡入、随机顺序、简单逆擦除基线，检验终帧/CLIP/DDC是否会奖励错误过程；有序mask一一匹配、独立完成度、运动幅度、笔事件和物理时间并报。
3. 分别干预GT/预测text与mask观察rollout误差；控制ε/x0转换后消融glyph目标；depth真/乱/常量、DF×layering严格2×2，同合成数据检机制。
4. 字形loss权重扫描报告动态—可读性—结构Pareto，人评按用户/题项相关给CI，区分多选可读、单选偏好、原始评分和归一比例。

写作按输出接口定义问题，方法按每项失败机制分工；主表给指标方向和基线训练条件，消融保留退化。Claim限定物理时间、任务和数据域，Limitations明确历史多解性、上游传播、配置/数据发布范围及评价捷径。上述实验均属计划，未实施。

当前339条目录/339份笔记，334章节或协议/5摘要；63项核心三遍与五项书面检查。其余核心精读、候选追引和部分全文仍未完成，未独立模型复现。无文件删除。
