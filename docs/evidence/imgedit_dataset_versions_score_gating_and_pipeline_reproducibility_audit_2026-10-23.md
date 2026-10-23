# ImgEdit：数据版本、评分门控与合成流水线复现条件审查

第一百五十九批完成[L148](../reviews/L148.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/imgedit_dataset_versions_score_gating_and_pipeline_reproducibility_audit_2026-10-23.json)。357目录（330论文／研究、27资源），268核心/271书面含未通过项；未确认核心62论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://proceedings.neurips.cc/paper_files/paper/2025/hash/bec783f119b969772c35243b1c801090-Abstract-Datasets_and_Benchmarks_Track.html)、[主源2](https://proceedings.neurips.cc/paper_files/paper/2025/file/bec783f119b969772c35243b1c801090-Paper-Datasets_and_Benchmarks_Track.pdf)、[主源3](https://arxiv.org/html/2505.20275v1)、[主源4](https://github.com/PKU-YuanGroup/ImgEdit/tree/b79848168744c8db8389086d01fe3def1758aa45)、[主源5](https://huggingface.co/datasets/sysuyy/ImgEdit/tree/f8de753484a2b6bd37f135fd20d308b66b09a523)、[主源6](https://huggingface.co/datasets/sysuyy/ImgEdit_recap_mask/tree/6218117caf0bb4f57b215896ac3cd7fe2fa5be0e)。

## 研究问题

能否通过高质量、多类型、具上下文依赖的编辑数据，提高目标定位、指令执行、细节保留与多轮编辑，并建立可诊断评价？四项制品为数据流水线/ImgEdit、专用编辑器E1、Bench和独立Judge，均以静态编辑图为基本输出；不提供汉字逐笔视频生成。

## 现有不足

旧数据的低分辨率、小编辑区域、粗指令、少数任务和不相关多轮限制编辑；通用CLIP/PSNR与编辑遵从不充分一致。单靠跨模型排行无法确定数据、理解骨干、视觉条件和算力谁贡献，作者补同E1换训练集实验；固定mask也限制形状跨度大的替换。

## 贡献

自动预过滤→caption/目标检测分割→含定位的任务指令→分任务ComfyUI合成→VLM评分过滤；10单轮/3多轮类型、E1双编码条件FLUX、basic/UGE/multi-turn基准及200K评分微调Judge。对象提取与参考编辑通过反向构造配对；现有数据消融证明训练集整体作用，尚未隔离全部质量/类型/比例因素。

## 输入、模块、输出与公式

E1源图+编辑文字→单张编辑图；参考编辑另含参考图。多轮沿前图和对话进行内容记忆/指代/版本回退，正式说每例3轮，公开部分含2轮。motion-change来自视频帧对后做静态姿态编辑，不输出视频。Judge源图+指令+结果图→三项1–5分/理由，与E1生成器独立；UniWorld-V1为继承相关能力的另一工作。

## 模型结构

E1将源图与指令交Qwen2.5VL7B，源图另过SigLIPv2SO16@512；各MLP投影后拼接为FLUX DiT文字支条件，VAE目标潜变量去噪。stage1冻Qwen/FLUX仅训Qwen连接器50Ksteps；stage2接Redux初始化SigLIP连接器，训两MLP+FLUX图支10Ksteps；全局batch128、Prodigy自适应lr1。Judge另解冻Qwen视觉编码器/LLM/MLP，200K近均衡任务与分数记录训1epoch；HF配置28层/hidden3584/28heads/4KVheads/bf16，视觉32层/patch14/merge2。没有新增理论定理或编号公式。

## 数据分布与划分

正式LAIONaes短边>1280/aes>4.75筛600K源图，正文motion150K帧对（v1为160K），后处理约弃20%。正式摘要约1M、Intro1M单轮+100K多轮、Table1写1.3M；T5十三行相加1161483=1046460单轮+115023多轮，HF/README与v1称1.2M，不能选一个作独立实数。固定GHb79848168744c8db8389086d01fe3def1758aa45共133成员/83文本配置450684B；basic737指令/171不同源图/615不同prompt，九类型94/100/94/117/86/92/95/23/36；UGE47指令47图。正式734basic+50UGE+30对话、Table2却779；v1为47UGE/Table2 811。HF主库f8de753484a2b6bd37f135fd20d308b66b09a523、预处理库6218117caf0bb4f57b215896ac3cd7fe2fa5be0e，主tree355条含37parquet/约5.87TB制品，未全下或独立数训练对。Benchmark.tar50319360B仅取3435094B后超时，明确不完整；其中两份完整JSONL各10对话，回退全3轮、记忆8个3轮/2个2轮，第三类/全图未核。

