# 视频评价：VBench、FVD与过程任务的证据边界，第五十一批

深化[VBench G031](../reviews/G031.md)、[FVD G032](../reviews/G032.md)。344项＝318论文／研究＋26资源，核心三遍119、五条书面检查121。本批核读精确版本核心、主表、原图及现有诊断对照，并选读固定官方源码。无删除、训练、推理或独立复现。所有后继工作继续独立精读；不能用本页替代整个视频评价领域的完整调查。

## 研究问题和输入输出

| 工作 | 所解决的评价困难 | 实际输入→输出 | 不可由结果直接推出 |
| --- | --- | --- | --- |
| VBench | 总体质量难诊断、自动分与人判断的关系不清 | 特定prompt采样的既有生成片→16维专家分、人/自动模型胜率、内容类分析 | 规范汉字视频生成能力、逐样本完全正确、维度统计独立 |
| FVD | 逐帧配对误差难评价多未来/无条件视频分布 | 真实/生成视频批→固定I3D嵌入→Gaussian两矩距离 | 每个输入指令正确、事件顺序正确、真实视频分布相等 |
| FVD论文的SCV | 自然动态难隔离、简单合成难度有限 | SC2Map/SC2LE agent/replay→可控游戏过程视频 | 新视频生成模型或新提出BAIR/SC2LE |

