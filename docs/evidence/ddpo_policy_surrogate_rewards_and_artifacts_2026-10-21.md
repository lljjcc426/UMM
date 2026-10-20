# DDPO：策略代理、奖励效用与公开制品

第七十二批完成[L185 DDPO](../reviews/L185.md)核心三遍与具体书面检查。350目录、155核心/157书面，195条未确认核心三遍（含资源）；无新增独立论文或文件删除，无模型复现。

## 原文与问题定义

[ICLR2024正式论文](https://proceedings.iclr.cc/paper_files/paper/2024/hash/14f75513f0f1ca01de1e826b52e6b840-Abstract-Conference.html)与[作者项目](https://rl-diffusion.github.io/)已核。核心§1–7、AppA–F、实际Fig2/3/4/7/10/11/12及T1已审指定范围；G全部样本未逐张判断。此前“未逐点核曲线”的缺项现以实际PDF补上，未伪造图中没有标注的精确终点数值。

作者从“最大化图像似然不等于满足下游目标”提出黑盒奖励优化。RWR以最终图的加权去噪近似处理问题；DDPO把中间去噪纳入MDP，令终端奖励对应整条轨迹的回报。它承认Fan/Lee等生成策略前作与DPOK并行研究，不可概括为首次扩散RL。

## 方法与理论适用条件

状态是prompt、扩散时刻和带噪latent，动作是下一latent，环境搬运该动作并递减时刻。冻结SD1.4文字encoder/VAE，主实验更新UNet；图像输出后计算JPEG、美学或LLaVA描述+BERTScore Recall，再更新。真实落笔/抬笔没有进入状态/动作监督。

在正方差高斯采样器下，每步转移密度可精确求值；on-policy SF可用$E[\sum_t\nabla\log p_\theta(a_t|s_t)R]$。IS/PPO用旧轨迹多次更新、局部单步密度比和裁剪，是近策略代理。一般整条轨迹的无偏离策略转换还需轨迹密度比；仅换当前动作比不同时改变旧状态和后续回报分布。不能把“每步密度可算”扩大为“所有离策略更新均精确无偏”。逐prompt除以reward标准差也改变了各prompt的相对权重。

固定[JAX f0b6ca7](https://github.com/jannerm/ddpo/tree/f0b6ca76516809b9534ad51bd4511117e8eb3682)与[GPU/LoRA 1958463](https://github.com/kvablack/ddpo-pytorch/tree/1958463f020112c9a7bc85768d296daacc2e1b4b)代码均将逐坐标高斯logdensity取mean再用于PPO：

$$\bar\ell=\frac1d\sum_{j=1}^d\log p_j,\quad r_\mathrm{code}=e^{\bar\ell_\mathrm{new}-\bar\ell_\mathrm{old}}=(p_\mathrm{new}/p_\mathrm{old})^{1/d}.$$

这不是完整联合密度比。SF处若只差固定1/d可视作梯度缩放，但放进exp与PPO clipping后，不能整体当一个学习率常数。以典型4×64×64 latent的d=16384为条件示例，代码clip区间$1\pm10^{-4}$对应联合比阈值$(1\pm10^{-4})^{16384}$；这里只做代数分析，未执行模型比较效果。该实现可能有稳定性动机，现有读取材料未隔离该贡献。

JAX另只在算logdensity时对std加下限；torch所读函数直接使用std。eta=0或零方差端点不能原样声称普通高斯密度公式成立；公开alignment scheduler steps_offset=1/set_alpha_to_one=false，不能凭抽象零端点假设断言该公开checkpoint运行失败。本批未执行路径，不下运行故障结论。

## 实际图表与实验能支持什么

| 证据 | 已核观察 | 仍需限制 |
| --- | --- | --- |
| Fig4三奖励 | DDPO两变体比RWR更有效；美学IS更高，JPEG两者接近/后期趋同 | 横轴是rewardqueries，非FLOPs或墙钟；阴影来源/训练重复未明确 |
| Fig10 CFG训练 | RWR第一轮后无CFG退步，有CFG持续改善 | 支持此设置的训练/采样一致性，不是所有采样器通用定理 |
| Fig11 interleaving | RWR256–16384样本/轮，频繁交替先有益再退化，未追上DDPO | 每轮更数固定使同query总更新数变化，未完全等计算 |
| Fig12泛化 | 新38动物接近训练45动物，50物体改善更弱 | 仍是同奖励预测器；与Fig4初始分/范围不同，未解释差异，不能跨图拼值 |
| AppB T1 | wolf50样本5.95±.03→6.14±.05（Universal）/6.63±.03（DDPO20K） | 均值±1SE限单prompt，不等训练seed CI；不含训练成本的推理速度不可当全成本 |
| AppC DPOK | 作者报告四prompt优势 | SD1.5+LoRA/lr/多prompt训练/KL不同，DPOK数字取原文，非同条件独立复跑 |

正式主实验50步/CFG5、每轮256采样，SF一更/IS四更、AdamW1e-5/clip1e-4；RWR10K采样/400更。DDPO v4-64TPU与RWR v3-128TPU各约4h至50K，VLM另8 A10080GB。详见L185完整七字段；奖励查询预算不能代替计算公平。

## 奖励上涨和真实任务

实际Fig7展示：不可压缩奖励最终推动噪声化；计数prompt诱导写数字/文字，未生成正确数量动物。AppA说明定性图由人选退化前最后checkpoint。因此它证明了有效优化所定义奖励，同时展示奖励与任务效用可分离；不能将同一VLM的训练/评价当独立正确性证据。

书写视频若只用OCR终态/VLM caption，仍可能缺笔、换序、反向、在画面写答案或利用识别器风格偏好。需要独立事件标注/识别、人评和真实执行指标。AppC用另一美学预测器监测退化是有用设计，但两个代理也不等真实笔顺成功。

## 无独立论文的实现、模型卡和调参资源

torch README全文明确默认base只为快速启动、未承诺好结果；它默认SD1.5/LoRA/lr3e-4、每GPU batch1，低显存条件下约10GB。DGX recipe改为SD1.4：256采样/轮，压缩4更，美学2更且200epoch，alignment6训练GPU+2奖励GPU、288采样/轮/2更/200epoch。README的约4h/100epoch展示不能统一覆盖这些recipe，更不能与原全UNet TPU主实验混同。LoRA rank未在当前调用显式给出，不凭库默认记为已核值。

模型卡[美学3941662](https://huggingface.co/kvablack/ddpo-aesthetic/tree/3941662709c710c4c17bf6f0620613d9ac3cd7d2)是40轮×256=10240采样；[对齐23c5dc4](https://huggingface.co/kvablack/ddpo-alignment/tree/23c5dc41c49dbd9495759200dad1b8c6fd727d21)是200轮×256=51200。卡片全文、目录元信息与对齐scheduler已读，CreativeML OpenRAIL-M标签与代码MIT身份分列；这些制品关联现有论文，不另算新论文。未下载权重/运行训练，见[固定审查快照](../../data/ddpo_artifact_audit_2026-10-21.json)。

## 可证伪实验与研究写法

优势假设限可靠、可迁移、可评分随机轨迹和有用reward梯度的分布。固定底座/prompt与rollout、训练FLOPs、teacher墙钟，比较SF/IS/RWR和现有偏好优化；因子化采样频率、更数、sum/mean密度与clip重标定、KL/earlystop。独立测试严格笔事件、同终态错序/反向、数字文字捷径、罕见字与语言/书体留出、多样性和保真。以上均未运行，亦未把奖励漏洞直接当新颖课题，DPOK及后续RL须继续查新。

写作上学习先定义J/MDP，再推估计器，实验围绕优化、奖励、泛化三个问题；Claim必须区分优化代理与真实效用、理论与代码，Limitations明确选择检查点、统计/计算和宽分布边界。
