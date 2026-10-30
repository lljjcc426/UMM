# 全量执行证据布局

本索引描述存储布局，不表示队列已完成。实际计数以最终 `execution_summary.json`、`request_status.json` 和备份核验记录为准。

| 内容 | 私有位置 |
| --- | --- |
| 新运行云端根目录 | `/root/umm-p1-full-20261030` |
| 复用16项云端目录 | `/root/umm-p1-issue3-native-20261030` |
| 新运行本地根目录 | `/Users/cc/Documents/UMM/private/p1_full_server_2026-10-30` |
| 复用16项本地目录 | `/Users/cc/Documents/UMM/private/p1_native_pilot_issue3_2026-10-30` |
| 新生成与理解输入、输出、原始日志 | 云端 `bundles/<ID>/runs/<attempt>/`；本地 `requests/<ID>/runs/<attempt>/` |
| 原始MP4、编码前RGB、解码RGB、PTS、真实输入 | 上述 attempt 的 `t2v/`、`i2v/` 子目录 |
| 理解实际读帧、变换张量、上下文、回答 | 上述 attempt 的 `x2t_video/` 子目录 |
| codec原始读取、潜变量、重建、映射、日志 | 云端 `codec/<ID>/`；本地 `requests/<ID>/` |
| 每个已调用槽位的完整压缩归档 | 两个运行根目录各自的 `archives/<ID>.tar.gz` |
| CPU对照和构造记录 | 云端 `controls/O-*/`；本地 `diagnostics/controls/O-*/` |
| 最终环境、队列状态、控制器日志、代码快照 | 云端根目录；本地 `metadata_final/` |
| 两份离线盲审包 | 新运行本地目录 `offline_review/reviewer_1.zip`、`reviewer_2.zip`；云端 `offline_review/` 同名备份 |
| 隔离映射表 | 本地 `review_blind_mapping_private.json`；云端 `offline_review/review_blind_mapping_private.json`；不放进盲审包 |

每份盲审包解压后直接打开 `reviewer_*/index.html`。两位审核者分别领取各自的包，独立填写。视频原片与全部解码帧保留；可播放、逐帧、查看PTS、保存浏览器进度、导入导出JSON及保留修改历史。审核结束须导出JSON，浏览器本地进度不能替代归档。正式包不包含条件、seed、方法、提示、自动判断及源ID映射。

七项分别判断笔顺、方向、完整性、旧墨迹、时间可判性、最终字形和任务合规。字形相似或笔画相接不能独立证明时序或方向正确；缺乏可见过程证据时对应项选 `unknown`，不补推过程。可指明错误时填写理由和可定位的首错区间。无原片的槽位保留为工程缺失，不能代填真人结论。

大文件、映射表、原始帧、权重和服务器凭据不公开推入Git。Git中保存清单、采样索引、原始回答文字、辅助分析、校验清单与报告。P0及先导原证据保留；本轮没有删除文件。
