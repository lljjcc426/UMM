# Omni-Diffusion：连续语音接口、版本差异和解码启发式审查

第一百二十七批完成[L113](../reviews/L113.md)明确范围核心三遍及五项书面记录。[结构化证据](../../data/omni_diffusion_audio_interface_and_versioned_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），236核心/239书面含未通过项；未确认核心94论文／研究+27资源。资源按制品协议另审。没有新增目录、删除文件、下载权重、执行模型或独立复现。

以[ICML2026正式15页PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/li26dv/li26dv.pdf)和[官方接收记录](https://proceedings.mlr.press/v306/li26dv.html)为主，另对照[arXiv v2](https://arxiv.org/abs/2603.06577v2)。版本名、检查点和实验条件必须保留，后续版标注optimized不能替代逐项结果比较。

## 研究问题、实际数据流与方法

将Dream7B masked dLLM扩展为文字、静态图像与语音理解/生成，特别是语音驱动图像生成与视觉问答，并研究mask采样的质量/步数/长度折中。没有视频生成、汉字规范笔顺或真实绘画动作任务；inpainting定性示例不等于已系统评估任意指令编辑。

AR长多模态序列串行，已有离散统一工作任务范围和语音视觉联合能力有限；直接扩Dream又遇到pad目标过多、图像上下两端重复纹理、联合语音输出缺文本语义及初始mask长度难定。三阶段数据、pad掩码衰减和三类解码启发式分别处理这些具体问题，但缺全部组件及共享训练正迁移的充分控制消融。

共享masked-Dream主干和clean-token CE，MAGVITv2图像输入/输出、SenseVoice连续输入/GLM4Voice离散输出；三阶段训练与合成SDVI，tail-pad mask缩放gamma.6、负熵提交、图像位置惩罚、语音边界预填和长度比例初始化。摘要的统一离散token概括须结合§3.2：语音输入连续特征，不能写整个系统每个模态输入都经离散量化。

文字→Dream tokenizer；图像→MAGVITv2离散码；输入语音→16kHz fbank→SenseVoiceSmall连续语义特征→LayerNorm/两层MLP→主干embedding位置。输出文字直接解码，图像8192码经MAGVIT decoder，语音16384 FSQ码/12.5Hz经GLM4Voice flow/HiFT waveform decoder。图像/音频codecs不等主干本体。正式p4/5/6/7/8/13/14/15八实际PDF页已看，包括框架、全部八表和位置/预填消融。

Dream7B-Instruct初始化，HF固定config为28层hidden3584/FFN18944、28Q/4KVheads、RMSNorm、RoPE1e6、maxpos131072、vocab176264；元数据8,037,762,367 BF16参数不等包含所有外部codecs的总系统。训练maxseq3072与配置maxpos有别。MAGVITv2 stride16/8192码；256mask图像对应256²是按stride推断，非全部评测分辨率已齐。Eq1条件不mask、目标clean CE；负熵c=sum(p logp)，高c低熵优先提交，已提交码不改。语音预填在.25L后并行文本/音频，不是先完成整段文本再AR语音的流程，也不保证精确对齐或实时流式。正文位置系数gamma_p<1降低尾部logits，仅软调采样/提交，非严格因果约束。

正式T4：Tulu3 SFT670K全三stage；LAION2B caption10M前两stage；LLaVAOneVision820K+inhouse2M VQA后两stage；JourneyDB4M两行完全重复，来源未解释，不能擅计8M。ASR Libri100h/CommonVoice17 100h/Giga1000h/Peoples100h/VoxPopuli54h；TTS Libri58h/GLOBE50h/Emilia5000h；VoiceAssistant400K实际250K、AudioQA1M实际180K均后两stage。SDVI SpokenVQA约30K及speech-image30K第三stage，CosyVoice2合成，问题音色由1000条Giga片段克隆、回答固定声音；过滤数学/程序和>100词回答，多选改简答。COCO2014val随机10K描述/图像作生成评测，MME问题同样合成语音，缺随机seed/完整split去重/音色disjoint证明。内部2MVQA与完整原样本未公开定位。

ASR/TTS WER由WhisperLargeV3转录（TTS为再识别误差），不覆盖音色/自然度/韵律；POPE/MMEP/MMMU/SEED2Plus；图像CLIPT与文本对齐/CLIPI与配对GT相似，不直接测细字正确或完整视觉质量；v2另DPGBench聚合及分项。效率秒/图与RTF=延迟/语音时长，RTF<1不证明首包延迟或流式。没有笔画/书写事件/时序OCR/视频一致性评价。

AppA AdamW(.9,.95),eps1e-8，stageI/II lr1e-4、III1e-5，b128/maxseq3072，pad gamma.6、N=L−100、位置最小系数.5。论文未齐原GPU/总步数/总时长/各任务CFG与全部计时边界。TTS初始mask=3.5×文本token，ASR=.2×语音长度，非学习到任意长度；跨语言/语速需独立验证。发布微调例8卡×b1×acc16=128、24ksteps/lr1e-5、cosine/warm.03/wd0/clip1、seed956、默认seq1024/图256，属于现有模型微调例，不能代替三阶段原始配方。TTS评测例长度3.5、steps=L//2、temp0/top_p.9/重复惩罚1.2，无RTF计时实现于所读函数；其他采样入口有CFG额外前向。

AnyGPT/GLM4Voice/CosyVoice/CosyVoice2，InstructBLIP/LLaVA1.5/mPLUGOwl2/MiniGemini、LaVIT/Emu/Chameleon/VILA-U/Show-o/MMaDA/NeXT-GPT/NeXT-Omni等，缺多项完整结果，数据/预训/总参数未同预算。NeXT-Omni的特定DFM实现对比不能推成所有DFM必全token更新、MDM必与DFM理论互斥；已有masked离散flow路径需另追引。固定自身checkpoint多步数/位置惩罚消融较接近控制实验，仍无多seedCI。

## 正式版与v2：不可混用的结果

| 项目 | ICML正式版 | arXiv v2 |
| --- | --- | --- |
| ASR/TTS WER | 6.69/2.22 | 7.05/3.07 |
| MME-P/POPE/SEED2Plus | 1176.1/76.4/34.7 | 1216.7/76.6/34.5 |
| CLIP-T/I | .236/.662 | .235/.667 |
| 位置惩罚消融：T/I前→后 | .222/.647→.236/.662 | .233/.666→.235/.667 |
| TTS .5L/.25L/.125L WER | 2.22/2.67/5.54 | 3.07/3.74/4.83 |
| 同三档RTF | .427/.358/.341 | .524/.480/.330 |
| 文字问答→语音问题文字答→语音答 MME-P | 1176.1→997.1→967.1 | 1216.7→1019.9→1004.6 |
| DPG | 正式版未列 | 增加overall68.20，子项互有胜负 |

正式T1 ASR6.69低AnyGPT8.5但高GLM2.82；TTS2.22低Cosy2.89/Cosy2 2.47/GLM5.64。v2 ASR7.05/TTS3.07，TTS高Cosy2.89，不能仅凭optimized字样声称每项改善。正式T2 POPE76.4/MMEP1176.1/MMMU31.1/Seed34.7/CLIPT.236/I.662，POPE/MME低InstructBLIP78.9/1212.8、图像语义低Emu.286/图像相似低NeXT.691/Dream.697；v2变76.6/1216.7/无MMMU/34.5/.235/.667，不混表。正式T5文本问答MMEP1176.1→语音问题文字答997.1→语音答967.1，仍有179/209下降；v2为1216.7/1019.9/1004.6。v2新增DPG T7 overall68.20略高SD2 68.09，global76.90<77.67/entity77.87<78.13/other60.4<80.66，不能说各项全优或将.11视为已显著。

正式T3 T2I256/50/10steps为28.57/5.52/1.29s、CLIPT.2360/.2354/.2325、I.6614/.6593/.6524；S2I39.90/7.74/4.25s、T.2322/.2323/.2289、I.6450/.6454/.6376。正式TTS .5L/.25L/.125L RTF.427/.358/.341、WER2.22/2.67/5.54，快并非无损。正式T6位置惩罚T.222→.236/I.647→.662；v2同表.233→.235/.666→.667，效应显著缩小且无CI。F8预填仅两个定性例，长答不自动更准确；无pad比例/阶段/长度比例完整数值消融。正式T7 Emu3.02s/.286/.656、NeXT6.23/.225/.691，本作256步28.5s更慢、10步1.29s但质量各异；非固定质量全面支配。v2 T3 TTS RTF.524/.480/.330、WER3.07/3.74/4.83，与正式版速度误差也不同，v2S2I减步CLIP还不单调；不要将正式2.22和v2 .330拼成同一设置。

## 发布代码、模型与机制差异

[GH固定c4f4625](https://github.com/VITA-MLLM/Omni-Diffusion/tree/c4f4625f84197a72d556ea00f10e5b2775524252)与[HF固定2233ee1](https://huggingface.co/lijiang/Omni-Diffusion/tree/2233ee1ae2aa2b63e00466197afdeea0ca9e0901)分别核查，未把README示例当原三阶段完整配方。

发布c4f4625代码与论文至少三处需分开：generation_utils预填是.2L而文为.25L；图像例max_position_penalty=2，当前masked-logits排序内前100不罚，后部按负logit乘/正logit除系数，文为完整尾部统一gamma<1缩放。对全负logits[-2,-1]乘2会降低熵，对全正[1,2]除2提高熵，故该实现无统一增熵保证且依赖logit零点；这是公式分析，未运行模型。dataset forward_process另逐位置随机threshold，返回的每样本p_mask未用，不能直接声称与标准共享t前向完全同分布；gamma.6对eos类概率衰减已落实。固定HF有card/config/weights而未列自定义py，README要求克隆GH本地custommodel；AutoModel卡片例是否能单靠该HF加载未实测。缺完整三阶段mix/私有数据与所有评测计时；不能据这些差异推断论文结果无效。

语音输入路径已在tokenizer连续fbank、AudioEncoder与MLP注入代码相互核实；输出GLM4Voice由离散speech码解码。MAGVITv2也有独立encoder/decoder。共享主干与统一预测目标不等于外部codec不存在，也未通过等预算实验证明模态间必然正迁移。

位置惩罚的两个实现需要保留身份。原文统一缩小一位置的全部logits可作为升温解释；发布代码采用依正负不同的变换，又随剩余masked位置重新排序，不能沿用同一数学解释。两者可能都产生经验收益，但需要在同检查点/同采样预算下分别实验。代码差异也不足以否定原论文结果。

## 优势条件、可证伪实验与写作学习

静态codecs可保任务信息、联合数据覆盖语音视觉关联、输出mask长度近真实且低熵提交校准时，mask并行可减少串行深度；软位置先验可能抑制raster两端相关纹理，预填文本可给语音语义锚点。优势依赖这些条件，不保证跨域语速/文字/长语音、不保证共享模型正迁移。token揭示轨迹是计算过程，不能直接当真实书写时序；语音模态扩展也不能证明视频笔画能力。

固定checkpoint/COCO10K ID/分辨率/codec/CFG/NFE和同GPU计时，比较原文统一缩放、发布正负缩放、固定熵调度/随机同提交量，记录CLIP/重复区域/细字OCR与质量-延迟Pareto；测试logit平移只作机制诊断，无需穷举防御。预填.2/.25/不预填在同长度/步数下盲评内容正确、WER、MOS/说话人及首包延迟；pad gamma×共享t/逐位置mask×长度比例对齐曝光，跨语言/语速/长句测截断/多pad率。阶段/SDVI/独立专模与共享模型匹配总训练预算，测所有任务前后与真实说话人heldout，避免合成域优势。严格书写需另加事件标注与真实视频/动作基线。以上仅实验设计，均未执行。

Intro从AR串行和dLLM新接口切入，Method依输入输出codec→三阶段数据→分别对应故障的解码启发式组织，实验按语音/视觉/效率，附录补跨三模态、位置消融和局限。应学习故障-机制-实证链；摘要统一离散概括须以Method连续语音细节校正，first声明限作者时间/定义，optimized版本不能省略退步。Limitations只列未来编辑/扩规模，遗漏语音转换误差、私有mix和启发式长度；本笔记补充这些有来源边界，避免将未测问题当已证失败。

## 本次实际阅读边界

ICML2026完整15页PDF Abstract/§1–5核心与Impact、Eq1/2、T1–8全部、AppA/B1–4/C全部研究文字，F1–6/8–10图注；实际p4/5/6/7/8/13/14/15八页，未逐篇Refs或所有定性例。arxivv2 HTML核心与App研究文字/主变更表和额外DPG已读，未宣称全部v2图片逐例。GHc4f4625完整72项树/README全文；tokenizer、audio_processor全文，modeling_dream指定构造/语音注入/forward/generate，resampler全文；generation_utils sample/440–630、dataset_qwen2 28–97/904–958及SenseVoice1070–1112、finetune shell/yaml全文、LibriTTS92–152与inference225–295/406–449；trainer主要定位非全文，其他下载源码不等读完。HF2233ee1元数据/card/config全文，未下载权重/原数据、未执行模型或独立复现。

继续L114–116及后续统一模型、数据/评价与绘画/视频队列；Dream、SenseVoice、GLM4Voice、MAGVITv2、NeXT-Omni等先按已有ID去重再做原论文追引。此处接口审查不代表这些被引工作的核心阅读已完成。
