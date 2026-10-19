# 长程交错生成、视觉记忆与多模态生成路径

核查日期2026-10-20，存量L154–L160，无新增独立研究/资源。全部数字为作者报告，无模型执行。每篇的原始来源、七字段、假设、反证实验和未读范围见[逐篇索引](../reviews/README.md)。

## 任务和证据应相互对应

ChatUMM训练混合任务对话、插干扰及重写远程依赖，但主量化为单轮理解/GenEval/GEdit，多轮主要案例。BAGEL到ChatUMM的GenEval.88→.85、GEdit整体EN6.52→6.95，保留取舍；CVPR2026 GRAIL-V为Workshop，不按主会归类。

UniLongGen在50固定文字故事、每例40图槽上测图像稳定性。它没有在主实验中自由规划文字，不能推完整故事生成能力。正文/AppB评GPT5.2，Table1caption却写GPT4o/HPSv2，列头HPSv3；实际裁判需代码进一步核。

最新L156的LongMIG100故事平均9.2图，另有38故事×24图Long+Ext，50+图为展示，几个范围分别记录。语义全历史继续可见，生成仅检索anchor、近期和同scene状态；32图时间102.9→54.9s/图，但合成context仍增长，51图满窗为外推。不得称常数总上下文。

## 机制论证的强度

UniLongGen以浅层文字、深层VAE的内部相关度选历史块，dense HPS3.1677→7.5701/DINO.3164→.4272；TextL1 PickScore.2031仍略胜双probe.2025。人工相关度topK为5.1158，它只是在该相关性定义下的人工选择，不能视为真正生成效用oracle。

不同分辨率/图事件数与文字token匹配，是有用控制；注意力熵增长仍要排除key数效应，相关重尾不能代替离群patch的因果干预。约11倍速度明确关CFG、累计flow时间，完整dense probe/prefill/缓存成本还要核。

L156提供scene错标、去anchor、GTFT对selfrollout消融；selfrollout保持下一图GT目标，替换部分过去历史，不是RL。场景预测错误会退化；anchor也占生成成本。同底座比较仍应拆固定权重策略与新增训练贡献。

## 名称相近，像素生成路径不同

| 研究 | 中间表示与最终解码 | 相关局限 |
| --- | --- | --- |
| MIO | Yi因果预测32个SEED图码，经MLP再条件扩散 | 细节码率有限，视频主要展示；TTS WER12→4.2同时ASR6.3→10.3 |
| OmniFlow | 各模态潜空间独立噪声时间与联合attention；文字最后TinyLlama解码 | latent流不代表全部输出无AR；同义重建不保证exactstring |
| M2-omni | 先输出caption，再独立SD3medium | 文字瓶颈不保留全部像素/动作状态，不能把SD质量当共享生成协同 |
| Ming-Lite-Omni | 冻结感知Ling，训练多尺度query/connector/DiT | 生成梯度无法更新冻结LLM，双向学习收益未由该训练证明 |

OmniFlow的约30M为额外微调图，继承SD3历史预训练；GenEval.62未超过SD3medium.62。补充I2A FAD全任务1.83、I2Aonly2.05提示共享任务收益，但需匹配数据/计算才判因果。两两模态边缘一般不能唯一识别三模态联合，合成caption监督也应单列。

M2omni按验证loss历史斜率分配权重并EMA，解决收敛失衡有经验支持；loss归一不保证梯度冲突消失。Table12最优MSVD76.5仍来自独立video模型，平衡模型74.8，不能照抄所有模态都超过独立训练。

## 制品版本与下一步

当前[Ming](https://github.com/inclusionAI/Ming)默认README已是FlashOmni2.0。核[2025-06-12提交](https://github.com/inclusionAI/Ming/tree/75fb7ec73bbc8d4c5391251e2ec90e99971d7cd9)的原版README与config：Lite激活2.8B；示例CFG6/20步、480×544，不能直接视为论文主表条件。config残留SANM并有Whisper配置，未追执行分支前不凭字段存在认定模块启用。Flash2.0的100B/6B不得写进早期Lite记录。

严格书写实验应比较规则状态/轨迹渲染、正确历史oracle、窗口/筛块/scene记忆、专用视频和共享UMM；相同数据和可见历史，所有辅助参考图/规划/探测成本计入，字符终态、笔画事件、连续RGB和执行成功分别验证。现有长程图序列成果不能直接改写为规范笔顺视频能力。
