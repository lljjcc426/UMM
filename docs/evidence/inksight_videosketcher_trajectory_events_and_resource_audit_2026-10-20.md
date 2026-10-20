# InkSight/VideoSketcher：轨迹、绘画过程、统计与资源审查（第五十七批）

原记录[X01](../reviews/X01.md)、[L010](../reviews/L010.md)完成明示范围核心三遍书面检查。347目录不变，128核心/130书面；没有文件删除或模型训练、推理、独立复现。SketchAgent原文已取得，仍待本轮精读，不提前验收。

## 先由输入、输出和监督确定任务

| 工作 | 输入→输出 | 主要监督/模型 | 已验证的评价 | 不应外推的结论 |
| --- | --- | --- | --- | --- |
| InkSight v4 | 照片+任务prompt/可选OCR文字→坐标/起笔token | 冻结ViT+从头mT5形状序列模型，五任务桥接真实OCR与独立ink | 几何语义OCR F1、online识别、人评、识别训练增广 | 唯一原始历史、真实速度/压力、规范汉字笔顺、开放文字到视频 |
| VideoSketcher v1 | 编号语义计划/可选笔刷首帧→RGB渐进素描视频 | Wan14B两阶段LoRA：15几何视频→7手画SVG；CausVid1.3B续画 | 最终可辨/过程曲线、LLM顺序偏好、styleGram、多笔帧 | 笔画实例ID/严格顺序准确率、符号正确性、真实执行动作、同质量加速倍数 |

前者的静态图不能唯一确定历史，须区分合理重建、真实历史恢复和规范约束。后者已直接建模逐步绘画且评价并笔问题，必须纳入研究假设和新颖性判断。

## InkSight：补齐训练条件，检验指标究竟说明什么

