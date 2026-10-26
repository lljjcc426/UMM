"""Validate research-plan structure and local references; never run a model."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"planned", "ready", "running", "blocked", "completed", "stopped"}
REQUIRED = {"id", "phase", "hypothesis", "depends_on", "baselines", "primary_metrics",
            "deliverables", "success_condition", "status", "run_records", "result_artifacts"}


def validate_payload(config: Any, registry: Any, root: Path | None = None) -> dict:
    errors: list[str] = []
    checked_paths: set[str] = set()

    def check(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    def number(value: Any, low: float, high: float) -> bool:
        return (isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value) and low <= value <= high)

    def local_file(value: Any, label: str) -> None:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}: expected nonempty relative path")
            return
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or "://" in value:
            errors.append(f"{label}: path must remain inside repository")
            return
        if root is not None:
            resolved = (root / path).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append(f"{label}: missing or unsafe file {value}")
            else:
                checked_paths.add(value)

    if not isinstance(config, dict) or not isinstance(registry, dict):
        return {"passed": False, "errors": ["config and registry must be objects"],
                "experiments": 0, "local_files_checked": 0, "model_results_verified": False}
    check(config.get("schema_version") == 1, "unsupported config schema")
    check(registry.get("schema_version") == 1, "unsupported registry schema")
    protocol = config.get("protocol_id")
    check(isinstance(protocol, str) and bool(protocol), "missing protocol_id")
    check(registry.get("protocol_id") == protocol, "protocol_id mismatch")
    data = config.get("data_plan", {})
    if not isinstance(data, dict):
        errors.append("data_plan must be object")
        data = {}
    counts = [data.get(k) for k in ("train_characters", "validation_characters", "test_characters")]
    count_valid = all(type(v) is int and v > 0 for v in counts)
    check(count_valid, "split counts must be positive integers")
    if count_valid:
        check(sum(counts) == data.get("main_total_characters"), "split counts do not sum to main total")
    check(type(data.get("calibration_characters")) is int and data.get("calibration_characters", 0) > 0,
          "invalid calibration count")
    seeds = config.get("seeds", {})
    for kind in ("training", "inference"):
        values = seeds.get(kind) if isinstance(seeds, dict) else None
        good = isinstance(values, list) and bool(values) and all(type(x) is int and x >= 0 for x in values)
        check(bool(good), f"invalid {kind} seeds")
        if good:
            check(len(values) == len(set(values)), f"duplicate {kind} seeds")
    gates = config.get("gates", {})
    if not isinstance(gates, dict):
        gates = {}
    for name in ("calibration_min_coverage", "false_accept_upper95_max"):
        check(number(gates.get(name), 0, 1), f"{name} outside [0,1]")
    for name in ("minimum_effect_pp", "final_character_noninferiority_margin_pp"):
        check(number(gates.get(name), 0, 100), f"{name} outside [0,100]")
    budget = config.get("budget", {})
    if not isinstance(budget, dict):
        errors.append("budget must be object")
        budget = {}
    check(type(budget.get("configured")) is bool, "budget.configured must be boolean")
    if budget.get("configured") is True:
        check(isinstance(budget.get("gpu_model"), str) and bool(budget.get("gpu_model")), "missing gpu_model")
        check(type(budget.get("gpu_count")) is int and budget.get("gpu_count", 0) > 0, "invalid gpu_count")
        check(number(budget.get("max_gpu_hours"), 0.001, 1e9), "invalid max_gpu_hours")
    documents = config.get("documents", {})
    check(isinstance(documents, dict) and bool(documents), "documents must be nonempty object")
    if isinstance(documents, dict):
        for key, value in documents.items():
            local_file(value, f"document {key}")
    rows = registry.get("experiments")
    if not isinstance(rows, list) or not rows:
        errors.append("experiments must be nonempty list")
        rows = []
    ids: list[str] = []
    graph: dict[str, list[str]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"record {index}: expected object")
            continue
        name = row.get("id")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"record {index}: invalid id")
            continue
        ids.append(name)
        check(not (REQUIRED - row.keys()), f"{name}: missing required fields")
        check(row.get("phase") in {f"P{i}" for i in range(7)}, f"{name}: invalid phase")
        check(row.get("status") in STATUSES, f"{name}: invalid status")
        for field in ("hypothesis", "success_condition"):
            check(isinstance(row.get(field), str) and bool(row.get(field)), f"{name}: empty {field}")
        for field in ("depends_on", "baselines", "primary_metrics", "deliverables", "run_records", "result_artifacts"):
            values = row.get(field)
            ok = isinstance(values, list) and all(isinstance(v, str) and bool(v) for v in values)
            check(ok, f"{name}: {field} must be a string list")
            if field in {"baselines", "primary_metrics", "deliverables"}:
                check(bool(values) and ok, f"{name}: empty {field}")
        deps = row.get("depends_on", [])
        graph[name] = deps if isinstance(deps, list) and all(isinstance(d, str) for d in deps) else []
        runs, results = row.get("run_records", []), row.get("result_artifacts", [])
        if row.get("status") == "completed":
            check(isinstance(runs, list) and bool(runs) and isinstance(results, list) and bool(results),
                  f"{name}: completed requires run records and result artifacts")
        if row.get("status") == "planned":
            check(runs == [] and results == [], f"{name}: planned cannot contain claimed run/results")
        for field in ("run_records", "result_artifacts"):
            values = row.get(field, [])
            if isinstance(values, list):
                for value in values:
                    local_file(value, f"{name}.{field}")
    check(len(ids) == len(set(ids)), "duplicate experiment IDs")
    known = set(ids)
    for name, deps in graph.items():
        check(len(deps) == len(set(deps)), f"{name}: duplicate dependency")
        for dep in deps:
            check(dep in known, f"{name}: unknown dependency {dep}")
    visiting: set[str] = set()
    done: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            errors.append(f"dependency cycle at {name}")
            return
        if name in done:
            return
        visiting.add(name)
        for dep in graph.get(name, []):
            if dep in known:
                visit(dep)
        visiting.remove(name)
        done.add(name)

    for name in ids:
        visit(name)
    return {"passed": not errors, "protocol_id": protocol, "experiments": len(rows),
            "local_files_checked": len(checked_paths), "errors": errors,
            "model_results_verified": False,
            "scope": "schema/dependencies/local paths only; no dataset, judge or model validation"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        config = json.loads((root / "configs/research/stroke_video_v1.json").read_text(encoding="utf-8"))
        registry = json.loads((root / "data/research/experiments_v1.json").read_text(encoding="utf-8"))
        report = validate_payload(config, registry, root)
    except (OSError, ValueError, TypeError) as exc:
        report = {"passed": False, "errors": [str(exc)], "model_results_verified": False}
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
