# 原生像素、潜空间代理与机器人书写前史

2026-10-20。存量U26–U31六项、正式新论文L186与存量N08、一项无独立论文适配器R08；七字段、五个核心问题及写作学习详见[逐篇目录](../reviews/README.md)。四份五项书面理解检查新增，累计26；完整三遍及复现未完成。无删除文件。

## 各方法在生成什么

| 工作 | 真实接口 | 条件与证据边界 |
| --- | --- | --- |
| SenseNova-U1.5 | 像素FM/文字AR，MoT共享attention、分支独立参数 | 无外部ViT/VAE仍有卷积接口和空间head；文字/图序列不证明笔顺视频 |
| UniModel | RGB与文字绘制图双向扩散 | 固定字体512²、长文截断；只给定性展示，无标准主分数 |
| LatentUMM | 后训练隐表示映射/一致性代理 | 原公式固定φ与代码可训练映射不同；指定task/pref loss未执行RGB回环 |
| MIRROR | 工具定位/覆盖视觉标记，再读原图回答 | Molmo/SAM依赖，归为工具反思；没有新场景图生成器 |
| LatentUM | 语义离散码与文字AR，可选DiT转像素 | 直接理解图码，最终RGB仍可能不同；导航当前实现是像素回环 |
| DIVA | caption与inpainting双flow后训练 | shared/unique因素对齐，信息分解依假设，主表/消融数值待澄清 |
| G-HTR | 字图→宽度/penstate轨迹→外部brush控制 | 正式CVPR2026，带宽轨迹和机器人强直接前史 |
| 层级O2O | 字图+双域先验→M/L向量命令 | 正式Springer2026，已含书写动力学与同形恒速control |

## 不能沿用的泛化Claim

