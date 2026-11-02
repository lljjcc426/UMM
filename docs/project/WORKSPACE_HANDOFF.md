# 下一实验工作区交接

## S0–S1追加交接（2026-11-02）

最新补齐见[全量报告](../research/paired_strokes_v1/s0_s1_completion_2026-11-02.md)：S0完成，S1 CPU工作完整覆盖PRE-01至PRE-07，新增对照后2232条离线请求，原1504条主清单和阈值保留。208项CPU测试与一个浏览器工作流通过；240字/2189笔的12批审核包已准备，实际新审核仍为0。不能称全量S0–S1已完成，剩余实际独立审核须交还；原16字不重审。PAIR只核对图文规范序列，不升级E3/E4/E5；新的合格pilot导出按原train/validation/test分开。没有模型调用或训练。

当前实际分支为`codex/research/new`。用户已直接授权静态图文配对S0–S1，本轮CPU交付见[执行报告](../research/paired_strokes_v1/execution_report_2026-11-02.md)和[协议](../research/paired_strokes_v1/protocol.md)。256字候选配对及评价工具已实现；后续已收到16字/54笔独立审核，见[接收报告](../research/paired_strokes_v1/human_review_receipt_2026-11-02.md)。E3/E5各16字通过，E4为14字通过、“未”unknown、“一”不适用；D-SMOKE数据侧16对具备资格，240个pilot候选仍待审，无正式保留集。1504条请求未执行模型推理，模型分值保持null。新模型权重、GPU/MPS调用、训练、远端推送、main及S2–S6没有授权。P0/P1/Batch A状态与历史原文保留。下文为此前整理交接快照。

整理日期：2026-11-02。当前分支`exp/p1-process-diagnostic`，整理前HEAD为`a1c2d5fbe3f00d80cf1ad00d8819ea322e05cdad`。本轮保存上一轮未提交的复核材料并更新导航；没有开始新实验。

## 先读什么

1. [AGENTS.md](../../AGENTS.md)：本轮权限、科学证据与分支边界。
2. [Batch A科学复核](../research/next/batch_A_scientific_review_2026-11-01.md)：最新科学判断及FIT-01缺口。
3. [当前研究导航](../research/next/README.md)：Benchmark、SC-CoIT、模型接口与原执行报告。
4. [新实验计划模板](../../templates/experiment_plan.md)：填写下一问题、精确对照、资源、授权及验收。

## 已完成与未获批准

| 项目 | 已有证据/状态 | 下一任务须保留的边界 |
|---|---|---|
| P0/P1 | 有限负结果结项；原状态、负结果及资格缺口保留 | 工程整理不改变正式发布状态；P1主线合并未批准 |
| Batch A | 24次精确调用，20原答、4原片；182项CPU测试；只读复核完成 | 工程有效不等于能力通过；3项截断、失败和正面个案全保留 |
| K-CHAR | 当前Video管线四个错答个案 | 无原生image/官方正控、主模型加载键覆盖，尚不能完全排除接口因素 |
| H-ACTUAL | 同末帧配对成立；013局部时序正确，多项明确事实错误 | 时间编码有混杂，未证明可靠理解历史或唯一根因 |
| G-ATOMIC | 023源/解码均向右增长；其他三项形状/过程不足 | 单seed与开发微任务，不能外推完整汉字 |
| FIT-01 / Batch B / Batch C | 对照与接口契约已准备，尚未执行 | 监督资格、配方、容量/预算和单独批准仍需确定 |
| 工程与本机LTX | 8字受控预览；2段LTX真实原生视频及技术失败记录 | 预览不算原生UMM成绩，未证明正确书写或规划能力 |

本次整理只授权本地文件、导航和保存。新GPU/MPS调用、训练、模型/数据下载、付费资源、远端推送、main修改或合并没有因此获得批准。下一目标尚待用户指定；未代为建立新实验或新分支。

## 目录与运行入口

