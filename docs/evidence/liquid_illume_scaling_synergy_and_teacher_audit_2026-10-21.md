# Liquid与ILLUME：规模、协同、教师信号及发布协议复核

第一百零四批完成已有[L088 Liquid](../reviews/L088.md)、[L089 ILLUME](../reviews/L089.md)指定版本核心三遍、实际框架/主实验与消融图表、五条书面检查。356目录（329论文／研究、27资源），209核心/212书面含未通过项，147条未确认核心（含资源）。[结构化审查](../../data/liquid_illume_scaling_synergy_and_teacher_audit_2026-10-21.json)含来源、制品revision与后续候选；未删除文件、下载权重/数据媒体、运行模型或复现原表。

| 工作 | 证据版本 | 实际问题与适用边界 |
| --- | --- | --- |
| Liquid | [IJCV2026 134(1), article39](https://doi.org/10.1007/s11263-025-02639-5)身份，2026-01-07在线；方法结果读完整[arXiv2412.04332v4](https://arxiv.org/html/2412.04332v4) | 已有LLM扩离散视觉词表，检验规模和文本/理解/生成训练相互作用；正式期刊全文受限，不能把v4全部细节标为正式全文已核；未核年度SCI分区 |
| ILLUME | [ICCV2025完整11页正式主文](https://openaccess.thecvf.com/content/ICCV2025/html/Wang_ILLUME_Illuminating_Your_LLMs_to_See_Draw_and_Self-Enhance_ICCV_2025_paper.html)，辅以[唯一arXiv v1](https://arxiv.org/html/2412.06673v1)附录A | 连续图像理解输入、语义离散生成、扩散解码与教师引导SFT；正式补充下载不完整，未作为已读证据 |

两者主要量化静态图像/文本任务。交错图文样例及未来视频方向不构成书写视频、规范笔画事件或字内笔顺实验。

## Liquid：统一接口与经验规模趋势

Chameleon预训练VQGAN将512²图压为32²=1024码、码本8192；图像码偏移后扩入LLM词表，与BPE文字通过同一因果decoder预测。Gemma7B发布配置28层、hidden3072、16head/16KV、vocab264192。主体无需新增CLIP分支或扩散decoder，但仍依赖外部预训练VQGAN。基础Gemma/512、†额外epoch、‡LLaMA2/UniTok256结果属于不同条件。

继续预训30M文本（DCLM15M/SlimPajama12M/StarCoder3M，约60Btoken）与30M JourneyDB/内部MJ风格图文（约30B图像码）；20%T2I反转为caption。混合60M与各30M单任务版本比较。SFT3.5M=1MLMSYS+1MT2I+1.5MMiniGemini。交错定性§4.4另加入交错数据，不能称模型完全未见交错训练。

| 已核实验 | 结果 | 合理解释与边界 |
| --- | --- | --- |
| F3规模/loss/生成分数 | 六规模0.5/1/2/7/9/32B，VQAScore-vs-loss线性拟合R²=.9051 | 经验关系；跨基座家族、未给完整compute-optimal幂律系数/不确定性，不能当普适理论 |
| F5语言差距 | 平均差距总体缩小但不单调，32B仍约.5百分点 | 不支持所有语言冲突已消除；0.5→1、7→9局部不单调 |
| F6视觉差距 | 混合视觉验证loss在所有规模仍劣于T2I专训；9/32B VQAScore差距小 | 作者提示评价可能饱和，分数差小不能证明表示或优化冲突消失 |
| T1扩数据 | 30M基线gFID19.9/MME909.6；加10M生成12.8/1066.8；加10M理解14.9/1035.1 | 更多数据下两个任务相关收益；缺同总计算/普通数据增量对照，尚未识别共享梯度因果 |
| T5语言控制 | 原Gemma MMLU62.6、文本继续55.5、Liquid56.0；Qwen32文本68→混合66.5 | **原表有原始基座和文本继续训练控制，旧笔记“缺少对照”的暗示已纠正**。应同时报告相对两类控制的变化 |
| T2–4生成 | FID5.47较SDXL9.55/PixArt6.14好，较Playground4.48差；GenAI基本.83/高级.65 | logical.46低于SDXL.50/VILA.53；WISE总体.41低于SDXL.43/PixArt.47/FLUXdev.50，不能声称全部指标领先 |
| T6理解变体 | 基础VQA68/GQA56.1/Text40.4；†71.3/58.4/42.4；‡76.8/61.1/51.6 | 额外epoch、基座、tokenizer与分辨率变动需明示，‡不能写成基础Gemma同checkpoint |

实际核看v4 F2框架、F3/F5/F6及T1/T5；全部T1–6逐项读取。原Gemma一行ARC-e53.8/ARC-c81.0似有列序疑点，未追原基座评测核定，按原表保留并排除出优势推论。FID、VQAScore和通用VQA不测笔顺或逐帧状态。

### 当前公开制品的复现范围

固定[GH b2a7dd53](https://github.com/FoundationVision/Liquid/tree/b2a7dd53bb02ef9728a848d3aa8aaf1955553b02)完整76blob树，读README、Data/TRAIN、指定评测/核心训练/采样片段；固定[HF a0e7b763](https://huggingface.co/Junfeng5/Liquid_V1_7B/tree/a0e7b763fe3869d383a22c64cde1a9dcaab65160)卡/config/generation/目录与trainer_state。只确认7B指令模型，六规模pretrain发布在清单仍未勾选，不把模型卡列出的规模当已公开权重。

| 条件 | 固定论文v4 | 当前公开脚本/资料 |
| --- | --- | --- |
| 更新与批量 | lr2e-5、b1024、context2048、ZeRO3；规模constant、其他cosine；≥7B clip.5/max-z | 默认示例LoRA r64/alpha16/drop.05；8进程×perGPU4×accum4通常有效128，非原实跑日志 |
| 任务比例 | 图文80%T2I/20%caption | `T2I_ratio=.1`按collator分支为10%T2I/90%caption；默认参数值与显式脚本也需区分 |
| 数据可得性 | 内部高质量图文 | Data.md明确JourneyDB单独不能复现文生图；understanding SFT/多比例提取部分WIP |
| 环境 | 论文未统一给全步骤依赖 | expand-vocab的`mean_resizing`需Transformers≥4.46，训练推荐4.39.2；分步骤依赖不能简单合并成同环境要求 |
| 生成 | 1024图像位置AR | 默认4样本、CFG7/temp.99/topk4096/topp.96；采样过滤函数会屏蔽文本词表，未发现“完全没有图像mask”问题 |

公开目标会mask指令前缀；统一CE也要区分输入条件与实际监督位置。`get_fid.py`调用clean-fid，不是CLIP语义评分。HF trainer_state来自指令checkpoint，global_step88688/epoch2；没有证据将其当作原60M混合预训日志或据其推导GPU数/完整训练成本。论文“100×”需计入复用的LLM/VQGAN历史训练边界；未以公开小例配置验证该倍数。

## ILLUME：语义码、连续输入与教师反馈

UNIT语义特征一支连续送adapter/Vicuna7B作理解，一支量化成16384码本/256生成位置。语义重建为smoothL1与cosine目标，随后SDXL仅attention训练作像素解码。LLM next-token、quantizer重建与扩散训练是不同阶段目标。

I阶段LLaVA558k+COYO600k重建预热新视觉embedding/head与adapter；II15M包括EMOVA、COYO及内部7MT2I；III约7.36M指令/图文/编辑与50K评价样本，主图四舍五入7.3M。**另外tokenizer用COYO80M，SDXLdecoder用COYO4M+内部6M**，还复用Vicuna、UNIT和SDXL。15M是LLM对齐阶段用量，不能解释为整个模型只训练15M数据或比Janus端到端省4倍算力。

正式T5三阶段batch256/1024/1024、steps5000/15000/8000；I adapter1e-3/视觉embedding-head2e-4，II5e-5，III所有组件2e-5。旧v1 III视觉2e-6与正式版不同，实验条件以正式主文为准。论文给32节点、每节点8Ascend NPU、约3天；不能写成总共32NPU。v1附录A的tokenizer/SDXL实施参数作为版本限定补充，正式supp未完整读取。

| 证据 | 已核结果 | 能支持的范围 |
| --- | --- | --- |
| T3直接联合训练 | GenAI.63与gen-only相同，GenEval.56低于.58；理解多项提高但MMVet27.4低于28 | 作者明确未见明显直接互促；联合目标本身不足以证明协同 |
| T8教师评价数据 | 1.3M子集加50K：MME1358.6→1446.7、GenEval.56→.59、计数.35→.43 | POPE86.4→86.1、位置.34→.33反降；需等量优质教师SFT/曝光/调用预算对照 |
| F6语义tokenizer | 同20MT2I、均扩散解码512²条件，语义码loss/FID较好 | tokenizer预训/码熵不完全匹配，跨词表CE不可单独作公平对齐效率指标 |
| F7初始化 | 梯度尖峰较少，II后FID11.2→10.7 | 多了I阶段计算；未给等计算控制或理论收敛证明 |
| T9连续输入 | COYO5M+LLaVA665k下POPE85.4>83.5、MME1408.5>1213.7、SEED67.8>61.3等 | 支持局部连续输入收益，不能证明所有离散tokenizer均不适合理解 |
| T4理解主表 | POPE88.5/MMB75.1/SEED72.9/MMVet37/Doc76 | MMVet低于LLaVA-NeXT43.9、Doc低于Emu3-Chat76.3；非各列最佳 |
| T6生成主表 | FID7.76好于SDXL9.55，差于VILA384 7.69/PixArt6.14；GenEval.61持平Janus | 颜色/位置/颜色属性低于Janus；GenAI.75/.60低于SDXL.83/.63 |
| T7编辑 | DINO.791低于EmuEdit.819、CLIPI.879最高、CLIPT.260低于PUMA.270 | 图像保持与指令改变是不同目标，CLIPI高不能单独证明编辑成功 |

50K流程先由ILLUME生成训练prompt图，再由**GPT-4o**给对象/计数/颜色/关系评分及分析；好例单轮assessment、坏例assessment+refinement两轮SFT。其名称self-enhance不消除教师监督或额外数据/推理成本，也未给每次测试必须自评修正的量化协议。需把自身评估能力提升与外部教师提供训练信号分开检验。

实际核正式p3 F3以及p8 F6/F7/T8/T9，完整T1–9。原论文一手链接与选定仓库/模型检索未确认原版完整训练/权重发布；检索结论不代表穷尽所有网络位置。未下载任何权重，也没有实现或复现这两篇模型。

## 后续工作与可证伪问题

发现池原已包含[ILLUME+ 2504.01934](https://arxiv.org/abs/2504.01934)和[ILLUME-X 2606.30054](https://arxiv.org/abs/2606.30054)，本批明确进入后续原文与发布审查队列，尚未新增到356主目录或计核心完成。前者[作者仓库](https://github.com/illume-unified-mllm/ILLUME_plus)README给3B/7B、DualViTok/SDXL制品与训练入口，但diffusion decoder训练仍未勾选发布；后者[作者master仓库](https://github.com/ChonghuinanWang/ILLUME-X)给交错图文模型/ILScore、推理与权重、数据coming soon。各自正式会议身份和完整方法/实验仍待下一项核查。后续制品不能当作原ILLUME的已发布复现。

对统一模型的关键验证是固定基座/codec/总token与FLOPs，同时比较共享、独立、普通数据增量、重复曝光和梯度隔离；Liquid还要同时保留原基座与等计算文本继续预训控制。对ILLUME的50K需要等量普通教师SFT、筛选、打乱评价、去推理/改图及独立专用模型，匹配GPT调用成本，报告多seed与各属性CI。用细粒度OCR、反事实字符/逻辑/计数/位置及外域文字检验指标饱和和语义压缩失真。书写视频另测每帧状态、笔画身份/顺序与抬落笔事件，加入规则SVG/轨迹渲染和独立识别强基线。以上均为待执行实验设计。

研究写法可学习：先将成本、优化和互促拆成具体可测问题；Method按数据流与阶段冻结范围组织；每个设计对应局部对照和失效指标。经验相关、额外数据收益、条件性假设与理论保证分开表述，Limitations保留历史预训成本、教师、内部数据、版本与未匹配计算，避免将静态图像能力外推为规范书写过程。
