# H1前置门槛：答案接口与当前线条状态

当前只推进两项：**模型能否稳定回答正确；模型能否区分实际已出现的线条及其完成程度。** 两项获得稳定结果后，再启动顺序学习。Show-o2已在本机接通文字和图像理解路径，并完成文字及首轮静态视觉状态监督适配；当前完成程度判断仍不稳定，尚未通过完整H1。

## 1. 两项门槛怎样分开

| 门槛 | 输入 | 检查内容 | 暂不推断 |
|---|---|---|---|
| A：答案接口与状态判断 | 准确文字状态，不提供图像 | 格式是否有效、答案是否正确、等价问法是否都答对 | 看图能力、顺序理解 |
| B：当前视觉状态 | 完整参考＋当前画面；另设只给当前画面的对照 | 指定线条是否出现，是否达到完整参考，依据不足时是否回答未知 | 实际先后、运笔方向、生成收益 |

A先比较短答案和单字段JSON，例如 `部分` 与 `{"answer":"部分"}`。不使用A/B/C/D选项，不在主评分中自动补全、纠正或从长解释中抽取答案。格式有效与内容正确分别计数。

另设事后答案词审计：仅对完整的单词回答或单字段JSON中的明确词汇进行中英映射，例如`yes`对应“有”、`part`对应“部分”。映射表、原始回答和审计成绩独立保存，不改变严格评分，不作为门槛通过证据。它用于判断低分来自输出约定、状态错误，还是两者都有。

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

每项报告分子、分母、各类别正确率、两种问法均正确的案例比例，以及按几何组重采样的95%置信区间。配对比较按问题与实际RGB像素去重；相同图像使用不同文件名也只计一次。存在与完成同时正确、两者逻辑一致分别报告，不能把一致但错误的回答当作成功。未输出的题计为失败；未完成运行不能通过缩小分母提高分数。开发集仅7组，区间和分数都只用于诊断。

采用此前H1拟定的工程门槛作为起点：A格式有效率≥98%、两类内容各≥95%；B存在判断≥90%、完成程度≥85%、确实缺少依据时回答未知≥90%。同时要求A的等价问法均正确率≥95%，B对应比例达到各自内容门槛，参考对照成对正确率≥85%。这些门槛需要在正式运行前固定，不是已取得结果或领域标准。

同一模型、提示、输出形式和计算设置固定后才运行test。检查类别混淆，避免多数类掩盖“未出现”或“完整”的持续失败。若更改提示或训练使用了test信息，该集合转为开发用途，重新留出测试。

两项通过只支持进入顺序实验。完整H1仍需要同终态不同历史、实际顺序和方向、首次违规、动作判断、字符/风格/来源独立划分，以及相对冻结模型和末帧基线的改善证据。H2、H3保持未开始。

## 4. 底座与计算条件

