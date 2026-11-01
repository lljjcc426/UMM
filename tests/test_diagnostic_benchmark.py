"""Measurement contracts and CPU artifacts; no model or GPU calls."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import numpy as np
from PIL import Image

from scripts.diagnostics import adapters,build,contracts,evaluate,media,observer,prepare,reviews,training


class DiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name)
        cls.dataset=cls.root/'benchmark';cls.summary=build.build(cls.dataset)
        cls.rows=[json.loads(s) for s in (cls.dataset/'manifest.jsonl').read_text().splitlines()]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def observe(self,case):
        frames=build.render_lines(case);pts=np.arange(len(frames))/12
        return observer.judge_execution(observer.observe_rgb(frames,pts,build.REGIONS),build.REFERENCE)
    def test_all_tracks_and_small_materialization(self):
        self.assertEqual(set(self.summary['tracks']),set(contracts.TRACKS));self.assertEqual(self.summary['samples'],74)
        self.assertEqual(self.summary['CPU_videos'],26);self.assertEqual(self.summary['formal_holdout'],0)
    def test_input_answer_separation_and_metadata(self):
        for row in self.rows:
            p=self.dataset/row['input'];value=json.loads(p.read_text());contracts.validate_input(value)
            self.assertNotIn('evaluation',value)
            if value['track']=='K-CHAR':
                self.assertNotIn('character',value);self.assertEqual(Image.open(p.parent/value['media'][0]).info,{})
    def test_kchar_label_leaks_rejected(self):
        v={'id':'S1','track':'K-CHAR','prompt':'Identify 士','media':[]}
        with self.assertRaises(ValueError):contracts.validate_input(v)
    def test_hactual_answer_and_geometry_leaks_rejected(self):
        v={'id':'S1','track':'H-ACTUAL','prompt':'Observe','media':[],'geometry_permission':'G0'}
        for leak in [{'normative_program':['upper','lower']},{'prompt':'standard_order=upper,lower'},{'geometry_permission':'O'},
                     {'visible_state':{'order':['upper','lower']}}]:
            with self.assertRaises(ValueError):contracts.validate_input({**v,**leak})
    def test_permission_path_is_input_only(self):
        with self.assertRaises(ValueError):contracts.validate_input({'id':'S','track':'K-CHAR','prompt':'Identify','media':['../evaluation_only/answer.json']})
    def test_no_source_group_split_leak(self):
        rows=copy.deepcopy(self.rows[:2]);rows[1].update(source_group=rows[0]['source_group'],split='validation')
        with self.assertRaises(ValueError):contracts.validate_manifest(rows)
    def test_development_reference_never_becomes_gold(self):
        rows=copy.deepcopy(self.rows);rows[0]['formal_gold']=True
        with self.assertRaises(ValueError):contracts.validate_manifest(rows)
    def test_same_final_different_history(self):
        a,b=build.render_lines('correct'),build.render_lines('swap')
        np.testing.assert_array_equal(a[-1],b[-1]);self.assertFalse(np.array_equal(a,b))
        self.assertEqual(self.observe('correct')['stroke_order'],'correct');self.assertEqual(self.observe('swap')['stroke_order'],'incorrect')
        group=next(r['source_group'] for r in self.rows if r['source_group'].startswith('exposed-hanzi'))
        rows=[r for r in self.rows if r['track']=='H-ACTUAL' and r['source_group']==group]
        decoded=[]
        for row in rows:
            p=self.dataset/row['input'];payload=json.loads(p.read_text());decoded.append(media.decode(p.parent/payload['media'][0])[0])
        np.testing.assert_array_equal(decoded[0][-1],decoded[1][-1]);self.assertFalse(np.array_equal(*decoded))
    def test_four_cells_plan_does_not_replace_pixels(self):
        for plan_correct in (False,True):
            for actual_correct in (False,True):
                # Planned state is deliberately not an argument to the pixel observer.
                facets=self.observe('correct' if actual_correct else 'swap')
                self.assertEqual(facets['stroke_order'],'correct' if actual_correct else 'incorrect')
    def test_representation_and_identity_invariance(self):
        f=build.render_lines('correct');t=np.arange(33)/12
        regions=copy.deepcopy(build.REGIONS)[::-1]
        for r in regions:r['id']={'upper':'z9','lower':'a2'}[r['id']]
        ref={'order':['z9','a2'],'directions':{'z9':'positive','a2':'positive'}}
        got=observer.judge_execution(observer.observe_rgb(f,t,regions),ref)
        self.assertEqual(got,self.observe('correct'))
    def test_reverse_direction(self):self.assertEqual(self.observe('reverse')['direction'],'incorrect')
    def test_missing_and_extra(self):
        for case in ('missing','extra','blank'):self.assertEqual(self.observe(case)['completeness'],'incorrect')
    def test_history_loss(self):self.assertEqual(self.observe('disappear')['historical_ink'],'incorrect')
    def test_flash_and_sparse_do_not_invent_order(self):
        for case in ('flash','sparse'):
            self.assertEqual(self.observe(case)['stroke_order'],'unknown');self.assertEqual(self.observe(case)['direction'],'unknown')
    def test_dense_overlap_is_error_not_unknown(self):self.assertEqual(self.observe('overlap')['stroke_order'],'incorrect')
    def test_decode_33_frames_actual_pts(self):
        row=next(r for r in self.rows if r['track']=='H-ACTUAL' and r['source_group'].startswith('exposed-hanzi'))
        v=json.loads((self.dataset/row['input']).read_text());f,t=media.decode(self.dataset/Path(row['input']).parent/v['media'][0])
        self.assertEqual(len(t),33);self.assertTrue(np.all(np.diff(t)>0));self.assertAlmostEqual(t[-1],32/12,places=4)
    def test_static_and_interleaved_not_native_video(self):
        for kind in ('interleaved_images','static_image'):self.assertFalse(media.validate_media(kind)['dense_video_eligible'])
    def test_all_attempt_denominator_and_formal_null(self):
        good={k:'correct' for k in contracts.FACETS}
        rows=[{'id':'a','status':'completed','facets':good},{'id':'b','status':'failed'},
              {'id':'c','status':'unknown'},{'id':'d','status':'not_applicable'}]
        r=evaluate.summarize(rows);self.assertEqual(r['all_attempt_success_lower_bound'],.25)
        self.assertEqual(r['technical_failure_rate'],.25);self.assertIsNone(r['formal_primary_metrics'])
        self.assertNotIn('incorrect',r['dimensions']['stroke_order']['counts'])
    def test_failure_does_not_become_order_error(self):
        with self.assertRaises(ValueError):evaluate.summarize([{'id':'f','status':'failed','facets':{'stroke_order':'incorrect'}}])
    def test_unknown_incorrect_na_remain_distinct(self):
        rows=[{'id':str(i),'status':'completed','facets':{'direction':v}} for i,v in enumerate(('unknown','incorrect','not_applicable','correct'))]
        r=evaluate.summarize(rows)['dimensions']['direction']
        self.assertEqual(r['clear_coverage'],.5);self.assertEqual(r['conditional_correct'],.5);self.assertEqual(r['correct_all_attempts'],.25)
    def test_all_seeds_retained_paired(self):
        rows=[{'id':str(s)+c,'character':'士','seed':s,'condition':c,'status':'failed' if s==29 else 'completed'} for s in (11,29,47) for c in ('plain','ordered')]
        pairs=evaluate.paired_attempts(rows);self.assertEqual(len(pairs),3);self.assertEqual(sum(len(p['attempt_ids']) for p in pairs),6)
    def test_policy_draw_need_intermediate_evidence(self):
        self.assertEqual(evaluate.classify_error(False,False,True),'policy_error')
        self.assertEqual(evaluate.classify_error(True,False,True),'draw_error')
        self.assertEqual(evaluate.classify_error(False,False,False),'unattributed')
    def test_narrative_and_construction_not_event_gold(self):
        self.assertEqual(evaluate.score_response('H-ACTUAL',{'events':['upper']},{'construction_events':['upper']})['status'],'unknown')
        self.assertEqual(evaluate.score_response('K-CHAR','I think 士',{'character':'士'})['status'],'unknown')
    def test_error_node_loss_mask_and_context(self):
        for branch,error in [('draw','draw_error_image'),('policy','policy_error_text')]:
            nodes=training.recovery_nodes(branch);bad=next(n for n in nodes if n['type']==error)
            self.assertTrue(bad['in_context']);self.assertEqual(bad['CE_mask']+bad['FM_mask'],0)
            self.assertEqual(len({n['logical_step'] for n in nodes}),1)
    def test_loss_normalized_by_supervised_modality_positions(self):
        a=training.normalized_loss([2,999,4],[1,0,1],[10000,6],[0,1])
        self.assertEqual(a,{'CE':3.,'FM':6.,'total':9.})
        self.assertEqual(training.normalized_loss([],[],[3],[1])['total'],3)
    def test_replay_previous_joint_only(self):
        prev=[{'id':str(i),'draw_error':True,'policy_error':i<10} for i in range(20)]
        r=training.select_replay(prev,[],[]);self.assertEqual(len(r['previous_round_joint_replay']),3)
        self.assertEqual(r,training.select_replay(prev,[],[]))
    def test_mock_valid_corrupt_static_and_missing(self):
        for case in ('correct','corrupt','static','swap','missing_frames'):
            adapter=adapters.MockAdapter(case)
            p=adapter.prepare_input({'id':'S','track':'G-ATOMIC','prompt':'Grow lines','media':[]},self.root/('mock-'+case));adapter.run(p)
            if case in ('corrupt','missing_frames'):
                with self.assertRaises((ValueError,subprocess.CalledProcessError)):adapter.validate_media(p)
            else:self.assertEqual(adapter.validate_media(p)['frames'],33)
        f,t=media.decode(self.root/'mock-static/mock.mp4');self.assertEqual(observer.judge_execution(observer.observe_rgb(f,t,build.REGIONS),build.REFERENCE)['stroke_order'],'unknown')
    def test_real_adapter_cannot_run_or_download(self):
        adapter=adapters.PreparationAdapter({'id':'Lance','task_support':{}})
        with self.assertRaises(PermissionError):adapter.run('/not/run')
    def test_prepare_exact_budgeted_manifest(self):
        p=prepare.prepare(self.dataset,self.root/'batch')
        self.assertEqual(len(p['requests']),24);self.assertEqual(len(set(p['batch_A']['unique_request_ids'])),24)
        self.assertEqual(sum(r['native_task']=='t2v' for r in p['requests']),4)
        for row in p['requests']:
            native=json.loads((Path(row['input_directory'])/(row['native_task']+'.json')).read_text())
            if row['native_task']=='t2v':self.assertEqual(native['0001'],row['prompt'])
        with self.assertRaises(PermissionError):prepare.execution_gate(p['batch_A'])
        b=copy.deepcopy(p['batch_A']);b['gpu_authorized']=True;b['max_spend']=None
        with self.assertRaises(ValueError):prepare.execution_gate(b)
    def test_output_does_not_overwrite_p1_or_current_dataset(self):
        with self.assertRaises(FileExistsError):build.build(self.dataset)
        original=Path('data/research/runs/p1_full_server_2026-10-30')
        with self.assertRaises(FileExistsError):build.build(original)


class HumanImportTests(unittest.TestCase):
    def fixtures(self):
        cards={'id':'test-only-A','cards':[{'id':'blind1','video':'a.mp4'},{'id':'missing','video':None}]}
        row={'id':'blind1','reviewer':'TEST_ONLY_PERSON_A','submitted_at':'2026-11-01T00:00:00Z','reason':'Synthetic test unknown; not a human record',
             **{k:'unknown' for k in contracts.FACETS}}
        export={'schema':'P1-human-review-v1','package_id':cards['id'],'current':{'blind1':row},'versions':[row.copy(),row.copy()]}
        return cards,export
    def test_unknown_versions_and_missing_denominator(self):
        c,e=self.fixtures();r=reviews.validate_export(e,c)
        self.assertEqual(r['version_count'],2);self.assertEqual(r['revision_or_duplicate_count'],1)
        self.assertEqual(r['missing_video_slots'],1);self.assertFalse(r['independence_confirmed'])
    def test_no_human_judgment_for_missing_video(self):
        c,e=self.fixtures();e['versions'][0]['id']='missing'
        with self.assertRaises(ValueError):reviews.validate_export(e,c)
    def test_no_forged_or_merged_identity(self):
        c,e=self.fixtures();e['versions'][0]['reviewer']=''
        with self.assertRaises(ValueError):reviews.validate_export(e,c)
    def test_current_preserves_last_revision(self):
        c,e=self.fixtures();e['current']['blind1']['direction']='correct'
        with self.assertRaises(ValueError):reviews.validate_export(e,c)
    def test_two_codes_do_not_imply_independence(self):
        c,a=self.fixtures();d,b=copy.deepcopy(c),copy.deepcopy(a);d['id']='test-only-B';b['package_id']=d['id']
        b['current']['blind1']['reviewer']='TEST_ONLY_PERSON_B'
        for r in b['versions']:r['reviewer']='TEST_ONLY_PERSON_B'
        mapping={c['id']:[{'blind_id':'blind1','source_id':'SOURCE_TEST'}],d['id']:[{'blind_id':'blind1','source_id':'SOURCE_TEST'}]}
        r=reviews.compare_exports(a,b,c,d,mapping);self.assertEqual(r['paired_submissions'],1)
        self.assertFalse(r['independence_confirmed']);self.assertIsNone(r['formal_primary_metrics'])
