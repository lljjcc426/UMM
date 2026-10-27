"""Validate v2 research design contracts; no data, model, or scientific validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

if __package__:
    from .validate_research_plan import validate_payload
else:
    from validate_research_plan import validate_payload

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BASELINES = {"same_data_sft", "trajectory_style_renderer", "spatial_control", "separated_ug"}
REQUIRED_EXPERIMENTS = {"ADAPT-01", "EVAL-02", "CAUSAL-01", "SO-04"}


def validate_v2(config: Any, registry: Any, root: Path | None = None) -> dict:
    report = validate_payload(config, registry, root)
    errors = list(report["errors"])
    if not isinstance(config, dict) or not isinstance(registry, dict):
        return report

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(config.get("protocol_id") == "stroke-video-v2", "v2 protocol required")
    require(config.get("research_focus") == "method_driven_observable_stroke_execution", "method focus missing")
    require(config.get("primary_protocol") == "T", "complete T generation must remain primary")
    require(config.get("inference_uses_gold_event_boundaries") is False, "gold event boundaries forbidden in primary inference")
    require(config.get("generator_logs_are_evaluation_truth") is False, "generator logs cannot serve as RGB truth")
    required = config.get("required_baselines")
    require(isinstance(required, list) and all(isinstance(v, str) for v in required)
            and REQUIRED_BASELINES.issubset(set(required)), "strong baseline contract missing")
    rows = registry.get("experiments", [])
    rows = rows if isinstance(rows, list) else []
    by_id = {r["id"]: r for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str)}
    require(REQUIRED_EXPERIMENTS.issubset(by_id), "required v2 experiment missing")
    optional = config.get("optional_experiments", [])
    optional_ok = isinstance(optional, list) and all(isinstance(v, str) for v in optional)
    require(optional_ok, "optional_experiments must be string list")
    optional = set(optional) if optional_ok else set()
    require(optional == {"REC-01", "EF-01"}, "feedback and efficiency must remain optional")
    require(optional.issubset(by_id), "optional experiment ID missing")

    def ancestors(name: str) -> set[str]:
        seen: set[str] = set()
        pending = [name]
        while pending:
            current = pending.pop()
            deps = by_id.get(current, {}).get("depends_on", [])
            if not isinstance(deps, list):
                continue
            for dep in deps:
                if isinstance(dep, str) and dep not in seen:
                    seen.add(dep)
                    pending.append(dep)
        return seen

    require(not (ancestors("SO-04") & optional), "optional work must not gate core held-out evaluation")
    require("ADAPT-01" in ancestors("SO-03B"), "mechanism comparison must follow same-data adaptation")
    require("EVAL-02" in ancestors("SO-04"), "generated-domain evaluator calibration required")
    require("ENV-01" not in ancestors("EVAL-01"), "controlled CPU evaluator calibration must not require GPU environment")
    if config.get("status") == "design_only":
        require(config.get("sharing_benefit_established") is False, "design cannot claim established sharing benefit")
        require(all(r.get("status") == "planned" for r in by_id.values()), "design_only registry must remain planned")
    report.update(passed=not errors, errors=errors, model_results_verified=False,
                  scope="v2 schema, dependencies, information and baseline contracts only; no model performance validation")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        config = json.loads((root / "configs/research/stroke_video_v2.json").read_text(encoding="utf-8"))
        registry = json.loads((root / "data/research/experiments_v2.json").read_text(encoding="utf-8"))
        report = validate_v2(config, registry, root)
    except (OSError, ValueError, TypeError) as exc:
        report = {"passed": False, "errors": [str(exc)], "model_results_verified": False}
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
