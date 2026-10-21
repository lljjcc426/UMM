# Representation Forcing：协同基线、离散前缀与量化伪代码

第一百二十一批完成[L106](../reviews/L106.md)固定v4核心三遍及五项书面记录。[结构化证据](../../data/representation_forcing_synergy_and_quantization_audit_2026-10-22.json)。357目录（330论文／研究、27资源），230核心/233书面含未通过项，127条未确认核心（含资源）。没有新增目录、删除文件、下载权重或运行模型。

## 来源及实际阅读范围

固定[2605.31604v4](https://arxiv.org/abs/2605.31604v4)，2026-07-03，完整16页。Abstract/§1–5、Eq1–3、T1/2/3(a–e)、F1–4图注，实际PDF AppA–C/Alg1全部研究文字已读；HTML将附录转成§6–8，记录依实际PDF。实际查看p2架构、p5训练、p7生成表、p8理解表、p9全部五项消融、p16配置与算法。参考文献未逐篇，生成gallery未逐图。正式会场未核。

[作者项目页](https://yuqingwang1029.github.io/RepresentationForcing/)完整结构和外链已核，列论文、框架及展示，未定位代码/权重直链；不据此断言全网无发布。对照选读[SwAV官方量化归一化函数](https://github.com/facebookresearch/swav/blob/main/main_swav.py#L353-L376)，未审查全部SwAV或执行本作。

## 方法与理论边界

主模型保留预训DINOv3 ViT-H+/16理解encoder，joint阶段可训练；Qwen3-A3B初始化MoT，共享selfattention，理解/表示预测/像素三类FFN池。3B指每token活跃参数，不能记作全系统总量。

生成训练用GT图像经EMAencoder，在最终norm前取patch表示、2×2pool、在线VQ形成K16384分类目标；raster顺序的R token在T之后AR预测、teacher-forced输入，随后P patch双向flow。推理只从文字预测R，再以文字和R条件生成RGB，不调用GT/EMAencoder或外部VAE。量化prototype和用于LLM的position2D+identity embedding是不同对象。

16×16像素patch、每N表示对应4N像素patch；1024²按配置为1024个AR表示、4096像素patch，25flowsteps不能代表完整AR/CFG成本。hard argmax与EMA更新不形成通常的全路径连续反传；联合训练不能写成flow梯度直接穿过EMA量化更新encoder，也不能写成无上游视觉预训。

Eq1 $z_t=t x+(1-t)\epsilon$，Eq2预测clean x的速度误差，等价clean误差除$(1-t)^2$；Eq3是语言CE+表示CE+flow。中间表示以条件前缀参与，像素同时读文字与噪声，并未强迫全部RGB信息只经离散码本重建。去外部冻结VAE的结构限制与一般意义的无信息瓶颈需区分；VAE重建误差也不能直接推出每项GenEval等生成指标的统一上界。R的空间raster顺序无物理书写顺序意义。

## 完整表格与协同判断

| 证据 | 核读结论 |
| --- | --- |
| T1生成 | 无改写GenEval .84、DPG84.15；BAGEL .82/85.07，Showo2 .76/86.14，JanusPro .80/84.19。DPG非最高。改写后GenEval .88与BAGEL†同，六项.98/.95/.88/.87/.92/.70；颜色低于无改写.89和BAGEL†.95。†改写/不同数据和规模不能混作受控优势 |
| T2 RF对Pixel | 八项49.9/63.7/76.6/49.4/63.1/85.8/90/81.7→54.2/64.8/80.2/53/65.8/90.3/88/81.3；六升，Doc−2/Chart−.4。相对VAE+RF六升，RW65.8<66.6/Doc88<88.3 |
| T2对VLM-only | VLM-only56.2/65/79.7/56.2/65.8/90.3/89.3/86；Pixel+RF仅MME+.5，RW/AI2D同，五项下降。因此支持相对联合Pixel基线的部分退化缓解，未证明全面正协同 |
| T2 RF对VAE | 五升三降；MMMU−1.4/AI2D−2.9/Doc−1.7。MME*为感知/认知题平均accuracy，不能用常规汇总MME尺度解读 |
| T3a | 256消融Pixel .25→RF .76、VAE .52→RF .77；在此预算明显缩小质量差距，没有误差/等效检验，不能称统计等价 |
| T3b/c | 无.25/REPA .43/RF .76；连续表示.26/离散.76。额外R池、前缀长度/采样成本、连续head/损失/调参未完整控制，机制解释尚非唯一归因；离散AR同样有预测/曝光误差 |
| T3d/e | K16384 .76/32768 .77，只测两点。e明确为**VLM-only**，DINOv3五项四高、MMMU56.2<56.3；不能作为RF后完整生成效果或预训目标唯一因果证据 |

F2/F4为高分辨率展示与结构改善精选例，未报告全分布结构失真率、局部生成字串或笔画拓扑。缺少细字/文档能力的稳定改善，尤其需与目标研究的文字正确性分开判断。

## 训练条件与数据缺口

数据跟随BAGEL构建/过滤，纯文本与图文理解/生成，未给本作实际名单/独立规模/总tokens/比例/去重；不能直接继承BAGEL全部数目。三阶段10K仅MLP、50K≤256全解冻、20K≤1024继续；NaViT动态打包每GPU32768tokens。AdamW β.9/.95 eps1e-8/wd.1/clip1，warmup后constant，前两阶段base5e-5、第三2.5e-5，新生成参数4×。

码本decay .9999/temperature .5/一次SK，推理模型EMA .9999。top-k的k未给，25flowsteps+动态shift，wrep2/wpix3，文字和整段R独立drop .1。硬件/数卡、globalbatch/卡时、flow时间分布与shift公式、逐表快照/多seedCI、CFG精确组合未齐。T2强调pretraining且无posttraining，不能与其他系统后训练分数作同预算归因。

## 实际PDF算法疑点

AppB Alg1先`softmax(score,dim=1)`再`softmax(score,dim=0)`。SwAV官方函数先对相似度作exp，再除以行列边际和进行迭代；第二次softmax会再指数化已归一化值，不等同该SK操作。即使正确执行一次软归一化，后续argmax也不保证硬计数完全均衡。论文所谓避免collapse应有占用/熵与稳定性数据。

同页scatter index扩为(BL,K)，src却是(BL,D)、目标(K,D)，计数N_k形状(K,)直接除prototype(K,D)也没有显式列维。按通常PyTorch维度语义需要澄清。这里记录的是实际PDF伪代码与算法定义/shape对应，未定位可运行实现，不能据此宣称训练结果无效或已执行失败。

## 假设、可证伪实验与写作

合理优势条件是理解表示包含可由文字预测的结构、EMA/VQ目标稳定、条件前缀确实降低像素建模难度且AR成本可接受。应固定全部预训资源/数据曝光/总FLOPs/参数与推理预算，用VLM-only、匹配成本辅助CE、VAE/Pixel×RF检验真正协同；屏蔽/打乱R、保CE无R条件、冻结encoder及控制共享梯度，拆分辅助目标与条件作用。GT/预测/扰动R测曝光误差；连续方案匹配head、维数、损失与采样调参。实际SK/shape先核作者实现，再报告码本占用/熵/跨batch稳定性。

多seedCI、原prompt/改写、完整AR+flow+CFG延迟及局部生成字串/非汉字/真实事件视频应独立报告。以上是未运行的验证建议，创新性尚需追引。Latent Forcing（2602.11401）、REPA、DINOv3和SwAV进入追引队列，不能把被引即当成已独立精读；BitDance/WeTok等此前队列继续保留。

Introduction从外部VAE→像素缺口→内部表示→显式条件组织，Method按来源/生成/训练展开，T3逐项映射设计值得学习。作者Discussion承认预训LLM与静态任务，读者需补DINO预训、AR曝光/成本、实际数据/方差和码本伪代码问题；T2中VLM-only和文档退步必须进入Claim，不能只摘六升结论。
