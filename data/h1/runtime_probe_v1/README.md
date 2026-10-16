# H1 运行诊断补充

查看`pilot_v1`与`focused_v1`失败后，增加6个不要求JSON的短问答，检查基础文字和图像输入能否起作用。它们属于运行排查，未计入H1准确率，也不构成新的能力基准。

输入保存在`inputs.jsonl`，图片复用`pilot_v1`。人工核对标准：17＋25为42；半条上横应继续完成上横；空白、单横、三横分别为0、1、3条；“十”按两条完整相交直线计为2。最后一项的“四个分支”与“两条完整直线”需要区分，不能单凭该回答推断实现故障。

运行命令：

```bash
python scripts/h1_run_mlx.py --inputs data/h1/runtime_probe_v1/inputs.jsonl --output results/h1/qwen3_vl_2b_4bit/runtime_probe_new_run --max-tokens 128
```

`response_format=text`保存未经JSON解释的原文；逐条结果和判断见[H1报告](../../../docs/experiments/h1_diagnostic.md)。
