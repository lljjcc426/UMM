# InternVL-U：理解保留、CoT条件与TextEdit指标实现审查

第一百三十六批完成[L123](../reviews/L123.md)明确范围核心三遍和五项书面记录。[结构化证据](../../data/internvlu_retention_cot_and_textedit_metric_audit_2026-10-22.json)。357目录（330论文／研究、27资源），245核心/248书面含未通过项；未确认核心85论文／研究+27资源，资源另审。无新增目录、删除文件、下载权重或独立结果复现。

来源：[v1完整61页](https://arxiv.org/pdf/2603.09877v1)、[主代码018a59c](https://github.com/OpenGVLab/InternVL-U/tree/018a59c1b69690a33698234128aa04e9b3f46c71)、[TextEdit代码721741a](https://github.com/open-compass/TextEdit/tree/721741ae6d0d0197a6dd7b8053f5f969bd81fea4)、[EvalKit bab8bf9](https://github.com/open-compass/GenEditEvalKit/tree/bab8bf9ea3795dbfcd1f57da1c96b911b1f37856)。正式会场未核。

## 研究问题与贡献

以约4B统一模型做图像/文字理解、知识推理、生图与静态编辑，改善轻量UMM的条件保真、知识生成、文本渲染和任务覆盖，并建立TextEdit文字编辑评价。输入文字/参考静态图，输出文字或静态RGB；3D位置编码和旋转编辑不构成视频生成、可执行绘画或汉字规范笔顺能力。

较大UMM训练/部署成本高，轻量VLM条件与去噪图像表示不对齐，复杂指令和文字/科学生成缺特定数据；一般编辑基准较少覆盖文字替换与背景保持。作者结合预训语义骨干、新MMDiT、分阶段联合训练和专门合成数据。数据、教师、初始化和结构同时变化，不能把总分归因某一个新模块，也不能将总参数较小直接等同于等质量低总成本。

从InternVL3.5-2B扩展新1.7B MMDiT，文本AR交叉熵与连续图像latent flow matching共享上下文；双流有独立QKVO/FFN但联合注意，元素门控和多尺度3D RoPE；文本生图、参考图编辑经阶段对齐再混入理解联合训练。最后两层VLM状态通道拼接作为生成条件；可先AR输出显式CoT再条件生成图。另给TextEdit2148样本/18子类与OCR、MLLM复合评价。门控/位置机制单项因果和“首次”主张未由本轮独立新颖性检索证明。

## 模型与数据流

理解：输入图经ViT与pixel shuffle/projector加文字→VLM自回归文字。直接生成：VLM倒数两层选中上下文沿通道cat4096→RMSNorm/Linear→MMDiT条件；编辑的参考图另经QwenImage VAE作为条件latent。目标噪声16通道VAE latent经2×2 patch为64特征，20步DPM更新后VAE解码静态RGB。CoT先在条件分支生成最多默认200新文字token，再重跑VLM并生图；不是只加学习query，未核到每张图生成后反复自省修改循环。mask从每例第二个im_start到待生成img_start，排除system/padding，保留所选上下文；不等于仅取最后token。

表2约0.3B ViT+2B语义骨干+1.7B新初始化MMDiT≈4B，表中2B+1.7B标签未计ViT。HF VLM Qwen3-1.7B为28L/2048/16Q8KV/head128/FFN6144/vocab151936；ViT24L/1024/16heads/patch14/448，shuffle.5。生成20L/hidden1536=12×128/FFN6144，text joint4096，外projector identity但内部RMSNorm4096再Linear1536，RMSNorm不做均值中心化。VAE16原始通道/空间8倍压缩，in_channels64是patch化维度；输出16通道。MSRoPE轴16/56/56，视觉scale1、VLM条件.25；论文插值统一位置范围，其实际实现全路径未逐行核。独立文本/图像流不等于完全无跨模态交互。

## 数据、评价和条件

表1覆盖LAION/BLIP3o/ShareGPT4o/OSP/Echo/OpenGPT/FluxReason/HumanCaption/POSTERTEXT/AutoPoster/CTW和InstructPix2Pix/AnyEdit/PIPE/ImgEdit/SEEDDataEdit/OmniEdit/UltraEdit/HQEdit/X2Edit/X2I2/UniWorld/NHREdit/GPThqedit/NanoConsistent/PicoBanana等。清洗与pHash、Qwen2.5VL分粒度caption、英中翻译；Qwen72B编辑路由/指令、多编辑教师及MLLM筛选。文字用自然/纯色叠字、字体/布局/reflow，PaddleOCR定位→Qwen72B指令→FluxText编辑。科学数据来自MMMU等及教材/竞赛，声称剔除与科学benchmark相同图像，未证明全任务语义/组合独立。物理用PaddleOCR/Gemini3Flash SVG，CS用matplotlib/Graphviz加算法步骤及Qwen3Max改写，几何GeoGebra/matplotlib，CAD ABC/OCC与Objaverse旋转合成，meme五阶段流水。化学PubChem800K筛至600K并成600K QA仅指该子集。总体unique数量/全生命周期上游数据与训练硬件时长未给；分阶段曝光不可当独立样本。

理解T4 MME/SEED/ChartQA/OCRBench/MMMU/MathVerse/LogicVista；生成T5–14 GenEval/DPG/TIIF短长/OneIG英中/CVTG/LongText/WISE/GenExam；编辑T15–19 ImgEdit/GEdit/TextEdit/RISE；附录T20–24基准、分类、指标、mini。CVTG静态词准确、NED相似度、CLIP不能代替笔顺事件。LongText固定EvalKit用Qwen2.5VL32B OCR，英语Counter词/中文Counter字符交集数÷GT总数微平均，忽略顺序且不直接罚额外识别内容，不能当严格逐字顺序精确率。TextEdit报告OP/OR只背景匹配，发布实现同时目标/背景加权且做行级一对一贪心；MLLM报告线性归一化与源码离散映射有差异，需锁评价版本。

各表NanoBananaPro/GPTImage1.5/Seedream4/4.5、QwenImage/Edit、ZImage、FLUXKontext等生成编辑系统；BAGEL、OvisU1、LuminaDiMOO、JanusPro、BLIP3o、ShowO2、Mogao、XOmni、UniWorld等UMM，理解含原InternVL3.5-2B和MammothVL等。每表版本/CoT/闭源状态和原论文/星号重评来源分别保留。WISE表BAGEL.49非CoT标记，不直接等同DeepGen表CoT .70。DeepGen1更早已报CVTG词.7533，本表未纳入；故不能据表内结果宣称所有同期UMM最优。

T3阶段1：512/250K更新/b2048/lr3e-4/constant/wd0/clip.2，backbone冻结、T2I:IT2I4:1、CE:FM0:1；阶段2：512–1024/长宽.5–2/60K/b1024/1e-4/cos/wd0/clip.2，仍冻结并加VAE参考、3:4/0:1；阶段3全骨干解冻20K/b1024/1e-5/cos/wd.01/clip1，T2I:IT2I:理解1:1:2、CE:FM1:20。AdamW(.9,.999,eps1e-8)、warm1000、shift3，理解448。按通常batch×更新推算总593.92M样本呈现，非unique且含理解，缺日志确认步定义。T2I条件drop10%，编辑全条件5%/仅文字5%。论文评价20 DPM solver/CFG3.5、1.5；HF scheduler dpmsolver++二阶/midpoint/flow_prediction/shift3。源码直接image默认4.5、2.0，text_image为3.5、1.5，CoT对照必须显式对齐；每步三CFG分支拼batch，有AR/ViT/VAE额外成本。未给硬件延迟、多训练seed或CI，本轮未运行。

## 结果与可归因范围

理解相对InternVL3.5-2B：MME1552.1→1607.5、OCR83.6→83.9，但SEED75.3→75.2、Chart80.7→76.6、MMMU59→54.7、MathVerse53.4→45.6、Logic47.7→40.3，5/7降；原基座无星号重评标记，需配对协议后归因遗忘。GenEval.85（Qwen.87），DPG85.18（Qwen88.32），TIIF短74.9/长73.9，OneIG英/中.50/.50；均非所有子类更优。CVTG词平均.623（BAGEL.356、Qwen.829），LongText英.738/中.860（Qwen.943/.946）。CoT WISE.46→.58、GenExam20.8→22.9、ImgEdit3.67→3.82、GEdit6.66→6.88，但GenExam历史24.9→20.3、ImgEdit风格4.77→4.69/混合3.03→3.00，GEdit若干子类退化。TextEdit full经典Real/Virtual F1 .71/.75，MLLM平均.88/.83，低于Nano .91/.92；mini MLLM .89/.79不可混full。RISE CoT空间原表5→1.8，四类4.7/7.8/1.8/5.9却总9.4，超过任一分项；保留原数、聚合一致性待解，不自行改成18。

报告无专门拆门控/MSRoPE/两层条件/阶段数据/训练预算的受控消融表；主要有同模型CoT开关的任务对比。WISE六类皆上升，但GenExam、ImgEdit、GEdit和RISE空间有退步，且公开默认CFG随模式不同，不能当显式推理机制单独因果。T4是原骨干与联合系统的结果对比，非固定数据/损失/训练步的理解保留控制；T23/24 mini只是另一子集评测，非结构消融。无给定等参数/等算力单任务生成器及联合训练正迁移因果实验。

## 局限与优势条件

T19 RISE原表不满足同指标分类均值的凸组合约束，固定EvalKit确用各类/全体同score.mean再25(s−1)，原逐例结果缺失，无法判笔误/协议差异。TextEdit Eq7/8背景最佳文本匹配与代码目标.5+背景.5贪心行匹配不同；Eq12(s−1)/4与代码{1:0,2:.2,3:.6,4:.8,5:1}不同，cutoff需CLI开启。ROI代码另要求sim(source,target)<.5才把仍像源图的结果×.2，比报告多一条件；故报告可能惩罚近似正确短修改的假设不应直接套代码。报告AES通常1–5但表值>5，代码线性预测未限界可解释值域，不构成证伪结果。指标NFKC/去标点空格/小写会忽略部分真实文字错误；LongText无序召回不测行序。数据/训练日志和完整trainer未发布于32项主树，科学图像去重不等全域无交叉；小模型标签不含教师/总预训。无视频时序/笔顺/动作指标及独立统计复现。

若预训语义骨干已含任务知识，连续生成分支经足量专门数据对齐，选定上下文与双参考可改善静态文字/知识编辑；显式CoT在可分解指令或科学关系下可能提高遵从。门控可能压低无关条件、位置尺度对齐可能减轻异粒度token混合，这些是动机假设，缺独立消融。优势取决于静态分布、caption/教师质量、采样CFG和评价器；共享模型是否促进理解、严格顺序、真实细笔可恢复均需单独证据。

## 可证伪实验与研究写法

固定初始化、unique数据/曝光、teacher、参数与训练FLOPs，交叉门控/双流/MSRoPE/最后一层或两层/条件ViT+VAE，报告生成/编辑/理解Pareto。CoT用同20步/CFG/随机种子、固定token预算与等延迟直接生成，纳入改写提示、额外采样和独立人工judge，测错误推理传播及每子类CI。取得RISE逐例JSON按四分类/同映射重算；TextEdit同输出同时跑报告公式与固定代码，公开归一化/cutoff/行配对/ROI与OCR版本，做标点/大小写/行序、最小字符修改、额外字/重复字/透视/空背景压力测试及盲评校准。LongText另报有序CER/WER、严格整行正确与额外内容精度。训练测试做图像/提示/来源族语义独立切分。迁移汉字视频先oracleVAE细笔可恢复，再同终态异笔顺、规则SVG/VideoSketcher/强视频基线测事件顺序/可见性/持续性/真实执行；均未执行。

Intro将大众可用的小模型目标拆为语义条件、生成结构、数据和评价四层；Method先整体接口再门控/位置/三阶段与科学文字数据，附录把评价量化和提示公开，组织可借鉴。Claim应区分任务覆盖、表内排名、子类/总分、参数与生命周期成本，理解5/7退化与CoT负例必须保留。无独立Limitations/受控架构消融时，应明确缺证而不把动机当证明。报告与公开实现存在差异，应并列锁版本记录并用逐例重算验证；不能修数后宣称已解决。

## 实际阅读范围

v1完整61页35474152bytes；Abstract/§1–6全部核心、AppendixA/B全部研究文字/指标及评价提示，T1–24文本单元、Eq1–14、F1–29图注；实际p9/10/25/26/27/28/29/31/33/35/36/37/52/53/54/55/59共17页核框架、指定表和公式，未逐页看全部示例/参考文献。主GH固定018a59c完整32项树，README介绍/使用选段、MIT全文，pipeline mask141–264/条件339–429/CoT497–605及模式默认、decoder构造/transformer指定构造/RMSNorm/gate/三分支去噪535–607；未全读110KB transformer/processor/attention底层。HF固定f012d76共23项metadata/card介绍与示例、VLM/生成/VAE/scheduler配置全文。TextEdit固定721741a完整50blob树/README介绍与指标/经典metric100–340和特定clip/aesthetic入口、OCRtools1–60/MLLM归一化与204–246聚合及cutoff参数；数据HF固定9ac3f14元数据4348文件，未下载图像/标注内容。GenEditEvalKit固定bab8bf9完整3640blob树，README介绍/功能选段，InternVL-U两wrapper全文，LongText summary全文/OCR入口1–130，RISE指定judge/score/分类聚合段；未全读全工具箱/原运行JSON/训练日志/权重，无模型运行或独立复现。

## 理解保留与推理开关

| 评价 | 对照 | InternVL-U / CoT | 解释 |
| --- | ---: | ---: | --- |
| MMMU：原InternVL3.5-2B→U | 59.0 | 54.7 | −4.3分，需配对评价协议 |
| MathVerse：原基座→U | 53.4 | 45.6 | −7.8分 |
| LogicVista：原基座→U | 47.7 | 40.3 | −7.4分 |
| WISE：直接→CoT | .46 | .58 | 六类提高，CFG/额外AR成本须匹配 |
| GenExam总 / 历史 | 20.8 / 24.9 | 22.9 / 20.3 | 总分上升同时子类下降 |
| ImgEdit总 / 风格 | 3.67 / 4.77 | 3.82 / 4.69 | 有任务权衡，Ovis总3.97更高 |
| GEdit总 / 文字 | 6.66 / 6.85 | 6.88 / 6.46 | 总体改善不推出所有编辑改善 |
| RISE空间 / 总分 | 5.0 / 3.6 | 1.8 / 9.4 | 按报告原数保留，聚合不一致待解 |

RISE CoT四类为4.7/7.8/1.8/5.9，总9.4超过所有分项。固定EvalKit将逐例相同score分别全体/分类求mean，再同一线性映射25(s−1)；在同一覆盖集、非负分类权重下总分应位于分项最小/最大之间。当前未取得原JSON和精确运行配置，不能擅自改表或确认错误原因。

## TextEdit：定义与发布实现分别记录

| 项目 | 报告定义 | 固定发布实现 |
| --- | --- | --- |
| OP/OR/F1 | 背景文本双向最佳匹配 | 目标权重.5+背景.5，行级贪心一对一对齐后计算 |
| 1—5分归一化 | (s−1)/4 | 1→0、2→.2、3→.6、4→.8、5→1 |
| 次要维度cutoff | 主项原分<4时置零 | 只有传enable_cutoff开关才启用；权重仍.4/.3/.1/.1/.1 |
| ROI源文本残留惩罚 | 预测仍像源文本则×.2 | 还要求sim(source,target)<.5；避免把报告风险直接套实现 |
| AES | 描述通常1—5 | 768→1线性预测器无显式限界，表5.70可记录为原值 |

原表究竟对应哪一版实现需逐例评分与运行revision。发布差异本身不能证明所有结果失效。报告F1所衡量的背景保持和代码的目标/背景混合分也不能混用于跨基准排名。NFKC、小写和去标点/空白提高容错，同时使部分真实排版/字符错误不可见。

TextEdit有2148个人工编辑GT样本，761 Virtual/1387 Real、18子类，mini500。Full MLLM平均.88/.83与mini .89/.79分别记录。基准做静态文字编辑，不能误标成汉字笔顺视频生成。

## 无论文制品与跨任务成本

[HF模型f012d76](https://huggingface.co/InternVL-U/InternVL-U/tree/f012d760e69712bb47f7d3d09a24280f346cee01)23项文件提供VLM、生成器、VAE和scheduler配置/权重索引，本轮只读小型配置与卡。主仓完整32项树含推理模块，未见完整训练/合成/原评分日志。根MIT与上游权重和数据的各自条件分别记录。

[TextEdit数据9ac3f14](https://huggingface.co/datasets/opencompass/TextEdit/tree/9ac3f14d55ce92bf1a6288ac21a5e783983eb0b4)元数据4348项；本轮未读取所有图像/标注。GenEditEvalKit3640个blob大量集成其他工作，不因读取其树便算全部基准或模型已精读。其InternVL-U wrapper默认text_image/seed42，未显式覆盖CFG；上游直接image默认4.5/2.0、CoT3.5/1.5，论文写3.5/1.5。需锁实际运行参数。

20步指ODE求解器步数，每步三条件分支拼batch；显式CoT另有AR和再次VLM计算。表中约4B参数不含合成数据教师与总预训开销。按表训练步×batch推算593.92M是呈现次数，原始unique训练集总量未给。

## 与文字时序和绘画研究的联系

LongText源码按英语词/中文字符Counter交集除GT数量微平均，顺序调换仍可能满分，额外文本也不直接影响分母；应补有序CER/WER、整行准确与输出精度。这个例子说明，指标定义必须与所提研究问题一致：终态OCR无法区分同终态的两种笔顺。

可迁移双参考、知识数据合成与文本保真评价到绘画/跨文字视频的前提，是先验证细笔VAE重建、RGB时序可观测性与真实事件约束；再用等预算共享UMM对强单任务/规则SVG/VideoSketcher和视频模型比较。所列设计未运行。

追引门控注意与MSRoPE原始工作、FluxText/FluxReason、GenExam/LongText/CVTG评价、GeoGebra/Graphviz/PubChem合成资源。相关引用不代表这些原工作已独立精读。下一项L124 Mamoda2.5，保留所有未完成队列。
