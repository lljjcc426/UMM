# S2训练前评测准备与真值资格修正

2026-11-03，分支`codex/research/new`，沿用`lljjcc426/UMM`和草稿PR #5。本次完成CPU代码与实验准备，状态为`prepared_not_executed`。没有下载新模型权重、加载模型/原生tokenizer、调用GPU/MPS或训练；没有模型能力分数。S0–S1工程交付保留初步审核认可，逐笔真值覆盖按实际证据修正。

## 真值资格修正

此前将220字概括确认计入E3/E4/E5资格，证据等级处理过高。原判定只检查accepted、审核者、版本、规范引用和笔号范围，遗漏了逐项判断的覆盖与取值。本次补上该条件，没有修改审核原文。

| 证据 | 实际覆盖 | 当前用途 |
|---|---:|---|
| 两份实际逐项表单 | 36字/130笔，128条字×指标记录，500项选择 | 按指标准入；未知项继续排除 |
| 用户对其余字的概括确认 | 220字/2113笔，转录为880条汇总结论，`item_decisions`为空 | 开发图文配对接受；不授予E3/E4/E5逐笔真值资格 |

全部1008条记录保留在[原审核表](../../../data/research/paired_strokes_v1/evaluation_only/reviews.jsonl)。旧版资格判定与记录在Git提交`fde088a5`及之前版本中保留，原始审核JSON仍在原接收目录。本次没有补造选择、重写unknown或追加人工任务。

`gold.qualify`现在要求E3具有规范序列和全部实例选择，E4再具有全部适用笔画对选择，E5再具有全部方向选择，且相应选择均为accepted。记录仍须匹配原gold revision、规范引用和笔号；disputed继续阻止准入。PAIR沿用开发配对接受规则，不能通过指标继承取得逐笔资格。

修正后E3/E5各36字通过，E4为27通过、7未知、2不适用。原主清单中的E3/E5仍各54项可评分，E4为84项可评分、18项几何未知、6项资格不足。模型分值均为null。D-SMOKE16对与D-PILOT240对（192/24/24）配对导出保留，后者不代表240字都有独立逐笔真值。

256字/2243笔、规范序列、源几何和mask、原1504条主请求与2232条完整套件、冻结指标及容差、开发划分全部保留。正式保留集仍为0，本轮四字是已暴露的`audit_development`样本。

## 四模型官方接口核验

完整revision、文件布局、加载/调用/解码路径、环境版本和官方证据URL见[模型登记](../../../configs/research/paired_strokes_v1/s2_models.json)。沿用S0固定检查点，另固定官方代码版本。本轮核验依据为官方模型卡、配置和源码，未将静态核验写成实际加载成功。

