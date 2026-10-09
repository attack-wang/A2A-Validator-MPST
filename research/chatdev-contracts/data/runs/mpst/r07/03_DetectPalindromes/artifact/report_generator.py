'''
ReportGenerator module.
Formats palindrome analysis results into a human-readable report
and provides helpers to print or export them.
'''
class ReportGenerator:
    """Builds formatted text reports from analysis results."""
    def __init__(self, source_name=""):
        self.source_name = source_name
    def generate_report(self, results):
        """Build the full report string."""
        lines = []
        lines.append("=" * 60)
        lines.append("PALINDROME DETECTION REPORT")
        lines.append("=" * 60)
        lines.append(f"Source: {self.source_name}")
        lines.append("")
        words = results.get("word_palindromes", [])
        lines.append(f"Palindromic words found: {len(words)}")
        ...