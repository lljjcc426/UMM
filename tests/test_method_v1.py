from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import importlib.util
TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None
if TORCH_AVAILABLE:
    import torch
from PIL import Image

from method_v1.paired import parse_description, read_pairs, audit_disjoint
if TORCH_AVAILABLE:
    from method_v1.fusion import TinyPairedStrokeModel, stroke_sequence_loss, global_contrastive_loss
from method_v1.program import parse_program, render_frames, order_signature, save_mp4, audit_mp4
from method_v1.cli import demo_programs, build_fixtures, smoke_models

ROOT = Path(__file__).resolve().parents[1] / 'data/research/method_v1_cpu_2026-11-04/attachment'

class PairAndIdentifiabilityTest(unittest.TestCase):
    def test_real_training_schema_and_strokes(self):
        self.assertEqual(parse_description('横、撇、竖、横、竖、横、在'),((1,3,2,1,2,1),'在'))
        self.assertEqual(parse_description('横、竖、横、土'), ((1,2,1),'土'))
        self.assertEqual(parse_description('横、竖、横、士'), ((1,2,1),'士'))
        for desc in ('横、竖、土[EOF]', '横、空、土', '土', ''):
            with self.assertRaises(ValueError):
                parse_description(desc)

    def test_pair_loader_keeps_gold_and_geometry_out(self):
        pairs = read_pairs(ROOT/'examples'/'synthetic_pairs.jsonl', ROOT/'examples')
        self.assertEqual(len(pairs), 2)
        self.assertEqual({p.character for p in pairs}, {'土','士'})
        self.assertEqual(pairs[0].strokes, pairs[1].strokes)
        self.assertNotEqual(pairs[0].image_digest, pairs[1].image_digest)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'bad.jsonl'
            r = json.loads((ROOT/'examples'/'synthetic_pairs.jsonl').read_text().splitlines()[0])
            r['evaluation_only'] = {'gold_path': 'do-not-read'}
            p.write_text(json.dumps(r,ensure_ascii=False)+'\n')
            with self.assertRaisesRegex(ValueError,'unexpected'):
                read_pairs(p,ROOT/'examples')

    def test_blank_background_without_ink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory/'media').mkdir()
            sid = '00000000000000ab'
            Image.new('RGB',(64,64),'white').save(directory/'media'/f'{sid}.png')
            record = {'id':sid,'model_inputs':{'image':f'media/{sid}.png'},
                      'training_targets':{'description':'横、土'}}
            (directory/'train.jsonl').write_text(json.dumps(record,ensure_ascii=False)+'\n')
            with self.assertRaisesRegex(ValueError,'No visible character ink'):
                read_pairs(directory/'train.jsonl', directory)

    def test_split_leakage_checks(self):
        pairs = read_pairs(ROOT/'examples'/'synthetic_pairs.jsonl', ROOT/'examples')
        self.assertTrue(audit_disjoint({'train':[pairs[0]],'dev':[pairs[1]]})['passed'])
        with self.assertRaisesRegex(ValueError,'leakage'):
            audit_disjoint({'train':[pairs[0]],'dev':[pairs[0]]})

    def test_same_image_and_same_description_can_hide_a_swapped_order(self):
        correct = parse_program(demo_programs()['tu'])
        wrong = parse_program(json.loads((ROOT/'examples'/'tu_swapped.program.json').read_text()))
        self.assertEqual(order_signature(correct),order_signature(wrong))
        frames_a = list(render_frames(correct))
        frames_b = list(render_frames(wrong))
        self.assertTrue(np.array_equal(frames_a[0],frames_b[0]))
        self.assertTrue(np.array_equal(frames_a[-1],frames_b[-1]))
        self.assertFalse(np.array_equal(frames_a[6],frames_b[6]))

