# HYDRA-X：时间压缩、编辑交互与完整视频证据

第一百二十二批完成[L107](../reviews/L107.md)固定v1核心三遍与五项书面记录；另补[L103 HYDRA](../reviews/L103.md)的官方会场元数据，不重复增加验收。[结构化证据](../../data/hydrax_temporal_tokenization_and_editing_audit_2026-10-22.json)。357目录（330论文／研究、27资源），231核心/234书面含未通过项，126条未确认核心（含资源）。没有新增目录、删除文件、下载权重或运行模型。

## 来源、会场与阅读范围

固定[2606.13289v1](https://arxiv.org/abs/2606.13289v1)，2026-06-11，完整27页。Abstract/§1–7、Eq1–7、全部T1–13、AppA–G全文及AppH文字/全部F1–11图注已读。实际核PDF p4/5/6/7/8/9/17/19/20/21，p19 F5四例全部查看；H六页展示未逐图、参考文献未逐篇。

[NeurIPS2026官方目录](https://neurips.cc/Downloads/2026)及[HYDRA-X海报155676](https://neurips.cc/virtual/2026/poster/155676)核到标题、作者和接收/Poster身份，官方链接[OpenReview3mwm6O3FZt](https://openreview.net/forum?id=3mwm6O3FZt)，其API本次403，camera-ready/proceedings全文未对读。原[HYDRA海报149164](https://neurips.cc/virtual/2026/poster/149164)同样核到，修正原记录仅有作者仓库接收消息的边界；不把X和原作混为同一论文。

[作者主页](https://totalhuang.github.io/)与[HF论文页作者评论](https://huggingface.co/papers/2606.13289)补充任务定位。后者是论文页，不能作为实际模型卡/权重。原HYDRA README发布段列原模型/原tokenizer，尚不能视为X实现。所读来源未定位X可核运行代码/权重，不作全网不存在断言。

## 完整数据流及待核接口

SigLIP2初始化Gen-ViT→64维Generation-Semantic Bottleneck→Sem-ViT；3D RoPE、局部causal时间连接与两次2×时间patchify。输入3×(1+T)×H×W变成64×(1+T/4)×H/16×W/16，17帧对应5个latent时间位置。s0为首帧的空间patch块；不能写成整图1token。每层mask读当前和前一时间位置，堆叠层/压缩会扩大有效原帧感受野，不能称全模型仅看两原帧。

训练期Decompressor将压缩Sem时间维恢复：两次1×1conv扩通道再channel-to-time与transformer，对接SigLIP图像/InternVideo-Next-L视频教师，之后丢弃。图像anchor直接cos蒸馏，视频尾部经D蒸馏；纯图像去掉视频项。没有证明恢复了压缩前所有细节或唯一动作。

Qwen2.5-7B共享LLM，语言NTP和视觉latent flow，默认1:1。F4显示Gen后加噪再Sem，编辑Gen分别编码，只有Sem以source→noisy-target的causal路由交互；编辑不启Gen跨帧。Eq5的⊥表示模块中无交互边，不能读作统计独立。

§3称pixeldecoder仅tokenizer训练调用，而§6/AppA又描述对称ViT与27层重建decoder，主模型输出是latent flow。最终RGB需要解码映射，但生成期调用接口没有完整展开。笔记保留该疑点，等待代码/正式版本对应；不凭空移除decoder或继承原HYDRA推理默认。单ViT/7B分别指视觉编码设计与LLM骨干，系统另有decoder、训练期教师/Decompressor。

## 十三张表

| 表 | 核查结果和反例 |
| --- | --- |
| T1重建消融 | 三种mask均单步4×，仅Ours为tubelet+2×2。Ours IN31.73/.8936/.329、DAVIS27.97/.8307/11.19较强；单forward latency .25s慢于单步tubelet .17s，快于Full .49s。延迟用17×512²，重建指标256，非全生成计时；缺全mask×压缩交叉矩阵 |
| T2蒸馏 | 视频teacher配置MV45.4/VideoMME45/Gen72/Edit3.20，优于解压后图像teacher44.7/44.3/70.7/3.07；AI2D62.5<62.7、MME1501<1522。bidir六项均降，限1.5B/此配方；无蒸馏显著下降，不能称所有信息完全崩溃 |
| T3交互 | 同容量/配方STI ImgEdit2.8→3.2，ReconPSNR20.74→27.65，Gen70.51→71.97；VideoMME45同，其他小涨无CI。6.91dB支持该设置保真改善，未排除其他容量/监督方法；没有训练收敛曲线或walltime加速实测 |
| T4图像理解 | 九项86.5/2350/51.5/84.5/84/68.7/86.5/81.7/59.1，多数强于列出同级UMM，RW低于BLIP3o69；MMMU/OCR/Doc/Info低于专用QwenVL，不能称所有文本细节无损 |
| T5视频理解 | 59.1/60/59.5/30在列出的UMM较高，MV低于IXC69.1，VideoMME低于强专用/闭源。采帧、fps/上下文预算未完整匹配 |
| T6生成概览 | GenEval .88、WISE .56，17帧640×384 VBench QS83.97/SS81.57/Total83.49；较所列UMM高，不代表每个动作/时序指标均强，也不能推长视频 |
| T7编辑 | ImgEdit4.34，GEdit7.80/7.24/7.17。GPQ低于UniWorld7.43、Qwen7.86，GSC/GOver低于Qwen8/7.56；高总分仍需未改区/需改区分别评价 |
| T8训练 | 50K/200K/20K，global1024、256/512/1024，256/512/512GPU约10/96/24h，另tokenizer约24h。caption“256h GPUs”未提供硬件型号。stageII Edit比例0与文字加入2M编辑、stageIII VideoSFT比例0与文字1.2M LLaVA-Video的分类映射未解释 |
| T9重建 | †仅IN训练32.96/.905/.154，相对FLUX32.86/.917/.176的SSIM仍低；完整图视频版IN32.04/.898/.465，静态rFID也弱于AToken .209。DAVIS28.19/.835/11.61、UCF36.88/.967/3.11较强，存在图像/视频折中。†仍继承SigLIP预训，不能唯一归因结构 |
| T10 GenEval | 六项.99/.95/.83/.90/.84/.75；前作HYDRA†1/.97/.68/.91/.81/.80有四项更高，主表省略该行后的每列最强不能扩为完整表结论。†改写条件亦须匹配 |
| T11 WISE | 六项.53/.57/.72/.53/.64/.40；所列同级UMM较强，time低于FLUX .58。不是全部模型/任务普适优势 |
| T12编辑细项 | 4.49/4.27/4.04/4.41/4.38/4.30/4.77/3.43/4.32；style/action低于OmniGen2 4.81/4.68，replace/bg/hybrid等有专用模型更高 |
| T13 VBench | SC95.70/BC95.88/MS92.69/DD35.42/AQ63.73/IQ65.23均低于Showo2 97.28/96.78/98.25/40.83/65.15/67.06；OC96.52/MO76.68/HA99/C87.37/SR73.88/Scene69.74较强。列12具名子项+QS/SS，文字all14不能当完整标准独立子项；缺失维度/聚合协议需补 |

fs16对8是单空间轴缩放，二维token数相差4倍，实际码率还取决C/dtype/熵编码；不能把“twice compression”直接作完整表示存储/信息量结论。F5四个source-reconstruction样例显示局部保真改善，但identity重建协议未完整给出，不能代替所有实际编辑的指令成功率或证明独立编码理论上不可恢复。

## 数据、训练与复现边界

Tokenizer先IN1.2M/256，后256视频+256–2048图像混合，StageI300K/AdamWpeak2e-4；II冻结encoder仅27层decoder加GAN；III按latent通道统计μ/σ，冻结Gen/decoder仅训Sem。后两stage步数/混合语料来源/完整loss权重、μ与采样路径未齐；不从前作实现补作本作事实。

UMM I100M图文；II30M理解+30M生成（筛自I）+约2M编辑+10M视频；III6M LLaVA-OneVision/Pixmo、1.2M LLaVA-Video、10M筛图+6M合成和未给数编辑。阶段重用不能算独立样本。1.5B消融用20M图文、LLaVA1.5/LLaVA-Video/ImgEdit，不能替代7B所有结论。

T8比例按text/IC/IG/VC/VSFT/ISFT/edit为0:1:3:0:0:0:0、0:2:6:1:1:0:0、1:0:3:3:0:1:3。visionhead lr1e-4/5e-5/5e-5，Sem5e-5后LLM+Sem2e-5。未齐主模型采样NFE/CFG、视频FPS、多seedCI、全部optimizer参数、实际数据类别映射与正式版本解码接口；不能把原HYDRA的50/200步默认填入X。

## 对严格书写研究的含义及实验

局部时间冗余较强、短clip与图像先验能迁移时，tubelet/层级压缩可能形成较好质量成本折中；视频teacher有助动态语义，细字/文档却可能退步。17→5个时间位置和较低动态度表明，VBench总分不能支持严格笔画事件、抬笔或非汉字过程正确性。

补三mask×两patchify、等参数/FLOPs/充分训练的全因子和CI；图像/视频teacher×直采样/Decomp等成本对照。STI分别测identity重建、未改区保真、需改区指令，和扩大LLM/更长训练/损失等成本替代；GT目标只作训练监督，逐步核noisy-target到RGB的真实推理。报告完整NFE/CFG延迟。书写视频另做FPS×时间压缩、逆序/短事件最小对照、笔画拓扑/事件GT；建议均未运行，新颖性未定。

Introduction将图像到视频扩展拆为重建/语义，再引出编辑；Method逐项映射T1–3、附录完整细表值得学习。Claim需保留更慢的Ours、teacher图文退步、GenEval和动态度反例，first须限定定义并追查AToken/OmniTokenizer。作者AppE已承认规模、长视频与视频编辑未测，读者还需补真实采样、数据比例/解码接口和统计边界。
