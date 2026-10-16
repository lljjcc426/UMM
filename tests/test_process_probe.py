"""Check the observer with hand-built pixel frames, independent of the renderer."""
import unittest
import numpy as np
from scripts.process_probe import Stroke, observe


class ProcessProbeTest(unittest.TestCase):
    def setUp(self):
        self.strokes = [Stroke('top', (5, 8), (25, 8)),
                        Stroke('bottom', (5, 25), (25, 25))]

    def test_same_final_different_order(self):
        frames = np.full((5, 34, 32), 255, dtype=np.uint8)
        frames[1:, 22:29, 5:12] = 0
        frames[2:, 22:29, 5:26] = 0
        frames[3:, 5:12, 5:12] = 0
        frames[4:, 5:12, 5:26] = 0
        result = observe(frames, self.strokes)
        self.assertEqual(result['final_ink_iou'], 1)
        self.assertEqual(result['sequence'], ['bottom', 'top'])
        self.assertFalse(result['sequence_exact'])
        self.assertTrue(result['direction_exact'])

    def test_two_frames_do_not_establish_order(self):
        frames = np.full((2, 34, 32), 255, dtype=np.uint8)
        frames[1, 5:12, 5:26] = 0
        frames[1, 22:29, 5:26] = 0
        result = observe(frames, self.strokes)
        self.assertIsNone(result['sequence_exact'])
        self.assertIsNone(result['direction_exact'])
        self.assertIsNone(result['strict_process_correct'])

    def test_reverse_direction_and_early_next_stroke(self):
        frames = np.full((5, 34, 32), 255, dtype=np.uint8)
        frames[1:, 5:12, 19:26] = 0
        frames[2:, 22:29, 5:12] = 0
        frames[3:, 5:12, 5:26] = 0
        frames[4:, 22:29, 5:26] = 0
        result = observe(frames, self.strokes)
        self.assertTrue(result['sequence_exact'])
        self.assertFalse(result['direction_exact'])
        self.assertFalse(result['complete_before_next'])


if __name__ == '__main__':
    unittest.main()
