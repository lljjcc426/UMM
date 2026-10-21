# PixelUMM：原始像素、管状块与协同证据

第一百二十三批完成[L108](../reviews/L108.md)固定v1核心三遍及五项书面记录。[结构化证据](../../data/pixelumm_xprediction_tubelet_and_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），232核心/235书面含未通过项，125条未确认核心（含资源）。本批无新增目录、删除文件、权重下载或模型运行。

## 来源与定位

固定[2609.38597v1](https://arxiv.org/abs/2609.38597v1)，2026-09-29，完整31页。读Abstract/§1–5、Eq1–2及未编号目标、T1–9、F1–F8实验文字与全部21图注，实际查看PDF p5/7/8/11/13/14/17/19/22/23十页；未逐图看其他展示或逐篇读参考文献。无独立附录，本批未核实正式会场/期刊接收。

[官方项目页](https://nv-tlabs.github.io/PixelUMM/)与[代码固定e19e91a](https://github.com/nv-tlabs/PixelUMM/tree/e19e91aabb99784f7b5524268ed42ec59c1ad660)、[HF固定4bb3ce9](https://huggingface.co/nvidia/PixelUMM/tree/4bb3ce9a112e7e1c7d375b1c5bd64f54d259ecc8)交叉核对。官网文本已读，动态视频未播放。完整115项代码树、README/CHECKPOINT/EVAL/TRAIN、F22/F18 profile、Regular21评测合同、GPUtubeify全文及model_factory/主模型指定段选读；未全审所有源码/solver/依赖或执行。

真实任务为图像/视频理解与生成，96帧/24FPS/4秒T2V，额外F7微调I2V/编辑。没有规范笔顺、跨文字书写或绘画事件评测。文字prompt生成自然视频和视频中的字串正确性/书写动作需分别评价。

## 方法与公式

图像16×16 patch、视频4×16×16 tubelet，各经任务独立单层linear接Qwen3 MoT。clean图像/视频与文字走理解专家，noisy目标走生成专家；Norm/QKV/out/FFN仍分专家，每层共同attention运算。输出RMSNorm+linear再unpatchify，迭代积分生成RGB。HF模型卡总参15,199,672,064（约15.2B），论文“8B MoT”指骨干/专家规模，不能直接当全系统8B。

图像一个双向块，sparse视频帧内双向/帧间causal；dense segment可构成一个双向tubelet块。生成完整目标内双向，前文不能回读目标。三轴RoPE temporal占半head，HW各1/4，thetaT1e6/HW1e4。理解FlexAttention、生成two_way两次变长FlashAttention；这些mask不提供规范书写动作约束。

\(z_t=(1-t)x+t\epsilon\)，head预测clean \(\hat x\)，以\((z_t-\hat x)/\max(t,0.05)\)对\((z_t-x)/\max(t,0.05)\)算v-loss，即\(\max(t,0.05)^{-2}\)加权cleanMSE。网络不显式接t/AdaLN，但加噪、转换速度和采样仍需要t。发布代码构造了冻结time_embedder，指定路径没有用其给denoiser条件，不能把“无显式时间输入”写成程序完全没有时间模块。

3Dpatchify只是重排，本身可逆。4×16×16 RGB为3072标量，F11给hidden4096；若线性满列秩，3072→4096可单射。把4帧合token不自动等于丢掉3/4信息。实际短笔画损失须分别核采样FPS、resize、投影秩、学习过程与输出head。p32t1与p16t4均1024像素/token，几何布局不同而loss不同，也说明不能只用token码率解释。

## 八组实验的因果边界

| 实验 | 结果 | 可以支持与尚不能支持的内容 |
| --- | --- | --- |
| F1图像patch | p16低于p32训练MSE；p32同seqbudget可多处理4倍图像 | 支持所测步数/token预算下优化难度差异；样本曝光与linear参数改变，尚无等全部成本的普遍最优结论 |
| F2视频tubelet | p32t4/p32t2/p16t4/p32t1；最后一项loss最低，最终选p16t4 | 选择理由为对齐常见VAE时空约定；p16t4并非所有指标最优。p32t1与p16t4同像素/token，不能只归因总压缩 |
| F3输出head | linear空间/时间边界1.078/1.160；Wan约1；TS1.033/1.033、ST1.039/1.037 | Wan loss>.05且更糊，shuffle约.02。均匀模糊也可降低边界，需内容/动作保真共同验证。72prompt mean±SEM不等训练多seedCI |
| F4pixel/VAE | 10K时VAE-loss约4.3倍、梯度norm近似，pixel偶有spike | 不同输出空间/目标方差，且pixel x-pred与VAE v-pred混杂，数值大小不能证明学习速度或质量优劣 |
| F5容量 | b256，8B约14K对40K达到MSE.06，10K对31K达CE.5 | 约3倍步数效率；未提供同FLOPs/GPU时/墙钟收益，MoT专家规模不能当总参 |
| F6资源 | 1.7B，8→128GPU；CE1约2K对17.5K，MSE.065约17K对23K | 16倍GPU数，globalbatch/累计曝光和通信时间未齐，不能称9倍算力效率或墙钟加速 |
| F7条件任务 | 15K八任务后图像9升11降1平；两mode四video均升 | SEED-I−5.41、OCR−.30、V*−1.57需保留；额外video监督/训练步数混杂，无等15K旧任务继续训练对照，不能唯一归新条件能力 |
| F8video接口 | 同Und3第9K点，dense−sparse +.07/−.22/−.68/0 | 4FPS未稳定更好，无显著性/等价检验；只≤96s且源≥4FPS真正切换，其余fallback相同，整体均值会稀释目标子集效果 |

F3四head的卷积/linear前向成本在96×176×320下为133/2274/1279/747GFLOPs，参数12.6/18.3/52.9/15.1M；排除了norm/activation/无参shuffle，只计head，不能作完整模型或整个采样的成本。发布检查点、主表及非该消融展示均保留linear；卷积改进没有自动进入正式评测。

F8 dense对短高FPS视频采4FPS≤384帧，τ4；sparse采1FPS≤96帧。低FPS或长视频均回退逐帧/均匀≤96帧，nativeaspect每帧448²预算。它不证明高FPS对抬笔、短事件或逆序识别无用，也不等于长视频都以4FPS观测。

## 主表与评测协议

T5共21图像任务/64750次generation。计数Count94.30/PixMo73.03较强；MMMU41.67低于BAGEL55.30/Tuna2 50.70，Doc90.42/Info63.67低于Qwen2.5VL94.90/81.70，不能称全面保持细字理解。完整本作21列在[L108](../reviews/L108.md)。MME1809.54为原尺度总分。

T6 video70.53/57.33/59.61/40.41，主评sparse≤96帧；VideoMME无字幕，57.33低于LLaVAOV2 71.90/Qwen71.40，MV70.53低于PLM77.10。各baseline保留自身协议，所列UMM更高不构成等预算架构归因。

T7 GenEval553prompt×4，原.77/改写.83，BAGEL-long改写让single .99→.98、twoobj .95持平，其他子项提高；仍低于BAGEL†.88/TUNA.90。DPG1065prompt×4得85.74，低于TUNA86.76/Tuna2 86.54/Showo86.14，Other92.62较高。†只表示报告了改写，缺†不能证明其他论文没用。

T8/9完整16项VBench分两表，本作QS84.10/SS79.80/Total83.24，低于TUNA84.32/83.04/84.06与Lance85.14/84.96/85.11。subject95.05/dynamic64.44低于TUNA95.99/69.39，imaging67.63/temporalstyle25.84/overallconsistency27.90较所列UMM强。使用GPT-enhanced prompts；不能将主表结果等同原prompt、严格文字生成或真实执行正确性。

## 数据、训练、发布制品

理解FineVision、VideoChat-Flash、LLaVA-Video-178K；生成称public real/synthetic并引[52]ViPE（2508.10934）。该引用没有补齐实际语料清单；主生成来源/各源规模与筛选、text-only来源、总曝光仍未详。F6标MidJourney配方，不可扩成全部主数据。

六stage依次150K/200K/100K/20K/15K/20K，前二lr1e-4后2e-5、constant/warm1K、AdamW(.9,.95,1e-8)/wd0/clip.2。两joint训两专家、Gen只gen、三Und只und；seq前三60K后三80K。生成256→512，理解图像256→native/video224→448。CE/image/video loss依次1:10:0、0:10:30、1:0:0三stage、1:10:30。

每步examples按text/I2T/T2I/V2T/T2V为.5:1:4:0:0、0:0:1:0:3、1:10:0:0:0、1:5:0:5:0两stage、1:5:11:5:33；与loss权重区分。shift为sqrt(HW/256²)。主训练globalbatch、硬件型号/GPU时、主表完整NFE/CFG未齐。F7另15K/FusedAdam(.9,.99,1e-8)、lr2e-5、八任务1:2:2:2:3:3:2:3、visual/textcap60K/32768。F7展示DPM50/shift10/textCFG6不能直接填为主表协议。

官方默认S8-F22-R05对应主表。S8-F18-R01另外10K 480p/720p微调、没有videoUnd，不能混作同一能力检查点。HF目录另有F19/F21，尚未独立审查。发布profile确认无显式t输入、unitGaussian、xpred/vloss、tmin.05、线性head；主模型选读已见真正videoUnd专用入口，不能因generation-only helper的异常提示断言整个模型不支持dense video。

四步toy训练每步一个任务、从现成F22开始、fresh AdamW/不存optimizerstate，文档称7×≥48GiB/约61GB FP32模型输出；这些是toy条件，无法代替完整六stage原训练。HF卡标NVIDIA非商业研究许可，GH主源码Apache2但文件保留各自notice；没有完成许可证法律文本审查，权重许可不能从代码许可继承。

## 可证伪实验与写作学习

相同上游/总参下分别控制样本曝光、视觉token和总FLOPs，交叉p×τ×head×CFG。加同模糊度平滑与无运动对照，联合边界谱、文字OCR/笔画拓扑、短事件和全采样延迟。F7加等15K旧任务继续训练、只增video监督/冻结专家对照，测理解/生成Pareto和多seed。F8按真正切换子集分层，在逐笔事件/逆序最小对照上分FPS×τ×预算，报告fallback占比；显式t/AdaLN与跨噪声/分辨率分布作补充。全部建议未运行，新颖性需进一步追引。

Introduction从双流管线负担到像素图像进展再收窄视频接口；Method按接口/序列/目标/阶段，F1–F8按问题、控制、图、有限takeaway组织。跨空间loss、步数/墙钟、异数据跨模型归因的限制值得学习。正文没有单独Limitations节，Conclusion承认专家参数分离/p64τ8待探索；官网另列实体合并、手部细节、物理交互失败。写作应把这些失败和F7退步、F8分层、数据/发布条件一起用于约束Claim。
