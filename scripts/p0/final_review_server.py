"""Local one-package review: own-only state, blind predictions, append-only saves."""
from __future__ import annotations

import argparse
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse,parse_qs

from scripts.p0.casia_subset import PRIVATE
from scripts.p0.review_server import blind_png

REASONS={'wrong_order':'先后错误','reverse_direction':'方向错误','missing':'缺笔或不完整','extra':'多笔或额外墨迹',
         'concurrent':'同时或提前添墨','disappeared':'旧墨迹消失','blank':'空白','temporal_ambiguity':'时间证据不足',
         'geometry_ambiguity':'笔画身份不清','norm_conflict':'与规范不符','segmentation':'裁切或字符对应有误','other':'其他'}


def validate(entry,task,protocol,reviewer):
    """Validate actual user input once; never synthesize a missing judgment."""
    if entry.get('protocol_id')!=protocol or entry.get('reviewer_id')!=reviewer or entry.get('kind')!=task['kind']:
        raise ValueError('协议、审核者或项目类型不一致')
    choices=['correct','incorrect','unknown'] if task['kind']=='rgb' else ['pass','fail','unknown']
    if task['kind']=='normative':
        values=entry.get('judgments',{})
        if set(values)!={'identity_order','direction'} or any(v not in choices for v in values.values()):
            raise ValueError('请明确记录身份/次序与方向；不确定可选未知')
    elif entry.get('decision') not in choices:raise ValueError('请选择实际判断')
    if any(r not in REASONS for r in entry.get('reasons',[])):raise ValueError('错误原因代码无效')
    if task['kind']=='rgb' and entry['decision']=='incorrect' and not entry.get('reasons'):
        raise ValueError('请至少点选一个实际错误原因')


class FinalStore:
    def __init__(self,pack,directory,preview=False):
        self.pack=pack;self.directory=directory;self.preview=preview;directory.mkdir(parents=True,exist_ok=True)
        self.tasks={t['blind_id']:t for t in pack['tasks']};self.internal={t['id']:t for t in pack['tasks']}

    def ids(self,reviewer):
        if reviewer not in ['1','2']:raise ValueError('请选择本人审核者ID：1或2')
        return [self.internal[i]['blind_id'] for i in self.pack['reviewer_orders'][reviewer]]

    def state(self,reviewer):
        self.ids(reviewer);path=self.directory/(reviewer+'.jsonl');latest={}
        if path.exists():
            for line in path.read_text().splitlines():
                event=json.loads(line)
                if event['kind']=='annotation':latest[event['annotation']['blind_id']]=event['annotation']
        return dict(annotations=list(latest.values()),total=len(self.ids(reviewer)),saved=len(latest),reviewer_id=reviewer)

    def append(self,reviewer,entry,origin='human_UI'):
        ids=self.ids(reviewer)
        if entry.get('blind_id') not in ids:raise ValueError('记录不属于本轮本人任务')
        validate(entry,self.tasks[entry['blind_id']],self.pack['protocol']['id'],reviewer)
        self.write_event(reviewer,entry,origin)

    def write_event(self,reviewer,entry,origin):
        event=dict(kind='annotation',annotation=entry,origin=origin,server_saved_at=datetime.now(timezone.utc).isoformat())
        with (self.directory/(reviewer+'.jsonl')).open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')

    def public(self,task):
        bid=task['blind_id'];result={k:task[k] for k in ['kind','character','question','line_text','position','explanation'] if k in task}
        result['blind_id']=bid
        if task['kind']=='normative':result.update(strokes=task['strokes'],reference='/asset/'+bid+'/reference')
        elif task['kind']=='rgb':result.update(media='/media/'+bid,reference='/asset/'+bid+'/reference',frame_timestamps=task['frame_timestamps'])
        else:result.update(context='/asset/'+bid+'/context',cut='/asset/'+bid+'/cut')
        return result


