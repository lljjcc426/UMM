# S2原生运行器与CPU审核报告

2026-11-03，`codex/research/new`，草稿PR #5。用户已认可`7c843c37a7d360b9482dd6104e3795966134450d`的S2 CPU准备，本次以其为固定基线完成执行代码、CPU检查和后续扩大覆盖方案。状态：**CPU准备完成，真实执行未开始**。新增GPU运行、权重下载、训练、S3–S6及main合并均未获授权。

## 冻结范围与执行顺序

四份[GPU申请](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/)、36条请求、提示、标签、种子20261103、BF16、batch=1及`do_sample=false / num_beams=1 / max_new_tokens=128`全部沿用基线。入口比较这些文件与基线Git内容；不重新生成队列，不改冻结指标或规范。

每次命令只运行一个模型，最多一次完整模型加载、36次生成、零重试。顺序如下：

1. 检查该模型的明确资源批准，确认批准的GPU UUID；未批准时在设备查询和worker创建之前退出。
2. 检查独占空闲A100 80GB、主存、CPU和磁盘；遇到其他任务占用即停止，不干预其进程。
3. 在受watchdog监督的worker中，逐文件核对固定检查点；核对Python/依赖版本，离线加载全模型，检查各组件加载键、参数有限性、tokenizer词表及EOS/PAD/图像token与embedding的对应关系。
4. 每条请求先用原生processor构建输入，保存实际token、RGB尺寸、像素/grid张量、视觉token位置及有效embedding长度，检查4096 token和262144 pixel上限；不截断输入。
5. 逐条执行前4条视觉正控。只有4/4严格解析且正确才发送其余32条。错误、unknown、格式错误、空输出、图像接线或接口异常均停止该模型，保留失败类型与原文。
6. 余下请求按原顺序各执行一次。任何技术失败停止；正常完成后用原冻结评测器计算开发预实验结果。技术中止时能力统计保持空值，所有36个槽位继续保留。

前三项中的检查点与原生运行时检查在未来获批资源上执行。本轮没有可用于这四模型的完整本地检查点，不能将CPU替身测试计作这些检查已经通过。

## 原生接口

| 模型 | 加载与调用 | 输出与图像证据 |
|---|---|---|
| InternVL-U | 加载固定源码和完整pipeline的VLM、generation decoder、VAE、scheduler及processor；逐组件取得`output_loading_info`；沿用原生`processor → pipeline._generate`文字路径 | 捕获送入tokenizer的实际模板文本；保存视觉模型forward输入；返回续写token，直接解码 |
| Ovis-U1-3B | 固定检查点remote code，`AutoModelForCausalLM`；`preprocess_inputs(propagate_exception=True)`；以原生`inputs=`参数向`model.generate`传入token | 计算视觉atom替换后的真实embedding长度；保存AIMv2视觉tokenizer实际forward输入；返回续写token，直接解码 |
| Qwen3-VL-4B/8B | 分别加载自己的固定检查点与`AutoProcessor`；`apply_chat_template`后调用`generate`，SDPA | 保存image grid和实际视觉forward输入；核对原输出的输入前缀后，仅截去该前缀，按冻结方式解码 |

图像请求必须同时有非空、有限、非恒定的原生像素张量和视觉token位置，且实际调用视觉模块。纯文字请求不注入图片或视觉占位。没有JSON修复、补问或失败后重试。正控错误只说明该次视觉接口/模型组合未通过放行检查，不能直接归因于汉字理解能力。

[检查点文件清单](../../../configs/research/paired_strokes_v1/s2_checkpoint_files.json)由此前保存的官方固定revision元数据生成，共61个运行时文件，其中12个权重文件；包含配置、tokenizer、模板、remote code及各权重的官方大小和摘要。实际执行时做一次顺序流式核对；小文件用Git blob SHA-1，LFS载荷用SHA-256，不在每条请求重复检查权重。官方模型/源码地址和版本见[已冻结模型配置](../../../configs/research/paired_strokes_v1/s2_models.json)。未下载权重或tokenizer载荷。

