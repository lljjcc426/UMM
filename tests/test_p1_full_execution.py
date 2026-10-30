import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.p1.full_common import input_fingerprint, validate_scope


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


if __name__ == '__main__':unittest.main()
