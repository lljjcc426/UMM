"""Structured UMM requests and bounded correction; no simulated fallback."""
import json
import subprocess
import time

from .catalog import validate_plan


class BackendUnavailable(ValueError):
    pass


def parse_answer(answer):
    text = answer.strip()
    if text.startswith('```') and text.endswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    return json.loads(text)


class CommandBackend:
    """Configured by the operator, never by a browser request. No shell eval."""
    def __init__(self, command=None):
        self.command = command

    @property
    def configured(self):
        return bool(self.command)

    def ask(self, payload, folder):
        if not self.configured:
            raise BackendUnavailable('UMM尚未连接。可以先使用CPU执行预览。')
        folder.mkdir(parents=True)
        request, response = folder / 'request.json', folder / 'response.json'
        request.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        started = time.perf_counter()
        with (folder / 'backend.log').open('w') as log:
            result = subprocess.run([*self.command, '--request', str(request.resolve()),
                '--response', str(response.resolve())], stdout=log, stderr=subprocess.STDOUT,
                timeout=900, check=False)
        (folder / 'process.json').write_text(json.dumps({'exit_code': result.returncode,
            'elapsed_seconds': time.perf_counter()-started, 'command': self.command}, indent=2))
        if result.returncode:
            raise RuntimeError('UMM调用失败，原始日志已保留')
        return parse_answer(json.loads(response.read_text())['answer'])


def recognize(backend, image, folder):
    payload = {'operation': 'recognize', 'image': str(image.resolve()),
        'prompt': '识别图片中唯一的汉字。多字、模糊或无法确定时标记unknown。只输出JSON：'
                  '{"status":"identified或unknown","character":"一个汉字或空字符串"}。'}
    answer = backend.ask(payload, folder)
    if not isinstance(answer, dict) or answer.get('status') != 'identified':
        raise ValueError('UMM无法确定图中的单个汉字，请更换清晰图片或输入文字')
    char = answer.get('character')
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError('UMM没有返回唯一汉字')
    return char


def plan_with_correction(backend, ref, image, folder):
    guide = [{'position': i, **stroke} for i, stroke in enumerate(ref['sequence'], 1)]
    payload = {'operation': 'plan', 'character': ref['character'],
        'image': str(image.resolve()) if image else None,
        'prompt': f'用户要求书写汉字“{ref["character"]}”。依据以下规范参考检查笔画身份、顺序和方向。'
            '只返回JSON {"character":"目标字","strokes":[{"id":"笔画ID","direction":"forward或reverse"}]}。'
            '不要输出思维过程。forward表示沿所列规范方向。规范参考：' + json.dumps(guide, ensure_ascii=False)}
    for attempt in range(2):
        try:
            plan = backend.ask(payload, folder / f'plan-{attempt+1}')
            errors = validate_plan(plan, ref)
        except (json.JSONDecodeError, KeyError) as error:
            plan, errors = None, ['返回内容不符合JSON协议：' + str(error)]
        (folder / f'validation-{attempt+1}.json').write_text(json.dumps(
            {'plan': plan, 'errors': errors}, ensure_ascii=False, indent=2))
        if not errors:
            return plan, attempt + 1
        payload = {**payload, 'prompt': payload['prompt'] + '\n前次输出未通过校验：'
                   + '；'.join(errors) + '。请重新检查后返回完整JSON。',
                   'previous_answer': plan, 'validation_errors': errors}
    raise ValueError('UMM两次计划均未通过规范校验，已保留原始回答，未生成视频')
