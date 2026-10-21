# 知识盲区与集中补学清单

按“在当前论文里做什么→输入输出→去掉会怎样→核心公式是否需要推导”记录。下面的已理解部分以本次阅读和简短推导为限；“待补”保持未完成，不把概念出现次数当作掌握证明。

| 概念与对应来源 | 当前可以解释的作用 | 尚需集中补学/验证 | 对书写研究的具体问题 |
| --- | --- | --- | --- |
| [EDM/G027](../reviews/G027.md)预条件与采样 | cskip/cout/cin缩放输入/目标及训练权重；Heun用第二次导数修正Euler | 完整补充材料、误差/调度推导、不同score/velocity参数化的统一换元 | 少步是否漏短笔/接触事件，计算用NFE而非只报步数 |
| [Consistency Policy/E03](../reviews/E03.md)轨迹蒸馏 | 学习从噪声t跳到更小s，局部教师/stop-gradient/DSM给训练约束 | 教师/学生完整代码和多模态保持，初始化方差与蒸馏误差分开 | 更快动作是否牺牲合法笔序多样性，反馈频率是否匹配执行周期 |
| [F5-TTS/E05](../reviews/E05.md)Sway | 改变噪声ODE求解节点分布，较多预算放在去噪早期 | 核查语音对齐机制与结构化事件任务的迁移实验 | 求解器时间与真实落笔时间不同，不能以Sway直接控制书写速度 |
| [UniTok/L061](../reviews/L061.md)MCQ与[TokenFlow/L094](../reviews/L094.md)共享索引 | 多子码本扩大组合表示，或共同索引同时保存语义/像素 | 固定比特率、token长度、训练FLOPs与内层预测开销的公平实验 | 一笔差、交叉笔和低对比墨迹是否量化丢失 |
| [Show-o2/C02](../reviews/C02.md)混合注意力/3DVAE | 文本AR、视觉段内双向，因果VAE压缩视频 | 全部高分辨率/视频checkpoint数据映射与逐事件信息保留 | “causal VAE”能否保存短抬笔；不把视觉全注意力当在线输出保证 |
| [L181](../reviews/L181.md)部件树与TPE | 用路径特征表示汉字空间结构，双网对比/双向学习 | 修正文中正弦定义/编号/归一化，再核实际编码和训练配置 | 部件树可支持未见字形，时间序列仍需独立表示 |
| [UReason/L032](../reviews/L032.md)/[RSI/L033](../reviews/L033.md)协同机制 | 固定意图干预、程序可验证数据和读写循环能定位部分瓶颈 | 自评器共谋/偏好、同预算联合与分离、外部裁判校准 | 提升来自过程理解、额外监督还是执行器能力 |
| [L055](../reviews/L055.md)/[L056](../reviews/L056.md)严格前缀 | 未来信息不可用，query在条件成立以前可输出空mask | baseline前缀裁切、源视频身份拆分、切换延迟与不确定性指标 | 不可见的笔尖接触事件应允许不可判，不强制猜唯一顺序 |

## 已澄清：确定性ODE与多模态分布

确定性求解不意味着最终分布只能有一个模式。ODE生成通常从随机初值出发；确定性映射会推送整个随机分布。

一个直接的数学反例是令Z服从标准正态，Φ为其CDF；取一个连续、严格正密度的双峰高斯混合，其CDF为F。则`X=F⁻¹(Φ(Z))`具有该双峰混合分布。映射是确定的，分布仍可双峰。还可定义单调插值`T_s(z)=(1−s)z+sF⁻¹(Φ(z))`，其正导数使它可诱导时间相关确定性速度场；这说明该反例与确定性连续输运并不矛盾。

因此，论文中观察到某种ODE策略模式减少，应继续检查随机初始化、噪声方差、教师近似、蒸馏目标、网络容量及求解误差；需要证据确定具体原因。这个反例不证明任意训练模型都能保留多样性，也不替代多峰动作的实测。

## 已定位但未解决：TPE文字公式与实现

L181 Eq17/18/19按文字定义：令A为Root，同时L1=A；首左子为`(A+A)/2=A`，首右子为`(A+R1)/2`。若A与R1正交，则原始内积分别为`||A||²`和`||A||²/2`，不能得到Eq21的相等。官方实现给首左右子使用不同频率基，故需要依据实际实现重新说明理论，而不能把文字反例扩展成实现必错。

