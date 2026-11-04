# 图文方法CPU验证工具

本目录接入用户提供的2026-11-04 CPU原型。实际数据为S0–S1原有192条训练导出；只检查数据、张量、梯度通路和受约束程序执行。没有预训练模型、参数更新或能力分数。

从仓库根目录运行，不覆盖已有输出目录：

```bash
.venv/bin/python -m method_v1.cli audit-pairs \
  --pairs data/research/paired_strokes_v1/training_pairs.jsonl \
  --root data/research/paired_strokes_v1

# 不依赖torch：数据、RGB输入与原SVG逐像素重建核对。
.venv/bin/python -m method_v1.cli integrate \
  --dataset data/research/paired_strokes_v1 \
  --output private/method_cpu_data_check

# CPU torch环境：另外检查四种随机模块的真实RGB特征与首批梯度；优化器step=0。
/path/to/cpu-python -m method_v1.cli integrate \
  --dataset data/research/paired_strokes_v1 \
  --output private/method_cpu_features_check --features
```

本机本次复用了同仓库已有`private/ltx_local/venv312/bin/python`中的torch2.8.0，只执行CPU代码，没有运行LTX或加载其权重。Linux CI用独立Python3.12环境安装根目录requirements及[可选CPU依赖](requirements-cpu.txt)，torch从官方CPU wheel索引安装，不向基础工程环境加入torch。

```bash
/path/to/cpu-python -m unittest tests.test_method_v1 tests.test_method_integration -v

.venv/bin/python -m method_v1.cli render \
  --program data/research/method_v1_cpu_2026-11-04/attachment/examples/tu.program.json \
  --output private/tu_shared_renderer.mp4
```

`paired.py`仅读窄训练导出；`batches.py`产生原尺寸RGB和监督。完整描述保留终字；CPU的9类粗笔型/PAD/MASK/BOS/EOS词表用于接口检查，Unicode embedding只进入辅助全局配对分支。当前小网络没有预测终字的解码器，不能作为真实Image→完整Description SFT。正式基线必须接入选定底座自己的tokenizer、EOS和完整描述监督。

`fusion.py`的四种模式共享随机视觉/因果文本模块，添加从图像patch网格计算的二维位置；这不提供标准笔画位置。跨注意力和有序槽位仍为接口，不等于逐笔绑定、分割或完整双向融合。全局文本辅助头可在训练检查中读完整D，预测分支只读因果右移前缀；图像推理接口不接收D或终字。

`program.py`将原始JSON程序转换为仓库`stroke_geometry`和共享单调mask执行器。它没有目标字查表或规范计划纠正。程序示例和源SVG上界只用于CPU执行器对照，不能作为G2模型生成成绩。实际验证、限制、GPU申请及后续顺序见[接入报告](../docs/research/paired_strokes_v1/method_cpu_integration_2026-11-04.md)。
