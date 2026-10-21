# EvoTok：残差深度、任务折中与公开训练协议

第一百一十八批完成[L102](../reviews/L102.md)固定v1核心三遍与五项书面记录。[结构化证据](../../data/evotok_residual_depth_and_training_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），227核心/230书面含未通过项，130条未确认核心（含资源）。没有新增目录、删除文件、下载权重或运行模型。

## 版本与任务

固定[2603.12108v1](https://arxiv.org/abs/2603.12108v1)，2026-03-12，完整16页。核心Abstract/§1–5、Eq1–11、T1–5全部行与F1–6图注已读；实际核PDF p5框架F2/Eq6–8、p7T1、p8T2、p10T3/4、p11F5、p12F6/T5。无附录，参考文献未逐篇追读。ECCV2026[官方接收列表](https://eccv.ecva.net/Conferences/2026/AcceptedPapers)查到同题同作者，页面注明preliminary pending publisher checks；正式出版全文和页码未定位，不能写成已核正式版本。

任务为静态重建、图像理解和文本生图。残差轨迹对应同一图像的表示深度，没有物理时间或真实绘制过程监督。共享tokenizer后分别训练理解和生成入口；尚不能用两张下游主表证明同一checkpoint联合训练的正协同。

## 方法与数据流

SigLIP2-large16-256初始化encoder，把256²图像映射为16×16位置；16级残差量化，每级独立32768×32码本。前4级累积向量经pixeldecoder重建，16级累积经3层semanticdecoder对齐冻结SigLIP2特征。shared指两个目标共享残差前缀路径，各层码本没有绑成一张表。T1的131072为4×32768像素码本槽位，完整16表名义524288槽位；每个分类头仍是32768类。

像素分支MSE/LPIPS/GAN，语义分支cosine，另有累积VQcommitment。Eq7的stopgrad使该项更新encoder，码本由代码中的EMA .99与restart更新；不能因公式未出现可导码本项断言码本未训练。两个STE分支向同encoder传梯度，并未证明梯度冲突在数学上消失。

理解将每位置16码之和解码成1024维语义特征，再经MLP/Qwen2.5-7B生成文字，LLM读256个聚合位置。生成则空间AR遍历256位置，depth head逐位置预测4个32768类码并累积为32维像素特征，再pixeldecoder出图；应计256×4次码预测与depthhead成本。公开head为6层、2560维、40heads，构造16个分类器但生成用前4个。理解/生成MLP输入模式不同，不能直接声称所有参数/检查点一致。

Tokenizer用CC12M+IN约13M；理解先LLaVA558K对齐再13M SFT，生成22M来自ImageNet-QwenImage/BLIP3oShort/OV1.5/ShareGPT4o/OpenGPT4o。13M只属于tokenizer训练口径，另有SigLIP/Qwen上游预训、教师特征和继承的合成数据。作者没有重新标注自身数据，不足以概括成全系统无蒸馏、无合成或只用13M。

## 全部主表和机制证据

| 证据 | 结果与适用范围 |
| --- | --- |
| T1重建 | IN256² rFID .43优于DualToken .52/TokenFlowL .63，UniTok .33更低；保留各表原值与数据/教师/码率差异 |
| T2理解 | SEED71.8/MMVet39.9/GQA61.8/AI2D76.2/RW62/MMMU45.9/MMB74.9/MME1895.1/MMEP1455.9。“7/9最好”限所列离散统一组，含SEED/MMB与Dual、GQA与QLIP三项并列；MMVet低于Dual40.5、MMEP低于TokLIP1488.4；连续ShareGPT4V GQA63.3/MME1943.8和ILLUME MMB75.1更高。MMMU对Dual只多.1，无CI |
| T3生成 | GenAI Basic .87较高，Advanced .66低于UniTok .67；GenEval .75与Dual同，count .44低于DALLE3 .47及ILLUME/TokenFlow .45。Position .69/colorattr .62优势限列出的基线；作者用GPT4o改写prompt，未齐所有方法改写与采样预算 |
| T4轨迹 | 4/4→4/16使rFID .66→.55、PSNR22.96→23.60、SSIM .76→.77，SEED62.7→67.1/GQA58→61.3/MME1668.9→1793.5，GenAI .70/.59→.75/.62、GenEval .64→.67；反向16/4重建 .44/24.39/.79更好，GenEval .60较差。码数、容量与生成head深度同时变化，不能纯归因顺序 |
| T5替代 | 同码 .66、异层 .59、分支 .68、本法 .55，仅有rFID，尚未证明理解/生成也优于这些结构；T4 .55与主表 .43的训练协议差异未交代 |
| F5/6 | rFID到depth4最低后略升约.5，pixel相似度趋平而semantic相似度继续升；双轴数值不直接比。tSNE与挑选簇样例支持解释性观察，教师/decoder/监督位置和取样选择会影响曲线，不能证明后12级纯语义或自然因果演化 |

## 实验与代码条件

正文tokenizer500K步/global256/lr1e-4、16GPU型号未说明，生成CFG7.5。实际MLLM的混合比例、完整步数、总卡时、多seed/CI及prompt改写预算未齐。主文未单列Limitations。

固定[GitHub147b1b2](https://github.com/VisionXLab/EvoTok/tree/147b1b2aaac32bb28c5eb246e2a4a04c3e80041c)，90项树与README、tokenizer/reconstruction/四个MLLM训练脚本和数据入口已读。选读encoder/quantizer/loss/optimizer，以及VQ tower、RQhead和Qwen实际自定义图像路径；attention、pixeldecoder和数据加载未全部逐行读。

公开tokenizer用bf16、32768×32、VQEMA warm2K、Adam β.9/.95。parser默认wd .05但Adam调用未传此参数，不把.05记成实际weight decay。LPIPS1、GAN .5从20K开始，semantic除cosine另加fold4；commitment按深度mean，论文Eq7为sum，尺度对应需补核。MLLM示例1epoch/perGPU8/accum1、lr1e-3对齐→2e-5 SFT、wd0、cos/warm .03、context2048/ZeRO2；外部worldsize没有确定所有主实验GPU数。

理解SFT示例665K与主表13M不同，生成pre/SFT均指558K_generation_debug，与22M主实验不同。重建脚本dataset=coco、图像路径LLaVA，不能直接作IN主表协议。README/树未给对应权重下载链接，本次HF同名搜索未找到相关作者制品；这不证明其他渠道不存在。没有下载权重或执行代码，入口差异也不能直接判定论文结果失效。

## 假设、研究设计与写作学习

可检验假设为：较短残差前缀足够重建时，额外残差改善语义对齐，并形成理解/重建/生成的有利折中。需要固定teacher、初始化、总bits/参数、数据曝光和FLOPs，扫描4/4、4/16、16/4及替代分支，补三任务Pareto与多seed。F5另做监督位置、随机teacher/冻结probe与模块干预，公开聚类取样。统一tokenizer下分别SFT和同checkpoint联合SFT应分别比较。

对当前研究，还须单独验证细笔/多语言OCR、真实接触/抬笔/墨迹GT和视频顺序。早4级丢失细笔时，后12级语义增强不能自动修复生成细节。建议均未运行，新颖性需继续追引。

Introduction以同码冲突和过度分离引出前缀折中，Method按tokenizer/理解/生成区分I/O，T4正反轨迹与T5替代结构的组织值得学习。Claim须保留并列、Advanced/计数/重建退步、教师预训与训练示例差异；Limitations应明确联合checkpoint证据、成本/方差、因果解释和文字视频未测范围。
