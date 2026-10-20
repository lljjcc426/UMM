# PaintsAlter / StrokeNUWA：查询、表示、训练配方与指标审查（第五十九批）

原记录[L014](../reviews/L014.md)、[L016](../reviews/L016.md)完成明示范围核心三遍书面检查。347目录保持，132核心/134书面。无文件删除、模型训练、推理或独立复现；DiffSketcher新版与其他剩余工作继续。

## 两个任务对应不同的过程含义

| 工作 | 实际任务/输出 | 与本项目关联 | 不应外推 |
| --- | --- | --- | --- |
| PaintsAlter | 源画布/步骤集合→任意过去/未来、非连续状态集合；视频DiT+分区VAE/步骤因果投影+SDXL调度 | 直接绘画视频/状态生成、非连续查询与时空VAE限制、交互/多历史 | 唯一真实历史、底层编辑动作、规范文字一笔、不可擦除过程 |
| StrokeNUWA | 关键词→压缩SVG码→重建/修补→单色图标 | 紧凑矢量表示、LLM的AR序列成本、后处理与语法/几何取舍 | token恰好是一规范汉字笔画、独立语义ID、实际笔画时间或RGB视频 |

有序文件内容、归一化画布状态、真实动作和规范笔画事件需要各自监督与指标。二者都纳入相关工作及强基线，不能将名称中的stroke或process直接当具体事件能力。

## PaintsAlter：方法与现实数字绘画操作

