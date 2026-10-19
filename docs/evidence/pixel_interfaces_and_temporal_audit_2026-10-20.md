# 像素接口、连续表示与真实时间：第十三批审查

2026-10-20；L101–L108指定方法、实验及附录阅读。新增8份笔记，累计218份；主目录332条中章节232、摘要33、历史待核67。HYDRA补五项书面检查，累计6项；全部文献的完整三遍精读仍未完成，未运行模型。本批未删除文件。

## 任务与输出的边界

| 记录 | 真实接口与本次已核贡献 | 对文字/书写研究的限制 |
| --- | --- | --- |
| [UniWeTok/L101](../reviews/L101.md) | 128bit组量化、PPD/GAP、混合骨干；静态图像 | 2^128为隐式组合空间；64位置不代表只64个普通离散符号，usage定义需核 |
| [EvoTok/L102](../reviews/L102.md) | 前4残差层重建、全16层语义；独立方向训练入口 | 深度序列没有真实时间标签；13M指tokenizer，合成数据和语义教师仍存在 |
| [HYDRA/L103](../reviews/L103.md) | GenViT/GSB/SemViT和共享Qwen双head | 连续64维仍有压缩；联合曝光/计算和缩放重建协议需控制 |
| [UniCom/L104](../reviews/L104.md) | 预测压缩连续语义，扩散decoder渲染 | 最终decoder调用FluxVAE；纯压缩OCR明显下降，默认理解还用原始特征 |
| [Tuna-2/L105](../reviews/L105.md) | encoderfree像素patch、mask辅助学习 | 大规模内部预训；编辑与部分理解指标退化，无实测视频协议 |
| [RF/L106](../reviews/L106.md) | 先AR结构表示，再像素flow | 保留独立理解encoder/EMA/VQ；Doc/Chart退化；伪码需实现核查 |
| [Hydra-X/L107](../reviews/L107.md) | 局部causal/分级时间压缩、双teacher、源目标SemViT交互 | 17帧；没有长视频/视频编辑；×4压缩可能影响短笔画事件 |
| [PixelUMM/L108](../reviews/L108.md) | 线性像素/时空tubelet、MoT、96帧视频 | 两expert含独立参数，主checkpoint仍有linearpatch边界问题；通用QA不衡量笔顺 |

## 沿源码核查“无VAE”的作用范围

