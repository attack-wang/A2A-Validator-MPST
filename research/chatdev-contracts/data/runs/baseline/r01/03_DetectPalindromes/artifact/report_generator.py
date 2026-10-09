'''
Report generation utilities for the Palindrome Detector application.
Formats detection results into readable reports and handles output.
'''
from collections import Counter
def generate_report(matches, source_name, settings_summary=None):
    '''Generate a formatted, human-readable report from detection results.'''
    lines = []
    lines.append("=" * 60)
    lines.append("PALINDROME DETECTION REPORT")
    lines.append("=" * 60)
    lines.append(f"Source file: {source_name}")
    if settings_summary:
        lines.append(f"Settings: {settings_summary}")
    lines.append("")
    if not matches:
        lines.append("No palindromes were found in the given text file.")
    else:
        by_mode = {'line': [], 'phrase': [], 'word': []}
        for m in matches:
            by_mode[m.mode].append(m)
        lines.append(f"Total palindromes found: {len(matches)}")
        lines.append(f"  - Palindromic lines:   {len(by_mode['line'])}")
        lines.append(f"  - Palindromic phrases: {len(by_mode['phrase'])}")
        lines.append(f"  - Palindromic words:   {len(by_mode['word'])}")
        lines.append("")
        # unique palindromes with counts
        counter = Counter(m.text.lower() for m in matches)
        lines.append("Unique palindromes (with occurrence counts):")
        for text, count in counter.most_common():
            lines.append(f"  {text!r} x{count}")
        lines.append("")
        # detailed listing
        lines.append("-" * 60)
        lines.append("Detailed matches:")
        lines.append("-" * 60)
        for i, m in enumerate(matches, 1):
            lines.append(f"[{i}] Mode: {m.mode}")
            lines.append(f"    Line {m.line_number}, columns {m.start_index + 1}-{m.end_index}")
            lines.append(f"    Text: {m.text}")
        lines.append("")
    lines.append("=" * 60)
    lines.append("END OF REPORT")
    lines.append("=" * 60)
    return "\n".join(lines)
def print_report(report):
    '''Print the report to standard output.'''
    print(report)
def save_report(report, filepath):
    '''Save the report to a text file. Returns filepath on success.'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
        f.write("\n")
    return filepath