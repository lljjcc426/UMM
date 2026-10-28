"""Local P0 review service: blind payloads and versioned, reviewer-scoped saves.

Run with --preview for non-holdout operation tests before protocol freeze.
The repository, manifests, original IDs, predictions and event logs have no route.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import struct
from urllib.parse import parse_qs, urlparse
import uuid

from scripts.p0.prepare_acceptance import RUN, FACETS, STATUS_VALUES, REASONS

REFERENCE = Path('/Users/cc/.cache/umm-survey-20261023/223/R06-beijing.pdf')


def blind_png(raw):
    """Keep generic license/attribution text; remove sample-identity text without touching animation or pixels."""
    result = bytearray(raw[:8]); offset = 8
    while offset < len(raw):
        length = struct.unpack('>I', raw[offset:offset+4])[0]
        kind = raw[offset+4:offset+8]
        end = offset + 12 + length
        text_chunk=kind in [b'tEXt', b'zTXt', b'iTXt']
        key=raw[offset+8:offset+8+length].split(b'\0',1)[0] if text_chunk else None
        if not text_chunk or key in [b'license',b'modification_notice',b'source_revision']:
            result.extend(raw[offset:end])
        offset = end
    return bytes(result)


def public_task(task):
    fields = ['blind_id', 'type', 'character', 'official_page', 'official_index',
              'candidate_strokes', 'candidate_medians', 'frame_timestamps']
    result = {key: task[key] for key in fields if key in task}
    if task['type']=='rgb_event': result['media']='/media/'+task['blind_id']
    if 'ai_suggestion' in task:
        suggestion=task['ai_suggestion']
        result['ai_suggestion']={k:suggestion[k] for k in ['decision','facets','reasons','notes','disputed',
            'observed_order','events','model_version','priority','review_method','review_coverage','evidence']}
        if task['type']=='normative' and suggestion.get('reference_diagram'):
            result['reference_diagram']='/evidence/'+task['blind_id']
        result['assigned_partition']=task.get('assigned_partition')
        result['cross_review']=task.get('cross_review',False)
    return result


def validate_annotation(entry, task, protocol_id):
    """Validate the incoming annotation once; never infer human judgments."""
    if entry.get('protocol_id')!=protocol_id or entry.get('type')!=task['type']:
        raise ValueError('记录协议或任务类型不匹配')
    choices = ['consistent','conflict','unverified'] if task['type']=='normative' else ['correct','incorrect','unknown']
    if entry.get('decision') not in choices:
        raise ValueError('请选择独立结论')
    facets=entry.get('facets',{})
    if set(facets)!=set(FACETS[task['type']]) or any(v not in STATUS_VALUES for v in facets.values()):
        raise ValueError('各核验项目须独立选择；无法判断请选择未知')
    if any(reason not in REASONS for reason in entry.get('reasons',[])):
        raise ValueError('未知原因代码')
    if (entry.get('disputed') or entry['decision'] in ['incorrect','conflict']) and not entry.get('notes','').strip():
        raise ValueError('错误或争议记录请填写依据，不能由程序补填')
    return entry


class ReviewStore:
    def __init__(self, pack, directory, preview=False):
        self.pack=pack; self.directory=directory; self.preview=preview
        directory.mkdir(parents=True,exist_ok=True)
        self.tasks={t['blind_id']:t for values in pack['batches'].values() for t in values}
        self.tasks.update({t['blind_id']:t for t in pack['tutorial']})

    def reviewer(self, value):
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,40}',value or ''):
            raise ValueError('标注者ID请用1–40个英文字母、数字、下划线或短横线')
        return value

    def events(self, reviewer):
        path=self.directory/(self.reviewer(reviewer)+'.jsonl')
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def append(self, reviewer, event):
        event=dict(event,server_saved_at=datetime.now(timezone.utc).isoformat())
        with (self.directory/(self.reviewer(reviewer)+'.jsonl')).open('a') as handle:
            handle.write(json.dumps(event,ensure_ascii=False)+'\n')

    def state(self, reviewer):
        events=self.events(reviewer)
        annotations={}
        onboarded=False; progress={}
        for event in events:
            if event['kind']=='annotation':
                annotations[event['annotation']['blind_id']]=event['annotation']
                progress=event.get('progress',progress)
            elif event['kind']=='onboarding': onboarded=True
        return dict(annotations=list(annotations.values()),onboarded=onboarded,progress=progress,
                    legacy_import_events=sum(e['kind']=='legacy_import' for e in events))

    def allowed_batch(self, batch, reviewer):
        if batch not in self.pack['batches']: raise ValueError('不存在此批次')
        if self.pack['protocol'].get('mode')=='assisted': return
        if batch.startswith('practice'): return
        if self.preview: raise ValueError('页面操作测试只允许非保留集练习任务')
        state=self.state(reviewer)
        if not state['onboarded']: raise ValueError('先阅读准则、保存4项规范和12项RGB练习，再确认已理解口径')
        if batch=='holdout_rgb':
            done={a['blind_id'] for a in state['annotations']}
            if not all(t['blind_id'] in done for t in self.pack['batches']['holdout_norm']):
                raise ValueError('先分别完成64个保留字的规范核对；争议可保留，不能补造答案')


def handler_for(store):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, body, kind='application/json; charset=utf-8'):
            content=json.dumps(body,ensure_ascii=False).encode() if isinstance(body,(dict,list)) else body
            self.send_response(status); self.send_header('Content-Type',kind)
            self.send_header('Content-Length',str(len(content))); self.send_header('Cache-Control','no-store')
            self.end_headers(); self.wfile.write(content)

        def do_GET(self):
            url=urlparse(self.path); query=parse_qs(url.query)
            reviewer=query.get('reviewer',[''])[0]
            try:
                if url.path=='/':
                    filename='review_assisted.html' if store.pack['protocol'].get('mode')=='assisted' else 'review_v2.html'
                    self.reply(200,(Path('scripts/p0')/filename).read_bytes(),'text/html; charset=utf-8')
                elif url.path=='/api/protocol':
                    protocol=store.pack['protocol']
                    # Sampling seed, source IDs, labels and private order mappings stay off the review API.
                    self.reply(200,{k:protocol[k] for k in ['id','status','facets','status_values','error_reasons','mode'] if k in protocol})
                elif url.path=='/api/state': self.reply(200,store.state(reviewer))
                elif url.path=='/api/tasks':
                    batch=query.get('batch',['practice_norm'])[0]
                    store.allowed_batch(batch,reviewer)
                    self.reply(200,[public_task(t) for t in store.pack['batches'][batch]])
                elif url.path=='/api/tutorial':
                    self.reply(200,[dict(public_task(t),construction_demo=t['case']) for t in store.pack['tutorial']])
                elif url.path.startswith('/evidence/') and store.pack['protocol'].get('mode')=='assisted':
                    task=store.tasks[url.path.removeprefix('/evidence/')]
                    self.reply(200,Path(task['ai_suggestion']['reference_diagram']).read_bytes(),'image/png')
                elif url.path.startswith('/media/'):
                    task=store.tasks.get(url.path.removeprefix('/media/'))
                    if not task or task['type']!='rgb_event': self.reply(404,dict(error='不存在此媒体')); return
                    if task['batch']!='tutorial': store.allowed_batch(task['batch'],reviewer)
                    self.reply(200,blind_png(Path(task['media_path']).read_bytes()),'image/png')
                elif url.path=='/api/export':
                    state=store.state(reviewer)
                    self.reply(200,dict(schema='p0-human-annotations-v2',protocol_id=store.pack['protocol']['id'],
                        reviewer_id=reviewer,exported_at=datetime.now(timezone.utc).isoformat(),
                        annotations=state['annotations'],onboarded=state['onboarded'],progress=state['progress']))
                elif url.path=='/reference/standard.pdf' and REFERENCE.exists():
                    self.send_response(200); self.send_header('Content-Type','application/pdf')
                    self.send_header('Content-Length',str(REFERENCE.stat().st_size)); self.end_headers()
                    import shutil
                    with REFERENCE.open('rb') as source: shutil.copyfileobj(source,self.wfile)
                elif url.path=='/reference/license':
                    self.reply(200,Path('data/research/datasets/p0_stroke_synthetic_v1/licenses/ARPHICPL.TXT').read_bytes(),'text/plain; charset=utf-8')
                else: self.reply(404,dict(error='仅提供审核页面、白名单任务和媒体；不提供原始标签、清单或预测'))
            except ValueError as error:
                self.reply(400,dict(error=str(error)))

        def do_POST(self):
            try:
                payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                reviewer=store.reviewer(payload.get('reviewer_id',''))
                if self.path=='/api/save':
                    entry=payload['annotation']; task=store.tasks[entry['blind_id']]
                    store.allowed_batch(task['batch'],reviewer)
                    validate_annotation(entry,task,store.pack['protocol']['id'])
                    if entry.get('reviewer_id')!=reviewer: raise ValueError('记录与当前标注者不一致')
                    store.append(reviewer,dict(kind='annotation',annotation=entry,progress=payload.get('progress',{})))
                    self.reply(200,dict(saved=True))
                elif self.path=='/api/onboard':
                    done={a['blind_id'] for a in store.state(reviewer)['annotations']}
                    needed=store.pack['batches']['practice_norm']+store.pack['batches']['practice_rgb']
                    if not payload.get('acknowledged') or not all(t['blind_id'] in done for t in needed):
                        raise ValueError('请完成4项规范与12项RGB操作练习，并由本人确认已读判定口径')
                    store.append(reviewer,dict(kind='onboarding',acknowledged=True,
                        scope='User attested rubric understanding and operation practice; no expert gold qualification claimed'))
                    self.reply(200,dict(saved=True))
                elif self.path=='/api/import':
                    imported=payload['payload']; schema=imported.get('schema')
                    if schema=='p0-human-annotations-v1':
                        import_id=uuid.uuid4().hex
                        destination=store.directory/('legacy-'+import_id+'.json')
                        destination.write_text(json.dumps(imported,ensure_ascii=False,indent=2)+'\n')
                        store.append(reviewer,dict(kind='legacy_import',file=destination.name,
                            records=len(imported['annotations']),formal_credited=0))
                        self.reply(200,dict(saved=True,legacy_records=len(imported['annotations']),formal_credited=0))
                    elif schema=='p0-human-annotations-v2':
                        entries=imported['annotations']
                        # Restoring an existing export does not require the new
                        # store to already contain that export's onboarding/tasks.
                        # Validate once, before appending any human record.
                        for entry in entries:
                            task=store.tasks[entry['blind_id']]
                            if store.preview and not task['batch'].startswith('practice'):
                                raise ValueError('操作测试只导入非保留集练习记录')
                            validate_annotation(entry,task,store.pack['protocol']['id'])
                            if entry.get('reviewer_id')!=reviewer: raise ValueError('只导入当前标注者自己的记录，避免其他答案暴露')
                        prior_state=store.state(reviewer)
                        current={a['blind_id']:a for a in prior_state['annotations']}
                        added=conflicts=0
                        for entry in entries:
                            if entry['blind_id'] in current:
                                if current[entry['blind_id']]!=entry:
                                    store.append(reviewer,dict(kind='import_conflict',incoming=entry,existing_preserved=True)); conflicts+=1
                            else:
                                store.append(reviewer,dict(kind='annotation',annotation=entry,
                                    progress=imported.get('progress',{}))); added+=1
                        required=store.pack['batches'].get('practice_norm',[])+store.pack['batches'].get('practice_rgb',[])
                        restored_ids=set(current)|{entry['blind_id'] for entry in entries}
                        if imported.get('onboarded') is True and not prior_state['onboarded'] and all(t['blind_id'] in restored_ids for t in required):
                            store.append(reviewer,dict(kind='onboarding',acknowledged=True,
                                origin='Restored original own-export attestation after its practice records; no new human conclusion inferred'))
                        self.reply(200,dict(saved=True,imported=added,conflicts=conflicts))
                    else: raise ValueError('只支持v1原始试标或v2审核导出文件')
                else: self.reply(404,dict(error='不存在此操作'))
            except (ValueError,KeyError) as error:
                self.reply(400,dict(error=str(error)))
    return Handler


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8766)
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--assisted',action='store_true',help='Human review of AI prereview results; separate protocol/store')
    parser.add_argument('--storage',type=Path)
    args=parser.parse_args()
    if args.assisted:
        from scripts.p0.ai_prereview import RUN as AI_RUN
        pack=json.loads((AI_RUN/'assisted_review_pack.json').read_text())
    else: pack=json.loads((RUN/('review_draft.json' if args.preview else 'review_freeze.json')).read_text())
    storage=args.storage or Path('private/p0_assisted_human_review_2026-10-28' if args.assisted else 'private/p0_human_review_2026-10-28')
    server=ThreadingHTTPServer(('127.0.0.1',args.port),handler_for(ReviewStore(pack,storage,args.preview)))
    print('P0 review', 'non-holdout preview' if args.preview else 'frozen protocol', server.server_address,flush=True)
    server.serve_forever()
