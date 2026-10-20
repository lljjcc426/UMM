# 离散概率流、语音对齐、视频缓存与空间拓扑：核心三遍审查

本批完成[E04 Discrete Flow Matching](../reviews/E04.md)、[E05 F5-TTS](../reviews/E05.md)、[E06 TeaCache](../reviews/E06.md)、[E07 clDice](../reviews/E07.md)四项既有记录的核心三遍阅读及各五项书面检查。主目录仍340项，累计86项核心三遍。阅读覆盖正式原文核心公式、框架图、主表/现有消融、附录重点和固定版本关键实现；具体未读与缺报分别保留。未独立训练、生成、语音听评或分割复现，无文件删除。

## 任务与机制

| 工作 | 问题和干预 | 可能产生优势的条件 | 不能据此证明 |
| --- | --- | --- | --- |
| Discrete FM | 离散类别的合法概率速度；后验训练、路径/耦合和corrector | 目标离散、后验可靠、并行算力充分 | 低生成PPL等于代码正确或笔顺合法 |
| F5-TTS | 字符到长mel对齐；文本细化与Sway采样 | 语音/文字条件分布覆盖、早期积分误差重要 | 语音对齐直接解决文字视觉/书写时序 |
| TeaCache | DiT迭代冗余；输入proxy决定残差复用 | 标定能迁移、特征变化集中、网络计算主导 | 总体VBench保持即每条细笔/动作保持 |
| clDice | 体积损失忽略细连接；骨架mask交叉覆盖 | 图状细长结构、骨架可信、拓扑条件适用 | 静态连通或soft高分保证真实笔顺/方向 |

四篇涉及不同的“时间”：离散FM/语音FM的生成演化参数、TeaCache的去噪步、书写视频的物理帧序列。积分节点密集于某段生成时间，不表示在真实视频中先写哪笔或放慢哪段动作。clDice主要评价空间结构，交换同一mask的生成顺序不会改变静态分数。

## 离散FM：理论、代理指标和实际任务

[NeurIPS2024正式论文](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f0d629a734b56a642701bba7bc8bb3ed-Abstract-Conference.html)定义的速度是离散转移率；后验平均把条件路径转为联合边缘速度，条件product不表示边缘词元独立。αuf−βub在α−β=1时沿pt，差0时fixed-t stationary；固定t证明与并行采样的小步近似、不可约/非周期条件需要分开。Prop6时间无关仅针对指定all-mask路径。

正式T2无温度/无corrector、1024NFE的Eq9 Llama3生成PPL33.8优AR54.8；T5改double precision分类采样后变101.3，entropy7.2→8.0，而AR54.8/7.1。代理质量与多样性及采样精度密切相关。T4代码HumanEval Pass1 6.7低AR14.3；带GT长度oracle11.6仍低。不能用低PPL代替任务成功。CIFAR最佳FID3.63需要1024NFE及corrector/温度搜索；低NFE MaskGIT有优势。

