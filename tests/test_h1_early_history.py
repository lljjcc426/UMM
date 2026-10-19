"""Required T6 information-control, causal-memory and scoring checks."""
import sys,json,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import torch
from h1_event_model import EventState,rule_action
from h1_event_ledger import EventLedger
from h1_early_history_data import DATA,OUT
from h1_early_history_io import model_input

class EarlyHistoryTests(unittest.TestCase):
    def test_registered_data_contract(self):
        c=json.loads((OUT/'data_contract_checks.json').read_text());self.assertTrue(c['zero_training_gate']);self.assertEqual(c['locked_test_pairs'],40)
        self.assertTrue(all(r['recent8_inputs_exact'] and r['feature_cache_exact'] for r in c['B3_input_checks']))
        r=json.loads((DATA/'cases.json').read_text());groups={}
        for x in r:groups.setdefault(json.dumps(x['strokes']),set()).add(x['split'])
        self.assertEqual(len(groups),50);self.assertTrue(all(len(s)==1 for s in groups.values()))
    def test_model_input_whitelist(self):
        keys=['reference','visual','small','ref_small','kinds','hints','rgb']
        x={k:None for k in keys};x.update(row=dict(indices=[0,4],variant='forbidden',label_source_order=[1,0]),masks='oracle',state='forbidden')
        v=model_input(x);self.assertEqual(set(v),set(keys+['row']));self.assertEqual(v['row'],{'indices':[0,4]});self.assertNotIn('masks',v)
    def test_variable_shapes_and_causality(self):
        torch.set_num_threads(4);torch.manual_seed(42)
        for t,q in [(5,2),(24,5),(7,3)]:
            for temporal in [True,False]:
                m=EventState(temporal=temporal).eval();x=torch.randn(1,t,q,196);y=x.clone();y[:,3:]=torch.randn_like(y[:,3:])*20
                with torch.no_grad():a=m(x);b=m(y)
                self.assertEqual(tuple(a['state'].shape),(1,t,q,3))
                self.assertTrue(all(torch.equal(a[k][:,:3],b[k][:,:3]) for k in a))
                mask=EventState.causal_mask(t,q);self.assertFalse(bool(mask[:q,:q].any()));self.assertTrue(bool(mask[:q,q:].all()))
    def test_ledger_partial_uncertainty_and_online_prefix(self):
        l=EventLedger(3);l.update(0,[0]*3,[0]*3,[0]*3,['unknown']*3,[0]*3)
        first=l.update(1,[1,1,0],[1,1,0],[2,2,0],['unknown']*3,[1,1,0]);frozen=json.dumps(first,sort_keys=True)
        final=l.update(2,[1,1,1],[1,1,.5],[2,2,1],['unknown','unknown','forward'],[0,0,.5])
        self.assertIsNone(final['event_order']);self.assertEqual(final['unresolved_order_groups'],[[0,1]])
        self.assertEqual(sorted(final['confirmed_precedence']),[[0,2],[1,2]])
        self.assertEqual(final['uncertainty_reason'],'merged_onset_interval');self.assertEqual(frozen,json.dumps(first,sort_keys=True))
        self.assertEqual(final['recovery'],'requires_missing_past_observations')
    def test_first_violation_and_action(self):
        for order,index in [([1,0,2],0),([0,2,1],1),([0,1,2],None)]:
            d=rule_action(dict(event_order=order,progress=[1]*3,direction=['forward']*3),[0,1,2]);self.assertEqual(d['first_error'],index)
            self.assertEqual(d['action'],'end_ink_task' if index is None else 'stop_erroneous_process')
    def test_pair_denominator_keeps_reused_correct_history(self):
        from h1_early_history_score import compute_pairs,estimate,partial_score
        rs=[dict(id='g-'+v,group='g',t=t,q=5,order_correct=not(v=='swap2' and t==15),prediction={'event_order':[0,1]},truth={'event_order':[0,1]}) for v in ['correct','swap1','swap2'] for t in [15,20,23]]
        pairs=compute_pairs(rs);self.assertEqual(len(pairs),6)
        score=estimate(pairs,lambda r:r['both_correct']);self.assertEqual(score['geometry_groups'],1);self.assertAlmostEqual(score['value'],5/6)
        p=dict(confirmed_precedence=[[0,2],[1,2]],unresolved_order_groups=[[0,1]])
        partial=partial_score([dict(id='g',group='g',t=23,prediction=p,truth=p)])
        self.assertEqual(partial['confirmed_recall'],1);self.assertEqual(partial['unresolved_precision'],1)

if __name__=='__main__':unittest.main()
