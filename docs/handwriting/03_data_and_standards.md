# 数据、笔顺标准与标注协议

## 数据层级

| 数据 | 本库定位 | 实际可以提供 | 不自动提供 |
|---|---|---|---|
| [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) | 规则渲染/参考路径 | 有序轮廓、粗略medians、部件 | 真实压力、艺术书体完整轨迹 |
| [Hanzi Writer](https://hanziwriter.org/docs.html) | 执行基线 | 依路径的动画、速度/颜色/停顿 | 生成陌生字形 |
| [CASIA](https://nlpr.ia.ac.cn/databases/handwriting/home.html) | 真实轨迹与风格 | 实际在线数据与文字 | 所有样本符合一个规范 |
| [OpenHandWrite](https://link.springer.com/article/10.3758/s13428-026-03001-4) | 笔画级时间对照 | 采集与分析工具；具体字段依文档 | 自动规范金标准 |
| [Mobao/Moyun](https://arxiv.org/abs/2410.07618) | 静态艺术风格 | 字图、样式条件 | 每幅图的真实历史 |
| [UniCalli数据](https://arxiv.org/html/2510.13745v2) | 列级风格/布局 | 字符、边界框、书体等 | 每一笔的时间戳 |
| [官方笔顺规范](https://www.moe.gov.cn/jyb_sjzl/ziliao/A19/202103/W020210318300204215237.pdf) | 明确所用规范来源 | 官方PDF§1–5确认8105字及笔顺含次序/方向；前12页已读 | 全部8105条尚未逐字核查；无真实采样时间 |

不在本仓库分发字体、数据集或论文全文。代码许可与权重、衍生字体数据许可不同，应分别审查。

## 建议标注字段（设计，不是现成数据）

`sample_id, character_text, script, locale, standard_ref, allowed_orders, reference_style_id, writer_id, source_domain, stroke_events, timestamps, pen_down, coordinate_system, observed_or_generated, visibility, annotation_provenance`。

对每个笔事件：
- 字符ID/笔画ID；
- 起止时间、方向、中心线或已知参考轨迹；
- 合法前缀条件；
- 是否发生新增墨迹；
- 由于遮挡/帧率无法判断时明确`unobservable`，不填错误或正确。

## 划分

至少区分未见字符、未见组合、未见书写者、未见艺术风格、未见渲染器、超出训练长度。未见句子不等于未见字形。
静态模板合成的视频若训练与测试使用相同生成管线，容易测到模板适配而非真实泛化。

## 规范与书体

先固定简繁、地区和书体，再定义允许集。标准楷书可采用严格序列；允许连笔的书体应专家指定哪些合并与顺序变体有效。不能把“永字八法”当作“永字有八笔”的笔画计数标签。

## 真实时间与压力

程序路径通常只有几何；按弧长匀速播放是合成假设。真实时间、速度、压力、笔尖姿态不能从一个渲染参数自动得到。
[OnOff](https://arxiv.org/html/2608.03198v1)使用速度代理压力；检验该假设应使用实际传感记录，而不是以另一个相同代理为真值。

2026-10-20资源协议更新：[GF0023定义](../reviews/R06.md)、[OpenHandWrite实际字段/单位](../reviews/R07.md)、[BCSS加工版与论文差异](../reviews/S007.md)已逐项记录。BCSS六类mask不提供逐笔时间身份，标准1–5串也不能区分所有同类笔画交换。

## 教程步骤图与严格笔事件

UEval含art步骤图任务及题级rubric（本批U22）。它是绘画步骤生成评价的已有前史，拼格/多图步骤不等连续RGB视频；规范笔顺仍要strokeidentity/方向/顺序/penstate/遮挡及终态一致，不能只用“步骤完整/可读”文字judge。
