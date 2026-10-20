# Emu3 / Janus-Pro：版本、训练与归因审查（第六十二批）

[U02](../reviews/U02.md)、[U04](../reviews/U04.md)完成所列版本核心阅读和五问书面审查。347条目录保持，138项核心阅读、140项五条书面检查，209项尚未确认核心三遍（含资源等层级）。Janus-Pro没有逐因素消融，验收记录明确解释该缺失，未补造实验或声称原文提供消融。无文件删除、训练、推理或独立复现。

## 版本与任务

| 工作 | 原始版本 | 新核事实 | 能力范围 |
| --- | --- | --- | --- |
| Emu3 | [arXiv2409.18869v1](https://arxiv.org/html/2409.18869v1)，2024-09-27 | [Nature正式扩展](https://www.nature.com/articles/s41586-025-10041-x)，2026-01-28，650:327–333，DOI10.1038/s41586-025-10041-x | 离散AR图文视频；正式版增加消融、scaling、变序、交错图文与CALVIN动作。沿用U02关联，未重复计论文；具体年份SCI分区未核 |
| Janus-Pro | [arXiv2501.17811v1](https://arxiv.org/html/2501.17811v1)，2025-01-29 | 当前核实来源仍为技术报告；原Janus与JanusFlow接收情况不能套用 | 继承Janus编码分离，扩展数据/训练/规模；静态图和理解，未评价笔顺/视频 |

阅读范围在各笔记末尾逐项记录。Emu3正式HTML全部核心、主T1及实际EDT1–7图片已核，实际Fig1/3/4与完整补充PDFp13 FigS9已看。补PDF完整取得38页，选读数据、训练、主评测与消融小节；全部附录/参考文献和样例尚未逐一追读。Janus-Pro §1–4/T1–5核心全部读、实际Fig3框架已看。两者均无独立结果复现。

## Emu3：主模型与完整系统

文字BPE、视觉VQ生成离散token，拼入caption/分辨率、视频fps/duration与结构标记，共享dense causal decoder预测下一token。8.49B由6.98B Transformer和1.51B embedding组成，32层/4096hidden、32query/8KVheads，RMSNorm/SwiGLU/RoPE/GQA。图像/视频视觉码本32768、压缩4×8×8，4帧512²或单图转4096视觉token。

主模型从零预训练用CE，视觉权重.5。视觉tokenizer基于SBER-MoVQGAN并采用L2/LPIPS/GAN/commitment；DPO联合偏好损失与.2SFT。图像QFT、理解指令后训练各自适配；官方Emu3-Gen/Chat分为两个任务检查点。视频还用稳定化与4×超分网络后处理，稳定化基于SVD temporal VAE，并非在推理中执行SVD扩散采样。应逐层说明，避免“全系统只含CE”或“一个最终检查点全部最优”等推断。

| 正式EDT1 | 阶段1 | 阶段2 | 阶段3 |
| --- | --- | --- | --- |
| steps / context | 90K / 5120 | 90K / 5120 | 90K / 65536 |
| lr / schedule | 1e−4 / cosine | 5e−5 / constant | 5e−5 / constant |
| dropout / clip | 0 / 1 | .1 / 5 | .1 / 5 |
| seen tokens | 2.4T | 2.4T | 7.5T |
| text / T2I / I2T / T2V / V2T采样 | .2/.64/.16/0/0 | .2/.64/.16/0/0 | .1/.08/.02/.64/.16 |

WD.1、AdamW β.9/.95/ε1e−6，warmup3600/1800/1800，视觉:文本loss=.5:1。补S7估预训995K等效GPU小时，1280张80GB等效卡集群；不包含全部后训练/数据标注/分词器等总工程成本。2024 v1描述两阶段5120→131072、lr5e−5 cosine，两版配方分别记录，不能混成一个实验。正式视频QFT使用131072上下文，不与正式预训练65536混用。

### 原表及评测条件

| 证据 | 结果 | 限定 |
| --- | --- | --- |
| 正式EDT2、补S10 / v1 T7 | Emu3 GenEval原prompt .54、GPT4V重写 .66；DPO .52 / .64 | .66不能作为原prompt分数；GenEval4图/CFG5.5，CompBench10图/CFG5，topk16384/p1 |
| 正式EDT2 | Emu3 FID12.8、CLIP-I.689、CLIP-T.313；DPO19.3/.680/.312，DPG80.60→81.60 | DPO并非全指标改善；Emu3512²、DPO720²，数据/训练/分辨率也影响比较。DPG4图/CFG5、mPLUG-large |
| 正式EDT3 / 补S11 | VBench80.96，dynamic79.27，human action77.71；CogVideoX81.61/动作99.40、Wan2.1总83.69 | 5s24fps、topk8192/p1/T.95，稳定化+4×SR后评价；不等原始AR输出或文字事件正确率 |
| 正式EDT4 | SEED68.2、OCRBench687、MMVet37.2、MMB58.5等 | 部分图像在训练见过以*标记；主T1理解62.1为12benchmark归一化汇总，不能当一个数据集正确率 |
| 正式EDT5 | CALVIN ABCD→D AvgLen4.64、连续5任务成功.870；RoboVLMs4.49/.826 | FAST1024动作码、窗口20/chunk10、双视角、b192/8K/lr8e−5；仅模拟，尚无真实书写机器人验证 |

100用户prompt×3人评分包含视觉质量/提示跟随，主T1图像70.0属于人评分制，与理解汇总或VBench单位不同。补S12有中英文提示结果，缺评委聚类CI和完整标尺/加权细节。不能把接近分数称统计等效。

### 实际消融与理论边界

补S3码本4K/8K/16K/32K/64K的gFID为2.506/2.533/2.586/2.468/3.014，64K利用率68%；更大码本不单调更好。UCF101视频tokenizer在相同分辨率时以少4倍token取得rFVD27.893/PSNR27.546，图像tokenizer26.675/30.499；等token图像rFVD139.930。保留压缩/质量取舍，不能将“可比”改写为所有重建指标更优。

实际Fig3b的1.5B OpenImages AR/DiT比较，AR按等样本GenEval更好；补S4按估算FLOPs相当。两者使用Emu3 VQ与SDXL VAE、不同有效token长度，仍有分词器/表示差异。Fig3c训练相近scratch理解loss，CLIP预训late-fusion明显更低，无法证明任意预训规模下组合架构无优势。

实际补FigS9显示dropout.1从稳定检查点恢复训练，并考察视觉/文本loss权重；.5:1为双任务折中，1:1生成更好、text-only理解更好。loss消融为Qwen2.5-1.5B结构/b3840/30K/lr5e−4/ctx5120，不能套作8.49B所有配方已验证。变序EDT6为额外50B token适配，diagonal .61vs scratch.17，block .66/.18，spiral .60/.16；空间token顺序与真实落笔事件不同，inpainting的zero-shot指无专门任务微调，不能省去变序适配。

scaling采用L(N,D)=E+A/N^α+B/D^β，β.55，T2I/I2T α.25、T2V α.35，7B外推R²≥.95/MAPE<3%。它拟合特定数据/配方的验证loss，不能推出任意任务准确率、笔顺语法或物理规律保证。

### 数据分布与工程发布

正式EDT7/补S6：视频文字面积>1%被OCR过滤，motion/美学再筛选；部分图像低美学分支剔除text-rich/单色图。理解另补文字丰富样本，两条数据路径分别描述。书写视频常含大面积文字、细线和局部低运动，需要测筛选保留率与tokenizer短事件重建上限；此处为待测假设，尚未测量。

[固定dbbf985发布](https://github.com/baaivision/Emu3/tree/dbbf9858194d70b8c58293e219ecffe22df0f9c7)README与[HF Gen卡](https://huggingface.co/BAAI/Emu3-Gen)示例：CFG3/topk2048，附加美学正提示和含`text`的负提示，与论文评测采样不同。用于文字任务时应显式比较移除/保留这些提示，不能照抄后将失效归给模型。`scripts/t2i_sft.sh`给720²、ctx10240、4epoch、perGPU2/accum4、lr1e−5→1e−6等示例，与正式QFT b240/ctx9216/20K各自记录。README评测、预训/DPO训练仍TODO；尚未核正式新增视频/交错/动作的所有检查点发布，不能由模型族介绍推断全部产物可复现。

## Janus-Pro：继承结构、系统扩展与缺失归因

理解SigLIP-L16/384→MLP，生成LlamaGen VQ16/16384→MLP，各自编码接共享DeepSeekLLM1.5B或7B；独立imagehead输出576视觉码并解码384²。Pro沿用Janus结构。StageI延长ImageNet训练以训练adaptor/head，StageII去掉占原T2I前2/3步骤的ImageNet，改densecaption；StageIII比例理解:文本:生成7:3:10→5:1:4。

理解StageII增加约90M（YFCC/Docmatix等），StageIII另加MEME/中文对话等；生成增加72M合成美学，统一预训real:synth1:1。Ref43为midjourney-prompts提示资源，无法推出所有合成图生成器/数据清单。1B标签实际LLM1.5B；7B HF配置vocab102400/max_position_embeddings16384，论文/README上下文4096。配置容量不等实际训练长度。

T2计划steps I/II/III=20K/360K/80K(1.5B)或40K(7B)，§3.1实际II在270K早停。恒定lr1e−3/1e−4/4e−5、AdamW β.9/.95、WD0/clip1、warm600/5000/0、batch256/512/128。16/32nodes×8A10040GB约9/14天，继承预训成本另计。理解长边384灰pad、生成短边384中心裁剪，需考虑文档细节/长行信息损失。

| 主表 | Janus1.5B | Pro1B（LLM1.5B） | Pro7B | 解读 |
| --- | --- | --- | --- | --- |
| T3 MMB | 69.4 | 75.5 | 79.2 | 同1.5B改善仍同时改数据/训练 |
| T3 POPE | 87.0 | 86.2 | 87.4 | Pro1B有下降，不能称所有指标提升 |
| T4 GenEval | .61 | .73 | .80 | 7B counting .59低于SD3M .72；总体SD3M .74 |
| T5 DPG | 79.68 | 82.63 | 84.19 | SD3M84.08，.11差无CI；Dalle3 global90.97高于Pro86.90 |

全文无数据×策略×规模独立消融、无7:3:10和5:1:4控制表，也未量化报告合成带来的稳定性方差。Pro1B/7B还同时改变III步数。主表证明作者报告协议下的系统差异，无法给三个因素独立因果收益。五条书面审查对此给具体解释，未把缺失消融标成已读消融。

[固定1daa72f发布](https://github.com/deepseek-ai/Janus/tree/1daa72fa409002d40931bd7b36a9280362469ead)README Pro生成示例CFG5、T1、16并行、576码；根`generation_inference.py`默认仍为旧Janus-1.3B，不能未经改模型路径当Pro实现。[HF7B卡/config](https://huggingface.co/deepseek-ai/Janus-Pro-7B)已读，卡元数据MIT与正文DeepSeek模型许可分别记录，具体使用需读对应许可。未核完整评测代码/训练器、权重或运行；示例参数不能倒填论文GenEval/DPG协议。作者明确384²/VQ限制OCR与小细节，定性简单文字样例不等逐字符正确性或笔顺能力。

## 可证伪实验与写作学习

固定最终checkpoint同时测理解/生成；对共享单模型、等总预算专门单模型、双模型系统分别比较。AR×diffusion须控制分词器或单列表示瓶颈，报告原prompt/同重写器、原始输出/后处理、分辨率与采样。Janus-Pro做数据数量/质量×策略全因子、同III步数/同计算的规模比较，多seed/独立validation择参与收敛方差。全部尚未执行。

书写域加入文字/motion过滤保留率、短事件重建、字符/文字体系/作者留出、严格事件/顺序/方向与RGB时序指标；真实机器人执行单独验证。Emu3的空间变序、CALVIN和Janus-Pro静态图已有研究必须作为相关先例，但无法直接支撑规范逐笔视频结论。

学习Emu3把范式主张转为架构、压缩和训练对照，Janus-Pro按strategy/data/scale组织系统工作；Introduction明确继承基础，Method按实际数据路径/训练阶段讲，Claim写任务、子项和协议，Limitations保留分词瓶颈、静态/模拟范围与发布缺口。遇到未报告消融应说明归因不足，再检索后续解法，不能直接将其当可发表创新。