AppF在A10080GB/b1的HumanEval延迟，256NFE19.97s对AR50.94s，512NFE则接近；作者明示AR KV缓存吞吐较好。AppG把两组batch/iteration都写big models，尚未解决，未补猜配置。[固定官方flow_matching库](https://github.com/facebookresearch/flow_matching/tree/11568d37f8d5a080e12aa7b5305d9c35ae07d136)为后续Guide工作，FineWeb示例、AdamW设置和1−exp跳转均需与原文分开。

## F5-TTS：对齐能力、真实开销与版本

[ACL2025正式全文](https://aclanthology.org/2025.acl-long.313/)的输入包含参考音频及其转录、目标文本和总长度。中文经jieba/pypinyin处理；ConvNeXt本身细化文本，不能把“省额外预训练encoder”写成完全无文本处理。Sway f(u;s)=u+s[cos(πu/2)−1+u]在给定单调范围改变节点密度，s<0靠近Gaussian侧早期。

主表F5 WER/速度好于所复现E2，但LibriSpeechPC SIM.66低E2.69，SeedEN SIM.67低.71，Seed更大模型仍有更低WER。小模型GT时长未解决E2失败，去audio则WER改善但声音相似大降；支持研究条件纠缠，但无法推出任意数据/架构的一般因果结论。ELLA难句仍跳词，LJSpeech久训WER由200K的2.93恶化到600K的5.25。

正式文字定义NFE为网络评估次数，表中“16/32”与[固定代码](https://github.com/SWivid/F5-TTS/tree/2f866649b779881af8bd644e76b9a6d95053da29)steps参数需细核：每区间midpoint通常两次场评估，CFG包含条件/无条件计算，当前合为batch2。Table6同16标签Euler RTF.15、midpoint.26，不能只凭标签跨solver比较计算。当前batch eval总时间含vocoder/写wav；原3090 RTF分项未由当前代码自动确定。

[固定HF制品](https://huggingface.co/SWivid/F5-TTS/tree/84e5a410d9cead4de2f847e7c9369a6440bdfaca)有Base1200K、v1 1250K、BigVGAN及no_zero_init等版本。模型卡明确CC-BY-NC-4.0，代码MIT分开。v1及后续适配未自动计入论文原模型性能；这里只读卡、文件清单和关键配置。

## TeaCache：速度分母与校准边界

[CVPR2025正式论文](https://openaccess.thecvf.com/content/CVPR2025/papers/Liu_Timestep_Embedding_Tells_Its_Time_to_Cache_for_Video_Diffusion_CVPR_2025_paper.pdf)的4.41倍属于OpenSora-Plan150steps/65帧512²，VBench80.39→80.32%，下降0.07个百分点；fast6.83倍降至79.72%。其他基础模型和scheduler加速不同。T4八卡32.02倍与单卡基线比较；同八卡47.79→10.13s约4.72倍，须区分算法与并行贡献。

不训练生成器仍要用70个prompt标定多项式。核心实现复用堆栈残差，同时当前输入和sampler仍更新；首末步强制计算。正文poly1d描述不能当实际拟合器：固定代码给的是已有系数，np.poly1d构造并评价。全局相对meanL1是经验proxy，未提供局部细字/笔事件误差界。

T3二/四阶VBench均78.48，微小PSNR差未有方差；OpenSora PABslow PSNR24.50高TeaCacheslow23.62，质量并非每项胜。校准与评价身份/拆分、转移到高密文字和全流程延迟仍须独立实验。后续Wan等工程适配只作为资源入口，未本批全部精读。

## clDice：定理条件与经验近似

[CVPR2021正式论文](https://openaccess.thecvf.com/content/CVPR2021/html/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.html)中Cor1.1的前景/背景图状骨架与双向包含条件，要求两者hardclDice均1。训练的soft骨架、有限k和只优化前景为进一步近似/数据假设；高soft分数没有任意汉字拓扑保证。补A最少修正讨论不能推SGD找到全局最少修正。

RoadsUNet α.5提高clDice和β1，但α.3 Dice与clDice均下降；Vessap α.1的β1也退步。跨文献DRIVE Hu的β1低本工作对应值，训练subset和实现不同，应保留。补充H的Euler ratio与正文绝对误差定义不同，尚待原实验实现确认；随机patch拓扑不能自动代替全图。

[固定代码](https://github.com/jocpae/clDice/tree/47d31a6cc4a8101b1ffe8052994821961e57af9f)的loss虽接iter_，实际SoftSkeletonize(num_iter=10)硬编码，调前者不改变k。metric里P/R变量名对换，最终调和均值对称，不能因命名直接判分数错误。完整训练lr/epoch等缺报保持待核。

## 可证伪实验

1. 离散事件建模固定tokenizer/训练tokens/FLOPs，对AR缓存、MaskGIT、离散FM/扩散；评价顺序合法、短笔Recall、几何与RGB重建，披露precision/temp/corrector与搜索预算。
2. 符号到连续序列对齐固定实际场评估数和encoder/vocoder，拆分文本细化、backbone、Sway和solver；笔顺/方向/接触单独标注与评价。
3. Cache固定prompt/noise/权重/CFG/scheduler，独立标定/验证/测试，比较等总延迟sampler及已有cache；全局proxy与笔画ROI/尾部差对照，测小新增笔画漏失。
4. 空间loss使用同最终mask不同顺序的反例，以及错误桥接/断连/多组件字；空间拓扑、增量墨迹、方向和事件先后共同报告，避免只优化最终帧得分。

以上均为待验证设计。现有前作范围仍需继续扩查，局限本身不构成新颖性证据。
