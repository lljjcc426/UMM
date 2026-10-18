# T2官方视频路径核查

依据本地固定源码show-o2/inference_mmu_vid.py、utils.load_video、configs/showo2_1.5b_demo_video_understanding.yaml和models/omni_attention.py，保持源码归档不改动。

1. 调用load_video(..., fps=1, force_sample=True)时，最终帧索引总被linspace(0,N-1,max_frames_num,dtype=int)覆盖。示例32帧，在短片中并非每秒一帧；短片少于32帧会重复索引。输入必须是已观察前缀，不能把整条未来视频先采样再截出早期决策。
2. 视频帧经432等比例resize/pad、[-1,1]归一化，video.unsqueeze(2)使各帧成为batch中独立长度1的VAE输入。这里没有利用连续长片的VAE时间压缩。
3. 每帧语义／生成融合为27×27×1536，经bilinear压为14×14，再按frame-major排列，8帧为1568个视觉token，示例32帧为6272。
4. 只有一个boi/eoi和time_embed(t=1)。该t是扩散时间条件，不能解释为视频时间戳。load_video返回的frame_time没有加入问题；顺序主要由输入排列和语言位置表示传入。
5. num_mmu_image_tokens配置为729，add_time后为730，attention模态矩形从text_a+2（首个视觉token）开始，仅覆盖730个视觉位置。8帧其余838个视觉位置保持因果mask；32帧同样沿用730。实际执行官方mask函数的结果见T2_attention_audit.json。它是输入结构差异，尚无证据说明这是本任务错误的主要原因。本批先保留原行为，不能静默改为全视频bidirectional后声称复现。
6. 本机没有decord，采用PyAV实现原load_video实际调用的VideoReader/get_avg_fps/get_batch接口，并执行原函数AST，原索引公式不变。无损RGB视频逐帧对比原PNG以确认解码。设备改为CPU fp32 VAE／MPS bf16理解路径；直接视频调用按帧串行以限制内存，固定一次seed。此为算法路径复现，不声称与CUDA批处理逐bit相同。

数据构造预检查发现Pillow偶数线宽会令反向画线的栅格横移一行，造成虚假的完成缺口。正式数据统一奇数线宽13，正反完整路径像素相同；该问题在数据落盘及训练前修正。没有用提高完成阈值掩盖渲染错误。
