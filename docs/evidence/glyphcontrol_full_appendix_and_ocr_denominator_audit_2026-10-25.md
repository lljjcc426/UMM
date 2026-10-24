# GlyphControl：完整附录、OCR分母与发布代码审查

第二百零四批完成[S003](../reviews/S003.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/glyphcontrol_full_appendix_and_ocr_denominator_audit_2026-10-25.json)。358目录（331论文／研究、27资源），309核心/314书面含未通过项；待完成核心深审22篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8951bbdcf234132bcce680825e7cb354-Abstract-Conference.html)、[主源2](https://proceedings.neurips.cc/paper_files/paper/2023/file/8951bbdcf234132bcce680825e7cb354-Paper-Conference.pdf)、[主源3](https://github.com/AIGText/GlyphControl-release/tree/5891d9b245ac9209c22e3d6d5e933b95d428a230)、[主源4](https://github.com/AIGText/GlyphControl-release/blob/5891d9b245ac9209c22e3d6d5e933b95d428a230/ocr_acc.py)、[主源5](https://github.com/AIGText/GlyphControl-release/blob/5891d9b245ac9209c22e3d6d5e933b95d428a230/ldm/data/laion_glyph_control.py)。

## 研究问题

给词、位置、旋转和字框，能否以字形空间条件控制扩散生成可读场景文字？

## 现有不足

纯语义prompt无法精确指定字母形状/位置，强语言编码器仍可能错拼；需要利用已有印刷字形而保留场景融合。

## 贡献

在SD2.0base加入渲染字形ControlNet，Pillow glyph instructions；筛LAIONGlyph10M，并用词频分层两基准。继承ControlNet/扩散骨架，未提出书写时间模型。

## 输入、模块、输出与公式

文本prompt与用户字形指令（位置、框宽、行数、旋转）→512²静态图；训练OCR取字并在白板渲染。字形条件不是实际手写轨迹，无视频输出。

## 模型结构

SD2.0base，冻结VAE/OpenCLIP/原UNet，trainableControlNet+ZeroConv注入glyph，噪声latent与caption同时进两支。F2图注写ControlNet随机初始化，§4.1明确两支copySD2base；主文与图注不一致，按§4.1/README初始checkpoint说明记录，未读weights验证。训练OpenCLIPYAML和T1CLIP354M亦比泛称OpenAICLIP具体。TextCaps开放原UNetdecoder为独立checkpoint；总1.3B不含文本encoder354M，也非1.3B全部可训练。无新编号公式/算法。

## 数据分布与划分

LAION2B-en美学≥4.5，PP-OCRv3，丢边缘字/文字总面积<5%/框>5，BLIP2重caption得10M；子集100K/1M/10M。SimpleBench单词标牌与CreativeBench场景模板，各四词频桶100词×4采样，模型主要英语。FID独立10K图。

## 指标与评价协议

训练OCR为PP-OCRv3，公开评分使用EasyOCR英文。Acc代码是目标字符串是否等于任一OCR检测文本，忽略大小写版本同理，额外无关文字不罚；并非整幅图转写完全一致。LD取所有OCR文本对目标的最小Levenshtein；ocr_acc.py行89仅非空OCR时update，未检测到文字的图从LD分母跳过，而Acc记0；test_on_benchmark.py确调用这些counter。因此LD并非无条件每生成图均值，跨模型漏检率不同会偏。1−WER的泛称也不适用于一般含插入删除WER。T1斜线Simple/Creative，另有CLIP/FID10K，不测规范笔顺或人类可读性一致率。

## 对比方法

SD2/SDXL/DeepFloyd IF各规模；参数表排除文本encoder，IF有额外超分模型/1024²输出。提供glyph的模型输入信息更强，条件/算力并非严格全匹配。

## 实验条件和发布边界

100K60epoch/1M20epoch/10M6epoch，即约6M/20M/60M样本曝光，数据规模与总曝光混杂；512²，ControlNet/ZeroConv baseLR1e−4，两支captiondrop.1/.5；DDIM20，CFG9，benchmark无附加prompt且空negative，README全局seed0。普通inference.py默认附加质量和negative词，不等同benchmark设置。YAML主batch16×accum2但GPU数/实际logs未给，TextCapsbatch4×accum1、sd_lockedFalse/decoderLR1e−4；warmup1注释resume，fromscratch10000，勿把模板认成精确训练日志。固定commit5891d9b245ac9209c22e3d6d5e933b95d428a230读README、9核心源码/配置说明，test_on_benchmark相关调用/参数选读；未权重/模型/OCR/API执行。

## 主结果

T1Acc%10M42/28、caseinsensitive48/34、LD1.43/2.40；IFXL.6/1、33/21、1.63/3.09；SDXL.3/.5、13/8、6.26/6.30。10M对IFXL大小写忽略提升15/13pp，输入额外glyph且专业数据，非纯架构因果。T2CLIP10M33.9/36.2，对IFXL33.5/35.2；FID SD34.03/SDXL44.77/IFM23.37/IFL30.97/IFXL26.58/Glyph100K22.04/1M22.19/10M22.22，扩大数据未降低FID。定性F1/4/6/7/8有selected成功，F9/11明确长小字、重叠、漏/错/重/多字、过旋转等失败，不能说SD从不生成任何可读字。

## 消融及进一步实验

T3small/medium/large Acc5/4、30/19、23/20；caseignore10/7、37/24、27/23，LD4.85/5.51、1.77/2.58、1.94/2.37，CLIP31.7/33.4、33.7/36.2、33.1/35.7。F10频率分桶可见低频OCR更差而CLIP未同向，4panel无精确柱标，读趋势不伪造单柱数值。完整AppD/T4a同100K起点+TextCaps5K40epoch，frozendecoder Acc48/39、case55/43、LD1.21/1.73；unlock61/43、68/49、.76/1.38，故开放decoder额外13/4pp。T4bunlock10/20/40epochAcc48/28、50/34、61/43，F12显示逐渐标牌化/融合与创意下降。固定README却从10M起点追加TextCaps，40epoch71/41、case77/46，与论文100K起点61/43为不同实验，不能抄成同一checkpoint。

## 局限与疑问

完成正式17页全部研究内容。额外glyph相对纯prompt信息更强，训练数据/曝光、IF超分1024与本512/参数排除encoder不匹配；无多seedCI/全词行转写/长文本人工可读性。公开LD排除OCR空结果且只取最相似检测，不能替代全图CER/额外字惩罚。公开训练loader __getitem__先data={}，行129从data[ocr_info]读取而非ori_data，按静态路径会KeyError；render_text_image_laionglyph又按三项解包，与dataREADME嵌套二项不同，发布训练路径需修正并确认版本。未执行该训练或断言全部checkpoint结果无效。公开READMETextCaps起点与论文不同，测试默认需对齐。过滤>5框/面积限制和VAE压缩只解释部分小字失败，无时间/接触/规范顺序监督。

## 预期优势条件

场景视觉文字布局已知、词长度/字高适中时，glyph空间条件可优于无字形prompt；单调书写生成需glyph随真实事件演进，不能把去噪过程当笔画时间。

## 可证伪实验

Q1OCR优势有多少来自评分：固定生成集，完整报告无检测数、任一框命中、全图转写exact/CER/多余字、人工盲读；把空结果按目标长度计LD并与原条件LD并列，按字高/字长/频率/旋转分层。源代码静态检查即可提出分母问题，未运行OCR。Q2字形控制/数据/开放decoder各自效应：同SD骨干/同glyph输入预算和数据曝光，纯prompt/box/mask/glyph控制，freeze×TextCaps双因子，100K与10M起点分开；文字准确率与背景融合/样式多样性联合评价。迁移手写增加相同终态不同事件序列，单独测笔画接触和规范合法性。

## 论文组织与Claim学习

简单空间条件+专业数据贡献清楚；公开报告起点/冻结范围/字高和采样预算，图注随机初始化应与§4.1拷贝一致。评分写出命中匹配和漏检分母，避免把条件LD当全体平均；附录TextCapsaccuracy与场景融合权衡值得主文同步。推理/发布模板不能代替实际训练记录。

## 实际阅读范围

NeurIPS正式17页§1–6、AppA–D全部、T1–4含4a/4b所有单元、F1–12实际视觉（F10原页放大核趋势）、37条references清单/关键引文；无新编号式/算法。固定commit9个核心源码/配置/说明全文及test_on_benchmark计分调用/参数选读，非全依赖代码审计；未运行模型/OCR/API/训练或下载数据权重。核心三遍和五书面完成。

## OCR分母与匹配规则

公开ocr_acc.py的Acc检验目标是否等于任一识别框；额外文字不罚。LD取所有框中最小距离，且只有OCR非空才更新均值。test_on_benchmark确调用这些counter，因此低LD可与无检测样本被排除并存。应同时报告漏检与全图转写，当前不重跑OCR。

## 论文与公开制品

论文T4从100K模型追加TextCaps；README从10M追加，数值不能混作同实验。LAION训练loader先初始化空data，再从data读取ocr_info；公开渲染器解包又与README字段不同，发布训练路径需要修复和版本确认。此处仅静态路径分析，不据此否定已发布权重全部效果。
