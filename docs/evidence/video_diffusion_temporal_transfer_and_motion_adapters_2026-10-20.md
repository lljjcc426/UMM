# 视频扩散、潜空间时间适配与运动模块：第四十五批

深化[Video Diffusion Models](../reviews/G009.md)、[Video LDM](../reviews/G010.md)、[AnimateDiff](../reviews/G011.md)。主目录仍为343项＝318论文／研究＋25资源；核心三遍107、五条书面检查109。实际阅读版本、正式版交叉核和缺失补充协议逐篇注明；没有训练、推理、独立复现或文件删除。

## 任务接口与机制

| 工作 | 学习的对象 | 条件／输出 | 重要边界 |
| --- | --- | --- | --- |
| VDM | 像素视频块的因子分解UNet；重建引导条件采样 | 无条件／文字／已知帧→RGB视频；可插值／SR | 时间位置和整块建模未约束规范笔事件；条件score是近似 |
| Video LDM | 预训练图像LDM的时间层、时间D、插值与SR | 文字／前帧→分层视频；多SD版本不同协议 | E仍逐帧，文字插值全参训练；整个pipeline不全冻结 |
| AnimateDiff | 可迁移时间模块、空间domain LoRA、时间MotionLoRA | 兼容SD个性化模型／文字→短视频 | 相机运动适配与绘画动作不同；SparseCtrl属于后继独立研究 |

噪声时间、真实帧序号、潜表示时间压缩和显式笔事件分属不同变量。本文三项没有给出规范笔顺的直接实验；不能从自然动作更平滑推出笔画身份／先后／落笔状态正确。

## VDM：抽样方式与特征网络决定数值含义

