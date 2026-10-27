"""Validate phase-release evidence paths; this is not a scientific truth checker.

Stage-branch pushes accept draft manifests. Promotion to main requires a
completed experimental phase with traceable run/result artifacts and a
reference to explicit user approval. Human review remains mandatory.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASE = Path("docs/project/stages/P0-release.json")
REGISTRY = Path("data/research/experiments_v2.json")
STATUSES = {"in_progress", "blocked", "ready_for_review"}
VALID_CONCLUSIONS = {"phase_gate_passed", "supported_positive", "supported_negative"}


def validate_release(manifest: Any, registry: Any, root: Path,
                     require_ready: bool = False, head_ref: str | None = None) -> dict:
    errors: list[str] = []
    root = root.resolve()

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def check_file(value: Any, label: str) -> None:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}: empty reference")
            return
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or "://" in value:
            errors.append(f"{label}: unsafe path")
            return
        resolved = (root / path).resolve()
        if not resolved.is_relative_to(root) or not resolved.is_file():
            errors.append(f"{label}: evidence file missing: {value}")

    if not isinstance(manifest, dict) or not isinstance(registry, dict):
        return {"passed": False, "errors": ["manifest and registry must be dictionaries"]}

    check(manifest.get("schema_version") == 1, "invalid stage manifest version")
    check(manifest.get("protocol_id") == "stroke-video-v2", "invalid research protocol")
    check(registry.get("protocol_id") == manifest.get("protocol_id"),
          "protocol and registry mismatch")
    phase, branch = manifest.get("phase"), manifest.get("branch")
    check(isinstance(phase, str) and bool(re.fullmatch(r"P[0-6]", phase)), "invalid phase")
    check(isinstance(branch, str) and bool(re.fullmatch(r"research/p[0-6]-[a-z0-9-]+", branch)),
          "invalid research branch")
    if isinstance(branch, str) and isinstance(phase, str):
        check(branch.startswith(f"research/{phase.lower()}-"), "branch/phase mismatch")
    if head_ref is not None:
        check(head_ref == branch, "PR head differs from manifest branch")

    status = manifest.get("status")
    check(status in STATUSES, "invalid release status")
    ids = manifest.get("experiment_ids")
    if not isinstance(ids, list) or not ids or any(not isinstance(x, str) or not x for x in ids):
        errors.append("invalid experiment list")
        ids = []
    rows = registry.get("experiments")
    if not isinstance(rows, list):
        errors.append("missing experiment registry")
        rows = []
    indexed = {row.get("id"): row for row in rows if isinstance(row, dict)}
    expected = {row.get("id") for row in rows if isinstance(row, dict) and row.get("phase") == phase}
    check(len(ids) == len(set(ids)), "duplicate experiment IDs")
    check(set(ids) == expected and bool(expected), "experiment set differs from phase")
    for exp_id in ids:
        check(exp_id in indexed, f"unknown experiment {exp_id}")

    bundle = manifest.get("evidence_bundle")
    blockers = manifest.get("unresolved_blockers")
    limitations = manifest.get("limitations")
    check(isinstance(bundle, list) and all(isinstance(f, str) for f in bundle),
          "evidence_bundle must be a string list")
    check(isinstance(blockers, list) and all(isinstance(f, str) for f in blockers),
          "unresolved_blockers must be a string list")
    check(isinstance(limitations, list) and all(isinstance(f, str) for f in limitations),
          "limitations must be a string list")

    promote = require_ready or status == "ready_for_review"
    if promote:
        check(status == "ready_for_review", "PR requires ready_for_review")
        check(manifest.get("conclusion") in VALID_CONCLUSIONS,
              "phase conclusion is pending or unsupported")
        approval = manifest.get("approval_reference")
        check(isinstance(approval, str) and len(approval.strip()) >= 10
              and approval.strip().lower() not in {"pending", "todo", "placeholder"},
              "missing user approval reference")
        check(isinstance(blockers, list) and len(blockers) == 0,
              "unresolved phase blockers")
        check(isinstance(bundle, list) and len(bundle) > 0, "no stage evidence bundle")
        if isinstance(bundle, list):
            for filename in bundle:
                check_file(filename, "stage evidence bundle")
        for exp_id in ids:
            row = indexed.get(exp_id)
            if not isinstance(row, dict):
                continue
            check(row.get("status") == "completed", f"{exp_id}: not completed")
            for key in ("run_records", "result_artifacts"):
                arr = row.get(key)
                check(isinstance(arr, list) and len(arr) > 0, f"{exp_id}: {key} missing")
                if isinstance(arr, list):
                    for filename in arr:
                        check_file(filename, f"{exp_id}.{key}")

    return {
        "passed": not errors, "errors": errors,
        "mode": "merge_gate" if require_ready else "development",
        "phase": phase, "branch": branch, "experiments": len(ids),
        "scientific_claims_verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-ready", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--head-ref", default=os.environ.get("GITHUB_HEAD_REF"))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        manifest = json.loads((root / RELEASE).read_text(encoding="utf-8"))
        registry = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
        result = validate_release(manifest, registry, root,
                                  require_ready=args.require_ready,
                                  head_ref=args.head_ref if args.require_ready else None)
    except (OSError, TypeError, ValueError) as e:
        result = {"passed": False, "errors": [str(e)], "scientific_claims_verified": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
