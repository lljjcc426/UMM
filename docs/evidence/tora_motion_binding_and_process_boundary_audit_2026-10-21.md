# Tora/Tora2：轨迹、身份绑定和书写过程边界

第八十六批补完[L034 Tora](../reviews/L034.md)与[L035 Tora2](../reviews/L035.md)明确版本研究核心/五项书面。350目录，175核心/178项五条书面（含未通过项），175条未确认核心三遍（含资源）。无删除、权重下载或模型执行。

## 证据版本

- [Tora正式CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhang_Tora_Trajectory-oriented_Diffusion_Transformer_for_Video_Generation_CVPR_2025_paper.pdf)11页+[官方supp](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Zhang_Tora_Trajectory-oriented_Diffusion_CVPR_2025_supplemental.pdf)7页研究核心；实际框架p4、完整主表/消融p7、课程表/规模图p8。未逐幅观看全部生成视频。
- [Tora2 arXiv2507.05963v2](https://arxiv.org/pdf/2507.05963v2)10页研究核心/全部五张表；实际框架p4、主表/表示消融p6、绑定/CL图表p8。正式[Crossref](https://api.crossref.org/works/10.1145/3746027.3754869)确认ACM MM2025 pp9434–9443；所读v2 DOI/ISBN仍为模板，出版全文尚未核对。
- [固定官方共享仓库](https://github.com/alibaba/Tora/tree/9a23dceb905d8b224983f7a94f42a6db79c9c63b)的树、README、配置和轨迹/调制/训练/推理选定代码，以及两份HF模型元数据，见[制品审查](../../data/tora_motion_binding_release_audit_2026-10-21.json)。代码未执行。

## Tora解决什么

给定每帧坐标，稀疏位移直接条件难与跨帧压缩token对齐。Tora将flow可视化后用3D motionVAE压缩，再由卷积和残差调制注入时间块，dense后sparse课程适配交互轨迹。主实验用OpenSora1.2；正式版另加CogVideoX2B/5B规模实验，公开代码以Cog5B为底座。两条路径的VAE、通道和attention不同，应分别记录。

主表128帧TrajError11.72低于MotionCtrl38.39及同底座DragNUWA21.75；FVD494低于731/565。16帧时OpenSora的FVD430优于Tora438，CLIP.2452亦高于.2447。消融给3D压缩、adaptive调制、hybrid课程各自支持，但extraVAE和总曝光未完全等预算。有限两种模型/三个训练量不能建立普适规模定律。

训练631053片/2952.93小时，含内部标注；185测试片主要从对象分割集取稳定相机片，mask中心作真值。生成轨迹提取/漏跟踪处理、完整评测释放和多seed区间不足。人评对Kling物理45%、观感43%、遵指41%，保留该差距。人类“物理感”、FVD和L1轨迹不等于接触动力学或物理守恒证明。

## Tora2补哪一层

多实体需要把外观参考、名词和轨迹对上。Tora2用DINO+Face/ReID先验、adapter/QFormer生成外观，再门控selfattn绑定每实体三种条件；运动调制、图文fullattention、外观crossattention分层注入。两向跨模态InfoNCE加强匹配，公式没有显式entity–entity或motion–motion同模态负对项。

T1非人SubjS .615低于VideoAlchemist .626，VidS .741低于.743；人FaceS .419高于.411。与Tora+Flux首图管线相比，轨迹误差非人19.72→17.43、人17.41→13.52。绝对cosine差−.011/+.008，乘100为−1.1/+0.8分；不能照抄为相对−1.1%/+0.8%。VA没有轨迹项，不填0或据此判它误差最高。

T2在去motion/绑定条件下DPE胜各列；T3门控轨迹17.31优于线性20.74，但TextS .259低于.261；T4加CL降至14.16；T5先运动后外观误差14.16低于19.23，而FaceS .404低于反序.409。总体取舍比“全面最优”更准确。先验更多、参数更多和融合机制尚未全隔离。

## 代码和论文需保留的未决项

| 项目 | 核查事实及边界 |
| --- | --- |
| Tora原表与发布 | README旧声明不开放完整版，后续TODO勾complete；固定树为Cog5B。不能仅由TODO断定原OpenSora主表可复现 |
| 训练配方 | 公布Cog样例49帧480×720/8fps，dense/sparse各15K步、lr1e-4/5e-5；主OpenSora论文2e-5、多bucket/2+1epoch。不同实现配置需要分别评估 |
| latent帧数 | SAT `sampling_num_frames=13` 经(13−1)×4+1得到49RGB帧，不能报告只生成13帧 |
| 低显存声明 | diffusers约5GiB依赖sequential CPU offload，README说明会慢；Sage/compile有首步成本，未本机测量，不算同质量/硬件的实测提升 |
| 轨迹表示 | 256画布整数坐标，重采样/缩放再高斯99×99 sigma10；同帧同像素flow赋值会覆盖先前轨迹，不含实体ID和接触状态。提示表示信息损失，未量化实际失败率 |
| Tora2冻结 | F2 TE/MGF也标雪花，§4.1明确联合优化它们；实际freeze未决，未用图或文字之一替代完整配置 |
| Tora2初始化 | Eq2零γβ却无显式identity项，与原Tora残差简写不同；固定代码可证明Tora MGF有identity，不能据此推定未定位Tora2代码 |
| Tora2公开性 | 共享README有论文链接，固定树未定位DPE/门控/CL专门训练及对应权重；不能将Tora发布当Tora2发布 |

HF的[原SAT制品](https://huggingface.co/Alibaba-Research-Intelligence-Computing/Tora/tree/e6df4064927f07a802d2d670767bb80665be0725)和[diffusers制品](https://huggingface.co/Alibaba-Research-Intelligence-Computing/Tora_T2V_diffusers/tree/055ee0f4fcfbabcedd33065a15405a60865da5fb)许可元数据为other，源码Apache2另有CogVideoX权重许可要求。未下载权重或推断统一许可。

## 与书写的关系及实验设计

对象中心轨迹控制、实体身份绑定、落笔动作和留墨是不同可观测量。Tora2解决部分错配动机，仍未验证同终态异笔顺、旧墨迹保留、新笔生成或笔尖接触。因此不能将两篇归类为专门规范书写视频模型。

先固定底座/数据/预算检验压缩×融合×dense/sparse课程，显式计motionVAE额外成本；对Tora2匹配prior/参数量/总计算，比较QFormer与MLP、门控与普通attention、CL与无CL，打乱实体对应作负对照。轨迹按相机、遮挡、实体数、交叉、同像素反向和高频折返分层；报告归一化误差、漏检测/跟踪、身份交换、盲评和区间。书写另加入事件ID/接触/累计mask及非汉字，测CER/方向/顺序/留墨。方案未运行。

作者共享仓库还指向[Tora3](https://arxiv.org/abs/2604.09057)与[Wan玩偶LoRA](https://github.com/alibaba/wan-toy-transform)。本批只发现并记入后续核读，尚不计其精读或新增独立记录；结合已有Wan-Move等后续再判研究缺口。

写作可学具体错配→模块→对应消融的组织。Claim保留版本/输入条件/指标取舍；频率、解耦、物理和最优等词需要操作定义、干预和误差证据。Limitations列未公开配方、检测分母、图文不一致与分布过滤；本笔记的批评不写成作者已承认。
