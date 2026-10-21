# Selftok：Bellman必要性、策略梯度与公开制品

第一百一十三批完成已有[L098](../reviews/L098.md)固定核心三遍与五项书面记录。[结构化来源和审查](../../data/selftok_bellman_gradient_and_release_audit_2026-10-22.json)。356目录（329论文／研究、27资源），222核心/225书面含未通过项，134条未确认核心（含资源）。无新增目录、仓库文件删除、权重下载、模型运行或独立复现。

## 版本与范围

固定[2505.07538v3](https://arxiv.org/abs/2505.07538v3)，2025-05-27，完整42页技术报告。已读Abstract/§1–5全部核心研究文字、Eq1–20、T1–8、AppA1–3含T9/Algorithm1与AppB研究文字；定性图多数仅图注、参考文献未逐篇读。实际核p10F7、p15T2/T4/F8/F9、p22F15/T6、p25Eq19/20、p27F17、p28T7/T8。

其前身DDT-LLaMA的正式[CVPR2025条目](https://openaccess.thecvf.com/content/CVPR2025/html/Pan_Generative_Multimodal_Pretraining_with_Discrete_Diffusion_Timestep_Tokens_CVPR_2025_paper.html)题名为Generative Multimodal Pretraining with Discrete Diffusion Timestep Tokens，pp26136–26146；[作者项目](https://ddt-llama.github.io/)说明扩展关系。此正式录用不直接移给Selftok报告，Selftok的RL/renderer及新表分数也不回填进前身。本批只核前身身份/摘要和supp首表，进入全文队列，未计新增精读工作。

Selftok研究静态图像非空间离散表示、共享纯AR图文模型及视觉奖励后训练。扩散时间上的渐进重建与物理绘画/书写过程无直接对应；规范笔顺和视频物理被列为后续问题，未作为本作已完成任务。

## 模型、损失与数据

图像经SD3 VAE×8压缩；image/query双流MMDiT以co-attention和token-aware AdaLN产生512/1024个非空间query。512维特征降至16维，以32768码本、cos最近邻和STE量化。decoder初始化SD3 image流并重训token流；`x_t=(1−t)noise+t*image`，仅给token后缀`V≥k(t)`，从带噪点复原原图。Eq9前向码值不变、反向按`.5/p_k`补偿token被保留频率。

另训一步renderer：以learnedcanvas换带噪输入、冻结tokenizer表示，MSE/LPIPS/GAN联合优化；前30K perceptual/GAN权重.1/0，此后.5/.5。该新增decoder训练影响重建质量，不能将收益全部归于码的AR性质。共享Llama3-8B扩32768视觉词，文字/图像ID统一CE；有图理解、图像编辑和文本生图路径。

Tokenizer ImageNet1K train、256²中心裁剪，在50Kval评价；rFID比较重建val与真实train分布。AR的530M含COYO/DataComp/LAION子集、内部图文及文字序列，不能全部称530M独立图文对。QwenVL/MiniCPM生成多层caption。生成SFT252202内部模型合成对；编辑总1487148样本、含PIPE/UltraEdit/OmniEdit和内部数据，再有约2K内部精调；旧笔记只写约2K，已补全。理解SFT含VQAv2、OK/AOKVQA、IconQA、GQA、OCRVQA、OneVision、TextVQA、PixMo、VizWiz，具体重采比例未全给。

AR预训384Ascend910B2/b7680/200K，AdamWβ.9/.95、lr1e-4cos→1e-5。生成SFT8芯片/b32、编辑16芯片/b128、理解32芯片/b128，均lr1e-5。生成256²；PIE700各方法指标统一512²评价。推理entropy>2才做logitadjustment，生图scale10、编辑7.5、再top-k采样；实际k、每prompt采样数和seed未核齐。RL作者称prompt去重且无额外testtimescaling，完整清单、RL lr/rollout/总卡时仍缺。

## 理论审查：表示图与生成策略需要分别定义

原文§2明确承认任意联合分布都有链式分解，另定义带do干预语义的AR约束。因此不能将其论证简化成“作者仅用链式法则证明因果”。但以下更强推断仍缺支持。

1. **空间码与Bellman。** §4以future token会影响已选token为由宣称空间码不能RL。固定prompt c，令状态`(c,z1,…,zk)`、动作为下一空间码、转移为确定追加，最后以`R(decoder(z1,…,zK),c)`作终端收益，便得到有限时域MDP。对k<K有`V_k(prefix)=Σ_z π(z|prefix)V_{k+1}(prefix,z)`，终端V_K为图像奖励。生成中已选前缀不被后续动作改写，encoder训练时的空间依赖不破坏此递归。此反例只否定一般“不兼容”必要条件，不保证所有tokenizer的RL效率相同。
2. **训练最优性。** 精确值函数下的policy improvement条件，不自动保证神经策略、近似奖励和有限采样的梯度更新达到最优。同参数更新影响多个状态是一般函数逼近现象，不足以推出空间码特有的Bellman失效。已读[L185 DDPO](../reviews/L185.md)也提供扩散过程的MDP/RL相关工作，不能把DPO近似轨迹问题扩写为所有diffusionRL不可能。
3. **递减entropy。** 不同位置的条件熵可以因变量本身信息量而增大；例如第一码恒定、第二码独立均匀二值，仍可按前缀AR采样。分段递减曲线是当前表示/模型的经验特征，不能单独证明因果可识别或作为AR必要充分条件。
4. **噪声作为IV。** §2将独立噪声视作instrument并据重参数化宣称码无偏。仍需写清被识别的因果量、相关性/排除条件和估计量；独立噪声与重建目标本身未提供所有表示的识别保证。有限码带宽也不自动证明解耦。

上述为对当前论证的分析性审查，没有运行数值实验，也不直接构成新课题。

## Eq20与奖励的实际可核范围

程序奖励用MMDetection阈值.6评对象/计数/关系；QA奖励用InternVL/mPLUG对prompt拆出的语义问题评分。编辑RL使用InternVL2.5-78B、0–5指令遵循分；AppB几百步改进仅以例图展示，无同等完整定量表。去重prompt不能单独排除组合模板、教师和评价器同源偏差。

p25 Eq19为组内标准化优势。Eq20印为`L=−mean[A_i−λD_KL(π||π_old)]`，未显式出现`A_i logπ`或重要性ratio。若固定rollout、A停止梯度，直接对印出的有限样本式反传不能得到奖励score-function项；若采用对采样分布求导或省略记法，需要额外说明。公开仓库未提供RL训练loop，现阶段不能判实际实现错误，也不能声称已经验证其GRPO实现。

## 主表与消融

| 结果 | 可支持的比较与边界 |
| --- | --- |
| T1重建 | 1024码rFID.54/PSNR26.30/SSIM.805/LPIPS.063，优于该表FlowMoHi .56/24.93/.785/.073；后者14bit/token，本作15bit，不能视为相同码率。512码rFID.70弱于LlamaGen1024码.59，跨预算分别看 |
| T2 schedule | uniform-time/customschedule21.86/.600/.150；uniform/uniform21.10/.564/.177，六组中前者重建更好，未证明其他序列不能AR/RL |
| T3码本 | 32768→65536，PSNR21.86→22.12，同时每码多1bit |
| T4 renderer | 512码PSNR21.86→24.14、LPIPS.150→.084；1024码PSNR26.26，与T1/README26.30差.04，未解释。单910B2/b1重建8.2→.31秒约26.45倍，不含LLM512步AR |
| PIE T5 | 相对EditAR结构35.89<39.43、PSNR23.76>21.32等改善，但LPIPS124.48>117.15更差；整体结构/背景也未胜NTI/PnP等全部指标 |
| 理解T6 | MME1381.3，高于表内部分统一模型，低于JanusPro1576、LLaVA1532.1，不能写理解SOTA |
| F15协同 | 固定4:6双任务减单任务，Selftok绘制各点Δ正，空间码部分负；左5M空间码略高于Selftok，不能写所有点本作更强。无CI/等FLOPs/原始点表 |

| T7/T8 | GenEval | DPG |
| --- | --- | --- |
| SelftokPre | 60 | 80.37 |
| PreZero | 84 | 未列 |
| SelftokSFT | 74 | 81.80 |
| SelftokZero | 95 | 85.57 |
| JanusPro作者重测 | 79 | 83.48 |
| JanusPro同流程RL | 85 | 84.49 |
| HiDream-I1 | 83 | 85.89 |

GenEval Selftok+21分，Janus+6分，最终差10分；原文另有92、+18、+7表述，均与主表不一致，按来源保留。DPG+3.77，但85.57低于同表HiDream85.89；Janus也有+1.01，Attribute略降。程序与QA收益不能跨不同量纲直接比较为哪种奖励普遍更有效。

实际F17中两模型GenEval reward均上升，DPG曲线接近且阴影重叠；阴影的统计含义未说明，不能称独立多seed置信区间。最终表比分、训练/评估reward曲线、推理条件需分别解释。

## 非论文制品与复现配置

[GH4695474](https://github.com/selftok-team/SelftokTokenizer/tree/46954740736f406b909a221b8eda8fd6962e1880)63树项；README、test、两个evalyaml、Pipeline编解码、ImageTokenizer forward/时间采样、quantizer/EMA与diti映射核心已核，底层MMDiT/flow/量化未全读。README明确训练代码尚待发布，未见VLM/RL训练loop。存在类内loss不等于完整训练协议公开。

[HF a3ee3c29](https://huggingface.co/selftok-team/SelftokTokenizer/tree/a3ee3c2918e7029921cb15f84afcecc37d62ff6c)六个文件，四个512/1024 tokenizer/renderer权重未下载；卡主要复制旧README。代码MIT，SD3上游模型条款另计。

| 发布细节 | 审查结论 |
| --- | --- |
| `SelftokPipeline` | 默认50步flow重建；renderer单次前向后VAE还原；完整T2I仍需LLM先生成码 |
| 原文/码序 | README要求AR训练反向读码，代码时间/索引需映射，不把符号方向差直接判错误 |
| time sampler | evalyaml名义`log_norm`；实际ImageTokenizer forward直接`torch.rand`采t，不能只看yaml就断定训练用logit-normal |
| EMA | yaml`decay=.99`确传入码本cluster/embed EMA；`.8`为`ema_entropy_ratio`控制其他项，与论文codebookEMA.8未对齐，不能混同参数名 |
| 路径/示例 | 当前GH示例含args/sd3_path；HF旧renderer例缺args解析/sd3_path、导入未在树内的engine路径，Notes提GPU模块但树未见，不将两来源合并成可直接复现流程 |

## 后续可证伪实验与写作学习

固定LLM、数据、renderer、码率、可用预训先验与FLOPs，仅换空间/非空间码；分别固定rollout和总计算比较RL效率，公开scorefunction/ratio、prompt语义去重、seed及奖励独立的检测/VLM/人工/多样性评价。奖励高同时检查独立CER/属性和分布外组合，区分reward优化与泛化。对IV明确估计量和假设，再检验表示信息/干预效应。严格书写另建同终态异顺序、时变墨迹与接触抬笔GT。这些均为未执行建议，新颖性还需追引。

可学习其问题→扩散递归→表示组件→共享VLM→RL的组织，利用重建消融、单/双任务和同RL基线分别回答问题。Claim需承认理论必要性未被实验识别、部分基线更强及不同模型预算；Limitations应补内部数据、奖励同源、未匹配码率和未公开训练，不能把未来视频/512²示例写成已经发布的完整能力。
