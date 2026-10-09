'''
report_generator.py
Module responsible for formatting palindrome analysis results for
console display and text file output.
'''
class ReportGenerator:
    '''
    Formats palindrome analysis results into human-readable reports.
    '''
    def __init__(self, source_filename):
        '''
        Initialize the report generator.
        :param source_filename: Name of the analyzed source file.
        '''
        self.source_filename = source_filename
    def generate_report(self, results):
        '''
        Generate a full text report from analysis results.
        :param results: Dictionary returned by PalindromeDetector.analyze().
        :return: Formatted report string.
        '''
        lines = []
        lines.append("=" * 60)
        lines.append("PALINDROME DETECTION REPORT")
        lines.append("=" * 60)
        lines.append(f"Source file: {self.source_filename}")
        lines.append("")
        word_palindromes = results.get('word_palindromes', [])
        phrase_palindromes = results.get('phrase_palindromes', [])
        lines.append(f"Palindromic words found: {len(word_palindromes)}")
        if word_palindromes:
            lines.append("-" * 60)
            for word, line_number in word_palindromes:
                lines.append(f"  Line {line_number}: \"{word}\"")
        lines.append("")
        lines.append(f"Palindromic phrases found: {len(phrase_palindromes)}")
        if phrase_palindromes:
            lines.append("-" * 60)
            for phrase, line_number in phrase_palindromes:
                lines.append(f"  Line {line_number}: \"{phrase}\"")
        lines.append("")
        total = len(word_palindromes) + len(phrase_palindromes)
        lines.append(f"Total palindromes detected: {total}")
        lines.append("=" * 60)
        return "\n".join(lines)
    def print_report(self, results):
        '''
        Print the report to the console.
        :param results: Dictionary returned by PalindromeDetector.analyze().
        '''
        print(self.generate_report(results))