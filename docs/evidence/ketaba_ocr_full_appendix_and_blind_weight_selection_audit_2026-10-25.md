# KetabaOCR：完整附录、blind定权和伪真值审查

第二百一十批完成[S001](../reviews/S001.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/ketaba_ocr_full_appendix_and_blind_weight_selection_audit_2026-10-25.json)。358目录（331论文／研究、27资源），315核心/320书面含未通过项；待完成核心深审16篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://aclanthology.org/2026.nakbanlp-1.21/)、[主源2](https://aclanthology.org/2026.nakbanlp-1.21.pdf)、[主源3](https://github.com/HasanBGit/Ketaba-OCR-LoRA/tree/f1aefa8317edda0d7f064c2ae1731cdb4186b076)、[主源4](https://github.com/HasanBGit/Ketaba-OCR-LoRA/blob/f1aefa8317edda0d7f064c2ae1731cdb4186b076/src/ensemble/weight_configs.py)、[主源5](https://github.com/HasanBGit/Ketaba-OCR-LoRA/blob/f1aefa8317edda0d7f064c2ae1731cdb4186b076/src/ensemble/advanced_ensemble.py)、[主源6](https://huggingface.co/HassanB4/Ketaba-OCR-LoRA/tree/7f55602e5e83041c4af6ff007c7ccd1dc3e23202)、[主源7](https://huggingface.co/sherif1313/Arabic-English-handwritten-OCR-v3/blob/a404b5ba97a7d7ec6513d8e007897c9ad28c3da9/README.md)。

## 研究问题

在低显存与有限标注下，如何把已有Arabic-English HRT视觉语言识别模型适配1951–1965 Al-Saleh历史Ruqah/Naskh手稿行，同时保持字形、正字和附标转录？

## 现有不足

历史连笔/变体/褪色/噪声与现代文字预训练分布有差，通用VLM易现代化改写或循环。作者选择专业预训HRT底座再PEFT；同底座对照支持适配收益，但无单独证明每个模块或更强泛化/抗噪机制。

## 贡献

专用预训HRT上的NF4 QLoRA+DoRA/RSLoRA适配，六模型Linear+Boost/规范化分组/3gram/共识选择。正式OCR领域系统论文；低秩与量化是既有方法，线性加阈值boost为启发式融合，未给普适最优/原创性证明。

## 输入、模块、输出与公式

已切行RGB稿图→Unicode文字，保正字/附标；生成式decoder用于识别转录。无图生成、规范笔顺、笔尖时序或视频接口，若作手写生成评判器须独立验域外字形/时序偏差。

## 模型结构

sherif1313/Arabic-English-handwritten-OCR-v3源自Qwen2.5VL3B，论文含视觉总约4.07B；冻结NF4 base，attentionq/k/v/o+MLPgate/up/down加r32α64/drop.05，DoRA/RSLoRA均开。Eq1 Wprime=W+BA省略缩放/DoRA范数细节，不能据此当完整实现。输入prompt标签mask为−100，assistant转录CE。图1额外写CLIP/SigLIP视觉初始化但未给具体checkpoint，不据图自行更换底座定义。融合Eq2/5 wi=norm(1−CER+.5I(CER<.15))。

## 数据分布与划分

官方train15962/dev1774/development-test2095，最终blind2671。repo/HF写最终train15962+2095=18057，training_info同总量/19chunks/每chunk1000/完成2026-02-11；已并入训练的2095不能充作最终未触碰test。公开train_model缺外部eval时随机90/10，与最终chunk制品/1774dev关系未说明；按page/writer/年代隔离未证。专业底座卡当前列Muharaf/47,842样本/KHATT/English等，确认Muharaf线索；README Kitab/IAM与论文Muharaf/IAM并未完全对齐，不能把Kitab与Muharaf视同一数据。

## 指标与评价协议

CER=字符Levenshtein/参考长度、WER=(S+D+I)/参考词数(Eq3/4)，插入多时可>1。perline逐行后均值，与官方全文连接corpus评分/排序分开。作者提供两个排行榜，正式排名以CER为主；按行CER第一不推出WER第一。全部报告数未独立取2671隐藏GT/复算。

## 对比方法

最相关同专业HRT未适配.2032/.5031→单适配.0884/.2699；ensemble.0819/.2588进一步提升。organizer.591/.885 blind、test.584/.881为不同底座/条件，不能把从.58到.08全归LoRA。通用Qwen/不同QARI/GLMOCR比较有预训/提示/分辨率/适配差异。六模型集成对单模型还增加总推理成本，未见等成本采样/蒸馏对照。

## 实验条件和发布边界

RGB长边≤1024/Lanczos后各边向上32倍数，无额外增强/文本规范化；maxseq2048。AdamW fused2e-5/cosine/warm200/wd.01/clip1/b1acc4有效4/1epoch，seed42/eval-save500/NF4doublequant/bf16，配置与adapter元信息一致。公开trainer按eval_loss选best而AppD泛称CERmin超参选择，两阶段须分开。公开infer默认greedy/max512/repetitionpenalty1.1，README例未列此penalty，非全部论文run同设置证明。约8GBvs40GB为作者主张，未实测peak/总时/六模型总成本。

## 主结果

