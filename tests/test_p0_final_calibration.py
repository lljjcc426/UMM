import json
from pathlib import Path
import struct
import tempfile
import unittest
from contextlib import redirect_stdout
import io
from unittest.mock import patch

import numpy as np

from scripts.p0.casia_subset import parse_pot,parse_wptt
from scripts.p0.final_calibration import render_trajectory,reference_geometry
from scripts.p0.final_review_server import FinalStore,validate


class FinalCalibrationTests(unittest.TestCase):
    def test_POT_records_keep_original_pen_order_and_not_physical_time(self):
        points=[(10,20),(20,30),(-1,0),(50,50),(60,70),(-1,0),(-1,-1)]
        payload=b''.join(struct.pack('<hh',*p) for p in points)
        tag=int.from_bytes('犬'.encode('gbk'),'big');raw=struct.pack('<HIH',8+len(payload),tag,2)+payload
        records=parse_pot(raw)
        self.assertEqual(records[0]['character'],'犬')
        self.assertEqual(records[0]['strokes'],[[[10,20],[20,30]],[[50,50],[60,70]]])
        self.assertNotIn('timestamps',records[0])

    def test_WPTT_line_labels_do_not_create_character_boundaries(self):
        header=struct.pack('<I',12)+b'WPTT\0\0\0\0'
        body=struct.pack('<iiiH',0,16,1,2)+struct.pack('<HHHH',10,20,20,30)
        body+=struct.pack('<HHHH',1,1,0,1)+'犬'.encode('gbk')
        page=parse_wptt(header+body)
        self.assertEqual(page['lines'][0]['text'],'犬')
        self.assertFalse(page['character_boundaries_available'])

    def test_original_bends_final_pixels_and_monotonic_ink_are_preserved(self):
        strokes=[np.array([[20,20],[20,70],[65,70],[65,30]],float),np.array([[80,20],[90,80]],float)]
        masks,_=reference_geometry(strokes);frames=np.asarray(render_trajectory(strokes,'source_order'));ink=frames.min(-1)<128
        self.assertTrue(np.array_equal(ink[-1],masks.any(0)))
        self.assertFalse(np.any(ink[:-1]&~ink[1:]))
        self.assertTrue(np.array_equal(np.asarray(render_trajectory(strokes,'reverse'))[-1],frames[-1]))

    def pack(self):
        task=dict(id='V01',blind_id='F-123456789a',kind='rgb',character='犬',part='validation',writer_id='secret',
            nominal_case='reverse',path='/private/example.png',reference_path='/private/ref.png',frame_timestamps=[0,.08])
        return dict(protocol={'id':'OP_TEST'},tasks=[task],reviewer_orders={'1':['V01'],'2':['V01']})

    def test_blind_payload_hides_case_source_and_private_paths(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.pack();store=FinalStore(p,Path(d));public=store.public(p['tasks'][0])
            for key in ['id','part','writer_id','nominal_case','path','reference_path','AI_v2']:
                self.assertNotIn(key,public)
            self.assertEqual(public['media'],'/media/F-123456789a')

    def test_actual_unknown_and_revisions_remain_separate_for_each_reviewer(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.pack();store=FinalStore(p,Path(d));entry=dict(protocol_id='OP_TEST',reviewer_id='1',kind='rgb',
                blind_id='F-123456789a',decision='unknown',reasons=[],notes='UI_TEST_ONLY')
            store.append('1',entry);store.append('1',dict(entry,decision='correct'))
            self.assertEqual(len((Path(d)/'1.jsonl').read_text().splitlines()),2)
            self.assertEqual(store.state('1')['saved'],1);self.assertEqual(store.state('2')['saved'],0)

    def test_normative_mixed_unknown_is_not_filled_and_wrong_RGB_needs_a_reason(self):
        entry=dict(protocol_id='P',reviewer_id='1',kind='normative',judgments={'identity_order':'pass','direction':'unknown'})
        before=json.dumps(entry);validate(entry,{'kind':'normative'},'P','1');self.assertEqual(json.dumps(entry),before)
        with self.assertRaises(ValueError):validate(dict(protocol_id='P',reviewer_id='1',kind='rgb',decision='incorrect',reasons=[]),{'kind':'rgb'},'P','1')

    def test_paired_collection_keeps_unknown_and_counts_false_accepts_by_writer(self):
        from scripts.p0 import final_calibration as module
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);run=root/'run';private=root/'private';run.mkdir();private.mkdir()
            tasks=[dict(id='N1',kind='normative'),dict(id='N2',kind='normative'),
                dict(id='V1',kind='rgb',norm_id='N1'),dict(id='V2',kind='rgb',norm_id='N2'),dict(id='I1',kind='record')]
            for t in tasks:t.update(blind_id=t['id'],formal=True)
            pack=dict(protocol={'id':'TEST'},tasks=tasks,reviewer_orders={r:[t['id'] for t in tasks] for r in ['1','2']})
            (private/'pack_frozen.json').write_text(json.dumps(pack))
            store=FinalStore(pack,private/'human_records')
            for reviewer in ['1','2']:
                for task in tasks:
                    entry=dict(protocol_id='TEST',reviewer_id=reviewer,blind_id=task['id'],kind=task['kind'],reasons=[])
                    if task['kind']=='normative':entry['judgments']=dict(identity_order='pass',direction='unknown' if task['id']=='N1' else 'pass')
                    elif task['kind']=='rgb':entry.update(decision='correct' if task['id']=='V1' else 'incorrect',reasons=[] if task['id']=='V1' else ['wrong_order'])
                    else:entry['decision']='pass' if reviewer=='1' else 'unknown'
                    store.append(reviewer,entry)
            predictions=[dict(id='V'+str(i),writer_id=str(i),**{m:{'decision':'correct'} for m in ['frozen_observer','AI_v1','AI_v2']}) for i in [1,2]]
            (run/'predictions.jsonl').write_text(''.join(json.dumps(p)+'\n' for p in predictions))
            (run/'pre_review_exposure.json').write_text(json.dumps({'character_named_AI_flag_writer_ids':['2']}))
            output=root/'dated-results';output.mkdir()
            with patch.object(module,'RUN',run),patch.object(module,'PRIVATE',private),redirect_stdout(io.StringIO()):result=module.collect(output_dir=output,records_dir=private/'human_records')
            self.assertTrue((output/'human_calibration_results.json').exists())
            self.assertFalse((run/'human_calibration_results.json').exists())
            self.assertEqual([r['human_reference'] for r in result['video_reference']],['unknown','incorrect'])
            self.assertEqual(result['consensus_counts']['record'],{'unknown':1})
            metric=result['metrics']['frozen_observer']
            self.assertEqual(metric['false_accept_writer_groups'],1)
            self.assertEqual(metric['unknown_reference_accepted'],1)
            self.assertIsNone(metric['prior_AI_character_flag_exclusion']['false_accept_upper95'])
            self.assertFalse(result['P0_auto_pass'])
            self.assertFalse(result['full_per_stroke_timings_inferred'])


if __name__=='__main__':unittest.main()
