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


## 第六十四批补充（2026-10-21）

N10训练教师链Sora与T2I→I2V不一致，未核公开数据/配置/权重；N11缺UniPC步数、LoRA秩/target/预算，N12缺RePaint调度配置。资源未找到或未披露明确记缺，未用基础模型/相关工作的示例倒填实际条件；RePaint官方实现列后续补读。见[证据边界](../evidence/calligraphy_inpainting_and_video_text_evidence_audit_2026-10-21.md)。


## 第六十五批补充（2026-10-21）

已读RePaint固定8e2a055 README、face示例与指定scheduler/gaussian_diffusion路径：代码重构未全重评，实际keep mask/注入时序、NFE与参数字段需单列。未下载权重/核完整训练保存，示例不填充CalliPaint缺项；附本仓库stdlib理论审计脚本及输出。见[审计](../evidence/repaint_sampling_and_linear_theory_audit_2026-10-21.md)。


## 第六十六批补充（2026-10-21）

N13关联HF卡公开MIT标记/9.89GB，文件需接受访问条件并分享账户资料，未访问媒体或同意条款；作者项目静态文字已读，未播放原视频。N06未获黑盒训练/rewriter配置，N07结合R07字段/指标代码仍不等全部原轨迹审计。见[审查](../evidence/video_reasoning_and_handwriting_observability_audit_2026-10-21.md)。


## 第六十七批补充（2026-10-21）

U08关联Anole/BAGEL模型卡、Zebra18配置与代码bbf53c3已固定版本。HF计数合182384但未下载原样本；论文BAGEL1000步/脚本5000步，公开停止/转图实现与正文差异单列；卡许可标签与基模正文不一致保留。见[制品审查](../evidence/zebra_cot_negative_results_and_artifact_audit_2026-10-21.md)，不重复计独立论文。


## 第六十八批补充（2026-10-21）

G030官方仓库paper dd65516保留RNN原实验，main475e0bc为temporal-attention v1.5并改maze设置/指标；公开Drive checkpoint/mini数据未下载，机器人底层控制代码需请求。公开默认和recipe与正文36/48帧、GRU设置差异记录，不当全部run已复核。见[审查](../evidence/diffusion_forcing_theory_protocol_and_versions_2026-10-21.md)。


## 第六十九批补充（2026-10-21）

G038 GitHub530f8bf/HF0959def配套DFoT/BD/SD/FS/FT与VAE、I3D/RAFT、RE10K档案均有公开目录；Space9077cb7观察RUNTIME_ERROR仅在线部署状态。默认验证数非正式FVD样本数、warmup由dataset override、MC uniform_future与HG-f的ω−1实现已核，未下权重/大数据或执行。见[审查](../evidence/history_guided_video_diffusion_audit_2026-10-21.md)。


## 第七十批补充（2026-10-21）

L092配套GitHub4eb6087提供FINETUNE与decoder-only BLIP3o60K后续-o模型，作者报GenEval.85（正式.76），公开example freeze_llm=False不能当该配方；原HF4cc9763目录与JanusFlow HFba75944/代码1daa72f已核，未下权重。MIT/DeepSeek模型许可正文分列，代码prefix cache空list静态问题不当执行结论。见[审查](../evidence/janusflow_harmon_shared_representation_audit_2026-10-21.md)。


## 第七十一批补充（2026-10-21）

G027配套固定NVlabs/edm008a4e5包含公开checkpoint/FID统计/训练与数据工具；README/loss/预条件及指定配置已读。新ImageNet/原ADM各有reference统计，采样状态FP64而网络FP32/可FP16；未下载/反序列化权重或执行。见[审查](../evidence/edm_numerics_training_and_selection_audit_2026-10-21.md)。


## 第七十二批补充（2026-10-21）

L185配套无独立论文GPU/LoRA实现固定1958463与HF美学3941662/对齐23c5dc4已核；base快速启动SD1.5/lr3e-4与原TPU SD1.4全UNet1e-5不同；DGX美学/对齐200epoch、公开美学卡40×256/对齐200×256，不能全当50K主模型。见[审查](../evidence/ddpo_policy_surrogate_rewards_and_artifacts_2026-10-21.md)。


## 第七十三批补充（2026-10-21）

L001数据声明处理数据/实现需向作者合理请求，未当公开可下载/未发索取消息；L004官方源包仅TeX/图/模板、未含正文引用supp或训练实现，不能当开源训练配方。未下载权重/执行。见[审查](../evidence/ordered_recovery_and_layout_strokes_audit_2026-10-21.md)。


