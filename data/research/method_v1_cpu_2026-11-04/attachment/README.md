# 汉字图文配对双路协同＋受约束代码渲染：CPU 研究原型

**日期：2026-11-04｜性质：仅方法接口和可识别性验证。**

此包针对 `lljjcc426/UMM` 的方案 v1.0 制作，不会自动写入 GitHub。仓库可对照版本：`713ab5b01dfb1cbcea93761d07218a261b9e12e7`。保持 S2 四模型36请求的冻结基线 `7c843c37a7d360b9482dd6104e3795966134450d`。当前未获 GPU/权重下载/模型训练的精确批准，均未执行。

## 已实际完成

1. **原始图文配对合同**：仅读取 `id / model_inputs.image / training_targets.description`；描述为五类有序笔型＋结果字；保留结果字但不把 `[EOF]` 当普通文本；没有读取部首、部件、语义或 evaluation-only 几何标签。校验空图、重复 ID、跨 split 的字符/图像哈希泄漏。
2. **四种模型接口冒烟**：`sft`、`global`、`cross`、`ordered`，包括视觉 patch 编码、文本前缀因果建模、局部 Cross-Attention、有序查询和图文全局对比头。用随机初始化的小网络检查真实张量前后向、梯度通路、未来目标泄漏；**没有预训练模型、没有训练、没有性能数据**。
3. **图像→绘制程序→CPU MP4 的执行后端**：将受约束 JSON DSL 安全解释为逐笔线条和曲线折线，累积已出现墨迹，FFmpeg 编码，重新解码 RGB 审核，拒绝越界/非法参数/任意代码执行。提供三个真实生成的示例 MP4。
4. **一个必要的信息边界测试**：在合成的“土”中，用相同笔画几何交换两条横线的真实出现次序。**粗类型序列一致、源终帧像素完全一致，但时间过程不同**。经 H.264 编码，两视频终帧二值墨迹一致，原始 RGB 允许少量压缩差异。
5. **13 项单元测试成功**，含严格的未来目标屏蔽、每个模态梯度、几何数据权限、代码渲染单调性和真实 MP4 解码。

## 执行

依赖：Python >=3.10、numpy、Pillow、torch（CPU）、opencv-python（用于解码审核）、系统 `ffmpeg`。

在解压后的目录运行：

```bash
python -m unittest discover -s tests -v
python -m method_v1.cli smoke-models
python -m method_v1.cli audit-pairs --pairs examples/synthetic_pairs.jsonl --root examples
# 已提供示例MP4，可运行新的输出文件路径：
python -m method_v1.cli render --program examples/tu.program.json --output results/tu_again.mp4
```

在真实 UMM 仓库上先**只读取现有训练导出**验证 schema（使用实际数据根目录，且不接触 `evaluation_only`）：

```bash
python -m method_v1.cli audit-pairs \
  --pairs /path/to/UMM/data/research/paired_strokes_v1/training_pairs.jsonl \
  --root /path/to/UMM/data/research/paired_strokes_v1
```

该审计命令不会训练；只验证一个导出文件，不改变 split、金标或请求列表。真实仓库的 192 对数据尚未在本容器上实测，因为当前容器不包含它们的原始图像文件。

## 实际范围限制

- 目前的 `TinyPairedStrokeModel` 仅负责**方法张量和损失接口验证**。`cross` 是因果文本→视觉局部注意力，**尚未实现 XMP-Font 完整双向融合、masked visual 重建及正式有序实例对齐损失**；`ordered` 加了顺序槽位查询，但其注意力不等于笔画分割或可信实例绑定。
- `forward(..., targets, character_unicode)` 中完整 `D` 仅由**独立全局配对辅助头**使用；图像到序列的预测只读取右移文本前缀，避免同位置看到答案。字符 Unicode embedding 是 CPU 合同替身，正式模型必须使用基座的真实 tokenizer/LLM。
- 本原型的输出头只预测**五类粗笔型 token＋EOS**。生成结果字符、细笔型、规范方向及精确曲线代码的模型训练接口尚未完成。后续须由真实预训练底座和可审计的训练方案支持。
- `demo_programs` 是合成的 **土/士** 几何样本，用于验证执行器与同序列歧义；**没有独立人审、没有模型输出**，不能作为对正式 Benchmark 的成绩或规范金标。
- 固定画布、黑字白底的折线演示已验证；复杂笔锋、全部规范汉字、真实字体/OOD、SVG 轮廓填充与贝塞尔路径仍需借助项目已有 `hanzi_video` / `scripts.p0.geometry` 源码扩展。不要以此包替换成熟的原仓库渲染代码。
- 真实程序生成（G2）尚未训练。若只给 `Image + D` 训练，能否准确预测独立的笔内路径仍是需要实验回答的问题；额外 SVG/实例标签必须独立登记为额外监督。

## 与当前仓库的建议衔接

将此包作为**隔离的 CPU 方法验证证据**归档（例如新实验目录），不要覆盖原 `hanzi_video`、`paired_strokes_v1` 或 S2 执行器。后续 Codex 应复用已有 `hanzi_video/render.py` / `scripts/p0/geometry.py`，将 DSL 解释层作为上游，同时确保从真实预测程序直接渲染，不从规范 catalog 替模型纠正笔序。详见 `CODEX_INTEGRATION.md`。

## 文件列表

- `method_v1/paired.py`：真实训练导出读取及隔离检查。
- `method_v1/fusion.py`：四种架构合同、正确右移的序列损失、全局配对辅助损失。
- `method_v1/program.py`：限制性代码 DSL、CPU 视频执行、独立 RGB 解码检查。
- `method_v1/cli.py`：CPU 执行入口。
- `examples/`：仅演示的图文配对样本、绘图程序和合成图像。
- `results/`：真实渲染的 MP4、自动生成的原始数值与检查报告。
- `tests/`：13 项实际运行的 CPU 测试。
- `EXECUTION_REPORT.md`：具体执行结果及下一阶段实验准入判断。
