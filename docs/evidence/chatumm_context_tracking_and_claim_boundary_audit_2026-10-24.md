# ChatUMM：多轮上下文机制、完整补充与长程结论边界

第一百六十六批完成[L154](../reviews/L154.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/chatumm_context_tracking_and_claim_boundary_audit_2026-10-24.json)。357目录（330论文／研究、27资源），272核心/277书面含未通过项；未确认核心58论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://openaccess.thecvf.com/content/CVPR2026W/GRAIL-V/html/Dai_ChatUMM_Robust_Context_Tracking_for_Conversational_Interleaved_Generation_CVPRW_2026_paper.html)、[主源2](https://openaccess.thecvf.com/content/CVPR2026W/GRAIL-V/papers/Dai_ChatUMM_Robust_Context_Tracking_for_Conversational_Interleaved_Generation_CVPRW_2026_paper.pdf)、[主源3](https://openaccess.thecvf.com/content/CVPR2026W/GRAIL-V/supplemental/Dai_ChatUMM_Robust_Context_CVPRW_2026_supplemental.pdf)、[主源4](https://arxiv.org/html/2602.06442v2)、[主源5](https://dai-wenxun.github.io/ChatUMM-page/)。

## 研究问题

怎样使理解/生成统一模型在连续图文对话中回指早先的文字或图片，在插入无关任务后继续编辑指定主体，并自主切换图像与文本输出？

## 现有不足

单轮理解和生成分数不测跨轮目标选择，前一图也未必是当前编辑目标；仅串接单轮模型或扩大上下文长度，均不能直接保证历史回指和输出模态正确。必须分开验证指代解析、视觉保真、编辑执行和长期错误累积。

## 贡献

基于BAGEL的交错多轮训练和对话数据合成；提出输入/输出/历史依赖模态/依赖深度四轴分类与十种LLM原子操作，将单轮图像任务转成基本对话、插入干扰轮、加入图后问答三阶段数据。主要贡献是训练/数据配方，未提出新的通用视频骨干或笔画轨迹生成器。

## 输入、模块、输出与公式

输入序列化历史图文和当前请求；共享上下文中的文本token、ViT语义token、VAE细节latent供下一段预测。输出图像、文字或图后文字；预测|v_s|触发图像，预测|im_s|触发文本，|end|结束一轮。对话轮间编辑输出为静态图片，不能直接视为连续视频帧、笔画顺序或物理执行动作。

## 模型结构

BAGEL 7B MoT继承共享self-attention及分开的理解/生成FFN；文本/ViT走理解路由，VAE走生成路由。文本用|im_s|/|im_e|，视觉用|v_s|/|v_e|封装。当前图的加噪latent以flow-matching/MSE预测noise→data速度；文本和模态特殊token用CE。训练允许读取历史文字、clean VAE和ViT，屏蔽历史加噪VAE；当前生成块内部图像token双向交互并受历史因果条件。clean仅指无扩散噪声，不保证历史语义正确。正式图2已核，未获源码独立重建attention mask；无正式编号公式，不虚构Eq号。

## 数据分布与划分

四轴<input>_<output>_<dependency>_<depth>：input t/ti，output i/ti，历史0/t1/tn/i1/in，深度0/1/n；n>1代表隔轮，不是已披露固定轮数或样本量。stage(a)六类：t_i_0_0、t_i_t1_1、ti_i_0_0、t_i_i1_1、t_i_in_1、ti_i_i1_1；stage(b)在历史间插入T2I、理解或文本干扰并显式改写目标；stage(c)从末图caption派生Q/A形成query+Q→image+A。补充F1 caption2query要求EN/ZH各短中长共6种，query2dep_q要求EN/ZH各3个短请求，两语言独立。十操作及完整两prompt已读；Gemini辅助合成，v2明确Gemini2.5Pro。未披露完整源数据清单、unique样本数、各依赖深度/干扰数量分布、人工验收及主体隔离划分；6种改写不是总数据量。

