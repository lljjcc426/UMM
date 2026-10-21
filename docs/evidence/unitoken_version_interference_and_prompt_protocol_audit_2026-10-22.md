# UniToken：版本、联合训练干扰与改写提示词协议

第一百一十二批完成已有[L097](../reviews/L097.md)核心三遍与五项书面记录。[固定来源与制品审查](../../data/unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.json)。356条目录（329论文／研究、27资源），221核心/224书面含未通过项，135条未确认核心（含资源）。未新增研究条目、删除仓库文件、下载权重/训练媒体或执行模型；文本提示词统计不构成独立复现。

## 版本与真实任务

正式[CVPR2025 Workshops/MMFM论文](https://openaccess.thecvf.com/content/CVPR2025W/MMFM/papers/Jiao_UniToken_Harmonizing_Multimodal_Understanding_and_Generation_through_Unified_Visual_Encoding_CVPRW_2025_paper.pdf)，pp3609–3619，完整11页1,476,050B。属于workshop，不计CVPR主会CCF-A录用。已读Abstract/§1–5核心全文、Eq1、T1–6和图注，实际核p3F2/p4T1–2/p5T3–4/p6T5–6。定性F3/F4未逐图核、参考文献未逐篇读。

另核[2504.04423v1](https://arxiv.org/html/2504.04423v1)§3–5、T2–6更新配方/主表。其正文沿用“两阶段”表述，又增加第三阶段高质量SFT；不能将arXiv三阶段结果、正式两阶段结果和当前StageII检查点合并为一套实验。

| 项目 | 正式workshop | arXiv v1 |
| --- | --- | --- |
| 训练 | I caption对齐；II理解/生成混训 | 另加III：423K长对话/文档与100K对象生成 |
| 主结果 | II：GenEval .58，OCRBench634 | III：GenEval .63，OCRBench757 |
| 消融编号 | T5单任务/联合；T6数据规模/比例 | T5数据；T6单任务/联合 |
| 消融范围 | 不用AnyRes | 另不使用III |

研究问题是让共享AR骨干兼顾图像理解和静态图像生成，并减少联合训练干扰。没有视频、笔画事件或指定文字书写任务。OCRBench测读取输入图像文字，GenEval测对象/属性/位置，二者均不足以证明可写规范汉字笔顺。

## 表示与训练：什么信息在哪条路径可用

采用Chameleon7B架构、Lumina-mGPT初始化；ChameleonVQ为16384码/downsample16。输入图像一支量化为离散ID，一支经过SigLIPSO400M-patch14-384，1152维特征用两层MLP对齐。顺序为`[BOI]image_d[SEP]image_c[EOI]text`，在序列维拼接，LLM及预测head共享，视觉网络仍有离散与连续两支。

问答读取两支图像信息后输出文字。文本生成图像没有已知目标图像供SigLIP编码，输出离散码再用VQ decoder还原；生成收益经共享权重训练产生，不能解释为推理时直接输出连续字形。AnyRes支持2×2、1×2/3、2/3×1网格；768²为最大方图，代码还有384×1152/1152×384矩形，不能写成所有长边至多768。

I用2.5M captions，ShareGPT4V49.5%/LLaVA22.2%/ALLaVA28.2%，冻结LLM训练ViT/adapter。II约10M公开理解与10M私有Midjourney合成图文，联合训练ViT/adapter/LLM；T1理解子项标示数相加9.899M，不等于已取得精确清单。连续位置不作为离散目标预测；主文问答只对answer、生成只对图像ID算CE，当前代码另有SEP监督和可选zloss，未逐行复原全部预token化mask。

正式T2：I全局1e-3/ViT1e-5；II均1e-5，AdamWβ.9/.95、cosine、batch128、各1epoch。作者称ViT lr5e-4发生collapse，但未给完整扫描/普适阈值。理解greedy，生成multinomial；GenEvalCFG5.5/CompBench5。每prompt采样数、seed、原始硬件/总FLOPs未核齐，当前8进程脚本不补足原始运行记录。

## 主表：双任务可用与全面领先应分别判断

正式T3 UniToken按MMMU/MMB中文/MMB英文/MMStar/SEED/MathVista/HallusionBench/AI2D/OCRBench为34.2/64.1/70.3/45.2/70.3/41.6/49.6/67.6/634。MMMU低于Chameleon34.4、ShareGPT37.2，OCR低于Emu3-chat687，AI2D低于Emu3-chat70。Emu3的chat/generation是不同权重，不作为单一共享UMM检查点。

正式T4 GenEval.58低于Janus.61、Transfusion.63、SD3.74；位置.26低于Janus.46。CompBench颜色/形状/纹理.7115/.5179/.6670也未全面胜过DALL-E3 .811/.675/.807。不同模型预训、数据、参数与接口有差异，排行榜不能单独识别双输入表示的因果效应。

| 指标 | II | arXiv III | 变化 |
| --- | --- | --- | --- |
| GenEval | .58 | .63 | +.05 |
| OCRBench | 634 | 757 | +123 |
| HallusionBench | 49.6 | 57.8 | +8.2 |
| MMMU | 34.2 | 32.8 | −1.4 |
| MMB中文 | 64.1 | 62.0 | −2.1 |
| SEED | 70.3 | 69.9 | −.4 |
| MathVista | 41.6 | 38.5 | −3.1 |
| GenEval Counting | .39 | .35 | −.04 |

III增加数据与步骤后有能力取舍；该结果不能表述为所有理解和生成能力均提升，也未用配方等量的III消融单独定位原因。

## 消融检验了什么

| 正式T5 | 单生成GenEval→联合 | 单生成Comp→联合 | 单理解General→联合 | 单理解TextRead→联合 |
| --- | --- | --- | --- | --- |
| Chameleon† | 51.2→31.1 | 40.1→26.0 | 45.4→45.6 | 28.7→28.4 |
| UniToken* | 51.1→49.4 | 39.5→39.4 | 53.2→53.3 | 50.1→49.5 |

在所测配方中，UniToken的生成负迁移较小；它仍有GenEval−1.7分、TextRead−.6分。General平均八项、TextRead平均三项（AI2D/OCRBench/MMVet），精确跨量纲缩放未核齐，不能直接平均原始OCR/MME数。联合20M与单任务10M训练曝光/总计算不同，也没有直接测梯度冲突。

正式T6：2M理解+2M生成的GenEval/Comp51.3/40.3；2M+1M为50.7/39.7；10M+10M为49.4/39.4；10M+5M为38.4/33.8。减半生成数据同时改变总数据、生成曝光和总步数，不能得出普适最优1:1。放大两类数据也没有单调改善生成。未提供AnyRes×ViT微调×III的完整因子实验或训练多seed区间。

## 固定制品与非论文研究内容

[GH 9181c613](https://github.com/SxJyJay/UniToken/tree/9181c61367baf44e67f08984cac8347c1d5a1626)104树项，已读README/TRAIN、base与AnyRes StageII shell、phase2混合yaml、AnyRes特征插入/label/zloss、两类生成接口和CFG核心；底层框架/完整预处理未全读。

| 实际内容 | 复现影响 |
| --- | --- |
| `generate_img` | 强制加入图像起始前缀，`do_sample=True`；与问答`generate`的greedy不同 |
| 问答图像路径 | 插连续feature并mask相应label；当前断言只有一个image-end，TRAIN的多图格式例子不证明此路径任意多图可运行 |
| StageII shell | lr1e-5、wd.1、dropout.05、zloss1e-5、macro128/micro16/8process、clip4、warm.01、maxlen4096 |
| 配置引用 | shell仍指phase1captionyaml，`accum_iter`未在该文件定义；另有phase2混合yaml和绝对`/home`路径，不能自动视为已经正确调用/数据齐全 |
| 发布范围 | 104项未见完整benchmark入口或III专门脚本；README仅四个base/AnyRes I/II模型 |

[HF StageII revision96d1e4c](https://huggingface.co/OceanJay/UniToken-AnyRes-StageII/tree/96d1e4c505e4298cd4cbe9eed27850cf6b738e9a)卡仅31B Apache元数据，三片权重未下载。1.71MB模型config下载仅.84MB超时，排除该不完整文件；不能据此确认正式/arXiv每一行检查点。

[提示词数据 revision579054e](https://huggingface.co/datasets/OceanJay/rewrite_geneval_t2icompbench/tree/579054e1dc28083a7157fe333566df7b80f1652d)是需要单独记录的非论文制品：9个文本文件，含GenEval与8类CompBench。已取得GenEval553个非空唯一行、color300行，读首例和做全文计数，其他七组未下载、未逐条做语义审核。README称短prompt效果不足而改写，例子确实加入更长场景细节；数据卡/许可说明未见。原表各baseline是否用同一改写版本、逐条映射和prompt级结果未齐，保留待核，不能直接判定原表无效。

## 优势假设、可证伪实验与写作学习

输入语义/小字信息可由预训SigLIP提取、而VQ语义抽象不足时，连续旁路可能改善理解；保持原AR图像分布可能减轻联合生成遗忘。额外预训先验、参数、输入token与成本需计入，不能将收益全部归于离散/连续类型。

固定Lumina/Chameleon初始化与可用SigLIP先验，按相同总FLOPs比较离散、双输入、同长度随机/重建特征、仅理解连续支路。拆AnyRes、ViT lr与III，分别固定总数据和每任务曝光扫描配比；报告遗忘、梯度冲突、双任务Pareto和多seed。原prompt/统一改写对所有baseline交叉测试，公开映射、采样数与seed，分计数/位置/长度。上述实验均未执行，新颖性仍需系统查新。

跨字体/文字体系分别测“读图”与“生成指定字”的CER/形近拓扑，严格书写另加时变墨迹、接触抬笔和顺序事件；静态图像优势不推出时序能力。

可学习Introduction从表示不足定位联合干扰，Method按编码→训练→loss→推理展开，单任务/联合表直接响应问题。Claim应限定所测配置干扰减小，保留负迁移和III退步；正式版无独立Limitations节，笔记需补私有数据、未匹配成本、prompt/版本和复现配置边界。Mode-switching负担与量化不足是动机，未测延迟或普适理论证明。
