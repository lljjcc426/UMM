import unittest
from scripts.stroke_metrics import evaluate

class EventMetricTest(unittest.TestCase):
    def test_identical(self):
        result = evaluate(["a", "b"], ["a", "b"])
        self.assertTrue(result["sequence_exact"])
        self.assertEqual(result["event_edit_distance"], 0)
        self.assertIsNone(result["first_mismatch_1_based"])
    def test_swap_is_not_exact(self):
        result = evaluate(["a", "b", "c"], ["a", "c", "b"])
        self.assertFalse(result["sequence_exact"])
        self.assertEqual(result["event_edit_distance"], 2)
        self.assertEqual(result["first_mismatch_1_based"], 2)
    def test_missing(self):
        result = evaluate(["a", "b"], ["a"])
        self.assertEqual(result["event_edit_distance"], 1)
        self.assertEqual(result["first_mismatch_1_based"], 2)
    def test_extra(self):
        self.assertEqual(evaluate(["a"], ["a","b"])["first_mismatch_1_based"], 2)
    def test_empty(self):
        self.assertTrue(evaluate([], [])["sequence_exact"])
    def test_invalid(self):
        with self.assertRaises(TypeError):
            evaluate("abc", ["a"])
        with self.assertRaises(ValueError):
            evaluate([""], [])

if __name__ == "__main__":
    unittest.main()
