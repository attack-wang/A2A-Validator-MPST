'''
report_generator.py
Presentation layer for the Palindrome Detector application.
Converts lists of PalindromeMatch objects plus scan statistics into
formatted reports suitable for console display or plain-text file export.
'''
from palindrome_detector import PalindromeMatch
class ReportGenerator:
    """Builds human-readable reports from palindrome scan results."""
    _SEPARATOR = '-' * 72
    @classmethod
    def generate_console_report(cls, matches, stats):
        """Return a color-free, plain report string for console printing."""
        return cls.generate_text_report(matches, stats)