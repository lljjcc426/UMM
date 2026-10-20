# Janus/Show-o：表示、共享收益、视频扩展及公式审查（第五十六批）

补完原目录[U03](../reviews/U03.md)、[U06](../reviews/U06.md)核心三遍书面检查；347项目录不变，126项核心三遍、128项书面五问。无删除、训练、模型推理或独立复现；剩余精读继续。核心验收仅覆盖逐条记录明示的版本、章节、表、公式和实际看过的图，不代表所有附录、全部源码或独立证明。

## 四种共享层级应分开检验

| 项目 | Janus 2410.13848v1 | Show-o 2408.12528v7 |
| --- | --- | --- |
| 输入表示 | 理解SigLIP连续特征；生成LlamaGen离散VQ | 默认MAGVIT-v2离散LFQ；另有连续/CLIP理解变体 |
| 共享对象 | DeepSeek1.3B因果LLM；视觉encoder/adapter和image head分工 | Phi1.5单Transformer；图内双向、跨块因果omni-attention |
| 目标 | 理解文字CE、生成离散码AR CE | 文字NTP、图像masked-token prediction |
| 图像输出 | 384²/576码逐一生成 | 256²/256或512²/1024码，多轮整图并行掩码 |
| 条件引导 | lu+s(lc−lu)，示例s=5 | (1+w)lc−wlu，故同实际强度应s=w+1 |
| 实验边界 | 理解/静态图生成、encoder和单任务消融 | 理解/静态图生成、表示/数据/预训消融；GenHowTo关键帧和短视频定性扩展 |

“统一”可能分别指表示、骨干、输出词表或训练目标。解耦encoder仍可共享骨干；同一骨干也可有不同条件mask和loss。不能用模型名字代替可检验的结构假设。

## Janus：保留有冲突的消融，不只记录主表

