# GAN、VAE：理论、估计器与视频表示边界，第五十批

深化[GAN G028](../reviews/G028.md)、[AEVB/VAE G029](../reviews/G029.md)。实际精读[1406.2661v1](https://arxiv.org/html/1406.2661v1)、[1312.6114v11](https://arxiv.org/html/1312.6114v11)核心、所列证明/附录、主结果及已有对照。目录344项＝318研究＋26资源，核心三遍117、五条书面检查119。无删除、训练、推理或独立复现；完整其他图/代码和历史版差异不在本批验收内。

## 两种目标回答的不同问题

| 对象 | 研究困难与机制 | 可成立的条件 | 对书写/视频不能省略的验证 |
| --- | --- | --- | --- |
| GAN | 隐式G与可学习D绕开显式密度/归一化/逐例推断，以真假反馈学习采样 | 可微G/D、足够容量与协调优化；理论另有理想假设 | 训练稳定/模式覆盖、稀有字符、顺序与重复/擦除；D分不能替真值事件 |
| AEVB/VAE | 难积后验与高方差梯度；SGVB路径导数和摊销推断联合优化下界 | 连续可重参数化latent、可微函数/合法期望微分、近似后验足够 | 原RGB→posterior重建→prior/骨干生成逐级测细线和时标；ELBO不替过程质量 |

GAN与VAE的原实验均为静态图像。后继视频VAE、绘画动作模型和对抗蒸馏可以借用思想，但数据时间维、编码压缩、条件接口、优化目标与评价均需独立说明，不能把原图像结果写成已证明的视频优势。

## GAN：分布最优与有限网络训练

原minimax为minG maxD Edata logD+Ez log(1−D(G(z)))。固定G逐点求最优D得到pdata/(pdata+pg)，代回为−log4+2JSD；因此在理想可行的分布空间，全局最优分布相等。两密度皆零处D未由目标规定；唯一分布不表示参数、latent映射或整个空间D都唯一。原Fig1四幅分布/映射示意和Algorithm1已核。

Proposition2另要求每一步D达到最优并对pg作足够小更新；它讨论分布函数空间。有限网络参数化有多个临界点，实际k1判别/G交替和momentum不能直接获得该收敛保证。原文已主动讨论D/G同步及Helvetica式模式塌缩；此不足已有长线研究，不能重新包装成新发现。

非饱和−logD(G(z))缓解D强时生成梯度弱，原文给出机制解释；它与原minimax有相关理想固定点，但不保持全部目标/梯度，更不能把实际任意训练loss直接称在最小化JSD。该文无现代全面组件消融，笔记明确缺失，没有另造实验或数字。原例MLP/maxout/dropout和CIFAR卷积示例也不能替成后来的DCGAN架构。

T1 MNIST Parzen225±2高于DeepGSN214±1.1；TFD2057±26均值低于StackedCAE2110±50。MNIST为实值版本，±项为测试样本间SEM；TFD为fold间SEM、各fold验证σ。Parzen是对生成样本拟合的平滑密度，非pg精确似然，作者明确承认高维局限。没有FID/IS、没有视频/笔顺指标；不同数据表示/估计器不可跨VAE曲线排名。作者没有声称视觉样本优于所有前作，最近邻样例也无法证明全模型无记忆。

## VAE：既有变分下界与SGVB贡献

logpθ(x)=L(θ,φ;x)+KL(qφ(z|x)||pθ(z|x))，L=Eq logpθ(x|z)−KL(qφ(z|x)||pθ(z))。ELBO是既有变分基础，本文的贡献是SGVB可微估计/梯度和AEVB摊销联合学习。Gaussian实例z=μ+σ⊙ε，ε独立于参数；解析KL的估计器只对重建采样，减少估计噪声。原Fig1的生成实线和近似后验虚线、Algorithm1及Eq1–12/AppB–C已核。

对角Gaussian与单hidden MLP为实例选择，不能称所有SGVB只能对角高斯。连续路径导数有可微/求导与积分交换等条件；离散latent不能直接照搬。同样，无偏MC下界/梯度不表示q等于真后验、有限样本倒数/取log的似然估计无偏。更高ELBO可能来自更紧q，也可能伴更好生成模型，不能仅以重建误差判断prior样本质量。

原训练M100/L1、Adagrad步长{.01,.02,.1}按初期训练表现选，含小weight-decay对应MAP；MNIST/Frey hidden500/200。FullVB附录还推导权重后验，但主实验并未验证这一扩展。§5出现generative“encoder”与variational“decoder”的反置用词；按定义/公式和AppC解释方向，未传播该错误。原重建为概率log-likelihood，Gaussian仅在方差等条件固定时化为MSE；现代LPIPS/GAN和任意KL系数不能无说明称原ELBO。β>1仍可低于原ELBO但恒等分解已变，β<1一般不保证下界。

## 主结果和现有对照的真实范围

| 原结果 | 观察 | 可支持的结论 |
| --- | --- | --- |
| VAE Fig2 | MNIST latent3/5/10/20/200，Frey2/5/10/20，AEVB所示ELBO更快更高 | 支持所测模型/维度的优化优势，仍有train/test gap，非任意高维免过拟合 |
| VAE Fig3小数据 | Ntrain1000、hidden100/latent3，AEVB train约−109/test约−143；MCEM test约−141 | AEVB训练提升较快，测试估计未全面胜出；数字为读图近似 |
| VAE Fig3大数据 | Ntrain50000，AEVB test约−138，wake-sleep约−141/MCEM约−149 | 所测样本处理预算更有优势，横轴非严格等墙钟 |
| 估计协议 | AppD低维<5较可靠；AppE用前1000 train/test点、50后验样本/4HMC leapfrog | 估计型评价受维度/混合/密度拟合影响，不是精确似然与多seed CI |

该VAE论文无主数字结果表，以主曲线/潜维和数据量及算法对照作解读，明确没有现代消融矩阵。MCEM使用HMC不表示AEVB训练或prior采样必须MCMC；实验评价的估计过程应单独计成本。SGVB的likelihood评价与GAN高维Parzen不同，不以曲线/表的原数值互排。

GAN正式身份由[NIPS2014条目](https://proceedings.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)确认；arXiv标题Networks与会议Nets保留版本差异。AEVB的[作者旧材料](https://dpkingma.com/old/)标ICLR2014 Banff，[ICLR官方Test of Time](https://blog.iclr.cc/2024/05/07/iclr-2024-test-of-time-award/)也确认研究并明确提到Rezende同期工作；2022 v11只是arXiv修abstract typo，未改写成2022新模型。

## 实验设计和研究写作

对抗绘画/视频蒸馏先固定数据、骨干、条件和预算，比较D/G步数、判别器容量、饱和/非饱和loss；看多训练seed、质量/模式覆盖、长尾字符与乱序/静止/反播反例。D应同时评局部细线和全时序，外部独立评测器/真值事件/人评避免只优化自身真假分。

视频VAE固定潜维或码率与decoder预算，分posterior均值/样本重建、decoder均值/采样、prior采样与下游生成阶段；测OCR、拓扑、笔事件召回/时标及跨作者/字形。KL/重建/感知/对抗项分别扫，记录其概率解释、后验使用/先验失配与训练/推理成本。对比更灵活q/迭代推断时区分摊销和近似误差，不能只报低重建loss。以上未运行。

写作学习：由难计算的具体操作界定问题，再给可计算目标/估计器与算法；定理写清空间/容量/优化假设，实例设计不冒充一般理论限制；Claim包含指标/估计器和负结果，Limitations公开有限网络、覆盖率、近似后验和高维评价问题。原文未直接量化的后验塌缩/视频细线等以本仓库问题提出，继续追引相邻研究后再判断新颖性。

阅读边界：GAN完整核心与证明/T1/2、Fig1四幅；Fig2/3未完整视觉、正式PDF差异及全代码未核。VAE核心与AppB–E全读、F至Algorithm2/F.1初段；F.1最后展开、AppA完整图与全代码未核。全部剩余审查继续。
