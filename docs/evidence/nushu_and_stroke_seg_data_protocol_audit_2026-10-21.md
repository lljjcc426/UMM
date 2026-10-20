# 女书资源与 Stroke-Seg：过程数据、类分割和协议核对

第七十七批补完[L047女书研究](../reviews/L047.md)的明确范围核心三遍；[L184 Stroke-Seg](../reviews/L184.md)重新审完正式核心文本，实际图表视觉核查尚未完成，**不计核心三遍完成**。350目录、164核心/167项五条书面记录，186条尚未确认核心三遍（含资源）；书面记录不自动代表五项均已通过。无新增独立论文、文件删除、模型执行或复现。

## 两项工作的任务界定

| 条目 | 正式来源 | 可确认的研究贡献 |
| --- | --- | --- |
| NüshuVision / NüshuStrokes | [EMNLP2025 main，12419–12428](https://aclanthology.org/2025.emnlp-main.627/)、[正式PDF](https://aclanthology.org/2025.emnlp-main.627.pdf) | 500字体渲染句图/静态OCR，另397字符Smartpen过程记录；没有训练文字到书写视频生成器 |
| Stroke-Seg / BCSS | [IET Image Processing18(13):4341–4355](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/ipr2.13255)、[正式PDF](https://ietresearch.onlinelibrary.wiley.com/doi/epdf/10.1049/ipr2.13255) | 静态毛笔图→10类重叠mask、字典先验及BCE+Dice；输出未携带唯一落笔实例、方向或时间 |

## 女书：静态字体图和动态记录分别审查

正式F2数据流程与p12421主表/公式已实际核看。Vision用一字体NotoSansNushu-Regular，把专家核验文本渲染为传统竖排右起384²图；“真实/专家校验”描述文本来源，图像仍是字体渲染，不能转写成自然手稿。Strokes来自一位有11年古汉字书法训练的贡献者，397字MP4平均3.94秒，均值不能写每段等长。

相邻灰度帧MSE<.1、静止超过一帧后取该段最早帧；缺fps、强度归一、接触/边界真值和一致性，不由停顿自动推出精确落笔事件。图例展示累积墨迹，原MP4未取得，无法确认纸面实拍/软件回放、手遮挡/实际pen接触。女书为音节文字，不能预设汉字部件和规范笔顺标签适用。

Appendix C与未来工作提stroke masking的教育/识别用途；主实验仅静态TrOCR转录，未用Strokes训练或验证其增益。原文没有字体、方向、书家或动态监督的定量消融，此缺项应保留。

## CER及日志分数的含义

主表五中文简繁OCR的1−CER均0；TrOCR微调CER.6735。CER=(替换+删除+插入)/参考长度，插入多时可大于1，CER1也可能仍含部分正确字符；1−CER不能当逐字符分类准确率。

[固定GitHub94f2a059](https://github.com/ivoryayang/NushuMultimodal/tree/94f2a059738299023ea805fef2e1dac38ecd060c)的[output.log](https://github.com/ivoryayang/NushuMultimodal/blob/94f2a059738299023ea805fef2e1dac38ecd060c/output.log)同时报：CER .673469387755102、句子ExactMatch0、按位置字符正确率.23517978620019436。1−CER约.3265，显然不等于这里的.2352；这是作者日志，未独立重跑。

`TrOCR_CER.py`清除U+FFFD和Unicode控制类后计算Levenshtein，另以zip_longest按位置比较。删除无效预测可能改变错误计数，建议原始与清理结果并列；不能把日志内“字符正确”解释成编辑对齐后的正确字符。五中文零样本与400条女书监督同时改变输出文字覆盖和适配预算，也不足隔离TrOCR架构优势。

## 原文训练和公开脚本的差异

| 项目 | 正式§5 | 固定制品 |
| --- | --- | --- |
| 训练 | 单GPU，2000epochs，batch16，lr3e-5，wd.01，AdamW | finetuning_nvshu.py为200epochs/batch8，未显式给论文lr/wd；不能自行填库默认值当原表 |
| 数据 | 随机400/100，最终留出100 | 训练split未固定random_state，test用于Trainer每50step评价；独立TrOCR_CER.py又以seed42重划，没有保存原split，无法确认同一留出集合 |
| 处理器/模型 | trocr-base-stage1 | 训练为stage1；独立评估processor换base-handwritten，checkpoint1400为本地路径；未确认处理器完全等价 |
| 长度/生成 | label128，beam4/lengthpenalty2/no-repeat3 | 主脚本label128、generation max64；完整表配置/checkpoint未公开核实 |
| 渲染 | 长句适当缩小base30字体 | generation.py在>10字符时用max(40,30−(n−10))，本语料对应40，字面增大；源图是否由该版本产生尚不明 |

重新分割可能把训练样本纳入评估，当前没有原checkpoint训练清单证明实际泄漏，不能把风险写成已发生事实。两个notebook也未固定split且参数不同，不能凭文件存在声称完全复现原文。未运行任何作者程序。

完整CSV500行经普通统计：499唯一句；1-based第294/315行句文本相同，尚不知原split是否跨组。原字符串4–18字符，共345不同字符，其中343个Unicode名称NUSHU字符，以及空格和汉字“漠”；保留原数据，未删改。397是另一个Strokes字符库的作者规模，不能沿用为Vision字表数。数据统计不是模型独立复现。

## 发布声明与可取得材料

论文Ethics称代码、两个完整数据都公开。固定tree实际15文件：字体、CSV、渲染/训练/评价脚本、notebook及log；没有PNG、397 MP4、stroke边界、Smartpen处理或checkpoint。CSV/字体/代码可用于重建静态图，不代表已取得动态集。该结论限这个固定官方tree，未据此断言其他站点不存在发布。

详[女书制品JSON](../../data/nushu_multimodal_artifact_audit_2026-10-21.json)。本轮未联系作者、下载权重或执行训练/推理。跨书家/方向/字体/书页固定留出、文本去重、保留原CER与EM、确认真实采集/接触与笔事件，才可检验动态资源对识别或生成的作用。

## Stroke-Seg：保留此前制品差异，补齐正文分析

正式核心§1–6/Eq1–8/T1–4数值和图注本批已重读。26形态按视觉/交叉关系合成10类；recognizer取字ID后查10类计数，构成11维先验，上采样与灰度图拼接；每通道阈值.6保不同类交叉，BDLoss逐类.5BCE+.5Dice。它仍可能合并同类相交实例；类别二值mask未保存哪次落笔、方向和时间。任意数值字ID的重编号敏感性、计数/ID各自收益、gold/pred识别误差应单测，不能把先验利用直接称语义推理。

TSR按图平均“与GT IoU>.8的正确笔数/GT笔数”，FSR也以GT笔数归一，错误还含漏笔等。GT匹配/重复计数一对一规则不详，FSR不是通常precision，也不必等于1−TSR。

T2 U-Net Dice无prior .681，加prior .880，增加19.9pp；完整BDLoss+prior .955，较.681为27.4pp。正文把19.9概述为整框架相对Dice独用改善，比较口径不清。TransUNet BD无prior .935/.072，带prior .982/.018；FCN .932/.061→.961/.045，支持此设置先验收益，未独立隔离类别重组与多标签。

正文说T2验证集，表注却称updated test set；§5.2又提four curated visual cases，而T3多行数值与T2重复，不能擅定统计集合。明确的外部评估在§5.3/T4：300图总TSR.897/FSR.103，已知字150为.962/.065，未知字150为.831/.140，不能以98.2%宣传外域或未知字表现。

正式T1 1322图/14766笔、10类/11维先验；此前核过[S007 HF加工版](../reviews/S007.md)1212图/6类/7值和[S016入口代码](../reviews/S016.md)固定6输出/未用prior参数存在差异，不能把它们当原主表复现。新官方tree2451eb75仍无完整训练/损失/匹配checkpoint。正式数据可用性写当时待发布，不覆盖后来HF制品；两个时间点分别记录。

## 尚未通过的图示验收与研究思路

本批Wiley正文/公式/数值读取成功；直接PDF下载403，图2/表页截图未成功，实际勾选列与框架布局尚未视觉核验。L184的五项书面回答明确写此缺项，**不把章节文字覆盖计成核心三遍完成**；继续保留在未完成队列，相关失败入口不反复重试。

女书论文可学“视觉/时间资源分别定义，先数据再基线”，但CER表达、静态渲染/真实文本和公开声明需精确。Stroke-Seg可学交叉瓶颈→模块→同backbone消融→外部未知字→错误分析的组织；Claim仍须保留匹配/统计集和实际制品缺项。

可证伪设计：固定信息/优化预算，类别重组×多标签×字ID/计数×BDLoss全因子；字ID重编号与gold/pred/noisy条件、同类/三笔交叉及未知字/书家留出，公开GT一对一匹配和阈值选择，再测实例/方向/次序及实际RGB可见事件。这些是未运行方案，尚无创新性闭环或模型复现。
