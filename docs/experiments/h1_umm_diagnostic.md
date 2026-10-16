# H1：UMM本体的实际过程理解诊断

**主实验使用Janus-Pro-1B，当前结果尚不支持H1。** 已完成33道短序列题及一次33题选项位置对照。模型有明显的首选项偏向，仅空白图题在两种选项排列下都答对。接下来应继续定位理解与回答接口的问题，H2、H3尚未启动。

## 1. 为什么选择这个底座

[Janus-Pro-1B官方模型卡](https://huggingface.co/deepseek-ai/Janus-Pro-1B)和[官方实现](https://github.com/deepseek-ai/Janus)明确提供统一的理解与图像生成能力：理解使用SigLIP编码器，生成使用视觉token及解码器，两条路径共享语言Transformer。

本次加载完整UMM，运行记录包含`vision_model`、`aligner`、`gen_vision_model`、`gen_aligner`、`gen_head`、`gen_embed`和`language_model`。只调用理解路径；未添加外部理解器，未训练，也未生成图像或视频。

发布名称为1B，完整模型实际加载约20.89亿参数。原始bfloat16权重约4.18GB，适合在本机尝试。官方列出的序列长度为4096；每图384×384、576个图像token，因此采用最多4图的短序列。模型配置中的更大位置编码上限没有被当作已验证的训练上下文。

它是图像级UMM，源码支持多张图片的标记与嵌入。本实验借此输入短帧序列，属于H1的本机起点；原生视频UMM和后续生成底座仍需单独选择与验证。Qwen3-VL的既有结果保存为[外部VLM辅助诊断](h1_diagnostic.md)，不用于判定UMM的H1，也不与本次不同协议的分数直接比较。

## 2. 测量内容

沿用规则绘制的“三”“十”，拆成观察、判断和下一动作。全部问题只要求选择一个选项，不要求同时生成大量状态字段。

| 层次 | 问题 | 数量 |
|---|---|---:|
| 观察 | 哪些具体线条已出现 | 8 |
| 观察 | 相对完整参考，哪些已完成、哪些只有部分 | 6 |
| 观察 | 各笔实际出现顺序 | 4 |
| 观察 | 笔内实际增长方向 | 2 |
| 判断 | 相对给定规范，第一次顺序错误在哪里 | 4 |
| 判断 | 开始新笔时，上一笔是否写完 | 2 |
| 判断 | 只有终态时，能否承认顺序不可确定 | 2 |
| 下一动作 | 给准确文字状态，选择继续、下一笔、结束或停止 | 5 |

顺序题保留空白和每笔结束时的累积画面；方向题另外保留相邻增长帧；提前换笔题保留参考及换笔前后状态。不会用只有终态的图片评价实际历史恢复。动作题隔离视觉读取，当前没有测从实际画面到动作的完整闭环。

完整输入、选项、标签及帧索引见[umm_pilot_v1](../../data/h1/umm_pilot_v1/README.md)。这是两个字的受控诊断，没有训练集、独立留出集或风格泛化评价。

## 3. 配置与结果

- 运行日期：2026-10-16；Apple M5、16GB统一内存、macOS 26.6。
- 官方源码提交：`1daa72fa409002d40931bd7b36a9280362469ead`。
- 权重：[ModelScope官方仓库](https://modelscope.cn/models/deepseek-ai/Janus-Pro-1B)，版本`bc299531bae896710f9ea16e7d4d8ea5719290f6`。
- PyTorch 2.7.1、Transformers 4.46.3、bfloat16、MPS；冻结全部参数。
- 每题独立上下文；贪心解码、种子0、最多64个输出token；实际输入182—2481 token，未超4096限制；每个条件只运行一次。

原定主评分只接受单字母，可带空白或句号。看到回答常附带选项文字后，另增**内容评分**：只接受单字母，或字母与该选项完整原文完全对应的回答。文字不对应、歧义或其他输出不修补。内容评分是事后分析，原始预测及主评分保持不变。

| 项目 | 原排列严格评分 | 原排列内容评分 | 移位排列内容评分 |
|---|---:|---:|---:|
| 可见实例 | 1/8 | 1/8 | 3/8 |
| 完成程度 | 0/6 | 1/6 | 1/6 |
| 实际顺序 | 0/4 | 2/4 | 0/4 |
| 首次顺序错误 | 0/4 | 0/4 | 2/4 |
| 笔内方向 | 0/2 | 0/2 | 1/2 |
| 提前换笔 | 1/2 | 1/2 | 1/2 |
| 准确状态下的下一动作 | 1/5 | 1/5 | 1/5 |
| 终态顺序不可确定 | 1/2 | 1/2 | 0/2 |
| 合计 | 4/33 | 7/33 | 9/33 |

移位排列的严格评分为6/33。四选一均匀猜测期望为25%；原排列始终选A为9/33。各题共享少量源案例，不能把总分当成独立样本统计，也不能仅凭某项两道题答对一道就认定掌握了该能力。

首轮33题中29次以A开头，因此增加一次[选项位置对照](../../data/h1/umm_position_control_v1/README.md)：图片、问题文字、选项含义和推理设置不变，仅把选项循环移动一位。移动后仍有29次以A开头，33对中29对首字母不变。**内容评分下，只有空白图这一题在两种排列中都正确。** 两组同终态正序/换序对没有稳定恢复实际顺序。

具体例子：

- 空白图中，“无”从A移动到B，回答也从A变为B。这道题能随内容移动。
- 上→下→中的换序视频，原排列A恰为正确顺序，回答附带了该顺序；正确选项移到B后，回答仍以A开头，文字也错误。
- 竖→横的视频，正确顺序从A移到B，回答转为A项“无法确定”。
- 准确状态已说明上横只写了一半，原排列选择A项“开始中横”，移动后选择A项“停止并处理已发生的错误”；均未选择继续上横。

这些现象显示当前结果受选项位置与指令遵循影响。尚不能把低分单独归于时序视觉编码，也不能把偶然答对解释为过程理解。所有原始输出、解析状态及失败均保留。

| 条件 | 配置 | 原始回答 | 逐题及汇总评分 |
|---|---|---|---|
| 原排列 | [run.json](../../results/h1/janus_pro_1b/umm_pilot_v1/run.json) | [predictions.jsonl](../../results/h1/janus_pro_1b/umm_pilot_v1/predictions.jsonl) | [scores.json](../../results/h1/janus_pro_1b/umm_pilot_v1/scores.json) |
| 选项移位 | [run.json](../../results/h1/janus_pro_1b/umm_position_control_v1/run.json) | [predictions.jsonl](../../results/h1/janus_pro_1b/umm_position_control_v1/predictions.jsonl) | [scores.json](../../results/h1/janus_pro_1b/umm_position_control_v1/scores.json) |

两批推理累计约64.8秒，不含下载、环境准备和模型加载。回答后采样的MPS驱动分配最大值约7.67GB，不能当作整机内存峰值。模型确实能在本机运行，但尚未显示可用于可靠反馈控制的理解能力。

## 4. 下一步仍聚焦H1

1. **先排除选项位置主导。** 用同一小组过程事实比较不带选项的短自然语言、固定状态字段和选项移位。继续保存全部回答，不挑最好的提示作为最终成绩。
2. **把观察与判断分开建立可靠接口。** 分别确认具体笔画位置、完成程度、相邻帧新增部分，再问规范违规与下一动作。准确文字状态仍答错时，应先定位规则应用或回答接口的问题。
3. **再恢复完整时序。** 必须在相同终态、不同实际顺序的成对输入上同时正确，并在选项或表达方式改变后保持结论，才能扩大到点、折、包围和更多字。
4. **核查底座适配范围。** 当前是一个小型图像UMM在中文短序列上的结果。后续选择支持视频理解的UMM及合适计算资源，不能将Janus-Pro-1B的表现外推到所有UMM。

H1得到可靠支持后，再开展理解帮助生成的H2与统一学习收益的H3。本实验不提供这两层结论。

## 5. 复现

建议使用独立Python环境，避免与外部MLX对照的Transformers版本混用。官方源码和权重均放入已忽略的`checkpoints/`，不上传模型文件。

```bash
python -m venv checkpoints/Janus-env
checkpoints/Janus-env/bin/python -m pip install -r requirements-h1-umm.txt
git clone https://github.com/deepseek-ai/Janus.git checkpoints/Janus-source
git -C checkpoints/Janus-source checkout 1daa72fa409002d40931bd7b36a9280362469ead
```

将上述固定版本的官方权重放到`checkpoints/Janus-Pro-1B`，保留配置、处理器、tokenizer和`pytorch_model.bin`。本次因Git传输中断，官方Python源码通过GitHub API按同一固定提交下载；模型与源码均未修改。

```bash
checkpoints/Janus-env/bin/python scripts/h1_umm_dataset.py
checkpoints/Janus-env/bin/python scripts/h1_run_janus.py --output results/h1/janus_pro_1b/new_run
checkpoints/Janus-env/bin/python scripts/h1_score.py results/h1/janus_pro_1b/new_run/predictions.jsonl --dataset data/h1/umm_pilot_v1
```

选项位置对照的构造与运行命令见对应数据说明。使用新的输出目录保留每次尝试；本版本数据不根据结果修改。
