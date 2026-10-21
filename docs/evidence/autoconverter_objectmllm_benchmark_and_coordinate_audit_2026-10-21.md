# AutoConverter/VMCBench与ObjectMLLM：基准构造、坐标表示及既有负结果

第九十六批追引Timage/BoxTuning的原始基准和对照，补录[G042](../reviews/G042.md)、[G043](../reviews/G043.md)并完成指定范围核心三遍/五项书面检查，同时补正[L053](../reviews/L053.md)、[L054](../reviews/L054.md)的前作边界。[固定发布记录](../../data/autoconverter_objectmllm_formal_and_release_audit_2026-10-21.json)保存来源、版本、代码差异和未执行项。当前356条（329论文／研究、27资源），193项核心/196项书面含未通过项；163条未确认核心。未删除文件，未运行模型/远端API或独立复现，未下载模型权重和数据媒体。

## 正式版本、任务和阅读范围

[AutoConverter正式CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhang_Automated_Generation_of_Challenging_Multiple-Choice_Questions_for_Vision_Language_Model_CVPR_2025_paper.pdf)11页核心§1–6，实际核p4F3框架/消融和p8T1；[正式24页supp](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Zhang_Automated_Generation_of_CVPR_2025_supplemental.pdf)读p1–2全部A–C说明、Limitations/伦理/复现段和选项置换T2，未逐页精读后续全部prompt/例图。其输入是图像、问题和原答案，输出干扰项；VMCBench测静态VQA。两者不提供视频生成或规范笔顺生成模型。

[ObjectMLLM正式ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Tang_How_Can_Objects_Help_Video-Language_Understanding_ICCV_2025_paper.pdf)10页核心§1–5/F2–7/T1–5，实际核p3/p5–8框架、学习曲线和主表；[10页supp](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Tang_How_Can_Objects_ICCV_2025_supplemental.pdf)读A–F全部说明及A1–11表，实际核p2–5表/画框例。未逐帧精读全部p6–10例图。它把视频显式框/标签/时间戳和可选caption/视觉embedding用于问答；BABEL-QA另读原3D姿态做问答。论文结论限定这些任务和适配条件。

## VMCBench从9,450到9,018的构造与Timage订正

原§5完整给出构造链：20集各随机至多500，共9,450；12个开放式集转换、8个选择题集换干扰项。GPT-4o正确性1–5分分别有103/162/399/635/8,151题。6名PhD检查全部1,299道低于5分题和最高分抽样1,101题，共2,400；去掉已识别错题后保留9,018，拆1,000开发/8,018测试。

