# 统一视频、静态文字、草图动画与资源协议的交叉复核

2026-10-20；第二十九批。九项已有记录补独立分析，无新增独立文献，无删除，无模型运行。334条当前记录均有结构化笔记，五条仍仅摘要；完整三遍和扩展检索继续。七篇新增书面理解检查，不将它们自动计作完整三遍。具体字段、已读范围和待核项见[笔记目录](../reviews/README.md)。

## 统一架构的结论需要版本和成本条件

[UniVideo v4](https://arxiv.org/pdf/2510.08377v4)是当前主技术来源，不能沿用旧v2的VBench82.58作为最新结果；v4为83.48。GenEval原prompt.53、改写.69，均低表中BAGEL.82。冻结Qwen2.5VL的理解成绩不能证明视频生成联合训练带来理解增益。MLLM7B和HunyuanVideo13B应分别说明，不能只把7B当全系统规模。hidden与512query两版本均保留；冻结MLLM参数仍可能需要为query优化保留反传图。

v4 Table7给shift5，固定[公开隐藏态配置](https://github.com/KlingAIResearch/UniVideo/tree/893c9da04b87fdf5099e8e0e9ef164bca6753327)示例shift7/2条件帧；RefVIE加Ditto fallback的训练演示不能当论文全部配对监督。骨干cross/selfattention比较同时换预训练和可训练参数，未单独识别attention形式的因果效应。

[Lance v1](https://arxiv.org/pdf/2605.18678v1)实现语义与视觉专家交错上下文，MaPE、任务比例和多阶段训练均有作用证据。3B是active规模，实际总参数待核；两个decoder/ViT从Qwen2.5VL初始化，from scratch说法需给定义。OCR GRPO针对图像，不能外推视频笔顺。Table9多任务比例不存在所有指标统一最优点。固定[公开微调文档](https://github.com/bytedance/Lance/blob/4baeee086648996f6ab12e673cbe461b0b149997/train.md)说明validation尚不支持；debug repeat256、训练分辨率和公开示例须与论文全量协议分开。

## 静态文字与已知在线轨迹不能替代过程监督

[XMPFont正式CVPR2022](https://openaccess.thecvf.com/content/CVPR2022/html/Liu_XMP-Font_Self-Supervised_Cross-Modality_Pre-Training_for_Few-Shot_Font_Generation_CVPR_2022_paper.html)用笔画类别序列预训练图像表征，输出静态字形。未知字体FID36.80及模块消融支持该设置，但没有笔尖位置、真实时间、压力或动态视频评价。§3.4的30训练字体与§4.1的100训练字体描述仍待对应。用户偏好差是28.42百分点，不是相同数值的相对提升。

[L176](https://arxiv.org/pdf/2402.15307v1)输入已经观测到的在线轨迹，通过坐标串与时间/距离颜色提升LVLM识别；它丢弃抬笔间隔且对轨迹重采样。双输入改善CER不证明从静态图能唯一恢复过程。越南文MyScript仍更好，LoRA5B也未全面优全调700M，模型规模和参数高效适配不能只看单指标。

[UMText](https://arxiv.org/pdf/2601.08321v1)输出静态设计图；正式AAAI DOI [10.1609/aaai.v40i10.37722](https://doi.org/10.1609/aaai.v40i10.37722)已核，技术差异尚未对正式PDF复读。UDiff重建LPIPS.0479劣DreamText.0328，与正文更低叙述冲突；训练Planner用了产品域，不能把整个pipeline称未见该域。共用Planner布局的对照主要评价渲染器；RCI中的Canny路径需实现验证。

## 画布编辑、草图动画与绘制过程

[PaintFlow](https://arxiv.org/pdf/2512.08534v1)让用户按局部mask、sketch、参考图编辑画布，训练数据来自合成油画，缺真实画家创作轨迹。论文AAAI2026页脚尚无本次独立主办录用证据。完整FID234.27相对所列对照改善，但训练文本通道关闭、推理融合lambda来源及参考条件预算仍有缺项。不能据多次静态编辑称已生成规范不可逆笔过程。

[VidSketch v2](https://arxiv.org/pdf/2502.01101v2)将草图关键帧转成自然动画。固定[训练代码](https://github.com/CSfufu/VidSketch/blob/ad7fcdb8099e39d253364275711a992febb91eb4/VidSketch/train_vidsketch.py)把首帧恢复为clean latent，loss排除首帧；这部分与论文一致。[candles.yaml](https://github.com/CSfufu/VidSketch/blob/ad7fcdb8099e39d253364275711a992febb91eb4/VidSketch/configs/candles.yaml)覆盖函数默认，设lr3e-5/b1/15K，与论文相同，不能只读默认lr3e-6就判不一致。

公开[inference.py](https://github.com/CSfufu/VidSketch/blob/ad7fcdb8099e39d253364275711a992febb91eb4/VidSketch/inference.py)计算抽象度后仅打印，pipe仍固定tau=.5/scale=.65；detail使用轮廓数，未用论文GLCM。[pipeline](https://github.com/CSfufu/VidSketch/blob/ad7fcdb8099e39d253364275711a992febb91eb4/VidSketch/inference/pipelines/pipeline_VidSketch.py)以t≥(1−tau)T注入adapter，对降序t是早期去噪。该入口不足以复现论文自适应逻辑，论文实验实际版本仍待。主表PickScore非最高，人评47.92是12case之和，约3.99/5。

## Calligraphy Bench：公开全量元数据与评分语义

固定[数据卡](https://huggingface.co/datasets/haizelabs/calligraphy-bench/blob/d3f189f76568729def5e845569543ba9786c317e/README.md)称88字符、20书家；公开[datasets-server](https://datasets-server.huggingface.co/rows?dataset=haizelabs%2Fcalligraphy-bench&config=default&split=test&offset=0&length=100)返回完整88行、partial=false，实际82个不同Unicode字符、18个书家标签。39行stroke_count与SVG/中线长度不同，后两者相互一致；逐行计数存[精简审计](../../data/calligraphy_bench_metadata_audit_2026-10-20.json)。当前缓存没有不可变parquet revision，与固定README版本边界分开。

[官网](https://calligraphybench.com)公开应用说明canonical SVG/中线来自Make Me a Hanzi，书家图像来自Kaggle另一数据集。工具允许修改/删除/清空笔画和保存最终画布，不能当无撤销真实书写动作。stroke recall为X/N，order为Y/X，只在匹配笔中计序，漏笔可能不被order单项惩罚。39项差异可能涉及跨来源变体/元数据滞后，未读judge全部实现/输出和逐图对应前，不能断言评分错误。模型排名为作者报告，未重跑；仍需judge提示、版本、API日期、调用预算和校准人评。

## 无独立论文制品仍须核具体接口

[CoFRIDA-Sharpie固定卡](https://huggingface.co/skeeterman/CoFRIDA-Sharpie/blob/58d397f81bd0bf64eb43d85ee8bd5191acd9824d/README.md) YAML列diffusers/sdxl-instructpix2pix-768，正文列timbrooks/instruct-pix2pix；无法据两个描述确定204MB权重实际base。未下载运行权重、未将相关论文表格赋予这个制品。卡没有完整rank/lr/adapterconfig和机器人链说明，这些缺失影响可复用性，仍有研究记录价值。
