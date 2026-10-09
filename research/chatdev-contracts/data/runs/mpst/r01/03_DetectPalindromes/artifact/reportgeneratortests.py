class ReportGeneratorTests(unittest.TestCase):
    def test_generate_contains_statistics(self):
        detector = PalindromeDetector(min_length=2)
        analysis = detector.analyze(['level', 'hello'])
        generator = ReportGenerator(source_name='test.txt')
        report = generator.generate(analysis)
        self.assertIn('Total words analysed      : 2', report)
        self.assertIn('level', report)
    def test_save_report(self):
        ...