后续优先核对实现对应哪组主实验，再决定是否需要运行最小数学诊断。当前未为这些来源编写镜像单元测试，也未修改外部研究代码。

## 第十批新增待系统处理

- 冻结扩散score的MSE条件学习与KL/最大似然的等价需要哪些理想教师、时间权重和分布假设？DreamLLM给出解释，尚不把它当一般定理。
- 区分CLIP图像—图像相似、文字—图像相似、FID与局部OCR，SEED/Emu2分别采用不同对象和比例。
- RQ空间位置数、每位置残差深度与真实AR开销如何分别计量？VILA-U的16²×4或27²×16不能只报空间token数。
- VILA-U公开脚本名义global_bs与per_device参数间的8进程倍数关系需核实际运行配置；未执行，不据此认定论文真实batch错误。

## 第十一批新增待系统处理

- 固定每任务样本曝光与固定总FLOPs是两种对照：联合模型的额外计算和样本顺序如何估计？JanusFlow提供前者，尚缺后者。
- 软量化τ极限、码本几何、预训练查表接口和随机投影初始化应分别消融；Orthus Table5不能将所有差距归因连续/离散。
- 监督式GPT-4o反馈、GRPO OCR/VLM奖励、模型内部一致性与独立正确性分别检验；教师失误和奖励漏洞须在未见文字/字体/长度下测。
- MetaMorph AppD重复200K行标记；UGen k极限和全mask算法描述；Harmon Eq去mask符号等，后续读公开实现才能定位，现阶段不称代码bug。

## 第十二批新增需系统处理

- 量化失真分解为Σq(k)[Var(e|k)+||E(e|k)-c_k||²]；不平衡簇不能无条件改为1/K平均。码coverage、熵、perplexity和语义互信息分别测。
- prefix生成MDP、静态数据编码图、图像自然因果模型是三个对象；Bellman条件不能由空间码之间相关性直接否定。
- scorefunction梯度、importance ratio与KL代理各自作用：Selftok Eq20未显式给logπ因子，实际代码尚未核；DDPO使用可求密度的随机转移，确定性ODE需另论。
- 高分辨量化理论的常数依赖源分布/尺度，非均匀分布下固定码率最优点密度与均匀用码未必等价；需后续读原始量化理论。

## 像素接口、分配算法和真实时间

1. 预测空间去VAE、参考图像条件去VAE和最终decode去VAE是三个不同接口；UniCom的公开runtime可用于沿调用链学习。
2. 在线量化的软均衡、hardargmax使用率和标准Sinkhorn行列缩放分开；RF PDFp16伪码已核，实际实现与分配统计待读。
3. 时空patch4帧、残差深度16层、flow噪声t与真实笔画起止分别定义；反事实事件实验不可用通用VBench替代。
4. 跨像素/latent的MSE量纲、按步数收敛、按样本曝光与总计算效率分开；PixelUMM F4/F6的条件限定可作为学习案例。

## 需要集中补学：路径、速率与调度

区分概率路径p_t、CTMC速率、随机mask概率及其采样密度；给定路径的kinetic最优不等于全局生成最优。插入Poisson count/identity loss与maskCE的不同、双时钟条件一致性、有损bidirectionalcache与因果prefixcache、外部GPT2PPL与flow似然均需按公式及实现学习。Muddit PDF与cosmask代码是具体案例；FullFlow的teacherreferenceFID需与真图FID分别命名。

## 部署与评价效度补学

区分total/active/trainable参数、裸权重字节、编译图精度、按需加载/内存驻留和peakRSS，磁盘下载量不等于RAM。GenEval的检测/局部颜色分类不等价全图CLIP相似度；人类一致率、kappa、全体一致子集与全分布效度各需限定。多奖励归一不能自动解决reward相关/测试提示重用。

## 梯度投影与奖励顺序

需区分当前梯度、历史动量、实际旧任务梯度，以及欧氏投影与Adam对角预条件后的更新。带epsilon分母的投影与无epsilon正交证明不能直接互换；无新增持久状态也不等价于零临时内存。OCR字符计数集合奖励会忽略计数单位内部的排列，需要核实际分词/空间对齐。

## 后训练公式补学

logσ(a)+logσ(b)一般不等于logσ(ab)；正乘积不能区分双正/双负。潜变量链式概率要对latent求和/积分才能得到边缘分布。互信息恒等式、条件NLL上界、flowMSE训练替代与共享参数Pareto增益是不同命题。sqrt在[.6,1]压缩差异；概率几何平均控制长度仍含语言先验。no_grad阻断本次反传不冻结后续参数更新。

