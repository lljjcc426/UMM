# 规范汉字书写视频：首版工程契约与实施记录

日期：2026-10-31。分支：`codex/engineering-hanzi-video`；基点：`ed92bd8a`。用户确认“允许UMM识别和规划，再由受控执行模块生成视频”及“按这个首版范围推进”。本轮不涉及GPU、训练、远端推送或main合并。

## 产品边界

大陆规范简体、单字文本或单张清晰字图输入，标准楷体式黑字白底，512×512、24fps、MP4。视频从空白开始，单笔沿有向路径逐步形成，笔间停顿，已写墨迹保留，末尾停留。速度支持慢速、标准、快速，不支持艺术字、多字、任意风格或视频输入。

当前字库为士、丑、小、以、广、刃、乞、点，共32笔。首版8字用于检验完整工程接口；不承诺8105字或任意输入都已具备规范资格。8字已对照GF0023-2020的逐笔图与**实际Arphic矢量及中线**重新做AI视觉绑定；原CASIA的数组下标、方向或既有整体人审结论均未直接迁移。资格为`AI_reviewed_engineering_preview`，`human_per_stroke_gold=false`。缺少可靠绑定的字被拒绝，不能让模型临时猜一套路径直接交付。字库扩充需要逐字参考与绑定资格，不能把9574个源记录直接变成规范真值。

## 执行链路与权限

1. 文本输入直接固定目标；图片输入由UMM识别候选，用户确认目标字后进入规划。模糊、多字或不确定返回unknown，不自动猜字。图片识别结果保留独立记录，不能被生成请求暗换。
2. UMM接受目标、只读规范笔画指南和可选目标图，输出结构化`character/strokes[id,direction]`。图像理解使用源码已有的`x2t_image`入口；文本规划使用空白视觉输入加真实文字请求。禁止ENV-01“十”字fixture、答案占位或历史示例覆盖真实请求。
3. 校验器从独立配置读取显式规范顺序与有向几何绑定，检查目标、笔画数量、身份、顺序和方向。错误计划可反馈一次，原回答和两轮校验均保留；仍错误则失败。模型不能修改规范、路径或校验器。模型思维过程不作为验收证据，不要求输出隐藏思维链。
4. 执行器仅按通过的计划与固定几何逐笔揭示黑色墨迹。几何存储按独立ID排序；规范顺序另存`sequence`。通过重排存储的测试，避免数组位置隐含规范真值。
5. 对实际编码MP4重新解码，读取PTS，检查尺寸/帧率、空白首帧、13个中线地标的实际出现时刻、笔画前后关系、历史墨迹与最终完整性。审核器不接收执行事件日志。未通过的文件保留在私有目录，但不发布到页面下载接口。

这套回读检查针对**固定参考的受控执行器**，与P0通用自动观察器不同；仍共享参考几何，不能独立证明参考本身符合规范，也不能推广为自然书写通用识别准确率。复杂折钩使用沿中线的多个地标，覆盖范围有限，正式发布前需补充参考资格及更广泛的折钩/交叉案例。

## 当前可运行内容

```bash
.venv/bin/python -m hanzi_video.server --port 8780
```

浏览器打开 `http://127.0.0.1:8780/`。CPU执行预览不调用模型；UMM未连接时页面明确标注、相关按钮停用，直接请求UMM接口也拒绝。文本、速度、实际MP4播放与下载可本地体验。图片选择可预览；图片识别和UMM规划须待真实后端连接。

依赖在`requirements.txt`，新增`imageio-ffmpeg`提供FFmpeg，不要求系统另装编码器。完整本地验证见`data/engineering/hanzi_video_v1/`，原片、操作截图与故障注入视频在`private/engineering_hanzi_video/`，无原片公开上传。

## 接口

| 接口 | 输入与实际行为 |
| --- | --- |
| `GET /api/catalog` | 支持字集、笔画说明、参考资格和后端配置状态；配置状态不冒充实际联调通过 |
| `POST /api/recognize` | 单张图片data URL；创建UMM识别任务；返回任务ID；unknown独立失败，不生成视频 |
| `POST /api/generate` | `character, mode=umm/preview, speed=.75/1/1.5`；图片另传已确认的`recognition_id` |
| `GET /api/jobs/{id}` | queued/running/completed/failed、实际耗时、参考版本、回读结果与视频路径 |
| `GET /outputs/{id}/video.mp4` | 只提供已通过检查任务的视频；PNG为最终字形海报 |

规划器适配协议：操作员通过`UMM_PLANNER_COMMAND`提供JSON格式argv列表；服务追加`--request <JSON文件> --response <JSON文件>`，不使用shell拼接。请求包含本次prompt、operation、character和image；响应必须包含原始`answer`。原始日志与输入均保留。生产页面没有模拟模型的接口；测试桩只存在于单元测试。

真实适配脚本为`scripts/engineering/lance_planner.py`，参数`--upstream --model --vit --request --response`。使用原Lance_3B_Video和已有Qwen2.5-VL视觉塔，沿用固定revision；不下载、不训练、不调用收费API。`x2t_image`在该视频checkpoint上的识字能力仍需实测，不从源码存在推断质量。脚本在原生方法入口记录实际conditioning token与VIT规模，核对本次prompt存在且占位标签未泄漏，保留原始回答、argv、峰值显存与时间。最大输出512token，只改运行时输出长度，不改权重。

在获准的GPU环境中可以将命令配置为：

