# SEED-X / UniTok / SEED-Data-Edit：表示、旁路与过程监督

第九十批补完[L060 SEED-X](../reviews/L060.md)、[L061 UniTok](../reviews/L061.md)，追引补录[G040 SEED-Data-Edit](../reviews/G040.md)。目录353条（326论文／研究、27资源），182项核心三遍/185项五条书面（含未通过项），171条尚未确认核心三遍（含资源）。[固定发布及样本审查](../../data/seedx_unitok_seeddata_protocol_release_audit_2026-10-21.json)区分原文、代码、卡片、有限标注样本和研究假设。没有删除文件或运行模型。

## 原始来源与阅读范围

[SEED-X固定v2](https://arxiv.org/html/2404.14396v2)核心、AppA/B及指定AppC和全部T2/T3已读，实际查看源F3/F4/F7/F8。下载PDF未完整取得，未将其当全文证据；以固定HTML和原始图为阅读依据。v2注称新增评测/消融而不更新模型，未核实正式会议版本。

[UniTok NeurIPS2025正式24页](https://proceedings.neurips.cc/paper_files/paper/2025/file/bbe04d329d531e8814f1199098bd8fb6-Paper-Conference.pdf)与先读arXivv3核心核对，读主表、AppA/B和算力/无errorbar说明，实际核F2/T2/T6–8/F6/T10–11。未逐行遍读全部参考文献/checklist、所有底层库或完整训练实现。

[SEED-Data-Edit v1](https://arxiv.org/abs/2405.04007v1)为8页技术报告，读核心全部，实际核T1/F2/F4。报告没有定量模型结果主表、受控消融和独立Limitations节，笔记明确标注这些缺失，未为满足检查表编造实验。各篇的17字段、八项笔记、五条书面检查及具体未读范围见逐篇链接。

## 两条表示路线与同一误区

SEED-X以连续ViT特征连接Llama2-chat-13B+LoRA和SDXL；文字/框用CE，64个query回归图像特征，发布配置CE1+MSE6。编辑另接源图VAE细节旁路。分块加全局图处理宽高比，不能据此保证任意高分辨率无损。SEED-X、I、Edit为不同微调版本，§3.3.2未把全部能力纳入同一最终模型。静态图像/故事插图也没有建立连续视频、规范笔画事件或动作执行能力。

UniTok以8个独立4096条目的8维子码本表示每个空间位置，实际总条目32768；可能码组2^96，每位置原始96bit。256位置是256×8个子码，不能当256个单14bit码；“组合空间更大”也没有自动保证实际码熵、利用率或LLM可学性。图像LlamaGen与MLLM是不同下游实验，输出head层数也不同。

二者都表明需要把**重建上限、下游可预测性和任务成功率分别测量**。SEED-X F7的256特征重建选例细节较多，但F8由LLM预测256时反而失真；这些是定性观察，缺总体统计。UniTok T9的CLIP初始化零样本top1更高，却可在下游理解落后随机初始化，不能以单代理替代实际任务。

## 实验表格中的反例

| 工作/比较 | 原始结果 | 可支持范围 |
| --- | --- | --- |
| SEED-X T2 | VQAv2 71.2/GQA49.1；LLaVA1.5 78.5/62；MM-Vet43高于Dream36.6 | 若干统一能力有竞争力，逐项领先不成立 |
| SEED-X GenEval | 总体.51，SDXL.55；空间.18>.15，但计数.31<LWM.46 | 语义类别有取舍，不能替代OCR/笔顺评价 |
| SEED-X F7/F8 | 32/64/256、全UNet、多层resampler/预测条件反训的选例 | 未给定量全因子/多seed；不证明64普遍最优 |
| UniTok T2无CFG | VQGAN14.65→UniTok2.51，表差12.14，正文写12.11 | 小算术差异保留；基线384再缩256与UniTok256并非严格同条件 |
| UniTok T2有CFG | UniTok2.77，VQGAN2.34，gFID越低越好 | 优势受CFG协议影响；不能无条件引用无CFG结论 |
| UniTok T6 | joint VQA69.14>68.95，但GQA56.06<56.89、MME1333<1373等 | 不能将有限重建/分类观察写成所有理解任务均无冲突 |
| UniTok T7 | MCQ rFID.55/top163.7，RQ3.46/58.8 | 总条目相同，但码本参数和原始bitrate不同，非同成本纯机制对照 |
| UniTok T4及App | GenEval.59；GenAI-Bench basic.85/advanced.67 | 两个不同基准；GenEval低于Janus.61，GenAI的否定项与Liquid持平 |
| UniTok T5 | MJHQ7.46@256、Liquid5.47@512 | 分辨率不同，论文亦限制直接比较 |
| SEED-Data-Edit T1/F4 | 规模表与挑选案例，无模型量化主表/成分消融 | 未证明总体领先、各分量有效或多轮过程控制 |

UniTok T7 RQ共享32768×64约209.7万码本参数，MCQ8×4096×8约26.2万；RQ8层×15bit为120bit，MCQ8×12bit为96bit。这是按报告结构计算的原始参数/码率，不含其他网络、熵编码和实际使用率。不能用总条目数相同宣称参数与码率全匹配。T8各子码本设置的重建和对比曲线分别训练，也不能拼为同一联合模型的全部指标。

## 多轮数据存在与历史监督使用

SEED-Data-Edit T1精确3,669,644对、21,382序列、最长5轮；正文约3.5M自动、52K真实PS、95K人工。自动部分含检测/分割/擦除及反向添加，和caption修改/PnP/CLIP筛选两类；真实PS图重标指令，人工PS记录逐步静态图像和指令。没有操作鼠标轨迹、落笔/抬笔事件、连续RGB帧或机器人动作。

报告§4明确将多轮序列拆成单轮训练SEED-X-Edit，同时使用InstructPix2Pix/MagicBrush，decoder也在本数据训练且带源图旁路。16×A10040G约40小时没有给完整lr/batch/步数和split。F4只支持所选案例的指令/细节表现，没有历史条件、多轮链成功率或同底座同预算成分消融。由此无法将数据量、旁路、外部数据及共享主干各自贡献分离。

已核整体数据卡及OpenImages/Unsplash/Part2-3三个固定分包树。每包只用HTTP Range取一份split_0001.jsonl的首16KiB、解析前3个完整记录，共9条，没有下载图片或全量标注。报告A说Unsplash对应掩码擦除、B说OpenImages对应caption/PnP；首3条OpenImages有remove_object/mask_ratio，首3条Unsplash有source_caption/target_caption/match_score，来源—字段关联与文字不符。可能涉及版本、混合或命名，**该有限样本不足判定整个分包标签/管线颠倒**，也没有像素内容证据。需扩大有分母的版本化抽样后再判。

多轮首3条分别3/5/5轮，用source_image、edit_image_i、instruction_i表达；没有单独target_image字段。读入时需保留链ID和轮次，原图/编辑链同源分组再划分，避免拆单轮后同源泄漏。当前只提出验证方案，尚未执行全量去重/训练。

## 固定公开制品中的条件

- SEED-X GH `420d347dc50ba9ccdb8747efe9da3d250a50946c`：LoRA r32/alpha32/drop.05，64query、CE1/MSE6。SFT sh --batch_size50未传入DataLoader2构建，数据流batch6/context320，另有DS microbatch8；不能算成全局800。公开编辑配置仅Part1两个源，缺完整三部分/外部数据混合。默认edit1×1网格+全局图，有限缩放视图；t2i/edit50步、CFG7.5/1024默认，t2i seedNone/edit42，不直接当正式GenEval配方。
- UniTok GH `bb8012e8e8d7be66928bedd80506c56a55ea6305`：固定MCQ/投影/head及训练配置指定段，TokenEmbedder对8子码嵌入求和。正式lr1e-3/disc2e-4与源码/HF默认5e-4/2e-5不同；EVAL示例10crop/CFG1/temp.9不代表全表。公开README的部分GenAI-Bench子项与正式表不符，以正式表为准；带causal的实验名不能证明权重attention类型。
- HF SEED-X `534d2ff…`、UniTok tokenizer `7f6ea34…`/MLLM `710296c…`及数据各分包固定revision见JSON。模型/代码/数据/论文许可是不同资产，HF自定义/Apache2/MIT及数据CC-BY-NC4等不能全局合并。完整许可和全部底层实现未审完；没有权重、媒体下载或推理。

## 可证伪研究和写作学习

表示实验要固定encoder/decoder/LLM、数据、有效码率及训练推理FLOPs，交叉特征数、MCQ/RQ、attention/linear、recon/contrast/joint和源图旁路，分别测重建OCR/细笔拓扑、生成字形、语义组合与下游理解。报告正负迁移、同CFG/分辨率/候选数及多seed，不能只引用有利指标。书写另加同终态不同顺序、方向、停顿/接触和累计墨迹，判定改善是否真正涉及事件。

数据实验按原图/编辑链/来源分组，固定底座和总样本/FLOPs，对自动A/B、真实PS、人工序列做成分消融；比较flat、history、打乱history、等量单轮对照。逐步评指令完成、保留区LPIPS/OCR、身份及全链成功率，分真实/合成域与错误类型。若收益只来自源图旁路或样本量，应相应收缩共享协同/过程学习主张。以上实验未运行。

论文组织可学习“具体失败→表示/接口瓶颈→对应机制→匹配实验”的链条。Introduction避免把全部冲突归于单因；Method画清主干/旁路与阶段；Experiments保留CFG反转及joint退步；Claim注明版本、分辨率、flat/history及定性证据；Limitations明确未收敛、无区间/成分消融和发布配方不足。发现问题后仍需追检已有解法，不能直接视为创新课题。
