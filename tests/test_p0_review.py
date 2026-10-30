"""Review integrity: blind media, independent facets and preserved human history."""
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer

import numpy as np
from PIL import Image, ImageSequence

from scripts.p0.prepare_acceptance import FACETS, RUN
from scripts.p0.review_server import ReviewStore, blind_png, public_task, validate_annotation, handler_for


class ReviewIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.pack=json.loads((RUN/'review_draft.json').read_text())
        self.rgb=self.pack['batches']['practice_rgb'][0]

    def test_blind_media_preserves_all_RGB_frames_and_durations(self):
        original=Path('examples/p0_data_eval/correct.png').read_bytes()
        served=blind_png(original)
        def decode(raw):
            with Image.open(io.BytesIO(raw)) as image:
                return [(np.asarray(frame.convert('RGB')).copy(),frame.info.get('duration'))
                        for frame in ImageSequence.Iterator(image)]
        left,right=decode(original),decode(served)
        self.assertEqual(len(left),len(right))
        for (a,ta),(b,tb) in zip(left,right):
            self.assertTrue(np.array_equal(a,b)); self.assertEqual(ta,tb)
        self.assertNotIn(b'sample_id',served)
        self.assertIn(b'Arphic Public License',served)
        self.assertIn(b'copyright (C) 1999',served)

    def test_payload_omits_case_and_reference_order_for_RGB(self):
        result=public_task(self.rgb)
        for key in ['case','renderer','role','original_id','expected','source_group_id','candidate_strokes']:
            self.assertNotIn(key,result)
        self.assertTrue(result['media'].startswith('/media/R-'))

    def test_process_error_and_unknown_order_can_coexist_without_relabel(self):
        entry=dict(protocol_id=self.pack['protocol']['id'],type='rgb_event',decision='incorrect',
            facets={k:'unknown' for k in FACETS['rgb_event']},reasons=['temporal_ambiguity'],
            notes='实际过程没有逐笔形成；顺序无法观察',disputed=True)
        before=json.dumps(entry,ensure_ascii=False)
        validate_annotation(entry,self.rgb,self.pack['protocol']['id'])
        self.assertEqual(json.dumps(entry,ensure_ascii=False),before)

    def test_revisions_and_reviewers_are_separate_and_holdout_preview_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            store=ReviewStore(self.pack,Path(directory),preview=True)
            for decision in ['unknown','incorrect']:
                store.append('1',dict(kind='annotation',annotation=dict(blind_id=self.rgb['blind_id'],decision=decision)))
            self.assertEqual(len(store.events('1')),2)
            self.assertEqual(store.state('1')['annotations'][0]['decision'],'incorrect')
            self.assertEqual(store.state('2')['annotations'],[])
            with self.assertRaises(ValueError): store.allowed_batch('holdout_rgb','1')

    def test_existing_export_was_not_given_formal_or_facet_credit(self):
        audit=json.loads((RUN/'legacy_annotation_audit.json').read_text())
        self.assertEqual(audit['raw_records'],38)
        self.assertEqual(audit['formal_RGB_count'],0)
        self.assertTrue(all(not r['formal_eligible'] for r in audit['normalized_records']))
        hole=next(c for c in audit['character_coverage'] if c['character']=='穴')
        self.assertEqual(hole['rgb_global_records'],10)
        self.assertEqual([m['construction_case'] for m in hole['rgb_cases_missing']],['swap'])

    def test_own_export_restores_progress_to_fresh_store_without_new_judgments(self):
        # Standalone toy IDs only; no real holdout record or media is inspected.
        pack=dict(protocol={'id':'TEST_PROTOCOL'},tutorial=[],batches={
            'practice_norm':[dict(blind_id='TEST_PN',type='normative',batch='practice_norm')],
            'practice_rgb':[dict(blind_id='TEST_PR',type='rgb_event',batch='practice_rgb')],
            'holdout_norm':[dict(blind_id='TEST_FN',type='normative',batch='holdout_norm')],
            'holdout_rgb':[]})
        entries=[]
        for batch in pack['batches'].values():
            for task in batch:
                entries.append(dict(protocol_id='TEST_PROTOCOL',blind_id=task['blind_id'],type=task['type'],
                    reviewer_id='UI_TEST_RESTORE',decision='unverified' if task['type']=='normative' else 'unknown',
                    facets={k:'unknown' for k in FACETS[task['type']]},notes='UI_TEST_ONLY',reasons=[],disputed=False))
        original=json.dumps(entries)
        with tempfile.TemporaryDirectory() as directory:
            store=ReviewStore(pack,Path(directory))
            server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(store))
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                progress=dict(batch='holdout_norm',index=0)
                payload=dict(reviewer_id='UI_TEST_RESTORE',payload=dict(schema='p0-human-annotations-v2',annotations=entries,onboarded=True,progress=progress))
                request=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/api/import',
                    data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(request) as response: result=json.load(response)
                self.assertEqual(result['imported'],3)
                restored=store.state('UI_TEST_RESTORE')
                self.assertTrue(restored['onboarded'])
                self.assertEqual(json.dumps(restored['annotations']),original)
                self.assertEqual(restored['progress'],progress)
            finally:
                server.shutdown();server.server_close();thread.join()


if __name__=='__main__':
    unittest.main()
