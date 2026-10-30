import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from scripts.p1.full_common import input_fingerprint, validate_scope
from scripts.p1.execute_full import audit_understanding, main as execute_full


class FullExecutionTests(unittest.TestCase):
    def scope(self):
        rows = json.loads(Path('data/research/plans/p1_baseline_2026-10-30/prepared/requests.json').read_text())
        manifest = dict(generation=rows, understanding=[{'id': f'U{i}'} for i in range(28)],
                        codec=[{'id': f'C{i}'} for i in range(8)], controls=[{'id': f'O{i}'} for i in range(8)])
        auth = dict(user_approved=True, max_extra_GPU_retries=0,
                    approved_ids={k:[r['id'] for r in v] for k,v in manifest.items()},
                    generation_conditions=sorted({r['condition'] for r in rows}), norm_ids=sorted({r['norm_id'] for r in rows}))
        return auth, manifest

    def test_exact_original_matrix(self):
        auth, manifest = self.scope()
        self.assertEqual(len(validate_scope(auth, manifest)['generation']), 64)

    def test_added_or_duplicate_slots_rejected(self):
        for key in ['generation', 'understanding', 'codec', 'controls']:
            auth, manifest = self.scope()
            manifest[key].append(copy.deepcopy(manifest[key][0]))
            with self.assertRaises(ValueError): validate_scope(auth, manifest)

    def test_permission_task_seed_and_approval_rejected(self):
        for field,value in [('seed',99),('seed',29),('task','train'),('geometry_permission','G1_fixed_development_template')]:
            auth, manifest = self.scope();manifest['generation'][0][field]=value
            with self.assertRaises(ValueError): validate_scope(auth, manifest)
        auth,manifest=self.scope();auth['user_approved']=False
        with self.assertRaises(ValueError):validate_scope(auth,manifest)

    def test_asset_relocation_preserves_fingerprint_content_change_does_not(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder);paths=[]
            for name in ['before','after']:
                parent=base/name;parent.mkdir();asset=parent/'blank.png';asset.write_bytes(b'white asset')
                path=parent/'input.json';path.write_text(json.dumps({'1':{'interleave_array':['same prompt',str(asset)],'element_dtype_array':['text','image'],'istarget_in_interleave':[0,0]}}));paths.append(path)
            self.assertEqual(input_fingerprint(paths[0]),input_fingerprint(paths[1]))
            (paths[1].parent/'blank.png').write_bytes(b'target image leakage')
            self.assertNotEqual(input_fingerprint(paths[0]),input_fingerprint(paths[1]))

    def test_actual_understanding_context_and_archived_input(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);bundle=root/'bundle';run=root/'run';attempt=run/'x2t_video'
            for parent in [bundle/'inputs',run/'inputs',attempt/'outputs']:parent.mkdir(parents=True)
            sample={'0001':{'interleave_array':['Observe actual motion.'],'element_dtype_array':['text']}}
            # The native text element is a three-part schema, ending with a withheld placeholder.
            sample['0001']['interleave_array']=['unused',['instruction','Observe actual motion.','Reference answer withheld.']]
            sample['0001']['element_dtype_array']=['text','text']
            for parent in [bundle/'inputs',run/'inputs']:(parent/'x2t_video.json').write_text(json.dumps(sample))
            (attempt/'outputs/result.json').write_text(json.dumps([{'answer':'The motion is unclear.'}]))
            actual={'conditioning_decoded_text':'Observe actual motion.','torch_initial_seed':11}
            (attempt/'actual_understanding_input.json').write_text(json.dumps(actual))
            (attempt/'actual_sampling.json').write_text(json.dumps([{'indices':[0,2]}]))
            row={'task':'x2t_video','seed':11,'input_sha256':input_fingerprint(bundle/'inputs/x2t_video.json')}
            self.assertTrue(audit_understanding(bundle,run,row)['passed'])
            actual['conditioning_decoded_text']='Reference answer withheld.'
            (attempt/'actual_understanding_input.json').write_text(json.dumps(actual))
            self.assertFalse(audit_understanding(bundle,run,row)['passed'])

    def test_failed_attempt_is_not_retried_on_resume(self):
        auth,manifest=self.scope()
        auth['hard_stop_at_utc']=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()
        state={k:[{'id':r['id'],'status':'completed'} for r in rows] for k,rows in manifest.items()}
        state['generation'][0]['status']='failed'
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for name,value in [('authorization',auth),('manifest',manifest),('state',state),('first_request_gate',{'technical_integrity_passed':True})]:
                (root/(name+'.json')).write_text(json.dumps(value))
            with patch('sys.argv',['execute_full','--root',str(root),'--phase','generation']),patch('scripts.p1.execute_full.run_owned') as invoke:
                self.assertEqual(execute_full(),0)
                invoke.assert_not_called()
            self.assertEqual(json.loads((root/'state.json').read_text())['generation'][0]['status'],'failed')


if __name__ == '__main__':unittest.main()
