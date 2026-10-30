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
REGISTRY = Path("data/research/experiments_v2.json")
STATUSES = {"in_progress", "blocked", "ready_for_review", "closed_with_negative_results"}
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

    check(manifest.get("schema_version") in {1, 2}, "invalid stage manifest version")
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

    closure = manifest.get("closure")
    limited_closeout = status == "closed_with_negative_results" or closure is not None
    if limited_closeout:
        check(status in {"closed_with_negative_results", "ready_for_review"}, "limited closeout lifecycle is inconsistent")
        check(manifest.get("schema_version") == 2 and phase == "P0", "limited closeout requires P0 schema2")
        check(manifest.get("conclusion") == "supported_negative", "limited closeout cannot claim original gates passed")
        closure = closure if isinstance(closure, dict) else {}
        check(closure.get("accepted_scope") == "limited_research_foundation", "missing limited accepted scope")
        check(closure.get("original_scientific_gates_met") is False, "original scientific failures must remain explicit")
        check(closure.get("automatic_scorer_required_for_P1") is False, "P1 must support the independent human evaluation route")
        routes = closure.get("formal_evaluation_path", [])
        check(isinstance(routes, list) and {"trusted_normative_reference", "independent_human_judgments",
              "automatic_auxiliary_only", "strict_unknown_handling"}.issubset(routes),
              "incomplete alternative evaluation path")
        for key in ("scope_approval_reference", "original_contract", "original_release_manifest", "final_report"):
            check_file(closure.get(key), "closure." + key)
        unmet = closure.get("unmet_original_criteria")
        check(isinstance(unmet, list) and len(unmet) > 0 and all(
            isinstance(x, dict) and x.get("experiment_id") in ids and x.get("criterion")
            and x.get("observed") and x.get("disposition") for x in unmet),
            "missing explicit disposition of unmet original criteria")
        if isinstance(unmet, list):
            unmet_ids = {x.get("experiment_id") for x in unmet if isinstance(x, dict)}
            check({"DATA-01", "EVAL-01"}.issubset(unmet_ids), "DATA/EVAL original failures omitted")
        check(blockers == [], "unresolved blockers to the approved limited closeout")

    promote = require_ready or status == "ready_for_review"
    # A scientifically closed P0 negative release can be promoted without
    # changing its lifecycle label back to a pending-review state. This
    # exception still requires a separate, documented main-merge approval.
    negative_closeout_merge_ready = (
        limited_closeout
        and status == "closed_with_negative_results"
        and isinstance(closure, dict)
        and closure.get("user_final_report_review") == "approved"
        and closure.get("main_merge_authorized") is True
    )
    promotion_errors = []
    if promote:
        approval = manifest.get("approval_reference")
        promotion_errors = [message for condition, message in [
            (status == "ready_for_review" or negative_closeout_merge_ready,
             "PR requires ready_for_review"),
            (manifest.get("conclusion") in VALID_CONCLUSIONS, "phase conclusion is pending or unsupported"),
            (isinstance(approval, str) and len(approval.strip()) >= 10
             and approval.strip().lower() not in {"pending", "todo", "placeholder"}, "missing user approval reference"),
            (isinstance(blockers, list) and len(blockers) == 0, "unresolved phase blockers"),
        ] if not condition]
    if promote or limited_closeout:
        check(isinstance(bundle, list) and len(bundle) > 0, "no stage evidence bundle")
        if isinstance(bundle, list):
            for filename in bundle:
                check_file(filename, "stage evidence bundle")
        for exp_id in ids:
            row = indexed.get(exp_id)
            if not isinstance(row, dict):
                continue
            state = row.get("status")
            allowed = {"completed", "completed_negative", "completed_with_limitations"} if limited_closeout else {"completed"}
            check(state in allowed, f"{exp_id}: not completed")
            outcome = row.get("scientific_outcome", {})
            if state in {"completed_negative", "completed_with_limitations"}:
                check(isinstance(outcome, dict) and outcome.get("original_gate_met") is False
                      and bool(outcome.get("unmet_criteria")), f"{exp_id}: incomplete negative/limited outcome")
            elif isinstance(outcome, dict) and outcome.get("original_gate_met") is False:
                check(False, f"{exp_id}: unmet original gate cannot be recorded as unqualified completed")
            if limited_closeout and exp_id == "ENV-01":
                check(state == "completed", "ENV-01 verified scope must remain completed")
            if limited_closeout and exp_id in {"DATA-01", "EVAL-01"}:
                expected_state = "completed_with_limitations" if exp_id == "DATA-01" else "completed_negative"
                check(state == expected_state, f"{exp_id}: original outcome must remain limited/negative")
            for key in ("run_records", "result_artifacts"):
                arr = row.get(key)
                check(isinstance(arr, list) and len(arr) > 0, f"{exp_id}: {key} missing")
                if isinstance(arr, list):
                    for filename in arr:
                        check_file(filename, f"{exp_id}.{key}")

    # Scientific completion is independent from subsequent merge authorization.
    phase_completed = limited_closeout and not errors
    if promote and status == "closed_with_negative_results":
        # Reject a bare approval assertion. The merge-specific source must
        # exist in the repository and remain separate from science approval.
        check_file(manifest.get("approval_reference"), "explicit merge approval")
    errors.extend(promotion_errors)
    return {
        "passed": not errors, "errors": errors,
        "mode": "merge_gate" if require_ready else "development",
        "phase": phase, "branch": branch, "experiments": len(ids),
        "scientific_claims_verified": False,
        "phase_completed": phase_completed,
        "original_scientific_gates_met": False if limited_closeout else None,
        "merge_authorized": promote and not errors,
    }


def validate_ci_release(manifest: Any, registry: Any, root: Path,
                        event_name: str, event: dict) -> dict:
    """A draft can be reviewed but cannot merge; ready PRs keep the strict gate."""
    head_ref = None
    stage_pr = False
    draft = False
    if event_name == "pull_request":
        pr = event["pull_request"]
        head_ref = pr["head"]["ref"]
        stage_pr = head_ref.startswith("research/")
        draft = pr["draft"]
    require_ready = stage_pr and not draft
    result = validate_release(manifest, registry, root, require_ready=require_ready,
                              head_ref=head_ref if require_ready else None)
    result["approval_gate"] = (
        "required" if require_ready else
        "deferred_non_mergeable_draft" if stage_pr else "not_applicable"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--require-ready", action="store_true")
    mode.add_argument("--github-event", action="store_true",
                      help="Check drafts for review; enforce approval for non-draft research PRs")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--phase", choices=[f"P{i}" for i in range(7)],
                        help="Audit a historical phase; defaults to the configured current phase")
    parser.add_argument("--head-ref", default=os.environ.get("GITHUB_HEAD_REF"))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        phase = args.phase or json.loads(
            (root / "configs/research/stroke_video_v2.json").read_text(encoding="utf-8"))["current_phase"]
        manifest = json.loads((root / f"docs/project/stages/{phase}-release.json").read_text(encoding="utf-8"))
        registry = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
        if args.github_event:
            event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
            result = validate_ci_release(manifest, registry, root,
                                         os.environ["GITHUB_EVENT_NAME"], event)
        else:
            result = validate_release(manifest, registry, root,
                                      require_ready=args.require_ready,
                                      head_ref=args.head_ref if args.require_ready else None)
    except (OSError, TypeError, ValueError) as e:
        result = {"passed": False, "errors": [str(e)], "scientific_claims_verified": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