## 指标与评价协议

单轮理解七指标MME-P/MME-S（P+C）、MMBench/MMMU/MMVet/MathVista/MMVP；T2I用GenEval六子维与overall；GEdit-Bench EN/CN full set的G_SC/G_PQ/G_O均↑，由GPT4.1评审。它们分别测单轮理解、组合图文对齐和编辑质量。正式全文/补充未提供跨轮目标选择准确率、按历史距离成功率、长对话生存曲线、图后文字与实际生成图一致率、bootstrap或重复seed方差。选例不提供这些总体指标。

## 对比方法

主文T1七配置，补充T2扩29配置；T2六配置，补充T3扩21配置；T3五配置，补充T4扩9配置。包括BAGEL7B MoT、Janus/JanusPro、MetaQuery、Showo、TokenFlow、Chameleon、LlamaFusion/MetaMorph及专用Qwen/InternVL/Kimi；生成含FLUX1dev、SD3/XL、DALL-E2/3等，编辑含Step1X/IP2P/MagicBrush/AnyEdit/OmniGen和闭源Gemini2/GPT4o。主表/补充逐行核，缺失值保持null，参数规模与预训练预算不同；无同预算多轮外部检索基线。

## 实验条件和发布边界

从预训练BAGEL继续训15K步约30B tokens，除冻结VAE外训练参数，任务均匀；AdamW β1=.9/β2=.95/eps1e-15、wd0、clip1、lr2e-5，warmup200后恒定，CE:MSE1:1，不用EMA。FSDP HYBRID_SHARD、FlexAttention，每rank packing约61–64K tokens；v2补num_shard32、t_shift1.0。第二阶段再5K步约10B，维持优化设置，理解/文本/T2I/编辑相对采样率.25/.15/.5/1，多轮每类.1；缺各类数，不自行归一。共20K/约40B新增tokens，不能以额外训练后成绩单独归因多轮机制。“annealing”名称不证明lr衰减。GenEval †BAGEL/ChatUMM/FLUX/MetaQuery用了LLM重写；MMMU *无CoT。未给全硬件/总GPUh/推理步CFG/seed和错误重试预算，61–64K packing不等于经64K能力测评。核过当前项目页及官方附录，未见源码、权重、数据下载入口，无法代码或rollout独立复核；未执行模型。

## 主结果

主表BAGEL→ChatUMM：理解七项1687/2388/85.0/53.7/67.2/73.1/69.3→1685/2382/84.6/53.8/66.4/74.7/68.7，2升5降；MathVista+1.6、MMVet−.8，无方差不能判显著。GenEval .88→.85，single/two +.01/+ .01，counting−.05、color−.03、position−.09、colorattr不变；不能据优于Janus/MetaQuery就称优于原BAGEL。GEdit EN6.52→6.95（+.43）、CN6.50→6.73（+.23）；Chat EN超过Step1X6.70，但CN低于Step1X6.86；GPT4o EN7.53/CN7.30更高。主文18行与补充59行全数值保存JSON。F7和补充F2/F3可见跨干扰回指首图、双主体组合和图后问答，属于作者选例，未独立估计成功率。

## 消融及进一步实验

完整正式主文§1–5与补充§1–2无组件消融表；补充扩展单轮基线、十操作和两模板、两页多轮选例，并未新增历史距离量化。缺interleaved-only/无distractor/无rewrite/无问答/无clean-history等同预算对照，也无真实生成历史对比teacher-forcing。目前可支持额外训练后静态编辑指标提高，并展示多轮能力的存在案例；无法识别提升源自40B增训、编辑加权、模态边界还是依赖合成。

## 局限与疑问

