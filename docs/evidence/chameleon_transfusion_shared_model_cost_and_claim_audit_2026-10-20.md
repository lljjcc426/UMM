# Chameleon与Transfusion：共享成本与Claim核查，第五十五批

补完原目录[U01](../reviews/U01.md)、[U05](../reviews/U05.md)的核心书面三遍。目录仍347项＝321研究＋26资源，核心三遍124、五条书面检查126；本批无新增独立研究、无删除、训练或独立复现。Janus/Show-o已取原文，后续继续，未提前登记完成。

## 两条路线的具体差别

| 项目 | Chameleon 2405.09818v2 | Transfusion 2408.11039v1 |
| --- | --- | --- |
| 问题 | 早融合图文交错在大规模下稳定训练及对齐 | 连续图像+离散文字共享模型的效率/表征/目标 |
| 表示 | 512²图→1024离散码、8192码本；BPE总65536 | 256²图→32²×8连续VAE潜图，再linear/U-Net patch |
| 核心 | 同一因果Transformer，统一AR token CE | 同一Transformer，图内双向/其他因果，文字CE+5图像噪声MSE |
| 稳定/适配 | QKnorm、输出zloss、支路norm重排，规模依赖dropout，SFT模态平衡 | 模态输入输出小层，caption在前80%；图先时可限制噪声t≤500 |
| 验证 | 多任务表、真实稳定性消融及1048人评 | 同recipe重训离散基线、参数/数据/6ND proxy曲线、mask/patch/外围/noise消融 |
| 范围 | 静态图文交错，无规范笔序或视频验证 | 静态图文和8K样例编辑SFT，无规范书写过程验证 |

核心图均实际视觉：Chameleon Fig1和Fig8/12全部子图；Transfusion Fig1/3/4及Fig5 FID/CIDEr曲线。前者依然使用图像tokenizer/detokenizer，不能因“统一”写成完全无模态编解码；后者VAE与裁图仍可能损失信息，避免额外量化不等像素无损。图内双向mask也不自动适用有因果事件要求的整段书写视频。

## Chameleon的数字与人评边界

[原文v2](https://arxiv.org/html/2405.09818v2)TI列4.4T数据、2.1epoch，正文约9.2T训练见过token；不能混为4.4T训练总量。§2.2三项2.9T文字+1.5T图文+.4T交错合计4.8T，尚未取得与TI4.4T的去重/加权解释，保留原口径。7B/34B为1024/3072 A10080GB、856481/4282407 GPUh；与其他文本模型数据量和预算不等。

QKnorm作用于attention softmax输入；1e−5(log Z)^2作用于输出softmax分区。34B支路attention/FFN之后norm再加残差；7B recipe使用dropout.1，34B不用，SFT dropout.05。实际Fig8的QKnorm单消融短程loss略差，图中未呈现单独爆炸；作者正文另称约20%epoch发散。输出norm组合消融与34B重排图支持规模/recipe依赖的不稳定，不能把所有曲线概括为“移掉任意组件必然立即发散”。

TVII预训34B COCO120.2/Flickr74.7/VQA66.0均2-shot；任务特定SFT COCO140.8为0-shot，MultiTask139.1/76.2/69.6。不同训练/shot分列。文本MMLU65.8低于Llama2-70B68.9，不能说全部领先。

1048人评prompt全部筛成期望图文交错输出，其中441图文输入、607纯文字输入；无OCR/图表。原GPT4V/Gemini只出文字，带加号版本经其caption交DALL-E3生成图，故比较的是异构系统。三标注多数、随机顺序、无一致平局；任务完成度α=.338、95%CI[.319,.356]；对Gemini+/GPT4V+相对α=.337/.396。

具体复算：附录TXI总435胜、362平、251负，按win+.5tie为616/1048=58.7786%，四舍五入58.8%；正文/Intro的60.4%对应混合输入子集(194+72.5)/441=60.4308%，不能写为总体。GPT4V+总体51.6%，混合输入子集47.3%；原版Gemini/GPT4V总体69.1/61.7。原图Fig21胜平负为41.5/34.5/24，与58.8对应。保留原表与正文差异，不静默替作者修改研究结果。

[官方仓库README](https://github.com/facebookresearch/chameleon)全文核推理代码、viewer、评测prompt、申请模型与研究许可入口；HF7B卡返回401，未读，不猜当前发布权重是否具备论文全部生成能力。未获取完整训练loop、全量数据或运行权重。

## Transfusion哪些实验支持哪些结论

[v1原文](https://arxiv.org/html/2408.11039v1)精读与[ICLR2025正式元数据](https://openreview.net/forum?id=SI2hI0frk6)分列；正式PDF未逐页比对。常规.5T为图/文token1:1，380M Shutterstock与Llama2语料。最大2T加入公开无人物图、人物上采样、CC12M，形成每epoch692M混合、约3.5B图文暴露；这些不全是独立唯一Shutterstock图。Transformer从头训练；VAE86M另训，AppA为L1/LPIPS/GAN/MoCo-perceptual+1e−6KL，50K后开GAN，非纯ELBO。

TIII同.5T的7B连续/离散：C4 7.72/8.41、Llama准确61.5/59.1、CIDEr27.2/18.0、FID16.8/29.6。理论FLOP proxy为6ND；拟合FID parity .029≈34倍、caption .218。作者还对弱离散点设拟合筛选门槛，图显示有限范围内曲线间距；没有实测训练/推理34倍提速，也未证明普遍缩放指数定律。实际注意力、VAE/U-Net、250步去噪/CFG与部署硬件成本须另测。

TIV .76B纯文字准确53.7，加入diffusion为51.7；离散稳定修改51.9、再加图token48.9。支持相对代价较小，未证明共享学习超过纯文字基线。竞争输出词表/参数分配为作者假说，尚无唯一因果证明。

TV线性因果→图内双向，FID61.3→20.3；U-Net16.8→16.7，因其内部已有双向attention。TVI U-Net256/64/16位置FID16.7/16.0/16.1，但文字准确51.9/50.7/49.2，且固定token预算使大patch看更多图。TVII7B加U-Net仅多3.8%参数仍改善caption27.2→33.7/FID18.6→16.0，支持外围归纳偏置，仍缺完全等参和等图像暴露因子。TVIII图先时t≤500令.76B CIDEr25.4→29.4、7B33.7→35.2，支持减少作为条件图的破坏。TV/VI准确率箭头误为↓，数值意义应↑。

控制CFG5、结构消融CFG3、最大按benchmark调；结构5K FID/主表30K分列。TIX最大7.3B/2T FID6.78、GenEval.63，SD3为.68；文献模型数据、caption、分辨/重排不同。编辑仅8K SFT后随机例观察，无完整定量成功率。不能把这些结果写成全模态最优或已验证视频/笔序。

## 我们应如何检验共享收益

先验证tokenizer对细字、局部笔画和同终图不同过程的可辨上限，再做共享/分离/部分共享×单任务/多任务。分别控制实际样本暴露与实测总FLOPs，计入外围编码器、VAE、attention和推理步骤；patch×图像数×外围等参、条件图噪声×损失权重全因子。按文字体系/作者/字/生成器留出，报文本理解、事件正确、生成质量和成本的Pareto及多seed区间。

写作可学习“定义共享对象→受控比较→组件因果消融→扩展任务”的顺序。Claim须区分联合可用、负迁移较小、正迁移；Limitations写清重建上限、筛选、预算/shot差异和仅定性证据。上述新实验均未执行，全部剩余精读继续。
