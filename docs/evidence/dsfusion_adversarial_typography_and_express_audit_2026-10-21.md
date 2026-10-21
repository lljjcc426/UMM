# DS-Fusion：静态艺术字、对抗约束与Express制品

第九十二批补录并完成[G041](../reviews/G041.md)核心三遍/五条书面，目录354条（327论文／研究、27资源），185项核心/188项书面含未通过项，169条尚未确认核心三遍（含资源）。[固定代码/Space审查](../../data/dsfusion_formal_and_express_release_audit_2026-10-21.json)记录发布与论文的条件差异。没有删除文件、下载模型权重/数据媒体或运行模型/在线demo。

## 原文与任务

[DS-Fusion ICCV2023正式论文](https://openaccess.thecvf.com/content/ICCV2023/papers/Tanveer_DS-Fusion_Artistic_Typography_via_Discriminated_and_Stylized_Diffusion_ICCV_2023_paper.pdf)pp374–384，共11页；读核心§1–6/全部核心式/T1–2与已有消融文字。实际核p2F2、p7T1、p8T2/中文日文F12、p9F15–19。[作者supp](https://ds-fusion.github.io/static/pdf/supp.pdf)17页，读§1–6说明和指定人评/构造图；未遍读全部画廊/参考文献。固定源码只审指定核心路径，未全审所有库或完整训练/评测生态。

输入是栅格字形与语义风格词/可选属性，输出静态彩色艺术字。论文展示多字整体、中文、日文及一般形状，需纳入相关工作，不能误记为仅Latin。字形输入已存在；没有连续视频、笔画顺序、落笔/抬笔或机器人执行监督。与[L051 Word-As-Image](../reviews/L051.md)不同，它训练扩散UNet和判别器，并允许栅格色彩/纹理；与[L052 modal动画](../reviews/L052.md)也没有同一时间目标。

## 方法和模型

冻结LDM先按风格生成约25张图；冻结VAE将style图和glyph分别编码。BERT条件UNet对加噪style latent预测噪声并反算clean latent，DCGAN式latent D将其与glyph latent对比；交替训练UNet/D，diffusion MSE与λ=.01对抗项维持语义/字形折中。推理经扩散采样/VAE decode输出图像。单字组合例另用rembg去背景，并渲染/配色其余字母排版。

默认为BERT条件LDM256，公开配置BERT32层/1280、UNet base320/4层级/heads8、latent4×32×32，VAE/文字encoder冻结。不能将其默认架构记成CLIP版SD1.5或理解/生成共享UMM。D在latent上5层卷积、普通1头/generic26头；代码G用非饱和BCE(Dfake,1)，D用real1/fake0 BCE，论文总min-max表达不是精确代码标量。

latent分布约束可提高字形相似，但不保证每张样本逐字符正确。λ过高使glyph占优/语义弱，过低可能收敛不到glyph，F15实际展示此取舍。其理论适用条件应是VAE仍保留可辨字形、合成style覆盖目标语义和二者可协调；相同机制不能直接保证笔顺或真实书写可执行性。

## 主结果和评价条件

| 协议 | 原始报告 | 可采信结论 |
| --- | --- | --- |
| T1单字体SF | OCR36.4/blur61.8/CLIP21.1；SD7.0/4.9/23.1；DALL-E2 4.9/9.8/22.3 | 指定OCR较好、风格affinity较低，不是双目标全面领先 |
| T1多字体MF | DS5.1/20.5/24.1；CLIPDraw6.4/17.9/23.2 | 风格/blurOCR提升，但原OCR下降；字体训练分布改变 |
| T2方法人评 | DS49.06、DALL-E29.38、SD9.38、CLIPDraw6.88、Equal5.31（%） | 32人/10案例、设计师从每方法4候选选1；不等于随机无筛选胜率 |
| T2艺术家人评 | Human57.14、Equal11.19、DS31.67（%） | DS加Equal42.86%，严格胜出31.67%；不能写42%击败艺术家 |
| 非Latin/多字/泛化/自绘风格 | 主F5/F10/F12、supp自绘6图等 | 以选例为主，未给这些子分布的系统准确率/链式过程评价 |
| F15/F16/F17 | λ.1/.01/.001、5/25/50style图、CLIP encoder例 | 定性消融，缺λ0/去D量化、多seed/CI和纯encoder受控对照 |

量化称21个style词、全部字母、每词每方法随机4张；最后样本分母、随机发生在排序前后尚不明确。方法§3.4又给CLIP字形/语义双轴排序；人评另用设计师选样。三种候选政策须分别保留。T1与Word-As-Image的10字四选一识别协议不同，不能直接把OCR36.4与选择题.90排同榜。EasyOCR规范化/失败分母、blur核和CLIP可执行配方仍不足；“显著/最优”缺统计检验数值时不得自行加强。

正式训练写Adam lrG1e-5/D1e-4、单字体800 epochs约5分钟、多字体1200 epochs约8分钟、RTX3090。没有完整阶段成本拆分，不能直接解释成一张图推理延迟或与无逐例训练baseline等算力。

## 固定源码与无论文制品核查

[GH c63e5de](https://github.com/tmaham/DS-Fusion/tree/c63e5de51244914033ea444751cbfd6e757b6d9c)根16项及ldm78项子树已取得，超大递归全树响应不完整，未作为完整树证据。读README/两个finetune配置、D全文及训练loss/冻结/optimizer、Rasterizer、主入口数据/LR和采样指定段。需要保留这些差异：

- 源码AdamW，配置max_steps800、batch1、num_samples2001；与论文800/1200个完整epoch不能互换。generic配置仍接普通单字Rasterizer/number0，没有据此复原40style×26字训练流程。
- 新style生成2×10=20张，报告25；Rasterizer按i%(N−1)访问未排序列表，若新目录20张则19项可达。旧缓存可能改变N，本次未执行/统计实际目录，不能把结构推论冒充实验。
- 默认预生成字体路径将输入截为首大写字符，custom_font分支可保留全串；多字/中文论文选例不能自动当默认CLI端到端已复现。style目录按首style词复用，属性变化需明确重生；README写make_data而实际参数data_make。
- txt2img内部随机1–500覆盖参数默认seed42；显式示例50步/eta1与parser200步/eta0不同。所读采样入口直接保存候选，未看到论文CLIP双轴排序/完整EasyOCR评测入口。
- classes.txt42非空行、41唯一词且CACTUS重复；不能当正式40类精确清单。上述差异限制复现配方完整性，不能反推论文权重必有某项错误。

同时核查[HF DS-Fusion-Express固定482a035](https://huggingface.co/spaces/tmaham/DS-Fusion-Express/tree/482a03580b670affd03511829e8453f2c517e1c5)元数据/README与app生成/界面指定段。这是配套通用checkpoint demo制品，关联G041记录，不重复计独立论文/模型研究。

app用all2.ckpt、首输入字符、4候选/50DDIM/CFG5/eta1/256²；所读生成函数没有每输入微调调用，字体选择UI与去背景按钮已注释。它与每style–glyph逐例微调、完整多字/中文、原论文自动排序均不能直接等同。≈60seconds是界面文字，未实测；all2.ckpt与论文generic/README下载checkpoint的对应关系未确认，未下载权重或调用服务。代码MIT、网页CC-BY-SA4和底座/权重/字体条款属于不同资产，完整许可未审。

## 可证伪设计与科研写作

固定底座、训练/生成样本和总FLOPs、字体信息，对无D/像素D/latentD/显式OCR约束、style量/λ/字体混合做全因子与多seed。分别随机/CLIP排序/人工从相同候选数选，报告所有候选及筛后结果、自由转录/完整词、独立语义/美感盲评，校准OCR和blur代理。对style×letter×font隔离测试真正新组合，单独验证通用版与逐例训练；完整阶段延迟和额外数据成本入表。先修明确版本配方，再谈复现，以上实验未运行。

若迁移书写任务，先确认latent codec对字形/细笔的重建上限，再加入非周期事件/累计墨迹监督，评同终态不同笔顺/方向/暂停及动作约束。静态latent D只说明终态/局部分布，不识别唯一合法过程；也不能以“加入判别器”本身作为创新，需要继续检索已有动作/轨迹研究。

Intro可学习把语义/字形竞争与无配对目标连到具体设计，Method按数据流给style latent/判别/总目标/排序；主表SF/MF保留退步，人评将胜出与Equal分开，Limitations列style–glyph不相合、长词结构、逐例成本和选择器不足。与L051/L052的关系应按输入、优化对象、输出表示和真实时间定义组织，避免按“都用扩散”合并任务。
