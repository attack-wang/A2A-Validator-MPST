'''
Report generation for palindrome detection results.
This module formats the results produced by PalindromeDetector into a
clean, human-readable text report that can be printed to the console
or saved to a file. It contains no detection logic of its own.
'''
from datetime import datetime
class ReportGenerator:
    """Builds a formatted text report from palindrome detection results."""
    def __init__(self, source_file=""):
        """
        :param source_file: Name/path of the analyzed file, shown in the header.
        """
        self.source_file = source_file
    def generate(self, word_palindromes, line_palindromes=None):
        """
        Create the complete report as a single string.
        :param word_palindromes: List of dicts from
                                 PalindromeDetector.find_palindrome_words().
        :param line_palindromes: List of dicts from
                                 PalindromeDetector.find_palindrome_lines(),
                                 or None to omit the line section entirely.
        :return: The formatted report text.
        """
        separator = "=" * 60
        lines = [
            separator,
            "PALINDROME DETECTION REPORT",
            separator,
            f"Source file : {self.source_file}",
            f"Generated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "--- Palindromic Words ---",
        ]
        if word_palindromes:
            lines.append(f"{'Word':<20}{'Length':<10}{'First Line':<12}{'Count':<8}")
            lines.append("-" * 50)
            for item in word_palindromes:
                lines.append(
                    f"{item['word']:<20}"
                    f"{len(item['clean']):<10}"
                    f"{item['line']:<12}"
                    f"{item['count']:<8}"
                )
            lines.append(f"\nTotal unique palindromic words: {len(word_palindromes)}")
        else:
            lines.append("No palindromic words found.")
        if line_palindromes is not None:
            lines.append("")
            lines.append("--- Palindromic Lines ---")
            if line_palindromes:
                for item in line_palindromes:
                    lines.append(f"Line {item['line_number']}: {item['text']}")
                lines.append(f"\nTotal palindromic lines: {len(line_palindromes)}")
            else:
                lines.append("No palindromic lines found.")
        lines.extend(["", separator, "End of report", separator])
        return "\n".join(lines)