选用 `showlab/show-o2-1.5B-w-video-und`，使用完整统一检查点；调用文字和图像理解路径，未执行生成模块保留在CPU。该版本经视频理解训练，与普通Show-o2-1.5B检查点不同。官方当前仍将视频生成权重列为待发布项，故本次不能证明后续H2的视频生成底座已具备。[官方说明](https://github.com/showlab/Show-o/blob/45a5a2de01d1ebd10cd5864d29310a76476cdf23/show-o2/README.md)

- 官方源码：`showlab/Show-o@45a5a2de01d1ebd10cd5864d29310a76476cdf23`。
- 权重：ModelScope同名仓库版本`412f647429897ad888771d18008de4edfb2c42a6`；完整加载后参数量3,063,740,640，名称中的1.5B不能当作整个系统的参数量。
- 本次已实测：Apple M5／16GB、MPS、bfloat16；[运行脚本](../../scripts/h1_run_showo.py)记录包版本、全部输入、原始回答和耗时。
- 加载适配：SigLIP只按配置构建结构，随后由完整Show-o2检查点载入全部保留权重，沿用上游缺失键检查，避免重复下载随后会被覆盖的基础SigLIP权重。没有使用原始Qwen模型权重替代UMM权重。
- 可接入设备：RTX 4060 Laptop／8GB、Windows 11、PyTorch 2.6.0+cu124；由设备信息提供，目前尚未通过SSH登录实测。显存还需容纳视觉编码、中间张量和训练状态，不能据参数名称保证训练可行。
- Lance官方列出推理至少40GB显存，当前4060不满足其公开配置；不作为本轮默认模型。[官方要求](https://github.com/bytedance/Lance#recommended-environment)

**当前在M5／16GB本机继续推进，远程连接不作为前置条件。** 上述4060信息仅保留为后续资源评估；只有本机确实无法完成必要实验时，再重新评估远程计算需求。

## 5. 运行方式

运行器支持A的文字输入和B的静态图像输入；无图成绩不能解释为视觉成绩，静态图成绩不能解释为视频顺序理解。源码、模型与辅助配置放在忽略的`checkpoints/`下。准备环境时安装适合平台的PyTorch/torchvision，再安装`requirements-h1-showo.txt`。

图像路径沿用上游MMU输入组织与注意力掩码。432×432组合图直接归一化至[-1,1]，不裁剪；Wan VAE使用CPU float32，采样随机种子固定为0，同一图像在一轮内复用编码；双路径视觉表示融合及语言模块使用MPS bfloat16。上、下半部分别对应参考和当前，均保留在同一图像中；本轮不使用视频编码。该实现完成本机运行，不代表与CUDA float32数值完全一致。

运行器默认目录约定：

| 目录 | 所需内容 |
|---|---|
| `checkpoints/Show-o-source/show-o2/models/` | 上述固定源码版本的模型文件；无需整个上游训练环境 |
| `checkpoints/Show-o2-1.5B-video/` | 指定视频理解检查点的`config.json`和`pytorch_model.bin` |
| `checkpoints/Show-o-assets/Qwen2.5-1.5B-Instruct/` | 官方`config.json`、`tokenizer.json`、`tokenizer_config.json`、`vocab.json`、`merges.txt`；无需基础Qwen权重 |
| `checkpoints/Show-o-assets/siglip/` | 官方`google/siglip-so400m-patch14-384/config.json`；无需基础SigLIP权重 |
| `checkpoints/Show-o-assets/Wan2.1_VAE.pth` | 官方Wan2.1 VAE；图像路径需要，文字路径不使用 |

本轮辅助配置、Wan VAE来源及版本保存为[初始化记录](../../results/h1/showo2_video_1_5b/initialization.json)。

```bash
python scripts/h1_state_gate.py build
python scripts/h1_run_showo.py --device mps --split dev --format plain \
  --output results/h1/showo2_video_1_5b/new_run
python scripts/h1_state_gate.py score --split dev --format plain --view oracle_text \
  --predictions results/h1/showo2_video_1_5b/new_run/predictions.jsonl \
  --output results/h1/showo2_video_1_5b/new_run/score

PYTORCH_ENABLE_MPS_FALLBACK=1 python scripts/h1_run_showo.py \
  --device mps --view reference_current --format json \
  --output results/h1/showo2_video_1_5b/new_visual_run
python scripts/h1_state_gate.py score --split dev --format json \
  --view reference_current --audit-words \
  --predictions results/h1/showo2_video_1_5b/new_visual_run/predictions.jsonl \
  --output results/h1/showo2_video_1_5b/new_visual_run/score
```

只给当前画面的对照将两条视觉命令中的`reference_current`改为`current_only`，使用另一个输出目录。每轮目录不可覆盖。实际开发集结果与接口修订记录见[本轮结果](../../results/h1/showo2_video_1_5b/README.md)。

`--blank-image`仅是文字题附带空白图的接口排查条件。它同时改变了模态输入和提示模板，且空白图可能与文字记录冲突，不能据此隔离单一原因或评价视觉状态能力。

## 6. 本机文字状态监督适配

先检验已有失败能否通过有限监督改善，只训练准确文字条件下的存在和完成判断。使用[独立构建的适配数据](../../data/h1/state_training_v1/README.md)：128个训练几何案例、512行问题；52个开发案例、208行问题。排除与开发问题文本重合的整组训练样本，并把仅几何位置不同、可见文字相同的组归并计入置信区间。开发集去重后为192个不同问题、13组；相同模板仍在两集合出现。

从同一完整Show-o2检查点开始，采用[LoRA](https://arxiv.org/abs/2106.09685)冻结基础参数、训练低秩更新。当前在语言模块最后8层的q/v投影中添加rank 8、alpha 16的适配参数，共311,296个；原有视觉和生成模块保留。基础参数使用bfloat16，适配参数与优化器使用float32。

只对答案及结束符计算交叉熵，提示文本不计入损失。固定2轮、256个优化步骤，梯度累积4，AdamW学习率2e-4，前10%步骤预热后余弦下降，梯度范数限制1。训练种子731；只评价最终检查点，没有根据中间开发成绩挑选检查点。本机实测训练约161秒，未训练图像、时间顺序或动作预测。

保留自由生成结果，再对冻结和训练后模型都使用相同的固定答案解码约束。约束仅允许`{"answer":"判断词"}`的合法词表，不读取真值，不修正生成后的错误标签。**其格式有效率由接口保证，内容、两问均对及参考依赖仍需单独检验。**

```bash
python scripts/h1_state_gate.py build-training
python scripts/h1_train_state.py \
  --output results/h1/showo2_video_1_5b/new_text_training \
  --adapter checkpoints/new_text_training/adapter.pt
python scripts/h1_run_showo.py --device mps --format json \
  --inputs data/h1/state_training_v1/inputs.jsonl \
  --adapter checkpoints/new_text_training/adapter.pt --constrain-answers \
  --output results/h1/showo2_video_1_5b/new_text_adapted_eval
```

冻结对照使用相同命令但不指定`--adapter`。适配权重存放于本地忽略的`checkpoints/`；训练配置、全部训练输入与逐步损失，以及评价原始回答保存在结果目录。此实验只能支持文字状态接口的适配可行性，视觉迁移、生成质量保持及完整H1仍需分别验证。

## 7. 直接视觉状态监督

文字适配没有可靠迁移到实际画面，随后加入[独立生成的视觉训练数据](../../data/h1/state_visual_training_v1/README.md)：78个状态案例、21个几何组、624条问答，覆盖参考有但当前无、半条与完整、同当前不同参考、缺少参考及多线条目标选择。开发评价仍使用原26例；130例视觉测试在开发门槛稳定前保留。

从文字LoRA的最终权重继续，保持适配层、rank和学习率设置，混入原512条文字训练题。2轮共568步，固定结束后评价，不按中途开发成绩选权重。冻结Wan VAE及融合视觉编码，先编码156张图像并在CPU缓存特征，训练期间只更新语言模块的31万个LoRA参数。图像提示、特征及注意力掩码与冻结评价共享实现；损失仍只监督答案和EOS。只有下游语言适配接受视觉监督，不能把本轮描述为训练了视觉编码器。

```bash
python scripts/h1_state_gate.py build-visual-training
PYTORCH_ENABLE_MPS_FALLBACK=1 python scripts/h1_train_state.py \
  --data data/h1/state_visual_training_v1 \
  --views reference_current current_only \
  --text-replay data/h1/state_training_v1 \
  --init-adapter checkpoints/h1_text_state_lora_v1/adapter.pt \
  --output results/h1/showo2_video_1_5b/new_visual_training \
  --adapter checkpoints/new_visual_training/adapter.pt
```

训练后分别评价参考＋当前、仅当前，以及原文字开发集。所有视觉比较使用相同固定答案解码，分别报告冻结、文字适配及视觉适配结果，不能混用旧自由生成成绩计算训练收益。文字开发回归只检验已知任务上的能力保持；已有文字测试不重新作为独立留出。训练数据仍是同一渲染器和形状家族，当前不评价视频、汉字风格或生成质量。

## 8. 目标对应诊断与同图不同目标监督

首轮视觉适配在多线条目标缺失上失败。用同样12个开发案例比较原图、仅改提示、加目标蓝框、只保留正确目标，固定模型权重与解码。蓝框未改善；隔离目标后存在24/24，完成19/24。隔离需要外部正确实例标注，不能作为自主定位通过。另在12个已见训练案例上检查，存在18/24、完成13/24，目标缺失时存在0/6，说明仍有训练内拟合问题。全部证据见[控制结果](../../results/h1/showo2_video_1_5b/target_controls_v1/README.md)。

继续训练采用[同图不同目标数据](../../data/h1/state_target_contrast_v1/README.md)。48幅新画面覆盖6个几何组，每幅图询问所有目标；同图不同目标可有不同真值，相同目标也覆盖不同进度。864条新题、624条原视觉题、512条原文字题混合，固定1轮、500步；保持相同LoRA结构、优化器和答案损失。只评价最终权重。此设计增加了目标对应约束，但同时增加训练量；没有等预算复习对照时，不把全部收益归于数据结构本身。

```bash
python scripts/h1_target_contrast.py
PYTORCH_ENABLE_MPS_FALLBACK=1 python scripts/h1_train_state.py \
  --data data/h1/state_target_contrast_v1 \
  --views reference_current current_only \
  --text-replay data/h1/state_training_v1 \
  --init-adapter checkpoints/h1_visual_state_lora_v1/adapter.pt \
  --epochs 1 \
  --output results/h1/showo2_video_1_5b/new_target_training \
  --adapter checkpoints/new_target_training/adapter.pt
```

评价仍采用完整原图，辅以同一开发图像切换目标的112题；复用原基线完全相同的48个输入，仅新增64次基线调用。各目标依赖同一图像，按原几何组报告区间，不把目标数量当作独立图像数。训练内检查使用`--split train`，不混入开发或独立测试成绩。

该轮已在M5／16GB完成：图像编码约12.6分钟，500步梯度训练约18.9分钟。原开发集存在仍47/52、完成35→36/52，完成两问均对仍17/26；完成改善的配对95%区间为[-4.5,7.1]个百分点。训练子集存在18→21/24、完成13→17/24，但仍未拟合稳定。同图切换目标的完成两问均对仍13/28；真值不同的两个目标都答对仍0/20，含两种问法，仅3个几何组。文字开发回归保持96/96、95/96。完整记录见[本轮结果](../../results/h1/showo2_video_1_5b/target_controls_v1/README.md)。

下一项优先做小规模训练内拟合诊断：固定少量已见多实例案例和训练预算，比较现有最后8层适配与更早层也参与适配，先看目标缺失和完成状态能否学会。现有结果尚不能确定失败来自更新范围、训练量、图像表示还是任务表达；不能据当前负结果直接下定论。拟合诊断不计入开发或独立验收，稳定后再固定训练设置并评价留出数据。顺序学习继续保持未开始。