## 联合优化需要补的数学条件

两梯度凸组合的闭式权重须与所乘向量对应；Pareto驻点只必要条件。上尾截断正态Var=1+zλ−λ²，不普遍≤尾概率p。乘性指数阈值Tnext=T^(1+μΔ)在线性化时不能漏lnT*；reward均值增加不等价梯度范数增加。组均值是随机量，中心化advantage含跨样本协方差。重加权概率须归一；条件速度的期望不可直接解释为终图模糊平均。

## 评价与数据处理的逻辑边界

信息经过通道不增加，并不推出固定非最优解码器准确率必下降；去干扰可能令其更容易读出同一信息。原图问答只宜作参考。层级平均与micro不同，分布距离归一到0–100也不等价概率准确率；总体分母、stage实例和subject数需区分。点态可表示参数扰动不等于实际固定风险梯度学习。

## 多语言和评价统计

字符/grapheme/byte应分别定义，不能由中文双字节推字符ED归一。清符号改变测量目标；平均分乘积不等价全部必要条件的合取。Kendalltau-b可处理ties，全部常数组的未定义问题需单列；RC自身也需并列处理规则。相关系数差.007无CI不足称显著；五项或多条件全对率要控制条件数量/难度。

## 长程与多任务优化

注意力熵需考虑key数，重尾/相关注意力不直接等于因果必要条件；两两边缘一般不能唯一识别多模态联合分布。loss倒数与收敛斜率权重不等价梯度冲突消除；累积/轮转比较要分别控制样本、更新次数和计算。语义上下文保留时总成本仍会增长。

## 归一、统计单位与编辑折中

CoMM印刷式的求和项数与均值系数不一致，须同时核索引和代码；图像出现次数/唯一图/文字三元组/最终图对数量分别统计。FID、CIDEr、VQA均值不称统一准确率；CLIP保持—编辑曲线不可单点或单指标代替。旧基座微调样本不能当全部预训练成本。

## 理论假设与控制频率

Fourier特征的有限线性张成与全部三角多项式不同，需含正确频率/常数和函数空间；atan2稳定依局部分支与扰动范围，Lipschitz常数随K增大不保证数值鲁棒。MUNI先验成本—互信息单调为flow情形附加假设。动作块吞吐、观测更新和闭环延迟分别计算；可逆颜色编码仍经过有损VAE。

## 确定性latent与概率代理

Monet公式把旧hidden视为固定方差Gaussian动作，发布runner却取均值；需区分可优化距离代理与真实随机行为策略。相同context/参数时距离为零，其梯度也为零，文本更新或数值差异可打破等式；因此不能直接断言训练无效。下一步核两阶段teacher-forcing和旧logprob的真实执行路径。

## 多维评分的锚定与相关检验

GapEval印刷附录联合学θ/β/µ时，有每模态平移对称性；跨模态能力差需锚定，且仅两项全局β不等逐题难度。见[推导条件](glyph_conditions_paired_benchmarks_and_structural_targets_2026-10-20.md)，实现是否有额外约束待核。VGUBench离散评分有ties，Spearman简式不能默认适用；去重答案恢复为多题后的相关需cluster推断，p小与效应大分开。

## Oracle信息论与实际生成误差

VisWorld的条件熵非增与KL链式分解在其oracle/state假设下成立；不能推出有误差生成图的实际答案准确率非减。完全观测确定过程没有额外信息，有限算力表示便利仍可有收益。UniAR AR效率不含FM像素decoder，理论码本2^64也不等实际利用率。

## 冻结目标、可训练映射与运动参数化

LatentUMM固定E*两输入距离对UMM参数无梯度；指定代码通过可训练映射改成有梯度的代理，还不能证明等同真实RGB生成回环。DIVA信息分解是建模假设，unique独立可由collapse达成，必须检验信息保留。书写速度与曲率须保真实Δt/采样定义；同形重参数化能改变速度，不应从单张字图声称唯一还原时间。

## 代理真值、检索空间与顺序参数化

Ketaba附录以集成输出为PseudoGT分析个体，无法据此独立证明集成每行正确；官方隐藏GT成绩与该诊断分开。UniCalli内容latent最近邻字库依字库覆盖和位置切分，公开base与论文三模态版本不同。DrawThisFirst的累计弧长、OnOff点距压力proxy与真实时间/力不同；再参数化和采样密度可能改proxy而终态不变，应通过保持几何的干预检验。