## 资源限制与原始产物

外部CPU控制器每秒采样一次本任务进程组的显存、RSS和磁盘占用，限制为72GiB、48GiB、64GiB；worker设置8核亲和性和线程上限。总时长3600秒，检查点核对与加载阶段600秒，每个请求包括预处理、生成和产物保存120秒。超过上限、采集异常或出现其他GPU任务占用即停止本模型。仅终止控制器创建的worker进程组，SIGTERM后最多等待5秒再SIGKILL。监控为采样检查，存在采样间隔及`nvidia-smi`查询延迟；显存实测还保存PyTorch分配/保留峰值，预算上限不代表实测使用量。

每次执行使用新的输出目录；不恢复旧worker或重复执行失败槽位。模型、GPU UUID、原批准、固定申请、请求、runner版本和环境保存在目录根部，模型worker不接收真值标签。`HF_HUB_OFFLINE=1`、`TRANSFORMERS_OFFLINE=1`，全部加载使用明确本地路径，不提供下载或替代模型分支。

| 产物 | 内容 |
|---|---|
| `state.json`、`events.jsonl` | 加载尝试、生成开始次数、36槽成功/失败/停止后未运行、控制门状态；不缩分母 |
| `checkpoint_integrity.json`、`loading.json`、`loaded_contract.json` | 文件核对、逐组件missing/unexpected/mismatched/error信息、词表/embedding/视觉处理器契约 |
| `snapshot_metadata/`、`environment.json`、`load_resources.json` | 原配置/tokenizer及源码文件、完整依赖版本、加载时显存和时长 |
| `inputs/`、`requests/<id>/input.json`、`formatted_prompt.txt` | 原RGB、原请求、实际模板、token IDs、视觉位置和尺寸；不拼接标签 |
| `native_inputs.pt`、`model_inputs.pt`、`vision_forward.pt` | processor输出、实际送入生成的设备/dtype转换后张量、实际视觉forward接收的张量 |
| `generated_tokens.pt`、`output.json`、`raw_output.txt` | 完整输出token、续写token、未经修复的解码文本、达到128 token上限的标记 |
| `result.json`、`resources.jsonl`、stdout/stderr及error日志 | 单请求显存/时间、外部资源样本、完整异常堆栈 |
| `predictions.jsonl`、`evaluation.json` | 已返回原始文本、严格解析和资格感知评测；技术中止时保留槽位记录，能力统计为空 |

`.pt`产物是未来执行保存的原始本地张量，不属于本轮模型输出。本轮CPU测试仅在临时目录写入明确标识的替身产物，未纳入研究结果。

## 后续获批执行入口

批准文件由后续明确资源授权形成，至少包含下列字段。现阶段不创建`gpu_authorized=true`的真实批准文件：

- `baseline`：上述完整基线提交；`gpu_authorized`；`approval_text`；批准的`gpu_uuid`。
- `model`、`revision`、`approved_request_ids`、`resource_caps`：逐项等于该模型冻结申请。
- `maximum_generation_calls=36`、`extra_retries=0`、`allow_training=false`、`allow_download_weights=false`。

后续如需补充下载批准，下载与文件落盘应单独办理，运行器仍只读取已完整准备的本地检查点。每个模型使用[冻结环境](../../../configs/research/paired_strokes_v1/s2_models.json)的独立Python环境，不在本机CPU测试环境安装模型依赖。

```bash
/approved/model-env/bin/python -m scripts.paired_strokes.s2_runner \
  --model qwen3-vl-4b-instruct \
  --checkpoint /approved/checkpoints/ebb281ec70b05090aa6165b016eac8ec08e71b17 \
  --authorization /approved/s2-qwen4b.json \
  --output /approved/runs/s2-qwen4b-first-attempt
```

