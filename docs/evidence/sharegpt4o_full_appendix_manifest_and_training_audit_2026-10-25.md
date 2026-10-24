# ShareGPT4oImage：完整附录、精确清单和训练入口审查

第二百零九批完成[L174](../reviews/L174.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/sharegpt4o_full_appendix_manifest_and_training_audit_2026-10-25.json)。358目录（331论文／研究、27资源），314核心/319书面含未通过项；待完成核心深审17篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2506.18095v1)、[主源2](https://arxiv.org/pdf/2506.18095v1)、[主源3](https://arxiv.org/html/2506.18095v1)、[主源4](https://github.com/FreedomIntelligence/ShareGPT-4o-Image/tree/19ac7d779d8b893b549c2640373c78947ee4b6d5)、[主源5](https://github.com/FreedomIntelligence/ShareGPT-4o-Image/blob/19ac7d779d8b893b549c2640373c78947ee4b6d5/train_janus.py)、[主源6](https://huggingface.co/datasets/FreedomIntelligence/ShareGPT-4o-Image/tree/f9bcb9494e562f3b6d46585bda0e7f0f0d6ec43f)、[主源7](https://huggingface.co/FreedomIntelligence/Janus-4o-7B/tree/cc772ef77695f829f48e08c81c6c381b7e76b9e8)。

## 研究问题

少量强教师合成图/编辑数据，能否在已有Janus-Pro7B上增强文生图并增加源图+文字条件编辑能力？训练微调成本与骨干/教师数据成本需分别计算。

## 现有不足

闭源教师高质量输出难以开放复用，已有开源Janus文生图有差距且无直接图编辑接口；用教师输出监督并为源图加语义与VQ两通道。教师架构仍不公开，论文“联合架构”“pixel dependency”描述不能当教师内部机制已证。

## 贡献

ShareGPT4oImage数据集与Janus-Pro7B微调Janus4o；文本+源语义embedding+源VQtokens输入，随机丢源图码，三条件logit混合后CFG采样。沿用既有AR统一骨干/视觉资产，无从零训练7B或证明等同教师完整能力。

## 输入、模块、输出与公式

文→单张图；源图+英文指令→单张编辑图；公开demo还有理解函数但论文未评理解保持。无视频、实际笔画轨迹/接触时钟/多步规范书写输出。T3“Motion Change”为单图动作编辑类别，AppB“storyboarding”是任务类别，无连续视频验证。

## 模型结构

继承Janus-Pro理解视觉编码与生成VQ编码解耦、共享因果LLM。目标图CE nexttoken，图384²/576token在公开实现；编辑输入E(Ihat)+Xhat+S。lc全条件、lo去源VQ仍保留源语义/文字、lu全部mask，lcprime=(lc+5lo)/6，lg=lu+5(lcprime−lu)，temperature1；sprime0全源VQ，增大偏向无VQ条件，可解释像素保留/改动折中，论文无消融。文本10%在公开代码为样本概率全promptdrop，源VQ50%为整块跳过填入，并非明确逐token独立mask。

## 数据分布与划分

论文简写45K文生图+46K编辑=91K。当前HF两JSON实际45717/46539=92256，与当前README/HF精确表一致，修正旧记录“92K分项不合”的说法；README仍夹91K概述，不能把发布精确数倒灌论文实际训练量。文生图字段input_prompt/output_image/output_image_resolution；编辑多input_image/其resolution，46539全部单源图，缺少来源/教师快照/采样参数/任务标签/split。输出路径各集内唯一，不等于像素去重。仅解析约50MB JSON，不下载20个图tar或权重。JSON文生图37534方1024²、余多横/竖；编辑有5条声明1×1，未取图不能断言实际像素。

## 指标与评价协议

GenEval对象/计数/颜色/位置/颜色绑定，DPG密集指令，ImgEdit八类单轮编辑；无CER/字符笔画或动态指标。52文生图/35编辑Twitter例，单一评价者、随机输出排列、指令+视觉偏好。F5胜/平/负51.9/26.9/21.2%(可由27/14/11共52对应)，51.4/28.6/20%(18/10/7共35对应)；无多标注者一致性/CI或显著性支持。

## 对比方法

T1/2JanusPro7B作者同协议复现为最相关beforeafter，其他从原文引用；T3不同底座/预训练/训练量，#Data只列后续任务数据，JanusPro预训练与教师生成成本未计入91K，不能证明全流程比所有基线省训练成本。T3本表3.26胜Step1X/E1各3.17，不等于2026全部最新编辑模型排名，也未直接与GPT4o量化同表比较。

## 实验条件和发布边界

论文3epoch/LR5e-6/batch128/全参数微调、8A800约6h，无完整teacher API日期/质量/失败筛选/采样成本与seedCI。固定训练代码AdamW/wd.1、cosinewarmup5%/minLR.15/seed42/bf16，config为ZeRO1而带zero3flag，不将其称ZeRO3实际训。README命令每卡1×8卡×累积8=有效64，与论文128不同；parser默认累积16可得128，但不据默认推定实跑。README写configs/sft.yaml而树为config/sft.yaml；data_path是JSON本地文件/图相对路径，需先合两清单，并非直接给HF字符串可用。脚本449行末只到#Start training，未调用train(args)，不能照发布脚本宣称可直接复现；未执行。

## 主结果

T1 JanusPro overall.76→.80，single1持平、two.85→.92/count.53→.58/position.69→.70/binding.58→.70，color.90→.88下降；四百分点非4%相对。T2DPG84.12→85.71(+1.59)，global80.70→92.59大增，但attribute90.04→89.51降。T3overall3.26本表最高，motion4.13/style4.47突出；addition3.60<Step3.90/removal2.28<2.61/replace3.27<3.45/background3.32<E1 3.38/object2.28<2.55/hybrid2.74<2.87。总体改善与每类短板同时保留。F1/2少量示例展示多样性，不证明教师全部能力迁移。

## 消融及进一步实验

19页全文及AppA–E中未提供数据规模/混合比例/两视觉输入/50%mask/第二CFG权重/不同teacher或真实图的独立消融；不能把所有改善分别归因每个部件。B1六维含ImageNet1000对象，T4剩五维，F6类别频率；B2 k1–100指数权exp(−λ(k−1))，F8标λ.1，但正文仅给函数未明确全生成配置或归一采样实现。T5五大14小编辑类别/F7分布，不含逐类别效果因果实验。

## 局限与疑问

v1实际19页8图5表/全部无编号目标与logit公式/指数权式、AppA1–3/B1–2/C1–3/D1–2/E全核。§2.1 imagefirst明确ALLaVA原图+新caption，F3却画imagegeneration/摘要与AppE称全synthetic，来源占比/逐条标记缺失，JSON不能确认哪张由教师重绘。C3提示允许任务不合时忽略base task、优先描述美感，不能保证14任务标签忠实；C2要求模板不含可读文字，与D1先生成文档内容再写prompt的关系未清。未量化理解能力退化/长文本字形/闭源教师偏差。AppE明确未事后偏差过滤。

## 预期优势条件

已有JanusPro视觉/语言预训练提供基础，少量较高质目标图+源图双通道可改善指令图生成/编辑；源VQ与无VQ混合调局部保真/大改动。效果依底座、分辨率、教师覆盖，数据质量/接口/解码贡献尚未独立拆开。

## 可证伪实验

同JanusPro、相同训练token/预算与测试源，分真实/教师图、promptfirst/imagefirst、T2I/edit比例；源语义only/VQonly/both、整块mask比例、sprime曲线各因子消融。拆教师合成/底座预训练/微调成本，逐条记录来源与任务忠实度。锁评估器/分辨率/seed，多人双盲并报分项区间与理解/文字CER保留；若用于手写另加密集笔画事件真值。均为设计，未执行。

## 论文组织与Claim学习

将“fromscratch”限定新增编辑任务，把6h限定微调；数据标题教师级不等于学生达教师能力，官方README也明确仍落后GPT4o。精确发布清单与论文简写/实际训练版本分开；mask单元和有效batch须同步文档/代码，公开入口需完整。对任务标签服从、来源真实性与静态/动态能力给可核证据，少量单人偏好避免用显著改善作为统计结论。

## 实际阅读范围

arXiv2506.18095v1全部19页§1–5、references清单及关键引文、AppA–E全部，包括C1–3完整meta prompts/D全文/E未偏差过滤；F1–8实际视觉/T1–5逐表、所有无编号CE/CFG/混合/指数公式；7张contact全看F5p7原页放大。固定repo19ac7d7 README全文/全部3研究代码文件train449行+config28行+demo356行，modelcard正文对照；HF固定两JSON全量结构/条目数量解析，metadata/cards读取，未视觉审查92256图或取20图tar/模型权重，raw config为LFS pointer未冒称完整配置读过。未运行推理/teacherAPI/训练；核心三遍/五书面完成。

## 清单补证

当前发布两JSON精确为45,717文生图和46,539编辑，共92,256条；公开卡精确表与此一致，更新旧记录对92K分项的疑问。论文91K是历史简写，尚无实跑清单证明训练用当前全部条目。编辑清单全部单源图，字段不提供来源或任务标签。

## 复现入口与训练口径

README命令的有效batch为1×8×8=64；论文写128，parser默认累积16只能说明另一可配置值。发布树config/sft.yaml与命令configs/sft.yaml不同；训练脚本主入口设置种子后停在注释，缺少train(args)调用。数据入口读取本地JSON且未自动合并两任务清单。这是静态检查，不代表执行过训练。

## 全部合成表述范围

正文image-first写ALLaVA原图配新caption，图示/摘要/数据卡则笼统称GPT4o合成，公开字段不能区分来源。C3还允许忽略不合适的base task，因此类别抽样不保证任务忠实。当前HF数据卡Apache2与模型卡MIT是发布元信息；模型卡指向LICENSE但当前文件树缺该文件，未据此作法律结论。
