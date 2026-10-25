# 余下7篇：A06原图补读与全文缺项

2026-10-25，第二百二十四批，基线2d61ab93。

本次仍未完成这7篇的核心深审。新增实质阅读为A06的8幅出版社原图；据此修正原笔记中“架构及基线全部待核”的表述。其余6篇补查作者、机构、出版方和公开仓库，仍未补齐各自缺项。核心完成数保持326/333，历史五条书面记录保持329项（包含未通过项）。无新增论文、无模型训练或推理、无文件删除。

## A06：逐图观察

论文：[Font Generation and Keypoint Ranking for Stroke Order of Chinese Characters by Deep Neural Networks](https://link.springer.com/article/10.1007/s42979-021-00717-2)，SN Computer Science 2:324，2021。

8个PNG均从出版社媒体端取得，并实际查看图像。下表只记录图中能确认的内容，完整方法、全部表格和实验条件仍未取得。[结构化来源与逐图记录](../../data/seven_remaining_source_and_figure_audit_2026-10-25.json)保存8个独立原图链接及访问结果。

| 图 | 已核内容 | 解释范围 |
| --- | --- | --- |
| F1 | G/F双向映射、Dx/Dy判别器、循环重建链和G的类别嵌入 | 能确认生成结构示意，不能据此命名InfoGAN、补造损失公式或权重。 |
| F2 | 字符、笔画、关键点三个Encoder；关键点经Gaussian Function；Concat后两个FC模块、ranking scores、Softmax、Cross Entropy Loss | 编码器内部结构、候选产生规则、训练标签与排序定义仍须正文。 |
| F3 | Standard Kai Font、Slender-gold-style、Running script三组字形 | 展示格数与编号不能充当完整数据规模或训练/测试划分。 |
| F4 | Generated Images与Input Images对照，红框显示交叉/短笔画附近异常 | 可确认字形生成存在局部缺陷；该图无法给出笔顺错误率。 |
| F5 | 下、化、露、照，每字三个不同外观的图像 | 图内没有列方法名，保留各列归属未知。 |
| F6 | 一、丁等字符的生成字形网格，编号到0112 | 图内没有笔顺、随机抽样说明或评测分布。 |
| F7 | Standard Kai Style、StrokeGAN、Ours、Slender Gold Style四行具名比较 | 确认StrokeGAN是字形定性比较对象；排序数值基线和消融尚未核到。 |
| F8 | 偌字原图、骨架、红蓝关键点和两组拆分图块 | 图中没有时间轴或顺序编号；图块数、颜色及方向不能直接解释为真实落笔事件。 |

### 对方法与证据的判断

**已有方法覆盖到哪里。** F2确认字符级上下文、笔画局部形状和关键点位置被共同编码。对UMM方案而言，静态汉字的多层表示与排序已有直接先例；仅以“字符—笔画—关键点联合表示”主张新颖性缺乏依据。需要进一步核对真实过程的观测与执行、输入输出监督及联合训练是否提供额外能力。

**可能有效的原因。** 字体生成可能扩充字形变化，字符分支可能提供全字结构约束，笔画与关键点分支可能帮助处理交叉处歧义。这些是从框架推导的机制假设。当前没有取得分支消融、字体隔离实验和等量数据扩充比较，不能将假设写成已经验证的增益来源。

**现有结果证明到哪里。** 摘要报告平均NDCG 0.9667、29.53%样本高于0.98。NDCG度量排序质量，不能换算为相同比例的字符完整笔顺全对。F4/F7描述字形质量，F8描述中间分解，均缺少独立的真实时间观测。还需知道相关性标签、候选覆盖率和失败样本处理，才能判断排序结果是否代表端到端恢复能力。

**优先补查的反证。** 第一，训练/测试之间同字不同字体是否隔离，能否同时泛化到未见字与未见风格。第二，评分是否只针对成功提取的关键点；若困难字符被排除，高NDCG可能掩盖候选漏检。第三，去除GAN或任一编码分支后，收益是否保留。第四，NDCG相近的输出在严格全序、方向和落笔段划分上是否仍差异明显。上述均为待核实验条件，没有执行模型。

本次已核[排序原图F2](https://media.springernature.com/full/springer-static/image/art%3A10.1007%2Fs42979-021-00717-2/MediaObjects/42979_2021_717_Fig2_HTML.png)与[比较原图F7](https://media.springernature.com/full/springer-static/image/art%3A10.1007%2Fs42979-021-00717-2/MediaObjects/42979_2021_717_Fig7_HTML.png)。[作者出版物页](https://www.cs.ccu.edu.tw/~ckchiang/Publication.htm)没有补齐该论文9页全文；Paperity的截断转录也未作为完整全文。

## 其余6篇及当前缺项

| ID / 论文 | 本次核查增量 | 继续完成所需材料 |
| --- | --- | --- |
| L002 / Diff-Writer | 官方章节、PAL成果索引、作者公开GitHub；OLHWG属于已收录L001，主页仓库为通用模板 | 完整ICONIP章节，含方法公式、全部实验及图表。 |
| L006 / Frequency-guided cross-modal diffusion | 查作者机构UPM库及题名/DOI；保留在线2026、卷期2027的区别 | 完整Information Sciences论文，含方法、频率模块、训练和实验。 |
| L021 / Write More at Once | 官方PDF仍受访问限制；第三方作者和Withdrawn未取得官方确认 | OpenReview对应版本完整PDF及附录；相似ICDAR论文不能替代。 |
| L022 / Layout-Offsets | 普通隔离Chrome仍停在验证页；搜索缓存含p8零散文字/图注 | 对应OpenReview版本全文、附录和实际原图；缓存零散页不足。 |
| F05 / Online Cursive Handwriting Generation… | Samsung说明的论文链接仍指向IEEE11463098，没有独立作者PDF | 正式ICASSP论文全文；现有作者说明缺正式方法细节和完整实验协议。 |
| L184 / Stroke-Seg | 正式15页文字已读；补查ResearchGate缺图页、Wiley图像入口和普通浏览器，均未取得缺图像素；另实看BCSS数据示例 | F1、F3、F4、F5、F6、F7、F9实际原图或含图完整PDF。现有F2/F8及数据示例不能补齐。 |

ResearchGate本页全文注明由出版方提供；本次访问记录据此修正此前“作者上传”的泛称。可读图注、自动图像描述或截图引用字符串均未算作实际图像。L021/L022的第三方状态也未据此更新正式接收/撤稿结论。

完整逐项链接见[当前来源矩阵](remaining_source_access_and_reading_handoff_2026-10-25.md)。本地Downloads与项目目录目前仅找到已完成阅读的《Towards Grand Unification of Multi-Human Activity Recognition》PDF。已请求用户提供其他本地PDF目录/路径；本次未取得这些文件。
