# 实现、底座与资源方案

2026-10-26。状态：设计与官方接口核查；没有下载权重、运行GPU推理或测量训练显存。本仓库配置是研究计划，不是可直接运行的第三方训练配置。

## 1. 主底座与备选

| 角色 | 当前选择与依据 | 使用前检查 |
| --- | --- | --- |
| 主视频UMM | [Lance](https://github.com/bytedance/Lance)，`Lance_3B_Video`；已公开视频理解、生成和联合微调路径 | 权重/代码固定revision、共享参数、前缀条件支持、训练batch字段、完整成本 |
| 直接绘画视频对照 | [VideoSketcher](https://github.com/rhfeiyang/VideoSketcher)；计划+视频和AR变体 | 相同汉字数据适配；原生能力与微调后结果分开；不同底座规模不当完全等参 |
| 通用视频/外部组合 | 同一可运行视频生成器；独立VLM读取前缀并给同格式状态 | VLM版本、条件token和调用成本与共享模型对齐 |
| 规则/轨迹强基线 | 规范SVG+渲染；可用的在线轨迹模型+相同渲染 | 同样的规范与风格输入；不额外给其完整目标图后混入T协议 |
| 低资源研究备选 | BAGEL等图文模型做事件理解/下一关键帧 | 输出连续视频前必须补生成及验证；关键帧插值不等完整笔内过程 |

官方Lance README当前说明推理至少40GB显存、视频训练范围480p/12FPS；这不是本项目微调显存实测或单卡40GB训练保证。VideoSketcher官方建议14B推理48GB、AR约30GB、训练多卡80GB级；也只是作者环境建议。正式选型依据ENV-01实测及用户可用预算。

## 2. 已核官方训练接口

本轮读取[Lance train.md](https://github.com/bytedance/Lance/blob/main/train.md)，该文件blob SHA为 `4c5b44843ef6a744ec4698ebc6743aff23071ec1`；动态main只说明核查时内容，实际运行仍须锁定commit。

官方三个入口：`scripts/sft_lance_understand.sh`、`scripts/sft_lance_generation.sh`、`scripts/sft_lance_unified.sh`，均启动 `train/unified_train.py`。本地parquet包含v2t/t2v/v2v等任务；schema需按同revision的 `train_dataset.md` 实际转换。

官方明确 `VALIDATION_STEP=-1`，内置固定验证尚不支持。正式训练另建离线验证，不能设正数后声称已验证。理解任务注意 `VISUAL_GEN=False`；生成batch必须含相应latent字段。官方发布全量/分片训练入口不代表本项目LoRA和事件条件adapter已实现。

## 3. 最小实现顺序

1. **Smoke**：固定commit和权重，先用官方示例验证v2t、t2v及可用条件生成接口；保存输入、输出、环境和真实峰值。先推理后单步反传，再检查梯度和checkpoint重载。
2. **Data adapter**：从已审核manifest读取媒体/文字，构建v2t状态问答和t2v/v2v训练记录。单元测试禁止未来帧/evaluation_only进入prefix输入；记录标签padding、mask、FPS和真实时间戳。
3. **Independent evaluator**：实现稳定ROI/墨迹/实例绑定与三态判断；先通过EVAL-01，生成端和评分端不得共享渲染事件日志。
4. **Single-task fit**：16条开发样本过拟合检查；分别训练U-only/G-only。未收敛先查数据mask/时间/梯度，再谈共享冲突。
5. **Joint baseline**：同底座混合两类任务，固定冻结参数和loss归一；按实际有效token/视觉元素记录权重，不直接比较CE和MSE原数值大小。
6. **Event conditioning**：先JSON状态接原条件，再测试soft queries/空间条件；损失开关和状态来源逐项对照。
7. **Rollout**：推理时只给真实前缀；缓存只保存允许历史，避免使用训练teacher-forcing的未来target。前缀保持mask和跨片段latent续接属于待实现项，须验证接口，不能假定原Lance直接支持任意前缀冻结。

## 4. 原生视频限制与任务收窄

帧数、分辨率与codec下采样必须服从所选模型的有效配置。先采用官方验证过的短视频设置；把高频合成原视频降采样到原生FPS，单独测短笔信息损失。若多个模型原生设置不同，给native能力表及可比子协议，不通过插帧声称同等真实时间信息。

若只有I2V最后帧条件而无法输入完整prefix，理解器可先读prefix并输出状态，生成器读最后帧+状态；必须明确此信息路径。若需要新adapter支持多帧条件，它是实现/贡献的一部分，应与相同adapter的分离基线比较。

无法满足训练内存时，优先冻结codec、缩短片段、梯度累计、checkpointing，再考虑已实现的PEFT；每次改动做质量/成本对照。不能从3B活跃参数推算全部权重驻留或训练显存。仍不可行则停在评价/过程理解或关键帧任务，明确缩小论文范围。

## 5. 预算与运行记录

`configs/research/stroke_video_v1.json`中GPU型号/数量、总GPU时和模型revision初始为null；这表示正式运行前必须填写。用ENV-01的单位训练步/每视频实测量计算：

`estimated_gpu_hours = sum(actual_GPUs × measured_seconds / 3600)`

另计数据合成、教师标注、观察器、人评和存储。预估与实际分别保存，不能把估算称实测。开发阶段先少量字符/种子，正式阶段依据功效与预算冻结全量；不在看到结果后选择最有利seed。

每次复制[运行模板](../../templates/research_run.json)到独立run目录，填模型和数据revision、完整命令、git diff、冻结参数、trainable/total/active参数、曝光量、硬件和失败覆盖。指标初始null；完成后由原始输出和标签生成汇总。模型身份、提示改写和验证裁判不能随运行静默变化。

## 6. 本轮提供和未提供的代码

已提供计划结构/依赖/文件引用验证脚本与确定性单元测试。已有 `scripts/stroke_metrics.py`仅比较已标注ID序列，已有PX-01是模板辅助像素反例。**尚未提供完整数据适配器、通用RGB事件观察器、UMM事件条件模块或训练实现**；这些是上面的实验交付物。校验脚本通过不能把任何一项自动标记为模型实验完成。
