# P1最小可执行实验清单（P0已最终验收，云端输入已准备）

本轮已完成CPU计划、64请求及private原生输入包准备。当前模型调用0、视频生成0、训练0、新人工任务0。完整方案见[报告](../../../../docs/research/v2/p1_baseline_failure_plan_2026-10-30.md)。

1. P0有限结项已获用户最终科学验收，审批见`data/research/runs/p0_final_acceptance_2026-10-30/final_scientific_approval.json`。用户已提供1×A10080云主机，当前连接与部署准备；无需再租无卡CPU主机。P1推理授权与模型运行结果分别记录。
2. 沿分支流程完成P0审核/获准合并，再从最新获准main建立`research/p1-native-baselines`。不得以当前计划擅自推理或改main。
3. 部署固定Lance代码/权重和已核依赖，复用既有环境记录。materialize原生输入包：更新upstream软链接及输入JSON的绝对路径；当前云主机保留ENV-01固定运行环境及权重，可直接复用；P1实际解码索引尚未产生。取得授权后将计划approval.user_approved改为true并附批准记录，原prepared版本保留。
4. 在运行环境审计实际视频解码、native抽帧索引及最多8例codec重建。保存原片/PTS/原生采样/重建并核查短事件；证据不足先报告，不将重建成功预填为SO-00通过。
5. 选择requests.json中pilot=true的16个唯一ID。按请求调用原生运行器，串行单输入、33帧/480×848/12fps/30步/CFG4，seed11或29。每次launch均保存原片、stdout、错误、真实峰值显存和含加载耗时；不能挑最好seed。
6. 使用同4字准备4个确定性规范渲染O对照，几何绑定仍标AI开发级，实际形成过程另核，不宣称完整金标。固定33帧、同画布/编码参数；保留高时间分辨率源与均匀抽样索引供SO-00比较。
7. 完成归档及环境/成本记录后释放GPU，再在本地对16生成＋4对照开展两位独立真人视频分项判断。40次视频审核为后续预算，本轮未分派。先保存独立原文，再处理分歧，unknown不计成功。
8. 根据真实运行成本与可判性，用户决定是否扩展剩余48次生成、额外4个O对照及28次SO-01理解请求。实际RGB未产生前，不构造假的EVAL-02或理解输入。不自动SFT、LoRA或联合训练。

已验证的CPU准备命令（输出目录必须新建以保留历史）：

```sh
python -m scripts.p1.prepare_baseline \
  --output data/research/plans/p1_baseline_NEW_VERSION/prepared \
  --private-output private/p1_baseline_NEW_VERSION \
  --upstream /absolute/path/to/fixed/Lance/upstream
```

请求包dry-run命令只打印原生参数，不导入模型：

```sh
python -m scripts.env01.run_interfaces --bundle PREPARED_BUNDLE --dry-run
```

GPU执行授权、云端路径/权重准备及计划批准记录完成后的命令：

```sh
python -m scripts.env01.run_interfaces --bundle PREPARED_BUNDLE
```

当前prepared包approval.user_approved=false，执行命令应在导入GPU库前拒绝。本轮已验证该拒绝行为；不能把CPU dry-run认作GPU环境或视频解码验证。
