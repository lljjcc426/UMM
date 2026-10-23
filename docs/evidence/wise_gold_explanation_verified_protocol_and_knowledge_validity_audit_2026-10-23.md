# WISE：金标准解释、Verified协议变化与知识标注有效性审查

第一百五十八批完成[L147](../reviews/L147.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/wise_gold_explanation_verified_protocol_and_knowledge_validity_audit_2026-10-23.json)。357目录（330论文／研究、27资源），267核心/270书面含未通过项；未确认核心63论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://proceedings.mlr.press/v306/niu26c.html)、[主源2](https://raw.githubusercontent.com/mlresearch/v306/main/assets/niu26c/niu26c.pdf)、[主源3](https://arxiv.org/html/2503.07265v4)、[主源4](https://github.com/PKU-YuanGroup/WISE/tree/09b5539d64681bf11102fc5c87e63a387beaf71d)、[主源5](https://github.com/PKU-YuanGroup/WISE/blob/09b5539d64681bf11102fc5c87e63a387beaf71d/data_verified/spatio-temporal_reasoning_verified.json)、[主源6](https://www.iana.org/time-zones)、[主源7](https://openstax.org/books/college-physics-2e/pages/13-6-humidity-evaporation-and-boiling)。

## 研究问题

静态T2I能否从未直接命名答案的知识线索推断目标实体/关系/状态，并把知识落实为可见正确内容？WISE是1000题评价基准与外部裁判协议；时空类包含单图时刻/视角知识，无连续视频、规范笔顺、动作轨迹或新生成模型训练。

## 现有不足

显式列出对象的组合prompt和全图相似度难以诊断知识检索及细粒度科学状态。作者构造隐式知识问题，再由人工解释辅助裁判；但终图失败还混合知识、推理、渲染和裁判因素，低分不能直接定位内部缺知识或深度共享架构的因果优势。

## 贡献

三域25概念子域/1000原始提示和Explanation；WiScore以一致/真实/美观三项0–2按.7/.2/.1加权再除2。20主模型及BAGEL-CoT、GPT基于Prompt+金标准Explanation的显式重写、权重/裁判/seed/分辨率/人评和新增架构分析。另独立记录官方无单独论文的维护版WISE_Verified：新提示分布、Qwen3.5-35B-A3B裁判和二值协议，不能与正式论文同名WiScore直接比数值。

## 输入、模块、输出与公式

主任务隐含线索文字→一张图；GPT4o裁判输入原Prompt+人工Explanation+图→Consistency/Realism/Aesthetic三分。重写器也获得Explanation，再将答案/状态写成显式图像指令，属于额外真值信息条件；BAGEL自身CoT是另一条件。Verified输入刷新后的Prompt→图，开放权重裁判同样看Explanation→单一0/1；可用于世界知识图像评价，不能当书写时序评价。

## 模型结构

基准无新训练骨干。专T2I包括SD/SDXL/SD3/3.5、FLUX、PixArt和Playground；统一模型覆盖视觉token AR、语言条件扩散和深融合Bagel，QwenImage等“AR+Diffusion”在本文指条件语言骨干，不代表AR生成视觉token。Legacy用openai.ChatCompletion接口GPT4o2024-05-13；Verified用vLLM OpenAI兼容接口Qwen3.5-35B-A3B，temperature0/max_tokens500/enable_thinkingFalse，三次仅解析失败重试。该维护版没有重新训练judge或生成网络的公开过程。

## 数据分布与划分

固定GH09b5539d64681bf11102fc5c87e63a387beaf71d，30成员；选择全部18个md/py/sh/json文件取回。Legacy三JSON完整程序核1000唯一ID：Culture400/Time167/Space133/Bio100/Physics100/Chem100，另三重写JSON各ID对应。Verified三JSON亦1000唯一ID：400/120/120/120/120/120，merge顺序不同但按ID全字段完全一致。两版跨全集有513个完全相同Prompt字符串，同ID同Prompt332；其余差异包含改写/换题/重编号，不能当487项独立语义换题。原始raw子类标签27种、Verified26种，正式概念分组25含更粗空间归并。原始来源教育资料/百科/题集/LLM候选后人工筛选，全部1000题未逐题事实复核；本轮全量结构审计与定向标注纠偏。未找到并使用经确认的独立HF数据集，先前推测路径401不视为资源不存在。

## 指标与评价协议

