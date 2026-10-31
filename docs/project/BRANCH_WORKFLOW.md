# 科研分支治理与阶段合并标准

## 当前工程工作流（2026-10-31）

用户已确认将当前工作转为规范汉字视频工程，允许UMM识别/规划与受控执行组合。工程分支`codex/engineering-hanzi-video`从保留未推送P1结项提交的`ed92bd8a`建立；这次派生用于保存连续历史，不代表P1获准合入main或启动P2。P0/P1契约、科学结论和分支保留。

本轮可在本地实现、调试、测试与保存工程成果。工程交付按[独立工程契约](../engineering/hanzi_video_v1.md)检查实际功能、参考覆盖和模型实测边界，不关闭或篡改研究门禁。真实UMM联调所需的新GPU、付费调用、训练、扩大数据授权及远端推送需要新的明确授权；模型未连接不得冒充UMM成功。main仍只能通过用户明确批准的PR进入，禁止直接写入、自动合并。当前研究CI与严格合并门禁保留；新增`codex/**`触发及工程目录检测不会授予科学批准。

下文为保留的研究阶段制度。

更新：2026-10-27。本文件在研究阶段分支中先行实践；当前 `main` 的 GitHub `protected=false`，未设置规则集。平台强制性保护需要仓库拥有者另行配置。

## 分支角色

| 分支 | 职责 | 合并条件 |
| --- | --- | --- |
| `main` | 稳定研究协议、已经验收的模型/代码/数据与可支持的结论 | 只能通过经用户批准的 PR；所有必须检查与科学审核通过 |
| `research/p0-stroke-video-foundation` | 历史P0：已有限负结果结项，分支与原证据保留 | 已获准P0 PR #2合入main，原科学失败保持 |
| `research/p1-native-baselines` | 当前P1：已按明确批准的有限范围负结果结项 | 最终报告待审阅；main合并及下一阶段仍需单独批准 |
| `research/pN-主题` | 后续阶段集成分支，从已验收的最新 main 派生 | 按阶段验收，独立 PR 进入 main |
| `feat/pN-*` / `fix/pN-*` / `exp/pN-*` | 某个功能、缺陷修复、隔离性实验 | 测试后汇入阶段分支；常规不得直入 main |
| 已存在的其他研究分支 | 历史/并行实验，协议可能不同 | 保留原样；审计并获用户许可后选择性移植 |

## 每个阶段的执行周期

1. **澄清研究意图**：Codex 在新任务执行前向用户提问、复述目标、预算和验收条件，取得明确批准。
2. **开发与试验**：只在获准研究分支上修改；每个 run 固定模型/代码/数据 revision、随机种子、完整命令、原始输出、失败和成本。缺少资源或授权时标为 blocked。
3. **证明工程可用**：完成适用的代码/配置/数据检查、回归测试和无泄漏检查；CI 成功不等同于模型实验结论成立。
4. **验证研究结论**：必须有符合该阶段问题的强基线、评价协议、实际运行产物、分母与失败样本、独立评审/人工核验及统计。可以得出经过验证的正结论或负结论。若结果无法判定，则保留分支继续验证或明确停止，不将其标成通过。
5. **用户阶段验收**：总结结论、未完成内容和反例；取得用户明确允许提出合并请求的决定。
6. **PR 审核**：向 main 提出 PR，附阶段清单、每个实验的运行路径、结果/样本覆盖、CI 链接和用户批准引用。所有适用门禁通过并经用户确认后才合并；禁止自动合并。
7. **下一阶段**：合入 main 后从最新 main 开始新的阶段分支，旧阶段分支保留供追溯；未经用户允许不删除。

阶段门禁CLI默认读取`configs/research/stroke_video_v2.json`的`current_phase`所对应发布文件；当前为P1。审计历史P0可显式使用`python scripts/validate_stage_release.py --phase P0`。研究分支开发检查通过不授予科学验收或main合并权限；P1范围结项后，缺少最终报告审阅及main合并批准时严格合并门禁继续拒绝。

## P1有限负结果结项（2026-10-31）

用户已明确批准[P1有限原生基线负结果范围](stages/P1.md)，批准记录见`data/research/runs/p1_closeout_2026-10-31/scope_approval.json`。该范围独立于P0例外，不推广至P2以后。原P1契约、原发布清单和原登记留档，四项未满足标准及原阻塞明确保留，允许结束本轮而不追加GPU或机械人审。

