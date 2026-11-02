"""Build a new offline review ZIP from existing Batch A evidence, CPU only."""
from datetime import datetime, timezone
import hashlib
import html
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import zipfile


REPO = Path.cwd()
AUDIT = REPO/'data/research/reviews/batch_A_readonly_2026-11-01'
OLD = REPO/'data/research/runs/diagnostic_batch_A_2026-11-01'
RAW = REPO/'private/diagnostic_batch_A_2026-11-01/server_artifacts'
DELIVERY = REPO/'private/batch_A_readonly_2026-11-01'
PACKAGE = DELIVERY/'review_package'
VISUALS = DELIVERY/'visuals_verified'
changes=[]


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    with path.open('x') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def sanitize(text):
    text=text.replace(str(REPO),'/REPO').replace('/Users/cc','/LOCAL_USER')
    text=text.replace('/mnt/data/umm-diagnostic-batch-a-20261101','/TASK')
    text=text.replace('/root/','/REMOTE_HOME/').replace('/home/vipuser/','/REMOTE_HOME/')
    text=re.sub(r'/Users/[^/\s"\']+', '/LOCAL_USER', text)
    def redact_IP(match):
        candidate=match[0]
        try:
            ipaddress.IPv4Address(candidate)
        except ipaddress.AddressValueError:
            return candidate
        return '[REDACTED_IP]'
    text=re.sub(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',redact_IP,text)
    text=re.sub(r'https?://[^\s"<>]+',lambda m:m[0].split('?')[0]+'?[REDACTED_QUERY]' if '?' in m[0] else m[0],text)
    text=re.sub(r'(?i)(Bearer\s+)[A-Za-z0-9._-]+',r'\1[REDACTED]',text)
    text=re.sub(r'\bhf_[A-Za-z0-9]{16,}\b','[REDACTED_ACCESS_TOKEN]',text)
    return text


def put(source, target):
    destination=PACKAGE/target
    destination.parent.mkdir(parents=True,exist_ok=True)
    original=source.read_bytes()
    if source.suffix in {'.json','.jsonl','.py','.sh','.md','.txt','.log','.csv','.patch'} or source.name=='LICENSE':
        after=sanitize(original.decode()).encode()
    else:
        after=original
    with destination.open('xb') as f:f.write(after)
    if after!=original:changes.append(str(target))
    return destination


def main():
    PACKAGE.mkdir(exist_ok=False)
    rows=read(AUDIT/'per_request_evidence.json')
    state=read(OLD/'state.json')
    notes=[
        '丑被回答为squint；冻结视频接口中的身份错答。',
        '广被描述为类似小写l的符号，未识别身份。',
        '士被描述为water字的一笔，身份/整体不符。',
        '小被回答为J，身份不符。',
        '丑的计划转为人物和车辆移动，无可执行逐笔计划。',
        '广的计划复述任务并声称6秒，没有具体笔画。',
        '士的横竖描述含混，未完整绑定实例/顺序/方向。',
        '小的计划复述任务，没有具体笔画。',
        '丑结构回答不足，不能因未输出JSON直接判笔顺错误。',
        '广结构回答只泛谈长度粗细，缺少具体绑定。',
        '士结构回答未提供可核验几何关系。',
        '小静态描述属实，但结构任务没有充分回答。',
        '士：横后中央竖的局部时序正确；墨滴叙事/时长不符。',
        '士交换：人形行走叙事未反映真实笔画历史。',
        '小：分解、碎片脱落与实际持续增墨矛盾。',
        '小交换：人头和肢体叙事未可靠对应笔画身份/方向。',
        '实际上横右→左、下横左→右；回答说反，且截断。',
        '实际只有两条横线；回答虚构多条横竖线，且截断。',
        '实际两条线突现后静止；回答虚构上下移动。',
        '实际上横后下横均左→右；回答复述/额外细线，且截断。',
        '弯折曲线逐渐变形；水平形状失败，纯方向unknown。',
        '首帧整高竖线，33帧墨迹不变；增长未实现，方向unknown。',
        '源/解码均右向增长；右端193→687、一次1像素回退；局部正证据。',
        '短曲线，无第二横线与要求的先后过程；顺序/方向unknown。',
    ]
    findings=[]
    for r,note in zip(rows,notes,strict=True):
        findings.append({'id':r['id'],'track':r['track'],'AI_evidence_review':note,
                         'authority':'AI_development_evidence_review','formal_human_judgment':None,
                         'formal_primary_metric':None,'SC_CoIT_attribution':'unattributed',
                         'raw_answer_unchanged':True if r['raw_answer'] is not None else None})
    matrix=[
        {'capability':'engineering_integrity','n':24,'finding':'24 requests, 20 full answers, four native videos and logs present','limitation':'Does not establish model capability; strict=False key coverage unrecorded'},
        {'capability':'character_identity','n':4,'finding':'Four explicit AI-reviewed identity mismatches under x2t_video static carriers','limitation':'No native image/official positive controls; no formal accuracy'},
        {'capability':'normative_planning','n':4,'finding':'No complete executable stroke plan in these raw answers','limitation':'Blank-video text carrier; no full qualified normative gold'},
        {'capability':'static_geometry','n':4,'finding':'No sufficiently grounded complete stroke/endpoint descriptions','limitation':'Narrative parser returns unknown; not a formal stroke-error score'},
        {'capability':'actual_history','n':8,'finding':'One partial-order positive; explicit false direction/motion/count/disintegration statements','limitation':'Five matched-final comparisons; answer differences do not establish correct history use; timing encoding confound; three cutoffs'},
        {'capability':'atomic_generation','n':4,'finding':'023 left-to-right growth exists before and after encoding; other cases have shape/process deficiencies','limitation':'One checkpoint/seed; no full Hanzi pass; unknown stays separate'},
        {'capability':'FIT_01','finding':'Preparation may continue; not admitted to training execution','limitation':'Separate user approval, interface positive controls, qualified targets and frozen recipe/budget/gradient+reload checks required'},
    ]
    save(AUDIT/'per_request_scientific_findings.json',findings)
    save(AUDIT/'capability_matrix.json',matrix)
    index=read(REPO/'private/diagnostic_batch_A_2026-11-01/server_backup/archive_index.json')
    indexed=[x for x in index if x['kind']=='file']
    index_ok=all((RAW/x['path']).is_file() and (RAW/x['path']).stat().st_size==x['bytes'] for x in indexed)
    save(AUDIT/'review_scope_and_checks.json',{
        'review_created_at_utc':datetime.now(timezone.utc).isoformat(),
        'reviewed_commit':'a1c2d5fbe3f00d80cf1ad00d8819ea322e05cdad',
        'branch':'exp/p1-process-diagnostic','new_model_calls':0,'training_runs':0,
        'network_or_SSH_calls':0,'historical_tracked_file_changes':False,
        'request_count':24,'raw_answer_count':20,'native_output_videos':4,
        'archive_index_files':len(indexed),'all_index_files_present_and_size_matches':index_ok,
        'formal_scientific_status_unchanged':True,'formal_primary_metrics':None,
        'FIT_01':{'decision':'prepare_only_not_admitted_to_execution','Batch_B_authorized':False,'Batch_C_authorized':False},
        'uncertainties':['native image/official positive controls absent','strict=False load key coverage absent',
                         'no runtime post-ViT feature trace','fixed temporal grid interval differs from sampled PTS',
                         'local decoder not bit-identical to original decoder','no new independent human/gold/holdout evidence']})
    for source in sorted(AUDIT.iterdir()):
        if source.is_file() and source.name!='build_review_package.py':put(source,Path('audit')/source.name)
    report=put(REPO/'docs/research/next/batch_A_scientific_review_2026-11-01.md',Path('reports/scientific_review.md'))
    # Relocate document links only in the new package derivative.
    body=report.read_text().replace('../../../data/research/reviews/batch_A_readonly_2026-11-01/','../audit/')
    report.write_text(body)
    changes.append('reports/scientific_review.md (package link relocation)')
    put(REPO/'docs/research/next/batch_A_results_2026-11-01.md',Path('reports/original_report_historical_sanitized.md'))
    for source in sorted(OLD.iterdir()):
        if source.is_file() and source.name!='server_preflight.json':
            put(source,Path('historical_records')/source.name)
    put(REPO/'data/research/next/gpu_pilot_manifest.json',Path('configuration/frozen_24_requests.json'))
    put(REPO/'docs/research/next/gpu_pilot_request.md',Path('configuration/original_batch_request.md'))
    patch=subprocess.run(['git','diff','--no-ext-diff','a1c2d5fb^','a1c2d5fb','--','scripts/diagnostics','tests/test_diagnostic_execution.py'],capture_output=True,check=True).stdout.decode()
    (PACKAGE/'code').mkdir()
    (PACKAGE/'code/a1c2d5fb_vs_parent.patch').write_text(sanitize(patch))
    metadata=subprocess.run(['git','show','-s','--format=%H%n%P%n%T%n%s','a1c2d5fb'],capture_output=True,text=True,check=True).stdout.splitlines()
    save(PACKAGE/'code/commit.json',dict(zip(['commit','parents','tree','subject'],metadata)))
    for source in sorted((RAW/'repository').rglob('*')):
        if source.is_file() and source.suffix in {'.py','.sh'} and '__pycache__' not in str(source):
            put(source,Path('code/executed_repository')/source.relative_to(RAW/'repository'))
    for source in sorted((RAW/'upstream').rglob('*')):
        if source.is_file() and not source.is_symlink() and '__pycache__' not in str(source):
            put(source,Path('code/pinned_Lance_source')/source.relative_to(RAW/'upstream'))
    failure_names=['CPU_decode_pre_generation.log','CPU_decode_compatibility_result.json',
                   'install_ffmpeg.log','install_ffmpeg_ranges.log','flash_resume_4jobs.log',
                   'flash_build_resume.json','restore_controller.log','finalize_restore.log',
                   'download_fixed.log','download_fixed_parallel.log','download_transport_revision.json',
                   'driver_compatibility.json','upstream_manifest.json']
    for name in failure_names:
        put(RAW/name,Path('setup_and_failure_evidence')/name)
    for q in state['requests']:
        run=RAW/q['native_run']
        task='t2v' if 'G-ATOMIC' in q['id'] else 'x2t_video'
        for source in sorted(run.rglob('*')):
            if source.is_file() and not source.is_symlink():
                put(source,Path('requests')/q['id']/source.relative_to(run))
    for source in sorted(VISUALS.rglob('*')):
        if source.is_file():put(source,Path('visuals')/source.relative_to(VISUALS))
    # The full answers must survive sanitization unchanged; only metadata paths move.
    answer_equal=[];video_equal=[]
    for q in state['requests']:
        rid=q['id']
        if 'G-ATOMIC' in rid:
            original=(RAW/q['native_run']/'t2v/outputs/000001.mp4').read_bytes()
            copy=(PACKAGE/'requests'/rid/'t2v/outputs/000001.mp4').read_bytes()
            video_equal.append(original==copy)
        else:
            original=read(RAW/q['native_run']/'x2t_video/outputs/result.json')[0]['answer']
            copy=read(PACKAGE/'requests'/rid/'x2t_video/outputs/result.json')[0]['answer']
            answer_equal.append(original==copy)
    cards=[]
    for r, finding in zip(rows,findings,strict=True):
        rid=r['id'];base=f'requests/{rid}';prompt=html.escape(r['prompt']);note=html.escape(finding['AI_evidence_review'])
        if r['raw_answer'] is not None:
            media=f'<video controls preload="none" src="{base}/inputs/visible.mp4"></video>'
            detail=f'<details><summary>完整原答与输入联系图</summary><pre>{html.escape(r["raw_answer"])}</pre><img src="visuals/{rid}-actual_input.png" alt="全部实际读取帧"><p><a href="{base}/x2t_video/actual_understanding_input.json">实际打包上下文</a> · <a href="{base}/x2t_video/actual_sampling.json">采样与PTS</a> · <a href="{base}/x2t_video/outputs/result.json">原答JSON</a></p></details>'
        else:
            media=f'<video controls preload="none" src="{base}/t2v/outputs/000001.mp4"></video>'
            detail=f'<div class="frames"><label>逐帧 <input type="range" min="0" max="32" value="0" data-rid="{rid}" oninput="showFrame(this)"><output>0 / 32</output></label><div class="pair"><figure><figcaption>编码前源RGB</figcaption><img id="{rid}-source" src="visuals/{rid}-source-frames/00.png"></figure><figure><figcaption>本机FFmpeg7.1解码</figcaption><img id="{rid}-decoded" src="visuals/{rid}-decoded-frames/00.png"></figure></div><p><a href="{base}/t2v/source_rgb_uint8.npz">源RGB数组</a> · <a href="{base}/t2v/decoded_rgb_uint8.npz">原服务器4.2.2解码数组</a></p></div>'
        cards.append(f'<article id="{rid}"><h2>{rid}</h2><p>{prompt}</p><p class="note">AI复核：{note}</p>{media}{detail}<p><a href="{base}/{r["native_task"]}/process.log">原执行日志</a> · <a href="{base}/{r["native_task"]}/worker_metrics.json">资源</a></p></article>')
    index_html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Batch A 独立证据审核</title><style>body{font:16px/1.65 system-ui;margin:24px auto;max-width:1180px;padding:0 16px;color:#17212b;background:#f5f6f8}article,header{background:white;padding:22px;margin:18px 0;border:1px solid #d4dbe2;border-radius:8px}h2{font-size:19px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;padding:16px}video{max-width:520px;width:100%;max-height:320px;background:#fff}img{max-width:100%;height:auto}input{width:55%}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}a{color:#0756a2}.note{border-left:3px solid #8796a8;padding-left:12px}summary{cursor:pointer;padding:8px}details>img{max-width:780px}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><header><h1>Batch A 独立证据审核包</h1><p>24次既有调用：20份完整原答、4段原生输出。另附20段实际输入视频。此页展示AI分析供独立复核，未采集或代填真人结论。</p><p><a href="reports/scientific_review.md">科学复核报告</a> · <a href="audit/per_request_evidence.csv">逐请求表</a> · <a href="audit/capability_matrix.json">能力矩阵</a> · <a href="audit/generation_all_frames.csv">全部逐帧记录</a> · <a href="code/a1c2d5fb_vs_parent.patch">代码差异</a> · <a href="README.md">范围与去敏说明</a></p><p>FIT-01：可继续准备，尚未准入训练执行。原P1状态不变。离线文件可直接打开，无外部请求。</p></header>'''+''.join(cards)+'''<script>function showFrame(el){const n=Number(el.value),rid=el.dataset.rid,s=String(n).padStart(2,'0');el.nextElementSibling.textContent=n+' / 32 ('+(n/12).toFixed(3)+'s)';for(const kind of ['source','decoded'])document.getElementById(rid+'-'+kind).src='visuals/'+rid+'-'+kind+'-frames/'+s+'.png';}</script></html>'''
    (PACKAGE/'index.html').write_text(index_html)
    (PACKAGE/'README.md').write_text('''# Batch A 独立证据审核包

解压后直接打开 index.html，无服务器或网络依赖。完整科学复核见 reports/scientific_review.md；original_report_historical_sanitized.md 是此前报告的去敏历史副本，其措辞需结合本轮限制阅读。

本包含24项既有请求、20份完整回答、4段原生输出MP4、20段已用输入MP4、全部实际读取/变换张量与采样、源/归档解码RGB、逐帧PNG、日志、配置、固定源码及提交代码差异。所有生成输出MP4字节与原件相同；20份回答内容与原件完全相同。文本副本仅去除私人路径、IP、访问凭据和URL查询信息，保留提示、答案、seed、参数、版本和科学数值；路径以 /TASK、/REPO、/LOCAL_USER 代替。JSON中实验状态为历史快照，不授予再次执行权限。

审核依据：本批全部为开发暴露数据，AI意见不构成真人金标；未知不计成方向错误；叙述未结构化不能当作笔顺错误。023有编码前后共同的右向增长正证据；4项识字错答仍有原生image正控、主模型键覆盖、内部视觉trace缺口。原生时间位置编码固定1秒，未反映12fps采样的每2帧间隔。原4.2.2与本机7.1解码单通道差最大2/255，像素不完全相同；每帧时间、增长方向和主要内容一致。

本轮未新增模型请求、GPU、训练、下载或真人任务；未推送/合并、未改历史与P1正式状态。FIT-01仅允许继续方案准备；Batch B/C仍须独立审批。

不含模型权重、tokenizer文件、安装环境、编译wheel、下载残片、SSH连接信息或私有Git历史。原备份的全部大文件仍保存在原本地归档；本包足以离线复核已保存结果，不能据此声称可直接离线重新推理。CPU审计脚本在 audit/，原执行代码在 code/executed_repository/；脚本原始运行入口依赖原仓库与原解包证据，禁止误当新GPU启动入口。

code/a1c2d5fb_vs_parent.patch 是目标提交相对其父提交的本批代码/测试差异；完整执行相关文件在 code/，上游Lance源码含LICENSE。package_manifest.json 列出包内文件及SHA-256；它不包含自身与外层ZIP。交付回执位于ZIP外部，防止循环校验。原20份回答和4份生成MP4的保真检查记录见 package_validation.json。
''')
    save(PACKAGE/'sanitization_record.json',{'text_derivatives_with_redactions_or_link_relocations':changes,
        'rules':['private absolute paths replaced with stable placeholders','IPv4 addresses redacted','URL query strings redacted',
                 'Bearer/access tokens redacted','no SSH or environment secrets included'],
        'raw_answers_unchanged':all(answer_equal),'native_output_MP4_bytes_unchanged':all(video_equal),
        'excluded':['model/tokenizer files','runtime/cache','compiled wheel','download binary fragments','SSH preflight','Git user identity/history'],
        'original_evidence_modified':False})
    # Scan the concrete deliverable, without echoing possibly sensitive matches.
    leaks=[]
    for path in PACKAGE.rglob('*'):
        if path.is_file() and path.suffix in {'.json','.jsonl','.py','.sh','.md','.txt','.log','.csv','.patch','.html'}:
            txt=path.read_text()
            if any(p in txt for p in [str(REPO),'/Users/cc','223.109.239.','180.127.11.','/home/vipuser/']):leaks.append(str(path.relative_to(PACKAGE)))
    if leaks or not all(answer_equal) or not all(video_equal):
        raise ValueError('Package privacy or preservation check failed; inspect local build without distributing')
    save(PACKAGE/'package_validation.json',{'existing_requests':24,'original_answers':20,'original_generated_videos':4,
        'input_carrier_videos':20,'all_raw_answers_equal_original':all(answer_equal),
        'all_four_native_MP4_bytes_equal_original':all(video_equal),'sensitive_literal_findings':len(leaks),
        'new_GPU_requests':0,'new_training':0})
    manifest=[]
    for path in sorted(PACKAGE.rglob('*')):
        if path.is_file():
            data=path.read_bytes();manifest.append({'path':str(path.relative_to(PACKAGE)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    save(PACKAGE/'package_manifest.json',{'excludes':['package_manifest.json','outer ZIP'],'files':manifest})
    zip_path=DELIVERY/'Batch_A_scientific_review_sanitized.zip'
    with zipfile.ZipFile(zip_path,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in sorted(PACKAGE.rglob('*')):
            if path.is_file():z.write(path,str(path.relative_to(PACKAGE)))
    with zipfile.ZipFile(zip_path) as z:
        corrupt=z.testzip()
        members=z.namelist()
    if corrupt:raise ValueError('New review ZIP CRC failure')
    sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
    receipt={'zip':str(zip_path.relative_to(REPO)),'bytes':zip_path.stat().st_size,'sha256':sha,
             'ZIP_CRC_check':'passed','files':len(members),'original_answers':20,'original_generated_videos':4,
             'input_videos':20,'all_original_answers_and_four_generated_videos_preserved':True,
             'sensitive_literal_findings':0,'GPU_calls':0,'training_runs':0}
    save(AUDIT/'delivery_receipt.json',receipt)
    save(DELIVERY/'delivery_receipt.json',receipt)
    print(json.dumps(receipt,ensure_ascii=False))


if __name__=='__main__':
    main()
