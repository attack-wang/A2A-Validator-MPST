"""Detect palindromes in a given text file.

Usage: python main.py [path_to_text_file]
If no path is given, defaults to "input.txt".
Reports palindrome words (per line) and fully palindromic lines,
ignoring case and non-alphanumeric characters.
"""

import sys
from pathlib import Path


def normalize(text: str) -> str:
    """Lowercase and keep only alphanumeric characters."""
    return "".join(ch.lower() for ch in text if ch.isalnum())


def is_palindrome(text: str) -> bool:
    """Return True if normalized text reads the same forwards and backwards."""
    cleaned = normalize(text)
    return len(cleaned) > 0 and cleaned == cleaned[::-1]


def find_palindromes(path: str):
    """Scan the file; return (word_hits, line_hits).

    word_hits: list of (line_number, word) for each palindrome word occurrence.
    line_hits: list of (line_number, line_text) for palindromic whole lines.
    """
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    word_hits = []
    line_hits = []
    seen = set()
    for line_no, line in enumerate(lines, start=1):
        if is_palindrome(line):
            line_hits.append((line_no, line.strip()))
        for word in line.split():
            key = normalize(word)
            if key and is_palindrome(word) and (key, line_no) not in seen:
                seen.add((key, line_no))
                word_hits.append((line_no, word))
    return word_hits, line_hits


def main(argv) -> int:
    path = argv[1] if len(argv) > 1 else "input.txt"
    file_path = Path(path)
    if not file_path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1

    word_hits, line_hits = find_palindromes(str(file_path))

    print(f"Palindromes found in '{path}':")

    if word_hits:
        print("\nPalindrome words:")
        for line_no, word in word_hits:
            print(f"  Line {line_no}: {word}")
    else:
        print("\nNo palindrome words found.")

    if line_hits:
        print("\nPalindrome lines:")
        for line_no, text in line_hits:
            print(f"  Line {line_no}: {text}")
    else:
        print("\nNo palindrome lines found.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))