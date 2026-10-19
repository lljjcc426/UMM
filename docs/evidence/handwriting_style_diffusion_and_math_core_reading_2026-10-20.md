# 手写风格、静态书法扩散与数学轨迹：核心三遍审查

本批完成七项既有研究的核心问题/动机、公式作用、框架图视觉核、主表/消融与批判性阅读，逐篇补五条书面理解检查：[SDT](../reviews/A09.md)、[Luhman2020](../reviews/A10.md)、[StrokeExtraction](../reviews/A11.md)、[Calliffusion](../reviews/B01.md)、[Moyun](../reviews/B02.md)、[InkDiffuser](../reviews/B03.md)、[DiffMath](../reviews/B09.md)。缺失作者消融/条件按证据缺口记录，未运行模型。

## 接口与研究先例

| 研究 | 输入→输出 | 需保留的任务边界 |
| --- | --- | --- |
| SDT，CVPR2023 | 标准字体图+作者离线字图→在线单字 | 各语言分别训练，频谱差异未证明严格解耦 |
| Luhman2020 | 文字+离线作者行图→在线英文行 | 已有早期在线扩散先例；长度外部设定 |
| StrokeExtraction，AAAI2023 | 已知有序模板+目标图→逐笔mask | 顺序继承模板，静态分割不观测真实历史 |
| Calliffusion，ICCC2023 | 字/书体/作者prompt→静态图；新字符LoRA | 新字符调用已有风格，任意新作者仍属未来方向 |
| Moyun，McGE2025 | 三种ID→VAE/Mamba静态图 | MM附属workshop；大资源不等实验训练集 |
| InkDiffuser，2026预印本 | 内容/风格图→静态字体 | temporal指去噪步，未测真实墨水动态 |
| DiffMath v2，2026预印本 | LaTeX/RelAST→在线数学轨迹 | LaTeXML依赖、两类pen、无规范笔顺评价 |

## 公式、表格和实现应相互核对

[SDT正式补充](https://openaccess.thecvf.com/content/CVPR2023/supplemental/Dai_Disentangling_Writer_and_CVPR_2023_supplemental.pdf)的预测损失印刷缺少负对数/负号，但[固定loss实现](https://github.com/dailenson/SDT/blob/ba1da572c5c9947a192672e7de639987b878603f/models/loss.py)使用NLL/CE。不能把印刷问题推为原训练方向错误。其test上的α搜索和测试作者监督critic仍需单列，不能因此声称零样本作者评价。

[Luhman2020](https://arxiv.org/pdf/2011.06704v1)Table1的modified sampling FID7.10优于8.05，GS3.3e-3劣于2.7e-3；正文升降描述反向。定量样本明确来自training data，两项共同改善与独立测试泛化均未由该表证明。

[StrokeExtraction正式论文](https://ojs.aaai.org/index.php/AAAI/article/download/25220/24992)均值IoU印刷式缺1/n，[固定源码](https://github.com/MengLi-l1/StrokeExtraction/tree/2d273e0eaa1df448aa5354375bb1a0a9c131f66d)的已读评估函数返回np.mean。无身份版每输出选最大intersection，可复用GT；该指标不等一一匹配身份正确率。模板index也不等真实历史估计。

[InkDiffuser](https://arxiv.org/pdf/2605.05865v1)印刷soft erosion/dilation绝对值≤τ，因此τ→0趋零，不能一般逼近邻域min/max。min/max几乎处处可微，不能笼统说无法反传。[固定公开实现](https://github.com/JingVIPLab/InkDiffuser/tree/4d9f6c1aef2a13ac1b4779aa090389c0d609e227)则用log-mean-exp，训练入口/默认权重与论文仍有差异。STAF-only LPIPS退化、λ指标取舍和两张消融表底座不明均保留，不能选取支持性行。

## 统计结论与实验规模

[Calliffusion正式论文](https://computationalcreativity.net/iccc23/papers/ICCC-2023_paper_111.pdf)150人10题的识真/识假p>.05，支持未拒绝随机猜测假设，不能证明与随机严格等效或图像不可辨。应预设等效margin、考虑题项/参与者相关并增大随机题集。style条件提升总体准确率，但草书字符.72→.64退化也须保留。

[Moyun v2](https://arxiv.org/pdf/2410.07618v2)的[DOI登记](https://api.crossref.org/works/10.1145/3746278.3759378)确认McGE2025 workshop pp19–26。约193万处理图是资源介绍；实际benchmark12985图。40作者×共同40字、每pair至多4图按字面最多6400，若另按script等单位应明确补条件，暂不替作者解释。OCR表分母和1295比test1296少一项；Table2 IoU↓与正文定义↑相反，不能判本法IoU胜。9人选优样本匹配问卷未独立隔离backbone或TripleLabel作用。

[DiffMath v2](https://arxiv.org/pdf/2606.19939v2)将结构条件、latent CTC与count分开消融，count仅额外+.87pp ExpRate，需CI。下游固定一epoch加入150K/30K合成会增加优化steps；新LaTeX分布、数量与结构机制需同曝光对照。不同基线预训/LoRA五epoch/从头重训预算也不相同。[固定仓库](https://github.com/awei669/DiffMath/tree/ec4aa2c651c537622fac9db91aa404cc7918f2cb)目前只有README与Coming soon，不能写成完整代码已公开。

## 选题与验证

静态书法已有三因素条件与新字符迁移；在线生成已有2020扩散、作者风格、整行与显式数学结构；模板笔分割也已有成熟先例。新课题应定义规范事件、历史可观测性和执行约束，并用同信息/同训练曝光/同总成本的强基线验证共享UMM额外收益。

新增实验：①保留几何置换模板编号，区分继承顺序与预测历史；②按新字符/新作者/新书体三种leave-out检PEFT；③对软形态先验做常数邻域、低温极限与梯度解析核，再比简单edge/硬minmax；④合成增强匹配样本数、优化步数与LaTeX新颖度；⑤style评价器多模型校准、独立validation选参。均属计划，未实施。

当前339条目录/339份笔记，334章节或协议、5仅摘要；58项核心三遍及五项书面检查。其余仍待完成核心阅读，候选未全纳入，未独立模型复现；无文件删除。
