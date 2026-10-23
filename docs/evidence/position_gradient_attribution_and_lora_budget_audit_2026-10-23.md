# PAM：位置梯度归因、生成目标与LoRA预算审查

第一百五十三批完成[L140](../reviews/L140.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/position_gradient_attribution_and_lora_budget_audit_2026-10-23.json)。357目录（330论文／研究、27资源），262核心/265书面含未通过项；未确认核心68论文／研究+27资源。资源另按制品审查。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2609.38485)、[主源2](https://arxiv.org/pdf/2609.38485v1)、[主源3](https://arxiv.org/html/2609.38485v1)、[主源4](https://arxiv.org/src/2609.38485v1)、[主源5](https://arxiv.org/abs/2408.12528)、[主源6](https://github.com/showlab/Show-o/blob/45a5a2de01d1ebd10cd5864d29310a76476cdf23/models/modeling_showo.py)。

## 研究问题

理解与静态图像生成在共享骨干上的梯度冲突是否除层深外还有视觉token调用位置这一轴，能否只调高冲突位置改善两任务折中？这是一阶归因/LoRA后训研究，无笔画事件或书写视频生成。

## 现有不足

层级平均可遮盖同层各token调用的贡献差异，参数分离也未使用这一轴。但必须先厘清位置是空间raster索引、模块调用位置还是loss项位置；这些均不自动等于语义粒度或实际生成时间。

## 贡献

Eq1–3用线性模块activation和输出梯度的rank-one积按16桶累计，建立layer×bucket冲突图；再按独立诊断选择6桶，以PAM仅移去对缓存理解梯度反向的生成分量。另做norm归一、DINO语义探针、随机桶与层级LoRA对照及频段FID代价。有效性和实现仍受下列设定/归因/预算问题限制。

## 输入、模块、输出与公式

固定理解/生成batch→共享模块输入ht与反向δt→gb=sum(t in Bb)δt ht^T；与理解模块梯度算cos，产生L×16图。用浅/深层平均−cos排序，m6/τ.13。训练中gb′=gb−min(0,<gb,û>)û，û为每2K步刷新的理解梯度EMA单位向量；未选桶和理解梯度保持，最终仍原模型静态图/答案。Eq2恒等式准确分解模块调用位置贡献；跨位置attention后，gb通常不等只保留桶内loss再反传。Eq3不同形状模块写sum_m再vec，需实际拼接/逐模块聚合规则。

## 模型结构

Show-o1.3B列L24/d2048/T256（16×16），JanusPro7B列L30/d4096/T576（24×24）；Show-o理解共享VQ流，Janus理解SigLIP/生成VQ分开，共享attention参数。tokenizer固定。重要：本文把两模型均按图像raster AR/Lg next-token描述，原Show-o主源与固定官方源码实际是文字NTP+图像masked-token离散扩散/并行重遮罩；未说明AR转换和mask/采样协议，不能把本文设定直接视为原Show-o实际行为。原Show-o仅针对forward/t2i_generate做定向核查，不重计U06完成。

## 数据分布与划分

诊断8×(64理解+64生成)=1024样本，3dropoutseed=24batch-seed重复；额外4batch只选桶/阈值。语义探针10K held-out图，桶embedding预测DINOv2全局向量R²；关联跨2模型×3层段×16桶=96cell。训练20K×batch128、1:1任务比，但全文/附录未给训练语料名称、规模、采样/去重/划分和probe训练集，不能用MME/POPE/GenEval/MJHQ评价数据替代训练数据。

## 指标与评价协议

MME perception、POPE F1、GenEval、MJHQ FID30K；三层Laplacian分LF/MF/HF单独算FID，频段FID不相加成overall。冲突cos、norm下降、两因素ANOVA partial eta²；DINO可解码性及HF残差Spearman。1万次按prompt/item配对percentile bootstrap，另报3seed SD；item CI不自动覆盖训练随机性。CI跨0只表示差异未确证，不能称statistical parity/等效。

## 对比方法

joint+norm、layer-wise LoRA separation、PAM、same-count随机桶、layerwise+PAM、单任务理解/生成参照。Layerwise浅深每任务rank8、中层共享rank16，其他单套rank16/qkvo/alllayers；m2/4/6/8/12、K8/16/32、downweight w.25。未报告同预算原PCGrad/CAGrad或语义/空间匹配选桶；两个异构checkpoint的差别无法单独归因token共享。

## 实验条件和发布边界

全臂LoRA r16/α32/drop.05/qkvo，20K步batch128/lr1e−4 AdamW/warm500/cosine，1:1、3seed但ID未列；betas/wd/精度/分辨率、生成CFG/NFE/mask、训练语料等未齐。论文称12.6M/31.5M可训参数，按4个d×d投影单套LoRA应8Ldr=6,291,456/15,728,640，约一半；若双套/额外模块须源码说明，不能自行补。probe backward开销1.21×/1.17×、PAM训练+.3%为不同口径；图前置map每模型28H200h、全文总200h。AppE分12环境+28map+8norm+10semantic+78训练+30跨架构+34评价，78仅称four-arm而表有5主臂/单任务/消融，逐run分配未齐。v1源码包160910bytes/22成员全列，无.py/experiments或canonical数据；Repro称supplementary有position_probe.py，abs称acceptance后公开，有限title+GitHub/HF未核官方发布。未运行。

## 主结果

T1 Show-o eta_layer/pos/int=.353/.312/.085，F1040.1/1389.9/9.8；Janus .299/.150/.068、F808.5/678.8/9。按AppC dferr45696/57120与eta=Fdf/(Fdf+dferr)计算，Show-o layer .343621/int .068892，未等于表.353/.085，超打印舍入；需原始ANOVA重核。T3按MME/POPE/GenEval/FID：joint1339/84.9/.550/6.84；layer1397/86.4/.603/6.05；PAM1418/86.6/.627/5.97；random1364/85.3/.574/6.50；组合1424/86.7/.632/5.94；单U1431/87.6，单G.641/5.79。PAM−layer +21 CI[9,34]、+.2[−.4,.8]、+2.4pp[1.1,3.7]、−.08[−.19,.04]；只前两主能力指标中MME/GenEval增益明确，POPE/FID未确证差。关闭剩余单任务差约62%/63%，不称理论上界。T5 Janus joint1372/87.9/.662/5.63，layer1379/88.1/.670/5.48，PAM1387/88.3/.681/5.44，random1381/88.2/.674/5.57，组合1390/88.3/.684/5.42。PAM−layer MME+8[2,14]、POPE+.2[−.3,.7]、GenEval+1.1pp[.3,1.9]、FID−.04[−.12,.04]。

## 消融及进一步实验

F1 Show-o quartercos−.18/−.09/−.05/−.02，Janus−.11/−.05/−.03/−.01；最强−.42(layer19,b3)/−.37(layer25,b1)，深浅更强，中层较弱，F7分层段显示相同趋势。T2 norm下降2.63×/1.92×，归一后eta_pos .312→.249/.150→.114，保留79.7%/75.8%；这是归一稳健性，两个partial eta比值不等正交可加的“80%因果来自方向”。F3 conflict对DINO R² rho.64，对HF残差−.58，96cell有模型/层/桶依赖。F6 m2/4/6/8/12相对joint GenEval+4.6/+6.8/+7.7/+7.2/+6.1pp，K8/16/32为+6.9/+7.7/+7.5；downweight+6.2(.612)低于投影.627。random回收Show-o MME31.6%/GenEval31.2%，Janus60%/63.2%。T4 LF/MF/HF/overall：joint2.41/3.11/2.87/6.84，layer2.02/2.76/2.66/6.05，PAM2.00/2.75/2.77/5.97，random2.23/2.94/2.83/6.50；HF+4.14%/LF−.99%。组合优于单方法，但按Show-o四臂均值MME交互1424−1397−1418+1339=−52、GenEval−.048，不能将“combine additively”解释成增益简单相加或机制独立。F10a按现有图例将两模型eta柱对调（Show-o蓝对应Janus表值），以T1主表和正文为准并保留图示冲突。

## 局限与疑问

作者列一阶小probe、分辨率/tokenizer依赖、28H200h重测、无人类纹理评价、未全参微调。独立核查：(1) Show-o AR假设与官方masked生成不符，需模型变体和mask设置；raster早晚更不等全局/纹理或笔画时间。(2) Eq2为调用归因，跨位置loss梯度另有非零项，“bruteforce self-test”若只遮activation可成立但不能证明loss归因，未取得脚本。(3) Eq3不同shape拼接、LoRA A/B空间与冻结W空间投影如何对应均未交代；训练参数约2倍歧义。(4) 正文zero-index S={1,2,3,4,6,7}，AppB却同数字one-index；F4c实际高分0–3/5/6支持后者，不能当同一索引集合。(5) ANOVA将同batch/seed/module相关cell当平衡残差，F与eta/自由度还有数值不对应；需混合效应/聚类重测。(6) 缓存EMA正交保证只对选桶与旧方向，未保证全部生成梯度、当前理解梯度或AdamW实际更新无冲突。(7) DINO相关与两异构架构对比未隔离语义/位置/数据/体量；预声明和“released”均按作者声明，未核事前注册/补充制品。

## 预期优势条件

当真实模型的模块调用位置确有稳定任务冲突、位置指标与目标功能错误跨集对应、投影空间和参数预算一致时，局部调节可能保留更多有益生成更新，优于全层分离。本文有有限Show-o/Janus主表增益及随机对照提示；归因术语、Show-o目标和源码缺口未解决前，不据其直接推出空间/语义/时间的普遍规律。书写可用真实事件而非raster索引建立位置轴。

## 可证伪实验

公开准确checkpoint、训练/诊断数据、mask/解码、LoRA参数清单和投影代码；区分模块调用归因、loss项归因及LoRA参数梯度，用两位置混合解析例核语义并对照原自测。原Show-o masked目标与明确AR改造分组，固定空间内容的逆序/随机排列、next-scale和语义匹配桶分离索引/空间/语义。按run和item分层bootstrap或混合效应ANOVA，核F/eta表一致；给POPE/FID预定等效界。全预算含诊断成本、随机桶重抽和独立选桶、多seed及原PCGrad/CAGrad；比较缓存/当前u、实际AdamW参数步与理解loss。对书写用严格事件/细笔OCR/顺序/执行约束，同时测高频损失，未执行。

## 论文组织与Claim学习

问题定义从层到位置的测量单位转换，Introduction→图→归一控制→语义探针→干预→随机对照→预声明代价的结构清楚。应学习报告收益及HF代价；Claim需明确测量单位和真实目标，归一稳健性不写作因果比例，CI跨0不称等效，组合改善不称数值可加。Method要把训练数据、投影空间、参数数与源码接口写全，Limitations应包含这些复现缺口。

## 实际阅读范围

v1完整20页512334bytes，Abstract/§1–9全部研究正文、p11 AIUse/Repro/Ethics、AppA–F全部研究内容，Eq1–4/T1–6/F1–10全部图注；实际看p3/4/5/6/7/8/9/18/19/20共10页，覆盖全部图和表。参考目录定位未逐篇读；源码tar22成员目录已查无.py/experiments/canonical数据。原Show-o abs和固定官方modeling_showo.py forward/t2i_generate定向主源核查，不计新独立精读。有限title+GitHub/HF检索，无PAM官方实现/训练数据/权重取得，无运行或独立复现。

## 调用归因与损失归因的解析区别

以下为仓库解析例，未运行模型：两个位置共享标量W，y1=W a、y2=W b，后续跨位置混合产生唯一损失L2=(y1+y2)^2/2。按模块调用位置，第二位置贡献为(y1+y2)b；只保留第二位置损失再反传，梯度为(y1+y2)(a+b)。第一位置虽无局部loss，仍经跨位置依赖收到梯度。因此PAM Eq2对调用分解的精确性不能自动赋予loss-token归因语义。

## 配置与统计核算

- 单套4个d×d投影的LoRA参数为8Ldr，所列两配置得到6,291,456/15,728,640；论文报12.6M/31.5M。需要双套/额外模块说明，不能替作者补设定。
- 按AppC dferr=L×16×5×24−L×16，分别45,696/57,120。partial eta²=F df_effect/(F df_effect+dferr)。Show-o表F给layer .343621、position .313302、interaction .068892，原报.353/.312/.085；Janus为.291020/.151288/.064144，原报.299/.150/.068。F保留一位的舍入不足解释主要差异，需原始ANOVA输出。
- 正文zero-index桶集和附录one-index相同数字有实质一桶偏移；F4c高分0–3/5/6对应附录1–4/6/7。未替论文选定实际训练掩码。
- F10a按图例将两模型eta值反向对应，与T1不一致，保留主表及矛盾位置。

## 五个关键问题

1. 层均值是否掩盖共享模块在各调用位置的梯度差别？
2. 既有层级优化没有这一轴，但需先验证位置所指对象和真实生成目标。
3. 本文新在hook分桶图及独立选桶PAM组合，不提供新tokenizer或视频模型。
4. 若调用归因稳定且与真实功能错误相关、参数和预算匹配，局部调节可能保留更多非冲突更新；当前主表仅支持有限底座上的联合增益。
5. 原始实现和数据、AR/masked分组、排列/空间/语义控制、run聚类和实际优化步验证，是核机制必要条件。

## 追引与范围

原Show-o/Janus已在目录，当前仅定向交叉核。待去重扩查masked generation、raster/随机排列、next-scale和spectral bias、LoRA forgetting、token-level imbalance及run/item混合效应。已读参考清单不计逐篇完成。
