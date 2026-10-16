"""Focused checks for H1 counterfactuals, observability and score attribution."""
import unittest
import numpy as np
from scripts.h1_dataset import render, annotation
from scripts.h1_score import score


class H1Test(unittest.TestCase):
    def test_matched_final_different_history(self):
        a = [('top',1,False),('middle',1,False),('bottom',1,False)]
        b = [a[0],a[2],a[1]]
        self.assertTrue(np.array_equal(np.asarray(render('three',a)[-1]),
                                       np.asarray(render('three',b)[-1])))
        self.assertEqual(annotation('three',b,'sampled_frames')['first_error'],2)
        self.assertEqual(annotation('three',a,'last_frame'),annotation('three',b,'last_frame'))

    def test_partial_complete_and_early_switch_have_distinct_actions(self):
        partial = [('top',.5,False)]
        complete = [('top',1,False)]
        self.assertEqual(annotation('three',partial,'sampled_frames')['next'],'continue')
        self.assertEqual(annotation('three',complete,'sampled_frames')['target'],'middle')
        self.assertEqual(annotation('three',partial+[('middle',1,False)],'sampled_frames')['error_type'],'early_switch')

    def test_missing_unknown_and_wrong_action_are_distinct(self):
        expected = annotation('three',[('top',.5,False)],'last_frame')
        label = dict(expected=expected,score_observation=True)
        self.assertTrue(score(expected,label)['all_required'])
        predicted = dict(expected,next='continue',target='top')
        self.assertTrue(score(predicted,label)['judgment'])
        self.assertFalse(score(predicted,label)['action'])
        self.assertFalse(score({},label)['all_required'])

    def test_oracle_state_does_not_score_copied_observations(self):
        expected = annotation('three',[('top',1,True)],'oracle_state')
        pred = {k:expected[k] for k in ['status','first_error','error_type','next','target']}
        metrics = score(pred,dict(expected=expected,score_observation=False))
        self.assertNotIn('order',metrics)
        self.assertTrue(metrics['all_required'])

    def test_static_state_can_confirm_error_without_recovering_order(self):
        impossible = [('top',.5,False),('middle',1,False)]
        result = annotation('three',impossible,'last_frame')
        self.assertEqual(result['status'],'invalid')
        self.assertIsNone(result['order'])
        self.assertEqual(result['first_error'],'unknown')
        self.assertEqual(result['next'],'stop_error')
        self.assertEqual(result,annotation('three',list(reversed(impossible)),'last_frame'))


if __name__ == '__main__':
    unittest.main()
