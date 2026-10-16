"""Evaluate the understanding path of the complete Janus-Pro unified model."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import re
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_REVISION='1daa72fa409002d40931bd7b36a9280362469ead'
MODEL_REVISION='bc299531bae896710f9ea16e7d4d8ea5719290f6'


def run(args):
    sys.path.insert(0,str(args.source.resolve()))
    import torch
    from PIL import Image
    from janus.models import MultiModalityCausalLM, VLChatProcessor

    args.output.mkdir(parents=True,exist_ok=False)
    processor=VLChatProcessor.from_pretrained(str(args.model))
    tokenizer=processor.tokenizer
    model=MultiModalityCausalLM.from_pretrained(str(args.model),torch_dtype=torch.bfloat16,
                                               low_cpu_mem_usage=True).to('mps').eval()
    rows=[json.loads(line) for line in args.inputs.read_text().splitlines()]
    metadata=dict(model_id='deepseek-ai/Janus-Pro-1B',download_source='ModelScope',
                  model_revision=MODEL_REVISION,source_revision=SOURCE_REVISION,
                  condition='frozen_full_UMM_understanding_path_only',dtype='bfloat16',device='mps',
                  input_manifest=str(args.inputs.resolve().relative_to(ROOT)),
                  started_utc=datetime.now(timezone.utc).isoformat(),
                  samples=[r['sample_id'] for r in rows],max_new_tokens=args.max_tokens,
                  do_sample=False,seed=0,declared_context_limit=4096,
                  image_processor_size=processor.image_processor.image_size,
                  image_tokens_per_image=processor.num_image_tokens,
                  model_components=list(dict(model.named_children())),
                  total_parameters=sum(p.numel() for p in model.parameters()),
                  python=platform.python_version(),platform=platform.platform(),
                  hardware=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip(),
                  system_memory_gib=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True))/(1024**3),
                  packages={p:importlib.metadata.version(p) for p in
                            ['torch','torchvision','transformers','timm','accelerate','numpy','Pillow']})
    (args.output/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
    with (args.output/'predictions.jsonl').open('w') as output,torch.inference_mode():
        for index,row in enumerate(rows,1):
            torch.manual_seed(0)
            image_paths=[args.inputs.parent/p for p in row['images']]
            prefix=''.join(f'图{i+1}：<image_placeholder>\n' for i in range(len(image_paths)))
            conversation=[{'role':'<|User|>','content':prefix+row['prompt']},
                          {'role':'<|Assistant|>','content':''}]
            torch.mps.synchronize()
            started=time.perf_counter()
            if image_paths:
                images=[Image.open(p).convert('RGB') for p in image_paths]
                prepared=processor(conversations=conversation,images=images,force_batchify=True).to('mps')
                embeds=model.prepare_inputs_embeds(**prepared)
                mask=prepared.attention_mask
            else:
                prompt=processor.apply_sft_template_for_multi_turn_prompts(
                    conversations=conversation,sft_format=processor.sft_format,
                    system_prompt=processor.system_prompt)
                tokens=tokenizer(prompt,return_tensors='pt').to('mps')
                embeds=model.language_model.get_input_embeddings()(tokens.input_ids)
                mask=tokens.attention_mask
            count=embeds.shape[1]
            if count+args.max_tokens>4096:
                raise ValueError(f'{row["sample_id"]} exceeds the published 4096-token context')
            generated=model.language_model.generate(
                inputs_embeds=embeds,attention_mask=mask,max_new_tokens=args.max_tokens,
                pad_token_id=tokenizer.eos_token_id,bos_token_id=tokenizer.bos_token_id,
                eos_token_id=tokenizer.eos_token_id,do_sample=False,use_cache=True)
            torch.mps.synchronize()
            elapsed=time.perf_counter()-started
            raw=tokenizer.decode(generated[0].cpu().tolist(),skip_special_tokens=True)
            match=re.fullmatch(r'\s*([A-D])[.。]?\s*',raw)
            prediction={'answer':match.group(1)} if match else None
            record=dict(sample_id=row['sample_id'],view=row['view'],raw_response=raw,
                        prediction=prediction,parse_error=None if match else 'Expected one option letter A-D',
                        image_count=len(image_paths),prompt_tokens=count,generation_tokens=generated.shape[1],
                        seconds=elapsed,process_max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                        mps_driver_allocated_bytes_after_response=torch.mps.driver_allocated_memory())
            if match:
                record['selected_text']=row['options']['ABCD'.index(match.group(1))]
            output.write(json.dumps(record,ensure_ascii=False)+'\n');output.flush()
            print(f'{index}/{len(rows)} {row["sample_id"]} {elapsed:.1f}s {raw!r}',flush=True)
            del embeds,mask,generated
            if image_paths:
                del prepared
            torch.mps.empty_cache()
    metadata['finished_utc']=datetime.now(timezone.utc).isoformat()
    (args.output/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'checkpoints/Janus-source')
    p.add_argument('--model',type=Path,default=ROOT/'checkpoints/Janus-Pro-1B')
    p.add_argument('--inputs',type=Path,default=ROOT/'data/h1/umm_pilot_v1/inputs.jsonl')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--max-tokens',type=int,default=64)
    run(p.parse_args())