[SenseNova-U1.5 v1](https://arxiv.org/pdf/2609.11929v1) Table11总体CVTG.948高U1.940，但二/三区域低于U1；Table8/9 OneIG整体也非全部模型最高。Table2 SFT比例.3/.4/.3/.1合计1.1，来源未解释是否权重、误写或其他口径；本次保留，不自行归一或断言训练配置错误。四专家OCR用中英multisetIoU，不直接惩罚所有文字排列错误；准确字符串和版式仍需独立评。架构/数据/RL/蒸馏同时改变，主表不足归因单组件。

[UniModel v1](https://arxiv.org/pdf/2511.16917v1) §4.2明确没有标准量化比较。可读caption样例和循环推理不等同VQA基准成绩或cycle loss训练。训练数据、lr/batch/硬件仍缺充分可核配置，相关栏保留未核，不从QwenImage底座移植答案。

[DIVA v1](https://arxiv.org/pdf/2605.25328v1) Table1/3 Showo GenEval base/full=.57/.64；Table2/4同名行=.69/.75。附录训练又称Showo8B，主表1.5B。存在未解释差异时，不能拼成一套确定结果。NexusGen MMMU43.5→49.4和选定去unique/stopgrad行可分别引用。Eq4的shared/unique分解不自动可识别；低互信息也可能来自因子塌缩，需信息保留干预。

## LatentUMM：公式与实现分别审

[原文](https://arxiv.org/pdf/2605.17766v1) Eq1的φ=固定外部E*，若仅对固定训练配对计算距离，则对UMM参数梯度为0。这个条件判断针对所写公式，不等于对实验有效性作结论。同维向量还不能据此证明坐标几何相同。

公开[TorchUMM固定版本](https://github.com/AIFrontierLab/TorchUMM/tree/425efa19cb2a18d43278d4d222ed238b5e244546/src/umm/post_training/LatentUMM)包含可训练aligner/MLP，BAGEL `modeling/bagel/bagel.py`374–412的modal约束经过hidden_to_embed、task经过hidden_to_embed→embed_to_hidden，pref在加噪hidden的代理往返上计算cosine间隔；另有GTembedding回归。此实现有相应可训练路径，所读辅助loss没有生成RGB再调用外部embedding。其他RIR支路存在，尚未全审，不能用局部读码断言整个系统绝不做图像rollout。

AppC r16/α32/λtask.09/pref.06与公开stage2脚本r64/α128/.01/.001不同；CLI允许覆盖，故记录配置差异并待核。论文RecA MathVista overall51.6小于MC79.81与free64.57，若为同总体子集加权聚合则不成立；具体协议需核，不擅改。后续实验要比较真实RGB闭环、MLP代理和同预算SFT，并同时测平均质量/最差质量/多样性。

## 交错推理的成本与数据量

[MIRROR v3](https://arxiv.org/pdf/2602.18746v3) Table6支持训练+工具+loop共同收益，AppTable11 MMVet2.81→3.73秒、token85.50→112.58。需要等延迟反思/重采样、错误/正确定位干预。上游漏检与密集标记遮挡是可检验局限，不能凭attention图认为已建立因果机制。

[LatentUM v1](https://arxiv.org/pdf/2604.02097v1) Table2自奖励.85→.87但颜色子项下降，pixelreward.92又使用外部评价。Table4 fine.99对应18K训练，coarse.85是6K；差值不能只归因语义码或交错粒度。§4.4导航实现明确解码像素再编码上下文，不能称现有全部世界模型rollout完全避开像素。自奖励仅读语义码，应测相同码经随机decoder后的像素是否仍满足题目。

## 必须加入的书写直接前史

[G-HTR正式CVPR2026](https://openaccess.thecvf.com/content/CVPR2026/html/Qin_Towards_Human-Like_Robot_Handwriting_via_Contour-Aware_Generation_CVPR_2026_paper.html)提出CHTR并构建110540配对，训练88169/测试22371，合计9837类/1080style。静态来源是Founder和CASIAHWDB；stroke detector+标准组成匹配决定笔序，CNNLSTM提取宽度轨迹后人工纠错。标签渲染mIoU.972证明轮廓一致性，未证明恢复原作者真实动作或速度。Table4宽度适配对TrajFormer帮助很大，应使用适配版强基线。

Table3全test DTW18.277→12.765、LPIPS.092→.066，按所列值计算约降30.16%/28.26%，正文写27.69%/22.83%。保留表值和计算差异，不借此否定其余结果。Table6多尺度图与主文稀有字笔序失败均已记录。机器人控制借前人brushmodel/RL链；宽度尚非真实压力传感。固定[官方仓库](https://github.com/RittoQin/CHTR/tree/98e6b16756dc61d70e2c3e6c9c6097b206b1eb70)树只含README，正文“code/data available”尚不能视作实际取得，supp zip与控制细节待读。

[Hierarchical O2O正式论文](https://link.springer.com/article/10.1007/s44443-026-01050-5)与L006同作者不同DOI/问题，不合并。CASIA真实轨迹+字体伪轨迹，ICDAR2013独立评测；Sw仅起点/笔数/长度，不能替代全笔序。它已有速度—曲率JSD/幂律/对齐相关和同形恒速control：Table7 fullJSD.071/r.84，恒速.246/.19，去motionprior.122/.70。所读先验使用重采样近似速度，真实Δt/时间单位需核后才可解释物理速度。不能遗漏这组已存在的动力学实验。期刊已正式发表，SCI分区年份/类别尚未核实。

## 无独立论文资源：R08

官方[HF LoRAs固定版本](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT-LoRAs/tree/f33b8fe0216e6f10e5aed58ebbfdd05f02826732)实际含8step/V2两权重与中英卡，无adapter_config。卡声明Apache2.0、final底座、不兼容Preview；未下载权重tensor，rank/targets不能猜。V2色彩/过锐改善尚无独立数表，不继承U26全榜分数。

[加载代码](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/src/sensenova_u1/utils/lora.py)以strength×alpha/rank合并up@down；[旧蒸馏说明](https://github.com/OpenSenseNova/SenseNova-U1/blob/c35c83b58ef6e238a08b986aa58f3b73303aa42f/docs/base_vs_distill.md)称旧8step训于SFT、final兼容未必最佳，不能跨版本断言V2同训练。50步CFG4与8步CFG1改变网络次数，100NFE/8NFE的标题不等真实加速比例。官方training文档明确U1及U1.5生成PT，仍不能据此认定V2蒸馏和完整U1.5RL/OPD公开。按静态中英文字/编辑、具体基础权重和推荐参数纳入资源基线。
