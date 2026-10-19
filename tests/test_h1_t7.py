"""Requested T7 contracts; no training or model-cache extraction."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import torch
from h1_event_model import StrokeGrounding
from h1_target_contrast import target_contrast
from h1_t7_io import model_input,prepare_group
from h1_t7_data import rows

class T7Contracts(unittest.TestCase):
    def test_same_reference_queries_remain_distinct(self):
        torch.manual_seed(42);torch.set_num_threads(4);a=StrokeGrounding().eval()
        ref=torch.zeros(1,729,1536);k=torch.ones(1,3,dtype=torch.long);h=torch.zeros(1,3,2)
        with torch.no_grad():p,_=a(ref,k,h)
        self.assertFalse(torch.equal(p[:,0],p[:,1]))
        for q in [3,5]:
            with torch.no_grad():p,_=a(ref,torch.ones(1,q,dtype=torch.long),torch.zeros(1,q,2))
            self.assertEqual(p.shape,(1,q,729))

    def test_shared_regions_are_not_contrastive_negatives(self):
        target=torch.tensor([[[1.,0.,1.],[0.,1.,1.]]]);exclusive=torch.tensor([[[1.,0.,0.],[0.,1.,0.]]]);shared=torch.tensor([[0.,0.,1.]])
        logits=torch.zeros_like(target,requires_grad=True)
        loss=target_contrast(logits,target,exclusive,shared,torch.ones(1,2,dtype=torch.long),torch.zeros(1,2,2));loss.backward()
        self.assertTrue(torch.equal(logits.grad[:,:,2],torch.zeros(1,2)))
        self.assertLess(float(logits.grad[0,0,0]),0);self.assertGreater(float(logits.grad[0,0,1]),0)

    def test_label_free_input(self):
        x={k:None for k in ['reference','visual','small','ref_small','kinds','hints','rgb']};x.update(row=dict(indices=[0,4],split='test',label_source_order=[1,0]),masks='privileged',truth_states='hidden')
        p=model_input(x)
        self.assertNotIn('masks',p);self.assertNotIn('truth_states',p);self.assertEqual(p['row'],dict(indices=[0,4]))

    def test_group_split_and_query_ids(self):
        seen={};qs=set()
        for r in rows():
            if r['group'] in seen:self.assertEqual(seen[r['group']],r['split'])
            seen[r['group']]=r['split'];q=len(r['strokes']);qs.add(q);self.assertEqual(r['query']['instance_ids'],list(range(q)))
        self.assertEqual(qs,{3,5});self.assertEqual(len(seen),90)

    def test_training_partition_and_test_lock(self):
        from unittest.mock import patch
        from tempfile import TemporaryDirectory
        original=Path.read_text;opened=[]
        def read(path,*args,**kwargs):
            opened.append(str(path));return original(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):train=rows('train')
        self.assertTrue(all(r['split']=='train' for r in train))
        self.assertFalse(any('/test-' in p or p.endswith('instance_onset_v1/cases.json') for p in opened))
        with TemporaryDirectory() as directory,patch('h1_t7_io.OUT',Path(directory)):
            with self.assertRaisesRegex(RuntimeError,'locked'):next(prepare_group('test-close-q3-00'))

    def test_mixed_q_pair_denominator_and_cluster_weighting(self):
        from h1_t7_score import pairs,estimate
        records=[]
        for q in [3,5]:
            for variant in ['correct','swap1']+(['swap2'] if q==5 else []):
                for t in [15,20,23]:records.append(dict(group=f'g{q}',q=q,family='parallel',variant=variant,t=t,order_correct=variant!='swap2'))
        ps=pairs(records);self.assertEqual(len(ps),9)
        metric=estimate(ps,lambda p:p['both_correct'])
        self.assertAlmostEqual(metric['value'],2/3);self.assertAlmostEqual(metric['geometry_balanced'],.75)

if __name__=='__main__':unittest.main()
