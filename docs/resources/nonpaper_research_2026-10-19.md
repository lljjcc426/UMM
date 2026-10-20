# 无独立论文项目、模型卡与数据集：2026-10-19 核查补录

**发现规则**：arXiv/会议之外，同时查 Hugging Face Models/Datasets/Spaces、GitHub、原作者网页、训练 YAML、权重 adapter_config、评测提交和数据许可。记录单元为“实际发布的资源/版本”，即使该资源后来被论文引用，也要保存独立资源卡；切忌以 README 营销性表述替代测量。

| 资源 | 证据入口 | 实际输入→输出 | 与书写视频的关系 | 本次阅读层级 |
| --- | --- | --- | --- | --- |
| AnimCJK | [GitHub README](https://github.com/parsimonhi/animCJK) | Unicode CJK 字→语言/地区版本的 SVG 逐笔动画 | 规范化/方言对照及确定性渲染基线；没有学习型视频生成器 | 官方 README / SVG 示例 |
| KanjiVG | [GitHub README](https://github.com/KanjiVG/kanjivg)、[规范](https://kanjivg.tagaini.net/) | 日本汉字 SVG 路径、结构属性 | 日本标准约定下顺序/组件参考；跨语种必须核对顺序差异 | README、SVG格式规范与中SVG已核，见S010 |
| Qari-OCR-LoRA | [GitHub](https://github.com/HasanBGit/QARI-OCR-LoRA)、[HF](https://huggingface.co/HassanB4/Qari-OCR-LoRA) | 阿拉伯语手稿图→转录文本 | 低参数、多模型基座对照，**未提供视频生成** | HF固定配置/训练信息与README已核，见S011 |
| CASIA-HWDB2-line 的 HF 衍生版 | [HF 数据集](https://huggingface.co/datasets/Teklia/CASIA-HWDB2-line) | 离线汉字手写**行图像＋文本** | 静态 OCR/数据增强；公开衍生字段不能直接当在线笔尖序列 | 固定revision的image/text字段与split已核，见S012 |
| Hanzi Writer | [官方文档](https://hanziwriter.org/docs.html) | 汉字及笔画形状→预设顺序动画/练习 | 制作无生成学习成本的强规则基线 | 继承主目录 R01 |
| Make Me a Hanzi | [原始仓库](https://github.com/skishore/makemeahanzi) | 字符→有序 stroke 轮廓、medians | 生成事件标注、可控 SVG 渲染；中心线不等于真实压力轨迹 | 继承主目录 R02 |
| Ketaba-OCR-LoRA | [HF 适配器](https://huggingface.co/HassanB4/Ketaba-OCR-LoRA)、[代码](https://github.com/HasanBGit/Ketaba-OCR-LoRA) | 阿拉伯语手稿行图→识别串 | 论文现已在 NakbaNLP 2026 发表；模型卡继续作为独立可执行制品核查 | 论文+代码实核，见 [精读](../handwriting/papers/ketaba_ocr_lora.md) |

## AnimCJK：为什么必须有这个工程基线？

README 明确区分 svgsZhHans（简体中国用字）、svgsZhHant（台湾繁体）、svgsJa、svgsKo 等 SVG 目录，并提供 clipPath + CSS 动画示例。所读 README 中简体目录约 8,244 个、繁体目录约 1,513 个、日文目录约 7,336 个字形（项目持续更新，复现时冻结版本）。**同一 Unicode 在语言/地区间可以具有不同笔顺、方向甚至笔画数**：作者举例马偏旁与草字头在不同目录的差异。

- 数据用途：将标准动画转为 event timeline；按语言/规范层设置可接受序列；合成合法、交换笔顺、反画方向、同时落墨反例。
- 不可推断：SVG 动画有顺序，不代表轨迹来自真人手写；不能用其中某地区写法判另一地区“错误”。
- 需要审计：每一 SVG 是否有可导出的中心线与落笔/抬笔标注、矢量曲线的生成时长；仓库及生成 SVG 的许可证分别确认。
- 建议实验：把同一字在 svgsZhHans/Ja/Hant 的可用序列当交叉规范条件，测模型在指明地区时能否按给定序列执行。

## KanjiVG：日本汉字形体与结构的对照

KanjiVG README 标注 CC BY-SA 3.0；SVG 含 stroke/radical/element 等自定义属性，方便事件实例与部件对应。它为日本字形与部件研究提供可控数据，但**它的默认字形和简体汉字并不自然等价**，需分别保存书写规范、字符变体及地区标签。高价值变量是偏旁结构和形态复杂度，用于设计 unseen-component / repeated-stroke 测试切分。

## Qari-OCR-LoRA：同团队的非主模型制品

- 实际基座 NAMAA-Space/Qari-OCR-v0.3-VL-2B-Instruct；Qwen2-VL-2B 路线，官方称约 2.2B 参数。
- LoRA/DoRA/RSLoRA 适配器；作者 README 称约 37.6M 可训练参数（1.67%）。
- 原始 README 报告 blind CER=0.2635、WER=0.5521；这是作者提交中的辅助实验模型。Ketaba 论文也提到此对照，因此不可泛称“从未出现在论文中”。
- 核对事项：实际适配器配置、训练 split、tokenizer、重现 CER 的数据规范化流程；本文未本地跑模型。对汉字笔顺只迁移比较 PEFT 技术，不能作为视频生成 baseline。

## HF 离线/在线字段错配：CASIA 衍生版是反例

HF 名称中 HWDB2-line 易使人误认资源“有时序笔划”。这个衍生页面公开的是行图/对应文字，无证据表明每条包含 ordered (x,y,pen_state) 轨迹；研究汉字笔顺应另查原始 **CASIA-OLHWDB 在线数据**与采集许可、设备和时间字段。离线数据可作为识别监督、字体分布或纹理素材，不能直接造出真实历史。不要把无法从最终图像唯一反推的顺序假设标成真值。

## 资源复现卡必填字段

资源名+作者、精确版本/commit+HF revision、链接、输入输出接口、底座和适配器依赖、公开权重与否、数据集/字段/许可、训练脚本和默认超参、作者指标及统计口径、环境/VRAM、已测试/未测试、已知命名差异、可迁移机制及负面结果；新资源先登记，再进入“论文/工程项目”分类。

## 检索漏项的技术原因及修复

只搜论文标题会漏掉 HF LoRA/adapter、数据子集、API-only 产品、CJK 字形引擎和伴随模型。建议同时查：
- Hugging Face：handwriting、OCR、stroke、trajectory、calligraphy、Arabic manuscript、LoRA、video text 等 model/dataset/space 标签。
- GitHub：stroke animation SVG、brush drawing sequence、text video edit、writing video diffusion、dataset card、workflow YAML。
- 跨语种：Chinese Hanzi、Japanese kanji、Korean Hanja、Arabic calligraphy、Latin cursive、Indic script、Omniglot symbols；分开按语言对应笔顺标准。
- 逆向参考：视频文字论文 Related Work、工具被引用的论文、论文 GitHub Issues 与 model card 的 base_model、数据卡 license/字段。
候选若只有名称或镜像，保留为“待确认真实来源”，不补虚构配置。只用该轮公开可访问信息，未下载受限数据或权重。

## 追加：高相关性的“正式论文之外”资料

### Calligraphy Bench｜直接影响汉字笔顺新颖性的基准

[Haize Labs 项目](https://github.com/haizelabs/calligraphy) 和 [Hugging Face 88 条测试样本](https://huggingface.co/datasets/haizelabs/calligraphy-bench) 展示了智能体用 tldraw stroke API 描绘参考书法，报告笔画召回、正确顺序、1–5 风格相似度及成对偏好分数。**它评估书法绘图动作，不能用其 77–82% order 分数表达整段 RGB 视频规范书写准确率。** HF Viewer 另显示 strokes_svg / medians 字段，待审计这些字段与评分器之间的信息通路。详情请看 [逐项研究笔记](../handwriting/papers/calligraphy_bench.md)。

### BCSS｜静态笔画 mask，与时序真值隔开

[BCSS 官方仓库](https://github.com/Rvosuke/BCSS) 与 [HF 衍生包](https://huggingface.co/datasets/Rvosuke/BCSS) 的来源关系已核对：作者 README 描述完整数据 **1,322 图、10,653 笔画**，但正式论文Table1分组数相加为14,766，差异未解决（训练/验证 1,022，外部测试 300）；HF 发布说明此处可加载的加工子集约 **1,212 图**，由 1,082 训练/验证和 130 外部测试图组成。两种规模必须带上各自版本，不要将 HF subset 误报为全文数据。HF实际是固定六类重叠mask，论文为十类；主要用于墨迹类别/重叠分割与视觉结构约束，单图 mask **不含真实笔尖的时间方向**。衍生数据许可证与源数据许可须分开核实。

### Wuji Writing VAM｜公开 video+action 联合写字权重

[Wuji Writing HF model card](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819) 清楚列明 Wan2.2-TI2V-5B 视频权重与 action_dit 动作流同时输出，输入人类头视角写字示范、机器人三视角图、54D proprio 与指令；输出短期三视角视频及 54D 动作。当前训练资源是**0–9 数字、487 teleop episodes、896 个人类参考视频 episodes**，发布 step-12500 训练日志只作当前快照。视频和动作的同步协同已有工程探索，仍缺中文字体规范/真实机器执行对照。详见 [单独模型卡](../handwriting/papers/wuji_vam_modelcard.md)。

### SceneDAPR 与 Quick, Draw!：真实素描过程先验

[SceneDAPR 官方仓库](https://github.com/DSAIL-SKKU/SceneDAPR) 报告场景素描与 stroke order、绘制时间等注释，数值为 1,399 场景画与 6,420 个物体级标注；可研究同一画面内多对象绘制顺序的事件边界，需要读取实际字段确认时间单位、实例归属和许可。Google [Quick Draw! Dataset](https://github.com/googlecreativelab/quickdraw-dataset) 提供用户画笔的时序矢量墨迹，尤其适合建构**在线轨迹基线与时序错误注入**，其物体类别绘制顺序不能直接当中文汉字规范。另有 [ark60/sketch-diffusion](https://github.com/ark60/sketch-diffusion) 个人 notebook 发布 8 层 transformer + 1000 步 DDPM/Quick Draw 子集生成序列素描及 GIF；需核 Notebook 的 train/test 分割、运行日志、FID/KID 数值，不能将 README 中示意输出当作已复现成绩。

### 额外的“看似相关、任务却不同”的工程与研究

- [VidSketch](https://github.com/CSfufu/VidSketch)：由用户**给定**不同时间的手绘草图和提示，生成场景动画。它处理“草图约束下场景动起来”，与“白纸上新增每一笔”训练标签不同。
- [MoSketch](https://github.com/jyliu-98/MoSketch)：静态多物体素描经实例/运动分解实现动画；所述 stroke assignment 是移动物体/线条控制，不证明汉字笔顺。
- [SketchEdit](https://github.com/CMACH508/SketchEdit)：自由手绘矢量 stroke 级的图像编辑；适合研究局部笔画身份与不误伤，尚不具备规范书写视频结果。
- [DiffStroke](https://github.com/CMACH508/DiffStroke)：稀疏草图引导的局部图像修改，与逐笔生成历史不同。
- [KAIST 课程 Sequential Sketch Stroke Generation](https://github.com/KAIST-Visual-AI-Group/Diffusion-Project-Drawing)：基于 Quick Draw 时序数据的公开教学任务和评价结构。适合作为实现学习材料，不可计为独立同行评审新方法。

上述各项均需进一步固定仓库版本、数据许可与实际训练协议。是否配套有正式论文请检查仓库指向并按 DOI/arXiv 合并研究，避免将模型卡、课程代码和同论文训练附件重复统计为多篇成果。

## 2026-10-20实际配置与源码追加

本页保留首轮发现过程；当前结论以[资源实现审查](../evidence/resource_implementation_review_2026-10-20.md)及[S007](../reviews/S007.md)/[S008](../reviews/S008.md)/[S009](../reviews/S009.md)/[S010](../reviews/S010.md)/[S011](../reviews/S011.md)/[S012](../reviews/S012.md)/[S013](../reviews/S013.md)/[S014](../reviews/S014.md)/[S015](../reviews/S015.md)/[S016](../reviews/S016.md)为准。已读取实际HF配置/字段、选定源码和保存输出；Qari多指标得失、VidSketch训练目标、sketch-diffusion编码/反向公式及测试索引复用均明确记录。资源关联论文不重复计数；本轮补独立Stroke-Seg论文[L184](../reviews/L184.md)。

## 论文关联代码与模型卡补查：像素/连续接口

本批关联到既有L102/L103/L104，未重复增加独立论文数。EvoTok tokenizer/生成训练脚本、HYDRA模型/配置/flow路径、UniCom最终decoder调用均已指定段落读取；两项HF卡提供权重组成与依赖信息。UniCom卡明确decoder-side FluxVAE；HYDRA需latentstats、YAML构建及额外Qwen依赖。完整运行/权重/训练配方未复现，详见[逐篇笔记](../reviews/README.md)与[专题](../evidence/pixel_interfaces_and_temporal_audit_2026-10-20.md)。

## 第十四批代码配方核查

Muddit公开train_unified.sh在revisiond048cf7设text_loss_weight=0，按当前脚本不能复现原文联合训练；代码采用cos随机mask和按mask率重加权CE，与原文密度记号需对应。Lumina-DiMOO revision81344e6当前imagegenerator只重采样剩余mask；MLcache为近似。ht_grpo子目录虽写稍后发布，根README已链接arXiv2605.16842，属于有论文配套工程，尚未在本批重复增加记录。详见[专题](../evidence/discrete_paths_and_flow_audit_2026-10-20.md)。

## 第十五批：模型卡与导出配方

BLIP3o8B模型卡公开数据checkpoint GenEval.83/DPG80.73/WISE.52，论文含私有数据版.84/81.60/.62。Mobile-O有公开iOS app/export.py与模型/训练资源；本批未重复增为独立论文，导出LLM默认4bit、visionFP16、DiT/VAE/MCPFP32。论文LLM8bit/视觉FP32及<2GB口径需复核。HunyuanBase/Instruct/Distil按任务区别；TMP已有论文。见[专题](../evidence/open_models_and_deployment_audit_2026-10-20.md)。

## 第十六批：加载配置与公开边界

UniFlow官方配置实际num_sampling_steps为1，与Python类默认100/10的入口不同，按加载配置解释一步重建。Mamoda2.5已公开说明/代码入口，指定revision权重仍Coming Soon，不能写成已公开权重。Rosetta训练demo100step与全规模300B/100M训练分开。以上均关联既有论文ID，不重复新增独立论文。

## 第十七批：训练配方实物核查

HermesFlow4997368 train_pairdpo.py549–554用两DPO加权和，和正式/预印本乘积公式不同；YAML50Ksteps/b1/warm5K与论文3K/b4也分记。GvU8203768 run_grpo.sh包含8进程、LoRA8α32、group2/lr1e-6/β.03，但dataset占位不提供论文完整数据配方；gvu_score/TRL trainer已选读，不把存在脚本写成复现已通过。均关联既有论文，不新增重复资源。

## 第十八批：SyncR1发布制品与论文差异

[官方9ca4254子目录](https://github.com/arctanxarc/UniCTokens/tree/9ca4254c4e94dce82f0fe0e131f27632f89424a2/sync_r1_grpo)实际依赖根models/training/llava、原始模型/CLIP/FaceNet权重和逐概念UniCTokens阶段2checkpoint。grpo.py记录每步全图token并按sum做DrGRPO；DGS筛选用CLIP图/文分的.65/.35组合，阈值代码为target−observed后指数与±.005步变动，和论文动量控制式不同。其含义是存在可审实现；未验证能直接重现论文表格。资源关联L135，不增独立论文数。

## 第二十五批：配置与checkpoint属于研究证据

[本批审查](../evidence/glyph_conditions_paired_benchmarks_and_structural_targets_2026-10-20.md)核WriteLikeYou固定model.py：默认风格4层/20GMM/cycle0，论文3层/λcycle5；均值cycle与随机完整生成要分开。GlyphControl README区分10M与额外TextCaps5K40epoch版本，后者开放原decoder且承认多样性损失；主YAML是resume warmup1，不能当从头10000配置。TextDiffuser README b24/acc4需8卡才对应768。以上为已有论文的配套制品，不增独立论文/无论文资源计数；HF模型卡和权重未取得/执行，不以README指针宣称完成权重复核。

## R08：U1.5八步LoRA与配置资源

新增[逐资源分析](../reviews/R08.md)，官方HF的8step/V2适配器没有单独论文，关联U26基础报告但单列实验条件。核中英模型卡、实际文件名、Apache2.0声明和加载合并代码；不下载权重、不把基础榜分数赋给V2。旧8step文档说训在SFT，V2卡指向final；两版不能混。CFG与步数的推荐不同，100NFE/8NFE应与50/8 solversteps、真实延迟区分。

## 第二十八批：公开制品不等完整论文实现

UniCalli固定README只勾选无pred_box base/生成推理/量化/数据，识别推理和训练未勾选；OnOff固定树仅2文件，仍为code/data coming soon。DeepCalliFont已公开训练脚本和配置，默认值不自动代表论文全部实验。Ketaba有正式ACL论文，同时HF适配器配置/训练信息独立核查；不可再归无论文工作。具体版本与范围见[专题](../evidence/calligraphy_video_text_order_and_ocr_protocols_2026-10-20.md)。

## 第二十九批：数据卡、公开实例与推理入口交叉核

Calligraphy Bench官方卡与公开88行不完全一致：82个不同Unicode字符、18个书家标签，39行declared stroke count与SVG/中线条数不同（SVG与中线条数一致）。这些是可复查元数据差异，尚未证明judge实际误计；每行见[审计JSON](../../data/calligraphy_bench_metadata_audit_2026-10-20.json)。CoFRIDA-Sharpie YAML与正文列两个不同base，未下载权重，无法判定实际base。VidSketch公开代码计算abstractness却未把分数接入pipe参数，不把论文的自适应机制自动等同当前公开入口。见[专题](../evidence/unified_video_static_text_sketch_and_resource_mismatches_2026-10-20.md)。


## 第三十批补充

新增[R09 Datumwell公开10例](../reviews/R09.md)：模拟状态/五维计划关节action/多视角RGB及原生约3Hz→50Hz保持协议。审卡/metadata/loader，未下载完整轨迹视频或运行policy。尚未定位独立论文，权利边界保留。


## 第三十二批补充

DiffMath固定ec4aa2c树仅README，代码未发；SDT固定ba1da57默认配方与论文不同且Tamil未同等提供；StrokeExtraction固定2d273e0提供RHSEDB，CCSEDB未见同等下载。论文存在不等配方/数据完整发布，也不能仅因资源有仓库名就判可复现。


## 第三十三批补充

KineTy模板版权限制完整584K数据分发，公开构建需许可模板/AfterEffects/Nexrender；DynamicTypography默认参数/运行显存和loss权重可查但逐prompt优化；AnyText2与InversePainting默认训练配置不同于论文。InversePainting HF权重与sample_data不等完整294视频发布。


## 第三十四批补充

Show-o2固定45a5a2d README视频理解已发，T2V/I2V/mixed-modality生成权重仍TODO。ReCA固定99ebefe复现指南提供分辨率/瓶颈/冻理解训练经验，Harmon示例50K不同论文5K；BAGEL示例集不等完整预训集。HF量化/ComfyUI存在不自动证明原精度和速度相同。


## 第三十五批补充

固定UniCache800fca9区分torch动态预算fakequant与engine固定type预算/冻结H2O，默认editing量化位宽与group不同；FlashU189f877配置35步/末11full、README旧API和VAE占位需核。Reflection0f4a135公开SFT/RL入口、HF fullweights和数据卡：29529轨迹/1265anchor，数据research-only，GEdit174例应从对应评估训练中去掉；未下载权重/大数据。


## 第三十六批补充

固定Hunyuan60783e7 SSTA实现OR对论文AND、公开Muon/LoRA r8/alpha16续训模板需自建loader；WanMove80c58a7时间sample对paper average，MoveBench d02e0c4含en/zh/首帧mask/track/visibility/eval入口。原LTX19B HFdfcc210有8stepCFG1蒸馏/LoRA384及VAE/connector config；当前Git e98f6d9已2.5/22B/Gemma4且LoRA模板r32/AdamW1e−4，不能混成原预训。VACE48eb44f及HF benchmark c70300e分开发布版本/许可。


## 第三十七批补充

固定SF33593df/HF2f8b779、SGF79be9ac/HFffaf490、Salt5fbb513/HF07877f3的模型、初始化、prompt和公开训练配置关联D05–D07，不重复计论文。SF global64/600iter、SGF global8/frame1500/chunk1200与可运行显存不混作原全部实验；Salt TRDmargin.1/weight.1/start700对正文600，CF EMA/LL regular generator、license other及LongLive非商用文件。WanR1官方代码模型入口未定位，不猜URL。


## 第三十八批补充

MF固定d70cb55 JAX/TPU与B4发布checkpoint/FIDstats，另有作者py-meanflow/pMF入口待单独读；iMF官方bf60cd7与HF fbc11eb目录含JAX/full/PyTorch权重/两套FIDstats，API无README/license元数据，不能推MIT权重许可。SGF+固定7a7734f/HF784c078含两全参数frame/chunk与SGF诊断generator+critic，64GPU/1900或700参考steps、max2000配置分列；110GB诊断worker/CPUoffload和单B200 Reactor为工程协议，无独立实测。关联已有研究，不重复计资源或论文。


## 第三十九批补充

关联E04：facebookresearch/flow_matching固定11568d37，后续Guide库FineWeb-EDU/WikiText103示例、1Msteps/8H100/AdamW配置，采样1−exp跳转与原论文δ+h·u分列。关联E05：Git2f866649与HF84e5a410，Base1200K/v1 1250K/BigVGAN/no_zero_init权重清单，MIT代码与CC-BY-NC-4.0模型分列；只读卡/配置不下载权重。关联E06：ali-vilab/TeaCache7c10efc，opensora四阶系数、首末强算/残差/阈值与VBench/参考指标协议，Wan等适配待逐个审查。关联E07：jocpae/clDice47d31a6，PyTorch实际num_iter10与iter_接口不一致、hardmetric P/R命名对换但分数对称；未运行。均为配套制品，不重复计独立论文/资源。


## 第四十批补充

配套制品不重复计论文：diffvg85802a71（Apache2.0）读wrapper/use_prefiltering、弧长采样pdf和VAE/GAN关键配置，须结合官方Eq6/7勘误。Bezier9612a228（MIT）读gsplat依赖bcca3ec、Adan/剪增500步与正文差异、full_eval SSIM和导出helper；逐层代码README仍TODO。FRIDA ICRA2023 tag df3f06f（GPL3）与ICRA2024 CoFRIDA tag1bf0205分开，原3参数→12编码、RMSprop规划与Adam笔触拟合；CoFRIDA冻结VAE/text、UNet全参MSE/AdamW8bit发布脚本及额外数据过滤已核。当前HEADf42fa618不替原实验；train_lora与HF权重卡仍待补，不据仓库同名认定已精读/运行。


## 第四十一批补充

H001模型卡SDXL字段与rank256/cross768 metadata不一致，官方加载为timbrooks/IP2P+canvas；当前Frida f42fa618 train_lora rank32/无canvas forward，不在ICRA24标签，不能绑定该HF权重。基础config固定31519b5/06653d4，权重仅读512KiB元数据，无执行/全下载。Magenta c15687e默认小LSTM/点drop等不同v2论文，LearningToPaint615c070预训练renderer/actor链接和FFmpeg过程视频是制品证据，未运行。


## 第四十二批补充

G016官方Paddle a5ceece当前五维预测+采色、serial更新与论文八维/速度表分开，未取得训练代码。G01792262f7默认500iter与论文约2000分开。F06e7a66b2含PyTorch命令/renderer和不同当前模型，未运行；F07google-deepmind5ee538c的19步无条件TFHub制品不等正文20步conditional。均关联论文，不再增加独立论文数。


## 第四十三批补充

DDPM官方1e0dceb TF1.15/TPU默认与loss选段；Score-SDE官方JAX0acb9e0配置/权重发布边界，个人资源重训制品和论文检查点分开；RF5a1fd4d普通/reflow/distill EMA.999999/.9999/.9999、uniform-L2和t0-LPIPS、A100环境与1M建议分开记录。FM后来官方library关联已有条目，未称2022原代码。无权重下载/执行；配套代码不重计独立论文。


## 第四十四批补充

新增[R10](../reviews/R10.md)：固定HF sd-vae-ft-ema/f04b2c4和sd-vae-ft-mse/31f26fd卡、API与config；decoder-only／两者EMA／未公开LAION-Humans／缺完整训练超参，重建rFID与DiT生成FID分开。另记LDM eval YAML非论文训练lr、DiT默认前三latent噪声通道CFG／MSE+CFG4、CM CT命令带teacher参数且初始化复制、DPM代码默认++；均未执行。


## 第四十五批补充

固定AD e92bd56：train.py名称筛选/冻结/AdamW和时间重排实现、v1 train/image-train与v3 infer配置；100步示例不等完整论文训练，image finetune全UNet不等domain LoRA。v2 motion453M与MotionLoRA19M/74MB（prose77MB）不替换原论文约30M storage不明单位。VDM作者不发模型，VideoLDM原项目本次未定位完整检查点；SparseCtrl/SVD另归独立工作，未下载权重。


## 第四十六批补充

新增[R11](../reviews/R11.md)：固定CogVideo7a1af71微调默认/关键实现与HF2B1137dac、5B8fc5b28、1.5fdc5267卡/config。r128/alpha64/QKV-out、AdamW2e−5、iid时刻，不当论文完整预训。latent尺度/时间patch/精度与LoRA/SFT/offload预算分版本；数据resize/抽帧、开发依赖及42GB/4090文档行问题保留。未下载权重或运行。


## 第四十七批补充

G013关联Wan2.1固定9737cba配置/关键实现：1.3B与14B不同维度/head；T2V50步/CFG5/shift5、81帧/16fps；1.3B README建议CFG6/shift8–12/480p。VAE逐通道mean/std、空负提示自动回填、T5 CPU/offload与提示扩写应保存。README新FLF2V/VACE制品不回填报告原版，衍生LoRA/量化资源尚待独立审查；不增加独立论文数。


## 第四十八批补充

LoRA/QLoRA/DoRA/rsLoRA原论文审查已补，但现代PEFT实现、量化/FSDP组合及训练脚本需要独立版本/默认值核查；不从库现默认补历史α/dropout或硬件。Ketaba S001和CogVideoX R11保留各自模型/代码协议，不能用四篇通用原理覆盖具体复核；本批不新增独立资源数。


## 第四十九批补充

ControlNet1.0官方ed85cd1所列教程/关键实现已交叉核：fill50k RGB归一化、单GPU/b4/lr1e−5/FP32、sd_locked；demo独立20DDIM/CFG9/附加与负prompt/guess权重。教程无显式50%prompt dropout，不能替原主实验；非论文工程默认纳入G025，独立资源数不变。后续Control-LoRA/新ControlNet卡与训练工作流仍需独立核。


## 第五十一批补充

第五十一批选读论文关联评价工程制品：[VBench固定代码](https://github.com/Vchitect/VBench/tree/fd18b3d055cb0fc6f066ca90fe2c3c8cbb698490)的dynamic/flicker/subject/background/constant与README指定章节、[GoogleFVD固定实现](https://github.com/google-research/google-research/tree/3ef52111c1fabc301880818f5a547570e926a76b/frechet_video_distance)的README/FVD.py全文。记录阈值/采帧/聚合、固定端点与权重、RGB/resize/I3D层/batch16依赖；未安装/运行、未全核外部库/权重。见[工程细节](../evidence/video_evaluation_vbench_fvd_protocol_and_scope_2026-10-20.md)与[G031](../reviews/G031.md)/[G032](../reviews/G032.md)，未另增独立论文或资源条目。


## 第五十二批补充

新增关联[ContentBias固定工程制品](https://github.com/songweige/content-debiased-fvd/tree/a1e037ab7cb087debd2221d14ae4a001ec054201)与[G033](../reviews/G033.md)：README/FVD/加载/统计全文和采样/时间插值选段。real=full/fake2048/seed42、数据不足重复、缓存seed0、SSv2微调checkpoint、不同输入路径/范围明确；未下载权重/运行。论文及制品关联，不重复增独立资源数。


## 第五十三批补充

关联G034的ImageSuite、I2V/trust评分源码、Long无独立论文工程文档：[固定代码](https://github.com/Vchitect/VBench/tree/fd18b3d055cb0fc6f066ca90fe2c3c8cbb698490)。355图元数据说明、人工两极bbox/crop脚本、采样/聚合/过滤/阈值及文档差异已核指定范围；未下载全图/权重或运行，Long仅README，见[工程审查](../evidence/vbench_plus_i2v_trustworthiness_protocol_and_implementation_2026-10-20.md)。不重复增独立研究或资源数。


## 第五十四批补充

G035关联HF VBench-2.0_human_anomaly卡、仓库JSONL结构、人体训练配置/README、实例滑窗推理、prompt改写首例和评分源码已读指定范围；无下载全图/权重或运行，LoRA训练全配方尚未取得，不重复计数。见[资源/协议审查](../evidence/vbench2_intrinsic_faithfulness_events_and_conditional_scores_2026-10-20.md)。


## 第五十五批补充

U01关联官方推理/viewer/prompts README已读，研究许可/模型需申请；HF原始卡401未读，不猜权重能力。U05 AppA VAE/VQ损失及训练条件已核，未取得完整官方训练配方/运行；关联材料不重复计数。见[资源边界](../evidence/chameleon_transfusion_shared_model_cost_and_claim_audit_2026-10-20.md)。


## 第五十六批补充

Janus原README的CFG tokenizer_config修复仅作者报告，原Janus与Pro/Flow分列；代码MIT不自动覆盖模型许可。Show-o原代码/三阶段配置已选读，RefinedWeb内部loader需替换，注释LM改变目标，不能称完整复现；配置loss1/.1/1及三阶段步数/seed已记。关联不重复计数。见[资源审查](../evidence/janus_showo_representation_video_and_math_audit_2026-10-20.md)。


## 第五十七批补充

关联InkSight公开Small-p卡/三模式InkML输出，HF卡TF2.15–2.17与较新仓库TF2.20/XLA工具分列；生成轨迹不作真实时序标签。VideoSketcher模型/数据HF API可访问并列制品名、无README卡；固定源码LoRA目标/repeat及I2V配方差异；未读zip/权重。见[资源协议审查](../evidence/inksight_videosketcher_trajectory_events_and_resource_audit_2026-10-20.md)。


## 第五十八批补充

固定SketchAgent14c4043的API参数/拟合/解析接口，当前temp0/top_k1与论文随机500例区分。固定ProcessPainterffeaa2c ARN配置256²/100K与正文512²/50K，AdamW与文中Prodigy、1–8条件与0–3分列；HF只有许可标签、数据仍待发布，未运行。详见[资源协议](../evidence/sketchagent_processpainter_protocol_and_claim_audit_2026-10-20.md)。


## 第五十九批补充

关联StrokeNUWA a52e1cc VQ/EDM训练例与FusedAdam主体，示例数据/1024维和主表512区别，环境与Hydra路径需运行对齐。PaintsAlter项目页仅链接PaintsUndo并标next version，不能直接以旧代码/权重称复现新论文。见[资源说明](../evidence/paintsalter_strokenuwa_query_representation_and_metrics_audit_2026-10-20.md)。


## 第六十批补充

固定DiffSketcher0319b29默认warmup2000/总2000，静态循环不启用ASDS，README800例亦未改；Font-diff44d29cf b16/属性维度分配与文章不同。已核选定配置/条件路径，未下权重或跑模型，不把公开示例等同精确复现。见[资源审查](../evidence/diffsketcher_difffont_condition_process_and_configuration_audit_2026-10-20.md)。


## 第六十一批补充（2026-10-21）

FontDiffuser两阶段launch与parser默认覆盖、SCR预训代码TODO；DiffBrush固定da9addc融合顺序/默认无CFG混合/5000FID与论文25K差别，yaml2000不可当实际800训练。均未运行。见[工程审查](../evidence/fontdiffuser_diffbrush_generalization_metrics_and_release_audit_2026-10-21.md)。


## 第六十二批补充（2026-10-21）

Emu3固定dbbf985 README/HFGen卡默认负提示含text、topk2048/CFG3与论文不同，SFT示例与正式QFT分列；预训/DPO/评测仍TODO。Janus固定1daa72f README Pro示例与默认旧Janus的根推理脚本、HF16K配置上限与论文4K实际上下文分别记录。未下权重或运行。见[发布审查](../evidence/emu3_januspro_versions_training_and_causal_audit_2026-10-21.md)。


## 第六十三批补充（2026-10-21）

AnyText固定3d4a260当前train.py为200K子集示例，v1.1依赖社区RealisticVision V5.0 noVAE，卡许可/外置VAE/采样/含text-sketch-drawing负提示已记录。UniVid固定98b5c425源码存在，当前hook/外部服务/缓存与论文不同，HF a9398c3只有adapter+training_state，无完整backbone或模型卡；未下/载权重或运行。详见[实现/资源审查](../evidence/anytext_univid_protocol_code_and_namesake_audit_2026-10-21.md)。
