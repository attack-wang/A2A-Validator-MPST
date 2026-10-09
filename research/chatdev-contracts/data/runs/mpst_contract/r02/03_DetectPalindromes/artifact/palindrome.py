"""Palindrome detection utilities."""
import re
from collections import Counter


def normalize(text):
    """Lowercase and keep only Unicode letters and digits."""
    return "".join(ch for ch in text.lower() if ch.isalnum())


def is_palindrome(text, min_length=1):
    """Return True if the normalized text reads the same forwards and backwards."""
    normalized = normalize(text)
    return len(normalized) >= min_length and normalized == normalized[::-1]


def find_word_palindromes(text, min_length=2):
    """Return a Counter mapping each palindromic word to its occurrence count."""
    hits = Counter()
    for word in re.findall(r"[^\W_]+", text, flags=re.UNICODE):
        if is_palindrome(word, min_length):
            hits[word] += 1
    return hits


def find_line_palindromes(text, min_length=2):
    """Return a list of (line_number, line_text) for palindromic lines."""
    results = []
    for number, line in enumerate(text.splitlines(), start=1):
        if is_palindrome(line, min_length):
            results.append((number, line))
    return results