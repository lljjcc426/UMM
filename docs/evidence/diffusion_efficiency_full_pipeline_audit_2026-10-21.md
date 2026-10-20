# 扩散效率综述：全流程成本、公式和汇总表审查

第八十四批补完[G023](../reviews/G023.md)固定v2研究核心和五项书面检查。350目录、172核心/175项五条书面（含未通过项），178条尚未确认核心三遍（含资源）。无文件删除或模型复现。

## 版本与范围

实际阅读[arXiv2410.11795v2](https://arxiv.org/pdf/2410.11795v2)62页中的§1–8完整研究核心（正文至32页）、Eq1–19、T1–7和框架，实际看p6 F3、p19 T5/Eq10/11、p22 T6。[出版元数据](https://api.crossref.org/works/10.1109/TPAMI.2025.3569700)确认TPAMI47(9):7506–7525,2025；20页正式全文尚未读到。以下问题限定所读v2，不能据此断言正式版仍有相同错误。参考文献未逐篇精读，SCI年度分区未核定。

## 可学习的研究结构

以原则、架构、训练/微调、采样、部署、应用六类组织成本：VAE/UNet/DiT/SSM/文本encoder，ControlNet/adapter/LoRA，偏好优化和个性化，求解器/蒸馏/GAN/检索，以及端侧/多GPU和ComfyUI/WebUI。其价值是把“采样快”扩为训练与部署的全流程问题。

综述没有共同重训模型或自有算法消融。表2是重建质量与压缩率，表3/4为不同数据、硬件、训练时长/步数的资源摘要，表5/6为不同原工作分数，不能直接作同预算排名。F6同时换模型、encoder、训练与中文prompt翻译，不是纯encoder消融。

## 必须回原始来源的技术问题

详细定位、原始来源和未决项见[结构化审查](../../data/diffusion_efficiency_equation_table_audit_2026-10-21.json)。

| v2位置 | 核对结果 |
| --- | --- |
| Eq10逆VP SDE | 写成−β/2(x−score)；按[原score-SDE Eq6](https://arxiv.org/html/2011.13456v2)代入f=−βx/2、g²=β，应为−βx/2−βscore，逆向dt<0。符号和系数都不能沿抄 |
| T5 DPM-Solver列 | FID6.37/4.28/3.90标在1/2/4 NFE；[原v3 T4](https://arxiv.org/html/2206.00927v3)为10/20/44，最后一项原表在50列特别标NFE44。不能据此说DPM-Solver1–4次达到这些分数 |
| §5求解精度 | DPM-Solver解析积分线性部分，非线性部分有限阶近似；有限NFE不保证精确ODE/数据分布，离散PC也不自动保持精确边缘 |
| §2.3 VQ-VAE泛称 | [LDM固定配置](https://github.com/CompVis/latent-diffusion/blob/a506df5756472e2ebaf9078affdde2c4f1502cd4/configs/latent-diffusion/txt2img-1p4B-eval.yaml)使用AutoencoderKL；连续KL与离散VQ应分别识别 |
| T1原DiT/Flux | 原DiT报告类别条件ImageNet，不能标为CLIP文本条件；Flux表1额外列bigG，与其F6和[官方固定加载器](https://github.com/black-forest-labs/flux/blob/802fb4713906133fcbd0d8dc5351620ca4773036/src/flux/util.py)的T5-XXL/CLIP-L不符 |
| §2.4空条件/ControlNet | 空条件不普遍是零向量；[固定ControlNet](https://github.com/lllyasviel/ControlNet/blob/ed85cd1e25a5ed592f7d8178495b4483de0331bf/cldm/cldm.py)的zero-conv输出空间残差，context独立处理，不能解释为训练null-text embedding |
| §3.3冻结encoder | 冻结减少梯度/优化器开销，仍有前向计算和权重占用；预缓存可以摊销计算，但缓存成本需计入 |
| §5.2 EMA/直流 | EMA更新目标θ−，在线θ由优化器更新。直线插值训练不保证边缘速度场轨迹都直或最优OT，Rectified Flow也可从数据直接训练，分类并非互斥 |
| 年份/纳类 | ScoreSDE ICLR2021、RF ICLR2023，v2分别标20/22；GGDM在原DPM-Solver表中标需要额外训练，不能无解释归入training-free；T6还有1/4/4列标头，其他未核单元不擅自修正 |

表2也说明质量维度不同：OpenSoraPlan在WebVid的PSNR/SSIM略高于SVD，但LPIPS.0586弱于.0547，且时间压缩率不同；不能把单一重建分数当生成或真实事件保留能力。

## 扩展覆盖与资源

从[固定官方综述仓库](https://github.com/TsinghuaC3I/Efficient-Diffusion-Models/tree/c34509eda9a00938043d4853e11e9657724a5947)提取全部单行`[[Paper]]`条目：208次出现，按arXiv ID/URL合并201候选，保留重复章节与原始链接。结果在[发现层文件](../../data/discovery/diffusion_efficiency_repository_candidates.json)。它与既有573条arXiv、200条UMM综述候选及主目录有交集，不能相加当独立论文或精读数。未声称其覆盖PDF全部引用。

发现层包含工程/适配/部署线索；ComfyUI/WebUI在本篇只完成用途核读，尚未独立审查其当前代码或作为新资源验收。模型卡、训练配置和代码无论文制品仍应按各自输入输出和实现条件调查。固定Flux加载器、LDM配置和ControlNet路径已纳入本批交叉证据；未执行或据此宣称全仓库审计。

## 可证伪实验与写作

记录总成本Tenc+Tvaeenc+Tdenoise+Tdecode+通信/缓存摊销，并分开教师/蒸馏/推理预算。固定数据、条件、checkpoint、分辨率和初噪比较等NFE与等延迟；固定teacher比较蒸馏，VAE先测细笔和短事件重建上界。LoRA需写rank/位置/冻结/学习率/验证搜索及合并状态，多种子报告OCR/字形/方向/顺序/漏笔、域外和非汉字结果。以上实验未运行。

Introduction可学完整成本问题的定义，Method式分类可用于相关工作组织；实验主张必须逐格提供原始协议。Claim避免将冻结、低rank、单步和开放权重分别扩大成无成本、不遗忘、同质量或许可统一；Limitations明确版本、证据来源、截止与未验证条件。当前选题仍需追引后续工作，不能拿2024综述的未来方向直接当2026新颖性。
