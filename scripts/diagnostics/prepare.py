"""Freeze unexecuted requests and actual input files on CPU. Never runs a model."""
import argparse
import json
from pathlib import Path
import shutil

import numpy as np
from PIL import Image

from .contracts import save,validate_input
from .media import encode,sha256

MODEL_REVISION='7395315758865e6f56ab87ad06a88c7ac172f056'
CODE_REVISION='4baeee086648996f6ab12e673cbe461b0b149997'
NATIVE={'height':480,'width':848,'num_frames':33,'fps':12,'denoising_steps':30,
        'cfg_text_scale':4.0,'use_kv_cache':True,'enhance_prompt':False,'seed':11}


def execution_gate(batch):
    if not batch.get('gpu_authorized'):raise PermissionError('New GPU execution has not been approved')
    if any(batch.get(k) is None or batch[k]<=0 for k in ('max_new_gpu_calls','max_gpu_hours','max_spend')):
        raise ValueError('Finite GPU call/time/spend caps required')
    if batch['max_new_gpu_calls']<len(batch['unique_request_ids']):raise ValueError('Request list exceeds call cap')
    if batch.get('max_technical_retries')!=0:raise ValueError('This frozen pilot has zero technical retries')
    if batch.get('allow_training') or batch.get('allow_download'):raise ValueError('Batch A excludes training and new downloads')
    return True


