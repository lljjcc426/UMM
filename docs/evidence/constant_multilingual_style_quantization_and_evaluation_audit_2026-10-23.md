# CONSTANT：多文字风格量化、扩散训练与评价协议

第一百四十九批完成[L183](../reviews/L183.md)明确范围核心三遍和五项书面验收。[结构化证据](../../data/constant_multilingual_style_quantization_and_evaluation_audit_2026-10-23.json)。357目录（330论文／研究、27资源），258核心/261书面含未通过项；未确认核心72论文／研究+27资源，资源另按制品审查。无目录新增、删除、数据/权重下载或模型执行。

来源：[WACV正式正文](https://openaccess.thecvf.com/content/WACV2026/papers/Le_CONSTANT_Towards_High-Quality_One-Shot_Handwriting_Generation_with_Patch_Contrastive_Enhancement_WACV_2026_paper.pdf)、[正式supp](https://openaccess.thecvf.com/content/WACV2026/supplemental/Le_CONSTANT_Towards_High-Quality_WACV_2026_supplemental.pdf)、[固定官方源码](https://github.com/duylebkHCM/CONSTANT/tree/cf31559c036b6f8d5ec64b20bff59809a66c8bfe)。

## 研究问题

一张参考手写图Xs+目标字符序列C→同风格静态文字图Xt，期望新词组合和未见写者泛化。one-shot限定推理参考数，训练使用多写者同作者参考/目标监督对及写者ID；没有一张图从零训练、书写笔顺/轨迹、写字视频、自由视频或理解—生成统一UMM。英语词/中文单字/越文词分别训练评估，不能称一个零样本跨语言共享checkpoint。

## 现有不足

单参考难区分稳定风格与偶然噪声，连续风格向量、固定高通特征可能丢墨色/局部细节；普通扩散噪声MSE不足以直接约束细部。作者用离散风格码本加连续旁路、同作者风格对比和同位置多尺度latent patch对比补足。该论证提供建模动机，未独立证明全部GAN不稳/全部高频方法丢颜色或每个token对应唯一可解释风格因子。

## 核心创新

SAQ以InceptionV3抽特征并VQ离散化，连续F与量化Fq拼接后AttentionPool融合；SCE同作者参考/目标正对、不同作者负对；LatentPCE把噪声预测恢复的z0与真实z0同坐标patch拉近、异坐标推远。单阶段训练以上模块，另提出ViHTGen越文数据。LDM/VQ/InfoNCE/CFG/DDIM已有基础，贡献是此手写条件组合与辅助目标；VAE和ImageNet特征已预训练，“单阶段”只指该阶段联合训练。

## 输入、核心模块、输出与公式

训练：目标Xt经预训练VAE→4通道z0，加随机t高斯噪声→zt；参考Xs经SAQ得到global供SCE和sequence供条件，C经三层字符Transformer；U-Net cross-attention接风格/内容，预测ε，噪声MSE为主loss。由预测ε和zt代数恢复z0_hat作LatentPCE，无须每次训练完整50步采样。推理：单参考+字符条件+高斯latent→CFG/DDIM50步→VAE解码静态图。Eq1 L=Ldenoise+.1(LPCE+LSCE+LSAQ)，Eq2最近码，Eq3 VQ/commit β.25，Eq4–5双向styleInfoNCE，Eq6–7双向多尺度patchInfoNCE；sg控制梯度而非额外标签。

## 结构

补充E：VAE空间8倍压缩，z∈R4×W/8×H/8；轻量U-Net ResNet+SpatialTransformer，隐藏512/4heads，参考WordStylist减ResNet块。Inception到Mixed6e输出768，码本K1024(IAM)/2048(IMGUR/IIIT)，F+Fq通道1536，AttentionPool/线性→512；字符encoder3层D512。PCE三尺度2²/4²/8²，每尺度最多256patch，浅MLP→256维。当前配置U-Net1ResBlock、channel_mult[1,1]；预训练SD1.5 VAE与FID-Inception权重。SAQ连续旁路一直参与，离散token不构成唯一信息瓶颈或预定义倾斜/宽度语义。报告模型124M，统计是否含全部冻结VAE须另给清单。

## 数据和切分

IAM62857英语词/500写者，339train/161test；IMGUR5K135375词/5305写者；IIIT-English-Word>700K/1215写者。中文CASIA60写者×3755单字，官方DATASET指定comp_test_data，converter对writer文件无seed随机80/20；非CASIA官方标准train/test，split清单未提供。ViHTGen补充D：>300大学期末卷、223写者、>50K词图/4644词；GoogleCloudVision框+人工校验、VinTernVL-1B转录+人工纠正，42000train/>8000test；未写清按写者/试卷分割，不能宣称越文未见写者。IMGUR/IIIT完整切分/四场景词表和参考映射未齐。README总Drive称权重+数据，DATASET的ViHTGen直接Link仍空；Drive工具不可读，未核内部文件/数量/许可或下载。

## 指标和含义

FID图像分布、HWD(Handwriting Distance)风格特征距离、AccWid写者分类、WER生成数据的下游效用及人评。补充F.1明确WER：用IAM test对应生成图训练AttentionHTR200K步/b128，再测真实IAMtest；故T1 .22为该transfer协议WER，不能直接称生成图22%错词。生成器不因此已证训练泄漏，但OCR训练文本/写者与目标真实test同域条件须公开。AccWid：真实IAMtest按80/20训验ImageNet-ResNet18，再测生成对应图；非生成器训练集准确率。HWD源码按writer取VGG特征均值的欧氏距离再平均，非逐笔轨迹距离，docs称HandwritingDirectionDistance有误。FID/HWD不验证字符/笔画或时间，需独立OCR/拓扑。T1/T2数值量级不同，global/bywriter/样本子集实际映射未给，不能直接跨表比较。

## 对比

HiGAN/HiGAN+/One-DM为单参考；HWT/VATr15参考、DiffusionPen通常5参考，T1–2需标参考预算。IAM可用公开预训练，其余按源码重训；训练/调参预算未完全对齐。补充H中文/越文DiffusionPen特地改为one-shot重训，其54.07中文FID不可当标准5shot性能。基线LDM、逐步SAQ/SCE/PCE；全局cosine/LPIPS/patchL2辅助loss。没有笔顺/轨迹/视频模型对比。

## 实验条件

正式Pytorch1.12.1/800K迭代，IAMbatch64，IMGUR/IIIT128，单V10032GB，AdamW lr1e−4 β.9/.999，高64保比例，条件drop.2，DDIM50步CFG7.5。α.1/βcommit.25；SCE温度正文符号τ未给具体数，PCE公开τ.07。当前IAM/CASIA/ViHT配置b64、K1024、CFG6+rescaled_phi.7，IAM宽64–352、validFalse；启用loss_balancing，用梯度标准差比动态权重，不等正式Eq1固定.1。公开VAE冻结/Inception预训练，训练并非从零。人评28人/30OOV内容/840偏好票，真假辨1680回答；未给种子/区间、序列长度一致计时细节或原始回答。未执行训练/推理/评测。

## 主结果

T1 IAM HWD/FID/WER/AccWid：CONSTANT .74/10.20/.22/69.43%，One-DM1.05/15.97/.36/4.5%，HiGAN+.89/13.90/.56/55.20%，DiffusionPen1.04/18.94/.23/38.86；报告点估计而非显著性。T2 IV-S .96/89.88、OOV-S .94/96.13、IV-U1.61/112.03、OOV-U1.63/118.10(HWD/FID)；IV-U HWD差于DiffusionPen1.52，正文称两个未见风格场景均最好不符该表。T3IMGUR .99/11.48 vsOne1.22/18.94；T6中文.37/22.74 vs.48/22.97，越文.83/18.81 vs1.08/22.53。补充T2IIIT .73/10.22 vs1.22/17.74；补充T3单参考DiffPen中文.57/54.07、越文1.05/23.59。中文FID仅改善.23，尚无其内容正确率。

## 消融、成本与人评

T5 base FID16.73/HWD.87→SAQ12.47/.85→加SCE12.55/.84→加PCE10.20/.74；SCE阶段FID稍退化，累积表未隔离所有交互或证明每项单独必增益。T4 base+cosine21.06、LPIPS14.05、patchL2 15.10、PCE14.01；比LPIPS仅.04且无方差。补充T5 K512/1024/2048：IAM .86/13.80、.84/12.46、.86/14.10，最优中值，不能只据2048较差判已证过拟合；该IAM与正式10.20/.74配置映射未交代。IMGUR FID13.37/12.9/11.48但HWD1.02/1.03/.99非单调；IIIT .75/14.02、.77/12.61、.73/10.22。补充T4真实OCR准确81.76→+100K82.13→+200K82.96，+1.20pp，无等量其他生成器/重复真实数据控制。补充T6同V100/50步：124Mvs185M、trainVRAM6.82vs18.66GB、推理1.25vs1.85s/sample、VRAM2.1vs2.9GB，未给训练总时长/同尺寸batch明细。偏好40.6%为六法最多票，非多数；真假正文53.8%但图矩阵对角26.90+26.73=53.63%，均不构成与随机统计等价证明。F7attention及跨域F8–9是定性，IAM训练忽略未见墨色同时是能力边界；补充L显示模糊/复杂背景/难读/艺术字失败。

## 局限及论文/代码差异

离散码本和attention热图不能证明笔宽/倾角/连笔已因果解耦，连续旁路/背景/内容都可携带写者信息；同坐标patch负例可能含重复部件，坐标匹配依赖对齐，InfoNCE最大化不直接保证字符合法/独立因子或原始图互信息严格增长。语言分别训，OOV新词不等未知alphabet/字类/新script；中文单字图不等笔顺。补充作者承认极模糊/复杂背景/难辨手写/艺术字和较长行文本限制。当前代码和正式损失/CFG有差；SCE为双向cross-batch CE、温度实为1，负库与正文2B−2不同；PCE三尺度均权后再除3，系数1/9而标准双向平均1/6；codebook在NCHW上先沿dim−1即宽度normalize，再permuted作768维lookup，非逐空间向量统一L2。test默认random_style_image=False使用目标图自身作style，sampling可CLI覆盖，正式表具体覆盖/参考映射未发布，不能据默认直接判正式泄漏。tools/eval.py使用未定义args.log_name，global不处理HWD；HWD distance函数不接verbose却调用带verbose；doc路径/模式和真实树不齐。以上为固定公开版本静态审查，无执行失败或私有正式训练版断言。

## 优势条件

若训练含足够作者/文字多样性且测试参考单张、字符词表已知、局部风格特征可迁移，离散/连续融合可正则风格提取，同位置latent对比可改善对齐局部细节；预期先体现在FID/HWD和限定下游OCR增广。需控制条件信息、风格/内容/背景混杂和预算，不能从现有指标推导未见汉字结构、跨script或逐笔动态优势。可作为文字视频的静态终图与风格条件基线，时间/执行约束需另建。

## 实验如何检验假设

分写者/词汇/字类/文字系统四种heldout，公布IAM四场景及CASIA/ViHT作者和参考映射，确保ref与target不同图/内容，另设同图重建对照。VQ有无×连续旁路×SCE×PCE等预算析因，配token使用率/置换/固定内容换风格/固定风格换内容干预，独立测倾角/粗细/墨色/连笔及字符oracle。PCE对齐/位移/重复部件/背景遮罩和softnegative对照，3seed+按writer区间。报生成图独立OCR的CER/WER/汉字拓扑和越文附加符号，而把生成→真实OCR单列迁移；下游等量真实重复、其他合成器和等训练步预算控制。核正式固定α/CFG7.5与公开动态配权/CFG6及PCE归一、码本归一维度；公开指标脚本/特征权重/同尺寸耗时。等终图不同笔顺/静态style+确定渲染/逐笔video强基线检验时序新增价值。以上未执行。

## 论文组织和Claim学习

可学Introduction单参考瓶颈→高频/连续表示不足→量化与两个对比目标→多语言数据验证；Method先任务定义/总图再按SAQ/SCE/PCE逐一说明，附录补指标、成本、失败，便于按假设审实验。写Claim需用当前数据/参考数/评测协议，“all best”“disentangle”“indistinguishable”“overfit”分别需逐表、干预、等价检验和训练/验证证据；表中非单调和辅助loss小差不宜用肯定因果措辞。正文和附录必须同读，WER在附录才有决定性定义。

## 实际阅读范围

正式主PDF10页2236432bytes：Abstract/§1–5完整研究正文、T1–6/Eq1–7/F1–9及图注；实际主PDFp1/3/4/5/6/7/8共7页，p2文字已读，p9–10参考定位未逐篇独立精读。正式supp8页3256687bytes：A–M完整研究内容、T1–6/Eq1/F1–11及图注，8页全部实际查看，参考文献定位不等逐篇精读；共15实际PDF页。固定cf31559/2026-05-26，92项完整树；README/DATASET/EVALUATING、IAM/CASIA/ViHT配置，SAQ forward/形状、codebook/SCE/PCE/PatchNCE完整，pipeline训练/配权/采样、diffusion噪声/恢复、dataset/sampler、train构建、sampling、eval及HWD/FID关键协议、CASIA转换已读；未称全库逐行。未读Drive内部数据/权重、跑模型或独立复现。

## 补充材料改变了什么理解

| 项目 | 新核到的协议 | 对解读的影响 |
| --- | --- | --- |
| WER | 生成IAMtest对应图训练OCR200K步，测真实test | 衡量该分布迁移效用，需要生成图直接OCR另测 |
| 写者分类 | 真实test80/20训练验证ResNet18，再判生成图 | 写者分类器见过这些写者，生成器写者泛化另看split |
| 越文 | 223写者、4644词、42Ktrain/>8Ktest | 文章未明确writer-disjoint，不能自动算未见写者 |
| DiffusionPen跨语言 | 专门改one-shot重新训练 | 避免与主表标准few-shot结果混用 |
| 人评 | 28人，偏好40.6%；真假文字53.8% | 最多票不等多数，接近50不等已证统计等价 |
| 失败 | 模糊/复杂背景/难辨/艺术手写，长行文本待研究 | 正文强泛化claim须保留此范围 |

## 五个关键问题

1. 单参考的稳定风格和局部细节如何提取，是本文实际研究问题。
2. 作者认为连续/高频风格和噪声MSE有不足；此为具体基线和数据下的解释，需表示干预进一步验证。
3. SAQ针对风格表示，SCE针对作者区分，PCE针对局部latent对应；三者与连续旁路共同作用。
4. 已知字符词表、多写者监督和单参考新风格条件下，预期FID/HWD和下游增广有益；新script、未知汉字类别及书写时序尚无证据。
5. 累积消融给局部支持，但IV-U HWD与SCE FID退化、PCE对LPIPS仅.04差距及K配置差异限制了宽泛归因；上文析因/干预/分布实验用于证伪。

## 公开实现需单独核对

当前配置loss_balancing=True：按噪声/辅助梯度标准差比动态缩放，formal Eq1固定α=.1不等该路径。PCE已将三层权归一到1/3，最终再除3，双向每项系数1/9；正文标准平均为1/6。SCE代码没有τ缩放，跨batch一个方向的候选也与正文全2B−2负库不同。码本normalize在NCHW的dim−1，实际沿宽度；应与逐空间768维特征的距离定义分别记录。不能据这些静态差别断言私有正式版本用了同一实现。

当前test配置同图作reference，sampling支持覆盖配置，真正四场景和新词测试要固定参考映射；此处记录公开默认行为，未判正式结果数据泄漏。eval入口未定义args.log_name、global分支未执行HWD，HWD距离接口不接verbose但调用带verbose，均未运行触发，仅静态可见。

## 追引与覆盖队列

全文追引并与现主目录核对：One-DM、DiffusionPen、WordStylist、HiGAN/HiGAN+、HWT、VATr/VATr++、Handwriting Distance、Rethinking HTG Evaluation: Bridging Generation and Recognition（arXiv2409.02683）、IIIT-English-Word数据论文、Vintern-1B（2408.12480）。本轮这些英文标题检索未命中主目录，仍需按作者/DOI/别名复核后补录，未宣称已完成精读。LatentDiffusion/DDPM/VQ/CFG/DDIM经典工作也须按既有条目去重。