[2402.05804v4](https://arxiv.org/html/2402.05804v4)为2025-06-17版本。已读核心§1–5/三主表、AppC–M文字和相关表，实际看Fig2/3/4/8；未逐看AppB/N大批样例。官方[仓库](https://github.com/google-research/inksight)明确2025-06 TMLR接收，官方OpenReview PDF检索页也显示06/2025；[forum](https://openreview.net/forum?id=pSyUfV5BqA)遇浏览验证，正式PDF全文未读，SCI分区未核不填。

Small-p为ImageNet21K ViT、Small-i/Large-i为JFT300M；mT5形状encoder-decoder随机初始化。模型词图224²，轨迹20ms重采样/RDP，坐标[0,224]、x/y各225类加起笔共451 token，约20K单字符文字词表；输入128/输出1024。没有真实速度/压力输出，AppI对生成点按20ms赋时来训练识别器，不可描述为恢复书写动力学真值。

五任务各20%，Adafactor β1=0/原文second-moment .8、lr峰值.01/5K warm/linear参数3e−6、dropout.1、340K步/b512。Small约33h、Large105h均64TPUv5e，约500h总实验也为64芯片集群时长口径。TIII仅标准与解冻项为3seed汇总，其他消融选择同三seed中最好初始化，不能给整张表加多seed均值保证。

公开OCR TIV合294882≈295K；公开ink正文约2.7M，TIV六子集之和2564569，口径待解释；内部OCR约500K/ink16M与Small-p不同。DeepWriting字/词/行是同源多粒度，不当成互相独立作者。200人描样本只给合理描摹参考，无原始书写轨迹。

TII HierText Large-i F1.61/online Acc.46、GVS.55/.01、人描.64/.74；IAM GVS F1.69高于Large.66而online识别.02低于.58。该F1依赖商业OCR的字符框/内容/线宽；人描也仅.64。TIII去all-recognition后IMGUR F1.51→.55但online Acc.33→.22，支持把几何/语义/顺序代理分列。标准HierText.61/.45、无OCR文字Vanilla.53/.35、R+D.57/.42，去增强.23/.13，支持任务桥接和增强在原分布下有效；尚缺最强恢复基线与严格事件指标。

实际Fig8：Large good52.5%、good+okay87%、humanlike67%；Small-i good+okay87.5%，所以并非所有人评项随规模单调。16评价者各样3票、κ=.46/.44。主观could-human无规范笔顺答案。AppI真实IAMOnDB CER6.1，单用生成7.8/8.2/8.4，混合4.6/4.5/4.6，说明增广用途而非证明原轨迹重建准确。

AppJ有R+D空墨迹后回退Vanilla，须把触发率、失败和第二次调用成本计入；跨脚本/复杂草图泛化多为案例。AppO的100不匹配prompt未生成对应文字，只支持该批设置，不能当所有条件下的能力不可能性证明。

## VideoSketcher：正文、附录、当前实现逐项关联

[v1 HTML](https://arxiv.org/html/2602.15819v1)当前完整标题为“Video Models Prior Enable Versatile Sequential Sketch Generation”，原目录副标题保留作别名。作者[官方仓库](https://github.com/rhfeiyang/VideoSketcher)2026-10宣布WACV2027接收；未来正式会议proceedings尚未核。另检索到[WACV2026同名工作](https://openaccess.thecvf.com/content/WACV2026/papers/Li_VideoSketcher_A_Training-Free_Approach_for_Coherent_Video_Sketch_Transfer_WACV_2026_paper.pdf)，是视频素描转换，待独立精读；不可仅按简称合并。同样，SketchAgent也有不同同名研究，当前对照为CVPR2025顺序草图生成。

核心§1–7/Eq1–3/TI–III、AppA及B–E文字已读，实际Fig2/3/7。SVG顺序动画提供单笔渐进监督；模型无新增task-specific loss，用xt=(1−t)x0+tε、velocity ε−x0的rectified-flow回归。15几何视频含每组合3顺序，7艺术家图为单一目标画风。7×A100、batch1（全局/每卡口径未明）、LoRA32、lr1e−4，两阶段各700遍，约22h；480×832/81帧，50步单A100约16min。少量目标数据背后有强预训底座和合成监督。

AR为CausVid/Wan1.3B，全DiT以ODE轨迹回归2700遍/lr2e−6；43教师生成视频的类排除评测类，另加7手画共50。81帧约11s/24帧约4s，对比14B教师时模型、质量、目标和算法均不同，不能写同质量87倍提速。

主识别50类×2seed=100，TI full.82/.96、原Wan.92/.99、PaintsUndo1/1、SketchAgent.48/.71、人画.52/.70、AR.45/.70。PaintsUndo获FLUX2终图，属于异构输入条件；原Wan高识别但过程静态。实际Fig7 y轴为CLIP classifier score，端点不能直接当TI hard accuracy。渐进识别/像素曲线只说明可辨性逐渐出现，不证明每个事件正确。

TII全模型.82/.95与TI Top5.96存在原数差异，保留。7-human-only.88/.96在最终识别更高，full提升的是与外观共同约束下的顺序偏好。primitive/full为26.9/53.4/19.7 Neither，7human/full29.6/48.3/22.1。评委先接收目标顺序词汇再抽取视频序列，可能确认偏差；primitive不可辨也影响评委。100prompts×3seed的LLM偏好百分比不等逐笔顺序准确率。

AppB.4/TIII已经量化并笔：QuickDraw200视频中2975/15196帧=19.58%，场景80视频2351/6361=36.96%。阈值、有效帧筛选和失败处理尚未拿到；分母不同于视频数×81，不能自行猜为只去空白或所有转移。更复杂概念与更短时窗/更多笔画是潜在混杂，须做固定时长与采样控制后再归因。

TI声称mean±std across categories；若每类2次硬分类准确率p属于{0,.5,1}，均值.82时方差最小由32类1和18类.5取得，为.0576，population SD=.24，无法得到.04。这是按表述作的条件性核算；尚未取得评估代码，可能另有汇总/SEM/软score，保留疑问，不替作者确定原因或静默修改。仅有最终图指标也不能比较数学函数/文字真实性；附录已展示符号/图中文字失败。

## 论文之外的资源也需要深度核查

| 资源 | 本次读到的证据 | 访问/协议边界 |
| --- | --- | --- |
| InkSight Small-p HF模型卡 | 全文：从头mT5/公开数据/接口/TF2.15–2.17要求 | 当前仓库README用TF/Text2.20并提供XLA导入工具；固定486d4772工具全文确认导入前禁用两个HLO pass和autotune0，未运行核功能 |
| InkSight-Derenderings | HF卡全文及仓库dataset.md全文 | 含三模型/三数据集/三模式的模型输出InkML与原图关联；不能把生成轨迹当原始人类时序真值。完整包未下载 |
| VideoSketcher模型库 | HF API revision44404d83列T2V/I2V LoRA、AR_1.3B.pt，public/non-gated | README卡请求404，但API可访问；不能推为权重不存在，也不能从文件名确认性能或继承许可证 |
| VideoSketcher数据库 | HF API revisiona9c2d1fa列sketch_shapes/real/distill/style zip等 | README卡404；压缩包和内部数据未读，数量依据论文，元数据仅确认制品路径 |
| VideoSketcher训练recipe | 固定79067883 T2V shell全文、train.py构造/forward/优化器与latent wrapper选读 | q/k/v/o/ffn.0/ffn.2、rank32、lr1e−4；repeat100×7由latent wrapper长度×repeat实现数据遍历700，不能当700个程序epoch。I2V示例7/13遍与论文未对齐 |

[InkSight模型](https://huggingface.co/Derendering/InkSight-Small-p)、[数据](https://huggingface.co/datasets/Derendering/InkSight-Derenderings)、[VideoSketcher模型](https://huggingface.co/VideoSketcher/VideoSketcher-models)、[数据](https://huggingface.co/datasets/VideoSketcher/VideoSketcher-data)作为原研究关联资源记录，不新增独立论文计数。VideoSketcher README的MIT badge与实际LICENSE开头Apache2.0不一致，未作完整法律分析，也未把仓库许可外推到Wan基础模型和HF权重。

## 可检验的下一步

建立同终图多历史和规范可接受集合；分别测合理描摹、真实历史、规范实例顺序。对InkSight做oracle/自动检测×OCR/内识别/无文字×已见/未见脚本，报告fallback和成本；对VideoSketcher做等预算几何stage×真实样本数，固定fps/时长与有效帧规则，校准LLM评委有/无目标词汇、顺序交换和人工时间戳真值。生成HF输出仅作弱监督并保留来源，按原始作者/图像隔离划分。

写作学习两篇把任务拆分、机制与指标逐一对应的思路；结论同时记录主表取舍、人工主观性、数据/预算差异与已发生失败。上述新实验均未执行，全部剩余工作继续。
