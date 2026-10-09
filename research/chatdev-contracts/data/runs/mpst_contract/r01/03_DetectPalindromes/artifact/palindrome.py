import re


def normalize(s):
    """Lowercase and keep only alphanumeric characters."""
    return re.sub(r"[^0-9a-z]", "", s.lower())


def is_palindrome(s):
    """True if s reads the same forwards and backwards (case/punctuation-insensitive)."""
    n = normalize(s)
    return len(n) >= 2 and n == n[::-1]


def find_palindromes(text):
    """Return (unique palindromic words, (line_number, line) palindromic lines)."""
    words = []
    seen = set()
    for raw in re.findall(r"[A-Za-z0-9']+", text):
        key = raw.lower()
        if is_palindrome(raw) and key not in seen:
            seen.add(key)
            words.append(raw)

    lines = []
    for num, line in enumerate(text.splitlines(), 1):
        if is_palindrome(line):
            lines.append((num, line.strip()))

    return words, lines