@unittest.skipUnless(TORCH_AVAILABLE, "CPU torch optional; exercised in the dedicated method CPU job")
class ModelContractTest(unittest.TestCase):
    def setUp(self):
        torch.default_generator.manual_seed(9)
        torch.set_num_threads(1)
        self.images=torch.rand(2,3,64,64)
        self.targets=torch.tensor([[1,2,1,8],[1,2,1,8]])
        self.chars=torch.tensor([ord('土'),ord('士')])

    def test_four_fusion_interfaces_no_training(self):
        for mode in ('sft','global','cross','ordered'):
            with self.subTest(mode=mode):
                model=TinyPairedStrokeModel(mode,width=32)
                output=model(self.images,self.targets,self.chars)
                self.assertEqual(list(output.logits.shape),[2,4,9])
                if mode in ('cross','ordered'):
                    self.assertEqual(list(output.attention.shape),[2,4,16])
                else:
                    self.assertIsNone(output.attention)
                loss=stroke_sequence_loss(output,self.targets)
                if mode!='sft': loss=loss+global_contrastive_loss(output)
                self.assertTrue(bool(torch.isfinite(loss)))
                loss.backward()
                self.assertTrue(any(x.grad is not None for x in model.parameters()))

    def test_decoder_never_sees_current_or_future_target(self):
        for mode in ('sft', 'global', 'cross', 'ordered'):
            with self.subTest(mode=mode):
                model=TinyPairedStrokeModel(mode,width=32).eval()
                target1=torch.tensor([[1,2,1,8]])
                target2=torch.tensor([[1,2,3,8]])
                im=self.images[:1]
                with torch.no_grad():
                    o1=model(im,target1).logits
                    o2=model(im,target2).logits
                # token 3 differs, prediction indices 0..2 must not change
                self.assertTrue(torch.allclose(o1[:,:3],o2[:,:3],rtol=0,atol=1e-6))
                self.assertFalse(torch.allclose(o1[:,3],o2[:,3]))

    def test_ordered_cross_modal_gradients_reach_both_branches(self):
        model = TinyPairedStrokeModel('ordered', width=32)
        output = model(self.images, self.targets, self.chars)
        stroke_sequence_loss(output, self.targets).backward()
        self.assertGreater(float(model.vision.weight.grad.abs().sum()), 0)
        self.assertGreater(float(model.text_tokens.weight.grad.abs().sum()), 0)
        self.assertGreater(float(model.cross.in_proj_weight.grad.abs().sum()), 0)
        self.assertGreater(float(model.visual_position.weight.grad.abs().sum()), 0)

    def test_character_only_in_separate_global_head(self):
        m=TinyPairedStrokeModel('ordered',width=32).eval()
        with torch.no_grad():
            out1=m(self.images,self.targets,self.chars)
            out2=m(self.images,self.targets,self.chars.flip(0))
        self.assertTrue(torch.allclose(out1.logits,out2.logits,atol=0,rtol=0))
        self.assertFalse(torch.allclose(out1.text_embedding,out2.text_embedding))

    def test_cpu_smoke_reports_no_updates(self):
        r=smoke_models()
        self.assertEqual(r['actual_model_train_steps'],0)
        self.assertEqual(set(r['mode_checks']),{'sft','global','cross','ordered'})

class ProgramTest(unittest.TestCase):
    def test_program_rejects_unsafe_and_invalid_actions(self):
        obj=demo_programs()['tu']
        for mutate in [
            lambda x:x.update({'command':'python -c ...'}),
            lambda x:x['strokes'][0].update({'order':3}),
            lambda x:x['strokes'][0].update({'path':[[0.2,0.3],[float('nan'),.5]]}),
            lambda x:x['strokes'][0].update({'width':-1}),
            lambda x:x['strokes'][0].update({'type':6}),
        ]:
            item=json.loads(json.dumps(obj))
            mutate(item)
            with self.assertRaises(ValueError):
                parse_program(item)

    def test_code_renderer_starts_blank_and_preserves_ink(self):
        prog=parse_program(demo_programs()['tu'])
        frames=list(render_frames(prog))
        self.assertEqual(len(frames),4+sum(s.frames for s in prog.strokes)+4)
        ink=[np.all(f<50,axis=2) for f in frames]
        self.assertFalse(ink[0].any())
        self.assertTrue(ink[-1].any())
        self.assertTrue(all(not (a & ~b).any() for a,b in zip(ink,ink[1:])))

    def test_real_mp4_and_independent_rgb_decode(self):
        prog=parse_program(demo_programs()['shi'])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'result.mp4'
            report=save_mp4(prog,path)
            evidence=audit_mp4(path)
            self.assertEqual(report['frames'],evidence['decoded_frames'])
            self.assertTrue(evidence['blank_first'])
            self.assertGreater(evidence['final_ink_pixels'],500)
            self.assertLess(evidence['max_erased_pixels'],40)
            self.assertFalse(evidence['normative_order_independently_verified'])
            with self.assertRaises(FileExistsError):
                save_mp4(prog,path)

if __name__=='__main__':unittest.main()
