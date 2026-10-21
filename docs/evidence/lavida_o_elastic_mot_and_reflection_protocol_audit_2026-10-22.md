# LaViDa-O：弹性MoT、分层采样和反思的适用条件

第一百二十五批完成[L111](../reviews/L111.md)正式核心三遍与五项书面记录。[结构化证据](../../data/lavida_o_elastic_mot_and_reflection_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），234核心/237书面含未通过项；123条未确认核心，其中96论文／研究、27资源。资源依制品协议另审，不能用缺论文三遍认定未审。本批未新增目录、删除文件、下载权重或运行模型。

## 来源和三句话定位

以[ICLR2026正式会议记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/52d7e1f59be8a140bd5c3b0b5b8bdee2-Abstract-Conference.html)和[33页PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/52d7e1f59be8a140bd5c3b0b5b8bdee2-Paper-Conference.pdf)为准。读Abstract/§1–5、Eq1–7/Alg1–3/T1–16、F1–16图注、AppA1–7/B1–8/C–F全部研究文字；实际p5/6/8/9/17/18/19/25/27/28/29/30十二页。未逐图看全部展示或逐篇参考文献。正式身份已核，GH旧标题与HF所引arxivv2分别保留版本信息。

成本、输出模态路由、图像并行揭示质量，以及理解如何帮助生成，是论文聚焦的困难。作者用较小生成分支/部分层jointattention、动态exp、空间分层采样，以及框规划和反思扩展理解型LaViDa。基础GenEval.77，经规划.85/反思.89，但有额外时间、部分任务退步及原文/发布协议缺项。

这是静态图像理解、REC定位、1024²生成和指令编辑。空间揭示token的顺序服务采样，不是书写事件标签；框布局也不能证明规范笔顺或真实执行。作者承认VQ不能忠实重建小字，未专门加入文字渲染数据，因而不能据其UMM性能推断文字书写视频能力。

## 输入、模块、输出及公式

输入图像经SigLIP-SO400M-p14-384得到语义Ci，编辑和历史图另经Meissonic VQ得到低层Cv，拼接prompt Cp与masked目标Xt。双分支Transformer输出clean文字/图像码；后者解压、VQdecoder还原RGB。相同图像既有语义又有VQ条件，不等于已训练统一视觉tokenizer。

理解分支8B/hidden4096/FFN12288，生成2.4B/hidden2048/FFN8192，QKV接共同4096维attention空间；生成权重从理解权重截断初始化。论文称生成“from scratch”须理解为没有继承成熟图像生成预训练，不能写成所有参数随机初始化。32层前16joint后16模态内，理解激活8B、T2I激活4+2.4B、交错激活8+2.4B。HF safetensors元数据11,094,351,587参数，双分支规模、可训量、激活量与全制品参数需分别报告。

VQ有8192码、空间stride16，1024²图像先有64²=4096原VQ码。源码2×2 stride2卷积将嵌入压成32²=1024 Transformer位置；输出用2×2转置卷积恢复4096位置再预测码。原码数与压缩位置数不同，附录“1024 VQ tokens”不宜直接当原tokenizer只有1024码。源图编辑也用低层VQ条件，保留细节能力仍受codec重建上限与采样学习影响。

正向mask路径为\(q(X_t\mid X_0)=\mathrm{Cat}((1-t)X_0+tM)\)，t0 clean、t1全mask。网络按位置预测clean目标，用maskedCE；理论Eq1为1/t加权，发布代码采用masked token平均CE及分别文本/图像loss相加。分母归一与时间权重需要一起核，看到代码无显式1/t不足以直接判实现错误。默认反向中已揭示位置保留，未揭示位置按模型分布/规则选择。

交错任务高t的整图折成文字exp，反向揭示exp后插入预定分辨率的生成mask槽；理解/裸T2I不启用。可变的是模态位置与展开，初始文字长度、图像分辨率仍预设，不能称任意长度无条件生成。

**正式Eq7疑似区间颠倒。** p18正文写t<texp时短序列，Eq7也给低t折叠目标X0′；p19 Fig7画高t折叠并以X0′监督、低t保留完整X0，与t0clean/t1mask定义一致。本笔记按图解释正确工作流程，同时保留原式冲突。未定位完整发布t_exp训练路径，尚不能靠代码消除这项差异。

## 分层采样、坐标和协同机制

分层采样先在2×2四区各揭示一个位置，再递归4×4等，对已有样本的子区不重复新增，从而前4^d个位置覆盖每个子区。公开pmj算法与该定义吻合，预测接口在stratified模式默认固定order seed42。被揭示的是静态图像格点，不能转译成真实绘画轨迹。空间相关性是设计动机，论文没有证明条件独立已恢复；分层是采样规则改变，需要以任务结果和预算验证。

Universal text conditioning将原尺寸、crop、aesthetic/HPS、亮度/对比度写成文本键值，训练随机丢条件、推理可选。它让生成分布偏向特定score，不等于相同图像内容下所有质量维度提高。F13有300responses，图估约70%偏好有条件、5%平、25%无条件；未给精确表、评价人数/独立图对数/CI，不制造精确胜率。

定位先pad方图、按D=max(H,W)归一化并量化到0…1024，共1025符号，每框固定四token，可一步并行多个框。REC的P@IoU.5是表达对应框命中，不能当检测mAP、密集多物体追踪或完整身份推理。

规划先预测对象/bbox再生成，编辑先定位目标区。反思每轮规划、生成、同模型文字反馈，错误则重生成；最多N图、ctx8192，最多保留三轮历史。文本反馈有模型先验，可能自评错停；当前实验没有与等时间无反馈重采样/BestN充分隔离。

## 主表和全部消融的结论边界

| 证据 | 实际结果及限制 |
| --- | --- |
| T2理解 | 对原LaViDa十一项均升，MathVista44.8→56.9，作者明确伴数据扩充；不能单归生成协同。MMMU45.1/MMEP1431低Dimple45.2/1514，多个任务低Qwen/Intern/BAGEL |
| T3生成 | GenEval.77→规划.85→反思.89，基础低BAGEL.82；DPG81.8/82.9/83.2全低FLUX84/SD3 84.1。基础MJHQ30KFID6.68优所列FLUX10.15，但该FID未用规划/反思 |
| T4ground | 4step对Intern八split6升1平1降，Refval92.3<92.5；1step仅2升1平5降。对Qwen更强不能写成对全部基线每split全优 |
| T5/T15编辑 | 3.71→3.80，低GPT4o4.20、与QwenVL+Flux3.80持平；replace/remove4.40/4.05高GPT4o4.35/3.66，但background−.06/style−.07。局部规划不普遍改善全局编辑 |
| T8分支宽度 | 同50K/globalb1024，2B .57/63.1/3.67s，8B .55/58.6/11.64s，约3.17倍每步速度；作者承认大模型需更多优化，不代表等终质量总算力优势 |
| T9 joint层 | M16/24/32的stage3 GenEval.89/.81/.85，DPG83.2/83/83.2。全部从M16预训点再训50K，改层带初始化分布影响，尚不能唯一归后层干扰。B2称固定gen4B、T8/9部分latency对应不同设置的关系待核 |
| F12初始化 | 截断初始化前20K validation loss低于随机；继承理解预训，不是从零总成本比较 |
| T10 sampler | 同64steps MJHQ30KFID：stratified6.68、Halton7.38、uniform8.22、confidence11.42；支持所测图像分布/预算，不证明所有领域最优 |
| T11 scheduler | 动态ground:und 3:1→1:3提升多个新旧任务；MME436低固定1:3的449，不能称无遗忘且全维度最好 |
| T12ground监督 | GenEval.74→.77/ImgEdit3.60→3.71，但DPG82→81.8；数据曝光/替补未严控时，不能由三列推出普遍正迁移 |
| T13planning/reflection | planning位置.65→.84，reflection到.89；计数.71→.75→.85，须附额外候选/规划/反馈成本 |
| T14跨类别 | 2D.388→.390、3D.414→.442、texture.613→.715；bbox的2D几何可影响视觉大小线索，不证明真实3D执行或空间物理正确 |
| T16推理扩展 | N1/2/4/8/12/16/20分数.848/.864/.875/.882/.890/.886/.886，延迟27.2/32.6/39.3/47.1/53.4/58.3/62.2s。最高所报.89有约53.4s条件，后续更多轮未改善，无CI/多seed不能断言差异显著 |
| F5/F14速度 | ground对Qwen最多6.8倍为特定步数/精度点；MathVista用FastDLLM阈值调速、max256tokens，较Qwen更快但更低accuracy。不能称所有任务质量/速度均占优 |

所有表分数是作者报告，跨模型继承预训、数据、参数、prompt与采样协议不同。BAGEL在T2的AR分组仅能对应文字侧，视觉连续flow仍应按[C01](../reviews/C01.md)解释。没有文字exactmatch、严格笔画事件或真实执行对照。

## 数据、训练与发布实际核查

正式A类200M图来自过滤LAION/COYO/SA1B/JourneyDB/BLIP3o/ShareGPT4o，含VLM重描述和合成teacher图；B理解、C GranD/RefCOCO、D指令编辑、E GroundingDinoL布局标注和ReflectDiT/ReflectionFlow。公共来源不代表无teacher。发布stage3yaml还列Echo4o/OmniEdit/HQEdit/UltraEdit等，论文列表与实际版本需逐项映射。作者训练readme明确原parquet含私有S3地址而未提供，不能声称200M原训练混合已完整下载可复现。

T7三stage80K/400K/100K、lr5e-6/1e-4/2e-5、AdamW(.99,.999)，可训8/2.4/10.4B。stage2生成256→512→1024，stage3为1024；语义encoder1/3可训、2不装，VQ仅Loaded未标可训。64A100/34.2天约53K GPUh，主globalbatch/每分辨率子stage分配仍未齐。

[GH固定e3a80df4](https://github.com/adobe-research/LaVida-O/tree/e3a80df47a4c2b433a4d26ac4918b95ab083f392)完整1987树，README/训练文档、base+四stage入口、evalshell全文；数据yaml和模型/采样指定代码已选读，具体范围见L111。[HF固定8e805608](https://huggingface.co/jacklishufan/LaViDa-O-v1.0/tree/8e80560856f2ad6ea6ee711e885cdd0249290977)卡/config/VQconfig与index键摘要已核，未下载权重。Adobe Research许可标识已核，法律条文未逐条审。

公开GenEval/DPG shell64steps/CFG4.5/shift7/1024/score6.711、temperature5→.2，GenEval加realistic4k前缀，num_samples1。shell指向的eval_hd.yaml在固定树中缺失，DPG还用作者绝对路径；主函数默认confidence_policy=mmada、yaml可能覆盖，不能未经配置核明就声称默认一定stratified，更不能把这些旗标自动补成全部正式主表条件。原样启动未执行。

stage1/2/3脚本含作者本地路径、debug_dataset与部分不同LR/steps；可能是示例或分阶段继续训练设置，现有材料不足以恢复正式T7全时间线。stage1yaml的ground/und weights为100/100并注明手调，与论文动态scheduler不能简单视同。所读maskedforward分别噪化文字/图像，规划与反馈经显式model.generate和text_to_image调用；未定位完整自动exp训练/推理Alg1，既不声称实现已核，也不据此断言整个仓库绝无实现。

另有两个结构差异：源码用零起blocks[i]、split_tower=(layer_id>16)，按HF配置dual16的该构造路径会有17个joint/15个split，论文写16/16；仍待全加载override和运行核明。T6生成attnout表为[4096,2048]，所读源码使用共享4096×4096 attn_out、index有32份且无attn_out_vision，和简单独立2K输出投影叙述不同。没有凭这些差异推断论文已报分数不实。

## 学习研究思路与可证伪验证

问题定义把成本、mask路由、采样覆盖和任务协同分开，各有机制和实验。Method从接口到结构/路由再任务模块，A1–7补算法，B2–7逐设计给对照，组织清楚。Limitations将小字VQ瓶颈、合成编辑pixelshift、数学差距落实到可查来源。Claim仍需保留任务退步、额外推理预算与跨数据混杂，公式/表形状/发布配置的一致性也属于复核范围。

下一步建议：M×width全因子在同初始/样本/总FLOPs分别对齐，重训不同M的stage2再同stage3；sampler同NFE/CFG/seed并测文字/组合、明确4096码与1024位置。ground移除用等token/训练曝光替补并记录全部任务退步和CI；planning/reflection比较随机/Oracle框、无反馈等候选BestN、固定judge和等墙钟，分错→对/对→错。先测文字原图→VQ重建exactmatch/拓扑，确定可达上限，再考虑书写事件/合法顺序与固定终图逆序最小对照。均为未执行实验设计，仍需追引查新。

追引LaViDa原理解模型、Sparse-LaViDa（CVPR2026）、LaViDa-R1、Meissonic及Halton scheduler/Besnier2025，须按正式身份/ID去重后独立阅读，当前只核引用和官方资源入口，未计作已精读。
