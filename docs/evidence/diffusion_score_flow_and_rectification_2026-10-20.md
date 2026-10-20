# 扩散、Score-SDE、Flow Matching与Rectified Flow：第四十三批

深化[DDPM](../reviews/G001.md)、[Score-SDE](../reviews/G002.md)、[Flow Matching](../reviews/G005.md)、[Rectified Flow](../reviews/G006.md)。新增四项明确版本的核心三遍及五条书面检查，累计100项核心三遍/102项书面检查。342项主目录不增删；未训练、推理或复现，未宣称全部旧记录/候选已读完。各篇记录数据、架构、指标、基线、条件、因果假设和写作学习。

## 四项工作的任务与理论接口

| 工作 | 学习目标与采样 | 论文证据 | 对书写视频的边界 |
| --- | --- | --- | --- |
| DDPM | 固定高斯链，噪声回归；1000步逆向采样 | FID/IS、离散NLL上界、参数化/权重消融 | 扩散时刻为噪声级，没有真实笔事件 |
| Score-SDE | 连续score；逆SDE、PC或probability-flow ODE | 等NFE对照、连续密度、结构扫描 | 理想共享边缘不保证真实过程 |
| Flow Matching | 条件速度回归，推理ODE | 同架构目标/路径对照，NFE/NLL、超分 | 训练条件样本不等文本条件；条件OT不等全局OT |
| Rectified Flow | 线性coupling回归，reflow重建端点对，另distill | 步数曲线、直度、FID/recall、域适配 | 直度/凸位移成本不约束笔顺、物理执行 |

以上是静态图像/分布输运研究。迁移到视频时，模型生成流时间t与视频帧时间τ需要明确分离；生成轨迹平滑不能直接用作书写过程正确的证据。

## DDPM：去权重带来的质量—似然取舍

