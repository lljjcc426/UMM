# Unified-IO 2 / AnyGPT：统一接口、共享收益与评测条件

第八十九批补完[L058](../reviews/L058.md)、[L059](../reviews/L059.md)正式核心三遍与五项书面。目录352条，179项核心/182项五条书面（含未通过项），173条未确认核心三遍（含资源）。[固定制品审查](../../data/unified_io2_anygpt_protocol_release_audit_2026-10-21.json)记录代码、模型卡与未决项。没有删除文件、下载权重或运行模型。

## 版本和真实任务

[Unified-IO 2](https://openaccess.thecvf.com/content/CVPR2024/html/Lu_Unified-IO_2_Scaling_Autoregressive_Multimodal_Models_with_Vision_Language_Audio_CVPR_2024_paper.html)为CVPR2024 pp26439–26455；读正式17页核心及官方20页supp指定段。统一encoder-decoder输入文字、图像、短视频/音频历史等，输出文字、图像/音频码或坐标/动作。视频理解、下一帧预测和动作接口未建立规范笔顺RGB过程的能力证据。

[AnyGPT](https://aclanthology.org/2024.acl-long.521/)为ACL2024 pp9637–9662，正式26页。四模态为文字/图像/语音/音乐，没有视频流。Llama2-7B对离散码做next-token，SEED/unCLIP、SpeechTokenizer/SoundStorm和Encodec负责模态变换。图像最终用扩散decoder，不能据AR主干将整条输出链记成纯AR一步生成。

已实际核看UIO2主F2/T2–4、suppF3/F5/F6及AnyGPT F1/T2–8；读完核心研究文字与指定补充协议。未逐条读全部任务清单、合成提示、画廊、参考文献，也未全审所有底层库。完整范围和每篇17字段、五条问答以逐篇笔记为准。

## 表示和训练机制

UIO2为24层encoder+24层decoder，L/XL/XXL约1.1/3.2/6.8B。图像ViT-B、音频AST的第二层与倒数第二层特征作为输入，历史经Perceiver压缩。1000坐标bin、RGB编码的dense map和文本动作原语提供通用接口。Mixture-of-Denoisers是离散mask/重建训练；dynamic decoder mask防止去噪目标从AR teacher-forcing泄漏，tokenize后动态packing减少padding。它们不能直接归入Gaussian DDPM机制。

AnyGPT图像32个SEED码/8192词表；语音只让LLM预测首RVQ层1024词表，SoundStorm补后7层；音乐4层×2048词表按帧展开，5秒约1000码。正式T1音乐8192与正文及代码一致，**旧笔记的4096冲突对该正式版解除**。独立codec保留什么信息会约束后续可达能力，32个图像语义码没有自动保证细笔/OCR保真。

AnyGPT先学text↔X，再用GPT4文本对话经DALL-E3/MusicGen/AzureTTS多模态化。已知p(X|T)和p(Y|T)一般不足以确定真实p(X,Y|T)，可以存在多个相同边缘、不同耦合的联合分布。若直接乘积，则额外假设条件独立。合成对话可提供某种耦合监督，但不能保证与真实图像—音乐关系一致。这是方法适用条件的推论，尚未测实际误差。

## 影响结果解释的协议

| 研究/项目 | 正式结果或条件 | 结论边界 |
| --- | --- | --- |
| UIO2规模 | GRIT L/XL/XXL60.8/65.2/66.9；法向44.5/46.7/45.2 | 综合随规模提高，逐项全提高不成立；FAD XL2.59也优于XXL2.64 |
| UIO2图像 | FID13.39，CoDi11.26/Emu11.66；TIFA81.3高于二者 | FID/TIFA取舍；PT T2的TIFA78.7与IT T4阶段不同 |
| UIO2图像采样 | suppG6 COCO30K captions×8候选、CLIP择优；CFG FID13.39→33.77 | 候选成本约240K次；质量主张需保留筛选/CFG，不直接等同1候选协议 |
| UIO2音频 | AudioCaps取四个真实2秒片段作history再生成下一段，FAD2.64 | 带真实音频续写；作者明确与纯T2A不可直接匹配，AudioLDM1.96/CoDi1.80更低 |
| UIO2动作 | VIMA全动作从初始图像open-loop预测；L1/L2/L3/L4=71.3/70.4/68.0/15.5 | 新对象与新任务分开；对象中心VIMA有不同信息/反馈，avg72.6高于UIO2 56.3 |
| AnyGPT caption | CIDEr107.5，Dream115.4/Emu112.4；灰SEED123.6标有训练样本 | 保留灰字和异训练条件；LAION-COCO不能误记为MS-COCO |
| AnyGPT图像 | CLIP .65 vs SEED.69/GILL.67/Emu.66 | 语义相似不评价细笔/文字事件；无FID或规范笔顺表 |
| AnyGPT语音 | ASR WER8.5 vs Whisper2.7；TTS8.5/.77 vs USLM6.5/.84 | ASR训练57Kh/680Kh不同；TTS WER/SIM属于自动评价，无MOS替代关系 |
| AnyGPT音乐 | caption CLAP.11 vs real.16；generation.14 vs Riffusion.19/Mousai.23 | 五秒和指定指标，不能推广长音乐或全部any-to-any组合 |
| AnyGPT base/chat | 主T2–6测预训练base，chat主要案例 | 缺受控机制消融，不能归因为AnyInstruct使所有指标改善 |

UIO2 suppF5展示多模态训练gradient爆炸、XXL loss/accuracy崩塌，F6给稳定配方下三规模训练曲线；缺各改动的完整定量全因子。AnyGPT核心及所读AppA–C无独立机制消融：主比较、超参表和案例分别说明用途，不能捏造消融来满足检查表。

## 固定发布、资源和冲突

[UIO2固定源码](https://github.com/allenai/unified-io-2/tree/502ac4d81239f82c891a9f412b000c3c8d4e2946)的实际图像码本16384，+2保留token后TPU补齐head16512；音频代码8192，+2后补齐8320。正式正文/D1音频8196与代码不一致，不能把8320当codec大小。主图audio输入256与D1/配置128也未解；4帧历史总128视觉/64音频与每帧32/16一致，不把它们混成同一矛盾。

UIO2 suppD5 PT/IT batch512/256，后文称effective512及各约1Ttoken，主文语言比较约250Btoken；单位/packing口径未完全解释。主文220任务/120数据集与T10合计227 data sources也分开保留。深度专调和K400额外5epoch属于额外诊断，不能合进通用未专调主表。G4 caption条件VQA84.6 vs58.5与主文84.6 vs81.2需要后续核对版本/设置。

UIO2 README链接S3三种3m checkpoint，初始管线只含部分任务；注明多数正式分数由离线评测得到，公开seqio指标主要做validation。另有官方PyTorch仓库，尚未深审；没有把未审查说成没有发布。config、base/large/xxl gin及target码偏移指定段已核，未全审底层训练器或运行。

[AnyGPT固定源码](https://github.com/OpenMOSS/AnyGPT/tree/fc3bcc4e9dd76edec8a63300b7ae163a9ecec3d4)包括训练/推理和词表。两个公开sh全文显示stage1 4096步/lr3e−5，论文81K/lr6e−5/b480；stage2 context4096与论文4500不同。节点数来自Slurm，不给定实际总GPU，不能靠每节点8GPU推算原训练总成本。CLI按模态加载配置，当前文字sampling与论文beam5不同；通用config中beam5没有覆盖该路径。

固定[base](https://huggingface.co/fnlp/AnyGPT-base/tree/7f3d03542f4dfa7738978f5f07918490e0a932e5)、[chat](https://huggingface.co/fnlp/AnyGPT-chat/tree/c8999624b077b3837f32c3948f0f9e90bd67b860)、[AnyInstruct](https://huggingface.co/datasets/fnlp/AnyInstruct/tree/3949858dd47345b63bdb310209087dbef47c593f)卡与元数据已核：模型metadata Apache2与正文Llama2许可相冲突；base config最大位置2048与论文context4500的runtime关系未全追；speech_conv卡108K与正文另100K有差；主图像包为224²，另链接1024版。均保留未决，未下载权重/媒体或执行模型。

AnyGPT T7 Youtube-Music-1M写100M pairs，而正文为>1M视频，唯一视频/切片/对数口径未知；caption主要从Spotify元信息及歌词合成，不能保证实际音频忠实。音乐decode对整数取模2048并丢尾部不足4码，可能掩盖非法层序列；这属于代码语义，尚未统计生成时的发生率。当前20秒music input参数不构成20秒输出评测证据。

## 科研假设和写作学习

共享接口的优势应在相同codec、原始数据、总训练token/FLOPs、观测信息和推理采样成本下，与独立专家/共享主干及等量文本SFT比较。对UIO2交叉norm/RoPE/mask/packing，对AnyGPT交叉text↔X、真实X↔Y、合成对话，报告base/chat和未见任务/模态组合的正负迁移及多seed区间。上述实验未运行。

图像一候选/八候选、纯文字音频/真实history/生成history、open/closed-loop动作分别成对控制。书写任务先测codec重建的字形/OCR/细笔上限，再测同终态不同过程的顺序、方向、暂停、接触和累计墨迹；不能让终态语义相似替代过程评价。创新点需继续检索已有解决方案后再定。

Intro可学习“任务接口困难→训练稳定/数据稀缺→对应机制”的连接，Method按数据流及训练阶段组织；Experiments需把每项Claim关联可比较协议。Limitations应保留逐项退步、codec/短序列瓶颈、缺机制消融、合成域偏差与资源未决。没有原文定量消融时，明确指出缺失并设计可证伪对照，比重新命名主表更可靠。
