'''
test_report_generator.py
Unit tests for the ReportGenerator class in report_generator.py.
Verifies report content, formatting, and file saving behaviour.
'''
import os
import tempfile
import unittest
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
class ReportGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.detector = PalindromeDetector(min_length=2)
        self.analysis = self.detector.analyze(['level', 'hello', 'level'])
        self.generator = ReportGenerator(source_name='test.txt')
    def test_generate_contains_statistics(self):
        report = self.generator.generate(self.analysis)
        self.assertIn('Total words analysed      : 3', report)
        self.assertIn('Palindromic words found   : 2', report)
        self.assertIn('Unique palindromes        : 1', report)
        self.assertIn('level', report)
    def test_generate_empty_analysis(self):
        analysis = self.detector.analyze([])
        report = self.generator.generate(analysis)
        self.assertIn('No palindromic words were found.', report)
    def test_generate_respects_top_limit(self):
        analysis = self.detector.analyze(['level', 'noon', 'kayak', 'hello'])
        report = self.generator.generate(analysis, top=2)
        self.assertIn('... and 1 more unique palindromes.', report)
    def test_generate_includes_phrases(self):
        phrases = [{'phrase': 'Step on no pets', 'length': 4, 'sentence': 1}]
        report = self.generator.generate(self.analysis, phrases=phrases)
        self.assertIn('Step on no pets', report)
        self.assertIn('[sentence 1]', report)
    def test_save_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = os.path.join(tmp, 'out', 'report.txt')
            report = self.generator.generate(self.analysis)
            self.generator.save_report(report, output_path)
            self.assertTrue(os.path.exists(output_path))
            with open(output_path, 'r', encoding='utf-8') as handle:
                saved = handle.read()
            self.assertIn('PALINDROME DETECTION REPORT', saved)
            self.assertTrue(saved.endswith('\n'))
if __name__ == '__main__':
    unittest.main()