def handler_for(store):
    class Handler(BaseHTTPRequestHandler):
        def reply(self,status,value,kind='application/json; charset=utf-8'):
            raw=json.dumps(value,ensure_ascii=False).encode() if isinstance(value,(dict,list)) else value
            self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)))
            self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)

        def do_GET(self):
            u=urlparse(self.path);q=parse_qs(u.query);reviewer=q.get('reviewer',['1'])[0]
            try:
                if u.path=='/':self.reply(200,Path('scripts/p0/review_final.html').read_bytes(),'text/html; charset=utf-8')
                elif u.path=='/api/protocol':
                    p=store.pack['protocol'];self.reply(200,{k:p[k] for k in ['id','status','human_characters','human_normative_tasks','human_RGB_tasks','human_record_tasks','tasks_per_reviewer'] if k in p}|dict(error_reasons=REASONS,preview=store.preview))
                elif u.path=='/api/tasks':self.reply(200,[store.public(store.tasks[i]) for i in store.ids(reviewer)])
                elif u.path=='/api/state':self.reply(200,store.state(reviewer))
                elif u.path=='/api/export':self.reply(200,dict(schema='p0-final-human-review-v1',protocol_id=store.pack['protocol']['id'],**store.state(reviewer)))
                elif u.path=='/api/tutorial':
                    self.reply(200,[dict(id=t['id'],explanation=t['explanation'],media='/demo/'+t['id']) for t in store.pack.get('tutorial',[])])
                elif u.path.startswith('/asset/'):
                    _,_,bid,asset=u.path.split('/');task=store.tasks[bid]
                    path=task[{'reference':'reference_path','context':'context_path','cut':'cut_path'}[asset]]
                    self.reply(200,Path(path).read_bytes(),'image/png')
                elif u.path.startswith('/media/'):
                    task=store.tasks[u.path.removeprefix('/media/')]
                    self.reply(200,blind_png(Path(task['path']).read_bytes()),'image/png')
                elif u.path.startswith('/demo/'):
                    task=next(t for t in store.pack.get('tutorial',[]) if t['id']==u.path.removeprefix('/demo/'))
                    self.reply(200,blind_png(Path(task['path']).read_bytes()),'image/png')
                else:self.reply(404,dict(error='仅提供本轮页面、本人进度和指定参考；不提供预测、构造标签或原始目录'))
            except (ValueError,KeyError,StopIteration) as e:self.reply(400,dict(error=str(e)))

        def do_POST(self):
            try:
                data=json.loads(self.rfile.read(int(self.headers['Content-Length'])));reviewer=data['reviewer_id'];store.ids(reviewer)
                if self.path=='/api/save':
                    store.append(reviewer,data['annotation']);self.reply(200,dict(saved=True))
                elif self.path=='/api/import':
                    incoming=data['payload']
                    if incoming.get('schema')!='p0-final-human-review-v1' or incoming.get('protocol_id')!=store.pack['protocol']['id'] or incoming.get('reviewer_id')!=reviewer:
                        raise ValueError('只导入本人本轮的导出文件')
                    entries=incoming['annotations'];ids=store.ids(reviewer)
                    # Validate the complete import before appending any record.
                    for entry in entries:
                        if entry.get('blind_id') not in ids:raise ValueError('导入含非本轮项目')
                        validate(entry,store.tasks[entry['blind_id']],store.pack['protocol']['id'],reviewer)
                    current={e['blind_id']:e for e in store.state(reviewer)['annotations']};added=conflicts=0
                    for entry in entries:
                        if entry['blind_id'] not in current:store.write_event(reviewer,entry,'own_import');added+=1
                        elif current[entry['blind_id']]!=entry:
                            with (store.directory/(reviewer+'-import-conflicts.jsonl')).open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
                            conflicts+=1
                    self.reply(200,dict(imported=added,conflicts_preserved=conflicts))
                else:self.reply(404,dict(error='未知操作'))
            except (ValueError,KeyError) as e:self.reply(400,dict(error=str(e)))
    return Handler


def prepare_blind_ids(path):
    import random
    pack=json.loads(path.read_text());rng=random.Random(2026102805)
    ids=rng.sample(range(1<<40),len(pack['tasks']))
    for t,bid in zip(pack['tasks'],ids):t['blind_id']=f'F-{bid:010x}'
    path.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8770);p.add_argument('--preview',action='store_true');p.add_argument('--storage',type=Path)
    args=p.parse_args();path=PRIVATE/('operation_pack.json' if args.preview else 'pack_frozen.json')
    directory=args.storage or PRIVATE/('UI_TEST' if args.preview else 'human_records')
    ThreadingHTTPServer(('127.0.0.1',args.port),handler_for(FinalStore(json.loads(path.read_text()),directory,args.preview))).serve_forever()
