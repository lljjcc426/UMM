# FontDiffuser / DiffBrush：泛化轴、指标与发布配置（第六十一批）

[L019](../reviews/L019.md)、[L023](../reviews/L023.md)完成所列版本核心阅读/五问书面检查。目录347条保持，136核心/138书面，211条尚未确认核心三遍（含资源等层级）。本批无文件删除、模型训练、推理或独立复现。

## 任务和数据分布

| 项目 | 实际问题 | 明确的泛化/条件 | 不能外推 |
| --- | --- | --- | --- |
| FontDiffuser | 一参考字体图+宋体内容图→96²静态字形 | SFUC100已见字体×272未见字；UFUC24未见字体×300未见字；UFSC24未见字体×800已见字 | 规范笔顺、视频或动作；定性中→韩不等所有文字体系稳定 |
| DiffBrush | 一参考作者行图+字符串→64×1024静态整行图 | IAM496/161作者、CVL283/27作者；中文HWDB816/203作者；词模型重训行数据与拼接另列 | 3D判别的切片轴为真实视频时间；行中左右字符序为实际落笔序 |

FontDiffuser有内容图，摆脱Diff-Font固定字符ID的未见内容限制。DiffBrush已有英文/中文的整行生成及字间距、垂直对齐研究；后续问题必须具体到有序事件、RGB过程或真实执行，不能把这些静态任务重新称空白。

## FontDiffuser：方法与原表

