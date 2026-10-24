# UMM共同空间：完整跨分支干预与架构归因审查

第一百九十八批完成[L031](../reviews/L031.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/one_space_full_directional_steering_and_architecture_claim_audit_2026-10-25.json)。358目录（331论文／研究、27资源），303核心/308书面含未通过项；待完成核心深审28篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2607.26411v1)、[主源2](https://arxiv.org/html/2607.26411v1)、[主源3](https://arxiv.org/pdf/2607.26411v1)、[主源4](https://rain305f.github.io/)。

## 研究问题

冻结UMM从理解文本QA或生成VAE hidden提取已知概念差向量，注入另一分支能否控制颜色/数量/关系/文字等；是否存在方向性可迁移表示。目标是诊断已有概念的线性干预兼容性，不直接检验新概念学习或真实理解能力增益。

## 现有不足

共享backbone不保证不同token/任务目标的表示可直接交换；任务分数和纯相似度难观察跨分支可用性。将同一目标向量施加另一分支可验证特定干预的效果，但成功不证明全局只有一个语义空间，失败也未排除非线性/位置特异/重参数化后的共享结构。

## 贡献

UMMSteer七语义族、51名义二元概念对；CAA/RepE/ITI三个提取器，双向steering、同分支对照及PSP层级投影；多架构、norm-matched随机/无关方向、object/attention pooling、逆向token位置、强度和层消融；双阶段VQA judge与350图人工一致性；关系生成纠错和ConceptMix模板外测试。

## 输入、模块、输出与公式

Definition1对比上下文/答案只变目标属性。U输入纯文本场景QA+答案，在答案token取h+/h−，并非从图像感知任务直接提取；G对比生成prompt，在各层VAE token全局均值。Eq4 pooled h=mean_t∈Tvae h_t，未完整说明跨denoise timestep采集/平均方式及同noise配对实现。Eq6 CAA=mean(h+−h−)；Eq7 RepE=差向量首PC，方向符号定向/是否中心化细节不全；Eq8 ITI线性分类超平面法向并按该轴std归一，classifier正则/求解器未细化。U→G缓存文本prefixKV后，在默认全部层/去噪过程中把αv(l)加到所有VAE token（Eq1）；G→U加所有text hidden（Eq5），另测concept-input与answer-prediction位。Eq2–3 mLD=logitpositive−logitnegative，Δ为steered−base；多subword答案聚合规则未给。Eq9/10 SSR/GenScore皆对象存在AND属性成立，区别在target由干预向量还是原prompt给定。Eq11–13对比差做PCA取k20、U正交基，PSP=||Uᵀs||²/||s||²∈[0,1]为能量比例。

## 模型结构

主BAGEL共享MoT文本/理解与生成expert、AR文本+连续VAE rectified-flow；跨架构Show-o2 hybrid、Janus-Pro和UniPic-1纯AR。本文不训练backbone，学习的是统计差向量/PC/线性分类方向。具体checkpoint大小/revision、AR生成token干预细节及每模型等效α/幅度校准未全给；不能把所有模型当相同continuous-VAE接口。PSP是选定对比数据/20维的线性子空间诊断，未给PCA heldout和k敏感性及投影替换后的因果救援对照，不足推成可迁移必要充分条件。

## 数据分布与划分

UMMSteer名义51对：color8/text8/count10/position7/appearance8/style8/persona2；每二元对每分支50训练pairs、每个概念50held例，B.2按两个方向SSR平均，未给完全公开样本/去重/分词/各阶段确切总计。主控模板隔离属性，未覆盖任意自然语言或真实视频。F11–13称完整逐概念图，实际标签color8/text8/count8/position6/appearance8/style7/persona2共47，count未画1↔5和2↔5、position未画above↔under、style未画happy↔unhappy；缺原始结果不能核它们是否计入T1平均。ConceptMix仅color/count k2/3/4、每格样本数未报。人工7类各50图=350。

## 指标与评价协议

SSR=生成图可见目标对象/证据且目标属性成立，不是严格实例identity保持或只改局部属性；uncertain不计yes。Qwen3-VL-30B judge（正文多处写Qwen-VL-3 30B）两阶段同图问题，T3 overall原始一致率95.4%、κ.894；不是判断准确率95.4%，未给多人工一致性/混淆矩阵/人评CI。颜色κ.540、text.658表明分族强弱不同，不能只引overall。T1±为概念对间std，非seedCI/显著性。逆向SSR衡量把有明确原属性的QA答案推向相反目标，0%是该干预未改变回答，不能读成模型原始理解准确率0或生成学不到知识。GenScore关系prompt忠实度用同judge，非标准GenEval scorer。

## 对比方法

CAA均值差、RepE首PC、ITI分类方向；norm-matched random和无关persona方向；U→U与G→G同分支；G全局pool/object GroundingDINO bbox/attention-weighted；逆向全部text/concept-input/answer-prediction；无干预GenScore baseline、多α、单层。四模型比较同时改变骨干/codec/训练/接口，对架构因果归因不充分。

## 实验条件和发布边界

多用2×A10080GB；官方预训练checkpoint无重训练；BAGEL 1024分辨率、50generation/50diffusion timesteps按原文、text/image CFG各1、interval[.4,1]、renormmin0、shift3、seed42。默认所有层，单层F16另设；默认CAAα.1，RepE/ITIα.2。α扫.1/.15/.2/.25/.3/.35/.4，逆向声称dense/broad scan但具体网格及每配置原始N未全列。无统一成本或seed稳健统计；公开论文及作者主页本项只有Paper链接，未定位可下载UMMSteer/本文执行代码，不能把“will be released/使用开源实现”当已公开该数据与完整配置。未运行模型或judge。

## 主结果

T1依color/text/count/position/style/appearance/persona SSR%：CAA96.20±1.46/43.46±28.79/68.75±23.96/78.60±16.57/82.71±24.57/79.88±21.06/24.37±31.25；RepE52.95±40.63/21.13±22.50/6.87±7.79/59.83±21.74/29.29±26.61/44.25±23.95/34.00±33.94；ITI96.48±1.66/43.09±29.06/34.90±28.35/78.96±17.32/80.75±21.70/78.86±21.80/29.38±30.58。T3text98/κ.658、position98/.790、style100/1、persona90/.800、appearance90/.786、count98/.929、color94/.540、overall95.4/.894。T4 color/count/position/style：BAGEL96.20/68.75/78.60/82.71，Show-o2 87.13/43.07/32.20/64.20，Janus48.75/20.57/8.67/47.80，UniPic2.30/13.07/13.40/37.80；AR结果较低但并非各项全0。T7 ConceptMix k2/3/4 color46.25/21.43/20.45、count42.22/33.33/17.28，复杂组合明显下降。F6关系GenScore% inside/outside28→92、left/right45→78、above/below55→67、behind/front80→95，图无CI不擅称统计显著。全部8表单元另存结构化专题。

## 消融及进一步实验

T5 random与unrelated四族全0，目标CAA对应96.20/68.75/78.60/82.71，说明当前任务下不由幅度或任意语义向量解释。T6 G→U三种pool在color/count/style/appearance均0；C.7三token位置×三pool同为0并声称幅度scan仍0，尚缺独立已验证G语义向量阳性对照。F5 G→G主要改变背景/全局色而对象仍红，说明当前提取器未稳定给出可操控对象颜色的向量，不能反推整个G表示不含对象语义。F16 black→red单层2–5有效，深层衰减；不能以此替默认全层结果。T8α从.1到.4：CAA100/96.25/91.25/81.25/48.75/23.75/10；RepE1.25/16.25/20/12.5/7.5/3.75/1.25；ITI7.5/96.5/97.5/97.5/97.5/96.25/93.75，因此原文“各法随α一致下降”不成立，全段明显非单调。F11–13短text/计数/抽象persona差异大；F18误目标、全局过度应用、拼写错和text/visual混淆；图注重复写保持identity与失败内容不一致，以实际图/正文为准。

## 局限与疑问

§6/F5较强架构解释被AppB.4主动收窄：连续VAE干预更兼容当前protocol，不证明hybrid天然更统一；报告时采用此限制。生成与理解提取的载体不对称（答案词含直接词汇监督vs图像token pool），G→G阳性都未稳定成功，G→U null不能单独识别为语义空间不可共享。纯文本QA逆向目标故意冲突已描述事实，测的是可控偏置而非真实视觉理解/新知识迁移。PSP高低为相关诊断，未进行匹配PCA数据/维度/重参数化和投影救援，不能推出只要/只有落共享空间即可迁移。T1统计与47图标签/51名义对覆盖边界、生成时间采集、分词打分、跨模型接口、样本原始清单和配置未全开放；单seed/模板数据限制泛化。SSR对象存在gate不能保证原实例/布局保持，部分展示背景/对象也改变；不据静态文字改色扩展到规范笔顺。

## 预期优势条件

对于BAGEL/Show-o2已有且可视觉验证的单属性，纯文本QA差向量在连续图像hidden中可能以较少参数提供属性控制和关系纠错；理论优势来自可访问干预接口与基础模型能力，不保证复杂组合、抽象persona/长拼写或跨所有架构。

## 可证伪实验

Q1逆向失败来自提取/接口还是语义不可用：冻结同骨干，匹配层/模长/denoise时刻，先证明G向量能完成同分支对象级阳性控制，再比全局/局部/时间条件/非线性映射及注入name/answer/VAE位；heldout PCA、k扫描、随机子空间及投影后行为救援分开报告。Q2对笔顺是否有用：在相同字最终轮廓下设合法/非法顺序对、只变指定事件，匹配静态识别与自由解释、动作序列/视频事件执行、实例/布局保持；比较U已知语义steering与L030新伪词地址patch，控制单层/全层、全VAE/name位置与强度，跨seed和OOD长度字体。先公开51对清单与缺失4对原始结果，盲多人审并报逐类CI和总成本。均为建议，未执行模型。

## 论文组织与Claim学习

先写可证伪的操作性问题“当前向量/位置/任务能否交换”，再讨论表示机制；图像对象存在与实例保持、主动违反原prompt与纠正prompt忠实度分别命名。默认全层和单层消融清楚区分，表内非单调趋势不能统一说随强度下降。主文架构必然性须与AppB.4兼容，保留弱结果/失败图及51概念覆盖疑点。与L030 Janus窗口差异首先按对比已有词vs新概念、allVAE全层vs名字单层、反事实SSRvs实例检索的协议解释，不宣称相互证伪。

## 实际阅读范围

v1全部31页§1–7、AppA–F及参考清单、Definition1、Eq1–13、T1–8全部单元、F1–18原PDF页实际视觉，含F11–13全部标签与失败图；作者官方主页本项Paper入口核查，无可定位本文代码/数据下载链接。未运行预训练模型/生成/QA/judge，未独立复现。核心三遍及五项书面检查完成，原文/资源未充分披露项仍保留。

## 与新概念入口研究的关系

[L030](../reviews/L030.md)以新实体伪词绑定、单层name token地址patch和24way实例检索测试；本篇以已有颜色/关系QA差向量、默认全层所有VAE token干预及反事实SSR测试。Janus在两篇结果不同，尚无同checkpoint/接口/数据/预算对齐实验，不能据此断言互相证伪。

§6较强的hybrid架构解释与AppB.4的限制应并列；最终结论采用“当前连续VAE干预协议更兼容”这一可由实验支持的范围。

完整8表原单元、51名义概念分类及4个未出现在逐项图的概念对保留在结构化证据中。