## 指标与评价协议

任务专属三维1–5：指令遵从、编辑质量、细节保持，各例均分后任务均分；正式T6 Overall为九任务宏平均，不能按737微平均。后两维按rubric受第一维封顶，构念统计关联是设计的一部分，计分脚本未再次强制裁剪。UGE代码单综合分/非编辑区变化时不超3；模板仅明确要求Brief reasoning而解析器需独立数字行，有格式缺口。FakeShield fake-positive召回是检测器结果，不能当人眼真实性/背景改变定位证明。人评Top2选择比与Judge±1一致率是不同实验。

## 对比方法

主实验GPT4oImage+Step1X/UltraEdit/AnySD/MagicBrush/IP2P/E1七模型，Gemini主用于多轮；Table6新13模型另含ICEdit/UniWorldV1/V2/BAGEL/OmniGen2/KontextDev/OvisU1，未列E1。数据消融同E1换AnyEdit并列AnySD；Judge对Qwen2.5VL7B/GPT4omini。需补固定任务频率/总样本/训练曝光的质量消融、同骨干VLM/SigLIP/VAE结构消融和mask-copy/规则编辑/专用OCR。

## 实验条件和发布边界

正式§1–7/AppA–G及checklist已读，7表11图、无编号理论公式；实际PDF16页2/4/5/6/7/8/9/21/22/23/24/25/27/28/29/30全图表覆盖。正式§5.1每模型五次均值，v1三次；上一轮三次记录已纠正。512 UltraEdit/AnySD，其他原生1024；未报告各生成seed/成本配齐和配对CI。主文GPT4o、Table6换GPT4.1；源码gpt4o未固定快照/温度/max_tokens。F1后处理混GPT4o2024-11-20/08-06与GPT4.1mini2025-04-14，约1/5单分其余三分。Judge硬件原文1xNvidia 8A100 80G一天，措辞保留不擅定单卡；E1硬件/具体采样步数未齐。HF Judge像素1016064–1354752、generation do_sampleTrue/temperature1e-6，READMEmax_new_tokens2048；配置字段不等于所有论文API设置。未下载权重/运行模型/复现分数。

## 主结果

T4同E1架构/超参数：ImgEdit3.21 vs AnyEdit2.76（+.45），AnySD2.45；Adjust3.38<3.44，其他八项提高。T3十人/每子任务五图Top2：IP2P0/Magic3/AnySD5/Ultra4/E151/Step1X46/GPT91%，七项总200%，属于两项选择率，无显著性CI。T6用GPT4.1另报UniWorldV2 4.49/GPT4o4.20/Ovis3.97/Kontext3.71/OmniGen2 3.44/BAGEL3.42，不能将此表直接与E1旧GPT4o榜比较。T7 Judge±1一致71.6%、GPTmini68.3%、Qwen44.2%，以有限人工筛选样本为界。

## 消融及进一步实验

B1固定E1架构和所述超参数换训练集支持整体数据作用，但作者也承认提取/混合任务的相对频率更高，不能把差异全归过滤质量或已证明结构无用。A6未做详细结构/训练消融，与B1补充数据消融分别记录。Judge人评主文60图，E3先说扩120，随后仍写每分12/总60，未给可匹配manifest；不要把单个数字认定最终样本量。±1内相同不等精确评分正确，十人中至少两人同分筛选减少分歧但改变测试分布。多轮仅案例+人工yes/no，缺完整分项数表和置信区间。

## 局限与疑问

统计版本/人评60与120/重复三与五不统一；教师GPT生成/过滤/评测可能共盲点。Fake分无法单独推出全局像素漂移；文本生成、跨语种和严格时序未验证。固定mask替换形状不匹配导致系统性失败，过滤会改变保留任务分布。源码basic README传--basic_edit而脚本实际--edit_json；UGE示例带句号/括号的数字不满足纯isdigit解析，失败记录可能非字符串/跳过使分母变化。后处理process_folder传4参数给3形参call_gpt，当前入口需修正；未据这些公开代码问题反推正式实验造假或所有分数失效。GH/配套HF未见单独E1训练入口/权重，Judge权重与继承的UniWorld需区分。G1数据CCBY4与HF主卡Apache/预处理卡MIT的范围未齐，仅记录元数据不作授权结论。

## 预期优势条件

