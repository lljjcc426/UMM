# DiffSketcher / Diff-Font：条件、过程含义与公开配置审查（第六十批）

[L017](../reviews/L017.md)、[L018](../reviews/L018.md)完成明示版本的核心阅读与五问书面检查。347目录保持，134核心/136书面；其余213项仍没有核心三遍确认（含资源与不同证据层级）。无文件删除、模型训练、推理或独立复现。

## 研究问题和可辨识性

| 工作 | 输入→输出/机制 | 已有证据覆盖 | 不能直接推断 |
| --- | --- | --- | --- |
| DiffSketcher | prompt→整体优化可微Bézier/opacity→SVG；冻结LDM、JVSP/ASDS及注意力初始化 | 最终素描的语义、美学和少量辨识/人评、定性优化消融 | 整体优化帧就是人类落笔序列，真实动作或规范汉字笔顺 |
| Diff-Font | 一张风格图+字符ID+可选笔画类型count→像素DDPM/DDIM→静态字形 | 训练内容已见、字体未见的字形重建/感知与偏好；count/guidance消融 | count表达顺序/方向/拓扑，未见字符ID泛化，视频或机器人动作 |

类型计数在同一组笔画的任意重排下不变，因此仅给计数无法区分两个不同顺序。这是表示的信息限制；需要有序事件、空间对应或额外监督才能检验规范笔顺。DiffSketcher多条曲线可一起移动，迭代时刻与真实书写时刻也需要分别定义。

## DiffSketcher：版本与实验

