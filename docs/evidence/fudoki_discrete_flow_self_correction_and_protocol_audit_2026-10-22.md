# FUDOKI：离散概率流、纠错与复现协议

第一百二十四批完成[L109](../reviews/L109.md)明确范围的核心三遍与五项书面记录。[结构化证据](../../data/fudoki_discrete_flow_self_correction_and_protocol_audit_2026-10-22.json)。357目录（330论文／研究、27资源），233核心/236书面含未通过项；124条未确认核心，其中97条论文／研究、27条资源。资源另按模型卡、代码、数据与训练协议审查，不以缺论文三遍认定资源未审。本批未新增目录、删除文件、下载权重或运行模型。

## 正式来源与阅读范围

以[NeurIPS2025正式主会记录](https://proceedings.neurips.cc/paper_files/paper/2025/hash/74e9002aef14078b3a6346129990763f-Abstract-Conference.html)及[39页正式PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/74e9002aef14078b3a6346129990763f-Paper-Conference.pdf)为准。读Abstract/§1–5、Eq1–6、T1–5、全部F1–12图注与AppA–F研究文字；实际查看p4/5/8/9/10/35/38/39八页。Maze仅文字/图注，未逐图；checklist6/7选读，参考文献仅关键定位。22页独立supp前十为同AppA–F、后参考，未另全读22页。arXiv2505.20147v3仅作intro/β等版本对照。

[官方代码固定ffcfc8e](https://github.com/fudoki-hku/FUDOKI/tree/ffcfc8eff85eaf55f0f1da1455e5726fa177f2e0)完整626项树和README、model入口/CFG wrapper/path全文、solver308–640、注意力/head及推理脚本指定段；[HF固定6827760](https://huggingface.co/LucasJinWang/FUDOKI/tree/6827760f631d253b9219158a6a36d3fda2b38821)元数据/目录、README/config全文。没有全审626文件、读取pt/safetensors、训练、推理或独立复现。README自称Spotlight/Top3.5%，本批只独立确认正式主会身份。

## 三句话概括与任务定位

默认AR与absorbing-mask采样对已确定token的回访受限，作者研究可反复修正的双向离散生成。方法把Janus1.5B改为双向Transformer，以embedding距离路径和条件跳转速率训练图像/文字终态预测。GenEval达到.77，但相对JanusPro1B理解只有1/7指标提高；纠错增益、BestN收益和采样速度均需附协议条件。

输入为图像+问题或文字prompt，输出文字回答或384²静态图像。SigLIP理解仍用连续特征，LlamaGen生成用离散码，双接口保留。“pure DFM”限定生成目标；不能写成全系统只有离散表示、视频模型或规范书写UMM。IAM/ChromeWriting是静态识别数据，F12还明示特定文字渲染失败。概率流的连续时间不等于现实笔画执行时间。

## 方法、关键符号与最优性的范围

Janus1.5B继承预训，24层Llama/hidden2048/16heads/FFN5632，双向fullattention；输出logit后移一位承接nexttoken能力，无额外t embedding。理解SigLIP-L16-384的1024维特征经两层MLP到2048，生成VQ16/8维code经独立MLP；文字词表102400、图像16384，576个图像码=24×24→384²。两个head输出各自分布，结构统一并未消除视觉接口差异。

给定终态token \(x_1\)，令

\[
p_t(x\mid x_1)=\frac{e^{-\beta_t d(x,x_1)}}{\sum_y e^{-\beta_t d(y,x_1)}},\qquad
\beta_t=3\left(\frac{t}{1-t}\right)^{0.9}.
\]

正文称 \(d\) 为归一化embedding的L2距离；文字embedding来自JanusPro7B，图像来自LlamaGencodebook。这份7B派生先验不应从成本叙述消失。条件路径各坐标独立，不代表对不同真实终态混合后的联合分布独立。

Eq5给非对角条件速率（从\(z\)跳到\(x\)）：

\[
u_t(x,z\mid x_1)=p_t(x\mid x_1)\dot\beta_t[d(z,x_1)-d(x,x_1)]_+,\quad x\ne z.
\]

AppE另规定负对角为流出速率之负和，使各列和零。不能把Eq5代入x=z得到零后指责作者没有CTMC负对角。由softmax求导可核 \(p'_t(x)=\dot\beta_t p_t(x)(\mathbb E_{p_t}d-d(x,x_1))\)，代入正向flux公式即得Eq5；这里只作当前公式一致性解释，没有独立复核全部参考理论。

所谓kinetic-optimal，固定规定概率路径及权重\(w_t(x,z)=1/p_t(x)\)，在连续性/非负flux/边界条件下最小化指定动能，核心结果继承[38]。[原始ICLR2025论文](https://proceedings.iclr.cc/paper_files/paper/2025/file/29cd7f8331d13ede6dc6d6ef3dfacb70-Paper-Conference.pdf)已定位，独立全篇阅读仍入队。它不推出对所有概率路径、RGB运动、笔画顺序或终任务质量全局最优。

训练uniform t、按路径腐蚀真实目标，条件prompt/图像问题保持clean，对全部回答（含EOS/pad）算CE。先只训Transformer，再称wholemodel；VQcodec是否第二阶段更新仍需完整训练实现。推理每步重估\(\hat x_1\)，以\(1-e^{-h\lambda}\)决定跳转，目的地按非对角速率归一化；有限步冻结速率近似，源码末步直接取预测终态。固定真实x1时跳转朝近邻，实际预测x1可变，无法推出对真实答案的错误率单调下降。

## 五张表与消融实际支持什么

| 证据 | 报告结果 | 判断与限制 |
| --- | --- | --- |
| T1 GenEval | 本作.77；Janus.61、Pro1B.73、SD3.74 | single.96低Janus.97/Pro.98；color.88低Pro.89；count.56低SD3.72。不能说各属性全优 |
| T1 BestN | 32图经VILA-Judge选4，overall.88 | 增加候选、judge预训与筛选成本；单样本模型分数仍.77。†标外部预训diffusion组件，不代表prompt改写 |
| T2 DPG | 83.63对Pro82.63、SD3 84.08 | entity89.73/relation93.66较强，但global80.55/attr88.05/Other78低Pro87.58/88.17/88.3 |
| T3 理解 | POPE86.1/MME-P1485.4/MMB73.9/SEED68.2/GQA57.6/MMMU34.3/MMVet38 | 对Janus5升2降，对Pro1B仅MME-P升、另6降，MMVet低39.8；数据/继承预训也不同 |
| T4 纠错 | 原37.98；AR1B36.33、AR7B38.30、本作38.53 | +.55分，对7B纠错仅+.23；缺CI。AR追加原答和纠错prompt，本作以原答初始化32步，接口/上下文/成本未匹配 |
| 正文Best8 | MMVet38→55.5 | 8候选及LLMjudge，确切judge版本/开销未齐；不能当单次生成能力或已实施RL |
| T5 MathVista | testmini38.6，Janus32.4/Pro35.1 | 支持所报测试集分数较高，尚未隔离额外监督与DFM结构收益 |
| F5 初始化 | 前8K步ARinit loss低于scratch | 继承大规模预训练，步数差不代表全生命周期算力收益 |
| F5 t embedding | 无显式t loss略低 | 缺对应终任务、噪声泛化和OOD对照，不能推广所有DFM无需时间条件 |
| F5 步数曲线 | 低NFE快而质量低，增步质量升/速度降 | 原图点/硬件/batch/精度/距离成本未齐；不把32步说成质量与速度均无条件胜AR |

AppC maze的三个尺寸与4步精修展示属定性证据，训练集/holdout规模、成功率/无解率及预算未详。文字例子改拼写、数学和SaraLee识别展示修正可能性，不能替代对错转移统计。

## 数据数量和复现差异

正文约13M=9M生成+4M理解；AppD写12.62M=8.76M+3.86M。实际八类为general1506.8K、OCR428K、doc155.8K、table180.2K、chart362.6K、screen24.6K、math544.9K、language510.2K，合3713.1K。F11图写3.71M、图注3.86M，差146.9K。Chart细项359.6K与标题362.6K差3K，math细项547.9K与标题544.9K反差3K。保留这些冲突，未人为补齐缺项。

General包含70K in-house，正文“public understanding”需收紧。OCR含IAM5.7K/ChromeWriting8.8K等，FUNSD也列doc；来源重复列名不自动证明样本重复，需ID/split去重。8.76M生成原数据与完整理解混合版本未齐，不能宣称全数据公开。

正式版约43000GPUhours，但GPU型号、optimizer/LR/globalbatch、stage步数/epoch和混合比例未完整。Checklist6/7自答训练/统计充分，实际已读表和附录仍有上述缺项，审查按具体公开材料判断。

| 论文/发布位置 | 核对事实与影响 |
| --- | --- |
| 距离 | 正文L2；path.metric及solver将 \((\|a\|^2+\|b\|^2-2a^Tb)^2\)用于归一化向量，即L2四次方；二者代码内部一致，但与正文定义有别。未运行，不能据此断言已报结果错误 |
| 步数 | 正文32；Python默认128；shell显式50。复现须锁定入口/参数 |
| CFG | T2I脚本scale5；wrapper使用\((1+s)\ell_c-s\ell_u\)，每步两次模型调用。理解topk1后softmax；多步token跳转仍随机 |
| 精度与长度 | 脚本seed999/float32；HF骨干dtypebf16但外层float32。I2T总文字槽500包含prompt，论文写response500，不能简单视同协议 |
| 边界步 | a=.9使βdot在0奇异但可积，源码t0设0，末步直接取终态；属具体离散实现，需报告其对质量/成本的影响 |
| 发布范围 | 有I2T/T2I示例、embedding文件与权重、改动VLMEvalKit；指定材料未提供完整两阶段原训练配方，文件存在不等已复现 |

## 转述纠错与写作学习

Formal F2正确写D-DiT文字离散/图像连续，AppA却与UniDisc并列全离散。原作[CVPR2025 D-DiT §3](https://openaccess.thecvf.com/content/CVPR2025/papers/Li_Dual_Diffusion_for_Unified_Image_Generation_and_Understanding_CVPR_2025_paper.pdf)直接写连续图像flow+离散mask文字，已核该方法段，尚未独立全篇三遍。BAGEL[C01](../reviews/C01.md)为AR文字+连续视觉flow，不能列成全AR；Transfusion[U05](../reviews/U05.md)为共享Transformer加局部patch适配/U-Net模块，不能把整个模型归成纯U-Net DDPM。CNF在[NeuralODE NeurIPS2018摘要](https://papers.nips.cc/paper_files/paper/2018/hash/69386f6bb1dfed68692a24c8686939b9-Abstract.html)已有，AppA把CNF起源归Lipman不成立。该2018条目本批仅核摘要时间/贡献，未声称全篇精读。

Introduction的AR限制→mask限制→metric路径→预训复用问题链、Method的预备知识→路径→结构→训练→采样组织值得学习。写Claim应保留对Pro六项退步、有限预算纠错、BestN筛选成本和理论最优性的条件。AppF固定长度、复杂文字、专业知识有F12失败支撑；AGI/医学等应用愿景没有相应实验证据。

## 可证伪验证与下一步

固定Janus起点、有效13M样本、视觉接口，分别对齐NFE/总FLOPs/墙钟比较AR编辑、mask+remask、L2/L2²/L2⁴/随机度量。记录距离矩阵和CFG两次前向；相同错误回答、条件与修改预算，报告错→对、对→错、长度分层和多seed/bootstrapCI。BestN固定候选/外部judge/独立终评并计总成本。所有这些均为未执行设计。

若迁移严格书写，需要显式事件/轨迹表示、合法拓扑和顺序约束，核距离是否反映笔形/执行可行性；固定终图构造相反顺序对照，同时测字符exactmatch、抬笔/笔画事件、RGB时序可观测性及执行。普通embedding近邻与概率时间不能替代这些定义。继续独立阅读[38]、D-DiT及相关remask/corrector工作，查新后才判断课题创新。