[arXiv v1原文](https://arxiv.org/html/2410.13848v1)全部核心、五张表与AppA已读；[CVPR2025正式来源](https://openaccess.thecvf.com/content/CVPR2025/html/Wu_Janus_Decoupling_Visual_Encoding_for_Unified_Multimodal_Understanding_and_Generation_CVPR_2025_paper.html)页12966–12977，正式PDF选读§4.4/4.5及TV、实际看第7页。正式版GenEval/FID的TIII/TIV顺序与arXiv交换，引用时标版本；未称全正式版逐页读完。

Fig2/3/6实际看过。三阶段分别只训练adapter/head、再放开LLM、最后除生成encoder外全部放开含SigLIP。mmu:text:gen为1:0:1、2:3:5、7:3:10；“无额外任务loss权重”不能写成训练完全无任务加权。128×A10040GB约7天包含原Janus阶段，LLM/SigLIP/VQ上游训练另计。配置、数据与原始Janus分列，Janus-Pro/Flow不可混用。

TV的重要对照：

| 方案 | POPE | MMBench | SEED | MMMU | FID↓ |
| --- | --- | --- | --- | --- | --- |
| 共享VQ A | 60.1 | 35.0 | 34.9 | 24.7 | 8.72 |
| 共享语义蒸馏tokenizer B | 82.4 | 52.7 | 54.9 | 26.6 | 7.11 |
| 解耦Janus D | 87.0 | 69.4 | 63.7 | 30.5 | 8.53 |
| SigLIP理解单任务 E | 85.9 | 70.6 | 64.8 | 28.8 | — |
| VQ生成单任务 F | — | — | — | — | 8.92 |

D改善了相对A/B的理解，但B的FID更好；D相对E有两升两降，D/F的FID差.39没有CI。作者匹配每个任务训练步数，不能因此认定总FLOPs、上游预训、总参数和所有样本暴露完全一致。B额外语义decoder/teacher目标与D的理解encoder不同，构成机制与预算混杂。可写“改善此组理解/生成取舍”，不能写全面正迁移或解耦支配所有指标。

GQA48.7→59.1正文称30%提升；按原数为10.4绝对点、21.36%相对提升。正式版§4.4仍见同说法，记录冲突，不复述错误百分比。GenEval.61与旧Show-o.53是2024文献条件；Show-o v7后更新为.68/.69，跨版本排名须注明。

[官方README](https://github.com/deepseek-ai/Janus)选读原Janus安装/模型路径、完整生成函数及许可入口；新闻记录2024-10-20 tokenizer_config.json修复CFG为作者报告，未运行验证。代码MIT与模型DeepSeekModelLicense不同，完整法律条款未审；不从代码许可推模型许可。多语言prompt例子没有文字渲染/OCR/笔序专项数值，音频/EEG/3D和diffusion为未来方向。

## Show-o：必须纳入视频相关先例，限定它验证的范围

[v7原文](https://arxiv.org/html/2408.12528v7)与[ICLR2025元数据](https://openreview.net/forum?id=o6Ynz6OIQ6)分列，正式PDF未全文。已读核心§1–5/TI–TV、AppA–F/I/J/K文字和公式，AppB读过但未独立验证全部证明；G prompts/H视频未逐项。实际看Fig2/3/4/5/9；Fig8/12资源下载未完成，不计实际图像审阅。

§4.4在GenHowTo交错关键帧caption上微调，图内并行、帧块间AR。§4.5把MAGVIT-v2膨胀成video tokenizer：8fps下3×17×256²压成5×16²图码，展示短视频理解/生成。应将其纳入交错多模态/视频生成相关工作；所读仅定性例子，无FVD/VBench/严格笔画事件或视频文字质量量化，不能据此认定规范书写已解决，也不能删去视频扩展说它只研究静态图。

默认TI理解为2B/512²，TII FID9.24属35M模型，TIII v7GenEval.68/.69含不同CLIP变体，预算和variant必须分列。TV在35M/256²下CLIP shared-pretrain yes/no的POPE84.5/84.5、MME1182.7/1161.6、Flickr64.3/68.5、VQA-val71.9/73.5、GQA57.5/58.7、MMMU27.4/29.2：四项下降、一平、一升。MAGVIT连续分支六项上升，离散分支MMMU25.1/28.1下降。结论依赖表示和任务，不能宣称普遍协同。TIV与TV的VQA test-dev/val不同，也不能混列。

[原Show-o固定源码](https://github.com/showlab/Show-o/tree/45a5a2de01d1ebd10cd5864d29310a76476cdf23)读了model构造、forward和t2i_generate，stage1/2/3/demo配置全文；README选读。图像MTP不shift、文字与MMU CE各自shift；配置loss系数1/.1/1，三阶段步500K/1M/50K（最后注明按HQ量调整），lr1e−4/1e−4/2e−5、seed10086。mask schedule迭代每轮整图，CFG双流，temperature逐轮更新后送random-topk helper；helper内部未逐行，不附加未核机制。源码默认18轮与论文512²比较采用50轮分列，“1024/50≈20”是采样步骤比，不等实测端到端提速。

README指出RefinedWeb loader为内部实现，复现需自行替换；若按提示注释LM分支，训练目标就与原联合目标有差异。配置数据路径也是原内部绝对路径，不能把公开配置视作开箱即用的完整数据/训练复现。未读全部loader，不把perworker batch机械相加后断言论文全局batch错误。

## 附录公式：给出具体反例，明确影响范围

以下针对v7 HTML展示的符号，尚未核正式PDF是否修正，也没有独立验证整个AppB。

1. Eq6后以Markov为由写q(x[t−1]|x[t],x0)=q(x[t−1]|x[t])。一般Markov性质只给出正向q(x[t]|x[t−1],x0)=q(x[t]|x[t−1])，反向有额外初始观测通常会改变后验。解析反例：X0为均匀二元变量，两步各独立以.1概率翻转，则q(X1=1|X2=0,X0=0)=.01/(.81+.01)=1/82，而q(X1=1|X2=0)=.1。Eq6后验公式本身仍保留x0，不能由这句错误解释断定全部算法失效。
2. Eq8定义K个非MASK状态加1个MASK，ω=1−α−β、ν=β/(K+1)。展示矩阵每非MASK行的和为ω+Kν+α=1−β/(K+1)，β>0时小于1；如K=2、α=.2、β=.3，对应[.6,.1,.2]和为.9。需核均匀项分母/剩余概率的约定。正文实际采用纯mask β=0，此时行和恢复1；不能把未采用的uniform扩展问题直接当成实际MTP生成结果无效的证据。

AppK给出文字识别、新词生成与计数失败，作者解释数据不足，但该解释尚未排除分辨率/tokenizer上限与提示因素。把作者解释和因果证明分开，保留竞争假设。

## 研究假设和实验设计

对理解/生成任务，在同上游encoder、样本与参数/FLOPs下做encoder共享/解耦×骨干共享/分离×单/多任务；语义蒸馏基线必须保留。报告各任务Pareto、多seed区间以及tokenizer细字重建上限。生成方式用相同实际CFG系数、图码数量/分辨率、推理预算比较AR/离散masked/连续diffusion，实测延迟/显存/能耗；不以迭代数代替成本。

对书写视频，还需跨文字体系/字/作者留出，建立同终图而错序/缺笔/回擦的对照，分别测事件正确、RGB可见笔序与真实执行约束；把GenHowTo关键帧、渐进绘画与规则SVG纳入已有路线。上述实验均待执行。写作上学习“目标冲突→结构假设→受控表→具体消融→扩展范围”，Claim与Limitations同时写出取舍、未隔离因素和定性证据。