核心实际读[2204.03458v2](https://arxiv.org/html/2204.03458v2)，[NeurIPS2022正式版](https://proceedings.neurips.cc/paper_files/paper/2022/file/39235c56aef13fb05a6adc95eb9d8d66-Paper-Conference.pdf)另补核§4.1／4.2。UCF101表中列名FID使用C3D视频特征和10K生成，C3D内部resize112²；它与图像Inception FID、I3D-FVD分开记录。BAIR为100次256生成对固定256测试，不能写100个训练seed。Kinetics50K无放回抽样、生成和参考用相同随机子序列；FVD16.2→16.9来自同一模型改成旧方法的抽样协议，不能作为两个模型胜负。

空间1×3×3卷积／空间attention和时间attention因子分解，mask可让来自**同一视频数据集**的独立图像帧隔离训练。独立帧0／4／8的文字小模型FVD train参考202.28／68.11／57.84，支持联合训练设置；额外独立帧也增加监督与计算，需要等预算对照。不能把额外帧写成新增LAION图像集。

重建引导补近似条件score，对观测误差向未知帧反传，Eq7带wrα／2系数；只有相应理想模型与小噪声极限的近似依据，不能称任意t的精确条件采样。64帧外推w2 FVD136.22／134.55好于replacement451.45／436.16，支持条件块连接改善；不足以保证任意长视频物理正确。PC名义128／256步另有等数corrector调用，重建引导再加反传，名义步数不能直接作NFE或墙钟。

文字大模型w1 FVD41.65／43.70，w5为163.74／160.21，而IS提高。这里w的定义为(1+w)cond−wuncond，w1对应常用CFG条件系数2。FVD／FID双值为train／val参考，IS双值为1split／10splits，不能套同一个双值含义。作者明确不发布模型，10M文字视频来源清单不充分，不能承诺完整独立复现。

## Video LDM：时间质量与静态质量有取舍

[2304.08818v2](https://arxiv.org/html/2304.08818v2)的逐帧E不压缩时间；视频D微调和3D video discriminator处理解码闪烁。新增时间层和α融合不等训练后保持原图像函数。文本先进行WebVid空间适配，H2又明确文本插值全参训练；关键帧冻结空间骨干不能概括整个流程。

| 任务／对照 | FVD，低好 | FID，低好 | 可支持的结论 |
| --- | --- | --- | --- |
| RDS普通→条件引导生成 | 389→356 | 31.6→51.9 | 时间分布改善伴静态分布退步 |
| RDS image D→video D重建 | 390.88→32.94 | 7.61→9.17 | 重建时间改善，不等全部生成指标改善 |
| RDS单帧SR→视频SR，GT低分输入 | 165.98→45.39 | 19.71→19.85 | 时间一致改善与像素／图像质量分开 |
| Mountain LVG→VideoLDM | 85.3→118 | 21.1→7.73 | 视频FVD更差，静态FID更好 |

UCF零样本SD2.1 FVD550.61差于Make-A-Video367.23，MSRVTT帧平均CLIP.2929也低于.3049；训练数据与prompt模板还不同，不能全指标SOTA。小模型完整时间层对attention-only FVD534.17／704.41，但batch／通道／步数改变，需注明对照强度。加imageDisc后重建FVD51.01比videoDisc单独32.94差，额外目标没有自动获得协同收益。

一般FVD2048条16帧，SD2.1 UCF用10K生成；MSRVTT2990视频各选1／20描述、共47840帧测CLIP。G通用30fps与H1 RDS基线10fps需要按任务确认，不能统一填同帧率。人评100对×4回答未提供充分CI／训练seed信息。文字关键帧402Ksteps、b3×256A10080GB，插值95K、b8×128A10080GB，还有D／SR训练，不能把整体成本描述成少量LoRA训练。RDS专有、原项目本次未定位完整原检查点／实现；SVD后继资源单列。

## AnimateDiff：三阶段方法、示例代码与后继制品分开

[2307.04725v2](https://arxiv.org/html/2307.04725v2)为核心阅读版，[ICLR2024条目](https://proceedings.iclr.cc/paper_files/paper/2024/hash/94894cf9bab20c00f6eaaff3b7f2be70-Abstract-Conference.html)核正式身份。空间domain LoRA→冻结后训时间模块→可选时间MotionLoRA，推理移除／缩放domain adapter并迁移到兼容SD个性化模型。时间位置与零初始化解释结构可用性，训练后恒等保持、任意域解耦和规范事件均未被证明。

| T1量化 | T2V-Zero | Tune-A-Video | AnimateDiff |
| --- | --- | --- | --- |
| AUR文字 | 1.620 | 2.180 | 2.210 |
| AUR域 | 2.620 | 1.100 | 2.280 |
| AUR平滑 | 1.560 | 1.615 | 2.825 |
| CLIP文字 | 32.04 | 35.98 | 31.39 |
| CLIP域 | 84.84 | 80.68 | 87.29 |
| CLIP平滑 | 96.57 | 97.42 | 98.00 |

域人评与文字CLIP都存在负结果，文字人评分差缺CI，不能概括全指标最好。原主文未给足人数、CLIP骨干和聚合精确定义，原补充协议仍待取得；不能自行补一个相似度公式。Fig6仅首帧水印变化，原动画未播放核；N5外观过拟合与N50改善为数据量取舍，camera LoRA的线性组合不能外推复杂书写动作。

固定[官方e92bd56代码](https://github.com/guoyww/AnimateDiff/tree/e92bd5671ba62c0d774a32951453e328018b7c5b)读取配置与关键实现。v1运动示例256²／16帧／stride4／b4／lr1e−4／100steps；train.py只按名称解冻motion_modules，VAE与CLIP冻结。image示例b50／lr1e−5／100steps、trainable_modules为“.”使UNet参数可训，不能当论文domain LoRA完整训练配方。v3 inference、v2 453M motion及19M MotionLoRA均不同版本；README MotionLoRA文件74MB／prose77MB和原文约30M storage单位各自保留，不拼接参数量。当前仓库SparseCtrl草图能力归独立论文2311.16933，尚需另读。

## 待验证假设与研究写作

固定空间模型、E／D、条件与参考，拆时间模块、时间D、插值、共享训练、domain适配及运动LoRA，分别用等样本／墙钟／质量预算。PC corrector、重建反传、各阶段预训练、每个个性化模型增量、SR和decode计入成本。先测压缩重建OCR／细线拓扑，再测真实帧上笔事件可见性和顺序／方向／落笔状态；保持终帧相同的乱序、倒放、静止复制与瞬间出现用于检验自然视频指标盲区。将显式轨迹渲染、深度／草图控制与直接过程生成分任务比较，避免不同输入的信息优势混淆。

写作学习：VDM由模型可行性到条件score近似，VideoLDM按潜生成／插值／D／SR分职责，AnimateDiff按共享训练／域污染／小样本适配分阶段。Introduction的不足须对应可干预机制，Method每阶段写冻结和可训对象，实验保留负指标、条件与完整成本；Claim限定数据／版本／指标，Limitations写协议缺口和未解决的事件约束。以上实验设计未执行。

追引线索（尚未按独立全文完成，需去重）：RaMViD2206.07696、SparseCtrl2311.16933、VideoFusion、VideoCrafter、LongVideoGAN，以及相关视频tokenizer时间压缩工作。CogVideoX／Wan已取得原文，后续独立精读；下载到资料不计完成。
