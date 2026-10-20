# JanusFlow 与 Harmon：共享、解耦及协同收益的证据

第七十批补完[L086 JanusFlow](../reviews/L086.md)与[L092 Harmon](../reviews/L092.md)的正式核心三遍和五条书面检查。目录仍350条，153项核心三遍、155项书面；197项尚未确认核心三遍（含资源）。无文件删除、权重下载、模型执行或独立复现。原笔记的预印本阅读有价值，本批补上正式会场、真实框架/消融图、附录和固定公开实现。

## 版本、真实任务与研究逻辑

[JanusFlow CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/html/Ma_JanusFlow_Harmonizing_Autoregression_and_Rectified_Flow_for_Unified_Multimodal_Understanding_CVPR_2025_paper.html)，pp7739–7751；[Harmon ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/html/Wu_Harmonizing_Visual_Representations_for_Unified_Multimodal_Understanding_and_Generation_ICCV_2025_paper.html)，pp17739–17750。两篇正式OA与独立补充材料已读指定完整研究范围，表号按正式版修正：JanusFlow关键消融T5，Harmon编码器/阶段/分辨率T5/6/7。没有把新会场状态由预印本猜出。

| 比较项 | JanusFlow | Harmon |
| --- | --- | --- |
| 具体困难 | VQ重建瓶颈、语义理解与带噪连续预测冲突 | 重建encoder语义弱，解耦后共享/迁移不充分 |
| 新机制 | SigLIP与生成encoder解耦，LLM预测RF速度，REPA对齐中间特征 | 共享MAR encoder，LLM融合文字，MAR decoder和小扩散头预测masked latent |
| 真实输出 | 文字回答或静态384²图片 | 文字回答或静态图片，主最终512² |
| 底层压缩 | 冻结SDXL VAE | 仍有冻结VAE；正式图为简洁省略，supp明确说明 |
| 时间/顺序含义 | RF ODE的噪声输运时间 | 静态latent patches的unmask顺序 |
| 尚未验证 | 规范笔顺、真实RGB视频事件、共享UMM执行收益 | 同左；共享表示并未自动成为过程状态 |

JanusFlow的问题定义引向简洁的连续生成接口，并保留强语义encoder；Harmon先用ImageNet线性probe与特征响应说明生成预训MAR有语义，再设计共享架构。它们检验不同表示/预训练/损失配置，不能仅凭结论选出“共享必优”或“解耦必优”。

## 方法为什么可能有效、何时可能不适用

JanusFlow以SigLIP理解干净图像，生成侧将噪声latent经2×2 patchify与ConvNeXt送同一因果LLM，预测全部latent的速度，经Euler迭代再VAE解码。第6层特征通过3层MLP与干净SigLIP特征负余弦对齐，教师stop-grad；AR CE、RF速度MSE和REPA按1:1:1组合。它可能降低生成学习语义的难度，但对齐到不含细笔身份/动作的教师，也可能丢任务细节。RF去噪轨迹没有被监督为书写动作。

Harmon理解侧使用完整latent图、生成侧使用已见patch+buffer，两者共享MAR encoder；LLM输出送MAR decoder，再以其条件向量控制小MLP扩散头采新latent patch。它可能让语义理解监督改善生成的对象/属性，但仍受VAE可恢复信息与MAR预训练限制。空间生成顺序没有笔事件语义，复杂字的重建上限必须先测。

## 主结果和反例

JanusFlow主MJHQ FID30K9.51、GenEval.63、DPG80.09；正式T4相对Janus的MMB69.4→74.9、SEED63.7→70.5，但MME1338→1333.1、MMMU30.5→29.3、MM-Vet34.3→30.9。主表VILA-U384 FID7.69更低、DALLE3 GenEval.67和DPG83.50更高，不能声称全部领先。

正式supp特别说明基础LLM增强后多选理解已改善；这一先验变化与RF/REPA混杂。256²版本GenEval.70/DPG81.23高于384² .63/80.09，而FID12.70差于9.51，表明分辨率对不同指标存在取舍。supp“低复杂度更易控制”的解释是作者归因，未独立隔离训练差异。

Harmon主1.5B GenEval.76、COCO/MJHQ FID8.39/5.15，优于所列统一模型的相应总体生成指标；理解MMMU38.9高于JanusPro36.3，但MME-P1155低于1444、MMB65.5低于75.5、GQA58.9低于59.3。GenEval color .85/attribute .48低于JanusPro .89/.56；不能由overall掩盖子项。

Harmon正式supp WISE.41高于所列统一模型Show-o.35，但SDXL.43/FLUX-dev.50更高，物理项.44也低于Show-o.46。WISE的隐式知识生成不同于汉字识别/笔顺执行。main说见S3，实际量表是supp Table S1，已按正式表核对。

## 协同消融究竟支持什么

