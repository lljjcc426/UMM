# 加速、缓存与反思：核心三遍审查

本批完成[Hyper-Bagel](../reviews/C03.md)、[FlashU](../reviews/C04.md)、[UniCache](../reviews/C05.md)、[UMM-Reflection](../reviews/C07.md)核心方法、公式作用、框架视觉、主表与现有消融、批判阅读和各五项书面检查。核三公开代码固定版本及Reflection的HF模型/数据卡，无独立模型运行。

## 加速与质量必须在同一条件下解释

| 工作 | 实际机制 | 已读证据与限制 |
| --- | --- | --- |
| Hyper-Bagel，2025技术报告 | target验证draft；多阶段蒸馏降6/1NFE | 理解98.3→212.4TPS；生成16.67×/22×由100/6、132/6计算，缺相应端到端延迟 |
| FlashU，CVPR2026 Findings | FFN/层/token剪枝、head缓存、少步CFG | A100约1.78–2.01×；MMStar56.6→48.3，7B GenEval .76→.72，需明确质量代价 |
| UniCache，2026预印本 | task/type分KV、混合eviction/quantization、预算调度 | BAGEL多数指标近基模；SenseNova GEdit6.691→6.130；managedKV压缩≠总峰值显存同比下降 |
| UMM-Reflection，2026预印本 | SFT后共享根图的整轨迹RL同时更新text/flow | 本地GenEval约.72→.84、四图对照与指令替换支持修复收益；仍需同总算力独立双模型对照 |

