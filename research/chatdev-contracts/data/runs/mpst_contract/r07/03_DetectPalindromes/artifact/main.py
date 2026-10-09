"""Detect palindromes in a given text file.

Usage:
    python main.py <textfile>
"""

import argparse
import sys

from palindrome import find_palindromic_lines, find_palindromic_words


def read_file(path):
    """Read the whole file as text; exit with an error message on failure."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Error: cannot read '{path}': {exc}", file=sys.stderr)
        sys.exit(1)


def report(path, text):
    """Print all palindromic words and lines found in the text."""
    words = find_palindromic_words(text)
    lines = find_palindromic_lines(text.splitlines(keepends=True))

    print(f"File: {path}")
    if words:
        print(f"Palindromic words ({len(words)}):")
        for word in words:
            print(f"  {word}")
    else:
        print("No palindromic words found.")

    if lines:
        print(f"Palindromic lines ({len(lines)}):")
        for number, line in lines:
            print(f"  Line {number}: {line.strip()}")
    else:
        print("No palindromic lines found.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Detect palindromes in a text file."
    )
    parser.add_argument("file", help="path to the text file to scan")
    args = parser.parse_args(argv)

    text = read_file(args.file)
    report(args.file, text)


if __name__ == "__main__":
    main()