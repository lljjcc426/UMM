# LTX-Video 2B本机验证记录

2026-11-01；分支`codex/engineering-hanzi-video`。用户在“优先本机运行，尽量不租GPU”的选型后回复“继续”，本轮完成所建议的两条件小验证。授权与结果分别见[data目录](../../data/engineering/ltx_local_2026-11-01/authorization.json)和[实际登记](../../data/engineering/ltx_local_2026-11-01/status.json)。

**结论：这台Apple M5、16GiB统一内存的Mac可以运行两段低分辨率原生视频生成；本次两段输出未满足规范汉字书写要求。** 文字条件得到非目标多字形；图片条件的“士”从首帧就已完整出现，没有所要求的逐笔过程。保留LTX为本机原生视频模块候选，当前不接管规范执行器，也不计为识字、规划或自纠错闭环成功。

## 配置与真实输入

使用[官方LTX源码](https://github.com/Lightricks/LTX-Video)，固定提交`4b2d053057623ddd4d0a1d3e9cd28890e9ef487f`；模型`Lightricks/LTX-Video`固定HF revision `8984fa25007f376c1a299016d0957a37a2f797bb`，文件`ltxv-2b-0.9.8-distilled.safetensors`。未更改官方源码、权重或采样时间步。

本机Python3.12.14、PyTorch2.8.0、Transformers4.51.3、Diffusers0.34.0，MPS可用；依赖安装在`private/ltx_local/venv312`，原工程`.venv`保持原样。可复建依赖在`../../scripts/engineering/requirements-ltx-mps.txt`，实际完整版本锁在[data目录](../../data/engineering/ltx_local_2026-11-01/requirements-lock.txt)。

两请求固定目标“士”、种子11、256×256、33帧、12fps、2.75秒、BF16、8步；时间步为`[1, .9937, .9875, .9812, .975, .9094, .725, .4219]`，与checkpoint内置允许列表一致。关闭提示增强和超分辨率，单尺度执行。这个低分辨率配置用于本机可行性检查，不能据其质量推断其他分辨率、时长或采样设置。

提示保留字面“士”与英文三笔说明：上长横从左到右、中竖从上到下、下短横从左到右，要求白底空白起始及已有墨迹保留。[完整冻结配置](../../data/engineering/ltx_local_2026-11-01/config.json)与[实际分词输入](../../data/engineering/ltx_local_2026-11-01/attempt03/actual_text_input.json)均保留。T5将字面“士”映射为一个unknown词元；英文描述正常保留，不能声称已证明中文字形的直接文本识别。

图片条件增加一张既有Arphic工程预览几何生成的“士”图，放在第32帧，强度1。此设置提供末态外观，不提供动画、逐笔视频或事件日志；外观相似不计为独立识字证据。图源仍是`AI_reviewed_engineering_preview`，未提升为真人逐笔金标。没有从ENV-01或旧UMM请求导入fixture。

## 运行结果与失败

| 运行 | 实际行为 | 结果 |
| --- | --- | --- |
| attempt01 | T5加载 | Transformers试图预分配一个9.12GiB缓存，Metal拒绝；未调用视频管线 |
| attempt02 | T5编码；文字、图片视频各一调用 | 编码完成；新包装器缓存掩码留在CPU，两个视频调用在注意力计算处失败，无原片 |
| attempt03 | 复用同一真实文本编码；修正掩码设备后各一调用 | 两段原生MP4完成，66帧全部可解码，尺寸/帧率正确，PTS严格递增 |

实际视频管线调用**4次：技术失败2次，有效原片2段**；最终两个条件均完成，无未运行条件。原始失败、输入、traceback与原片分别保存，没有覆盖失败或另挑种子。一次加载失败不计为视频生成调用。

修复局限于运行包装器：用作用域内补丁跳过Transformers4.51.3的单块allocator预热性能优化，实际参数仍照常加载；将缓存掩码与编码一起转到MPS。没有修改模型运算、权重、提示、种子或生成设置。复用已完成的真实编码避免重复加载同一T5。原日志的meshgrid索引和config字段访问警告保留，本轮没有为这些弃用警告更换依赖。

资源记录如下，均排除下载和前期调试时间：

| 阶段 | 进程墙钟 | 其中视频推理 | 采样MPS驱动分配峰值 |
| --- | ---: | ---: | ---: |
| 共享文本编码一次 | 20.22秒 | — | 10.16GiB |
| 文字条件请求 | 20.08秒 | 6.75秒 | 7.17GiB |
| 图片条件请求 | 16.58秒 | 6.57秒 | 7.16GiB |

MPS当前张量分配和驱动分配每0.5秒采样；这不是精确的瞬时最大值。各进程最大RSS另存于metrics。统一内存下这些指标有重叠，不相加为物理内存需求。两请求共享一次文本编码；该三阶段墙钟合计约56.9秒，不能外推至高清、长视频或任意提示。云GPU、训练、收费API均为0；未计算本机电费。

原生视频的第0、4、8、12、16、20、24、28、32帧由AI查看，全部33帧由程序解码。文字片首帧已有约4.26%的深色区域，图像片约8.84%，两者全片变化很小；AI查看均为预存字形的近静态画面。图片片外观接近参考“士”，但从首帧已完整出现。两者未呈现空白到逐笔形成，笔顺、方向标为`unknown_no_observable_writing`。[检查记录](../../data/engineering/ltx_local_2026-11-01/output_review.json)明确标识AI检查，没有代填真人结论或计算总体笔顺准确率。

单字、单种子、低分辨率的结果只支持本次配置下的工程判断。当前不追加提示搜索、种子筛选、训练或云端调用。工程下一步宜补齐本机图像理解与结构化规划，再沿用显式规范校验及受控笔画执行；LTX是否能通过额外控制得到书写过程，需要另行确定范围，不能从两段结果预设成功。

## 产物与复用

私有原片与源RGB位于：

- `private/ltx_local/trial_2026-11-01/attempt03/text.mp4`、`text_source_rgb.npy`、`text_contact.png`
- `private/ltx_local/trial_2026-11-01/attempt03/image.mp4`、`image_source_rgb.npy`、`image_contact.png`
- 同目录`target.png`、`config.json`、`prompt_embeddings.safetensors`、实际请求和日志。
- `attempt01/`、`attempt02/`保留原始技术失败；对应小型日志和JSON另归档至data目录。

必要权重和配置共12文件、25,390,866,849字节，约23.65GiB。官方HF下载客户端先停滞，直链约20KB/s；改用固定ModelScope revision `933a33a1bfacefb22e41297766c2c669627c33cd`，主模型及四个编码分片与HF官方SHA-256一致，在下载流中各核对一次。并行下载最长约732.5秒。[下载凭据](../../data/engineering/ltx_local_2026-11-01/download_receipts.json)和原慢速传输残片均保留，没有重复扫描缓存。模型采用独立的[LTXV Open Weights License 0.X](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt)，许可副本在私有模型目录，不能将模型权重描述为Apache/MIT授权。

运行入口：

```bash
private/ltx_local/venv312/bin/python scripts/engineering/ltx_local_trial.py \
  --upstream private/ltx_local/upstream \
  --models private/ltx_local/models \
  --output /absolute/path/to/a-new-trial-directory
```

新目录需要本次配置的副本和`target.png`；为了保留旧证据，复跑使用新目录。准备现有原片即可查看结果，不必重复运行。下载脚本仅用于新缓存，读取`expected_files.json`，正常复用缓存时无需重新下载或校验全部权重。原生管线阶段各有600秒超时，实际均未触发。

本轮只修改`AGENTS.md`以记录本机小验证授权和实际结果；新增下载脚本、分进程运行脚本、隔离依赖清单、本报告与`data/engineering/ltx_local_2026-11-01/`证据。没有删除既有文件，没有改动原应用执行链、历史研究结论或主线。测试以实际编码、原生生成和MP4解码为依据，未为独立脚本反复运行无关研究回归。权重、原片与RGB保持私有，不推送或合并main。
