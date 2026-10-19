# 字形条件、成对基准和结构目标审查

2026-10-20，L003/S002/S003/U13–U16/U19八项，逐篇七字段、五研究问题及写作学习见[笔记目录](../reviews/README.md)。新增L003/S002五项书面检查。没有模型执行、没有新增独立计数、没有删除文件。

## 任务边界与主要证据

| 工作 | 输入→输出/贡献 | 关键条件 |
| --- | --- | --- |
| Write Like You | 标准内容轨迹+作者字样→草写轨迹 | zero-shot仍有M参考；OOV有外部xc；主文三层风格、代码默认四层 |
| TextDiffuser | prompt/布局/模板→静态场景文字图 | 95字符空间mask，17通道UNet；不生成笔顺/视频 |
| GlyphControl | prompt+渲染glyph→静态场景图 | 主训练冻结SD，TextCaps后续开放decoder；短英语词为主 |
| GapEval | 同义问题→文字/图分别评价 | 成对准确与共成功，IRT式总Gap需锚定核查 |
| UniG2U | 原图/问题→答案或辅助图后答案 | 35系统含agentic，closestbase非严格相同预训对照 |
| RealUnify | 理解型生成/生成型理解基准 | direct/step额外调用不同，不能都归因共享参数 |
| VGUBench | 文字问题→文字/答案字图；GT答案→字图 | 2164题、答案复用、固定512²黑底白字模板 |
| UniMRG | 四目标后训练→理解及静态生成 | teacher深度/SAM边界，OpenUni额外3000step生成 |

## 论文与发布配置

[WriteLikeYou代码a335b02f](https://github.com/ShusenTang/WriteLikeYou/blob/a335b02f806d846ba85a6f37f990eb8c2d57b3b6/model.py)默认enc2_rnn_layers=4、num_mixture=20，style/content cycle weight均0；[正式作者PDF](https://www.wict.pku.edu.cn/zlian/docs/2021-03/20210325112352381488.pdf)§5报告风格三层、λcycle5。命令行hparams可覆盖，因此记录为默认与论文条件不同，不断言论文没有执行。380–392行cycle用GMM加权位移均值和阈值pen-state构造假轨迹，xy均值可导，状态阈值路径不可导；它与完整随机rollout/真实时序分布对齐不同。

[TextDiffuser README](https://github.com/microsoft/unilm/blob/31c5b904ca1bf2afb4c234a6675c683a4e5fc7cd/textdiffuser/README.md)每进程24×acc4需8进程对应全局768。字符感知latent分割网络先1epoch；像素制标分割网络约4M/10epoch。主扩散训练四天未涵盖所有辅助成本。Table2准确.396→.494是9.8pp；Table4FID38.758弱于DeepFloyd34.902，OCR和图质分开。

[GlyphControl README](https://github.com/AIGText/GlyphControl-release/tree/5891d9b245ac9209c22e3d6d5e933b95d428a230)说明TextCaps5K额外40epoch并训练原decoder，承认创造性/多样性可能下降。主[训练YAML](https://github.com/AIGText/GlyphControl-release/blob/5891d9b245ac9209c22e3d6d5e933b95d428a230/configs/train_configs/laion_glyph_glyphcontrol_train.yaml)warmup1注明resume；从头10000，启动配置需保留。Table1斜线Simple/Creative，42/28是敏感大小写，48/34才是忽略大小写。主表参数不含textencoder，IF还用超分，不能按这些数字认定相同总参数/预算。

## GapEval参数可识别性：本次公式分析

[arXiv2602.02140v2](https://arxiv.org/pdf/2602.02140v2) AppB Eq7–11为每模型两维θ、两项模态β，µ/Σ也联合估计，边际成功/失败计数进入似然。已印式未出现逐题难度β_j；主文“区分题目难度”解释需实现补证。Eq1主文省略失败项，但Eq9有，不能仅据Eq1判断模型完全忽略失败。

按AppB印刷目标，任取两维常数c，令θ_i′=θ_i+c、β′=β+c、µ′=µ+c，Σ不变。则θ_i′−β′与θ_i′−µ′均不变，似然和高斯项/行列式保持；当c_text≠c_image时，Eq12的跨模态θ差改变，Eq13及后续Gap可改变。因此，在这些参数确实自由且无额外锚定的条件下，目标不能唯一确定该Gap。本次没有取得拟合代码，不能排除实现额外固定µ/β/初始化约束；该结论是对已印公式的条件推导，不是独立重算或对表格数据真实性判断。

还应区分共成功率、一致性与训练协同。AppF2.2 BAGEL需混官方标准数据维持生成，另两模型才做纯单侧；非迁移可能受更新位置/优化/生成瓶颈影响，尚非知识表征分离的唯一解释。主表“GPT家族”分文字/图API，也不足以确认相同共享参数。

## 对照与取舍

[UniG2U v1](https://arxiv.org/pdf/2603.03241v1)定义base差值有助于减少异构混杂，但正文也承认无官方base时选closestVLM；文字cap、图default和OOM降分辨率不能证明同FLOPs/同观测预算。BAGEL direct35.84/GtA36.10略高本组base33.35，Showo2 direct31.59/GtA26.59低base33.35，任务和协议分别报告。

[RealUnify v2](https://arxiv.org/pdf/2509.24897v2) UEG图像分与GEU选择题理解不同；NanoBanana UEG63.0而BAGEL GEU39.3，GeminiPro GEU54.8。生成辅助图有时可提高理解，有时错误图损害推理。step文字重写改善生成仍需同调用数纯文字对照，不能只据更高分证明共享结构协同。

[VGUBench v1](https://arxiv.org/pdf/2602.23711v1) Avg含可读/完整/正确，不是答案accuracy。表2有显著但很小的相关，QwenImage r−.0897；离散评分并列rank与重复答案映射需要tie处理和cluster区间。文中给Pearson“依赖近似正态”的说法过宽：系数本身可直接定义，精确t检验的分布假设另说。未核统计代码，不擅自改原表p值。

[UniMRG v3](https://arxiv.org/pdf/2601.21406v3) 主表Harmon DPG RecA86.61→UniMRG85.27下降1.34pp，OpenUni GenEval RecA70.07→68.00下降；比base仍改善。原文“not harming”须按基线/指标限定。深度minmax按图归一，没有绝对距离；SAM边界不等带类别分割。新增teacher监督和OpenUni额外生成训练均是收益解释的重要变量。

## 阅读边界

八篇只按逐篇已读范围升级相关章节，完整附录和代码继续补；五项全文受限仍未升级。尚未独立复现、尚不能宣称所有三遍完成或全领域零遗漏。下一批U20–31与新绘画/机器人/无论文制品并行扩展检索，先去重再核原始材料。
