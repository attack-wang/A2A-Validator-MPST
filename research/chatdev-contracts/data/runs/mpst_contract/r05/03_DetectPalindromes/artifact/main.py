"""Detect palindromes in a text file.

Usage:
    python main.py <file> [--min-length N] [--phrases] [--all]
"""

import argparse
import sys

from palindromes import find_palindromic_phrases, find_palindromic_words, is_palindrome


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError as exc:
        sys.exit(f"Error reading '{path}': {exc}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("file", help="Path to the text file to scan.")
    parser.add_argument("--min-length", type=int, default=2,
                        help="Minimum normalized length to count as a palindrome (default: 2).")
    parser.add_argument("--phrases", action="store_true",
                        help="Also report palindromic phrases (whole lines).")
    parser.add_argument("--all", action="store_true",
                        help="Report only lines that are themselves palindromes.")
    args = parser.parse_args(argv)

    text = read_file(args.file)

    if args.all:
        hits = [line.strip() for line in text.splitlines()
                if is_palindrome(line, args.min_length)]
        print(f"Palindromic lines in '{args.file}': {len(hits)}")
        for line in hits:
            print(f"  - {line}")
        return 0

    words = find_palindromic_words(text, args.min_length)
    print(f"Palindromic words in '{args.file}': {len(words)}")
    for word in words:
        print(f"  - {word}")

    if args.phrases:
        phrases = find_palindromic_phrases(text, args.min_length)
        print(f"Palindromic phrases in '{args.file}': {len(phrases)}")
        for phrase in phrases:
            print(f"  - {phrase}")

    return 0


if __name__ == "__main__":
    sys.exit(main())