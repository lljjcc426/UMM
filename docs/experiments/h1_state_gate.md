# H1前置门槛：答案接口与当前线条状态

当前只推进两项：**模型能否稳定回答正确；模型能否区分实际已出现的线条及其完成程度。** 两项获得稳定结果后，再启动顺序学习。Show-o2已运行文字状态开发集，视觉题尚未运行，未开展训练；本页不报告H1通过。

## 1. 两项门槛怎样分开

| 门槛 | 输入 | 检查内容 | 暂不推断 |
|---|---|---|---|
| A：答案接口与状态判断 | 准确文字状态，不提供图像 | 格式是否有效、答案是否正确、等价问法是否都答对 | 看图能力、顺序理解 |
| B：当前视觉状态 | 完整参考＋当前画面；另设只给当前画面的对照 | 指定线条是否出现，是否达到完整参考，依据不足时是否回答未知 | 实际先后、运笔方向、生成收益 |

A先比较短答案和单字段JSON，例如 `部分` 与 `{"answer":"部分"}`。不使用A/B/C/D选项，不在主评分中自动补全、纠正或从长解释中抽取答案。格式有效与内容正确分别计数。

准确文字条件说明：所有已有线条都沿参考路径从起点连续延伸，没有偏移、隐藏或重复；给出参考完整长度与当前已有长度。这样才能依据长度判断完成程度。仅给两段长度、没有路径对应关系，不能一般性地推出形状完整。

B明确区分：

- **存在**：部分线条也算出现，不能把参考图中的线条算入当前画面。
- **完成**：相对于指定参考判断；短线可以完整，长线也可以尚未完成。
- **未知**：只有当前静态线条且没有完整目标时，长度不能确定它是否完成。此对照用于检查模型是否利用参考，不能把始终回答未知视为通过。

当前不要求模型从静态图推断实际书写顺序。状态判断通过后，再加入相邻帧变化、实际顺序、首错和下一动作，最后开展过程监督训练与冻结模型对照。

## 2. 已构造的数据

[数据目录](../../data/h1/state_gate_v1/)由[生成与评分脚本](../../scripts/h1_state_gate.py)确定性产生，均为本项目生成的线条图形。

| 集合 | 基础案例 | 独立几何组 | 用途 |
|---|---:|---:|---|
| dev | 26 | 7 | 调整接口、定位错误 |
| test | 130 | 35 | 接口固定后评价；目前未调用模型 |

覆盖单横、单竖、重复横线、重复竖线、交叉与折线；包括未出现、35%、75%和完整状态。每个案例有准确文字、参考＋当前、仅当前三种输入，两类问题、两种等价问法及两种输出形式。合计3744行输入是这些条件的展开，**独立案例数为156，不能按3744个独立样本计算置信度。**

另有6组参考对照：当前像素完全相同，短参考下是完整，长参考下是部分。每组的两题都答对，才说明该对照成功。图像上半部为参考，下半部为当前，使用相同比例与位置，没有时间序列含义。

同一几何组的状态、问法、输出形式和参考对照全部归入同一集合。测试集留出新的几何参数；它仍使用相同形状家族和Pillow渲染器，**没有达到未见汉字、字体或渲染来源的泛化要求**。后续完整H1必须另行满足这些要求。

## 3. 评分与推进条件

每项报告分子、分母、各类别正确率、两种问法均正确的案例比例，以及按几何组重采样的95%置信区间。未输出的题计为失败；未完成运行不能通过缩小分母提高分数。开发集仅7组，区间和分数都只用于诊断。

采用此前H1拟定的工程门槛作为起点：A格式有效率≥98%、两类内容各≥95%；B存在判断≥90%、完成程度≥85%、确实缺少依据时回答未知≥90%。同时要求A的等价问法均正确率≥95%，B对应比例达到各自内容门槛，参考对照成对正确率≥85%。这些门槛需要在正式运行前固定，不是已取得结果或领域标准。

同一模型、提示、输出形式和计算设置固定后才运行test。检查类别混淆，避免多数类掩盖“未出现”或“完整”的持续失败。若更改提示或训练使用了test信息，该集合转为开发用途，重新留出测试。

