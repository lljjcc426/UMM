# 统一主干、训练规模与重建对齐：核心三遍审查

本批完成[BAGEL v3](../reviews/C01.md)、[Show-o2 v3](../reviews/C02.md)、[ReCA v4](../reviews/C06.md)的核心三遍与各五条书面理解检查。公式作用、框架图、主表和现有消融逐项核，三官方仓库固定版本查配置/部分源码。没有模型运行。

## 机制与任务边界

| 研究 | 统一接口与关键设计 | 已有证据的限制 |
| --- | --- | --- |
| BAGEL，2025技术报告 | 文字AR/视觉RF；双专家MoT共享attention、双视觉encoder、大规模交错数据 | active7B/total14B；导航另FT、物理世界能力主要定性 |
| Show-o2，NeurIPS2025 | Wan3D VAE高语义/低层双路径，Qwen+LM/flow head，两阶段 | video2B与7B主模型不同；7B主训无video/interleaved；生成视频权重仍TODO |
| ReCA，ICLR2026 | 原UMM视觉embedding条件重建，后训转移回文字/编辑 | 共享模型仍混I2T；低分辨率瓶颈防复制，已有强重建模型可能无益 |

[Show-o2官方NeurIPS登记](https://proceedings.neurips.cc/paper_files/paper/2025/hash/43e8fd8b9581faa71a6a61602bc28435-Abstract-Conference.html)与[ReCA官方ICLR登记](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c34ddd05eb089991f06f3c5dc36836e0-Abstract-Conference.html)已核。BAGEL按已读技术报告身份记录，不由开源热度推正式会议。三者均未在本批证据中验证规范笔顺或机器人书写执行。

## 统一模型的优势须用具体表格界定

[BAGEL v3](https://arxiv.org/pdf/2505.14683v3)GenEval .82与rewriter .88属于不同推理输入；WISE不开思考.52低于MetaQuery .55，SelfCoT升.70。思考提高KRIS总分，但逻辑52.54→48.12、指令分解50.56→50.22退化。IntelligentBench闭源模型仅回答子集，需统一拒答分母。Figure7所谓达到峰值85%的token量是作者学习阶段定义；在约3T时分辨率、context和配比也改变，尚不证明token增长单独触发相变。MoT小规模trainloss对照有价值，但总容量与主规模双任务正迁移仍需控制。

[Show-o2 v3](https://arxiv.org/pdf/2506.15564v3)的GenEval1.5B/7B .73/.76低于表中JanusPro/BAGEL，DPG较好；OneIG text .002，HQ升.125仍落后FLUX .523。VBench总81.34低于CogVideoX81.61，dynamic40.83低70.97。两阶段减轻遗忘，但7B GSM8K82.49→75.28；不能写原语言能力完全保持。Fusion pilot在1B/约1M理解+ImageNet有效，不等主规模/视频已全面消融。Eq2写−log cosine而未说明非正cos处理；未取得独立蒸馏实现，保留数学定义域缺项，不替作者补公式。

[ReCA v4](https://arxiv.org/pdf/2509.07295v4)Harmon无GPT4o数据 .86/87.21，.90/88.15另经BLIP3o SFT路线。Table4 POPEF1和GQA略降、Show-o WISE不变，不能写所有任务无损提升。F2报告同空间同分辨率输入复制导致CE近零而生成退化；G节BLIP3o已有重建能力时无额外增益。PCA少数feature可视化与两组案例相关不构成完整空间同构或普遍因果证明。

## 训练和资源应逐版本核

[BAGEL固定代码](https://github.com/ByteDance-Seed/Bagel/tree/a2fa77dd8caeefc41e6607ae0ec17408d3f4ee9f)RF路径t0data/t1noise、target ε−data；Show-o2正文t0noise/t1data，比较公式需先换同一约定。BAGEL训练示例提供T2I/编辑/VLM小样本，不能当数万亿token原始训练集已完整公开。

[Show-o2固定代码](https://github.com/showlab/Show-o/tree/45a5a2de01d1ebd10cd5864d29310a76476cdf23/show-o2)补充hidden1536/flowhead10层与stage1每卡gen6/understanding2（64卡对应384/128）。README同时说明：视频理解权重已发，T2V/I2V和mixed-modality生成权重仍TODO。论文能力、已发布checkpoint和公开训练入口需分别关联。

[ReCA固定代码](https://github.com/HorizonWind2004/reconstruction-alignment/tree/99ebefeab7a6ebc2cb856d7b6ab3402caf5aa834)中文指南明确要求最小支持分辨率、尽量冻理解；共享模型需I2T。默认Harmon配置50K iterations，而论文Table8为5K。Table8 Harmon1.5B单A10012.5h，BAGEL每卡b8/6卡4.5h=27GPUh；正文单GPU总述与1.5B关联27h需保留冲突，不统一改写成同一成本。BAGEL的ReCA使用10K FLUX图是为减域差，其他模型MJ成功不意味着BAGEL也稳健。

## 可证伪验证与写作

1. 双任务共享价值：匹配active FLOPs与total参数两种条件分别比较dense/MoE/MoT、独立双模型+小接口，干预跨专家attention和条件特征，报告任务Pareto、训练/推理总成本。
2. 规模/涌现：固定配比、resolution/context、数据去重和推理预算，只改变seen tokens，多seed连续指标与多个阈值，检验阶段变化与评估非线性。
3. 重建迁移：相同token/FLOPs下替换语义/VAE/随机或打乱特征，扫描分辨率/模糊/模板；同时评复制、重建、文字生成、理解与计数。SFT/ReCA/I2T曝光分别匹配。
4. 规范书写：从静态重建到事件预测需额外数据和事件loss；逐笔方向/抬落/重复/缺笔、RGB可观测性和执行成功分开，加入规则SVG、强在线生成与独立理解/生成基线。

学习其问题定义、方法分工、阶段表和同基模对照；Claim按模型/版本/数据路线与预算表述，Limitations主动写失败模型和评价范围。上述实验均为方案，未实施。

当前339条主目录/339笔记、334章节或协议/5摘要、66项核心三遍和五项书面检查。其余阅读/候选追引未完成；未独立模型复现，无文件删除。
