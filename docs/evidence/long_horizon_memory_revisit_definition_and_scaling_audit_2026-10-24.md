# 长程交错生成：回访间隔定义、记忆策略与效率证据

第一百六十七批完成[L156](../reviews/L156.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/long_horizon_memory_revisit_definition_and_scaling_audit_2026-10-24.json)。357目录（330论文／研究、27资源），273核心/278书面含未通过项；未确认核心57论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2610.17080)、[主源2](https://arxiv.org/html/2610.17080v1)、[主源3](https://arxiv.org/pdf/2610.17080v1)、[主源4](https://arxiv.org/html/2610.17080v1/horizon_scaling.svg)。

## 研究问题

怎样让原生图文交错模型在多次场景切换后恢复历史实例细节，同时控制稠密视觉历史成本并减轻自生成误差累积？

## 现有不足

完整VAE历史不断增长并混入无关/错误视觉状态，固定近期窗口又会丢失旧场景；teacher-forcing的干净GT历史与推理的自生成历史分布不同。需分别处理长期身份、场景检索和暴露偏移，不能仅扩大上下文。

## 贡献

持久视觉anchor、预测sceneID后检索同场景早期/近期稠密状态，以及离线self-rollout历史适配；完整语义历史继续可见。提出LongMIG100故事和Long+Ext38×24图压力测试。没有给骨干独立名称/可唯一对应总参数，不将其写作已公开Hunyuan型号；交错图像是故事/过程状态图片，无连续笔画视频输出。

## 输入、模块、输出与公式

输入故事指令或用户照片；原生先输出<think>文字规划+自生成anchor，再在<answer>交错输出规划文字和故事图（Eq1–4）。每张历史图有语义h_sem及生成m两种表示。sceneID由理解路径产生并被控制器解析，用来设置当前生成对历史视觉key的可见性；没有外部GT scene给推理。输出可含辅助图，最终故事评价排除辅助图但成本需计入。

## 模型结构

大规模MoT，理解/生成分支稀疏专家，256K多模态context；层数、总/激活参数、完整初始化未披露。Eq6 M_k=A∪R_k∪F_k∪L_k：所有持久anchor+全局最近Kr+同scene最早N和最近M；Eq7只筛生成侧历史，语义图文全留。固定anchor数/窗口下稠密历史槽数至多|A|+Kr+N+M（本仓库集合上界，不是总context常数）。Eq8–11将部分历史clean条件换为模型图，当前FM/noised target仍GT；离线生成写回，不在优化步内采样、不用自身错误作监督目标，亦非RL。

## 数据分布与划分

候选约1e8，PT约1e6/SFT约1e5为量级；专用长程21162故事/197653图=53499anchor+144154panel，每故事2–24panel/1–10anchor、anchor众数2，平均panel约6.81（本仓库算术）。T3来源占比storyboard45.3%、有/无参考绘本18.5/7.9%、社媒漫画14.5%、长漫画9.1%、品牌设计4.7%，未给源ID/许可及训练测试去重清单。rollout两阶段5721/7522合13243轨迹计次，不能当已核独立unique；anchor及最初两张非reference故事图不替换。LongMIG T2MI/I2MI各50故事、462/460shots，均9.2，各50style、七aspect、双语，回访均6.16/6.04。Long+Ext38故事、每个24固定slots/2角色/3场景。独立全数据下载未得。

## 指标与评价协议

六项GPT6整轨迹1–5分：Identity/Scene/VisualFidelity/VisualMemory/Aesthetic/TextRendering；SceneGap=同场景平均相似−跨场景平均相似，用SigLIP2/DINOv3（Eq15），不是逐对象或时序正确率。D.2三套完整prompt：主judge识别回访并解释，全部同背景Scene≤2；visual-memory复制同图记1、用户参考身份本身不算memory。文字judge无合格文字帧时设rendering=match=0；有文字时rendering只评字形，text_match另评文字内容，主表未细化二字段合成/0的汇总。关键Eq14 LR用k−首次场景位置e_s≥8，不保证距最近同场景位置≥8；应另报last_seen间隔才能检验近期窗口之外回忆。

## 对比方法

T1共13行：六agent-planned StoryDiffusion/QwenImage/UniSpace/HiDream/Lance3B/Showo2与native BAGEL/SenseNovaU1.5/ILLUMEX/Emu3.5/SEEDStory/UniLongGen*及Ours。agent共用GPT6分解后独立生成，I2MI按支持能力给参考；native按自身接口共享轨迹，跨协议不构成等信息/预算架构因果对照。AppE.4明确UniLongGen*保留本文模型权重，仅替换training-free上下文选择，因此是同权重策略对照，修正原笔记仅称同主干的含糊表述；不再把未知改训差异当成已证混杂。

## 实验条件和发布边界

完整HTML及AppA–G均核完。未披露可复现optimizer/lr/steps/batch/GPU训练h、Kr/N/M具体值、完整scene解析/回退、CFG/分辨率/seed/采样重试或judge精确快照和人评相关。Table5八故事扩32图，同权重/decoding/hardware两节点AR TP8+图生成TP8，每图30去噪；未给GPU型号，不用秒数外推单卡。F11另为固定长轨迹trace，和八故事均值分开。去reference消融重建同故事、删除所有anchor调用，panel顺序保留，但训练tokens/预算不相等是否补齐未知；GTFT/selfrollout同追加数据是原文声明，未给步数预算。原文完整HTML/11图已取得，PDF两次下载均截断，未据此宣称完整PDF；本批未获可核官方模型/代码/数据，不执行模型。

## 主结果

T1同权重UniLongGen*→Ours：Identity3.46→3.62、Scene2.61→3.35、GapS−.0081→.0930、GapD−.0135→.2499、Fidelity3.05→3.75、VisualMemory2.60→3.77、Aesthetic2.97→3.75、Text2.28→3.50；Ours六/八列最高，Identity低于SenseNova3.72、Fidelity低于Qwen3.83。Table5 32图前缀平均102.9→54.9s/图，最后图ARprefill69→19.4s，分别约1.87×/3.56×，后者不能当端到端倍数。Fig11每图context边际5028→1546tokens，32图164.6K→71.9K；51图full-history满256K是线性外推，50+图仅选例，不是50+图平均成功率。原表所有行与五张表已结构化，图例做定性核查，无模型重算。

## 消融及进一步实验

T2为分阶段10行/三组，非全组合factorial。predicted/GTscene：Scene3.26/3.32，LRScene3.10/3.15；30%错scene降2.81/2.76，Recent4为2.85/2.79，Recent2为2.58/2.47。去anchor：Identity3.36→3.18、LRScene3.10→2.03、LRGapD.119→.005，Fidelity3.15→3.13。GTFT→rollout：Identity3.23→3.59、Scene2.71→3.25、LRScene2.52→3.12，Fidelity3.35→3.38；Base→GTFT Fidelity2.57→3.35，须单列额外训练本身收益。各组基线值不同，不把三组差相加或声称完整交互因果已识别。数据/步骤/重复次数缺口保留。

## 局限与疑问

问题1：LR定义从首次出现算，包含近期又出现的场景；本仓库ABC循环第10步距首次A9、距最近A3，满足Eq14而Recent4仍看得到，不能只凭该分层确认超窗口记忆。完整场景表未公开核，真实受影响比例未知。问题2：文字0分/无文字覆盖和glyph-only rendering/text_match聚合未细化；整轨迹judge自动对齐、不给帧数奖惩，仍需独立剧情覆盖/遗漏评价。API快照/校准/原始judge理由缺，SceneGap可受主体/风格相似混入。问题3：语义history仍线性长，anchor多实体时也增长；scene文本格式无效或错分影响检索；作者AppG承认小物件、多人、文字与早错累积，没解决逐实例状态绑定。无rollout标注/权重，无法检验clean-anchor是否过强。

## 预期优势条件

当少数稳定身份和反复场景需长期复用、且语义scene预测可靠时，anchor+相关图路由可能以较低稠密注意力成本保留视觉决策。若物体持续改变、位置相同但状态不同，粗scene检索可能重引过时状态；笔顺应保存最新有序前缀/对象级状态并检验下一笔，不能套用固定身份anchor当完整过程记忆。

## 可证伪实验

按首次距离和最近距离双轴重算LR，对last_seen>Kr的独立子集给逐故事配对CI；固定24slots/角色与场景，构造ABC短循环及真正长空窗，对比RecentK/semantic检索/sceneoracle与相同容量路由。对anchors×rollout做同权重策略及等数据更新预算2×2，给错anchor/错scene/无scene格式干预并报target命中、对象状态、覆盖与恢复率。公布三judge原始JSON/API版本，文字分开报requested/present/matched覆盖、rendering与match/严格CER；无文字按是否要求文字定义NA或失败并给分母。效率同时报全部anchor/规划/参考/控制器成本、GPU型/显存/方差，区分均值、prefill与trace外推。笔顺固定终态反事实换序，用真实生成前缀测试状态保持与下一笔执行。

## 论文组织与Claim学习

可借鉴三种失效→三组件→分阶段消融与独立效率表的对应。定义LR必须明确first_seen与last_seen；指标名称的适用范围需由公式检验。把语义/稠密context、原生交错/单图planner协议、平均时延/末图prefill、实测/外推分别披露；同权重对照已存在就准确承认。完整评审prompt有价值，仍需说明输出字段与分母如何变成表中数字、并公开原始制品。

## 实际阅读范围

arXiv2610.17080v1完整HTML：§1–5、AppA.1–3/B.1–5/C.1–5/D.1–2全部三judgeprompt/E.1–4/F.1–2/G.1–3；Eq1–15、T1–5每行和F1–11所有实际原图/图注已核。F4标1–52/1–48的稀疏选帧、F6/7完整作者展示烹饪序列、F9规划/生成轨迹、F10规格、F11SVG实线/虚线分别看；不声称独立逐帧人标/OCR、重构所有曲线点或生成复现。PDF下载截断，完整阅读依据HTML与11个独立作者图资产；参考文献追引相关条目，未逐篇精读全部参考。三遍定位/方法全图表/书面批判，无独立口试或模型执行。

## LR的可识别性反例

以24步ABC循环为假设序列，第10步是A；首次A在第1步，最近A在第7步。Eq14条件10−1≥8为真，但Recent4可读第7步（10−7=3）。该纯标签反例说明“距首次≥8”不能保证旧场景落在近期窗口之外；未执行模型，亦未估算真实Long+Ext中这类回访比例。建议同时报告first_seen/last_seen间隔和last_seen>Kr子集。

## 需要修正的历史笔记

原笔记把LRgap≥8笼统称为远程间隔，现按Eq14明确其参照为首次场景。AppE.4明确UniLongGen*保留本文底座权重，主表比较可按同权重记忆策略解释；训练预算混杂应放在分阶段重训消融和跨家族比较的相应位置。

## 长度与效率证据分层

主基准100故事平均9.2shots；24图Long+Ext用于消融；八故事32图用于前缀平均效率；F11为单轨迹trace；50+仅稀疏选帧；51图满窗为线性外推。32图平均速度约1.87倍，末图prefill约3.56倍，不能互换。语义历史仍增长，图像侧context路由后边际1546tokens/image，未降至常量。

## 文字指标字段

无合格文字时prompt令text_rendering/text_match均0；有文字时两字段分别测字形与内容，正文笼统的1–5和语义忠实描述不足还原表中聚合。需发布原始JSON及0/NA规则，避免把不需文字和漏掉指定文字混为同类。

