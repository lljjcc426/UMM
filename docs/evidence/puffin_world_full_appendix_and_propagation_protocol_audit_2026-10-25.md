# Puffin-World：完整附录与传播评测条件审查

第二百一十五批完成[L168](../reviews/L168.md)明确范围核心三遍及五项书面验收。[结构化证据](../../data/puffin_world_full_appendix_and_propagation_protocol_audit_2026-10-25.json)。358目录（331论文／研究、27资源），320核心/325书面含未通过项；待完成核心深审11篇论文／研究；27项资源按制品协议另审。无目录新增、文件删除或模型执行。

来源：[主源1](https://arxiv.org/abs/2609.04196)、[主源2](https://arxiv.org/pdf/2609.04196v1)、[主源3](https://kangliao929.github.io/projects/puffin-world/)、[主源4](https://kangliao929.github.io/projects/puffin-world/supplementary.html)、[主源5](https://github.com/KangLiao929/Puffin/tree/c6d9ae5e63bc79d5d01554235b7c1d3772c327c8/Puffin-World)、[主源6](https://huggingface.co/ACERobotics/Puffin-World/tree/02976cb47817597dc126cfce7bfbdce60b952c68)、[主源7](https://huggingface.co/datasets/KangLiao/Puffin-16M/tree/2112b3502f9ea0cc1d31d2c5a2b7f2259b52cffd)。

## 研究问题

如何用同一模型理解绝对相机姿态、按相对轨迹生成多视图RGB/depth，并保持重力与几何一致？

## 现有不足

相对ray只有视图关系而无重力锚，absolutePerspectiveField适合单图却缺平移轨迹；RGB生成缺显式几何，重建依赖独立模块，多源数据旋转变化不足。

## 贡献

OmniCamera9ch绝对up2/latitude1+relativeorigin3/direction3，rolemask4ch通过轻fuser加到latent并稀疏多层再注入；首帧重力相对旋转传播，RGB/深度共latent及asymattention，4stage训练。PuffinCam15M/PuffinTraj1M及28公开源44.5M伪camera标注。相机姿态几何传播支撑指定camera任务，不建一般接触/物体动力学。

## 输入、模块、输出与公式

Fig3单图→visionencoder/LLM→scene+roll/pitch/FoV；text/camera或refimage+轨迹→queryconnector+diffusion→RGB/depth，pose反投影点云。PP只传首图gravity、后view条件由既定相对pose形成。文字到3D先T2Ianchor再I2multi；selfcalibration演示估姿后纠正camera，非笔尖动作或环境物体互动。

## 模型结构

Base C-RADIOv3H+Qwen2.5 7B+SD3.5medium2.5B；Pro C-RADIOv4H+Qwen2.5 1.5B+SD3.5large8.1B，64query/6层connector，另Caption Qwen3.5 .8B独立标注专家。Eq1–4dense相机，Eq5/6zero初始化注入，Eq7gt=Rrelg0；Eq8/9两种FM分别按view数均值/深度warmup。frozen16chVAE共用于RGB/Hilbertdepth，RGB/textquery不读depth但depth读全部，zeroembed逐渐启用；同权重仍受depthgradient影响，asymmask不等于无训练耦合。长程lastlatent直接传下chunk避重复VAE，但不保证全局scene记忆或无漂移。

## 数据分布与划分

论文900K全景→15Mperspective，生成筛8M，排Stanford2D3D以供评测；roll/pitch±45/FoV20–105，Traj yaw0–360/FoV60–100，每轨单旋转轴/可往返，不提供真实动态对象。T8训练Traj1M约100Mframes；HF卡固定2112b35实际15338221triplets/1136696轨迹各90帧，规模口径分开，bench600/100声明源全景与train互斥。DL3DV6377scenes/2M、RE10K5134/.6M、ScanNet1468/2M、Hypersim756/70K、MVS120/12K、Tartan369/300K。T7另一标注子集Hypersim448/Tartan18scenes与T8不同需保留。公共绝对相机为模型伪标签非标定GT；height五类别Qwen3VL32B解释非准确米制高度。DA3补realdepth并对稀疏scale。

## 指标与评价协议

T3roll/pitch/vFoVmedian及AUC1/5/10；T4up/latitude/gravitymean/median+FID(600)，由自身perception估generatedcamera，独立校准误差与共模偏差未拆。T5RE10K50heldout/Traj100的PSNR/SSIM/LPIPS及后者camera，T6PP同评估器。T4general模型仅同prompt/camera描述，专用model可读densecondition，预算不等。F5caption称显示errorcloser0但图signednumbers看似姿态值，未从该标注单独推出误差。无深度量化主表/3D reconstruction精度/闭环成功率/置信区间。

## 对比方法

相机DeepCalib/GeoCalib/Puffin等，AnyCalibFoV专用参考也列；生成GPTImage2/NanoBanana2/FLUX2/QwenImage2/PreciseCam/Puffin；worldMotionCtrl/CameraCtrl/ViewCrafter/SEVA/MVGenMaster。T5MVGenMaster†训练含RE10K，不可忽略脚注。两骨干配置/参数/数据均变，未单因子归因于统一架构。

## 实验条件和发布边界

论文4stage lr1e-4/2e-5/5e-5/2e-5、b512/512/256/128，AdamW.9/.95wd.05cos；II全训visiongrad.1，III/IV冻visionLLMprojector；8views640²，III1–3ref/IV1ref，depthramp3000至1，jointdrop.1/PFdrop.15，50NFEgreedyunderstanding，CFG4.5single/2world。公开Pro I/II配置lr乘acc2为2e-4/4e-5，maxmicro30000/44000；IIIrepeat7×4000=28000micro，IV3000×sumrepeat，depthwarmup2000micro异于论文3000。实际GPU/运行时/各表variant和重复seed未给齐。

## 主结果

T3除Any参考后12/12median/33of36AUC含tie；若计表列Any，LaMARFoV2.73>Any2.25，AUC5 43<51.6，故“所有”需限定参考组。LaMARpitch.71与Puffin相同。T4gravitymean1.32vsPuffin4.92/FID75.93vs80.29均优。T5RE10K17.22/.595/.318优所列，Traj18/.613/.288对SEVA17.94/.614/.307，SSIM略低，camera.8/1.1/2.96优。T6均PSNR19.87→20.54SSIM.62→.67LPIPS.23→.21、roll1.94→1.76pitch5.14→4.75，作者报告，差值无CI不推统计显著。

## 消融及进一步实验

T6+F12仅PP有/无分roll/pitch/yaw，yaw变化小与重力不变机制一致；无同数据同computeabsolute/relative/融合位置/数据scale/depthwarmup/asym/单多任务完整因子消融。F7mimic/selfcalib、F15回转、F16长程compound、F17RGBdepth点云为选择性定性。源代码self_calibration先估roll/pitch后build_action规则每7步线性减到0，再生成；没有生成后重新感知迭代到阈值的验证循环，序列monitor遇首个异常纠正后停，不能将演示当学出闭环actionpolicy。

## 局限与疑问

固定代码generation_multi_view默认offline_prop，model.py1573读取global首帧gt_cam_params[0]再相对pose传播，后chunk传anchor，无VLM；这里字段GT可能是模型预标注或合成真标签，依数据不同，不能统称纯在线。online才估首帧，offline逐帧读预标注，docs默认config已与代码不符；论文各表实际选项未说明不能直接假定。glb默认跨chunkoverlapdepth比例+每windowdepth-to-pose尺度搜索，优化投影depthagreement，只用于点云显示不改图像；native重建展示仍有确定性后处理。depth颜色映射7段cube路径+f=1−(1+d/10)^−2、逆解nearestsegment，VAE可引offcurve误差/远处饱和。末段明确未来扩dynamicworld，现模型对书写/碰撞/力学无直接证明。

## 预期优势条件

视角运动主导的静态场景、首帧重力可靠且目标pose已知时，absolute锚+relative可能减roll/pitch漂移；RGBdepth共同输出可少外部学习模块，但pointcloud视觉质量仍需测原始与对齐后差异。

## 可证伪实验

同底座预算拆Omniabs/relative/PP/depth/asym/data，分别报online/offline_prop/offline及独立相机GT/估计器；首帧角度噪声传播/平移遮挡/往返回访长程误差；原始depth与对齐点云独立几何GT；samebudgetjoint/single和语义遗忘；自校准多轮观测/执行/重新观测成功率，区分规则plan与模型policy。书写另需penstate/笔顺/接触时间。未执行模型。

## 论文组织与Claim学习

三类状态→绝对相对表示缺口→PP敏感旋转消融，机制与实验对应清楚；宜限定physics为gravity/camera，不以action字样推出一般动力学。T3参考基线计数/600vsdoc650、defaultoffline_prop/2000vs3000warmup、原始/对齐点云及规则action必须写清。无externalmodule需限定推理学习模块，不能抹去训练Qwen/DA3伪标和确定性后处理。

## 实际阅读范围

唯一v1全32页§1–6/136条references清单与关键来源/AppA1.1/A1.2/A2/A3.1–3；F1–17全11contacts，F3/p5T5/6p16及F10/11p26放大；T1–8全行/Eq1–9全读。官方project及supplement文字与对应论文fig视觉已核；动态视频未独立播放，不声称全部媒体逐帧。固定c6d9ae代码README/TRAINING/EVALUATION/EVALUATION_World指定节、ProI–IV配置及mix、model.py PP关键分支/depthcodec/transitionhook/selfcalib函数核；HF模型02976cb4三pth存在、数据2112b35卡metadata/统计核。未全量数据、完整代码或模型复现；核心三遍五书面完成。

## 发布协议差异

代码默认offline_prop只消费首帧预标注并传播，online才运行首帧感知；逐帧offline又不同。参数名含GT不能一概当真实标定。论文各表模式未给齐。Pro发布depthwarmup2000micro和论文3000不同；初两stage lr还乘acc。

## 控制与几何展示

selfcalibration公开demo按估计角度规则逐7步线性纠正；没有生成后反复重估闭环验收。点云融合默认尺度搜索为显示后处理，原RGB/深度PNG未改。两者都需在论文结论边界中保留，不能因此直接否定主表分数。
