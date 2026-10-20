# 素描序列、绘画策略与共绘LoRA：第四十一批

四项既有记录更新：[sketch-rnn](../reviews/G014.md)、[Learning to Paint](../reviews/G015.md)、[英文连笔](../reviews/F05.md)、[CoFRIDA-Sharpie](../reviews/H001.md)。新增两项核心三遍，累计92项；四项各五条书面检查，累计94项。F05仍限作者报告；H001属资源协议核查，均未计论文核心三遍。主目录仍340项，没有新增独立论文计数，没有训练/推理或文件删除。

## 表示和任务边界

| 工作 | 实际输入→输出 | 主要证据/未证实目标 |
| --- | --- | --- |
| sketch-rnn | 在线素描五元组→隐空间/自回归矢量序列；可无条件/补全 | 短素描分布与latent定性；无规范汉字笔顺/真实视频 |
| Learning to Paint | 目标图+画布→连续笔触→模拟重建画布 | 终图ℓ2与效率；无人体/工具/真实执行时序训练 |
| 英文连笔 | 独立字符轨迹→角色分类/优化→连笔轨迹 | 作者报告英文外观、识别与CPU延迟；IEEE正文仍缺 |
| CoFRIDA-Sharpie | 官方加载代码为text+canvas→目标图，另接FRIDA | 模型卡/权重结构/调用证据；未绑定论文分数或运行结果 |

## sketch-rnn：似然、潜空间和真实事件分开