## 条件数据、可微路径与评价分母

UMText RCI含传统Canny，需追实现确认哪些路径停止梯度、哪些保持可微，不能单凭损失名推论优化有效。Calligraphy Bench SVG/中线来自Make Me a Hanzi而书家图像来自独立图像库，canonical轨迹与书法变体未必逐笔等价。L176将时间/距离编码颜色但去掉抬笔间隔，XMPFont类别顺序不含坐标，二者均不能自动恢复真实动作。


## 第三十批补充

完整JSD凸性结论不能自动移到topK/entryclip/EMA代理优化。Bézier控制点可在曲线外，逐控制点SDF约束的几何影响需单独验证。50fps重复播放不增加原生视觉采样信息；短接触事件的不可识别性需用实际观测算子分析。


## 第三十一批补充

静态PDE扩散参数时间、模型去噪时间与笔尖物理时间应区分。共享latent平方差在独立采样下同时惩罚均值差与方差。AIoU只评形状，LDTW仍混合几何和顺序；规范笔序需事件定义。


## 第三十二批补充

不显著不等统计等效；重复题项/参与者需相关模型。min/max几乎处处可微，可用subgradient；τsigmoid范围≤τ，不能作为普遍softmin/max。分析连续噪声条件、后验采样方差、固定长度与EOS时应分别说明职责。


## 第三十三批补充

ε预测必须经x_t与α转换成x0才可解释为clean latent；直接VAEdecode ε不能自动等同重建图。IS方向与实现需对应；unsigned角度约束不保证有向拓扑。相邻帧高相似可由静止取得，指标需同时约束运动。延迟下降与吞吐上升分母不同。


## 第三十四批补充

Flow时间方向是符号约定，BAGEL data→noise与Show-o2 noise→data需统一后比velocity。active与total参数、packed tokens与batch数、GPUh与wallh、推理seed与训练seed不同。PCA投影相近不证明同构；重建复制捷径、阈值涌现与真正因果转移需受控实验。


## 第三十五批补充

NFE比不自动等walltime；KV预算/managedKV/临时workspace/peakVRAM需分母明确。逻辑mask/fakequant参考与物理packed实现可能策略不同。初图detach仍因共享参数漂移；p不显著不能证明等价，线性probe可解码不等模型可靠自判。


## 第三十六批补充

掩码AND/OR改变保留集合，时间sample/average改变快事件表示；代码默认和论文须分版本核。顺序条件分解可表示联合概率，实际模型限制不能写理论不可能。thinking registers不等显式推理，VAE平移等变仅设计近似；人评近半且无CI不证明等价。


## 第三十七批补充

自生成历史对齐、历史writer梯度、完整rolloutBPTT互不等价；随机exit留训练推理近似，前向bf16恢复不证明梯度精确。精确ODE flow半群与Euler组合误差有别，论文对称loss不保证实现双支反传。GRPO嵌入相似代理与离散约束oracle可验证性分层，单GT路径奖励会误罚合法多解。


## 第三十八批补充

平均速度沿marginal characteristic积分，conditional直线不保证marginal直线；JVP输入条件与切向需按实现链式求导。原MF等价重写和iMF改变JVP输入分开，辅助头停梯度后需独立loss。冻结参数仍可对输入求导，CTM prediction经EMA s→0不能误detach。角色共享限制的局部位移几何不同于参数/算力公平，样本余弦不等聚合梯度。


## 第三十九批补充

离散速度是分类状态转移rate，δ+h·u需合法概率，fixed-t stationary与并行小步近似分开；全mask时间无关仅特定path。Sway改变生成ODE节点，physical时间另有定义；NFE/solver步/CFG批大小分开。TeaCache以t调制input估残差变化，校准系数为经验关系，poly1d不是拟合优化。clDice hard定理与soft有限k/仅前景经验简化分开，静态mask无时间方向，Euler正文/补充定义有待核不一致。


## 第四十批补充

Reynolds形状导数与弧长Jacobian/滤波核、最近点隐式导数条件；解析预滤conflation与MC方差。曲线位置t/优化迭代/图层顺序/实体时间分开。Gaussian配对插值与Xing凸性、重分配启发不等全局最优，导出SVG不自动严格等价。3形状量展开12坐标不增加独立动作维数。模拟拟合差/真实执行差、图像余弦距离/文本CLIPScore差分别定义，代理相关性不能证明学到物理。


