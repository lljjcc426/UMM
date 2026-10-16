"""Run frozen local MLX VLM inference on H1 inputs, without reading labels."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = 'mlx-community/Qwen3-VL-2B-Instruct-4bit'
MODEL_REVISION = '9c4f5209e57b31f4b9dfba735de3fb983739c9cc'
MIRROR_REVISION = 'f338871b6a559fe9dc10ea3cf041da8abaff3c50'


def parse_response(text):
    text = text.strip()
    if text.startswith('```') and text.endswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object')
    return value


def run(args):
    import mlx.core as mx
    from mlx_vlm import load, generate
    from mlx_vlm.prompt_utils import apply_chat_template
    from mlx_vlm.utils import load_config

    # An exclusive new output directory keeps earlier attempts intact.
    args.output.mkdir(parents=True, exist_ok=False)
    args.inputs = args.inputs.resolve()
    inputs = [json.loads(line) for line in args.inputs.read_text().splitlines()]
    if args.sample:
        inputs = [r for r in inputs if r['sample_id'] in args.sample]
    config = load_config(str(args.model))
    model, processor = load(str(args.model))
    metadata = dict(model_id=MODEL_ID, model_revision=MODEL_REVISION,
                    download_source='ModelScope', download_revision=MIRROR_REVISION,
                    condition='frozen_4bit_local_vlm_multi_image_no_training',
                    started_utc=datetime.now(timezone.utc).isoformat(),
                    input_manifest=str(args.inputs.relative_to(ROOT)),
                    samples=[r['sample_id'] for r in inputs], max_tokens=args.max_tokens,
                    temperature=0.0, seed=0, image_size=[224, 224],
                    input_layout='image roles and chronological order specified in each input prompt',
                    python=platform.python_version(), platform=platform.platform(),
                    hardware=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'], text=True).strip(),
                    system_memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'], text=True)),
                    preprocessor_config=json.loads((args.model/'preprocessor_config.json').read_text()),
                    runtime_image_processor=dict(
                        class_name=type(processor.image_processor).__name__,
                        **{k: getattr(processor.image_processor, k) for k in
                           ['min_pixels','max_pixels','patch_size','merge_size','temporal_patch_size']}),
                    packages={p: importlib.metadata.version(p) for p in
                              ['mlx-vlm','mlx','transformers','numpy','Pillow']})
    (args.output/'run.json').write_text(json.dumps(metadata, indent=2)+'\n')
    with (args.output/'predictions.jsonl').open('w') as out:
        for index, row in enumerate(inputs, 1):
            mx.random.seed(0)
            images = [str(args.inputs.parent/p) for p in row['images']]
            prompt = apply_chat_template(processor, config, row['prompt'], num_images=len(images))
            start = time.perf_counter()
            result = generate(model, processor, prompt, image=images or None,
                              max_tokens=args.max_tokens, temperature=0.0, verbose=False)
            elapsed = time.perf_counter()-start
            raw = result.text if hasattr(result, 'text') else str(result)
            record = dict(sample_id=row['sample_id'], view=row['view'], raw_response=raw,
                          seconds=elapsed, image_count=len(images))
            for name in ['prompt_tokens','generation_tokens','peak_memory']:
                if hasattr(result, name):
                    record[name] = getattr(result, name)
            if row.get('response_format') == 'text':
                record.update(prediction=raw.strip(), parse_error=None, response_format='text')
            else:
                try:
                    record['prediction'] = parse_response(raw)
                    record['parse_error'] = None
                except (ValueError, json.JSONDecodeError) as exc:
                    record.update(prediction=None, parse_error=str(exc))
            out.write(json.dumps(record, ensure_ascii=False)+'\n')
            out.flush()
            print(f'{index}/{len(inputs)} {row["sample_id"]} {elapsed:.1f}s '
                  f'output_ok={record["parse_error"] is None}', flush=True)
            mx.clear_cache()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model', type=Path, default=ROOT/'checkpoints/Qwen3-VL-2B-Instruct-4bit')
    p.add_argument('--inputs', type=Path, default=ROOT/'data/h1/pilot_v1/inputs.jsonl')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--sample', action='append', help='Optional exact sample ID; may repeat')
    p.add_argument('--max-tokens', type=int, default=512)
    run(p.parse_args())
