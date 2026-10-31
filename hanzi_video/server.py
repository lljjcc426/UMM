"""Start: python -m hanzi_video.server. Binds to local loopback only."""
import argparse
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re

from .planner import CommandBackend
from .service import VideoService
from .catalog import ASSETS

STATIC = Path(__file__).parent / 'static'


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, service, **kwargs):
        self.service = service
        super().__init__(*args, **kwargs)

    def json(self, status, value):
        raw = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == '/api/catalog':
            return self.json(200, self.service.catalog())
        match = re.fullmatch(r'/api/jobs/([0-9a-f]{16})', self.path)
        if match:
            path = self.service.output / match[1] / 'job.json'
            return self.json(200, self.service.job(match[1])) if path.exists() else self.json(404, {'error': '任务不存在'})
        if self.path == '/font-license':
            path, kind = ASSETS / 'licenses/ARPHICPL.TXT', 'text/plain; charset=utf-8'
        elif self.path in ('/', '/app.js', '/style.css'):
            name = 'index.html' if self.path == '/' else self.path[1:]
            path = STATIC / name
            kind = {'html': 'text/html; charset=utf-8', 'js': 'text/javascript; charset=utf-8', 'css': 'text/css; charset=utf-8'}[path.suffix[1:]]
        else:
            match = re.fullmatch(r'/outputs/([0-9a-f]{16})/(video\.mp4|video\.png)', self.path)
            if not match:
                return self.json(404, {'error': '页面不存在'})
            path = self.service.output / match[1] / match[2]
            if not path.exists() or self.service.job(match[1])['status'] != 'completed':
                return self.json(404, {'error': '视频尚未通过检查'})
            kind = 'video/mp4' if path.suffix == '.mp4' else 'image/png'
        raw = path.read_bytes()
        start, end = 0, len(raw)-1
        requested = self.headers.get('Range')
        if requested:
            interval = re.fullmatch(r'bytes=(\d*)-(\d*)', requested)
            if not interval or not any(interval.groups()):
                return self.json(416, {'error': '不支持该视频读取范围'})
            if interval[1]:
                start = int(interval[1])
                end = min(int(interval[2]), end) if interval[2] else end
            else:
                start = max(0, len(raw)-int(interval[2]))
            if start > end:
                return self.json(416, {'error': '视频读取范围超出文件'})
        self.send_response(206 if requested else 200)
        self.send_header('Content-Type', kind)
        self.send_header('Accept-Ranges', 'bytes')
        if requested:
            self.send_header('Content-Range', f'bytes {start}-{end}/{len(raw)}')
        self.send_header('Content-Length', str(end-start+1))
        self.end_headers()
        self.wfile.write(raw[start:end+1])

    def do_POST(self):
        if self.path not in ('/api/generate', '/api/recognize'):
            return self.json(404, {'error': '接口不存在'})
        if self.headers.get('Origin') and self.headers['Origin'] != 'http://' + self.headers.get('Host', ''):
            return self.json(403, {'error': '请从本地页面操作'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            if not 0 < length <= 3_000_000:
                raise ValueError('请求内容为空或图片过大')
            body = json.loads(self.rfile.read(length))
            state = self.service.submit(body, 'recognize' if self.path.endswith('recognize') else 'generate')
            self.json(202, state)
        except (ValueError, KeyError, OSError) as error:
            self.json(400, {'error': str(error)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8780)
    parser.add_argument('--output', type=Path, default=Path('private/engineering_hanzi_video/jobs'))
    args = parser.parse_args()
    command = json.loads(os.environ['UMM_PLANNER_COMMAND']) if os.environ.get('UMM_PLANNER_COMMAND') else None
    if command is not None and (not isinstance(command, list) or not command or not all(isinstance(s, str) for s in command)):
        parser.error('UMM_PLANNER_COMMAND must be a JSON array of command arguments')
    service = VideoService(args.output, CommandBackend(command))
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, service=service))
    print(f'Hanzi video: http://127.0.0.1:{args.port}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        service.executor.shutdown(wait=True)


if __name__ == '__main__':
    main()
