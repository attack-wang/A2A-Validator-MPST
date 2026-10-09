'''
report_generator.py
Formatting utilities that turn palindrome analysis results into
human-readable reports for console display or file output.
'''
from datetime import datetime
from file_handler import FileHandler
class ReportGenerator:
    '''
    Produces formatted textual reports from analysis dictionaries
    created by PalindromeDetector.analyze().
    '''
    @staticmethod
    def generate_report(analysis, source_name="input text"):
        '''
        Build a human-readable report from an analysis result.
        Args:
            analysis (dict): Output of PalindromeDetector.analyze().
            source_name (str): Display name of the analyzed source.
        Returns:
            str: The formatted multi-line report.
        '''
        lines = []
        lines.append("=" * 64)
        lines.append("PALINDROME DETECTION REPORT".center(64))
        lines.append("=" * 64)
        lines.append(f"Source:     {source_name}")
        lines.append(f"Generated:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("-" * 64)
        lines.append(f"Words scanned:          {analysis['total_words']}")
        lines.append(f"Sentences scanned:      {analysis['total_sentences']}")
        lines.append(f"Palindromic words:      {analysis['palindrome_count']}")
        lines.append(f"Palindromic phrases:    {len(analysis['palindromic_phrases'])}")
        lines.append(f"Palindromic sentences:  {len(analysis['palindromic_sentences'])}")
        lines.append("-" * 64)
        lines.append("PALINDROMIC WORDS")
        if analysis["palindromic_words"]:
            for entry in analysis["palindromic_words"]:
                lines.append(f"  - {entry['text']}  (word #{entry['position'] + 1})")
        else:
            lines.append("  (none found)")
        lines.append("-" * 64)
        lines.append("PALINDROMIC PHRASES")
        if analysis["palindromic_phrases"]:
            for entry in analysis["palindromic_phrases"]:
                lines.append(
                    f"  - \"{entry['text']}\"  "
                    f"({entry['word_count']} words, starting at word #{entry['start'] + 1})"
                )
        else:
            lines.append("  (none found)")
        lines.append("-" * 64)
        lines.append("PALINDROMIC SENTENCES")
        if analysis["palindromic_sentences"]:
            for entry in analysis["palindromic_sentences"]:
                lines.append(f"  - \"{entry['text']}\"")
        else:
            lines.append("  (none found)")
        lines.append("=" * 64)
        return "\n".join(lines)
    @staticmethod
    def save_report(report, filepath):
        '''
        Save a report to disk as a text file.
        Args:
            report (str): The report text.
            filepath (str): Destination path.
        '''
        FileHandler.write_text_file(filepath, report)