| 原文对照 | 已核数值或图形 | 可以支持的结论及缺项 |
| --- | --- | --- |
| JanusFlow T5 A→F，REPA | FID19.84→17.61、CLIP24.94→26.40；VQA69.62→69.20 | 改善此协议生成，理解并非全部改善 |
| T5 B→C，共享→独立同构 | FID18.05→17.53、VQA53.94→55.41；POPE78.13→75.30 | 解耦有取舍；SigLIP的额外语义先验还需单独控制 |
| T5 E生成only→F联合 | FID16.69→17.61、CLIP26.89→26.40 | 不能作为理解促进生成的正迁移证据 |
| T5 D理解only→F联合 | POPE85.03→84.73；VQA69.10→69.20、GQA54.23→54.83 | 部分指标相近/微变；无多训练seed CI |
| Harmon T5 MAR vsSigLIP | top5 probe83.1/95.9，POPE86.1/85.1，MME-P1123/1203，MMMU33.3/35.2 | MAR明显优于弱重建encoder，与SigLIP各有取舍；数据先验差异大 |
| Harmon实际Fig6(a,b) | 共享联合的理解柱相近，生成FID/GenEval改善 | 支持特定方向的迁移观察；图无精确标签，不伪写数值/显著性 |
| Harmon实际Fig6(c,d) | SigLIP+MAR双encoder没有同样生成收益 | 提示共享可能相关；缺完整任务曝光、总计算、梯度与seed控制 |
| Harmon T6/7 | 去III15.64/16.85/.56 vs完整8.86/6.08/.71；256→512 FID11.50→8.86/9.91→6.08 | 阶段移除混杂数据与步数；升分辨率需单独因子对照 |

JanusFlow T5是256²、50K步、FID10K、CFG7.5/30步；D13K/E37K按任务比例缩短，匹配任务曝光而未匹配总FLOPs。主结果384²、FID30K、CFG2，不能跨表用17.61和9.51估计REPA收益。

Harmon Fig6现已视觉核对，填补原笔记缺项；柱形没有完整原始数值与CI。作者的“理解监督促进生成”可作为特定条件观察，仍不能升级为普遍双向协同或因果证明。共享架构本身也不能证明改进来自理解内容而非额外数据/优化预算。

## 训练、采样及无独立论文制品

JanusFlow正式三阶段10K/380K/26K，batch512/512/256，AdamWβ(.9,.95)/wd0/clip1/EMA.99、packing4096、约1600 A100 GPU-days。增强LLM、2M内部图和重caption成本都应列入。固定[GitHub1daa72f](https://github.com/deepseek-ai/Janus/tree/1daa72fa409002d40931bd7b36a9280362469ead) README默认CFG5，demo函数默认2，主MJHQ2；需明确各自用途。

该README和demo的生成代码均在`past_key_values=[]`后迭代同一空list，没有取`outputs.past_key_values`，静态上未实现描述的prefix cache；本次没有运行以验证后续行为/影响。HF[ba75944](https://huggingface.co/deepseek-ai/JanusFlow-1.3B/tree/ba759449ee790649850a00d39caddb0acf1c9132)完整模型卡说明EMA SFT检查点、384²、SigLIP/SDXL-VAE；config max_position_embeddings16384只代表配置容量，不能改写paper训练4096。MIT标签与正文模型DeepSeek License分别记录。

Harmon32 A10080GB约4/8天，三阶段各50K、256/256/512²；完整LR/混合比例见精读。supp64次外层约10/30秒，16次约3/8秒；GenEval64/32为.76/.71、16为.74/.69、8为.66/.60、4为.47/.44（1.5B/.5B）。公开1.5B配置内层小扩散头100步，所以“64步”不能当全部网络成本；也不能把小头与全LLM调用混为6400次全模型。

固定[Harmon4eb6087](https://github.com/wusize/Harmon/tree/4eb608765629a1d1b1ce28a85f4c3d126d98b690)的README、FINETUNE、模型配置/训练example和`Harmon.sample`已读。正式§3.2写新增patch数mk−mk−1，与递减mask相反；实际代码用old/new mask XOR选新增位置、最后全剩余，不能由纸面错号断言代码按负数量生成。VAE kl16/16维、scale.2325、stride16、buffer64等已补入结构。

公开仓库另报告仅MAR decoder在BLIP3o-60k微调，GenEval达到.85，提供[HF固定4cc9763的harmon_1.5b-o.pth](https://huggingface.co/wusize/harmon/tree/4cc976310c0866198764eeb153b25a22cb75399e)。这属于配套后续制品：没有独立论文、没有本仓库复测，不能替换正式.76。公开50K/AdamW/lr1e-5/wd.02/随机seed未固定的example设`freeze_llm=False`，不能直接认定它就是.85的decoder-only训练配置。

[制品审查快照](../../data/janusflow_harmon_artifact_audit_2026-10-21.json)记录固定版本和边界；未下载权重、未执行训练/推理。两个现有论文相关制品不另加独立论文计数。

## 对本研究的实验与研究写法

可检验假设分三层：更好的压缩/生成表示是否改善终态；理解监督是否在同数据/预算下改善生成语义；这种收益是否进一步传到严格笔事件和真实执行。每层都需要直接指标，不能用上一层代替下一层。

建议固定LLM/encoder预训和teacher，分别匹配每任务曝光、总FLOPs，比较共享/独立同构/强语义解耦×理解/生成loss；加“同任务额外数据/计算”对照、多训练seed与Pareto曲线。书写任务先测VAE/patch重建上限，再对字符/书体/前缀留出测试身份、顺序、方向和可执行性。按生成时间与真实事件时间区分，以上方案全部未运行。

写作上，JanusFlow从背景范式、简洁接口到机制因子，Harmon从probe证据到共享假设、再分能力和消融，均有可学的论证组织。Introduction须提出可检验不足，Method解释模块如何对应不足，Claim保留具体指标/基线/预算，Limitations写出预训、统计、细节上限和无法外推的任务；不能仅用“统一”“协同”替代机制与实验。