问题1：主张robust long-range但只展示选例，未报告目标图识别、干扰强度、历史相似度和长度下的失败率；rewrite向当前请求补入目标外观，可能用caption/局部描述捷径，未证明依赖实际视觉历史。问题2：Q/A来自目标caption，文字回答可正确但图中未实现；训练clean历史与真实rollout语义错误需分离，本文未测错误传播。问题3：对照前后有约40B额外tokens和采样配方变化，缺等预算消融；理解5/7下降、T2I overall下降及CN编辑低于Step1X，摘要SOTA表述应受指标/语言/模型集合限制。项目页未给可核制品，数据污染/划分与实现仍未知。

## 预期优势条件

当用户需跨无关轮次准确定位先前静态图，四轴数据和显式模态边界可能增强回指编辑与图文交替；优势取决于目标识别线索、历史压缩、干扰相似度及错误历史覆盖。对笔顺课题可借鉴前缀/状态依赖的数据构造，但需额外的有序笔画事件和逐步过程评价，对话图像序列本身不提供规范笔顺证据。

## 可证伪实验

固定BAGEL骨干、额外tokens/编辑比例及推理预算，比较完整配方、去干扰、去目标改写、去问答、去交错与相同预算单轮；加外部检索+BAGEL、最后一图、caption-only和oracle目标基线。对相同query交换早图、删历史、插相似主体且只改一处细节，统计target-ID、局部编辑成功与主体一致，按depth/图数/相似度分层；避免文字已给答案使视觉回指不可识别。真实rollout与干净/人为错误历史分别测多轮生存/错误恢复、图后回答是否符合实际图、token/时延/显存。在笔顺迁移中固定终态，测换序/反向/跨字干扰及prefix-conditional执行。上述为待实验设计，本批无模型运行。

## 论文组织与Claim学习

可学习任务分类→原子操作→三阶段数据→训练及单轮主表→多轮选例的组织；应将数据阶段与两阶段训练分开。对共享self-attention/分FFN、噪声clean/语义正确、训练token长度/测试依赖距离、选例/总体成功率逐项精确定义；每项SOTA需指明基线集合、语言和指标。新增token训练预算及LLM重写资源应与机制claim绑定披露，不能让静态单轮表替代长程核心主张的实验。

## 实际阅读范围

正式主文10页§1–5全部研究正文，T1–3每行，F1–7实际图像/图注及架构/数据图已核；独立补充9页§1.1–1.5与§2完整研究文字、T1十操作及T2–4所有行、F1两完整prompt和F2/F3全部选例/图注已读，参考文献追引相关条目。arXiv2602.06442v2指定方法/数据/训练/结果与正式版对照，表号分版。核项目页当前资源入口，未获公开可核代码/数据/权重。三遍为定位/方法和全部表图/批判书面，不等于口试、独立生成或rollout复现；选例未逐像素做身份/OCR标注。

## 全表与证据对应

正式主文T1/T2/T3分别7/6/5行，补充T2/T3/T4分别29/21/9行，已按各自表号存JSON，避免把扩展基线误当新增长程实验。补充T1含10个操作，F1给两完整模板。主文F7与补充F3的目标回指可见，但选例没有随机抽样分母。

| BAGEL→ChatUMM | 前值 | 后值 | 差值 |
| --- | ---: | ---: | ---: |
| GenEval overall | .88 | .85 | −.03 |
| GenEval position | .78 | .69 | −.09 |
| GEdit EN overall | 6.52 | 6.95 | +.43 |
| GEdit CN overall | 6.50 | 6.73 | +.23 |
| MathVista | 73.1 | 74.7 | +1.6 |
| MMVet | 67.2 | 66.4 | −.8 |

表值是作者报告，差值是本仓库算术核对，无生成模型执行；无误差条，不据此判断显著性。CN编辑Step1X6.86高于ChatUMM6.73。

## 过程迁移边界

历史图即便编码为clean latent，也可能含错误对象、笔画或状态；clean只区分扩散噪声。对书写任务需以实际历史前缀做干预，控制终态但交换顺序，并验证下一步动作与状态。将对话静态编辑图连起来无法替代有标注的书写视频评价。

