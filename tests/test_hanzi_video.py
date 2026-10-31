import base64
from copy import deepcopy
from io import BytesIO
import json
import subprocess
from pathlib import Path
import tempfile
import unittest

import imageio_ffmpeg
import numpy as np
from PIL import Image

from hanzi_video.audit import audit_video
from hanzi_video.catalog import canonical_plan, geometry, load_catalog, reference, validate_plan
from hanzi_video.planner import BackendUnavailable, CommandBackend, plan_with_correction
from hanzi_video.render import render_video
from hanzi_video.service import VideoService
from scripts.engineering.lance_planner import native_args, prepare_input


class TestBackend:
    """Unit test only; never available from a product route or default setting."""
    configured = True

    def __init__(self, answers):
        self.answers = iter(answers)
        self.requests = []

    def ask(self, payload, folder):
        folder.mkdir(parents=True)
        self.requests.append(payload)
        value = next(self.answers)
        (folder / 'TEST_ONLY_answer.json').write_text(json.dumps(value, ensure_ascii=False))
        return value


class HanziVideoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_catalog_bindings_do_not_depend_on_geometry_storage_order(self):
        for char, ref in load_catalog()['characters'].items():
            self.assertFalse(ref['human_per_stroke_gold'])
            before = geometry(ref)
            ref['geometry'].reverse()
            self.assertEqual(before, geometry(ref), char)
            self.assertEqual([], validate_plan(canonical_plan(ref), ref))
        self.assertNotEqual([s['id'] for s in reference('士')['geometry']],
                            [s['id'] for s in reference('士')['sequence']])

    def test_target_order_direction_and_completeness_rejected_before_render(self):
        ref = reference('士')
        for change in ('target', 'order', 'direction', 'missing'):
            plan = canonical_plan(ref)
            if change == 'target':
                plan['character'] = '土'
            elif change == 'order':
                plan['strokes'].reverse()
            elif change == 'direction':
                plan['strokes'][0]['direction'] = 'reverse'
            else:
                plan['strokes'].pop()
            with self.subTest(change=change), self.assertRaises(ValueError):
                render_video(ref, plan, self.folder / 'not-created.mp4')
            self.assertFalse((self.folder / 'not-created.mp4').exists())

    def test_all_eight_actual_mp4s_pass_rgb_and_pts_check(self):
        for char, ref in load_catalog()['characters'].items():
            with self.subTest(character=char):
                path = self.folder / (str(ord(char)) + '.mp4')
                report = render_video(ref, canonical_plan(ref), path)
                audit = audit_video(path, ref)
                self.assertTrue(audit['passed'], audit['errors'])
                self.assertEqual(report['frames'], audit['decoded_frames'])
                self.assertFalse(audit['renderer_event_log_used'])

    def test_rgb_rejects_wrong_order_direction_and_missing_stroke(self):
        ref = reference('士')
        for change in ('order', 'direction', 'missing'):
            altered = deepcopy(ref)
            if change == 'order':
                altered['sequence'].reverse()
            elif change == 'direction':
                altered['sequence'][0]['direction'] = 'reverse'
            else:
                altered['sequence'].pop()
            path = self.folder / f'{change}.mp4'
            # Deliberately inconsistent reference for fault injection only.
            render_video(altered, canonical_plan(altered), path, size=128)
            audit = audit_video(path, ref, size=128)
            self.assertFalse(audit['passed'], change)

    def test_rgb_rejects_flash_and_history_erasure(self):
        ref = reference('士')
        good = self.folder / 'good.mp4'
        render_video(ref, canonical_plan(ref), good, size=128)
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(good),
            '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'], capture_output=True, check=True).stdout
        frames = list(np.frombuffer(raw, np.uint8).reshape(-1,128,128,3))
        for kind in ('flash', 'erasure'):
            modified = [f.copy() for f in frames]
            if kind == 'flash':
                modified[12:] = [frames[-1]] * (len(modified)-12)
            else:
                modified[-6:-3] = [frames[0]] * 3
            path = self.folder / f'{kind}.mp4'
            writer = imageio_ffmpeg.write_frames(str(path),(128,128),fps=24,codec='libx264',output_params=['-crf','10'],ffmpeg_log_level='error')
            writer.send(None)
            for frame in modified:
                writer.send(frame)
            writer.close()
            self.assertFalse(audit_video(path, ref, size=128)['passed'], kind)

    def test_invalid_plan_is_corrected_with_original_failure_preserved(self):
        ref = reference('小')
        wrong = canonical_plan(ref)
        wrong['strokes'].reverse()
        backend = TestBackend([wrong, canonical_plan(ref)])
        plan, calls = plan_with_correction(backend, ref, None, self.folder)
        self.assertEqual(calls, 2)
        self.assertEqual(plan, canonical_plan(ref))
        first = json.loads((self.folder / 'validation-1.json').read_text())
        self.assertTrue(first['errors'])
        self.assertEqual(first['plan'], wrong)
        self.assertIn('validation_errors', backend.requests[1])

    def test_two_invalid_plans_stop_without_fallback(self):
        backend = TestBackend([{'character':'错'}, {'character':'错'}])
        with self.assertRaises(ValueError):
            plan_with_correction(backend, reference('士'), None, self.folder)
        self.assertEqual(2, len(backend.requests))
        self.assertFalse(any(self.folder.glob('*.mp4')))

    def test_service_preview_and_offline_umm_are_separate(self):
        service = VideoService(self.folder, CommandBackend())
        with self.assertRaises(BackendUnavailable):
            service.submit({'character':'士','mode':'umm'})
        state = service.submit({'character':'士','mode':'preview'})
        service.executor.shutdown(wait=True)
        done = service.job(state['id'])
        self.assertEqual('completed', done['status'])
        self.assertEqual(0, done['model_calls'])
        self.assertEqual('preview', done['mode'])
        self.assertTrue(done['audit']['passed'])

    def test_image_recognition_record_and_explicit_target_are_separate(self):
        image = BytesIO()
        Image.new('RGB',(64,64),'white').save(image,format='PNG')
        encoded = 'data:image/png;base64,' + base64.b64encode(image.getvalue()).decode()
        service = VideoService(self.folder,TestBackend([{'status':'identified','character':'士'}]))
        state = service.submit({'image':encoded},operation='recognize')
        service.executor.shutdown(wait=True)
        done = service.job(state['id'])
        self.assertTrue(done['requires_user_confirmation'])
        self.assertTrue((self.folder / state['id'] / 'input_original').exists())
        self.assertFalse(any((self.folder / state['id']).glob('*.mp4')))
        with self.assertRaises(ValueError):
            service.submit({'character':'小','recognition_id':state['id'],'mode':'preview'})

    def test_umm_orchestration_uses_validated_plan_without_claiming_real_model(self):
        ref = reference('士')
        wrong = canonical_plan(ref)
        wrong['strokes'].reverse()
        backend = TestBackend([wrong, canonical_plan(ref)])
        service = VideoService(self.folder, backend)
        state = service.submit({'character':'士','mode':'umm'})
        service.executor.shutdown(wait=True)
        done = service.job(state['id'])
        self.assertEqual('completed', done['status'])
        self.assertEqual(2, done['model_calls'])
        self.assertEqual('umm', done['mode'])
        self.assertTrue(done['audit']['passed'])
        self.assertTrue((self.folder / state['id'] / 'validation-1.json').exists())

    def test_native_materialization_has_current_prompt_and_blank_text_image(self):
        payload = {'prompt':'为“点”规划笔画','image':None}
        dataset = prepare_input(payload,self.folder)
        row = json.loads(dataset.read_text())['engineering-request']
        self.assertEqual(row['interleave_array'][1][1],payload['prompt'])
        self.assertEqual(row['interleave_array'][1][2],'UNUSED_TARGET_PLACEHOLDER')
        self.assertTrue(np.asarray(Image.open(row['interleave_array'][0])).min()==255)
        args = native_args(Path('/model'),Path('/vit'),dataset,self.folder/'output')
        self.assertEqual(args[args.index('--task')+1],'x2t_image')
        self.assertEqual(args[args.index('--enhance_prompt')+1],'false')


if __name__ == '__main__':
    unittest.main()
