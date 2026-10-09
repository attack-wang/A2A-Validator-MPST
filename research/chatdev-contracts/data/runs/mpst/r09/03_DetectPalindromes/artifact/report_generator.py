'''
Report generation and display for the Palindrome Detector.
This module formats detection results into a human-readable report and
provides helpers to display it on the console.
'''
def _format_item_list(items):
    """Format a list of detected items, or a placeholder if empty."""
    if not items:
        return "  (none found)"
    return "\n".join(f"  - {item}" for item in items)
def format_word_results(words):
    """Format the list of palindromic words for the report."""
    return _format_item_list(words)
def format_phrase_results(phrases):
    """Format the list of palindromic phrases for the report."""
    return _format_item_list(phrases)
def format_line_results(lines):
    """Format the list of palindromic lines for the report."""
    return _format_item_list(lines)
def generate_report(results, source_file="input"):
    """
    Generate a human-readable report from detection results.
    :param results: Dictionary returned by PalindromeDetector.detect().
    :param source_file: Name of the analyzed file (for the report header).
    :return: The formatted report as a string.
    """
    stats = results.get("statistics", {})
    lines = [
        "=" * 60,
        "PALINDROME DETECTION REPORT",
        "=" * 60,
        f"Source file: {source_file}",
        "",
        "--- Palindromic Words ---",
        format_word_results(results.get("words", [])),
        "",
        "--- Palindromic Phrases ---",
        format_phrase_results(results.get("phrases", [])),
        "",
        "--- Palindromic Lines ---",
        format_line_results(results.get("lines", [])),
        "",
        "--- Statistics ---",
        f"  Unique palindromic words:    {stats.get('unique_palindrome_words', 0)}",
        f"  Unique palindromic phrases:  {stats.get('unique_palindrome_phrases', 0)}",
        f"  Palindromic lines:           {stats.get('palindrome_lines', 0)}",
        f"  Total palindromes found:     {stats.get('total_palindromes', 0)}",
        "=" * 60,
    ]
    return "\n".join(lines)
def display_report(report):
    """Print the report to the console."""
    print(report)