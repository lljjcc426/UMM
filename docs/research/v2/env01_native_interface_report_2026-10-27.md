# ENV-01 原生三接口云端验证记录

后续状态补充：[训练与独立重载验证](env01_training_reload_report_2026-10-27.md)已完成。下文保留本次原生接口子任务结束时的状态和全部失败，不覆盖历史记录。

本次获准任务已完成：三项原生推理接口均有实际成功输出。3个独立输入共启动4次，成功3次、失败1次，首次理解接口因驱动链接名缺失失败后单独重试通过。实测支持将该底座作为后续研究候选；两段生成视频均未满足本次笔顺指令，不能直接作为正确笔顺示范。梯度、保存重载、正式笔顺评价与 P0 科学验收仍未完成。

## 固定范围与实际资源

用户批准原生 `x2t_video`、`t2v`、`i2v` 各一个原创输入，费用不设上限，不训练。本机仅准备部署和接收证据；权重、CUDA 编译和模型推理均在用户租用的 GPU 主机进行，无需额外 CPU 云主机。

- 代码：`bytedance/Lance@4baeee086648996f6ab12e673cbe461b0b149997`，模型源码未修改。
- 权重：`bytedance-research/Lance@7395315758865e6f56ab87ad06a88c7ac172f056`；仅下载本次需要的模型、ViT、VAE 与配置文件。
- 实测：1×A100-SXM4-80GB，81920MiB 显存；16 CPU；主存 50,470,645,760 字节；Ubuntu22.04、驱动550.127.05、CUDA工具链12.4.99。
- 独立 Conda Python3.11；PyTorch2.5.1+cu124、torchvision0.20.1、torchaudio2.5.1；上游固定依赖保持原版本，额外固定未限定的 W&B0.19.11、SciPy1.15.3 以满足 Protobuf3.20.3、NumPy1.23.5 约束。
- 请求：seed11、33帧、480×848、12fps、30步、CFG4，关闭外部提示增强。i2v 原生尺寸桶的实际分辨率由输出解码记录。

完整授权、硬件、全部尝试与文件变更说明见[任务登记](../../../data/research/runs/env01_native_a10080_2026-10-27/task_record.json)。最终通过情况以原始运行 summary、进程日志、实际文本和 RGB 视频为准。

## 已发生的部署问题

| 环节 | 观察与处理 |
| --- | --- |
| SSH 非交互环境 | 镜像 PATH 未包含 CUDA/Conda；显式设置路径，在单独 Python3.11 环境安装，不以镜像宣传的包列表代替检查 |
| 首次依赖安装 | 下载日志长时间无进展，具体根因未确定；保留首次日志，切换清华 PyPI 镜像；PyTorch仍取官方cu124源 |
| 依赖回退 | W&B 未固定版本，与上游 Protobuf 约束导致回退；SciPy 新版与 NumPy1.23.5 约束导致回退。依据官方 PyPI 元数据固定兼容版本，保留中止记录 |
| 主权重传输 | 高频分段传输剩余三个10MiB稀疏空洞；只补这三个区段，并对人工修复后的主文件执行一次完整SHA256，与固定版本官方LFS值一致。保留旧 partial 和所有失败，不对普通成功下载文件反复校验 |
| 剩余权重 | CDN TLS握手/读取超时；保留异常，调整下载超时90秒、元数据超时30秒及并发8；重试374.04秒后完成 |
| FlashAttention 构建 | 官方2.6.3没有匹配本次torch2.5/cp311的预编译包，进入源码编译；初始PATH未暴露Ninja而串行构建，修正后采用四个Ninja作业。之后误用瞬时主存快照提高至八作业，实际耗尽47GiB主存和5.9GiB交换区；已中止并恢复四作业，复用已完成对象。是否触发内核OOM杀进程未确认，全部尝试日志保留 |
| Decord 打包检查 | 官方文件名为py3-none，包内WHEEL却标cp36-cp36m；pip26检查返回1。保留原失败，不改包内标签；实际Decord成功解码本次33帧480×848 RGB输入后继续。版本依赖无其他报错，平台标签检查仍有已知警告，不能称完整打包检查全绿 |
| Triton 驱动链接 | 首次x2t_video在GCC链接阶段找不到64位-lcuda；新建`/lib/x86_64-linux-gnu/libcuda.so → libcuda.so.1`，指向镜像已有550.127.05驱动，未改驱动二进制。保留首败，只重试理解接口；两项生成不重跑 |
| 安装状态记录 | 第4次安装在完成requirements后被中止，旧EXIT trap却记录exit0；后续编译/下载未完成，按中止记，不作为成功。原始日志与状态保留；脚本补充TERM/INT退出码，避免同类误记 |
| 视频预览 | `list(imageio_reader)`因长度提示为最大整数立即触发MemoryError；改为逐帧迭代成功。保留失败与原元数据，未知nframes在结构记录中写null；没有改视频或追加模型采样 |

三份大权重实际大小：主模型14,211,277,144字节、ViT1,337,407,560字节、VAE2,818,839,170字节。主权重人工修复后的单次校验值为 `7f0550e1d1511b29a4740a67c1e18e176302a4ecb3177c8a5850ff5fe6447c25`。

## 结果与适用范围