P1使用schema2/closed_with_negative_results/supported_negative，BASE-01为completed_negative，SO-00/EVAL-02/SO-01为completed_with_limitations，original_scientific_gates_met=false。已归档的双人粗筛不得升级为完整七维金标，H1继续not_established，自动辅助及unknown保留规则不变。原缺口记入closure.unmet_original_criteria及closure.previous_blockers；当前unresolved_blockers仅表示获准有限范围内尚未完成的工作，不代表原问题全部解决。

本地结项检查验证P1专属范围批准、原契约、原清单、报告、终态及证据。当前范围批准不授予新报告的最终审阅结论、main合并或P2执行。P1严格合并检查即使标为ready_for_review，也要求user_final_report_review=approved、main_merge_authorized=true及独立存在且不同于范围批准的合并批准文件。缺少任一项就拒绝。当前仅本地提交，不推送或合并。

## P0 有限结项及合并门槛（2026-10-30修订）

用户已明确批准[P0有限研究基础契约](stages/P0.md)。[原契约](stages/P0-contract-preclose-2026-10-29.md)及原阈值保留；本次阶段完成允许有充分证据的负结果和明确记录的资格缺口。ENV-01保持批准配方内通过，DATA-01以completed_with_limitations、EVAL-01以completed_negative结束本轮，不伪装成原标准达标。

发布schema2以closed_with_negative_results、supported_negative及original_scientific_gates_met=false表示结项。必须有范围批准、原契约/原发布清单、最终报告、全部运行及结果路径、原未满足标准的明确处置。未解决科学事项留在closure.unmet_original_criteria和限制中，不凭清空阻塞项伪造通过。普通completed仍用于原批准范围确已通过的任务。

本地结项门禁与main合并门禁分开。结项检查通过允许准备研究分支审核PR；普通阶段仍须`ready_for_review`、用户最终科学审核及明确合并批准。已科学结项的P0负结果阶段可保留`closed_with_negative_results`终态，在独立存在的main合并批准文件、`closure.main_merge_authorized=true`、`closure.user_final_report_review=approved`全部具备时才通过`--require-ready`。原科学失败标志不得改写；范围调整批准不能替代合并批准。草稿PR用于审查证据，GitHub草稿状态本身禁止合并；草稿CI通过不授予科学验收或合并批准。转为正式PR时必须执行严格合并门禁，缺少最终批准就拒绝，不能伪填批准使检查通过。

CI分别显示`engineering`与`validate`。前者运行目录、协议、阶段证据及全部测试；后者保留原检查名称，采用always运行并明确拒绝工程失败，再通过`--github-event`按GitHub实际PR状态选择门禁。研究草稿返回`approval_gate=deferred_non_mergeable_draft`，校验发布证据但不要求尚未申请的合并批准；正式研究PR返回`approval_gate=required`，完整执行原`--require-ready`规则。工作流监听opened、synchronize、reopened、ready_for_review及converted_to_draft，确保转换为正式PR即重跑批准检查，后续提交或恢复PR也重新检查。此前0684e3b2将草稿也作为合并候选而持续报错，本次修正该触发语义，历史失败保留。GitHub平台强制保护尚未启用，不能将检查名称等同于已配置的required status check。

自动评分器高可靠性改进为后续可选项。P1采用可信规范参考、独立人工实际RGB主评、自动辅助及严格未知处理，不以EVAL-01科学指标必须转正为前提；所有前置依赖仍须有已完成的结果和决策记录。P1 GPU实验、租机和训练均需新的明确批准；新执行分支仍从最新获准main派生。

后续P1–P6适用[v2实验协议](../research/v2/experiments.md)。任何有限结项均须用户明确批准范围，不能将此P0例外自动推广给其他阶段。

## GitHub 平台保护设置（目前尚未启用）

仓库拥有者在 `Settings → Rules → Rulesets` 中给 `main` 配置：

- 必须经 Pull Request 合并，禁止直接推送、强制推送和删除；
- 要求至少一名可用且符合权限的审核者批准（单人仓库的自审限制需结合协作者配置）；
- 将 GitHub Actions 的 `validate` 检查设置为 required status check；
- 禁止自动合并，限制可绕过人员。

**当前只有仓库规则和 CI 软门禁；在 GitHub 规则集真正生效前，不能声称 main 已被平台硬保护。** 用户的合并批准仍不可省略。

## 历史分支处理

2026-10-27 核查：已有 `research/stroke-order-joint-feedback`，与 main 存在明显分叉，内有实验资料。本文档建立新 P0 分支，不覆盖/删除旧分支，不基于旧结果直接认定 v2 研究结论。需要移植时先比较实验协议、数据泄漏、状态与源 commit，再请用户决定。