[固定HF ac748b6](https://huggingface.co/datasets/suyc21/VMCBench/tree/ac748b6f2a4454900477721f2bc9077f55c7c21f)的卡和元数据确认1000/8018，测试答案不公开；schema含image、question、A–D、answer/category/index。未下载约867MB数据、TSV图像base64或调用测试站。

据此补正上一批的疑问：Timage所写9,450有原始构造数量依据，不能据此断言“额外新增432题”。仍需它公开使用筛查前集合还是正式发布集、逐题ID、split、错题处理和100epoch训练隔离。如果混用阶段，主表可比性和训练/测试边界仍未明确。上一批核心阅读状态保持，修正具体解释与对应实验问题。

9,018条并未全部逐题人工通过，最高分8,151题只抽查1,101。最高分人工正确95%；三数据集转换实验的最高分仍3%错属另一范围，两者不合并成“整个基准97%正确”。6名标注者也不等于每题6人独立标注；论文未充分提供逐题重复标注/仲裁和区间。

## AutoConverter机制、原表与可支持结论

五种proposer分别模拟概念、视觉、推理、数据处理和问题偏见，Reviewer反馈后更新候选，Selector取3个。正确性Evaluator给1–5分，<4则Refiner修改，最多3轮。保留原题/真答案有助于固定任务，却同时继承错误答案；同一个GPT家族生成、审查和评分的相关错误不能由角色分工自动消除。

| 证据 | 原始结果 | 分析 |
| --- | --- | --- |
| F3b MMMU | human C4.59/均准确41.8；naive4.59/46.0；full4.69/40.7 | 联合提高代理正确性、降低平均模型分；难度要在有效题上解释 |
| 去Refiner | C4.28/准确37.8 | 更低准确伴随更差正确性，不代表更优造题 |
| 去Reviewer | C4.64/42.7 | 少一个模块也少调用预算，缺等调用预算对照 |
| full单模型 | 27.8/37.2/44.2/53.6；human33.4/35.2/46.0/52.4 | M2/M4在full更容易，不能写所有模型都比人工难 |
| 正式T1 | Qwen2VL72B85.0，GPT4o80.3，Qwen7B78.1 | 是固定版本测试集VQA；不可当2026所有模型最新排行 |
| §3.1规则/代理 | GPT4o约32→校正88；12模型排序ρ=.09，代理/人类agreement.95 | 揭示该设置规则误判；独立验证集/标注协议仍影响外推 |
| §3.2裁判版本 | ρ=1.0，绝对分约差6 | 两裁判排序一致本身不能证明与人类判断一致 |
| suppB3/B4 | 换三家生成器平均ρ=.90；MC对开放式模型代理ρ=.85/.71/.97 | 支持选定范围排序稳定；代理评分不等同独立人类真值 |
| suppC1/C4 | 人类91.7；两次选项乱序分数小变 | 人评样本细节不足、两次置换不证明全域无选项偏见 |

正式主表33模型，README摘要仍28；suppC1称“当前最佳GPT4o80.6”，正式主表却有Qwen85.0/GPT80.3。保留这些版本差异，不强行合成一个实验。InstructBLIP7B42.1高于13B41.1，也不应将参数规模趋势表述为每家严格单调规律。

## ObjectMLLM的信息、数据和实验条件

YOLO-World-v2-L_CLIP-Large800按每基准train框微调，SAM2.1hiera_large冻结；1FPS关键帧检测，SAM2用原视频帧率跟踪，IoU>.5去重复。检测lr2e-4/wd.05/b64，CLEVR60k图/7epoch/阈.001，PTest46k/50/.35，STAR106k/20/.2，NExT/Intent151k/10/.4。这些监督和预处理成本必须计入“少数据”定义。

框为ID、类别、可见时间戳和四坐标，文字分支量化0–100，投影分支连续0–1线性映到LLM embedding。LLaMA3-8B分支用LLaMA-Adapter，可选10帧CLIP和6帧LLaVA1.5-13B caption，按caption→box→visual逐模态训练；另分支从VideoLLaMA2-7B-16F用LoRA。框下采样经二分使文字少于1000tokens，CLEVR约6帧；不同视频频率不同，密集短事件可能丢失。

Adapter b64/lr.0225/20%warm，LoRA r128/b128/lr2e-5/3%warm，均cosine并冻vision。QA epoch分别CLEVR1、NExT/STAR5、PTest/Intent10、BABEL50；未给完整GPU/时长/多seed区间。CLEVR训练来自VideoChat2-IT，评测是MVBench转成MC的部分，题型不完全一致。六个任务包含BABEL原3D姿态，不等于六个普通RGB视频基准。

| 证据 | 原表结果 | 能说明什么 |
| --- | --- | --- |
| F5表示 | 文字/投影CLEVR77.6/64.9，PTest63.5/60.1；CLEVR约10k为63.8/44.5 | 特定数据/适配下文字坐标有效；不能推出所有投影方法无效 |
| T1 caption→+box | CLEVR47.8→75.5、PTest62.4→65.7、STAR60.1→64.4、NExT76.6→76.6、Intent75.7→75.6 | 任务依赖明显，后两集收益小或下降 |
| T1三模态 | 75.4/63.9/62.9/76.2/75.0 | 均未超过caption+box对应行，融合可退步 |
| T3 VideoLLaMA2 LoRA→+box | 67.9→77.6/66→66.6/66.5→67.2/79.8→78.5/76.7→75.5 | 这是BoxTuning直接对照来源之一；不能漏写NExT/Intent退步 |
| T5 BABEL | V66.6/C60.2/P63.5/V+P68.6/C+P69.4 | 原姿态文字能补充；未测试真实视频提姿态误差 |
| A2/A3/A4 | 投影随机→零42.8→64.9；增层约65；1→9token64.9→63.4<文字77.6 | 作者已测试初始化/表达力/token数，质疑须承认这些已有对照 |
| A6标签 | STAR标签58.8/标签框59.1；CLEVR59.8/77.6 | STAR大部分来自对象类别，CLEVR位置贡献更大 |
| A7频率 | CLEVR .25/.5/1/2FPS=74/73.9/77.6/78 | 频率和上下文影响结果，非严格单调 |
| A9改annotation并重训 | CLEVR74.9、PTest66.8、STAR78.9、NExT65.5、Intent65.3 | 非固定模型只换精度；STAR同时变化关注对象先验，部分annotation仍算法检测 |
| A10视觉画框 | 59.7<连续投影60.1<文字63.5（PTest） | 既有负尝试；不能称此前未研究画框提示 |
| A11对象embedding | 63.3<box63.5，frame62.7 | crop未带来额外提升；外观与高层状态仍可能未解决 |

附录“spatial-free caption”实验同时更换LLaVA为GPT4o，prompt还禁止具体对象；由此推“只移除空间”不充分。A9标注对象集合也与模型检测不同。后续应固定同caption生成器或同对象集合做因果控制。

## 固定公开发布和论文差异

[AutoConverter GH4b918c6](https://github.com/yuhui-zh15/AutoConverter/tree/4b918c60e0b38f9354a1dabd18f69fe8687d8c3e)完整5blob树，读README/main.py指定主流程。代码是单题Gradio：开启Refiner后无条件裁判并修订一次，没有论文<4/最多3轮条件；用浮动gpt-4o别名，temperature=0注释，seed1234仅Python选项排列。没有将它当完整正式批处理协议。README有MIT badge，完整树无LICENSE正文，HF卡MIT亦不代表20个上游集的全部许可已审核。

[ObjectMLLM GH4d04960](https://github.com/brown-palm/ObjectMLLM/tree/4d04960f41b92675d46ce9b7ca377e74614e0311)完整95blob树，读README/LICENSE、指定LLaMA3训练/加载/模型和VideoLLaMA2脚本/截断段：

- PTest文字/投影脚本context1200/700，b1×accum8×8GPU有效64，blr.09按64/256缩放为lr.0225；AdamW β.9,.95/wd.14。语言分支并非全参微调；可训gates/adapters/mmprojs，默认32层/每层10个adapter query。
- 投影器仅在--zero_init时置零，parser默认为False；所读ptest_box_projector.sh没有该参数。论文A2主对照采用零初始化，不能默认当前示例脚本精确复现论文最强投影对照，也不能由此断言发布权重如何训练。
- loader读取预处理bbox_textual/projector JSON和npz；文本量化/检测/跟踪/采样的原始生成链未在这些loader中实现。需要下载包和原预处理脚本继续核对，当前未获取数GB制品。
- VideoLLaMA2 PTest脚本是16帧/CLIP336/STC/LoRA r128 alpha256，默认drop.05，AdamW lr2e-5/wd0/warm.03/10epoch/global128/local4/context2048。对话配置名llama_2与Mistral骨干标识分别记载，未推断二者不兼容。截断代码存在，未量化实际丢失频率。
- README链接GoogleDrive预处理数据/框与逐集checkpoint，并给40/80GB等资源说明；没有下载验证可用性、内容或实测显存/时间。代码MIT不自动覆盖上游模型、视频和所有权重。

## 对BoxTuning、书写研究及实验设计的影响

ObjectMLLM在BoxTuning之前已探索固定颜色画框，只在该PTest设置得到负结果。BoxTuning增加legend/历史轨迹及更强预训视觉骨干适配，须在相同感知结果、监督和预算下归因。原ObjectMLLM还逐基准训练YOLO；BoxTuning所读版本对感知训练和各对照是否同源未完全说明，不能把两表相同数字当独立复现证明。当前修改L054补充既有尝试，未代替它的密集场景、ID错配或新骨干实验。

可检验假设一：真假答案可靠且无选项线索时，MC转换能减轻开放式评分格式误差。固定日期API、等调用预算、盲人评/跨模型judge，分评分层抽查并报告加权错率；无图/只选项/多次乱序/近义改写检查泄漏，独立人工开放式排序作外部依据。

可检验假设二：少数据和运动/位置主导任务中，已有数值词表的坐标输入能降低对齐难度；需同底座、同感知、同曝光，分别匹配tokens和FLOPs，对比坐标文字、1/9token投影、ROI、画框、legend和过去轨迹，报告全部pipeline成本。增加时间逆转/ID置换/漏检/框扰动和密集分层；已有A9不能充当这些全部误差干预。

书写场景须新增笔画事件、落抬笔/接触、同终态异顺序真值和RGB可观察性。静态选项正确率、对象位移或六帧姿态识别不足以确认规范笔顺生成。两篇的可迁移价值是基准有效性检验和显式轨迹表示的强基线，相关实验均未在本批运行。

写作上可学AutoConverter先展示评价失效，再拆正确性/难度目标；ObjectMLLM先提出表示与适配假设，分比较表示、融合、扩展并保留负结果。Claim应注明分布、预算、数值与退步；Limitations区分作者已讨论项与本次批判，避免将缺少某类误差实验等同“此前完全没考虑”。