VBench实际精读[2311.17982v1](https://arxiv.org/html/2311.17982v1)及G/H/I/J/K–L/M指定附录。另已取得[CVPR2024正式PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Huang_VBench_Comprehensive_Benchmark_Suite_for_Video_Generative_Models_CVPR_2024_paper.pdf)，视觉核首图、核T1及Fig5caption。正式T1的CogVideo背景一致性为96.20%，v1为95.42%；保留版本差异，其他会议PDF页未逐页全比。arXiv HTML的Fig1仅有caption，未据此冒称看过图；框架视觉依据正式PDF。

FVD实际精读[1812.01717v2](https://arxiv.org/html/1812.01717v2)核心和AppA/B/C。首次2018，v2为2019-03-27。相关[2019 workshop短文](https://openreview.net/pdf?id=rylgEULtdN)标题FVD: A New Metric for Video Generation，原PDF注明workshop；当前只核该短版身份/摘要，不能记成ICLR主会论文，也不把长短两版重复统计为两个独立指标。

## VBench：16维如何运行

| 维度 | 评价模型/规则 | 需要保留的适用条件 |
| --- | --- | --- |
| Subject Consistency | DINO整帧特征，对首帧与前帧cos平均 | 无主体分割保证，正确增加笔画也可能改变特征 |
| Background Consistency | CLIP整帧特征，同样对首/前帧 | 无背景分割保证，不能仅凭名称推断关注区域 |
| Temporal Flickering | 静态片相邻帧MAE，1−MAE/255 | 论文用静态prompt并光流筛；运动视频不能直接按同语义解释 |
| Motion Smoothness | 丢奇数帧→插帧恢复→MAE归一 | 插帧先验相符不等物理/笔画规则正确 |
| Dynamic Degree | RAFT，取光流最大的5%均值判动，统计非静态片比例 | 高运动不保证目标运动正确；静态投机已在原文讨论 |
| Aesthetic Quality | LAION aesthetic逐帧0–10→0–1 | 美学代理及其领域偏好 |
| Imaging Quality | MUSIQ-SPAQ逐帧/100 | 低层质量代理，细线/风格域需校准 |
| Object Class | GRiT目标类别检出帧比例 | 检测器误差混入生成器误差 |
| Multiple Objects | 所有要求类别同时检出帧比例 | 数量/遮挡/相近类影响，非严格字符多笔实例评价 |
| Human Action | 16帧→UMT，top5且阈值>.85候选与prompt动作匹配 | UMT非UMM，Kinetics动作不等笔事件 |
| Color | GRiT框与dense caption，目标颜色匹配 | 只在检到目标且caption有颜色的帧计分，分母影响覆盖 |
| Spatial Relationship | GRiT框、左右/上下轴距离及IoU系数 | 仅所列关系与可检目标，不覆盖笔画拓扑 |
| Scene | Tag2Text caption包含场景词 | 同义词/词表/组合性受限 |
| Appearance Style | CLIP帧/风格文本cos | 风格相似度不等绘制过程 |
| Temporal Style | ViCLIP视频/时序风格文本cos | 全局语义可能忽略短事件 |
| Overall Consistency | ViCLIP视频/完整prompt cos | 不能保证每个词/笔按要求执行 |

每维约100prompts，若干维共享；不能算作1600互不重叠测试。另8类各100共800。WebVid参考先按caption文本CLIP检索top5、截2秒/8fps；J2部分端点直接设0/100，另部分为检索/构造的极值，均不能当统计上确切分布上下界。J2末“错误语义100%”与零端点表矛盾，按原文笔误记录。

原采样并不严格匹配：LaVie16×512²、8fps、250DDPM、CFG7；ModelScope和VideoCrafter0.9均16×256²、8fps；CogVideo33×480²、10fps并译中文、执行插帧。所列模型seed2不表示同随机样本、等计算量或全部实验参数相等。历史结果回答当时接口下的比较，不能单独归因架构。

## 人类对齐究竟验证了什么

每prompt五组、每组四模型六配对；随机播放顺序，限定当前评价维度，胜1/负0/平.5。标注规则、60条试标、每60条包抽20%、错误>10%重标，作者再检查。总标注者数、多标一致率和按prompt/模型泛化CI未完整披露。

Fig5/A5每维只有四个模型汇总点。原caption称Spearman，但主体四点：自动[67.87,49.07,24.72,58.33]，人[69.95,56.30,20.42,53.33]；按表值重算Pearson=0.965075706，与原0.9651吻合；Spearman=0.8。正式CVPR Fig5仍称Spearman。这里指出数值与名称不一致，未无依据改写作者整个统计流程；需要原脚本进一步确定。颜色原相关0.6073，不能概括“所有维度均>0.8”。四点汇总相关也不等逐视频预测准确率。

FigA11静/半动/动态闪烁人胜率相关约.99，同样为四模型观察，支持该范围内排序相近；不能证明运动与闪烁在任意分布统计独立。原T1 LaVie背景/闪烁高但dynamic49.72，VideoCrafter dynamic89.72而平滑91.79；多维权衡已在原文讨论。内容类数据量/美学的相关性可启发数据假设，未通过干预实验证明数量无效或质量唯一决定。

附I.2 VideoChat-embed微调30K instructions、3epoch、lr2e−5、总batch64、8×A10080G约1h，数据含自动分映射0–10与人偏好。文中前后示例显示潜力；未见独立heldout定量表，不补出评价泛化准确率或新生成器训练收益。

## 官方实现的版本和调用条件

VBench代码固定[fd18b3d](https://github.com/Vchitect/VBench/tree/fd18b3d055cb0fc6f066ca90fe2c3c8cbb698490)。选读dynamic_degree.py、temporal_flickering.py、subject_consistency.py、background_consistency.py全文，README指定用法/版本区分和scripts/constant.py。其当前实现与2023原实验代码分开。

- Dynamic：mp4约按8fps取帧，光流20iters；阈值6×min(H,W)/256，要求超阈对数round(4×T/16)；分数是非静态视频比例。改变fps/片长/分辨率可能改变判别。
- Flicker：局部评分函数直接算MAE且注释要求静态，自身无光流筛除；不能只调用这个函数便声称已执行论文静态筛选全管线。总入口/所有依赖未全审。
- Subject/background：cos负值截0，整帧编码。主体单进程按有效帧对聚合，而多进程收集各片分再均值，混合长度时可能不同；背景多进程保留总和/计数按帧加权。未运行，不能断言当前标准等长benchmark受影响。
- 当前总分README与constant：固定端点归一后质量组dynamic权重.5、其他1，语义组各1，质量/语义权重4:1。它和原雷达“当前模型min→.3/max→.8”不同。自定义视频默认支持六维，不等自动具备原16维标准prompt/标签协议；完整聚合脚本、依赖和权重未全核。

Google原FVD实现固定[3ef52111](https://github.com/google-research/google-research/tree/3ef52111c1fabc301880818f5a547570e926a76b/frechet_video_distance)。README和FVD.py全文已读：视频[B,T,H,W,3]、RGB0–255，逐帧bilinear至224²并映射[-1,1]；TF-Hub Kinetics400/1的RGB/inception_i3d/Mean:0 logits，嵌入调用固定batch16；最终交TFGAN的frechet_classifier_distance_from_activations。batch16是每次嵌入批量，非整场评价仅16样本。README列TF/TFHub但代码还需TFGAN/six；未安装或执行，未读TFGAN内部数值分支，不能保证任意PyTorch移植自动同数。

这些是论文关联工程制品，未另增独立论文数；现有非论文资源入口已关联，继续分别审计后继版本/依赖/配置。

## FVD：理论、现有消融和反例

FVD对I3D特征拟合Gaussian，用||μr−μg||²+Tr(Σr+Σg−2(ΣrΣg)^1/2)。这是特征Gaussian的平方W2近似；原视频分布不同但特征两矩相同仍可能零分，不构成“视频分布完全相同”的判定。I3D动作特征携带时间信息，也不能因此推断它敏感于任意短笔事件或遵循文字指令。KVD采用三次kernel的无偏MMD²估计，不能把“无偏”转给有限样本FVD。

原噪声消融比较K400/K600、logits/pool、FVD/KVD和平均帧FID，在BAIR/Kinetics/HMDB加八类扰动。Fig3/6已视觉核：FVD能感知多种扰动，但interleaving强度并非全单调，K400logits并非每项最优；“八类均有响应”与“对每类严格单调或域外准确”是不同强度的主张。Fig4同分布不重叠子集FVD随N上升下降，50次抽样SEM；固定N是比较必要条件之一。

人评在BAIR历史条件预测模型，2context+14future；PSNR/SSIM每context100候选取最优。选10个同分或跨度模型、各3片、先两评者不一致再第三、盲模型可平。T1 spr.FVD与人一致71.9%，优于SSIM61.8/PSNR54.1/KVD69.4；但spr.SSIM列AvgFID62.7高FVD58.4，spr.PSNR列KVD63.8略高FVD63.5，不能写全列全胜。Fig5“约50点可感知”是BAIR特定模型/采样/人评经验，非所有数据通用阈值；“平”在该图计作不一致，需保留。

T2 SAVP BAIR116.4/KTH78.0最优，但MUtB64² SVP-FP276.7优于SAVP479.7、128² CDNA51.4低于SAVP204.4。FVD本身未提出SAVP，不能误写新方法模型结果。SCV各场景10000/2000/2000，动作click线索在RGB中，重放可调分辨率；不同任务反映路径、实体关系与记忆难度。各生成器训练300K更新，网格lr1e−3/4/5与β等；原β列表含重复1e−6，RTwM正文最多2+32与数据最大32帧口径有疑问，不擅补。原文概述3000模型和后文20000含训练阶段快照的口径分开，不全部称独立训练run。

## 过程任务的可证伪实验和写作学习

保持最终图像相同而改变顺序/方向，分别注入漏笔、重复、同时增墨、反播、静止；再加背景运动、正确纸面增墨与正常抬笔。固定fps/片长/分辨率/压缩/提示语言，报告每类检测能力、漏检覆盖和事件时间误差；按作者/字形/规范/模型留出。分布指标固定嵌入权重/层、N、裁片/是否context，给随机子集CI与独立人评；训练seed另列。不可用提高Dynamic Degree证明正确过程，也不能以同终图OCR证明正确顺序。

写作学习：从可观察失败定义评价目标，给量表、输入/预处理、代理机制和人评协议，再按失效假设安排扰动/跨域/留出实验。Claim区分模型级排名、视频级分辨与事件级正确，Limitations公开代理/域偏移、样本量、统计名称和版本差异。需要追引已解决部分，再评剩余不足是否具有新颖性。

## 继续追引：尚未计作精读

- [VBench++ 2411.13503](https://arxiv.org/abs/2411.13503)：原摘要/当前官方README确认扩展I2V、自适应ImageSuite及可信性；README称TPAMI2025，正式期刊身份/分区另核，未据README独立认定SCI一区。
- [VBench-2.0 2503.21755v2](https://arxiv.org/abs/2503.21755)：原摘要/README确认五大类、18细维与通用/专用评价器，需精读物理/常识/控制的定义和校准协议。
- [On the Content Bias in FVD 2404.12391](https://arxiv.org/abs/2404.12391)：原摘要确认已有内容/时间偏置分析与新特征方案；需精读而不能把时序偏置当本仓库新发现。

三者主目录当前未检到对应ID；本批仅作明确追引，接着核全文/去重后纳入。原VBench其他大附表未逐格、全部样例图/数据/权重、后继全文与FVD短版全篇仍在队列。全部剩余研究审查继续。
