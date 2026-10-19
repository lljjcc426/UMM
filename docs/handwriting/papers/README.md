# 精读与核查卡片索引

## 四篇指定论文

[Timage、ORVOS、SC-CoIT、BoxTuning 精读](../../evidence/attachment_reviews.md)依据所提供的实际 PDF，分别说明版本、训练、实验、局限与笔顺研究的联系。公开版本另见[预印本分析](../../evidence/public_preprint_reviews.md)。

## 书写生成与过程建模

| 顺序 | 笔记 | 最重要的辨析 |
|---|---|---|
| 1 | [DP-Font](dp_font.md) | 笔顺条件、静态图、物理先验与实际过程的差别 |
| 2 | [DiffInk](diffink.md) | 潜在可生成性、少步质量、实现和评价信息 |
| 3 | [HTR Diffusion](htr_diffusion.md) | 实际记录与规范、几何与顺序、1000步与多尺度 |
| 4 | [Inverse Painting](inverse_painting.md) | 高层规划、区域执行、实际运行时间与绘画进度 |

以上继承2026-10-13/14研究笔记，不标为本次独立复现。

## 直接相关研究

- [UniCalli](unicalli.md)：统一书法识别与生成。
- [OnOff](onoff.md)：在线笔迹、物理渲染与离线外观。
- [DeepCalliFont](deepcallifont.md)：图像—序列双模态。
- [层级双域HTR](hierarchical_htr.md)：结构、順序和运动先验。
- [VidScribe](vidscribe.md)、[VTR-Bench](vtr_bench.md)：视频文字评测已有覆盖与未覆盖。
- [视频零样本过程例](video_zero_shot.md)：有逐笔演示但不能泛化为中文总体准确率。
- [OpenHandWrite](openhandwrite.md)：真实过程数据。
- [Text-Animator](text_animator.md)、[Video Text Preservation](video_text_preservation.md)：视频文字控制与合成训练。
- [CalliffusionV2](calliffusion_v2.md)、[CalliPaint](callipaint.md)：个性化与局部修复邻近工作。
- [Unwritten](unwritten.md)：在没有可见墨迹时测试真正的过程感知，作为发散评测线索。

每张卡片标注阅读层级。卡片存在不代表已经读完全文或已复现。

## 2026-10-19 实际来源核查与新增卡片

- [VidScribe 三遍阅读](vidscribe.md)：基准任务和11+2指标、数据及DPO实验；无规范笔顺视频生成主张。
- [Calligraphy Bench](calligraphy_bench.md)：88字符的Agent逐笔书法生成评分；核对事件裁判输入与全字严格率。
- [VideoSketcher](videosketcher_deep_review.md)：序列素描视频、Wan2.1训练/LoRA/AR，实现证据和待核主表。
- [Ketaba-OCR-LoRA](ketaba_ocr_lora.md)：NakbaNLP2026论文 + HF adapter + train.yaml，OCR跨书体和集成。
- [Wuji Writing VAM](wuji_vam_modelcard.md)：机器人数字写字的人类视频条件、视频+动作联合模型卡。
- [TextDiffuser/GlyphControl](static_text_neurips_baselines.md)：NeurIPS2023静态文字扩散前作；论文完整表格待补。
- [增量矩阵](../../evidence/scoped_literature_matrix_2026-10-19.md) 和 [无论文资源](../../resources/nonpaper_research_2026-10-19.md)。
