"""Contract regressions for the real batch's false rejections."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import test_chatdev_content as integration
from content_lab.chatdev_contracts import parse_json_response, smoke_run, startup_evidence


class JsonTransportTests(unittest.TestCase):
    def test_explanatory_prose_and_fence_are_transport_only(self):
        obj = {'verdict': 'finished', 'issues': []}
        self.assertEqual(parse_json_response('Review complete.\n```json\n'+json.dumps(obj)+'\n```'), obj)

    def test_ambiguous_payload_cannot_choose_convenient_verdict(self):
        self.assertIsNone(parse_json_response('{"verdict":"finished","issues":[]}\n'
                                             '{"verdict":"changes_requested","issues":[]}'))

    def test_partial_outer_object_cannot_deliver_nested_result(self):
        self.assertIsNone(parse_json_response('{"unfinished": {"verdict":"finished","issues":[]}'))
        self.assertIsNone(parse_json_response('{"unfinished":\n{"verdict":"finished","issues":[]}'))

    def test_terminal_fence_delivers_final_payload_instead_of_earlier_draft(self):
        text = 'Draft:\n```json\n{"summary":"draft"}\n```\nFinal:\n```json\n{"summary":"final"}\n```'
        self.assertEqual(parse_json_response(text), {'summary':'final'})

    def test_braces_inside_summary_are_not_additional_objects(self):
        obj = {'summary': 'Use {path} and {"a": 1}.'}
        self.assertEqual(parse_json_response('Final: '+json.dumps(obj)), obj)


class LaunchConventionTests(unittest.TestCase):
    def run_source(self, source, timeout=3):
        with TemporaryDirectory() as temporary:
            files = {'main.py': source}
            (Path(temporary)/'main.py').write_text(source, encoding='utf-8')
            evidence = smoke_run(temporary, files, timeout=timeout)
            self.assertEqual(startup_evidence(evidence, files), [])
            return evidence

    def test_required_text_file_is_supplied_without_changing_program(self):
        evidence = self.run_source('import argparse\nfrom pathlib import Path\np = argparse.ArgumentParser()\n'
                                   'p.add_argument("file")\na = p.parse_args()\nprint(Path(a.file).read_text())')
        self.assertEqual(evidence['status'], 'passed')
        self.assertEqual(evidence['profile'], 'text_file_cli')
        self.assertIn('radar', evidence['stdout'])

    def test_cli_crash_with_valid_arguments_still_fails(self):
        evidence = self.run_source('import argparse\np = argparse.ArgumentParser()\np.add_argument("file")\n'
                                   'a = p.parse_args()\nopen(a.file, encoding="utf-8").read()\nraise RuntimeError("broken")')
        self.assertEqual(evidence['status'], 'failed')
        self.assertEqual(evidence['profile'], 'text_file_cli')

    def test_binary_input_does_not_receive_text_fixture(self):
        evidence = self.run_source('import argparse\np = argparse.ArgumentParser()\np.add_argument("file")\n'
                                   'a = p.parse_args()\nopen(a.file, "rb").read()')
        self.assertEqual(evidence['profile'], 'process_exit')
        self.assertEqual(evidence['status'], 'failed')

    def test_unknown_cli_does_not_receive_guessed_arguments(self):
        evidence = self.run_source('import argparse\np = argparse.ArgumentParser()\np.add_argument("server")\np.parse_args()')
        self.assertEqual(evidence['status'], 'failed')
        self.assertEqual(evidence['profile'], 'process_exit')

    def test_stdin_is_explicit_eof(self):
        evidence = self.run_source('import sys\nprint(sys.stdin.read())')
        self.assertEqual(evidence['status'], 'passed')

    def test_no_output_infinite_loop_is_not_startup_success(self):
        self.assertEqual(self.run_source('while True:\n    pass', timeout=0.1)['status'], 'inconclusive')

    def test_real_tk_event_loop_readiness_is_observed(self):
        evidence = self.run_source('import tkinter as tk\nroot = tk.Tk()\ntk.Label(root, text="ready").pack()\nroot.mainloop()')
        self.assertEqual(evidence['status'], 'passed')
        self.assertTrue(evidence['observation']['event_loop_observed'])

    def test_tk_callback_exception_is_not_swallowed(self):
        evidence = self.run_source('import tkinter as tk\nroot = tk.Tk()\ntk.Label(root, text="ready").pack()\n'
                                   'def broken():\n    raise RuntimeError("callback failed")\n'
                                   'root.after(10, broken)\nroot.mainloop()')
        self.assertEqual(evidence['status'], 'failed')


# Exercise the actual phase application path without rerunning inherited cases.
class CanonicalPhaseTests(unittest.TestCase):
    def test_accepted_review_is_canonicalized_before_application(self):
        harness = integration.PhaseIntegrationTests()
        harness.setUp()
        try:
            harness.prefix()
            harness.run_phase(integration.CodeReviewComment, 'Final review:\n```json\n{"verdict":"finished","issues":[]}\n```')
            self.assertEqual(harness.guard.last_review, {'verdict':'finished','issues':[]})
            self.assertEqual(json.loads(harness.env.env_dict['review_comments'])['verdict'], 'finished')
        finally:
            harness.doCleanups()


if __name__ == '__main__':
    unittest.main()
