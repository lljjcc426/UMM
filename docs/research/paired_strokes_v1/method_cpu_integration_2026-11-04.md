# CPU图文方法原型接入与后续执行顺序

2026-11-04，`codex/research/new`，接入起点`713ab5b0`，S2冻结基线仍为`7c843c37`。本次完成用户要求的第一步：将附件CPU工具接入现有科研分支并核对真实192条训练导出。四模型实际训练前评测尚未执行，后续真实推理等待独立GPU授权；没有启动训练或S3–S6。

## 实际数据与特征输入

| 检查 | 本次结果 | 证据 |
|---|---|---|
| 原训练导出 | 192字/1752笔，描述保留五类序列和终字 | [配对检查](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/pairs.json) |
| 原开发划分 | 192训练、24验证、24开发测试、16审核区；字符/ID/图像分区交集为0 | 同上；正式保留集仍为0 |
| 原RGB输入 | 192条均为3×256×256，范围[0,1]；无裁剪、标准几何或描述进入视觉输入 | [逐条输入记录](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/feature_inputs.jsonl) |
| 原SVG重建 | 复用`gold.render_masks → p0.geometry`，192/192与原PNG逐像素一致 | [重建记录](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/svg_reconstruction.json) |
| 四路CPU特征 | `sft/global/cross/ordered`各处理全部192张真实RGB，16×16 patch网格、宽度32；每路首批一次反向，各有效参数梯度有限且非零 | [特征与梯度](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/features.json) |
| 训练/原生能力 | 优化器step=0，预训练权重=0，GPU/MPS调用=0，原生模型processor执行=0 | 上述证据及[方法配置](../../../configs/research/method_v1_cpu.json) |

`read_pairs`只读窄训练导出和其图像；分区检查另读既有拆分文件，未读取`evaluation_only`或金标。SVG核对在单独审计函数中读取`source_subset.jsonl`，其结果不回填模型特征或目标。没有重新划分样本，也没有把SVG重建通过升级为E3/E4/E5独立真值。

192字中有一组实际反捷径样本：**埃、挨**的五类序列相同，完整描述末字不同。两字都保留在原训练分区；没有追加GPU探针或更改S2请求。终字必须作为监督保留，不能用Unicode真值作为图像预测分支的额外输入。

## 原型接入时的修正与限制

原附件的随机视觉patch没有显式二维位置；局部注意力对一组无位置的patch做查询时，单独改变其排列不会提供可靠的左右/上下参照。本次添加从图像网格直接计算的二维坐标投影，并验证其梯度，不输入标准笔画位置或mask。该修改解决位置输入缺口，尚未证明模型掌握空间关系。

同时冻结各模式未使用的参数，报告实际有效梯度路径，避免把未参与目标的组件计为已验证通路。四种小网络的活跃参数数目为31689、2130953、2135177、2137257；这些差异与随机模块结果均不能支持方法优劣或同预算模型比较。

完整描述从原导出保留，当前CPU小网络的序列头仍只预测五类粗笔型及EOS等9类合同token，终字Unicode只用于独立全局辅助头。没有实现预训练语言模型的完整Description解码、masked visual重建、完整双向融合或程序神经decoder。后续普通SFT须使用同一实际底座的原生tokenizer与EOS，不能将本接口当成强训练基线。

## 共享程序与SVG执行后端

`hanzi_video.render`拆出低层`mask_frames/render_masks_video`，工程catalog入口继续先做原规范计划校验。新`method_v1.program`仅将调用者提供的规范化路径转换为源坐标，调用同一个`p0.geometry.stroke_geometry`和单调执行器，不调用catalog、预期笔序或标准SVG纠正程序。`geometry`保留原默认方形轮廓渲染，新增可选矩形画布及中心线宽度；原8字工程视频与S0–S1回归通过。

重新执行附件的3个程序，均为CPU输入程序：

| 程序 | 实际MP4 | RGB解码结果 |
|---|---|---|
| 土 | [视频](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/videos/tu.mp4) | 52帧，首帧空白，终帧3878墨迹像素，相邻帧墨迹消失0 |
| 士 | [视频](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/videos/shi.mp4) | 52帧，首帧空白，终帧3624墨迹像素，相邻帧墨迹消失0 |
| 土，同几何换序 | [视频](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/videos/tu_swapped.mp4) | 52帧，首帧空白，终帧3878墨迹像素，相邻帧墨迹消失0 |

均为256×256、24fps。正序与换序的未编码首末帧完全相同、五类序列相同，早期过程帧不同；由此构成“终态字图＋粗笔型序列不足以唯一确定实例执行顺序”的具体反例。该构造不提供规范逐笔金标，也不证明神经模型能力。原附件视频和新共享后端的视频分别保留，不用新输出覆盖旧证据。

[原始数值](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/programs.json) · [实际解码帧联系图](../../../data/research/method_v1_cpu_2026-11-04/integration_v1/program_contact_sheet.png)

## 按用户指定顺序推进

