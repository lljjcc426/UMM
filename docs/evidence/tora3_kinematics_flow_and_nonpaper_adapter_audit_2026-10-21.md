# Tora3与Wan Toy Transform：运动学、条件flow与无论文适配资源

第八十七批新增[G039 Tora3](../reviews/G039.md)明确v3核心精读及[R12 Wan玩偶LoRA](../reviews/R12.md)资源协议审查。当前352条（325论文／研究、27资源），176项明确范围核心三遍/179项五条书面记录（含未通过项）；176条未确认核心三遍，含资源。没有删除文件、下载权重或运行模型。

## 一、研究类型和证据

| 工作 | 实际输入输出 | 已核查证据 | 本批完成边界 |
| --- | --- | --- | --- |
| Tora3 | 首图+文本+二维对象轨迹→同步视频/声音 | [固定arXiv v3](https://arxiv.org/pdf/2604.09057v3)10页核心、Eq1–19/T1–5；实际p4框架、p6主表、p8消融；[官方项目](https://ali-videoai.github.io/tora3_page/)与共享Tora README | 作者arXiv comment/README报告MM2026接收；关联DOI的Crossref查询404，正式出版全文未核。未定位Tora3专门代码、检查点或PAV下载 |
| Wan Toy Transform | 首图+风格变形描述→81帧视频 | [固定GitHub](https://github.com/alibaba/wan-toy-transform/tree/c86ea3638c137792389f2fc0f1c4d912353634dc)全部非assets文件；[固定HF](https://huggingface.co/Alibaba-Research-Intelligence-Computing/wan-toy-transform/tree/94ca3cd260d4b824c7f8e909fd2edbaf9e94db90)README/config/目录；Diffusers固定依赖相关源码 | 未定位对应独立论文/训练配方；属于非论文资源，不增加论文三遍通过数，未测本机效果 |

[制品审查JSON](../../data/tora3_and_wan_toy_release_audit_2026-10-21.json)保留所读版本/参数与未定位事项。Tora3项目页导航的`landmark-tokenized-dit`属于其他项目，不当作Tora3实现。仅有项目按钮、相同作者或共享README均不足以证明专门代码发布。

## 二、Tora3的五个核心问题

1. **问题**：通用视听联合生成可能在运动、接触时刻及音量演化上错配；本文把physical coherence操作化到轨迹层，而完整真实物理/材质接触声学仍超出验证范围。
2. **现有方法不足**：视频侧有运动条件也未必向音频提供可对齐的速度/事件信息，联合attention也未必学到时刻因果。二维中心轨迹同时缺失材质、接触力和世界尺度，单加轨迹无法唯一决定声音。
3. **具体改进**：视频传播首图latent到轨迹位置，音频引入8D位置/速度/加速度/模长及时间对齐CA；混合flow在条件区域采用轨迹latent端点，并平衡内外区域损失。
4. **优势条件**：可靠轨迹、声音随运动强弱及接触时刻变化、对象首图特征可传播时，显式共用条件可能更有帮助。遮挡、移动镜头、同轨迹不同材质或跟踪噪声属于需要单测的分布。
5. **实验检验**：论文分支、注入、运动学特征与hybrid表支持指定配置。还需等预算2×2路径×区域loss权重、轨迹错位/延时负对照、独立人工事件与更大N/CI；这些补充实验尚未运行。

视频条件用时间平均池化后的坐标在潜网格放入首帧特征，其他位置为0，同像素碰撞随机选一条；它没有显示笔尖落笔状态。声音8D经长边归一化、差分、signed log、训练统计Norm和3层MLP，再对音频query做RoPE对齐CA，门控gamma初始化−10，sigmoid值很小但非精确零。视频注入不增参数只限定该分支；完整模型从11.66B增至12.25B。

Eq13–19的条件端点需要认真区分：mask外`t=1`是Gaussian，mask内是轨迹latent；目标速度分别对应各自端点。该条件flow改变采样起点，没有给出`t=0`最终轨迹必然正确的约束证明。binary mask用于路径，Gaussian sigma.5的soft mask明示用于loss；不能将二者混写成相同conditioning。

## 三、主表、消融与实验条件

训练PAV460K来自公开源加内部视频，经Qwen筛动、SAM2首帧中心/CoTracker3伪轨迹及视频/声音caption；32A100、global batch32、30K步、lr4e−5、BF16。960K是曝光次数，不能当新增独立样本。训练分辨率/帧率、音频采样率和完整采样配置未报告定位。评测仅50段代表性视频，离散/连续事件子集分母、CI和去重不足。

| 对比 | 作者报告 | 可支持的判断与限制 |
| --- | --- | --- |
| T1 Tora3 vs AVControl | FVD784.1/829.6，Traj12.13/19.95，FGAS.234/.209，ETE.181/.214，MAIC.63/.55 | 指定50片协议下这些指标较优；额外训练/输入和底座预算未完全匹配 |
| T1非全胜 | AS4.61<MOVA4.63，PC1.81>MOVA1.77（↓），CLAP.44<MOVA.46 | 保留质量/复杂性/文字声音对齐取舍；不写全指标SOTA |
| T2分支 | 双分支FGAS.225/ETE.193/MAIC.66，视频单分支.198/.247/.46 | 支持显式声音条件；双分支AS4.47低于视频单4.51 |
| T3注入 | Tora-style/WanMove-style/本文Traj17.06/13.91/13.03，额外视频参数.99B/590K/0 | 是共同框架移植变体，未等同原发表模型全部协议；零参数不包含音频新增模块 |
| T4特征 | none→r+v→r+v+a→加模长，MAIC.39/.48/.56/.61 | 该协议单调改善，缺多seed和同容量通用特征对照 |
| T5 hybrid | FVD811.8→784.1、Traj12.94→12.13、FGAS.225→.234 | 同时改路径和loss；未报ETE/MAIC。主表MAIC.63低于T2的.66，不能宣称hybrid改善全部同步指标 |

TrajError是L2，Tora原论文用L1，跨论文不能直接比较绝对数值。AS虽名aesthetic，具体由MANIQA/MUSIQ图像质量代理平均；FGAS是CAV-MAE Sync特征相似，不能直接解释为真实接触正确率。ETE/MAIC的阈值/onset提取/时滞/子集N与ETE单位未完整定位，`.181`暂不标秒。

## 四、公式理解与待核盲区

中心差分的作用是把位置转为局部运动学条件，成立精度依赖光滑轨迹与真实采样时标。本文tau=1/fps；时间池化后应采用何种实际间隔需代码澄清，当前证据不足以判实现错误。若每坐标位置噪声独立方差为sigma²，直接代入差分可得速度噪声方差`sigma²/(2tau²)`、加速度`6sigma²/tau⁴`；这是本审查的解析推导，未做模型实验。接触瞬间不光滑，2D归一化也不提供世界米/秒或接触力。加速度是否增加速度取决于`v·a`，不能由a的方向孤立判断。

需要独立事件标注检验“轨迹派生事件—声音”是否只符合共享伪标注。控制相机、尺度、追踪误差、轨迹采样间隔和音频延时，报告失败而非只取成功跟踪片。与书写联系时分别标笔尖位置、落笔、累计墨迹、摩擦音；音视频相关高不代表笔画先后或方向正确。

## 五、无论文资源的深审：Wan玩偶LoRA

HF配置明确标准LoRA `r=96/alpha=96`、dropout0、bias none，无DoRA/rsLoRA；目标层含q/k/v/o、图像k/v和FFN两层，标准缩放alpha/r=1。这能说明发布参数，尚无证据说明r96为何最优。配置base字段为空，实际base由推理脚本确定为`Wan-AI/Wan2.1-I2V-14B-480P-Diffusers`。

完整脚本显式CLIPVision/VAE FP32、pipeline BF16，输入按约480×832面积和原比例缩放并向下对齐；长宽随原图变化。生成81帧、CFG5、空负prompt、16fps导出，未设Generator种子。脚本省略步数，但[所锁Diffusers v0.33.1源码签名](https://github.com/huggingface/diffusers/blob/v0.33.1/src/diffusers/pipelines/wan/pipeline_wan_i2v.py)明确默认50步，已核该签名及scheduler/去噪段。依赖另锁Transformers4.51.3/Accelerate1.6.0/PEFT0.15.2，README测试PyTorch2.6/Python3.12/cu124；模型ID未锁revision仍影响复现。

| Offload | 作者A100 VRAM | 作者生成时间 |
| --- | --- | --- |
| leaf | 11.9GB | 17m17s |
| block，group1 | 20.5GB | 16m48s |
| model | 39.4GB | 16m24s |
| none | 55.9GB | 16m08s |

这些是作者工程报告，未明确主机/精确shape/计时边界/热启动和方差；本次没有运行。offload将部分驻留/传输转至CPU，未证明更低总RAM、训练成本或更好生成质量。缺base无LoRA/全SFT/rank与目标层质量对照，也未公开定位训练数据/lr/步数/脚本；致谢diffusion-pipe不足以恢复配方。

HF许可标签MIT，固定GH树未见LICENSE文件；底座/组件另按原许可核对。该资源实现外观变形，逐步绘画还需验证新墨迹单调累积、笔尖接触和事件顺序。迁移实验需固定数据/预算，base/LoRA/全参及rank×alpha/r×目标层交叉，测风格/身份/时序/事件与CPU/GPU成本，不能从四个玩偶showcase推断文字能力。方案未执行。

写作学习：具体错配应对应模块和干预实验；计算开销限定到分支或完整模型；无论文资源照样核输入输出、数据、实际默认、指标、对照与条件。未证实的配方、实现、统计和机制均保留未决，不将审查推论归为作者自认。
