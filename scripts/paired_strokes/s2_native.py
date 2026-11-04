"""Private native worker for s2_runner; imports ML libraries only after dispatch.

Keep all three native processor/generation paths visible here. This module has
no download, training, retry or alternative-model path.
"""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import sys
import time
import traceback

from .data import write_json
from .s2 import generated_continuations, native_arguments
from .s2_runner import CONFIG, RunFailure, checkpoint_integrity


def audit_loading(reports, output):
    write_json(output, reports)
    for component, info in reports.items():
        if any(info.get(k) for k in ('missing_keys', 'unexpected_keys', 'mismatched_keys', 'error_msgs')):
            raise RunFailure('loading_keys', f'Unresolved checkpoint loading keys in {component}; see loading.json')


def check_input_contract(family, token_count, pixels, image_tokens, has_image, caps):
    """Effective embedding length includes Ovis's expanded visual atom."""
    if token_count > caps['input_tokens_per_request']:
        raise RunFailure('input_token_cap', f'Effective input tokens {token_count}; no truncation applied')
    if pixels > caps['processed_pixels_per_image']:
        raise RunFailure('image_pixel_cap', f'Native processed image has {pixels} pixels')
    if has_image and (pixels <= 0 or image_tokens <= 0):
        raise RunFailure('image_wiring', f'{family} image tensor or visual token span is missing')
    if not has_image and (pixels or image_tokens):
        raise RunFailure('image_wiring', 'Text-only request unexpectedly contains visual input')


def environment_check(model, output):
    versions = {d.metadata['Name']: d.version for d in importlib.metadata.distributions()}
    write_json(output / 'environment.json', {'python': sys.version, 'packages': versions,
               'offline': {k: os.environ.get(k) for k in ('HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE',
                            'CUDA_VISIBLE_DEVICES', 'HF_HOME', 'HF_MODULES_CACHE')}})
    expected = model['environment']
    if f'{sys.version_info.major}.{sys.version_info.minor}' != expected['python']:
        raise RunFailure('environment_version', 'Python version differs from the approved model environment')
    for package in ('torch', 'torchvision', 'transformers', 'accelerate', 'deepspeed', 'diffusers', 'flash_attn'):
        if package in expected:
            actual = importlib.metadata.version(package)
            wanted = expected[package]
            if (actual if '+' in wanted else actual.split('+')[0]) != wanted:
                raise RunFailure('environment_version', f'{package}={actual}, expected {wanted}')


