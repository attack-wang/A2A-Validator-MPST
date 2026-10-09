"""Palindrome detection utilities."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]")
_WORD = re.compile(r"[A-Za-z0-9']+")


def normalize(text):
    """Lowercase text and strip non-alphanumeric characters."""
    return _NON_ALNUM.sub("", text.lower())


def is_palindrome(text, min_length=2):
    """Return True if normalized text reads the same forwards and backwards."""
    cleaned = normalize(text)
    return len(cleaned) >= min_length and cleaned == cleaned[::-1]


def find_palindromic_words(text, min_length=2):
    """Return unique palindromic words found in text, in order of appearance."""
    seen = set()
    results = []
    for word in _WORD.findall(text):
        key = word.lower()
        if is_palindrome(word, min_length) and key not in seen:
            seen.add(key)
            results.append(key)
    return results


def find_palindromic_phrases(text, min_length=2):
    """Return unique palindromic phrases (whole lines) found in text."""
    seen = set()
    results = []
    for line in text.splitlines():
        cleaned = normalize(line)
        if len(cleaned) >= min_length and cleaned == cleaned[::-1] and cleaned not in seen:
            seen.add(cleaned)
            results.append(line.strip())
    return results