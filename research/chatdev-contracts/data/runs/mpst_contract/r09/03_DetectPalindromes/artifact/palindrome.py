import re


def is_palindrome(text, ignore_case=True):
    """Return True if text reads the same forwards and backwards.

    Non-alphanumeric characters are ignored.
    """
    cleaned = re.sub(r"[^0-9A-Za-z]", "", text)
    if ignore_case:
        cleaned = cleaned.lower()
    return len(cleaned) > 0 and cleaned == cleaned[::-1]


def find_palindromes(path, ignore_case=True):
    """Scan a text file and return a list of (palindrome, line_number) tuples."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            for token in re.findall(r"\S+", line):
                if is_palindrome(token, ignore_case=ignore_case):
                    results.append((token, line_no))
    return results