两项通过只支持进入顺序实验。完整H1仍需要同终态不同历史、实际顺序和方向、首次违规、动作判断、字符/风格/来源独立划分，以及相对冻结模型和末帧基线的改善证据。H2、H3保持未开始。

## 4. 底座与计算条件

选用 `showlab/show-o2-1.5B-w-video-und`，使用完整统一检查点；当前只调用其文字路径，视觉和生成模块保留在CPU。该版本经视频理解训练，与普通Show-o2-1.5B检查点不同。官方当前仍将视频生成权重列为待发布项，故本次不能证明后续H2的视频生成底座已具备。[官方说明](https://github.com/showlab/Show-o/blob/45a5a2de01d1ebd10cd5864d29310a76476cdf23/show-o2/README.md)

- 官方源码：`showlab/Show-o@45a5a2de01d1ebd10cd5864d29310a76476cdf23`。
- 权重：ModelScope同名仓库版本`412f647429897ad888771d18008de4edfb2c42a6`；完整加载后参数量3,063,740,640，名称中的1.5B不能当作整个系统的参数量。
- 本次已实测：Apple M5／16GB、MPS、bfloat16；[运行脚本](../../scripts/h1_run_showo.py)记录包版本、全部输入、原始回答和耗时。
- 加载适配：SigLIP只按配置构建结构，随后由完整Show-o2检查点载入全部保留权重，沿用上游缺失键检查，避免重复下载随后会被覆盖的基础SigLIP权重。没有使用原始Qwen模型权重替代UMM权重。
- 可接入设备：RTX 4060 Laptop／8GB、Windows 11、PyTorch 2.6.0+cu124；由设备信息提供，目前尚未通过SSH登录实测。显存还需容纳视觉编码、中间张量和训练状态，不能据参数名称保证训练可行。
- Lance官方列出推理至少40GB显存，当前4060不满足其公开配置；不作为本轮默认模型。[官方要求](https://github.com/bytedance/Lance#recommended-environment)

远程接入使用Windows OpenSSH Server。管理员PowerShell安装并启动服务后，再配置SSH公钥登录；管理员账户和普通账户的公钥文件位置不同。连接地址、凭据和本机密钥不写入仓库。[安装说明](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse) · [公钥配置](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement)

## 5. 运行方式

当前运行器只实现门槛A，不把无图文字回答标为视觉成绩。视觉接入后另行记录预处理、参考输入布局和显存实测。源码、模型与辅助配置放在忽略的`checkpoints/`下。准备环境时安装适合平台的PyTorch/torchvision，再安装`requirements-h1-showo.txt`；远程已有的CUDA环境先核实，避免直接覆盖。

运行器默认目录约定：

| 目录 | 所需内容 |
|---|---|
| `checkpoints/Show-o-source/show-o2/models/` | 上述固定源码版本的模型文件；无需整个上游训练环境 |
| `checkpoints/Show-o2-1.5B-video/` | 指定视频理解检查点的`config.json`和`pytorch_model.bin` |
| `checkpoints/Show-o-assets/Qwen2.5-1.5B-Instruct/` | 官方`config.json`、`tokenizer.json`、`tokenizer_config.json`、`vocab.json`、`merges.txt`；无需基础Qwen权重 |
| `checkpoints/Show-o-assets/siglip/` | 官方`google/siglip-so400m-patch14-384/config.json`；无需基础SigLIP权重 |

本轮辅助配置及来源版本保存为[初始化记录](../../results/h1/showo2_video_1_5b/initialization.json)。门槛A无图，不需要下载Wan VAE；视觉阶段需要单独接入VAE。

```bash
python scripts/h1_state_gate.py build
python scripts/h1_run_showo.py --device mps --split dev --format plain \
  --output results/h1/showo2_video_1_5b/new_run
python scripts/h1_state_gate.py score --split dev --format plain --view oracle_text \
  --predictions results/h1/showo2_video_1_5b/new_run/predictions.jsonl \
  --output results/h1/showo2_video_1_5b/new_run/score
```

每轮输出目录不可覆盖。CUDA主机将`--device`改为`cuda`；这条命令的CUDA路径尚未实测。实际开发集结果与接口修订记录见[本轮结果](../../results/h1/showo2_video_1_5b/README.md)。
