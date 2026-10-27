# 2026-10-27：直接前作复核及其对v2设计的约束

范围：原始出版/作者页面、指定官方README。未完成本轮所有PDF/附录逐图精读、下载权重或独立复现。以下补充不改变主目录360条或核心阅读327篇计数；新增研究应在完整建卡后再合并主目录，避免题录、代码和模型卡重复计数。

| 研究 | 本轮原始证据 | 已确认内容及研究影响 |
| --- | --- | --- |
| HiSAC: Hierarchical Style Aggregation for Versatile Chinese Handwriting Generation | [Springer ECCV2026正式条目](https://link.springer.com/chapter/10.1007/978-3-032-37490-5_6)，2026-09-16在线，pp104–122；仅元数据/摘要/参考文献 | 部首/部件/笔画层级空间风格对应、多频风格编码、在线Transformer轨迹和离线扩散图像接口。层级笔画/风格组合已有前作；摘要不足以说明规范RGB视频已解决。链接[IIP-Lab-XDU/HiSAC](https://github.com/IIP-Lab-XDU/HiSAC)的README本轮返回404，不把“代码已发布”变成已取得制品。 |
| Teaching an Agent to Sketch One Part at a Time | [arXiv2603.19500](https://arxiv.org/abs/2603.19500)、[作者项目](https://xiaodan.io/teaching-an-agent-to-sketch/)、[作者主页](https://xiaodan.io/)、[官方README](https://github.com/duxiaodan/teaching-an-agent-to-sketch-one-part-at-a-time)，blob f87f1b1bf24d5bbb9334cd592279557242f97644 | 部分级矢量草图、画布视觉反馈、SFT+多轮过程奖励，ControlSketch-Part。作者主页/仓库声明ECCV2026；本轮没有另核Springer终版。不能声称首次让VLM看画布后继续绘画或首次加过程奖励。 |
| OnOff | [作者项目](https://seonmip.github.io/onoff/)；仓库已有[N02笔记](../../reviews/N02.md) | 轨迹生成、参考风格笔刷参数、可微渲染、静态增强和机器人执行；在线/离线配对包括CASIA。项目标ECCV2026，code/data仍coming soon；不声称完整代码现成可跑。逐步渲染+风格机制必须纳入强替代路径。 |
| VideoSketcher | [作者项目](https://videosketcher.github.io/)、[已有L010](../../reviews/L010.md) | LLM语义计划+视频生成；作者明确披露多笔同帧、指令偏离、AR画质差。它提供RGB执行不足的具体动机，但本项目汉字错误率仍需新实验。项目标WACV2027为作者接收声明，当前日期尚早于会议年份。 |
| LVGM/OLHWG/DiffInk/InkSight/UniCalli | [A04](../../reviews/A04.md)、[A02](../../reviews/A02.md)、[A03](../../reviews/A03.md)、[X01](../../reviews/X01.md)、[N01](../../reviews/N01.md) | 逐笔向量、多字轨迹、读写联合与静态书法生成已有前作；这些任务中的准确率不可转成RGB规范笔顺排名。沿用仓库核读范围，未冒充本轮重读原文。 |
| 规范笔顺动画/工程制品 | [Make Me a Hanzi](https://github.com/skishore/makemeahanzi)、[Hanzi Writer](https://hanziwriter.org/docs.html)；之前调查的hbg-hanzi-chaizi-video、sweety-handdraw-video为工具路径 | 在已知模板下生成汉字笔顺动画已有基础。v2保留规则与轨迹渲染，测试应用需要超出它们的哪项能力。工程输出MP4不自动说明学习型视频模型已训练。 |
| DiffChar | [出版方入口](https://www.sciencedirect.com/science/article/pii/S0031320325009689)本轮403 | 先前调查归类为空中书写轨迹生成；本轮未取得新增全文证据，不加入可复现主baseline或推断RGB落墨性能。 |

## SketchOnePart开源状态需注意

官方README写明原实验Qwen3-VL-30B-A3B，现脚本默认换为Qwen3.6-35B-A3B，并明确替代模型未测试；不能把默认脚本直接视为原论文精确复现。训练/示例评估依赖Tinker服务和账号，推理输出SVG/PNG且该脚本不直接计算指标。作者另提供合并权重说明，本次未下载。原始LoRA导出并非直接PEFT加载格式。源码服务、数据版本、权重与论文成绩要各自固定。

## 对创新表述的硬约束

不主张“首次生成汉字”“首次加笔画层级”“首次用视频画图”“首次画布反馈”。当前候选主张只能在实验后写成：在规定输入和数据预算下，空间事件状态与RGB执行约束减少了已明确的笔顺/漏笔/同步添墨等失败；共享收益和反馈收益分别经对照成立。

不存在全领域零遗漏保证。若运行前发现更直接的同协议工作，应更新基线合同，而非隐去前作。文献总数不作为本项目能力或创新证明。
