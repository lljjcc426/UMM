# 视频骨干、联合声画与运动控制：核心三遍审查

本批完成[D01 HunyuanVideo1.5](../reviews/D01.md)、[D02 LTX-2](../reviews/D02.md)、[D03 VACE](../reviews/D03.md)、[D04 Wan-Move](../reviews/D04.md)核心方法、公式职责、框架与关键图表视觉核、主表/现有消融、批判阅读及各五项书面理解检查。无独立模型运行。四项均已有章节笔记，本批扩展其协议和批判分析，未增加重复论文。

## 任务和证据范围

| 工作 | 真实输入/输出与机制 | 主要证据及限制 |
| --- | --- | --- |
| HunyuanVideo1.5，2025技术报告 | 文本/首图→视频；8.3BDiT、Glyph条件、SSTA、独立8.3BSR | 人评部分领先、部分落后；单卡13.6GB与8H800速度分属不同配置；无规范笔顺实验 |
| LTX-2，2026技术报告 | 文字/可选声画→同步音视频；14B视频+5B音频，双向crossattention | H100每步1.22s对Wan22.30s；无完整人评数字或组件消融，不能推成片同质18倍 |
| VACE，ICCV2025 pp17191–17202 | T/F/M统一视频生成/编辑，contextadapter | LTX版多任务自动均值较好，但修补人评与参考生成有落后项；消融为验证loss |
| Wan-Move，NeurIPS2025主会 | 首图/文字/点轨迹→视频；沿轨迹复制首帧latent | MoveBench1018含192多对象，运动控制有效；遮挡、跟踪误差和严格新增墨迹未解决 |

