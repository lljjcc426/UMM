# LaVIT：动态视觉token、候选筛选和公开模型版本

第七十九批补完[L079](../reviews/L079.md)明确范围核心三遍与五项书面检查。350条目录，167项核心三遍/170项五条书面记录（含未通过项），183条尚未确认核心三遍（含资源）。无新增独立论文、文件删除、权重下载或模型执行。

## 原始证据与实际方法

采用[ICLR2024正式题录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e1762b64958760f7bfabe3a7062d007f-Abstract-Conference.html)及[21页PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/e1762b64958760f7bfabe3a7062d007f-Paper-Conference.pdf)，核完核心、指定附录及实际p4 F3/p5公式/p7 T1–2/p9 T3。全文七字段、五个分析问题、写作学习和验收详单篇。

冻结EVA-CLIP ViT-G/14，Gumbel selector决定保留patch；12层causal merger仍cross-attend未保留patch，训练16384语义码本和12层重建decoder。rho1/3、cosine语义重建和保留率正则lambda2；LLaMA1-7B预测图文离散目标，另调SD1.5 UNet还原像素。

理解路径实际输入连续merger特征，离散视觉码用作预测监督。全图ViT和未选patch已经包含整图信息，causal selfattention无法独立赋予真实书写时间语义。输入、监督目标与输出表示要分别说明，不能从摘要概述填成全系统输入均离散。

Eq3将l2写作norm，固定实现是F.normalize；这支持归一化意图，未核权重训练过程每步范数。Eq6把概率p(y)写成整个数据集log条件和，Eq5范数未写平方；保留记号疑点，不能自行修补后宣称作者用的目标。

## 正式结果及实验条件

| 证据 | 数值和条件 | 可支持范围 |
| --- | --- | --- |
| T1理解 | NoCaps114.2/Flickr83/VQA66/OK54.6/GQA46.8/VizWiz38.5 | 高于此表有值基线；异backbone/数据/prompt不隔离统一目标的因果作用 |
| T2 COCO30K FID | 7.4，AppA每prompt四样本CLIP选一 | 低于表内其他LLM，高于Imagen7.3/Parti7.2；需同候选预算比较 |
| T3a分类/回归 | Flickr73.2 vs60.4，VQA57.1 vs53.6，OK47.0 vs41.9 | 支持自家小encoder/数据子集配方，不能当完整Emu同预算复现 |
| T3b动态/固定 | 94token/18h vs256token/30h；Flickr74 vs71.1 | 时长减少40%，不表示任意端到端系统恒定加速40% |
| AppB语言保持 | MMLU35.1→27.1/30.9/33.6，随lr/文本比例变化 | 最佳公开配方仍降1.5分，未完全消除遗忘 |

T6 causal优于bidirectional；T7连续优于量化输入，解冻LLM优于冻结；T8 merger优于直接丢弃。各表CLIP-L/14消融与主模型EVA-G不同，各表略不同数值不拼为一套配置。缺完整生成/理解同预算正迁移、细笔保真和多seed曲线。

主LLM20K步/b2048/256A100约30h，tokenizer50K步/b2048/64A100约12h，UNet另20K步；其余优化器/lr/bf16/采样详笔记。93M理解+额外100M生成是数据来源容量，不能直接当全量唯一消耗。LaVIT正文称Emu2.6B图文/3.8B网页数据，与[Emu正式文](https://proceedings.iclr.cc/paper_files/paper/2024/file/34d5143080c89a7ce10932c8c5e1907f-Paper-Conference.pdf)报告82M实际样本/150Btokens的单位和口径不同；不据此算实耗优势。

## 固定代码解决k300歧义，公开权重另有版本差异

[官方固定8cde9b4f](https://github.com/jy0205/LaVIT/tree/8cde9b4f9d24e077db9e740f3740daba15428e8d/LaVIT)、[HF v2固定b6173182](https://huggingface.co/rain1011/LaVIT-7B-v2/tree/b61731821e79e43e84a43e063660deb1bce7a9aa)的静态阅读见[制品JSON](../../data/lavit_version_and_sampling_audit_2026-10-21.json)。

- 正式AppA“maximum sampled tokens k300”含糊，所查`evaluate_text2img.py`明确是top_k=300；未覆盖`generate_image(max_length=200)`，后者传给max_new_tokens。二者含义不同。
- 该评估取DDIM50、LLM/decoder CFG均1.5、四张CLIP-ViT-L/14选一、低分辨率分支512²、seed0+rank；默认demo或高分辨率版本不能填入原主表。
- `encode_features`用于理解连续特征，`tokenize_image`用于离散码；两条推理路径均有hard Gumbel随机选择，需测同图多seed稳定性。图像全局语义压缩不能自动保证细笔/OCR。
- 原文LLaMA1；README说明因其许可限制公开LLaMA2权重。v2另用20M重写caption的LAIONaesthetics+4.2M JourneyDB、8K步继续调LLM，并有新高分辨率decoder。它是配套后续模型研究，未另计论文。
- 固定README的LLaMA2-v1→v2 FID7.2→7.1，但NoCaps113.1→112、Flickr83.2→81.4、GQA48→47.9、VizWiz45.3→41，VQA68.2→68.3/OK55.7→55.9稍升。生成改善伴随部分理解退步；跨版本数据/权重变化，尚无因果归因或独立重跑。
- HF配置32层/4096hidden/2048positions/vocab48386，许可标llama2；README finetuning代码尚未勾选。元数据和推理制品不构成原LLaMA1训练全协议。

## 研究假设、验证与写作学习

可检验假设：在语义冗余且高层理解为主的分布上，动态token减少LLM输入长度，merger减少直接丢信息，离散分类改善简单确定性回归的多峰不足。验证需同教师/样本曝光/总FLOPs、固定/动态等码率、连续分布模型和简单L2分开、同时报OCR/细笔最小对/语言保持与生成质量。

将单样本与4选1拆开，计算tokenizer、AR、扩散和CLIP筛选全部成本；固定原LLaMA1与公开LLaMA2 v1/v2各组，控制额外数据和继续训练，重复Gumbel/采样seed。规范笔顺另需事件/方向/停笔监督与可观测RGB序列，不从静态token预测推出。以上实验未运行，未做新颖性闭环。

可学Introduction将两个明确不足映射到机制，Method按tokenizer—LM—像素decoder组织，附录将lr/文本混合与遗忘关联。Claim须保留输入连续/目标离散、四候选预算、版本变化和退步项；Limitations以表示瓶颈、短caption域偏移、训练协议与制品可用性为依据。
