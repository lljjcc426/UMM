# 汉字部件生成—识别联合优化：树几何、负迁移与公开协议

第一百四十七批完成[L181](../reviews/L181.md)明确范围核心三遍及五项书面记录。[结构化证据](../../data/chinese_radical_joint_tpe_geometry_and_negative_transfer_audit_2026-10-23.json)。357目录（330论文／研究、27资源），256核心/259书面含未通过项；未确认核心74论文／研究+27资源，资源另按制品审查。无目录新增、文件删除、权重下载或模型执行。

来源：[作者正式11页PDF](https://sprateam-ustc.github.io/Publications/Mobai-2023.pdf)、[DOI](https://doi.org/10.1016/j.patcog.2023.109538)、[固定官方代码](https://github.com/SPRATeam-USTC/G-R-Joint-Optimization/tree/03b07e7156cf96da6420ee9b794aa75a72256c44)。Pattern Recognition140(2023)109538，指定年份/体系的期刊分区未另核。

## 研究问题

汉字静态单字图像与部件/空间结构描述之间的双向映射：用对称但参数独立的生成器RTN-G和识别器RTN-R共同训练，改善未见字组合、印刷体/场景字/离线手写字的图像重建和识别。部件caption为结构token的深度优先序列，TPE为部件树位置；该序列不表示书写笔顺，FPS是静态图像处理吞吐。没有视频生成、笔画时间/轨迹、单共享参数基础UMM或GRPO强化学习。

## 动机与已有不足

递归RCN可能弱化长程与叶节点部件，整字封闭类别识别器难处理未见类别；单独生成与识别未用逆任务的对应特征。作者提出Transformer全局部件交互与双向训练，将部件/图像语义和注意力联系起来。普通1D序列距离不直接对应树上的父子/子树距离，因此设计TPE。动机合理性与实验证据分开；不能把整字分类器的封闭词表限制推广为所有字体渲染器或现代开放词表方法无法处理未见字。

## 核心贡献

RTN-G部件Transformer生成静态RGB，配RTN-R自回归部件识别；在部件特征、图像特征及转置注意力上施对齐，InfoNCE负样本来自同batch，双向caption→image→caption/image→caption→image重建。L=Lg+Lr+α(Lc+βLd)，另用根/左右层基向量沿祖先路径平均的TPE。新增是该具体汉字联合设计和TPE；attention、InfoNCE与dual learning已有基础，双网联合不等单一共享UMM。论文报告的遮挡负迁移及公开实现未完成均应纳入贡献边界。

## 输入、主要模块、输出及公式

生成：部件/结构SC+TPE→12层encoder→上下文；字体/背景/颜色/角度属性形成K16个画布query+PE→12层decoder cross-attention→4×4视觉特征→七块转置卷积→32²RGB。识别：32²RGB→VGG16→6层Transformer encoder+PE→6层AR decoder，先前部件/结构+TPE→下一token→caption。对齐对称部件/图像表征与Ag/Ar转置；输入真caption及图像都有直接监督，不能写成纯无监督。Eq1–8为表征/标准attention/条件概率，Eq9对比映射，Eq10–15损失，Eq16–24位置编码及证明。Eq11/15写L2范数，文字称MSE；Eq14注意力为−γa log(1−||Ar^T−Ag||₂/(MNN))，不能将印刷式直接抄成普通MSE；实际源码另用末层masked MSE。

## 模型结构

正式T1：G encoder/decoder各12层4head，R各6层8head，D512；生成FFN512→1024→512、识别512→512→512；VGG16图像提取，4×4背景query，七个上采样块stride(2,1,2,1,1,2,1)/kernel(3,3,3,3,3,5,5)。输出32×32×3。624部件+10空间结构。公开joint_config为两网均8层4head/D512，FREEZE_ENCODER=True并在SGD排除G_Encoder，权重J=.01/R_F=.05/J_F=.01，与正式α=.5/β=.2不构成同一配置。代码另有背景图back_fn、形变axy、RGB及随机种子条件；属性侧信息不能概括为任意自然语言单独生成。无参数总量或完整正式checkpoint说明。

## 数据集和划分

印刷集：论文称27533字/8字体（Hei/Song/Kai/Deng/Fangsong/Li/Yao/Youyuan），训练180052图22933类、测试31760图4172未见类；类数相加27105与27533差428，过滤/缺字清单未给，不能自行填成缺失字体。零样本指未见字类组合，8字体并非已证未见字体测试。CTW报告总1018402字/6属性，train760107图3580类、val52765图2015类、test103519图；识别用全部可用训练，生成/联合去低质且仅distorted/raised子集，实际子集大小未给；字体预训练分类器、颜色统计提供属性。手写CASIAHWDB1.0/1.1共2674784图，ICDAR2013词内，HWDB1.2选3277/3319非通用字类作词外；未见类中各部件覆盖率未齐。3000随机新/不存在caption称验证集，增广Out又包含同节随机caption，需独立构建清单明确验证/增广是否复用，不能仅据这点判真实测试泄漏。各离线增广集5M图。未下载图像或完整构建数据；正文Dataavailability为按请求提供。

## 实验指标

生成MSE/SSIM（32²匹配目标图，依赖归一/对齐，不能单独验证字义/拓扑）；识别Top1/Top5，T5明确radical expression recognition accuracy，字符描述树须整体正确，不等逐笔正确率。CTW按occluded/background/distorted/raised/wordart/handwritten及all分组。FPS衡量单模型测试吞吐，不是生成视频的帧一致指标。无逐笔事件、轨迹、时间、文字视频、字符级人评合法性、独立OCR/部件oracle、不同写者样式保真或训练多seedCI。公开validate主要exact caption及编辑距离/WER，含i==10调试停止；未提供完整SSIM/Top5/所有官方split复现流程，不能以该脚本默认跑分充作正式表格。

## 对比方法

生成RCN、规则SynthText、SRNet风格迁移；识别ResNet50/DenseNet、RAN/RTN-R、手写Direct+ConvNet/VGG14RAN/DenseRAN/TAN。T4仅两词内+两词外示例，SynthText需字体、SRNet需字图、RTN-G仍需部件caption与属性，输入/能力边界不同；空单元不足以证明所有渲染器永远无法渲染CTW词外合法字。识别其他方法成绩选自已发表论文，非同硬件同训练预算全面重训。重要内部对照为TPE/PE×SIM/DUAL×offline/online×within/out；没有图像质量/数据量/训练计算严格匹配的全部析因，也未和现代SVG结构渲染、扩散字图或强分离模块比较。

## 实验条件

PyTorch1.3/32²/D512/dropout.2/τ.1；α=.5/β=.2/γr=1/γc=1/γa=.8，称按验证调参。印刷b32/1×V10032GB/5h；场景b256/4×V10032GB/30h；手写b256/4×V10032GB/18h。报告时间不等独立重测，同版本各消融预算/epoch、seed、学习率和正式优化器未齐。公开config为SGDlr.1/momentum.1/wd0/400epoch/step100,200,300/gamma.8/gradclip10（utils训练），训练权重/层数/冻结与正式不同，不能用其补写正式设置。部分生成属性从原目标图估计；真实性条件化和开放生成要分开。离线各5M合成图，在线实际生成数、FLOPs/GPUh和磁盘I/O计时未给，少存图不推出总训练计算更低。

## 主结果

T2印刷isolated TPE→joint TPE：MSE .199→.160/SSIM .851→.929/Top1 87.22→93.61（+6.39百分点）/Top5 96.81→98.40。T3 CTW isolated PE87.31/TPE87.44→jointTPE88.64：相对PE+1.33pp、相对TPE+1.20pp；MSE .244→.199/SSIM .723→.858。T5联合SSIM另写.838，不能静默统一成.858；同表MSE .199胜SRNet.212、RCN.311和SynthText.325，FPS G141.7/R92.2，规则SynthText894.4更快。T8手写RTN-R→joint ICDAR2013 96.72→96.88（+.16pp）、HWDB1.2 42.53→44.12（+1.59pp）；TAN96.78/42.88。未见字识别仍仅44.12%，不能概括为已解决稳健零样本。T7Out离线88.42、在线88.91；作者报告点估计，未独立复现。

## 消融、分布分组和定性图

T2印刷SIM单独Top1 90.11/SSIM.887，DUAL89.20/.815，后者SSIM低于isolatedTPE.851；full双TPE93.61/.929，双PE92.55/.913。T3场景SIM87.60/.765，DUAL87.91/.771，方向与印刷SIM更强的相对结论不同；fullPE88.22/TPE88.64。T6 occluded RTN-R73.94→joint72.64（−1.30pp）；wordart84.25→86.95但RAN87.11更高；background84.54→85.13、distorted83.60→83.66、raised78.06→78.92、handwritten66.70→67.27、all87.31→88.64。作者将遮挡退步联系生成能力限制，不应只记录总体正迁移。T7 TPE基线87.44，离线Synth87.32（下降）/SRNet87.68/within87.56/out88.42，joint无额外88.64、onlinewithin88.72/out88.91；jointTop5 T7 92.47与T3/T5 92.44差异未解释。F6/7未见字及注意力，F8粘贴回场景的静态编辑，F9/10四个纠错样例，F11手写终图且作者承认多笔复杂字不足，均无笔顺/运动验证。

## 局限、证明及代码

TPE文字Eq17 Root=sin(2dπ/D)=L1，直接违背所称两两正交；Eq18首左子与根碰撞，Eq19原始内积下根到左右子相似不等，Eq21不能由所印定义推出。Fig5 DFS编号与证明2i+1/2i+2堆编号需区分。公开embed.py实际根freq1、左右深度l基freq2l/2l+1，与纸面不同，不能把Root=L1反例当实际实现结果。即按源码理想正交基修正，原始点积具有深度偏差：D512、结点LL与子LLL内积64，与非相邻祖父root85.333，后者不在Eq23排除集，故其全局邻近严格不等式仍不成立；这是闭式几何检查，不否定TPE经验收益。公开README明确联合部分未完成；joint.py SIM含作者bug注释，loss.py torch.exo且S_X/S_Y/R_G与config权重键不匹配，反向dual将flatten logits直接送GEncoder再long查embedding，缺可核正确离散桥/梯度处理。末层attention MSE与Eq6/14聚合/损失不同。遮挡负迁移、32²细笔丢失、未见合法性/样式可识别、数量/split/SSIM表差异、预算与seed不足仍需补。

## 何种条件下可能有优势

若未见汉字由已见部件/空间规则组成、所需属性可测、图像足够清晰且两个任务梯度/表征可互补，部件生成增加组合覆盖、对齐和双向重建可能提高同域生成/识别。TPE可提供树路径信息，经验优于PE不要求原证明全部成立。若生成器弱于识别器所需遮挡/噪声分布，联合约束会产生负迁移，T6已有证据。对称架构和cycle一致本身不保证语义正确：两网可共同偏差或用隐藏像素信息通信，需外部oracle。少磁盘I/O只支持存储优势假设，未证在线训练总成本更低；无笔画观测时静态部件树不能确定真实书写时间。

## 实验如何证伪假设

锁印刷类/字体名单、CTW过滤子集/目标属性、HWDB新类及部件覆盖，随机caption验证/训练严格分开；同V100预算/优化器/步数与总合成量做SIM×DUAL×TPE/PE×冻结/共享析因，多seed分层CI并同时报生成/识别Pareto。用独立识别器和部件/拓扑oracle排除两网迎合，遮挡训练比例×真实遮挡分布验证负迁移；离线/在线等总前向反传/属性侧信息/5M图量计时，分开磁盘存储与GPU成本。TPE核纸面/代码频率，改正堆/DFS映射及原始点积/余弦假设，用深度和祖先/兄弟/跨子树组合检验别名与距离再做等维度性能对照。对书写再加严格笔画事件监督，同终态正反序、抬落笔/遮挡/执行约束与规则SVG、现代扩散字图、强分离识别/生成基线。以上为方案，未训练/推理或独立复现。

## 研究思路与写作学习

可学习Introduction从未见字的封闭类别困难→部件描述→RCN叶节点瓶颈→对称任务→TPE，Method先两网再联合损失再独立说明树几何，Experiments按Q1组件/Q2基线/Q3增强组织，T6主动解释失败和Conclusion列复杂背景/笔画/行文本/成本未来工作。Claim须用该分布点估计，不把数学证明、注意力示例、人类直觉及显著性混用；+1.33为百分点，期刊论文不自动保证式子正确。记录已存在部件树+生成识别联合训练，避免把宽泛协同重新包装为首创；新问题需落到可观测时序/执行和强基线的因果收益。

## 实际阅读范围

正式作者11页PDF1909959bytes；Abstract/§1–7全部研究正文及Dataavailability/声明，T1–8/Eq1–24/F1–11/全部图注；实际PDFp1–10共10页，覆盖框架/全部表/公式/案例，p11参考文献定位未逐篇独立读。官方当前main已核仍03b07e7/2023-03-15，58项完整树；README、embed.py完整、joint.py forward/pred/树遍历、contrastive、config/optimizer、generator/recognizer结构/forward、loss.py完整、utils训练/测试及core validate、数据解析/归一定向读；未声称全库逐行、下载权重/数据、执行训练或复现。正式和公开参数/损失差别已限定。相关追引RCN2021/TAN/ACPR2017dual待正式源；L178 TPAMI Drawing and Recognizing已在主目录，先去重。

## 三个结论的证据层级

| 问题 | 原文或源码证据 | 可以得到的结论 |
| --- | --- | --- |
| 联合训练能否有益 | T2印刷87.22→93.61；T3CTW同TPE87.44→88.64；T8词外42.53→44.12 | 这些配置的点估计改善，不能自动扩展到所有分布/现代强基线 |
| 是否存在负迁移 | T6遮挡73.94→72.64；T2DUAL单独SSIM .815低于isolated .851 | 总体收益可与子分布损失并存；需分层分析 |
| TPE几何证明是否成立 | Eq17 Root=L1；代码频率不同；Eq19采用原始点积 | 所印正交前提不成立，源码版本应独立分析；不据此否定TPE表中经验收益 |
| 在线增强是否更便宜 | 每离线集5M图，作者论述少磁盘I/O；未给等GPUh计时 | 可记录存储假设，尚无充分总训练效率证明 |
| 是否复现了论文 | README称joint未完成；源码SIM和dual桥/权重存在差异 | 本轮仅阅读审查，正式训练实现和全部指标仍需补齐 |

## 树几何闭式复核

纸面Eq17的Root=sin(2πd/D)，L1=sin((4−2)πd/D)，因此两者相同。首左子(Root+L1)/2=Root；右子(Root+R1)/2不同，在Eq19未归一的内积下根到左右子相等的结论不能由原定义推出。该问题已在实际PDFp6核到，完整源码另用不同频率。

源码用单位深度方向的不同正弦频率，再沿祖先路径平均。以理想精确π、D512为例，LL路径基频为(1,2,4)，子LLL为(1,2,4,6)，祖父root为(1)。每个基向量平方范数256：φ(LL,LLL)=256/4=64，φ(LL,root)=256/3≈85.333。按堆编号i=3、child=7、grandparent=0，0不在Eq23所排除的自身/父/直接子集中，邻近差为−21.333，未满足其全局严格大于0主张。这里检查的是既定原始内积；改为余弦、改变路径缩放或缩小比较结点范围都需要重新声明命题和实验。该计算没有加载模型或做训练。

图5序列编号为DFS，证明表达2i+1/2i+2为堆编号，实际dataset.tree_node将DFS序列映射到堆位置。三种索引分别记录，避免将结构遍历误写为笔顺。

## 公开版本的具体边界

README日期2023-03-15，当前main仍03b07e7，作者明确说明joint未完全整理、仅供参考。joint.py对比支路含原作者bug注释；loss.py包含torch.exo，返回R_G/S_X/S_Y而当前权重配置未给同名键；GEncoder把输入long后查embedding，反向dual却直接传flatten logits。公开末层attention masked MSE与论文Eq6/14聚合/损失表达不同，8层4head及冻结GEncoder也不同于正式12/6层和4/8head。validate有i==10停止，不能作为完整测试协议。以上是静态阅读证据，未执行外部代码，也不声称这些文件就是正式表格所用私有版本。

## 对我们的研究和追引队列

生成—识别双向优化、部件树、未见组合增强均已有明确前作。后续创新需解释严格RGB时序可观测性、笔画事件/真实执行及共享UMM相对强分离模型的收益；32²终图、结构caption或静态FPS不提供该证据。遮挡负迁移提示生成器能力和真实评测分布必须单独控制。

补读队列增加RCN（ICDAR2021）、TAN（TMM2022/正式年卷待核）、2017ACPR汉字生成识别dual及相关InfoNCE/双向学习理论；L178《Drawing and recognizing Chinese characters with recurrent neural network》已在主目录，按现有记录关联，避免重复计数。下一批继续L182 STRIVE视频场景文字替换，并补L183 CONSTANT、未完成UMM/扩散flow/视频/绘画/语料资源队列；未经实际精读的追引不计完成。
