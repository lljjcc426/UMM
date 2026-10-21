# MotionCtrl：相机／对象控制与过程可观测性

第八十八批补完[L039](../reviews/L039.md)明确版本核心三遍与五项书面，352目录、177核心/180项五条书面（含未通过项），175条未确认核心三遍（含资源）。[固定制品审查](../../data/motionctrl_representation_release_audit_2026-10-21.json)记录代码/模型卡差异。没有删除文件、下载权重或运行模型。

## 研究和版本

所读[作者项目PDF](https://wzhouxiff.github.io/projects/MotionCtrl/assets/paper/MotionCtrl.pdf)22页含补充，标arXiv2312.03641v2及SIGGRAPH2024会议页眉。[Crossref](https://api.crossref.org/works/10.1145/3641519.3657518)正式题录页码1–11；尚未逐页对照出版社全文。已读Abstract/§1–6/Eq1–3/T1–3、附A–E研究文字/T4–6；画廊按图注选读，未逐幅观看全部视频。实际p4框架/p7主表/p14补表已核。

unified限定为同一控制器支持相机与对象运动。输入文字及R/t序列、对象轨迹，输出RGB；没有过程问答/识别与生成共同训练或中文规范笔顺评测。相机全局变换、对象局部运动、标注不齐三项困难，分别对应模块位置和分阶段训练动机。

CMCM将每帧12维R/t复制到空间位置，拼到时间块第一次selfattn输出，用FC回原维后做第二selfattn；训练包含原attn2，不能只记新增FC。OMCM逐帧卷积从位移场提取四级特征，加到UNet encoder。先在RealEstate10K训练相机，再冻结相机/底座，用WebVid动态轨迹dense→sparse适配对象；改变顺序可能破坏已适配对象特征，论文只有文字/定性说明，尚不足以量化归因。

## 协议和结果

| 要素 | 原文／代码核查 | 解释边界 |
| --- | --- | --- |
| 数据 | RE>60K，BLIP2五帧caption拼接；WebVid243K，随机32帧、skip1–16、ParticleSfM动态轨迹 | 伪轨迹的漏检/动态分离误差需独立统计；预处理报告约2min/32帧，设备不详 |
| 相机测试 | 407=80基本+200 RE+100 WebVid+27 HDVILA | 基本8pose×10prompt；RE20pose×10prompt，组合数不等于独立pose数 |
| 对象测试 | 283组合，74轨迹/77prompt | 重复轨迹/提示应在统计时聚类，不直接当283独立轨迹 |
| 主训练 | 8V100，Adam lr1e−4/b128，16×256²；CMCM50K，OMCM20K dense+20K sparse，最多8轨迹 | 未给多seed/CI、各baseline全预算与完整采样配置 |
| T1 | CamMC基本.0289 vs AD.0548，复杂.0735 vs VC.0950；Obj28.877 vs36.8351；FVD852.15 vs1004.99 | 支持这些指定指标，提取器关联/失败分母与SE3尺度处理不足 |
| T2 | temporal CamMC.0289，timeemb/spatialCA/spatialSA为.0887/.0857/.0902，base.9010 | 非时间变体也远低于base，正文close-to-original不能照搬；FID132.36弱于base130.62，CLIP.2355弱于.2359 |
| T3 | dense/sparse/hybrid Obj54.4114/34.6937/25.1198，FVD2227.87/2385.39/2001.57 | hybrid CLIP.2342低于sparse.2365；与T1数值不同，缺完整协议映射，不能拼作一表 |
| T4 | RE/WebVid/HDVILA CamMC .0840/.0589/.0499，VC .1073/.0702/.0953 | 保留分布分层；FID/FVD样本量和混合方式不能由CamMC加权方式代推 |
| T5 | 34参与者，整体偏好.9261、质量.9372、文字.9228、运动.9140 | 原始票数/片数/随机化/区间不足，比例不能直接换成“34人中92.61%的人” |

CamMC/ObjMC由ParticleSfM估计生成片的相机/轨迹再算Euclidean差；单目translation gauge、旋转与平移量纲/归一化、对象匹配和追踪失败处理关系到解释。FID/FVD为分布指标，不能当逐事件正确率。作者§5明确承认复杂相机和复杂对象联合控制成功率较低，需精心设计条件；相机/对象单项表不能替代联合成功率。

附E对MotionDirector/VideoComposer分别使用motionvectors/trajectories描述，而T6为templatevideos/motionvectors，存在二手比较不一致。应回到两篇原研究核对。DragNUWA当时未直接对比的理由是代码未公开，不能作为当前公开状态的结论。

## 发布和配置

读[固定主GitHub](https://github.com/TencentARC/MotionCtrl/tree/6242d55414d3f4ad690bf0934889660f78e81b6e)162项树、README全文、motionctrl.py、指定forward/Adapter/UI段及config/run.sh。固定主配置C4/scaling.18215、OpenCLIP1024、UNet320及四尺度；OMCM PixelUnshuffle8把2通道变128，再逐帧2D卷积。论文preliminary对通用LVDM的3D-AE介绍不能直接用来描述这份AutoencoderKL发布配置。

`run.sh`依次赋`both`、`object_motion`、`camera_motion`，最终camera生效；想同时控制必须修改该值。公开例seed1234、5个样本、b1、256²、50DDIM、eta1、CFG7.5。它补充可执行条件，尚未证明和论文全部表同协议；正文没有完整采样超参。后续AnimateDiff训练分支、SVD、VideoCrafter2与主VideoCrafter1均分别登记，未全审其他分支。

[固定HF模型卡](https://huggingface.co/TencentARC/MotionCtrl/tree/475b66ef80e0d77752cbade485bb56171340071a)将SVD区链接到`motionctrl.pth`，LVDM区又列`motionctrl_svd.ckpt`，与文件命名及主代码指向有矛盾；Usage请求`motionctrl.ckpt`，固定目录无该文件。未下载权重，实际tensor与底座匹配仍未验证，不擅自把它们视为可互换。源码LICENSE和卡元数据Apache2，底座另按来源核对。

## 可观测性推论与下一步实验

Eq3用相邻帧位移，首帧和无轨迹位置全零。完全静止轨迹与空条件在这种表示中相同，单靠该张量无法定位静止对象；这是表示层推论，未测实际生成失败率。该条件也没有实体ID、笔尖接触、抬笔或累计墨迹。

UI把1024画布重采样为16整数点再缩到256，做99×99 Gaussian sigma10。论文Eq3描述将位移放当前位置；UI把`p[i+1]-p[i]`放在前一点位置、帧i+1。训练npy约定尚未全核，保留坐标解释未决，不能据此直接判所有训练/推理错误。细线、暂停、短促落笔与交叉更需要按真实时标/坐标保留事件。

验证应固定底座/数据/参数/采样总预算，对dense20K+sparse20K加入sparse40K/dense40K/混合40K强对照；相机pose×对象轨迹做全因子，独立提取器/人工标注、失败分母和SE3对齐，报告多seed和配对CI。静止不同起点、暂停/反向/交叉、移动镜头分别测，书写再加入显式接触/累计mask及规则渲染基线，报告事件顺序/方向/留墨/CER。方案未运行，潜在不足需查后续相关论文后才能判创新。

写作学习：Intro具体区分运动与数据问题，Method按可获取监督组织，实验逐项对应机制；Claim限定统一对象、历史版本和非全胜指标，Limitations写明复杂联合失败及输入设计负担。公开脚本/模型卡也需要审查，论文文字与资源配置相互校正。
