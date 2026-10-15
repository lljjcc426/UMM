"""Metrics for already annotated event IDs; NOT a video stroke extractor.

This utility does not know Chinese writing standards. References must be supplied
from a declared, reviewed rule set. These simple metrics do not measure pressure,
style, image quality, temporal observability, or valid alternative orderings.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Sequence

def _check(seq: Sequence[str], name: str) -> list[str]:
    if isinstance(seq, (str, bytes)) or not isinstance(seq, (list, tuple)):
        raise TypeError(f"{name} must be a list or tuple of nonempty event-ID strings")
    if any(not isinstance(x, str) or not x.strip() for x in seq):
        raise ValueError(f"{name} contains an invalid event ID")
    return list(seq)

def evaluate(reference: Sequence[str], prediction: Sequence[str]) -> dict:
    ref, pred = _check(reference, "reference"), _check(prediction, "prediction")
    prev = list(range(len(pred) + 1))
    for i, a in enumerate(ref, 1):
        cur = [i]
        for j, b in enumerate(pred, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (a != b)))
        prev = cur
    mismatch = next((i + 1 for i, (a, b) in enumerate(zip(ref, pred)) if a != b), None)
    if mismatch is None and len(ref) != len(pred):
        mismatch = min(len(ref), len(pred)) + 1
    return {
        "reference_length": len(ref),
        "prediction_length": len(pred),
        "sequence_exact": ref == pred,
        "event_edit_distance": prev[-1],
        "first_mismatch_1_based": mismatch,
        "scope": "annotated_ID_sequence_only_not_a_model_benchmark"
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = evaluate(data["reference"], data["prediction"])
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
