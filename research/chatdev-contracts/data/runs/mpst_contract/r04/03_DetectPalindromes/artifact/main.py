"""Detect palindromes in a given text file.

Usage:
    python main.py path/to/file.txt
"""

import argparse
import sys

from palindrome_utils import find_palindromes


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("file", help="Path to the text file to scan.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        with open(args.file, "r", encoding="utf-8", errors="replace") as handle:
            lines = handle.readlines()
    except OSError as exc:
        print(f"Error: cannot read '{args.file}': {exc}", file=sys.stderr)
        return 1

    matches = find_palindromes(lines)
    if not matches:
        print("No palindromes found.")
        return 0

    print(f"Found {len(matches)} palindrome(s) in '{args.file}':")
    for lineno, kind, value in matches:
        print(f"  line {lineno}: {kind}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())