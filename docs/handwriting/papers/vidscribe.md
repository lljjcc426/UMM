# N04 · Beyond Legibility: Benchmarking Visual Text Rendering and In-Place Editing in Unified Video Generation (VidScribe)

核查日期：2026-10-15；层级：`primary_sections_read`。并非每篇都完成全部附录阅读或代码复现。

## 来源与版本
- https://arxiv.org/html/2609.36598v2
版本：arXiv v2 2026-10前公开
阅读范围：§3基准与指标、§4结果、因素附录

## 作者声明
作者主张：用可读性以外的结构、持续性、控制与编辑指标系统评测视频文字。

## 输入—机制—输出
803个人工核查样本；12因素；68%英语/32%中文；T2V/R2V/I2V/V2V；11公共指标和2编辑探针；含handwriting_stroke演化。

## 针对问题
最终读得出来仍可能形变、漂移、编辑失配，单一OCR无法覆盖。

## 目前可支持的结论
已测试11个系统并包含手写演化因素；论文A1/A2相关性较弱，提示读对与结构对要分开测。

## 边界与候选缺口
【边界】A2字形拓扑并非逐笔规范序列、方向和接触评分；协议并非每例都从完全空白开始。【推断】不能再声称没有中文/手写因素的视频文字基准。

## 应怎样放进研究对照
该记录不是“论文质量评价”。是否用作主要基线，取决于输入信息、输出对象和评价目标是否相同。
请与[最新重点复核](../01_focused_update_2026-10-15.md)和[实验协议](../../experiments/benchmark_protocol.md)一起阅读。
