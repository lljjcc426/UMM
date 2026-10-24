# MIO：模态取舍、离散序列与公开推理协议

第一百六十八批完成[L157](../reviews/L157.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/mio_tokenization_modality_tradeoffs_and_release_audit_2026-10-24.json)。357目录（330论文／研究、27资源），274核心/279书面含未通过项；未确认核心56论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2409.17692)、[主源2](https://arxiv.org/html/2409.17692v4)、[主源3](https://aclanthology.org/2025.emnlp-main.255/)、[主源4](https://github.com/MIO-Team/MIO/tree/6c0b5e62dfb5684bc741f34cce062aed15744057)、[主源5](https://huggingface.co/m-a-p/MIO-7B-Base/tree/16cd83760cfcad610da5cfdc8459ca54d24f8ea2)、[主源6](https://huggingface.co/m-a-p/MIO-7B-Instruct/tree/b8f5e48ce79fcf3268dba64b1395ac150c1ad99e)。

## 研究问题

如何用一套因果next-token序列理解并生成文字、图像、语音和视频关键帧，同时处理不同模态token数量及内容/音色学习难度不平衡？

## 现有不足

仅图文配对缺上下文交错监督，语音音色码在初始阶段较难学习且数量占优；连续/离散与AR+diffusion路线的输入输出表征不同。文中把噪声/VAE导致理解较弱当动机，但无同预算因果隔离。Transfusion确有训练加噪及理解侧t_cap策略，不能反向误写其输入始终无噪声。

## 贡献

Yi6BBase扩多模态词表，统一CE训练与sample隔离masked packing；语音先完整内容码、再三个完整音色码块；alignment/interleaved/speech增强三阶段，再16任务34公开数据集SFT。公开Base/Instruct权重、tokenization/推理/外部解码器代码。视频能力按有序关键帧建模，README明确不含完整连续帧及音轨；不据接口覆盖推断笔顺视频质量。

## 输入、模块、输出与公式

输入文本、SEED32图码、SpeechTokenizer内容码或视频关键帧序列，统一因果模型输出文字/图码/语音码/交错序列。图码→SEED codebook embedding/MLP→StableUnCLIP外部条件扩散→像素；语音生成的四块code重新堆叠后交SpeechTokenizer decoder。理解默认只保留RVQ1内容；生成含RVQ1+3音色。voice系统prompt明确限定以<spch>开始并只输出语音，std才允许选择模态，不能把所有输出选择当成无prompt约束。

## 模型结构

SEED CausalQFormer每图32离散码、词表8192；SpeechTokenizer原8codebook取前4，每book1024、50Hz，输入内容50tokens/s、输出四块合200tokens/s。新增12292=8192+4096+4边界为论文计数。HF固定配置两模型均LlamaForCausalLM/32层/hidden4096/32heads/vocab76294/max_position_embeddings4096/无rope_scaling；训练seq2800另列。统一LLM的CE不排除像素端扩散；公开SEED decode默认guidance10/20steps，论文T11语言模型Guidance1不能直接当像素解码CFG。图语义码的因果排列没有笔画时间标签。

## 数据分布与划分

预训练AppA：SBU/CC3M/LAIONCOCO/JourneyDB（后者仅生成）、RefinedWeb、OBELICS/MMC4-core-ff、WebVid10M/HowTo100M/YTTemporal180M、Libriheavy。4–8视频帧或场景变化keyframe，字幕/ASR/BLIP2caption经Yi34BChat整合。原文明确remove CLIPscore>.27，方向可疑；本批固定树无训练/预处理入口，保留原文不擅改小于。去非英语、宽高比>2/分辨率<224、speech≤15s。SFT T10完整16任务表含34公开集声明；同名训练集和评测集不自动构成泄漏，缺split/去重清单。15s语音输出约3000码，超过训练2800且尚有文字/边界，需披露切块/截断机制，不能据缺失代码断言所有15s样本都被错误截断。

## 指标与评价协议

T2 MMEUnify Overall/Understanding/Generation/Unify；T3 CIDEr/VQA/VizWiz/SEEDBench；T4生成图与GT图CLIP-I（图图相似，不单独识别文字对齐）；T5 ASR/TTS WER，TTS经Whispermedium转录再英语normalization；T6 MSVD/MSRVTTQA，T7 zero-shot MMLU，T8四选一OmniBench。附录T13 SSIM/LAIONaesthetic/三人平均rank；T14 GPT4o内容1–5；T15主观win/tie/lose；T16跨口音WER/speaker similarity。MME公开视频指标实现的问题见第163批，未核此表是否使用同代码，不给MIO分数做未经依据的修正。

## 对比方法

T1为建模/接口声明对照，未等量测所有模型能力。主表多取外文既报结果：Emu/SEED/AnyGPT/Flamingo/Kosmos/MetaLM/IDEFICS/CM3Leon/InstructBLIP/GILL；语音Wav2vec/Whisper/VALL-E/USLM；视频BLIP2等；OmniBench另Gemini/Reka/videoSALMONN/UIO2。MIO音色自回归，AnyGPT依外部voicecloning，TTS/直接s2s与转写级联的workflow不同，不能等同架构单变量实验。T7缺同Yi6B文本基线。

## 实验条件和发布边界

完整v4正文§1–5/Limitations、AppA–D/E1–6、Eq1、T1–16每行及F1–6实际原图均核完；正式PDF下载截断，只保留此前指定范围已读。T9 StageI/II各128A80080GB，24800/12800steps；III8A80032200steps；batchmix12:2:0:2→2:2:6:6→2:1:1:12；AdamW3e-5/cosine/warm.03/clip1/seq2800/FlashAttn，SFT同超参但总steps/GPUh缺。声称speech token12.5/37.5/75%恰等batchmix份额，真实pack token占比需日志，不武断当算错。T11 text beam5无采样；image/speech/video beam1/top-p.7采样，speech/video rep1.15；temp1。固定GH 6c0b5e62dfb5684bc741f34cce062aed15744057共206treeentries/182blobs，查README/infer/tokenization/utils/SEED配置与decoder，无完整训练或评测入口。HF仅元数据/config，不下载权重、不运行神经模型。

## 主结果

T2 MIO37.2/41.5/53.5/16.6，Overall列次Gemini45.6、Generation列最高，但Unify低于SEED/Anole各22.3。T3 MIO120.4/65.5/39.9/53.5/54.4，前四低于SEED124.5/66.2/45.9/55.1，SEEDBench较高。T4 Base→Instruct COCO64.15→67.76/Flickr62.71→68.97，后者列最高，COCO低于SEED-I70.68。T5 ASR6.3→10.3恶化4.0pp，TTS12→4.2改善7.8pp，WhisperASR2.7。T6视频QA42.6/35.5为表内最高；无单列连续视频生成质量表，MME聚合不隔离视频。T7 MMLU45.7低于Llama2Chat47.9；T8 OmniBench36.96低于Gemini42.67。完整16表结构化，保留空缺/横线原样，无跨协议总排名。

## 消融及进一步实验

T13 MIO图像SSIM COCO.2307/Flickr.1727、aesthetic4.019/4.326高于Emu/AnyGPT，三人100prompt平均rank1.2优于1.9/2.9；SSIM参考GT并不充分评价多解生成。T14直接s2s内容1.4，低于LlamaOmni转写级联2.4和Any1.8；T15 win54/tie25/lose21%，n/原始判断缺，不能据significantly措辞推显著。T16 MIO/Any跨口音GLOBE WER9.8/27.9、相似67.8/67.3；Libri-clean10.3/28.1、75.1/71.3。F2为三阶段loss曲线，阶段改变数据分布不能用总loss下降证明无遗忘。F3实际是各tokenizer在StageI固定3Ksteps的两组生成样例，非tokenizer收敛曲线；修正旧笔记“Fig3曲线”。SEED/VQGAN1024/8192未控制码长度、预训练、decoder且无最终同预算定量；语音顺序/交替主要prelim观察，三阶段无全组合消融。

## 局限与疑问

核心证据支持广接口覆盖及部分任务收益，ASR和统一子分下降/劣势需保留。T13 agreement定义all3samecases/100，却报82.3%；该定义下整数case比例应1%粒度，需公开逐例/实际分母或解释不同聚合，未将其直接判为伪造。GPT4o快照/n/人评校准缺；T15样本数缺。GH demo active为text/std、max_new_tokens512、beam5不采样，未启图/语音保存，不代表论文各模态T11配置；切到语音时若不改512预算，上限低于完整15s约3000码（扣文字/边界后更少），不是实测输出时长。utils.extract_frames返回os.listdir未显式排序，需核实际时间顺序，不能据此认定论文输入已错序。32码小字/笔画细节瓶颈是待测假设；README多项Low自评且视频只关键帧，无法证明连续笔画、视听同步或流式低时延。

## 预期优势条件

语义主导的图文/语音交错对话可复用LLM和离散SFT；把内容置于音色之前及分阶段增语音或可缓解优化失衡。对需要真实笔画先后、精细字形、长语音实时响应的分布，低码率语义图和整段内容再音色可能限制保真/首音时延；需单独测量，不把4模态支持当成已验证的过程控制。

## 可证伪实验

同Yi底座/数据/decoder控制图码长度与语义预训练，给小字CER/字形拓扑/终态相同但笔顺不同的反事实序列；直接测下一笔、真实连续帧事件顺序和运动。语音顺序×交替×三阶段在等样本/等tokens/等更新预算分别比较ASR/TTS/MMLU及首音/端到端时延Pareto，保存2800截断和实际modalitytoken日志。公开训练split/CLIP过滤方向、全T11与像素decoder参数、评测清单、逐例人评及judge快照；核100prompt agreement整数分母。独立固定视频帧名显式排序，先验证读帧时间轴；demo按模态配置并报失败/截断率，无需对基础边界堆低价值测试。

## 论文组织与Claim学习

tokenization→causalmodel→detokenization与三阶段问题对应清晰，可借鉴。Claim按支持接口、表内结果、组件因果分层；图3必须按实际样例命名，loss图跨阶段分布不同不当无遗忘证据。统一CE需同时披露外部扩散/语音decoder，LLMGuidance与像素CFG分开；保留SFT后ASR退步、direct-s2s劣势，说明人评定义、分母和原始制品。

## 实际阅读范围

完整arXiv2409.17692v4 HTML：§1–5、Limitations、AppA/B/C/D/E1–E6，Eq1与T1–16全部单元、F1框架/F2三阶段loss/F3tokenizer两组样例/F4高级能力/F5基础六类/F6多模态CoT/ICL实际原图及图注；不播放/独立转录图中的音频。正式23pPDF仅保留此前§2.1–2.3/§3Tables3–8/3.6/AppB/C/T9/10/E1/E6指定范围，未称正式PDF全文通过。固定GH README、infer.py、tokenization_mio.py、utils.py、SEED配置与seed_llama_tokenizer.py全文；HF两模型固定revision元数据/config。未逐个审182blobs、未读权重/执行模型/独立训练评测；三遍核心理解及五项书面验收，无独立口试。

## 主要边界

T2总体37.2及生成53.5须与Unify16.6一起解释，后者低于SEED/Anole22.3。SFT令TTS WER12→4.2、ASR6.3→10.3；直接s2s内容1.4低于转写级联2.4/1.8。六图中F2为loss，F3仅固定3Ksteps的生成样例，已修正历史笔记。

## 人评与配置缺口

100prompt三人完全一致比例若按整数case/100，应为1%粒度；82.3%需实际分母或不同聚合解释，未据此推断伪造。公开demo活跃配置为text/std与512新tokens，切换模态需配套T11参数和预算；外部SEED扩散默认CFG10/20steps与语言模型Guidance字段分开。

## 视频及笔顺适用范围

README明确video仅关键帧，utils返回文件未显式排序。前者限制连续视频能力结论，后者是公开实现待核问题，均不构成论文逐例错序率。图文/语音交错及示例不证明笔画事件顺序或连续运动保真。

