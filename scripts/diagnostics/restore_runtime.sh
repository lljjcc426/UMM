#!/usr/bin/env bash
# Restore the approved fixed checkpoint in this task's own environment only.
set -Eeuo pipefail
TASK_ROOT="${1:?Supply the independent Batch A directory}"
python3 - "$TASK_ROOT" <<'PY'
import json,sys
from pathlib import Path
root=Path(sys.argv[1])
approval=json.loads((root/'checkpoint_restore_approval.json').read_text())
if not approval['approved'] or approval['model_revision']!='7395315758865e6f56ab87ad06a88c7ac172f056':
    raise SystemExit('Missing fixed-checkpoint restoration approval')
PY
SETUP_DIR="$TASK_ROOT/setup/$(date -u +%Y%m%dT%H%M%S)-$$"
mkdir -p "$SETUP_DIR" "$TASK_ROOT/cache/conda" "$TASK_ROOT/cache/pip"
exec > >(tee "$SETUP_DIR/setup.log") 2>&1
export CONDA_PKGS_DIRS="$TASK_ROOT/cache/conda"
export PIP_CACHE_DIR="$TASK_ROOT/cache/pip"
export CUDA_HOME=/usr/local/cuda-12.4
export MAX_JOBS=2
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
export MKL_NUM_THREADS=2
if [[ ! -x "$TASK_ROOT/runtime/bin/python" ]]; then
    /home/vipuser/miniconda3/bin/conda create -y -p "$TASK_ROOT/runtime" python=3.11.18 pip
fi
PYTHON="$TASK_ROOT/runtime/bin/python"
export PATH="$TASK_ROOT/runtime/bin:$CUDA_HOME/bin:$PATH"
"$PYTHON" -m pip install --upgrade pip setuptools wheel ninja packaging psutil
"$PYTHON" -m pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
"$PYTHON" -m pip install -r "$TASK_ROOT/upstream/requirements.txt" wandb==0.19.11 scipy==1.15.3
"$PYTHON" -m pip install flash-attn==2.6.3 --no-build-isolation
"$PYTHON" -m pip freeze --all > "$SETUP_DIR/pip-freeze.txt"
"$PYTHON" - "$TASK_ROOT" <<'PY'
import json,sys
from pathlib import Path
from huggingface_hub import snapshot_download
root=Path(sys.argv[1])
snapshot_download(repo_id='bytedance-research/Lance',revision='7395315758865e6f56ab87ad06a88c7ac172f056',
    allow_patterns=['Lance_3B_Video/*','Qwen2.5-VL-ViT/*','Wan2.2_VAE.pth','config.json'],
    local_dir=root/'upstream/downloads',max_workers=2)
metadata=list((root/'upstream/downloads/.cache/huggingface/download').rglob('*.metadata'))
revisions={str(p.relative_to(root/'upstream/downloads')):p.read_text().splitlines()[0] for p in metadata}
provenance={'model_revision':'7395315758865e6f56ab87ad06a88c7ac172f056',
    'code_revision':'4baeee086648996f6ab12e673cbe461b0b149997',
    'download_metadata_revisions':revisions,
    'all_download_metadata_matches':bool(revisions) and all(v=='7395315758865e6f56ab87ad06a88c7ac172f056' for v in revisions.values()),
    'model_repository':'bytedance-research/Lance','weights_rehashed':False}
(root/'model_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps(provenance,indent=2))
PY
