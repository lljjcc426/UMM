# Transferability：完整评分解析、检出覆盖率与分布漂移审查

第一百八十四批完成[U18](../reviews/U18.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/transferability_full_parser_coverage_and_distribution_shift_audit_2026-10-24.json)。358目录（331论文／研究、27资源），289核心/294书面含未通过项；待完成核心深审42篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2607.04423v2)、[主源2](https://arxiv.org/html/2607.04423v2)、[主源3](https://arxiv.org/pdf/2607.04423v2)、[主源4](https://cvlab-kaist.github.io/UMM_Transferability/)、[主源5](https://github.com/cvlab-kaist/UMM_Transferability/tree/d5be8ea6039f25756e50da8aacb3d5e14abcf54e)。

## 研究问题

对UMM只用某一能力的理解或生成监督微调，在另一任务测试同能力，能否测到跨侧迁移？如何用理解监督改善计数、对角空间关系和字图生成并减少原生成分布漂移？研究单侧posttraining，不把共享接口或静态字图视作笔顺/视频能力。

## 现有不足

一般榜单上涨混入数据量与正则效应，难定位共享能力。直接生成微调可能偏向狭窄训练图分布，理解监督是否能在同图源下以较少漂移获得生成收益？其干预在每个模型内支持微调效果，跨不同模型/架构的差异尚未因果隔离。

## 贡献

四代表架构计数双向单侧LoRA对照；LuminaDiMOO三个能力的直接训练/跨侧训练、MMaDA复核两能力；比较基线分布FID/IS、文字多指标、一般理解保留；joint动态、固定步数rank消融、计数+空间组合实验。无新tokenizer/基础骨干/扩散目标；主要贡献为迁移实验与一种后训练策略。

## 输入、模块、输出与公式

Und:图+计数/四选对角关系/OCR指令→文字数值/选项/原句；Gen:同源图的计数/空间caption或固定Mathpix式目标句prompt→静态图。分别训练Und或Gen，只在另一侧测试同能力，和baseline/直接同侧训练比较。计数GenEval风格90prompt×4seed=360图；空间100prompt×4=400图；文字250句，GLMOCR转录后比GT。无编号公式；transfer strength文字定义为Δtransfer/Δdirect，同方向按高低优劣换符号。

## 模型结构

代表SharedTransformer+UnifiedVisualEncoder LuminaDiMOO8B，shared+separatevisualencoder JanusPro7B，MoT BAGEL7B，separatetransformer BLIP3o8B；补MMaDA同共享架构/离散diffusion。前两共享层不等于其视觉先验和生成目标相同：JanusAR，Lumina/MMaDA离散去噪，BAGEL/BLIP连续生成路径。在transformer Q/K/V及MLP加rank128LoRA，encoder、projector/aligner、LMhead和diffusionhead冻结；BLIP只调相应任务branch。名义7–8B不能保证total/active params/每token FLOPs等同，且不是同一初始化只替换架构。

## 数据分布与划分

计数65.6K图/约200K QA，PixMoCount/Points train按点数≤20筛；Gen同65.6K图，Qwen3VL根据标注caption，目标prompt可能多对象密集，T8四例含指/人/衣物多计数。Undtest540QA。空间200K：ImageNet1K两不同类图裁片置512²随机底色，各边150–300近方形不重叠，四对角各50K，10QA模板；Gen同源图+Qwen3VL描述；Und250validation转固定四选项，Gen100COCO类prompt。文字agentlans/high-quality-english-sentences train前200K，换行转空格/trim/截120字符，渲染单个H1标题，非完整复杂Markdown文档；Und随机clean_light/dark/sepia/blue_gray四CSS，Gen只clean_light，因此同句来源相同但图像样式分布不完全一致；test前250句重渲染clean_light。未公开精确样本清单/模板seed/字体版本。

## 指标与评价协议

计数exactmatch和MAD；Und先解析**数字**，失败再检查GT数字或英文数词是否出现在全文，GT依赖fallback并非独立抽取预测，多数字/解释输出可能得分，MAD遇不可解析如何计未说明。空间按检测框中心横纵符号判四对角，若任一物体未检测到就排除，因此准确率条件于检出，必须报coverage和全400失败计错版本。文字GLMOCR后小写/换行空格/trim，WER/CER/editdistance/BLEU/METEOR/tokenF1，大小写精度和版式未度量。FID参照baseline生成图而非真实分布，度量漂移；同图集对自身FID理论0，T11把baseline—称undefined并非数学结论。IS受类别/可分类性影响，不单独代表美学。

## 对比方法

四模型各baseline、Und→Gen、Gen→Und；Lumina三个能力再加直接Gen→Gen/Und→Und和joint。MMaDA两个能力双向用于支持非单个模型特例，仍只2个共享架构模型。没有同初始化/相同预训练/视觉tokenizer/目标/超参的架构因子实验，也没有wronglabel/无关Und目标对照；不能由一族最强断言共享视觉编码是必要充分条件。BLIP和BAGEL也有Und→Gen增益，摘要looselycoupled little/none需保留实际6pp/5pp。

## 实验条件和发布边界

AppA8bitAdamW/bf16，rank128，15epochs加earlystop选best，各任务单独训练无额外balance。LR：BAGEL1e−4/动态resize；Janus4e−5/保长宽比pad384²；Lumina3e−6/pad512²；BLIP2e−5/Qwen2.5VL默认图处理。MMaDA完整优化配置、batch/LoRAalpha/dropout/seed、checkpoint选择数据/指标和有效步数/总计算未齐；若用迁移目标test选best会引入选择偏差，但未公开依据，不断言已泄漏。rank对照固定3Ksteps，故rank12853.6不等主表57.0；jointF8横轴画至35epochs，独立joint设置未充分说明，不能套普通15epochs。官方repo HEAD d5be8ea6039f25756e50da8aacb3d5e14abcf54e递归tree仅README1blob，全文读完，含标题作者paper/projectlinks，无训练/eval代码、数据/LoRA/rawscores或运行入口；不把Code按钮等同已发布可复现代码，亦不推断历史实现。未执行模型/训练/judge。

## 主结果

T1 Lumina计数Gen48→57/MAD1.11→.83，Und22→30/2.48→1.88；JanusGen38→32/1.46→1.55，Und37→38但MAD2.70→3.34，指标方向不一致；BAGELGen42→47/1.16→1.11，Und63→64/.65→.62；BLIPGen31→37/2.08→1.80，Und63→62/.54→.56。T2Lumina直接Gen也57但MAD.91，COCOIS baseline16.86/transfer17.55/direct15.29，FID31.47/52.51。T3空间67→74transfer/80direct，IS16.86/17.50/17.41，FID30.95/32.28（T11对应30.96，小展示差保留）。T4文字baseline/transfer/direct：WER.654/.641/.641，CER.362/.351/.367，edit36.812/35.636/37.312，BLEU.277/.274/.354，METEOR.403/.410/.533，F1.446/.452/.525，transfer5升1降且增益小，direct在BLEU/METEOR/F1更好但CER/edit更差。T5Gen→Und计数30/MAD1.88、空间67、OCRWER.118/CER.061，相应直接Und57/.89、89、.091/.042，三能力反向有收益但不追平直接。

## 消融及进一步实验

T6transferstrength计数Und→Gen100%Acc/140%MAD，Gen→Und22.9/37.7；空间53.8/21.4；文字WER100/28.9、METEOR5.4/27.6、F17.6/25.9。140%说明直接训练仅经验参照、不是真上界；文字反向更强只对METEOR/F1等，不覆盖WER。T7CountingPOPE86.7→86.4/MMEP1534→1492、TextMMBench90.8→90.5，MMMU57.7→62.0/61.3/61.3；故概括基本保留可，逐项无退化不成立。T10MMaDA计数Gen15.8→20/MAD3.44→3.23、Und38.7→43.9/1.16→1.07，空间Gen33→46.3/Und40.8→48.8。T11两panel6组任务模型均transferFID低direct，taskIS有高有低；计数Lumina7.93→7.88transfer/9.20direct、FID14.74/80.45，COCO空间17.50/17.41及文字18.03/17.51，两种微调IS都高baseline，不能说直接生成总会损质量。T12rank8/32/128在3Ksteps GenAcc51.9/53.0/53.6，MAD1.01/.95/.88，fullfinetune塌陷仅文字描述缺量化。T13计数+空间混Und后400组合prompt joint24.7→28.5，未给全部清单/每prompt图数/coverage，定义fractiontargetobjects不可擅自当prompt全条件成功率。F8曲线波动提示训练动态难兼顾，不证明所有joint无法双赢。

## 局限与疑问

每模型内单侧训练是有效干预，但跨模型架构与预训练/目标/学习率/分辨率和可更新参数同时变化，架构因果未隔离。计数fallback和空间排除可影响效应大小，缺raw/coverage不能修正。文字四CSS对单CSS使同源目标对照仍有数据增强差别；English单H1和casefold/OCR误差限制细粒度笔画和多语种解释。低FID到baseline仅证明较小分布变化；改变本就错误的基线分布也可有益，IS/精选图不替代盲评/真实参考和置信区间；FIDtask1.8K/2K、COCO1Kprompts的有限样本误差未估。F10仅一fivecups例、多head平均：Lumina去噪第2/64步，JanusAR生成结束，阶段不同且层号不同；正文写textquery/imagekeys与Janus因果mask下prompt不能看未来图token的惯常方向需源码澄清，可能索引/转置或额外分析pass，不能据图推已证明attention因果。无多seed/CI、训练/采样预算与checkpoint选择不足。

## 预期优势条件

可借鉴仅训练OCR/计数等理解监督改善生成而少偏向合成图风格的策略，尤其有大量理解标注但缺高质量生成图时。文字增益依指标/语言/格式而变，图中笔画可读不保证笔序合法；书写和素描视频应将状态识别→轨迹生成或下一笔规划作为共享能力，另评执行和时序，不能由English字图直接外推。

## 可证伪实验

Q1效果是否被评分/样式混杂放大：公开每图/题raw，计数使用不看GT的唯一预测解析，失败独立记错并报告歧义率；空间固定400总分母+coverage/条件分双报，人工核detector。OCR采用相同四CSS/同句同图增强，大小写敏感与不敏感并报，多OCR+盲人转录，按字体/长度/非汉文字与笔画密度分层；若提升消失则收缩迁移强度。Q2共享机制和少漂移是否必要：同初始化预训练与预算，交叉shared/separatevisualpath及LoRA可更新部位，等更新步/实际参数/学习率搜索，加入无关Und目标和错标签；checkpoint只在独立validation选。使用盲评/真实参考保真与任务正确率联合评，多seed及按promptclusterCI；attention统一生成阶段、mask/方向并做head/path干预。固定基线样本计FID及独立baselinebaseline误差，不以直接训练为理论上界；几何/轨迹任务另验prefix因果与执行笔序。均建议，未运行神经模型。

## 论文组织与Claim学习

先将synergy缩成同能力单侧迁移，再方法和多任务/架构对照，最后实用策略、joint和保留能力讨论，叙事清楚。主张需分每模型内干预与跨架构相关，抽象摘要不能盖过BLIP/BAGEL已有正迁移；正文FID语义应与附录较谨慎的分布漂移一致。直接训练经验参照不要称上界，全部指标与负结果都报告；检测排除、GTfallback、CSS差异和bestcheckpoint依据应前置。Code链接只有README时明确发布边界。

## 实际阅读范围

完整v2 42页研究正文§1–6及Acknowledgements、AppA/B.1–3/C.1–5/D/E；T1–13全部（T11两panel共14HTMLtable）、F1–13全部视觉及100空间prompt全文、T8四计数/T9八空间数据例；无编号公式，全部inline关系/ratio/LoRA训练条件已核。PDF交核GTfallback、排除/attention/FID措辞及图8至35epoch，全部图例/定性对照已看。官方项目页与固定HEAD1README全审，无可运行实现/数据权重；核心三遍/五书面完成，未独立口试/模型复现。

## 证据和指标边界

本文在每个模型内用单侧训练检验跨侧能力，提升具备训练干预依据。架构比较使用不同预训练模型、目标、分辨率和学习率，仍只能支持所测架构与迁移强度关联。

计数fallback依赖已知GT，空间漏检样本被排除，是论文明确协议。因官方repo仅README，不能验证历史实际执行比例或自行重算作者主表。数据样式四对一、OCR小写和有限测试分布也需保留。FID到baseline衡量漂移；直接训练的部分IS/文字指标更好，不能据较小漂移直接断言总体质量更高。

T12固定3K步和主表15epochs/best是不同实验；T11分布样本也与主任务测试不同，未将它们混拼。T6文字METEOR/F1偏反向、WER偏正向，报告依指标变化。追引LuminaDiMOO/MMaDA/Janus/BAGEL/BLIP、原生协同U17及文字/轨迹研究，不自动提升其状态。
