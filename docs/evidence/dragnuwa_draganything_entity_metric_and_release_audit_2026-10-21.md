# DragNUWA与DragAnything：控制范围、实体表征、指标代码及发布协议

第一百零九批完成已有[L040 DragNUWA](../reviews/L040.md)、[L041 DragAnything](../reviews/L041.md)固定核心三遍、实际框架和全部现有主表/消融、五项书面检查，补全题名。[结构化证据](../../data/dragnuwa_draganything_entity_metric_and_release_audit_2026-10-21.json)。目录356条（329论文／研究、27资源），218核心/221书面含未通过项，138条未确认核心（含资源）。没有删除文件、新增独立论文/资源、下载权重/视频图片数据集或运行模型/复现；只读取论文图表、代码/配置及轨迹文本标注。

## 身份与固定来源

| 工作 | 固定原文及已读范围 | 实际核看与边界 |
| --- | --- | --- |
| DragNUWA | [2308.08089v1](https://arxiv.org/html/2308.08089v1)，2023-08-16；Abstract/§1–5/Eq1–7/T1和图注 | F3框架、完整T1配置、F6条件去除；没有量化主结果表或TS/MF/AT数值消融；未确认正式会议/期刊 |
| DragAnything | [2403.07420v3](https://arxiv.org/html/2403.07420v3)，2024-03-15；Abstract/§1–5/附§6.1–6.2/Eq1–3/T1–3及图注 | F4框架、完整T1/T2/T3、F8人评。正式[Springer ECCV2024/LNCS15080:331–348](https://link.springer.com/chapter/10.1007/978-3-031-72670-5_19)，2024-09-30；ECVA正式PDF仅取得1.06MB/26.90MB，不完整文件排除，未声称正式全文已读 |

两项未逐图审看全部样例/视频，也未逐篇精读其参考文献。固定预印本阅读、正式录用身份、当前制品和独立复现分别记录。

## DragNUWA：三种条件与课程具体解决什么

原论文针对文字/首图不足以精确指定运动、人体关键点标签难覆盖开放域及稀疏信号难学。TS使用UniMatch光流，在间隔16网格上加随机扰动，再按光流强度选1–8轨迹点并逐帧推进，以99/σ10高斯增强。网格改善覆盖，但后续仍按强度采样，不能声称静止/小运动与大运动等概率。

视频逐帧VAE得到x0，加标准VP噪声成为xt；首图重复L帧，轨迹图前补零帧，文字CLIP77×1024。多尺度UNet各层用zero-init卷积预测图像、可用mask及轨迹的w/b，再以h←w·h+b+h残差注入，文字cross-attention。x0代表干净latent，不代表视频第0帧。训练先完整dense flow再稀疏轨迹，Eq6/7均为噪声MSE，变化在条件/课程。

WebVid10M和自建VideoHD75K（网络片/BLIP2/人工筛错）。LD8帧320×192/2秒、HD16帧576×320/4秒，均4fps；1.60B/Adam5e-6/b128/WarmupLinear.05，各条件drop.1。两阶段步数、卡时、推理NFE/CFG/seed和精确测试集未核齐，不按常见配置补写。

F4/F5展示曲线、多物体和镜头运动；实际F6用冲浪图对比s2v/p2v/gs2v/ps2v/pgs2v，显示雪地文字和向右轨迹对特定例图的作用。只有可视化例图，无法支持总体成功率、显著优势或每项模块必要性。T1是实现配置，不能叫定量SOTA表。相关工作提及CVG/C2M/II2V/iPOKE/MCDiff/VideoComposer，缺同信息/算力外部主表和同总步TS/MF/AT对照。后作DragNUWA-SVD的评测数不回填成2023原始LD/HD结果。

### 当前官方制品状态与版本分离

[微软研究项目](https://www.microsoft.com/en-us/research/project/dragnuwa/)仍明确文字/图像/轨迹三条件；[固定官方GH babf27af](https://github.com/ProjectNUWA/DragNUWA/tree/babf27afb5fc72b9e65da3d0134840d26717c8f1)完整main树仅README，说明迁往Microsoft Branch待审查。旧`svd`分支tree API本次404。当前不能声称原训练/采样实现已完整公开并通读，第三方保存的SVD1.5说明也不当原论文代码核验。若以后取得历史合法固定版本，应单独记录底座、文字条件是否保留及配置。

## DragAnything：额外实体条件与身份/位置表示

“What entity/how drag”的动机清楚：同一点可能指局部、整个对象或背景，SAM/GT mask明示范围。首图加噪，在固定时间步读取冻结扩散UNet特征，按mask平均pool；实体向量在最大内切圆域铺开并沿CoTracker轨迹移动，同时生成Gaussian。两个条件encoder与noisy latent相加，控制UNet的多尺度残差进入冻结SVD，实体mask加权MSE训练控制分支。实际F4的雪花/火焰区分冻结和训练模块。

它增加首图mask和分割视频监督，且使用额外ChilloutMix/DIFT网络；有mask的简单区域/常量ID也是必要强对照。toy云层/鱼鸟局部变形可解释作者动机，未证明任意点方法或更强底座必然失败。圆域+pool保留身份但丢部分空间/形变/姿态，不能默认解决3D转身或接触。

| 实验 | 原始结果 | 解释范围 |
| --- | --- | --- |
| T1同SVD VIPSeg | ObjMC324.6→305.7，FVD519.3→494.8，FID39.8→33.5 | 差18.9/24.5/6.3；相对降约5.82%/4.72%/15.83%。只比DragNUWA-SVD，非所有视频模型 |
| T2表征 | 无两者410.7/496.3/34.2；entity318.4/494.5/34.1；Gaussian339.3/495.3/34.0；both305.7/494.8/33.5 | both的ObjMC/FID最佳，FVD略劣entity-only，未全指标单调增益 |
| T3 maskloss | 311.1/500.2/34.3→305.7/494.8/33.5 | 局部loss在所测配置改善，不等价于笔画/物理约束 |
| F8人评 | 运动63%vs37%、质量56%vs44%；30图/3专业评者 | “26%/12%”是票份额百分点差；正文自比较“outperforms DragAnything”笔误由图确认baseline为DragNUWA，raw票/平局未齐 |

FVD/FID是分布指标，不单独证明逐例连贯、轨迹正确或动作语义。论文附§6.2明确二维不能精控3D旋转，大运动有多腿/模糊失败；未来换SORA的设想未做实验，不当结果。

## 直接核查代码、HF与轨迹包

[固定GH 79355363](https://github.com/showlab/DragAnything/tree/79355363218a7eb9b3437a31b8604b6d436d9337)完整1872项树；阅读README研究/发布段、完整ObjMC和train_VIPSeg.sh、DIFT/GT生成/条件encoder核心、demo条件与pipeline默认。vendored diffusers未全读。[HF f66fb7cc](https://huggingface.co/weijiawu/DragAnything/tree/f66fb7cc44da731feae9393c7ba4959bd1daf37d)卡只有Apache元数据；config/权重目录存在，未下载权重。顶层许可不能覆盖SVD、ChilloutMix和CoTracker各自依赖。

### ObjMC实际求什么

`utils/Eval_ObjMC/ObjMC.py`读取GT/pred目录文件名交集，每个GT实体按ID取预测序列，用`zip`配点，将所有欧氏距离加入一个列表取mean。因此是点加权平均；长轨迹/多实体视频权重更大，文件缺失不计入、短序列被截断，未惩罚不可见/缺失。不能称每图等权平均或轨迹累计距离。

GT生成代码先用CoTracker网格，再选首帧网格轨迹中离最大内切圆中心最近的一条，写整数像素坐标；`pred_visibility`未用于过滤，后续mask内轨迹重选被注释。预测脚本路径带`14frames_OriginalSize`，存在以原尺寸处理的迹象；完整表1坐标缩放/截帧及失败处置未还原，不能把305.7当256²归一误差，也不能据代码静态审查直接判原表错误。

### 发布的原始标注与论文评测输入不同

读取固定`data/VIPSeg_Test/trajectories.zip`全部JSON，仅读文本，无视频/图片数据下载。

| 项目 | 实际统计 |
| --- | --- |
| 文件/轨迹/点 | 343 JSON、4,367轨迹、99,203点 |
| 每文件轨迹 | 2–79条 |
| 序列长度 | 5–46点，非统一14；15点2,006条、20点534条、46点706条等 |
| 坐标极值 | x −48,031至28,573；y −14,374至23,241 |
| 含负值 | 202文件、702轨迹、10,863点 |

负坐标反映原始跟踪允许离开图面或漂移；没有对应视频/可见性，不能逐点判错。这些值与非统一帧长要求明确预处理及有效点规则。当前统计只描述固定发布包，不冒充论文正式评价样本或生成结果重算。

### 论文、启动脚本与演示配置逐层区分

论文写25帧320×576、AdamW1e-5/100K步/A100；FVD14帧256²。公开训练shell为lr2e-5、perGPU1、accum2、500epochs/fp16和7卡可见列表；它调用的`train_DragAnything.py`未见完整树，README仍“Train(Awaiting release)”。不能由启动脚本推定原实验用了7卡，或将500epochs替换论文100K。

demo为20帧320×576、motionbucket180、controlscale1；pipeline默认25steps、逐帧CFG1→3/fps7/noise.02、无固定seed。DIFT默认t261/第3上采样层/空prompt/8噪声样本均值，属于一个固定时间步的批量特征提取，非8轮去噪。HF config14帧、旧class名，不能自动当25帧论文最终checkpoint协议。

正文写4块均下采样却最终1/8；当前条件encoder为通道16/32/96/256、三次stride2，最终1/8。记录文码差异，不把未发布训练实现补成四次下采样。

## 对研究假设与写作的启发

固定同骨干、额外mask信息、数据和总步数，先比较二值区域/常量ID/随机向量/DINO/CLIP/DIFT，拆Gaussian和局部loss；再注入分割/轨迹误差，分平移/形变/遮挡/多体冲突/相机测跟随、形状、背景和失败率。公开完整输入、坐标/帧长、缺失和可见性，按视频/实体给区间；人评给raw票/平局与随机顺序。

对DragNUWA，用同总步sparse-only、dense→sparse和混合课程比较，拆anchor/强度/高斯/尺度；有参考与稀疏点控制的优势应落在可跟踪、中低幅、短时分布，不由精选例图扩展到任意动作。

在书写/素描中，对象位置和实体身份只是部分约束：笔尖走过正确路径仍可能不留墨、抬笔划线、旧笔画漂移或事件错序。应分别测接触/抬笔、永久墨迹、可见笔画事件和同终态不同过程；整体运动分数不能替代。以上实验未执行，缺口不自动构成新颖课题，需追查已有实体/动作/过程研究。

写作上，DragNUWA按监督→多条件接口→课程→推理组织，DragAnything按对象范围→身份与位置表示→局部监督组织，可学习问题到模块的对应。Claim须限定附加信息、分布和具体指标，区分票份额差与相对提升；Limitations用具体失败、底座限制、伪标签和发布协议说明证据边界。
