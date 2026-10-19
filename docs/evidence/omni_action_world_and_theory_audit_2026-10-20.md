# 全模态、动作世界与理论论证审查

2026-10-20，L161–L168八项存量；各自七字段、实验条件/反证/写作分析见[逐篇索引](../reviews/README.md)。无模型执行，无文件删除。章节阅读数量不代表全文/三遍完成。

## 接口决定可声称的能力

| 系统 | 已读证据中的输出 | 与研究问题的关系 |
| --- | --- | --- |
| Ming-Flash-Omni | 文、静态图/编辑/分割、音频 | Video主要输入；Glyph-byT5服务静态文字，需预提取字符串 |
| LongCat-Flash-Omni | 文、语音 | 2FPS视频输入与压缩不保证短事件可观测，无图视频解码输出 |
| ERNIE5 | 文、图、视频、音频 | 图/视频next-frame-and-scale后有独立扩散refiner；VBench含真实视频生成量化 |
| MUNI | 图/文/音子集条件与共生成 | 共享语义latent与随机decoder，不是帧时序模型 |
| BagelVLA | 子任务文字、未来关键帧、动作块 | 第三动作专家；少步条件不要求完整未来图已生成 |
| WorldBagel | 动作块及动作条件未来观测 | 两BAGEL专家与Fourier头；动作开环执行 |
| SenseNova-Vision | CV结构文字、mask/几何图、混合输出 | scribble条件分割不能改称素描过程生成 |
| Puffin-World | camera文字、多视图RGB/depth | 物理锚为相机/重力几何，未建笔尖接触动力学 |

ERNIE GenEval90.1低于QwenImage91.0；VBench语义83.40高于Veo3 82.49，但整体84.20低于85.06。SenseNova MMVP83.3→79.0下降、GenEval.82→.85提升。所有数字按作者表报告，不能统一写“能力无损且全面领先”。

## WorldBagel定理4的可核验反例

来源：[arXivv1](https://arxiv.org/pdf/2607.03461v1) PDFp24，AppA4 Eq23–28，已渲染视觉核。以下是本次解析分析，不是作者承认或代码运行结论。

定理声称，对紧集A包含于[-1,1]的任意连续f，总存在K及w，使仅由sin(2^kπa)、cos(2^kπa)组成的线性组合任意一致逼近f。取其允许的A=[-1,1]及f(a)=1。

每一个上述非零整数频率基函数在[-1,1]积分均为0，因此任意有限线性组合g也满足积分g=0，而积分f=2。由积分绝对值不超过区间长度乘sup误差，有2=|积分(f−g)|≤2 sup|f−g|，故sup误差≥1。定理按当前印刷形式不成立。

证明引用完整三角多项式（包含常数和所有整数频率），随后把它写成给定指数频率特征的线性组合，这一步不成立。即使补DC，也不能仅凭完整三角多项式的稠密性推出缺失频率集合的结论。

该反例限制论文的线性通用逼近论证，不足以否定非线性动作头或实验成功率。表2的98.0%仍按作者报告保留；需要同容量、同数据、不同频率及数值精度比较。相位反解的局部稳定与全域无条件稳定也须区分，不能略去branch条件。

## MUNI的证明范围

MUNI AppB通过总相关/条件互信息描述充分latent，只对full或leave-one-out路线证明coherence-sufficiency。依赖总体风险、可表达/理想优化、足够小prior权重，以及prior最优成本与保留互信息的严格排序。对flow/diffusion prior，排序是额外假设；有限优化不自动满足。

现实图音文实验训练只有pair，多条件评测用FLUX合成triplet；两两CLIP/CLAP/AIS对齐不能唯一确定完整联合。需要真实triplet、高阶相关和假设破坏实验，不能把理想命题写成实际训练保证。

## 时延、资源与公开配置

BagelVLA主速度例1.2s/chunk48对应40动作/秒，是吞吐。异步72Hz可复用较旧视觉KV，需另报新观测到动作延迟和视觉刷新。CALVIN单view消融与主双view表分开，4.405和3.600不混用。LongCat的100ms首包在600–700ms端点检测之后，不是说话结束到音频全链路100ms。

[SenseNova固定launcher](https://github.com/OpenSenseNova/SenseNova-Vision/blob/4366e0e1f4d22d2207ecc8e339f886b765ba876e/scripts/train_cv_unify.sh)默认total_steps200000、max_num_tokens_per_sample24064、CEweight.25/tshift4；论文50K/32Ksample，两套协议分别记录。YAML提供24类任务权重，例如VLM/T2I各1.5、pose1.56，这些是未归一权重。代码未运行，完整采样实现未追。

[数据卡](https://huggingface.co/datasets/sensenova/SenseNova-Vision-Corpus-50M/blob/03dd7edfa27ee8bf6b20f91b6861cc2ba06bfd18/README.md)的50M为frame/任务样本，发布JSONL及派生资产，源RGB按相对路径另取；viewer的三组300条是展示配置，不能等价全部数据。官方demo推荐A80080GB、报告单请求38226MiB，仅为作者验证例，不是本次实测或全部任务显存上界。

Puffin-World主文jointappearance/geometry，当前README StageIV还注明rgb_blind_to_depth非对称attention；完整mask实现待核，不能只凭“联合”认定两支双向可见。自身感知生成camera标签/评价camera会有共同误差，需独立真值；规则深度颜色可逆也不保证经VAE后数值无损。

历史初次相关章节核查标记至此清零，33条摘要、5份第一遍、全部笔记未读范围和完整三遍仍继续办理。未宣称全领域零遗漏。
