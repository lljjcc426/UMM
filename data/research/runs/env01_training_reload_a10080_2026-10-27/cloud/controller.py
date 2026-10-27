"""Run the approved ENV-01 stages sequentially and retain each exit status."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',type=Path,required=True)
parser.add_argument('--bundle',type=Path,required=True)
parser.add_argument('--attempt',required=True)
parser.add_argument('--stages',nargs='+',default=['audit','train','resume'])
args=parser.parse_args()
run=args.root/args.attempt
env=os.environ.copy()
env.update(PATH=str(args.bundle/'runtime/bin')+':/usr/local/cuda-12.4/bin:'+env['PATH'],
           CUDA_HOME='/usr/local/cuda-12.4',CUDA_VISIBLE_DEVICES='0',EXP_HW_20250819='False',
           POSITION_EMBEDDING_3D_VERSION='v2',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
           WANDB_MODE='disabled',PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='4')
state={'status':'running','started_at_utc':datetime.now(timezone.utc).isoformat(),'stages':[]}
def save():
    (run/'controller.json').write_text(json.dumps(state,indent=2)+'\n')
save()
for stage in args.stages:
    cmd=[str(args.bundle/'runtime/bin/python'),str(args.root/'train_reload.py'),'--bundle',str(args.bundle),'--run',str(run),'--stage',stage]
    row={'stage':stage,'command':cmd,'status':'running','started_at_utc':datetime.now(timezone.utc).isoformat()}
    state['stages'].append(row);save()
    start=time.perf_counter()
    with (run/f'{stage}.log').open('w') as output,(run/f'{stage}_gpu_samples.csv').open('w') as gpu:
        monitor=subprocess.Popen(['nvidia-smi','--query-gpu=timestamp,memory.used,utilization.gpu','--format=csv,noheader,nounits','-l','1'],stdout=gpu,stderr=subprocess.STDOUT)
        try:
            result=subprocess.run(cmd,stdout=output,stderr=subprocess.STDOUT,env=env)
            row['exit_code']=result.returncode
        finally:
            monitor.terminate();monitor.wait()
    row.update(status='passed' if result.returncode==0 else 'failed',wall_seconds=time.perf_counter()-start)
    save()
    if result.returncode:
        state['status']='failed';break
else:
    state['status']='passed'
state['finished_at_utc']=datetime.now(timezone.utc).isoformat();save()
