# 资源协议补审与剩余论文访问缺项

截至2026-10-25第二百二十三批，360条目录中有333篇论文／研究与27项资源。论文核心三遍完成326篇，7篇仍缺可取得的全文或实际原图；329项书面检查包含未通过项。27项资源现已逐项完成公开协议审查，共135项回答，详见[机器台账](../../data/resource_acceptance_2026-10-25.json)。

这里的资源完成状态覆盖身份/版本/许可、字段、可取得的制品或明确访问结果、主张边界、研究迁移五项。原始数据、未发布训练流水线、权重运行和全量人工标注核验仍按项保留；没有将“未发布”或“暂时访问失败”填写为实际制品已验收。没有学习模型训练、推理、OCR/judge调用或独立复现。

原329项书面记录中，328项属于论文，1项属于资源H001（未通过论文核心验收）；本批保留该历史记录，并与135项资源协议回答分别计数。

其中22项已有公开源码/文件/图像或权重元数据检查；R03、R04、L049、L050仍缺原始样例包，R05仍未确认数据发布。

此前资源也套用论文三遍模板，导致台账统一显示“未完成”。本批增加独立资源验收与生成模板，论文完成数不因此增加。

## 实质新增证据

- **规范与矢量**：取得GF0023—2020完整581页PDF，核8105个序号和UCS索引完整唯一；逐笔图仅抽查。MMH完整字典9574字，图形31个完整样例；AnimCJK的馬在简/繁目录前两笔不同，KanjiVG补读心/食实例。
- **数据实物**：OpenHandWrite大表全部10表/行数/字段核查，50400行是字符级汇总；1242项模板ZIP目录未含HDF5原始轨迹。CalligraphyBench全部88张参考图、CASIA衍生两张行图和BCSS一个六类mask样例均实际查看。
- **时间与动作**：Datumwell全部10个parquet、59338行，确认约50Hz数值与约3Hz新图像；首视频6帧抽查。每例计划/状态RMSE约0.000341–0.000362rad为模拟记录差值，不能替代真实执行/规范笔顺指标。
- **源码边界**：Hanzi Writer容错/强制通过选项、Tegaki参考排序、Qari随机行拆分与显式loss mask缺项、SceneDAPR删除操作丢历史均已定位。VidSketch存在DPO成对loader，但未找到完整DPO目标/训练入口；所读adapter插值末端保持零的索引范围已记录。BCSS公开实现与论文维度/发布范围差异仍在。
- **模型组件**：Wuji54维统计文件已静态读取；CoFRIDA底座/矩阵维度矛盾未消除。SenseNova缩放/merge、CogVideoX加权目标/latent配置、SD VAE六组重建图与Wan Toy当前发布范围按实际文件核查，均未运行权重。

所有本批确定性数量与解析摘要见[实际制品观察](../../data/resource_artifact_observations_2026-10-25.json)。原始PDF、图片、数据和权重不提交到公开仓库。

## 27项资源逐项结论

