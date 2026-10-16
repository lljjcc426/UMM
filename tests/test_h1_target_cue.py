"""Check matched questions, preserved ink and unmarked no-reference replay."""
import unittest

from PIL import Image, ImageChops

from scripts.h1_state_gate import read_jsonl
from scripts.h1_target_cue import DATA


class TargetCueTest(unittest.TestCase):
    def test_cues_preserve_ink_and_matched_questions_without_marking_replay(self):
        checked=set()
        for name in ('train','train_reference','reference_dev','all_targets_dev'):
            raw, boxed = [DATA/arm/name for arm in ('raw','boxed')]
            a, b = [read_jsonl(path/'inputs.jsonl') for path in (raw,boxed)]
            self.assertEqual(read_jsonl(raw/'labels.jsonl'),read_jsonl(boxed/'labels.jsonl'))
            self.assertEqual([(r['sample_id'],r['prompt']) for r in a],
                             [(r['sample_id'],r['prompt']) for r in b])
            if name.startswith('train'):
                self.assertEqual({r['split'] for r in a},{'train'})
            for x,y in zip(a,b):
                key=y['images'][0]
                if key in checked:
                    continue
                checked.add(key)
                with Image.open(raw/x['images'][0]) as original, Image.open(boxed/key) as marked:
                    if x['view']=='current_only':
                        self.assertIsNone(ImageChops.difference(original,marked).getbbox())
                    else:
                        ink=lambda image:image.convert('L').point(lambda p:255 if p==0 else 0)
                        self.assertIsNone(ImageChops.difference(ink(original),ink(marked)).getbbox())
                        self.assertIsNotNone(ImageChops.difference(original,marked).getbbox())

if __name__=='__main__':
    unittest.main()
