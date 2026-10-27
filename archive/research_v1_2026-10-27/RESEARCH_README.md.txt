# 当前研究协议工作区

版本：stroke-video-v1，2026-10-26。状态：实施设计，尚无新模型结果。

按顺序阅读：[研究路线](../project/ROADMAP.md) → [任务和方法](task_and_method.md) → [数据协议](data_protocol.md) → [评价协议](evaluation_protocol.md) → [实现方案](implementation.md) → [逐实验矩阵](../project/EXPERIMENTS.md)。

[计划配置](../../configs/research/stroke_video_v1.json)、[实验登记](../../data/research/experiments_v1.json)、[运行模板](../../templates/research_run.json)共同构成执行入口。配置是研究计划，不能直接传给 Lance/Wan 的训练脚本；需要按[实现方案](implementation.md)编写并核验数据适配器。

## 与已有材料的关系

[跨论文综合](../reading/synthesis.md)、[笔顺专项](../handwriting/05_stroke_order_umm.md)、[数据与规范](../handwriting/03_data_and_standards.md)、[最小方案](../experiments/stroke_order_pilot.md)、[早期评测协议](../experiments/benchmark_protocol.md)继续保留，提供研究论证与历史依据。本目录将其收敛为当前实施协议；出现实施参数冲突时采用本版本并在运行记录固定。

## 四种不同的完成

文献核心阅读、代码／配置校验、评价器校准、模型实验完成分别记录。现有[PX-01](../experiments/process_probe.md)为八个受控像素案例，其模板辅助观察器未经过真实自由视频校准。新版研究协议、样本规模和成功门槛均不得冒充已建数据集或实测结果。

原始视频和大数据不存本目录；只存清单、版本、授权状态、校验和、标注说明和汇总证据。