T1blind单适配CER.0884/WER.2699→ensemble.0819/.2588，分别相对约7.35%/4.11%；未适配同HRT.2032→.0884相对56.5%(.2032→.0819约59.7%)，不能等同对organizer的约86%。T2官方corpus .0938/.2996 CER第3，Misraj.079/.244第1；T3perline .0819 CER第1但WER.2588>Misraj.2516。T6developmenttest通用Qwen7B.6808/.9198与3B.6213/.8628，README把这两行放BlindCER表，论文明确无对应blind结果，须按论文保留test标签。T4 mergedLoRA.1834/.4644弱于非merged适配.0884，二者优化/合并设置不同，不能解释为LoRA无效。

## 消融及进一步实验

AppE30命名配置config18 .0819胜inverse .0884/exp .0856/rank .0871；weight_configs.py明确CODABENCH_CER来自blind提交六值.09/.11/.18/.20/.26/.32，已消除旧笔记“权重何split未知”的一部分疑问：不是完全独立dev定权。AppE还按blind选最佳，与AppD validation选超参分阶段记录；未知提交次数与独立终测。30配置并非30独特权重，18/21/29因阈.15/.12/.13均只boost前两项相同，23/28同boost1。rank<16underfit/32最优只定性描述，未给逐rank数值曲线；无DoRA/RSLoRA/量化/全参单变量等预算消融。

## 局限与疑问

全部11页4图10表5式/AppA–H完成。F2两短词/F3长行只提供挑选质例；F4绿线近0与总体CER.0819不宜直接等同全库，未给样本选择/原始点/CI。F2/3解释噪声鲁棒/长程能力仍是样例，F4把QARI退化归recurrent/attention饱和没有机制证据。T6/T8同名Qwen/QARI数值/标签大幅差异，T8未注明足够split/预处理口径；CER>1可合法，不因此否定T8。H PseudoGT来自ensemble自身，只证明模型间分歧/循环可见，不能独立证实全部修正或用总体<10%保证每例可靠。T9/10原稿实际视觉看过，阿文乱码抽取未逐字采信；未独立历史正字校勘。 底座卡声称47,842训练样本及商业OCR优57%/DynamicEquilibriumTheorem，但未在本次获得独立测试manifest、正式定理假设/证明；这些不作为Ketaba可验证理论或分布外性能证据。

## 预期优势条件

存在相关专业HRT预训练、目标稿域偏移且显存受限时，PEFT可降低转录误差；多模型候选互补且校准独立时文本共识可能再收益。公开融合最终总返回已有某候选原文，规范化只分组，不会一律去附标，也不会凭空拼出新完整转录；错误同向时无法保证修复。

## 可证伪实验

独立dev定底座/超参/权重，冻结后blind一次；按page/writer/年代隔离，匹配数据/预算做LoRA/DoRA/RSLoRA/NF4/fullfine单因子，比较单模型等成本采样与六模型。报告micro/macro/连接协议、各行长度/噪声分层和正确字形/词界/附标；专家独立转录争议行替代PseudoGT循环证实。对循环/截断给真实GT错误率，图4公布原始点/筛选。若用于video奖励，加入可识别但笔顺错误/缺笔反例。未执行。

## 论文组织与Claim学习

先定义任务切分/真值可见性与聚合再报排名；domainHRT起点和organizer差异要拆，不能把约86%写成PEFT纯贡献。测试集定权/选配置需显式披露，30标签与独特比较数区分。PseudoGT只用于分歧分析，模型卡商业对比/理论称号不能替代独立实验。正文与README中test/blind、底座数据名称同步。

## 实际阅读范围

ACL正式11页pp160–170全部§1–7/Ethics/致谢/17条references清单及关键引文/AppA–H全含F1–3/H1–2；F1–4全部实际视觉、T1–10逐表含阿文样例页面、Eq1–5逐式；4contact全看并框架/长度图/伪真值页放大。固定repof1aefa8 README全文/YAML/adapter/training_info全文，train_model/preprocess/load/apply及ensemble完整advanced/weight_configs源码；inference指定参数，非全仓审计。固定HF7f55602 card与repo正文对照，底座a404b5b卡元数据/来源/结果/理论主张段审。未取数据/权重、未模型或OCR/训练/外部API执行；核心三遍和五书面完成，非隐藏GT复现或阿文史料校勘。

## 权重来源已补证

公开weight_configs.py明确把六个CER标为CodaBench submissions，文件名也对应blind输出；AppE选择blind最佳30命名配置。因此旧笔记中的权重来源疑问已有部分答案，仍无独立最终留出集证据。18/21/29对现有六CER产生同一权重，不能把30标签称30独立方案。

## 适配与排名

同HRT基线到单适配CER .2032→.0884为约56.5%相对下降；论文约86%比较涉及不同organizer基线。官方corpus排名第三，逐行CER第一，逐行WER则劣于Misraj。README将部分仅test通用模型分数放入blind表，正式论文Table6明确无blind值。

## 真值与规范化

PseudoGT由ensemble自身产生，H附录可供观察分歧/重复，无法独立证明每次修正正确。规范化为投票分组服务，返回已有候选原文；源码共识用SequenceMatcher相似率而非标准Levenshtein，不能把其名称当精确编辑距离优化。
