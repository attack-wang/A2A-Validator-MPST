"""Regression coverage for parser pollution seen in real 30-task responses."""
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'integrations/ChatDev1.0'))
os.environ.setdefault('OPENAI_API_KEY', 'offline-test')
os.environ['CHATDEV_CONTENT_ENABLED'] = 'true'

from camel.typing import ModelType  # initialize legacy import order
from chatdev.codes import Codes
from content_lab.source_files import parse_source_files, SourceExtractionError
from content_lab.chatdev_contracts import ChatDevContracts, ContentViolation


class SourceFileTests(unittest.TestCase):
    def test_analysis_blocks_are_not_guessed_into_files(self):
        response = '''Plan: call Board.copy() and board.is_solved(), e.g. here.
```python
def example():
    pass
```
Board layout:
```
8 | a | b |
```
**main.py**:
```python
print("ready")
```
'''
        self.assertEqual(parse_source_files(response), {'main.py': 'print("ready")'})
        self.assertEqual(Codes(response).codebooks, parse_source_files(response))

    def test_explicit_headers_preserve_names(self):
        for title in ('main.py', '**main.py**:', '`main.py`', '### main.py', 'File: main.py'):
            with self.subTest(title=title):
                self.assertEqual(parse_source_files(title+'\n```python\nprint(42)\n```'), {'main.py':'print(42)'})

    def test_no_filename_inference_from_class_or_main_guard(self):
        self.assertEqual(parse_source_files('Example:\n```python\nclass Widget:\n    pass\n```'), {})
        response = 'helper.py\n```python\nif __name__ == "__main__":\n    print(42)\n```'
        self.assertEqual(list(parse_source_files(response)), ['helper.py'])

    def test_blank_lines_and_case_preserved(self):
        code = 'CODE = 42\n\ndef answer():\n    return CODE'
        self.assertEqual(Codes('MyModule.py\n```python\n'+code+'\n```').codebooks, {'MyModule.py':code})

    def test_named_partial_file_cannot_be_delivered(self):
        response = 'main.py\n```python\nprint(42)\n```\nhelper.py\n```python\ndef incomplete():'
        with self.assertRaises(SourceExtractionError) as found:
            parse_source_files(response)
        self.assertEqual(found.exception.rule, 'output_truncated')

    def test_duplicate_declarations_rejected(self):
        response = 'main.py\n```python\nprint(1)\n```\nmain.py\n```python\nprint(2)\n```'
        with self.assertRaises(SourceExtractionError) as found:
            parse_source_files(response)
        self.assertEqual(found.exception.rule, 'duplicate_source_file')

    def test_declared_paths_still_rejected(self):
        for name in ('../main.py', 'pkg/main.py', 'pkg\\main.py', '.py'):
            with self.subTest(name=name), self.assertRaises(SourceExtractionError):
                parse_source_files(name+'\n```python\nprint(42)\n```')

    def test_missing_source_has_targeted_feedback(self):
        registry = ChatDevContracts()
        context = {'files':{},'phase_env':{},'phase':'Coding','last_review':None,'evidence':None}
        with self.assertRaises(ContentViolation) as found:
            registry.validate('Coding', 'Design discussion.\n```python\ndef draft():\n    pass\n```', context)
        self.assertEqual(found.exception.violations[0].rule, 'missing_source_files')
        self.assertIn('Stop analysis', found.exception.violations[0].repair)

    def test_provider_length_reason_is_explicit_truncation(self):
        registry = ChatDevContracts()
        context = {'files':{},'phase_env':{},'phase':'Coding','last_review':None,'evidence':None}
        with self.assertRaises(ContentViolation) as found:
            registry.validate('Coding', 'main.py\n```python\nprint(42)\n```', context,
                              {'termination_reasons':['length']})
        self.assertEqual(found.exception.violations[0].rule, 'output_truncated')
        self.assertEqual(registry.audit[-1]['termination_reasons'], ['length'])

    def test_codegen_prompt_does_not_ask_for_step_by_step_analysis(self):
        import json
        config = json.loads((ROOT/'integrations/ChatDev1.0/CompanyConfig/MPSTContent/PhaseConfig.json').read_text(encoding='utf-8'))
        for phase in ('Coding','CodeComplete','CodeReviewModification','TestModification'):
            prompt = '\n'.join(config[phase]['phase_prompt'])
            self.assertIn('FINAL SOURCE FILES ONLY', prompt)
            self.assertNotIn('Think step by step', prompt)


if __name__ == '__main__':
    unittest.main()
