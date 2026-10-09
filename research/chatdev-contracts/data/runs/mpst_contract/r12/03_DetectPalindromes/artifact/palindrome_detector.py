import re
from collections import Counter

WORD_PATTERN = re.compile(r"[A-Za-z0-9]+")


def is_palindrome(token):
    cleaned = token.lower()
    return len(cleaned) >= 2 and cleaned == cleaned[::-1]


def find_palindromes(text):
    tokens = WORD_PATTERN.findall(text)
    return Counter(token for token in tokens if is_palindrome(token))


def format_results(counts):
    total = sum(counts.values())
    if total == 0:
        return "No palindromes found."
    lines = [f"Found {total} palindrome occurrence(s) ({len(counts)} unique):"]
    for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0].lower())):
        lines.append(f"  {word}: {count}")
    return "\n".join(lines)