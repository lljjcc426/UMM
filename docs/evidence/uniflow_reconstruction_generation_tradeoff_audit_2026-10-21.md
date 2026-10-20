# UniFlow正式论文：重建、理解和生成的取舍

第八十批完成[L072](../reviews/L072.md)明确范围核心三遍与五项书面检查。350目录、168核心/171项五条书面记录（含未通过项），182条尚未确认核心三遍（含资源）。无新增论文、删除文件或模型复现。

依据[ICLR2026正式题录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/8882d370cdafec9885b918a8cfac642e-Abstract-Conference.html)和[32页正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/8882d370cdafec9885b918a8cfac642e-Paper-Conference.pdf)，补完核心/指定附录，实际核看p4框架公式、p7主表、p9消融与生成表、p32步数曲线。旧arXiv与旧表号仅作历史，七字段和五个分析问题详单篇。

## 方法的具体边界

冻结同初始化teacher，student以逐层cosine距离和深度先验分配蒸馏强度；最后层压64维接6层全局Transformer和12层patch级像素flow。它提供连续视觉tokenizer，下游理解用倒数第二层；生成实验分别训练MAR或SANA初始化的MMDiT。其patch flow沿加噪时间重建静态RGB，没有学习书写事件顺序。

正文x_t=(1−t)x+tε，目标ε−x，反向积分；固定代码采用反向时间约定并x+=dt*v，两者可以一致。HF明确num_sampling_steps=1会覆盖类默认100与decoder默认10。单步主张不能只据默认值否定，也不能扩展成整个生成流程一步：MAR另用256AR步。

## 主表中必须保留的反例

| 原始证据 | 结果及条件 | 支持范围 |
| --- | --- | --- |
| T1重建 | Intern rFID .26 vs UniTok .41；FLUX .18、SD-VAE3 .20更低 | 统一tokenizer组优势，未胜全部generative codec；各自native输入再缩256 |
| T2理解 | XL Avg79.09 vs73.04，高6.05综合分；MME-P1513.7<1551.1 | 平均先将两项MME各除20；异teacher/LLM/数据/尺寸，非相对6.05%或逐项最优 |
| T4类别生成 | 无CFG gFID2.45<同表MAR-VAE2.60；有CFG1.85>1.78 | 优势随采样条件变化，IS也有退步 |
| T6a蒸馏 | adaptive33.23/.26/1513.7；final33.41/.25/1435.6；uniform30.77/.45/1518.2 | 是取舍，adaptive非三个指标均最优 |
| F5a原teacher对照 | TextVQA−.28、MME-S−.20 | 小幅负迁移保留，未证明无损理解 |
| AppT15 | Intern rFID.26/gFID7.38；DINO .54/5.16 | 更好的重建FID不能推出更好的生成FID |

T3文生图另用SigLIP2-f16c32/40epochs+DINOlatent对齐、1M FLUX-Kera数据和125K额外训练/对齐步，不能把.65 GenEval/84.76 DPG归于单个不变tokenizer。视觉任务中分类为冻结linear probe；检测、深度和分割包含微调，须分别记录。

## 实验条件与公开制品

正文tokenizer全局batch512，AppT7–10写256，T14的70K步×512对应约36M曝光；批量冲突尚未解决。Intern原生448/1024patch，再缩到256评价，比原生256提供更多输入信息。正文SigLIP-L与AppSO400M也保留不一致。

固定[官方GH e6322d0](https://github.com/ZhengrongYue/UniFlow/tree/e6322d0b57bedbe7111a292104c6a07971fcfaea)、[HF e8288b98](https://huggingface.co/yuezhengrong/UniFlow/tree/e8288b984f2c0a60d5006e0d912b6150ba52865d)的推理模型/config/README、quick_start代码和文件树，见[制品核查](../../data/uniflow_decoder_and_protocol_audit_2026-10-21.json)。未发现原蒸馏训练、整套MLLM/MAR/MMDiT训练脚本；不等同正式实验可完整重跑。

quick_start实际输入center crop，指标目标却把整张图直接resize，非方图可能错位；SSIM给[0,1]浮点图设置data_range=2。此示例不应作为正式主表的评价协议。未执行该脚本、模型或速度测试。

F21实际含四encoder的PSNR随步数曲线，支持该实验中增加步数轻微降质；没有实测延迟曲线或多seed区间。条件分布近单点是作者解释，未估计条件分布或证明任意域均一步最优。F20是模拟权重图，不能当真实训练层权重统计。

## 可验证假设与写作学习

在强语义teacher、密集图像条件下，逐层约束有望保持语义、像素flow绕过冻结VAE、GTB补patch间一致性。验证需等原生输入/码率/总训练计算，比较蒸馏×解码器×loss的Pareto曲线，并固定下游LLM和生成器。补跨文字/细笔/OCR和遮挡实验，单独测多seed稳定性及完整端到端成本。

对笔顺研究，必须引入同终态不同事件过程与真实动作/RGB评价；给定视频逐帧重建无法验证书写时序。上述方案未运行，也未完成所有相关工作的新颖性排除。

Introduction和Method可学习将三类既有瓶颈映射到两个机制，再用模块消融检验。Claim需保留平均分单位、负迁移、有CFG退步和输入信息量；Limitations应说明公开训练边界、统计不确定性和文本细节域偏移。不能将定性例图或模拟曲线代入实测结论。
