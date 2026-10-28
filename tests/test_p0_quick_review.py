import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from urllib.request import urlopen
from http.server import ThreadingHTTPServer

from scripts.p0.quick_review import validate_feedback
from scripts.p0.review_server import ReviewStore, handler_for


class QuickReviewTests(unittest.TestCase):
    def test_scoped_reactions_do_not_generate_or_invert_gold(self):
        entry=dict(protocol_id='QUICK_TEST',type='quick_card',blind_id='Q-01',reviewer_id='1',
                   normative_feedback={'reaction':'agree'},rgb_feedback={'reaction':'disagree'},notes='')
        task=dict(type='quick_card')
        self.assertEqual(validate_feedback(entry,task,'QUICK_TEST'),entry)
        self.assertNotIn('decision',entry)
        # Disagreement carries no assertion that the opposite label is true.
        with self.assertRaises(ValueError):
            validate_feedback(dict(entry,decision='correct'),task,'QUICK_TEST')
        with self.assertRaises(ValueError):
            validate_feedback(dict(entry,rgb_feedback={}),task,'QUICK_TEST')

    def test_dispute_queue_is_small_and_hides_primary_answers(self):
        ai=dict(decision='unknown',facets={},reasons=[],notes='AI',disputed=False,
                observed_order=None,events=[],model_version='TEST',priority='high',
                review_method='test',review_coverage={},evidence=['AI'])
        def card(i):
            norm=dict(blind_id=f'N{i}',type='normative',character='二',batch='quick_cards',ai_suggestion=ai)
            rgb=dict(blind_id=f'V{i}',type='rgb_event',character='二',batch='quick_cards',ai_suggestion=ai)
            return dict(blind_id=f'Q-{i}',type='quick_card',batch='quick_cards',character='二',
                        normative=norm,rgb=rgb,frame_hints=[])
        pack=dict(protocol=dict(id='QUICK_TEST',mode='quick'),batches=dict(quick_cards=[card(1),card(2)]),tutorial=[])
        with tempfile.TemporaryDirectory() as directory:
            store=ReviewStore(pack,Path(directory))
            for i,reaction in [(1,'agree'),(2,'uncertain')]:
                store.append('1',dict(kind='annotation',annotation=dict(blind_id=f'Q-{i}',
                    normative_feedback={'reaction':'agree'},rgb_feedback={'reaction':reaction},notes='PRIMARY PRIVATE NOTE')))
            server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(store))
            thread=Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                with urlopen(f'http://127.0.0.1:{server.server_port}/api/tasks?batch=quick_cards&reviewer=2&disputes=1') as response:
                    raw=response.read().decode();tasks=json.loads(raw)
                self.assertEqual([t['blind_id'] for t in tasks],['Q-2'])
                self.assertNotIn('PRIMARY PRIVATE NOTE',raw)
                self.assertNotIn('rgb_feedback',raw)
                self.assertEqual(store.state('2')['annotations'],[])
            finally:
                server.shutdown();thread.join();server.server_close()


if __name__=='__main__':unittest.main()
