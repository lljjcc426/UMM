"""Exercise CI events without granting draft reviews permission to merge."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_stage_release import validate_ci_release

ROOT = Path(__file__).resolve().parents[1]


class CIStageGateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "evidence.json").write_text("{}")
        self.manifest = dict(schema_version=1, protocol_id="stroke-video-v2", phase="P0",
            branch="research/p0-stroke-video-foundation", status="in_progress",
            conclusion="pending", experiment_ids=["ENV-01"], evidence_bundle=["evidence.json"],
            approval_reference=None, unresolved_blockers=[], limitations=[])
        self.registry = dict(protocol_id="stroke-video-v2", experiments=[dict(
            id="ENV-01", phase="P0", status="completed", run_records=["evidence.json"],
            result_artifacts=["evidence.json"])])

    def event(self, draft, action="synchronize", head=None):
        return dict(action=action, pull_request=dict(draft=draft,
            head=dict(ref=head or self.manifest["branch"])))

    def result(self, draft, action="synchronize", head=None):
        return validate_ci_release(self.manifest, self.registry, self.root,
                                    "pull_request", self.event(draft, action, head))

    def test_draft_review_passes_without_merge_authorization(self):
        result = self.result(True)
        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual(result["approval_gate"], "deferred_non_mergeable_draft")
        self.assertFalse(result["merge_authorized"])

    def test_all_non_draft_pr_events_require_final_approval(self):
        for action in ["opened", "synchronize", "reopened", "ready_for_review"]:
            with self.subTest(action=action):
                result = self.result(False, action)
                self.assertFalse(result["passed"])
                self.assertEqual(result["approval_gate"], "required")
                self.assertIn("missing user approval reference", result["errors"])
                self.assertIn("PR requires ready_for_review", result["errors"])

    def test_approved_non_draft_can_pass_strict_gate(self):
        self.manifest.update(status="ready_for_review", conclusion="supported_negative",
                             approval_reference="fixture explicit human science and merge approval")
        result = self.result(False, "ready_for_review")
        self.assertTrue(result["passed"], result["errors"])
        self.assertTrue(result["merge_authorized"])

    def test_converting_back_to_draft_restores_review_only(self):
        result = self.result(True, "converted_to_draft")
        self.assertTrue(result["passed"], result["errors"])
        self.assertFalse(result["merge_authorized"])

    def test_draft_still_rejects_invalid_release_evidence(self):
        self.manifest["experiment_ids"] = ["missing-experiment"]
        result = self.result(True)
        self.assertFalse(result["passed"])
        self.assertIn("experiment set differs from phase", result["errors"])

    def test_non_draft_wrong_stage_branch_is_rejected(self):
        result = self.result(False, head="research/p1-other")
        self.assertIn("PR head differs from manifest branch", result["errors"])

    def test_branch_push_does_not_grant_merge_authorization(self):
        result = validate_ci_release(self.manifest, self.registry, self.root, "push", {})
        self.assertTrue(result["passed"], result["errors"])
        self.assertFalse(result["merge_authorized"])

    def test_workflow_cli_reads_actual_github_event_file(self):
        folder = self.root / "docs/project/stages"
        folder.mkdir(parents=True)
        (folder / "P0-release.json").write_text(json.dumps(self.manifest))
        folder = self.root / "data/research"
        folder.mkdir(parents=True)
        (folder / "experiments_v2.json").write_text(json.dumps(self.registry))
        event_file = self.root / "event.json"
        env = dict(os.environ, GITHUB_EVENT_NAME="pull_request", GITHUB_EVENT_PATH=str(event_file))
        for draft, expected_code in [(True, 0), (False, 1)]:
            with self.subTest(draft=draft):
                event_file.write_text(json.dumps(self.event(draft)))
                run = subprocess.run([sys.executable, str(ROOT / "scripts/validate_stage_release.py"),
                    "--github-event", "--root", str(self.root)], env=env, text=True, capture_output=True)
                self.assertEqual(run.returncode, expected_code, run.stdout + run.stderr)
                self.assertFalse(json.loads(run.stdout)["merge_authorized"])
