"""Palindrome detection utilities."""


def normalize(text: str) -> str:
    """Lowercase text and keep only alphanumeric characters."""
    return "".join(ch.lower() for ch in text if ch.isalnum())


def is_palindrome(text: str, min_length: int = 1) -> bool:
    """Return True if text is a palindrome, ignoring case and punctuation."""
    cleaned = normalize(text)
    return len(cleaned) >= min_length and cleaned == cleaned[::-1]


def find_palindromes(text: str, mode: str = "words", min_length: int = 1):
    """Yield unique palindromes found in text.

    mode: 'words' checks whitespace-separated tokens,
          'lines' checks whole lines.
    """
    units = text.split() if mode == "words" else text.splitlines()
    seen = set()
    for unit in units:
        if unit not in seen and is_palindrome(unit, min_length):
            seen.add(unit)
            yield unit