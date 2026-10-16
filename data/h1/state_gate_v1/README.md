# 线条存在与完成程度诊断

本目录为本项目自行生成的静态线条诊断数据，不含笔顺训练标签。协议、门槛和能力边界见[实验说明](../../../docs/experiments/h1_state_gate.md)。

- `cases.json`：156个基础案例的路径、当前进度、目标实例和集合；开发26例、留出130例。
- `images/`：完整参考在上、当前画面在下的组合图，以及仅保留当前画面的对照。上、下两部分没有时间先后含义。
- `inputs.jsonl`：三种信息条件、两类问题、两种等价问法和两种输出形式，共3744行；推理只读取此文件和图像。
- `labels.jsonl`：评分用标签，推理脚本不读取。
- `build.json`：随机种子、独立组数及数据构建信息。
- `text_controls.jsonl`、`text_control_labels.jsonl`：另外手工编写的3个简单文字状态、12个问法对照，用于区分直接状态读取与数值长度判断；不计入156个图形案例或正式门槛。
- `text_controls_en.jsonl`、`text_control_labels_en.jsonl`：上述12题的英文对照，用于检查语言和任务接口的影响；同样不作为独立新增案例。
- `basic_visual_controls.jsonl`、`basic_visual_control_labels.jsonl`及`images/basic-*.png`：4张整幅简单图、16题英文存在/数量问答，用于检查基础图像输入与回答能力。不要求上下分区、参考匹配或完成程度判断，不计入156个主诊断案例。使用`python scripts/h1_state_gate.py build-basic-control`重建。
- `simple_relation_controls.jsonl`、`simple_relation_control_labels.jsonl`：从已有开发集取10个单线与参考对照案例，改用40题简短英文yes/no问题，分别询问当前是否有线、是否已覆盖完整参考。它不包含多实例定位或未知类别；使用`python scripts/h1_state_gate.py build-relation-control`重建。
- `region_controls.jsonl`、`region_control_labels.jsonl`：保持同一存在问题和当前像素不变，仅移除或保留上半部参考，共40题。提示不宣称上半部一定存在参考，用于检验参考干扰；使用`python scripts/h1_state_gate.py build-region-control`重建。

运行 `python scripts/h1_state_gate.py build` 可重建。同一几何组的全部变体归入相同集合。当前只使用开发集调整接口，留出集尚未运行。相同形状家族和渲染器在两集合中均存在，因此不能声称跨汉字、字体或来源泛化。

历史运行保留各自输入快照；文字条件在开发阶段补充了路径对齐及长度关系，旧结果应使用对应快照解释。
