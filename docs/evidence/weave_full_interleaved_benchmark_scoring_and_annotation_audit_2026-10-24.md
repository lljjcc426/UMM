# WEAVE：完整交错基准、评分口径与测试标注审查

第一百七十八批完成[U12](../reviews/U12.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/weave_full_interleaved_benchmark_scoring_and_annotation_audit_2026-10-24.json)。358目录（331论文／研究、27资源），283核心/288书面含未通过项；待完成核心深审48篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2511.11434v1)、[主源2](https://arxiv.org/html/2511.11434v1)、[主源3](https://arxiv.org/pdf/2511.11434v1)、[主源4](https://openaccess.thecvf.com/content/CVPR2026/papers/Chow_WEAVE_Unleashing_and_Benchmarking_the_In-context_Interleaved_Comprehension_and_Generation_CVPR_2026_paper.pdf)、[主源5](https://github.com/weichow23/weave/tree/dfc17dd997f754f4860e195a412d414d074eb9ae)、[主源6](https://huggingface.co/WeiChow/Bagel-weave/tree/54dad66a381dc5a3d9b79ef907a087c7e7a2d4f5)、[主源7](https://huggingface.co/datasets/WeiChow/WEAVE/tree/b7d16e77dd2520920e9e2a9ef29cda192a2e2202)、[主源8](https://huggingface.co/datasets/WeiChow/WEAVE/blob/b7d16e77dd2520920e9e2a9ef29cda192a2e2202/test/test.json)。

## 研究问题

多轮图文任务是否能同时检验世界知识、视觉元素回溯、多图融合、编辑和跨模态生成？单轮问答/画图分数不足以刻画任务序列的依赖与状态保持。WEAVEBench关注交错理解生成的上下文任务，WEAVE100k用合成多图编辑数据后训练BAGEL；没有在线笔迹、笔画顺序或视频连续时间目标。

## 现有不足

现有数据常只支持单轮/单图/单类生成，多轮视觉记忆与理解生成协作覆盖不足；复杂顺序生成昂贵且成功率低。作者通过四条合成路线、人工测试集和细粒度VLM评分拓展任务，并检验单轮多参考图训练是否迁移到通用理解/生成；需要将外部检索历史图、模型内部持久状态与长程因果推理分别验证。

## 贡献

WEAVE100k共100750对话/505186图，四路线multiimagefusion、remove-and-back、derivedimagination-and-comparison、sequentialprocedure；WEAVEBench人工100例/16细任务/四域；KP/VC/IQ/文本ACC混合评测及BAGEL后训练。贡献为数据构造、基准协议和应用验证，BAGEL的MoT、AR文本与连续图像flow骨干均继承。完整主表和附录揭示分数目标随文本ACC是否存在而变，需谨慎解释统一能力增益。

## 输入、模块、输出与公式

输入多轮文字、原始/此前生成图及Image#引用→按partial仅取当前显式图号，full取历史图/文字（不同模型能力不同）→原生多图序列或横向带编号拼图→文本答案/当前编辑图→保存并供后轮检索。VLM full支持图文历史，多数生成模型仅图；yes-first与yes-front是图在对话中的布局。BAGEL公开入口每轮独立inferencer调用，输入选定多图+[instruction]，未保留跨轮KVcache；外部图片回取不能直接当作已学持久隐状态。GT历史oracle与实际生成历史分开。

## 模型结构

四条数据路线细读：Echo4o多图融合用GPTImage原始结果/Seedream重生，GPT4.1指令经QwenImage/Seedreamfallback、Step1X1.2编辑失败由Nano修，再逆指令拼接；removeback由GPT4.1筛至约25%指令再生成/逆恢复；Zebra棋/拼图改显式操作以比较；12类顺序procedure含story，复杂story需人监督，筛好story进test而train保留多轮edit。CLIP高相似触发重编辑、Qwen3VL4B过滤未改图，未给全部阈值与逐阶段保留数；CLIP变化不保证语义正确。理解题每对话最多随机一轮GPT4.1补caption/count/relation等。训练受上下文约束随机抽单轮并重编号Image#，每轮可多图；未将完整多轮对话持续端到端训练。HF llm_config为Qwen2 h3584/28层/28Q4KV/FF18944/vocab152064/maxpos32768；ViT27层h1152/16heads/patch14/image980；均配置静态核，不声称权重验证。

## 数据分布与划分

训练总100750；fusion75996（72348 GPTImage+3648Seedream，占75.43%）、Edit19903占19.75%、Recall1369占1.36%、Jigsaw1286占1.28%、Chess2196占2.18%，大类明显不均衡，不沿用relativelybalanced描述。均3.79轮/5.01图，至多8图，≥4图100584、≥5图60361、≥6图31571；平均questionlength195.49单位未给。测试原文100例/480图/16任务由STEM研究生设计；固定发布test.json实际100例、479个唯一图路径、325图响应+42文响应，文本元数据全计数但未下载imgs.zip核全部像素。四域Science含六细类、Creation四/Logic二/Game四；来源web、Zebra棋拼图、PhysBench光学物理及Seedream4/Nano/SeedEdit3等教师；源图/同题训练测试去重没有独立验证。

## 指标与评价协议

Eq1生成分=.5KP+.2VC+.3IQ；Eq2统一分=.4KP+.1VC+.2IQ+.3ACC；文字仅ACC。公开summarize依是否实际有accuracy键动态换公式，缺主指标还退现存数值均值；先对有效turn分别micro平均/10并round3，再加权，整体不是四域宏均值，也非等对话权。KP prompt本身70%满足任务+30%视觉质量，与IQ重叠；VC虽称pixel-level实际VLM主观打分；IQ将collage/grid一律封顶4，可能影响合法拼图/比较结果；ACC只0/5/10，经归一不等严格正确率。正文§4.4称GPT4.1，AppB1称GPT4o，公开config模型占位、示例gpt4o2024-08-06，缺实际主评快照/温度/重复评估；不能确定最终judge。

## 对比方法

4 VLM/7编辑/11统一家族，主T2含25行（Seedream/Nano分别partial/full及BAGEL三个checkpoint）。保留模态/历史/拼图与序列图标，不能因HTML纯文字漏图标而把三类Avg当同目标。BAGEL base/Zebra有ACC而WEAVE行四域ACC全部“-”，尽管模态仍标图文；主表.446→.640混用不同公式，不能直接视为相同统一任务得分提高。相同生成三指标公式可作分域近似重算，整体缺有效turn计数不能由四均值重建。官方异构参数/外部系统多次重试/遗漏有影响，无等时延FLOPs和统一历史覆盖基线。

## 实验条件和发布边界

8H100/每GPUb1/30Kstep约60h，LR2e-5、EMA.9999、maxlatent64、batchtoken11520/sample10240、ViTdrop0。BAGEL例50step、textCFG4/imgCFG2、shift3、seed42、文字greedy/max1000；HF generation_config却do_sampleTrue/T.7/topP.8/topK20，应分别记录配置与示例。Step1X例28step/CFG4/seed42且thinking/reflectionFalse。横拼参考图会改变单图分辨率，code长边上限8192；不能当与多图seq完全等条件。固定GHdfc17dd997f754f4860e195a412d414d074eb9ae的README、eval全六py与infer四py全文核（含loader），vis.ipynb未全文；HF 54dad66a381dc5a3d9b79ef907a087c7e7a2d4f5模型15文件清单/卡和四config、dataset b7d16e77dd2520920e9e2a9ef29cda192a2e2202的795文件清单/卡及完整test.json核；未下载权重/trainparquet/imageszip。公开无完整训练脚本/环境锁与全部baseline调用recipe。

## 主结果

T2 25行/T3 13模型行/T4完整模型和子指标、T5–10附录全行存审计JSON。T2 BAGEL base .446、Zebra .449、WEAVE .640；.640/.446−1约43.50%，但作者42.5%对应.640/.449−1约42.54%，Science34.6%也对应Zebra .399→.537，故修正旧笔记为比较分母不清，不能仅判算术错误；更关键是ACC缺失换公式。相同生成公式从展示三位值重算Science .4882→.5375，Creation .6783→.7061，Logic .5819→.5670（约−2.56%），Game .5093→.5313。只是显示聚合值复算，未复评逐题原始预测。Nano partial/full .764/.767，Seedream .765/.746，更多历史不保证更好。T3 GEdit总体6.52→6.83约+4.75%，11类8升3降（Motion5.09→4.97/Add7.94→7.88/Text7.16→7.06）。T4 MMB85→85.2/MMMU55.3→60.7为5.4pp或9.77%相对/MMVet67.2→67.4；GenEval.82→.84；RISE2.4/5.6/14/1.2→4.7/6.7/21/2.4，四项均值5.8→8.7为50%，spatial仅50%而logical100%，正文两者均100%不符表。

## 消融及进一步实验

F6a布局中QwenVL yesfirst优于无历史，正文约163%源于低基数；GPT4o同有布局依赖。F6bGT历史好于生成历史体现误差积累，不能据此分离推理/图质量；F6cBAGELseq好于cat，作者10.3%相对但图未给全精确原分，未从像素量精确反推。F6d三专家对Nano/QwenEdit/Seedream各100图、与GPT4o/Claude比较Pearson，KP柱略低.8，与正文所有维度持续>.8描述不齐；无raw/CI，相关高不能证明所有子域排名无偏。缺四数据路线同预算/样本量消融、单轮多图与全对话/持久缓存对照、换图/遮图干预和correctedlabel复评；因此长程内部视觉记忆及理解生成协同因果未确立。

## 局限与疑问

本次确认有实际测试标注问题。test idx67与F32：原图BC=3、A37°/B68°，AC=b应3sin68/sin37≈4.62194，标答1.541且写.6018/.9272≈1.541（实为.64905）；要求过A垂直BC，GT图画过C垂直AB，keyGT2却重复过A指令。随后文本含“C在AB上”与图点位冲突，不能给一致几何解释。idx68末问比较角大小，标答复制37degrees不回答；idx35 A→C的KP写B→C；idx3用户问White最佳，答案分析Black queen c7；idx90输出Image4但GTkey3配左半月描述，参考图索引与输出不齐。这些在公开JSON中可见，不限于排版；错误率/模型排名影响尚须全量人工复标和重评。F23重复四次OptionA仅论文展示，F39与公开jigsaw idx4–8已区分各选项，未将其误报现行数据同错。当前loader full分支range(max(img_idxs)+1)再取imgs[img_idx-1]，从0开始把imgs[-1]末图纳入，构成未来GT图输入；缺生成历史又自动fallback源GT而未显式oracle标记。casebagel默认partial，不能据此判所有主表用了fullbug。评测图读取失败打印后continue仍可判分，summary只汇总存在样本；论文已说明Seedream多次尝试仍有部分图省略，覆盖率需单列。config未定义main导入的DATASET_PATH、case_gpt的yes-first行缺冒号，当前示例需修正接线；这些为当前发布源码审查，无学习模型运行，也不能外推历史实验一定如此。

## 预期优势条件

多参考图显式编号、恢复被删元素及多轮编辑链，有望提高对象属性保持与回溯组合，扩展通用知识依赖编辑。书写方向可借鉴“取回原始构件/恢复局部笔画/跨轮保持风格”的任务构造，但需要真实笔画ID、时间方向、落抬笔、交叉拓扑及同终图多笔顺反例。自然图多轮编辑增益不直接推出汉字合法笔顺或素描过程视频；评价需把视觉美观、科学/几何可执行性、文字回答能力分别报告。

## 可证伪实验

Q1同一目标和标注下是否仍有协同收益：先按idx复标数学/迷宫/棋/月相等并冻结版本，对base/Zebra/WEAVE均执行同325图与42文turn、固定缺失罚分和覆盖率，统一生成三指标、文字ACC以及共同四项指标分别报告；固定judge快照、同参考输入，补按对话配对bootstrap/人类与规则judge。若同生成公式或correctedlabels不增，收缩统一能力结论。Q2历史检索与训练来源：修full索引并将生成/GT历史显式隔离，用同token/FLOPs/时间预算做单轮多图、完整多轮、持久缓存三组；四数据路线同样本量消融，移除/换序/打乱/替换被引用图，插入不相关历史，测回溯准确率/身份保持/真实逻辑规则及误差随轮数曲线。若换掉历史图不影响输出或未来GT去除后收益消失，应否定视觉记忆归因。上述是拟议实验，未运行模型/未重建排行榜。

## 论文组织与Claim学习

方法/数据/基准/迁移/案例链条清楚，跨系统表需写清比较目标、能力范围、输入历史和有效样本数。图文ACC缺失不能静默切评分公式后与base混报提升；百分比标明base或Zebra及相对/pp。科学逻辑基准先用可执行规则复核GT，VLM高人评相关不能补救错误答案。论文图示错误与发布JSON差异分别留证，公开例程索引/占位需说明，当前代码缺陷与历史实验结论之间保持证据边界。

## 实际阅读范围

本次arXivv1 51页研究§1–5及附录A–E全部研究正文/末级小节，Eq1/2，编号T1–10全部行（HTML另含F4统计表和prompt表），F1–39全部实际图/统计图与四完整SVGjudgeprompt（上下段补看）；F13–23训练案例/F24–39各测试细域均核。当前正式PDF访问403或截断，只沿用2026-10-20已核正式元数据/主表，不称完整正式版重核。固定GH所述10py+README、HF模型卡配置/数据卡清单、test.json全量结构计数及指定错标样本核；未看全部训练parquet/测试像素、未读完整notebook、未执行学习模型/独立复现。核心三遍与五项书面完成，未独立口试。

## 分数解释修正

此前以.446作为分母判正文42.5%算错不够充分：.449的Zebra基线与42.5%及Science34.6%都吻合。本次保留原始表值并改为比较对象不清。无论分母用哪个checkpoint，base/Zebra有ACC而WEAVE缺ACC造成换公式，仍阻止直接统一能力增幅解释。

## 标注与发布边界

具体样本编号沿用发布idx。数学长度按F32原图BC3与37/68度使用正弦定理核算，未运行神经模型；.6018/.9272也单独核为.64905。Maze路径长度等其余视觉疑点未追加未经规则确认的数值结论。F23重复A与F39/发布JSON已经分开的选项不混淆。公开test.json路径总479不是实际像素审查，未推定缺哪张图。正式PDF访问失败不改写此前已核的正式出版信息。

## 追引

BAGEL、Zebra-CoT、CoMM、Echo4o、RISE、KRIS、PhysBench、AnyEdit、UltraEdit、Step1X、OmniGen系列和Seedream按已有目录/主源关联；缺项后续按独立主源纳入，未自动标全文完成。
