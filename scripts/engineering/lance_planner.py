"""Real pinned Lance adapter. Requires a separately authorized CUDA runtime.

Never invoked by CPU preview. No fake answers, API services, or downloads.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys
import time


def native_args(model, vit, dataset, output):
    fixed = {'model_path': str(model), 'vit_path': str(vit), 'vit_type': 'qwen_2_5_vl_original',
        'llm_qk_norm': 'true', 'llm_qk_norm_und': 'true', 'llm_qk_norm_gen': 'true',
        'tie_word_embeddings': 'false', 'copy_init_moe': 'true', 'max_num_frames': 121,
        'max_latent_size': 64, 'visual_und': 'true', 'visual_gen': 'true', 'vae_model_type': 'wan',
        'apply_qwen_2_5_vl_pos_emb': 'true', 'apply_chat_template': 'false', 'cfg_type': 0,
        'global_seed': 11, 'validation_data_seed': 11, 'video_height': 512, 'video_width': 512,
        'num_frames': 1, 'task': 'x2t_image', 'save_path_gen': str(output),
        'resolution': 'image_512res', 'text_template': 'true', 'use_KVcache': 'true',
        'enhance_prompt': 'false', 'val_dataset_config_file': str(dataset)}
    return [part for key, value in fixed.items() for part in ('--' + key, str(value))] + ['--latent_patch_size', '1', '1', '1']


def prepare_input(payload, folder):
    from PIL import Image
    image = Path(payload['image']) if payload.get('image') else folder / 'blank.png'
    if not payload.get('image'):
        Image.new('RGB', (512, 512), 'white').save(image)
    dataset = folder / 'native_input.json'
    dataset.write_text(json.dumps({'engineering-request': {
        'interleave_array': [str(image.resolve()), ['Follow the user instructions.', payload['prompt'], 'UNUSED_TARGET_PLACEHOLDER']],
        'element_dtype_array': ['image', 'text'], 'istarget_in_interleave': [0, 1]}}, ensure_ascii=False, indent=2))
    return dataset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('upstream', 'model', 'vit', 'request', 'response'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    args.request, args.response = args.request.resolve(), args.response.resolve()
    args.upstream, args.model, args.vit = args.upstream.resolve(), args.model.resolve(), args.vit.resolve()
    payload = json.loads(args.request.read_text())
    folder = args.response.resolve().parent
    dataset = prepare_input(payload, folder)
    started = time.perf_counter()
    os.chdir(args.upstream)
    sys.path.insert(0, str(args.upstream))
    import torch
    from modeling.lance import Lance
    native = Lance.validation_und_KVcache

    def traced(model, *call_args, **kwargs):
        packed = kwargs['val_packed_text_ids'].detach().cpu()
        indexes = kwargs['val_ce_loss_indexes'].detach().cpu()
        context = packed[:int(indexes[0])+1] if len(indexes) else packed
        decoded = kwargs['tokenizer'].decode(context)
        tokens = kwargs['val_packed_vit_tokens']
        visual_elements = sum(t.numel() for t in tokens) if isinstance(tokens, list) else tokens.numel()
        actual = {'conditioning_text': decoded, 'conditioning_ids': context.tolist(),
                  'visual_elements': visual_elements, 'ce_indexes': indexes.tolist(),
                  'request_prompt_present': payload['prompt'] in decoded,
                  'target_placeholder_withheld': 'UNUSED_TARGET_PLACEHOLDER' not in decoded}
        (folder / 'actual_input.json').write_text(json.dumps(actual, ensure_ascii=False, indent=2))
        if not actual['request_prompt_present'] or not visual_elements or not actual['target_placeholder_withheld']:
            raise ValueError('Actual input prompt/image missing or target placeholder leaked into context')
        return native(model, *call_args, **kwargs)

    Lance.validation_und_KVcache = traced
    spec = importlib.util.spec_from_file_location('engineering_native_lance', args.upstream / 'inference_lance.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.MAX_GENERATION_LENGTH = 512
    argv = native_args(args.model, args.vit, dataset, folder / 'native_output')
    (folder / 'runtime.json').write_text(json.dumps({'argv': argv,
        'upstream_revision_expected': '4baeee086648996f6ab12e673cbe461b0b149997',
        'weights_revision_expected': '7395315758865e6f56ab87ad06a88c7ac172f056',
        'max_output_tokens': 512, 'inference_only': True,
        'image_understanding_on_video_checkpoint': 'requires_live_validation'}, indent=2))
    sys.argv = [str(args.upstream / 'inference_lance.py'), *argv]
    torch.cuda.reset_peak_memory_stats()
    try:
        module.main()
        rows = json.loads((folder / 'native_output' / 'result.json').read_text())
        if len(rows) != 1:
            raise ValueError('Expected one native understanding answer')
        args.response.write_text(json.dumps({'answer': rows[0]['answer'], 'model': 'Lance_3B_Video'}, ensure_ascii=False))
    finally:
        (folder / 'resources.json').write_text(json.dumps({
            'elapsed_seconds': time.perf_counter()-started,
            'peak_allocated_bytes': torch.cuda.max_memory_allocated(),
            'peak_reserved_bytes': torch.cuda.max_memory_reserved()}, indent=2))


if __name__ == '__main__':
    main()
