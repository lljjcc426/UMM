#!/usr/bin/env bash
set -euo pipefail
/home/vipuser/miniconda3/bin/python -m pip install --disable-pip-version-check --target /root/umm-env01-20261027-a10080/download-client hf_transfer==0.1.9
HF_HUB_ENABLE_HF_TRANSFER=1 PYTHONPATH=/root/umm-env01-20261027-a10080/download-client /home/vipuser/miniconda3/bin/python /root/umm-env01-20261027-a10080/download_weights.py /root/umm-env01-20261027-a10080/env01-cloud
