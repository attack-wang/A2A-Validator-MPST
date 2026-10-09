'''
report_generator.py
Report output for the Palindrome Detector application.
Provides the ReportGenerator class, which formats the analysis results
produced by PalindromeDetector.analyze() into a human-readable text report
and saves that report to disk. The report contains summary statistics, the
most frequent palindromic words (optionally limited to the top N), and any
palindromic phrases discovered during the scan.
'''
import os
class ReportGenerator:
    """Formats palindrome analysis results into a readable text report."""
    def __init__(self, source_name='input'):
        """
        Create a report generator bound to a source description.
        :param source_name: Name of the analysed file, shown in the report.
        """
        self.source_name = source_name
    def generate(self, analysis, phrases=None, top=10):
        """
        Build the report text from an analysis dictionary.
        :param analysis: Dictionary returned by PalindromeDetector.analyze().
        :param phrases: Optional list of palindromic phrase dictionaries with
                        'phrase', 'length' and 'sentence' keys.
        :param top: Maximum number of unique palindromes to list individually;
                    any remainder is summarised in a trailing line.
        :return: The full report as a string, terminated by a newline.
        """
        stats = analysis['statistics']
        lines = []
        lines.append('PALINDROME DETECTION REPORT')
        lines.append('=' * 40)
        lines.append(f"Source file               : {self.source_name}")
        lines.append('')
        lines.append(f"Total words analysed      : {stats['total_tokens']}")
        lines.append(f"Palindromic words found   : {stats['total_palindromes']}")
        lines.append(f"Unique palindromes        : {stats['unique_palindromes']}")
        lines.append(f"Palindrome ratio          : {stats['palindrome_ratio']:.2%}")
        lines.append('')
        counts = analysis['palindromes']
        if not counts:
            lines.append('No palindromic words were found.')
        else:
            lines.append('Palindromic words:')
            for word, count in counts.most_common(top):
                lines.append(f"  {word} (x{count})")
            if len(counts) > top:
                lines.append(f"... and {len(counts) - top} more unique palindromes.")
        if phrases:
            lines.append('')
            lines.append('Palindromic phrases:')
            for phrase_info in phrases:
                lines.append(
                    f"  \"{phrase_info['phrase']}\" "
                    f"(length {phrase_info['length']}) "
                    f"[sentence {phrase_info['sentence']}]"
                )
        return "\n".join(lines) + "\n"
    def save_report(self, report, output_path):
        """
        Write the report text to `output_path`.
        Parent directories are created automatically when they do not exist.
        """
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as handle:
            handle.write(report)