正式身份核于[VACE CVF](https://openaccess.thecvf.com/content/ICCV2025/html/Jiang_VACE_All-in-One_Video_Creation_and_Editing_ICCV_2025_paper.html)和[Wan-Move NeurIPS主会论文集](https://proceedings.neurips.cc/paper_files/paper/2025/hash/00b67df24009747e8bbed4c2c6f9c825-Abstract-Conference.html)。Hunyuan/LTX按技术报告，不凭仓库热度附会会议或期刊分区。

## 论文和公开实现的差异

[Hunyuan v2 PDF](https://arxiv.org/pdf/2511.18870v2)Algorithm1第20行写 `Msel ∧ Msta`，固定[60783e7代码ssta_attention.py](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/60783e704160023913bee78f0b47036d393d4dfa/hyvideo/models/transformers/modules/ssta_attention.py#L446)用 `torch.logical_or`。交集与并集改变保留连接，不能默认为等价。稀疏训练在蒸馏阶段引入；parameter-free只说明不新增参数，不能解读为无训练即可保持质量。

[Wan-Move v1](https://arxiv.org/pdf/2512.08765v1)描述连续时间段轨迹均值；固定[80c58a7推理入口](https://github.com/ali-vilab/Wan-Move/blob/80c58a7d2ad175fa82a4d57f79f2a1415317dcfa/wan/wan_move.py#L277)未传 `t_down_strategy`，其[helper默认sample](https://github.com/ali-vilab/Wan-Move/blob/80c58a7d2ad175fa82a4d57f79f2a1415317dcfa/wan/modules/trajectory.py#L72)。两种时间降采样需分列，尤其快动作/短笔事件。论文正文与附录对benchmark caption模型Gemini/Qwen2.5VL描述也不同，不能静默选一者。

[LTX-2 v1](https://arxiv.org/pdf/2601.03233v1)主体14B+5B、速度表19B，结论13B+3B，保留冲突。原HF固定[dfcc210模型卡](https://huggingface.co/Lightricks/LTX-2/blob/dfcc2108383fe1aaa0584bdf55d368a4bdadd90c/README.md)发布19B dev/量化/8步蒸馏/LoRA384与上采样器；[原VAE配置](https://huggingface.co/Lightricks/LTX-2/blob/dfcc2108383fe1aaa0584bdf55d368a4bdadd90c/vae/config.json)给空间32/时间8/128channels，transformer48层，connector两层/128registers。当前[e98f6d9代码](https://github.com/Lightricks/LTX-2/tree/e98f6d927d83c92ef2be6aec76c8440b19306e39)README已指LTX2.5/22B/Gemma4，不能用当前模板补v1预训配方；thinking tokens为条件隐向量，报告明确无显式reasoning/worldmodel。

[VACE正式PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Jiang_VACE_All-in-One_Video_Creation_and_Editing_ICCV_2025_paper.pdf)与arXivv1附录的设置分开引用。[48eb44f代码](https://github.com/ali-vilab/VACE/tree/48eb44f1c4be87cc65a98bff985a26976841e9f3)保留LTX0.9、Wan1.3Preview及后续1.3/14发布，不能将所有表理解为同一个checkpoint。M0是保持条件，未证明硬像素完全保持。

## 主表和消融的可采信结论

Hunyuan GSB净差为better减otherbetter：T2V对Wan+17.12pp、对Veo−10.32；I2V对Seed−5.77、对Veo−3.61。Table7无工程8H800/720p241帧每步5.5070→2.9475s≈1.87倍；Table8工程50步96.78→58.39s≈1.66倍。13.6GB是单卡pipeline/groupoffload+VAEtiling的720p121帧配置。报告未给Glyph、Muon、SSTA同质量的完整控制消融，不能按整系统成绩归因。

LTX-2 Table1单H100/720p121帧/Euler/CFG1的sec-per-step，不含多尺度/tiling/codec等完整流程同质比较。声画偏好只有叙述，没有样本数/分数/CI；历史AA排名只是2025-11-06自述，未独立核历史快照。无组件消融按缺失记录，attention可视化不作因果证明。

VACE Table2自动均值I2V74.38优Cog73.66，inpaint72.05优Pro70.15；人评inpaint平均3.00低Pro3.11、flow prompt2.90低FLATTEN3.50。R2V人评3.40低商业3.84–4.04。Fig5以每任务250验证例平均loss比较adapter/层配置/decouple，不直接测控制精度或未见任务组合。240测试视频平均每任务20，且对照有256p/短视频，需保留样本与资源混杂。

Wan-Move Table4 latent复制EPE2.6优pixel3.7；Table5 ControlNet EPE2.5略优concat2.6，但后者FVD83.5优84.6、总765s低987s。`+3s`是额外开销。vsKling2AFC47.8/53.4/50.2近半数，缺CI不能证明等价或显著领先；vsTora运动质量93.8与正文“all>96”不符。更多test oracle轨迹提高控制也增加输入信息；手画稀疏轨迹需单独评。长期遮挡、拥挤、物理不可能轨迹和上游CoTracker错误均未消除。

## 公开模型、数据、适配配置

本批读取HF卡/文件元信息，未下载权重或视频。MoveBench固定[d02e0c4](https://huggingface.co/datasets/Ruihang/MoveBench/tree/d02e0c4d74abcc1af9f4913815b76348511f74b3)给en/zh、首帧mask、track/visibility和bench.py，MIT标签；1018与其中192多对象按同视频计数。Wan模型固定[63a21fd](https://huggingface.co/Ruihang/Wan-Move-14B-480P/tree/63a21fd3f4f1e6c6104e29f6b8d9b8ce3d635456)Apache2，README评测要求关prompt extension；低显存40GB需T5CPU/offload/bf16，不能拼接论文另一时延当联合保证。

VACEBenchmark固定[c70300e](https://huggingface.co/datasets/ali-vilab/VACE-Benchmark/tree/c70300e817d21c9fdb6bccddecadf8d57e02a0f3)元信息765文件、2025-10补评估资料；未逐样本核视频/评分。模型许可随原LTX RAIL-M/Wan Apache2分别记录。

Hunyuan公开续训模板Muon/lr1e−5/b1/10Ksteps、LoRA r8/alpha16，要求替换dummy数据加载器。LTX当前LoRA有效配置r32/alpha32、AdamW1e−4/2Ksteps/b1/bf16、jointAV训练，验证30步/CFGvideo3/audio7/跨模态3；它们是适配入口，均不能填补原预训未公开的batch/steps/GPUh。LTX原19B为community license，不能按代码可见推Apache2。

## 可证伪实验与写作学习

同数据/总FLOPs/精度/分辨率/长度控制，比较骨干、Glyph、SSTA AND/OR、联合/顺序声画、VCU全参/adapter、坐标/随机外观/latent复制/ControlNet；分离预训/后训练与推理开销。视频质量、控制误差、人评CI和全部pipeline latency/peakVRAM同时报告。替换跟踪器或给人工轨迹，区分上游条件与生成误差。

书写单设空白纸到墨迹增长、笔尖接触/抬落、方向/次序/漏重笔与遮挡后可见性，oracle与预测轨迹并列。Glyph文字渲染、scribble条件生成和点运动控制都已有相关贡献，未验证规范书写事件的部分才进入后续假设。LTX声画同步可启发多时钟对齐，但不能由静态图示推执行正确。

Introduction可学习表示/注入两问与系统瓶颈拆分，Method按输入协议和模块职责组织；Claim明确单步/成片、净差/胜率、均值/分项及版本，Limitations写已有负结果和协议缺项。本批后339目录/339笔记，74项核心三遍与五项书面检查；剩余核心精读、候选追引和五项全文阻塞仍在继续。无文件删除。
