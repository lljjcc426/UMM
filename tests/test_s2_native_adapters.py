"""Exercise native API wiring with CPU tensors and processor doubles.

These doubles do not implement a tokenizer, vision processor, weights or model.
Actual native loading remains a required GPU-environment preflight.
"""
from contextlib import nullcontext
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np

from scripts.paired_strokes.s2 import DECODING
from scripts.paired_strokes.s2_native import NativeModel
from scripts.paired_strokes.s2_runner import RunFailure
from tests.test_s2_runner import CAPS, REQUESTS, runner


class Tensor(np.ndarray):
    def __new__(cls, data):
        return np.asarray(data).view(cls)

    def to(self, device=None, dtype=None):
        return self.astype(dtype) if dtype else self

    def detach(self):
        return self

    def cpu(self):
        return self

    def float(self):
        return self.astype(np.float32)

    def numel(self):
        return self.size

    def unsqueeze(self, dim):
        return np.expand_dims(self, dim)

    def prod(self, dim=None):
        return Tensor(np.prod(np.asarray(self), axis=dim))


class TorchDouble:
    bfloat16 = np.float32
    cuda = SimpleNamespace(synchronize=lambda: None)

    def __init__(self):
        self.saved = {}

    def save(self, obj, path):
        self.saved[path.name] = obj
        path.write_text('CPU tensor double; not a native tensor artifact')

    is_tensor = staticmethod(lambda value: isinstance(value, Tensor))
    isfinite = staticmethod(lambda value: Tensor(np.isfinite(value)))
    ne = staticmethod(lambda left, right: Tensor(left != right))
    inference_mode = staticmethod(nullcontext)


class TokenizerDouble:
    pad_token_id, eos_token_id = 0, 2

    def __init__(self, inputs):
        self.inputs = inputs

    def __call__(self, text, **kwargs):
        return self.inputs

    def decode(self, ids, **kwargs):
        return '{"answer":"unknown"}\n'


class ProcessorDouble:
    def __init__(self, inputs):
        self.tokenizer = TokenizerDouble(inputs)
        self.image_seq_length = 256
        self.image_processor = SimpleNamespace(patch_size=16, merge_size=2)
        self.inputs = inputs

    def __call__(self, **kwargs):
        self.last_kwargs = kwargs
        self.tokenizer(['exact native rendered prompt'], return_tensors='pt')
        return self.inputs.copy()

    def apply_chat_template(self, *args, **kwargs):
        self.last_kwargs = kwargs
        return 'exact native rendered prompt' if kwargs.get('tokenize') is False else self.inputs.copy()

    def batch_decode(self, ids, **kwargs):
        self.decoded_ids = ids
        return ['{"answer":"unknown"}\n']


