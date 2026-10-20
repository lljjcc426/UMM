# Versatile Diffusion 与 Emu：共享机制、完整主表和实际公开协议

第七十八批补完[L075](../reviews/L075.md)、[L077](../reviews/L077.md)明确范围的核心三遍与五项书面检查。主目录350条，166项核心三遍/169项五条书面记录（含未通过项），184条尚未确认核心三遍（含资源）。无新增独立论文、文件删除或模型复现。

## 正式来源和任务边界

| 工作 | 采用的原始版本 | 实际输入输出 |
| --- | --- | --- |
| Versatile Diffusion | [ICCV2023正式题录](https://openaccess.thecvf.com/content/ICCV2023/html/Xu_Versatile_Diffusion_Text_Images_and_Variations_All_in_One_Diffusion_ICCV_2023_paper.html)、[正文](https://openaccess.thecvf.com/content/ICCV2023/papers/Xu_Versatile_Diffusion_Text_Images_and_Variations_All_in_One_Diffusion_ICCV_2023_paper.pdf)、[补充](https://openaccess.thecvf.com/content/ICCV2023/supplemental/Xu_Versatile_Diffusion_Text_ICCV_2023_supplemental.pdf) | 图或文条件→静态图像/句子；四flow及多条件派生应用。视频/音频/3D为扩展方向 |
| Emu | [ICLR2024正式题录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/34d5143080c89a7ce10932c8c5e1907f-Abstract-Conference.html)、[正式PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/34d5143080c89a7ce10932c8c5e1907f-Paper-Conference.pdf) | 交错图文/视频帧输入→文字或静态图像；未做连续视频输出实验 |

两篇均未给规范笔顺事件或机器人可执行书写输出。VD的扩散步和Emu的causal latent次序都不能直接解释为真实绘画时间。

## VD：模块共享的贡献与证据强度

UNet分global时间层、按输出选择的data残差层和按条件选择的context crossattention。AutoKL图像latent与Optimus整句768维latent分别去噪，四flow梯度累积更新；不同模态仍有不同VAE、CLIP编码器和data层。实际p7757 F2/7758 F3–4、Alg1与p7760结果已核。

| 正式结果 | 数值 | 可以支持的结论 |
| --- | --- | --- |
| F6文生图FID | SD11.21±.03→VD11.10±.09 | 改善.11；±定义/重复次数不明，不能据此报告显著性 |
| F6图像variation FID | 18.81±.06→4.57±.02 | 图像边缘分布改善较大；仍需测输入条件保真 |
| 图生文字/文字variation | 正文F5及补表定性样例 | 无全任务定量主表，附录承认重复词句/长句问题 |
| 多条件/PCA/VD-Alt | 主要定性比较 | 展示可操作性，未隔离共享机制、额外训练、数据和梯度调参的因果作用 |

从SD1.4继续1→2→4flow，每阶段256²30M再512²6.4M样本；不能把全部成本写成从零36.4M。批大小/学习率/梯度尺度也随阶段改变；O(max(N,M))模块增长与O(NM)独立模型比较不等于实际同预算收益。CLIP局部主成分保留/移除经验控制style/semantic，未证明这两因素独立或可识别。

正式Eq1把边缘分布写成整个路径条件密度乘积，barαt的乘积上界也写T；标准写法需区分路径联合与对中间状态积分、上界t。这些记号疑点不能自动推成训练实现错误。

## VD：论文、固定代码与当前制品差异

[固定官方代码cf0f4a2b](https://github.com/SHI-Labs/Versatile-Diffusion/tree/cf0f4a2bc426a0567c672e4ab3dfbf61af0e265c)与[HF2926f8e1](https://huggingface.co/shi-labs/versatile-diffusion/tree/2926f8e11ea526b562cd592b099fcf9c2985d0b7)的指定文件审查见[制品JSON](../../data/versatile_diffusion_and_emu_artifact_audit_2026-10-21.json)。本批仅静态阅读：

- 正文β_start=8.5×10⁻⁵，配置`vd.yaml`为8.5×10⁻⁴；`diffusion_utils.py`名为linear的分支先线性插值平方根再平方，也需与“β线性”表述分开。
- `vd.py/p_losses`计算加权VLB用于日志，返回的默认目标为simple ε-MSE；未取得原FID/训练提交，不能把此版本差异写成原实验必然有误。
- `app.py`默认DDIM50步/eta0/CFG7.5，图variation用全零embedding作空条件，图生文字用黑图CLIP；文字还会做重复词后处理。示例配置不等于论文FID协议。
- README称I2T2I暂下线，HF保留deprecated和现用权重。ControlNet附录示例需先移除CLIP位置嵌入并额外微调CLIP-PA；不可写原四flow直接零训练接入。

Optimus单句向量丢词序/长句和训练域到网页caption的偏移有作者明确论述。对局部笔形、OCR与多语言序列的迁移需另测；只看FID/CLIP不足。

## Emu：全图causal表示、外部解码器与完整退步项

EVA-CLIP1B、12层Causal Transformer和LLaMA13B构成标称14B主体，文字CE/视觉L2交错AR；冻结主体另调SD1.5 UNet生成图像。14B不含所有外部解码部署参数。Causal Transformer的query虽用causal selfattention，仍cross-attend全图EVA特征；无法由此恢复实际笔画先后。

| 正式表及条件 | 结果与反例 |
| --- | --- |
| T1 Emu无星号 vs Flamingo9B* | COCO112.4较高；OKVQA38.2<44.7、VisDial47.4<48、MSVD18.8<30.2、MSRVTT8.3<13.7、NExT19.6<23。prompt条件不同须保留 |
| T1 Emu*两个文字示范 | OKVQA42.8仍<44.7、VisDial47.8<48；视频34.3/17.8/23.4改善。星号不能省略 |
| T1 SFT前后无星号 | VizWiz34.2→32.2、VisDial47.4→43、NExT19.6→5.8下降；同星号NExT23.4→19.9也下降 |
| T2 COCO FID | Emu11.66优于GILL12.20，弱于SD1.5 9.93；同PNDM50步但各自CFG5/3调优 |
| T3/4 | 8shot MSVD39.8<Flamingo40.8；MMVet总36.3±.3高于LLaVA35.5±.3，但OCR19.2<28.2/Spatial25.2<33/Math3.8<15。±是5次评估，非独立训练 |

T11另列CM3Leon/AnyMAL及Emu-I，不能从跨配置每列取最好宣称同一个base全面领先。NExTQA为WUPS、VisDial为NDCG，不能统称同一种accuracy。Eq1将log条件和写≈p(x)也存在概率与log似然口径问题；原图到语义latent未给可逆变换或原像素ELBO推导，L2的作用应按实际视觉预测目标解释。

## 视频数据消融与公开复现材料

YT-Storyboard来自18M视频的约1.8B缩略图与字幕，按时间交错，非1.8B原视频。随机8帧/224²不保证细笔事件可观测。正式AppA T6是7B小模型，先原数据7.2K步再加YT2.4K：COCO110.8→112.9、MSVD30.2→30.8、MSRVTT16.9→17.9，但OKVQA43.9→42.3下降；视频/图文对照应补等额外训练预算。

主预训128A10080GB10K步；SD decoder另32A10040GB15K步、b1600、LAIONCOCO:aesthetics7:2；Emu-I另16A10080GB16h，selfattention LoRA r/alpha16。完整优化器/学习率/数据配比和评估模板见单篇七字段。RICES从5000训练候选池检索，query视频8帧/support2帧，CoT、VizWiz拒答和答案清洗都是协议。

[官方固定d9f12f43](https://github.com/baaivision/Emu/tree/d9f12f431a4ea8219bd80ed2aa3173b7fa26fb12/Emu1)与[HF9d5face1](https://huggingface.co/BAAI/Emu/tree/9d5face1ae9d8f5cd5c0ed891dc09e47833d06e1)的资源审查补出：

- 已有推理/评价/权重及YT采集处理配方；README预训练/SFT代码仍未勾选。下载/处理脚本不等于完整媒体托管与原训练可复算。
- `image_inference.py`明确assert `instruct=False`，不能直接承诺Emu-I支持该图像decoder。
- `Emu-14B.json`为32个causal latent，`generate_image`逐步重算前缀，该函数未传复用pastKV；未实测速度。pipeline/example CFG7.5和in-context10均不同论文FID5。
- README权重遵循LLaMA1许可，HF cardData为空不提供宽松授权证据。

## 对研究设计与写作的启示

共享模块或视觉预测有利的假设须限定于语义表征充分、条件对齐良好、允许局部外观变化的任务。验证应固定数据曝光、总FLOPs、教师/初始化、prompt和检索候选池，分开joint-vs-separate、续训、视觉loss和causal表示。对视频加入时序打乱/错字幕、等额外步图文续训，对文字加入细笔/OCR/未见文字系统，对笔顺加入同终态异顺序、合法事件和RGB可观测性。

同时测理解/生成退步分项与保留能力，报告全参数、外部decoder、检索、AR、扩散和CFG的总延迟。上述是未运行的可证伪设计，尚未构成新颖性闭环。

写作可学两篇将问题、模块与训练阶段逐项对应；Claim应贴近具体表行、预算与失败项。Limitations从表示瓶颈、数据偏移、代码可用性与制品兼容性写起，避免照抄摘要的笼统领先结论。
