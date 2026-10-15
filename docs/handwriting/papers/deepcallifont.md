# N03 · DeepCalliFont: Few-shot Chinese Calligraphy Font Synthesis by Integrating Dual-modality Generative Models

核查日期：2026-10-15；层级：`primary_sections_read`。并非每篇都完成全部附录阅读或代码复现。

## 来源与版本
- https://arxiv.org/html/2312.10314v1
版本：AAAI 2024；arXiv首发2023
阅读范围：摘要、引言、方法相关章节

## 作者声明
作者主张：图像与书写序列双模态协同改善少样本书法合成。

## 输入—机制—输出
图像/轨迹生成分支，特征重组与跨模态约束，渲染一致性；先做单模态预训练。

## 针对问题
单模态方法难兼顾笔画细节与整体风格，不同书体的笔画与顺序存在差异。

## 目前可支持的结论
已有图像—序列双分支的中文书法生成；不能把联合两种表示作为首次贡献。

## 边界与候选缺口
【边界】字体合成、轨迹与完整写字视频仍不同；书体有效笔画划分不能强用一套楷书规则。

## 应怎样放进研究对照
该记录不是“论文质量评价”。是否用作主要基线，取决于输入信息、输出对象和评价目标是否相同。
请与[最新重点复核](../01_focused_update_2026-10-15.md)和[实验协议](../../experiments/benchmark_protocol.md)一起阅读。