## 第七十四批补充（2026-10-21）

StrokeFusion官方GitHub4fddf5d训练/采样/metric与HF abe809b数据/检查点纳入原G024制品关联，不重复新增独立论文。HF仅license卡、无配置说明；公共代码已摘实超参并注明与正式split/归一化/采样/metric差异，未权重下载/模型执行。见[审查](../evidence/painter_and_strokefusion_feedback_geometry_audit_2026-10-21.md)及[制品JSON](../../data/strokefusion_artifact_audit_2026-10-21.json)。


## 第七十五批补充（2026-10-21）

Loomis固定GitHub与14B/5B HF LoRA纳入原L015关联。代码rank128/b1/AdamW与epoch20/8、train/test loader、HF许可/缺项及v3数据管线承诺对照README未发布实况全部记录，未索取/权重下载/模型运行。见[审查](../evidence/strokebank_and_loomis_painter_version_audit_2026-10-21.md)/[制品JSON](../../data/loomis_painter_artifact_audit_2026-10-21.json)。


## 第七十六批补充（2026-10-21）

MMaDA官方Supplemental仍有RL待发布声明，但新关联dLLM-RL 10b4fd1c有token exp差PPO，selected MMU样例SEEDBench/group16/独立随机mask/KLold，非原三任务完整协议。关联原L063去重，见[审查](../evidence/mmada_and_think_in_strokes_protocol_audit_2026-10-21.md)/[制品JSON](../../data/mmada_unigrpo_artifact_audit_2026-10-21.json)，未下载权重或运行。


## 第七十七批补充（2026-10-21）

关联L047固定CSV/字体/渲染/训练/评价/log，论文全动态集发布声明与官方15文件tree未见MP4/边界/checkpoint的差异，公开条数/字符/重复统计及split/清理协议；无新增独立论文或权重下载。见[审查](../evidence/nushu_and_stroke_seg_data_protocol_audit_2026-10-21.md)/[制品JSON](../../data/nushu_multimodal_artifact_audit_2026-10-21.json)。S007/S016继续与L184关联，6类加工/样例不能套10类原表。


第七十八批（2026-10-21）：补VD固定配置噪声/目标/空条件/已下线I2T2I及HF旧新权重；Emu公开32latent推理/数据采集配方、SFT图像不兼容断言与未发布训练代码，不新增论文计数。见[审查](../evidence/versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)和[单篇L075](../reviews/L075.md)、[L077](../reviews/L077.md)。


第七十九批（2026-10-21）：LaVIT-v2配套后续模型另加24.2M候选库/8K步，HF固定版本及低/高分辨率decoder记录；不另计论文，原训练/finetuning未完整公开。见[审查](../evidence/lavit_dynamic_tokens_and_version_audit_2026-10-21.md)和[单篇L079](../reviews/L079.md)。


第八十批（2026-10-21）：补UniFlow固定HF一步config与代码、quick_start目标错位/SSIM范围和完整训练未公开边界；不另计论文。见[审查](../evidence/uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)和[单篇L072](../reviews/L072.md)。


第八十一批（2026-10-21）：补TokenFlow固定量化/多轮采样/训练示例及HF许可元数据；公开示例与主训练条件分开。见[审查](../evidence/tokenflow_shared_indices_and_claim_audit_2026-10-21.md)和[单篇L094](../reviews/L094.md)。


第八十二批（2026-10-21）：MetaMorph固定代码、条件置零与视觉回投影、原权重/MetaCLIP及替代数据复现限制。见[审查](../evidence/metamorph_synergy_and_data_budget_audit_2026-10-21.md)和[单篇L090](../reviews/L090.md)。


第八十四批（2026-10-21）：记录固定Flux加载器、LDM配置和ControlNet模块证据；ComfyUI/WebUI只核用途，待独立制品审查。见[审查](../evidence/diffusion_efficiency_full_pipeline_audit_2026-10-21.md)和[单篇G023](../reviews/G023.md)。


