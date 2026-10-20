# TokenFlow：共享索引、独立下游与图文主张核查

第八十一批补完[L094](../reviews/L094.md)正式核心三遍和五条书面检查。350目录、169核心/172条五项书面记录（含未通过项），181条尚未确认核心三遍（含资源）。本批无新增论文、文件删除或独立模型复现。

使用[CVPR2025正式主文11页](https://openaccess.thecvf.com/content/CVPR2025/papers/Qu_TokenFlow_Unified_Image_Tokenizer_for_Multimodal_Understanding_and_Generation_CVPR_2025_paper.pdf)及[官方supp10页](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Qu_TokenFlow_Unified_Image_CVPR_2025_supplemental.pdf)，完整阅读研究核心/指定附录并实际核看框架、理解主表、生成/消融/码本曲线和教师对照。旧arXiv记录作为历史保留，七字段与写作分析见单篇。

## 方法与任务边界

双encoder提取语义和像素特征，分别归一化，按dsem+dpix最小化取同一索引；每个索引查语义32维和像素8维两套embedding，独立decoder监督语义teacher及像素重建。多尺度残差码支持next-scale图像生成。

理解与生成分别训练Vicuna/Qwen和Llama2生成器，suppC明确全联合模型为未来工作。共享索引有双任务用途，尚无共享LLM协同证据；没有视频生成、真实绘画动作或规范笔顺任务。

## 必须写全的实验结果

| 证据 | 结果与条件 | 解读 |
| --- | --- | --- |
| T2重建 | 256²rFID1.37弱于VAR1.00；384².63较好，但SSIM.731低于VAR.774 | “384全部指标更优”超出表格 |
| T3理解 | LLaVA均分62.9、XL-Vicuna64.0、XL-Qwen67.4 | 7.2%为相对变化，差4.5分；XL数据/teacher/分辨率变化，Qwen也改变LLM |
| suppT9教师对照 | 连续58.9/61.3/62.9，离散55.2/57.5/61.1 | 同LLaVA数据仍有相对6.3/6.2/2.9%缺口；不能用主表胜LLaVA抵消 |
| T4生成 | GenEval.55原/.63改写，DPG73.38；正文DPG72.9 | 分开记录GPT4V重写成本；弱于Emu3 DPG80.60，图文数字矛盾保留 |
| T5机制 | rFID8.07→3.96→2.18→2.16；MMEP1252.38→1212.51→1209.90→1312.09 | 共享映射/MSVQ的重建改善伴理解下降，CLIP初始化才扭转 |
| suppT8输入 | 末尺度MME1634.3>全尺度1610.1，但TQA49.1<49.5，语义only49.7 | “all benchmarks”不成立 |

正式F6标2^12…2^16，正文称8192…131072；图上TQA在最大码本下降，生成FID最低点约2^14，与正文“超32768才下降”不一致。不能从正文抹去图上反例或擅自决定真实码本规模。图像pool聚类87.4%与patch占用>95%的分母/样本单位不同。

## 配套代码、模型与复现条件

固定[GH9812da01](https://github.com/ByteVisionLab/TokenFlow/tree/9812da01c0695f4989060cc4eea053715e9e4441)与[HF5924ad7](https://huggingface.co/ByteVisionLab/TokenFlow/tree/5924ad7f25fe030292de3995912b895ab9fd9321)，静态读共享量化、encoder路径、多轮采样和三类训练shell，见[制品JSON](../../data/tokenflow_codebook_sampling_audit_2026-10-21.json)。旧ByteFlow-AI仓库重定向ByteVisionLab；HF模型卡MIT、GitHub Apache2元数据分别记录，不推断上游LLM许可。

- 公开usage是本地训练131072索引滑窗，aggregate_usage=False，不能当全GPU全语料占用率。
- SigLIP像素路径将图上采样到432²，解码后缩384²，终点尺寸不等于内部全部尺寸。
- 采样每个尺度采用t=cfg×scale_fraction，logits=(1+t)cond−t×uncond；名义cfg7.5对应随尺度变化的标准条件系数1+t。无KV cache、反复前缀计算，不同模型单次调用成本不等。
- 公开demo默认loop1的topk600/p.6，论文single轮1200/.8；loop3为1200/100/1和.8/.8/0。CLI接收g_seed，实际调用硬编码None，负prompt含text。需要写出实际采用设置。
- tokenizer训练示例为ImageNet100epoch/b32，T2I10epoch/lr5e-4，正式分别web数据大量步数/b256和生成2epoch；所公开示例不能直接当原训练配方。完整60M筛选/去重和原生成优化器/算力仍未公开核齐。

未下载权重、执行脚本、重测2.7秒或独立复现任何分数。

## 可检验假设与写作学习

共享索引可在静态自然图里兼顾语义和外观，其优势需等teacher/输入/码率/计算比较；码本K、decoder增强和多轮采样分别控制，报告理解/重建/生成Pareto与OCR最小字形差。真正联合LLM需与分离训练比较正负迁移，采样要做等调用和等延迟两类对照。

同一终态字形可来自多个过程，图像码不提供唯一笔序；需要同终态异事件数据和RGB/动作评价。以上实验未运行，选题尚需相关工作追引。

可学的问题定义是先用两组诊断揭示两种失败，再映射共享索引与多尺度机制；Method将下游理解和生成分节。Claim应与suppC边界、教师差距和负迁移一致，Limitations应写清统计、训练数据与制品条件。图文冲突和按平均分的宽泛结论不能当已验证事实。
