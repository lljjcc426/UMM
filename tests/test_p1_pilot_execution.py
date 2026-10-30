"""The pilot operator cannot silently expand the explicitly approved GPU scope."""
import copy
import json
from pathlib import Path
import unittest

from scripts.p1.execute_pilot import validate_scope


class PilotScopeTests(unittest.TestCase):
    def setUp(self):
        self.auth=json.loads(Path('data/research/runs/p1_pilot_kickoff_2026-10-30/authorization.json').read_text())
        rows=json.loads(Path('data/research/plans/p1_baseline_2026-10-30/prepared/requests.json').read_text())
        self.manifest={'pilot_requests':[row for row in rows if row['pilot']]}

    def test_exact_approved_pilot_is_accepted(self):
        self.assertEqual(len(validate_scope(self.auth,self.manifest)),16)

    def test_duplicate_or_expanded_requests_are_rejected(self):
        for rows in [self.manifest['pilot_requests']+[self.manifest['pilot_requests'][0]],
                     [self.manifest['pilot_requests'][0]]*16]:
            with self.subTest(count=len(rows)):
                with self.assertRaises(ValueError):
                    validate_scope(self.auth,{'pilot_requests':rows})

    def test_geometry_or_interface_change_is_rejected(self):
        for key,value in [('geometry_permission','G1'),('task','i2v'),('seed',47)]:
            with self.subTest(field=key):
                manifest=copy.deepcopy(self.manifest)
                manifest['pilot_requests'][0][key]=value
                with self.assertRaises(ValueError):
                    validate_scope(self.auth,manifest)

    def test_unapproved_execution_is_rejected(self):
        self.auth['user_approved']=False
        with self.assertRaises(ValueError):
            validate_scope(self.auth,self.manifest)