InternVL-U另加`--source-root /approved/InternVL-U`，该Git工作树须干净且HEAD等于已冻结源码revision。其余模型名为`internvl-u`、`ovis-u1-3b`、`qwen3-vl-8b-instruct`。不得通过改名批准文件跨模型复用批准或自动运行全部四模型。

## 扩大训练前评测覆盖方案（提案，未执行）

先完成当前四字技术预实验并检查原始输入、正控、失败、耗时及资源峰值。通过后，再冻结新版本的开发评测队列和逐模型资源申请；不把当前36条申请扩展为额外调用许可。

建议复用现有256字和完整套件，保持192/24/24开发划分及16字审核区，覆盖不同笔数、五类主笔形、重复笔型、结构和易混关系。按当前逐项资格，E3/E5限36字，E4限27字；未知与不适用保持单列，不补造逐笔金标。可复用请求数量如下，均沿用原提示和标签：

| 类型 | 每模型调用数 |
|---|---:|
| 原4条视觉正控 | 4 |
| E8字识别健康检查，覆盖256字 | 256 |
| E2规范序列，派生E1笔数，覆盖256字 | 256 |
| 同256字纯文字规范先验对照 | 256 |
| E3实例身份，当前合格请求 | 54 |
| E4空间关系，当前合格且有确定真值的请求 | 84 |
| E5方向，当前合格请求 | 54 |
| E6现有正负配对条件 | 776 |
| **提议上限** | **1740/模型，四模型6960** |

E6各负例条件数量不平衡，须同时按条件报告分母；E3/E4/E5按字符分组报告，不能把同字多题当成独立字符。E6R暂不纳入本提案。现有36条中的相同模型/revision/输入/解码请求，应复用有效原始结果，不能重复调用后择优；届时申请列出复用和新增ID，最多1740为完整报告槽位数。技术正控是否复用或按新运行会话再测，须在新申请中明确，不能隐含增加调用。

扩大方案的GPU时长和资源预算在当前36条实际测量后制定；本轮不虚构吞吐、费用或可执行总时长。正式保留测试集仍为0；这批最多支持现有来源、已暴露开发字的训练前能力描述。最终泛化评价须另行建立来源/字符隔离的保留集，先明确来源许可与相应真值资格，再冻结并独立评测。

## CPU验证与文件变更

新增16项测试，覆盖未授权入口、冻结内容/批准一致性、一次加载零重试、4正控放行/失败停止、技术失败及超时分母、资源上限、仅终止自有进程、文件损坏/缺失、三种原生适配器的图像/纯文字输入和输出截取、实际视觉forward缺失。模型/processor双替身用于CPU接口接线检查，不替代真实运行验证。

实际CPU结果：S2定向24项通过，全库235项通过；catalog、research v1/v2及阶段发布结构检查均通过。未以测试通过推断模型能力或科学门槛达标。

验证命令：

```bash
.venv/bin/python -m unittest tests.test_s2_runner tests.test_s2_native_adapters tests.test_s2_preparation -v
.venv/bin/python -m unittest discover -s tests -q
.venv/bin/python scripts/validate_catalog.py
.venv/bin/python scripts/validate_research_plan.py --output reports/research_plan_v1_validation.json
.venv/bin/python scripts/validate_research_v2.py --output reports/research_plan_v2_validation.json
.venv/bin/python scripts/validate_stage_release.py
```

本次新增运行器`s2_runner.py`、原生适配`s2_native.py`、监控`s2_watchdog.py`、文件清单`s2_checkpoint_files.json`、两份CPU测试及本报告。修改AGENTS、主README、项目STATUS/WORKSPACE_HANDOFF及本目录README，更新当前入口和授权边界。**没有删除既有文件**；S0–S1数据、全部原审核、冻结S2文件和历史报告均保留。本次交付不产生任何模型能力结论。
