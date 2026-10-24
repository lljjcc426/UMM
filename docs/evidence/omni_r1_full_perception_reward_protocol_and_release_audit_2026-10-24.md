# Omni-R1：完整感知奖励、统一推理协议与发布链审查

第一百七十七批完成[U11](../reviews/U11.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/omni_r1_full_perception_reward_protocol_and_release_audit_2026-10-24.json)。358目录（331论文／研究、27资源），282核心/287书面含未通过项；待完成核心深审49篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2601.09536v2)、[主源2](https://arxiv.org/html/2601.09536v2)、[主源3](https://arxiv.org/pdf/2601.09536v2)、[主源4](https://aclanthology.org/2026.findings-acl.1937/)、[主源5](https://aclanthology.org/2026.findings-acl.1937.pdf)、[主源6](https://github.com/ModalityDance/Omni-R1/tree/a10fbb3d9d5d8a23277c93fad7f914a024458301)、[主源7](https://huggingface.co/ModalityDance/Omni-R1/tree/ef1738f65361872e43ef7d4a8eb5320cdc453b4f)、[主源8](https://huggingface.co/ModalityDance/Omni-R1-Zero/tree/7cbd5e59c987cebf0703c3396808012ead1962f4)、[主源9](https://huggingface.co/datasets/ModalityDance/Omni-Bench/tree/b6b5d077eccff3324f7ff634f2adfdd9e25d908f)。

## 研究问题

能否让同一原生图文生成底座通过中间功能图统一zoom/框/辅助线/标记/状态预测等多种视觉推理技能，并在缺人工交错轨迹时从文字CoT启动SFT+RL？检验最终正确率、功能图保真与跨任务迁移，输出静态辅助图和文本答案，未提供在线笔顺或视频生成目标。

## 现有不足

现有单技能/工具专用协议限制任务迁移；普通图像生成质量不能直接保证定位、几何/连通性与功能性，人工交错轨迹昂贵。作者用码本感知对齐和平滑奖励稳定功能图，并提出Zero自生成监督；是否保持原图内容、是否为答案所必需，需要额外干预而不能从可视化单例推出。

## 贡献

四Uni-Tasks/四Uni-Skills框架及800例Omni-Bench；PeSFT在Anole/BAGEL底座上将CE加冻结码本投影MSE，PeRPO将答案、格式、2D码本TV奖励结合组相对PPO；Omni-R1-Zero以791条M3CoT文字CoT种子生成逐步图，再走同SFT+RL。Grounding含ZOOM/BBOX，另AuxLine/Marking/VisualPrediction，因此四技能对应附录五原子动作，并无数量矛盾。主要为后训练/奖励与任务协议，未将底座生成架构归为新发明。

## 输入、模块、输出与公式

原图+问题→VQ图token/文字token同序列→AR生成文字解释与BOI–图码–EOI段→继续AR文字/图直到最终答案。发布Anole脚本单次generate完再解码保存图，没有外部zoom/绘线工具循环；附录A Eq18–22却用动作选择+确定性renderer更新状态形式化，和主文原生直接生成/当前入口应分开，尚缺动作到原生token的可执行对应。Zero每文字step一图用于合成训练，Zero不等于无SFT、无文本标注或zero-shot。

## 模型结构

Anole7B继承Chameleon离散AR；HF两卡配置32层h4096/32Q及KVheads/FFN11008/词表65536/RoPE10000，图VQ8192码×256维、默认1024图token对应32×32。普通checkpoint最大位置5120、Zero9900；不将入口max_length12000视为已验证支持。PeSFT Eq1 CE监督有效completion图文，Eq2将生成器隐藏态W:h4096→256对齐冻结码本GT向量，Eq3 λ=1。当前trainer图片段h[start:end]与同位置input_ids比较，CE另shift预测下一token，二者目标对齐不同；promptBOI标签-100排除输入图。loss_net以独立Trainer属性传入，states_to_hidden未注册到model，父Trainer.create_optimizer只遍历model.named_parameters，所读入口没有额外optimizer或挂载步骤；因此该发布路径未见投影参数加入优化器/模型保存，需作者补全实际训练接线，不外推私有实验也如此。BAGEL使用连续生成底座，其PeRPO实现/完整训练链当前未发布，不将离散TV代码默认直接套所有主表模型。

## 数据分布与划分

Omni-Bench四slice：Natural VStar100，Structured ArxivQA100+ChartQA100，Diagram Geometry3K100+MathVista100，VisionOperational ViC300，共800；最终均值权重100/200/200/300，非四slice等权。PeSFT从182K Zebra-CoT抽样但本次确切数未给；Zero791条M3CoT文字种子自生成图。RL约10%Zebra加1000 ArxivQA与250 Geometry3K train，训练/评测来源重叠本身不证明同样本泄漏，但尚缺原图/题ID清单和隔离核。HF OmniBench卡片称800、image为base64 list、question/answer字符串，dataset-api固定提交和文件清单核；未下载完整parquet，卡片默认split名train不可自动当论文训练集使用。

## 指标与评价协议

OmniBench用GPT judge只比GT和模型答案，T7完整prompt允许数字/单位/同义与无序列表；多选规则以提供options为条件，但User模板只有GT/ModelAnswer，无question/options字段，缺具体模型快照、T、重复稳定性与实际评判入口。训练规则reward与评测LLM judge分别记录。一般七指标先MME-P×.1、MME-R×.25再均值，POPE为F1，其余准确率；这是人为缩放混合分数，不是七任务共同准确率。无置信区间；小slice少数题与随机推理可影响相对百分比，未测功能图全量正确率/延迟/FLOPs。

## 对比方法

按底座分组Anole base/Zebra/Omni/Zero，BAGEL textCoT base/Zebra/Omni，Qwen2.5VL7B base/MMEureka/DeepEyes/MINT另组。BAGEL Omni .402与Qwen base .374差.028，但数据/训练/生成预算未等配，不能据此归因生成范式普遍胜理解模型。论文按30/60与10/20/30 RL步区分M/L和ZeroT/S/M，无全部统一算力匹配文字/工具基线、相同视觉操作GT或固定答案前缀干预；不把底座同7B标签视为总参数和推理成本已一致。

## 实验条件和发布边界

T6 LR1e-7/warm5/wd.1/KL.003/entropy.001/gradclip1，clip下.2上.28；seq-mean-token-mean；train64 prompts/gen192/PPOmini16、每prompt16响应、T1/topP.95。gen192是采集batch与16候选是不同参数，不直接判乘法矛盾。OmniM/L 30/60 RL步，ZeroT/S/M10/20/30。固定GHa10fbb3d9d5d8a23277c93fad7f914a024458301 5170树项/4374blob（含vendorTransformer），只读根README、PeSFT三文件、PeRPO rewards/config全文及Inference关键输入/生成/解码/默认段、vllm主要dataset/生成/参数段；vendor Trainer.optimizer与Chameleon映射/前向CE选段。README将端到端PeRPO与Zero合成标待发布，yaml customreward路径/metric空且filter_groups.enable=False，不能充当论文动态筛选已启用的完整recipe。HF普通ef1738f65361872e43ef7d4a8eb5320cdc453b4f、Zero7cbd5e59c987cebf0703c3396808012ead1962f4各12文件/两权重shard清单及README/config核，无权重下载。HF示例普通T.5、ZeroT1，根推理默认T.5但--do-sample默认关、maxLength12000；vllm T1/topP.9/maxNew1024、只保存prediction不含GPT判分链。未执行模型。

## 主结果

T2全部14行与T3全部7行保留结构化表。OmniBench Anole base .081，Zebra .129；OmniM .153（.440/.135/.115/.093）、L .153（.420/.175/.090/.090），相对base +87.7%；ZeroT .154、S .138、M .159（.410/.170/.120/.093），相对base +89.2/+69.2/+95.4%。M Structured .135<base .140，不能说每slice均改善；ZeroS→M主任务增而一般表降。BAGEL base .286→Zebra .333→Omni .402，Omni四slice .560/.706/.498/.083，相对+40.7%，绝对约+11.6pp。Qwen组base/MMEureka/DeepEyes/MINT .374/.397/.380/.363。按展示三位小数重算的末位差可由slice取整解释：Anole base65/800=.08125、Omni122/800=.1525、ZeroM127/800=.15875分别给87.6923%和95.3846%，不将.153小数差误报主表算错。T3缩放平均base22.25、Zebra38.12、OmniM46.23/L48.29、ZeroT45.73/S50.19/M45.16；ZeroS最高但多RL并非逐指标/均值单调，ZeroT MMVP36.67低base39与Zebra37。

## 消融及进一步实验

T4 ZeroM四slice .410/.170/.120/.093 Avg.159，去PeRPO .390/.130/.075/.033 Avg.113，去PeReward .330/.150/.085/.080 Avg.130；约4.6pp/2.9pp平均跌幅，RL和奖励有关联收益，但无独立PeSFT λ/投影、平滑强度/权重/聚合函数同预算因子实验。Eq4–11冻结码本图网格，Eh/Ev为横/纵相邻L2²均值，再除D；sr=1/(1+E/tau)，论文跨图mean。代码token2D默认32×32、tau3/inv，跨图默认min，可选max/median/mean；有隐藏态则改投影MSE，没有2D有效segment则退一维一阶/二阶/cos能量。主表分支/覆盖率未给，不能将这些默认全部混作同一个论文目标。固定码图E0得1是公式性质，不能确保框线/对象保真，也未证明训练实际作弊。代码默认wImg .05时wAcc .855/wFmt .095；图score失败则退.9/.1，存在隐式reward退化。format只查THOUGHT和Final Answer两子串，并不验证图或完整括号。答案匹配包含文本相似度>.77给连续分；若两文本数字列表相同则直接1，可忽略其它语义。未执行这些分支，疑点来自静态源码。

## 局限与疑问

论文正式Limitations已承认额外视觉生成推理成本、Zero抽象图削弱可解释性，不能当作者未提的空白。TV平滑不保证几何、局部身份或有用性；F9补齐拼图为新生成整图，内容真实性待检。F8轨迹文字前称0唯一邻居2，随后称0无邻边，且多节点被高亮，虽然最终No可能正确，中间状态并非可靠解释。tSNE按答对/错分群无同投影/长度/种子对照和干预，不能证明内生机制因果。附录A工具化执行形式与原生入口对应缺失。当前Inference.prepare_prompt_tokens算出image_tokens却未调用replace_image_placeholders，后续generate_once只传原input_ids、不传pixel_values，故该发布脚本图像未接入；HF卡片另有替换，不能据此说全部发布路径都忽略图片。PeSFT独立投影未见入优化器；RL端到端/Zero合成缺、reward平均与默认min/多分支不齐、yaml筛组选项关，均须澄清而非自动判论文实验错误。训练同源划分、GPTjudge复现、等预算、图像忠实性及方差未充分给；未独立复现。

## 预期优势条件

当局部定位、几何辅助线、对象标记和显式状态更新能忠实外化且生成成本可控时，功能图可能改善后继文字推理；Zero合成可降低人工轨迹成本。对书写可研究生成“当前笔画/已写状态”的视觉中介与规则执行器，但低TV会抹细笔画和交叉，须约束拓扑、笔画ID/方向/落抬笔和时间状态。静态框线或最终答案收益不能直接推出合法汉字笔顺/艺术字/素描视频生成能力。

## 可证伪实验

Q1平滑奖励是否提升有用视觉证据：同初始化/样本/更新/FLOPs做准确率reward、+TV、+语义/拓扑保真、+GT操作图四组，并扫描tau/权重、mean/min；固定图前文字随机保留/移除/换图/常量码图，测后继答案差、IoU/对象身份/连通性/细线保存、无效图与奖励分支覆盖率及按任务配对CI。如果常量图同样高奖或乱图不降答题，收缩功能性和因果解释。Q2Zero与统一范式收益来源：791例同题同预算textSFT、原生交错、确定性工具图以及无SFT RL，区分教师文本信息/模型既有能力/新图；按题ID和源图留出，补原配置完整RL/投影optimizer清单与图输入接线，再用固定judge快照、同maxTokens和按秒/FLOPs预算比较Anole/BAGEL/工具VLM。书写单独加同终图多笔顺反例、笔画拓扑及帧连续性。均为拟议实验，无训练/基准执行。

## 论文组织与Claim学习

统一任务→技能→两阶段方法→Zero→主表/消融/案例组织清楚，需在正文范式与附录renderer之间给可执行映射。按底座/样本权重报告均值，相对%和绝对pp分清；一般表混合缩放均值不能写成准确率。Zero定义为缺人工交错标注，不写无SFT/无监督。功能图应报告全量保真/错误，答对案例也核每步状态；发布默认、未发布组件与论文配置逐项对齐，既保留作者已述局限，也避免将当前代码缺陷外推历史实验。

## 实际阅读范围

本次arXivv2完整研究§1–6/附录A–F，Eq1–22、7表全部行及GPTjudge完整prompt；9实际图均看（8位图逐张，tSNE经正式p8），正式18页PDF补Limitations/Ethics及主表p7、p9、p18原页核。正式F4案例/F5tSNE与arXivF5案例/F4tSNE编号对调是版本差异，未当错误。参考文献按任务/技能/数据追引，未逐篇独立精读。固定GH/HF/数据文件清单及上述具体源码/段落核；未读5170树项全仓、权重或全部parquet，未运行学习模型、训练或独立复现。研究核心三遍和五项书面完成，未独立口试。

## 公式与代码的边界

论文Eq13的组筛选使用复合奖励标准差，因此所有答案都错的组仍可能因图像/格式分不同而被保留。Eq16在πold采样上写log(πθ/πref)，单样本可能负，未发布完整训练器前不推定实际采用哪一种KL估计。TV常量解只是数学性质，未观察到训练实际利用。

## 追引

Anole、BAGEL、Zebra-CoT、MVoT、MetaMorph、DeepEyes、MINT-CoT、VisualSketchpad、ViC-Bench、M3CoT、ArxivQA及Flow-GRPO按既有目录/主源关联，未自动标全文完成。