## 第四十一批补充

连续密度NLL可负；Nmax归一与EOS mask影响跨分布可比性。KL标量floor不同逐维free-bits；方差温度与标准差缩放分清。可微模拟环境不等物理动力学，终图奖励不识别规范过程。百分点与相对百分比/非劣性检验区分。LoRA矩阵shape可核rank/cross维，不能反推alpha/训练集/唯一底座；卡片/代码默认/原训练日志分层。


## 第四十二批补充

集合排列不变loss、alpha渲染有序和规范事件是不同层面；STE为近似梯度。单笔PSNR不能替代整图/视频；Sinkhorn固定迭代近似与精确OT/去偏divergence区分。WGAN势函数符号需随minD/maxreward一致，最优势非唯一不保证学习收益；同预训练家族评价存在相关性。


## 第四十三批补充

离散ELBO界/连续ODE密度/均匀去量化K、Hutchinson无偏log估计与指数化偏差分别处理；PC同NFE才解释收益。连续性方程给边缘而非joint路径，CFM条件期望与θ无关常数、conditional OT与global OT不同。RF Jensen凸成本和历次最小直度界依理想假设，FID可退化；流t与视频τ分开。


## 第四十四批补充

感知压缩与信息损失、生成FID／重建rFID、EMA权重与EMA target分开。DiT近似GFLOPS对照并非等参数；CT渐近loss对应需真score／平滑，不是有限N精确替代。DPM高阶误差仅相对学得ODE，NFE／步数／阶、终点ε与时刻映射分开；代码默认后续算法不可倒写原文。


## 第四十五批补充

C3D-FID与I3D-FVD/图像Inception FID分开，train/val参考与IS split双值分开。噪声时间/真实帧/潜时间压缩/笔事件不同；PC步数需加corrector与重建反传成本。冻结空间θ不代表全部pipeline冻结、初始化恒等不代表训练后恒等；帧平滑/CLIP相似不能替代运动幅度或笔事件。


## 第四十六批补充

几何压缩/位置token/潜元素/字节与完整计算分开；因果VAE不等full-attention生成因果。邻帧L1会混入真实运动，需GT差分/静止反例；EUS是特定均衡条件下的分层时刻采样。expert AdaLN不等稀疏MoE，公开trainer iid不等论文EUS；scale/invert、dtype/heads/timeembed与帧数跨版本不能拼。


## 第四十七批补充

Wan-VAE过去特征缓存、扩散采样近似attention/CFG缓存、Streamer窗口/一致性蒸馏分别具有不同假设。FM训练回归不取消采样求解，也不保证精确MLE；逐通道latent mean/std与单标量尺度分开。win-rate-gap带负值不能解释普通获胜概率，缺平局公式不转换；原图PSNR、表步数与帧率冲突按版本保留。


## 第四十八批补充

LoRA的ΔW低秩不要求总W低秩；DoRA模长缩放可能使总ΔW超r秩，完整norm投影与detach方向梯度分开。rsLoRA SGD首步/条件渐近量级不保证AdamW泛化或最大rank最优。QLoRA冻结NF4存储与BF16计算/activation分开；分页不是无成本。训练PPL、裁判相对分、Elo顺序重排误差及独立任务泛化分开。


## 第四十九批补充

零残差初始化函数相等不保证后续行为无损；外层zero权重与内层分支梯度不同步。冻结参数与输入梯度分开。CFG原w与常用s偏移1，理想每噪声score不保证有限步终点精确幂密度；FID最佳与强引导IS最佳不同。ControlNet hint/RW论文代码及CFG图例512/表1024冲突保留，不用库默认猜历史条件。


## 第五十批补充

理想D密度比/JSD与有限G参数训练分开，非饱和loss不沿用全部minimax性质，D支撑外不唯一。VAE ELBO后验gap、摊销/族误差、无偏梯度和倒数/log似然估计分别理解；MAP权重与FullVB扩展分开，任意β/感知/对抗目标不自动继承原恒等分解。Parzen/ELBO/MC边缘评价不可跨协议排名。


## 第五十一批补充

四model汇总Pearson/秩相关与逐样本校准不同；VBench A5主体重算Pearson.9650757、Spearman.8，原caption称Spearman需代码核。整帧相似度/代理光流/插帧不直接保证局部过程，分母可评覆盖率必报。FVD两矩近似/有限样本偏差/固定层与预处理、batch16和评价总N分别理解；BAIR50点经验非通用。


