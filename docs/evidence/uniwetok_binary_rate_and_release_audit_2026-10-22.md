# UniWeTok：二进制表示、成本口径与发布范围

第一百一十七批完成[L101](../reviews/L101.md)固定v3核心三遍和五项书面记录。[结构化审查](../../data/uniwetok_binary_rate_and_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），226核心/229书面含未通过项，131条未确认核心（含资源）。没有新增目录、删除文件、下载权重或执行模型。

## 来源与任务定位

固定[2602.14178v3](https://arxiv.org/abs/2602.14178v3)，2026-03-11，完整29页；Abstract/§1–5、Eq1–9、T1–13全部行、附录A/B研究文字与T14–33全部配置、C图注已读。实际核PDF p4框架F2/Eq1/2、p6课程F4、p8 T1–5、p10 T8/9、p11 T10/11、p12 T12/13、p21结构F5。参考文献未逐篇，其他定性图未逐图。未从正式发表源核到会场。

任务为静态图像重建/理解、文本生图和编辑，没有文字视频、真实笔顺或动作实验。论文统一预训后分别微调Gen/Edit/Chat；表11–13展示三个变体，不能据此宣称同一检查点或训练目标全指标正协同。公开共用仓库的BitDance NeurIPS2026消息指向2602.14041，不能移给UniWeTok。

## 机制与理论边界

Conv下采样同时扩channel，Transformer全局处理；g16×每组8bit做sign/STE，隐式组合空间2^128，未显式存储如此多embedding。量化前后各attentionpool对齐冻结SigLIP2-SO400M16-384全局向量；8.6M BitDance-T以query+shifted序列做next-token diffusion MSE，鼓励token可预测性。decoder将高斯noise与binary码concat，F5和公开uni文件一致；重建指标还受decoder随机性影响。

Eq9的SigLu为`−tanh(x/2)`，有限输入落在(−1,1)；公开uni分支用`2*sigmoid(x)−1=+tanh(x/2)`。符号差异可由权重/码约定吸收，需要核checkpoint和训练配置，不能仅凭符号判失败。有界和偏好端点不足以推出entropy与commitment两个函数或梯度严格等价；论文未给足q的温度、分布和证明，保留主张的适用边界。

“64 tokens”指64空间位置，每位置128bit。名义未熵编码表示为64×128=8192bit；256位置、16384词表的对照为256×14=3584bit。这个例子说明位置数与名义bits可能反向，不是对实际压缩文件大小的测量。T8的100%usage若解释为完整2^128组合覆盖，在50K×64位置中不可能实现；可能涉及组/bit统计，定义需补。组覆盖和联合熵、有效语义信息也不能互换。

T9的33B和REPA262B均按各自位置token口径。按每图64/256位置反推约.516B/1.023B图像曝光，只约2倍差；数据四舍五入、参数1.0B/675M、预训teacher/tokenizer和diffusion head成本仍不同。不能把33/262直接解释成全训练算力/卡时降至八分之一，也不能把64 AR位置当全系统64次简单softmax。

## 完整主表与消融结论

| 表 | 可采信结论与反例 |
| --- | --- |
| T8/9 | IN重建rFID.79与GigaTok.79并列、PSNR23.26；类别B/L/H FID2.35/1.68/1.38。H的IS284.34低于REPA305.7、precision.80低于OpenMAGVIT2 .84；FID优势有指标边界 |
| T10 | DC resize256 COCO rFID6.18/IN1.18；原尺寸COCO6.46差于WeTok16的5.30、IN1.25差于.81。resize IN PSNR22.97低于QLIP-L25.36，不能写所有分辨率/指标最优 |
| T11 | GenEval.81与SANA1.5同，DPG86.63；count.43低于SANA.86/JanusPro.59，position.78低于JanusPro.79。表中无FLUX行，83.84比较只见Abstract/Intro叙述 |
| T12 | Chat SEED69.3/MMMU40，TextVQA53.7低于Emu364.7，Chart65.1低于68.6，POPE85.6低于Harmon87.6，另有专用模型更高 |
| T13 | Edit EN语义5.86/感知5.89/overall5.09，CN5.78/5.92/5.11。ENoverall略高OmniGen5.06，但语义低于5.96、感知相同；低于BAGEL6.52/Step1X6.70 |
| T1/5 | PPD使gFID2.38→2.66、rFID1.33→1.12；加GAP gFID2.35、rFID1.18、PSNR22.27/SSIM.63下降。T5无query3.89、有query2.38，与T1完整配置2.35差异保留 |
| T2/3/4 | T2无SigLu pre55.26、post.10，加SigLu post41.51；T3有SigLu preonly.10/post41.51/both51.32。App配置说明有SigLu差异，但读出位置未齐，不能直接判表错。double使top39.45→46.89，为7.44个百分点 |
| T6/7/F4 | attention较linear rFID2.91→3.10变差；b128→1024分类4.09→11.69也增加8倍等步样本曝光。Hybrid rFID1.35/top35.41较强，PSNR22.54低于CNN22.56，Alex LPIPS.13差于.12。三阶段F4仅展示少量重建样例，没有独立OCR分层统计 |

## 条件与公开制品

IN消融正文250K步，App T14–33为250250；Adamβ.5/.9、wd0、lr1e-4 constant、warm0、EMA，256² randomcrop、g16/d′8/ch128。多数配置2resblock/16attention/global128；DC后组1024。T29标题bs1024但内容global128，T30内容1024，按单元值记录。IN T8重建.79与DC T10的1.18来自不同训练，不合并成一个检查点。三阶段后两阶段的完整数据/步数、人脸/文字敏感域名单、MLLM混合规模/卡时/采样预算仍缺；不能用引用论文或另一模型示例填空。

固定[GitHub59f56e67](https://github.com/shallowdream204/BitDance/tree/59f56e67ebd03e030755399351b3173a74f6351b)，完整84项树定位，读UniWeTok README全文、root主要方法/发布/训练/评测段、ImageNet README全文。选读autoencoder_uni编码/解码、noise和激活，GFQ entropy/STE，以及公共MLLM/pipeline imports。完整MLLM/attention/head未全读。

UniWeTok README的HF collection入口本次返回404，作者公开模型列表未出现UniWeTok命名；这不能证明其他名字或渠道没有制品。HF [BitDance-Tokenizer固定2d4e8863](https://huggingface.co/shallowdream204/BitDance-Tokenizer/tree/2d4e88636e9513340de60065c0dbfa1a6e7ac2e7)确有d16c32/d32c128/d32c256三个权重文件及配置，已读卡片/配置/metadata，未下载权重。d32c128配置128channel、chmult六级、4resblock，与消融配方2resblock不同，不能直接作T8/10精确checkpoint。模型卡自称BitDance tokenizer；对应关系需补。

公开MLLM和T2I pipeline import的是`autoencoder.py`，没有自动接入`autoencoder_uni.py`。ImageNet脚本和权重列表用d16c32、256位置和BitDance FID1.24等，与UniWeTok-H64位置/1.38不同。`scripts/train.sh`只有TODO；现有14B配置不构成本作8B完整训练入口。各类资源已记录在本条release审查，未虚增为独立论文。BitDance2602.14041和WeTok2508.05599保留待追读来源。

## 假设检验与写作学习

优势假设应限定固定总bits、teacher/encoder、数据曝光和总FLOPs下的语义/重建/可生成Pareto。建议做PPD×GAP×query×SigLu、多seed与真实q/H统计；同时比较等总步/等图像曝光、同checkpoint联合/独立SFT，固定原始与重写prompt、AR/head/decoder噪声预算。细字最小差、非汉字和人工OCR需独立测试；书写时序另需真实接触/墨迹事件GT。上述实验未运行，新颖性尚需追引。

Introduction三瓶颈、Method逐模块/总loss、App逐消融配方的对应组织值得学习。Claim保留自然分辨率退步、count弱项和独立微调变体；无单列Limitations，读者审查需补完整成本、usage/等价性定义、实现对应与时序未测范围。
