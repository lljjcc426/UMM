"""Package pinned public source and ENV-01 tools without weights or local dependencies."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import tarfile
from urllib.request import urlopen

from fixtures import prepare_inputs

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-cache", type=Path, action="append", default=[])
    args = parser.parse_args()
    output = args.output.resolve()
    bundle = output / "env01-cloud"
    bundle.mkdir(parents=True, exist_ok=True)
    plan = json.loads((ROOT / "configs/research/env01_interface_probe.json").read_text())
    tree = (ROOT / "data/research/audits/env01_static_2026-10-27/source_tree.txt").read_text().splitlines()
    paths = [name for name in tree
             if (Path(name).suffix in {".py", ".sh", ".yaml", ".yml", ".json"}
                 or name in {"LICENSE", "README.md", "requirements.txt"})
             and (not name.startswith("benchmarks/") or name == "benchmarks/sample_env.sh")]
    source = bundle / "upstream"
    manifest = {"code_revision": plan["code_revision"], "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "source": "https://github.com/bytedance/Lance", "operations": [], "complete": False}

    def collect(name: str) -> dict:
        target = source / name
        url = f"https://raw.githubusercontent.com/bytedance/Lance/{plan['code_revision']}/{name}"
        if target.is_file():
            return {"path": name, "url": url, "status": "retained_from_previous_attempt", "bytes": target.stat().st_size}
        for cache in args.source_cache:
            if (cache / name).is_file():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(cache / name, target)
                return {"path": name, "url": url, "status": "copied_from_pinned_audit_cache", "bytes": target.stat().st_size}
        try:
            with urlopen(url, timeout=45) as response:
                data = response.read()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            return {"path": name, "url": url, "status": "downloaded", "bytes": len(data)}
        except Exception as error:
            return {"path": name, "url": url, "status": "failed", "error": str(error)}

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(collect, name) for name in paths]
        for future in as_completed(futures):
            row = future.result()
            manifest["operations"].append(row)
            if row["status"] == "failed":
                print(json.dumps(row), flush=True)
    manifest["complete"] = not any(row["status"] == "failed" for row in manifest["operations"])
    output.mkdir(parents=True, exist_ok=True)
    attempt = output / ("source_collection_" + datetime.now(timezone.utc).strftime("%H%M%S%f") + ".json")
    attempt.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    if not manifest["complete"]:
        raise SystemExit("Source collection incomplete; failed requests retained in " + str(attempt))
    (bundle / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    (bundle / "upstream_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    tools = bundle / "tools"
    tools.mkdir(exist_ok=True)
    for name in ("bootstrap.sh", "run_interfaces.py", "fixtures.py"):
        shutil.copyfile(ROOT / "scripts/env01" / name, tools / name)
    shutil.copyfile(ROOT / "docs/research/v2/env01_cloud_deployment.md", bundle / "README.md")
    prepare_inputs(bundle, plan)
    archive = output / "env01-cloud.tar.gz"
    if archive.exists():
        raise SystemExit("Keep the existing archive; select a new --output directory to build a new version")
    with tarfile.open(archive, "w:gz") as handle:
        handle.add(bundle, arcname="env01-cloud")
    print(json.dumps({"archive": str(archive), "bytes": archive.stat().st_size,
                      "upstream_source_files": len(paths), "weights_included": False}, indent=2))


if __name__ == "__main__":
    main()