class NativeAdapterTest(unittest.TestCase):
    def native(self, family, image=True):
        native = NativeModel.__new__(NativeModel)
        native.family, native.torch = family, TorchDouble()
        native.image_token, native.embedding_rows = (-2 if family == 'ovis_u1' else 99), 1024
        span = 256 if family == 'internvlu' else 64
        ids = [1] + ([99] * span if image else []) + [2]
        values = Tensor(np.arange(3 * 448 * 448).reshape(1, 3, 448, 448) % 255)
        inputs = {'input_ids': Tensor([ids]), 'attention_mask': Tensor([[1] * len(ids)])}
        if image:
            inputs['pixel_values'] = values
            if family == 'qwen3_vl':
                inputs['image_grid_thw'] = Tensor([[1, 16, 16]])
        native.processor = ProcessorDouble(inputs)
        native.tokenizer = native.processor.tokenizer
        native.model = SimpleNamespace(device='cpu')
        native.vision = SimpleNamespace(device='cpu', config=SimpleNamespace(
            backbone_config=SimpleNamespace(patch_size=14), hidden_stride=2))
        if family == 'ovis_u1':
            ovis_ids = Tensor([1, -1, -2, -3, 2] if image else [1, 2])
            def preprocess(**kwargs):
                self.assertTrue(kwargs['propagate_exception'])
                self.assertFalse(kwargs['enable_thinking'])
                return 'exact native rendered prompt', ovis_ids, values if image else None, Tensor([[1, 32, 32]]) if image else None
            native.model.preprocess_inputs = preprocess
        return native

    def test_each_image_adapter_preserves_native_tokens_and_tensor_inputs(self):
        for family, expected_tokens, expected_pixels in [('internvlu', 256, 200704),
                                                        ('ovis_u1', 256, 200704),
                                                        ('qwen3_vl', 64, 65536)]:
            with self.subTest(family=family), tempfile.TemporaryDirectory() as tmp:
                native, path = self.native(family), Path(tmp)
                inputs = native.prepare(REQUESTS[0], runner.DATA, path, CAPS)
                record = json.loads((path / 'input.json').read_text())
                self.assertEqual(record['visual_tokens'], expected_tokens)
                self.assertEqual(record['processed_pixels'], expected_pixels)
                self.assertEqual(record['source_RGB_size'], [256, 256])
                self.assertEqual((path / 'formatted_prompt.txt').read_text(), 'exact native rendered prompt')
                self.assertIn('pixel_values', native.torch.saved['model_inputs.pt'])
                self.assertIs(inputs['pixel_values'], native.torch.saved['model_inputs.pt']['pixel_values'])
                if family == 'ovis_u1':
                    self.assertEqual(record['effective_input_tokens'], 260)
                if family != 'ovis_u1':
                    native.processor.inputs['pixel_values'] = Tensor([[[[np.nan]]]])
                    failed = path / 'nonfinite'
                    failed.mkdir()
                    with self.assertRaises(RunFailure) as caught:
                        native.prepare(REQUESTS[0], runner.DATA, failed, CAPS)
                    self.assertEqual(caught.exception.kind, 'input_tensor')
                    self.assertTrue((failed / 'native_inputs.pt').exists())

    def test_each_text_only_adapter_keeps_visual_input_absent(self):
        for family in ('internvlu', 'ovis_u1', 'qwen3_vl'):
            with self.subTest(family=family), tempfile.TemporaryDirectory() as tmp:
                native, path = self.native(family, image=False), Path(tmp)
                native.prepare(REQUESTS[-1], runner.DATA, path, CAPS)
                record = json.loads((path / 'input.json').read_text())
                self.assertEqual((record['processed_pixels'], record['visual_tokens']), (0, 0))
                self.assertIsNone(record['source_RGB_size'])

    def test_native_output_prefix_rules_and_exact_decoding(self):
        for family in ('internvlu', 'ovis_u1', 'qwen3_vl'):
            with self.subTest(family=family), tempfile.TemporaryDirectory() as tmp:
                native, path = self.native(family), Path(tmp)
                inputs = {'input_ids': Tensor([[1, 99, 2]])}
                if family == 'ovis_u1':
                    inputs.update(attention_mask=Tensor([[1, 1, 1]]), pixel_values=None, grid_thws=None)
                captured = {}
                def generate(inputs=None, **kwargs):
                    if family == 'ovis_u1':
                        self.assertIsNotNone(inputs)  # Native Ovis uses `inputs`, not `input_ids`.
                        self.assertNotIn('input_ids', kwargs)
                    captured.update(kwargs)
                    native.vision_calls += 1
                    ids = [10, 11, 2]
                    return Tensor([[1, 99, 2] + ids] if family == 'qwen3_vl' else [ids])
                native.model.generate = generate
                native.pipe = SimpleNamespace(_generate=lambda **kwargs: SimpleNamespace(generate_output=generate(**kwargs)))
                result = native.generate(inputs, path, DECODING, True)
                output = json.loads((path / 'output.json').read_text())
                self.assertEqual(output['continuation_token_ids'], [10, 11, 2])
                self.assertEqual(result['output'], '{"answer":"unknown"}\n')
                for key, value in DECODING.items():
                    self.assertEqual(captured[key], value)

    def test_missing_actual_vision_forward_is_interface_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            native, path = self.native('qwen3_vl'), Path(tmp)
            native.model.generate = lambda **kwargs: Tensor([[1, 99, 2, 10]])
            with self.assertRaises(RunFailure) as caught:
                native.generate({'input_ids': Tensor([[1, 99, 2]])}, path, DECODING, True)
            self.assertEqual(caught.exception.kind, 'image_wiring')
            self.assertTrue((path / 'raw_output.txt').exists())


if __name__ == '__main__':
    unittest.main()