[Google Research](https://research.google/pubs/a-neural-representation-of-sketch-drawings/)确认ICLR2018；实际正文为[arXiv1704.03477v2](https://arxiv.org/abs/1704.03477v2)。双向编码器、128维z、HyperLSTM与20分量二维GMM，输出位移及三笔状态。p4Fig4–5已视觉核：p2在当前点后抬笔，p3不渲染当前及后续点，不能把点事件与整笔结束混用。未包含真实速度/压力。

Eq10按Nmax归一，位移mask至有效点，pen CE含padding；连续概率密度NLL为负合法。Eq13 KL退火与总量floor调重建/先验权衡，温度缩放方差而非直接σ乘τ。T1 cat将wKL1降到.25，LR−.98→−1.46而KL.29→1.01；Fig8/12–13提示低LR未保证插值/形状连贯。all75类失败、>约300点难训练和过低温螺旋是作者明确限制。跨类Nmax不同，不直接按LR排名。

[固定Magenta代码](https://github.com/magenta/magenta/tree/c15687ebd1c1cc12658cd468c737d3c24c02b918/magenta/models/sketch_rnn)默认小LSTM/lr.001/点drop等与v2不同，README明确点drop未用于论文；eval额外mask EOS pen CE，须与论文/训练模式对齐。原QuickDraw75类实验与后来345类数据、Kanji/Omniglot扩展资源不能混填。

## Learning to Paint：可微环境、奖励和预算的组合

本批读[ICCV2019正式PDF](https://openaccess.thecvf.com/content_ICCV_2019/papers/Huang_Learning_to_Paint_With_Model-Based_Deep_Reinforcement_Learning_ICCV_2019_paper.pdf)核心正文与p2Fig2/p7Fig8–9。模型通过目标图/当前画布/步号预测五个13维动作；10维形状/透明经神经renderer后用RGB着色。modelbasedDDPG利用即时奖励与可微转移梯度，WGAN-GP、Action Bundle与笔画数另外影响性能。

主结果为曲线而非表格。作者报告同20不透明笔ℓ2约SPIRAL的1/3，modelbased约PatchQ的1/5、DDPG的1/20；图无精确端点表和CI，不补小数。Fig8b同200笔时bundle5在已测设置最佳，增加总笔则同时增算力。WGAN的局部收益不能推广成一切图像差异的通用定理。正文Eq3附近actor目标省略γ而Bellman含γ，固定代码使用.95^5，复现需核定义。

[固定官方代码615c070](https://github.com/hzwer/ICCV2019-LearningToPaint/tree/615c0707ce265706af41fd63a78d0c7824639f75)可把渲染帧拼成视频，这证明有可视过程，不证明学习了真实视频或人类规范笔顺。后续Paint Transformer、Stylized Neural Painting等也需在同预算下对比；静态监督下多种顺序可得同终图，是需专门实验检验的不可辨识问题。

## 英文连笔：外观改善与识别权衡

[ICASSP2026 program13860](https://www.cmsworkshops.com/ICASSP2026/view_paper.php?PaperNum=13860)确认正式论文，当前读到[Samsung作者说明](https://research.samsung.com/blog/Online-Cursive-Handwriting-Generation-Using-Trace-Transformation-and-Symbol-Independent-Point-Classification-Model)与Fig1/T1–3原图。正常View Manuscript转IEEE11463098，尚未取得正文。20点归一、约12K双层BiGRU角色分类与三目标凸二次轨迹优化，精确权重和训练协议留空。

| 指标 | 独立字符 | 连笔 | 可支持的解释 |
| --- | --- | --- | --- |
| HWD/FID/KID | .686/4.814/1.237e−3 | .649/4.591/1.058e−3 | 作者报告外观分布指标改善 |
| GPT4o WRR | 97.63 | 96.71 | 连笔相对独立下降.92个百分点 |
| Gemini2.5 WRR | 97.32 | 96.78 | 下降.54个百分点；相对用户93.57升3.21pp |
| 单字符分类+变形均值 | — | .125+.006=.131ms | S25单CPU线程；上游SDT另有129.041ms |

18人/55对的“non-inferior”报告未给预设界值/CI，不能写成严格统计非劣结论。语言无关点输入与英文验证分开；RTL留待验证。引文新线索CASHG（arXiv2604.02103）尚未全文阅读，应追读去重，不能用未读摘要声称问题已解决或完全新颖。

## CoFRIDA-Sharpie：制品结构能排除什么

[固定HF revision](https://huggingface.co/skeeterman/CoFRIDA-Sharpie/tree/58d397f81bd0bf64eb43d85ee8bd5191acd9824d)的YAML为SDXL-IP2P，正文写原IP2P。只读取bin前512KiB，用pickletools静态解析ZIP内完整data.pkl操作码，未执行pickle/加载张量值。256个LoRA矩阵均rank256，共51,019,776参数；attn2 K/V输入维768。

| 一手证据 | 结构/行为 | 结论范围 |
| --- | --- | --- |
| 权重metadata | cross768；通道320/640/1280 | 可筛除所填SDXL结构，不能唯一识别基础checkpoint |
| 原IP2P config31519b5 | cross768，block320/640/1280/1280 | 结构兼容线索 |
| SDXL-IP2P config06653d4 | cross2048，block320/640/1280，text_time | 与该adapter的768维投影不一致 |
| 官方src/cofrida.py/codraw.py | 默认timbrooks/IP2P，load_attn_procs，text+canvas | 支持原IP2P加载路径；未实际执行 |
| 当前train_lora.py | rank32，text与final image，无canvas拼接 | 与rank256制品不对齐，不能作原训练实录 |

当前代码固定f42fa618；[ICRA2024 v2.0.0](https://github.com/cmubig/Frida/tree/1bf0205bcabcaac007a07f97ecfff3d613eb3f4d)没有该LoRA训练文件。原论文全UNet训练、当前LoRA脚本与HF制品是三层证据。底座精确commit、训练集/日志、alpha和实际加载版本仍缺；结构可核不代表性能复现。

## 实验与写作学习

1. 短序列/长序列、随机采样/重建/补全分别设任务，统一Nmax与mask后测NLL、结构、保持、EOS和笔事件；以画者/长度/类留出。
2. 绘画固定renderer/奖励密度/网络/总笔和时间预算，拆可微信号×bundle×奖励×总笔，分列模拟重建与真实执行；乱序同终图作为评价反例。
3. 连笔固定上游/布局，比规则连接、角色分类和各优化项，报告识别—外观权衡、全链路时延和预设偏好协议。
4. HF制品固定底座/adapter/库/条件，先恢复实际运行配置再归因；F04论文分数不挪给H001，元数据与性能证据分开。

问题定义应限定表示和输出；Introduction中的每个不足需在Method与实验中有对应。Claim包含分布/预算/指标及负结果，Limitations写清原文缺失、分布外失败和代理指标无法验证的目标。上述实验是方案，未运行；相关前作追引尚未全部完成。
