"""Local job service. Artifacts stay under the private output directory."""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from io import BytesIO
import json
from pathlib import Path
import time
import traceback
import uuid

from PIL import Image, ImageOps

from .audit import audit_video
from .catalog import canonical_plan, load_catalog, reference
from .planner import BackendUnavailable, recognize, plan_with_correction
from .render import render_video


def save_json(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


class VideoService:
    def __init__(self, output, backend):
        self.output, self.backend = Path(output).resolve(), backend
        self.output.mkdir(parents=True, exist_ok=True)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def catalog(self):
        catalog = load_catalog()
        return {'version': catalog['version'], 'backend_configured': self.backend.configured,
            'backend_live_verified': False,
            'characters': [{'character': r['character'], 'strokes': r['sequence'],
                'qualification': r['qualification']} for r in catalog['characters'].values()]}

    def job(self, job_id):
        return json.loads((self.output / job_id / 'job.json').read_text())

    def submit(self, payload, operation='generate'):
        # All public request validation lives here, once, before queuing.
        if not isinstance(payload, dict):
            raise ValueError('请求格式错误')
        mode = payload.get('mode', 'umm')
        if mode not in ('umm', 'preview'):
            raise ValueError('请选择UMM生成或CPU预览')
        if (operation == 'recognize' or mode == 'umm') and not self.backend.configured:
            raise BackendUnavailable('UMM尚未连接；当前可以使用CPU执行预览')
        image_bytes, image_path = None, None
        if operation == 'recognize':
            encoded = payload.get('image', '')
            if not isinstance(encoded, str) or not encoded.startswith('data:image/') or len(encoded) > 3_000_000:
                raise ValueError('请上传不超过2MB的单字图片')
            image_bytes = base64.b64decode(encoded.split(',', 1)[1], validate=True)
            with Image.open(BytesIO(image_bytes)) as image:
                if max(image.size) > 4096:
                    raise ValueError('图片最长边不能超过4096像素')
                image.load()
        else:
            char = payload.get('character', '')
            if not isinstance(char, str) or len(char.strip()) != 1:
                raise ValueError('请一次输入一个汉字')
            char = char.strip()
            reference(char)
            recognition_id = payload.get('recognition_id')
            if recognition_id:
                if not isinstance(recognition_id, str) or len(recognition_id) != 16 or not all(c in '0123456789abcdef' for c in recognition_id):
                    raise ValueError('识别记录不存在')
                previous = self.job(recognition_id)
                if previous.get('status') != 'completed' or previous.get('operation') != 'recognize' or previous.get('character') != char:
                    raise ValueError('请先确认UMM实际识别的目标字')
                image_path = self.output / recognition_id / 'input.png'
            speed = payload.get('speed', 1)
            if type(speed) not in (int, float) or speed not in (.75, 1, 1.5):
                raise ValueError('请选择预设书写速度')
        job_id = uuid.uuid4().hex[:16]
        folder = self.output / job_id
        folder.mkdir()
        if image_bytes:
            (folder / 'input_original').write_bytes(image_bytes)
            with Image.open(BytesIO(image_bytes)) as image:
                rgba = ImageOps.exif_transpose(image).convert('RGBA')
                background = Image.new('RGBA', rgba.size, 'white')
                background.alpha_composite(rgba)
                background.convert('RGB').save(folder / 'input.png')
        state = {'id': job_id, 'operation': operation, 'mode': mode, 'status': 'queued',
                 'created_at': datetime.now(timezone.utc).isoformat(),
                 'character': payload.get('character'), 'speed': payload.get('speed', 1)}
        save_json(folder / 'job.json', state)
        save_json(folder / 'request.json', {k: v for k, v in payload.items() if k != 'image'})
        self.executor.submit(self._execute, state, folder, image_path)
        return state

    def _execute(self, state, folder, image):
        started = time.perf_counter()
        state = {**state, 'status': 'running'}
        save_json(folder / 'job.json', state)
        try:
            if state['operation'] == 'recognize':
                char = recognize(self.backend, folder / 'input.png', folder / 'recognition')
                state.update(character=char, supported=char in load_catalog()['characters'],
                             requires_user_confirmation=True, status='completed')
            else:
                ref = reference(state['character'])
                if state['mode'] == 'preview':
                    plan, calls = canonical_plan(ref), 0
                else:
                    plan, calls = plan_with_correction(self.backend, ref, image, folder)
                save_json(folder / 'accepted_plan.json', plan)
                render = render_video(ref, plan, folder / 'video.mp4', speed=state['speed'])
                save_json(folder / 'render.json', render)
                audit = audit_video(folder / 'video.mp4', ref)
                save_json(folder / 'rgb_audit.json', audit)
                if not audit['passed']:
                    raise ValueError('输出视频回读检查未通过：' + '；'.join(audit['errors']))
                state.update(status='completed', model_calls=calls,
                    reference_version=load_catalog()['version'], reference_qualification=ref['qualification'],
                    human_per_stroke_gold=False, rendering=render, audit=audit,
                    video_url=f'/outputs/{state["id"]}/video.mp4', poster_url=f'/outputs/{state["id"]}/video.png')
        except Exception as error:
            # One job boundary: preserve failure evidence, never substitute a preview.
            (folder / 'failure.txt').write_text(traceback.format_exc())
            state.update(status='failed', error=str(error))
        state['elapsed_seconds'] = time.perf_counter() - started
        save_json(folder / 'job.json', state)
