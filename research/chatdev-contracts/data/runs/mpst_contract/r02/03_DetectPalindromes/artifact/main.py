"""Command-line tool that detects palindromes in a text file."""
import argparse
import sys

from palindrome import find_line_palindromes, find_word_palindromes


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("file", help="Path to the text file to scan.")
    parser.add_argument("--min-length", type=int, default=2,
                        help="Minimum normalized length for a palindrome (default: 2).")
    parser.add_argument("--mode", choices=("words", "lines", "both"), default="both",
                        help="Scan words, whole lines, or both (default: both).")
    return parser.parse_args(argv)


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def report_words(text, min_length):
    hits = find_word_palindromes(text, min_length)
    if not hits:
        print("No palindromic words found.")
        return
    print(f"Palindromic words ({len(hits)} unique):")
    for word, count in sorted(hits.items(), key=lambda item: (-item[1], item[0].lower())):
        print(f"  {word}: {count} occurrence(s)")


def report_lines(text, min_length):
    hits = find_line_palindromes(text, min_length)
    if not hits:
        print("No palindromic lines found.")
        return
    print(f"Palindromic lines ({len(hits)} found):")
    for number, line in hits:
        print(f"  Line {number}: {line}")


def main(argv=None):
    args = parse_args(argv)
    try:
        text = read_text(args.file)
    except OSError as error:
        print(f"Error: cannot read '{args.file}': {error}", file=sys.stderr)
        return 1
    if args.mode in ("words", "both"):
        report_words(text, args.min_length)
    if args.mode in ("lines", "both"):
        if args.mode == "both":
            print()
        report_lines(text, args.min_length)
    return 0


if __name__ == "__main__":
    sys.exit(main())