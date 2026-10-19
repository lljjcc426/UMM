# 书法、视频文字、绘画顺序与OCR：任务和实验协议复核

2026-10-20；第二十八批。九项均为已有记录，新增本轮独立分析，无新增独立论文计数、无删除、无模型执行。逐篇字段及读过/尚未读范围见[325份笔记目录](../reviews/README.md)，本批七项书面理解检查有框架图视觉核，完整三遍仍未完成。

## 任务边界

UniCalli是列级静态书法生成/识别；DeepCalliFont处理参考风格图像与轨迹；OnOff连接词级轨迹、brush代理、静态增强与机器人。Text-Animator控制场景内完整字符串的字形与camera运动。Draw This First生成可由语言改变区域/部件顺序的polyline。Video models are zero-shot learners and reasoners用现有黑盒Veo API探索视觉任务。Ketaba将历史阿拉伯手稿行图转录为文字。

VidScribe的核心是四类视频文字任务的benchmark、评价框架及其偏好训练应用；VTR-Bench是多载体文字信息基准及首帧Agent推理应用。二者均不能改写成专门生成规范汉字笔顺视频的UMM。名称中的unified、stroke或generation必须结合真实输入/输出和评价目标解释。

## 读表后的必要修订

[DeepCalliFont正式AAAI论文](https://ojs.aaai.org/index.php/AAAI/article/view/28168) Table2常规字体FID105.9，FontRL40.7；ours在MAE/LPIPS/DTW较强但FID不是最优。书法子集FID14.6的优势不能跨分布概括。Table1去IFR23.7、去diff24.6、去预训43.4，对full14.6，勾选与数值已视觉核；训练数据/预算与真实时间动力学仍分别核。

[OnOff v1](https://arxiv.org/pdf/2608.03198v1) Table4接One-DM后CVL FID19.45→14.45，CER却.2877→.6285；IAM CER.3117不变。视觉真实感/样式和文字正确性不是同一指标。其pressure为RDP后相邻点距离归一反向proxy，无真实Δt/力单位，max合成也不建模完整湿墨/吸收历史。物理可解释性不保证参数可识别或力校准。作者项目标注ECCV2026；主办接受页本次未定位该条，正式页码与最终版本另核。

[UniCalli正式作者PDF](https://www.yingcong.me/publication/2026-xu-unicalli/2026-xu-unicalli.pdf) Table2总体识别.540略高CalliReader.533，但草/行/篆并非全优；Table5甲骨62.5低OracleNet73.9，AppTable6外部F1.498低GOT.593/Qwen.534。Table4加入最后drop时FID改善，SSIM.613→.602下降。方法共享与合成/无标注数据同时变化，未直接分离双任务的等预算因果收益。主文RoPE加embedding与AppE的feature加embedding描述有差异，需要按实际版本审码。

[Text-Animator v1](https://arxiv.org/pdf/2406.17777v1) Table1SenAcc.779/NED.802较强，但FID180.6不优AnyText+AnimateLCM153.7；Table3扩张.9的NED.804又略高默认1.2。两ControlNet沿既有方法/数据训练后冻结聚合，不能把“无需进一步调参”解释成没有训练。其同线depth和短16帧设定限制强形变/遮挡外推。

## 同图改序、弧长与严格笔画

[Draw This First v1](https://arxiv.org/pdf/2608.12064v1)已经做固定图和seed改变caption：Table1无captionτ.096→有caption.449，图IoU基本不变；Table3区域τ.838、part.461、pass.444，within-unit明显较低。AppTable5训练orderhead改善编码上界，但Table6gtlatent部署路径仍是原笔数2.29倍，说明碎片并非全由生成器产生。研究假设不能遗漏这组直接干预。

该codec用累计弧长，不保time/pressure/tilt/width；作者给出尾句指令31.5%低于无指令32.6%等具体失败。可迁移研究是细粒度笔事件、可观测性、方向/抬笔、全时序和执行控制，并必须继续检索其他工作是否已有解决，不能仅凭发现本文限制宣布新题。

[Video models are zero-shot learners and reasoners v2](https://arxiv.org/pdf/2509.20328v2) Figure30的逐笔符号复制6/12成功，颜色/数字是后加标注，非模型自产规范笔序。报告的其他定量结果区分pass1/pass10、末帧/事后真值选最佳帧；Vertex系统包含LLM重写，零本次任务适配不证明预训从未接触任务。把Veo当强现成零样本基线合理，声称汉字标准笔顺已解决则缺证据。

## 两个视频文字基准怎样用

[VidScribe v2](https://arxiv.org/pdf/2609.36598v2)为803例、12因素、11公共指标和2编辑probe。A2查采样帧空间拓扑；F12含handwriting_stroke，AppA2从已有首笔开始，没有完整规范strokeID/时间真值。1000独立prompt×8候选生成偏好，LoRA/DPO后heldoutT2V Overall45.92→48.42。人评文本偏好68.8%，非文本51.6%，不能只据超过一半就声称所有维度显著。因素回归/分层bootstrap加强关联诊断，但不等随机因果干预。

[VTR-Bench v1](https://arxiv.org/pdf/2610.01499v1)读每载体最清楚出现，对预测按reference长度+5截断并capWER1；不是完整时序或标准无界WER。H3Agent WER.4468→.3015，但它用了T2I、反馈和候选选择，未完整报告同成本调用预算；UI的I2V WER还优full。100条human样本偏向可读模型，需独立验证低可读尾部。两个基准可组合，不能互相替代或跨数据直接排模型名次。

## Ketaba：正式论文、模型卡与伪真值

[ACL正式论文](https://aclanthology.org/2026.nakbanlp-1.21/)明确官方corpus CER.0938/WER.2996第3；按行CER.0819第1，但WER.2588不优Misraj.2516。适配起点应比较未适配HRT.2032，organizer.584的差不能单归因LoRA。附录用集成输出构造PseudoGT分析个体；总体CER<.1不能保证每行伪真值正确，更不能独立证明集成比其他输出正确。

固定[代码](https://github.com/HasanBGit/Ketaba-OCR-LoRA/tree/f1aefa8317edda0d7f064c2ae1731cdb4186b076)与[HF制品](https://huggingface.co/HassanB4/Ketaba-OCR-LoRA/tree/7f55602e5e83041c4af6ff007c7ccd1dc3e23202)确认r32/α64/DoRA/RSLoRA、训练15962+开发test2095合18057。代码默认无外部eval时随机90/10，最终19chunk制品与该路径对应关系尚需核，不能凭函数自动断言最终切分。Arabic normalization用于分组后返回原候选，未将输出全部去附标。开发test并入训练后不能再当未触碰测试；30种ensemble选择的校准/盲测提交协议也需继续核。

## 实际可取得的实现范围

固定[UniCalli README](https://github.com/EnVision-Research/UniCalli/tree/8f0b42d95e7a374e992c08736a9a3cda79743f7c)说明公开base无pred_box、生成推理已给，训练/识别仍未勾选；generation接口固定5字，以书家/style文本构prompt。sampling复制两组imageids，model给投影后后半token加embedding；shape含token位置，并非AppE2简写的单个全局vm。它不能验证未发布论文全版的全部路径。量化18GB是发布方主张，未独立测量。

固定[OnOff树](https://github.com/SeonmiP/onoff/tree/ca3f8d6f7c76d142c95d6a86f97410249d0e5f7c)仅2文件/comingsoon；固定[DeepCalliFont配置](https://github.com/lsflyt-pku/DeepCalliFont/blob/5b0efdc5c1d688997fae5dabebd5b059c29b9721/config/train_common.yaml)默认100epoch/lr1e-4/b8，脚本Adam/cosine。实际论文多组实验与这些默认是否相同仍待日志/supp。论文、代码、制品、训练配置与发布承诺分别记录，保持可追溯。
