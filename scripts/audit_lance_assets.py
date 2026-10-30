"""Collect pinned Lance metadata only; never download tensors or execute model code."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import struct
from urllib.request import Request, urlopen

MODEL_ID = "bytedance-research/Lance"
WEIGHT_REVISION = "7395315758865e6f56ab87ad06a88c7ac172f056"
CODE_REVISION = "4baeee086648996f6ab12e673cbe461b0b149997"


def fetch(url: str, byte_range: tuple[int, int] | None = None) -> bytes:
    headers = {"User-Agent": "UMM-ENV01-static-audit"}
    if byte_range is not None:
        headers["Range"] = f"bytes={byte_range[0]}-{byte_range[1]}"
    with urlopen(Request(url, headers=headers), timeout=60) as response:
        if byte_range is not None:
            if response.status != 206:
                raise RuntimeError("Server ignored Range; refusing to download tensor data")
            return response.read(byte_range[1] - byte_range[0] + 1)
        return response.read()


def save_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tensor_summary(header: dict) -> dict:
    elements: Counter = Counter()
    storage_bytes: Counter = Counter()
    groups: Counter = Counter()
    for name, tensor in header.items():
        if name == "__metadata__":
            continue
        count = math.prod(tensor["shape"])
        elements[tensor["dtype"]] += count
        storage_bytes[tensor["dtype"]] += tensor["data_offsets"][1] - tensor["data_offsets"][0]
        groups[".".join(name.split(".")[:2])] += count
    return {"tensor_count": len(header) - int("__metadata__" in header),
            "tensor_elements_by_dtype": dict(elements), "storage_bytes_by_dtype": dict(storage_bytes),
            "tensor_elements_by_prefix": dict(groups)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="New evidence directory; existing output is not overwritten")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    base = f"https://huggingface.co/{MODEL_ID}/resolve/{WEIGHT_REVISION}"
    events = []
    summary = {"collected_at_utc": datetime.now(timezone.utc).isoformat(),
               "model_id": MODEL_ID, "code_revision": CODE_REVISION,
               "weight_revision": WEIGHT_REVISION, "model_executed": False,
               "tensor_payload_downloaded": False, "requests": events}
    try:
        url = f"https://huggingface.co/api/models/{MODEL_ID}/revision/{WEIGHT_REVISION}?blobs=true"
        metadata = json.loads(fetch(url))
        save_json(args.output / "model_metadata.json", metadata)
        events.append({"url": url, "status": "ok"})
        required = [item for item in metadata["siblings"] if
                    item["rfilename"].startswith(("Lance_3B_Video/", "Qwen2.5-VL-ViT/"))
                    or item["rfilename"] in {"Wan2.2_VAE.pth", "config.json"}]
        summary["required_assets"] = required
        summary["required_asset_bytes"] = sum(item["size"] for item in required)
        for name in ("Lance_3B_Video/llm_config.json", "Lance_3B_Video/generation_config.json",
                     "Lance_3B_Video/tokenizer_config.json", "Qwen2.5-VL-ViT/config.json", "config.json"):
            url = f"{base}/{name}"
            save_json(args.output / "configs" / name, json.loads(fetch(url)))
            events.append({"url": url, "status": "ok"})
        summary["safetensors"] = {}
        for name in ("Lance_3B_Video/model.safetensors", "Qwen2.5-VL-ViT/vit.safetensors"):
            url = f"{base}/{name}"
            size = struct.unpack("<Q", fetch(url, (0, 7)))[0]
            header = json.loads(fetch(url, (8, 7 + size)))
            save_json(args.output / "headers" / (name.replace("/", "__") + ".json"), header)
            summary["safetensors"][name] = {"header_bytes": size, **tensor_summary(header)}
            events.append({"url": url, "status": "ok", "byte_ranges": [[0, 7], [8, 7 + size]]})
        summary["collection_status"] = "completed"
    except Exception as exc:
        summary["collection_status"] = "failed"
        summary["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        save_json(args.output / "asset_summary.json", summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
