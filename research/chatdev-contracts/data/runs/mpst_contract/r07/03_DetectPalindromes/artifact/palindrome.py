"""Palindrome detection utilities."""


def normalize(text):
    """Lowercase text and keep only alphanumeric characters."""
    return "".join(ch.lower() for ch in text if ch.isalnum())


def is_palindrome(text):
    """Return True if text reads the same forwards and backwards.

    Comparison ignores case, spaces, and punctuation. A non-empty
    normalized string is required to count as a palindrome.
    """
    cleaned = normalize(text)
    return len(cleaned) > 0 and cleaned == cleaned[::-1]


def find_palindromic_words(text):
    """Return an ordered list of unique palindromic words found in text."""
    seen = set()
    result = []
    for word in text.split():
        cleaned = normalize(word)
        if cleaned and cleaned not in seen and is_palindrome(cleaned):
            seen.add(cleaned)
            result.append(cleaned)
    return result


def find_palindromic_lines(lines):
    """Return a list of (line_number, line_text) for palindromic lines."""
    return [
        (number, line.rstrip("\n"))
        for number, line in enumerate(lines, start=1)
        if is_palindrome(line)
    ]