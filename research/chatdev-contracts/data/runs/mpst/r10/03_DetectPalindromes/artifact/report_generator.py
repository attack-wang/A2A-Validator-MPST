'''
report_generator.py
Formatting and presentation of palindrome detection results.
The ReportGenerator class produces a human-readable report of the
detection run, either printed to the console or written to a
plain-text report file via the FileHandler utility.
'''
from file_handler import FileHandler
class ReportGenerator:
    '''
    Builds formatted reports from palindrome detection results.
    '''
    def __init__(self, detector_info=None):
        '''
        Initialize the report generator.
        Args:
            detector_info (dict): Optional metadata about the detection
                settings (input file, options) shown in the report header.
        '''
        self.detector_info = detector_info or {}
    @staticmethod
    def _header(title):
        '''
        Build a formatted section header.
        Args:
            title (str): The section title.
        Returns:
            str: A header string framed by separator bars.
        '''
        bar = '=' * 60
        return f'{bar}\n{title}\n{bar}'
    def _build_report_lines(self, mode, word_results, line_results, sentence_results, stats):
        '''
        Assemble the report body as a list of text lines.
        Args:
            mode (str): Detection mode used ('words', 'lines',
                'sentences', or 'all'); sections outside the mode are omitted.
            word_results (list): Palindromic words found.
            line_results (list): Palindromic lines found.
            sentence_results (list): Palindromic sentences found.
            stats (dict): Summary statistics about the scan.
        Returns:
            list: The report lines.
        '''
        lines = [self._header('PALINDROME DETECTION REPORT')]
        lines.append('Settings:')
        for key, value in self.detector_info.items():
            lines.append(f'  - {key}: {value}')
        lines.append('')
        lines.append(self._header('SUMMARY'))
        for key, value in stats.items():
            lines.append(f'  {key}: {value}')
        lines.append('')
        if mode in ('words', 'all'):
            lines.append(self._header(f'PALINDROMIC WORDS ({len(word_results)} unique)'))
            if word_results:
                for entry in word_results:
                    lines.append(f"  '{entry['word']}' (occurrences: {entry['count']})")
            else:
                lines.append('  No palindromic words found.')
            lines.append('')
        if mode in ('lines', 'all'):
            lines.append(self._header(f'PALINDROMIC LINES ({len(line_results)} found)'))
            if line_results:
                for entry in line_results:
                    lines.append(f"  Line {entry['line_number']}: {entry['line']}")
            else:
                lines.append('  No palindromic lines found.')
            lines.append('')
        if mode in ('sentences', 'all'):
            lines.append(self._header(f'PALINDROMIC SENTENCES ({len(sentence_results)} found)'))
            if sentence_results:
                for entry in sentence_results:
                    lines.append(f"  Sentence {entry['sentence_number']}: {entry['sentence']}")
            else:
                lines.append('  No palindromic sentences found.')
            lines.append('')
        return lines
    def generate_console_report(self, mode, word_results, line_results, sentence_results, stats):
        '''
        Print a formatted summary of detection results to the console.
        Args:
            mode (str): Detection mode used.
            word_results (list): Palindromic words found.
            line_results (list): Palindromic lines found.
            sentence_results (list): Palindromic sentences found.
            stats (dict): Summary statistics about the scan.
        '''
        report_lines = self._build_report_lines(
            mode, word_results, line_results, sentence_results, stats
        )
        print('\n'.join(report_lines))
    def generate_file_report(self, filepath, mode, word_results, line_results, sentence_results, stats):
        '''
        Write the full detection report to a text file.
        Args:
            filepath (str): Destination path for the report file.
            mode (str): Detection mode used.
            word_results (list): Palindromic words found.
            line_results (list): Palindromic lines found.
            sentence_results (list): Palindromic sentences found.
            stats (dict): Summary statistics about the scan.
        Returns:
            str: The path of the written report file.
        '''
        report_lines = self._build_report_lines(
            mode, word_results, line_results, sentence_results, stats
        )
        content = '\n'.join(report_lines) + '\n'
        return FileHandler.write_text(filepath, content)