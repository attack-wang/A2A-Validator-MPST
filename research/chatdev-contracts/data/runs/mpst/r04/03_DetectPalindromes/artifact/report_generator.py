'''
report_generator.py
Builds human-readable reports from palindrome detection results.
The ReportGenerator class formats summary statistics, the list of unique
palindrome words, and the list of multi-word palindrome phrases into a
single text report suitable for console display or saving to disk.
'''
from datetime import datetime
class ReportGenerator:
    """Builds human-readable reports from palindrome detection results."""
    SEPARATOR = "=" * 72
    SUB_SEPARATOR = "-" * 72
    # Maps stats dictionary keys to human-friendly display labels.
    _SUMMARY_LABELS = (
        ("total_lines", "Total lines"),
        ("total_words", "Total words"),
        ("total_characters", "Total characters"),
        ("unique_palindrome_words", "Unique palindrome words"),
        ("palindrome_word_occurrences", "Palindrome word occurrences"),
        ("unique_palindrome_phrases", "Unique palindrome phrases"),
        ("palindrome_phrase_occurrences", "Palindrome phrase occurrences"),
        ("longest_palindrome", "Longest palindrome"),
    )
    @staticmethod
    def format_settings(settings):
        """Render the detection settings as a compact comma-separated string."""
        parts = [
            "ignore_case={}".format(settings.get("ignore_case", True)),
            "ignore_non_alphanumeric={}".format(settings.get("ignore_non_alphanumeric", True)),
            "min_length={}".format(settings.get("min_length", 2)),
            "max_phrase_words={}".format(settings.get("max_phrase_words", 6)),
            "phrase_detection={}".format(settings.get("phrase_detection", True)),
        ]
        return ", ".join(parts)
    def build_report(self, source_name, word_matches, phrase_matches, stats, settings, max_listed=20):
        """Assemble the full report text from detection results."""
        lines = []
        lines.append(self.SEPARATOR)
        lines.append("PALINDROME DETECTION REPORT")
        lines.append(self.SEPARATOR)
        lines.append("Source file   : {}".format(source_name))
        lines.append("Generated on  : {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lines.append("Settings      : {}".format(self.format_settings(settings)))
        lines.append("")
        lines.append("SUMMARY")
        lines.append(self.SUB_SEPARATOR)
        for key, label in self._SUMMARY_LABELS:
            lines.append("{:<34}: {}".format(label, stats.get(key, "n/a")))
        lines.append("")
        lines.append("PALINDROME WORDS")
        lines.append(self.SUB_SEPARATOR)
        if word_matches:
            lines.extend(self._format_matches(word_matches, max_listed))
        else:
            lines.append("No palindrome words found.")
        lines.append("")
        lines.append("PALINDROME PHRASES")
        lines.append(self.SUB_SEPARATOR)
        if phrase_matches:
            lines.extend(self._format_matches(phrase_matches, max_listed))
        else:
            lines.append("No palindrome phrases found.")
        lines.append("")
        lines.append(self.SEPARATOR)
        lines.append("END OF REPORT")
        lines.append(self.SEPARATOR)
        return "\n".join(lines)
    def _format_matches(self, matches, max_listed):
        """Format PalindromeMatch objects as numbered lines, honouring the display limit."""
        formatted = []
        for index, match in enumerate(matches[:max_listed], start=1):
            formatted.append(
                "{:>3}. {:<42} (line {}, col {}, occurrences: {})".format(
                    index, '"{}"'.format(match.text), match.line_number,
                    match.column, match.occurrences)
            )
        hidden = len(matches) - max_listed
        if hidden > 0:
            formatted.append("... {} more match(es) not shown.".format(hidden))
        return formatted