FlashU正式身份核于[CVF Findings登记](https://openaccess.thecvf.com/content/CVPR2026F/html/Ke_Flash-Unified_A_Training-Free_and_Task-Aware_Acceleration_Framework_for_Native_Unified_CVPRF_2026_paper.html)，pp9131–9142。本批精读arXivv1，正式版未逐页比较；不将Findings记作主会。其余按当前已核预印本/技术报告身份。

[Hyper-Bagel v1](https://arxiv.org/pdf/2509.18824v1)6NFE GenEval .8647近自重评.8640，但位置.7400→.7175，两物体.9520→.9394；GEditEN总分微升而SC/PQ下降。1NFE .7962及编辑总分约5.97有明显代价。文字speculative verification和图像近似蒸馏的保证不同；当生成图像改变下一轮像素上下文时，冻结理解权重不能保证交错系统输出相同。原/蒸馏两套generation分支供prefill/denoise使用的内存与切换成本须纳入。

[FlashU v1](https://arxiv.org/pdf/2603.15271v1)Table4去layer skip后质量85.56优full84.39，耗时6.70s大于5.89s，显示Pareto取舍。正文Vnorm代理保低范数token，Algorithm1却TopK高范数，Gather也有歧义；不替作者补协议。固定[189f877代码](https://github.com/Rirayh/FlashU/tree/189f877953387f8b7f1e3f4d63eddbc5b597da52)的config默认35步、末11步full、前24步CFG7.5/后11步10，正文τ默认.2与附表.3不同。公开T2I patch已定位；完整MMU Vnorm路径未核，README旧API例/占位VAE下载需按实际入口处理。

## UniCache参考与物理实现需联立复核

[UniCache v1](https://arxiv.org/pdf/2609.32831v1)约80%/60%为KV预算和存储压缩，protected boundary/currentlatent不参与共享压缩预算。Figure8报告persistent managedKV，理解吞吐token/s、视觉吞吐denoise step/s，约20K KV/branch时up to1.78×，未给完整模型峰值VRAM同比数据。

固定[800fca9代码](https://github.com/Superone77/UniCache/tree/800fca9b17543b82a29ee1e36a12882c8d889731)README区分：torch参考版用attention-guided动态预算和fakequant做质量；engine物理版用固定类型预算和冻结H2O选择做效率。editing示例engine2bit/group128、torch初始4bit/group32并动态调度。不同默认路径不能直接拼成同一个配置同时实现表中质量与图中吞吐。下一步真正复现应对同engine配置同时测质量、managedKV、临时工作区、peakVRAM、端到端延迟；本轮没有运行这些实验。

Table3去保护GenEval .780→.567是重要消融；Table4线性与attention schedule同.780，PIE另有小优势。Tables1/3 UniCache PSNR18.969/19.100与Structure .100/.101不同，缺逐表配置对应。SenseNova编辑−.561约8.4%相对下降和BAGEL counting/binding下降，限制“全任务可忽略损失”表述。

## Reflection的机制证据与研究启发

[UMM-Reflection v1](https://arxiv.org/pdf/2609.35767v1)通过外部controller逐轮回填同BAGEL产生的反思与图像；训练使用外部verifier，推理只用UMM。共享根图的16 siblings整轨迹advantage同时更新文字/flow，初图detach但共享参数使其分布仍可漂移。

Table3 flow-only73/text-only78/joint84；四图BestOf4约80、forcedSFT72；AppJ固定图像、renderer和noise仅换指令，RL48.4%修复、SFT21.4%、原请求20.5%、规则27.6%，提供文字执行作用的受控证据。仍缺同总训练与推理FLOPs的独立VLM+renderer联合优化对照，不能据此认定共享架构具有必要优势。probe可解码正确性与attention相关也不能代替因果干预。

GenEval单物体1.00→.95，damage6.53%→约8.8%，正确图被错改的案例必须保留。primary最终几乎均编辑三轮；stopbonus实验112/116失败来自过早done，不能声称已学会可靠高效停止。OneIG只695个alignment样本，CompBench的3D关系仍是2D图像任务；初图差异不显著也不等证明等价。

固定[0f4a135代码](https://github.com/waltstephen/UMM-Reflection/tree/0f4a1352ac9e0b2c179518e54b31c4546b5aa539)的eval入口补CFG3/noise.8/temp.5，训练launcher覆盖裸config默认。论文每update2roots、HF卡写eachrank2prompts、launcher localbatch2，跨rank全局独立root总数尚未沿完整采样代码核清，保留协议差异。论文RL16H100×33h≈528GPUh仅update time，不含SFT和外部合成。

[HF RL卡固定版](https://huggingface.co/YijiaFan/UMM-Reflection-BAGEL-RL/blob/ba427ac677e98de385aaf16c167c159ff22845b5/README.md)和[HF数据卡固定版](https://huggingface.co/datasets/YijiaFan/UMM-Reflection-SFT-Data/blob/ecb5a3bff758ac2a71d42be10a622ea60832fa70/README.md)已读，文件目录含权重/100轨迹parquet分片；未下载大文件。29529轨迹与展开167363训练rows、1265anchor分别记录。数据含174条GEdit，若评该benchmark须剔除；数据research-only及行级source限制，不能由模型Apache2推数据同许可。

## 可证伪实验与写作

1. 加速：固定精度/分辨率/prompt/seed/CFG，分解prefill、draft/verify、denoise/head、VAE与加载，给同质量和同延迟两种Pareto、分位延迟及峰值显存。NFE、GPUh、managedKV、peakVRAM各有分母。
2. 缓存：同byte预算比全局与类型策略，逐项消融protection/allocation/schedule；同物理backend联立质量/速度，跨域校准与后期回访测试不可逆淘汰。
3. 协同：固定root/image/noise干预反思文字，text/flow更新2×2，加入独立critic+renderer；配平总FLOPs、图数与token成本，独立judge、人评、多seed并报repair/damage/stop。
4. 规范书写：以上全为静态图/编辑/回答证据。若迁移到视频或笔事件，需新增逐笔方向/顺序、抬落/重笔/漏笔、RGB时序可观测性和执行数据；不可用图文语义分数代替。

Method可学习按瓶颈分解、协议先行及固定根图对照；Claim需以同配置表格为范围，Limitations主动记录退化、停止失败、协议/实现差异。当前339条目录/339笔记，70项核心三遍与五项书面检查；其余精读、阻塞全文和候选追引仍在继续。无文件删除。