## 第五十二批补充

ContentBias：S/ST空间FID近似匹配不等完全控制所有图像因素；敏感性不等真实排序校准；经验null space不等线性空间。softmax权重优化只改选择，冻结只固定无运动，独立参考与唯一N/有效样本量需报。主FeatureStats协方差除N、辅助torch cov除N−1分开；当前默认VideoMAE经过监督微调。


## 第五十三批补充

默认设置/等预算公平、按模型汇总相关/逐片校准、预设外观标签/真实人群属性、NA分母/有限N分开。Binomial(10,.5)均匀二类下gender分数期望.75390625为解析示例，无模型复现。skin正文未归一和代码归一差别、整数多数阈值须逐版本记录。


## 第五十四批补充

动作顺序四点Pearson.993138665、Spearman1，与表名称冲突；分解问题仍共享VLM误差。初始状态筛后条件分数、无检测满分、部分分及系统异常默认正常需覆盖率，不能合并为无条件成功。


## 第五十五批补充

区分4.4T数据/9.2T暴露，子项4.8T口径待解释；总体435/362/251得58.8而非子集60.4。QKnorm/输出zloss作用不同。6ND/拟合parity非实测速度；连续图像仍有VAE压缩，大patch改变图像暴露。


## 第五十六批补充

反向后验通常仍依赖x0，不能直接套正向Markov独立；转移矩阵须按K+1状态核行和，Show-o β=0实际方案与β>0推广问题分列。CFG两种logit系数差1；每任务步相同不等总预算相同。GQA48.7→59.1相对21.36%，保留正式正文30%的冲突。


## 第五十七批补充

静态图→轨迹的多解性、20ms幻想时间与真实动力学、proxy识别与规范顺序；best-seed与3seed均值；LLM偏好含tie/目标词汇影响。每类2样本hard accuracy均值.82的类别SD至少.24，TI±.04的统计口径待代码确认。


## 第五十八批补充

Bézier几何参数与真实时间，最小二乘残差/分段不保证规范事件；CLIP骨干/样本和解析失败对跨表比较的影响；协作partial墨迹量混杂。关键帧下事件不可观测、重建误差与过程真实性分离，Prodigy/AdamW和条件采样配置版本对齐。


## 第五十九批补充

set-to-set查询与跨请求一致性；因果VAE投影不自动为因果动作模型；多解历史的重建评价、数字编辑与单调墨迹。ResidualVQ片段/规范stroke差别、CLIP特征Fréchet、自码本Recall/代码等价性、CR方向与stop-gradient符号核查。


## 第六十批补充

计数向量的排列不变性与顺序不可辨识性；优化迭代与动作时间；SDS忽略UNet Jacobian但保留VAE/渲染梯度；共享style的多分支CFG不等正交属性控制。偏好份额/人画判断比例和准确率不同，validation选择与test冻结。


## 第六十一批补充（2026-10-21）

未见字体/内容/作者的三种泛化轴；Fréchet整体计算不等分组算术平均；D_CER/WER下游训练协议受内容/多样性/域距/OCR预算影响。3D图像切片与物理时间、内容/风格解耦需要独立probe，固定顺序融合与CFG路径对齐。


## 第六十二批补充（2026-10-21）

统一主目标与分词器/后训练/后处理损失分别记录；经验loss scaling不等任务保证；等样本/估算FLOPs/真实walltime与预训成本分别比较。空间token序、模拟action与真实笔顺事件分开。未报告消融的书面审查注明缺失，不能补造已验证机制。


## 第六十三批补充（2026-10-21）

区域OCR正确不等全图文字正确；NED相似度方向、百分点/相对提升和>100百分比的定义分别核实。inv_mask固定分母改变有效权重；feature增益不等attention-score温度，独立cross-attn不能套联合token稀释论证。离散反思不自动实现score-function梯度，正对齐假设不等已证明收益。


## 第六十四批补充（2026-10-21）

四选风格识别/找真/找假不同；p不显著不证明等效，需效应界限/功效/题项相关。百分比提升需明确准确率pp/相对变化/错误率下降；同图额外条件会改变难度。Diffusion噪声预测与重建空间MSE不能在实现不明时替换，冻结LoRA原权不保证功能不遗忘。


## 第六十五批补充（2026-10-21）

高斯方差与标准差、mask1含义和注入时序需按版本核；分布收敛/多解真实感/逐样本恢复分别定义。线性子空间可识别性与谱范数收缩、近似误差地板；(E C)的逆不等于E(C逆)，用原目标正规方程复核闭式解。存在Lebesgue密度不推出全空间正密度。


