# Tuna-2：像素flow、mask条件与完整主表

第一百二十批完成[L105](../reviews/L105.md)固定v2核心三遍与五项书面记录。[结构化证据](../../data/tuna2_pixel_flow_masking_and_release_audit_2026-10-22.json)。357目录（330论文／研究、27资源），229核心/232书面含未通过项，128条未确认核心（含资源）。没有新增目录、删除文件、下载权重或运行模型。

## 固定来源与阅读范围

[2604.24763v2](https://arxiv.org/abs/2604.24763v2)，2026-05-18，完整21页。Abstract/§1–5、Eq1–4、全部T1–6/F1–7图注已读，无附录研究节；参考文献未逐篇。实际核PDF p1架构/雷达、p5 mask、p6理解、p7生成/偏好/编辑、p8重建、p9比例、p10 mask/缩放、p11注意力。正式会场未核。

本作实验为静态图像理解、生成、编辑和另微调的重建。仓库中[L100原TUNA](../reviews/L100.md)的VAE视频路径已在116批核查，不构成Tuna-2像素视频或规范笔顺生成实证。

## 数据流与关键公式

原TUNA经VAE后SigLIP；Tuna-R去VAE但保留SigLIP2；Tuna-2用Conv2d16×16/RMSNorm直接把RGB patch送Qwen2.5-7B。512²图像有1024个patch，每patch768值映射3584维。独立视觉tower被移除，patch投影、LLM预训及16层图像flow head仍存在，不能称没有视觉参数或所有参数仅7B。

线性路径 $x_t=t x_1+(1-t)x_0$，模型预测clean图像 $x_\theta$，速度 $v_\theta=(x_\theta-x_t)/(1-t)$。因此速度误差平方等于 $(x_\theta-x_1)^2/(1-t)^2$；应保留时间加权，不能简写成无权重的原像素MSE。公开JiT实现用clamp(.05)截断分母、noise scale2，与纸面标准噪声/未截断记法有区别。t为flow噪声时间，无书写物理顺序含义。

mask把选定patch替换为learned token，理解仍回答原标签，生成预测全部clean patches。遮罩可作为正则，但文字信息被遮后可能不可辨；不能保证恢复唯一真值。patch扩维也不保证投影满秩或整个预测链无损。

## 六张表的结果和反例

| 表 | 核读结果与条件 |
| --- | --- |
| T1理解 | Tuna-2十二项65/67.7/51.7/50.7/77.3/61.1/79.6/85.6/79.7/59.2/81.7/28.8；相对R九升、RW67.7<67.9/MMMU50.7<51.1、Chart同85.6，原Tuna Chart85.8更高。OneCat MMVet52.2/SEED61.6/V*63.4、QwenVL MMMU58.6/OCR83.7等反例，不能泛称全任务SOTA |
| T2生成 | 原Tuna/R/2的GenEval .90/.88/.87，DPG86.76/86.35/86.54。2的DPG高于R，应修饰正文R始终更好的概括；2的计数.80/位置.84/颜色属性.76低于R .82/.86/.79。†改写条件需匹配 |
| T3偏好 | GPT质量22.3/35.7/32.1合计90.1%，剩余9.9%原文未解释，保留原数，不归一化/虚构平票。Claude质量28.1/37.2/34.8。多样性GPT20.6/30.9/48.4、Claude28.2/29.9/41.9，支持2的相对多样性，质量仍偏R |
| T4编辑 | 总分4.31/4.18/4.09；Tuna-2九类4.34/4.13/2.22/4.53/4.42/4.36/4.58/3.91/4.28，只有style4.58高于R4.54，其他八类下降。QwenImage4.27/GPTImage4.20更高 |
| T5重建 | **另经微调**：R512 rFID .12/PSNR32.22/SSIM .93，2为.15/32.80/.93，同512 FLUXVAE .06/33.65/.93更好/同。其他原生256/384混列，不是同预算codec零样本比较 |
| T6 mask | 1.5B共享50K后各分支50K。R四项58.3/56.7/57.2/55.7→59.2/58/58.2/56；2 55.4/52.3/53.4/47.6→56.8/55.7/57.6/48.2。支持此配置小规模增益，2生成仍低于R无mask55.7，未给主7B同控制或多seedCI |

F5测试生成:理解3:7/5:5/7:3/7.5:2.5/8:2约11K步，CE/MSE会随各任务曝光变化；7:3折中未定义独立效用函数或全评测最优。F6横轴训练tokens至3T，R理解前期较强、2后期在OCR/MMVP/V*超过，R GenEval始终更高；不同额外encoder/对齐成本及每token计算未匹配，不构成完整计算优势或普适缩放律。F7四个精选attention示例无反事实答案、遮挡干预、统计定位或head/layer聚合协议，不能证明因果推理。

## 训练、数据与公开代码

550M内部图文对，caption:T2I=30:70；Nemotron纯文字占总预训数据20%，比例分母不同。主预训300K步/64nodes/lr1e-4，SFT50K/lr2e-5，每GPU pad16Ktoken。FineVision约13M对话、OmniEdit约2M和精选生成数据，后者数量、GPU型号/每node卡数/globalbatch、总卡时/全部分辨率/多seed未齐。R另3K connector-only alignment lr5e-4。重建微调配方未齐。LLM偏好1500 prompts、每模型每prompt4图，提示源/顺序盲法/票数协议需补。

固定[GH b53594e3](https://github.com/facebookresearch/tuna-2/tree/b53594e308095b573c31be46f24ea62936f3c440)完整2142项树，README全文及子README有关发布/参数；模型/预测/训练配置、patch_embed、_wrapper_base、jit_utils全文；模型初始化/forward/prepare与R视觉/mask路径、train.yaml核心、lmms加载/生成路径选读，两个模型评测配置及shell全文。未全读vendored评测库或全仓代码。

公开Tuna2模型配置mask min−.7/max.3，代码对int(N*r)≤0跳过，约30%样本mask且正比例≤30%；R模型默认maskfalse。论文训练为最后40%步中50%样本、U(0,.5)。需外部override/运行记录解释差异；不能把公开默认当成论文实际配方。评测配置关闭mask与输入噪声属于评测设置，不据此判错。

train.yaml示例T2I/edit/MMU/text=.5/.2/.2/.1、maxsteps1M，没有完整复原300K+50K的内部数据阶段。默认Euler50/CFG7.5/shift3、noise scale2、flow/ntp权重等均为文件默认，主表逐项使用情况另核。评测存在noneencoder/R/VAE三个适配器，noneencoder真实加载Tuna2PixelModel、脚本bf16/batch1；不能声称仅有R适配。

root README权重TODO/production不可释与子README released/reinit表述有差异。所读链接没有定位可验证官方Tuna2 checkpoint；HF广泛关键词搜索包含大量无关项，也不能据此宣称全站不存在。未下载权重/执行模型，所以代码条件差异属于静态核查。

## 假设、实验与写作学习

优势条件是足够联合训练预算、局部细节对标签有用、mask后仍可辨；SigLIP先验在低预算或高质量生成/编辑上仍可能有价值。应计入LLM/SigLIP/VAE上游预训、Ralignment、全部tokens/FLOPs/卡时，固定数据/曝光/分辨率/NFE和改写，比较质量-成本Pareto。论文mask、公开默认和无mask跨预算/规模比较，报告7B、多seedCI和被遮标签可辨性；重建匹配额外微调。偏好公开原票/无效票/顺序，注意力加遮挡反事实与答案统计。多语言生成字串、局部笔画拓扑、真实事件视频分别验证。上述建议未运行，创新性仍需检索。

Introduction逐级移除VAE/tower的问题组织、Method从clean预测到mask、三系统完整表与小模型受控消融值得学习。Claim需保留各任务退步、DPG反例、重建微调、token口径和90.1%悬项；不能把attention示例或OCR理解写成严格文字/笔顺生成证明。原文无独立Limitations节，读者应补私有数据/完整成本、遮罩不可辨性、公开权重与实际训练override、统计波动以及视频未测。
