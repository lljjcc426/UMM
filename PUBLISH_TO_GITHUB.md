# 仓库同步说明

本仓库是持续研究记录库，目标为 https://github.com/lljjcc426/UMM ，分支为 main。

## 2026-10-15 的导入

网页版集成曾返回403；这属于当时连接权限。当前本地GitHub CLI登录被API确认为仓库管理员，已读取并保留远端原README提交，在其上整合资料。实际同步结果与提交见 [delivery_status.json](reports/delivery_status.json)。

本次主体资料已成功提交并推送到 `main`，内容提交为 [`084cb50`](https://github.com/lljjcc426/UMM/commit/084cb50eab2f0ea53d0477e9e848929e22e91d8b)。共142个版本管理文件；后续状态记录另行提交，内容提交保持可追溯。

后续更新采用普通 `git add`、`git commit`、`git push origin main`，先审阅提交内容；不使用强制推送，不覆盖原始本地研究材料。用户已明确授权本次整合进入该仓库。

本地 `research/`、`.integration/` 和私有材料被Git忽略。主目录仅发布有公开来源的研究记录、原创分析、必要的公开样例核查图、数据索引与研究工具。原始PDF、模型权重、字体和受限数据不分发。

旧版发布说明保留在 `archive/imports/web_2026-10-15_PUBLISH_TO_GITHUB.md`；其中403和“未提交”是历史记录，不代表当前状态。