首次完整运行：[原始summary](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T114559963105Z/summary.json)，2/3接口输出通过；单项重试：[原始summary](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T115314642365Z/summary.json)，所选理解接口1/1通过。完整分母及汇总见[机器可读结果](../../../data/research/runs/env01_native_a10080_2026-10-27/interface_results.json)。原始失败保留，不能将4次启动写成首次3/3通过。

| 接口/尝试 | 实际结果 | 含加载墙钟s | PyTorch峰值allocated / reserved GiB | 整卡采样峰值MiB | CPU峰值RSS GiB |
| --- | --- | ---: | ---: | ---: | ---: |
| x2t_video 首次 | 链接失败，无成功答案 | 81.05 | 28.38 / 28.70 | 29901 | 31.40 |
| t2v | 33帧RGB视频 | 135.28 | 28.38 / 35.86 | 37257 | 31.40 |
| i2v | 33帧RGB视频 | 129.17 | 28.38 / 29.63 | 30863 | 31.37 |
| x2t_video 重试 | 非空理解答案 | 88.06 | 28.38 / 28.70 | 29901 | 31.38 |

两个视频实际均为480×848、33帧、12fps、2.75秒、H.264/yuv420p；[视频元数据与逐帧预览](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T114559963105Z/media_inspection/video_metadata.json)保留。采样整卡包含非模型开销且每秒一次，可能漏过短峰；allocated与reserved是同一进程分配器的不同指标，不能相加。各进程CPU峰值约31.4GiB，当前约47GiB主存足以完成本次加载。实测最高整卡37,257MiB支持本次80GB配置；未实测40GB卡，不作更长视频或训练可用性保证。

云端部署的95份上游文件与固定版本部署源逐字节比较一致，见[来源比较](../../../data/research/runs/env01_native_a10080_2026-10-27/source_comparison.json)。模型源码未修改；变更仅涉及部署、环境修复和采证/重试工具。完整依赖包含构建工具，见[实际环境冻结](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/setup/20261027T114551-7517/pip-freeze.txt)。

### 实际内容的定性观察

- 理解：识别先横后竖及交叉；没有清楚给出左右/上下方向，并加入输入不支持的速度变化、弯曲描述。[原始答案](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T115314642365Z/x2t_video/outputs/result.json)。
- t2v：开头已有复杂字形，随后变形，并出现手/笔，未呈现要求的空白→横→竖。[视频](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T114559963105Z/t2v/outputs/000001.mp4) · [帧预览](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T114559963105Z/media_inspection/t2v-contact.png)。
- i2v：保留横画起始输入后，竖画由下向上生长，方向与指令相反，既有横画位置也发生变化。[视频](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T114559963105Z/i2v/outputs/000001.mp4) · [帧预览](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/env01-cloud/runs/20261027T114559963105Z/media_inspection/i2v-contact.png)。

这些来自Agent对各一个输入、seed11实际输出的定性观察，没有准确率估计或经过校准的笔顺分数；未启动BASE-01或EVAL-01。底座原生可运行与应用目标之间仍有实际差距，能否通过适配改善尚无证据。

接口验证只判断单个输入能否经原生模型得到非空文本或可解码RGB视频；即使三项通过，也不能证明汉字笔顺准确、理解可靠、训练可行或共享参数带来收益。完整 ENV-01 与 P0 保持未验收。

## 计算成本

费用上限为null，实际账单为null，待平台账单核对。部署、失败、重试、编译、模型加载、推理与空闲时间均需保留；并行步骤的耗时不能直接相加冒充租用时长。4次接口启动累计墙钟433.56秒，含失败、加载与推理。首次安装09:47:19 UTC至证据采集11:57:31 UTC，可见执行窗口约2.17小时；采集时主机uptime约2.24小时。上述窗口包含并行依赖下载、编译、调试与空闲，不能替代平台计费起止。任务目录占用约24.73GiB，采集时文件系统剩余约116.27GiB；目录外的pip和编译缓存不包含在目录占用里。[采集记录](../../../data/research/runs/env01_native_a10080_2026-10-27/cloud/collection_inventory.json)。

## 工程检查

本地目录、v1/v2协议、P0开发状态门禁、shell语法检查均通过，50项回归测试通过。目录检查首轮发现上游README的三份文档及一个传递链接未收集，已从同一固定revision补齐四份文档，未改原文或模型源；首轮失败与重试成功日志见[检查记录](../../../data/research/runs/env01_native_a10080_2026-10-27/checks/attempt01.json)和[受影响检查重试](../../../data/research/runs/env01_native_a10080_2026-10-27/checks/attempt02.json)。这些为本地仓库检查，未触发GitHub CI，也未消除前述Decord平台标签检查失败。

## 交付与后续边界

全部原始运行、失败、环境日志和媒体已回传研究分支；权重、独立运行环境与编译wheel保留云端，不放入Git。没有删除仓库文件，没有远端推送或main改动。云实例仍保留运行，本任务模型进程均已结束。文件变更说明见任务登记。下一项建议为另行批准的最小梯度与保存重载验证；本次不启动。

来源：[固定代码与官方环境说明](https://github.com/bytedance/Lance/tree/4baeee086648996f6ab12e673cbe461b0b149997)、[固定权重版本](https://huggingface.co/bytedance-research/Lance/tree/7395315758865e6f56ab87ad06a88c7ac172f056)、[W&B0.19.11元数据](https://pypi.org/pypi/wandb/0.19.11/json)、[SciPy1.15.3元数据](https://pypi.org/pypi/scipy/1.15.3/json)。
