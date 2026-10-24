# Stroke-Seg：作者原图、消融勾选列与公开样例边界补查

第一百七十五批完成[L184](../reviews/L184.md)指定原文与公开协议审查；五项书面记录保留未通过，未增加核心三遍数。[结构化证据](../../data/stroke_seg_author_figure_checkbox_and_sample_code_recheck_2026-10-24.json)。358目录（331论文／研究、27资源），280核心/285书面含未通过项；待完成核心深审51篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.13255)、[主源2](https://ietresearch.onlinelibrary.wiley.com/doi/epdf/10.1049/ipr2.13255)、[主源3](https://airl.csu.edu.cn/news/shufa.html)、[主源4](https://airl.csu.edu.cn/img/shufa1.jpg)、[主源5](https://airl.csu.edu.cn/img/shufa2.jpg)、[主源6](https://github.com/Rvosuke/BCSS/tree/2451eb756ff4adb5a6e00e8b3d5cdd8fd8400621)。

## 研究问题

在静态毛笔字中保留交叉区域的完整笔画结构，并利用字级先验增强分割。

## 现有不足

单标签语义分割会截断交叉，多阶段实例检测局部框缺全局，逐笔生成输出位置不固定；26种形态频率不均。

## 贡献

将笔形按相似外观与相交关系归10类；字符识别→字典11维先验；多标签阈值输出和BCE+Dice组合BDLoss，兼容多backbone。

## 输入、模块、输出与公式

静态字图+由识别/字典得到的先验→10类重叠mask；没有视频生成或真实书写时间。

## 模型结构

Figure2：recognizer查character-ID+10类计数，经上采样成W×H×1和灰度图拼接。每通道独立阈值，Youden选λ=.6。BDLoss逐类求和，.5BCE+.5Dice，Dice使用平方分母及smooth1；是像素类别而非唯一落笔实例ID。 类别通道非唯一实例ID；同类相交在该二值表示中可能不可区分。11维先验含任意字符数值ID及10类计数，经空间上采样；应测ID重编号/正确识别/噪声ID，不将字典先验作用称语义推理。Eq5/6的yt在公式应作GT类标签，但原文用是否预测正确的表述有歧义，缺实现不能擅自定实际代码。 本次实际查看作者实验室原图F2：400×400灰度一通道、11维PKV经upsample成一空间通道、输入拼为400×400×2、输出400×400×10；图中同类多个笔画共享通道。公开FCN/UNet类数可配置，FCN示例n_class=10但输入是3通道320²随机RGB；两者forward的prior_feat参数未使用，FCN拼接语句被注释。DeepLab构造默认num_classes=16但build_decoder硬编码6；不能把所有源码一概称固定六类，也不能仅据prior_feat未用推定外部调用永远不可能在x中拼先验。

## 数据分布与划分

论文Table1：1022trainval(10301笔)+90E3C未知字(1358)+113CCSEW(1660)+97异风格(1447)，1322图、相加14766笔；与repo/HF10653冲突保留。训练872图8793笔、验证150图1508笔；外部300再按150已知/150未知字报告。

## 指标与评价协议

TSR=按图平均(正确笔数/GT笔数)，正确要求单笔IoU>.8；FSR同以GT笔数作分母计算错误笔，未必1-TSR；非笔顺准确率。FLOPs及Params列用MB，不能无依据解释成百万参数。

## 对比方法

SSGAN、CCSE(MaskRCNN)、DeepStroke；FCN/UNet/DeepLabv3+/TransUNet/TransDeepLab/Mask2Former/OneFormer(后两SwinB)。原方法是否同样获得真字先验、recognizer误差是否端到端纳入未充分明确。

## 实验条件和发布边界

400²保比例pad、Otsu及连通域去噪；Adam β(.9,.990)、b16、200epochs/val plateau10，PyTorch1.12/2RTX3090。所读§4.3没有lr；阈值调参所用split未明确。Table2标题updatedtest与正文validation用词不同，保留差异。 正式§5.1称T2为validation，表注称updated test set；§5.2称four curated visual cases但T3数值多行与T2相同，确切统计集合需澄清；§5.3明确独立300外部集。固定GitHub tree2451eb756ff4adb5a6e00e8b3d5cdd8fd8400621未见完整train/loss/checkpoint，不能以样例推原表配置。 本次固定树共128项/122blob/18个Python文件；README全文明确仅FCN样例、部分原始数据/标注模板，要求按论文自行修改。选读FCN、DeepLab、UNet三个模型文件，缺完整训练、PKV字典/上采样、BDLoss、TSR实例匹配和checkpoint证据；没有运行模型。HF卡片另指Rvosuke/Stroke-Seg，当前GitHub公开入口404，不能推定其历史存在/删除情况。

## 主结果

Table3 TransUNet TSR.982/FSR.018(79G)，DeepStroke.935/.068(54.1G)，FCN.961/.045(39.9G)；§5.3/Table4外部300为.897/.103，其中已知150=.962/.065、未知150=.831/.140；不能以98.2%代表外部泛化。 正式T2 U-Net Dice无prior .681→Dice+prior .880为19.9pp；完整BDLoss+prior .955相对.681为27.4pp，§5.1把19.9写作整框架相对Dice独用的增益口径不清。不能套用摘要增幅而不标比较行。T3参数栏原单位MB，FLOPs不等于实测延迟或包含识别/字典维护成本。 正式HTML已解析T2完整勾选列，每个backbone六行依次BCE无/有prior、Dice无/有、BDLoss无/有；19.9pp与27.4pp比较行据此确认。T4已知/未知各150，(.962+.831)/2=.8965四舍五入.897，(.065+.140)/2=.1025四舍五入.103；该均值与表一致，TSR+FSR不要求恒为1，不能把已知项和大于1当算术错误。实际查看作者实验室F8，展示E3C/CCSEW/其它风格known/unknown两列，细交叉与连笔错误仍可见；展示样例不作为新的量化证据。

## 消融及进一步实验

Table2按backbone切换BCE/Dice/BDLoss及PKV；TransUNet BDLoss不带PKV .935/.072，带PKV .982/.018；FCN .932/.061→.961/.045。未充分单独隔离10类重组与多标签策略，复杂结构更稳等因果解释仍属作者解释。 其余backbone BD+prior相对BD大多改善，但没有多seed/同训练搜索成本区间；类合并/多标签未做独立全因子；prior含count+ID，未拆各分量或gold-vs-pred识别，不能证明新增识别能力。

## 局限与疑问

作者明确人工字典维护、交叉细边界、极端风格不足；§5.4说PKV未充分利用且需更多消融，不能写已证明其内部推理。类mask不保持同类重叠实例身份和笔顺。外部性能明显下降；HF6类7值与论文10通道不齐，FCN示例10类/UNet可配而DeepLab实际6类，公开样例不能称主表复现。论文计数/表split称谓、FSR具体匹配与重复笔计数仍须审。2026-10-24补看作者实验室F2/F8实际原图、正式HTML表2勾选列；其余F1/3/4/5/6/7/9仍仅图注/文字。出版方直接PDF、作者上传和幻灯片入口访问受限；网页工具可抽全文但截图未返回实际像素，本批不将其登记为视觉阅读，也不增加核心三遍数。

## 预期优势条件

多标签有利不同类交叉，已识别字符的结构先验可能降低类混淆；优势应在静态毛笔分割与相同先验条件下验证，对视频时序没有直接证明。

## 可证伪实验

固定图像/训练/预算，类别重组、multi-label、PKV、BDLoss全因子；gold/pred/noisy字符ID与等信息基线，测试未知字和同类交叉；GT匹配算法一对一公开，额外测实例重建与方向/事件次序，不能仅用TSR。 加字符ID随机重编号、gold/pred/noisy/no-ID×计数向量，排除ID记忆；同类交叉/三笔交叉与实例身份非唯一分层；阈值.6用独立val选择，公开原先验/GT匹配与前处理connected-domain阈值，完整含识别器总成本。

## 论文组织与Claim学习

从交叉/先验瓶颈对应到模块和消融的组织可借鉴；Claim须注明验证集与外部集，BCE+Dice与既有组合损失追引后判断创新；Limitation中机制未证实需保留。

## 实际阅读范围

此前正式Wiley 15页核心文本Abstract/§1–6、Eq1–8、T1–4数值/图注、§5.3外部300、§5.4错误/§5.5限制与数据可用性已读。本次重新核正式HTML T2全部42行及勾选列、T1/T3/T4，实际查看作者实验室原图F2框架/F8外部结果；并未本次从头重读所有旧全文。其余F1/3/4/5/6/7/9缺实际图版，保留partial。固定GH树128项/122blob/18py；README全文及FCN/DeepLab/UNet模型文件主实现已读，非全仓逐行；缺训练/权重/全部标注与评价匹配实现，未执行模型或独立复现。五项书面更新，核心三遍仍未通过。

## 逐图边界

本批只把作者实验室F2和F8记为实际图像阅读。正式HTML表2勾选列已核，其余图版仅有图注/文字，未登记核心三遍完成。公开样例源码可配置项与硬编码项分别记录。资源S016原笔记已作同样区分，本批未修改该资源笔记。
