class CommandLineTests(unittest.TestCase):
    def test_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = os.path.join(tmp, 'input.txt')
            output_path = os.path.join(tmp, 'report.txt')
            with open(input_path, 'w', encoding='utf-8') as handle:
                handle.write('Level kayak noon hello\n')
            result = subprocess.run(
                [sys.executable, 'main.py', input_path, '-o', output_path],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('level', result.stdout.lower())
            self.assertTrue(os.path.exists(output_path))