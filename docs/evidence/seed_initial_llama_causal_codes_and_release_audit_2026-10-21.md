# SEED初版与SEED-LLaMA：语义量化、因果码和发布配方

第九十四批补完[L078](../reviews/L078.md)、[L082](../reviews/L082.md)指定范围的核心三遍和五项书面检查。主目录354条（327论文／研究、27资源），189项核心/192项书面含未通过项，165条尚未确认核心（含资源）。[固定发布证据](../../data/seed_versions_and_release_audit_2026-10-21.json)保存版本、代码/HF模型卡、配置与未验证边界。本批未删除文件，未训练/推理/独立复现，未下载权重或数据媒体。

## 阅读版本与真实任务

[初版SEED v2](https://arxiv.org/pdf/2307.08041v2)是10页技术报告，读Abstract/§1–5及全部三张表，实际核p4F2/T1、p5F3/T2、p6F4、p7T3。[SEED-LLaMA](https://arxiv.org/html/2310.01218v1)核实ICLR2024正式书目；实际读2023-10-02 v1完整HTML核心§1–5、T1–10/AppA–D、AppE限定说明与图注，实际核F3、AppA F8原PNG及原始HTML T1–4/T6/T9重排渲染。正式25MB PDF多次超时未完整取得，OpenReview403，不将部分PDF算正式全文。

两者输出静态图像。SEED-LLaMA视频输入按4/8帧采样后做问答，多图故事输出也不构成连续视频生成。32个query与其自回归顺序不含真实落抬笔/笔画/帧时间。两篇均未验证严格汉字笔顺视频。

## 方法和公式的职责

两者从BLIP2 ViT取完整图像16×16特征，以32个query做causal self-attention，cross-attention仍可读整个图像。第一阶段用最后query与caption对比训练；第二阶段nearest VQ后重建连续语义embedding，优化cosine；再拟合冻结扩散模型所需条件，优化MSE。三个目标分别负责语义判别、量化后的语义保真及解码接口，不等价于精确像素/字形/过程约束。

初版ReverseQFormer产生77个SD文字条件embedding；后续SEED-LLaMA改MLP产生1个unCLIP图像条件embedding，用图像特征蒸馏替代文字条件蒸馏。后者扩展8192个视觉词，最大化∑log p(uᵢ|u₍ᵢ₋ₖ:ᵢ₋₁₎)，先LoRA并训练embedding/head，再merge且冻embedding全参训练，后做仅Answer计loss的指令微调。不能把后续8192码本/训练配置和权重反填初版未披露项。

“双向encoder不能AR”的强说法缺乏数学依据。有限码联合分布仍能链式分解；causal query可能改变表示及有限预算下的学习难度，需要指定实验判断。query因果mask也不使真实未来图像内容不可见。

## 原表结果、退步和可归因范围

| 工作/表 | 原始结果 | 可支持的结论与限制 |
| --- | --- | --- |
| 初版T1 | Flickr连续93.7→量化91.7；COCO80.7→77.4，BLIP2为92.9/80.3 | 量化损失明确；连续码还多训练5M，缺匹配曝光因果mask对照 |
| 初版T2 | SEED重建68.23/65.22；GILL67.45/65.16、SD68.43/65.40 | 本作输入图像，对照输入caption，不能判同输入T2I或忠实重建优胜 |
| 初版T3 | CIDEr119<BLIP2 131；VQAv2 42.8<51.9，GQA28.8<32.6 | 已具多任务接口，未超过BLIP2理解成绩 |
| LLaMA T1 | 连续93.6/82.5，量化90.8/78.2，BLIP2 92.9/80.3 | 新codec同样有量化损失，不能称不损理解 |
| LLaMA T2重建 | 图像条件77.35/76.52；初版文字条件68.23/65.22；unCLIP79.30/79.55 | 改善语义相似度，仍低于上游接口；条件目标/SD版本共同变化 |
| LLaMA T2文生图 | 原预训69.07/65.54，SFT70.68/66.55，GILL67.45/65.16 | CLIP-L14生成图—真实图相似，不能写文字—图像CLIP分数或精确文字质量 |
| LLaMA T3 | 8B SFT VQA66.2、14B63.4；14B caption126.9<BLIP2 144.5，SEEDBench53.7<InstructBLIP58.8 | 指令微调有效但无全面领先；Vicuna7B/Llama2Chat13B底座不同，非纯规模对照 |
| LLaMA §4.3 | 5000caption正确32码：causal4997、双向2134 | 测格式稳定性；缺强制长度解码后语义比较，不能升级为双向码AR不可能 |
| LLaMA T4 | LoRA CIDEr124.5/生成68.87→加全参125/69.07 | 多10k训练，缺LoRA等追加曝光/预算及多seed，不单独证明全参必要 |

实际AppA F8中图像条件重建保留更多主体语义，姿态、道路/场景布局与细节仍变化。未见OCR、笔画拓扑或严格几何指标。初版没有标准组件消融；后续消融和精选多轮例图也未证明生成与理解存在双向协同因果收益。

AppE明确指出，见过InstructPix2Pix等对应数据的multimodal-prompt图像生成不属于emergent。对其他多轮/组合Claim，需要训练组合隔离、完整成功率、失败分布及强基线；精选例图本身不足以验证。

## 数据、算力和当前发布的差异

初版约5M新增CC3M/Unsplash/COCO，继承BLIP2/SD/OPT预训。摘要5.7天/64V100与F4 SEED-OPT44小时/64V100分别记录，未把44小时当全部codec+LLM成本。初版lr/batch/LoRA rank等未充分披露，不用后续脚本补写。

后续预训源含LAIONCOCO600M、MMC4core7.3M文档、OBELISC141M文档、WebVid过滤8M等，源规模不等实际消费量。SFT还含生成/编辑、OCR和视频理解数据；不能仅从source名称推断无数据泄漏或训练样本数。v1T6为30kLoRA+10k全参、224²、AdamW lr1.5e-4/β.9,.98/eps1e-6/wd.05/warm.03/cosine；64A10040G预训8B144h/14B216h，32A10080G SFT16h/27h。该成本没有覆盖全部基础模型/codec预训。

固定[SEED GH93b3cf4](https://github.com/AILab-CVC/SEED/tree/93b3cf408196735ec4820ad2eb4d9dc4a670003d)完整526blob树；读README/SEED1、指定模型函数、训练sh与yaml。发现：

- 当前SEED_Tokenizer训练类默认distill_image=True/distill_text=False及1个图像query；旧77文字分支仍有代码，不表示默认运行。初版SEED-1.md指demo_recon.py，固定树无同名文件。
- 当前pretrain.sh为30k、β.9,.95/eps1e-5/perdevice128/accum4；数据yaml有额外Wikipedia第六组，前两类max_length200/140，论文160/128。六组sample_weights与各pipe batch/cycle共存，未经sampler完整核查不换算实际例数比例。SFT示例50k/lr1e-4/warm.07也不补充为v1原表协议。
- 当前LoRA r16/alpha32/drop.05除q/k/v/o/gate/up/down外，modules_to_save还含完整embedding/head和norm；参数预算要计入这些模块。
- 当前tokenizer decode默认20步、CFG10/noise_level0，并在实例初始化缓存随机latents；未验证论文原评测是否如此，未实际运行。
- README说明MMC4交错内容是另行指令训练，发布sft不具该特性。各演示和后续v2-1不能合并为一个原始checkpoint的能力表。

同时核[HF tokenizer2固定c6d957a](https://huggingface.co/AILab-CVC/seed-tokenizer-2/tree/c6d957a9b280d9ed3879b1eb5d99036cf8390012)及[8Bsft固定2c7d1d3](https://huggingface.co/AILab-CVC/seed-llama-8b-sft/tree/2c7d1d3532caa8c6ac7d41b3696dfe9911aaed7a)元数据、完整短模型卡和config/generationconfig。tokenizer卡仅Apache2头，LLM卡仅llama2头；unCLIP及上游条款另计，不能用单卡概括全栈许可。tokenizer配置极大的model_max_length是哨兵值；LLM实际config max_position_embeddings/max_seq_len均2048，vocab40194=32000+8192+2。float32配置和README量化显存宣传均未作运行测量；未下载权重/二进制tokenizer/图像。

## 可证伪问题与科研写作学习

优先假设：高层语义可压成32码时可节省AR长度；图像条件蒸馏比文字条件保留更多视觉信息；causal query可能改善既定自由解码的格式稳定性。需要固定同初始化/数据曝光/参数和生成器，分别做causal/bidirectional×自由/强制32码，报告全部样本质量、条件成功质量与格式错误；再比较同条件接口的图像/文字蒸馏。LoRA续训10k与全参10k按曝光和FLOPs分别对照。单独测codec OCR/细笔拓扑、未见字体语言及同终态异笔顺，后者还需真实事件监督。以上未运行。

写作可学其从tokenizer瓶颈组织两条设计、分codec/LLM阶段和分I2I/T2I表格的方式；需改进强因果措辞、原预训成本、退步和版本界定。Claim写具体分布/指标/失败定义，Limitations写量化精度、扩散先验、数据真值与发布漂移；可表达性、有限预算可学习性和实测成功率分别给证据。两篇无独立Limitations段，因此笔记明确区分作者结论与本次推论。
