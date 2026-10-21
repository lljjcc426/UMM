# DDT-LLaMA正式前身补漏：时间码、对照与版本边界

第一百一十四批补录[G044](../reviews/G044.md)，完成正式核心三遍与五项书面记录。它是[L098 Selftok](../reviews/L098.md)的正式前身，两条以同一工作家族关联，统计论文／研究记录时分别保留版本，不宣称两项独立无关创新。[固定证据](../../data/ddtllama_formal_precursor_and_protocol_audit_2026-10-22.json)。现357目录（330论文／研究、27资源），223核心/226书面含未通过项，134条未确认核心（含资源）。无删除文件、权重/训练媒体下载、模型运行或独立复现。

## 正式来源与任务

[CVPR2025正式条目](https://openaccess.thecvf.com/content/CVPR2025/html/Pan_Generative_Multimodal_Pretraining_with_Discrete_Diffusion_Timestep_Tokens_CVPR_2025_paper.html)，pp26136–26146，完整11页PDF4,943,187B；[正式supp](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Pan_Generative_Multimodal_Pretraining_CVPR_2025_supplemental.pdf)11页6,908,233B，先部分下载后补齐再读取。已读正式Abstract/§1–6所有核心研究文字、Eq1/2/T1–4，supp A–G全部研究说明；参考文献未逐篇、其他定性画廊未逐图。实际核主文p3F2/公式、p4T1/2、p7T3/4/F6、p8F7/8/9、suppp1超参表。

输入是图文、编辑指令，输出静态图像或文字回答；tokenizer通过不同噪声时间、不同前缀长度重建原图。素描出现在静态图像/风格例子，没有真实作画顺序或笔画事件。视频理解/生成在suppG为未来方向。

| 配置 | 正式DDT-LLaMA | 后续Selftok报告 |
| --- | --- | --- |
| query/码本 | 480/65536，16bit每码 | 512或1024/32768，15bit每码 |
| 名义480/512码容量 | 7680bit | 7680bit；仍非等数据/成本实验 |
| 重建 | 不同噪声时刻给相应前缀，多步解码 | 后缀配方和另训一步renderer |
| 预训数据 | 200M图文+10%纯文字 | 530M图文及文字序列总和 |
| 主GenEval | .66 | Pre.60/SFT.74/Zero.95 |
| RL | 无该实验 | 新增视觉奖励后训练 |

两文时间参数方向、码序与配方需要各自映射，不能将后续renderer .31s或.95结果归为正式CVPR实验。[作者项目](https://ddt-llama.github.io/)明确前身/扩展关系。

## 模型与研究逻辑

编码器输入1024图像位置与480learnedquery，两支20层Transformer、hidden256，分别加2D/1D位置编码，attention联合交换；只保留query。VQ将256维降至16，L2/cos最近邻查65536码，EMA更新与deadcode重激活。

decoder依SD3 MMDiT双流各24层/1536维，量化码代替文字，16维投影并去pooledtext。正式材料没有明确VAE路径或decoder的预训权重初始化，不能用后续Selftok代码替它补结论。作者“encoder-free”指不用专门预训CLIP，仍有自训DDT图像编码器。

Eq1 `x_t=t*noise+(1−t)*x0`，decoder给前t码，其他mask0，MSE重建x0并加commitment；前缀随加噪扩大，补偿图像属性损失。方法动机是将扩散属性层级变成较适合AR学习的序列。排列扰动收敛差异、定性属性替码可支持当前表示特征，未证明空间码为LLM不可能学习的语言，也未证明所有语义因子可识别/解耦。

Llama3-8B扩65536图像词和BOV/EOV，共享head、统一CE。预训图文对齐，SFT含生成、编辑、理解，仅answer算loss；输出模态外词表mask。480个AR码完成后还要多步图像解码，不能把离散AR或名义codec码率等同整链路低时延。

## 数据和完整实验条件

Tokenizer ImageNet1K约1.28M、256²中心裁；MLLM Laion/Coyo图文，ShareGPT4V为>400M图生成长caption，经CLIP筛出200M。训练长/短caption60/40、captiondrop10%，Wiki/Pile纯文字10%。SFT生成ShareGPT4V/ALLaVA/GRIT、编辑IP2P/HIVE及自建高质量对、理解ShareGPT4V/ALLaVA-instruct与InstructBLIP held-in训练；精确采样量/ID未齐。用CLIP筛数据又用相关CLIP评价，需独立人评/模型查选择偏差。

| suppT1 | MLLM预训 | MLLM微调 | Tokenizer |
| --- | --- | --- | --- |
| AdamW β/ε | .9/.95/1e-6 | .9/.95/1e-6 | .9/.99/1e-6 |
| lr/schedule | 1e-4/cos | 1e-5/cos | 1e-4/linear+cos |
| batch/steps | 1280/360K | 256或128/160K | 1024/140K |
| warm/wd/clip | 5K/.05/1 | 2K/.05/1 | 5K/0/未列 |
| 硬件/框架 | 512Ascend910B/TP8 | 256Ascend910B/TP8 | 32A800/DDP |

均bf16，预训约2周、codec约1周。表中MLLMβ行跨预训与微调两列，不误记微调为.99。文本topk50/topp1、图像topk4096/topp.9、CFG8。实际去噪调用数、每prompt图数、seed、采样时间未核齐；不借用Selftok当前代码填入。

## 完整主表中的改善与退步

T1 GenEval .66，高于所列MLLM整体，低于SD3 .74、DALL-E3 .67；子项single.99/two.64/count.56/color.87/position.39/colorattr.48，TwoObj低于Emu3 .71、LaVIT/Lumina .70。CompBench color/shape/texture/spatial/nonspatial/complex .728/.514/.642/.176/.314/.345，其中complex低于SEED-X .361；DrawBench CLIP .267与Lumina持平。Emu3比较明确不用prompt改写。

T2本作EVR L1/CVS14.5/85.5、MA5K L1/LPIPS14.2/29.6、MagicBrush L1/CVS7.1/92.4，在所列MLLM组各项更好；与专用模型仍有EVR L1差于UltraEdit14.4、MA5K L1差于MGIE13.3、MagicBrush L1差于UltraEdit6.6。贴近目标图的L1/CVS不唯一代表编辑指令与未编辑区域均正确。

T3 NoCaps/Flickr30K/VQAv2/GQA/OKVQA/VizWiz/MME/SEED/POPE为124.2/88.5/76.4/66.3/65.9/57.3/1378.9/67.9/86.9，VQAv2低于Emu2chat84.9、SEED低于Emu3 68.2，MME低于多专用理解模型。caption用CIDEr，VQA准确、MMEperception、SEEDMCQ、POPEF1，不作原始量纲混合总分。Emu2chat/gen分别权重不作为同模型双任务成绩。

T4 ImageNet PSNR21.7、类别生成FID6.1，相对所列VQGAN/VQGAN-LC/MoVQ/RQ有优势；没有所有最新codec、相同码率/decoder预算匹配，不作全领域最优结论。

## 对照与消融的证据范围

| 分析 | 证据 | 尚未支持的强结论 |
| --- | --- | --- |
| F1排列 | normal/reverse/partreverse/oddshuffle收敛不同 | 排列敏感性不证明语言必要结构或空间码无法学习 |
| F9a文本 | DDT perplexity约2.58→2.48；空间约2.58→2.71 | 测试文本集/CI/等预算不全；不是双任务减单任务的性能曲线 |
| F9b编辑 | 同Gemma2B、200M、编辑集和步数；global40比2/local25比8、总65比10偏好案例 | 未给人数/盲法/完整分母/平局，不能写65%或86.7%胜率 |
| F6替码/F8前缀 | 从细纹到轮廓/颜色的逐步复原与选例属性混合 | 非可识别解耦理论，也非真实绘画/笔顺顺序 |
| F7规模 | Gemma2B/Llama8B×50/75/100%训练阶段选例 | 同时改变家族、参数，未拟合幂律/残差或系统质量曲线 |

没有去递归/全部码固定/随机等长mask、独立head、词表和码长等完整因子实验。suppA称共享head更强，未给相应独立量化表，不能补出提升数字。suppD承认2B会只去掉局部雾气、改玫瑰颜色同时改形，扩大模型有改善选例；这些负例需保留。

## 制品、新颖性与后续检验

作者项目的code/checkpoint实际均转向Selftok仓库/HF。上一批固定[GH4695474](https://github.com/selftok-team/SelftokTokenizer/tree/46954740736f406b909a221b8eda8fd6962e1880)63树、[HF a3ee3c29](https://huggingface.co/selftok-team/SelftokTokenizer/tree/a3ee3c2918e7029921cb15f84afcecc37d62ff6c)512/1024码四权重清单可关联；未见480码正式MLLM对应物，不能据这些链接认定正式训练和表已可复现。未下载权重或运行模型。

suppG明确256²ImageNet限制开放域重建和美感，500M及视频是后续方向。此正式CCF-A前作必须进入非空间时间码与UMM协同的查新；后续报告的共享码、renderer和RL须逐项标明新增，避免将同家族多版本当多个独立佐证。

实验建议：固定LLM、图文/文字曝光、码率/码长、decoder先验与计算，对空间/query×时间前缀/全部码/随机同长mask做因子对照；多seed报告理解、生成、重建与源保留。文本perplexity固定独立heldout集，同时测单/双任务差；人评盲化、报全部分母/平局/一致性。等家族参数/计算点后再拟合规模趋势。指定文字另测跨字体/脚本CER/细笔拓扑，严格书写另采时变墨迹和笔画事件。全部为未执行方案，新颖性需继续追引。

写作可学习冲突→排列观察→递归假设→模块→三任务→in-depth对照的组织。Claim需与有限曲线、表格和人评协议同范围，保留专用模型和部分指标占优；Limitations应写256域迁移、caption教师、版本与公开训练缺口，避免用impossible/disentangled/scalinglaw代替验证。
