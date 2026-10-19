# 第七批：规范、数据字段与实际实现

本批沿论文之外的模型卡、HF配置、SVG格式、训练代码及OSF制品追查。阅读范围逐条记录在笔记中，未运行外部模型/训练脚本，未下载权重。GitHub blob标识的是文件内容；HF revision标识该发布版本，二者不混称commit。

## 静态笔画类别与时间事件

[Stroke-Seg正式论文](../reviews/L184.md)是本批从BCSS资源追引补录的独立论文，配套[HF数据S007](../reviews/S007.md)和[实现S016](../reviews/S016.md)保留资源身份，不重复计作论文。

| 协议 | 类别与先验 | 数据/结果范围 | 必须保留的差异 |
| --- | --- | --- | --- |
| 论文§3–5 | 10类、character-ID+10计数的11维先验 | 872训练/150验证、外部300图 | Table3 TSR .982来自验证集；外部.897，未知字.831 |
| HF固定revision | 6类mask、id之后7个整数 | 1082内部+130外部，后者只有输入图 | 类别映射/加工步骤未厘清，不能套用论文结果 |
| 公开FCN/DeepLab入口 | FCN未使用prior_feat；DeepLab硬编码6输出 | 示例源码，没有主表checkpoint/完整训练配置 | 参数名称或目录名称不足以证明实际使用先验 |

HF说明称每张有per-stroke mask，但加载段明确为每个stroke class一通道。类别分割不自动提供每次落笔身份、方向或时间。同类相交仍需实例恢复；TSR不是笔顺准确率。

正式PDF Table1的笔画分组计数相加为14766；repo/HF称10653。两者并列保留，尚未确定版本差异或排版错误。Table2的updated-test标题与正文validation称谓也保留。FSR以GT笔数为分母，不能一概当作1−TSR。BCE+Dice的组合不直接证明新损失首创；仍需追查既有组合损失。

## 独立素描扩散实现的可定位问题

[ark60/sketch-diffusion](../reviews/S014.md)的固定notebook文件中：

1. 非末笔的每个点被编码为pen_up，解码每点结束一笔，渲染又跳过单点。对两条多点线段进行手工推演即可看到第一条丢失，无需训练模型。
2. 从其前向过程`x_t = sqrt(a_bar) x_0 + sqrt(1-a_bar) eps`移项，应有`x_0 = (x_t - sqrt(1-a_bar) eps) / sqrt(a_bar)`。所读反向代码第二项缺少`1/sqrt(a_bar)`。结论限定到该文件，不能外推整个DDPM方法或其他同名论文。
3. early stopping的validation和最终评估都读取test索引。训练MSE还包含padding；记录的train loss除累积步数、val不除，曲线数值不可直接比较。

README的28.4/.0234是示例文件内容。notebook保存的cat/bus/rabbit作者运行输出分别是FID260.4142/267.3336/267.6711与KID.250451/.276484/.265711。未独立复现；小样本FID/KID也不检验笔画顺序。完整序列采样后每笔50ms渲染GIF，不证明在线因果生成。

## 可复用配置与缺失的执行证据

- [Wuji S008](../reviews/S008.md)：视频与动作MoT、54D动作、数字0–9、12500步和训练配置已核。20样本快照不含机器人成功率；联合/分离的匹配对照缺失。
- [Qari S011](../reviews/S011.md)：实际adapter启用DoRA和RSLoRA。blind CER改善、WER变差；量化/秩/数据/基座必须受控后才能归因。
- [VidSketch S015](../reviews/S015.md)：当前训练入口采用MSE，README中的DPO需要定位另一路径及checkpoint。配置名、硬编码adapter路径、许可表述冲突均有记录。
- [CASIA HF S012](../reviews/S012.md)：实际只有image/text，52160离线行不能直接充当在线轨迹。
- [SceneDAPR S013](../reviews/S013.md)：总体绘画时间与笔画顺序不能补成逐点时间；公开坐标解析器仅适配其简单路径，复杂SVG可能被跳过。

## 规范与人类运动分别提供什么？

[GF0023—2020 R06](../reviews/R06.md)明确笔顺包含次序与方向，范围8105字；官方PDF定义和初始示例已读，全部字表未逐字核查。粗1–5笔形串不能区分所有重复同类笔画交换。

[AnimCJK S009](../reviews/S009.md)与[KanjiVG S010](../reviews/S010.md)提供可控路径和地区/变体结构。逻辑一笔可能拆多个SVG路径；动画速度、Bezier参数与真实速度不同。许可和日本/中国/台湾规范分别保留。

[OpenHandWrite论文N07](../reviews/N07.md)与[OSF制品R07](../reviews/R07.md)提供200Hz真实手写测量和多层统计。小xlsx是字符层聚合摘要，不是原始50400轨迹；R脚本空间换算`lpmm=200`和采集频率200Hz是两种量纲。原始采集包、全部附录及全部统计代码仍待审。

研究实验应同时报告：规范事件合规、RGB中可观察的过程、人类运动分布、真实执行约束。每一层都需要对应真值和匹配输入条件；单个静态分数无法代替整条证据链。