## 第六十六批补充（2026-10-21）

oracle选帧/pass@k/有效输出覆盖分列；有限样本比例粒度取决聚合分母，文件数不等全部API调用。回归主效应与层间交互、FDR边界/聚合偏差、控制Length后的条件效应；地板分数接近不证等效，词长是答案空间先验，style/writer混杂须干预。


## 第六十七批补充（2026-10-21）

GT脚手架同时改变信息/表示/预算；旋转新视角不等同原视角的等信息重编码。平均改善与子任务下降兼容，负面结果解释仍需干预。CE/MSE同系数但各自token归约不等梯度平衡；代码默认与实际run、模型卡参数与运行构造、元数据计数与原样本审计必须分列。


## 第六十八批补充（2026-10-21）

E_q log(p/q)=−KL，不能把正MSE当似然下界然后称最小化即增下界；充分表达/全局最优的同时代理结论不等有限网络稳定。MCG降模型梯度方差仍依赖模型未来正确，奖励停留偏差、跨维求和CRPS与分项能力要分开。


## 第六十九批补充（2026-10-21）

G038再次核到ELBO log比值应为−KL(q||p)，印刷方向/符号错误；分解路径一致性亦为作者承认的未解决条件。Gaussian后验频谱收缩依赖信号协方差，白噪声本身无低频偏好；分数组合MLE需要同一真目标/无偏Gaussian/已知协方差，实际调参HG未验证这些条件。


## 第七十批补充（2026-10-21）

同任务曝光、总FLOPs、预训teacher先验、生成压缩上限是不同控制变量。理解/生成共享接口不直接证明双向迁移；RF时间/MAR空间unmask顺序不当真实笔事件。Harmon仍用VAE，64外层与100步小扩散头的成本分列；JanusFlow增强LLM与REPA/范式贡献分开。


## 第七十一批补充（2026-10-21）

EDM的积分误差、score误差与下游笔事件不可混用；λcout²=1不等噪声均匀采样，NFE摘要不等同点FID，三次最小/检查点选择不等训练seed CI。Heun局部/全局阶及末步σ0、离散噪声rounding保留。


## 第七十二批补充（2026-10-21）

DDPO单步IS/冻结旧状态后续分布为近策略surrogate，非一般完整轨迹无偏校正；mean-logdensity的exp是联合比1/d次方，不能以学习率缩放抹去clip差异。训练reward/独立任务效用、prompt标准化与选择统计分开。


## 第七十三批补充（2026-10-21）

OrderAcc的笔数/IoU/全序不含笔内方向/contact；轨迹采样密度、类别与笔数复杂度、起点来源/骨干是独立混杂。因果AR序列不限制空间负offset。L004噪声/取整/pen定义与缺supp须保留，不能用常用实现代填。


## 第七十四批补充（2026-10-21）

逐笔反馈已有前作但缺独立因果消融；集合无序与笔内PE/等变应区分。指数距离场gamma0改变输入和目标，norm消融同时去box；PR最近球判定不等所有球并集，Inception不同权重不能混排行。


## 第七十五批补充（2026-10-21）

StrokeBank正/负margin与hinge符号相反、w非负未定义；真假判别50%不证明分布等价。Loomis v3 DDC引用旧作而非新PDP；终态锚定/注意力相关不能证明过程/因果，等epoch初期反例、人评重复票与test-as-val映射需区分事实和风险。


## 第七十六批补充（2026-10-21）

logp比值与exp差、平均token logp和序列概率、KL old与fixed reference须分清；后续通用RL实现不等于原三任务配置。GenEval主表/引言不一致、pp和relative、NFE与耗时/文本成本、单轮图像与单次网络forward不混同。


## 第七十七批补充（2026-10-21）

1−CER、位置字符准确与EM不同，原始/清理预测影响；CSV同句/混入字符需保存；训练split未固定而独立评估重新seed42不能保证留出，尚未证明原表泄漏。类mask与实例/动作非唯一、字ID任意编号/识别噪声控制，TSR/FSR匹配和validation/test口径需清楚。


第七十八批（2026-10-21）：路径联合/边缘分布、log似然/概率、sqrt线性噪声调度、CFG默认/论文评估、RICES条件与评估std/训练seed需区分。见[审查](versatile_diffusion_and_emu_evidence_audit_2026-10-21.md)和[单篇L075](../reviews/L075.md)、[L077](../reviews/L077.md)。


