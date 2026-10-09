'''
report_generator.py
Output module for the Palindrome Detector application.
Contains the ReportGenerator class, which turns a list of
PalindromeMatch objects into a formatted, human-readable report that
can be printed to the console and/or written to a file.
'''
import os
from typing import List, Optional
from palindrome_detector import PalindromeMatch
class ReportGenerator:
    """Builds and delivers formatted palindrome reports."""
    WIDTH = 64
    def __init__(self, show_details: bool = True) -> None:
        """Store whether per-match details (line/offset/length) are shown."""
        self.show_details = show_details
    def format_report(self,
                      matches: List[PalindromeMatch],
                      source_file: str,
                      mode: str,
                      stats: Optional[dict] = None) -> str:
        """Return the complete report as a single string."""
        separator = "=" * self.WIDTH
        thin = "-" * self.WIDTH
        lines = [
            separator,
            "PALINDROME DETECTION REPORT",
            separator,
            "Source file        : {0}".format(source_file),
            "Scan mode          : {0}".format(mode),
        ]
        if stats:
            lines.append("Lines scanned      : {0}".format(stats.get("lines", 0)))
            lines.append("Tokens examined    : {0}".format(stats.get("tokens_scanned", 0)))
        lines.append("Palindromes found  : {0}".format(len(matches)))
        lines.append(thin)
        if not matches:
            lines.append("No palindromes were detected in the given text.")
        else:
            for index, match in enumerate(matches, start=1):
                lines.append("{0:4d}. {1}".format(index, match.text))
                if self.show_details:
                    lines.append("      -> line {0}, offset {1}, length {2}".format(
                        match.line_number, match.start_index, match.length))
        lines.append(separator)
        return "\n".join(lines)
    def print_report(self, report: str) -> None:
        """Print the report to standard output."""
        print(report)
    def save_report(self, report: str, output_path: str) -> None:
        """Write the report to a text file, creating parent dirs if needed."""
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(report + "\n")