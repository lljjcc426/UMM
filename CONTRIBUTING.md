# 仓库维护与证据规范

更新：2026-11-02。当前入口：[README](README.md)、[工作区交接](docs/project/WORKSPACE_HANDOFF.md)。执行权限以用户本轮指令及[AGENTS.md](AGENTS.md)为准，分支规则见[BRANCH_WORKFLOW](docs/project/BRANCH_WORKFLOW.md)。

## 目录职责

| 位置 | 职责 |
|---|---|
| `docs/research/next/`、`configs/research/next/` | 当前诊断报告与候选方案/配置 |
| `data/research/next/` | 科研重启准备材料，冻结清单不追溯改成新实验 |
| `data/research/runs/<run_id>/` | 实际授权、执行日志、配置、失败与结果索引 |
| `data/research/reviews/<review_id>/` | 追加复核；不覆盖原预测、原答或人审 |
| `docs/research/v2/`、`docs/project/stages/`、`data/research/experiments_v2.json` | P0/P1原协议、阶段科学状态与正式证据 |
| `hanzi_video/`、`scripts/engineering/` | 工程原型与独立本地试验 |
| `data/literature.json`、`docs/reading/`、`docs/reviews/` | 文献权威源与索引；重渲染前确认不会覆盖手工内容 |
| `private/`、`checkpoints/` | 原片、字体、论文、权重及本地独立环境；Git忽略 |
| `archive/`、`docs/project/history/` | 历史材料，采用日期和原版本解释 |

新实验先用[实验计划模板](templates/experiment_plan.md)明确范围，运行元信息沿用[记录模板v2](templates/research_run_v2.json)并写明适用协议。新任务的分支名按获准范围确定，不自动从过期本地main建立工作分支。

## 证据与版本

文献成绩、静态代码审查、CPU测试、真实模型执行和科学结论分别记录。`completed`须有真实运行证据；准备完成不等同模型运行或能力通过。planned/blocked/unknown不填造性能。

冻结模型、权重、代码、字集、提示、seed、输入权限、数据分组及生成参数；记录实际RGB、完整原答、全部尝试、失败、时间/内存和成本边界。几何权限G0/G1分开，模型自报计划不替代实际RGB事件。

改变数据、指标、阈值、采样或协议时另建版本，保留旧预测与失败。暴露数据只作开发/回归，不能重新当新保留集；独立真人结论不得代填或升级成其未覆盖的金标。

不批量移动已被引用的数据目录，不删除旧分支/证据，不用`reset --hard`或强推整理仓库。改入口时先保留必要的原文快照并说明变动。私有证据留在忽略目录，公开登记只提供定位、资格和必要版本信息。

## 必要检查

按改动选择已有检查，避免为纯文档修改重复模型运行、权重哈希或新增实现镜像测试。

```bash
.venv/bin/python scripts/validate_catalog.py
.venv/bin/python scripts/validate_research_plan.py
.venv/bin/python scripts/validate_research_v2.py
.venv/bin/python scripts/validate_stage_release.py
# 代码变更时按影响范围选择测试；需要完整回归时：
.venv/bin/python -m unittest discover -s tests -v
```

工程检查通过不授予科学验收、GPU/训练、远端推送或main合并权限。本仓库Git操作使用`lljjcc426 <3115250840@qq.com>`。整理前本页原文见[导航快照](archive/workspace_navigation_2026-11-02/CONTRIBUTING.md.txt)。
