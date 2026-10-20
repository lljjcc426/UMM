# 神经绘画的集合、语义、优化与程序：第四十二批

深化[Paint Transformer](../reviews/G016.md)、[CLIPasso](../reviews/G017.md)，补录此前只作为基线提及的[Stylized Neural Painting](../reviews/F06.md)、[SPIRAL](../reviews/F07.md)。四项新增核心三遍及五条书面检查，累计96项核心三遍/98项书面检查；主目录342项（318论文/研究、24资源），这些是目录条目数，不等独立正式论文数。未训练、推理或删除文件。

## 任务、监督和过程的边界

| 工作 | 主要接口/监督 | 结果证据 | 对书写研究的边界 |
| --- | --- | --- | --- |
| Paint Transformer | target+canvas→局部笔触集合；随机合成笔触参数监督 | 重建误差/参数误差/速度 | 集合loss忽略笔顺，patch切割影响长结构 |
| CLIPasso | photo→Bézier控制点优化；冻结CLIP语义/几何 | 人类识别、两类分类器、定性消融 | 全部曲线同时优化，无时间顺序；语义抽象可损害近形字 |
| Stylized Neural Painting | photo→逐图参数优化；合成renderer+L1/OT | 单笔PSNR、终图示例/曲线 | 非真实画家时序，单笔PSNR不评价整段视频 |
| SPIRAL | image distribution/target→黑盒绘画或场景程序；RL+D | 重建曲线/无条件例图/MCMC调用 | 无人类程序GT，但仍有图像/手工动作/辅助奖励 |

## Paint Transformer：速度的比较对象和代码版本

实际正文为[arXiv2108.03798v2](https://arxiv.org/html/2108.03798v2)，[CVF](https://openaccess.thecvf.com/content/ICCV2021/html/Liu_Paint_Transformer_Feed_Forward_Neural_Painting_With_Stroke_Prediction_ICCV_2021_paper.html)核ICCV2021身份。随机背景/前景合成数据训练8query集合预测，Hungarian匹配L1/高斯W2/BCE，图像loss约束渲染。存在性前向Sign、反向sigmoid近似；不能把近似梯度称精确可微离散决策。

T1真实Lpixel/Lper，RL为.040/.737、本法.056/.807、Optim.059/.856；本法未全面领先。T2在512分辨率本法.304s、RL.322s、Optim521.447s，同RL仅约1.06倍；.304s也不足30FPS。去image/L1/W/BCE的像素误差各升高，但这些终图/参数指标没有检查规范事件。

[官方固定a5ceece](https://github.com/wzmsltw/PaintTransformer/tree/a5ceece46166665dbed3cb61a0f334f759e3a79e)在inference.py实例化5维形状输出，render_serial.py从预测中心grid_sample目标RGB再拼成8维。论文描述学习8维参数，两版本须分列。README称后来串行改进质量但变慢/省显存；不能把当前串行演示当论文T2重现。原训练代码未取得，PyTorch复现与Paddle原实现分别记录。

## CLIPasso：代理评价改变结论

读[作者项目34页PDF](https://clipasso.github.io/clipasso/static/source/paper_CLIPasso_Semantically_Aware_Object_Sketching.pdf)正文与补充核心。三次Bézier经diffvg，RN101中间几何+final语义loss，ViTB32 attention×XDoG初始化。3seed选最小无增广loss，通常2000iter；[官方92262f7](https://github.com/yael-vinker/CLIPasso/tree/92262f702b6592b6c25c80def6284ad06225eadd)默认500iter，不能混为同配置。

| 评价 | 16笔 | 32笔 | 结论范围 |
| --- | --- | --- | --- |
| 人类类别识别 | 97.9±.8 | 99.3±.5 | 5类、25图；4笔仅36±3 |
| ResNet34 Top1 | 54 | 63 | 人类98、baselineA67；本法未领先 |
| CLIP-ViTB32 Top1 | 78 | 91 | 同CLIP预训练家族，非完全独立裁判 |

补充的随机/显著初始化、去语义/几何与层/权重实验主要是定性图；没有同规模逐项人类消融。正文121参与者，补充60+38+24=122，需保留未解释差异；层编号正文3/4、补充消融3/2，未证明是实现错误。作者明确没有stroke ordering，高抽象与背景干扰会失败。

## Stylized Neural Painting：PSNR和OT分别说明什么

正式身份为CVPR2021，实际读[2011.08114v1](https://arxiv.org/html/2011.08114v1)及附录。双路径着色/轮廓renderer单笔拟合，逐图L1+OT优化笔触；OT在48²、ε.01、5次Sinkhorn下近似求plan，不能称已收敛的精确Wasserstein或全局最优。

T1平均前景/alpha PSNR油画full26.982，对单支路24.015/26.048；水彩31.389，对25.769/29.045。该表没有测最终画作/视频。Fig12有无OT的花形/数字示例支持位置优化动机，缺大样本和等时间消融；Fig10本法400笔、SPIRAL20笔且部分图取原文，不能据此宣布统一SOTA。[官方e7a66b2](https://github.com/jiupinjia/stylized-neural-painting/tree/e7a66b20259141656df04d41629b7d4f27fd9262)提供PyTorch代码/命令，当前模型加速宣传不当作论文结果，未执行。

## SPIRAL：黑盒、奖励和程序不可辨识

读[PMLR正式10页正文](https://proceedings.mlr.press/v80/ganin18a/ganin18a.pdf)及[2页补充](https://proceedings.mlr.press/v80/ganin18a/ganin18a-supp.pdf)。64²画布、CNN/残差/LSTM和tuple自回归动作，经Libmypaint或MuJoCo黑盒；A2C/IMPALA策略和WGAN-GP判别器交替学。无程序成对GT，仍依赖图像监督和预设动作空间。base为终步D奖励，MNIST有连续/空白惩罚、CelebA有颜色直方图辅助，不能把所有实验说成只有终图奖励。

Fig8曲线支持所测分布下学习D优于固定ℓ2；无精确端点/CI不造数字。Fig9承认早期笔触被后笔覆盖，说明终图成功不约束过程。MuJoCo按renderer调用比MCMC，需计策略训练摊销。每实例64CPUactors+2GPU、PBT12实例，训练成本不能写单GPU。

补充A正距离势与主文min LD=−D(target)+EgenD的方向不一致；按正文奖励最大化，距离势应为负范数至加常数。须先统一符号，不能据正距离公式设计吸引目标奖励，也不因此否定实际运行结果。最优势非唯一，D学习增益仍需实验。[官方5ee538c](https://github.com/google-deepmind/spiral/tree/5ee538cedf1d9cc827ced93fe86a44f8b8742ac0)公开19步无条件CelebA-HQ模型，不直接等正文20步条件重建。

## 可证伪实验与写作学习

固定renderer、笔数、画布/工具、硬件和运算预算，比较优化/RL/集合/自回归及后续扩散方法，分别报告训练摊销与推理质量。消融采色或学习颜色、图像或几何loss、OT近似、全局上下文和过程奖励。按长跨patch结构/重叠/近形文字/真实材料留出，测终图、拓扑、笔事件、遮挡和真实执行；乱序同终图检验代理指标的盲区。上述是实验设计，尚未运行。

Introduction提出的困难要由对应模块和实验支撑：效率对应等预算时延，renderer对应单笔拟合，语义抽象对应独立识别，规范过程对应事件/物理评价。Claim必须带数据分布、比较条件与负例；不能把终图、少笔抽象或渲染动画的证据扩为真实书写视频能力。后续CLIPascene/DiffSketcher、AttentionPainter/I-Paint等仍需追引去重，不能宣称覆盖结束。