第八十五批（2026-10-21）：固定v0/v1权重元数据、内部数据续训标记、默认引导/计时范围和训练脚本未定位。见[审查](../evidence/unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[单篇L076](../reviews/L076.md)。


第八十六批（2026-10-21）：Tora固定发布/训练样例、低显存配置成本、两模型元数据/许可；Tora2专门制品未定位，Wan玩偶LoRA候选待审查。见[审查](../evidence/tora_motion_binding_and_process_boundary_audit_2026-10-21.md)、[L034](../reviews/L034.md)/[L035](../reviews/L035.md)。


第八十七批（2026-10-21）：R12 Wan玩偶LoRA完整代码/config/依赖/作者VRAM表，无训练公开定位或质量对照；与Tora3仅项目展示不同证据。见[审查](../evidence/tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)、[G039](../reviews/G039.md)/[R12](../reviews/R12.md)。


第八十八批（2026-10-21）：主配置/模型卡文件名冲突、run.sh最终camera、不同底座发布与原表分开。见[审查](../evidence/motionctrl_camera_object_and_observability_audit_2026-10-21.md)、[L039](../reviews/L039.md)。


第八十九批（2026-10-21）：UIO2部分任务/S3与离线评测、AnyGPT固定训练/采样差异和模型卡/数据制品。见[审查](../evidence/unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)、[L058](../reviews/L058.md)/[L059](../reviews/L059.md)。


第九十批（2026-10-21）：固定SEED-X/UniTok源码/模型配置、三数据分包和首3条标注各包，未取媒体/权重。见[审查](../evidence/seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[L060](../reviews/L060.md)/[L061](../reviews/L061.md)/[G040](../reviews/G040.md)。


第九十一批（2026-10-21）：固定Word-As-Image配置/优化循环/视频输出；Strike项目仍Code(soon)。见[审查](../evidence/semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[L051](../reviews/L051.md)/[L052](../reviews/L052.md)。


第九十二批（2026-10-21）：DS-Fusion固定训练/采样/配置、HF Express首字符/四候选及UI条件，关联论文避免重复计数。见[审查](../evidence/dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[G041](../reviews/G041.md)。


第九十三批（2026-10-21）：MetaQuery固定训练/采样/curation及HF原/512数据；UnifiedIO推理配置和四模型下载入口，未取权重。见[审查](../evidence/metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[L062](../reviews/L062.md)、[L074](../reviews/L074.md)。


第九十四批（2026-10-21）：共享SEED526blob固定树、训练脚本/多数据yaml、tokenizer2和8Bsft模型卡/config，区别初版/后续与另训demo。见[审查](../evidence/seed_initial_llama_causal_codes_and_release_audit_2026-10-21.md)、[L078](../reviews/L078.md)、[L082](../reviews/L082.md)。


第九十五批（2026-10-21）：Box固定GH仅README，新增延迟/FLOPs/动态显存作者报告，代码/CR待发布；Timage有限检索未确认实现。见[审查](../evidence/timage_boxtuning_input_prompts_and_evidence_audit_2026-10-21.md)、[L053](../reviews/L053.md)、[L054](../reviews/L054.md)。


第九十六批（2026-10-21）：GH AutoConverter5blob与ObjectMLLM95blob、固定HF VMCBench dev/test、单题API实现/训练参数、未下载GoogleDrive制品和许可边界。见[审查](../evidence/autoconverter_objectmllm_benchmark_and_coordinate_audit_2026-10-21.md)、[G042](../reviews/G042.md)、[G043](../reviews/G043.md)。


第九十七批（2026-10-21）：GenEval固定af4902f代码/MIT与553metadata；top-confidence选择、额外位置角阈、汇总宏微/anysuccess差异。未下载权重/图像或执行生成检测。见[审查](../evidence/manzano_hybrid_tokenizer_and_geneval_measurement_audit_2026-10-21.md)、[L064](../reviews/L064.md)、[L071](../reviews/L071.md)。


第九十八批（2026-10-21）：两固定GH/HF、Qwen配置/采样/后端/显存与整段WAVdemo、Emu公开AR/DiDA待发布、CFG/seed/backend区别，代码卡不等完整训练流水线。见[审查](../evidence/qwen3omni_emu35_generation_scope_and_release_audit_2026-10-21.md)、[L065](../reviews/L065.md)、[L066](../reviews/L066.md)。


第九十九批（2026-10-21）：固定两GH/HF制品、quickstart教师差异、MCQ实际函数反例/37连续多真值、CV几何评分和demo参数；资源条件不与原表混用。见[审查](../evidence/xtc_imug_correctness_consistency_and_dynamic_history_audit_2026-10-21.md)、[L067](../reviews/L067.md)、[L068](../reviews/L068.md)。


第一百批（2026-10-21）：Unison固定GH/HF文本计数、judge231和模型配置、UGG回退/ME跨轮并集；VGAU公共driver/BAGEL调用与两manifest，原表与公开默认分开。见[审查](../evidence/unison_vgau_synergy_oracle_and_stop_protocol_audit_2026-10-21.md)、[L069](../reviews/L069.md)、[L070](../reviews/L070.md)。


第一百零一批（2026-10-21）：NExT旧HF与当前两代码线、Dream普通/美学checkpoint固定revision、缺独立卡与训练配置差异，均关联原研究去重。见[审查](../evidence/nextgpt_dreamllm_interfaces_synergy_and_release_audit_2026-10-21.md)、[L080](../reviews/L080.md)、[L081](../reviews/L081.md)。


第一百零二批（2026-10-21）：Emu三HF权重/目录和native推理路径；VILA256HF/RQ配置、8帧PNG、batch公式与内部数据可得性，制品关联去重。见[审查](../evidence/emu2_vilau_representations_icl_and_video_release_audit_2026-10-21.md)、[L083](../reviews/L083.md)、[L085](../reviews/L085.md)。


第一百零三批（2026-10-21）：CalliReader三个HF固定制品/卡/配置与CalliTrain卡误写及API行数差异；AWCV网站数据链接未等同完整VCRec代码；与主论文关联去重。见[审查](../evidence/callireader_awcv_recognition_order_and_release_audit_2026-10-21.md)、[L045](../reviews/L045.md)、[L046](../reviews/L046.md)。


第一百零四批（2026-10-21）：Liquid固定7B指令制品与LoRA/有效128/任务配比差异、部分WIP和内部数据限制；ILLUME后续制品不归原模型；两后续候选仍未新增主目录。见[审查](../evidence/liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.md)、[L088](../reviews/L088.md)、[L089](../reviews/L089.md)。


第一百零五批（2026-10-21）：X-Omni En/Zh/PT/SFT与LongText固定制品关联，10blob推理/评价非完整训练；prompt每语160、实评分无序召回/脚本适配。见[审查](../evidence/ugen_xomni_curriculum_reward_and_text_metric_audit_2026-10-21.md)、[L091](../reviews/L091.md)、[L093](../reviews/L093.md)。


第一百零六批（2026-10-21）：QLIP GH7blob/HF B16固定权重卡配置和分制品许可证；DualToken tokenizer训练loss/8卡入口已发、统一MLLM待发，不将论文/制品重复计独立研究。见[审查](../evidence/qlip_dualtoken_representation_and_cost_audit_2026-10-21.md)、[L095](../reviews/L095.md)、[L096](../reviews/L096.md)。


第一百零七批（2026-10-21）：MotiMotion固定规划/评价指令与MotiBench HF62条/98轨迹/来源许可，不重复计论文；Fluid项目GH404与uponacceptance边界。见[审查](../evidence/motimotion_fluidgen_motion_physics_and_release_audit_2026-10-21.md)、[L036](../reviews/L036.md)、[L037](../reviews/L037.md)。


第一百零八批（2026-10-21）：有限检索未确认RefTok原作者代码/模型卡，不能用自动文献列表当实际发布；不新增资源计数。见[审查](../evidence/reftok_reference_rate_and_stroke_access_audit_2026-10-21.md)、[L038](../reviews/L038.md)。


第一百零九批（2026-10-21）：DN固定官方主树只迁移说明；DA当前推理/指标/HF卡与343JSON轨迹包实际审查，训练主文件未见，不重复计论文/新增资源。见[审查](../evidence/dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.md)、[L040](../reviews/L040.md)、[L041](../reviews/L041.md)。


第一百一十批（2026-10-21）：TextVBench论文称released200manifest，有限主源检索未确认实际代码/数据入口，不冒充已审查制品或新增资源。见[审查](../evidence/textvbench_correspondence_and_metric_validity_audit_2026-10-21.md)、[L042](../reviews/L042.md)。


第一百一十一批（2026-10-22）：实际固定模型卡/训练推理代码/数据230+157文本清单/13×157公开数字审查，无权重/视频下载；不重复计独立论文或新资源。见[审查](../evidence/vitex_glyph_correction_and_release_protocol_audit_2026-10-22.md)、[L043](../reviews/L043.md)。


第一百一十二批（2026-10-22）：固定stageII卡/训练yaml和问答/图像采样，独立提示词资源553+300行文本统计；无权重/媒体/推理下载执行。见[审查](../evidence/unitoken_version_interference_and_prompt_protocol_audit_2026-10-22.md)、[L097](../reviews/L097.md)。


第一百一十三批（2026-10-22）：63树/四权重目录、evalyaml与50步/一步路径，HF旧示例和GH当前代码区分，无权重下载。见[审查](../evidence/selftok_bellman_gradient_and_release_audit_2026-10-22.md)、[L098](../reviews/L098.md)。


第一百一十四批（2026-10-22）：项目当前code/checkpoint跳转Selftok512/1024目录，不作480正式制品复现证据，无权重下载。见[审查](../evidence/ddtllama_formal_precursor_and_protocol_audit_2026-10-22.md)、[G044](../reviews/G044.md)、[L098](../reviews/L098.md)。


第一百一十五批（2026-10-22）：未定位UniCode²对应公开制品，HF论文关联0不证明未发布；不把论文页误记成模型权重。见[审查](../evidence/unicode2_codebook_theory_and_protocol_audit_2026-10-22.md)、[L099](../reviews/L099.md)。


第一百一十六批（2026-10-22）：固定Tuna2仓库原版cfg/train/inference/dataset选读；默认Tuna2不可混充原版，发布/复现边界保留。见[审查](../evidence/tuna_formal_version_synergy_and_release_audit_2026-10-22.md)、[L100](../reviews/L100.md)。


第一百一十七批（2026-10-22）：BitDanceTokenizer三配置/权重文件名已核，未下载；d32c128不自动等于本作三类MLLM权重；公共训练脚本TODO。见[审查](../evidence/uniwetok_binary_rate_and_release_audit_2026-10-22.md)、[L101](../reviews/L101.md)。


第一百一十八批（2026-10-22）：EvoTok训练脚本/模型模块选读，公开示例不对应主表完整配方；未定位相关权重链接。见[审查](../evidence/evotok_residual_depth_and_training_protocol_audit_2026-10-22.md)、[L102](../reviews/L102.md)。


第一百一十九批（2026-10-22）：HF四分片/decoder/VAE/teacher清单与代码配置已核，未下权重，公开为推理入口。见[审查](../evidence/unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.md)、[L104](../reviews/L104.md)。


第一百二十批（2026-10-22）：像素/R配置、JiT噪声/分母截断、模型与评测适配入口已核；完整内部配方/实际权重仍待核。见[审查](../evidence/tuna2_pixel_flow_masking_and_release_audit_2026-10-22.md)、[L105](../reviews/L105.md)。


第一百二十一批（2026-10-22）：项目页无已核运行代码/权重直链；SwAV SK函数为算法对照，不当成本作发布。见[审查](../evidence/representation_forcing_synergy_and_quantization_audit_2026-10-22.md)、[L106](../reviews/L106.md)。


第一百二十二批（2026-10-22）：原HYDRA发布不能代替X；X仅论文/作者说明/官方海报，未定位可核运行制品。见[审查](../evidence/hydrax_temporal_tokenization_and_editing_audit_2026-10-22.md)、[L107](../reviews/L107.md)。


第一百二十三批（2026-10-22）：真实GH/HF发布15.2B总参；F22/F18与四步toy/完整原训练区分。见[审查](../evidence/pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.md)、[L108](../reviews/L108.md)。


第一百二十四批（2026-10-22）：FUDOKI公开权重/embedding与推理入口；32/128/50步、CFG两前向、topk1与长度协议需锁定。见[审查](../evidence/fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.md)、[L109](../reviews/L109.md)。


第一百二十五批（2026-10-22）：公开脚本/配置、私有parquet省略、缺eval_hd.yaml和实际11.09B参数标识；未运行。见[审查](../evidence/lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.md)、[L111](../reviews/L111.md)。


第一百二十六批（2026-10-22）：HF8.081B元数据、SFT占位配置、两类MMU接口与采样CFG实际成本。见[审查](../evidence/lumina_dimoo_cache_selfgrpo_and_editing_protocol_audit_2026-10-22.md)、[L112](../reviews/L112.md)。


第一百二十七批（2026-10-22）：SenseVoice连续特征、GLM离散speech码、微调脚本与HF模型卡加载边界。见[审查](../evidence/omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.md)、[L113](../reviews/L113.md)。


第一百二十八批（2026-10-22）：16.322B主干、额外6B decoder/VAE、HF配置与两种decoder/CLI参数；SGLang消息版本区别。见[审查](../evidence/llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.md)、[L114](../reviews/L114.md)。


第一百二十九批（2026-10-22）：同名GH为gh-pages网页：192项静态资源/模板README，不将Code soon或网页许可视为模型发布。见[审查](../evidence/fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.md)、[L115](../reviews/L115.md)。


第一百三十批（2026-10-22）：HF预训/SFT/文本decoder与统计、外部RAE、公开Muon配方和GH/HF许可分别记录。见[审查](../evidence/multimodal_flow_chunk_codec_and_controlled_budget_audit_2026-10-22.md)、[L116](../reviews/L116.md)。


第一百三十一批（2026-10-22）：4/8B实际卡、三PT库/60K tar与文本viewer区别、当前main配置、NEXT制品分开记录。见[审查](../evidence/blip3o_semantic_flow_open_artifact_and_version_audit_2026-10-22.md)、[L117](../reviews/L117.md)。


第一百三十二批（2026-10-22）：六pth与外部底座、URL重caption、离线DC-AE latent、非商业许可及i2i开发状态。见[审查](../evidence/openuni_light_connector_template_shift_and_release_audit_2026-10-22.md)、[L118](../reviews/L118.md)。


第一百三十三批（2026-10-22）：分支冻结/RQhead/采样/六训练脚本，私有与占位数据、独立权重链接及根许可缺失的限定范围。见[审查](../evidence/unifork_alignment_neighborhood_and_fork_capacity_audit_2026-10-22.md)、[L119](../reviews/L119.md)。


第一百三十四批（2026-10-22）：三HF checkpoint配置/索引与8步蒸馏、外部PE和原生思考区别、T2I/编辑版本时间线及社区许可；未运行。见[审查](../evidence/hunyuanimage_native_moe_gsb_and_release_audit_2026-10-22.md)、[L120](../reviews/L120.md)。


第一百三十五批（2026-10-22）：原生18文件/diffusers24文件/HF数据仅3文件的发布边界，固定配置和RL默认与论文协议差异，未下载权重。见[审查](../evidence/deepgen_scb_multireward_and_benchmark_exposure_audit_2026-10-22.md)、[L121](../reviews/L121.md)。


第一百三十六批（2026-10-22）：固定模型组件配置、TextEdit数据与评分实现、GenEditEvalKit集成wrapper，发布推理和原训练/评分日志的边界。见[审查](../evidence/internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.md)、[L123](../reviews/L123.md)。


第一百三十七批（2026-10-22）：mamoda25固定推理制品/ByT5引号条件/权重ComingSoon和工程核发布边界，未下载权重或运行。见[审查](../evidence/mamoda25_moe_video_distillation_and_release_audit_2026-10-22.md)、[L124](../reviews/L124.md)。


第一百三十八批（2026-10-22）：固定训练入口/680MB格式样例/两HF配置索引、原U1少步LoRA局限及后续U1.5/Infographic/Interleaved版本队列。见[审查](../evidence/sensenova_pixel_mot_synergy_and_release_audit_2026-10-22.md)、[L125](../reviews/L125.md)。


第一百三十九批（2026-10-22）：MindOmni固定HF组合配置、stage1/2/RL脚本、unsupported任务名与内部数据依赖、cascade推理边界。见[审查](../evidence/mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.md)、[L128](../reviews/L128.md)。


第一百四十批（2026-10-22）：CoRL四HF数据实际声明量/字段，启动默认差异与额外TTRL投票/自选参考协议；完整TTRL trainer尚未精读。见[审查](../evidence/corl_joint_advantage_branch_and_reward_release_audit_2026-10-22.md)、[L129](../reviews/L129.md)。


第一百四十一批（2026-10-22）：PairUni固定源码0097f419/HFcomingsoon/占位引用，HPSv2.1/软文本reward与示例8000steps非正文1200。见[审查](../evidence/pairuni_pair_weighting_gradient_and_release_audit_2026-10-22.md)、[L130](../reviews/L130.md)。


第一百四十二批（2026-10-22）：UniCorn固定e3b4518d/HF5e8d1df7/UniCycleaa1cf81f，发布权重14.607B F32及model/ema索引差异，PersonaHub/seed来源条件。见[审查](../evidence/unicorn_selfplay_joint_objective_and_unicycle_protocol_audit_2026-10-22.md)、[L131](../reviews/L131.md)。


第一百四十三批（2026-10-22）：R3固定761b0b07含七训练/测试JSONL，GenEval12359train与553test交370；README权重指向BAGEL基座，独立R3/ITA未核到。见[审查](../evidence/r3_tree_rl_understanding_scope_and_prompt_overlap_audit_2026-10-22.md)、[L132](../reviews/L132.md)。


第一百四十四批（2026-10-22）：GvU8203768有280评测prompt、训练/生成占位脚本，无完整50K/GvU模型卡链接；GPT4.1写实协议和API失败计分入库。见[审查](../evidence/gvu_intrinsic_probability_reward_and_release_audit_2026-10-22.md)、[L133](../reviews/L133.md)。


第一百四十五批（2026-10-22）：LVRPO正文声称open-source，但本轮出链与有限GH/HF名称检索未核官方代码/模型/500K制品，维持证据边界。见[审查](../evidence/lvrpo_theory_reward_and_protocol_audit_2026-10-22.md)、[L134](../reviews/L134.md)。


第一百四十六批（2026-10-22）：UniCTokens固定代码新增cleaned Sync-R1路径，四专家部署待发布；本轮发现评分器接口/续算参数问题；HF卡头MIT与正文CC-BY-NC4冲突，原2025制品不等完整2026++。见[审查](../evidence/uni_synergy_dgs_theory_and_personalization_release_audit_2026-10-22.md)、[L135](../reviews/L135.md)。


第一百四十七批（2026-10-23）：官方代码仍03b07e7，README承认joint未完成；SIM/dual/配置与正式论文不齐，调试validate不代表全套评测。见[审查](../evidence/chinese_radical_joint_tpe_geometry_and_negative_transfer_audit_2026-10-23.md)、[L181](../reviews/L181.md)。


第一百四十八批（2026-10-23）：固定8c675f9仅README+三裁图+AWS，无模型训练/权重/正式评测；Unity与AWS框来源、parser转换和存储占位需补。见[审查](../evidence/strive_video_text_replacement_and_propagation_protocol_audit_2026-10-23.md)、[L182](../reviews/L182.md)。


第一百四十九批（2026-10-23）：cf31559固定代码/三语言配置，Drive称权重数据但内部未核；默认selfref可覆盖，eval入口/全局HWD/距离接口静态问题与文档不齐。见[审查](../evidence/constant_multilingual_style_quantization_and_evaluation_audit_2026-10-23.md)、[L183](../reviews/L183.md)。


第一百五十批（2026-10-23）：论文和有限检索未核官方STBridge代码/权重/数据；PickNano派生、teacher35B/judge122B及Gemini评价精确版本和成本需单独记录。见[审查](../evidence/stbridge_shared_target_alignment_and_causal_controls_audit_2026-10-23.md)、[L137](../reviews/L137.md)。


第一百五十一批（2026-10-23）：MATE脚本/config/候选记录声明以后发布，有限检索未核官方制品；UnifiedReward/AlignAnything/SigLIP精确版本需分别审查。见[审查](../evidence/mate_adversarial_pool_evolution_and_budget_audit_2026-10-23.md)、[L138](../reviews/L138.md)。


第一百五十二批（2026-10-23）：L139 abs称upon acceptance、Repro称released artifact，全文和有限检索未核官方config/CSV/manifest地址，保留声明与可获取性差别。见[审查](../evidence/gradient_conflict_metric_validity_and_causal_audit_2026-10-23.md)、[L139](../reviews/L139.md)。


第一百五十三批（2026-10-23）：PAM abs称待公开、Repro称supplementary position_probe.py；arXiv源码包22成员无该脚本/数据，有限检索未核官方代码；原Show-o脚本只定向阅读。见[审查](../evidence/position_gradient_attribution_and_lora_budget_audit_2026-10-23.md)、[L140](../reviews/L140.md)。


第一百五十四批（2026-10-23）：官方UniKE固定代码/九配置/HF全JSON已定向核；README最低48GB不当正式硬件，未下载权重/矩阵，下载35文件不等全库逐行读。见[审查](../evidence/unike_cross_modal_editing_and_artifact_protocol_audit_2026-10-23.md)、[L141](../reviews/L141.md)。


第一百五十五批（2026-10-23）：固定UniEval核心与Janus/Showo/UniToken/Qwen/FLUX/DALLE包装定向核、UniBench全JSON；FLUXdev四次均seed0，资源建议不当正式硬件，元数据审查不计推理。见[审查](../evidence/unieval_self_evaluation_identifiability_and_answer_bias_audit_2026-10-23.md)、[L143](../reviews/L143.md)。


第一百五十六批（2026-10-23）：固定Uni-MMMU31成员目录/8选择性源码、完整HF卡；1026549760B归档未取，卡sft/grpo声明与外部文件树区分，A100建议非正式A800预算。见[审查](../evidence/unimmmu_state_parsing_oracle_length_and_synergy_audit_2026-10-23.md)、[L144](../reviews/L144.md)。


第一百五十七批（2026-10-23）：GENIUS固定GH10成员/5全文本、HF762成员/五JSON五viewer，510例但VC可启用270；复制检测为VLM判断，最长边1024/JPEG80影响细线。见[审查](../evidence/genius_contextual_rules_attention_theory_and_metric_tradeoffs_audit_2026-10-23.md)、[L145](../reviews/L145.md)。


第一百五十八批（2026-10-23）：新增深审WISE_Verified无独立论文维护制品：固定脚本/二值评分/120类配比，Prompt与ID变化、merge按ID一致；API部署示例非正式硬件成本。见[审查](../evidence/wise_gold_explanation_verified_protocol_and_knowledge_validity_audit_2026-10-23.md)、[L147](../reviews/L147.md)。


第一百五十九批（2026-10-23）：深核ImgEdit HFJudge卡/配置、37parquet清单及八ComfyUI模板；后处理入口参数数目/UGE输出解析不齐，裁判权重不可当E1权重，未下权重。见[审查](../evidence/imgedit_dataset_versions_score_gating_and_pipeline_reproducibility_audit_2026-10-23.md)、[L148](../reviews/L148.md)。


第一百六十批（2026-10-24）：KRIS GH/HF标注共有字段只两处标点/大小写差异；HF另有中文字段。发布评价脚本用浮动gpt-4o，解析/专用分支与正式协议分开记录。见[审查](../evidence/kris_knowledge_hint_calibration_and_released_protocol_audit_2026-10-24.md)、[L150](../reviews/L150.md)。


第一百六十一批（2026-10-24）：固定MMIG GH/HF版本与zip索引；官网正确数据入口与GH旧MMGen README链接分开记录，发布宣传不作制品存在证据。见[审查](../evidence/mmig_ams_estimand_and_public_release_audit_2026-10-24.md)、[L149](../reviews/L149.md)。


第一百六十二批（2026-10-24）：MMIG正式主表覆盖与公开项目页/代码README不一致，应逐版本核。新增模型表值没有对应公开方面QA/评分制品。见[审查](../evidence/mmig_formal_version_delta_2026-10-24.md)、[L149](../reviews/L149.md)。


第一百六十三批（2026-10-24）：MME CSQ404扩展名/8主体名与AL260目录需显式映射，映射后均有HF候选，不误报缺664图；未下载全图核内容。见[审查](../evidence/mme_unify_temporal_metric_and_terminal_step_audit_2026-10-24.md)、[L142](../reviews/L142.md)。


第一百六十四批（2026-10-24）：固定CompBench GH六文件、HF卡train2905+multi_turn576行；存图640²/评分512²分列。全幅mask评分、union框和无权宏平均需明确；未下载3.8GB全图数据。见[审查](../evidence/compbench_region_metrics_and_released_protocol_audit_2026-10-24.md)、[L151](../reviews/L151.md)。


第一百六十五批（2026-10-24）：OneIG固定GH两CSV与HF两JSON逐category/id核2440提示无字符串差异；7 Q/D共1590提示25053问题。生成黑图补位与评分过滤须报名义/有效分母。见[审查](../evidence/oneig_text_metric_ranking_and_public_protocol_audit_2026-10-24.md)、[L152](../reviews/L152.md)。


第一百七十七批（2026-10-24）：ModalityDanceOmniR1 GH a10fbb3及两HF卡/配置、OmniBench数据卡清单已核；README端到端PeRPO和Zero合成待发布，yaml占位/筛选关闭，vllm只存预测无judge链。见[审查](../evidence/omni_r1_full_perception_reward_protocol_and_release_audit_2026-10-24.md)、[U11](../reviews/U11.md)。


第一百七十八批（2026-10-24）：GH dfc17dd10py/README、HF模型54dad66/数据b7d16e7清单配置和test.json已核；缺训练recipe，评测配置接线/示例语法与未标GT回填需补。见[审查](../evidence/weave_full_interleaved_benchmark_scoring_and_annotation_audit_2026-10-24.md)、[U12](../reviews/U12.md)。


第一百七十九批（2026-10-24）：GapEval GH46树41blob/32yaml，指定三文件全文与judge重点分支/五yaml；HF622prompt全解析含nested897，未跑模型/fit或下载全像素。缺完整训练及历史raw联合计数。见[审查](../evidence/gapeval_full_bidirectional_information_scoring_and_release_audit_2026-10-24.md)、[U13](../reviews/U13.md)。
