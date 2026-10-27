"""Independent hand-built pixels and information boundaries for the P0 observer."""
import unittest

import numpy as np

from scripts.p0.observer import observe, model_input, one_sided_upper


class PixelObserverTests(unittest.TestCase):
    def setUp(self):
        self.masks=np.zeros((2,24,24),dtype=bool)
        self.masks[0,4:7,3:21]=True
        self.masks[1,17:20,3:21]=True
        self.progress=np.broadcast_to(np.linspace(0,1,24),(2,24,24)).copy()
        self.frames=np.full((13,24,24,3),255,dtype=np.uint8)
        for t in range(1,13):
            if t>=1:self.frames[t,4:7,3:min(21,3+4*t)]=0
            if t>=7:self.frames[t,17:20,3:min(21,3+4*(t-6))]=0

    def test_correct_and_same_final_swapped_pixels(self):
        self.assertEqual(observe(self.frames,self.masks,self.progress)['decision'],'correct')
        swapped=self.frames.copy()
        swapped[:,4:7]=self.frames[:,17:20]
        swapped[:,17:20]=self.frames[:,4:7]
        self.assertTrue(np.array_equal(swapped[-1],self.frames[-1]))
        self.assertIn('wrong_instance_order',observe(swapped,self.masks,self.progress)['errors'])

    def test_sparse_pixels_do_not_establish_order(self):
        self.assertEqual(observe(self.frames[[0,-1]],self.masks,self.progress)['decision'],'unknown')

    def test_disappearing_visible_ink_is_rejected(self):
        frames=self.frames.copy()
        frames[-1,4:7,3:21]=255
        result=observe(frames,self.masks,self.progress)
        self.assertEqual(result['decision'],'incorrect')
        self.assertIn('visible_ink_disappeared',result['errors'])

    def test_real_concurrent_growth_is_rejected(self):
        frames=self.frames.copy()
        frames[:,17:20]=frames[:,4:7]
        result=observe(frames,self.masks,self.progress)
        self.assertIn('observable_concurrent_growth',result['errors'])

    def test_prefix_excludes_future_and_evaluation_fields(self):
        sample={'character':'二','evaluation_only':{'answer':'secret'},'training_targets':{'rgb':'future'}}
        times=np.arange(13)/12
        t=model_input(sample,self.frames,times,'T')
        p=model_input(sample,self.frames,times,'P',prefix_end=.25)
        self.assertEqual(set(t),{'character','instruction'})
        self.assertEqual(len(p['prefix_rgb']),4)
        self.assertLessEqual(p['prefix_timestamps'].max(),.25)
        self.assertNotIn('evaluation_only',p)

    def test_group_bound_uses_independent_group_denominator(self):
        self.assertAlmostEqual(one_sided_upper(0,64),1-.05**(1/64))
        self.assertGreater(one_sided_upper(0,32),.05)
        self.assertLess(one_sided_upper(0,64),.05)


if __name__=='__main__':
    unittest.main()
