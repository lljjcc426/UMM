# Diffusion Forcing：理论、任务协议和代码版本审查

第六十八批补完[G030](../reviews/G030.md)正式核心阅读与五条书面检查。349条目录保持，150项核心三遍、152项书面；199项尚未确认核心三遍（含资源）。没有删除文件、下载权重/大数据或运行学习模型；以下结果来自原文，KL检查为解析代数。

## 来源与问题定位

[NeurIPS2024正式会议页](https://proceedings.neurips.cc/paper_files/paper/2024/hash/2aee1c4159e48407d68fe16ae8e6e49e-Abstract-Conference.html)确认主会身份；本批读[正式45页论文与附录](https://proceedings.neurips.cc/paper_files/paper/2024/file/2aee1c4159e48407d68fe16ae8e6e49e-Paper-Conference.pdf)，核心§1–5、AppA–F的指定全文范围见精读。实际看过p3 Fig2、p8 Table1、p16/17定理与p20证明页。arXiv当前页列v4/2024-12-10，本次理论错误针对正式论文集版本，未核v4是否修订相应公式。仓库引用year2025不改变NeurIPS2024会议身份。

连续序列的teacher forcing只依赖干净真实历史，生成误差会累积；整段扩散更容易作轨迹引导，却常绑定固定窗口与同步噪声。作者把时间t和噪声k作为两个独立轴：每个token随机采自己的噪声级，因果网络学习从各种可靠程度的历史预测。AR-Diffusion/Rolling Diffusion已有按位置变化噪声先例；本文的独立噪声及其采样自由度须与它们比较。

## 方法如何运行、为什么可能有效

实际Fig2与Alg1/2对应以下流程：逐时刻给干净token加噪，输入上一隐状态z、当前噪声token和k，转移/观察头预测净token及下一z。采样时从白噪声序列出发，按二维矩阵K逐行、逐时刻去噪；近期可以先变干净，远期保留更多不确定性。视频U-Net/空间隐状态/GRU，非图像ResMLP/GRU；隐状态是学到的预测摘要，不能直接当真实物理状态或精确后验。

| 机制 | 当前论文中的作用 | 需要保留的条件 |
| --- | --- | --- |
| 独立噪声训练 | 覆盖多种噪声历史/未来组合，允许改采样调度 | 训练覆盖不等有限模型每个条件均学准 |
| 小噪声历史 | 保留较不可靠的历史状态，缓解把自身生成当真值 | 噪声也可能损坏精确字符/细笔画身份 |
| pyramid调度 | 近期动作较确定、远期仍可变化 | 调度与误差/目标梯度需任务匹配 |
| MCG | 从同一近期状态采多个模型未来并平均引导梯度 | 增加计算；模型未来期望不等真实环境最优期望 |
| 真实观测回写 | 执行动作后以实测状态更新隐状态 | 模型状态—动作一致性仍需执行验证 |

B1 fused-SNR把当前与历史信号强度组合为启发式权重，作者称对视频有效、非图像未见加速；它没有独立证明所有序列的最优重加权。B3视频用v目标、规划/模仿x0，不能把正文统一epsilon伪码当全部实际训练目标。

## 理论附录的具体错误与保证范围

正式p20 AppA.2 Part2将正向过程下的log密度比期望写成正的KL。对给定的高噪声条件，令q为较干净变量的后验、p为逆向模型，标准定义给出：

\[
D_{\mathrm{KL}}(q\|p)=\int q(y)\log\frac{q(y)}{p(y)}dy,
\qquad E_q\log\frac{p(y)}{q(y)}=-D_{\mathrm{KL}}(q\|p).
\]

原式为正号。取q=N(0,1)、p=N(1,1)，log(p/q)=y−1/2，所以其q期望为−1/2，而KL为+1/2。该反例直接针对p20的等式；已核实际PDF，排除了仅为文本抽取丢负号的解释。p16/17 TheoremA1/A3及CorollaryA2也把正KL/正MSE置于似然下界一侧，不能按印刷式直接解释为“减小loss即增大该下界”。

这里没有完成整套修正定理与所有索引/边界的重新证明；也没有由这处错误推断独立噪声训练的经验结果无效。可学习的是noise-as-masking与条件扩散的统一思路；引用理论保证时必须给出正确的负KL方向，并单列尚未完成的修订推导。

此外，A1.1/1.2关于不同噪声组合同时最优的论证依赖足够表达的模型、隐状态足以保留历史，以及能同时优化相应项。作者自己说明固定噪声序列的目标未必直接由训练loss下界，只在这些理想条件下建立代理联系。它不证明有限RNN在任意长序列无误差；“所有子序列”也不等训练分布外所有新文字/新笔顺。理论与实验应分别评价。

## 各任务证据及实际限制

| 任务 | 数据/条件与已读结果 | 能支持的范围 |
| --- | --- | --- |
| 视频 | TECO Minecraft128²/72帧、DMLab64²；约10%子序列、弃动作。同RNN比较teacher-forced next-frame diffusion/causal full-sequence；主图至1000帧，E3称试过2000帧 | 有限场景的定性长滚动/一致性；无标准FVD主量表、无无限稳定定理 |
| 规划 | D4RL三maze固定goal/随机goal六环境；DF单/多平均reward141.7/146.2 vsDiffuser119.5/129.4 | 作者报告平均优势；Multi2D U-Maze119.1±4.0低于128.9±1.8，正文“all6更优”不成立 |
| MCG消融 | 去MCG单/多均值129.67/127.7，六行均低于完整方法 | 支持该配置下MCG有用；缺同NFE/墙钟的多未来替代对照 |
| 机器人 | 150条VR遥操Franka、双相机/6DoF、两初始果位；500–600步下采样40帧、每帧15动作。success80%，扰动76%，next-frame扰动48% | 记忆/不可靠观测的任务先例；试验N/CI及同预算有记忆对照未完整给 |
| 时间序列 | GluonTS六集、100采样/19分位CRPSsum↓，五种子均值±std | 通用概率序列能力；跨维求和好不保证每一维都好，也不证明因果结构 |

机器人80→76下降4个百分点。论文checklist称量化结果都有均值/std，但正文机器人比例缺明确试验N与误差条；不能由该自述补齐。时序DF的Solar .289/Electricity .023/Wikipedia .085均高于TimeGrad .287/.021/.049，不能写所有任务胜过TimeGrad或全面SOTA。Exchange/Traffic/Taxi分别.003/.040/.075则有优势。完整六集及基线见精读。

Maze Table1为标准化episode reward，可以超过100；它不等成功率。B8指出奖励会奖励靠近目标后的停留，而离线数据只包含经过目标的轨迹；first-hit时间、碰墙率和路径效率更能补充目标达成，但原文未给完整对应新量表。Diffuser使用PD控制器与直接执行生成动作差异很大，应分别比较；不能将手工控制优势/劣势都归于训练噪声。

## 实验条件与版本不能混用

正式B10：视频8A100/fp16、50K步、batch8×16，约40K/12h收敛；其他单2080Ti11GB，多50–100K步/4–8h，maze/composition b2048、imitation b32。K1000、DDIM视频100步/其他50步，stack DMLab4/Minecraft8/maze10。F1说DMLab48帧，但E3/Fig10及代码配置36帧；保留原差异，不能静默选一个当所有实验条件。

官方[paper分支固定dd65516…](https://github.com/buoyancy99/diffusion-forcing/tree/dd65516a470b0eda08dcc0f9cb55c87d6527eb9e)提供原研究代码、mini数据/Drive checkpoint入口（本次未下载）、机器人控制代码按请求提供。公开README/配置和指定代码段已读：AdamW、手动warmup；视频默认β(.9,.99)、wd.002/warmup5000、v目标/fused-SNR；Minecraft recipe stack8/netsize64/cum-SNR.96/lr2e-4。DMLab命令设num_gru_layers=0，而B2统一描述GRU；内部全部构造尚未逐项审计。

论文数值建议guidance8–12，网站展示建议.1–1，展示参数与主表参数不同。video类将FVD设None、FID/LPIPS默认关闭，虽有其他日志，不可据代码存在指标接口就宣称论文已报FVD。时序类按最小CRPS记录；E1写6轮未改善早停，B9却写未increased，具体callback未全审，不自行恢复成已确认执行协议。

官方[main固定475e0bc… README](https://github.com/buoyancy99/diffusion-forcing/blob/475e0bcab87545e48b24b39fb46a81fe59d80594/README.md)说明已为v1.5 temporal-attention重实现；长滚动需要滑窗，MCG/部分任务未全部重做，maze目标/评价也改了。它不能替代原RNN论文条件。项目页后来加入Wan2.1/History-Guided Video Diffusion，属于后续工作，未追溯记成2024训练结果。

## 研究假设与写法学习

可检验的假设是：若主要误差来自历史可靠性，独立噪声与小噪声历史能改善跨步预测；若远期目标可微且模型未来足够可靠，MCG能在同预算下改善动作。建议同骨干交叉训练目标、fused-SNR、stack与历史噪声；同NFE/墙钟比较多未来方法。报告随长度变化的状态/字符身份、严格笔事件/方向、视觉质量和真实执行；全部未运行。

D05 Self Forcing、D06 Self Gradient Forcing已为相关训练偏差/长滚动前作；[History-Guided Video Diffusion正式ICML2025](https://proceedings.mlr.press/v267/song25b.html)已定位到原始论文入口，待下一批全文阅读。不能把“小噪声历史”“用自生成历史”“长视频”本身直接当新课题。

本论文值得学习的思路是从两类序列范式的具体限制，抽象成时刻×噪声两个轴，再按采样能力组织不同任务的实验。Introduction中的统一视角、Method的算法与调度、实验的能力分解有参考价值；Claim仍须回到每任务/每基线/每分母。Limitations应公开规模、奖励、误差统计、版本和理论式问题，顶会身份不能替代逐式逐表审查。
