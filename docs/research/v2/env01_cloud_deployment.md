# ENV-01 云端最小接口验证

本任务已获用户批准，费用不设上限。范围固定为 Lance_3B_Video 原生 `x2t_video`、`t2v`、`i2v` 各一个输入；不训练，不启动新的实验组，不作笔顺准确率或共享收益结论。完整 ENV-01 的梯度与重载检查另待批准，本次接口通过也不能将整个 ENV-01 标成完成。

## 租用配置

- 智星云 GPU 云主机：**1×NVIDIA A100-SXM4-80GB，16核 CPU / 48GB 内存**。
- 建议可写磁盘 **150GB**，供约18.38GB选定权重、运行环境、编译缓存及输出使用。150GB为预留量，尚非实测最低值。
- Linux x86_64，优先 Ubuntu 22.04 + CUDA 12.6 **开发环境**（含 `nvcc`），含 Conda 或 Python 3.11。驱动须支持 CUDA 12.6 的 PyTorch；连接后核实实际配置。
- 若界面只有其他镜像，先给出镜像名称，由执行 Agent 核对，无需自行反复安装。
- **无需额外租无卡 CPU 主机**。部署包直接上传 GPU 主机；大权重直接在云端下载。本地不加载模型。
- 若 A100 80GB 暂无库存，可以等。其他卡的替代方案须依据实际可用配置评估；本脚本未声明它们已可运行。

截图中的8元/小时对应8核/16GB配置；16核/48GB的实际租价以平台下单页为准，记录到账单中。

## 部署包与固定来源

仓库构建命令（维护者使用；本地仅收集公开源码及绘制小图片，不下载权重）：

```bash
python3 scripts/env01/prepare_bundle.py --output private/env01_deployment_build_2026-10-27 \
  --source-cache /tmp/umm-env01-lance-raw-20261027 \
  --source-cache /tmp/umm-env01-lance-20261027
```

交付压缩包：`data/research/deployments/env01_interface_2026-10-27/env01-cloud.tar.gz`。解压后顶层为 `env01-cloud/`，包含原作者许可、固定源码、计划、脚本和原创输入图片，不含权重及外部数据集。`upstream_manifest.json` 记录逐文件来源和收集失败；构建尝试记录另随交付包保留。将整个目录放在持久可写磁盘；脚本运行环境与权重都在该目录下。

固定代码：`bytedance/Lance@4baeee086648996f6ab12e673cbe461b0b149997`。
固定权重：`bytedance-research/Lance@7395315758865e6f56ab87ad06a88c7ac172f056`。
安装方案依据该版官方说明：Python 3.11、PyTorch 2.8.0/cu126、FlashAttention 2.8.3，并安装该版 `requirements.txt`。依赖安装、扩展编译和权重下载尚待云端验证，成功安装后保存完整 `pip freeze`。FlashAttention以 `MAX_JOBS=2` 控制编译主存。

实例开通后提供控制台中的 SSH 主机、端口、用户名或本机 SSH 别名。使用 SSH 密钥或现有登录方式；无需把密码写入研究仓库。macOS自带 `ssh` 和 `scp`，平台也支持 SFTP。

以下 `PORT`、`USER`、`HOST` 和 `/your/persistent/disk` 替换为实际值；可由执行 Agent 在获得连接信息后完成：

```bash
scp -P PORT data/research/deployments/env01_interface_2026-10-27/env01-cloud.tar.gz USER@HOST:/your/persistent/disk/
ssh -p PORT USER@HOST
cd /your/persistent/disk
tar -xzf env01-cloud.tar.gz
bash env01-cloud/tools/bootstrap.sh
env01-cloud/runtime/bin/python env01-cloud/tools/run_interfaces.py --bundle env01-cloud
```

安装与模型运行分为两个命令，安装失败会保存日志并退出；处理任务内兼容问题时保留失败尝试及具体变更，不改写原始源码冒充原生成功。不要重复解压覆盖已有运行目录。断线后先检查既有进程，再决定是否重试。

## 输入和记录

三个接口各1个输入，随机种子11；生成请求33帧、480×848、12fps、30步、CFG4.0，关闭外部提示增强。原生 i2v 图像预处理可能选择尺寸桶，实际输出尺寸由RGB解码记录，不假定等于请求值。

- `x2t_video`：原创黑笔画视频，先横后竖，询问可见时序与方向。目标字段提供无答案信息的占位文字以满足原生schema；理解推理按首个CE索引截断上下文，不将参考答案输入当作正确性证据。
- `t2v`：白底逐笔写“十”的文本描述，使用原生纯文本JSON结构。
- `i2v`：只提供实际已写横画的图像及继续写竖画的指令，不提供未来帧或完整字图。

这些原创直线图只服务接口验证，不代替 DATA-01 的规范字形、真实数据授权与分组设计。模型生成是否符合笔顺须后续独立审计，不能凭程序退出码或模型自述判定。

每次执行产生新的 `runs/<UTC时间>/`，逐项保留命令、输入快照、原生输出、完整日志、失败、CPU峰值RSS、PyTorch显存峰值与加载在内的耗时。另用 `nvidia-smi` 每秒采样整卡显存；短暂峰值可能漏采，与分配器峰值分别报告。三项按独立进程顺序执行，单项失败不抹去其他项。进程退出为0仍需检查非空理解答案或实际可解码RGB视频。

`setup/<UTC时间>/` 保留安装/下载日志、实际硬件、依赖版本及耗时。完整计算成本还需结合账单核对开机、安装、下载、空闲、失败重试和推理；费用未知时保留null，不能用纯推理时间替代总账单。

运行后回传完整 `runs/`、`setup/`、`plan.json`、`inputs/manifest.json` 和任何调试补丁到研究分支，保留全部分母和失败。云端压缩时排除 `runtime/`、`upstream/downloads/`，保留所有运行输出。没有实例连接信息之前，状态为“部署准备，等待实例”，没有任何模型实测结果。

来源：[固定源码及官方要求](https://github.com/bytedance/Lance/tree/4baeee086648996f6ab12e673cbe461b0b149997)、[固定权重](https://huggingface.co/bytedance-research/Lance/tree/7395315758865e6f56ab87ad06a88c7ac172f056)、[平台macOS SSH指南](https://gpu.ai-galaxy.cn/docs_v2/macOS%E7%B3%BB%E7%BB%9F%E8%BF%9E%E6%8E%A5%E5%88%B0%E4%BA%91%E4%B8%BB%E6%9C%BA.html)。