第七十九批（2026-10-21）：top_k300是候选词表截断，所查实现max_new_tokens默认200；数据源体量/实际曝光与概率/log似然区分。见[审查](lavit_dynamic_tokens_and_version_audit_2026-10-21.md)和[单篇L079](../reviews/L079.md)。


第八十批（2026-10-21）：重建rFID不能推出生成gFID；逆时间flow符号，模拟/实测曲线及SSIM数据范围分别检查。见[审查](uniflow_reconstruction_generation_tradeoff_audit_2026-10-21.md)和[单篇L072](../reviews/L072.md)。


第八十一批（2026-10-21）：综合分与相对百分比、局部滑窗/整图聚类利用率、尺度相关CFG和图文矛盾。见[审查](tokenflow_shared_indices_and_claim_audit_2026-10-21.md)和[单篇L094](../reviews/L094.md)。


第八十二批（2026-10-21）：负方向质量指标相关性符号、规模混杂、条件丢弃概率和推理CFG区别。见[审查](metamorph_synergy_and_data_budget_audit_2026-10-21.md)和[单篇L090](../reviews/L090.md)。


第八十三批（2026-10-21）：负loglikelihood变分上界、原始归属、条件期望及综述检索可复核性。见[审查](diffusion_vision_survey_scope_and_attribution_audit_2026-10-21.md)和[单篇G022](../reviews/G022.md)。


第八十四批（2026-10-21）：NFE表头、空条件/zero-conv、冻结前向成本和EMA方向。见[审查](diffusion_efficiency_full_pipeline_audit_2026-10-21.md)和[单篇G023](../reviews/G023.md)。


第八十五批（2026-10-21）：CFG尺度定义、噪声重采、31块构造与文字codec重建指标。见[审查](unidiffuser_distribution_cfg_and_codec_audit_2026-10-21.md)和[单篇L076](../reviews/L076.md)。


第八十六批（2026-10-21）：latent帧数、256画布量化/重采样、同像素覆盖、绝对分差/相对百分比及冻结图文矛盾。见[审查](tora_motion_binding_and_process_boundary_audit_2026-10-21.md)、[L034](../reviews/L034.md)/[L035](../reviews/L035.md)。


第八十七批（2026-10-21）：时间池化后tau、ETE提取/单位、伪标签偏差、固定依赖默认与未锁模型revision。见[审查](tora3_kinematics_flow_and_nonpaper_adapter_audit_2026-10-21.md)、[G039](../reviews/G039.md)/[R12](../reviews/R12.md)。


第八十八批（2026-10-21）：SE3单位/gauge、GUI位移位置约定、投票分母及HF权重文件映射。见[审查](motionctrl_camera_object_and_observability_audit_2026-10-21.md)、[L039](../reviews/L039.md)。


第八十九批（2026-10-21）：UIO2音频码本/输入、batch-token口径；AnyGPT100K/108K、音乐规模及许可未决，正式词表旧冲突解除。见[审查](unified_io2_anygpt_discrete_interfaces_and_protocol_audit_2026-10-21.md)、[L058](../reviews/L058.md)/[L059](../reviews/L059.md)。


第九十批（2026-10-21）：来源—管线有限样本差异、正式/发布学习率与batch、投影维/表差值未决。见[审查](seedx_unitok_seeddata_representation_and_process_audit_2026-10-21.md)、[L060](../reviews/L060.md)/[L061](../reviews/L061.md)/[G040](../reviews/G040.md)。


第九十一批（2026-10-21）：论文/代码tone与LR、部件/刚体归因、模板误差和无源码/多seed边界。见[审查](semantic_modal_typography_static_animation_and_writing_2026-10-21.md)、[L051](../reviews/L051.md)/[L052](../reviews/L052.md)。


第九十二批（2026-10-21）：候选协议/量化分母、20/25图、epoch-step/optimizer、generic配方及checkpoint对应未决。见[审查](dsfusion_adversarial_typography_and_express_audit_2026-10-21.md)、[G041](../reviews/G041.md)。


第九十三批（2026-10-21）：embedding实际漂移/覆盖配置、target min/mean/阈值标度、未发布完整训练及多seed。见[审查](metaqueries_unifiedio_transfer_and_freezing_audit_2026-10-21.md)、[L062](../reviews/L062.md)、[L074](../reviews/L074.md)。
