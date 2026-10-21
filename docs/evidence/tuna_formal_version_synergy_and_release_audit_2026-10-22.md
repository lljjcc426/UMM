# TUNA：正式版本、任务协同与公开实现审查

第一百一十六批完成已有[L100](../reviews/L100.md)明确范围的核心三遍与五项书面记录。[结构化审查](../../data/tuna_formal_version_synergy_and_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），225核心/228书面含未通过项，132条未确认核心（含资源）。本批没有新增目录、删除文件、下载权重或运行模型。

## 原始来源与阅读范围

正式[CVPR2026](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_TUNA_Taming_Unified_Visual_Representations_for_Native_Unified_Multimodal_Models_CVPR_2026_paper.html)，pp15740–15751，完整12页PDF；官方链接的完整supplemental.zip内只提取12页TUNA_appendix.pdf，未播放其中视频。正式Abstract/§1–5核心、Eq1–3、T1–6及F1–4图注，附录§6–12研究文字、T7–11和F5–8图注已读。参考文献未逐篇追读，其他定性图未逐图。另读固定[arXiv2512.02014v1](https://arxiv.org/abs/2512.02014v1)核心和T1–7比较版本。实际核正式p3 F2、p6 T2–4、p7 T5/6、p8 F4，以及supp p2 T7–10。

本作处理图像/视频理解、静态生成/编辑、视频生成。静态OneIG文字维和少量视频文字案例均不构成规范字形、逐笔事件或严格笔顺评价。7B变体没有视频训练，视频结果使用1.5B LLM骨干变体；不能写全系统仅1.5B。论文脚注把native定义为任务共同预训练，不能解释成全部权重从零训练。Intro将Transfusion归为VQ-VAE不准确；[U05](../reviews/U05.md)使用连续VAE表示，保持独立核查后的分类。

## 问题、机制与优势假设

论文关注语义和生成表示的格式/时空压缩差异，以及晚融合时的任务偏向。冻结Wan2.2 causal3D VAE，以改造patch层的SigLIP2编码VAE潜变量，经两层MLP输入Qwen2.5-Instruct；文字用AR，随机初始化的flowhead回归速度。理解取干净latent，生成处理带噪latent，`x_t=t*x_1+(1−t)*noise`，视觉bidirectional/文字causal，另有时间token、AdaLNZero和3DRoPE。

VAE空间×16、时间×4。论文称SigLIP2-400M16-512，patch16改随机1×1，公开原版模型配置显示48通道。latent帧并入batch独立编码，但causalVAE可能保留此前信息，不能据“4帧窗口”推断严格4帧感受野。这是连续表示级联，与[L099](../reviews/L099.md)固定离散索引/适配embedding级联不同。

可能的优势依赖VAE保留任务信息、语义encoder适配带噪潜空间、混合比例适当。有限消融可支持所测配置的折中，尚不能证明所有连续表示优于离散、所有共享架构优于解耦，或共享训练对全部任务都有正协同。

## 数据与实验条件

正式§3.1补充177M私有image-caption用于I/II；FineVision13M对话和OmniEdit约2M用于II/III；约10M高质量SFT图文含筛选真实与少量其他T2I模型合成。视频约10M私有caption对和LLaVA-Video178K约1.6M instruction用于II/III。存在跨阶段/来源关系，不能直接相加为去重样本量。训练过滤清单、完整混合/去重和benchmark重合审计未给。

| 条件 | 正文与附录证据 |
| --- | --- |
| 学习率 | 正文I/II=1e-4、III=2e-5；sup T7为1e-4/5e-5/1e-5，差异保留 |
| 训练进度 | sup T7 constant；steps200K/100K/30K，warm2K/2K/3K，wd0、clip1 |
| 优化器 | I/II共用β.9/.999、ε1e-15；III β.9/.95，III ε未给 |
| 损失/EMA | CE:MSE=.2:1；EMA .9999/.9999/.995 |
| 任务比例 | gen:und:text=4:1:0→3:1:0→4:2:1 |
| 分辨率 | 短边/长边上限I/II gen和und(384,672)，III gen(384,1024)/und(384,672)；shift3/3/4 |

GPU数、global batch、总卡时、视频FPS/实际帧长、benchmark每prompt采样次数/seed未齐。公开训练示例与原文条件不同，不用于填补这些空白。消融用子集、较小flowhead和I+III相同步数，也未证明每任务曝光或总FLOPs相同。

## 主表和消融支持到哪里

| 结果 | 作者报告与限制 |
| --- | --- |
| 理解T1 | 7B MME1641.5/GQA63.9/RW66.1/SEED74.7/MMMU49.8/MMStar61.2/AI2D79.3/Chart85.8/OCR74.3；BAGEL的MME1687/SEED78.5/MMMU55.3/AI2D89.2更高，1.5B SEED69.3低于JanusFlow70.5 |
| 生图T2/3、supT8 | GenEval7B .90、1.5B .88；7B count.81低于BAGEL.84、color.91低于Mogao.93。DPG86.76/86.03。OneIG avg.50/text.82低于QwenImage.54/.89，diversity.19低于Janus.37 |
| 编辑T4、supT9 | ImgEdit4.31，extract2.46低于Qwen3.43、style4.69低于4.81；GEdit7.29低于Qwen7.56。正式编辑子分与v1不同，overall同4.31 |
| 视频T5 | VBench total84.06/Q84.32/S83.04；DD69.39低于Emu379.27，SC95.99低于Showo297.28，AS23.18/TS24.68也低于Showo2；总分和分项须一起解释 |
| 视频理解supT10 | 54.4/49.1/49.7/27.4，未在全部任务胜专用大模型。v1 T5列16/32/49/64不同输入帧，正式supT10无帧数列，不混写版本 |
| 单→联合T6/supT11 | MME1386→1361，MMMU37.6→38.1、SEED62.9→66.5、GQA57.4→58.2；GenEval77.8→79.4、DPG83.33→84.20。因此MME−25，不能写全指标受益 |
| 架构消融 | 联合解耦1346/37.2/61.4/56.5/78.3/83.50低于对应TUNA配置；DINOv3相对SigLIP2 MME1396更高但MMMU37.3、Gen78.9更低；Wan2.1→2.2的MME1379→1361、GQA58.4→58.2下降 |

正式T6九行，supT11完整13行，v1为T7；Showo2联合MMMU正式35.5/v1 35.4。GenEval部分基线带LLM重写†，跨架构/数据/模型规模条件不等，未核齐所有prompt/采样预算。CKNNA使用1024 WikipediaCaptions图比较层特征邻域，实际F4中SigLIP2两曲线交叉、各有高低，SD3对齐TUNA逐层较高。峰值/支路相似度不证明因果、不量化有效任务信息，缺少CI与干预。

## 公开实现与无论文制品的审查

旧[wren93/tuna](https://github.com/wren93/tuna)当前README指向[facebookresearch/tuna-2固定b53594e3](https://github.com/facebookresearch/tuna-2/tree/b53594e308095b573c31be46f24ea62936f3c440)。完整2142项树用于定位，大量lmms-eval未逐文件读。已读README、tuna训练guide、原版2b/7b配置、训练/视频/预测示例，并选读模型初始化、forward、输入选择、损失、帧处理、dataset和loader/unit调用链；attention/transport/VAE/eval底层未全读。

原版`tuna_2b`对应Qwen1.5B，`tuna_7b`对应7B；默认训练模型`tuna_2_pixel_7b`属于[L105 Tuna-2](../reviews/L105.md)，需显式选择原版。本作配置48通道、32latent设置、SigLIP配置384与论文512表述不同，另有截断层设置。示例flowhead16层、CFG7.5/Euler50/bf16等是代码条件，未证实等于论文所有benchmark协议。通用示例任务50%T2I/20%edit/20%MMU/10%text、lr2e-5/wd.01/warm1K，与正式全课程不同。

README权重TODO未勾、说明完整生产模型受发布限制并计划发布移除部分层的foundation；训练guide又称released foundation的部分层随机重初始化。两处表述有差异，本次未核到对应下载链接及精确checkpoint，保留待核，不概括为世界范围没有权重。代码Apache2与上游模型授权分别看待。视频有训练/预测入口，README称受政策限制未发布video model；`latent_frames=13`是潜帧参数，不能直接称13帧RGB或已验证49帧。未下载权重或运行模型。

静态调用链发现需优先测试的条件分支：TIDataset对T2I也可返回clean `images_clip`；默认loader/unit传入模型；forward把该分支做deterministic VAE作为`pixel_values`；`_prepare_embeds`有值时优先于带噪`image_latents=x_t`。在此配置下，可能出现训练条件含clean目标、推理从noise条件的差异。这里只追了公开代码的条件路径，未执行张量probe，不能据此判原论文checkpoint训练错误。需检查实际数据字段、运行覆盖和版本配方后再作结论。

## 可证伪实验与研究写作

固定VAE/encoder/flowhead/LLM容量、样本和总FLOPs，比较解耦、晚融合、深融合；分别固定总步与每任务曝光，记录多seed全部退步项及Pareto。CKNNA配合模块替换/信息probe；公开实现先对clean/noisy两路做张量追踪，再谈复现。文字/绘画应用按小字、非汉字、短于4帧的接触/抬笔事件分层，建立真实动作/墨迹GT并与SVG强基线比较；VBench、静态OneIG不能替代笔顺评价。这些实验尚未运行，创新性还需追引。

Introduction按表示格式、成本与协同组织，Method从级联表示、共享骨干/head到三阶段课程，实验对照表述清楚。正式版把数据补入§3.1，并将长相关工作、OneIG/GEdit/视频理解移附录，精读需要两处联读。Claim应保留模型规模和任务范围、MME退步、强基线与不等预算。未见单列Limitations；本审查补充私有数据、完整成本、配方/发布差异和未评价文字视频的限制，不冒充作者已讨论。