对于合成mask能覆盖、目标身份可保持、局部编辑/提取/混合类型充分且测试不泄漏源图的分布，结构条件+语义条件与针对任务数据有望提高执行和保留。跨多个指令共享171源图，方差需按源图/对话聚类；回退可借外部版本存储，并不自动证明内部长期记忆。严格书写可借局部确定性修改和版本历史，仍需笔画事件真值、不可擦除约束及中间帧检查。

## 可证伪实验

等数据量/任务频次/图像源/训练曝光比较分辨率、位置指令、GPT过滤与合成质量；同骨干替换VLM/SigLIP/VAE连接路径，隔离数据和架构贡献。保存逐图三分检查封顶违规/缺失分，固定judge快照+盲人评和独立OCR；按171源图聚类bootstrap。回退比较全对话、仅末轮、外部版本缓存，测试修辞/指代/新对象；笔画视频另设时间反转、帧置乱、非法笔画与局部重绘。所有方案未运行。

## 论文组织与Claim学习

Introduction以数据质量/任务覆盖/评测三缺口配四项制品，Method按类型→流水线→示范模型→Bench→Judge组织，附录训练/数据消融/勘误可学。Claim应限定E1同架构换数据支持整体数据，Top2偏好不当准确率，教师评分不当独立人类事实；正式/早期/代码计数显式分版本。Limitations落到mask形状偏差、文字/语言/上下文能力及开放配置缺口，不能把未来UMM扩展写成已实现。

## 实际阅读范围

NeurIPS2025正式31页12416801B，Abstract/§1–7/AppA–G全部研究内容及checklist，7表全行/11图及图注、16实际PDF页；arXivv1全研究正文与AppA–D文本对照。固定83文本数据配置取回，完整read主README、三个评测README、basic/UGE评测和3计分脚本、6_postprocess、1_filter、4_yolo_seg及4.sh、ComfyUIbase/flux_inpaint/dlc_add；5_generate_prompt仅指定模型调用/候选门限，八工作流完整JSON程序抽采样/模型条件，未逐节点人工走通。basic/UGE完整结构，截断tar仅两完整JSONL/20对话手读；五HF卡/配置读，tokenizer配置未逐项解释。无权重/模型运行。

## 版本与计数

| 来源 | 计数/条件 | 本轮处理 |
| --- | --- | --- |
| 正式摘要/§3.4 | 约1M，包含100K多轮 | 原文保留 |
| 正式Intro | 1M单轮+100K多轮 | 与总数措辞区分 |
| 正式Table1 | 1.3M | 不擅改为1.2M |
| 正式Table5逐行求和 | 1046460单轮+115023多轮=1161483 | 本地算术，不冒充原始训练对统计 |
| arXivv1/当前README、HF卡 | 1.2M，v1 motion160K | 正式motion写150K |
| 正式Bench§4.1 | 734basic/50UGE/30对话×3轮；Table2写779 | 单位与数字未齐 |
| 固定公开JSON | basic737/171源图/615不同prompt；UGE47/47图 | 结构程序核，不把指令当图像数 |
| 正式§5.1 / v1 | 每模型五次 / 三次 | 本轮纠正上一轮三次泛化 |
| 人评E3 | 开头扩120，后仍每分12/总60 | 不把60或120擅定最终唯一口径 |

固定GitHub `b79848168744c8db8389086d01fe3def1758aa45`、HF主库 `f8de753484a2b6bd37f135fd20d308b66b09a523`。HF tree含355成员/37个parquet及约5.87TB制品，本轮没有全量下载和统计训练记录。Benchmark.tar预期50319360B，连接在3435094B超时；仅从完整tar成员取两份完整JSONL，各10对话并逐条读。回退全三轮，记忆八个三轮/两个两轮；第三种对话和全部图片未核，不将截断包记为完整开放数据审查。

## 方法与为什么可能有效

数据选择先提高分辨率/目标可见性，GPT指令引入bbox位置，再以任务专用FLUX/SDXL填充、结构控制/参考条件生成并过滤。Fig9及代码显示：add可逆用remove的空区域填充构造，提取/参考也可反向配对，减少单纯从原对象难以保身份的依赖。局部crop后回贴边缘融合有利保持未改区域，同时mask形状会限制形状变化大的新对象。这是可检验机制，不应把所有收益归“理解更强”。

