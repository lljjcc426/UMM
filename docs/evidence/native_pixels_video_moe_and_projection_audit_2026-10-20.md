# 原生像素、视频MoE与投影优化：第十六批

2026-10-20；L072、L123–L126共五项存量研究。累计238份笔记，章节252/摘要33/历史待核47。五项书面检查9项，完整三遍验收0，独立复现0。没有删除文件。

## 证据及限定

| 研究 | 复核内容 | 对选题的影响 |
| --- | --- | --- |
| [UniFlow/L072](../reviews/L072.md) | 自适应蒸馏在重建/理解间取舍；final层rFID.25优于adaptive.26，uniform MME1518.2高于adaptive1513.7 | 不能概括全部指标最好；语义码是否保留细笔画要独立测 |
| [InternVL-U/L123](../reviews/L123.md) | 图像生成/编辑与理解；TextEdit2148对、Mini500；合成中英文字训练 | 文字编辑的强前作必须比较；OCR目标/背景指标均不能验证笔顺 |
| [Mamoda2.5/L124](../reviews/L124.md) | 25B/3B是DiT口径，另有Qwen3VL8B、ByT5、WanVAE；支持图/视频编辑 | 视频字幕编辑属于已有任务；不可把3Bactive写成总系统参数 |
| [SenseNova-U1/L125](../reviews/L125.md) | 原生像素双流MoT、OCR/偏好RL、2K生成后降1K评价 | 无VAE不保证细字保真；“1K评测”要同时记录2K生成计算 |
| [Rosetta/L126](../reviews/L126.md) | 共享QKV+共享/路由专家，动量投影；旧任务有升降 | 共享专家和投影无法直接推出无遗忘；需匹配训练/优化器对照 |

## 代码与数学核对

UniFlow[固定代码](https://github.com/ZhengrongYue/UniFlow/tree/e6322d0b57bedbe7111a292104c6a07971fcfaea)类默认采样步数与[实际模型配置](https://huggingface.co/yuezhengrong/UniFlow/blob/main/config.json)不同：发布配置明确一步，不能从默认100/10步否定论文一步重建。正文batch512与附录表256仍需核执行配置；其他训练代码尚未全审。

Rosetta[固定代码](https://github.com/Lxiangyue/Rosetta/tree/30fada710b1d79b9b6dad17e0349b0f97c9ea938)对每个共享参数tensor分别投影，参考向量为Adam历史动量。论文Eq4含epsilon，Eq5证明省略epsilon；冲突时残余内积为原内积乘epsilon/(范数平方+epsilon)，严格等于零不成立。代码采用范数阈值和无epsilon除法，须区分公式证明与实现。欧氏动量约束也不能保证Adam预条件后每个旧任务的有限步loss不升。

代码为共享参数g/m构造float克隆并在列表暂存，增加临时缓冲；“没有额外持久优化器状态”可成立，“零额外内存/计算”的严格推论不成立。作者profile峰值58.8GB/8602tokens每秒未独立复现，临时分配不直接证明其测量数字错误。

## 对照、消融和可证伪实验

Mamoda的编码器×注入方法2×2显示Qwen3跨注意力65.52/76.44低于umT5跨注意力67.30/77.08，换in-context才达68.50/78.84。文字编码器收益依赖接口，需做交互对照。MoE ImgEdit总分2.87→4.05但Action4.11→3.89；VBench2 61.64仍低于LongCat62.11/Veo66.72。DMD/NFT四步速度不能代替独立质量指标。

SenseNova的OCR奖励使用字符计数多重集IoU，实际单位需代码确认；若按单字符，将重排同字符文本设为反例。比较OCR reward、序列编辑距离、二维框匹配和人工布局，检验奖励投机。原生像素/语义codec/VAE需固定训练曝光和生成计算，再测细笔画最小对/长字符串/中英阿拉伯混排。

Rosetta消融要同时匹配DiffLR、shield、投影开关、共享结构，测MMLU/ARC/MBPP等各自遗忘曲线；记录每任务曝光，至少多seed。主表MMLU51.6→49.2、ARC67.3→62.9而MBPP36.2→42.4，不能平均后写无遗忘。

## 未核范围

本批各篇完整附录、全部图及实现仍有缺项。InternVL-U正文对MoT的概括不能代替原MoT定义；Mamoda权重在官方指定revision仍Coming Soon；SenseNova主系统硬件/完整有效batch、OCR分词及数据去重仍待核。RosettaPDF第4/14页框架和证明已视觉读，其他页面不自动算读完。没有运行模型或下载权重。