[UniCom官方revision55b9001](https://github.com/Tencent-Hunyuan/UniCom/tree/55b9001a0fee623528676d995d8945fd6db7e23e)的README列出主模型、decoder transformer、Flux VAE和SigLIP2四组件；[HF模型卡](https://huggingface.co/tencent/Unicom-Unified-Multimodal-Modeling-via-Compressed-Continuous-Semantic-Representations)也明确写decoder-side Flux VAE required at inference time。

`UniCom_Decoder/runtime.py`第395行导入FluxAutoencoderKL，第413行加载并冻结；`_decode_latents`第368行调用`vae.decode`。主pipeline将该VAE路径传入decoder配置。由这些实际调用可确认：主模型生成目标为语义特征，最终成图仍依赖VAE。论文“without relying on VAE”不能扩展为整个推理路径没有VAE。

相邻Tuna-2、PixelUMM直接预测像素，RF直接像素生成但保留理解encoder和离散中间表示。架构比较应分别列出输入表示、预测目标、条件路径、最终解码及预训练依赖，不能只贴统一或无encoder标签。

[HYDRA ca3e71d](https://github.com/Tencent-Hunyuan/HYdra/tree/ca3e71d9356dee02cc13ac6cc02a73090e40f781)与[模型卡](https://huggingface.co/Xuerui123/HYdra)说明checkpoint、tokenizer和latentstats的组合，实际模型先调用und_vit(SemViT)再semantic_proj。PDF第4页Fig3视觉核查吻合该通路。公开阶段数据路径是模板，完整权重可见不代表实际数据配方可重建。GenEval的1.5B50步、7B200步也要计入成本。

[EvoTok147b1b2](https://github.com/VisionXLab/EvoTok/tree/147b1b2aaac32bb28c5eb246e2a4a04c3e80041c)tokenizer脚本明确VQGAN_DEPTH4、VQKD_DEPTH16、32768码与500K步；理解和生成分别有训练入口。当前未核到一个checkpoint在匹配联合训练下的协同实验，不能据两个方向主成绩认定共享训练正迁移。

## 负迁移与数表反例

- UniWeTok Table1加GAP改善gFID2.66→2.35，同时rFID1.12→1.18、SSIM.65→.63变差；Table5有query2.38与Table1数值不同，保留口径疑问。
- UniCom Table5 OCRBench55.40→MHA压缩36.00，原特征sequenceconcat回55.50，但额外保留原特征并增加上下文。MHA优于MLP不证明压缩无损。
- Tuna-R→Tuna-2 OCR78.3→79.7，MMMU51.1→50.7，ImgEdit4.18→4.09；原Tuna编辑4.31。优势依任务/数据规模。
- RF Pixel+RF六项理解改善，DocVQA−2.0、ChartQA−.4。256的GenEval.25→.76包含表示预测expert/AR步骤成本，不能单独归因离散码“本质更优”。
- Hydra-X Table1分级压缩rFVD13.69→11.19、单次延迟.17→.25秒；质量与延迟需共同报告。STI视频VideoMME持平，source重建PSNR不等于编辑target未改区保真。

这些是作者原表在指定条件下的结果。对公式、指标解释和预算的质疑属于本仓库分析，未据此断言作者代码或全部实验无效。

## 在线量化与公式呈现

RF PDF第16页Algorithm1已渲染核对，伪码确实先softmax(dim=1)，再softmax(dim=0)。这与对同一非负矩阵做标准Sinkhorn交替行列缩放不同；第二次softmax又对第一次概率取指数。单轮后hardargmax也不保证各prototype得到相同样本数。伪码中的scatterindex扩为K而feature维为D，还需实际实现澄清。本次未读取该工作运行代码，没有把呈现问题当成实测失败。

UniWeTok的SigLu等于−tanh(x/2)，限定输出范围不能单独推出tokenentropy与commitment两个损失数值、梯度等价。2^128的100%usage不能解作有限验证集遍历全部128bit组合；应先核作者按bit、组码或整码如何定义。

HYDRA正文噪声写H_bn+tε，所读公开ICPlan按t*x1+(1−t)*x0构造。记录式子/实现差异，实际训练选择和标准化流程仍须继续核查。

## 四种“顺序”需要分别建模

1. 图像残差量化深度：同一静态图像不同层级的信息分配。
2. 扩散/flow时间：从噪声到样本的求解参数。
3. 时空patch：多帧数值被折叠成一个输入单元。
4. 实际书写事件：笔画身份、先后、方向、落笔/抬笔及其RGB可观察结果。

EvoTok前两类表示不能直接提供第4类真值。Hydra-X/PixelUMM时间×4也不必然删除所有4帧内信息，但是否可恢复短事件必须实测，不能只从压缩倍数推定丢失。应构造最终字形相同而事件相反的样例，按1–4帧短笔、速度、遮挡和最小笔形差分层。

## 学习实验组织与Claim的条件限定

PixelUMM F4主动说明不同像素/latent空间MSE不能直接比较学习速度；F5的3×为步数收敛，F6增加GPU后的9×也未证明墙钟或算力效率。F8在同checkpoint比较4fps/t4与1fps独立帧：MV+.07、VideoMME−.22、Long−.68、LV0，只支持通用QA中未见一致收益，不能推广成书写不需要高帧率。

后续实验同时给两种对照：等样本曝光和等总计算。保持teacher、初始化、分辨率、有效bits与decoder一致，额外AR序列、采样NFE和预训练外部模型都计入成本。理解/OCR、终态字形、真实事件、编辑未改区、视频质量与人评分别测量。

写作可学习Tuna-R中间架构阶梯、RF的Pixel/VAE×有无RF四格实验、Hydra-X两轴重建消融，以及PixelUMM明确编号和条件的八组研究。Introduction提出具体可检验不足；Method解释输入输出及训练/推理差别；Claim写明分布、尺度和比较对象；Limitations保留退化项、数据不可得及未测时间任务。
