# Ming-Lite-Uni配套追引：多尺度收益、论文与发布物对齐

第一百七十二批完成[L191](../reviews/L191.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/ming_lite_uni_companion_multiscale_and_release_alignment_audit_2026-10-24.json)。358目录（331论文／研究、27资源），278核心/283书面含未通过项；未确认核心53论文／研究+27资源。资源另按制品审查。补录L191；无文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2505.02471v3)、[主源2](https://arxiv.org/html/2505.02471v3)、[主源3](https://arxiv.org/pdf/2505.02471v3)、[主源4](https://github.com/inclusionAI/Ming/tree/69f28cdb5c3e60d351448ae0f50c583b3f3d359d/Ming-unify)、[主源5](https://github.com/inclusionAI/Ming/blob/69f28cdb5c3e60d351448ae0f50c583b3f3d359d/Ming-unify/Ming_Uni/MingUniInference.py)、[主源6](https://huggingface.co/inclusionAI/Ming-Lite-Uni/tree/f08100716d7d488dc71288d090b91161175eb40c)、[主源7](https://huggingface.co/inclusionAI/Ming-Lite-Uni/blob/f08100716d7d488dc71288d090b91161175eb40c/qwen2_5_llm/config.json)。

## 研究问题

将冻结的多模态理解模型接到可训练扩散生成器，在保留既有感知能力的条件下增加文本生图、指令编辑、风格迁移和多轮交互。需要验证多尺度query及表示对齐是否在等预算下提供语义与细节收益；本作不生成视频、真实作画轨迹或规范笔顺。

## 现有不足

理解特征侧重语义，像素生成需要细节；仅传caption会丢失源图和隐藏表示，多尺度query试图在冻结底座与DiT间形成连续条件。作者称此前Janus/TokenFlow采用diffusion decoder的归类过宽，Janus生成路径为离散码AR，不能沿用该说法解释全部相邻方法。关于冻结底座无任务折损/双向增强仍需相同底座前后测试与因果消融。

## 贡献

将MetaQueries式冻结MLLM桥接与M2-omni底座结合；增加4²/8²/16²共336个学习query、边界和位置编码；可训练connector传条件给SANA，配多尺度DiT中间表征与最终语义表征MSE及flow matching。报告GenEval.62和理解69.7，并展示图像编辑。配套Ming-Omni的多尺度机制已有此前说明，不能将同一机制重复算作独立首创。

## 输入、模块、输出与公式

输入文字与可选源图→视觉encoder/MLP与textembedding→冻结MLLM；文本输出按AR，生成时追加三组query及每组首尾标记，query隐藏态经connector给可训练DiT/AutoencoderDC生成最终图。F2训练三分辨率128/256/512共享DiT，推理画512最终分支；不等同逐轮生成一幅图后再送下一轮。Eq1学习Q_s，Eq2每尺度[START,Q,END]，Eq3拼接后加P，Eq4H=f_theta(Z)。按文字定义Q的token数336、加六boundary后342，但P仍只定义336行，Eq3边界位置编码未写齐，需补约定；此为符号维度缺口，不证明实际张量运算失败。对齐MSE对象/层/归一与权重、各尺度loss和联合训练完整公式未给。

## 模型结构

论文§2.2写NaViT、2×2拼接/MLP、M2-omni基于Llama3.1-8B或Llama3.3-70B、M-RoPE；未指定T2哪一骨干/完整生成训练超参。实际链接发布物是Qwen2.5路线：qwen2_5_llm配置28层h3584、28heads/4KV、vocab152064、maxpos32768、M-RoPE；QwenViT32层h1280、out8192、merge2；connector为Qwen2.5-0.5B配置24层h896/14heads2KV，代码改为非因果attention，3584↔896投影；SANA20层70heads×32、cross2240/caption2304/in32。代码query为4/8/16、learnable_queries_1d=True，对应1×s²布局，不能默认等同论文二维gridPE。公开脚本一次MLLM取三组隐藏态，各组分别connector并采样三次相同height/width，最后只返回16²组图；与Ming-Omni原版只最终尺度采样分开记录。

## 数据分布与划分

§3列LAION1555342102、Zero151766788、COYO61915700；Wukong34826982、Midjourney5421512、others440951902，六项名义和2250224986，不保证去重后的独立训练量或同阶段实际暴露数。过滤aspect≤2.5/watermark≤.5/CLIP≥.45；美学AVA255000/TAD66000/AesMMIT21904/APDD10023。编辑InstructPix2Pix-filtered、SEEDpart2/3、Ultra-edit、SynCD、Subjects200k、HQ-edit、MagicBrush总5008795，未列各源完整采样权重与训练/测试ID。T1多轮MagicBrush2步1151/3步1572，SynCD2步25438，SEEDpart3为472/7453/8783/4669；长度类别计数不当额外独立数据量。WikiArt81444/27styles；StyleBooth80922，另述67styles每类717pairs的乘积48039与总数口径未齐，合成/增广后数量需说明。F5/6为训练样本，不能作为模型测试结果。

## 指标与评价协议

理解T2七项MMB/MMS/MMMU/MathVista/HallusionBench/AI2D/MM-Vet及作者汇总Avg，沿用OpenCompass而未给逐题预测/汇总权重/CI。GenEval六项single/two/count/color/position/colorattribute及overall；.62为六项宏平均的舍入值。MSE声称>2dB PSNR/+1.5%GenEval，但无重建集、对照分数/误差条、百分比相对或百分点定义；README另称多尺度+3.5%及4090<1s，均缺可核计时配置。编辑只有F1/F7定性，无指令成功/源保留/多轮累积误差或盲评数字；不将静态sketch风格例当绘画过程评价。

## 对比方法

T2理解专用LLaVA72B、Qwen2VL72B、Qwen2.5VL7B、Emu3Chat、InternVL2.5 8/38/78B、DeepSeekVL2、GPT4o20241120、Step1o；统一DreamLLM/MetaMorph/Show-o256/512/TokenFlowXL/Chameleon/Janus/JanusPro7B。T3生成专用LlamaGen/LDM/SD1.5/PixArtα/SD2.1/DALLE2/Emu3Gen/SDXL/DALLE3/SD3medium，统一Chameleon/LWM/SEEDX/Show-o/TokenFlowXL/Janus/JanusPro1B/MetaQueries。基线来自不同数据/预训练/规模和采样条件，不当等预算。Emu3Chat和Emu3Gen分别任务版本，不能据此推同权重双用。

## 实验条件和发布边界

v3完整HTML§1–4、四式三表七图；贡献名单仅核范围、参考仅相关追引。v1→v3研究正文基本相同，主要修订链接/引用，不把MSE声明当本版新增完整消融。GH固定Ming-Lite-Omni-Preview 69f28cdb5c3e60d351448ae0f50c583b3f3d359d，117entries/101blobs；Ming-unify目录18blobs、12py，选读README/inference/主推理/SANALoss/processor全文及pipeline相关段。HF f08100716d7d488dc71288d090b91161175eb40c 66files，核11份readme/code/config与7主shard/connector/MLP/SANA/VAE存在元数据；未下载权重。HF与GH主推理/SANALoss/inference内容一致；HFprocessor把传入路径覆盖为作者服务器本地路径，GH改Qwen官方模型名，环境可移植性不同。训练器/完整MSE优化loop/GenEval原始输出未定位；不能由SANALoss默认repa_loss=False反推作者未训练对齐。发布例512²/30steps/seed42/CFG5；函数默认20steps/CFG7，论文T3实际用哪套不明。README<1s未明确冷/热、batch、步数、完整LLM+三采样时间，未运行验证。

## 主结果

T2本作Avg69.7，7指标80.7/60.5/51.2/68.3/51.8/84.5/72.3；Avg低于GPT4o72.0/Qwen2.5VL7B76.2/Step1o77.7，高于DeepSeek66.4，但对DeepSeek七项四胜、两负、一平；对GPT4o仅Math68.3>59.9，其余六项更低。T2未列Gemini，文字“超过GPT4o/Gemini”缺同表支持；与M2-omni9B同一理解向量重用，不能单当生成带来理解提升证据。T3本作.99/.76/.53/.87/.26/.30，总.62>.61MetaQueries/.61Janus/.55SDXL，但低于DALLE3.67、SD3medium.74、JanusPro1B.73；正文“.62超过所有方法并超过DALLE3.67”与本表冲突。single.99与SD3持平，position/colorbinding仍.26/.30，不可泛化为全任务领先。F1“stop sign”下是餐桌房间图，标为展示指令/图配对不符单例，不能估失败率；F7sketch/对象替换等定性有演示价值，无总体可靠率。三主表每行收录结构化证据。

## 消融及进一步实验

论文没有受控消融表或消融曲线。承认§2.1报告对齐>2dB/+1.5%，README再述query+3.5%，但缺基线分数、训练匹配、误差、具体实现，不能标记这些组件已完成因果隔离。也没有冻结/全训、单/多尺度、connector大小、caption vshidden条件、querytoken预算、迭代编辑、位置编码1D/2D和端到端速度对照。后续Ming-Omni的.64与本作.62涉及不同底座/数据/发布版本，不能直接归因某一组件。

## 局限与疑问

论文Llama/M2描述与所链接Qwen发布物未对齐，T2具体模型身份不明确；主表不支持“全部领先/模态互相增强”。冻结MLLM使生成loss不直接更新其参数，保持相同权重的感知输出较稳定，但额外query/processor/上下文仍需实测，亦无法凭此论证双向训练迁移。Eq3边界PE维度省略；MSE缺完整目标与可执行训练loop。发布推理对三scale独立同尺寸采样并丢两图，与F2单末尺度推理意图/README时延范围需说明，三次调用不能直接推定精确3倍耗时。多轮训练数据不代表长程编辑已验证；精选样例、CLIP筛样、公开测试是否与训练实体重叠、种子/采样改写/N均未齐，不认定泄漏或造假。

## 预期优势条件

已有强视觉理解底座且需追加低改动图生成/编辑时，连续query有机会保留caption难表达的身份/细节，多尺度训练可能让同一DiT适应不同语义粒度。此优势依赖源图条件和数据对齐，不能由336query数量本身推出层次解耦或细笔画保留。对于汉字/非Latin组合字形和素描逐笔过程，需单独字形/路径/时序监督与评价。

## 可证伪实验

先固定同一MLLM/SANA、训练数据、总querytoken及更新FLOPs，对caption、单尺度336、16²加等长随机prefix、多尺度学习query和各尺度单独移除做对照；对齐MSE开/关及匹配额外投影参数，公开原始重建PSNR/GenEval逐例与相对/百分点定义。冻结/LoRA/全训报理解和生成Pareto及梯度去向。完整端到端计时对三次采样、只采最后一组和F2协议，固定512/steps/CFG/seed、计含LLM/connector/decoder，前两图是否被任何后续计算使用以调用图验证。补M2论文模型和Qwen发布物各自身份/主表；多轮MagicBrush按scene/subject隔离并测源保留、数词/位置/字形CER与长度退化，接真实轨迹测试正逆序和shuffle。

## 论文组织与Claim学习

明确写MetaQueries/M2基础与多尺度新部分的分工、冻结/可训模块和训练/推理差异；数据过滤阈值与多轮长度统计值得保留。论文主张需逐项回指数字表，.62不能支持超越.67，整体平均也不能代替分项。组件收益必须附可核消融协议，README速度须定义系统边界；论文与发布骨干/默认路径要给版本映射。用“alpha、尚待完整评价”的范围陈述约束整体宣传，风格终态与过程生成分开。

## 实际阅读范围

arXiv2505.02471v3完整HTML研究§1–4、Eq1–4、T1–3全部行、七张实际原图F1–7全部视觉阅读；贡献仅名单范围/参考相关追引；v1/v3研究文字差异核，未把完整PDF阅读作为凭据。核心三遍与五项书面完成，未独立口述/模型复现。固定GH预览分支117树/101blobs、相关Ming-unify18blob路径清单及六份源码/README实际阅读；HF66文件元数据与11个文本配置/关键代码核。未下载权重、未模型执行，未称所有源码逐行。

## 配套前作追引的结果

本批补录L191，关闭第171批“先读Ming-Lite-Uni”的具体未完成项。它确实给出MSE>2dB/+1.5%文字收益，README有query+3.5%，完整研究范围仍无受控消融表。后续课题应把已有声明列为待复核先验，避免将同一多尺度机制重复包装成新贡献。

## 发布执行范围

固定源码对4/8/16三组隐藏态分别connector和SANA.sample，height/width相同，各次没有接前一张图，只返回最后图。这与Ming-Omni第171批的仅末尺度采样代码分开。没有运行模型，不能估精确时延比。论文写M2/Llama，实际权重配置Qwen2.5，T2具体模型身份需作者给出映射。