```text
["/absolute/venv/bin/python", "/absolute/UMM/scripts/engineering/lance_planner.py",
 "--upstream", "/absolute/Lance", "--model", "/absolute/Lance_3B_Video",
 "--vit", "/absolute/Qwen2.5-VL-ViT"]
```

本地页面可通过SSH转发访问服务器上的同一回环地址。当前没有建立SSH连接或租用实例。实现为每次命令调用加载一次模型，便于首轮追溯；尚未做常驻推理服务与延迟优化。

## 参考来源与许可

Make Me a Hanzi `graphics.txt` 固定revision `bddc96d41bef78427ed0e034e9f7e31d71fd1b92`。从已在本机的源提取8字轮廓与中线，没有新下载。子集命名Yibi Kai Preview，附修改通知、源COPYING和完整未改动的Arphic公共许可证；几何派生物继续按其条款提供。GF0023-2020仅作为规范对照，官方PDF和裁图不打包分发。重建命令：

```bash
.venv/bin/python -m scripts.engineering.build_catalog --graphics /path/to/graphics.txt
```

本次AI视觉对照图保存在`private/engineering_hanzi_video/reference_binding_comparison.png`。该记录表示实际开发核对，不表示真人批准。

## 验证与未完成事项

实际结果以`data/engineering/hanzi_video_v1/validation.json`、`tests_final.log`、`browser.json`和`regression.log`为准。测试覆盖8字真实MP4、计划目标/顺序/方向/数量、源存储重排、错误计划反馈及两次失败停止、离线UMM拒绝、图片识别与生成分离、当前输入材料化，以及倒序/反向/缺笔/闪现/墨迹消失的像素故障注入。测试桩不计为真实UMM实测。

本轮实际验证：8/8预览通过，共952解码帧；5/5注入错误被拒绝，CPU验证脚本用时约3.70秒。完整回归139项通过，入口校验整理后的定向11项复测通过；文献目录、研究v1/v2和当前阶段清单四项检查均通过。浏览器覆盖播放、MP4下载、图片预览、缺参考拒绝、离线UMM拒绝和移动布局。

视觉复核额外发现HTTP接口未支持Range时，浏览器即使整片已缓冲，拖动进度条仍回到首帧。已补充206/Content-Range分段读取，浏览器测试增加实际seek后的时间与画面墨迹断言，防止“播放器加载成功”掩盖播放问题。另一处首轮图片预览断言过早的问题已通过等待FileReader异步完成修正。初始测试解码辅助函数的资源警告也已消除。原故障与修复说明保存在`development_issues.json`，不计为模型实验。

剩余工程工作：

- 获准GPU上验证文本规划和图片识字的真实输入、输出、结构化遵循率、错答拒绝和资源占用；当前模型链路未验收。已有A10080可胜任此前原生路径，工程图像理解的显存和延迟待实测，不预填数值。
- 将8字参考提升到面向正式发布所需的逐笔核准，并扩大经过核准的字库；当前不新增人工任务。
- 真正连续使用前补充常驻UMM、队列取消/重启恢复和部署管理。本地原型重启后保留旧任务文件，但不自动重跑中断任务。

工程改造没有修改P0/P1阈值、原预测、人审、失败或阶段发布状态，没有将受控视频计为UMM原生视频成功。当前工程结果不能被写成全字库已保证正确或UMM自纠错已实证有效。

## 文件变更说明

没有删除既有项目文件、研究产物或失败记录。文件按用途说明如下：

| 文件 | 本次变化及用途 |
| --- | --- |
| `hanzi_video/__init__.py`、`catalog.py` | 新工程包；显式规范顺序与几何绑定，验证目标、数量、顺序和方向 |
| `hanzi_video/planner.py` | UMM结构化调用、原回答保存、一次纠错及失败停止；无模拟后备 |
| `hanzi_video/render.py`、`audit.py` | CPU逐笔执行；实际MP4 RGB、地标和PTS回读检查 |
| `hanzi_video/service.py`、`server.py` | 本地任务、图片输入、状态与失败归档、仅已检查视频下载、HTTP Range |
| `hanzi_video/static/index.html`、`app.js`、`style.css` | 文本/图像输入、模型状态区分、播放、速度和下载页面 |
| `hanzi_video/assets/catalog.json`、`NOTICE.md`、`licenses/COPYING`、`licenses/ARPHICPL.TXT` | 8字源几何、显式新绑定、修改通知、原许可证与归因 |
| `scripts/engineering/build_catalog.py`、`lance_planner.py` | 从本机源可复建字库；真实原生UMM适配器，尚未GPU调用 |
| `scripts/engineering/validate_preview.py`、`test_browser.cjs`、`tests/test_hanzi_video.py` | 实际预览与故障证据、浏览器操作检查、11项工程回归 |
| `data/engineering/hanzi_video_v1/`下9份JSON/日志 | 范围/实际状态、8字与故障结果、浏览器结果、完整/定向测试、研究门禁回归、已知问题 |
| `docs/engineering/hanzi_video_v1.md` | 本契约、报告、接口、资格和文件变更记录 |
| `AGENTS.md`、`README.md`、`docs/project/STATUS.md`、`docs/project/BRANCH_WORKFLOW.md` | 更新当前工程入口与工作流，原研究制度和结果作为历史保留 |
| `requirements.txt`、`.github/workflows/validate-research.yml` | 增加FFmpeg运行依赖及工程目录/分支CI触发，原研究门禁不变 |

私有目录另保存8字原片、5类故障片、1段故障构建源片、最初开发预览、浏览器操作产物和规范对照图；均不加入公开Git提交。测试临时目录由测试框架正常回收，不涉及清理历史产物。
