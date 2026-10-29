"""Semantic regression tests independent of CASIA/private assets."""
from copy import deepcopy
from dataclasses import replace
import inspect
import unittest

import numpy as np

from scripts.p0.judgments import DeclaredPlan, judge_execution, judge_normative, normative_plan
from scripts.p0.normative_reference import BindingItem, GeometryBinding, NormSpec, qualify_reference
from scripts.p0.rgb_observation import GeometryInstance, observe_rgb


class DecoupledTests(unittest.TestCase):
    def setUp(self):
        self.spec = NormSpec('test-reference', 'fixture', ('s1','s2'), ('horizontal','vertical'), 'test fixture only')
        self.binding = GeometryBinding('test-binding', (BindingItem('opaque-z','s1','A','B'), BindingItem('opaque-a','s2','X','Y')))
        self.reviews = [dict(instance_id=i.instance_id,canonical_id=i.canonical_id,start_anchor=i.start_anchor,
            end_anchor=i.end_anchor,norm_reference_id='test-reference',normative_position=k+1,
            normative_stroke_description=self.spec.stroke_descriptions[k],identity_status='verified',direction_status='verified',
            evidence_id='fixture-'+str(k),evidence='Known hand-written test facts',normative_comparison='test fixture',audit_level='test_fixture')
            for k,i in enumerate(self.binding.items)]
        self.ref = qualify_reference(self.spec,self.binding,self.reviews)
        def event(start):
            return dict(geometry_observable=True,final_coverage=1.,onset={'frame':start},complete={'frame':start+1})
        self.e = dict(events={'opaque-z':dict(event(1),anchors={'A':{'frame':1},'B':{'frame':2}}),
                              'opaque-a':dict(event(4),anchors={'X':{'frame':4},'Y':{'frame':5}})},
            frame_count=7,timestamps=list(range(7)),completion_fraction=.92,
            temporal_sampling_available=True,all_blank=False,extra_ink=False,ink_disappeared=False,
            concurrent_growth=False,initial_ink_pixels=0)

    def test_four_cells_distinguish_intention_and_actual_norm(self):
        good=normative_plan(self.ref)
        bad=replace(good,plan_id='wrong',order=tuple(reversed(good.order)))
        wrong=deepcopy(self.e)
        for key,delta in [('opaque-z',3),('opaque-a',-3)]:
            for field in ['onset','complete']:wrong['events'][key][field]['frame']+=delta
            for anchor in wrong['events'][key]['anchors'].values():anchor['frame']+=delta
        for evidence,actual in [(self.e,'correct'),(wrong,'incorrect')]:
            self.assertEqual(judge_normative(evidence,self.ref)['decision'],actual)
            for plan,matched in [(good,actual=='correct'),(bad,actual=='incorrect')]:
                self.assertEqual(judge_execution(evidence,plan)['decision'],'match' if matched else 'mismatch')

    def test_global_pass_cannot_qualify_instance_binding(self):
        global_pass=[dict(instance_id=i.instance_id,decision='pass') for i in self.binding.items]
        ref=qualify_reference(self.spec,self.binding,global_pass)
        self.assertEqual(ref.status,'unknown')
        self.assertEqual(judge_normative(self.e,ref)['decision'],'unknown')

    def test_changed_reference_version_requires_its_own_evidence(self):
        ref=qualify_reference(replace(self.spec,reference_id='new-unreviewed'),self.binding,self.reviews)
        self.assertEqual(ref.status,'unknown')
        self.assertEqual(judge_execution(self.e,normative_plan(self.ref))['decision'],'match')
        self.assertEqual(judge_normative(self.e,ref)['decision'],'unknown')

    def test_unobserved_order_is_unknown_and_visible_violation_is_incorrect(self):
        sparse=deepcopy(self.e);sparse.update(temporal_sampling_available=False,frame_count=2,timestamps=[0,1])
        for event in sparse['events'].values():
            event['onset']={'frame':1};event['complete']={'frame':1}
            event['anchors']={name:{'frame':1} for name in event['anchors']}
        self.assertEqual(judge_normative(sparse,self.ref)['decision'],'unknown')
        sparse['extra_ink']=True
        self.assertEqual(judge_normative(sparse,self.ref)['decision'],'incorrect')

    def test_blank_T_output_does_not_need_normative_binding_to_fail(self):
        unknown=qualify_reference(self.spec,self.binding,[])
        evidence=dict(self.e,all_blank=True,temporal_sampling_available=False)
        self.assertEqual(judge_normative(evidence,unknown)['decision'],'incorrect')
        self.assertEqual(judge_execution(evidence,None)['decision'],'not_applicable')

    def test_opaque_ids_and_anchor_names_have_no_rank_semantics(self):
        items=tuple(replace(i,instance_id='new-'+i.instance_id,start_anchor='last',end_anchor='first') for i in reversed(self.binding.items))
        reviews=[dict(r,instance_id='new-'+r['instance_id'],start_anchor='last',end_anchor='first') for r in self.reviews]
        ref=qualify_reference(self.spec,GeometryBinding('renamed',items),reviews)
        evidence=deepcopy(self.e)
        evidence['events']={'new-'+k:dict(v,anchors=dict(zip(['last','first'],v['anchors'].values()))) for k,v in reversed(list(evidence['events'].items()))}
        self.assertEqual(judge_normative(evidence,ref)['decision'],'correct')

    def test_pixel_observer_reports_evidence_without_implicit_direction_verdict(self):
        # Three tiny in-memory array fixtures; no new video file/research sample.
        frames=np.full((3,3,3,3),255,np.uint8);frames[1:,1,0]=0;frames[2:,1,2]=0
        mask=np.zeros((3,3),bool);mask[1,[0,2]]=True
        a=np.zeros_like(mask);a[1,0]=True;b=np.zeros_like(mask);b[1,2]=True
        cfg=dict(ink=128,onset=.04,complete=.92,region=.12,minimum_exclusive_pixels=1,
                 minimum_region_pixels=1,extra_ink_pixels=0,disappeared_pixels=0)
        g=GeometryInstance('arbitrary',mask,{'end_label':a,'start_label':b})
        result=observe_rgb(frames,[0,.1,.2],[g],cfg)
        self.assertNotIn('decision',result)
        self.assertEqual(result['events']['arbitrary']['anchors']['end_label']['frame'],1)
        self.assertEqual(result['events']['arbitrary']['anchors']['start_label']['frame'],2)
        self.assertNotIn('plan',inspect.signature(observe_rgb).parameters)
        self.assertNotIn('norm_spec',inspect.signature(observe_rgb).parameters)


if __name__=='__main__':
    unittest.main()