作者[项目页](https://lllyasviel.github.io/paints_alter_web/)与[13页PDF](https://lllyasviel.github.io/paints_alter_web/paints_alter.pdf)确认ACM TOG44(4), Article127, SIGGRAPH2025，[DOI](https://doi.org/10.1145/3731160)。核心§1–5/Eq1–6/TI–IV读完，实际Fig3与Fig9/10、TIII/IV；其他样例/视频未逐一看。具体SCI分区年度未核。

Eq1把查询写为源状态/索引与查询索引到状态集合。连续段各自经冻结3DVAE编码，source/query即使相邻也独立编码；源噪声level置0，query回归flow velocity ε−z。operation索引的因果投影与VAE padding/stride匹配，使源与查询的索引/latent对齐。该causal指压缩编码结构，未证明跨多次查询的全局因果一致性。SDXL另加4源latent通道与s/q标量，只用于单源单query或长查询的关键帧，再由视频补区间。

约19艺术家同意提供2018–2020长录屏，shot检测/过滤后20K clips；默认145帧，长shot区间随机采样最多32次。归一smax1000并非1000个真实stroke或1000秒。5%留出未给按作者/原视频分组清单，不能据此断言泄漏，也不能视作严格作者外泛化。人评另50未见真实画作。视频基座LTXVideo/CogVideoX1.5，SDXL辅助；8H10080GB，Adafactor1e−5/bf16/clip.5/无EMA，约4/9/3天，video512px/image1024px。WD14对输入最高step帧取prompt，未给完整batch/采样步数/seed。

TI Cog17.04dB/.6712/.4022、LTX16.31/.6510/.4259、SDXL15.98/.5995/.4515；ProcessPainter13.52/.4901/.6143、Painting Many Pasts（Zhao2020）12.27/.4847/.6851。ProcessPainter按其建议在同数据微调；InversePainting因输出/segmentation不兼容从定量和人评排除，仅定性。不同基座/预算同时变化，不能全部改善归因分区设计。多历史任务的像素重建只测对该参考历史的距离，可能惩罚另一个合理历史。

TII为六候选质量选择份额：Cog+image30.12±5.8%、LTX+image26.51±6.1%；四候选响应选择份额LTX+image47.43±9.1、Cog+image16.62±5.2。13人（1学生/8众包/4艺术家）、五轮std；这些百分数不等成对胜率或总体CI。TIII L40S测1/65/129帧：Cog7.2/193.1/327.4s、LTX4.8/8.4/41.3s、SDXL3.9/251.2/495.1s。最快/最优来自不同后端，不能拼成单模型表现。

实际Fig9为不分区编码相隔帧产生ghosting、分区改善的定性案例，无全量模块消融。TIV对50作品人工计突变总数13.1±.7人画、11.4±.8生成，含可见性切换、变形、导入删除、色曲和层序。这些在数字绘画可合法发生，因此单调增墨须限定任务；RGB中类似频率也不能证明恢复了真实编辑命令。图6/7的“5% (s=5)”与smax1000不一致，保留原标注，未用其换算规范时间。作者明确域外UI文字/结构及照片风格失败。

项目页链接的是PaintsUndo，并把PaintsAlter标next version；作者名仓库检索无单独命中，只限定该次检索。未找到可与全文训练配方逐项对齐的独立PaintsAlter发布，不能直接拿PaintsUndo代码/权重声称复现本论文。

## StrokeNUWA：压缩收益、指标定义与公开示例

[ICML/PMLR元数据](https://proceedings.mlr.press/v235/tang24h.html)及[正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/tang24h/tang24h.pdf)确认pp47830–47845。核心§1–6/Eq1–3/四表与AppA/B/C文字、TV已读，实际Fig3和TII/III/Fig7。附录大批图未逐看；arXiv v2/v3 HTML404不改变正式PDF可访问事实。

VQ-Stroke将SVG简化M/L/C，每命令9维（type/始末点/控制点），1D卷积+残差VQ，码本4096×512、depth2；FlanT5 3B冻encoder训decoder和新embedding/head，CE预测码。PC直接改接点，PI插Move保持片段；Move不画出连接线。压缩token可对应一段命令，语义/规范stroke不是结构保证。Eq3的sg被原文写为gradient clipping；按VQ公式通常为stop-gradient，当前quantizer实现尚未逐读，不能据用词认定程序有同样错误。

FIGR8SVG过滤至740K/8K/2K，最多1024命令、至少2关键词；优化基线因耗时随机500例。主表64V100/DeepSpeed、len512，Iconshop同FlanT5重实现但max1500；输出path预算也不同。人评正文50prompts，补充10评委各100例、win/tie/lose，重复映射/完整随机协议待补。

| 对象 | Fréchet↓ / CLIP↑ / HPS↑ | tokenRecall / EDIT↓ | 时间 |
| --- | --- | --- | --- |
| StrokeNUWA PI | 6.513 / 17.994 / 16.801 | .207 / 12249.091 | 19.128s |
| StrokeNUWA PC | 6.607 / 17.852 / 16.134 | .239 / 9092.476 | 19.128s |
| VectorFusion | 7.754 / 17.539 / 15.901 | .079 / — | 约30min |
| Iconshop | 17.828 / 8.402 / 8.234 | .114 / 24792.476 | 63.743s |

文中称FID，但脚注明确CLIP图像encoder特征，不能与Inception-FID混排。Recall为自身VQ token集合与参考的交集占比，不能评token顺序/真实语义，可能偏向自身表示；EDIT对等价SVG代码写法敏感。94倍对应30min/19.128≈94.1，28min约87.8，未匹配输出质量或计训练成本。

TIII C2PI Fréchet3.518/CLIP20.290/EDIT1315.137/占比13.780%，C4PI4.943/15.192/2100.671/6.890%，存在明显压缩/质量取舍。正文CR=Len(rawtoken)/Len(stroketoken)与表<100%的存储占比方向相反；正文lowest CLIP与箭头↑/20.290更高亦冲突，保留原表，不静默改数。TIV增码本2048→4096→8192在512维下Fréchet5.702→3.518→2.639；4096维度512→1024反变3.901，不能推所有容量增加总有效。TV换自然语言模板5仅简单图/无量化，模板4 Fréchet11.607，显示关键词训练分布限制。

固定[a52e1cc源码](https://github.com/ProjectNUWA/StrokeNUWA/tree/a52e1cc29d7d512d299404b4293d8eea03a34be0)的README/VQ example.yaml/EDM example.sh/train_vq.py主体已读。README测试Py3.10.13/CUDA11.1，安装例Py3.9/CUDA11.8；公开VQ示例emb_width1024（主表512）、b128/lr3e−4/90epochs/单device、FusedAdam。EDM示例4×16GPU、b25/卡、lr5e−6/20epoch/warm60、len512/ZeRO3/gradientcheckpoint，数据路径是example sample；这些给出工程参考，未证明论文同配置。训练脚本Hydra默认configs/experiment、示例文件在configs/VQ-Stroke，完整路径启动与依赖尚未运行核实，不把README命令当已复现。

## 可证伪实验与研究写作

PaintsAlter按原视频/艺术家分组，固定后端做partition×step投影×查询类型消融；测联合/分批查询一致性、多个合理历史和真实动作，端到端延迟纳入tagger/调度。StrokeNUWA固定骨干/预算比较rawSVG、不同压缩、PC/PI/无Fixer，单列原始合法率/后处理几何代价；重排等价SVG，跨自然句/复杂度，以独立几何/语义事件指标补自码本Recall。全部未执行。

学习前者从用户查询推出形式化任务，后者从序列成本推出表示设计；Method依数据流分解，实验把重建/生成/人评/运行时对应具体Claim。Limitations须包括数据分组、域外失败、后处理、指标偏置与公开配置差异，现有不足仍需追引检索后才可作为新选题。