class NativeModel:
    def __init__(self, model, snapshot, output):
        import torch
        self.torch, self.family, self.model_spec = torch, model['family'], model
        self.output, self.vision_calls = output, 0
        self.active_path = None
        reports = {}
        if self.family == 'internvlu':
            from internvlu import InternVLUPipeline
            from internvlu.vlm import InternVLUChatModel
            from internvlu.diffusion import InternVLUGenerationDecoder
            from internvlu.processing_internvlu import InternVLUProcessor
            from diffusers import AutoencoderKLQwenImage, DPMSolverMultistepScheduler
            components = {}
            for name, cls in (('vlm', InternVLUChatModel), ('generation_decoder', InternVLUGenerationDecoder),
                              ('vae', AutoencoderKLQwenImage)):
                components[name], reports[name] = cls.from_pretrained(
                    str(snapshot / name), torch_dtype=torch.bfloat16, local_files_only=True,
                    use_safetensors=True, output_loading_info=True)
                # Persist each completed component even if the next one fails to load.
                audit_loading(reports, output / 'loading.json')
            components['processor'] = InternVLUProcessor.from_pretrained(str(snapshot / 'processor'))
            components['scheduler'] = DPMSolverMultistepScheduler.from_pretrained(
                str(snapshot / 'scheduler'), local_files_only=True)
            self.pipe = InternVLUPipeline.from_pretrained(str(snapshot), **components, local_files_only=True,
                                                          torch_dtype=torch.bfloat16).to('cuda:0')
            self.model, self.tokenizer = self.pipe.vlm, self.pipe.tokenizer
            self.processor = self.pipe.processor
            self.vision = self.model.vision_model
            self.image_token = self.model.img_context_token_id
        elif self.family == 'ovis_u1':
            from transformers import AutoModelForCausalLM
            self.model, reports['model'] = AutoModelForCausalLM.from_pretrained(
                str(snapshot), torch_dtype=torch.bfloat16, trust_remote_code=True,
                local_files_only=True, use_safetensors=True, output_loading_info=True)
            audit_loading(reports, output / 'loading.json')
            self.model = self.model.eval().to('cuda:0').to(torch.bfloat16)
            self.tokenizer = self.model.get_text_tokenizer()
            self.vision = self.model.get_visual_tokenizer()
            self.processor = self.vision.image_processor
            config_module = importlib.import_module(type(self.model).__module__.rsplit('.', 1)[0] + '.configuration_ovis_u1')
            self.image_token = config_module.IMAGE_ATOM_ID
        else:
            from transformers import AutoProcessor, Qwen3VLForConditionalGeneration
            self.model, reports['model'] = Qwen3VLForConditionalGeneration.from_pretrained(
                str(snapshot), dtype=torch.bfloat16, device_map={'': 'cuda:0'}, attn_implementation='sdpa',
                local_files_only=True, use_safetensors=True, output_loading_info=True)
            audit_loading(reports, output / 'loading.json')
            self.processor = AutoProcessor.from_pretrained(str(snapshot), local_files_only=True)
            self.tokenizer = self.processor.tokenizer
            self.vision = self.model.model.visual
            self.image_token = self.model.config.image_token_id
        self.model.eval()
        # Check once after loading. The checkpoint is never altered or randomly reinitialized here.
        parameter_count = 0
        modules = [self.model] if self.family != 'internvlu' else [self.pipe.vlm, self.pipe.generation_decoder, self.pipe.vae]
        for module in modules:
            for name, parameter in module.named_parameters():
                parameter_count += parameter.numel()
                if parameter.is_meta or not torch.isfinite(parameter).all().item():
                    raise RunFailure('loading_tensor', f'Meta/non-finite parameter: {name}')
        vocabulary = self.tokenizer.get_vocab()
        embeddings = self.model.get_input_embeddings() if self.family != 'ovis_u1' else self.model.get_wte()
        embedding_rows = embeddings.weight.shape[0]
        for token in (self.tokenizer.eos_token_id, self.tokenizer.pad_token_id):
            if not isinstance(token, int) or not 0 <= token < embedding_rows:
                raise RunFailure('tokenizer', 'Invalid EOS/PAD token or embedding vocabulary mismatch')
        if max(vocabulary.values()) >= embedding_rows:
            raise RunFailure('tokenizer', 'Tokenizer vocabulary exceeds checkpoint embeddings')
        if self.family != 'ovis_u1' and (self.image_token is None or self.image_token == self.tokenizer.unk_token_id):
            raise RunFailure('tokenizer', 'Image token is missing or resolves to unknown')
        self.embedding_rows = embedding_rows
        image_processor = self.processor.image_processor if hasattr(self.processor, 'image_processor') else self.processor
        write_json(output / 'loaded_contract.json', {
            'parameter_count': parameter_count, 'loading_keys_resolved': True,
            'state_keys_per_component': {str(i): len(m.state_dict()) for i, m in enumerate(modules)},
            'model_class': type(self.model).__module__ + '.' + type(self.model).__name__,
            'tokenizer_class': type(self.tokenizer).__name__, 'vocabulary_size': len(vocabulary),
            'embedding_rows': embedding_rows, 'eos_id': self.tokenizer.eos_token_id,
            'pad_id': self.tokenizer.pad_token_id, 'image_token_id': self.image_token,
            'processor_class': type(self.processor).__name__,
            'image_processor': image_processor.to_dict(),
            'generation_config': self.model.generation_config.to_dict()})
        self.vision.register_forward_pre_hook(self.capture_vision, with_kwargs=True)

    def capture_vision(self, module, args, kwargs):
        self.vision_calls += 1
        tensors = {'arg_' + str(i): v.detach().cpu() for i, v in enumerate(args) if self.torch.is_tensor(v)}
        tensors.update({k: v.detach().cpu() for k, v in kwargs.items() if self.torch.is_tensor(v)})
        self.torch.save(tensors, self.active_path / 'vision_forward.pt')

    def prepare(self, request, dataset, path, caps):
        torch = self.torch
        args = native_arguments(self.family, request['model_inputs'], dataset)
        has_image = 'image' in request['model_inputs']
        image = None
        if has_image:
            image = (args['image'] if self.family == 'internvlu' else args['images'][0]
                     if self.family == 'ovis_u1' else args['conversation'][0]['content'][0]['image'])
        if self.family == 'internvlu':
            # Same processor call and _generate route as native pipeline.__call__;
            # split here so tensors can be inspected before the first forward.
            original_tokenizer = self.processor.tokenizer
            class CaptureTokenizer:
                def __getattr__(self, name):
                    return getattr(original_tokenizer, name)

                def __call__(self, text, **kwargs):
                    self.text = text
                    return original_tokenizer(text, **kwargs)
            capture = CaptureTokenizer()
            self.processor.tokenizer = capture
            inputs = self.processor(prompt=args['prompt'], image=args['image'], generation_mode='text',
                                    padding=True, return_tensors='pt', height=None, width=None, system_prompt=None)
            self.processor.tokenizer = original_tokenizer
            prompt = capture.text[0] if isinstance(capture.text, list) else capture.text
            pixels = int(inputs['pixel_values'].shape[0] * inputs['pixel_values'].shape[-2] * inputs['pixel_values'].shape[-1]) if has_image else 0
        elif self.family == 'ovis_u1':
            prompt, ids, values, grids = self.model.preprocess_inputs(**args)
            inputs = {'input_ids': ids.unsqueeze(0), 'attention_mask': torch.ne(ids, self.tokenizer.pad_token_id).unsqueeze(0),
                      'pixel_values': values, 'grid_thws': grids}
            pixels = int(grids[:, 1:].prod(dim=1).sum().item()) * self.vision.config.backbone_config.patch_size ** 2 if has_image else 0
        else:
            prompt = self.processor.apply_chat_template(args['conversation'], tokenize=False, add_generation_prompt=True)
            inputs = self.processor.apply_chat_template(**args)
            pixels = int(inputs['image_grid_thw'][:, 1:].prod(dim=1).sum().item()) * self.processor.image_processor.patch_size ** 2 if has_image else 0
        tensor_info = {}
        cpu_tensors = {}
        for name, tensor in inputs.items():
            if torch.is_tensor(tensor):
                cpu_tensors[name] = tensor.detach().cpu()
                finite = bool(torch.isfinite(tensor).all().item())
                tensor_info[name] = {'shape': list(tensor.shape), 'dtype': str(tensor.dtype), 'finite': finite}
        torch.save(cpu_tensors, path / 'native_inputs.pt')
        for name, info in tensor_info.items():
            if not info['finite']:
                raise RunFailure('input_tensor', f'Non-finite native tensor: {name}')
        ids = inputs['input_ids'][0].tolist()
        image_positions = [i for i, value in enumerate(ids) if value == self.image_token]
        visual_tokens = len(image_positions)
        effective = len(ids)
        if self.family == 'ovis_u1' and has_image:
            visual_tokens = int(inputs['grid_thws'].prod(dim=1).sum().item()) // self.vision.config.hidden_stride ** 2
            effective += visual_tokens - len(image_positions)
            if len(image_positions) != 1:
                raise RunFailure('image_wiring', 'Expected one native Ovis visual atom')
        if self.family == 'internvlu' and has_image and visual_tokens != self.processor.image_seq_length:
            raise RunFailure('image_wiring', 'InternVL-U image token span differs from native image_seq_length')
        if self.family == 'qwen3_vl' and has_image:
            expected = int(inputs['image_grid_thw'].prod(dim=1).sum().item()) // self.processor.image_processor.merge_size ** 2
            if visual_tokens != expected:
                raise RunFailure('image_wiring', 'Qwen grid and actual image-token span differ')
        (path / 'formatted_prompt.txt').write_text(prompt)
        write_json(path / 'input.json', {'request': request, 'input_token_ids': ids,
                   'source_RGB_size': list(image.size) if image else None,
                   'effective_input_tokens': effective, 'processed_pixels': pixels,
                   'visual_tokens': visual_tokens, 'image_positions': image_positions,
                   'tensors': tensor_info, 'truncation_applied': False})
        check_input_contract(self.family, effective, pixels, visual_tokens, has_image, caps)
        if any(i >= self.embedding_rows for i in ids) or (self.family != 'ovis_u1' and min(ids) < 0):
            raise RunFailure('tokenizer', 'Input token outside checkpoint embeddings')
        if has_image:
            values = inputs.get('pixel_values')
            if values is None or values.numel() == 0 or values.float().std().item() == 0:
                raise RunFailure('image_wiring', 'Missing or constant native image tensor')
            if not image_positions:
                raise RunFailure('image_wiring', 'Native image placeholder/token span missing')
        for name, tensor in inputs.items():
            if torch.is_tensor(tensor):
                if self.family == 'ovis_u1' and name in ('pixel_values', 'grid_thws'):
                    inputs[name] = tensor.to(device=self.vision.device, dtype=torch.bfloat16 if name == 'pixel_values' else tensor.dtype)
                else:
                    inputs[name] = tensor.to(self.model.device)
        # Save the exact device/dtype conversion used by generate, separately
        # from the processor's original tensors.
        torch.save({k: v.detach().cpu() for k, v in inputs.items() if torch.is_tensor(v)},
                   path / 'model_inputs.pt')
        return inputs

    def generate(self, inputs, path, decoding, has_image):
        torch = self.torch
        self.active_path, self.vision_calls = path, 0
        with torch.inference_mode():
            if self.family == 'internvlu':
                generated = self.pipe._generate(**inputs, **decoding).generate_output
            elif self.family == 'ovis_u1':
                generated = self.model.generate(inputs=inputs['input_ids'],
                    attention_mask=inputs['attention_mask'], pixel_values=inputs['pixel_values'],
                    grid_thws=inputs['grid_thws'], **decoding, eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id, use_cache=True)
            else:
                generated = self.model.generate(**inputs, **decoding)
        torch.cuda.synchronize()
        torch.save(generated.detach().cpu(), path / 'generated_tokens.pt')
        raw_ids = generated.tolist()
        if self.family == 'qwen3_vl' and raw_ids[0][:inputs['input_ids'].shape[1]] != inputs['input_ids'][0].tolist():
            raise RunFailure('output_interface', 'Native Qwen output prefix differs from input IDs')
        continuation = generated_continuations(self.family, raw_ids, [inputs['input_ids'].shape[1]])[0]
        if self.family == 'qwen3_vl':
            output = self.processor.batch_decode([continuation], skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        else:
            output = self.tokenizer.decode(continuation, skip_special_tokens=True)
        (path / 'raw_output.txt').write_text(output)
        write_json(path / 'output.json', {'generated_token_ids': raw_ids, 'continuation_token_ids': continuation,
                   'output': output, 'reached_max_new_tokens': len(continuation) >= decoding['max_new_tokens'],
                   'vision_forward_calls': self.vision_calls})
        if bool(self.vision_calls) != has_image:
            raise RunFailure('image_wiring', 'Actual vision-forward calls do not match image/text-only request')
        if len(continuation) > decoding['max_new_tokens']:
            raise RunFailure('output_token_cap', 'Native output exceeded frozen generation limit')
        if not continuation or not output.strip():
            raise RunFailure('empty_output', 'Native generation returned no usable text')
        return {'output': output, 'generated_tokens': len(continuation),
                'reached_max_new_tokens': len(continuation) >= decoding['max_new_tokens']}


def worker(snapshot, output, key, stream):
    def emit(kind, **fields):
        with (output / 'events.jsonl').open('a') as events:
            events.write(json.dumps({'event': kind, **fields}, ensure_ascii=False) + '\n')
    phase, active = 'load', None
    try:
        config = json.loads(stream.readline())  # Received only from the authorized controller's pipe.
        app, model = config['application'], config['model']
        os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:app['resource_caps']['cpu_cores']])
        spec = json.loads((CONFIG / 's2_checkpoint_files.json').read_text())['models'][key]
        checkpoint_integrity(snapshot, spec, output / 'checkpoint_integrity.json')
        for entry in spec['files']:
            if not entry['path'].endswith('.safetensors'):
                target = output / 'snapshot_metadata' / entry['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((snapshot / entry['path']).read_bytes())
        environment_check(model, output)
        import torch
        import numpy as np
        torch.set_num_threads(app['resource_caps']['cpu_cores'])
        torch.manual_seed(app['seed'])
        random.seed(app['seed'])
        np.random.seed(app['seed'])
        torch.cuda.manual_seed_all(app['seed'])
        load_started = time.monotonic()
        emit('load_started')
        native = NativeModel(model, snapshot, output)
        write_json(output / 'load_resources.json', {'native_load_seconds': time.monotonic() - load_started,
                   'torch_peak_allocated_bytes': torch.cuda.max_memory_allocated(),
                   'torch_peak_reserved_bytes': torch.cuda.max_memory_reserved(),
                   'cuda': torch.version.cuda, 'device_name': torch.cuda.get_device_name(0)})
        emit('ready')
        for line in stream:
            request = json.loads(line)
            if request.get('stop'):
                break
            active, phase = request['id'], 'preprocessing'
            path = output / 'requests' / active
            path.mkdir(parents=True)
            began = time.monotonic()
            torch.cuda.reset_peak_memory_stats()
            inputs = native.prepare(request, output / 'inputs', path, app['resource_caps'])
            phase = 'generation'
            emit('generation_started', id=active)
            result = native.generate(inputs, path, app['decoding'], 'image' in request['model_inputs'])
            result.update(seconds=time.monotonic() - began,
                          torch_peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                          torch_peak_reserved_bytes=torch.cuda.max_memory_reserved())
            write_json(path / 'result.json', result)
            emit('result', id=active, result=result)
    except Exception as error:
        if isinstance(error, RunFailure):
            kind = error.kind
        elif 'out of memory' in str(error).lower():
            kind = 'oom'
        else:
            kind = phase + '_exception'
        (output / 'worker_error.log').write_text(traceback.format_exc())
        emit('failure', id=active, failure_type=kind, message=str(error))
        raise


if __name__ == '__main__':
    if len(sys.argv) != 5 or sys.argv[1] != '--worker' or sys.stdin.isatty():
        raise SystemExit('Use scripts.paired_strokes.s2_runner with explicit authorization')
    worker(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.stdin)
