# Ming-Omni：多尺度桥接、上下文折中与原版发布

第一百七十一批完成[L160](../reviews/L160.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/mingomni_multiscale_bridge_and_context_tradeoff_audit_2026-10-24.json)。357目录（330论文／研究、27资源），277核心/282书面含未通过项；未确认核心53论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2506.09344v1)、[主源2](https://arxiv.org/pdf/2506.09344v1)、[主源3](https://arxiv.org/html/2506.09344v1)、[主源4](https://github.com/inclusionAI/Ming/tree/75fb7ec73bbc8d4c5391251e2ec90e99971d7cd9)、[主源5](https://github.com/inclusionAI/Ming/blob/75fb7ec73bbc8d4c5391251e2ec90e99971d7cd9/modeling_bailingmm.py)、[主源6](https://github.com/inclusionAI/Ming/blob/75fb7ec73bbc8d4c5391251e2ec90e99971d7cd9/modeling_bailing_moe.py)、[主源7](https://huggingface.co/inclusionAI/Ming-Lite-Omni/tree/ecd74fdae16ecb5a97429f943f262f7715ca2ee6)、[主源8](https://arxiv.org/abs/2505.02471)。

## 研究问题

怎样以稀疏MoE统一图/文/音/视频感知，并通过可训练的图像、语音桥接输出，同时保留感知底座能力并控制激活计算？

## 现有不足

模态token数量/表示/收敛不同，单一router可能偏置；生成和理解粒度不同、联合更新可能干扰。纯caption→生成器接口会压缩细节，但直接共享像素token也有优化折中。应区分路由选择、共享专家和生成器适配，检验理解是否真正帮助生成，不能只凭接口存在下协同结论。

## 贡献

Ling共享注意力+模态专用router；继承M2-omni平衡策略，感知PT/IT/AT之后冻结MLLM，图生成训练多尺度query/connector/DiT，语音训练独立ARdecoder+BPE/流匹配声码器。图桥接由文字描述扩展到隐藏表示，可静态生成/编辑/风格迁移。多模态支持与单任务成绩分别核，不把后继FlashOmni/2.0成绩移给Lite。Ming-Lite-Uni(2505.02471)为本报告明确指向的图生成配套前作，新增追引缺口，不把本报告三遍覆盖冒当配套全文已读。

## 输入、模块、输出与公式

输入T/I/V/A，经视觉/音编码投影并concat后入Ling；输出文字，或另经talker→音码BPE逆变换→flow/vocoder得语音，或query隐藏状态→connector→SanaDiT/VAE得静态图。视频仅输入理解，无视频/笔画事件输出。图生成先追加4²+8²+16²=336query及六边界token，一次骨干forward；公开generate仅处理16²隐藏状态并最终采一张图，低尺度query仍可经注意力影响16²，不能说完全未使用低尺度。不描述成必有三个低到高分辨率图像采样过程。

## 模型结构

Qwen2.5VL视觉约675M、Whisper音频；发布config及执行分支同时保留SANM，默认use_whisper_encoder=False走SANM，ASR示例显式True走Whisper，SpeechQA示例False；纠正旧“残留字段”未决项。Ling28层h2048/16heads/4KV，64路由专家每token取6+2共享，multi_gate=true；文本/image/audio各router选择同一expertpool，并非三套完全隔离专家。maxpos32768为配置。HFconnector为36层Qwen2 h2048，talker24层h896，Sana20层head70×32；2.8B是主体激活口径，不能替代包含connector/解码器的端到端总参数、显存与延迟。

## 数据分布与划分

F6全六配置：PT1图文885M/音389K小时；PT2图文576M/文494M/音389K小时；PT3图文613M/文494M/视频9M/音266K小时；IT1图文31.7M/文14.6M/音330K小时；IT2图文35.7M/文15.5M/视频4.3M/音400K小时；IT3图文36.3M/文15.5M/视频4.3M/音521K小时/audioQA8.3M。小时与条数不直接相加，跨阶段不当去重unique。caption迭代切片、模型分数阈值再MLLM质量过滤，评分定义/τ/T/成本不齐；结构化实体链接QA、8领域百科web与人工过滤、GUI/CoT/偏好41子类9领域。图生成IP2P/SEED-Edit2/3/UltraEdit、StyleBooth/WikiArt。附录T13新图21sources/T14音18sources小时/T15视频15sources全核；另内部web/合成数据。内部百科29924题/偏好1025/方言5×5000/五领域2252，训练测试按实体/说话人去重细节未齐。

## 指标与评价协议

T1八视觉指标；T2 RefCOCO系列grounding；T3GUI；T4InfoSeek Hmean/未见问题/实体；T5 GenEval六属性/DPG/FID；T6 OCR含低为优OmniDocBench；T7内部百科宏均值；T8视频四集；T9五维对话；T10ASR↓；T11语音QA七项；T12 SeedTTSEval中英文WER↓/说话人相似度↑。T12保留原文WER字段，不擅改中文CER。文字识别不证明生成图中文字正确，终态sketch不证明绘制时序。FID缺清楚参考集/N/采样协议不能单据4.85宣称所有现存方法SOTA；内部人工审题不等明确了最终评分者/盲评/重复次数。

## 对比方法

Qwen2.5Omni/Qwen2.5VL7B与32B/InternVL2.5/3/Gemma3/PaLIX/GroundingDINO；T2I专用SDXL/SD3medium/Emu3与统一Janus/Flow/Pro/SEEDX/TokenFlow。T10Qwen2Audio/Kimi，T11另Step/GLM/Baichuan/MiniCPMo，T12SeedTTS/MaskGCT/E2/F5/CosyVoice2。容量/训练数据/额外生成器/提示改写/推理预算不齐，作者以JanusPro改写解释GenEval差距但未作同提示受控对照，保留为作者归因。

## 实验条件和发布边界

v1完整28p研究§1–5、贡献§6和数据§7–9、T1–15/F1–8全部；无编号算法/公式，MSE/多尺度符号在正文。视频T8表注和§4.3/PDF均为统一128帧，修正旧32帧。感知训练继承M2三子阶段，生成冻MLLM、只训connector/query/DiT或audio decoder，具体LR/batch/steps/NFE/冻结精度/seed未齐。原发布README H80080GB/CUDA12.2、bf16约40890MB是作者demo报告非本项目实测；demoCFG6/20steps、T2I480×544/编辑512²、输入451584pixels；generate默认CFG3.5/30steps/seed0/512²，不冒当主表协议。GH固定75fb7ec73bbc8d4c5391251e2ec90e99971d7cd9125entries/109blobs，审README/config和11相关源码段。HF ecd74fdae16ecb5a97429f943f262f7715ca2ee6168files，五子配置核，16主权重分片/connector3分片与生成配套可见，未下载/运行。当前main已更换Flash系列，未混版本。

## 主结果

T1视觉八项均值约71.4对QwenVL71.5，Math71.6>68.1/OCR88.4>87.8，其余六项低；T2ground87.3<QwenOmni87.7；T3GUI82.1/84.1/66.6好于对应基线79.5/81.4/57.6。T4 InfoSeek27.7/30.4/25.4>QwenVL32B19.4/20.6/18.3，训练不同不独立归因结构数据。T5 GenEval.64>SDXL.55/JanusFlow.63，<JanusPro.80/SD3medium.74；DPG81.72<JanusPro84.19；FID4.85为该表最小，缺协议不足外推。T6对QwenVL Chart85.1<87.2/Doc93<95.6/Text82.8<85.1/OCRv253.3/52.0<56.3/57.2，OmniDoc34.0/34.4对30.8/39.8有升降。T7百科52.03>46.83，Vehicle41.91<42.29，原README多General类均值58.54是另一口径。T8视频59.4对59.2，Long56.6>54.7但VideoMME67.0<67.3/MMMU46.3<47.4，无CI不称显著。T9均值4.296>4.274但Richness3.498<3.828。T10中文均3.89/英文4.08/内部5.45，分别优QwenOmni4.05/5.04/14.79；内部方言五项强、Health/Knowledge/Local三领域非best。T11仅Alpaca4.63表内最高，MMSU47.53<61.32/OpenBook61.98<81.10，不能泛化全语音QA胜。全部数值表结构化。

## 消融及进一步实验

T12提供context-aware triplet训练版对标准版：中文WER1.69→1.98、英文4.31→5.10均退，说话人sim .68/.51各保持；不能以“加入上下文提升所有语音指标”概括，亦不证明上下文没价值，表缺上下文遵从/情绪匹配指标与等训练量说明。英文标准WER4.31也劣QwenOmni2.72/F5 1.83，sim .51<.63/.65。全文未给router/多尺度/MSE冻结策略的匹配消融，BPE35%/36%(50→约32Hz)为序列压缩报告，无量化端到端时延或独立BPE质量消融；可逆重编码保持既定码串，不保证有限模型生成分布/质量不变。音数据2%方言平台只有文字描述、未给曲线/数值。

## 局限与疑问

冻结感知参数避免生成loss直接改写旧权重，但不能证明生成采用底座知识，亦不能产生经这些冻结参数更新的双向迁移。公开图生成generate分支382–464无audio_feats读取，音输入在此未编码；有video_embeds时assert拒绝，默认入口的跨模态任意组合生成范围有限，未GPU运行、不否定论文其他能力。SANALoss有repa_loss标志/MLP但审阅文件未找到实际MSE计算或完整训练器，无法核论文对齐loss。三router共享专家池仍有共享参数干扰，缺路由分布/冲突量化。F8羊戴墨镜的文字配火车前后图，属展示配对不一致，未将其自动计模型指令失败。内部评测训练来源相似，但无证据认定泄漏；需独立实体/说话人划分、逐例分数与CI。

## 预期优势条件

已有强感知MoE、希望追加生成且控制对旧底座参数扰动时，冻结query桥接有适配优势；多尺度prefix可能提供层次条件、独立router让不同模态选择不同共享专家。对精细字形、多个实体引用、空间关系和过程时序，336query/只输出16²条件的表征保留能力仍需验证；终态风格转sketch不提供画笔路径。

## 可证伪实验

固定Ling/Sana/数据与可训参数/FLOPs，比caption、等token单尺度、多尺度随机/学习prefix、有无MSE、冻结/LoRA/全训，分别报理解和生成Pareto；shuffle或替换低尺度query检查其是否通过注意力作用于最终条件，公开各层表示与独立16²直接条件对照。三router对单router和独立expertpool匹配总/激活参数，测路由负载与梯度干扰。T12标准/context按等数据与预算，并报WER/sim及上下文忠实度、情绪保留、独立人评、首包/整句延迟；BPE对原码等音秒预算，不把token率降低当速度同比提升。补音/视频→图可达入口与先转文字/隐藏态对照；严格汉字/数字/空间布局/身份保留，再接真实逐笔序列和逆序/shuffle诊断。先精读配套Ming-Lite-Uni，避免将它已做的组件实验列为原创缺口。

## 论文组织与Claim学习

主干→声/图桥接→感知/生成冻结关系的组织可学，数据pipeline细节比笼统开源主张更有用。报告Lite激活量时同时列额外connector/decoder，数值表按PDF实际编号；HTML交叉引用有转换错误。Claim对齐任务/指标，保留context和richness退化，区分BPE可逆与模型质量、最终风格图与过程视频，明确配套论文贡献归属。

## 实际阅读范围

完整arXiv2506.09344v1 PDF28页研究§1–5/数据附录§7–9，贡献§6看范围，参考仅相关追引；T1–15每行、F1–8全部实际图片含八张原图及PDF音频三表视觉核；纠正32→128帧。三遍核心与五项书面，未独立口述/模型复现。原GH75fb7e固定125entries/109blobs，README与config全文、11相关源码下载并读router/模型构造/Whisper与SANM分支/query追加/generate/生成模块加载/SANALoss与BPE实现相关段，不称全部源码精读。HF ecd74fd元数据168files及connector/talker/transformer/scheduler/mlp配置核，未下载权重或执行模型。Ming-Lite-Uni配套全文另排追引，未借邻篇补本报告消融。

## 原记录更正

视频T8和§4.3的PDF明确每视频128帧，原32帧记录已更正。SANM并非仅凭字段能判废弃：代码构造两种音频encoder，默认False走SANM，ASR示例True走Whisper，SpeechQA示例False。T12的context训练版中英文WER1.69→1.98、4.31→5.10，sim不变；需补上下文忠实度指标后再判断折中。

## 多尺度与路由的实际含义

336query分4²/8²/16²，加六边界token后一次Ling forward；仅16²状态过connector/Sana采样。低尺度仍可经注意力影响最终状态，不能写成完全无用，也不能当已经逐尺度采样三幅图。T/I/A分别router选同一64expertpool，另有两共享专家；三router不等三组隔离模型。2.8B激活量不代表另含36层connector等的端到端成本。

## 跨模态生成与训练发布边界

原generate图分支无audio_feats读取，并拒有video_embeds，公开入口尚不足覆盖任意组合到图。SANALoss保留repa_loss/MLP定义，当前审阅文件未见实际MSE计算/训练器；不据此认定作者没训练。Ming-Lite-Uni(2505.02471)是明确配套前作，需单独补录精读后判断哪些消融或机制问题已被回答。