原WiScore=(.7C+.2R+.1A)/2；六类总体权重.4/.167/.133/.1/.1/.1，与原分布一致。即使C=0，R/A都2仍有.3分，不能把总分等同知识事实准确率。Verified只判知识/关系正确且视觉可用，明确不因非写实风格或普通美观程度本身拒绝，六类权重.4/.12/.12/.12/.12/.12；完整每ID单一二值时等于1000例准确比例。两版缺图/三次解析失败跳过，但计分通常要求1000ID齐；present_ids却先于有效score校验记录，覆盖还需核有效分数数。T5权重Spearman、T6跨judge、T9五生成seed、T10Krippendorffalpha均为各自有限范围。

## 对比方法

正式主表10专生成+10统一，BAGEL-CoT为同一模型额外配置，共21行。FLUXdev/schnell、PixArtAlpha、Playground2.5、SD1.5/2.1/XL0.9/3medium/3.5medium/large；BAGEL、QwenImage、UniWorldV1、MetaQueryXL、BLIP3o8B、Emu3、JanusPro7/1B、Janus1.3B、VILAU256。T11另7新架构，官方Verified另29模型并有Agent/CoT，不能混成受控架构消融。CLIPScore/VQAScore对人评是评价基线；应补知识问答→渲染分解、无答案等长重写、错答案和oracle重写、检索+程序约束、同底座同预算CoT。

## 实验条件和发布边界

正式§1–5/AppA–L全、1式11表7图，实际PDF p1/2/3/5/6/17/18/21共8页；全部主表行/附录模板及限制已读，v4定向对照。固定18源码/数据下载，完整核README、vllm_eval.py/calculate_verified.py/eval_qwen.sh、Legacy gpt_eval.py/Calculate.py，旧README读研究说明/用法1–121行及相关定位，未宣称所有旧HTML榜单逐行。Legacy judge温度0/max2000，Verified温度0/max500、不启thinking，eval_qwen96并发为部署示例；TP2/A80GB建议非正式实验硬件。生成主实验官方默认/固定seed未列全部数值；T9代表模型42–46五seed另用Gemini3.1FlashLitePreview，T6开放judge为Qwen3.5-122B-A10B，与Verified35B不同。无权重下载/API推理/独立复现。

## 主结果

正式T1：BAGEL.52/CoT.70、QwenImage.62、UniWorld/MetaQuery.55、BLIP3o.52、FLUXdev.50、JanusPro7B.35。T2GPT拿Explanation重写后FLUX.50→.73、Qwen.62→.88、JanusPro7B.35→.71，但MetaQuery物理.63→.59下降.04，不能称所有子类提高。T11 LongCatNext.57/Infinity.47/Emu3.5.57/NextFlow.62、LongCatImage.65/HunyuanImage3.0.57/DeepGen1.0.73；新AR也有强结果，跨模型不能因果证明架构。Verified榜29行另外报告QwenAgent.902/NanoPro.876/BagelCoT.628/Bagel.352；是维护版新数据新裁判成绩。

## 消融及进一步实验

T5十三模型更换权重(.7,.2,.1)→(.5,.3,.2)/(.4,.4,.2)，与原权重Spearman均.993；保留近邻交换/并列。T6QwenImage原.62/Gemini.50/Qwen122B.57，绝对分不同，Janus1.3B与Pro1B等有反序。T7原难例重写有效39.9%/仍难60.1%，物理有效14.9%；阈值.6/.7/.8分区/排名补充未提供完整操作代码和逐样本统计，分母要区分。T9 QwenImage五seed均.5029±.0046/95%CI[.4972,.5086]、FLUXschnell.3388±.0231/[.3102,.3675]，不是全模型同方差。T10人评QwenImage/UniWorld各180图，文化80/其他各20，每图5独立人，可搜索事实；C/R/A alpha=.82/.78/.67。F4六类别均分曲线未给图级相关和误差/CI，视觉接近不能充作高精度逐图可靠性。K统一512部分模型近邻SD3.5 medium/large交换.01，限该集合。

## 局限与疑问

原标注401把旧金山08点对应悉尼写为傍晚；本地zoneinfo对2025-01-15/07-15换算为次日03/01点，反例表明原解释有误，不能将全部人工Explanation视为无误。新版改成伦敦午夜对应悉尼白天，保留来源区分。蜡烛in-space需明确暴露真空/供氧；季节叶色需树种/品种和环境，避免唯一答案超出prompt。AppA把蒸发限定于沸点、将尘埃激光例放色散等有科学概念混淆，文本需核，不能照抄作理论。当前Verified QwenImage2.0列1000complete/二值单次，却总.7954且文化.8219，超出相应.001/.0025网格；缺原始score尚未解释，可能有效数/重复/聚合或表值，未断定原实验错误。有限文化/知识采样、合成/人工解释偏差、裁判共盲点、相邻分数无配对CI和生成成本不齐均限制结论。

