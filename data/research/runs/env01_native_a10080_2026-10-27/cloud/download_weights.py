import json, sys, time, traceback
from pathlib import Path
from huggingface_hub import snapshot_download, constants
constants.HF_TRANSFER_CONCURRENCY = 8
bundle=Path(sys.argv[1])
plan=json.loads((bundle/'plan.json').read_text())
started=time.monotonic()
result={'repository':plan['weight_repository'],'revision':plan['weight_revision'],'status':'failed'}
try:
 snapshot_download(repo_id=plan['weight_repository'],revision=plan['weight_revision'],allow_patterns=plan['weight_patterns'],local_dir=bundle/'upstream/downloads',max_workers=2)
 result['status']='download_completed'
except BaseException as e:
 result['error']=str(e);result['traceback']=traceback.format_exc();traceback.print_exc()
finally:
 result['elapsed_seconds']=time.monotonic()-started
 (bundle.parent/'weight-download-status.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['status']=='download_completed' else 1)