| ID | 实际证据与关键结论 | 剩余制品缺项 |
| --- | --- | --- |
| [R01](../reviews/R01.md) | 完整读Quiz.ts、strokeMatches.ts、defaultOptions.ts。接受条件包含isMatch、达到markStrokeCorrectAfterMisses阈值，或逆向匹配且acceptBackwardsStrokes=true。默认后两项均false，quizLeniency=1。当前笔画与后续笔画比较会收紧容差，不能将其简化为完全没有几何容错的序号判定。 | 未运行浏览器；未逐字验证整个hanzi-writer-data；没有真实摄像或学习模型成绩。 |
| [R02](../reviews/R02.md) | 本批完整解析dictionary.txt：9574行、9574个不重复字符。graphics全文件下载未成功，实际解析HTTP Range前64KiB中的31个完整JSON条目：31条的strokes与medians数量均一一对应；末尾不完整行未计入。 | 全量graphics及每字准确性未验收；时间/压力/真实外观须另采集；版本仍是有日期的master快照。 |
| [R03](../reviews/R03.md) | 已读官方采集、统计、POT/WPTT格式和使用条件；本批未成功下载原始包，二进制样例解析未完成。格式证据与样例证据分列，Teklia的离线行图不替代在线包。 | 原始POT/WPTT样例与全包仍未取得；基础数据论文全部实验不由资源协议审查替代。 |
| [R04](../reviews/R04.md) | 现有核查覆盖Overview、Characteristics、Terms和完整格式字段说明。本次未注册/下载样例，没有将文档例子计为实测XML解析。 | 注册数据与样例未取得；完整基础论文、逐样本标注和视频对应未核。 |
| [R05](../reviews/R05.md) | 已核§4.1采集/分割文字及Introduction；作者主页仍描述规模，未给出可确认的Mobao完整包。本次未取到原始样例，未用猜测的第三方仓库代替官方发布。 | 数据发布入口、许可、样例和拆分清单均未确认；尚不能按现成可复用数据集安排实验。 |
| [R06](../reviews/R06.md) | 取得581页、51,412,684字节PDF，阅读全文§1–5；整份文本提取并检查8105组“字表序号—UCS”：序号恰为1..8105，二者各8105唯一项，无缺号/重复编码。实际查看规则/表首与末页，未逐字转录全部逐笔图。 | 8105字逐笔图全部人工转录/双人校对尚未做；完整索引检查与视觉抽查的范围已分别记录。 |
| [R07](../reviews/R07.md) | 完整读取batch入口与主要汇总/长度/延迟函数；完整遍历12.76MB大xlsx全部10个工作表行数与表头，其中Trial_Character-Level为50400行27列字符级汇总。读取99MB模板ZIP完整中央目录1242项，并用Range提取README、experiment.psyexp、ccutil.py及wintabgraphics.py关键采集段；目录无HDF5/原始报告文件。 | 未取得原始HDF5/逐点报告，未完整下载模板ZIP或运行PsychoPy/R；未逐段重做HTML统计分析。 |
| [L044](../reviews/L044.md) | 全部88条元数据/几何已解析；本批下载并实际查看全部88张参考图，资源URL包含同一固定revision。82个唯一字符、18个书家标签；此前39行笔画计数与几何数量差异仍在，视觉查看未消除这些不一致。 | 完整评测harness、裁判快照/校准、完整提示和预算未取得；39行跨源对应仍待专家核验。 |
| [L048](../reviews/L048.md) | 完整读providers/datasets、match.ts、guide.ts。zh优先MMH、ja优先KanjiVG，首个非空参考胜出；match以24点等弧长重采样、正反向距离与Hungarian一一分配。guide在笔数不对应时以16点投影、35%位置分位数排序并估方向。 | 未执行字体抽取或浏览器；未逐字验证1110个几何结果、全部字体和fallback；不声明全仓源码逐行审完。 |
| [L049](../reviews/L049.md) | 已读§2–5及Tables1–4采集、标注与算法；本轮继续核当前下载可用性，未找到/取得可验证的原始数据包，因此没有新样例解析。 | 原始包、实际二进制规范与适用授权仍待取得；本次未补齐整套资源实物。 |
| [L050](../reviews/L050.md) | 已读官方数据规模、划分和完整InkML说明；没有取到压缩包或解析原始样例，不将格式文档当作数据实物。 | 原始InkML样例、压力单位/许可细则与配套论文全部实验未完成；本条只完成公开资源协议审查。 |
| [S007](../reviews/S007.md) | 本批取得完整images.zip，并实际取样007054的原图和6张mask、七维先验[25,3,4,2,3,0,2]；查看全部7张图，mask_5为空，其余显示类别分组。样例媒体来自datasets-server的图像导出，未把缓存JPEG当原始无损标注做像素指标。 | 全量mask ZIP下载未完成，未逐图审全标注；未取得同论文实验的完整原版本与checkpoint。 |
| [S008](../reviews/S008.md) | 本批取得871字节action_stats.npy，以pickletools静态读取结构和原始float32载荷，不执行pickle。mean/std各54维，count=438986；std最小约0.04499、最大25.69574。结合原先配置核查，确认实际统计文件存在并具有相应形状。 | 11.54GB权重未下载/执行；完整MoT实现、动作维度语义、统计split与物理任务评测仍缺。 |
| [S009](../reviews/S009.md) | 实际读中4笔及简/繁目录中馬的两个10笔SVG。馬的前两条轮廓/中心线顺序在两个目录交换，构成locale影响的具体例子；没有将全部字体文件都称为已读。 | 未逐字验证完整多语字库与所有生成脚本；动画时间不提供物理真值。 |
| [S010](../reviews/S010.md) | 本批补读心(05fc3，4笔)、食(098df，9笔)完整SVG及COPYING，结合既有中(04e2d，4笔)示例和格式说明核字段/次序。 | 未逐字校全库及所有变体；无逐点物理时序、压力或真实RGB过程真值。 |
| [S011](../reviews/S011.md) | 完整读train.py、training_config.yaml与inference.py。数据来自本地ARABIC_OCR_FINAL，按行random_split 95/5、seed42；collator显式labels=input_ids.clone()，未显式把prompt/padding/image token设-100。精确底座revision和完整语料构建未给出。 | 适配器未运行；缺完整数据构建、分组证据和评价实现；不声称所读源码就是比赛checkpoint完整训练记录。 |
| [S012](../reviews/S012.md) | 在已读完整数据卡/规模/字段基础上，本批取train首两条、实际查看两张行图并核文本字段；缓存图像URL含固定revision。未将两条样例当作全52160行质量检查。 | 未下载全部parquet或逐条图像核验；缺原作者/段落/在线关联和过程真值。 |
| [S013](../reviews/S013.md) | 新增读SketchForm采集/撤销/提交完整逻辑、后端resolver全文和COCO转换器；实际查看公开检测示意图。既有preprocessing SVG转换限制保留，没有调用采集系统服务器或读取受限参与者数据。 | 受限原始参与者数据未取得；删除事件日志和逐点时间并未由当前采集格式保存。 |
| [S014](../reviews/S014.md) | 静态提取42个cell的全部源码，选读Dataset、点序转换、模型/扩散采样、训练/EMA和evaluate_category。EMA=.9999，evaluate加载checkpoint后应用EMA；这些读取未执行notebook。 | 未执行、未取得训练数据/权重及运行记录对应；未声称42个cell全部逐行推导或修复上游。 |
| [S015](../reviews/S015.md) | 本批完整读dataset_DPO.py，并读inference/pipelines/pipeline_VidSketch.py的接口与adapter/去噪核心；结合已读train_vidsketch.py的MSE主损失，修正此前笼统“DPO脚本缺失”为“成对loader存在，未找到完整DPO训练目标/入口”。 | 缺完整DPO训练目标/发布checkpoint映射及数据；未执行pipeline或全审所有替代路径/依赖。 |
| [S016](../reviews/S016.md) | 在既有README、完整tree、FCN/DeepLab/LabelMe样例阅读基础上，补读backbone选择入口、decoder和UNet基本模块全文。固定tree没有论文完整训练/eval/checkpoint流水线，主表模型结果仍无法从该发布直接复现。 | 完整训练/评价、阈值、识别器和论文主表checkpoint缺失；未逐行审全部backbone或运行模型。 |
| [H001](../reviews/H001.md) | 既有固定bin前512KiB ZIP/data.pkl元数据已静态全读，不执行pickle；本批重读完整卡，与官方f42fa618的rank32训练配置及两个底座config交叉核。仍未找到本bin与官方训练版本的精确对应。 | 精确底座/alpha、训练集/日志、依赖版本未齐；未完整读取/运行权重或复现绘画。 |
| [R08](../reviews/R08.md) | 本批完整读固定README和utils/lora.py；配对矩阵缺失或零匹配会报错。重复调用merge会继续累加，调用方需管理状态。V2建议final base、8step、CFG1、norm none、shift3按卡记录。 | 未下载/运行权重、未核全训练实现与训练数据；没有本项目质量/效率对照。 |
| [R09](../reviews/R09.md) | 本批完整解析全部10个parquet共59338行：每例时间严格递增，中位步长约.02000046s，state/action均5维；实际引用图像源索引的变化间隔中位.334s，最大image age约.332s。首段tabletop MP4解码确认为640×480 H264/50fps/125.76s，实际查看0/25/50/75/100/125秒六帧。 | 30路视频仅解码/抽看其中首例一视角；未逐帧人工验全视频、未取得200集合或运行policy/物理重仿真。源加速度报告未独立重算。 |
| [R10](../reviews/R10.md) | 本批补读完整卡片并实际查看全部6张发布的EMA/MSE/原图三联重建图；顺序为左EMA、中MSE、右原图。两重建表均按作者原值记录，没有运行重建或重新计算指标。 | 未读取/运行权重，训练数据/超参仍不完整；发布的6图未验证汉字规范过程能力。 |
| [R11](../reviews/R11.md) | 本批完整读T2VLoraTrainer约240行encode/collate/compute_loss/validation，结合既有args/cache/冻结与配置。encode路径固定乘scaling_factor，未显式按invert_scale_latents分支；1.5的对应配置为true，兼容性需在相应依赖/完整pipeline中进一步验证。 | 未训练/推理、未测资源占用，未全审全部训练依赖/样例；invert配置和完整版本兼容仍待运行证据。 |
| [R12](../reviews/R12.md) | 既有完整10项tree、README/requirements/generate.py102行全文、HF adapter_config及相关Diffusers官方pipeline段均已读；本批重读README确认当前发布范围，未补出训练脚本。 | 训练/数据/验证脚本和精确底座revision缺失；未下载/运行权重、未测书写或硬件表现。 |

