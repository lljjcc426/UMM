"""P1 finite negative closeout preserves unknowns and separate merge approval."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_stage_release import validate_release


class P1CloseoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "evidence.json").write_text("{}")
        self.scope = dict(phase="P1", decision="approved", accepted_scope="limited_native_baseline_negative")
        (self.root / "scope.json").write_text(json.dumps(self.scope))
        states = {"SO-00": "completed_with_limitations", "BASE-01": "completed_negative",
                  "EVAL-02": "completed_with_limitations", "SO-01": "completed_with_limitations"}
        self.registry = dict(protocol_id="stroke-video-v2", experiments=[
            dict(id=name, phase="P1", status=state, run_records=["evidence.json"],
                 result_artifacts=["evidence.json"], scientific_outcome=dict(
                     original_gate_met=False, unmet_criteria=["original requirement not established"],
                     conclusion="bounded evidence; unknowns retained")) for name, state in states.items()])
        self.manifest = dict(schema_version=2, protocol_id="stroke-video-v2", phase="P1",
            branch="research/p1-native-baselines", status="closed_with_negative_results",
            conclusion="supported_negative", experiment_ids=list(states), evidence_bundle=["evidence.json"],
            unresolved_blockers=[], limitations=["coarse screening only; H1 unknown"], approval_reference=None,
            closure=dict(accepted_scope=self.scope["accepted_scope"], original_scientific_gates_met=False,
                scope_approval_reference="scope.json", original_contract="evidence.json",
                original_release_manifest="evidence.json", final_report="evidence.json",
                human_evidence_level="user_relayed_coarse_screening", formal_seven_facet_review_completed=False,
                H1_status="not_established", automatic_judge_role="auxiliary_only",
                unknown_policy="preserved_without_imputation", user_final_report_review="pending",
                main_merge_authorized=False, unmet_original_criteria=[
                    dict(experiment_id=name, criterion="original criterion", observed="not established",
                         disposition="preserved as unverified, not waived as passed") for name in states]))

    def result(self, merge=False):
        return validate_release(self.manifest, self.registry, self.root, require_ready=merge,
                                head_ref=self.manifest["branch"] if merge else None)

    def test_closure_completes_scope_without_claiming_original_science_or_merge(self):
        result = self.result()
        self.assertTrue(result["passed"], result["errors"])
        self.assertTrue(result["phase_completed"])
        self.assertFalse(result["original_scientific_gates_met"])
        self.assertFalse(result["merge_authorized"])

    def test_scope_approval_does_not_promote_even_with_ready_label(self):
        self.manifest.update(status="ready_for_review", approval_reference="scope.json")
        result = self.result(merge=True)
        self.assertTrue(result["phase_completed"])
        self.assertFalse(result["passed"])
        self.assertIn("P1 final report review is pending", result["errors"])
        self.assertIn("P1 main merge not authorized", result["errors"])
        self.assertIn("P1 scope approval cannot replace separate merge approval", result["errors"])

    def test_distinct_later_report_and_merge_approval_can_promote_negative_release(self):
        (self.root / "merge-approved.json").write_text("{}")
        self.manifest["approval_reference"] = "merge-approved.json"
        self.manifest["closure"].update(user_final_report_review="approved", main_merge_authorized=True)
        result = self.result(merge=True)
        self.assertTrue(result["passed"], result["errors"])
        self.assertTrue(result["merge_authorized"])
        self.assertFalse(result["original_scientific_gates_met"])

    def test_original_unmet_conditions_and_nonterminal_rows_cannot_disappear(self):
        self.manifest["closure"]["unmet_original_criteria"].pop()
        self.assertFalse(self.result()["passed"])
        self.registry["experiments"][-1]["status"] = "pending_human_review"
        self.assertIn("SO-01: not completed", self.result()["errors"])

    def test_coarse_review_and_unproven_H1_cannot_be_relabelled(self):
        for field, value in [("formal_seven_facet_review_completed", True), ("H1_status", "established")]:
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest["closure"][field] = value
                self.assertFalse(validate_release(manifest, self.registry, self.root)["passed"])
        self.registry["experiments"][1]["status"] = "completed"
        self.assertFalse(self.result()["passed"])

    def test_P0_or_future_phase_cannot_reuse_this_scope(self):
        self.scope["phase"] = "P0"
        (self.root / "scope.json").write_text(json.dumps(self.scope))
        self.assertIn("P1 requires its own explicit limited-scope approval", self.result()["errors"])
        self.manifest.update(phase="P2", branch="research/p2-limited")
        for row in self.registry["experiments"]:
            row["phase"] = "P2"
        self.assertFalse(self.result()["passed"])

    def test_missing_preserved_contract_blocks_closure(self):
        self.manifest["closure"]["original_contract"] = "missing-original.md"
        result = self.result()
        self.assertFalse(result["passed"])
        self.assertFalse(result["phase_completed"])
