# CalliReader与AWCV-100K：识别、顺序及发布协议复核

第一百零三批完成已有[L045 CalliReader](../reviews/L045.md)、[L046 AWCV-100K/VCRec](../reviews/L046.md)指定范围核心三遍、实际框架/主实验和消融表、五条书面检查。356目录（329论文／研究、27资源），207核心/210书面含未通过项，149条未确认核心（含资源）。[结构化审查](../../data/callireader_awcv_reading_order_and_airwriting_audit_2026-10-21.json)记录来源与范围；未删除文件、下载权重/数据媒体、运行模型或复现原表。

| 工作 | 原始问题 | 已核来源 | 对书写视频研究的适用范围 |
| --- | --- | --- | --- |
| CalliReader / CalliBench | 静态书法全页/区域识别与文化上下文VQA | [ICCV2025完整11页主文](https://openaccess.thecvf.com/content/ICCV2025/html/Luo_CalliReader_Contextualizing_Chinese_Calligraphy_via_an_Embedding-Aligned_Vision-Language_Model_ICCV_2025_paper.html)、完整10页补充选定段落；固定[2503.06472v2](https://arxiv.org/html/2503.06472v2)交叉；实际p4 F4和p7 T3–8 | 高分辨率切片、视觉到文字embedding对齐、低资源适配和识别评价；OrderFormer处理阅读顺序，不处理字内规范笔顺 |
| AWCV-100K / VCRec | 普通RGB视频的空中书写识别 | [TCSVT2024 34(9):8602–8613](https://doi.org/10.1109/TCSVT.2024.3385851)出版元数据、[作者完整13页accepted稿](https://huuuuusy.github.io/files/AWCV100k.pdf)，实际p7 F6–9和p10 T6–11 | 30fps运动可观测性、跟踪误差、cross-writer与时空表征；未提供墨迹、接触/抬笔规范事件或视频生成能力 |

CalliBench与[L044 Calligraphy Bench](../reviews/L044.md)是不同资源。前者评价识别/上下文理解，后者涉及逐步书法绘制，不能按名称合并。TCSVT论文未核对应年度SCI分区，不标成已确认SCI一区。

## CalliReader：高分辨率证据与语言先验的边界

页面经YOLOv10检测、OrderFormer读序排序，单字448²图送冻结ViT/MLP，CalliAlign以四层Perceiver/三个查询将256视觉位置压为3个伪文本embedding。L2拟合归一化文字embedding，推理反归一后与问题、可用全局图像token一起送InternLM2.5-7b-chat。e-IT结合7357真实页面和6000诗词单字检索合成序列，仅LoRA微调LLM。每字位置压缩98.8%不能解释成全系统计算或时延减少98.8%。

| 证据 | 结果与解释 | 尚不能推出的结论 |
| --- | --- | --- |
| 主表T2 | Hard F1 .609 vs微调InternVL .511，+9.8百分点；NED .516 vs.579 | 不能把F1等同阅读顺序、笔顺或语义真实性 |
| T3文化VQA | layout77.81、author95.06、翻译STSim61.14、intent76.88；style75.33低于Qwen2.5-VL+ft78.67 | 未因果隔离款识、诗词记忆与视觉风格；句向量/judge分数非逐事实准确率 |
| T5模块 | 四层LN L2/Acc .096/.897优于两层.146/.865、GN.529/.791及额外损失 | 只支持所测配置，未证明归一化与LLM误差容忍的普遍最优 |
| T6微调 | e-IT+scale .609/.516；无扩增.600/.530；移除Align .489/.614；图像微调+Align .496/.617 | 需同数据暴露/总预算实验区分接口、合成数量与优化差异 |
| T7时延 | Easy1.48秒慢于1.32；Hard33.50快于41.29 | 较难输入中少重复/短输出可能影响计时，不能视为同输出长度纯算力优势 |
| 补充检测/外域 | Hard检测recall .830；OCRBenchv2 CN均值41.3>36.3，EN38.6<39.6 | 存在检测级联瓶颈及外语反例，不能声称所有通用能力均保留/提升 |
| 人研 | 142人含18专家、30随机页；.918 vs.512，NED .092 vs.590 | 40.6百分点相当于相对79.3% F1提升；NED相对下降84.4%；该子集不代表全部页面/人群 |

当前[固定GH](https://github.com/LoYuXr/CalliReader/tree/797808d4e394d03b918167b0412b7e616926b06a)完整树830个blob，核README、指定训练/推理/度量和embedding注入片段。`utils/utils.py::calculate_metrics`无序匹配每个字符，TP等于字符多重集的重合数量。静态推导GT“甲乙”、预测“乙甲”的F1为1，NED为1；需同时报告内容计数与顺序敏感指标。此处没有执行作者模型，也没有据此声称原表算错。`evaluate.py`当前GT去标点/数字，预测仅简繁转换；选择题按字母/文本包含规则，亦需复现时统一规范化与解析。

正文OrderFormer lr=.01，补充D2.2与公开默认训练lr=.0002；代码支持后者，但没有原训练日志证明实际采用哪项。正文CalliAlign64head，已读推理loader连接`models/perceiver_resampler.py`默认8head、每头64维，未下载checkpoint核形状。公开e-IT配置给per-device2、累积2/两进程通常有效b8、lr5e-5、LoRA r128/alpha256/dropout.05/maxlen8192，不能追认为原表全部条件。

### 当前发布制品与论文样本量分开

| 制品 | 固定revision | 已核情况 |
| --- | --- | --- |
| [gtang666/CalliReader](https://huggingface.co/gtang666/CalliReader/tree/14dbb524edb60a513b192f89b45f7e7b404e1089) | 14dbb524 | InternVL与params目录；根卡为demo/`gpl`元数据，内层README复制基座并标mit；不能作为统一模型授权结论 |
| [CalliBench](https://huggingface.co/datasets/gtang666/CalliBench/tree/b6d48f6c45cf90ba72a0edf2ae95f41bf7721ffb) | b6d48f6c | 卡列7个任务配置及apache-2.0；只核文本/目录 |
| [CalliTrain](https://huggingface.co/datasets/gtang666/CalliTrain/tree/7667b4f9297f211452e28fccde765fe6b8c0eb20) | 7667b4f9 | `data/train.parquet`；卡复制CalliBench3192叙述，但GH及规模API均7357 |

截至2026-10-21的[CalliBench规模API](https://datasets-server.huggingface.co/size?dataset=gtang666/CalliBench)报告Full_page3192、Author1194、Style750、Layout806，与论文一致；Bilingual2310、Intent191、Region726行，与论文500/500/727有差异。API没有固定到上述revision，行数也不等于独立图像数，可能涉及任务构建/重复和更新；未下载样本或确认原表实际使用子集。不能把不同配置相加统计独立页面/论文，也不能把当前元数据差异追认为原实验数据错误。

意图judge提示要求英语连贯、80%意图/20%支持，并宽容事实细节小错；两judge各三次平均只降低部分评分波动，未证明与专家真实意图完全一致。需做遮挡/替换诗句、罕见款识、作品/作者/内容互斥划分及实体级人工核查，检验视觉保真与语言补全的关系。

## AWCV：几何表征的收益和适用分布

102688视频、8819068帧、3755 GB1字、211人；按人约8:1:1划分。参与者20–30岁、210右手/1左手，覆盖背景/光照/视角不等于未见设备或人群泛化。T1手宽分箱67+140+24=231与总211不一致，源表数字保留并标疑。

指尖跟踪使用MediaPipe引用[40–41]。8D包括位置差、方向/曲率sin-cos、相邻stroke-id相同/不同指示；时序残差1DCNN后以轨迹片段作GAT节点。空间关系与时间信息相加、平均后分类。缺少`s_t`实际划分的充分公开说明，不能将片段节点或stroke-id当作规范笔画标注。

| 表 | 已核结果 | 评价边界 |
| --- | --- | --- |
| T3–4 | VCRec52.43%/3.9M/88.2FPS；ST-R3D23.40%/55.4M/168.7FPS；强时序1DCNN47.51%/1.1M | 分别+29.03与+4.92百分点；并非FPS全面领先，参数和跟踪开销未完全匹配 |
| T5融合 | A/B/C/D47.51/48.19/51.77/52.43；C/D均3.9M | 同参数融合D比C仅+.66百分点，需重复seed评估稳定性 |
| T6–7 | 去时序39.67；1DCNN+GAT52.43；GCN51.88、SparseGAT49.34 | 说明当前组合较好，GAT对GCN仅+.55百分点；热图不证明规范拓扑理解 |
| T8解码 | CTC49.66；FC1/3/2层50.43/51.43/52.43 | 正文单FC与最佳两层差异；F6图注写CTC，§VE说明英文多字符改CTC |
| T9传感器中文 | IAHCC96.85 vs1DCNN96.78 | 仅+.07百分点，无方差不判稳健收益 |
| T10–11英文 | WiTA CER30.12，差于29.24/29.86；IAHEW CAR96.51，差于97.45 | 支持已做跨语言实验，不能声称跨语言全面领先 |

已核实现条件为4×TITAN RTX24GB、112²、Adam/b8/lr.001、plateau乘.01、dropout.2、单层8head GAT；完整epoch/停止与FPS计时范围未核。当前[固定GH](https://github.com/wmeiqi/AWCV-100K-UCAS2024/tree/308bafd7100d92f30c80a090164d9470fd606933)265个blob是数据网站/静态资产，README给Baidu数据链接，未找到VCRec训练`.py`/配置或模型权重路径。网站CC BY-SA声明不能自动当数据集/模型统一许可。

## 可以检验的迁移假设与研究写法

CalliReader的有利条件是检测覆盖充分、单字库丰富而页面少；AWCV的有利条件是指尖稳定可跟踪、低帧率普通相机与空间结构显著的中文单字。前者需要用作品/诗词内容互斥、改字与遮挡对照检验语言先验，后者需要oracle轨迹、跟踪噪声、30→15→7.5fps与背景/设备外域对照。两者都需固定数据/计算、强预训练基线及按页面/作者或writer分层置信区间。

严格书写视频还需单独标注笔画身份、笔顺、接触/抬落笔、每帧可观测状态及动作合法性。对生成结果同时评价内容、顺序、运动可见性和端到端成本；规则SVG、纯轨迹渲染、独立识别与生成组合应纳入。上述为待执行实验，现有识别分数不回答生成过程是否符合规范。

可学习的写法是先明确输入/输出与应用约束，再以小实验验证设计前提，按模块接口组织Method，并用主表、局部失败、外域和组件对照共同约束Claim。Limitations应包含检测/跟踪级联、内容先验、样本和发布协议差异、跨语言反例；“小参数”“压缩”“泛化”都需要带成本范围、分布及指标。
