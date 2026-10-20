# 发现层候选

- `arxiv_candidates.json`：此前检索取得的573条arXiv元数据，含题名、作者、摘要、时间、版本、来源和发现路径。
- `survey_repository_candidates.json`：从综述仓库整理的200条候选题名与链接。

两份文件有重叠，也与主目录有交集。它们不是新增773篇精读文献；未核读候选不作为结果或新颖性结论的依据。相关且经过调查整理的研究进入上一级 `literature.json`，并登记核查层级。


- [扩散效率综述仓库候选](diffusion_efficiency_repository_candidates.json)：2026-10-21固定官方README的208次单行Paper条目，按arXiv ID或URL合并201项；与前两份及主目录有交集。只属发现层，尚未全部判定相关性、核读原文或纳入主目录。部分源链接拼写错误保留原值并注明规范化，源仓库年份标签也未作为已核事实。
