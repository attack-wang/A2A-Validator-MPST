"""Projection-to-execution tests, including unsafe merges and legacy behavior."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import test_chatdev_content as integration
from chatdev.mpst_pilot import ChatDevSessionTypeMonitor
from chatdev.mpst_global import GlobalPilotMonitor
from chatdev.content_guard import ChatDevContentGuard
from content_lab.chatdev_contracts import ChatDevContracts, ContentViolation
from content_lab.protocol_annotations import compile_annotations
from gt_projection import GTProjection

ROOT = Path(__file__).resolve().parents[1]


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / 'example.gt'

    def write(self, protocol):
        self.path.write_text(protocol, encoding='utf-8')

    def monitor(self, callback=None):
        return ChatDevSessionTypeMonitor(self.path, role_map={'A': 'A', 'B': 'B', 'C': 'C'},
            use_default_roles=False, contract_validator=callback)

    def send(self, monitor, sender='A', receiver='B', text='payload', label='result'):
        return monitor.check(SimpleNamespace(target=SimpleNamespace(id=receiver)),
            SimpleNamespace(content=text, message_label=label), SimpleNamespace(id=sender))

    def test_reference_is_preserved_on_both_participants_not_others(self):
        self.write('A -> B : result(ReviewReport) @contract("review.v1"). B -> C : notify. 0')
        monitor = self.monitor(lambda *args: None)
        for role, action in [('A', 'send'), ('B', 'receive')]:
            transition = monitor.validators[role].protocol.get_expected_transitions()[0]
            self.assertEqual(transition.contract_ref, 'review.v1')
            self.assertEqual(transition.payload_schema, 'ReviewReport')
            self.assertEqual(transition.label, 'result')
            self.assertEqual(transition.action.value, action)
        self.assertTrue(all(t.contract_ref is None for state in monitor.validators['C'].protocol.states.values()
                            for t in state.transitions))

    def test_callback_is_automatic_and_rejection_does_not_advance(self):
        self.write('A -> B : result @contract("review.v1"). 0')
        calls = []
        def callback(reference, text, transition, generation):
            calls.append((reference, text, transition['interaction_id']))
            if text == 'bad':
                raise ValueError('rejected')
        monitor = self.monitor(callback)
        before = {role: v.protocol.current_position for role, v in monitor.validators.items()}
        with self.assertRaisesRegex(ValueError, 'rejected'):
            self.send(monitor, text='bad')
        self.assertEqual(before, {r: v.protocol.current_position for r, v in monitor.validators.items()})
        self.send(monitor, text='good')
        self.assertTrue(monitor.is_terminated)
        self.assertEqual([c[0] for c in calls], ['review.v1', 'review.v1'])

    def test_missing_executor_cannot_silently_skip_reference(self):
        self.write('A -> B : result @contract("review.v1"). 0')
        monitor = self.monitor()
        with self.assertRaisesRegex(Exception, 'no contract executor'):
            self.send(monitor)
        self.assertFalse(monitor.is_terminated)

    def test_old_unannotated_protocol_needs_no_executor(self):
        self.write('A -> B : result. 0')
        monitor = self.monitor()
        self.send(monitor)
        self.assertTrue(monitor.is_terminated)

    def test_identical_wire_labels_in_sequence_keep_distinct_contracts(self):
        self.write('A -> B : result @contract("first.v1"). A -> B : result @contract("second.v1"). 0')
        calls = []
        monitor = self.monitor(lambda reference, *args: calls.append(reference))
        self.send(monitor)
        self.send(monitor)
        self.assertEqual(calls, ['first.v1', 'second.v1'])
        self.assertTrue(monitor.is_terminated)

    def test_loop_checks_each_iteration_with_the_same_reference(self):
        self.write('mu t. (A -> B : result @contract("review.v1"). t + A -> B : stop. 0)')
        calls = []
        monitor = self.monitor(lambda reference, *args: calls.append(reference))
        self.send(monitor)
        self.send(monitor)
        self.send(monitor, label='stop')
        self.assertEqual(calls, ['review.v1', 'review.v1'])
        self.assertTrue(monitor.is_terminated)

    def test_branch_preserves_reference_and_wrong_message_order_is_rejected(self):
        self.write('(A -> B : left @contract("left.v1"). 0 + A -> B : right @contract("right.v1"). 0)')
        calls = []
        monitor = self.monitor(lambda reference, *args: calls.append(reference))
        with self.assertRaises(Exception):
            self.send(monitor, sender='B', receiver='A', label='left')
        self.send(monitor, label='right')
        self.assertEqual(calls, ['right.v1'])

    def test_conflicting_enabled_contracts_are_not_merged(self):
        self.write('(A -> B : result @contract("first.v1"). 0 + A -> B : result @contract("second.v1"). 0)')
        monitor = self.monitor(lambda *args: None)
        with self.assertRaisesRegex(Exception, 'Ambiguous'):
            self.send(monitor)

    def test_identical_policy_can_merge_without_losing_occurrence_audit(self):
        compiled, bindings = compile_annotations(
            'A -> B : result @contract("review.v1"). A -> B : result @contract("review.v1"). 0')
        self.assertEqual(len(bindings), 1)
        self.assertEqual(len(next(iter(bindings.values()))['interaction_ids']), 2)

    def test_classical_projection_preserves_reference(self):
        self.write('A -> B : result @contract("review.v1"). 0')
        result = GTProjection('classical').project_protocol(str(self.path), 'example', 'A')
        self.assertIsNone(result['error'])
        self.assertIn('review.v1', result['display_local_protocol'])
        self.assertEqual(len(result['contract_bindings']), 1)

    def test_malformed_annotation_is_not_ignored_by_legacy_parser(self):
        for text in ['A -> B : result @contract(review.v1). 0',
                     'A -> B : result @contract(""). 0',
                     'A -> B : result @contract("review.v1". 0']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                compile_annotations(text)

    def test_type_map_survives_annotation_compilation(self):
        self.write('A -> B : result @contract("integer.v1"). 0')
        self.path.with_suffix('.type.json').write_text('{"result":"int"}', encoding='utf-8')
        monitor = self.monitor(lambda *args: None)
        with self.assertRaises(Exception):
            self.send(monitor, text='not an integer')
        self.send(monitor, text='42')
        self.assertTrue(monitor.is_terminated)


class ChatDevReferenceTests(unittest.TestCase):
    def test_projected_contract_retry_limit_is_used_by_real_roleplaying(self):
        harness = integration.PhaseIntegrationTests()
        harness.setUp()
        self.addCleanup(harness.doCleanups)
        harness.run_phase(integration.DemandAnalysis, 'Application')
        harness.run_phase(integration.LanguageChoose, 'Python')
        harness.guard.contracts.definitions['chatdev.coding.v1']['retry']['max_attempts'] = 2
        session = integration.scripted_session([integration.BAD, integration.BAD, integration.GOOD], None)
        phase = harness.phase(integration.Coding)
        before = deepcopy(harness.guard.monitor.monitor.expected_transitions('Coordinator'))
        with patch('chatdev.phase.RolePlaying', return_value=session), self.assertRaises(ContentViolation):
            phase.execute(harness.env, 1, False)
        self.assertEqual(len(session.assistant_agent.inputs), 2)
        self.assertEqual(harness.env.codes.codebooks, {})
        self.assertEqual(harness.guard.monitor.monitor.expected_transitions('Coordinator'), before)

    def test_unknown_reference_fails_at_startup(self):
        monitor = GlobalPilotMonitor()
        key = next(iter(monitor.monitor.contract_bindings))
        monitor.monitor.contract_bindings[key]['contract_ref'] = 'missing.v1'
        env = SimpleNamespace(codes=SimpleNamespace(codebooks={}))
        with self.assertRaisesRegex(ValueError, 'Unknown protocol contract'):
            ChatDevContentGuard(monitor, env)

    def test_schema_mismatch_fails_at_startup(self):
        monitor = GlobalPilotMonitor()
        key = next(iter(monitor.monitor.contract_bindings))
        monitor.monitor.contract_bindings[key]['payload_schema'] = 'WrongSchema'
        env = SimpleNamespace(codes=SimpleNamespace(codebooks={}))
        with self.assertRaisesRegex(ValueError, 'Payload schema differs'):
            ChatDevContentGuard(monitor, env)

    def test_checks_are_selected_from_reference_not_phase_legacy_checks(self):
        harness = integration.PhaseIntegrationTests()
        harness.setUp()
        self.addCleanup(harness.doCleanups)
        harness.guard.contracts.registry['phases']['Coding']['checks'] = ['python_language']
        harness.run_phase(integration.DemandAnalysis, 'Application')
        harness.run_phase(integration.LanguageChoose, 'Python')
        with self.assertRaises(ContentViolation):
            harness.run_phase(integration.Coding, integration.BAD)
        harness.run_phase(integration.Coding, integration.GOOD)
        audits = [c for c in harness.guard.contracts.audit if c.get('phase') == 'Coding']
        self.assertTrue(any(not c['accepted'] for c in audits))
        self.assertTrue(all(c['trigger'] == 'projected_transition' for c in audits))
        self.assertEqual(harness.env.codes.codebooks['main.py'], 'print("hello")')


if __name__ == '__main__':
    unittest.main()
