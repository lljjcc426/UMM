# Ketaba-OCR-LoRA｜阿拉伯历史手稿转录与参数高效适配：原文、权重、代码交叉阅读

- 正式论文：Ketaba-OCR at AR-MS NakbaNLP 2026: Efficient Adaptation of Vision-Language Models for Handwritten Recognition
- 作者：Hassan Barmandah 等
- 发表：[NakbaNLP 2026，LREC 2026 Workshop，ACL Anthology](https://aclanthology.org/2026.nakbanlp-1.21/)，DOI 10.63317/3inc2znes52o；本次核查 2026-10-19
- 原始资料：[论文 PDF](https://aclanthology.org/2026.nakbanlp-1.21.pdf) · [代码仓库](https://github.com/HasanBGit/Ketaba-OCR-LoRA) · [HF 适配器](https://huggingface.co/HassanB4/Ketaba-OCR-LoRA) · [HF 基座](https://huggingface.co/sherif1313/Arabic-English-handwritten-OCR-v3)
- 已核查范围：论文正文和实验表、仓库 README、训练 YAML、训练/推理 Python、集成策略；本机未训练或运行权重。
- 分类：静态**阿拉伯语手写 OCR/HTR**、QLoRA 领域适配与集成；无视频输出、无笔画时序生成。

## 第一遍｜三句话

通用 OCR 对历史阿拉伯草写体、退化墨迹及领域差异敏感。作者以专门预训练的阿拉伯/英语 HTR 基座进行 4-bit QLoRA、DoRA/RSLoRA 微调，再融合多套预测，专注将历史手稿行图转为文字。盲测中集成模型每行平均 CER=0.0819、WER=0.2588；该数字仅衡量转录，不衡量书写顺序或视频内容质量。

## 第二遍｜五个问题

### Problem：输入和输出具体是什么？

输入是已裁切的阿拉伯历史手稿**行图像**，输出是该行机器可读的文字串。应用对象 Omar Al-Saleh Memoir Collection（1951–1965），字体包含 Ruq'ah 和 Naskh。论文不追踪笔尖、时间戳、书写方向，不根据转录生成视频。

### Motivation：旧方法欠缺什么？

零样本通用 VLM 在领域特定历史书体中容易混淆字符/附加符号；完全微调成本较高。作者利用已具跨书体 HTR 先验的基座，少量可训练参数适配目标域；采用多预测模型集成抑制不稳定识别。

### Contribution：实际增加了什么？

1. 将已有 Sherif HTR 视觉语言基座迁移到 NakbaNLP 阿拉伯历史手稿转录任务；采用 NF4 QLoRA 并启用 DoRA、RSLoRA。
2. 构造 Linear+Boost 权重：先用 (1−CER)，对所用校准分数低于 0.15 的模型增加 0.5，再归一化；后续按文字完全一致投票、阿拉伯书写规范化、n-gram 和字符串一致性等择优。
3. 说明逐行平均 CER/WER 和官方全语料拼接 CER/WER 的差异；这两个统计口径产生不同排名。

DoRA/RSLoRA 是已知参数高效微调技术；论文中尚未看到严格的一因子一消融来证明每种技巧独立带来多少提升。

### Method：精确实现流程

裁切行图 → Qwen2.5-VL 系列模型视觉输入处理器 → Sherif 阿英手写 OCR 预训练基座 → 4-bit NF4 量化（计算 bf16，double quant）→ 对 attention q/k/v/o 与 MLP gate/up/down 施加 LoRA/DoRA/RSLoRA → 用答案文本交叉熵微调（屏蔽用户问题 token）→ 单模型自回归文字解码 → 多模型集成择优 → 计算文本编辑误差。

**核实的仓库超参数：**

| 配置 | 代码及 YAML 数值 |
| --- | --- |
| 基座标识 | sherif1313/Arabic-English-handwritten-OCR-v3 |
| 模型结构 | Qwen2.5-VL 视觉语言生成/识别模型；模型卡称约 4.07B |
| LoRA | rank=32，alpha=64，dropout=0.05 |
| 扩展 | use_dora=true，use_rslora=true |
| 量化 | 4-bit NF4，bf16，double quant |
| 优化 | AdamW，lr=2e-5，cosine，warmup=200，weight decay=0.01，max_grad_norm=1.0 |
| batch 与 epoch | 每设备 batch=1、累积 4、1 epoch |
| 输入限制 | max_seq_length=2048、max_image_size=1024 |
| 其他 | seed=42，训练脚本显式把答案前缀 labels 置 -100 |

参数和实际 GPU 用量应依据固定代码 commit 与运行日志；作者 README 约 8GB 显存的表述不能视为端到端训练峰值的独立实测。

### Experiments：数据、主结果、对比与口径

论文/仓库说明常规 train 15,962、dev-test 2,095，系统最后用二者共 **18,057** 条作最终训练；另有独立 blind-test **2,671** 行。不能把合并的 dev-test 再当成未经使用的最终验证集。还需核对原论文是否另列开发分组（与本文最后训练分组分开陈述）。

| 结果 | CER ↓ | WER ↓ | 数据统计口径 |
| --- | ---: | ---: | --- |
| 单个微调 HTR 模型盲测 | 约 0.0884 | 约 0.2699 | 作者报告；模型与集成分开 |
| 最终集成盲测 | 0.0819 | 0.2588 | 每行独立计算后平均，作者称第 1 |
| 最终集成盲测 | 0.0938 | 0.2996 | 全语料拼接计算，官方榜第 3 |
| QARI 辅助实验模型 | 0.2635 | 0.5521 | 盲测，每行口径；非主集成的整体排名 |

CER 是字符编辑距离归一化后的比率，WER 是词错误率。阿拉伯语的词形拼接使 CER 与 WER 对错误敏感性不同。论文/README 对其他 VLM、组织方基线和 QARI 有对照，使用预训练数据与模型规模不同，不能把性能差异完全归因为 QLoRA 技巧。

**消融读法：**模型集成与单个 HTR 模型性能可比较；不同权重策略是组合器消融的线索。训练域、模型基座、适配器方案和集成策略同时变化的横向比较，不能当作某一种 LoRA 变体因果效应。要证明需固定同一基座、训练分组与 seed，再逐一开启 DoRA、RSLoRA、ensemble。

## 第三遍｜严格核对与质疑

### 代码/文档可复现性差异

- HF 官方适配器 ID 是 **HassanB4/Ketaba-OCR-LoRA**，但 GitHub README 示例和 src/inference/inference.py 默认参数写 **HassanB4/Ketab-OCR-LoRA**（少字母 a）。运行前必须固定实际可拉取的目标模型 ID；此处未做下载测试，不能断言重定向成功或失败。
- README 中个别表格把底座缩写为 **sherif1313/Arabic-English-OCR-v3**；configs/training_config.yaml、src/training/config.py 及 src/inference/inference.py 使用 **sherif1313/Arabic-English-handwritten-OCR-v3**。复现时以 pinned HF adapter_config 与代码依赖核对。
- 检查训练代码确实 mask 用户问题 token，且数据最终训练合并 dev-test；若后续重新划分开发集，避免调参评估反向影响盲测报告。
- 集成额外使用多个模型预测及调权；端到端延迟、每行成本和校准数据成本需另记，不能与单模型“参数高效”混为同一成本指标。

### 研究限制及可检验的迁移思考

1. 严重褪色、污损、符号相近和字符粘连是应当做错误聚类的样本；关注每类占比和样本级分数。
2. 当前资料没有跨年代、跨地区阿拉伯手稿的独立泛化验证；把它作为待核实验，而非断言其他领域全部失效。
3. 当前模型只有图像→文字能力。若用于 UMM 汉字书写研究，可把**低资源跨书体领域适配**作为迁移思想，先验证是否能读懂真实笔画前缀；生成能力需另配完整模型与实验。
4. 要测试模型学到字符几何还是文本语言先验，可用外观近似/无语义字符、稀有字及强制错序过程作为分布外反例。后者已超出原论文任务。

## 八项标准笔记

1. **Problem：**历史阿拉伯手写文本识别。
2. **Motivation：**历史书体域移位，通用模型零样本转录存在较高错误。
3. **Contribution：**专用 HTR 底座的 QLoRA + DoRA/RSLoRA 领域适配，以及集成策略与双 CER 评价口径。
4. **Method：**行图→视觉语言模型+低秩适配→文本候选→加权投票→最终转录。
5. **Experiments：**Omar Al-Saleh 手稿；单模型、其他识别模型、组合器对照；盲测 CER/WER，见上表；缺少可证明单个适配技巧独立贡献的充分分因子消融。
6. **Limitations：**跨语域泛化、影像退化，集成成本，公开推理 ID 不一致；对过程视频无指标。
7. **Insights：**借鉴少参数跨书体适配、强专业模型对比、双口径评价；切勿用 OCR 成绩替代笔顺执行正确率。
8. **一句话：**Ketaba 展示低成本专业手写 OCR 领域适配与集成可以改善文本转录，但未解决书写动作或视频生成。

## 如何借鉴其论文写法

Introduction 从具体应用域差异建立必要性；Method 先解释底座与数据，再解释低秩训练及集成；Experiments 把排名口径和不同方案明确列出；Limitations 应按未测语域及退化类别说明。未来写论文须报告硬件、成本、固定 split、学习率及种子，避免将多变量变化说成一种训练技巧奏效。
