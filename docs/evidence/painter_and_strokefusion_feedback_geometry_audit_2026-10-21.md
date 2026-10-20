# Painter 与 StrokeFusion：反馈、几何和过程证据

第七十四批补完[L180](../reviews/L180.md)、[G024](../reviews/G024.md)的明确范围核心三遍与五项书面检查。350目录、159核心/161书面，191条尚未确认核心三遍（含资源）；本批不新增独立论文、不删除文件、不运行模型。实际已读范围详见两笔记，参考文献没有因此自动计为精读。

## 来源与真实任务

| 工作 | 正式身份/来源 | 输入、输出与时间含义 |
| --- | --- | --- |
| Painter | [ICCV2023W/MMFM，305–314正式PDF](https://openaccess.thecvf.com/content/ICCV2023W/MMFM/papers/Pourreza_Painter_Teaching_Auto-Regressive_Language_Models_to_Draw_Sketches_ICCVW_2023_paper.pdf) | 文本/画布→逐笔动作/分类，渲染画布逐笔反馈；Workshop，不能写ICCV主会 |
| StrokeFusion | [AAAI2026，40(16):13656–13664](https://ojs.aaai.org/index.php/AAAI/article/view/38372) | 噪声/类别→无序笔画latent/box/presence→矢量草图；去噪时间不等真实绘制时间 |

两者与书写问题直接相关：Painter给出早期预训练LLM直接输出笔触及渲染反馈的先例，StrokeFusion给出局部形状/布局拆分与集合生成强基线。它们均没有提供严格汉字规范事件、真实手部RGB视频或共享UMM协同优势的完整证据。

## Painter：闭环设计与闭环有效性之间尚缺实验

QuickDraw单物体不覆盖关系/布局，作者结合VisualGenome关系框及随机1–4对象合成约20M；实际约2M用于本实验，约1000 eval，精确train/val与原对象/组合身份隔离未给。六任务包括新画、补画、擦全部/局部、复画、分类，BLOOM176B改写指令、ThePile正则。

OPT125M/1.3B全量FT，冻结ResNet50，以图占位处hidden为query、带空间位置的图特征为key/value；除末层外加残差单头crossattention。普通tokenizer输出HTML/颜色/宽度/点串，loss只response且mask图占位。每笔line renderer更新画布，再把新画布插入下轮上下文直至结束。正式p307 F1与p308 T2已实际核看。Eq1层上限的L与前文文本长度L/图中层N记号冲突，按明确文字“除最后层”理解，不代填作者代码。

已有反馈设计不能略过；但“模型利用反馈修复错误”仍缺无反馈/扰动画布恢复对照。训练GT画布、推理生成画布还存在暴露差异。F6注意力图只显示相关定位，不能证明因果纠错；ResNet优于CLIP的动机也未有控制实验。

正式p308 T3实际结果：

| 设置 | exact分类% | 擦全部PSNR | 擦局部PSNR | 复画PSNR |
| --- | --- | --- | --- | --- |
| 125M | 34.50 | 20.15 | 22.69 | 17.74 |
| 125M+Pile | 17.57 | 20.25 | 22.95 | 17.21 |
| 1.3B | 3.20 | 19.56 | 22.27 | 17.20 |
| 1.3B+Pile | 40.26 | 20.64 | 23.90 | 16.97 |

文字混训有尺度/任务交互，不能概括为普遍提升。新画/补画只有selected定性，作者明确没有预算做人评；不虚构生成FID/人评或主SOTA。exact字符串会罚等义关系/近似类别，白底PSNR可能弱化小对象错漏。白2px擦黑1px是覆盖，重叠前景会受损，不能按真实对象图层恢复解读。

训练两A100/Adam1e-5/b4/一epoch，分类greedy、其余top-p.9；Pile配比/完整tokens/运行时/seedCI未报。所有定性默认1.3B+Pile，attention特用125M。方法是可行性前作，仍需同预算反馈、encoder、混训与多任务消融。

## StrokeFusion：归一化形状、显式布局与无序集合

每笔重采点，几何Transformer与指数距离场CNN联合VAE重建；冻结encoder后扩散联合latent、box与presence，16层Transformer不加笔间位置编码。最终v>0的笔画解码/还原box，覆盖构图。实际p13658框架与p13661/2主表/消融已看。

无序结构准确表述为置换等变 F(PX)=PF(X)；输出集合渲染不变。单笔点序仍有PE，不能说所有顺序都被消除；但笔间规范顺序未建模。中间去噪状态会同时变形/移动/出现消失，不能当逐笔单调新增的视频。

正式主表支持特定优势及反例：

| 对照 | 作者数值 | 解释边界 |
| --- | --- | --- |
| QuickDraw简单类 vs ChiroDiff | FID19.53 vs17.17；precision/recall .71/.58 vs.61/.50 | 质量/覆盖指标有取舍 |
| 中/高复杂类 vs ChiroDiff | FID18.99/17.76 vs23.84/27.78 | 与结构假设相容；分组类别不同，不能隔离笔数因果 |
| FaceX | 7.27/.76/.89 | 所列表内优势大，仍缺多seed与协议补齐 |
| TU Berlin vs SketchRNN | precision .66 vs.73 | 不能声称全指标最好；语义歧义的解释待独立测试 |
| CreativeBirds vs Doodleformer | FID26.19 vs27.32，precision .56 vs.67、recall .30 vs.55 | 更低FID不意味着precision/recall更高 |
| CreativeCreatures vs Doodleformer | FID19.41 vs33.46，recall .32 vs.69 | 主表caption“全部指标更好”有反例；precision .58也低于ChiroDiff .59 |

T3 moon/TV/spider的full均优于两对照，但去归一化同时去box；去image正文设γ0。由Eq3/4的 I(g)=exp(−γd²)，γ0令非空笔画场恒1，改变视觉输入及重建目标。它未单独隔离“去掉image loss”的作用，需input/target/loss/容量控制。单笔反向的距离场相同，而几何点分支可能不同，方向应独立测。

正式未给完整LR/batch/预算；所谓跨域generalization实际各数据分别训练，不能改写为zero-shot。Ns按99百分位并丢长尾、算法切分笔跨语义部件与高频长笔困难均应保留。

## 无独立论文制品与可复用配置

[GitHub固定4fddf5d](https://github.com/doudin404/StrokeFusion/tree/4fddf5d834909bc838faa68f20e7c5ac104c5173)有训练/模型/数据处理/评价脚本；[HF固定abe809b](https://huggingface.co/doudin404/stroke_fusion/tree/abe809b1850d2dd0404ad477d5f8141c67206c60)有数据包、多个VAE及diffusion检查点。HF卡只有CC-BY-NC-4.0声明，无完整训练说明；GitHub API未列license，不能据HF卡推所有代码/原始数据授权。未下载/加载权重或运行模型。完整范围与文件清单见[制品审查](../../data/strokefusion_artifact_audit_2026-10-21.json)。

固定代码提供可试配方但未确认逐一对应论文表：VAE latent64/Np64/AdamW1e-4、b18；diffusion16层/512宽/16头、b256、两GPU、1000线性DDPM、10epochwarmup后恒lr、max32笔筛长、无限epochs与val最优选模，未给总预算。全局/局部坐标及box实现是[-1,1]/半宽，正式写[0,1]，不能混用；采样clip_sampleFalse、RDP epsilon2在×128坐标下。encoder SVG split99:1/seed42，diffusion99:1未传generator，无法假定两阶段身份严格隔离；这只是具体风险，原表测试集关系仍未知。

正文说推理只vector decoder，Limitations又说UDF解码开销。代码decode同时计算vector/image，sampler弃image输出，能解释此版实际冗余计算，但没有profiling/运行时间证据。

## 评价实现差异：先保留作者值，再统一协议

公开metrics使用torchvision ImageNet InceptionV3/去fc、299²白边与ImageNetnormalize。其FID绝对数值不能默认等同其他常用FID权重/预处理。PR main默认k20，而函数默认k3；函数只判断测试点是否落在最近中心的半径内。

[所引NeurIPS2019原文§2 Eq1](https://proceedings.neurips.cc/paper_files/paper/2019/file/0234c510bc6d908b28c70ff313743079-Paper.pdf)定义落在**至少一个**中心的kNN球内，即全部球并集。一般情况下，最近中心的球没覆盖，不排除较远中心的大球覆盖；故两定义不等价。当前静态分析只识别固定版本差异，不证明原表用了同版，也没有重新计算数值。后续须锁定weights/预处理/k/reference/RDP和球并集实现后再公平比较，不把FID与precision/recall取舍草率归为质量优劣。

## 可证伪设计与研究写法

Painter：相同OPT/数据/总更新与tokens，开环/逐笔RGB/残差/显式事件状态，注入漏笔偏移并测检测和恢复，拆Pile配比×模型规模、对象/模板组合留出，报告区域保持率/关系/事件与成本。StrokeFusion：norm×box×visualinput×imageloss，匹配类别/笔数/复杂度并保长尾；集合+合法排序器、AR顺序模型、规则SVG同预算，加入相同终态错序/反向/pen事件。所有实验未运行。

写作可学习Painter按数据缺口→任务/IO→反馈时机组织，以及StrokeFusion将局部形状与全局布局联系到复杂度分组。Claim应跟随实际反例、统计与预算；Method明确集合等变、场/坐标定义与推理路径；Limitations写清评价实现和协议缺项，缺失材料不能靠常用默认值补齐。
