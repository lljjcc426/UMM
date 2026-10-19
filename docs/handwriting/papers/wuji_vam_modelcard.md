# Wuji Writing VAM｜无独立论文的机器人示教书写：视频与动作联合预测权重

来源：[作者 HF 模型卡 knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819](https://huggingface.co/knightnemo/wuji-writing-vam-ti2v5b-30l-0522-0819)，核查日期 2026-10-19。仅官方 model card / metadata，**未检查全部训练源码、下载 11.54GB 权重、执行推理或核对论文**。HF 显示 license: other，使用前单独核许可。

## 第一遍｜三句话

这是一套人类参考视频条件的机器人毛笔/书写控制预测系统制品。以 Wan2.2-TI2V-5B 的视频 DiT 和单独 action_dit/ActionMoT 结构联合预测机器人三视角未来视频与 54 维动作。模型卡只报告数字 0–9 的示教采集与一次训练期间验证快照；不能声称该权重已解决中文规范笔顺、真实机器执行或完整视频模型排行。

## 第二遍｜七字段与五问

**研究问题**：从人类第一视角书写演示与机器人当前多摄像头/运动状态预测短期机器人动作和视觉结果，用于模仿式机器人书写。

**原始数据**：本地 wuji-writing 数据包；teleop 487 episodes，ego_ref 896，训练 439，验证 48；字符范围 **数字 0–9**。视频来源不同：人类参考 observation.images.head；机器人目标三视图网格（stereo_left、cam_left_wrist、cam_right_wrist）。作者说明按 task_index 数字匹配序列，**不作逐帧/几何对齐**。

**模型结构**：作者称 Wan2.2-TI2V-5B 视频 DiT + action_dit.* 动作流，视频及动作联合训练。为完整运行需单独安装匹配 VAM 代码和原始 Wan2.2-TI2V-5B 基座、文本编码器、VAE 与 tokenizer。不是直接 Transformers 单模型生成接口。

**输入→输出**：
- 输入：人类 egocentric 参考视频、当前机器人三视角 anchor frame、文字 prompt、54 维本体感觉 state。
- 输出：短期机器人三视角视频 rollout 与每步 54 维动作 targets。
- 固定条件：分辨率 384×320；raw target 33 帧、目标 9 帧；reference 69 帧；action horizon=32；action_dim=54，proprio_dim=54。
- 训练配置摘要：mask_variant=v2，full_ref=true，bridge_exclude_ref=true；checkpoint step 12,500。action_stats 来自 438,986 teleop action rows。

**作者报告的验证快照（非完整部署评估）**：
- step 12500，20 / 39326 samples，loss 0.278802（video 0.146057、action 0.132745）。
- write_zero 验证 action_MSE 3.898803、action_MAE 0.801526，video_MSE 2325.59、PSNR 16.28、SSIM 0.5810、LPIPS 0.2252。
- 单次训练中间快照与真实机器人写字成功率之间没有确定换算关系；所报视频像素指标也不回答规范笔顺。

**Baselines**：公开 model card 未提供同协议视频-only、action-only、端到端机器人成功率对照表；必须标“待核”，禁止推测模型的相对性能。

**核心不足与待验证机制**：示教匹配按数字/排序，参考片段和目标片段无严格时空配准；跨实施体把人类手势转成机器人动作有迁移难点。需要对照 reference shuffling、错误参考、动作头移除、状态头移除、相同预算训练，并量化真实笔画出现/压力/完成度。

## 八项模板

1. Problem：视频条件的机器人书写动作与未来观察预测。
2. Motivation：示教和执行形态跨人/机器人存在差异，需要联合感知与控制。
3. Contribution：发布训练权重、动作归一化、结构/训练配置及验证日志；无本轮确认的正式论文新机制。
4. Method：人类参考+机器人状态/多视角→视频 DiT 和动作模型联合→未来视频与动作。
5. Experiments：数字 0–9，本地 episodes/特定验证快照；完整对照与真实机器人成功率待查。
6. Limitations：领域极窄、无对齐时序、模型卡指标不含笔顺、权重依赖和许可需核。
7. Insights：证明书写研究已有 video+action 的公开工程路径；实验应从观测对齐/动作执行验证出发，不能借用数字 PSNR 证明中文字视频正确。
8. 一句话：Wuji VAM 是与视频—动作联合建模高度相关的非论文制品，但仅有数字机器人写字的有限核查证据。

**复现前提**：固定 HF revision、base model revision、仓库代码 commit、观察帧预处理、动作归一化；检查 model_config.json、training_config.yaml 与 README 是否相符，再执行极小 batch smoke test。无需把所有 11.54GB 权重复制进调研仓库。
