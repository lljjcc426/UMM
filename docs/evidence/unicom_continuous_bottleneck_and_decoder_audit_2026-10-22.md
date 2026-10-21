# UniCom：连续瓶颈、完整主表与解码依赖

第一百一十九批完成[L104](../reviews/L104.md)固定v1核心三遍与五项书面记录。[结构化证据](../../data/unicom_continuous_bottleneck_and_decoder_audit_2026-10-22.json)。357目录（330论文／研究、27资源），228核心/231书面含未通过项，129条未确认核心（含资源）。没有新增目录、删除文件、下载权重或运行模型。

## 来源和阅读范围

固定[2603.10702v1](https://arxiv.org/abs/2603.10702v1)，2026-03-11，完整22页；Abstract/§1–5、Eq1–5、T1–7全部行、AppA–G研究文字和全部图注已读。实际核PDF p4框架F2、p5Eq2–5/T1、p6T2、p8F4/5、p9T3/4与F6/7、p10T5/F8、p19T7。未逐图全部定性页，未逐篇参考文献；正式发表会场未核。

任务为静态理解、重建、文生图和图像编辑；视频列为未来工作。没有书写动作、文字视频或真实笔顺实验。

## 数据流与理论边界

冻结SigLIP2-SO400M16NaFlex→最多1024位置×1152维→MHA压缩到每位置64维→解压/FLUX扩散decoder→FLUX VAEdecode→RGB。先联合训压缩/decoder，再冻结二者训Qwen2.5-7B，以CE生成文字、flow预测语义latent，图像内部双向/文字causal。理解正文读原特征，编辑读压缩源图；不能把各路径统称仅64维统一输入。

Eq1是模型选择的条件分解；若视作真实分布恒等式，需要z提供足够条件信息，论文未给一般性充分性证明。低维流形、易建模及语义保留为机制动机与指定设置下的经验。d从1152到64为18倍通道压缩，N保持1024；不能推成LLM上下文或完整FLOPs降低18倍。浮点维数也不等同熵编码后的实际比特率。

公开AttentionCompressionNet是attention投影、线性残差与GeGLU；压缩时18个64维head输出取均值，扩展时拼接。没有VQ码本。Eq3–5为t0噪声→t1数据的线性flow、目标z−noise和MSE。

论文的语义生成目标与参考图条件避开VAE latent；固定公开runtime仍加载FluxAutoencoderKL并调用vae.decode，模型卡也明确decoder-side VAE必需。完整推理的VAE依赖应保留。

## 七张表与实际图表核查

| 证据 | 结果、反例和条件 |
| --- | --- |
| T1重建 | d64 .42/22.28/.61对d1152 .38/22.60/.61，有失真；FLUXVAE .06/33.65/.93更强。原生256/384/512/1024不同，不能直接归因tokenizer结构 |
| T2生成 | GenEval .87低于Mogao .89/BAGEL .88；DPG85.92低于XOmni87.65/Showo2 86.14。WISE .58为所列最高，Culture .55低于MetaQuery .56、Time .56低于FLUX .58、Space .73与UniWorld同。†改写条件不同 |
| T3编辑 | ImgEdit4.22低于TUNA4.31/QwenImage4.27；GEdit语义8.06较高，感知7.33低于TUNA7.48/Qwen7.86，overall7.32低于Qwen7.56。KRIS70.11/World4.12在列出的开放组较强，非全方法/全维度最优 |
| T4形状 | 原1024×1152 rFID .40/PSNR23.26/SSIM .69；256×1152 .72/20.29/.56；MLP1024×256 .62/21.73/.66、MLP64 .55/22.17/.66、MHA64 .56/22.61/.69。支持此配方的空间保留，但总Nd/参数/FLOPs未等，MHA的rFID还略弱MLP |
| T5理解 | MHA相对MLP六项均高；相对原特征六项均降，OCR55.40→36.00，下降19.40点。Seqconcat原特征后OCR55.50，GQA/SEED/MMMU仍低于baseline；增加原特征/上下文成本。原始旁路不能证明纯压缩无损 |
| T6协议 | 四阶段20K/115K/60K/7K步，lr2e-5/1e-4/1e-4/1e-5；数据采样text .20/.25/.20/.10、T2I0/.45/.40/.20、I2T .80/.15/.20/.40、I2I0/.15/.20/.30。数据名单/独立规模与主batch仍缺 |
| T7 WorldEdit | 全11原因类/四维及Avg已核；总分4.12与T3一致，低于Seedream4.45/GPT4o4.36/NanoBanana4.22。Time4.08低于WorldEdit4.10、Light4.02低于4.09、Squeeze3.63低于3.73、Twist4.13低于4.16等。AppE文字4.35与两表4.12冲突，保留待澄清 |

F6正文约5倍，图注和箭头3.8倍，横轴为训练迭代；没有完整端到端walltime比较。F7 MLLM初始化1.5倍和Transfusion3.4倍同属作者曲线。PathII正文冻结MLLM，PathI可训练，F2却给MLLM火焰图标；训练状态/预算需澄清，不能把差距全归query长度。F8六类各150图的tSNE不证明全分布语义/因果，F9通道压缩初期还更慢。F5文字重建图与其他原生分辨率不同，精选样例不替代OCR统计。AppF CoT仅展示例图，无受控开关的定量效应。

## 训练与公开制品

Decoder内部图像、33比例桶1:4–4:1、base1024²/global256/50K步。主四阶段AdamW β.9/.95 eps1e-6、clip1、wd0/.01/.01/.01、warm600/5000/5000/100，后3阶段FM:CE5:1。理解消融LLaVA557K+Cambrian737K不能填作主系统全部数据。完整主语料、硬件/卡时、主batch、perceptual λ、训练多seed/CI未齐。

固定[GH55b9001](https://github.com/Tencent-Hunyuan/UniCom/tree/55b9001a0fee623528676d995d8945fd6db7e23e)94项完整树、README全文、compression.py、三份decoder配置；runtime加载/解码、decoder投影入口、MLLM的原特征与编辑路径为选读。未见完整四阶段训练/私有数据发布，未逐行所有模型或pipeline。

固定[HF78e43059](https://huggingface.co/tencent/Unicom-Unified-Multimodal-Modeling-via-Compressed-Continuous-Semantic-Representations/tree/78e43059d8358a045e64fca35698fda86c476154)卡、清单、config以及modeling/SigLIP2的有关输出/投影代码。明确列主模型四分片、decoder、SigLIP2与VAE；未下载权重。CLI主latent50步/CFG3.5/shift3，decoder100步/CFG1；重建demo50步/CFG1；默认think_recaption与CoT最多1536token、README每prompt4样本，均属公开示例，主表实际使用需核。

新定位的静态对应疑点：HF config的vision hidden1152、aligner input1216，所读GH/HF `_forward_vision_encoder`把last_hidden_state直接交aligner；SigLIP2输出与LightProjector处未见补64维拼接。须核加载时配置修改和真实理解入口运行；未做模型执行，不能宣称实测失败。编辑源图经独立64维patch路径，因此也不能据此否定全部生成/编辑结果。

## 可证伪实验与写作学习

固定teacher/分辨率/FLUX预训与总Nd、bits、参数、FLOPs和曝光，二维扫描N×d，补三任务Pareto与多seed。PathI/II匹配冻结状态、可训练容量、query数与数据预算；理解预训成本计入初始化实验。纯压缩/原始/拼接应在同上下文预算测细字、非汉字OCR、局部编辑未改区；汇报两级NFE、CFG、CoT和多样本选择的完整延迟。理解入口先做实际加载/shape核查。视频过程需另有事件GT。建议均未执行，新颖性未确认。

值得学习的是Introduction分开表示和预测机制，Method先分布分解再模块，消融逐层对应shape/projector/初始化，T6列逐阶段配方。Claim需保留退步项和信息旁路、VAE依赖、3.8倍的迭代口径及原文冲突。作者AppG已承认极细节损失与计算成本；读者进一步补齐私有数据、统计方差、OCR/视频未测边界。