def prepare(dataset,destination):
    dataset=Path(dataset);destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    rows=[json.loads(s) for s in (dataset/'manifest.jsonl').read_text().splitlines()]
    # Four exposed structural examples; no selection based on new model quality.
    # Resolve IDs from explicit existing catalog rather than assuming character-to-ID positions.
    from hanzi_video.catalog import reference
    groups=['exposed-hanzi-'+reference(c)['reference_id'] for c in ('士','小','广','丑')]
    selected=[]
    for track in ('K-CHAR','K-ORDER','V-STRUCT'):
        selected.extend(sorted([r for r in rows if r['track']==track and r['source_group'] in groups],key=lambda r:r['source_group']))
    for group in groups[:2]:selected.extend(sorted([r for r in rows if r['track']=='H-ACTUAL' and r['source_group']==group],key=lambda r:r['id']))
    cases={'correct','swap','reverse','flash'}
    selected.extend(sorted([r for r in rows if r['track']=='H-ACTUAL' and r['source_group']=='micro-two-lines'
        and json.loads((dataset/r['evaluation']).read_text())['case'] in cases],key=lambda r:r['id']))
    selected.extend(sorted([r for r in rows if r['track']=='G-ATOMIC'],key=lambda r:r['id']))
    requests=[]
    for i,row in enumerate(selected,1):
        payload=validate_input(json.loads((dataset/row['input']).read_text()))
        rid=f'DIAG-A-{i:03}-{row["track"]}-s11'
        directory=destination/rid/'inputs';directory.mkdir(parents=True)
        task='t2v' if row['track']=='G-ATOMIC' else 'x2t_video'
        transform='none'
        if task=='x2t_video':
            if payload['media']:
                source=dataset/Path(row['input']).parent/payload['media'][0]
                if source.suffix=='.mp4':shutil.copyfile(source,directory/'visible.mp4')
                else:
                    image=np.asarray(Image.open(source).convert('RGB'))
                    encode(directory/'visible.mp4',np.repeat(image[None],33,axis=0))
                    transform='same static RGB image repeated 33 times; no claimed motion or interpolation'
            else:
                encode(directory/'visible.mp4',np.full((33,128,128,3),255,np.uint8))
                transform='blank video carrier for text-only knowledge diagnostic; no target image'
            native={'0001':{'interleave_array':['visible.mp4',['Answer only the question from permitted input.',payload['prompt'],'Reference answer withheld.']],
                            'element_dtype_array':['video','text'],'istarget_in_interleave':[0,1]}}
        else:
            # The frozen Lance T2V loader takes id -> literal prompt, unlike X2T.
            native={'0001':payload['prompt']}
        save(directory/(task+'.json'),native)
        files=[{'path':str(p.relative_to(destination/rid)),'bytes':p.stat().st_size,'sha256':sha256(p)} for p in sorted(directory.iterdir())]
        requests.append({'id':rid,'sample_id':row['id'],'source_group':row['source_group'],'track':row['track'],
            'seed':11,'native_task':task,'native_parameters':NATIVE,'status':'unexecuted','geometry_permission':'G0',
            'prompt':payload['prompt'],'input_directory':str(directory),'input_files':files,
            'media_transform':transform,'model_revision':MODEL_REVISION,'code_revision':CODE_REVISION,
            'legacy_ENV_fixture_allowed':False,'scientific_outputs':None})
    batch={'id':'Batch-A-Lance','status':'awaiting_explicit_GPU_authorization','gpu_authorized':False,
           'model_id':'Lance_3B_Video','model_revision':MODEL_REVISION,'code_revision':CODE_REVISION,
           'task_ids':sorted({r['track'] for r in requests}),'unique_request_ids':[r['id'] for r in requests],
           'max_new_gpu_calls':len(requests),'max_technical_retries':0,'max_gpu_hours':2.0,'max_spend':120,
           'spend_currency':'CNY','allow_download':False,'allow_training':False,'wall_timeout':900,
           'data_source':'74-item exposed development benchmark v0.1 plus archived P1 reuse',
           'stop_conditions':['time/spend cap reached','input replaced by fixture','input permission leakage',
                              'systematic media corruption','OOM; preserve and do not automatically retry'],
           'required_artifacts':['actual packed tokens/context','actual read indices and transformed tensors','source RGB and MP4',
                                 'decoded RGB and native PTS','all raw answers','torch/device peaks','wall time and failures','checkpoint/code revisions'],
           'resource_proposal':{'GPU':'1xA100-SXM4-80GB','CPU_cores':16,'RAM_GiB':48,
                                'prior_device_peak_MiB':37283,'prior_peak_is_not_new_task_guarantee':True,
                                'expected_process_hours_range':[.5,1.2],'price_CNY_hour':None,'actual_cost_CNY':None},
           'blockers':['new explicit GPU authorization','available instance and fixed checkpoint cache',
                       'new authorized launcher; old P1 fixed-ID approvals must not be reused']}
    later=[]
    for name,reason,training in [('Batch-A2-Bagel-or-other','new weight/download and environment/resource qualification',False),
                                 ('Batch-B-FIT-SFT','qualified training targets, trainable parameter plan and fit capacity measurement',True),
                                 ('Batch-C-recovery','post-SFT observable errors, explicit recoverable state interface and equal-budget baselines',True)]:
        later.append({'id':name,'status':'blocked_not_execution_ready','gpu_authorized':False,'model_revision':None,
            'task_ids':[],'unique_request_ids':[],'max_new_gpu_calls':None,'max_technical_retries':0,
            'max_gpu_hours':None,'max_spend':None,'allow_download':False,'allow_training':False,
            'training_requested_only_in_future':training,'wall_timeout':None,'data_source':None,
            'stop_conditions':['missing prerequisite or cap'],'required_artifacts':['all attempts, gradients/masks/checkpoints where applicable'],
            'blockers':[reason]})
    plan={'schema':'diagnostic-GPU-proposal-v1','status':'prepared_unexecuted','batch_A':batch,'later_batches':later,
          'requests':requests,'reuse_P1_generation_initial_attempts':64,'new_GPU_calls':0,
          'formal_primary_metrics':None,'training_or_fee_authorized':False}
    save(destination/'manifest.json',plan)
    return plan


def main():
    p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    plan=prepare(a.dataset,a.output);print(json.dumps({'requests':len(plan['requests']),'new_GPU_calls':0,'status':plan['status']}))

if __name__=='__main__':main()
