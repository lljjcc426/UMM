"""Focused checks for H1 counterfactuals, observability and score attribution."""
import unittest
import json
import tempfile
from pathlib import Path
import numpy as np
from scripts.h1_dataset import render, annotation
from scripts.h1_score import score, evaluate


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

    def test_choice_echo_analysis_preserves_strict_score_and_rejects_conflict(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            inputs=[dict(sample_id=str(i),view='seen_mc',options=['上横','下横','中横','无']) for i in range(3)]
            labels=[dict(sample_id=str(i),expected={'answer':'A'},score_fields=['answer'],construction='test') for i in range(3)]
            predictions=[dict(sample_id='0',raw_response='A. 上横',prediction=None),
                         dict(sample_id='1',raw_response='A. 下横',prediction=None),
                         dict(sample_id='2',raw_response='A',prediction={'answer':'A'})]
            for name,rows in [('inputs',inputs),('labels',labels),('predictions',predictions)]:
                (root/name).write_text(''.join(json.dumps(r)+'\n' for r in rows))
            report=evaluate(root/'inputs',root/'labels',root/'predictions')
            self.assertEqual(report['by_view']['seen_mc']['answer']['correct'],1)
            self.assertEqual(report['by_view']['seen_mc']['choice_content']['correct'],2)
            self.assertFalse(report['details'][0]['metrics']['all_required'])
            self.assertFalse(report['details'][1]['metrics']['choice_content'])


if __name__ == '__main__':
    unittest.main()
