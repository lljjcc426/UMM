# 开放模型、训练归因与部署条件：第十五批

2026-10-20；本批L071、L117–L122共7项，累计233份笔记。主目录332条中章节247、摘要33、历史待复核52；五项书面检查8项，完整三遍验收未完成。没有删除文件，未运行模型。

## 已核的重要区别

| 研究 | 证据与结果 | 研究判断 |
| --- | --- | --- |
| [GenEval/L071](../reviews/L071.md) | Mask2Former实例检测；CLIP仅局部颜色分类；553prompt×4图，任务均分 | 不能将其概括为整图CLIPScore；素描OOD/笔顺事件需新效度验证 |
| [BLIP3o/L117](../reviews/L117.md) | 旧main418fc44保留，默认分支转NEXT；HF8B公开.83/80.73/.52 vs私有论文.84/81.60/.62 | 必须绑定分支、模型权重和数据范围；像素decoder额外成本需计 |
| [OpenUni/L118](../reviews/L118.md) | Base GenEval.62→.84，DPG79.04→80.29，主要增加60K定向蒸馏 | 组合基准与更广泛指标增益不同；冻结理解骨干不能证明双向协同 |
| [UniFork/L119](../reviews/L119.md) | 小消融.33/FID16.3，生成专家.36/15.1；SEED55.1 vs专家56.6 | 部分共享优于全共享的证据不等价于全面优于专家；主版本同时改数据/分辨率/head |
| [HunyuanImage3/L120](../reviews/L120.md) | 80Btotal/13Bactive；文本AR+图连续去噪；初始Base与后续Instruct/Distil不同 | 视频挖图对不等于视频生成；单图/编辑能力按版本，MoE深层专门化只为相关性 |
| [DeepGen/L121](../reviews/L121.md) | 约5B、64H200、600K两阶段步数；RL用OCR/偏好/CLIP | 小参数量不足以推出训练廉价；部分消融GenEval不变；RL/SFT来源含基准集合需核交叉 |
| [Mobile-O/L122](../reviews/L122.md) | MCP无预训消融70.4，主74.2；quadpost62.1/74.2 | 消融条件和主模型不能混用；quad带额外QA信息要等曝光对照 |

## Mobile-O公开实现核查

[export.py固定revision91c2550](https://github.com/Amshaker/Mobile-O/blob/91c255080a0130846fe5b5cd54ff5af3c05ab2b9/Mobile-O-App/export.py)第154/176行DiT为FP32，第191/201行VAE FP32，connector FP32；第256/257行vision为FP16，392行LLM bits默认4。论文§4.5写LLM8bit、视觉全FP32，需分别记录。600MFP32裸权重约2.4GB，加上其他组件后如何得到<2GB运行内存，取决实际部署精度/按需加载/驻留与测量，当前材料不足以解释。

appREADME写约3.6GB下载/5GB磁盘，不能当运行RAM。PDF第4页Fig2已视觉读，记录MCP输入输出及双loss路径；尚未编译或在真机测peakRAM。Table8列I5epochs，正文50K/b512/9M约2.84epochs，亦需训练脚本解释。记录这些差异不等于否定全部模型结果。

## 假设与实验设计

1. 共享是否互利：单任务/全共享/Y形/connector联合组，分别匹配总参数、active计算及每任务曝光；不能只列一个均分。
2. 数据是否解释增益：BLIP60K按手势/物体/地标/文字留出，pair/quad共享同图和QA，独立新组合测试；基准提示/生成teacher数据查交叉。
3. 表示是否保留文字：先测codec重建OCR和最小笔差，再测静态生成；语义码/连续语义/像素解码分别计参数和NFE。
4. 移动部署是否成立：固定真机、编译版本、精度、分辨率、NFE、冷暖启动及能耗，文字测整段回答，图像测端到端和peakRAM；4/8bit与visionFP16/32单独比较。
5. 评价是否可靠：照片/素描/书法分层做人评，报告检测/分割错误、agreement和kappa；笔顺须另测事件身份/次序/方向，不靠终帧GenEval/OCR。

## 尚未完成

GenEval全部标注附录、各论文全部框架图/表/公式及官方实现仍有缺项。BLIP3o-NEXT和TMP均有论文，需去重后安排进一步原文核查；不能归无论文。DeepGen warmup正文/表冲突、Hunyuan具体优化超参、Mobile-O内存协议仍未解决。本批没有完成任何模型独立复现。
