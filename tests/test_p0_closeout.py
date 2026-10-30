"""Meaningful limited closeout must preserve failures and the human approval gate."""
import copy
import tempfile
import unittest
from pathlib import Path

from scripts.validate_stage_release import validate_release


class LimitedCloseoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evidence.json').write_text('{}')
        self.registry = dict(protocol_id='stroke-video-v2', experiments=[])
        for name, state in [('ENV-01', 'completed'), ('DATA-01', 'completed_with_limitations'),
                            ('EVAL-01', 'completed_negative')]:
            row = dict(id=name, phase='P0', status=state, run_records=['evidence.json'],
                       result_artifacts=['evidence.json'])
            if name != 'ENV-01':
                row['scientific_outcome'] = dict(original_gate_met=False, unmet_criteria=['original criterion'],
                                                 conclusion='bounded negative result')
            self.registry['experiments'].append(row)
        self.manifest = dict(schema_version=2, protocol_id='stroke-video-v2', phase='P0',
            branch='research/p0-stroke-video-foundation', status='closed_with_negative_results',
            conclusion='supported_negative', experiment_ids=['ENV-01', 'DATA-01', 'EVAL-01'],
            evidence_bundle=['evidence.json'], limitations=['original gates failed'], unresolved_blockers=[],
            approval_reference=None, closure=dict(accepted_scope='limited_research_foundation',
                original_scientific_gates_met=False, automatic_scorer_required_for_P1=False,
                scope_approval_reference='evidence.json', original_contract='evidence.json',
                original_release_manifest='evidence.json', final_report='evidence.json',
                formal_evaluation_path=['trusted_normative_reference', 'independent_human_judgments',
                                       'automatic_auxiliary_only', 'strict_unknown_handling'],
                unmet_original_criteria=[dict(experiment_id=n, criterion='original threshold',
                    observed='not met', disposition='documented limit, independent human path')
                    for n in ['DATA-01', 'EVAL-01']]))

    def result(self, merge=False):
        return validate_release(self.manifest, self.registry, self.root, require_ready=merge,
                                head_ref=self.manifest['branch'] if merge else None)

    def test_closed_phase_does_not_claim_scientific_pass_or_merge(self):
        r = self.result()
        self.assertTrue(r['passed'], r['errors'])
        self.assertTrue(r['phase_completed'])
        self.assertFalse(r['original_scientific_gates_met'])
        self.assertFalse(r['merge_authorized'])

    def test_scope_approval_cannot_replace_merge_approval(self):
        r=self.result(merge=True)
        self.assertIn('missing user approval reference', r['errors'])
        self.assertTrue(r['phase_completed'])
        self.assertFalse(r['merge_authorized'])

    def test_final_human_approval_can_release_a_negative_stage(self):
        self.manifest.update(status='ready_for_review', approval_reference='explicit final human science and merge approval')
        self.assertTrue(self.result(merge=True)['passed'])

    def test_relabeling_original_failure_as_pass_is_rejected(self):
        self.registry['experiments'][2]['status'] = 'completed'
        self.assertFalse(self.result()['passed'])
        self.manifest['conclusion'] = 'phase_gate_passed'
        self.assertIn('limited closeout cannot claim original gates passed', self.result()['errors'])

    def test_omitting_failed_original_criteria_is_rejected(self):
        self.manifest['closure']['unmet_original_criteria'] = []
        self.assertFalse(self.result()['passed'])

    def test_missing_original_contract_or_scope_decision_blocks_closeout(self):
        for key in ['original_contract', 'scope_approval_reference']:
            with self.subTest(key=key):
                m = copy.deepcopy(self.manifest)
                m['closure'][key] = 'missing.json'
                self.assertFalse(validate_release(m, self.registry, self.root)['passed'])

    def test_unfinished_experiment_or_missing_evidence_still_blocks(self):
        for field, value in [('status', 'blocked'), ('run_records', [])]:
            with self.subTest(field=field):
                r = copy.deepcopy(self.registry)
                r['experiments'][1][field] = value
                self.assertFalse(validate_release(self.manifest, r, self.root)['passed'])

    def test_human_evaluation_route_cannot_be_removed(self):
        self.manifest['closure']['formal_evaluation_path'] = ['automatic_auxiliary_only']
        self.assertFalse(self.result()['passed'])

    def test_closed_negative_merge_requires_separate_user_authorization(self):
        self.manifest['approval_reference'] = 'evidence.json'
        self.manifest['closure']['user_final_report_review'] = 'approved'
        r = self.result(merge=True)
        self.assertFalse(r['passed'])
        self.assertIn('PR requires ready_for_review', r['errors'])
        self.manifest['closure']['main_merge_authorized'] = True
        r = self.result(merge=True)
        self.assertTrue(r['passed'], r['errors'])
        self.assertTrue(r['merge_authorized'])
        self.assertFalse(r['original_scientific_gates_met'])

    def test_closed_negative_merge_requires_existing_approval_evidence(self):
        self.manifest['approval_reference'] = 'missing-approval.json'
        self.manifest['closure'].update(
            user_final_report_review='approved', main_merge_authorized=True)
        r = self.result(merge=True)
        self.assertFalse(r['passed'])
        self.assertTrue(any('explicit merge approval: evidence file missing' in
                            e for e in r['errors']))
        self.assertFalse(r['merge_authorized'])

    def test_in_progress_metadata_cannot_claim_phase_completion(self):
        self.manifest['status']='in_progress'
        r=self.result()
        self.assertFalse(r['passed'])
        self.assertFalse(r['phase_completed'])
