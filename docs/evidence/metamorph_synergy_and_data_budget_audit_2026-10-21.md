# MetaMorph：协同、数据预算与制品条件审查

第八十二批补完[L090](../reviews/L090.md)正式研究核心与官方补充材料。350条目录，170项核心三遍、173项五条书面记录（含未通过项），180条尚未确认核心三遍（含资源）。未删除文件、下载权重或复现模型。

阅读[ICCV2025主文12页](https://openaccess.thecvf.com/content/ICCV2025/papers/Tong_MetaMorph_Multimodal_Understanding_and_Generation_via_Instruction_Tuning_ICCV_2025_paper.pdf)与[官方supp8页](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Tong_MetaMorph_Multimodal_Understanding_ICCV_2025_supplemental.pdf)，核看框架、相关性图、主结果和数据/模型消融。八项笔记、七个协议字段、五个因果问题及写作分析见单篇；此处集中列需要影响研究判断的证据。

## 表示和任务

冻结SigLIP视觉编码器，压成64个连续视觉token，MLP适配进LLaMA；文本用交叉熵、图像响应用余弦损失。独立SD1.5可视化器将预测特征解成RGB，训练projector/UNet、冻结VAE。理解与生成共享LLM，视觉编码器和像素解码器承担不同部分，不能据此宣称零外部生成训练。

主配置为LLaMA3.1-8B，另有LLaMA3-8B/70B；不同底座的结果分开。本文任务没有规范汉字笔顺、绘画动作或逐笔视频评价。少量推理/知识例图不能独立证明内部视觉推理机制。

## 主表、反例与混杂

| 位置 | 原始证据 | 可支持的结论和限制 |
| --- | --- | --- |
| 主T1 | SQA83.2、VStar44.0、Chart37.1、TextVQA60.5、FID11.8 | 多项弱于表列理解模型；FID弱于Janus8.5、Transfusion6.7和SD1.5的9.6，不能写全面领先 |
| suppT3 | 余弦联合Avg55.93、VQA-only55.50，L1联合53.83 | 余弦缓解总体冲突，但MMMU37.29→35.29、TextVQA59.96→59.79等仍退步；作者未公平比较L1/余弦生成质量 |
| suppT4 | 5K T2I下联合FID19.2、仅生成116.4 | 支持指定配置下借助理解训练迁移，5K只计T2I子集；其他输出图像任务和可视化器训练不能忽略 |
| suppT4重复行 | 同为200K出现15.2/110.7及14.7/93.7两组FID | 已实际核看表格；无法据此擅改第二行数据量，保留来源冲突 |
| suppT6 | 7M VQA时1M→2M T2I，Avg55.8→55.4、FID14.5→14.8；3M→4M FID14.2→14.9、CLIP27.5→26.3 | 整体趋势容许局部负迁移，数据更多不保证每项更优 |
| suppT7 | 3.1-8B Avg56.7/FID13.2/CLIP27.1，3-70B 60.7/13.8/26.8 | 更大模型在该对照中提高理解，生成退步；底座版本也改变 |
| F8 | SEED与CLIP相关.94、与FID−.95；MMMU与CLIP−.26、与FID.23 | 不能概括所有任务正相关或将FID符号反写；数据量、步数和共同训练造成混杂，相关性不单独证明因果协同 |

数据表列Cambrian ImageQA7067K、MetaCLIP5000K、VideoStar1055K/ShareVideo540K、HowTo1193K/SmthSmth220K、VisualCoT361K/VStar148K、IP2P313K/Aurora169K，合计16.066M条目，跨集去重后的唯一数未给。suppC3承认图像可能重叠；QA不逐条完全重复不足以证明无污染。训练一epoch时数据量同时改变优化步数，不能当等算力研究。

## 无独立论文制品也纳入

固定[官方GH 0b13debf](https://github.com/facebookresearch/metamorph/tree/0b13debff55363c81dce90ad21269d05e7f7ac80)，静态阅读模型、数据载入、训练、可视化与提交脚本，记录于[制品JSON](../../data/metamorph_data_cfg_release_audit_2026-10-21.json)。该固定README仍称权重待批准，MetaCLIP原始数据未公开；CC12M/LAION/COYO替代配方改变分布。可核流程与原模型重建条件分开记录。

`cfg_prob`控制训练时随机把图像条件置零；论文“CFG level .7”不能直接填作推理guidance scale。脚本示例.8/默认.1也不证明原训练值。README adapter batch448/lr3.74e-5与正式768/4.90e-5不同。greedy_decode在llm_forward内部执行视觉head和回投影，不能因返回变量名误认其绕过图像预测head；关闭KV cache影响实际成本，尚未实测。

正式可视化器batch2112、约14K步，约29.568M样本暴露次数，不能等同唯一图像数；推理完整步数/CFG/种子尚未核齐。LICENSE为CC BY-NC4.0头，README说明部分来自Apache2代码；分别保留来源范围，不扩大成统一上游授权判断。

## 实验与研究写作学习

协同假设应在相同初始化/数据身份/总token/步数或FLOPs下比较理解单任务、生成单任务、联合、等量额外任务及打乱配对；多种子报告逐任务正负迁移，控制decoder和teacher。去重审查要覆盖图像及近似图像，分域/分字符测真实迁移。验证余弦机制需控制幅值和损失权重，测梯度冲突及细字形丢失；不能把更多监督收益都归因表示统一。以上均为未运行的设计。

Introduction先提出视觉监督统一，再用可扩展数据实验组织协同主张；Method区分视觉表示、响应训练和可视化；实验写作应同时呈现主表、单任务对照和规模矩阵。Claim应限定总体趋势、数据与预算，Limitations需明确重叠、原始数据/权重、外部解码器和例图证据的边界。共享连续特征对过程信息是否足够仍要同终态异轨迹数据验证，不能直接迁移为笔顺创新。
