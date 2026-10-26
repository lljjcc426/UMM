"""Synthetic validation tests; no learned-model inference or data benchmark."""
import copy
import tempfile
import unittest
from pathlib import Path
from scripts.validate_research_plan import validate_payload


class ResearchPlanTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "schema_version": 1, "protocol_id": "test-v1",
            "data_plan": {"train_characters": 3, "validation_characters": 1,
                          "test_characters": 2, "main_total_characters": 6, "calibration_characters": 2},
            "seeds": {"training": [11, 23, 47], "inference": [11, 23, 47]},
            "gates": {"calibration_min_coverage": .9, "false_accept_upper95_max": .05,
                      "minimum_effect_pp": 5, "final_character_noninferiority_margin_pp": 2},
            "budget": {"configured": False, "gpu_model": None, "gpu_count": None, "max_gpu_hours": None},
            "documents": {"roadmap": "docs/plan.md"}}
        row = {"id": "A", "phase": "P0", "hypothesis": "test", "depends_on": [],
               "baselines": ["test baseline"], "primary_metrics": ["coverage"],
               "deliverables": ["future manifest"], "success_condition": "calibrate first",
               "status": "planned", "run_records": [], "result_artifacts": []}
        self.registry = {"schema_version": 1, "protocol_id": "test-v1", "experiments": [row]}

    def validate(self):
        return validate_payload(self.config, self.registry)

    def test_valid_design(self):
        self.assertTrue(self.validate()["passed"])
        self.assertFalse(self.validate()["model_results_verified"])

    def test_duplicate_ids(self):
        self.registry["experiments"].append(copy.deepcopy(self.registry["experiments"][0]))
        self.assertFalse(self.validate()["passed"])

    def test_unknown_dependency(self):
        self.registry["experiments"][0]["depends_on"] = ["missing"]
        self.assertFalse(self.validate()["passed"])

    def test_cycle(self):
        self.registry["experiments"][0]["depends_on"] = ["A"]
        self.assertFalse(self.validate()["passed"])

    def test_two_node_cycle(self):
        row = copy.deepcopy(self.registry["experiments"][0])
        row.update(id="B", depends_on=["A"])
        self.registry["experiments"][0]["depends_on"] = ["B"]
        self.registry["experiments"].append(row)
        self.assertFalse(self.validate()["passed"])

    def test_split_total(self):
        self.config["data_plan"]["main_total_characters"] = 7
        self.assertFalse(self.validate()["passed"])

    def test_bool_is_not_count(self):
        self.config["data_plan"]["train_characters"] = True
        self.assertFalse(self.validate()["passed"])

    def test_duplicate_seed(self):
        self.config["seeds"]["training"] = [11, 11]
        self.assertFalse(self.validate()["passed"])

    def test_completed_requires_evidence(self):
        self.registry["experiments"][0]["status"] = "completed"
        self.assertFalse(self.validate()["passed"])

    def test_planned_cannot_claim_results(self):
        self.registry["experiments"][0]["result_artifacts"] = ["fake-result.json"]
        self.assertFalse(self.validate()["passed"])

    def test_configured_budget_requires_values(self):
        self.config["budget"]["configured"] = True
        self.assertFalse(self.validate()["passed"])

    def test_protocol_mismatch(self):
        self.registry["protocol_id"] = "other"
        self.assertFalse(self.validate()["passed"])

    def test_gate_nan(self):
        self.config["gates"]["calibration_min_coverage"] = float("nan")
        self.assertFalse(self.validate()["passed"])

    def test_invalid_record_type(self):
        self.registry["experiments"].append("bad record")
        self.assertFalse(self.validate()["passed"])

    def test_invalid_top_level(self):
        self.assertFalse(validate_payload([], self.registry)["passed"])

    def test_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertFalse(validate_payload(self.config, self.registry, root)["passed"])
            (root / "docs").mkdir()
            (root / "docs/plan.md").write_text("test", encoding="utf-8")
            self.assertTrue(validate_payload(self.config, self.registry, root)["passed"])
            self.config["documents"]["roadmap"] = "../outside.md"
            self.assertFalse(validate_payload(self.config, self.registry, root)["passed"])


if __name__ == "__main__":
    unittest.main()