1. **真实数据与CPU接入：本轮已完成。** 入口为[工具README](../../../method_v1/README.md)，无参数更新或原生模型结果。
2. **S2：先36条/模型技术预实验，再扩大理解覆盖。** 保持四模型检查点、提示、标签、解码、失败分母和先4正控的放行逻辑；实际输入与视觉接口检查通过后再解释汉字结果。扩大覆盖的1740槽/模型沿用[已有提案](s2_runner_preparation_2026-11-03.md)，依据本轮实际推理的耗时、显存和失败制定新的精确申请，不能自动从144次授权扩展。
3. **强训练基线：待S2结果与单卡可训练性证据后选择底座。** 先记录M0训练前结果，再做M1普通Image→完整Description SFT；然后比较M2全局双向InfoNCE、M3标准因果Cross-Attention、M4有序查询。模型、原生tokenizer/处理器、图像与文本、192/24/24开发划分、种子、优化器/更新数/预算须在训练前冻结，分别报告可训练参数和资源。当前小网络的cross仅为文本查询视觉，不能写成完整双向融合。底座、训练配方、显存和训练预算目前均未确定，没有开始拟合。
4. **程序迁移：同执行器、同输入权限的训练前后比较。** G0源模板上界、G1额外无序几何诊断、G2纯RGB→原始程序分别报告。G2前后都不能输入真实D、标准SVG或规范计划，也不能在评价前做字库纠错；解析/渲染/解码失败保留在固定分母，评价实际解码RGB。有序执行器强制的时间顺序不能归因于模型的规范笔顺能力。跨字符、跨字体、跨底座实验须随后另建来源与字符隔离的保留集并冻结资格；当前无最终泛化结论。

## 下一次真实推理所需授权

现有四份申请均仍为未授权、未执行；本次未改动任何一份申请：

| 模型 | 精确冻结申请 |
|---|---|
| InternVL-U | [internvl-u.json](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/internvl-u.json) |
| Ovis-U1-3B | [ovis-u1-3b.json](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/ovis-u1-3b.json) |
| Qwen3-VL-4B | [qwen3-vl-4b-instruct.json](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/qwen3-vl-4b-instruct.json) |
| Qwen3-VL-8B | [qwen3-vl-8b-instruct.json](../../../data/research/paired_strokes_v1/s2_preflight_v1/gpu_applications/qwen3-vl-8b-instruct.json) |

每模型最多36次、四模型最多144次；每模型先4正控，失败停止，无额外GPU重试，一次加载。申请单卡A100 80GB，进程显存72GiB、主存48GiB、8核、磁盘64GiB，每模型总时长3600秒、加载600秒、请求120秒。四模型顺序执行，各使用独立原生环境，不改seed20261103、BF16、greedy及128续写token上限。资源实际峰值/费用尚未测得。

真实执行仍需用户提供可用服务器/GPU UUID并明确批准对应申请；缺失固定权重时另需明确允许下载这些revision，运行器本身仍仅离线读本地检查点。此后再按[运行器报告](s2_runner_preparation_2026-11-03.md)执行文件完整性、加载键、tokenizer、视觉processor和实际张量检查。用户本轮明确要求“在独立GPU授权后执行”，故纳入科研分支没有自动授予GPU、权重下载、训练或main合并权限。

## CPU验证与改动文件

- 主工程环境运行全库255项：250通过，5项可选torch测试跳过；这些5项由已有CPU torch2.8.0环境实测覆盖。方法定向20项全部通过，覆盖原13项与新增7项真实数据/共享渲染测试。原工程与配对数据定向40项通过。
- catalog、research v1/v2和stage发布结构检查通过。CI新增独立Python3.12 CPU torch作业，避免把torch加入S2或基础工程环境；阶段检查等待两个CPU作业通过。
- 本机仅复用同仓库已有`private/ltx_local/venv312`的CPU运行库，没有启动LTX、MPS或加载任何预训练权重。`.venv`与既有模型环境未修改。

| 文件或目录 | 改动与原因 |
|---|---|
| `method_v1/{paired,fusion,program,cli}.py`、`__init__.py` | 接入附件工具；优化读取，补二维patch坐标，冻结未使用通路，改用共享渲染与现有FFmpeg运行库，增加真实数据CLI |
| `method_v1/{batches,integration}.py`、README及可选requirements | 新增真实RGB/目标padding、四分区/SVG审计、全部192样本的CPU特征检查与运行说明 |
| `hanzi_video/render.py` | 提取共享单调mask执行/编码；保留工程入口的原规范校验、时序和返回证据 |
| `scripts/p0/geometry.py` | 复用SVG/路径进度，新增可选矩形画布与中心线宽度，原默认行为回归通过 |
| `tests/test_method_v1.py`、`test_method_integration.py` | 接入原测试并增加真实数据/共享执行器检查；torch缺失时仅可选模块跳过 |
| `.github/workflows/validate-research.yml` | 纳入method目录触发和独立CPU torch测试，阶段状态继续不授予合并 |
| `configs/research/method_v1_cpu.json` | 固定CPU接口设置和后续对照/信息权限方案，训练底座与配方保持待定 |
| `data/research/method_v1_cpu_2026-11-04/` | 保存附件原始示例/视频/文档及本轮新数据、特征、程序证据，来源分开 |
| 本报告、AGENTS、项目README/STATUS/WORKSPACE_HANDOFF和研究README | 更新入口、本轮CPU范围及用户指定的后续顺序 |

**没有删除既有文件。** 原256字/2243笔、192训练导出、1008条人审、36字逐项资格、全部S2请求/标签/申请、冻结阈值与已有模型结果没有重写；P0/P1/Batch A科学状态和PR #5草稿状态保持。
