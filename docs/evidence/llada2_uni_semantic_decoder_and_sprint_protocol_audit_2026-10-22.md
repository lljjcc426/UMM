# LLaDA2.0-Uni：语义码、连续解码器与SPRINT协议审查

第一百二十八批完成[L114](../reviews/L114.md)明确范围核心三遍及五项书面记录。[结构化证据](../../data/llada2_uni_semantic_decoder_and_sprint_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），237核心/240书面含未通过项；未确认核心93论文／研究+27资源。资源按制品协议另审。本批没有新增目录、删除文件、下载权重、执行模型或独立复现。

来源：[arXiv v1](https://arxiv.org/abs/2604.20796v1)、[完整25页PDF](https://arxiv.org/pdf/2604.20796v1)、[GH固定ee9dfd5](https://github.com/inclusionAI/LLaDA2.0-Uni/tree/ee9dfd57c59e231aec4245df76e2e8a6758485b7)、[HF固定dc2cde4](https://huggingface.co/inclusionAI/LLaDA2.0-Uni/tree/dc2cde43e008aafd53ab6e4049187ae7e1cbc22e)。正式会场未独立核明。

## 问题与设计动机

用语义离散视觉码与block-masked MoE主干支持图文理解、静态生成/编辑、稀疏交错图文和推理，并减少主干反复前向和外部图像解码开销。采用视频抽帧训练交错序列，但没有真实笔画事件、连续RGB书写视频、严格规范笔顺或音频任务的实验。

重建VQ的语义不足/压缩细节损失、双视觉分支的优化差异及全双向文本生成不稳定是作者动机。SigLIP-VQ取语义、6B连续decoder恢复视觉细节，block因果先验保序，SPRINT和蒸馏降成本。作者将这些视作现有差距根因，但无逐组件等预算消融排除MoE容量/390B训练tokens和数据质量的贡献，不能将根因论断视为已证明。

## 输入输出、模块与统一目标的范围

SigLIP-VQ语义码统一输入输出，16B总参数LLaDA2mini MoE做block内双向/块间因果mask预测，独立6B ZImageBase连续flow decoder以视觉码为条件并2倍超分；SPRINT混key范数与top1概率剪prefix及阈值自适应提交；SFT互补mask/按mask数平方根重权；decoder FM+consistency蒸馏50→8步无CFG。统一单CE范围限主干，encoder冻结预提码、decoder另训，非全系统仅一个目标联合端到端训练。

文字/图像→文本tokenizer或SigLIP2g→16384×2048语义码→加图像高宽/边界并扁平排入MoE dLLM→文字或视觉码；文字直接解码，视觉码查embedding+MLP→连续ZImage flow latent→VAE RGB。decoder不额外读原prompt，不能推出码无损或无外部模型先验。代码generate_image先将请求宽高除2再按stride16制码，因此请求1024²对应32²=1024语义码，再超分至1024；CLI请求512对应256码/最终512，与README1024例有别。实际PDFp5/6/7/9/10/12/13/14/15/16/17/18/19十三页框架、公式、全部十四表与交错/蒸馏已看。

HFdc2cde4主干config为20层hidden2048、16Q/4KV heads、head128、partialRoPE.5/theta600000，vocab173568/图像offset157184，256路由experts/top8+1shared、8group择4、MoEFFN512、首层denseFFN5120，routing scale2.5；主干BF16元数据16,322,752,256参数非激活参数、更非含decoder/tokenizer/VAE全系统。config maxpos8192与论文SFT扩16K分别记。HF图tokenizer包装为GlmImage，vision40层/1536/16heads/patch16、VQ2048/16384；包装类名不单独证明换了论文SigLIP来源。decoder30层/3840hidden/30heads、16latentchannels、cap4096；SigVQ提取器4096维不同于encoder2048码维度。BDLM Eq3/5只当前block noisy目标，前block clean；互补mask每位在一对样本中各遮一次，不等2倍独立数据或消除全部数据/估计偏置。

## 数据、实验指标和条件

主干S0图文+文本100Btokens，S1多任务210B，S2高质指令/交错/CoT80B，共390B曝光，不能当390B独立样本或包含原LLaDA/ZImage预训。理解PaddleOCR伪标签/Qwen3VL细化、Objects365/RefCOCO过滤与235B教师验证，坐标0–1000；SFT约60M/text:MM=1:5，用Qwen审核问题、GPTOSS过滤回答。生成>200Mweb→140M，增加人体/含字图像，短边>=512、ArtiMuse>=60/DeQA>=4并235B重描述；压缩过滤原式(HW)/filesize<.15的单位/方向解释未齐，保留原式不自行修正。编辑混X2Edit/OmniEdit/NanoConsistent/PicoBanana/UniWorld/StructVisuals/UnicEdit/CrispEdit及合成、Qwen按实际变化改指令。Koala36M过滤得6M10–30s片段，每5s采一帧2–6帧；去75%与36M→6M统计基数未说明，不擅写严格同一分母。CoT/交错推理8M来自Flux6M/ZebraCoT/Weave。私有mix/去重/全部样本和decoder各阶段量未齐。

21项理解含MMStar/MMB中英/MMEC/幻觉/RWQA/SimpleVQA、MMMU/Pro/MathVista/MathVision/WeMath、CharXiv/ChartQA/OCRBench/DocVQA/AI2D/InfoVQA、Count/Reward/Vstar；生成GenEval/DPG/OneIGEN/UniGenBench/WISE，静态文字CVTG2K多区域WordAccuracy、NED↑及CLIP；NED方向按原表保留，不能当原始编辑距离越大越好。ImgEdit九类1–5、GEdit中英semantic/perceptual/overall、MICo四类；InterGen150例由Gemini3/Qwen3VL评文字连贯/图文对齐/ID一致，但T12只按三任务聚合。TPS/秒每图不代首帧、峰值显存或全系统加载时间。无严格笔画/视频时序指标，文字生成分数不等识别分数或笔顺。

理解Qwen2.5VL7B/LLaDAV/BAGEL/InternVLU/LuminaDiMOO/LLaDAo；生成FLUX/Seedream3/QwenImage/LongCat/ZImage/Emu3/mGPT2、JanusPro/MMaDA/BAGEL/OmniGen2等，编辑另Kontext/Step1X等。参数、预训、教师、数据与计算不同。InterGen仅Emu3.5，NextFlow/Mogao未开源是论文时点说明，不能当2026-10当前事实。T9本作Lumina对手3.41/3.26/2.21等与L112自报四类分数不同，未核同judge/解码协议，不跨表拼接。无替换tokenizer/MoE或block目标且同数据预算的因果主表。

T1主干S0 256→512语义分辨率/S1S2 512，decoder1024；理解边800约2048tokens；seq8192/8192/8192→16384。未公开齐各stage优化器/lr/batch/GPU/训练总步数/耗时；dFactory/VeOmni与预提码/packing只是基础设施描述，不能补填未给参数。decoder独立warmup冻结semanticprocessor→全解冻多域→高质refine，FM后蒸馏，缺各阶段具体优化曝光/权重。SPRINT alpha.5、tau.93/.95，T13无SGLang；T14单GPU/b1/BF16/1024²但型号未给，50步CFG对8步CFGfree。发布CLI默认T2I16steps/CFG4/request512、decoder50steps；README8steps/CFG2/request1024；文字32steps每block32/gen2048，不能把steps视为整段总NFE。代码decoder normal为2cond−uncond带norm截断、Turbo仅cond；还含VAE及加载卸载，未证明表14包括全部这些开销。

## 全部十四表支持的结论与反例

T2按表内Qwen2.5VL7B对照21项有4高/17低：MMStar64.1>63.9/MathVision26.7>22.4/Count86>84.9/Reward47.8>45.2，但MMMU50.1<51.3/OCR75.7<84.2/Doc89.5<94.9/Vstar61.8<80.1；对Lumina也有MMBEN81.5<84.5/MMMU50.1<58.6/Reward47.8<51.7，不能称理解全类全优。T3GenEval.89优表内统一基线，count.73低Lumina.85/BAGEL.81，color.92低LLaDAo.96；未纳L112 SelfGRPO.91条件。T4DPG87.76低Qwen88.32/Seedream88.27，Global91.14低LLaDAo92.91/Relation92.17低Lumina94.31；Other实际表93.18，正文94.04不符，未擅改。T5OneIG.505高表内统一，但Text.661低Intern.740/OmniGen.680；T6UniGen79.63高所列，但Text31.23低FLUX32.18/专模68–72。T7CVTG平均.765/2→5区域.788→.746为强统一表现，仍低LongCat.865/Qwen.829/ZImage.858，CLIP.818低Lumina.831；缺脚本/字体/语言/OOD分解。

T8WISE.68→thinking.78为+.10绝对/10个百分点，相对约14.7%，非相对10%；需计额外推理token预算。T9ImgEdit3.92高统一所列、低Qwen4.35/ZImage4.30；replace4.04低Intern4.13、style4.60低OmniGen4.81。T10GEditEN/CN6.61/6.66，EN低Intern6.66；语义6.68/6.63低BAGEL7.36/7.34，PQ7.52/7.67较高，不能PQ高就称编辑语义或原图细节完全保持。T11MICo47.1优表内但object51<Qwen52.4；来自不同容量/数据非唯一架构因果。T12InterGenStory6.42/7.02、Forecast5.19/5.94略高Emu，ExplanationGemini6.22>6.19/Qwen6.35<6.48，无judge/seed置信区间；F8象棋/物理仅定性。T13SPRINT平均76.3→75.7/TPS24.3→39.8，OCR75.7→73.4/DPG87.76→86.27，MMMU50.1→52.5/Chart80.1→81；Doc8→27.6TPS约3.45倍，1.6是平均TPS比，非所有任务上限。T14decoder50→8步32.95→2.90s≈11.36倍，GenEval.89→.87/DPG87.76→87.24/OneIG.505→.500，UniGen79.63→79.76/WISE.68同；不能称全面无损或把1.6×11.4当全系统加速。

## 公式、公开代码与局限

原文Eq3/5在alpha为随噪声时间递减的保留率惯例下，外负号、内部alpha_prime和logp的组合与文中正权重CE解释有符号疑问；已看实际PDFp9/10，HFforward只同位置CE，不含完整BDLM/MTRS训练流水线，故保留需澄清，未判原训练实现错误。Eq4负载bias更新还需u的符号/路由约定，未补造。Eq6若L_j为masked CE和，则逆sqrt(n)使贡献约sqrt(n)，属于长度折中、不等所有样本等权。Conclusion承认语义码丢精细编辑、交错规模不足、RL未来；无本版完整RL成效。发布SPRINT fractional image_keep_ratio只用于>=1 pin分支，没有按.8分别topk；full1/1在无validmask时直接保留全prefix、global.5不再裁。部分pin时先把importance设inf再mean归一化，alpha<1且confidence分支会有inf/inf、未pin范数项归零的运算风险，未执行，不据此否定表13。语义码不等原像素保持，READMEperfect-preserve超过现有证据。

## 优势假设、可证伪设计与研究写作

语义离散码对任务信息充分、连续decoder先验可恢复细节、block条件化不破坏所需全局关系且confidence校准时，可用语义训练改善理解/组合生成，并在prefix冗余时降低缓存计算。key范数不等真实注意力贡献：q的方向/归一化/softmax共同决定权重；高概率提交也可能固化细字错误。长图文收益、OCR损失与作者假设有对应证据，但尚未拆解各组件因果；稀疏2–6图帧与规范动作序列之间仍缺真实时序监督/评测。

固定相同LLaDA/decoder预训、390B曝光、分辨率、数据与总FLOPs，换语义/重建码、MoE/dense、blocksize/全双向，评理解-生成-细字/编辑Pareto；固定符号定义核清Eq3/5后再复建原训练。SPRINT拆cache复用/剪枝/阈值三项，比较论文模态topk与发布global/pin实现，配对同seed报告OCR/结构/误提交率和端到端时间/显存，多seedCI；无需编造未运行的数值。蒸馏固定语义码测50/8步、多文字/中文形近字/稀有script与真实masked区域RGB变化，包含主干、codec、VAE和模型加载分段计时。thinking与等FLOPsBestN/多采样对照，InterGen扩样本、多judge盲评并加真实连续视频和事件时长/顺序指标，先排已有书写方法解决。所有实验为设计，未执行。

Intro把表示语义/细节、attention和输出长度问题连到三组件，Method按tokenizer→主干→decoder→加速组织，Data/Training分开、14表按任务和消融分组，值得学习。但singleobjective/endtoend应限定冻结码和分训decoder范围；T2能力边界、T4Other冲突、T8绝对/相对改善和T13/T14质量损失须保留。完整三阶段超参、对应评测脚本与基线预算不足限制归因，不能从MICo大差距宣称唯一证明架构。Limitations明确保留语义压缩细节/交错/RL未来，比将定性推理泛化成已验证推理能力更稳妥。

## 实际阅读边界

arxivv1完整25页PDF，Abstract/§1–6所有核心研究文字、Eq1–8/T1–14/F1–9图注，实际p5/6/7/9/10/12/13/14/15/16/17/18/19十三页；未逐篇Refs或逐例全部定性图。GH ee9dfd5完整41项树（含diffusers submodule，未递归读该外部仓库）、README全文，scripts T2I/MMU/edit全文、decoder decode/SigVQ全文、encoder1–64/464–510与指定接口；HF dc2cde4元数据/configs（主干/两decoder/image/VAE）全文、modeling router464–541/forward1249–1356/SPRINT1507–1610与2180–2249、highlevel2282–2350/2406–2441选读。HFREADME仅模型/推理选段；底层transport/attention、全部modeling、训练基础设施和新SGLang/FP8未深读。未下载权重/原数据、执行模型、复现训练或速度。

## 与书写、文字和视频课题的关系

T7提供静态多区域文字渲染结果，说明语义离散主干配连续decoder已能改善这类任务。它仍存在专用生成模型差距，T5/T6密集文字评价也没有全部占优。因此“统一模型不能生成可读文字”过宽；可进一步研究的须限定稀有文字、笔画拓扑、特定编辑条件或真实事件时序，并检索对应已有研究。

Koala片段按5秒取2–6帧，只支持此种稀疏交错数据分布上的训练描述。InterGen150例及两个judge的任务均值不直接测书写事件完整性、笔顺合规、每笔速度或RGB时间可观测性。将交错生成重命名为严格笔顺视频会造成任务误解。

T8 thinking .68→.78应记录额外推理成本；T13主干SPRINT与T14decoder是不同部件、不同测试集合，不能将1.6与11.4相乘后当端到端加速。总时延需按主干、语义查表、flow、VAE及加载/传输分解，再在同任务实测。

当前GH明确说SGLang已于2026-05-29支持，HF卡仍写coming soon；二者为更新时间不同的制品状态。本文未读外部SGLang实现或FP8模型，未将其测速当论文T13无SGLang结果。GH树含外部diffusers子模块，41项不是该子模块的全部源码。

后续补Block Diffusion原工作、LLaDA2mini、Z-Image、UCGM/一致性蒸馏、dFactory以及CVTG原评价协议，按已有ID去重后独立记录；本次使用其接口/引用不代表这些研究已完成三遍精读。