## 7篇论文仍未通过完整核心验收

本批完成了下面这些访问补查，未取得足以补齐缺项的文件。共有6篇缺完整论文（其中F05已有作者说明），另1篇缺实际原图。不能把摘要、空响应、检索缓存或截图引用标识当作已读原文。

| ID | 论文 | 当前缺项与补访证据 |
| --- | --- | --- |
| [A06](../reviews/A06.md) | Font Generation and Keypoint Ranking for Stroke Order of Chinese Characters by Deep Neural Networks | CCU作者成果页仅有书目，Springer全文仍未取得；截断转录不作9页全文。 [本次主入口](https://publication.ccu.edu.tw/user/377/research?type=0) |
| [L002](../reviews/L002.md) | Diff-Writer: A Diffusion Model-Based Stylized Online Handwritten Chinese Character Generator | 官方PAL 2023成果索引有该条，当前页面访问失败/超时，未取得ICONIP章节全文。 [本次主入口](https://nlpr.ia.ac.cn/pal/publications/P2023.html) |
| [L006](../reviews/L006.md) | Frequency-guided cross-modal diffusion for online Chinese handwriting enhancement | ScienceDirect可读摘要/引言与检索片段；未取得完整方法、实验及PDF，不以片段升级。 [本次主入口](https://www.sciencedirect.com/science/article/pii/S0020025526010674) |
| [L021](../reviews/L021.md) | Write More at Once，公开投稿版本 | 补查api.openreview.net/pdf?id=VdDtRu7RTf仍403；未取得完整PDF，搜索首段和相似ICDAR论文不替代版本证据。 [本次主入口](https://api.openreview.net/pdf?id=VdDtRu7RTf) |
| [L022](../reviews/L022.md) | Stylized Handwriting Generation of Arbitrary Structures and OOV Expressions，公开投稿版本 | 补查另一官方hash-PDF及api2 PDF入口，仍受403/challenge；搜索缓存前两页不足以完成全文和原图核查。 [本次主入口](https://openreview.net/pdf/6c8886af438417e6666dfb3cd4675854fcee6ca5.pdf) |
| [F05](../reviews/F05.md) | Online Cursive Handwriting Generation Using Trace Transformation and Symbol-Independent Point Classification Model | ICASSP官方PaperNum=13860的View Manuscript跳转IEEE文档11463098；本次返回HTTP202空响应。已核正式身份/作者，仍缺正式论文全文。 [本次主入口](https://cmsworkshops.com/ICASSP2026/view_paper.php?PaperNum=13860) |
| [L184](../reviews/L184.md) | Stroke-Seg: A deep learning-based framework for chinese stroke segmentation | 正式HTML/epdf全文文字可读，截图没有返回可查看的实际图像；作者上传ResearchGate PDF和直接PDF仍403。F1/3/4/5/6/7/9视觉缺项保留，F2/F8既有实图不扩展为全部。 [本次主入口](https://ietresearch.onlinelibrary.wiley.com/doi/epdf/10.1049/ipr2.13255) |

这7项需要可读的完整PDF/作者稿；L184也可由缺失图1/3/4/5/6/7/9的原图或包含这些图的完整PDF补齐。清单同时保留在[来源矩阵](../../data/remaining_source_access_and_reading_handoff_2026-10-25.json)。取得文件后，仍须实际阅读/看图才能升级，下载成功本身不构成验收。

## 对研究方案的影响

当前可直接推进的是规范/矢量基线的数据设计和原始字段适配。规范顺序、参考驱动几何、实际采集顺序、RGB可见事件及计划动作分别保留来源；任何两个字段之间的对应都需显式建立。静态OCR、类别mask、规则动画或模拟小误差均不能独立证明艺术字视频的正确笔顺。

可用数据仍需满足拟定实验所需的实例/方向/时间、许可及split条件。完整规范索引不替代8105字逐笔人工标注，资源协议审查不替代原始包验收，发布缺项也不自动改写为本项目已复现。
