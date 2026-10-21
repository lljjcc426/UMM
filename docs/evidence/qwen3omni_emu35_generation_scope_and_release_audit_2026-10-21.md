# Qwen3-Omni与Emu3.5：生成模态、负迁移、扩散分工及发布边界

第九十八批完成已有[L065](../reviews/L065.md)、[L066](../reviews/L066.md)固定v1核心三遍与五项书面检查。[版本/固定发布记录](../../data/qwen3omni_emu35_capability_and_release_audit_2026-10-21.json)保存GitHub/HF revision和未执行边界。目录356条（329论文／研究、27资源），197核心/200项五条书面含未通过项；159条未确认核心（含资源）。本批未删除文件、运行模型、下载权重/音视频或进行真实执行实验。

## 任务先按输入输出界定

| 工作 | 输入 | 输出/附加模块 | 本批所读 |
| --- | --- | --- | --- |
| Qwen3-Omni | 文字/图像/音频/视频 | Thinker文字；Talker语音。Thinking/Captioner仅Thinker | [2509.17765v1](https://arxiv.org/html/2509.17765v1)核心§1–7/T1–16、App9.1/T17–18，指定9.2协议；实际F2/T2/T4/T13/T16 |
| Emu3.5 | 交错图文/参考图 | 主干文字/CoT/图像ID；IBQ或可选SD3.5像素解码；连续视频另用Wan2.2 decoder | [2510.26583v1](https://arxiv.org/html/2510.26583v1)核心§1–7/T1–16；实际F3/F9、T5/T6/T7/T16，未逐图精读补充案例 |

前者视频理解不等图像/视频生成；后者具身输出为子任务文字与关键帧计划，无电机动作和执行成功率。方法的真实可迁移价值需要落到这些接口，不能由omni/world等标签扩写能力。

## Qwen3-Omni：共享理解与语音流式模块

AuT使用2000万小时监督音频预训，中英伪ASR80%/其他语10%/理解10%，输出12.5Hz。视觉采用SigLIP2初始化的Qwen3VL encoder；音频16kHz、128mel、25ms窗/10ms步。TM-RoPE为80ms绝对时间及24/20/20交错时间/高/宽角。Talker读音视中间特征、历史/当前文字token，AR预测第0码本，MTP再AR补残余码本，16组codec每帧80ms，因果Code2Wav出语音。没有完整放弃文字条件，也没有并行生成全部未来语音。

S1冻LLM先adapter后encoder，S2全参，S3 8k→32k；S2称约2T，分项.57/.77/.82/.05/.05T合2.26T，近似与统计口径保留。Thinker轻SFT→教师off/onpolicy KL蒸馏→GSPO；Talker预训→优质CPT/长上下文→多语DPO→speakerFT。数据和lr/batch/GPU等不足完整独立重训。

| 证据 | 原表与解释 |
| --- | --- |
| T16受控Base | 作者称同参数、同模态数据/epochs/schedule、匹配FLOPs；Omni对text MMLU81.24→81.69、EvalPlus69.70→73.96，同时MMLUPro61.81→61.57、MultiPLE65.75→64.79 |
| T16对VL | MMMU57.22→59.33、Info81.17→83.31；RW73.98→71.89、MVBench71.87→69.50、TextVQA81.67→81.65。无方差/非劣界限，不把小负差当统计显著，也不写逐项已证无退化 |
| T4/5后训练 | Instruct Zebra90→76、Poly43.1→37.9；Thinking AIME85→73.7。Base受控结论不能直接覆盖全部后训练模型 |
| T6/17 ASR | Instruct Libri1.22/2.48；Thinking2.22/4.38。Fleurs19语Instruct5.33仍高于GPT4o4.48。思考不普遍改善感知，作者附录承认 |
| T8/18音乐 | GTZAN Instruct93、Thinking89；强感知与推理开销取舍需分任务 |
| T13语音 | 英WER1.39优于所列对照，中文1.07仍高于Cosy3 .71；该表仅内容一致性，无SIM列 |
| T2首包 | 并发1/4/6，音频234/728/1172ms、视频547/1517/2284ms；RTF.47/.56/.66。正文TTFT“largely unaffected”不适用这些幅度 |

T2标题为theoretical，vLLM/torch.compile/CUDAGraph条件有描述，GPU型号、输入长度、网络与分位数不全。234ms不能直接充当任意部署的实测SLA。§5.2作者明确缺综合X→speech评估，主要用text→speech；WER/SIM无法覆盖多轮视听应答自然性。§5.1.3已指出长视频位置外推/context不足；Captioner三例不证明统一定量低幻觉率。

## Emu3.5：三种扩散作用及证据层级

主干通称32B，含embedding为34.1B；64层/hidden5120/FF25600/Q64KV8、vocab282926、context32768。IBQ455M、f16、131072码、256维并用SigLIP蒸馏。统一文字/图像CE用于预训、SFT和GRPO。

1. DiDA把每幅图复制噪声副本，同图噪声token双向相看且读取既有clean上下文；clean文字/图像保持因果。原F9 SVG已直接核图，最初嵌入截图未显示图形已排除。文字仍AR，图像全序列多轮离散去噪。精确噪声分布/步数/完整优化未披露。
2. 可选图像decoder从SD3.5medium初始化，以flow matching读quantized embedding成图，LoRA蒸馏50→4步，输出可为vanilla两倍分辨率。这是像素解码加速，与DiDA视觉ID生成分开。
3. 额外视频decoder从Wan2.2-5B初始化，读关键帧quantized embedding/可选文字/4通道mask生成连续视频，1秒80k、2–5秒80k再1080微调。主干的稀疏关键帧计划和此decoder的连续运动生成分开评价。

63M视频平均6.5min，scene/ASR构成交错序列，平均.27keyframe/s；配对图文500M、视频文30M、X2I27.35M、纯文3T。S1/S2见token10.3/3.5T、lr5e-4/1e-5、700k/240k/b448/TP8CP2/seq32k。SFT T3合150.1B **tokens**，总览“150 billion samples”不能作为样本数。叙事430K/指导960K/探索200K/具身973K是另一统计。

SFT两阶段各3000步、b1024、lr6e-6、16k→32k、视觉loss1→.5。GRPO b640/lr1e-6/rollout8，任务奖励归一1–10后联合一遍，再单图T2I/X2I专门RL。F8 reward上涨不能单独证明无reward hacking或每任务互促；缺少同预算去任务/去奖励/单任务对照。

| 证据 | 原值与边界 |
| --- | --- |
| T5/6 OneIG | EN.564最佳、ZH.529低于Qwen.548；EN diversity.151低于多数模型，整体平均不能代表所有维度 |
| T7/8/9文字 | LeX hard4.39/.87强，easy pnED.43仍劣于Seedream.34；LongText英.976/中.928，中文低于Qwen.946；CVTG WordAcc.9123/NED.9656，NED沿原文↑口径 |
| T10–13 X2I | ImgEdit4.41/GEdit7.59/OmniContext8.82/ICE.637整体优；人脸/风格/部分编辑仍弱。GEditG_O不能由SC/PQ均值代算 |
| T14交错偏好 | 叙事win49.2/tie10.3/lose40.5；指导51.5/9.5/39；探索65.5/0/34.5；具身67.1/2.4/30.5，均ChatGPT判断，非独立人评或执行成功率 |
| §6.6具身样本 | 总数称331，组成10真实+109抽样+192合成=311，保留差异待逐样本清单；5种机器人/50余任务/3–13步 |
| T15重建 | diffusion相对vanilla TACC41.52→51.11/TNED65.39→70.52；rFID.42→.49/LPIPS.08→.10，face不变，额外分辨率/模型混杂 |
| T16速度质量 | AR→DiDA naive512→22s，FlagScale120→10s，分别约23.3×/12×；GenEval.86不变、DPG88.26→87.46、GEdit7.59→7.56，保留小退步与无CI |

ImgEdit737条/GPT4.1；GEdit606条/GPT4o；OmniContext400条/GPT4.1；ICE6538条用AES/MUSIQ/CLIP/Qwen2VL72B等任务加权。另四交错任务仅写ChatGPT，版本/完整prompt/顺序/区间不足。judge认为物理合理无法证明所有接触/动力学约束，图像任务分数也不能替代连续视频时序或真实机器人执行。

## 无独立论文制品也按发布版本核查

[Qwen GH e423585](https://github.com/QwenLM/Qwen3-Omni/tree/e4235853125589c789f06a2dd83e9f4126df5e9d)完整28blob，含cookbooks/demo/Docker而非完整训练仓库；读指定README段、LICENSE首部、web_demo调用及OCR/场景转换notebook代码cell，不读取base64媒体输出。代码Apache2，HF卡license=other、license_name=apache-2.0，原文分别保留。

[Qwen HF26291f79](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct/tree/26291f793822fb6be9555850f06dfe95f2d7e695) config证Thinker48层/128expert top8、Talker20层/top6/16组码本；config声明4.57dev，当前README推荐>=5.2，是制品记录与当前运行建议的不同字段。WhisperFeatureExtractor名称只指前处理，不能据此把AuT识别为Whisperencoder。

README评测Instruct greedy/video2FPS；web_demo却thinker_do_sample=True、默认temperature.7，model.generate返回整体audio后写WAV再yield。它不是论文逐首包输出的完整实现。该demo的vLLM分支只文字，README所述vLLM serve也仅Thinker；不将这些限制扩大为所有外部后端都不能语音。BF16/FlashAttention2最低内存表Instruct15s78.85GB/120s144.81GB是作者报告，非本次实测。

[Emu GH8fcf1da](https://github.com/baaivision/Emu3.5/tree/8fcf1da48f9c5252fe0a0b8dc842e07b6efcd745)完整72blob，读README/ApacheLICENSE首部、generic config、inference/model_runtime/model_utils/generation_utils指定段。[HFef6e632](https://huggingface.co/BAAI/Emu3.5/tree/ef6e632f2cbda5269f766b04e443bbf116cd093e)主干config确认64层、5120、32k、vocab。README明确Emu3.5与Emu3.5-Image两主权重纯AR、DiDA inference/weights为TODO；当前vLLM 4–5×声明与论文DiDA约20×分开。

generic story默认image_area518400/CFG3，文字topk1024/topp.9、图像topk10240/topp1、T1。CFG实际由custom logits processor读取classifier_free_guidance；sampling_params中的guidance_scale1不能误作实际总CFG。main只见Python random.seed，vLLM builder另有seed；不能假设两后端随机性一致。模型BF16/FlashAttention2、decode_code逐图成RGB，未取得DiDA/SD3.5/Wan视频完整发布与训练流水线；model_runtime名为streaming也不自动指视频逐帧输出。

## 实验假设和写作学习

Qwen的可验证假设是早混合与时间对齐在匹配预算下保持原任务并改善视听推理；需Base/SFT/RL逐阶段、任务非劣界限、多seed，控制数据/总FLOPs或模态曝光并明示两种协议。低延迟需相同硬件/输入长/并发、P50/P95、网络和端到端成本，与等质量级联比较。

Emu的可验证假设是交错数据与多任务奖励提高长程上下文，DiDA降低大图视觉序列串行成本；需同主干/数据/decoder的去交错/去RL/单任务和步骤质量-速度曲线。独立人评、时间逆转/状态反事实、接触/可执行约束验证judge是否只看图文合理。

书写/素描可采用关键帧+视频decoder作为强基线，但.27FPS可能遗漏多个事件；插值无法从同一终态唯一确定规范笔顺。必须另有笔画事件/落抬笔、同终态异顺序、未见字/多语字形与实际RGB时序，并对比规则SVG/轨迹渲染。以上为未执行设计。

写作可学两篇按具体瓶颈→接口/模块→训练→分类实验组织；不能照搬其无退化/全最佳/无损/严格物理等强措辞。Limitations保留Qwen长视频与思考退步、Emu欠系统人评与压缩开销，并增加本次版本/单位/样本数/对照与发布缺口。核心阅读通过不代表确认作者全部研究结论。
