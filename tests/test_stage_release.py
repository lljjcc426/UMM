"""Verify draft/promotion gate behavior. No real model is executed."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_stage_release import validate_release

ROOT = Path(__file__).resolve().parents[1]


class ResearchStageGateTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(
            (ROOT / "docs/project/stages/P0-release.json").read_text(encoding="utf-8"))
        self.registry = json.loads(
            (ROOT / "data/research/experiments_v2.json").read_text(encoding="utf-8"))
        # Legacy protocol fixtures must not change when the live P0 closes.
        self.manifest = dict(schema_version=1, protocol_id="stroke-video-v2", phase="P0",
            branch="research/p0-stroke-video-foundation", status="in_progress", conclusion="pending",
            experiment_ids=["ENV-01", "DATA-01", "EVAL-01"], evidence_bundle=[],
            approval_reference=None, unresolved_blockers=["pending science"], limitations=[])
        for row in self.registry['experiments']:
            row.pop('scientific_outcome', None)

    def result(self, ready=False, root=ROOT, head=None):
        return validate_release(self.manifest, self.registry, root,
                                require_ready=ready, head_ref=head)

    def test_draft_can_pass_branch_development(self):
        result = self.result()
        self.assertTrue(result["passed"], result["errors"])
        self.assertFalse(result["scientific_claims_verified"])

    def test_unfinished_stage_cannot_pass_merge_gate(self):
        result = self.result(ready=True, head=self.manifest["branch"])
        self.assertFalse(result["passed"])
        self.assertIn("PR requires ready_for_review", result["errors"])

    def test_incorrect_head_branch_cannot_promote(self):
        result = self.result(ready=True, head="research/p1-different")
        self.assertIn("PR head differs from manifest branch", result["errors"])

    def test_incomplete_experiment_list_rejected(self):
        self.manifest["experiment_ids"] = ["ENV-01"]
        result = self.result()
        self.assertIn("experiment set differs from phase", result["errors"])

    def test_ready_without_artifacts_fails(self):
        self.manifest.update(status="ready_for_review", conclusion="phase_gate_passed",
                             approval_reference="user approved phase checklist",
                             unresolved_blockers=[], evidence_bundle=[])
        for record in self.registry["experiments"]:
            if record["phase"] == "P0":
                record.update(status="planned", run_records=[], result_artifacts=[])
        result = self.result()
        self.assertIn("no stage evidence bundle", result["errors"])
        self.assertIn("ENV-01: not completed", result["errors"])

    def test_evidence_outside_repo_rejected(self):
        self.manifest.update(status="ready_for_review", conclusion="supported_negative",
                             approval_reference="user approval reference 2026",
                             unresolved_blockers=[], evidence_bundle=["../escape.json"])
        result = self.result()
        self.assertIn("stage evidence bundle: unsafe path", result["errors"])

    def test_verified_negative_is_valid_release_type(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "run"
            folder.mkdir()
            (folder / "phase_summary.md").write_text("Signed audited negative result", encoding="utf-8")
            for rec in self.registry["experiments"]:
                if rec["phase"] == "P0":
                    rec["status"] = "completed"
                    file = folder / f"{rec['id']}.txt"
                    file.write_text("Audited run results with all attempts", encoding="utf-8")
                    rec["run_records"] = [f"run/{rec['id']}.txt"]
                    rec["result_artifacts"] = [f"run/{rec['id']}.txt"]
            self.manifest.update(status="ready_for_review", conclusion="supported_negative",
                                 approval_reference="user approved science review",
                                 unresolved_blockers=[], evidence_bundle=["run/phase_summary.md"])
            result = self.result(ready=True, root=root, head=self.manifest["branch"])
            self.assertTrue(result["passed"], result["errors"])
            self.assertFalse(result["scientific_claims_verified"])

    def test_missing_run_file_fails_even_when_completed(self):
        self.manifest.update(status="ready_for_review", conclusion="phase_gate_passed",
                             approval_reference="user approved phase checklist",
                             unresolved_blockers=[], evidence_bundle=["docs/project/stages/P0.md"])
        for rec in self.registry["experiments"]:
            if rec["phase"] == "P0":
                rec["status"] = "completed"
                rec["run_records"] = ["missing/env.json"]
                rec["result_artifacts"] = ["missing/results.json"]
        result = self.result()
        self.assertFalse(result["passed"])
        self.assertTrue(any("evidence file missing" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