| 路径 | 用途 |
|---|---|
| `scripts/diagnostics/` | CPU数据构造、评价契约、观察器、原生输入采证、执行器与汇总 |
| `configs/research/next/` | Benchmark与候选训练对照配置 |
| `data/research/next/` | 准备快照与冻结24请求，禁止清空state或改ID后重跑 |
| `data/research/runs/diagnostic_batch_A_2026-11-01/` | 本批原授权、实际调用、环境、资源与结果 |
| `data/research/reviews/batch_A_readonly_2026-11-01/` | 独立追加复核、能力矩阵、每帧与每请求证据 |
| `docs/research/next/` | 实验报告、文献审计与下一步建议 |
| `templates/experiment_plan.md` | 下一实验的空白计划；不含默认批准 |

从仓库根目录运行CPU工具并使用现有`.venv`。例如，以下命令只汇总已有文件：

```bash
.venv/bin/python -m scripts.diagnostics.summarize_batch \
  --root private/diagnostic_batch_A_2026-11-01/server_artifacts \
  --output reports/batch_A_existing_evidence_summary.json
```

`scripts.diagnostics.execute`为真实模型执行入口，不属于CPU整理命令；新任务获得精确授权前不要运行。原固定恢复脚本也不构成再次下载许可。

## 私有证据与环境

| 本地路径 | 内容 |
|---|---|
| `private/diagnostic_batch_A_2026-11-01/server_artifacts/` | 原答、原片、编码前RGB、解码RGB、实际输入、采样、变换张量与原生源代码 |
| `private/diagnostic_batch_A_2026-11-01/server_backup/` | 原完整服务器证据备份，复核时哈希已确认 |
| `private/batch_A_readonly_2026-11-01/Batch_A_scientific_review_sanitized.zip` | 52,767,875 bytes独立审核包，解压后打开index.html；20原答/4原生输出及20段输入载体 |
| `private/research_restart_2026-11-01/` | 启动包、论文、开发数据与已用输入 |
| `private/`中的其他日期目录 | P0/P1、工程与LTX旧原件/独立环境，按原报告定位 |
| `checkpoints/` | 本机模型缓存，保持原位 |

上述目录被Git忽略；普通提交不会包含审核ZIP、原始大文件或权重。文件路径可复用，不代表环境在未来服务器上仍存在。本轮没有SSH或联网核查服务器/远端。

一次磁盘盘点：`.git`约212MB、`.venv`约1GB、`checkpoints`约25GB、`private`约30GB、`data`约174MB、`docs`约22MB。8个已跟踪文件超过5MiB，均是旧P0清单/预测/审核/媒体证据，最大约30.42MiB；本轮保留，不引入LFS或改写Git历史，也未删除缓存腾空间。

## 分支交接

本地P1分支`research/p1-native-baselines`停在`ed92bd8a`，工程分支`codex/engineering-hanzi-video`停在`d40d7647`，当前分支连续保留这些未推送成果。其他分支与工作树不改动。

本地`main=e95bed37`，缓存`origin/main=ce2bc8a8`，本轮未fetch；不能据此声称已核对GitHub最新状态。下一实验分支和基线须根据用户的新任务确定，不自动切main或覆盖当前工作。Git身份：`lljjcc426 <3115250840@qq.com>`；本轮仅本地提交。

## 本次具体整理

- 保存原先未跟踪的Batch A复核报告及`data/research/reviews/batch_A_readonly_2026-11-01/`；原私有审核包原位保留，未重新打包/重复哈希。
- 更新`README.md`、`docs/project/STATUS.md`、`docs/research/README.md`、`CONTRIBUTING.md`、`data/README.md`，突出当前状态与入口；五份旧导航原文完整保存于[archive快照](../../archive/workspace_navigation_2026-11-02/README.md)。
- 在`AGENTS.md`与`BRANCH_WORKFLOW.md`增加当前交接指针，在`archive/README.md`增加快照入口。
- 新增本交接、当前研究README、复核目录README、实验计划模板及独立整理记录。文献计数按现有主数据修正文档为360项（333篇论文/研究、27项资源），未重生成导出表。
- 未删除或移动实验文件、旧分支、原答、视频、权重、阈值、人审及历史报告；未修改正式实验登记、P0/P1发布状态、运行器、测试或CI逻辑。

本次只运行目录/链接与既有协议/阶段开发门禁等适用CPU检查；旧182项模型相关代码回归不因导航改动重复。实际检查结果见[整理记录](../../data/research/workspace_cleanup_2026-11-02/record.json)。
