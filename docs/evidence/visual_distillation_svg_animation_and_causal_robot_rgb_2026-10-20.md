# 视觉蒸馏、矢量动画与机器人低频观测

## 阅读完成度的判定

本批L187–L190完成用户要求的核心三遍阅读：问题定位、方法/核心公式作用、框架图、主结果/消融和批判性分析，并逐项记录五个理解检查。计时口试、全部源码审计和独立复现分别记录，不额外作为读懂论文的必要条件。未取得的关键原文不能据摘要升级。此前40项书面检查仍保持原状态，随后逐篇核定核心阅读是否完成，不批量改标。本批无模型运行、无文件删除。

## Visual-OPSD：额外视觉监督的作用与生成分支来源

[v6原文](https://arxiv.org/pdf/2606.18974v6)报告九任务均值74.03，优于完整ThinkMorph70.63，也优于同初始化直接关闭视觉思考的69.90。后一差值为4.13百分点；对BAGEL起点SFT的10.28百分点混有初始化和步数差异。Noise条件64.15低于同初始化直接推理，不能仅对较弱SFT称小幅改善。

teacher多看预存视觉思考图，student仍读取原问题图；训练不调用当前生成路径。两者初始同权，随后teacher使用EMA。真实参考比Noise高9.88百分点，支持参考语义有用；尚未排除真实crop、人工diagram或一般特权视觉监督的替代解释。14.3倍延迟比含关闭多步生成和缩短输出的作用，缺直接关闭视觉思考的延迟，不能全归蒸馏。

[固定loss代码](https://github.com/TiezMind/Visual-OPSD/blob/32f245d03aaa6d06e16ca608c38f8895b2c433a3/scripts/visual_opsd/opsd_loss.py)逐词表分量clip后求和，与v6对应。完整JSD凸性下界不能证明topK、clip、EMA优化的全局最优性。论文7B骨干与1822M总参数描述、[EVAL示例](https://github.com/TiezMind/Visual-OPSD/blob/32f245d03aaa6d06e16ca608c38f8895b2c433a3/EVAL.md)的温度/长度及部分judge口径存在差异，实际日志未取得。详见[L187](../reviews/L187.md)。

## LiveSVG与AniClipart：动画路径与不可逆绘制

[LiveSVG v1](https://arxiv.org/pdf/2605.30174v1)先生成10–20个候选视频、筛选目标，再拟合组homography和局部Bézier参数。86.7%人评为逐例best-of-three oracle，固定Veo变体66.7%；候选生成和筛选成本应独立列明。时间/显存与采样次数在正文、表和附录有不同数字，笔记保留差异，不拼成单一复现配方。颜色消融同时改变目标视频，无法只归因优化对应。见[L188](../reviews/L188.md)。

[AniClipart正式IJCV论文](https://doi.org/10.1007/s11263-024-02306-1)发表于133卷3149–3165页，2024年在线、2025年卷期。它通过关键点Bézier轨迹、可微ARAP与视频SDS生成保形动画。正文数据为30个SVG，后续工作所用43例必须核版本。线性轨迹的连续性更高、变形更低但运动小，展示指标权衡。默认正向再倒放的loop不能表达不可逆墨迹累积。见[L189](../reviews/L189.md)。

两项均以已有SVG形状的运动为核心，不提供从空白逐笔出现的规范笔顺监督。可迁移低维几何和可微渲染思路，但需另外定义笔尖接触、抬笔、墨迹累积和事件可观测性。

## VitaGlyph：正式版强基线与公开实现范围

[WACV2026正式版](https://openaccess.thecvf.com/content/WACV2026/papers/Feng_VitaGlyph_Vitalizing_Artistic_Typography_with_Flexible_Dual-branch_Diffusion_Models_WACV_2026_paper.pdf)加入QwenImage：中文OCR92.23持平，CLIP26.58低于27.45、FID236.15差于232.07，美学较高。去语义变形后的OCR92.98更高，不能把所有分项改善合并成全面优势。

[当前公开实现](https://github.com/Carlofkl/VitaGlyph/tree/ca7d0f82524d855b76dfd755ab91bb245c0587d7)手工输入prompt、不同检测阈值、单主体范围及attention实现选择与论文设置有区别。预印本SDXL与SD1.5描述也需保留版本冲突。正式版图像到视频是后接应用，未给规范笔顺的量化证据。见[L190](../reviews/L190.md)。

## Datumwell：50fps容器与约3Hz原生视觉

[固定公开10例资源](https://huggingface.co/datasets/allen-datumwell/datumwell-handwriting-sample/tree/b58ba9d09a907333a0733fbfc415e381c06765e6)提供59338条数值记录与30段视频，train6/test4；200例源集合需申请，本轮未申请。它是MuJoCo模拟执行加外观重渲染，action为五维计划绝对关节位置，normal_force为模拟观测，没有压力动作标签。

50Hz数值/视频索引通过因果保持旧原生帧对齐；首例378个原生时间戳的中位间隔约.334秒，即约2.994Hz，整段平均约2.998Hz。重复帧不会增加短笔事件信息。辅助OCR9/10来自最后俯视原生帧，不是过程质量；便利样本不等统计代表性测试集。未下载完整视频/轨迹、未训练policy。

检查结果存[精简元数据审计](../../data/datumwell_metadata_audit_2026-10-20.json)，详细动作/字段/权限和可证伪实验见[R09](../reviews/R09.md)。尚未定位到对应独立论文，仍需继续检索，不能用关联论文结果替该资源作质量保证。
