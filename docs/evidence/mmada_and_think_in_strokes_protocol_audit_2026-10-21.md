# MMaDA 与 Think in Strokes：联合训练、过程监督与实验条件

第七十六批补完[L063](../reviews/L063.md)和[L029](../reviews/L029.md)明确范围核心三遍/五项书面检查。350目录、163核心/165书面，187条尚未确认核心三遍（含资源）。无新增独立论文、文件删除、权重下载或模型运行。

## 固定来源与任务分类

| 工作 | 本批原始来源 | 输入输出及边界 |
| --- | --- | --- |
| MMaDA | [NeurIPS2025主会正式页](https://proceedings.neurips.cc/paper_files/paper/2025/hash/caa934a507a952698d54efb24845fc4b-Abstract-Conference.html)、[41页PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/caa934a507a952698d54efb24845fc4b-Paper-Conference.pdf)、[官方Supplemental ZIP](https://proceedings.neurips.cc/paper_files/paper/2025/file/caa934a507a952698d54efb24845fc4b-Supplemental-Conference.zip) | 图文→文字推理/理解/静态图；DOI10.52202/085713-4636。无书写或视频事件输出 |
| Think in Strokes | [arXiv2604.04746v3](https://arxiv.org/abs/2604.04746v3)、[固定PDF](https://arxiv.org/pdf/2604.04746v3) | prompt→多轮文字计划/整图草稿/检查/修订→终图；无显式笔坐标或规范笔序 |

Think in Strokes固定PDF页边提交April8、首页自署Date April9,2026。此前未固定HTML中的August24日期不能沿用。MMaDA正式版主表/消融编号与旧arXiv笔记不同，以正式版为准。两条修订保留Git历史。

## MMaDA：共享离散恢复目标不等于全部组件同构

LLaDA8BInstruct初始化，文本LLaDA tokenizer、图像Show-o MAGVIT-v2 f16/8192码本，512²图像变1024离散码。双向主体共享masked CE、1/t权重，prompt保持完整；统一CoT reasoning/result后再UniGRPO。文字64token块半AR，图像全块cosine remask。摘要“去掉模态特定组件”只能限于共享主体/目标，两个tokenizer和采样协议仍有区别。

正式p4 Fig2框架、p6 Eq3–5和p21 T6/奖励曲线已实际核看。噪声恢复迭代没有真实绘画时间含义，不能用去噪动画充当笔顺视频。

## 正式版结果中的反例

| 比较 | 正式结果 | 可支持的范围 |
| --- | --- | --- |
| T2理解 | MMaDA POPE86.1/MME1410.7/Flickr67.6/VQA76.7/GQA61.3/MMMU30.2 | 高于部分基线，MME/VQA/GQA/MMMU低于LLaVA1.5；MME/MMMU低于SEED-X，Flickr低于Chameleon |
| T3生成 | GenEval.63 / WISE(Natural).67 / ImageReward1.15 / CLIP32.46 | 正式表列名Natural，旧笔记“文化.67”纠正；Position.20/ColorAttr.37低于Janus.46/.42 |
| T4语言 | MMLU68.4 / GSM73.4 / MATH36 / GPQA28.4 | 均低于Qwen2相应70.3/80.2/43.5/30.8；TruthfulQA43.1也低于LLaDA46.4，摘要广泛胜过强LLM的表述不能直接照搬 |

正式T6 Stage1→CoT→RL：GSM17.4→65.2→73.4，MATH5004.2→26.5→36，Geo8.3→15.9→21，CLEVR10.3→27.5→34.5，CLIP23.1→29.4→32.5，IR.69→.84→1.15。加数据、训练和奖励共同改变，支持整套后训练有效，未隔离CoT形式或跨任务迁移。Fig3三曲线同时上涨也没有joint-vs-separate对照；§5 Stage2 120K–200K的说法与§4 50K阶段口径不明。

正式T5图像1024/50/15步CLIP32.8/32.0/31.7；文字1024/512/256步MMLU66.9/66.3/65.7；理解caption CLIP35.5/36.1/35.4非单调。网络调用步数少不能直接推出同硬件端到端延迟相同倍数降低。

训练64A10080GB/global1280/AdamW初始5e-5 cosine，预训200K+400K、CoT50K、RL50K均是步数。生成50K测试prompt与teacher/train的去重、精确源配比、RL的G/μ/β/clip和原表配置未完整给出。图像CLIP和ImageReward兼作奖励与主指标，独立评价仍必要。

## UniGRPO：数学记号、正式补充代码和后续工程实现分开审查

正式Eq3/4将π′定义成logp期望/平均，Eq5直接作π′比值并写概率KL。字面上这与exp(logp_new−logp_old)不同，平均logp也不等于严格序列似然。这个疑点不能自动推成原实际训练用了错误ratio。

正式Supplemental ZIP的README Stage3仍写录用后发布RL。其generate.py和modeling_mmada.py用`torch.topk`默认最大confidence解除mask，与正式Appendix C“最低confidence解除mask”字面相反：低置信remask与低置信unmask需要区分。

新找到官方关联[dLLM-RL固定10b4fd1c](https://github.com/Gen-Verse/dLLM-RL/tree/10b4fd1cba83e4496c20585dc2fd01dc02f20255)。详[制品审查JSON](../../data/mmada_unigrpo_artifact_audit_2026-10-21.json)，静态阅读范围明确，无执行：

- `train/train_mmada_v_policy.py`先缓存old token logp，再用`exp(clamp(logp_new−logp_old,-10,10))`作PPO比值，按mask平均。该代码没有直接相除logp。
- 所查KL用缓存old，未用另一个固定reference；random-mask样例每样本独立取两次t∈[.1,.9]，并非论文Algorithm1那套均匀跨迭代覆盖的完整配置。
- `configs/rl_mmada_v.yaml`是SEEDBench_IMG_32图像理解示例，group16、eps.2/beta.01、lr1e-6、50外轮；`reward/rl_reward_v.py`是答案正确性组归一，未实现本文件内CLIP/ImageReward聚合。

因此，不能再笼统记“无RL实现”；也不能把这个后续MMU配置当作原论文全部三任务RL复现协议。原始多任务训练版本/奖励聚合仍待确认。

## Think in Strokes：监督的是可编辑图像状态

场景图子图扩展→Flux-Kontext生成/GPT筛选→丰富remove/swap/refine操作；再从自身轨迹采样“步骤文字与全prompt冲突”，用Gen-Ref扩展“图像与步骤指令不一致”的critique。BAGEL-7B交错SFT：文字AR CE含视觉边界，图像rectified-flow MSE，两项按lambdaCE组合。噪声时间t与语义编辑轮分开。

固定PDF T1为32012多轮样本（平均3.51图/最多5）、15201冲突（6905正/8296负）、15000图文对齐（5000正/10000负），合62213。正文称alignment balanced与1:2不符。teacher版本、过滤阈值、源prompt去重/留出和总合成成本未给全。

实际p4框架展示移除多余人物；p7主表/公式、p8 WISE、p10全部消融已核。整图可重写、删除，无法保证纸墨单调累积或动作可执行。Introduction把一次整图生成描述成single-forward-pass，也应限定为单轮输出；扩散图像生成通常含多次网络评价。

## 主表、增幅与成本不能混写

| 项目 | 固定PDF实际行 | 原文差异或限制 |
| --- | --- | --- |
| GenEval | T2 BAGEL官方复测.77→.83，6pp；Counting.76→.75下降，Position.51→.72，Attr.56→.69 | Introduction/Conclusion写.79→.83；表注/结论又写5%absolute，互不一致；旧笔记“主表.79”本批纠正 |
| WISE | .70→.76，6pp/约8.57%relative；Culture.76→.74、Space.75→.73下降；Time+.13、Chemistry+.20 | 表注8.5%absolute及近15%领域概述不准确；对FLUX.50→.76为26pp/52%relative |
| 训练条数 | 本法62K vs PARM RL688K，约11.1倍 | 不含teacher/底座与每轨迹图数，不能称总数据预算等比例降低；Intro写两者8倍不符 |
| 推理成本 | 本法平均2.62轮×50=131采样步，PARM bestof20×50=1000，约7.63倍 | 无同硬件耗时/文本AR/上下文/外部teacher成本；GPTInspector表中50是否含初稿不清 |

T5多样编辑比仅add提升Position/Attr；T6自采样critique .87/.72/.69优于scenegraph .83/.70/.67。T7仅文字监督更改善Position、仅图文更改善Counting，合用.75/.87/.72/.69最高，支持此设置互补。未报同数据量/过滤开销、多seed区间，不能扩为所有任务的必要性定理。GPTPlanner .60/Inspector .80与本法.83只说明这些特定组合，不足证明所有训练外部反馈必然无效。

8H100全参数10000steps、packed33000tokens、lr2e-5 cosine；batch/累积/lambdaCE、每轮CFG/采样上限/停止失败率、完整评测脚本缺项。未核实独立公开模型/数据/代码链接，不以检索不到推断绝对不存在。此文未测完整理解保留或真实绘画事件。

## 因果假设、实验与写作学习

MMaDA的优势假设是全局静态离散恢复、事实CoT和并行补全有助组合/知识生成；Think in Strokes的假设是视觉草稿反馈和可判定中间状态有助位置/属性纠错。应按相同数据曝光、teacher、总优化/搜索FLOPs比较联合/独立模型，终图SFT/多轮无critique/双类critique；同时报告失败分项、理解遗忘和独立评价器。

对中间反馈做屏蔽或错误critique干预，标注正确未完成/真错误/未来计划省略，量化误报与修复，避免只选成功例。绘质量对NFE、文本token、上下文、秒数与数据制造成本曲线。严格书写另加不可擦除画布、合法方向/顺序/停笔与实际可见RGB事件；整图修订收益不能直接当笔顺能力。

可学论文用明确歧义或后训练缺口组织Introduction，让数据/机制/消融对应；Claim保留反例，Method统一概率与log概率记号、噪声时间与语义时间，Limitations写实际协议和公开材料缺项。以上均为审查与未运行实验建议，未声称独立模型复现或新颖性闭环。
