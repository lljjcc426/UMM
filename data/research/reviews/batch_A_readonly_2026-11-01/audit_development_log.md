# 本轮CPU复核脚本调试记录

首次运行在读取第001项时因相对 evidence 路径与绝对 repo 路径调用 relative_to 不兼容而退出（ValueError）。尚未写出审计JSON或改变历史文件，已创建的空 visuals 目录保留。入口统一 resolve evidence 路径后，使用新 visuals_verified 目录重新执行。属于本地审计程序调试，无模型请求、训练或历史产物覆盖。