| 模型与固定检查点 | 原生加载、处理与输出 |
|---|---|
| [InternVL-U/InternVL-U](https://huggingface.co/InternVL-U/InternVL-U/tree/f012d760e69712bb47f7d3d09a24280f346cee01)，`f012d760…` | `InternVLUPipeline.from_pretrained`加载完整pipeline；VLM、生成解码器、VAE及processor分别由`model_index.json`绑定。`processor/`内含tokenizer和GotOcr2处理器，256方图按配置缩放至448方图，不切块。文字理解使用`generation_mode="text"`；`generate_output`由`inputs_embeds`生成，直接解码续写token。 |
| [ATH-MaaS/Ovis-U1-3B](https://huggingface.co/ATH-MaaS/Ovis-U1-3B/tree/cbc005ddff7376a20bc98a89136d088e0f7e1623)，`cbc005dd…` | `AutoModelForCausalLM`配合checkpoint的`auto_map`和`trust_remote_code=True`加载OvisU1。通过模型自身的文本/视觉tokenizer及`preprocess_inputs`处理RGB，传递`pixel_values`、`grid_thws`和attention mask；直接解码返回的续写token。 |
| [Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct/tree/ebb281ec70b05090aa6165b016eac8ec08e71b17)，`ebb281ec…` | 原生`Qwen3VLForConditionalGeneration`和`AutoProcessor`，使用checkpoint聊天模板，将PIL图像与文字交给`apply_chat_template`。按每条实际输入长度截去生成序列中的输入前缀，再解码。 |
| [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct/tree/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b)，`0c351dd0…` | 与4B采用相同类型的原生接口，分别读取8B检查点、配置、processor和tokenizer，不能用4B路径替代。 |

InternVL-U官方代码固定为`018a59c1…`；[pipeline](https://github.com/OpenGVLab/InternVL-U/blob/018a59c1b69690a33698234128aa04e9b3f46c71/internvlu/pipeline_internvlu.py)和[VLM生成实现](https://github.com/OpenGVLab/InternVL-U/blob/018a59c1b69690a33698234128aa04e9b3f46c71/internvlu/vlm/modeling_internvlu_chat.py)支持上述加载与解码路径。环境按官方要求准备Torch2.6.0/cu124、Transformers4.52.3、Diffusers0.35.1和FlashAttention2.7.4.post1。

Ovis官方代码固定为`55b7ce25…`，环境依据为Torch2.4.0、Transformers4.51.3等原要求。[官方示例](https://github.com/ATH-MaaS/Ovis-U1/blob/55b7ce25507aa6da3cec0b786c1f9a31e781d8ab/test_img_to_txt.py)设置`propagate_exception=False`，[检查点源码](https://huggingface.co/ATH-MaaS/Ovis-U1-3B/blob/cbc005ddff7376a20bc98a89136d088e0f7e1623/modeling_ovis_u1.py)在异常时可能构造mock图。S2输入适配明确设为True，失败须原样记录并停止。

Qwen官方代码/说明固定为`96588727…`，计划运行环境固定Transformers4.57.1，已核对该官方tag具有[Qwen3-VL处理实现](https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen3_vl/processing_qwen3_vl.py)。4B/8B检查点默认生成配置启用采样，本申请统一显式使用`do_sample=False`、`num_beams=1`、`max_new_tokens=128`。三类原生接口均无本任务JSON正确性保证；原始输出严格解析，格式错、未知和截断保留，不修补答案或二次询问。

所有模型均使用明确的本地固定快照、离线模式与原检查点权重，禁止静默改用配置中提到的语言底座。实际加载键覆盖、EOS/tokenizer行为、图像张量、视觉token数、显存与速度仍需在获批资源上核验，当前为空或未验证。

## 少量冻结请求

[S2请求](../../../data/research/paired_strokes_v1/s2_preflight_v1/requests.jsonl)每模型36次，四模型最多144次。先执行四张确定性CPU正控图：红/蓝方块一对，左/右黑圆点一对；每对提示完全一致，只改变图像。4/4通过是继续放行的前提，同时须保存并核对真实图像张量。正控失败时保留“接口或模型失败尚未区分”，停止该模型的后续队列。

| 请求 | 每模型数量 | 统计用途 |
|---|---:|---|
| 视觉正控VPC | 4 | 健康检查，独立报告 |
| 单字OCR E8 | 4 | 健康检查，独立报告，不作为主任务放行条件 |
| E2规范五类序列，随之派生E1笔数 | 4 | 主任务；E1冻结定义不变 |
| E3实例内部点 | 4 | 主任务；士第2笔、木第3笔、口第2笔、永第5笔 |
| E4空间关系 | 8 | 主任务；覆盖六种关系与重复笔型，均具逐项资格且不在几何未知带 |
| E5规范起终点方向 | 4 | 主任务；保持静态规范推断定义 |
| E6配对正确性 | 4 | 主任务；2正对、2同字错序负例 |
| E2纯文字规范先验 | 4 | 单列text_only，不进入图像主分母 |

四字固定为士、木、口、永。32条汉字请求及标签从原完整套件逐条复用ID和原文；新建的只有4条合成视觉健康检查。主表仅24条，健康8条和文字4条分别报告。模型输入适配只接收`model_inputs`；E6描述不会丢失，评价标签及内部规范引用不会进入输入。正控不作为汉字逐笔真值。

## 逐模型GPU申请

| 模型 | 精确申请 | 权重文件合计，十进制GB | 请求级生成上限 |
|---|---|---:|---:|
| InternVL-U | [申请](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/internvl-u.json) | 8.756 | 36 |
| Ovis-U1-3B | [申请](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/ovis-u1-3b.json) | 10.247 | 36 |
| Qwen3-VL-4B | [申请](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/qwen3-vl-4b-instruct.json) | 8.876 | 36 |
| Qwen3-VL-8B | [申请](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/qwen3-vl-8b-instruct.json) | 17.534 | 36 |

每模型独立申请1张A10080，batch1、BF16、无量化，最多一次加载、32次图像条件调用和4次纯文字调用。各有完整36个request ID白名单，种子20261103；额外重试0。申请上限为进程GPU内存72GiB、主机内存48GiB、8核CPU、64GiB本地磁盘；加载600秒、单请求120秒、总墙钟3600秒（包含加载），输入4096 token、单图处理后262144像素、最多生成4608 token。四模型顺序运行时总GPU占用上限4小时，不代表预计耗时或已获资源。

内存、时间和磁盘数值为待执行的预算上限；权重文件大小来自官方元信息，不能据此声称运行显存已测或必定可装载。实际峰值、耗时、价格和模型调用数的测量结果均未产生。执行时须落实独立进程watchdog与资源监控，记录GPU型号/UUID/空闲量、进程显存与Torch峰值、RSS、时间、token数及图像张量。新权重下载和GPU执行都需后续明确授权；本申请未授予这些权限。

加载失败、关键权重未覆盖、输入丢失/模拟替代、非有限张量、OOM、超时、正控失败或资源超限均停止该模型。只终止本任务进程，不驱逐其他任务；不追加prompt、seed、模型或重试。每个白名单槽位保留success/failure/not_run_after_stop，失败分母不缩小。完整原生prompt、输入token/像素/grid张量、生成token、未编辑原答、错误栈、stdout/stderr、环境/加载记录和资源采样均为必交原始产物。

## CPU检查与文件变更

37项针对性CPU测试通过：覆盖概括确认不准入、逐项缺失/unknown不准入、正式分母排除、三类原生输入接线、描述保留、文字条件无假图、配对正控、主表与对照分离及申请白名单。检查登记见[checks.json](../../../data/research/paired_strokes_v1/s2_preflight_v1/checks.json)。单元测试使用的答案只存在于测试内，不写成模型结果。

修改`gold.py`、`intake.py`和审核schema，刷新已有状态/验收；审核原表及数据载荷保持原样。新增`s2.py`、对应回归测试、四模型配置、36条请求与独立标签、4张正控图、4份GPU申请及本报告；同步既有导航。没有删除旧文件或覆盖旧模型结果。PR #5保持草稿可审查状态，main不合并。

准备命令（输出须为新的目录）：

```bash
.venv/bin/python -m scripts.paired_strokes.s2 \
  --output data/research/paired_strokes_v1/s2_preflight_v2
.venv/bin/python -m unittest tests.test_paired_strokes tests.test_s2_preparation -q
```

日后仅对真实保存的`{id, output}`预测进行CPU离线评价：

```bash
.venv/bin/python -m scripts.paired_strokes.s2 \
  --predictions /absolute/path/to/actual_predictions.jsonl \
  --output /absolute/path/to/evaluation.json
```

该命令不调用模型。正式保留测试集尚未建立，开发结果不能写为最终泛化结论。
