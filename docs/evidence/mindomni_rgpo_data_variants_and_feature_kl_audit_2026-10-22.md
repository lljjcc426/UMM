# MindOmni：RGPO、数据版本与特征KL的证据审查

第一百三十九批完成[L128](../reviews/L128.md)明确范围核心三遍与五项书面记录。[结构化证据](../../data/mindomni_rgpo_data_variants_and_feature_kl_audit_2026-10-22.json)。357目录（330论文／研究、27资源），248核心/251书面含未通过项；未确认核心82论文／研究+27资源，资源另审。无目录新增、文件删除、权重下载或独立复现。

来源：[NeurIPS2025正式版](https://papers.nips.cc/paper_files/paper/2025/hash/802e90325f4c8546e13e5763b2ecab88-Abstract-Conference.html)、[固定源码](https://github.com/TencentARC/MindOmni/tree/a4c943667d0dbc06fa61577d8a4b585a66972e14)、[HF制品](https://huggingface.co/EasonXiao-888/MindOmni/tree/9329cf54d0b66c4f499fd8f4c1575c81b6edde86)。正式PDF25页；官方supplement ZIP含旧RG-VLM稿4页补充，名称/编号不同，不当独立新研究。

## 问题与贡献

把已有VLM的知识、算术和图像条件理解传给图像生成器，使复杂提示经过显式文字推理后生成符合隐含语义的图像，并用实际图像反馈优化推理策略。任务为图文理解/图像生成及图像编辑，不提供连续视频、中文字笔顺或真实执行验证。

传统T2I直接编码提示，隐含数学/文化/时间空间信息可能未被解出；外置LLM重写和生成器接口易损失上下文，纯文字RL奖励也不能直接反映图像结果。用VLM隐藏状态接入扩散器、CoT SFT建立格式与语义规划，再用格式及CLIP图文反馈更新文字策略，双模态正则约束偏离。该反馈仍可能忽略精确计数/顺序/字形与物理正确性。

三阶段：冻结预训VLM/OmniGen训练decoder connector并用RF/教师特征蒸馏对齐；CoT指令SFT训练生成接口和decoder LoRA；RGPO采样多条文字CoT并生成图像，用格式+CLIP组相对优势更新VLM LoRA，加文字和视觉特征KL。公开实现的policy ratio在文字token上，生成器提供奖励及可微辅助特征；不等于对扩散轨迹执行图像policy gradient。

## 输入输出与结构

文字/可选参考图→Qwen2.5-VL图文编码与AR文字CoT/answer/IMG→隐藏序列经3584到3072投影与2层Phi3 decoder connector→OmniGen噪声latent/t与语义条件→RF迭代→VAE解码RGB图像；理解路径输出文字。正文提出编辑时额外VAE参考图条件保纹理布局；当前src/mindomni.py的公开generate_image接口实际将参考图传VLM，gen_pipe调用仅传正负context等，未见这里显式传参考VAE latent，不能据此认定所有实现路径都提供正文设计。cascade_thinking选项再做一次文字推理，不是中间图像反馈循环。

VLM Qwen2.5-VL-7B、独立OmniGen约3.8B/Phi3-32层3072维decoder、connector及VAE组合。HF mllm配置28L/hidden3584/Q28KV4/FF18944；ViT32L/1280/16heads/patch14/merge2；image_decoder32L/3072/32heads/FF8192；VAE4通道latent/空间8倍/scaling.13025。connector线性3584→3072后2层Phi3DecoderLayer。表中7B明确仅LLM backbone，不能作为整个系统驻留参数。AR文字CoT和RF连续图像两套机制共用语义条件；无视频时序/笔画事件头。

## 数据和实验协议

A1 stage1 LAION-COCO/JourneyDB图文、OmniGen X2I多任务/上下文/主体数据，Sana与FLUX按已有prompt合成；stage2 Qwen2.5-VL生成CoT指令，stage3 Qwen3合成逻辑推理文字。正式表2/3星号版另加高质量数据，相关引用GPT-4o生成及BLIP3o，当前README明确使用BLIP3o公开数据；与原阶段消融版本区分。未公开完整逐阶段unique样本量/切分、去重/去污染、所有合成筛选和完整内部路径数据；教师上游先验与数据成本不能忽略。

GenEval对象/计数/颜色/位置/属性；DPG-Bench多维提示遵循；WISE文化/时间/空间/生物/物理/化学及overall；理解MMMU/MMBench/RealWorldQA；正式A2新增GEdit SC/PQ/overall。训练奖励为格式regex和CLIP图文一致性，不能当这些测试指标的等价物；无有序OCR/CER、文字空间绑定、笔画时序或视频指标。WISE分数在T3用0–1而T7–9用0–100，分别记录。

T2专用生成Sana1.5/FLUX/SD3.5/PixArt-alpha/HunyuanDiT与统一OmniGen/Showo/Janus-Pro/BLIP3o/BAGEL等；T3同类及闭源GPT-4o/Gemini2.5，T4 Qwen2.5-VL/Janus-Pro/MetaMorph/LLaVA-NeXT/Emu等。部分†分数使用prompt rewriting，不是完全相同提示协议；参数列仅LLM backbone，预训数据、额外HQ数据和采样预算不统一。T3 FLUX2.7B与T2 12B列存在口径差异待原始来源核；不以榜单作受控架构优越性证明。

正式A1 stage1恒定lr1e-4/wd.05/batch1024/256²，stage2 lr5e-5/512²，stage3 cosine/G4/βT.01/βI.06；WISE thinking1024²。公开stage1启动为1进程×batch16/lr2e-5/wd.0001，stage2 batch1/decoderLoRA16/lr5e-5/wd.0001，冻结VLM；这些示例不是正式全训练配置。RL脚本8进程×perdevice4/accum1/G4/maxcompletion2048/lr1e-5/LoRA64alpha128drop.05/冻结vision/100epochs/存验50步；内部checkpoint与数据路径，未取得原始运行日志或硬件时长。RL图像反馈512²/CFG3/seed42固定，推理pipeline默认50步/两CFG分支/1024²，50步约100分支前向且还需VLM/VAE成本；没有端到端速度测量。

## 主结果与消融

T2原MindOmni GenEval.81/DPG83.0，星号HQ版.83/82.5：Gen总体升但DPG降，双对象.97→.94/计数.77→.71/位置.59→.71有取舍。OmniGen.70/81.2；Sana1.5 DPG84.5高于两版。T3原模型无CoT.43、CoT.60，星号CoT.71；BAGEL.70，星号文化.75<.76/物理.72<.75/化学.52<.58，不能称各类最佳。T4 Qwen2.5VL基线51.1/83.4/68.9→51.6/83.2/68.1，MMBench−.2/RealWorldQA−.8，三项均值−.167分；正文约.1%说法不等同严格不退。正文较MetaMorph MMB+9.8与表75.2→83.2的+8.0pp不一致。正式A2 GEdit SC6.55/PQ6.92/overall5.95，未给完整编辑对照和方差。

T5 stage1 .73/.42→+stage2 .81/.54→+stage3 .81/.60；跳SFT只RL .72/.49，支持此配置下SFT打底且RGPO增加WISE6pp，Gen不再升；不能把星号.71的全部收益归RGPO。T6 MLP1层.1%/2G/.63，decoder1层1.5%/31G/.68、2层3%/60G/.73，结构/参数/FLOPs同时改变，不是等容量机制隔离。T7 βT0/βI.01为.79/58.8，.01/.06为.81/59.8，.004/.01为.80/58.9，.01/0为.78/58.2；部分比较同时改两系数。T8 G2/4/6为.79/59.2、.81/59.8、.79/59.3，预算不等。T9格式56.1、CLIP59.4、二者59.8，+.4无CI。F4奖励约.30→.312/format趋1/长度增；F5长度100约59.2、300约59.8、600约57.8，未呈单调test-time scaling。

## 局限与条件化优势

Eq4印刷优势分母为组内平方偏差平均即variance，代码用torch.std+1e-4；Eq6视觉KL正文写current||reference，代码F.kl_div(logcurrent,reference)为reference||current。pretrain teacherKL也具体采用层特征标准化+温度3的softmax，非RGB分布KL。RL gen_kl用新高斯latent/随机t、同一冻结decoder/connector的逐层特征；output_images仅取尺寸，不是生成轨迹完整分布KL。公开TASK_TYPE=mindomni经自定义reward selector仅接受rec/ust，所读分支将落Unsupported；还依赖内部初始化/权重路径，未执行不能宣称可直接复现。CLIP比较输入含user+assistant CoT，可能偏好冗长相关描述；fixed seed不检验多噪声泛化。附录Fig9 answer写two large elephants，图示为一象一兔，与CoT/指令不完全一致，单例不估总体率。A4承认纯文字CoT，多模态CoT/扩展模态为未来。无完整训练数据、配对多seed统计和视频笔顺验证。

在需要从知识/算术/图像理解解出隐含条件、VLM答案可信且CLIP足以区分候选图语义的分布上，CoT接口+图像反馈可能比无推理条件提高WISE；KL在不完全破坏原生成器分布时可能减轻遗忘。精确字符顺序/笔画、复杂空间关系、超长或跨文字识别、CLIP语义捷径、错误推理及参考图细纹理未必受益。长CoT或额外HQ样本带来的收益须与推理和数据成本对齐；不推出共享UMM一定胜独立rewrite+generator。

## 可证伪实验与科研写作

固定VLM/OmniGen、原始及HQ数据量、unique提示族和总训练GPU秒，比较无CoT/SFT、answer-only、完整CoT、打乱或错误CoT、外置同VLM重写同生成器；拆CoT内容与额外tokens。RL格式/CLIP/可验证算术或关系奖励逐因子，固定βI测βT并比较variance/std与两KL方向；G2/4/6匹配总rollout和解码预算。独立多seed生成、评测裁判/CLIP版本固定，报告置信区间、计数/关系/CoT正确-图正确四格、错误CoT传播。对文字任务测区域对齐、有序CER/重复增字和跨字体字系，对严格笔顺用规则SVG/VideoSketcher/强视频模型同终态异轨迹对照和事件接触/持续性指标；图像推理结果不能替代视频因果检验。实验均未运行。

Intro从T2I隐含推理缺口到VLM知识迁移、CoT、图像反馈三环，Method按接口/对齐损失/SFT/RGPO组织，Experiment把基本生成/推理生成/理解保留与阶段消融分开，适合学习。Claim要绑定正式版原始/HQ数据和具体任务；视觉KL应明说特征代理、方向/归一化与代码一致，7B标注完整系统口径。长CoT效果曲线为限制主张提供反证；Limitations还应写CoT不忠实、CLIP捷径、数据/预算/入口复现问题，而不只把未来多模态扩展当局限。

## 实际读取范围

NeurIPS2025正式25页PDF完整下载17065999bytes，Abstract/Intro/Related/Method§3.1–3.4/Experiments§4.1–4.4/Conclusion、T1–9与Eq1–7核心原文；A1训练全文、A2 GEdit、A3详细response选读、A4限制/A5图注及checklist统计/资源相关声明；非逐篇参考文献/全checklist泛用指南。实际p4/5/6/7/8/9/10/16/18共9页核框架、公式、主表/消融、曲线与CoT样例；其他定性页未逐图。arxiv v2 HTML全部核心及A1–4，正式新增星号/编辑优先正式版；官方ZIP中4页旧RG-VLM补充仅读A1与部分详细CoT，不独立算新研究。固定GH a4c9436完整171项树/137blob，README发布/数据/结果段，pretrain model构造/connector、loss核心、两启动全文、train冻结/LoRA优化器段；RL stage3启动全文/主入口/奖励选择、trainer冻结和policy损失、qwen奖励与gen_kl活跃函数；src mindomni图文/CoT隐藏/生成入口、image_pipeline采样/两CFG段。HF9329cf5元数据25文件/卡片全文与mllm/image_decoder/VAE配置全文。无权重下载、运行训练推理或独立复现。

## 版本与因果归属

| 正式证据 | 可以支持及需要保留的边界 |
| --- | --- |
| 原版GenEval.81/DPG83.0/WISE-CoT.60 | 对应三阶段主消融；WISE从SFT .54到RGPO .60，GenEval不变 |
| 星号HQ版.83/82.5/.71 | 追加高质量数据后的不同版本，DPG和计数等也下降；不能把WISE+.29全归RGPO |
| 表4 Qwen2.5VL 51.1/83.4/68.9→51.6/83.2/68.1 | 有理解分项退步，不能写完全不遗忘 |
| 表6 decoder2层.73 vs MLP .63 | 参数/FLOPs3%/60G vs.1%/2G，容量与计算均未对齐 |
| 表7 βT/βI多处同时变化 | 一次只改一项的比较才较接近隔离正则作用，仍需统计 |
| 表8 G4优于2/6 | 需匹配总采样数/训练和推理成本 |
| 表9 CLIP59.4→CLIP+format59.8 | 小幅差异，无多seed区间不能推出稳定普适收益 |
| Fig5长度300约59.8、600约57.8 | 更长CoT不保证更准确，需同预算思考质量和停止策略 |

## 正文与实现差异

[预训练loss](https://github.com/TencentARC/MindOmni/blob/a4c943667d0dbc06fa61577d8a4b585a66972e14/pretrain/train_helper/loss.py)用随机RF路径MSE和教师逐层隐藏特征蒸馏。特征先标准化，再以温度3 softmax，KL按teacher||student计算。论文抽象的分布正则在这里是特征代理，不能解释为准确测量图像密度的KL。

[RL trainer](https://github.com/TencentARC/MindOmni/blob/a4c943667d0dbc06fa61577d8a4b585a66972e14/rl-postrain/src/open-r1-multimodal/src/open_r1/trainer/grpo_trainer.py)将format和CLIP奖励求和，用组内torch.std归一化；Eq4写的是平方偏差平均即variance。policy ratio/clip在文字completion token上；图像decoder和connector冻结，其可微前向仍可把辅助梯度传给VLM条件。不能写decoder冻结就没有视觉梯度，也不能写整条扩散轨迹在做policy gradient。

[gen_kl活跃函数](https://github.com/TencentARC/MindOmni/blob/a4c943667d0dbc06fa61577d8a4b585a66972e14/rl-postrain/src/open-r1-multimodal/src/open_r1/vlm_modules/gen_kl.py)只从output_images取得尺寸，再抽新高斯latent及随机t；比较当前/参考VLM条件经过同一冻结生成器后的逐层标准化隐藏特征，F.kl_div(logcurrent,reference)对应reference||current，与正文Eq6方向相反。它不计算已生成图片的精确概率，也没有重放实际采样轨迹的所有状态。方向及std/variance差异的效果需实验，静态审查不能确定最终主表用了哪版实现。

[qwen奖励](https://github.com/TencentARC/MindOmni/blob/a4c943667d0dbc06fa61577d8a4b585a66972e14/rl-postrain/src/open-r1-multimodal/src/open_r1/vlm_modules/qwen_module.py)格式用regex search，验证标记而非推理正确；CLIP的文字含原请求及assistant CoT，图像反馈固定512²/CFG3/seed42。需要独立算术/关系/文字顺序正确度与随机图像种子评价，避免学到相关词或格式捷径。

## 无独立论文制品与复现入口

[stage3启动](https://github.com/TencentARC/MindOmni/blob/a4c943667d0dbc06fa61577d8a4b585a66972e14/rl-postrain/train_stage3.sh)设TASK_TYPE=mindomni且打开自定义reward，所调用select_reward_func只支持rec/ust，mindomni会落到Unsupported分支；这是按当前源码路径推导，未运行启动脚本。get_question_template另有默认模板，不能用它的兜底推断奖励也支持该任务名。还存在内部venus初始化、训练数据与checkpoint路径，因此发布入口需要适配。

stage1示例的lr2e-5/wd.0001/batch16与正式A1的1e-4/.05/1024不同。stage2示例decoder LoRA16、冻结VLM；RL LoRA64/alpha128/drop.05/冻结视觉/G4/maxcompletion2048，与训练实际日志仍需区分。HF卡片仅简短元数据；mllm、image_decoder、vae分目录配置完整可读。权重没有下载，模型没有运行。README中paper超链接指向2406.02395，已用正式题名/作者/DOI和2505.13031核清身份。

当前[src生成入口](https://github.com/TencentARC/MindOmni/blob/a4c943667d0dbc06fa61577d8a4b585a66972e14/src/mindomni.py)可选择cascade_thinking，额外再做一次文字CoT；没有中途观察新图像的交错推理闭环。generate_image调用将参考图传VLM但未显式向gen_pipe传参考VAE latent，与正文编辑设计分开记。正式A2有GEdit6.55/6.92/5.95分数，尚不足确认所有当前公开路径与该评测完全一致。

## CoT忠实性与后续队列

正式附录Fig9中一象一兔提示的answer写two large elephants，显示图为一象一兔。该单例支持进一步检查文字规划和生成结果的一致性，不能外推错误比例；Fig11苹果解方程则明确根据物体数量取正整数解3，不能把忽略负根直接判作该任务的错误。

继续L129 CoRL、PairUni/UniCorn等协同和强化学习队列，独立追PARM、GoT、RPG/DiffusionMaster、VLM-R1/DeepSeek-GRPO等引文的最新原文及制品；引用被识别不代表已经完成精读。严格笔顺/视频生成仍需事件和RGB时序可观测性实验，MindOmni的静态图像和CoT结果不提供此验证。
