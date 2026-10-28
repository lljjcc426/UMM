import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from scripts.p0.ai_prereview import inspect_rgb, normative_suggestion
from scripts.p0.review_server import ReviewStore, public_task


class AIPrereviewTest(unittest.TestCase):
    def test_actual_pixels_distinguish_swap_and_ink_loss_without_schedule(self):
        masks=np.zeros((2,128,128),bool)
        masks[0,20:60,25:30]=True;masks[1,20:60,75:80]=True
        medians=[[[x,800],[x,400]] for x in [160,640]]
        frames=np.full((4,128,128,3),255,np.uint8)
        frames[1,masks[1]]=0
        frames[2,masks.any(axis=0)]=0
        # A visible disappearance is independent of uncertain direction.
        frames[3,masks[0]]=0
        result=inspect_rgb(frames,np.arange(4)*.1,masks,medians)
        self.assertEqual(result['facets']['order'],'fail')
        self.assertEqual(result['facets']['ink_preservation'],'fail')
        self.assertEqual(result['observed_order'],[2,1])
        self.assertEqual(result['decision'],'incorrect')
        self.assertFalse(result['review_coverage']['AI_visually_watched_all_frames'])

    def test_reference_count_match_does_not_invent_complete_normative_approval(self):
        template=dict(character='二',strokes=['first','second'],medians=[[[100,600],[800,600]],[[100,300],[800,300]]])
        reference=dict(status='extracted',official_codes='11',printed_stroke_count=2,official_page=1,official_index=1)
        result=normative_suggestion(template,reference)
        self.assertEqual(result['facets']['stroke_count'],'pass')
        self.assertEqual(result['facets']['order'],'unknown')
        self.assertEqual(result['decision'],'unverified')
        self.assertFalse(result['review_coverage']['full_normative_semantics_verified'])

    def test_assisted_AI_payload_does_not_create_or_leak_another_human_record(self):
        ai=dict(decision='unknown',facets={},reasons=[],notes='AI only',disputed=False,observed_order=None,
            events=[],model_version='TEST',priority='high',review_method='test',review_coverage={},evidence=['test'])
        task=dict(blind_id='TEST_AI',type='rgb_event',character='二',batch='assisted_rgb',ai_suggestion=ai)
        pack=dict(protocol=dict(id='TEST',mode='assisted'),batches=dict(assisted_rgb=[task]),tutorial=[])
        with tempfile.TemporaryDirectory() as directory:
            store=ReviewStore(pack,Path(directory))
            store.allowed_batch('assisted_rgb','UI_TEST_1')
            self.assertEqual(public_task(task)['ai_suggestion']['notes'],'AI only')
            self.assertEqual(store.state('UI_TEST_1')['annotations'],[])
            store.append('UI_TEST_1',dict(kind='annotation',annotation=dict(blind_id='TEST_AI',decision='unknown')))
            self.assertEqual(store.state('UI_TEST_2')['annotations'],[])


if __name__=='__main__':unittest.main()
