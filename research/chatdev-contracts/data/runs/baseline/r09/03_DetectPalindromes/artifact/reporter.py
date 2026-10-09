'''
reporter.py
Presentation layer for palindrome detection results.
ResultReporter converts the raw analysis dictionary produced by
PalindromeDetector.analyze() into a human-readable report that can be
printed to the console and optionally saved to a text file.
'''
from file_handler import FileHandler
class ResultReporter:
    """Formats, prints and saves palindrome analysis results."""
    WIDTH = 60
    def __init__(self, source_name='input'):
        """
        :param source_name: Human-readable name of the analyzed source
                            (e.g. the input file path) shown in the report.
        """
        self.source_name = source_name
    def build_report(self, analysis):
        """
        Build a multi-line, human-readable report from an analysis result.
        :param analysis: Dictionary returned by PalindromeDetector.analyze().
        :return: The complete report as a single string.
        """
        lines = []
        rule = '=' * self.WIDTH
        lines.append(rule)
        lines.append('PALINDROME DETECTION REPORT')
        lines.append(f'Source: {self.source_name}')
        lines.append(rule)
        lines.append('')
        lines.append('--- Summary ---')
        lines.append(f'Words scanned: {analysis["total_words_scanned"]}')
        lines.append(f'Sentences scanned: {analysis["total_sentences_scanned"]}')
        lines.append(
            f'Palindromic words found: {len(analysis["word_palindromes"])}'
        )
        lines.append(
            f'Palindromic sentences found: {len(analysis["sentence_palindromes"])}'
        )
        whole_text = 'YES' if analysis['whole_text_is_palindrome'] else 'NO'
        lines.append(f'Whole text is a palindrome: {whole_text}')
        lines.append('')
        lines.append('--- Palindromic Words ---')
        if analysis['word_palindromes']:
            for item in analysis['word_palindromes']:
                lines.append(
                    f'  Line {item["line"]}, word #{item["position"]}: '
                    f'"{item["word"]}"'
                )
            unique = ', '.join(analysis['unique_word_palindromes'])
            lines.append(f'  Unique palindromic words: {unique}')
        else:
            lines.append('  (none found)')
        lines.append('')
        lines.append('--- Palindromic Sentences ---')
        if analysis['sentence_palindromes']:
            for item in analysis['sentence_palindromes']:
                lines.append(f'  Line {item["line"]}: "{item["sentence"]}"')
        else:
            lines.append('  (none found)')
        lines.append('')
        lines.append(rule)
        lines.append('END OF REPORT')
        lines.append(rule)
        return '\n'.join(lines)
    def print_report(self, analysis):
        """
        Print the formatted report to standard output.
        :param analysis: Dictionary returned by PalindromeDetector.analyze().
        :return: None
        """
        print(self.build_report(analysis))
    def save_report(self, analysis, output_path):
        """
        Save the formatted report to a text file on disk.
        :param analysis: Dictionary returned by PalindromeDetector.analyze().
        :param output_path: Path of the file to write the report to.
        :return: None
        """
        FileHandler.write_text_file(output_path, self.build_report(analysis))