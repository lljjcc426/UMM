# H1 单项诊断补充

此版本在查看`pilot_v1`首轮结果后制定，用于定位失败原因。它属于后续探索，不作为独立测试集，也不替换或合并首轮成绩。首次运行前固定全部30个输入，运行后不修改这些提示和标签。

沿用[pilot_v1](../pilot_v1/README.md)原始图片和案例，采用更短提示、每次一个问题：

| 条件 | 数量 | 所要区分的问题 |
|---|---:|---|
| `seen_no_reference` | 4 | 只给当前图，能否找出可见实例？ |
| `seen_with_reference` | 4 | 同样四个案例增加完整参考图，是否仍只描述当前图？ |
| `completion_only` | 4 | 参考图＋当前图，能否区分完整与部分笔画？ |
| `order_only` | 4 | 去掉参考图，只看全部过程帧，能否还原“三”“十”的正序和换序？ |
| `direction_only` | 2 | 正向与反向上横，只看第一笔的过程帧，能否识别方向？ |
| `oracle_judgment` | 5 | 给准确状态，单独判断合规与违规 |
| `oracle_action` | 5 | 给准确状态，单独选择动作及目标 |
| `static_order_unknown` | 2 | 只有终态时，能否承认实际顺序不可确定？ |

`order_only`与首轮同时改变了提示长度、回答字段数量和参考图条件，其结果差异不能单独归因于其中一个因素。两种`seen`条件可用于局部配对比较，但样本仅4个。文字状态已给出实际顺序、方向和提前换笔标志，只检验规则应用，不测视觉读取。

`inputs.jsonl`保存实际输入；`labels.jsonl`中的`score_fields`指定本次需要的字段。缺失、错误类型和非JSON输出均计错；集合字段忽略排列。推理脚本只读输入文件。

复现：

```bash
python scripts/h1_focus.py
python scripts/h1_run_mlx.py --inputs data/h1/focused_v1/inputs.jsonl --output results/h1/qwen3_vl_2b_4bit/focused_new_run
python scripts/h1_score.py results/h1/qwen3_vl_2b_4bit/focused_new_run/predictions.jsonl --dataset data/h1/focused_v1
```
