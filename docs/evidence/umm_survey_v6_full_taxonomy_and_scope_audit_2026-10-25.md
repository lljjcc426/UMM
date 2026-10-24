# UMM综述v6：完整分类与能力范围审查

第二百零三批完成[L057](../reviews/L057.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/umm_survey_v6_full_taxonomy_and_scope_audit_2026-10-25.json)。358目录（331论文／研究、27资源），308核心/313书面含未通过项；待完成核心深审23篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2505.02567v6)、[主源2](https://arxiv.org/html/2505.02567v6)、[主源3](https://arxiv.org/pdf/2505.02567v6)、[主源4](https://github.com/AIDC-AI/Awesome-Unified-Multimodal-Models)、[主源5](https://raw.githubusercontent.com/djghosh13/geneval/main/prompts/evaluation_metadata.jsonl)、[主源6](https://huggingface.co/datasets/wendlerc/RenderedText)。

## 研究问题

组织统一理解/生成模型的架构、tokenizer、任务接口、数据和评测；输入研究文献，输出分类与研究导航。无新增训练模型，新增实验的训练条件/对照/消融不适用。

## 现有不足

理解常用AR、生成常用diffusion，统一名称不足区分哪些权重/表征/损失共享；需要可追到encoder/backbone/decoder/mask的比较。导言AR落后扩散的整体判断缺统一重跑，不能当普遍架构定理。

## 贡献

全篇以diffusion/AR/AR+diffusion三类；AR再分pixel/semantic/learnablequery/hybrid，hybrid分任务择支pseudo与同时融特征joint；融合类分pixel/hybrid。T1结构矩阵、T2超越图文接口、T3训练数据五类、T4理解/生成/交错及其他评测；F1时间轴、F2理解组件、F3扩散、F4AR单元、F5八种结构示意。无新的模型效果或统一重跑。

## 输入、模块、输出与公式

§2.1 encoder→connector→LLM，projection/query/fusion三种connector；§2.2 Eq1–3 GaussianDDPM正反转移、Eq4AR联合分解、Eq5NLL；正文未编号simpleepsilonMSE被笼统称VLB，严格VLB通常有权重/其他项，勿当任意扩散的完整目标。§3.1包含离散mask/flow，Gaussian定义不能统摄UniDisc/FUDOKI。AR预测连续embedding再由diffusionMLP/SD/FLUX解码也在AR类，故分类按主干组织，不是所有组件都纯AR。

## 模型结构

pixel指重建目标编码，含连续latents；semantic包含CLIP和兼重建UNIT/UniTok等，并非完全互斥。learnablequery指汇聚/输出接口，叠加于semanticencoder，可与其他轴重合。pseudo选择不同任务分支，joint并联/特征融合；是否贡献跨任务知识仍要核梯度与干预。F5 c类是主干图文损失共建，与b类外挂diffusion需按每篇训练路径再查。因存在decoder/expert，统一模型不必所有模态同一tokenizer/参数。

## 数据分布与划分

T3与§4.1–4.5全读：理解图文对、T2I、编辑triplet、交错documents、subject/control条件数据；额外image/video合成管线。数据规模单位混合图像/文档/token/编辑条，不能横向直接求和。MMC4约101Mdocuments571Mimages，OBELICS141Mdocuments353Mimages115Btokens，OmniCorpus正文2.2Bdocuments8.6Bimages1696Btokens而表只写8B样本，须带单位。RenderedText官方卡确写手写外观，但实际为Blender+约8000字体的静态1024图/行字框，无落笔时序/接触/规范顺序，不可当真实在线手写轨迹。

## 指标与评价协议

§5全读理解perception/reasoning、T2I对齐/关系/知识、编辑改动和保持、交错coherence/consistency、unificationUEG/GEU。FID分布拟合、CLIP语义、OCR/检测/VQA/人评各有偏差，指标不同不能聚成架构优劣因果。T4GenEval写1000prompts；本次官方evaluation_metadata.jsonl确定性计553，记录该表错误。T4HQEdit约200K等训练总量不等同固定测试规模，引用前核任务split。

## 对比方法

T1–2逐行比较架构与release标签，T3–4逐行数据/评测资源清单，均为引文汇总而非控制数据/计算的baseline表。无系统检索库、搜索式、纳入排除、双人筛选或质量评估流程，不能据未列出工作推出不存在。已读具体模型有优先原文解释权。

## 实验条件和发布边界

固定v6包含截至2025末部分工作，2026-01-26更新，非2026-10全景。§2基础5式仅介绍背景，无新定理/训练。未执行任何被引模型/生成/训练/benchmark/APIjudge，没下载全部被引数据。本次对GenEval公开metadata只计行及类别，不进行模型评分。

## 主结果

研究结果为分类/资源地图；T1–4无本综述新增模型数值实验。§5.4的1000例10类32任务UEG/GEU来源RealUnify，诊断分步有用但“精确定位瓶颈”仍依赖各阶段oracle/评分有效性。§3.4把M2omni笼统描述为处理/生成video，T2实际只列SD3图像decoder与CosyVoice音频decoder；既有L159原文审查视频为输入、图像caption接SD3，不能增加视频生成能力。

## 消融及进一步实验

无新模型受控消融；各类别后优缺点是作者归纳和假说，不能从一个冻结encoder推定所有query法一定弱，或从一个VAE压缩推出所有手写细节必丢。§6强调token效率/attention/data/eval/CoT/RL/公平性/个性化，文中已有MMaDAUniGRPO、UniPic双任务RL与交错编辑资源，因此末段“largelyunexplored”须限定具体任务/版本和受控缺口。

## 局限与疑问

34页研究正文§1–7、5图4表5编号式全读；参考清单[1]–[403]核目录及关键引用，不等于403篇原作逐篇读。分类轴粒度不齐、外挂decoder与共享骨干同称统一；anytoany标签不保证任意模态组合或视频生成。未声明系统纳入流程，时间截止和遗漏限制显著；表内GenEval规模错误，数据单位/训练测试混写，会议/日期引文仍须原站核。

## 预期优势条件

对跨领域发现候选、按encoder/主干/decoder/mask建立共享边界有用；做手写时需再加像素/轨迹/接触/事件/规则轴和可观察监督。统一表示可能促进迁移，需匹配训练预算和跨任务干预证据，不能由分类名或终态生成分数判断笔顺理解。

## 可证伪实验

Q1分类是否稳健：固定同一模型版本，双人独立按输入/输出、tokenizer目标、共享层/梯度、loss、最后decoder标注，报告混淆与分歧，检验AR外挂diffusion/semantic重建等交叉例。Q2所谓缺口是否仍存在：预声明关键词/日期/原站搜索，对§6个性化、编辑、交错、RL逐项查同任务先行工作，再用同预算双任务对单任务/adapter和表示干预测增益；手写分别比较最终静态字形、轨迹复原及规范顺序，防止泛化claim偷换。仅方案未执行学习实验。

## 论文组织与Claim学习

综述从背景→架构→数据→评测→挑战的组织可复用；补系统检索/纳入与截止规则、所有规模单位及测试split。为每条能力列方向和具体解码接口，避免video输入即输出。展望需与正文已列成果一致，把仍缺受控验证的条件写具体。

## 实际阅读范围

v6全34页§1–7全部研究文字、Eq1–5、F1–5实际视觉、T1–4全部行及表注；末[1]–[403]参考目录/关键引文查证，未逐篇读403原文。GenEval官方metadata553行确定性核、RenderedText官方卡核合成静态外观/行字框；无模型/训练/OCR/API执行。综述核心三遍和五书面完成。

## 本次补读发现

表4把GenEval写成1000prompts；官方evaluation_metadata.jsonl实际553行，已保留差异。T3同时列document/image/triplet等单位，OmniCorpus表8B与正文8.6Bimages/2.2Bdocuments须分别解释。

learnablequery是编码汇聚接口，semantic是表征训练目标，二者可以同时成立。分类对检索有用，做受控架构结论前需要重建输入输出、损失、共享梯度与最终解码器。参考目录[1]–[403]核清单，不代表已逐篇阅读引用。
