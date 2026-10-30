#!/usr/bin/env bash
# Run on the rented Linux GPU instance, after extracting env01-cloud.tar.gz.
set -Eeuo pipefail
BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETUP_DIR="$BUNDLE_DIR/setup/$(date -u +%Y%m%dT%H%M%S)-$$"
mkdir -p "$SETUP_DIR"
exec > >(tee "$SETUP_DIR/setup.log") 2>&1
SETUP_STARTED=$(date +%s)
finish() {
    local code=$?
    trap - EXIT
    local elapsed=$(( $(date +%s) - SETUP_STARTED ))
    printf '{"exit_code":%s,"elapsed_seconds":%s,"weights_downloaded_on":"cloud","dependency_check":"dependency-check.json"}\n' "$code" "$elapsed" > "$SETUP_DIR/status.json"
    exit "$code"
}
trap finish EXIT
set -x
uname -a
nvidia-smi | tee "$SETUP_DIR/nvidia-smi.txt"
nvcc --version
df -h "$BUNDLE_DIR"
free -h

ENV_DIR="$BUNDLE_DIR/runtime"
if [[ ! -x "$ENV_DIR/bin/python" ]]; then
    if command -v conda >/dev/null 2>&1; then
        conda create -y -p "$ENV_DIR" python=3.11 pip
    else
        # Python 3.11 is required by this reproducible deployment recipe.
        python3.11 -m venv "$ENV_DIR"
    fi
fi
PYTHON="$ENV_DIR/bin/python"
export PATH="$ENV_DIR/bin:$PATH"
export HF_HUB_DOWNLOAD_TIMEOUT="${HF_HUB_DOWNLOAD_TIMEOUT:-90}"
export HF_HUB_ETAG_TIMEOUT="${HF_HUB_ETAG_TIMEOUT:-30}"
"$PYTHON" -m pip install --upgrade pip setuptools wheel ninja packaging psutil
"$PYTHON" -m pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
# Resolve upstream's unpinned packages against its protobuf/numpy constraints.
"$PYTHON" -m pip install -r "$BUNDLE_DIR/upstream/requirements.txt" wandb==0.19.11 scipy==1.15.3
# Four Ninja jobs fit measured free memory on the 16-core/48 GB host.
MAX_JOBS=4 "$PYTHON" -m pip install flash-attn==2.6.3 --no-build-isolation --find-links "$BUNDLE_DIR/wheelhouse"
"$PYTHON" -m pip freeze --all > "$SETUP_DIR/pip-freeze.txt"
"$PYTHON" - "$BUNDLE_DIR" <<'PY'
import json
from pathlib import Path
import sys
from huggingface_hub import snapshot_download
bundle = Path(sys.argv[1])
plan = json.loads((bundle / "plan.json").read_text())
snapshot_download(repo_id=plan["weight_repository"], revision=plan["weight_revision"],
                  allow_patterns=plan["weight_patterns"], local_dir=bundle / "upstream/downloads",
                  max_workers=2)
PY
"$PYTHON" "$BUNDLE_DIR/tools/fixtures.py" --bundle "$BUNDLE_DIR" --encode-video
"$PYTHON" "$BUNDLE_DIR/tools/check_dependencies.py" --bundle "$BUNDLE_DIR" --setup "$SETUP_DIR"
printf 'Setup completed. Run: %q %q --bundle %q\n' "$PYTHON" "$BUNDLE_DIR/tools/run_interfaces.py" "$BUNDLE_DIR"
