# UMM选项位置对照

在Janus-Pro-1B完成[umm_pilot_v1](../umm_pilot_v1/README.md)后，发现33题中29次回答以A开头，因此增加一次完整配对对照。

保持全部33题的图片、问题文字、选项含义和推理设置不变，仅把原来的D移到A、A移到B、B移到C、C移到D，并同步正确标签。该条件在查看首轮结果后制定，属于探索性对照；33对共享相同案例，不是66个独立样本。没有多轮提示搜索或择优报告。

```bash
python scripts/h1_umm_dataset.py --position-control
python scripts/h1_run_janus.py --inputs data/h1/umm_position_control_v1/inputs.jsonl --output results/h1/janus_pro_1b/position_new_run
python scripts/h1_score.py results/h1/janus_pro_1b/position_new_run/predictions.jsonl --dataset data/h1/umm_position_control_v1
```

原定严格单字母评分保持不变。另作明确标识的后分析：若回答为单字母，或字母后紧跟对应选项的完整原文，则按其明确选择评价；文字不匹配、多选或其他回答均不修补。评分文件中分别记录`answer`和`choice_content`，避免把附带正确选项原文的回答一律解释为内容错误。

完整结果及限制见[UMM H1报告](../../../docs/experiments/h1_umm_diagnostic.md)。
