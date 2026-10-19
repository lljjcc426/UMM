# 交错推理、成本和latent策略审查

2026-10-20，N13/U07–U12/L178八项存量；不增加独立论文计数。各项七字段、五个研究问题及写作分析见[逐篇笔记](../reviews/README.md)。U07/U10/L178完成本批五项书面理解检查，未计时口试、未执行模型。

## 接口和贡献

| 工作 | 本次已核输入输出/贡献 | 未被证明的能力 |
| --- | --- | --- |
| Unwritten Benchmark | 无墨迹音视频→英文单词；数据/评测 | 不生成书写视频；性能低不唯一证明架构缺乏因果机制 |
| UniDisc | 文字和LFQ图token联合mask恢复 | 去mask时间不等笔顺；无视频生成实验 |
| Zebra-CoT | 182384图文交错轨迹及SFT | GT前缀收益不等生成图的必要性 |
| ThinkMorph | BAGEL辅助图/文字互补训练和多候选分析 | 视觉thought因果中介尚需直接干预 |
| Monet | QwenVL连续hidden思考及蒸馏/RL代理 | hidden无图像解码器，不能当通用图/视频生成 |
| Omni-R1 | 感知码本损失/平滑奖励+交错RL | Zero仍有791合成SFT，TV不保证语义正确 |
| WEAVE | 多轮静态编辑数据、基准及BAGEL微调 | 单轮多参考训练不等完整长对话训练；无连续笔画事件 |
| Drawing and Recognizing | 类条件GRU轨迹与独立辨别RNN | 识别ensemble98.15%不能当生成/笔顺正确率 |

## 数值和协议纠偏

1. [Unwritten v1](https://arxiv.org/pdf/2608.14558v1) Table1 GeminiPro audio10.04%、Table2 Retrace11.69%、Table3自然整词13.15%；摘要均低10%的表述过强。人类MV80.78而AV77.01，不能统称全部模态人类超过80%。人类仅300文件子集，模型10491文件；比较需对齐样本。来源编号2608与页面/正文日期2026-05-15不一致，照实标注，未自行修定日期。
2. [UniDisc](https://arxiv.org/pdf/2503.20853v1) AppH GenEval.42低于SD1.5 .43；COCOFID23.86劣于CoDi22.26，MJHQ18.67则优于19.87。主生成实验有按同验证loss调整AR训练量的比较，ISO-FLOP是另一组，不能统一声称同预算。约13.2倍拟合对比还涉及精确AR似然与扩散上界口径。
3. [Zebra v2](https://arxiv.org/pdf/2507.16746v2) Table2列7benchmark，表注写8；VisuLogic8.50→21.80是13.30pp，正文不同段13.1/13.3保留冲突。脚手架提供真实中间步骤，更多信息可直接帮助答案，不能直接归因视觉形式。
4. [ThinkMorph v3](https://arxiv.org/pdf/2510.27492v3) PDFp16 AppB3/表6已视觉核。交错N4=4269token，文字N8=2879，前者更多；对应准确70%/68%。原文称前者“更少token”与表矛盾。这不否定更高准确率，但该例不能支持所写成本优势。图FM每token计算还不同，需真实GPU时间。ChartQA文字81.66高交错79.78；三模式3000step和最终8000step不要混表。
5. [Monet正式CVPR](https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_Monet_Reasoning_in_Latent_Visual_Space_Beyond_Image_and_Language_CVPR_2026_paper.pdf) Table3的55.50−45.75=9.75是百分点；表行名relative不能将相减当相对百分比。arXiv主文warmup4epoch与附录3epoch不一致；验证选K策略未齐，不能给单一默认K结论。
6. [WEAVE正式CVPR](https://openaccess.thecvf.com/content/CVPR2026/papers/Chow_WEAVE_Unleashing_and_Benchmarking_the_In-context_Interleaved_Comprehension_and_Generation_CVPR_2026_paper.pdf) Table4 RISE spatial14→21为50%相对，正文说spatial/logical均100%，只有logical1.2→2.4符合。BAGEL.446→.640保留原分，不能照搬正文42.5%。arXiv附录明确随机抽单轮训练，可包含多图，不能解释为完全无历史信息，也不能说完整长对话端到端训练。

以上按原表解析和算术核查，不是独立模型成绩。未据个别算术问题否定整个方法。

## Monet公式与发布实现

固定[Monet代码08939998](https://github.com/NOVAglow646/Monet/tree/08939998d3d643a73a316e349faa34f420429153)。[runner](https://github.com/NOVAglow646/Monet/blob/08939998d3d643a73a316e349faa34f420429153/RL/monet_models/vllm/monet_gpu_model_runner.py)第1326–1337行注释说Gaussian采样，实际sampled=mu，随机噪声被注释；隐状态直接反馈并发出float16记录。[actor](https://github.com/NOVAglow646/Monet/blob/08939998d3d643a73a316e349faa34f420429153/RL/verl/workers/actor/dp_actor.py)135–158按−||z−mu||²/(2sigma²)给latent打logprob，300–303替换相应位置。

论文Eq8比率exp(−||hold−hθ||²/(2sigma²))可作距离代理。若确实相同context且新旧参数未变，hθ=hold，导数为零；这是条件数学事实。后续文字更新、浮点/跨引擎实现差异会使其非零，完整运行路径尚未核验，不能推出整个RL无效或主表伪造。确定性均值行为策略与非退化Gaussian分布不相同，“标准无偏策略梯度”解释需要进一步论证。

公开launcher还提供难度(0,.6)在线筛样、重复惩罚、Gemini API辅助判题、sigma10/rollout8/8GPU；复现时要记筛选/判题成本和模型版本，不能只照paper概述“accuracy+format”。本次不执行训练或API判题。

## 非论文制品与评价口径

[WEAVE发布代码dfc17dd9](https://github.com/weichow23/weave/tree/dfc17dd997f754f4860e195a412d414d074eb9ae)含eval/infer及HF数据/模型指针。README明确Image #i是images数组中的图号，非轮号；推理要一次替换引用。summarize82–109按是否有ACC采用不同权重，和附录两套公式一致。可理解/可生成模型的Avg含义不同，不宜混成同一种能力榜。

[TPAMI元数据](https://api.crossref.org/works/10.1109/TPAMI.2017.2695539)确认L178正式卷40(4):849–862/2018-04，2016 arXiv的已读内容与正式版本尚未逐页比对。其30分量GMM、pen-down/up/end和GRU是严格书写任务需面对的历史基线；“早期方法没有时序”一类泛称不成立。

## 后续验证

保留/移除/打乱/GT替换视觉thought或latent，并固定文字上下文，区分训练收益和测试中间图的因果贡献。对比同内容文字、规则渲染/轨迹oracle，按实际FLOPs/延迟/图NFE匹配预算。TV奖励测试常量码图、细笔画和正确边界，避免平滑等价正确。下一批继续25条摘要和5份第一遍，再补已有笔记未读范围，不把下载成功计作精读。
