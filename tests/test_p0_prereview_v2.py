import unittest
import numpy as np

from scripts.p0.ai_prereview import inspect_rgb
from scripts.p0.prereview_v2 import inspect_rgb_v2


class SmallStrokeEvidenceTests(unittest.TestCase):
    def fixture(self):
        masks=np.zeros((1,128,128),bool);masks[0,30,30:38]=True
        frames=np.full((10,128,128,3),255,np.uint8)
        for i in range(1,10):frames[i,30,30:30+min(i,8)]=0
        inv=lambda x:(x-10)*1024/108
        median=[[[inv(30),900-inv(30)],[inv(37),900-inv(30)]]]
        return frames,np.arange(10)*.1,masks,median

    def test_eight_pixel_stroke_has_distinct_temporal_evidence(self):
        f,t,m,p=self.fixture()
        self.assertEqual(inspect_rgb(f,t,m,p)['facets']['direction'],'unknown')
        self.assertEqual(inspect_rgb_v2(f,t,m,p)['facets']['direction'],'pass')

    def test_reverse_visible_direction_is_not_hidden_by_shared_anchors(self):
        f,t,m,p=self.fixture();reverse=f.copy()
        reverse[:,:,30:38]=f[:,:,30:38][:,:,::-1]
        self.assertEqual(inspect_rgb_v2(reverse,t,m,p)['facets']['direction'],'fail')

    def test_sparse_or_coincident_endpoint_evidence_stays_unknown(self):
        f,t,m,p=self.fixture()
        self.assertEqual(inspect_rgb_v2(f[[0,-1]],t[[0,-1]],m,p)['facets']['direction'],'unknown')
        p[0][-1]=p[0][0]
        self.assertEqual(inspect_rgb_v2(f,t,m,p)['facets']['direction'],'unknown')


if __name__=='__main__':unittest.main()