实际读[2006.11239v2](https://arxiv.org/html/2006.11239v2)，[NeurIPS2020论文页](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)核身份。固定q允许任意t闭式加噪，ε参数化逆均值，简化loss移除ELBO噪声MSE中的时间权重。两者需结合分析。

| CIFAR配置 | FID | 测试NLL界（bpd） | 支持的结论 |
| --- | --- | --- | --- |
| ε+无权MSE | 3.17 | ≤3.75 | 所测感知质量较好，似然界较差 |
| ε+VLB | 13.51 | ≤3.70 | 优化界未同时改善FID |
| 均值+VLB，T2 | 13.22 | 该行未给 | 单改ε参数化未解释质量差距 |

FID3.17以训练统计作参考，换测试统计为5.24；不得混用。IS9.46±.11不代表多训练seed置信区间。最终配置各训练一次并按最低FID选checkpoint。CIFAR采样批256约17s、256²采样批128约300s，均为批量时间。[官方1e0dceb](https://github.com/hojonathanho/diffusion/tree/1e0dceb3b3495bbe19116a5e1b3596cd0706c543)CIFAR默认与loss选段已核，未运行。

## Score-SDE：固定预算、检查点和密度定义

实际读[2011.13456v2](https://arxiv.org/html/2011.13456v2)。前向f/g与score给反向SDE漂移f−g²score；probability-flow ODE为f−½g²score。在正确score和正则条件下，两者共享各时刻边缘；路径不同，有限回归/积分误差需另测。

T1同2000次score调用，VE reverse-diffusion的P2000 FID4.74±.08对PC1000 3.60±.02；VP对应3.19±.02对3.18±.01，优势大小依SDE变化。PC1000包含1000predictor和1000corrector；只比P1000会混入预算差。C2000为VE20.43/VP19.06，纯校正较差。五次为采样重复，SNR网格调参成本也应计入。

T2深DDPM++ subVP末checkpoint的ODE NLL2.99/FID2.92，与T3深NCSN++ VE最小FID checkpoint的PC FID2.20/IS9.89分列。连续去量化ODE密度、Hutchinson迹估计/数值容差与DDPM离散ELBO上界定义不同，不拼成同一模型双最优结果。class条件还需噪声classifier训练，逆问题存在近似，不能概括为所有条件都无需新训练。

[官方0acb9e0](https://github.com/yang-song/score_sde/tree/0acb9e0ea3b8cccd935068cd9c657318fbc6ce4c)JAX配置：b128/lr2e−4/warmup5000/clip1，deepVE用Langevin、deep subVP配置corrector=none。README四V100是框架benchmark；原CelebA系列权重未公开，后来个人资源重训制品与论文checkpoint分开。

## Flow Matching：条件目标正确性与有限模型收益

[2210.02747v2](https://arxiv.org/html/2210.02747v2)用连续性方程与条件期望推导边缘速度，CFM与FM平方目标相差θ无关常数。OT高斯条件路径给恒定条件速度；总体边缘流仍可弯曲。σmin>0意味着终分布被平滑，已核文本未找到明确运行σmin数值，保持待核。训练免ODE积分，采样/密度仍需积分。

T1同ADM架构：CIFAR DDPM为3.12bpd/7.48FID/274NFE，FMdiffusion3.10/8.06/183，FMOT2.99/6.35/142；ImageNet64为DDPM3.32/17.36/264、FMOT3.31/14.45/138。此处CIFAR6.35未胜过原DDPM3.17或Score-SDE2.20的不同配置，不能宣称跨论文全面领先。

超分T2 FMOT FID3.4/IS200.8好于SR3 5.2/180.1，但PSNR24.7/SSIM.747低于SR3 26.4/.762；应报告感知与失真取舍。IN128模型较ADM大25%，500K×1536与4.36M×256训练样本量也不同，不能只按steps宣称九倍总成本加速。AppC的Hutchinson无偏论证给log density；指数化后的density与数值误差不自动继承该无偏性。AppE/F去量化K设置另记。

## Rectified Flow：低步收益与高步负结果同时存在

[2209.03003v1](https://arxiv.org/html/2209.03003v1)回归线性插值的端点差，条件平均速度诱导ODE；reflow使用旧ODE端点对再次训练。[ICLR2023官方目录](https://iclr.cc/Downloads/2023)确认FM/RF身份，但此次未完整读取两者正式终版PDF。

| CIFAR生成 | 1-RF | 2-RF | 3-RF |
| --- | --- | --- | --- |
| 未蒸馏一步Euler FID | 378 | 12.21 | 8.15 |
| 另做LPIPS蒸馏后一步FID | 6.18 | 4.85 | 5.21 |
| RK45充分积分FID | 2.58 | 3.36 | 3.96 |
| RK45 NFE | 127 | 110 | 104 |

少步表现改善、充分积分质量退化可同时出现，作者讨论velocity估计误差积累。4.85包含额外蒸馏，且3-RF蒸馏5.21未单调改善。Fig8质量—步数和Fig9直度原图已核；直度下降不推出FID下降。

Thm3.5在理想条件期望/正则假设下保证凸位移成本不增；Thm3.7为历次最小直度的O(1/K)界，非有限NN每轮或FID保证。高维直coupling不必全局OT；同一时间ODE流线不交也不禁止真实笔迹跨时间交叉。图像转换feature-weighted变体不自动继承原L2全部理论。域适配OfficeHome69.2对CORAL68.7，DomainNet41.4低于CORAL41.5；目标测试特征访问协议仍需补核。

[官方5a1fd4d](https://github.com/gnobitab/RectifiedFlow/tree/5a1fd4dd3ea7db764ce370a84ce35f9c8b15fde6)：普通EMA.999999，reflow/distill EMA.9999；uniform-t/L2与t0/LPIPS分开。正文4M端点对+300K微调，README至少1M建议和命令100K一批分开；额外教师采样/存储成本需计。代码反向ODE直接从t=1积分到ε，重参数化负号公式还需变换时间变量。

## 研究假设和实验设计

固定架构、数据、样本吞吐、训练预算与checkpoint选择，拆参数化/目标/路径/solver，分别比较固定NFE、固定墙钟、固定质量；学习率/SNR搜索和教师数据生成纳入总成本。多训练seed与同模型多采样重复分开，NLL注明离散界/连续密度/去量化K/trace与积分误差。超分并列FID和PSNR/SSIM，RF完整画少步到充分积分曲线，均为待执行设计。

用于文字视频时，额外控制字符/书体/语言/近形差/细笔、真实动作与相机分布；静态终图和FID之外测拓扑、笔事件次序、时间可观测性、工具可执行性。用同终图乱序/覆写/瞬间出现反例检验指标；静态图像流论文尚未验证这些假设。已有DDPM、Score-SDE、FM/RF的不足只提供问题线索，后续LDM、DiT、consistency、快速求解器、视频模型及新研究仍需追引，未据此宣布新颖性。

## 阅读与写作边界

本批完成明确预印本版本的核心三遍，逐篇sections_read列实际正文、附录、视觉核和代码选段。部分正式PDF未完整获取、不计已读；未对全附录/源码/全部图逐条审查。先讲公式承担的作用，再核正则假设和推导，知识缺口单列。Introduction的问题要对应Method机制和实验；Claim带分布/预算/指标，Limitations保留负结果、近似与协议空缺。无训练/推理、无独立复现、无文件删除。