[AAAI官方](https://ojs.aaai.org/index.php/AAAI/article/view/28482)确认2024,38(7),6603–6611、DOI10.1609/aaai.v38i7.28482。实际完整核心及附录文字来自[arXiv2312.12142v1](https://arxiv.org/html/2312.12142v1)，正式PDF未完整取得，不计全文。已看实际Fig2/Fig6；参考文献和全部样例未逐一追读。

MCA融合三尺度content及style crossattention；RSI参考结构Q与UNet skip K/V计算offset，经DCN改变skip；预训VGG多层SCR冻结作风格监督，以同内容异风格负样本减少内容捷径。两阶段noiseMSE+VGG感知.01+offset.5，第二阶段加SCR.01；预测x0送SCR。400字体×800字训练，96²，单3090，AdamW，440K/b16/lr1e−4 linear→30K/b16/lr1e−5 constant/K16。SCR另训同数据K48/warmup1000/lr1e−4，完整总steps成本不明；DPM-Solver++20/CFG7.5。

| T1/T2条件 | FID↓ | SSIM↑ | LPIPS↓ | L1↓ | 人评份额 |
| --- | --- | --- | --- | --- | --- |
| SFUC，本法 | 7.6985 | .4682 | .1416 | .3454 | 46.85% |
| SFUC，CG-GAN | 7.7862 | .4004 | .1961 | .4100 | 32.87% |
| UFUC，本法 | 8.5352 | .4206 | .1496 | .3870 | 47.15% |
| UFUC，MX-Font | 10.7689 | .3928 | .1653 | .4098 | 14.11% |
| UFSC，本法 | 7.6708 | .4942 | .1426 | .3279 | — |
| UFSC，Diff-Font | 12.0809 | .4192 | .2022 | .3877 | — |

Average FID在全部复杂度样本上计算，不能取分组FID算术平均。UFUC hard本法SSIM.3420低于CF-Font.3434、L1.4508高于CF.4420，因此分组并非全指标最优。25人从全部方法挑最好，30个SFUC/20个UFUC字体，每字体6字；偏好份额不等成对胜率或正确率，缺CI/多seed。

T3 baseline→+M→+MR→+MRS：FID8.1153→7.8419→8.4427→8.5352，SSIM.4112→.4114→.4137→.4206、LPIPS.1526→.1511→.1506→.1496、L1.3955→.3954→.3925→.3870。渐进模块消融非全因子，FID与配对指标不同步。T4增强使FID8.1758→8.5352变差，其余改善；T10 scale1的FID7.1447低于7.5的8.5352，后者配对指标更好。需要报告取舍与validation选参。

## DiffBrush：判别信号和评价的实际意义

[CVF正式论文](https://openaccess.thecvf.com/content/ICCV2025/papers/Dai_Beyond_Isolated_Words_Diffusion_Brush_for_Handwritten_Text-Line_Generation_ICCV_2025_paper.pdf)和[含附录PDF](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Dai_Beyond_Isolated_Words_ICCV_2025_supplemental.pdf)完整取得；[arXiv v1](https://arxiv.org/html/2508.03256v1)核心§1–6/AppB–N文字/T1–8已读。实际正式p3 Fig3、p7 Fig7、p8 Fig8–11、附录p14已看。未全AppA/参考文献/O全部样例或逐页正式全文。

双head提取完整style，再mask列/行作作者proxy监督；条件本身保留完整style。行判别将content guidance与生成图拼通道，切32段经3DCNN建字符上下文；词attention预训后冻结定位，2DCNN监督局部结构。图像空间切片索引可以当3D卷积第三维，不产生视频。8RTX4090/800epoch约4天，前750仅diffusion+style，后50加判别并5步去噪生成粗图；冻结SD1.5VAE/1000linear/DDIM50，论文drop.1/CFG.2/mask.5。

| 证据/指标 | 实际定义与结果 | 解读限制 |
| --- | --- | --- |
| T1 IAM | 本法HWD1.41、D_CER8.59、D_WER28.60、FID8.69、IS1.85、GS.00235；One-DM1.80/20.91/54.27/10.60/1.82/.00842 | D_CER/WER由生成集训练OCR后测真实test；含内容、多样性、域距和OCR训练因素，非直接生成图错误率 |
| T1 CVL | 本法1.06/20.92/36.38/7.57/1.70/.0296 | 不同作者/分布，不能与IAM绝对值直接作同任务排名 |
| Fig11中文 | 本法HWD.73/D_AR96.24/D_CR96.65/FID7.87；OneDM1.09/81.99/82.80/17.38 | D_AR/CR仍为下游真实集识别；单独中文训练，不等零样本跨语言 |
| Fig7消融 | no-mask1.82/56.02/87.25→双head1.47/54.64/84.33→加word1.42/14.61/43.93或line1.44/15.28/43.31→两者1.41/8.59/28.60 | 支持局部/全局互补，缺完整预算匹配/CI与内容probe，不能证明严格因果解耦 |
| AppT3/T4 | CTC最佳λ.1 HWD1.67/D_CER16.53；判别λ.05 1.41/8.59；2Dline改3Dline D_CER13.18→8.59 | λ/mask在IAMtest择优，需独立validation冻结 |
| AppT8增强真实训练集 | CER5.78→4.62，WER21.76→16.86，CER相对降低20.07% | 真实+生成混合训OCR，与T1纯生成训OCR协议分开 |

HWD为手写VGG16特征距离；FID论文25K生成对全部train，GS5K生成对5Ktest，IS在生成test。WIER识别器按test作者图80/20训练/验证，评价生成风格，未证明未知身份分类器泛化。主表词方法在行数据重训；Fig10用固定排版拼接，AppH更强Otsu间距/质心线拼接，三种设置必须区分。

AppD两个30人×30轮=900回答研究：五候选style偏好本法35.7%、OneDM21.9%、VATr14.8%、CSA14.4%、TS13.2%；真假混淆矩阵为全部回答份额，Real→Real27.22/Real→Fake22.78/Fake→Real28.11/Fake→Fake21.89，总正确49.11%。它没有统计等效检验、多评委重复依赖CI或任意分布不可分证明。低频标点/Greek结构错误已有失败分析；文称Unifont可接受任意Unicode，输入可编码与输出可靠需分开。

## 固定工程制品的核对

| 固定版本 | 阅读范围 | 配方/发布差异 |
| --- | --- | --- |
| [FontDiffuser7b28ce9](https://github.com/yeungchenwa/FontDiffuser/tree/7b28ce9c3b357f4fb23296622f458cf169803539) | README主体、config与两launch全文、RSI/DCN/attention选段 | 两launch b16/440K→30K与论文主要条件相同，parser默认b4被覆盖；seed123/phase1warm10000/WD.01/clip1。SCR预训README仍ComingSoon，但云盘权重标released，不能称全预训复现；含SCR辅助成本 |
| [DiffBrush da9addc](https://github.com/dailenson/DiffBrush/tree/da9addc1140bdfec463b2d41a974a0a392f80798) | README主体/IAMyaml、generate.py主体、DDIM、双head/mask/blender/UNet.forward选段 | 论文vertical→horizontal、代码horizontal→vertical；默认DDIM/forward调用路径没有无条件混合CFG。generate.py限WikiText35–61字、FID目录5000停，论文25K。yaml EPOCHS2000、主文800；README仅推理路径，不能据示例断言实际训练2000。未下权重或运行 |

代码差异是可定位的复现缺口，不能据此声称原论文实验错误；需作者精确脚本/配置或独立执行。所有工程读取边界均保留。

## 可证伪实验与研究写作

固定骨干、条件数、VAE/预训和总预算，FontDiffuser全因子MCA×RSI×SCR、DiffBrush双head/mask×行/词判别×CTC，多seed/按复杂度、作者、语言和行长分层。独立validation选参，直接OCR读生成图与下游OCR迁移/混合数据增益分别报告；独立content-probe及干预验证风格解耦，盲评按评委/作者cluster统计。若研究逐笔视频，加入真实事件、顺序/方向/时序可观察性和执行指标。全部未执行。

学习两篇由具体失败提出模块，再为各个Claim分别设计对照。Introduction须明示单字/整行及未见内容/字体/作者的区别；Method沿条件、噪声/图像、辅助监督组织；Limitations报告指标取舍、test调参、OCR依赖、词定位错误与公开配方差别。发现限制后还要追引后续解法，不能直接宣称新颖。
