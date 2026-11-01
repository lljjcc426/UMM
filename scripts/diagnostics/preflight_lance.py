"""Check frozen native arguments and actual video loading on CPU before calls."""
import argparse
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source = root / 'upstream'
    output = root / 'CPU_native_loader_preflight'
    output.mkdir(exist_ok=False)
    os.environ.update(EXP_HW_20250819='False', POSITION_EMBEDDING_3D_VERSION='v2',
        HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
    os.chdir(source)
    sys.path.insert(0, str(source))
    import torch
    from transformers import HfArgumentParser
    from config.config_factory import ModelArguments, DataArguments, InferenceArguments
    from modeling.qwen2 import Qwen2Tokenizer
    from data.data_utils import add_special_tokens
    from data.datasets_custom.validation_dataset import ValidationDataset
    from scripts.env01.run_interfaces import inference_args
    from scripts.p1.native_sampling import install_sampling_trace
    from scripts.diagnostics.contracts import save
    from scripts.diagnostics.execute import validate_authorization

    torch.set_num_threads(2)
    rows = validate_authorization(json.loads((root/'manifest.json').read_text()),
                                  json.loads((root/'authorization.json').read_text()))
    tokenizer, ids, _ = add_special_tokens(Qwen2Tokenizer.from_pretrained(str(source/'downloads/Lance_3B_Video')))
    ids['image_token_id'] = json.loads((source/'downloads/Lance_3B_Video/llm_config.json').read_text())['video_token_id']
    dataset = ValidationDataset(str(root/'inputs'/rows[0]['id']/'x2t_video.json'),
        tokenizer, None, None, None, ids, SimpleNamespace(resolution='video_480p', max_duration=6.0))
    trace = install_sampling_trace(output)
    results = []
    for row in rows:
        native = inference_args(root/'CPU_preflight_bundle',root/'inputs'/row['id'],
            output/row['id'],row['native_task'],row['native_parameters'])
        parsed = HfArgumentParser((ModelArguments,DataArguments,InferenceArguments)).parse_args_into_dataclasses(native)
        item = {'id':row['id'], 'argument_parse_passed':True, 'native_task':parsed[2].task,
                'seed':parsed[2].global_seed}
        if row['native_task']=='x2t_video':
            tensor = dataset.get_video_tensor_online(str(root/'inputs'/row['id']/'visible.mp4'),
                'vit_video',element_dtype='video')
            item.update(trace_id=trace[-1]['trace_id'], shape=list(tensor.shape),
                actual_indices=trace[-1]['indices'], PTS_intervals=trace[-1]['reader_PTS_intervals'],
                finite=bool(torch.isfinite(tensor).all()))
            del tensor
        results.append(item)
        print(json.dumps(item),flush=True)
    result = {'status':'passed', 'requests':24, 'video_inputs':20, 'GPU_initialized':torch.cuda.is_initialized(),
              'scope':'CPU native argument parsing and tokenizer/video-loader paths; model dependency import checked separately',
              'torch_version':torch.__version__, 'items':results}
    if result['GPU_initialized']:
        raise RuntimeError('CPU preflight unexpectedly initialized CUDA')
    save(output/'results.json',result)


if __name__ == '__main__':
    main()
