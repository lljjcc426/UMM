# TextDiffuser 与 GlyphControl｜CCF-A / NeurIPS 2023 静态文字扩散生成前作

本卡只根据两篇官方 NeurIPS 2023 发表页原始摘要进行**第一遍+初步第二遍**分析；训练超参、结果精确值、完整主表与消融待读取 PDF，不能标为全文精读。

## 1. TextDiffuser: Diffusion Models as Text Painters

[NeurIPS 2023 主会发表页面](https://papers.neurips.cc/paper_files/paper/2023/hash/1df4afb0b4ebf492a41218ce16b6d8df-Abstract-Conference.html)；作者 Jingye Chen 等。

**Problem**：文本提示到自然图时，视觉文字内容、位置及背景结合不稳定。**Motivation**：传统自由生成缺少对文字布局和字符边缘的显式结构约束。**Contribution**：两阶段“layout transformer→layout-conditioned diffusion”；构建 MARIO-10M，含约 1000 万 image-text 对与 OCR recognition、detection、字符 segmentation 标注；MARIO-Eval 用于视觉文字图像评估。**Method**：输入 prompt/可选 template，抽关键词预测布局，扩散模型根据布局和 prompt 生成静态带字图，也覆盖部分 image inpainting。**实验**：作者报告实验及用户研究改善可读与布局；本轮只核到发表摘要，无准确 OCR/FID 数值、训练批量、消融表，均待查。**Limitations/Insights**：输出**图片**，其文字像素细节控制可用于“逐笔序列的最终画面”条件，但不能评价书写历史。下一步以布局/字形相同而先后不同的过程视频测试其静态优势能否转化。

## 2. GlyphControl: Glyph Conditional Control for Visual Text Generation

[NeurIPS 2023 主会发表页面](https://proceedings.neurips.cc/paper_files/paper/2023/hash/8951bbdcf234132bcce680825e7cb354-Abstract-Conference.html)；作者 Yukang Yang 等。

**Problem**：Stable Diffusion 一类通用图片扩散模型对复杂文字内容、位置和尺寸控制不够。**Motivation**：纯文字条件缺少对每个字实际轮廓的强约束。**Contribution**：以 glyph 图作为条件，借用现成 Stable Diffusion 生成准确文字；公开 LAION-Glyph 训练数据集；评估 OCR/CLIP/FID。**Method**：文字与字形/位置掩码输入→字形条件融合到图像扩散→静态文字图。**实验**：官方摘要声称在 OCR、CLIP、FID 上优于 DeepFloyd IF；精确数值、置信度、所有对比条件与消融待核。**Limitations/Insights**：字符 glyph 控制可帮助每笔形状完整与布局对应，但**尚未生成或验证真实笔顺时间轴**。适合被作为按相同字形条件进行视觉执行的 static oracle 控制，不宜当作视频生成基线直接排序。

## 3. 与已经收录的 AnyText / AnyText2 区分

本仓库主目录已有 **AnyText2**（B04）与 AnyText（L025），这些同样主要解决静态文字图像可读性、位置和编辑。TextDiffuser 的布局先验、GlyphControl 的可明确绘制字形控制、AnyText2 的字形与排印适配都能启发汉字美术输出，但不能孤立宣称“加 glyph 条件让笔顺正确”。

## 4. 论文写法和技术路径

- Introduction：给出 OCR 错、字符位置错等可观察失败，继而引入与该失败对应的布局/字形显式控制。
- Method：分别说明文本布局表示、条件编码器、生成主干与 loss/训练阶段。
- Experiments：严格对齐 OCR、CLIP、FID 的定义和数据切分，并增设实际轨迹事件的严格指标。绝不根据最终字符准确率推导规范书写的逐事件准确率。
- 可证伪假设：给 VideoSketcher 或 Wan 视频分支相同的字形 mask 与相同采样预算，glyph 条件可改善完整率，但只加静态 mask 对乱序事件的修正幅度应由实验判断。比较固定 glyph+无轨迹、真实轨迹、预测轨迹与规则渲染。

**一句话总结**：两个 NeurIPS 2023 工作均为静态图文字扩散的核心前作，有直接结构控制价值；对时间执行的泛化尚需独立验证。
