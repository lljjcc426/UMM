# Calligraphy Bench｜中文书法智能体逐笔绘制基准（无独立正式论文记录）

- 名称：Calligraphy Bench: Can AI Write Chinese Calligraphy?
- 发布主体：Haize Labs；来源 [HF Dataset](https://huggingface.co/datasets/haizelabs/calligraphy-bench) · [官方 GitHub](https://github.com/haizelabs/calligraphy) · [Leaderboard](https://haizelabs-calligraphy-bench-leaderboard.hf.space/)
- 研究形态：2026 年公开基准与工程评测；本轮未检索到正式同行评审论文，不能编造论文会议
- 核查：2026-10-19 读取官方 README、数据字段、榜单；未得到私有 harness 的实现细节，没有独立复算评分

## 第一遍｜三句话

中文书法质量受笔画顺序、结构、笔触强弱和艺术风格制约，通用 AI Agent 在高难参考书法图下的程序化绘制能力缺乏统一比较。该基准在 88 个字符/书法家配对样本上，让多模态智能体通过 tldraw 工具依次创建或修改路径，用视觉裁判评分笔画召回、顺序、外观和成对偏好。现有模型在作者报告中笔顺项约 77–82%、外观相似度低于 2.5/5；这些是**匹配笔画比例及裁判评分**，不能写成 88 个字中相同比例全对，更不能转成视频生成的规范笔顺率。

## 第二遍｜五问

### Problem

输入：**一张书法参考图** + 文字/工具接口。Agent 调用 create_stroke / update_stroke / delete_strokes / capture_canvas / save_document 等 API，单条笔画由控制点 (x,y,z_pressure) 和 size 构成。任务输出最终 tldraw 画面和可供工具记录的笔画对象。没有要求输出 diffusion RGB 视频，也没有使用原生 UMM 视频解码器。

### Motivation

静态文字 OCR、FID 与最终图样本难以区分笔画次序、召回与审美；程序画布提供结构化动作接口，可以将生成分解为具体 strokes。但作者在 README 表述“vision judge”，还未公开可独立复核的每笔事件裁判输入、日志及跨裁判一致性；“可评价”不等于已经验证裁判对全部顺序反例均正确。

### Contribution

建立难样本参考库和标准化 Agent 工具执行环境，分别报告 stroke recall、stroke order、1–5 visual fidelity、MJ1 pairwise win rate，补充传统静态美学评测对动作生成的覆盖。原创性声明严格限于该工程基准及协议，无正式论文级方法新颖性证明。

### Method

88 条测试输入（20 位名家，楷/行/草等） → 模型收到视觉参考 → 工具连续插入二维几何路径并附压力系数 → 保存最终图 → 作者的视觉评分器按规范笔画匹配和排序评价，配合图像保真及成对判别。HF 数据实际 Viewer 可见 stroke_count、strokes_svg、medians 等字段；字段来源、规范参照和是否用于裁判需下载/代码核实。

### Experiments

| 官方榜单（作者报告） | 笔画召回 | 笔顺分 | 外观相似 (1–5) | 偏好获胜率 |
| --- | ---: | ---: | ---: | ---: |
| GPT-5.4 | 86% | 82% | 2.2 | 75% |
| Claude Opus 4.6 | 89% | 77% | 1.6 | 60% |
| Kimi K2.5 | 83% | 79% | 1.3 | 34% |
| GLM-5 | 71% | 78% | 1.3 | 30% |

**环境：**公开使用 OpenHands SDK 与 tldraw MCP 工具，模型需可访问兼容 OpenAI Chat Completions 的视觉 API；训练数据/温度、token 限制、推理重试次数、各项评分的置信区间与全部原始动作文件未见充分官方公开说明。不能据此做严格等预算能力排序。

**对比方法：**上述四个 Agent；尚未与笔画规则引擎、传统在线 HTR 轨迹生成器、VideoSketcher RGB 视频模型以统一输出形态对照。

**消融：**文档未给“仅规则 vs 仅视觉 vs 可迭代画布”等因子消融，待建立可重复评测。

## 第三遍｜实质性科研质疑

1. **视觉 judge 如何读顺序？** 同一最终图像可由不同历史绘制。若裁判仅看最终画面，按信息论无法认出真实历史；若读取动作对象的 creation order，则可验证，但需要公开提取细节。这是首要复现疑问，不能提前断言作者方法出错。
2. **一笔与多笔匹配：**一个长轨迹合并两笔或一笔拆成多对象，order fraction 分母受匹配策略影响。必须额外测 strict exact-order、漏笔、重复、跨笔合并。
3. **书法风格与规范：**原图可能是草书/行书；应提供字体/规范允许的序列集合。书法家的实际风格差异和规范汉字楷书顺序不能混作唯一真值。
4. **人工与裁判对齐：**对相同几何图但乱序绘制的测试、复制对象后移动的测试、不同压力/顺序的对照，量化裁判误检。
5. **对原课题的影响：**“中文逐笔绘制基准无人提出”已不成立。视频 UMM 的潜在贡献需聚焦**不暴露工具日志的 RGB 过程观测、实际事件严格可证性、执行器服从规范、同资源下联合训练收益**。

## 八项模板

1. Problem：多模态 Agent 程序化书法绘制与执行顺序评估。
2. Motivation：静态文字与美学指标缺少动作与笔画维度。
3. Contribution：88 个难字样本、20 位书法家风格与四类评价；提供 HF 数据/榜单/工具接入。
4. Method：图像参考→Agent→笔画 API→画布图与评估。
5. Experiments：四个前沿 Agent；官方百分比见表；训练细节/重试预算/消融待核。
6. Limitations：视频生成之外的独立工具任务、评分器过程可审计程度有限、样本数少、样本选取高难且风格混杂。
7. Insights：使用数据中 medians/strokes 构造合法/错序过程；要求 **两条历史同一最终图，裁判给出不同结论**；新增精确事件证据链。
8. 一句话：Calligraphy Bench 已覆盖中文书法笔顺 Agent 评价，但未验证无结构化工具日志时的 RGB 视频真实笔画顺序。

**论文写法启发：**从被测任务本身的可操作定义出发，报告每项分数的分母和统计定义，不用带“stroke order”的名称掩盖判定器所见信息。
