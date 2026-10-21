# MetaQueries与Unified-IO：单向迁移、任务干扰和冻结语义

第九十三批补完[L062](../reviews/L062.md)、[L074](../reviews/L074.md)明确范围核心三遍及五条书面验收。目录仍354条（327论文／研究、27资源），187项核心/190项书面含未通过项，167条尚未确认核心（含资源）。[固定发布证据](../../data/metaqueries_unifiedio_protocol_release_audit_2026-10-21.json)区分正式书目、所读版本、源码和未验证假设。无删除、权重/数据媒体下载或模型复现。

## 原文范围和任务定义

[MetaQueries固定v1](https://arxiv.org/html/2504.06256v1)阅读Abstract/§1–6、T1–10及AppA/C说明，实际核F1原图与HTML原表T1–4/T9–10的重排渲染。PDF未完整取得，排除完整PDF阅读声明；没有核实正式录用，保留预印本身份。[Unified-IO固定v2](https://arxiv.org/pdf/2206.08916v2)33页，读完整核心§1–6/T1–7及指定任务说明，实际核p5F2/p7T3/p9T5–6/p10T7。ICLR2023官方入口确认会议，正式PDF本地403；所读版本是2022-10-04预印本。

MetaQueries处理MLLM到静态图像生成器的条件抽取；Unified-IO处理图像、文字、密集图与空间坐标的联合seq2seq。两者均未验证规范汉字书写视频。AR顺序、query位置、坐标排序、生成过程物理时间分别定义，不能互相替代。

## MetaQueries：条件接口及其可采信证据

附加可学习query参与冻结MLLM原因果attention，query hidden经24层双向Qwen式Enc-Proj connector进入SD1.5 UNet或Sana DiT。原文字理解不经过新connector。设计实验用.5B MLLM/64queries/Sana.6B/512²，主模型用256queries和.5/3/7B MLLM；Base connector已有316M参数，不应称仅训练极少query或冻结骨干无需反传。Sana发布分支采用flow matching：zσ=(1−σ)z+σε，预测ε−z并作平方误差；SD分支为其scheduler规定的噪声/velocity目标。

| 表/协议 | 原始数值及条件 | 限定结论 |
| --- | --- | --- |
| T1 query | learned64 7.43/.56/75.35；lastlayer7.49/.55/78.41 | FID略好、GenEval略高但DPG下降；512queries另为7.34/.56/78.43 |
| T2骨干/DiT | 冻MLLM+调DiT6.06/.61/76.66；全调6.28/.61/79.39 | 质量/对齐取舍，不能写冻结全面胜出 |
| T3connector | Enc-Proj24层316M/1.06×/FID7.43；Proj-Enc24层2046M/1.23×/7.41 | 前者省参数且对齐较好，FID略弱；宽度/容量也改变 |
| T4XL | COCO8.69用SD1.5；MJHQ6.02/GenEval.80†/DPG82.05用Sana | 不同decoder；†有prompt rewriting；理解为原路径成绩 |
| T5主体驱动 | .737 DINO/.852 CLIP-I/.301 CLIP-T | CLIP-T仍低于DreamBooth.305；不替代实体/几何编辑正确性 |
| T9知识/常识 | MetaQuery .55/57.67，lastlayer .48/52.83；DPG81.10<81.23 | 指定任务单向知识条件迁移，缺少显式问答→T2I等因果对照 |
| AppT10目标混合 | T2I7.43/.56/75.35；Mix8.27/.54/76.53，时间2.61× | 混合并未保持所有T2I分数；成本也增加 |

主预训25M×8epochs/global4096/lr1e-4→1e-5/warm4000，设计实验仅4epochs；Base指令3epochs/global2048，编辑1000步。重建结果本作另做重建微调，若干baseline直接解码encoder，不是相同适配条件。WISE部分外部结果只200/1000样本；CommonsenseT2I负prompt和CLIP评价需单列。重建/编辑、logo等多为定性，未有细笔OCR或过程约束表。

### 公开训练、数据制品和冻结细节

固定[GH a44e6e2](https://github.com/facebookresearch/metaquery/tree/a44e6e20edf25469a8160a244411950f5e4dcd25)小树、README、两配置、核心模型/训练参数/目标与curation指定段及eval说明。XL Sana配置仅CC12M、10epochs、per-device8、lr5e-5→1e-6、warm5000；3B指令配置10epochs/per-device1/warm2000。README明确公开CC12M示例不足保证原论文性能，不应把它伪装成25M完整配方。eval示例30步、COCO/MJHQ CFG3、GenEval/DPG CFG7.5；没有执行。

源码扩展词表以容纳query，解冻整张embedding表，用hook将旧词行梯度置零。固定环境Transformers4.49.0，train默认AdamW/weight_decay=.1；其[Trainer](https://github.com/huggingface/transformers/blob/v4.49.0/src/transformers/trainer.py)排除bias/norm，未排除embed_tokens.weight。对默认路径，旧行梯度为零仍不能单靠hook保证原值恒定：AdamW含w←(1−ηλ)w的衰减。它与“冻结原embedding/原理解路径”是不同实现条件。原实验可能有覆盖配置或保留独立理解分支，混合精度和保存过程也需检查；本次未取得权重/优化器轨迹，不能据此判原表失实。这里记录可复现疑点，不报告实际漂移或理解下降。

自然关联图像数据亦有三个需保留的版本差异：正文instruction生成器Qwen2.5VL3B，AppA和代码Qwen2VL7B；正文相似阈值.5，源码caption cosine先乘logit_scale再加bias，阈值50；正文target最小平均相似度，代码对图像相似矩阵取row-min再argmin。后者对称矩阵会倾向最不相似图像对的一端，无法等同平均离群定义，tie还受排列影响。均未据源码反推发布全量数据必按当前脚本生成。

同时核查[HF原始2.4M数据固定7b1c054](https://huggingface.co/datasets/xcpan/MetaQuery_Instruct_2.4M/tree/7b1c054ff00d25756edabec87d426c56940f938d)元数据/完整短数据卡，另有512res制品。卡标English/text-to-image/any-to-any、1M<n<10M和CC-by-NC/ODC-BY/CommonCrawl来源条款；没有完整样本协议、实际2.4M消费统计或媒体级验证。本次不下载Arrow/图像。论文数据策略仍应写“自然相关图像+合成指令”，不能提升为真实同主体编辑、精确动作或姿态变化真值。

## Unified-IO：统一输出与迁移证据

连续384²输入patch与文字/坐标进入共享encoder，decoder自回归预测文字/坐标或256个VQGAN码，再解码为256²RGB。深度/法线映射RGB，分割按实例随机颜色并在prompt给类别映射；词表32152文字+1000坐标+16384图像=49536。输出离散化不能被误写为输入图像也先经过VQGAN。71M/241M/776M/2925M不包含codec参数。

v2F2视觉核对见argmax‖z−zi‖，固定源码VectorQuantizer实际为平方欧氏距离argmin。最近邻的数学定义及实现一致，应把图示写法列为疑似符号错误，避免跟抄为“选择最远码”。本次没有核对正式排版是否修订此图。

95数据集/62源、8组22任务约130M任务实例。组别采样合成3/16、dense1/16、其余1/8，组内sqrt(size)；数据比例/采样率并不相同。text15%span和image75%mask预训各半；500K预训+500K多任务，Adafactor、前10K lr.01再1/√k、clip1，Large及以下global2048/XL1024、4路in-layer×128数据并行。具体TPU型号、总时长和训练方差未报告，不自行补数。

| 原表 | 数值 | 解释限制 |
| --- | --- | --- |
| T3GRIT | XLtest64.3；关键点67.7<MaskRCNN70.6，法线44.3<NLL50.5 | 全七任务覆盖相对只支持四任务有综合分优势，不能称四个共享任务分数翻倍 |
| T4same/new | 新概念定位74.4/分割64.2 | new只相对primary训练集定义，未排除全部web预训见过 |
| T5去合成 | Large250K Keypoint69.2→去合成200K18.3；定位63.4→62.9 | 匹配其余任务曝光而缩短训练；合成含T2I/补绘/seg条件，无法单独归因某一种 |
| T5去caption/NLP | 去caption VQA65.7→68.0，定位63.4→65.0；去NLP分类50.3→56.1 | 存在任务干扰，缺多seed/CI；不是所有目标互相促进 |
| T6额外任务 | depth.385优于UViM.467、弱于专家.330；ImageNet79.1/Places53.2 | 无单任务微调，但多任务与专门优化的成本/数据不同 |
| T7prompt | 训练模板78.9；Where is带空格41.5、去引号附近空格.1 | 小格式变化能大幅改变结果，提示鲁棒性不能只看语义同义 |

消融Large250K，移除组用200K/220K/235K保持剩余任务近似样本曝光；它验证的是这一资源分配目标，未实现等总FLOPs，也未验证XL相同因果效果。原文缺少VQGAN与采样/架构全因子，未提供统计区间。以“significant”措辞不得自行补写显著性检验。

固定[推理仓库ee0bd9d](https://github.com/allenai/unified-io-inference/tree/ee0bd9d848aafc855c0f3dbe24ac8714baa87496)13个blob完整树，读README/config及runner/network/VQ指定段：max_input_len默认64会truncate，论文最大256；文字默认beam、图像默认采样，返回depth为灰度/恢复尺寸图，不能直接当以米为单位的深度。README给四规模checkpoint下载入口，没有据此推断包含95数据混合训练脚本或执行过权重。A1.3分割有颜色聚类/删除<8像素连通域，需评其对细笔任务的信息损失；不能把自然图分割性能直接当汉字笔画正确率。

## 假设、验证设计及写作学习

MetaQueries的优势条件是源MLLM确有相关知识、接口可抽取、decoder能表达且训练覆盖待评输入。固定同MLLM/decoder和总预算，对query/lastlayer、learned/random、connector容量、冻/调以及显式问答→T2I进行受控比较，统一改写、负prompt和完整WISE样本；另测原embedding参数/旧理解行为，分开冻结、去wd及仅hook方案。重建与编辑应给各baseline相同适配，人工核验数据关系，按网页/实体隔离测试。

Unified-IO需同时给等目标曝光和等总FLOPs两组，拆开三类合成子任务并复核Large/XL、多个seed；报告每任务正负迁移及Pareto。先检codec重建/后处理的OCR、细笔拓扑和空间误差，再做模型预测。语义prompt改写×引号空格×tokenizer检查，公开模板规范化而非挑最好模板。过程研究还需同终态异笔顺、落抬笔与真实动作约束，不能从静态/空间任务迁移中推导唯一时间过程。以上均未运行。

科研写作上，MetaQueries从“保留原理解”的约束组织query/connector/冻结假设，Unified-IO从输出异构组织表示/架构/训练。应学习把每个设计对齐可检验消融，同时保留混合目标退步、任务干扰和专家弱项。Claim写具体版本、任务/分布/指标和实际预算，Limitations写数据真值、发布配方及代理误差；结构可表达性、经验表现和理论保证分别给证据。
