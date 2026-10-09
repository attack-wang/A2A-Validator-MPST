"""Utilities for detecting palindromes in text."""

import re


def normalize(text):
    """Lowercase text and keep only alphanumeric characters."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def is_palindrome(text):
    """Return True if text reads the same forwards and backwards."""
    cleaned = normalize(text)
    return len(cleaned) > 0 and cleaned == cleaned[::-1]


def find_palindromes(lines):
    """Scan lines and return (line_number, kind, value) for each palindrome.

    Detects palindrome words (normalized length > 1, reported once each) and
    whole-line phrase palindromes that ignore punctuation, spacing, and case.
    """
    results = []
    seen_words = set()
    for lineno, line in enumerate(lines, start=1):
        for word in re.findall(r"[A-Za-z0-9']+", line):
            cleaned = normalize(word)
            if len(cleaned) > 1 and cleaned == cleaned[::-1] and cleaned not in seen_words:
                seen_words.add(cleaned)
                results.append((lineno, "word", word))
        if len(normalize(line)) > 1 and is_palindrome(line):
            results.append((lineno, "phrase", line.strip()))
    return results