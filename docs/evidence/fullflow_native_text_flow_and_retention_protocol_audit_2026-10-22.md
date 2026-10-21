# FullFlow：原生文本插入、图像先验保留与预算审查

第一百二十九批完成[L115](../reviews/L115.md)明确范围核心三遍及五项书面记录。[结构化证据](../../data/fullflow_native_text_flow_and_retention_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），238核心/241书面含未通过项；未确认核心92论文／研究+27资源。资源另按制品协议审查。没有新增目录、删除文件、下载权重、执行模型或独立复现。

来源：[arXiv v1](https://arxiv.org/abs/2605.20316v1)、[完整36页PDF](https://arxiv.org/pdf/2605.20316v1)、[项目页](https://ericbill21.github.io/fullflow/)、[GH网页固定9a04534](https://github.com/ericbill21/fullflow/tree/9a04534fa45c56347c7eafc025c41446742ccad8)。[关联硕士论文DOI](https://doi.org/10.3929/ethz-c-000800257)仅定位未读；不能用其可能存在的细节补本篇空缺。

## 研究问题与具体动机

在保留SD3-M/FLUX.1-dev既有图像先验的条件下，以少量可训练参数给文生图flow骨干增加图像描述、图文联合生成和适配后VQA。研究对象是静态图像与自然语言序列，未生成连续视频、规范笔顺或书写动作；文本token插入与物理笔画事件不同。

mask文本难直接复用冻结的多tokenizer编码器；增加文本预测可能改变图像先验，MSE与分类损失梯度尺度不同，纯端点任务训练不覆盖共同带噪状态。作者选择删除/插入保留可解码token串、双独立时间及teacher约束。冻结CLIP可接受删除后的串，并不证明这些串语法通顺或等于原语义；也没有证明所有mask方法都无法低成本适配。

## 输入输出、框架与模型

保留图像连续RF latent，文本采用T5空间删除到EOS、反向按位置插入的Edit Flow，共享MM-DiT加独立t/τ调制、LoRA及计数/身份头；删除串解码再重分词喂冻结CLIP。用共享参数梯度比EMA平衡文本，LoRA关闭的同骨干作同噪teacher维持图像先验；先二维独立噪声训练再交替clean细化。双时间允许条件生成与联合轨迹、固定题目仅生成答案。不是新增外部AR语言decoder；这里decoder-free仅指文本生成接口，图像仍需VAE。

RGB→冻结VAE latent、文字→T5删除子序列→T5编码及decode/re-tokenize后的CLIP编码→共享LoRA MM-DiT分别受图像t与文本τ调制→图像velocity和文本插入计数/类别；Euler/插入过程推进至图像latent与完整字符串→VAE RGB/文本。固定τ=1文生图，固定t=1图生文；联合τ=t^(2^p)，p<0文本先、p>0图像先、p=0对角。实际看p4/5/6/7/8/9/17/19/20/21/22/24/27/28/34十五页。任意单调路径可用于采样不等于每条路径质量相同或近似训练场具有严格一致联合分布。

冻结SD3/FLUX骨干、T5/CLIP encoders；MM-DiT所有transformer_blocks线性层LoRA r32/alpha32/dropout.05/no bias，并直接训练新文本头、text AdaLN与τ处理器；SD3约136.1M可训、FLUX约298M。冻结参数仍占前向/显存，不能把136M当全系统大小。x_t=(1−t)noise+t*data，t0noise/1clean；文本每个非EOS token以τ保留，τ0EOS-only/1完整，反向插入是离散CTMC，不是标准连续高斯文本噪声。Eq2.8 Poisson count NLL加被删token CE；实际B6加BCE非零门π与条件Poisson，π称P(n>0)，但若门开后用未截断Poisson仍可抽0，是否截断/夹正及具体离散采样代码未给，保留待核。

## 数据、评价与实验条件

LAION-COCO-Aesthetic过滤双向长宽比<1.4，约280K图文，Moondream描述；预处理bicubic256²/center crop、VAE shift/scale，B1明确16×32×32 latent预存，训练不加载VAE。5K留出Moondream单参考caption评估；COCO人写多参考另评，二者CIDEr不能混。文生图nominal1900 prompts=COCO长短三桶各300+T2IComp八类各100+DrawBenchupsampled200，去重后精确数量未给，固定同prompts/seeds/scheduler/steps/CFG。VQA另100K步VQAv2；未见跨文字体系/严格笔顺视频/书写动作监督。

FID/CMMD相对冻结基础SD3生成图像分布，测prior retention，未相对真实图像分布；FID低不能直接称真实质量或文字正确性高。CMMD用CLIP-L14-336，图文CLIPscore用ViT-B32。CIDEr/BERTScore-F1对5K Moondream参考，另COCO人写参考CIDEr；RoBERTalarge baseline-rescaled BERTScore允许负值。T5 token union为词法重叠，GPT2 PPL为流畅性，均非事实性/OCR/规范笔画。VQAv2/VizWiz/OKVQA官方accuracy，吞吐steps/s为训练而非推理；表6GPUh与显存总量/每卡口径需分清。

T4重实现DualDiff-LoRA共享SD3/r32/相同数据optimizer、136.8M vs136.1M，但同时改mask/insert、encoder可训/冻结、图像RF/TeacherSN及噪声调度，多因素比较不能唯一归因接口。T3/10异预训容量分辨率的CM3Leon/Chameleon/LWM/ShowO/Transfusion/DualDiff及专用VLM。原文把JanusPro说成扩JanusFlow、T10把原ShowO图像标FM，与已核U04 JanusPro扩原Janus、U06原ShowO图像mask-MTP不一致，不沿用标签；ShowO2连续flow另列。OneFlow/EditFlows/DualDiffusion作为追引，未完成独立三遍。

SD3 2RTXA5000×24GB/DDP-NCCL/BF16、optimizerFP32/no checkpoint，globalbatch10(5/GPU)、T5max77、seed42；AdamW(.9,.999,1e-8)、constantlr/warm5K/clip2、EMAtrainable.9995。B4 LoRA/时间处理器lr1e-4 wd0，新heads/AdaLN5e-4 wd.01；T5却把head并到1e-4组、5e-4标Baseparameter，分组名称不一致，不能推全骨干解冻。梯度比每100步取micro3、EMA.99且先乘5，另wtxt.05再乘自适应λ，不能仅λ≈.04视作完整损失权重。主生产100K独立+50K交替=150K，收敛分析200K。采样28FlowMatchEuler步、文本shift1/topk1/temp.7、主结果CFG1；VQA另100K步wimg0/8步；FLUX3A5000手工分片、40K+20K/60K步36h/max128，非同两卡预算。

## 十张表、消融与结论边界

T1 100K LoRA-only CIDEr40.1、refiner-only0、LoRA+refiner19.9，同参预算不证明所有refiner无用；200K全部encoder对仅T5 CMMD.11<.50/FID34.25<44.55/CIDEr65.42>63.96，CLIP.25<.26，非所有指标改善。T2 FM→TeacherSN FID63.46→30.38/CMMD.579→.084，TeacherCT39.49/.310；只证对基础模型分布更接近，没有同表caption质量取舍。T4 DD62.65/.870/CIDEr2.0/BERT−.27，own-step29.32/.021/13.4/.02，own-time31.57/.121/99.4/.44；step反而更保先验，不能把time99.4配step显著更低FID。T9另报DD2.06/−.28、step13.16/.03、time107.11/.47，与T4差异未解释，不拼成一组结果。

T8 @200K val CIDEr纯ind65.43、纯ac96.97；switch75K111.80/100K107.63/125K108.76/150K84.68/175K107.11。150K切换低于96.97，反驳正文全部五种胜pureac；CI是5K样本不含训练seed不确定性，五实验是五切换时刻。T3/10 ownCOCO54.93/VQA56.5/Viz50.7/OK23.3；Viz优表内统一模型但专用InternVL2 62.9更高，VQA低ShowO64.7/69.4、OK低Dual28.5/25.3，不能称所有理解更优。F12γ1.2 CIDEr107.1→110、长度34.4→33.8而参考35.9，原文称更近与这些均值不符；γ4长57.8/CIDEr15表明强CFG退步。联合F6约1K样本对角CLIP较好，F21图像先常到约77token上限；长度更长不保证描述更准确。FLUX仅转移定性示例/算力，未单列完整FLUX主指标。

## 理论、预算和发布制品的待澄清处

T5称两方法两卡/200K，T6基线4卡24h，不能据wallclock称等GPU预算；baseline .25step/s与200K/24h不相容，缺各checkpoint实际步数。T6 SD3 18runs×2×28h=1008但行报864；列行864+108+96=1068而总报1212，总数与1008+108+96一致，需作者澄清。38GB vs84GB是峰显存总口径未说明，1.96/.25≈7.84为训练吞吐，非推理加速。E1证明中(n+n−2n)漏σ，应n+n−2nσ；最终8(1−σ)/n在假设下成立。E/F9用4×32²=4096与B1实际16×32²不一致；MSE/CE输出梯度界不直接推出共享参数梯度25倍，仍需Jacobian与尺度条件。项目repo固定9a04534完整192项只有网页/静态制品、无py/yaml/sh/权重；README模板，项目Code soon链作者主页，不能称模型训练代码已开源。

## 优势条件、假设验证与写作学习

已有高质RF图像先验、冻结多encoder接纳删除子串、图像teacher目标与期望分布相近、少量caption数据足够时，可低成本增加文本端而维持基础生成分布。二维预训练可能让后续端点适配更快，但T8反例/无配对seed和各切换预算限制普适性。TeacherSN约束的是base行为，也可能继承基础缺陷、约束新域适配；少可训参数并不保证总内存/全预训成本少。输出梯度理论只解释一种潜在尺度来源，自适应EMA合理性仍要受控实验，不能从保先验FID推出新文字/细笔/视频优势。

先取得同一checkpoint映射和完整训练代码，固定原SD3/data/teacher/seed/总GPUh，对deletevs合法mask桥、encoder冻/训、SN/CT/RF、单固定权重/自适应、ind/ac/两阶段做因子消融。报告base与real-reference FID分别、caption人参考/伪参考各指标、人工事实性/物体计数/静态OCR和稀有script；不同阶段多训练seed而非只5K样本CI。校正lr分组/实际步数、所有可训及冻结参数总资源，分开训练吞吐和完整28步含编码/VAE推理延迟；对比同GPUh及同steps两种协议。联合路径固定seed评长度截断、图文幻觉与路径一致性，限制与不限制77长度；非零计数截断协议独立核清。若扩书写须新增真实连续帧/事件监督及笔顺合规、事件完整率、速度/可观测性指标，先与已有绘画/书法和SVG强基线比。全部为实验设计，未执行。

Intro将低资源适配分成tokenizer兼容、梯度平衡与prior保留，再以A1–A4分别实验，是可学习的组织方式；先界定原模型能力与任务输入输出，再限制结论有助避免把静态文本生成当笔顺。主表对齐step与wallclock是有用比较视角，但硬件/各实际步数、T4/T9数值、T5/B4分组、T6算术和T8反例须明示。E1/E2的理想化假设、输出到参数梯度之间缺条件，以及CFG长度原文矛盾应写入Limitations，不能将定理当原算法全部正确性保证。

## 实际阅读范围

arxivv1完整36页PDF，Abstract/§1–6及Eq2.1–2.9/3.1–3.5，AppA–H全部研究文字/B1–11/C–G/E1E2证明与H1CFG公式，AppI引言/I1及全T1–10/F1–26图注；实际p4/5/6/7/8/9/17/19/20/21/22/24/27/28/34十五页。未逐例看全部qual图或逐篇参考文献。项目正文/recipe/链接及GH9a04534完整192树、README全文已核，网页不含原模型训练/推理代码；关联thesis仅定位未读，未下载权重/数据、执行模型或独立复现。

## 关键公式在算法中的作用

图像时间从噪声0走向数据1，x_t=(1−t)x_0+t x_1，标准RF目标是x_1−x_0。文本时间τ是每个非EOS token的保留概率，因而删除后的T5子序列长度可变。Poisson项λ−n logλ监督每个可插入位置的遗漏数量，交叉熵监督遗漏token类别；B6另加非零门来处理多数位置数量为0的稀疏监督。与物理书写过程没有一一映射，也没有从子词顺序到汉字笔顺的保证。

自适应权重的核心量为共享可训练参数上的图像梯度范数除以文本梯度范数，再以EMA更新。Eq3.4文字讲λ约.04，T5还给ratio scale5与外部text weight.05，两处必须共同记录；没有原训练代码时不能擅定完整有效权重或优化器分组。TeacherSN是在相同带噪图像与删除文本条件下匹配LoRA关闭的基础骨干velocity；它约束基础模型行为，仍需额外teacher前向，且可能限制新域偏离旧先验。

联合路径为τ=t^(2^p)，指数内还包含2^p；PDFp9和p34均核看。p=0得到τ=t，p负时文本较早完成，p正时图像较早完成。强路径依赖、77token截断与图文幻觉都需评估，选择路径本身不构成高质量联合分布的证明。

E1理想Gaussian下mean-MSE输出梯度平方期望8(1−σ)/n，E2 one-hot CE logits梯度平方期望处于 n/(n−1)(1−σ)^2 与2(1−σ)之间。E1中间一行漏写σ，但最终表达式可在其假设下推得。两界作用于不同输出空间，经链式法则映射到共享参数还依赖各自Jacobian，因此不能用它们直接证明实测25倍比例或所有骨干都必须采用该EMA。

## 需要读者保留的证据冲突

| 位置 | 原始证据 | 可支持的判断／待核 |
| --- | --- | --- |
| T4 vs T9 | time CIDEr99.4/BERT.44 vs107.11/.47 | checkpoint或协议对应未解释，分别保留 |
| A4/H3 vs T8 | 声称五种切换全优；150K切换84.68低于纯ac96.97 | 两阶段可有效，但本组不能证明全部切换均优 |
| T5 vs T6 | 双方两卡；实际baseline四卡24h | wallclock对齐不等GPUh对齐 |
| T6 SD3 | 18×2×28=1008，行写864；总写1212 | 行乘法与列求和不一致，不能静默修正 |
| B4 vs T5 | 新head/AdaLN5e-4；表head1e-4 | 需参数组原配置，不能推全骨干解冻 |
| E/F9 vs B1 | 4×32²=4096；SD3实际16×32² | 理论例子维度与实验latent不一致 |
| F12 | 均值34.4→33.8，参考35.9，称更近 | 按所列均值绝对距离1.5→2.1，文字解释不成立 |
| T10/§4 | 原ShowO标FM、JanusPro接JanusFlow | 按已核[U06](../reviews/U06.md)/[U04](../reviews/U04.md)修正来源脉络 |

## 无独立模型制品时如何审查

作者GitHub账户有同名fullflow仓库，但默认分支gh-pages。固定9a04534完整192项树只有README、index.html及static资源；README仍是项目页模板，在该树未见原模型py/yaml/sh或权重。网页Code soon指向作者主页。此证据仅限定所核版本和来源，不能宣称互联网任何位置都不存在代码；网页许可也不能移作未来模型/训练数据的许可。

本批把网页、论文与可训练模型制品分开核查，避免将GitHub链接的存在等同于实现可复现。OneFlow、Edit Flows、Dual Diffusion及关联硕士论文进入追引队列，先按arXiv/DOI去重；此处引用不表示它们已经完成独立深读。

## 与文字、绘画和视频问题的联系

该方法提供连续图像与离散变长文本的联合建模思路，说明有限可训练参数可以扩展静态图文接口。28步采样、静态低分辨率和伪caption分布的证据，不支持其已解决中文文字视频、严格笔顺、真实绘画过程或多语言书写执行。图像先验保留FID、caption流畅性和实际文字正确性必须分别评估。

可迁移的研究思路是先确定模态表示和预训练接口兼容，再设计可观测的冲突及保留指标。若扩到书写，需明确保留哪种图像/视频先验、监督哪类事件，并设计对现有书法/绘画方法和规则渲染的等预算对照。不能把论文的删除/插入过程直接解释成笔画生成。
