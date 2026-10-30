"""One authorized frozen Wan VAE round trip with actual Lance loader evidence."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import traceback
from types import SimpleNamespace

from full_common import sha256
from native_sampling import install_sampling_trace


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True);parser.add_argument('--id',required=True)
    args=parser.parse_args();root=args.root.resolve()
    row=next(r for r in json.loads((root/'manifest.json').read_text())['codec'] if r['id']==args.id)
    out=root/'codec'/args.id;out.mkdir(parents=True,exist_ok=False)
    result=dict(id=args.id,completed=False,model_call_started=False,seed=row['seed'])
    started=time.perf_counter();monitor=None;gpu_log=None
    try:
        source=root/row['input_file']
        assert sha256(source)==row['input_sha256'], 'Frozen codec source changed'
        upstream=next((root/'bundles').glob('*/upstream')).resolve()
        os.chdir(upstream);sys.path.insert(0,str(upstream))
        os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',EXP_HW_20250819='False',POSITION_EMBEDDING_3D_VERSION='v2')
        import numpy as np
        import torch
        import imageio.v2 as imageio
        from modeling.qwen2 import Qwen2Tokenizer
        from data.data_utils import add_special_tokens
        from data.datasets_custom.validation_dataset import ValidationDataset
        from modeling.vae.wan.model import WanVideoVAE
        tokenizer=Qwen2Tokenizer.from_pretrained(str(upstream/'downloads/Lance_3B_Video'))
        tokenizer,token_ids,_=add_special_tokens(tokenizer)
        token_ids['image_token_id']=json.loads((upstream/'downloads/Lance_3B_Video/llm_config.json').read_text())['video_token_id']
        # The actual native constructor installs its own sampler and transforms.
        prompt=root/'bundles/N076-T_G0_native_simple-s47/inputs/t2v.json'
        dataset=ValidationDataset(str(prompt),tokenizer,None,None,None,token_ids,
                                  SimpleNamespace(resolution='video_480p',max_duration=6.0))
        install_sampling_trace(out)
        tensor=dataset.get_video_tensor_online(str(source),'vae_video',element_dtype='video')
        probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_frames','-of','json',str(source)],
                             capture_output=True,text=True,check=True)
        (out/'input_ffprobe.json').write_text(probe.stdout)
        save(out/'loader_configuration.json',dict(constructor='ValidationDataset native __init__',resolution='video_480p',
            max_duration=6.0,vision_stream='vae_video',element_dtype='video',input_sha256=row['input_sha256'],
            temporal_mapping='Reconstruction frame j maps to actual_sampling.indices[j]; latent stride4, receptive fields overlap; no physical timing claim'))
        torch.manual_seed(row['seed']);torch.cuda.manual_seed_all(row['seed']);torch.cuda.set_device(0)
        torch.cuda.reset_peak_memory_stats()
        gpu_log=(out/'gpu_samples.csv').open('w')
        monitor=subprocess.Popen(['nvidia-smi','-i','0','--query-gpu=timestamp,memory.used,memory.total,utilization.gpu',
                                  '--format=csv,noheader,nounits','-l','1'],stdout=gpu_log,stderr=subprocess.STDOUT)
        result['model_call_started']=True;save(out/'result.json',result)
        vae=WanVideoVAE(device='cuda',dtype=torch.bfloat16)
        vae.vae.model.eval().requires_grad_(False)
        with torch.no_grad():
            latent=vae.vae_encode([tensor])[0]
            reconstructed=vae.vae_decode([latent])[0]
        torch.cuda.synchronize()
        np.savez_compressed(out/'latent_float32.npz',latent=latent.detach().cpu().float().numpy())
        frames=((reconstructed.float().clamp(-1,1)+1)*127.5).byte().permute(1,2,3,0).cpu().numpy()
        np.savez_compressed(out/'reconstructed_RGB_uint8.npz',frames=frames)
        imageio.mimsave(str(out/'reconstruction.mp4'),frames,fps=12,macro_block_size=1)
        native=((tensor.float()+1)*127.5).byte().permute(1,2,3,0).numpy()
        assert frames.shape==native.shape, 'Roundtrip changed temporal/spatial shape'
        trace=json.loads((out/'actual_sampling.json').read_text())[0]
        save(out/'reconstruction_time_mapping.json',dict(frame_count=len(frames),
            actual_read_indices=trace['indices'],source_PTS_intervals=trace['reader_PTS_intervals'],
            reconstruction_nominal_PTS=[i/12 for i in range(len(frames))],
            note='Frame-aligned codec comparison, not independent human event gold'))
        result.update(completed=True,input_shape=list(tensor.shape),latent_shape=list(latent.shape),
            reconstructed_shape=list(frames.shape),use_sample=vae.use_sample,
            mean_absolute_difference=float(np.abs(native.astype(np.int16)-frames.astype(np.int16)).mean()),
            cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated(),cuda_peak_reserved_bytes=torch.cuda.max_memory_reserved(),
            source_sha256=sha256(source),reconstruction_sha256=sha256(out/'reconstruction.mp4'),
            raw_RGB_sha256=sha256(out/'reconstructed_RGB_uint8.npz'))
    except BaseException:
        result['error']=traceback.format_exc();print(result['error'],flush=True)
    finally:
        if monitor is not None:monitor.terminate();monitor.wait();gpu_log.close()
        result.update(wall_seconds=time.perf_counter()-started,host_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
        save(out/'result.json',result)
    return 0 if result['completed'] else 1


if __name__=='__main__':raise SystemExit(main())