## 预期优势条件

当知识线索有单一可见答案、Explanation事实/前提正确、裁判能识别细粒度证据且对照预算一致时，WISE比粗语义相似更能揭示特定世界知识落实失败。Verified二值可减少知识错误被画质补偿，并允许非写实画风；它也丢失部分完成程度，需单独报告。严格书写可借鉴专家规则/解释辅助裁判，但必须另加字形、笔画事件和时序执行可观测指标。

## 可证伪实验

拆文字问答正确率、显式答案给定渲染和原任务端到端三阶段，oracle/无答案等长释义/错答案/外检索同预算比较；CoT固定底座和计算额度，再对推理内容扰动。Legacy/Verified的prompt集合×judge×rubric×权重做交叉实验，各自固定版本与完整1000有效分；新题只用新图，不能按相同ID复用旧图。专家核科学/时区/文化多解，补日期/位置/压力/氧气等前提；人评按图配对而非仅6类均分、分层bootstrap并独立验证裁判错图。文字视频需新增时序真值、动作合法性和反向/置乱对照。均未执行。

## 论文组织与Claim学习

Introduction从显式对齐局限→隐含知识可见目标→benchmark，Method用来源/人工解释/25域→裁判维度/公式，实验主表→答案重写→权重/裁判/seed/人评/分辨率→失败分析，结构可借鉴。Claim应限定重写新增金标准信息、跨架构相关而非因果、权重和人评样本范围；不同协议同名分数必须写版本。Limitations已列跨域重叠/动态知识/不可用模型/静态单图，还应补标注正确性、成本和构念有效性。

## 实际阅读范围

ICML2026正式21页3689224B，Abstract/§1–5/AppA–L全部研究内容，1编号公式、Tables1–11全行、Figures1–7及图注，实际PDF p1/2/3/5/6/17/18/21。v4定向对照，固定GH30成员/18文本数据取回，五评测/计分/部署脚本全文、当前README/榜单全文及旧README所列部分；Legacy/重写/Verified/merge共10JSON完整结构静态核，未逐题事实复核。仅两日期时区计算，无模型运行/复现。

## 正式论文与无独立论文维护制品

| 条件 | 正式论文/Legacy | WISE_Verified官方维护版 |
| --- | --- | --- |
| 数据六类数 | 400/167/133/100/100/100 | 400/120/120/120/120/120 |
| 裁判 | GPT4o2024-05-13 | Qwen3.5-35B-A3B/vLLM |
| 单图分 | C/R/A三项0–2加权/2 | 语义正确且可用→1，否则0 |
| 类别总体权重 | .4/.167/.133/.1/.1/.1 | .4/.12/.12/.12/.12/.12 |
| 正式/维护主排行 | 20模型+BagelCoT配置 | 29行，含Agent/CoT |
| 解读 | 知识遵循与画质组合分 | 新规则的二值通过率 |

同名WiScore不表示两版同量尺。原C=0、R=A=2仍得.3；新二值拒绝知识不符但容许清晰的非写实风格。对素描/文字/科学插图，原“照片级真实”奖励有风格偏好，需按研究目标分别报告结构正确和画质。

固定commit含30成员，取回18文本/数据文件。两版各1000唯一ID，三Verified文件与merge按ID全字段相同，只有排序差别。跨版本513个完全相同Prompt字符串，同ID同Prompt332；不能把其余487当确定的全新语义题，改写和重编号也产生差别。原27个raw子类标签与正式25概念组在空间类粒度不同；Verified26个标签含一条Electromagnetism，均已保留计数，不自动按拼写合并造统计。它作为L147配套制品记录，不另加独立论文数。

## 主表与干预的具体证据

T1的全部21行、T2的20行七类均值及增量存于对应data JSON。BAGEL.52→自身CoT.70，显式重写BAGEL.73；QwenImage.62→重写.88；JanusPro7B.35→.71。GPT重写模板输入Prompt和金标准Explanation，目标实体、颜色/状态等答案信息被直接写入指令。因此它测已给答案条件下的渲染上界及任务难度变化，不能只归因措辞更清楚或生成模型自己学会知识。MetaQuery物理.63→.59是负项。