[NeurIPS2023会议页](https://papers.nips.cc/paper_files/paper/2023/hash/333e67fc4728f147d31608db3ca78e09-Abstract-Conference.html)已核。完整核心与补充文字依据[arXiv v5，2026-04-08](https://arxiv.org/html/2306.14685v5)，另对照v2。正式PDF下载不完整，不记作已读；v5新增证据不自动归为2023正式发表内容。v5核心§1–6/Eq1–6、AppA–I文字/T1已读，实际Fig3/4/8已看，其他样例/视频未逐一看。

三次Bézier四点/透明度，经可微栅格器得到RGB，JVSP对齐LDM参考图的CLIP视觉特征/LPIPS；ASDS对增强后的图经VAE编码，以冻结UNet噪声预测差更新矢量参数。Eq6明确cross/self注意力融合，选定token定位首点，局部随机其余控制点。噪声区间[.05,.95]、CFG100；标准SDS/KL推导不构成规范事件或全局最优保证。

主定量在§5.2文字：CLIP ViT-L/14本法.3494/Canny.328/CLIPasso.3075，美学4.8206/4.3682/4.0821；未虚构不存在的主数值表。34类识别分布没有总体Top1数值。Fig8的250/1500/2000为单例优化迭代，比较attention/JVSP/ASDS，未给等质量墙钟加速或多seedCI。

v5 AppD/T1：41参与者，90生成图（3方法各30）+30网络真实自由素描，人画判断比例本法.65/人类.67/CLIPasso.39/VectorFusion.33。真实图33%也被误判、外部图来自各自论文/项目，未统一prompt/风格/预算。该比例不代表规范过程准确率，未给显著性依据，不能推出普遍接近人类能力。CLIPasso/Canny拿生成参考RGB、直接文本方法条件不同，也应单列。

## Diff-Font：正式发表与原表边界

[Springer正式页](https://link.springer.com/article/10.1007/s11263-024-02137-0)：IJCV132, 5372–5386 (2024)，在线2024-06-13；具体SCI分区年度未核。实际全文是[arXiv v3](https://arxiv.org/html/2212.05895v3)，§1–5/Eq1–10/T1–6及实际模型、count、消融图已读；期刊全文与预印本逐页差异待核。

中国字400训练字体/10测试字体，small800内容×400=320K，large6625×400=2.65M；测试内容ID已见。固定DG-Font风格encoder，UNet base128/3ResBlocks/attention40/20/10，80²像素，1000步线性噪声、DDIM25步；small300K+300K/b24，large420K+380K/b64，Adam1e−4/WD0。GPU/总墙钟/seed不完整。韩文195/6字体单独训练，Latin/Greek另训第一阶段、仅定性，不能视作中文模型跨语言零样本。

| 原表/条件 | SSIM↑ | RMSE↓ | LPIPS↓ | FID↓ |
| --- | --- | --- | --- | --- |
| T2 small，本法 | .742 | .271 | .124 | 27.30 |
| T2 small，DG-Font | .729 | .280 | .137 | 43.44 |
| T2 large，本法 | .722 | .277 | .104 | 16.20 |
| T2 large，MX-Font | .692 | .298 | .138 | 26.64 |
| T4 small，无count | .740 | .275 | .127 | 28.83 |
| T4 small，binary presence | .739 | .277 | .131 | 30.44 |
| T5 large，guidance 5/1 | .720 | .280 | .107 | 16.18 |

T4 count优于无count，但幅度与CI/seed缺项须报告，binary presence更差。T5默认3/3的FID16.20略高于5/1的16.18，后者RMSE/LPIPS反而更差；不能称3/3全部指标最优。正文明确在test set调guidance，应另设validation冻结选择再报告test。T3为64人×10字体=640次四候选偏好，本法48.75%、DG24.53%、FUNIT13.44%、MX13.28%；该份额不等pairwise胜率或识字准确率。

Eq9组合ε0+s1(εcs−ε0)+s2(εs,op−ε0)，两个分支共享style。因此两scale也共同改变style影响，s1=s2=1通常不等于完整三属性预测；无正交控制/顺序保证。

## 无论文工程制品也须独立核配方

| 固定代码 | 实际已核 | 与文章关系/缺口 |
| --- | --- | --- |
| [DiffSketcher 0319b29](https://github.com/ximinng/DiffSketcher/tree/0319b2903016baa2b057bd19922ff0a4e56751d9) | 默认yaml全文、README setup/quickstart与选定例、入口/merge/step初始化/循环/ASDS/曲线选段 | 默认2000步且sds.warmup2000，循环step从0到1999，无覆写时不进入ASDS；README800步例未改warmup。默认color_lr.01 vs AppA.1，attn_coeff1只cross，默认增强affine不含sharpness，所读ASDS一次增强。需对齐后才称论文配方 |
| [Font-diff 44d29cf](https://github.com/Hxyz-123/Font-diff/tree/44d29cf44b195109b9903bd4768ee8407730e46c) | README/两yaml全文，sample三分支CFG、dataset两个独立random .3 drop、UNet计数embedding/forward选段 | yaml b16 vs论文large b64；base128代码content128/stroke128/style256 vs论文128/256/128。计数相乘再flatten、双属性丢弃时style清零、三分支与Eq9对应。示例需数据/字体/encoder等，未下权重或运行 |

以上为特定版本静态路径与配置分析，不是全仓训练复现。DiffSketcher的-make_video保存各迭代整体画面，无法使其自动具备真实逐笔过程监督。

## 可证伪设计及研究写法

固定基座、prompt/字符/字体划分及优化/训练预算，分开最终图与过程指标。DiffSketcher做attention×JVSP×ASDS×增强，先校正warmup并公开seed/N/CI；Diff-Font按复杂度比较无属性/onebit/count/空间部件/有序事件，独立validation调参。构造count不变而顺序错误的反例，补独立OCR/结构/规范事件评价，样本与评委盲化。全部尚未执行。

两篇都把具体失败连接到表示/条件机制；学习Method沿数据流拆解，实验每项对应明确Claim。报告版本日期、定性与定量来源、偏好份额定义和公开配置差别，Limitations写出内容ID覆盖、count不可辨识性、预算及域外失败；发现限制之后仍须检索既有解决方案。
