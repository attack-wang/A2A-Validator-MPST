'''
report_generator.py
This module formats and outputs palindrome detection results.
It provides the ReportGenerator class, which can print reports
to the console and save them to a text file.
'''
class ReportGenerator:
    '''
    A class that generates human-readable reports from detection results.
    '''
    def __init__(self, source_name='input'):
        '''
        Initialize the report generator.
        :param source_name: name of the analyzed source (e.g., file name)
        '''
        self.source_name = source_name
    def generate_report(self, results):
        '''
        Build a formatted, multi-line report string from detection results.
        :param results: dictionary returned by PalindromeDetector.detect()
        :return: report as a string
        '''
        lines = []
        lines.append('=' * 60)
        lines.append('PALINDROME DETECTION REPORT')
        lines.append('=' * 60)
        lines.append(f'Source: {self.source_name}')
        lines.append('')
        stats = results.get('statistics', {})
        lines.append('--- Summary ---')
        lines.append(f"Total words analyzed:      {stats.get('total_words', 0)}")
        lines.append(f"Palindromic words found:   {stats.get('palindrome_words', 0)}")
        lines.append(f"Palindromic phrases found: {stats.get('palindrome_phrases', 0)}")
        lines.append('')
        words = results.get('words', [])
        lines.append('--- Palindromic Words ---')
        if words:
            for i, word in enumerate(words, start=1):
                lines.append(f"{i}. '{word['text']}' (length: {word['length']})")
        else:
            lines.append('No palindromic words found.')
        lines.append('')
        phrases = results.get('phrases', [])
        lines.append('--- Palindromic Phrases ---')
        if phrases:
            for i, phrase in enumerate(phrases, start=1):
                lines.append(f"{i}. \"{phrase['text']}\" ({phrase['word_count']} words)")
        else:
            lines.append('No palindromic phrases found.')
        lines.append('')
        lines.append('=' * 60)
        lines.append('END OF REPORT')
        lines.append('=' * 60)
        return '\n'.join(lines)
    def print_report(self, report):
        '''
        Print the report to standard output.
        :param report: report string
        '''
        print(report)
    def save_report(self, report, filepath):
        '''
        Save the report to a text file.
        :param report: report string
        :param filepath: destination path
        :return: the filepath written
        '''
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        return filepath