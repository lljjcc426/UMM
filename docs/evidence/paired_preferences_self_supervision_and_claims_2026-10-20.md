# 配对偏好、自监督与协同主张：第十七批

2026-10-20；L127–L133七项存量研究。245份笔记，章节259/摘要33/历史待核40。10项五项书面检查，完整三遍验收0、独立复现0，无删除文件。

## 最关键的版本与方法差异

| 研究 | 原文/代码证据 | 可支持的结论 |
| --- | --- | --- |
| [HermesFlow/L127](../reviews/L127.md) | NeurIPS正式Show-o GenEval.64，v2为.53；最终均.69；生成DPO.70 | 正式增幅为.05，Pair侧重取舍；不能沿用旧增幅或声称每项胜DPO |
| [MindOmni/L128](../reviews/L128.md) | 基础GenEval.81/DPG83.0/WISE.60；加高质数据*.83/82.5/.71 | 星号版增益混额外数据，DPG有下降；推理/参数/解码成本另计 |
| [CoRL/L129](../reviews/L129.md) | 联合RL→T2I/MC/OE refined阶段 | 联合初始化有用，最终分支是否同checkpoint需核；真实图/QA仍属监督 |
| [PairUni/L130](../reviews/L130.md) | Janus/Lumina用RL，BAGEL用SFT；加权GenEval1B均.79/7B均.85 | BAGEL支持数据配对迁移，无法证明PairGRPO；加权主要改善部分理解指标 |
| [UniCorn/L131](../reviews/L131.md) | 自采样/拒绝筛选+GCJR SFT；MME/MMB下降，MMMU/MMVP升 | 保持理解的大体水平需要逐项报告，不能表述普遍双向提升 |
| [R3/L132](../reviews/L132.md) | treeRL Reason+Reflect/Refine；训练与评测按基准另配 | 支持相关生成域的理解提升；多轮终图与实时书写过程需分开 |
| [GvU/L133](../reviews/L133.md) | prompt条件概率reward；多数常规理解项略降，MMT仅+.16 | 生成改善成立于报告范围；不能说理解全面增强 |

## HermesFlow公式/实现交叉审查

[NeurIPS正式版](https://proceedings.neurips.cc/paper_files/paper/2025/file/59d4e18a60490b9ed9913f3be2b14839-Paper-Conference.pdf)第15页Eq12/15及arXivv2第13页将两log-sigmoid之和改写为偏好差乘积的log-sigmoid，等式一般不成立。取a=b=0即可得到−2log2与−log2的差异；乘积还偏好双负，πθ=πref且确定同mask时零初始差使乘积目标一阶梯度为0。

[官方4997368代码](https://github.com/Gen-Verse/HermesFlow/blob/4997368578b4548cdcc6622a71b2d109f11a51c5/training/train_pairdpo.py)549–554行实际分别算两DPO再加权。公式问题不能直接推论代码训练失败。公开YAML50Ksteps/b1/warm5K与正文3K/b4不同，尚无运行日志对齐。正式Table6 MME-Unify总分提高但MITIU下降，反映协同需分项。

## 理论条件与裁判效度

UniCorn PDF第19/20页AppC Eq6将中间图I称latent，却遗漏求和/积分；右侧是特定I的联合项，不能直接等于I*边缘概率。互信息/Bayes恒等式无法单独证明共享参数四任务全部NLL下降；flowMSE与精确像素NLL亦需额外关系。保留其经验结果，限制理论保证。

MindOmni PDF第7页确以Var而非std归一，低方差组会有不同梯度尺度，实际稳定处理需代码。PairUni称sqrt放大高相似分数差异，与[.6,1]上平方根的压缩性质不符；其经验比较可独立评估。

GvU的reward是整段token概率几何均值，含语言先验。代码gvu_score使用no_grad，不意味着参数永久冻结；环境锁定PEFT0.17.1，其[官方定义](https://github.com/huggingface/peft/blob/v0.17.1/src/peft/peft_model.py)是@contextmanager。trainer482裸调用仅创建上下文对象，未执行禁用主体；标准PEFT路径仍带当前LoRA，433参考分支则正确使用with。不能记录成冻结base裁判，尚未运行验证其他路径。自评reward和独立人评/空间事件/文字次序之间尚有未证实的效度关系。

## 与书写/绘画视频的实验衔接

1. 先固定候选池检验理解裁判能否识别漏笔、错字、逆序、覆盖、重复笔和物理不执行；终帧OCR不能测完整事件。
2. 相同样本集合只改变配对关系，固定各任务token/图像曝光/候选生成成本；分别检验数据配对、loss及结构，不把增数据和更新规则混为单一机制。
3. 将生成器/裁判交叉冻结测试，自身闭环、一致性与外部正确性分开；错图/无图/字符重排对照检验语言先验和奖励投机。
4. 多轮编辑比较等NFE/延迟best-of-N与外部裁判；记录原图保留、停止误判及过程方向，不把编辑中间图当书写视频。
5. 分别报每项理解遗忘和生成收益、多seed/置信区间/Pareto；历史基线、正式版、改写提示和额外训练数据保持版本绑定。

## 尚未完成

其余正文/附录/图/代码仍有未读项，单篇笔记逐项列出。CoRL最终权重、PairUni数据GenEval来源/阈值口径、GvU完整运行链及MindOmni完整RL条件需继续核。本批没有运行模型、下载权重或宣称全领域零遗漏。
