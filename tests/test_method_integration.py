"""Contract and real data integration checks; no fitted or pretrained model."""
import json
from pathlib import Path
from unittest.mock import patch
import unittest

import numpy as np

from method_v1.batches import collate
from method_v1.integration import audit_dataset, audit_svg_reconstruction
from method_v1.paired import EOS, PAD
from method_v1.program import parse_program, render_frames
from method_v1.cli import demo_programs

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/research/paired_strokes_v1'


class RealPairIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.partitions, cls.audit = audit_dataset(DATA)
        cls.train = cls.partitions['train_development']

    def test_frozen_192_train_and_24_24_16_other_development_splits(self):
        self.assertEqual(self.audit['partitions'], {'train_development': 192,
            'validation_development': 24, 'test_development': 24, 'audit_development': 16})
        self.assertEqual(self.audit['training_strokes'], 1752)
        self.assertFalse(self.audit['evaluation_only_loaded'])
        self.assertEqual(self.audit['formal_holdout_characters'], 0)

    def test_original_rgb_target_character_eos_and_padding(self):
        batch = collate(self.train[:8])
        self.assertEqual(batch.images.shape, (8, 3, 256, 256))
        self.assertEqual((batch.images.min(), batch.images.max()), (0, 1))
        self.assertEqual(batch.descriptions[0], '撇、点、竖、个')
        self.assertEqual(batch.character_unicode[0], ord('个'))
        self.assertEqual(batch.targets[0, :4].tolist(), [3, 4, 2, EOS])
        self.assertEqual(batch.targets[1, :2].tolist(), [5, EOS])
        self.assertTrue(np.all(batch.targets[~batch.target_mask] == PAD))
        for tokens, valid in zip(batch.targets, batch.target_mask):
            self.assertEqual(tokens[valid][-1], EOS)
            self.assertEqual(np.count_nonzero(tokens == EOS), 1)

    def test_every_training_svg_matches_stored_pixels(self):
        report = audit_svg_reconstruction(self.train, DATA)
        self.assertEqual(report['samples'], 192)
        self.assertEqual(report['exact_matches'], 192)

    def test_real_same_sequence_examples_keep_character_supervision(self):
        groups = self.audit['same_sequence_different_character_groups']
        self.assertEqual(len(groups), 1)
        ids = set(groups[0]['ids'])
        pairs = [p for p in self.train if p.sample_id in ids]
        self.assertGreater(len({p.character for p in pairs}), 1)
        self.assertEqual(len({p.strokes for p in pairs}), 1)
        self.assertEqual(len({p.description for p in pairs}), len(pairs))

    def test_collate_cannot_read_geometry_or_normative_catalog(self):
        with (patch('method_v1.integration.audit_svg_reconstruction', side_effect=AssertionError('No SVG in features')),
              patch('hanzi_video.catalog.reference', side_effect=AssertionError('No catalog in features'))):
            self.assertEqual(collate(self.train[:2]).images.shape[0], 2)


class SharedProgramRendererTest(unittest.TestCase):
    def test_raw_program_order_not_corrected_with_normative_catalog(self):
        obj = demo_programs()['tu']
        obj['strokes'] = [{**s, 'order': i + 1} for i, s in enumerate(reversed(obj['strokes']))]
        raw = json.dumps(obj)
        with patch('hanzi_video.render.geometry', side_effect=AssertionError('No oracle SVG in G2 route')):
            actual = list(render_frames(parse_program(raw)))
        expected = list(render_frames(parse_program(demo_programs()['tu'])))
        self.assertTrue(np.array_equal(actual[-1], expected[-1]))
        self.assertFalse(np.array_equal(actual[6], expected[6]))
        self.assertEqual(json.loads(raw)['strokes'][0]['path'], obj['strokes'][0]['path'])

    def test_rectangular_program_reuses_geometry_transform(self):
        obj = demo_programs()['tu']
        obj['canvas'] = [128, 192]
        frames = list(render_frames(parse_program(obj)))
        self.assertEqual(frames[0].shape, (192, 128, 3))
        self.assertTrue(np.all(frames[0] == 255))
        self.assertTrue(np.any(frames[-1] == 0))


if __name__ == '__main__':
    unittest.main()
