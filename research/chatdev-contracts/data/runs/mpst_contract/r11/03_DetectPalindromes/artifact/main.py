"""Detect palindromes in a given text file.

Usage:
    python main.py input.txt [--mode words|lines] [--min-length N] [--output out.txt]
"""

import argparse
import sys

from palindrome import find_palindromes


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("file", help="Path to the input text file.")
    parser.add_argument("--mode", choices=("words", "lines"), default="words",
                        help="Check individual words or whole lines (default: words).")
    parser.add_argument("--min-length", type=int, default=1,
                        help="Minimum normalized length to count as a palindrome.")
    parser.add_argument("--output", help="Optional file to write the report to.")
    return parser.parse_args(argv)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        sys.exit(f"Error reading '{path}': {exc}")


def main(argv=None):
    args = parse_args(argv)
    text = read_text(args.file)
    results = list(find_palindromes(text, args.mode, args.min_length))

    lines = [f"Palindromes found: {len(results)}"]
    lines.extend(f"- {item}" for item in results)
    report = "\n".join(lines)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(report + "\n")
        except OSError as exc:
            sys.exit(f"Error writing '{args.output}': {exc}")
    print(report)


if __name__ == "__main__":
    main()