AppJ七新模型中NextFlow.62高于一些扩散组合，DeepGen.73为该表最高。跨模型训练语料、参数、采样预算、理解模块均不一致，排行只能说明既定系统表现。论文将QwenImage等归语言骨干条件扩散，不表示其AR生成视觉token；分类必须参照模型真实接口。

T5十三模型两组替代权重Spearman.993、T6双替代judge大体稳定，保留近邻反序，不能写排名完全相同。T9仅代表模型五seed42–46，CI例如QwenImage[.4972,.5086]、FLUXschnell[.3102,.3675]；使用Gemini3.1FlashLitePreview评分，不能移作原GPT主表的置信区间。T7难例重写有效39.9%/仍难60.1%，阈值分区与整体/难例分母需对应，未有逐样本统计脚本。

人评只涉及QwenImage/UniWorld各180图、每图5人、允许检索事实；alpha一致.82/真实.78/美观.67。F4展示六类别均值曲线，没有逐图Pearson、误差条和罕见科学错误的召回率；曲线接近不足以保证每项事实正确。K统一512验证限Qwen/FLUX/SD家族，不涵盖全部早期AR或全部预算条件。

## 标注、科学知识和覆盖的审查

旧时区样本401把旧金山08点对应悉尼写为傍晚，重写文件也继承该答案。本地Python zoneinfo：2025-01-15T08:00−08→悉尼次日03:00+11；2025-07-15T08:00−07→次日01:00+10。两个明确日期反例表明该解释有误，午夜/跨日和夏令时必须明确。Verified401更换成伦敦午夜对应悉尼白天，分别保留来源，未覆盖改写旧文来掩盖差异。[IANA时区数据库说明](https://www.iana.org/time-zones)支持按地点/日期解释规则；这里是静态换算，没有运行生成模型。

原901的太空蜡烛需明确暴露于缺氧真空还是有供氧舱；新881解释补“暴露太空/无持续火焰”，Prompt仍简略，需注意预设。原478把所有夏季枫叶严格限定绿色，品种/环境条件应补齐再作为唯一答案。AppA的蒸发描述限定于沸点，不符合蒸发可发生在沸点以下的定义，已对照[OpenStax原教材§13.6](https://openstax.org/books/college-physics-2e/pages/13-6-humidity-evaporation-and-boiling)；其激光穿尘例与色散条目也需分清散射/色散。这些是具体说明/前提问题，不能据几例估计全1000题的错误率；完整逐题事实复核尚未完成。

Verified榜单QwenImage2.0写Samples1000/Complete yes、二值单评分，但Overall=.7954、Culture=.8219。完整1000/文化400的单次0/1均值应落在.001/.0025网格，上述数值无法由这种条件产生。可能有效评分数、聚合/重复方式或表值有别，需原始JSONL。现有计分器先加入present-ID再校验score，ID完整不自动代表1000有效评分；这是代码可定位的条件，未将可能原因认定为实际实验原因。其他行及全部排行榜不因此一概否定。

新旧脚本遇缺图或三次解析失败跳过，计分器多数情况下会因缺ID拒总分；换用新旧数据/裁判须另建输出目录，不能按相同ID续跑旧结果。当前Verified温度0、max500、不启thinking，Legacy温度0/max2000；三次仅失败重试，均不作三个独立裁判或生成seed。部署96并发/TP2建议为操作配置，正式GPU/NFE/总费用仍缺。未调用API或下载权重。

## 五个问题与写作学习

1. 问题：隐含世界知识能否落实成正确可见内容？
2. 难点：语言知识、上下文推断、渲染映射和裁判误差共同影响终图分。
3. 补足：人工解释支持的知识提示和分项评分，重写用于观察给定答案后仍剩多少生成困难。
4. 优势条件：答案可见且唯一、解释正确、裁判校准及预算公平；不自动转移到文字时序或执行任务。
5. 验证：文字知识问答/显式答案渲染/端到端分解，等信息释义/错误答案/oracle和检索对照；协议四因素交叉、全部有效ID、人标逐图和专家事实核，书写另加笔画事件/时间扰动。

学习其缺口→可见任务→构造/公式→主表→分解和多种稳定性检查的逻辑。Claim必须限定给定答案重写、架构相关、人评两模型与维护版变更；Limitations写到实际科学前提/标注错误/预算和可观测性。ScImage、PhyBench、CommonsenseT2I、MMMG、WorldGenBench等相关线索先去重追引，本次引述不计独立完成。
