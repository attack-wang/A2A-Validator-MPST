'''
Report generation module.
Contains the ReportGenerator class, which converts raw detection
findings and statistics into a formatted, human-readable report that
can be printed to the console or written to a file.
'''
from datetime import datetime
class ReportGenerator:
    '''Formats palindrome detection results into readable reports.'''
    HEADER_TITLE = "PALINDROME DETECTION REPORT"
    SEPARATOR_WIDTH = 62
    def __init__(self, source_name="unknown"):
        '''Remember which input file the report describes.'''
        self.source_name = source_name
    def generate(self, findings, statistics):
        '''Build and return the complete report as a single string.'''
        separator = "=" * self.SEPARATOR_WIDTH
        lines = [
            separator,
            self.HEADER_TITLE,
            separator,
            f"Source file : {self.source_name}",
            f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "--- Summary ---",
            f"Total palindromes found : {statistics['total_palindromes']}",
            f"  Palindromic words     : {statistics['total_words']}",
            f"  Palindromic phrases   : {statistics['total_phrases']}",
            f"Unique palindromes      : {statistics['unique_palindromes']}",
        ]
        if statistics["most_frequent"]:
            word, count = statistics["most_frequent"]
            lines.append(f"Most frequent           : '{word}' ({count} occurrence(s))")
        if statistics["longest"]:
            lines.append(
                f"Longest palindrome      : '{statistics['longest']}' "
                f"({len(statistics['longest'])} characters)"
            )
        lines.extend(["", "--- Detailed findings ---"])
        if not findings:
            lines.append("No palindromes were found in the given text.")
        else:
            for finding in findings:
                lines.append(self._format_finding(finding))
        lines.append(separator)
        return "\n".join(lines)
    @staticmethod
    def _format_finding(finding):
        '''Format one single finding as one report line.'''
        kind = "word" if finding["type"] == "word" else "phrase"
        return (
            f"Line {finding['line']:>4}, Col {finding['column']:>3} | "
            f"{kind:>6} | {finding['text']}"
        )
    @staticmethod
    def print_report(report):
        '''Print a finished report to standard output.'''
        print(report)