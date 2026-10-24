# UEval：完整评分分母、标准效度与发布协议审查

第一百八十七批完成[U22](../reviews/U22.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/ueval_full_rubric_aggregation_and_release_protocol_audit_2026-10-25.json)。358目录（331论文／研究、27资源），292核心/297书面含未通过项；待完成核心深审39篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2601.22155v1)、[主源2](https://arxiv.org/pdf/2601.22155v1)、[主源3](https://zlab-princeton.github.io/UEval/)、[主源4](https://github.com/zlab-princeton/UEval/tree/3a5b5ea2c4d2d149c41b3f06645f2fd272aca88e)、[主源5](https://huggingface.co/datasets/zlab-princeton/UEval/tree/fdeac6654b113d20e7e89d496167a4a5bb55bc66)、[主源6](https://datasets-server.huggingface.co/rows?dataset=zlab-princeton%2FUEval&config=default&split=test&offset=0&length=100)。

## 研究问题

统一模型能否对真实问题同时生成正确的文字和图像，尤其是知识插图与多步骤视觉教程？提出逐题rubric评估基准，并检查图文能力差异及裁判可靠性；本身不训练新模型，也不提供笔轨迹或连续视频真值。

## 现有不足

仅用VQA和T2I独立分数难以覆盖图文联合回答、跨步骤内容保留和说明一致性。通用整体打分或成对胜率依赖对比模型集合，作者转用基于每题参考图文生成并人工核定的细分标准；其有效性仍依赖标准是否只约束题意必要内容、裁判的错误和汇总分母。

## 贡献

1000题、八任务、10417条rubric的图文生成benchmark；四closed知识任务space/textbook/diagram/paper，四open教程art/life/tech/exercise。Gemini2.5Pro草拟标准后两轮人工审查，逐条booleanjudge；比较九统一模型、两文本模型、六裁判与单被评模型人评，并展示给其他模型添加推理文字的定性例。贡献是数据与评估协议，无新tokenizer、扩散loss或训练架构。

## 输入、模块、输出与公式

构建：问题q与人工收集参考图文→Gemini2.5Pro草拟两侧标准→primaryannotator核问题/参考/标准→coauthors独立二轮，保一致项并去重、补OCR条款。评估：q→待测模型图文输出→每条rubric调用裁判→criteria_met true/false/not sure→每模态met/条数；代码not sure计false且保留分母。评估阶段代码不传参考图文，知识要求已嵌在rubric。无编号公式/算法。F10给单条联合图文prompt，公开实现实际区分textonly、closedimageonly与openimage+text三种上下文。

## 模型结构

九被评模型各沿用原架构，UEval无共享参数新骨干。JanusPro/Showo2/MMaDA/BAGEL同一q分别独立调用图生成和文字生成再配对；Emu3.5/Gemini/GPT原生联合输出。因图文相互条件、调用数、最大图数和预算不等，排名同时受生成协议影响，无法仅由该表因果归于原生交错架构。GPT5两模式通过官方chat界面获取，无法以公开APIcheckpoint和统一tokenbudget精确重建。

## 数据分布与划分

完整公开test1000条元数据核出唯一ID1000，image5573/text4844，总10417，与F1八任务条数一致；756题两侧rubric数不同。任务题数space100、textbook180、其余各120；原始task另有2条exercise_skill_generation（ID282/286）应映射exercise，原始值9种不等论文9任务。参考图共4605张：closed520题各1，open480题多图至22；本轮只取metadata与URL指针，未下载1000题原图。Space20seedQuora扩为100经人工核参考，textbookTQA；diagram近年会议原图/全文，paper经典论文和D2L/Medium/CS231n；教程WikiHow/YouTube/EasyDrawing/ArtForKidsHub等。GPT5生成部分知识题/reftext，标准由Gemini草拟，存在source/modelstyle关联；无独立训练污染审查。

## 指标与评价协议

标准满足率，需分清criterionwithinmodality、questionmacro、taskmacro和modalitymean。§2.2只写满足标准/总标准；T1每任务分与T4图/文等权均值吻合到舍入，最终Avg八任务macro；T2caption也写八任务均值而正文称所有题。公开compute_summary仅平均各题text_rate/image_rate，没有overall_avg_rate、没有按task分组，尽管README例子列overall。10417条全局micro、1000题macro和八任务macro、图文两侧等权不能互换；无逐题评分日志无法确认历史表精确实现。F7criterionagreement约90%、F8questionPearson.88均仅GPTThinking每task10%共100题；T3六裁判也只评GPTThinking一组输出，不是跨被评模型排名相关。

## 对比方法

T1九模型与参考回答；T2另Qwen3-32B/Gemma3-27B文本only，缺同骨干同预算联合/分离调用及固定图数对照。T3裁判Gemini2.5Pro/GPT5Thinking/Seed1.6Vision/Qwen3VL235BThinking与Instruct/GLM4.1VThinking；人评只选GPTThinking，未覆盖低分模型/OCR错/多图数量等分层。F9加GPTThinking推理文字到GPTInstant/Gemini2.5Flash/BAGEL，只展示一题，未给facts-only、等长caption、错误trace或额外planner计算预算对照。

## 实验条件和发布边界

官方repo固定3a5b5ea2c4d2d149c41b3f06645f2fd272aca88e，tree110项/80blob无truncated；重点审README/ueval_eval.py、Gemini生成器、Emu3.5的vLLM入口/visual_guidance配置/proto转换，未审全部vendor。HF数据tree记录fdeac6654b113d20e7e89d496167a4a5bb55bc66，rows服务取当前10页1000元数据，不宣称已由pinrevisionparquet解码。Gemini生成器默认旧primerL/UEval-all、modelgemini2.5flashimage，至多100attempt且同时有文字和图才保留，属jointsuccess条件采样，非按judge分选bestof100；需报告尝试数/失败。其domains过滤task_type，现数据字段task，按art等过滤会为0；生成字段gemini_text_ans/gemini_image_ans与eval默认text_answer/image_answer不同，需显式参数。Emu入口也默认旧dataset，split是HFsplit而现只有test；配置seed6666、4路TP、max32768token，textT.7/topP.8/topK200，图T1/topP1/topK10240、imagearea518400及outerCFG3。所有九模型的实际revision/采样/服务日期/预算不齐。judge默认gemini2.5pro、无固定snapshot/temp/seed，cache与directcontext路径应锁定。代码MIT，不等所有参考图片许可；HFcard无显式license字段、仅7feature无逐题sourceURL字段。未运行生成器/judge或重现分数。

## 主结果

T1按space/textbook/diagram/paper/art/life/tech/exercise，Reference96.2/94.4/93.1/96.2/90.6/87.7/90.6/89.2，Avg92.2；Janus21/31/37.4/15.2/26.4/23/17.6/11.5，22.9；Showo25.4/33.1/33.2/17.4/25.6/15.6/17.4/13.1，22.6；MMaDA10.8/20/14.2/13.3/15.7/15.8/12.4/12.6，14.4；BAGEL29.8/42.5/37.2/20/39/33.6/24.8/21.4，31；Emu59.1/57.4/41.1/31.6/59.3/62/37/45.4，49.1。Gemini2.065.2/55.2/47.6/45.8/70.4/58/50.2/48，55.1；Gemini2.578/74/66.4/71.6/66.6/63/58.2/50，66；Instant77.3/77.9/62.3/55.1/71.2/69.7/50.7/57.6，65.2；Thinking84/78/67.8/51.9/67.8/63.8/57/61.4，66.4。Thinking领先Emu17.3pp，但比Instant仅+1.2pp且paper/art/life下降；Gemini2.5paper与tech、Gemini2.0art、Instantlife各有更高值。参考92.2说明gold/标准/judge未完全自洽，不作为理论上界。

## 消融及进一步实验

T2图/文Reference87.8/96.8，Janus6.5/39.3、Showo8.3/36.9、MMaDA15.9/12.8、BAGEL13.6/48.5、Emu33.6/64.6，Gem2.036.9/73.2、Gem2.556.4/75.5、Instant52.8/77.7、Thinking49.1/83.8；Qwen3text81.2/Gemma83.1。Thinking文字比Instant+6.1pp，图像−3.7pp；MMaDA总体图高于文，T4EmuSpace64.6>53.6、Gem2.5Space82.6>73.5，故textconsistentlyhigher不能逐项成立。T4四openimageThinking37.5<Instant52，文85.5>72.6。T3六裁判完整八列已记录结构化数据；Gemini vsGPT对art67.8vs56.4、life63.8vs50.1、tech57vs45.4、exercise61.4vs51.7，所谓consistent不能解释为分值互换。F9自由女神像单例加入含crown/window/stair等事实的trace，Instant/Gemini改善、BAGEL失败，无全基准迁移量化。F11–14更多模型例暴露乱码、图序重复/跳步、纯文字替代动作；仍为作者选例。

## 局限与疑问

标准内容效度需单审：真实ID601图像标准要求外部face+crown可见并含窗后人，正确内部视角也可能因裁切条件失分；ID701题只问笔记本连WiFi，图像标准却要求modem/router硬件与admin设置，文字标准又要求聚焦笔记本并避免过多从头设router，存在过具体/跨侧不一致风险。不能从两个例推估全体缺陷率，需盲审。裁判同源于rubricdrafter，100题单模型agreement/Pearson不能证跨模型公平或criterion错误率低，缺混淆矩阵/κ/CI。微/宏分母与README/实现差别、原始task别名、旧field/domain和生成器成功条件影响可复现入口；并不据当前代码追认历史表有同样问题。图文双调用无共享上下文自然易失配，模型架构/知识/图数/预算混杂。referenceopenimage82对closed93.5不单独识别judge偏差或任务难度。无连续运动/轨迹、细笔保留、物理执行、复杂artiststyle与中文字符集覆盖；多步教程分数不等真实笔顺正确。

## 预期优势条件

逐题标准可定位知识细节、OCR和图文步骤错位，适合作为UMM静态教程/示意图层的补充诊断。迁移到书写/艺术字需另加字符合法性、部件拓扑/小笔画、prefix一致性、笔序/轨迹可执行性，并将可接受多解与必须条件分离。可借鉴模型草拟+专家核定标准的流程，但不直接把Gemini单一分数用于RLreward；要先验证judge盲点与优化投机。

## 可证伪实验

Q1rubric分数能否反映真实图文正确性：冻结数据/标准/裁判snapshot与promptpath，对八任务、模型家族、图数、OCR和低分样本分层盲评，专家独立核每条的必要性/多解容忍/参考依赖，报告criterion混淆矩阵、κ、CI和跨模型排名。对ID601内外合法视角与ID701仅客户端流程、图文置换/乱序/重复、正确字错图及文字满分图空白做预注册成对干预；分开标准错误与judge错误，同时报micro、questionmacro、taskmacro、两模态等权，若排名随口径显著变则收缩稳定性主张。Q2reasoningtrace是否超出事实提示：在独立题集预先生成planner文字，分别加原trace、等长事实列表/图片caption、无关或错误trace，固定下游模型/图数/总token与调用预算、多seed，报全基准与细笔/跨步指标及planner成本；匹配jointsuccess并计全部失败。另同骨干同预算nativejoint与双调用/有文字条件出图对照，避免把prompt条件差当架构因果。均建议，未调用模型。

## 论文组织与Claim学习

问题和八域例图直观，F4将标准构建与打分分开，主表后给模态拆分、人评和裁判敏感性，易追溯。需把得分汇总公式/权重、生成失败与采样次数写清；consistent/textalwayshigher/reasoningmuchbetter等概括应逐表检查例外。单例trace补事实不能承担机制和总体增益主张，人评单输出源不能支持所有模型可靠性；数据card旧paper链接和代码旧字段说明需要与版本对齐。

## 实际阅读范围

完整v1PDF22页正文§1–6、AppA–D；T1–5全部行（T4a/b图文八任务），F1–14全视觉含F10完整judgeprompt，无编号公式/算法。重点固定repo评估器/两生成入口/Emu配置与proto转换；110tree/80blob仅范围审查，未全读vendor。完整1000条metadata统计10417条rubric与4605参考图指针，八域代表prompt/rubric/reftext阅读，未语义逐条人工核10417项、未下载1000题原图。核心三遍/五项书面完成；无模型/judgeAPI执行或独立复现。

## 发布范围和统计边界

本批审查固定代码的实际行为，未修第三方仓库、未使用APIkey或运行裁判。当前生成入口的旧字段不能据此证明论文历史实验受同一缺陷影响；需要作者生成时版本与原始日志。完整metadata读取只用于结构/数量统计，10417条标准未全部进行语义人工审读，4605张参考图未下载。

表格全行数值存入结构化证据；T4逐模态和T3多裁判支持对论文概括作有限修正。F9中的trace含具体事实及目标画面描述，规划能力、知识补充与长度的作用尚待干预分离。

追引Emu3.5、BAGEL、Showo2、MMaDA、Janus、UniBench/UniEval及多步绘画研究；将UEval定位为静态图文教程诊断层，轨迹笔顺和物理执行须另行测量。
