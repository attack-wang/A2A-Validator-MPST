#!/usr/bin/env python3
"""Detect palindromes in a given text file."""

import sys


def normalize(text):
    """Return lowercase alphanumeric-only version of text."""
    return "".join(ch.lower() for ch in text if ch.isalnum())


def is_palindrome(text):
    """Return True if normalized text is a non-empty palindrome."""
    cleaned = normalize(text)
    return len(cleaned) > 0 and cleaned == cleaned[::-1]


def find_palindromes(lines):
    """Yield (line_number, word) for each palindrome word found."""
    for line_number, line in enumerate(lines, start=1):
        for word in line.split():
            if is_palindrome(word):
                yield line_number, word


def main(argv):
    if len(argv) != 2:
        print("Usage: python main.py <text_file>", file=sys.stderr)
        return 1
    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: cannot read {path}: {exc}", file=sys.stderr)
        return 1
    if not lines:
        print(f"File '{path}' is empty; no palindromes detected.")
        return 0
    found = list(find_palindromes(lines))
    if not found:
        print("No palindromes detected.")
        return 0
    for line_number, word in found:
        print(f"Line {line_number}: {word}")
    print(f"Total palindromes detected: {len(found)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))