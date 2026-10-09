'''
report_generator.py
Formats and outputs palindrome detection results.
Contains:
- ReportGenerator: builds a human-readable report, prints it to the
  console, and optionally saves it to a text file.
'''
from datetime import datetime
class ReportGenerator:
    """Produces console and file reports from PalindromeResult lists."""
    def print_console_report(self, results, source="input"):
        """Pretty-print the detection results to stdout."""
        print(self.build_report(results, source))
    def save_file_report(self, results, output_path, source="input"):
        """Write the report to `output_path` as plain text."""
        report = self.build_report(results, source)
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(report)
    def build_report(self, results, source="input"):
        """Return the full multi-line report string."""
        lines = []
        lines.append("=" * 60)
        lines.append("PALINDROME DETECTION REPORT")
        lines.append("=" * 60)
        lines.append(f"Source file : {source}")
        lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        if not results:
            lines.append("No palindromes were found.")
            lines.append("=" * 60)
            return "\n".join(lines)
        word_results = [r for r in results if r.kind == "word"]
        line_results = [r for r in results if r.kind == "line"]
        if word_results:
            lines.append(f"Palindromic words ({len(word_results)} found):")
            lines.append("-" * 60)
            for r in word_results:
                lines.append(
                    f"  Line {r.line_number}, col {r.column}: "
                    f"'{r.original}' (normalized: '{r.normalized}')"
                )
            lines.append("")
        if line_results:
            lines.append(f"Palindromic lines/phrases ({len(line_results)} found):")
            lines.append("-" * 60)
            for r in line_results:
                lines.append(f"  Line {r.line_number}: \"{r.original}\"")
            lines.append("")
        lines.append(self.build_summary(results))
        lines.append("=" * 60)
        return "\n".join(lines)
    def build_summary(self, results):
        """Return a short statistics summary string."""
        word_count = sum(1 for r in results if r.kind == "word")
        line_count = sum(1 for r in results if r.kind == "line")
        total = len(results)
        unique = len({r.normalized for r in results})
        return (
            f"Summary: {total} palindrome(s) detected "
            f"({word_count} word-level, {line_count} line-level); "
            f"{unique} unique normalized form(s)."
        )