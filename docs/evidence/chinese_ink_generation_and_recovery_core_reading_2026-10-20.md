# 中文墨迹生成与轨迹恢复：核心三遍阅读复核

本批精读七项既有记录[A01](../reviews/A01.md)、[A02](../reviews/A02.md)、[A03](../reviews/A03.md)、[A04](../reviews/A04.md)、[A05](../reviews/A05.md)、[A07](../reviews/A07.md)、[A08](../reviews/A08.md)。逐项核问题、核心方法/公式作用、框架图、主表与消融、局限和相关工作，并新增五项书面理解检查。原文没有报告的条件或消融明确保留，未独立运行模型。

## 同样涉及笔画，任务接口不同

| 工作 | 实际输入→输出 | 可以支持的判断 | 不能由该实验直接推出 |
| --- | --- | --- | --- |
| DP-Font | 内容/风格图+笔画类别序列→静态字图 | 该分布FID/SSIM改善 | 笔尖按规范顺序执行 |
| OLHWG | 文字+作者轨迹/布局前缀→单字轨迹再排成行 | 字形/布局条件控制 | 跨字连笔、无目标前缀同样有效 |
| DiffInk | 文字+真实参考前缀→整行轨迹 | 匹配数据下吞吐、内容和风格 | 未见文字零样本、严格短笔事件 |
| LVGM | 笔轮廓前缀→SVG字词诗句 | 压缩矢量续写和图形相似 | 中心线、接触、压力或真实时间 |
| 扩散轨迹恢复 | 静态渲染单字→多笔轨迹 | 该渲染域形状与距离改善 | 唯一真实历史或规范字典序 |
| PEN-Net | 字图→AR点轨迹 | 多语种分别训练的几何恢复 | 无监督统一文字体系泛化 |
| Cross-VAE | 成对字母图/xy→跨模态转换 | Unipen大写拉丁字母实验 | 任意复杂多笔字/个人速度 |

## 公式与指标的冲突保留原证据

[DP-Font正式论文](https://www.ijcai.org/proceedings/2024/0863.pdf)定义PSNR越高越好，但表箭头与正文最佳值按越低越好，不能把该项当改善证据。其PDE的网络输出接口、扩散系数、边界及离散求导未充分报告；物理命名不等于真实墨水动力学已校准。

[OLHWG论文](https://arxiv.org/pdf/2410.02309)对比公式分母排除正例，而[固定源码](https://github.com/singularityrms/OLHWG/blob/e1bed55e0a664e7ebac3279323419c1b94e75dfb/style_classifier.py)实际使用含正例的双向logsoftmax。论文AR/CR定义与一组真实数据数值也有顺序冲突，不能擅自交换标签。论文与公开UNet的学习率、迭代数、embedding维度不同，均单列。

[PEN-Net正式论文](https://openaccess.thecvf.com/content/ACCV2022/papers/Chen_Complex_Handwriting_Trajectory_Recovery_Evaluation_Metrics_and_Algorithm_ACCV_2022_paper.pdf)softmin印刷式缺前导负号。单元素或低温极限即可检查符号；[公开源码](https://github.com/ChenZhounan/PEN-Net/tree/03bc59199f47d34e6df09b1ecdb956bbc284bd4a)调用未随树给出的外部CUDA模块，故不据印刷错误断定原实际训练错误。该六文件版本还缺部分导入依赖/评估入口，默认点损失和pen权重不同于论文。

## 正式版和补充材料改变了什么

[DiffInk正式ICLR2026版本](https://proceedings.iclr.cc/paper_files/paper/2026/file/8547df6ea717b4aad8ae4e52b46a4a4f-Paper-Conference.pdf)已定位，核心公式、表和配置与v3交叉核。[固定掩码实现](https://github.com/awei669/DiffInk/blob/97bc6a3c39a5bdaa9728daaab6d3707480006343/utils/mask.py)确认真实prefix作为条件、有效suffix算训练loss。主评估是否含参考prefix仍需实际benchmark日志，不能把训练mask推成所有评价口径。代码YAML词表/作者占位由dataset按实际缓存覆盖，不能凭默认数字误判类别不一致。

双辅助使下游DiT AR74.77→94.38，VAE重建AR仍约97.6，说明“易重建”与“易生成”需要分别诊断。去ConvNeXt速度更快但内容更差；增加采样步数使AR提高而DTW变差，因此不以单一距离替代内容/事件质量。

[LVGM正式WACV2026版本](https://openaccess.thecvf.com/content/WACV2026/papers/Zhang_Stroke_Modeling_Enables_Vectorized_Character_Generation_with_Large_Vectorized_Glyph_WACV_2026_paper.pdf)及[补充](https://openaccess.thecvf.com/content/WACV2026/supplemental/Zhang_Stroke_Modeling_Enables_WACV_2026_supplemental.pdf)明确StageII为5 epochs；正文写5 iterations，保留冲突。StageI正文/补充正文与表的lr/步数仍不一致，不能拼成唯一配方。907267条主要来自有限字形与文本组合，实际LLM实验最多100K；每笔闭合轮廓不等真实笔尖中心线。

## 恢复分布与规范历史

[扩散轨迹恢复](https://arxiv.org/pdf/2607.03422v1)在相同CASIA渲染协议下比重实现基线更好，但未报告概率覆盖、校准或1000步推理成本。最细单尺度反而劣于全局向量，消融应解释这一反例。[Cross-VAE](https://arxiv.org/pdf/1906.06142v1)缺独立共享loss消融、样本量及writer划分，不能凭三行结构对照补出不存在的证据。

静态末图对应多种可行路径，实际CASIA记录顺序、规范字典顺序、可执行物理顺序应分开标注。建议同几何置换笔序/方向、同顺序改变宽度/采样密度，分别量几何、顺序和抬落笔事件；不能仅靠最大膨胀AIoU评价规范性。

## 完成状态校正

此前40项已有五条答案、核心图视觉证据与主表/消融解释。本批逐项确认其满足相同核心阅读口径，保留每项previous_boundary，不计新增40篇阅读。计时口试、逐行全部代码、全附录和独立复现分别记层级，不额外作为读懂核心论文的必要条件。

目前339条目录、339份笔记，334项章节/协议核查、5项仅摘要；51项完成核心三遍和五条书面检查。其余条目仍待核心复核。五项受阻全文与未读候选继续保留队列；不能宣称全部完成或全领域零遗漏。无文件删除。
