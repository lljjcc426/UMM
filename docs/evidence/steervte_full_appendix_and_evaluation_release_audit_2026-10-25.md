# SteerVTE：完整附录与公开评测协议审查

第二百一十六批完成[N14](../reviews/N14.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/steervte_full_appendix_and_evaluation_release_audit_2026-10-25.json)。358目录（331论文／研究、27资源），321核心/326书面含未通过项；待完成核心深审10篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2606.23254)、[主源2](https://arxiv.org/pdf/2606.23254v1)、[主源3](https://github.com/zengkaiya/SteerVTE/tree/5001972be6906eb92214c8121606f092a36b79f3)、[主源4](https://zengkaiya.github.io/SteerVTE/)、[主源5](https://huggingface.co/MewtwoX23/SteerVTE/tree/dab2056d2c24fa96fa07cd1cff684bbb085b1d6d)、[主源6](https://huggingface.co/datasets/MewtwoX23/VTE-Bench/tree/d4e4042b9de7b6861de2f3205e4dafe381deb21d)、[主源7](https://neurips.cc/Downloads/2026)、[主源8](https://neurips.cc/virtual/2026/poster/148744)、[主源9](https://openaccess.thecvf.com/content/ICCV2021/papers/G_STRIVE_Scene_Text_Replacement_in_Videos_ICCV_2021_paper.pdf)。

## 研究问题

已有源视频、时序文字mask和目标字符串时，怎样替换英文单行字，同时保留字体/材质、背景和跨帧一致性？

## 现有不足

逐帧图像编辑会闪烁，首帧I2V易更改后续源场景，通用视频编辑缺局部glyph先验；小区域在全局latentMSE中权重低，单独OCR又倾向简单风格。

## 贡献

冻结VACE14B主干，TextContextAdapter融合前背景mask条件、原比例QwenVLM风格、行VAE与字符OCR两级glyph；GLAS=3SF+.1OCR与CFM联合，三阶段500K合成图→300K真实图→200K合成视频；VTEBench论文100Synth+100Real。

## 输入、模块、输出与公式

Fig2源49帧+mask→VAE前/背景与mask通道；目标完整字符串渲染行图与80²字符图→行VAE/PPv3neck；首帧源字crop+源文本prompt→Qwen最后两hiddenstate→connector；adapter/LoRA调制DiT→编辑视频。源全片作为输入，适用于离线编辑，未提供逐笔因果写字控制。

## 模型结构

Qwen2.5VL3B风格编码器、PP-OCRv3字符encoder、VACE14B及T5/VAE冻结，两个connector先对齐；StageII/III adapterLoRAr64。发布VACE.process以src_text进style、gt_text进glyph；Qwen拼最后两层的整prompt/vision序列，属特征提取未生成风格描述。行neutralfont提供布局，字符80²font60；OCR识别特征不构成严格笔顺或拓扑证明。F3caption写connector和DiT共同训练，与正文冻DiT/训练adapter表述不精确，以图中冻结符号及推理载入vaceLoRA为界。

## 数据分布与划分

SteerVTE1M共1Mtriplets，800K静态图/200K视频。1933GoogleFonts/65letters-symbols/OpenSoraPlan；Easy894字体、<20chars、30–50px，Hard全字体≤30chars25–40px/透明描边；字幕框占8–15%、每例1–4个仅选一处编辑，OCR100%正确筛选。RealTE AnyWord3M500K可识别→TextCtrl编辑/OCR/StyleSim>.4余300K。论文Synth50easy50hard/Real100来自视频文字数据，无编辑GT的Real；字体/词/背景互斥未完整说明。HF固定d4e4042b CSV实核Synth100/Real100另SceneText200=400，新增SceneText未在论文主表单列，全部8列无空值。

## 指标与评价协议

论文除FVD外5帧均匀平均，PP-OCRv4检测识别P/R/F1/NED相似度↑/sentence，GT编辑框SSIMPSNRFIDStyleSim及背景，Real五位本实验室同事binary正确+风格+背景QualityRate，盲化/独立评审未写。公开入口eval.sh→eval_multi_csv默认frame_number20即单第20帧，OCR路径ppv3_rec.pth/SVTR模型，无法当论文v4/5帧协议。normalize_text转小写删全部空白，sentence不检大小写空格；P/R/F1用set字符，忽略顺序与重数：cba/abc及ab/aabb均P=R=F1=1，NED/sentence仍可区分。默认skip_missing_pred仅存在预测与各metric有效项为分母；actual_count/valid_rows有记录，需一起报告。

## 对比方法

FLUXText逐帧、VACE/VideoPainter有mask，VIVA/UniVideo/Kiwi/Seedance2不读mask；所有给lineglyph，Steer额外style/charglyph条件，输入能力不同。开源20steps闭源480pAPI，Seedance主要竞争者。STRIVE ICCV2021已有三段视频场景字替换与pairedsynthetic/real数据，未列69refs/主表；“first video text editing/benchmark”不适宜无范围照抄，统一扩散/字幕与scene覆盖应分开。

## 实验条件和发布边界

16H100 AdamW1e-5/b1是否perGPU未明；StageI40Kstep832×480静态/II20K512²/III23K49frame832×480。发布infer20NFE seed1 fps16/bfloat16 tiled，pipeline默认CFG需区分论文没写；速度测试GPU/计时边界未说明。论文Eq1 t0noise/t1data，AppB2 t<.3称low-noise且clean记z0矛盾；发布scheduler用sigma噪声占比、target=noise−data和x0=zt−sigma*v，符号自洽但与论文反向。FlowMatchSFTLoss公开实现没有OCR低噪阈值分支，mask权重1+sM归一化代替显式CFM+3||W*error||²，默认先采1latent帧再VAE decode和maskresize；无三阶段launcher/config验证实际训练参数，保留发布/论文差异。

## 主结果

Synthsentence61%vsSeed33、NED.9624/FVD14.55vsVACE14.80/Style.5936；Real77%vs32、NED.9579vs.6106/Quality71%vs23；这些是作者报告未经复现。T1foregroundPSNR12.30/SSIM.4034仍有差距，nearperfect限定识别相似型分数；T5速度108s/49帧vsKiwi8s、VACE103s，不具实时证明。Real低于100%且不检全帧，不推每时刻文字完全正确。

## 消融及进一步实验

T3mask13→24%sentence，line39/char27/dual50但FVDdual17.64逊line17.28；VLM53>VLEmb51但NED.9466<.9523/FVD16.90>16.31。T4curriculum61>hybrid53>video37，严格equalFLOPs/顺序与预算未说明。OCRonly65%/Style.4794，SFonly56%/.5691，GLAS61%/.5936；SFonlyFVD13.99优GLAS14.55，不能宣称联合每项最优。F6展示内容/风格取舍，F7–12仅选择性静帧示例，未独立播放全动态视频。

## 局限与疑问

发布FVD NUM_CLIPS1/CLIP_LEN16且linspace取start0，故49frame只读前16连续帧；固定第20帧largestcomponentmask/bbox用于所有FVD帧，有移动文字时覆盖会变。公开Real/SceneText CSV video指src且无编辑GT，eval_multi_csv仍统一输出foregroundSSIMPSNRFID/FVD，这些是与原字视频的比较，应按数据集GT可用性解释；Synth指tgt。发布训练/评估OCR同v3，论文异v3/v4仅同家族仍非统计独立。英文单行/静首帧style、合成平面字幕/OCR筛选偏好、无多seedCI与独立复现，渐进书写需可见笔画前缀。NeurIPS详情页经curl核标题/作者/摘要及OpenReview vMuUnsiZxf链接；OpenReview两个PDF入口连接失败，未取得另一正式PDF。

## 预期优势条件

目标完整字形已知、英文单行和可靠时序mask，三类where/style/what条件可能提高源视频局部替字。逐笔视频中完整targetglyph/CTC会鼓励提前补齐，必须改为因果可见前缀才可验证迁移。

## 可证伪实验

固定同mask/glyph/styleteacher和总FLOPs做全因子，跨字体/词/背景独立切分；统一第三方OCR且保留case/空格/顺序/重数，报有效coverage；全49帧与快速遮挡/文字出现消失邻域评估，移动mask与首16FVD对照，Real原字vs编辑GT分开；书写测可见前缀、提前生字/回填与笔尖轨迹，不执行模型。

## 论文组织与Claim学习

where/style/what机制与组件消融、OCR/SF内容风格取舍组织清楚；主张需限定单行英文字幕、800Kimages+200Kvideo及非实时。首次/统一指标最好需追旧STRIVE和表内例外；附录与发布协议写一致，严格分开作者主表与当前默认入口，不能从静态代码差异倒推原实验失真。

## 实际阅读范围

唯一arXivv1完整23页§1–5/69条reference清单/AppA–F全读；F1–12全8contacts、F2/p4与F6/T5p18放大；T1–5所有行/Eq1–17全核。官方project文字/对应论文图核，动态图未逐帧；官方NeurIPS目录和poster详情标题/作者/摘要/OpenReview链接核；另正式PDF未取得。固定5001972b repoREADME/infer_demo/infer_bench/eval.sh/eval_multi_csv、eval_baseline指定采样/GT/有效分母/FVD分支、OCRnormalize/metrics/model、fvd.py全读、pipelineVACE与styleencoder关键节、FlowMatchSFTLoss/flowscheduler关键节/ocrvideo函数核；HF8模型文件存在、1705数据文件及三CSV400行结构核。未下载全视频/权重、未执行模型或完整代码复现；核心三遍五书面完成。

## 可直接核验的发布差异

默认入口eval.sh以FRAME_NUMBER=20调用eval_multi_csv，后者调用eval_baseline的单帧prepare_samples，OCR默认ppv3_rec.pth；FVD NUM_CLIPS=1从0开始只取16帧。P/R/F1将字符串转字符集合，cba/abc与ab/aabb都为1；Sentence和NED仍检序列，但统一转小写删除空白。论文主表是否用该入口未核，不能据此重写主表。

## 数据与监督边界

公开Synth100/Real100/SceneText200。Synth的video指tgt，另两者指src；统一评测输出的前景指标因此使用不同参考对象。三阶段图像/视频数据合计1M，视频200K；逐笔书写和英文字替换需独立评价。