E1为Qwen2.5VL语义+SigLIPv2视觉各MLP后拼进FLUX文字条件；两阶段训练50K/10K、batch128/Prodigy lr1。该lr是自适应优化器约定，不能当常规SGD固定步幅推断训练不稳定。Judge另在200K任务/分数近均衡记录上解冻视觉/LLM/MLP训一epoch，配置、权重目录与E1不同。当前公开树没有单独E1训练入口/权重；README指向700K子集训练的UniWorld-V1，属于相关继承工作。

## 主表、消融与人评

T4同E1/同所述超参数换数据后九项均分3.21→2.76，支持数据集整体的作用；Adjust3.38→3.44为例外。作者也明确提取/混合占比不同，因此质量、覆盖和任务频率尚未完全拆开。A6说缺详细架构/训练消融，B1补的是数据消融，两段不矛盾。

T3 Top2七模型选择比例0/3/5/4/51/46/91%，总200%是两选设计；E1与Step1X差五个百分点，未给按图/评委重复结构的CI，不能写已证明显著。T6是GPT4.1评价另13模型，没有E1，UniWorldV2 4.49/GPT4o4.20/Ovis3.97；早期E1的GPT4o分不能直接并榜。当前basic多条指令共享源图，显著性宜按源图聚类，避免当737独立视觉场景。

T7 Judge±1一致71.6%、GPTmini68.3%、Qwen44.2%。主文60图、E3先120后60未对齐；人类至少两人同分筛选及分数均衡改变测试分布，不能扩展成全部现实编辑的可靠率。±1容差指标还应补精确一致、MAE、逐维混淆与难例错误召回。多轮Fig10/11是人工案例，模型版本又涉及Gemini2.0正文/2.5图注；缺完整API日期、全样本结果及对话编排记录。

## 评分和公开代码的实际约束

三维封顶由提示模板要求，计分器只提取“冒号+空格+纯数字”行并均分，不检查三项名称/数量/1–5范围或再次封顶；README本身有第一分1、后两分4/4的示例，不能假定所有裁判必遵守。失败/非字符串记录还需明确处理、有效覆盖和统一分母。UGE模板只明确要求Brief reasoning，README带句号/括号的示例分也不满足当前纯数字解析；这说明接口需补齐，尚未证明真实运行全无分数。

basic README的`--basic_edit`与脚本`--edit_json`不符；`6_postprocess.py`中`process_folder`传四参数而`call_gpt`定义三参数。它们会阻碍当前公开入口直接运行，不据此推断作者实际私有实验。源码base64原图发送、不固定API快照/temperature，重复五次对应哪些生成seed也未披露。

八个ComfyUI模板的采样节点/骨干/LoRA参数存入data证据。例如FLUX填充12步/sgm_uniform/dpmpp_2m/FluxGuidance30/CFG1，SDXL填充21步/karras/dpmpp_2m/CFG3，均为发布数据合成模板，不能写成E1正式推理超参数。`tools/1_filter_json_by_aes.py`默认5.0/512，与论文4.75/1280需显式传参；候选代码按bbox面积和CLIP/置信门限筛，不能当真实分割mask精确覆盖。README仍标流水线WIP。

FakeShield检测召回只证明其在给定阈值下识别合成痕迹，无法独立定位非编辑区改变或证明人眼真假。F1勘误还明确后处理模型和单/三评分混合，需各样本保留来源。正文/附录许可证与HF卡元数据不一致，按原文记录适用范围待明，不作法律结论。

## 与文字、素描和严格书写研究的关系

多轮公开题有改车牌为1、衣服字改Hello、看板字的增删，属于文字编辑/版本记忆场景；motion-change来自视频帧，依然静态输出。G节提到生成文化视频是社会影响举例，不能据此扩成视频训练能力。英文提示/文字弱项有明确局限，跨文字体系与汉字笔顺需独立任务和真值。

可借鉴局部确定性修改、保留约束、回退记录和身份保持，设计笔画事件/中间状态审核；必须比较规则渲染、外部版本缓存和逐笔动作条件的强基线。拟等量/等任务占比/等曝光拆数据质量、类型覆盖、位置指令，再同底座拆编码器与条件接口；固定裁判、盲人评、OCR及源图聚类CI，视频补逆序/置乱。方案均未执行。

学习其三类缺口对应四制品的Introduction、类型→流水线→模型→评测的Method、主表→数据消融→人评→勘误组织；写Claim时同时写负项/版本/预算，Limitations针对mask形状、文字和上下文局限。UnicEdit-10M、UniREditBench、UniEditBench与Image Editing As Programs已发现为后续追引，尚未计入独立完成。

