"""Evidence handling checks; no model or GPU dependencies are loaded."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.env01.run_interfaces import assess_attempt, inference_args

ROOT = Path(__file__).resolve().parents[1]


class NativeInterfaceEvidence(unittest.TestCase):
    def test_success_exit_without_artifact_is_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            result = assess_attempt("x2t_video", Path(directory), 0)
            self.assertEqual(result["status"], "failed")
            self.assertFalse(result["output_check"]["valid"])
            self.assertEqual(result["sample_denominator"], 1)

    def test_empty_native_answer_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt = Path(directory)
            (attempt / "outputs").mkdir()
            output = attempt / "outputs/result.json"
            output.write_text(json.dumps([{"answer": "  "}]))
            self.assertEqual(assess_attempt("x2t_video", attempt, 0)["status"], "failed")
            output.write_text(json.dumps([{"answer": "Horizontal, then vertical."}]))
            self.assertEqual(assess_attempt("x2t_video", attempt, 0)["status"], "interface_passed")

    def test_process_failure_retains_measurements_and_denominator(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt = Path(directory)
            failure = {"status": "failed", "error": "CUDA out of memory", "cuda_peak_allocated_bytes": 123}
            (attempt / "worker_metrics.json").write_text(json.dumps(failure))
            result = assess_attempt("t2v", attempt, 1)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["measurements"], failure)
            self.assertEqual(result["sample_denominator"], 1)

    def test_execution_records_both_model_and_noise_seeds(self):
        plan = json.loads((ROOT / "configs/research/env01_interface_probe.json").read_text())
        args = inference_args(Path("/bundle"), Path("/run/inputs"), Path("/run/outputs"), "i2v", plan)
        self.assertEqual(args[args.index("--global_seed") + 1], "11")
        self.assertEqual(args[args.index("--validation_data_seed") + 1], "11")
        self.assertEqual(args[args.index("--enhance_prompt") + 1], "false")
        self.assertEqual(args[args.index("--val_dataset_config_file") + 1], "/run/inputs/i2v.json")


if __name__ == "__main__":
    unittest.main()
