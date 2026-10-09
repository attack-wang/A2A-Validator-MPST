#!/usr/bin/env python3
"""Detect palindromes in a given text file."""

import argparse
import re
import sys


def normalize(text):
    """Lowercase text and keep only alphanumeric characters."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def is_palindrome(text, min_length=2):
    """Return True if normalized text is a palindrome of at least min_length chars."""
    cleaned = normalize(text)
    return len(cleaned) >= min_length and cleaned == cleaned[::-1]


def find_palindromes(lines, min_length=2):
    """Return (palindromic words, palindromic lines) found in the file lines."""
    words = set()
    word_pattern = re.compile(r"[A-Za-z0-9]+")
    line_hits = []
    for lineno, line in enumerate(lines, start=1):
        for word in word_pattern.findall(line):
            if is_palindrome(word, min_length):
                words.add(word.lower())
        if is_palindrome(line, min_length):
            line_hits.append((lineno, line.strip()))
    return sorted(words), line_hits


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("file", help="Path to the input text file")
    parser.add_argument("--min-length", type=int, default=2,
                        help="Minimum normalized length for a palindrome (default: 2)")
    args = parser.parse_args(argv)

    try:
        with open(args.file, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except (OSError, ValueError) as exc:
        print(f"Error: cannot read '{args.file}': {exc}", file=sys.stderr)
        return 1

    words, line_hits = find_palindromes(lines, args.min_length)

    print(f"Palindromic words ({len(words)}):")
    for word in words:
        print(f"  {word}")
    print(f"Palindromic lines ({len(line_hits)}):")
    for lineno, text in line_hits:
        print(f"  line {lineno}: {text}")
    if not words and not line_hits:
        print("No palindromes found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())