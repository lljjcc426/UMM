"""CPU replay of native packing against recorded generation-entry tokens."""
import argparse
import json
import os
from pathlib import Path
import random
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();root=args.root.resolve()
    upstream=next((root/'bundles').glob('*/upstream')).resolve();os.chdir(upstream);sys.path.insert(0,str(upstream))
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',EXP_HW_20250819='False',POSITION_EMBEDDING_3D_VERSION='v2')
    import torch
    import numpy as np
    from data.dataset_base import DataConfig
    from data.datasets_custom.validation_dataset import ValidationDataset
    from data.data_utils import add_special_tokens
    from modeling.qwen2 import Qwen2Tokenizer
    torch.set_num_threads(2)
    tokenizer,token_ids,_=add_special_tokens(Qwen2Tokenizer.from_pretrained(str(upstream/'downloads/Lance_3B_Video')))
    token_ids['image_token_id']=json.loads((upstream/'downloads/Lance_3B_Video/llm_config.json').read_text())['video_token_id']
    manifest=json.loads((root/'manifest.json').read_text());state=json.loads((root/'state.json').read_text());results=[]
    for row in manifest['generation']:
        entry=next(e for e in state['generation'] if e['id']==row['id'])
        if entry['status']!='completed':continue
        origin=Path('/root/umm-p1-issue3-native-20261030') if row['reused'] else root
        bundle=origin/'bundles'/row['id'];run=next((bundle/'runs').iterdir());input_path=run/'inputs'/(row['task']+'.json')
        actual=json.loads((run/row['task']/'actual_generation_input.json').read_text())
        cfg=DataConfig.from_yaml(str(input_path))
        for k,v in dict(resolution='video_480p',text_template=True,enhance_prompt=False,num_frames=33,H=480,W=848,
                        task=row['task'],latent_patch_size=[1,1,1],vae_downsample=(4,16,16),max_latent_size=64,max_num_frames=121).items():setattr(cfg,k,v)
        random.seed(row['seed']);np.random.seed(row['seed']);torch.manual_seed(row['seed'])
        dataset=ValidationDataset(str(input_path),tokenizer,None,None,None,token_ids,cfg);sample=dataset[0]
        ids=sample['packed_text_ids'].tolist();noise=sample['attn_modes'].index('noise');start=sum(sample['split_lens'][:noise])
        prepared=json.loads(input_path.read_text())['0001'];prompt=prepared if isinstance(prepared,str) else prepared['interleave_array'][0]
        conditional=sample['sample_modality']==0
        record=dict(id=row['id'],CPU_only=True,actual_packed_ids_equal_CPU_replay=ids==actual['packed_text_ids'],
            prompt_in_actual_packed_ids=prompt in tokenizer.decode(actual['packed_text_ids']),
            prompt_precedes_first_noise_block=prompt in tokenizer.decode(ids[:start]),
            CFG_text_token_count=int(conditional.sum()),CFG_text_decoded=tokenizer.decode(sample['packed_text_ids'][conditional].tolist()),
            prefix_token_count=start,attn_modes=sample['attn_modes'],split_lens=sample['split_lens'],
            model_forward_not_reexecuted=True)
        results.append(record)
    result=dict(audited=len(results),all_packed_inputs_match=all(r['actual_packed_ids_equal_CPU_replay'] for r in results),
                all_prompts_before_noise=all(r['prompt_precedes_first_noise_block'] for r in results),records=results,
                limitation='CPU reconstruction verifies the data/packing path; it does not prove conditional KV features influenced denoising')
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'}))


if __name__=='__main__':main()
