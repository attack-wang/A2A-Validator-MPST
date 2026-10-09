"""Detect palindromes in a given text file."""
import re
import sys
from pathlib import Path

SAMPLE = """Level
Hello world
A man, a plan, a canal: Panama
racecar noon kayak
Was it a car or a cat I saw?
Python
"""


def normalize(text: str) -> str:
    """Lowercase and strip non-alphanumeric characters."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def is_palindrome(text: str) -> bool:
    """Return True if text reads the same forwards and backwards."""
    cleaned = normalize(text)
    return len(cleaned) >= 1 and cleaned == cleaned[::-1]


def ensure_input(path: Path) -> bool:
    """Create a demo input file when the default input.txt is missing."""
    if path.is_file():
        return True
    if len(sys.argv) == 1 and path.name == "input.txt":
        path.write_text(SAMPLE, encoding="utf-8")
        print(f"Created sample input file: {path}")
        return True
    return False


def find_palindromes(path: Path):
    """Scan the file line by line and collect palindromic words and phrases."""
    results = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for lineno, line in enumerate(handle, start=1):
            tokens = re.findall(r"[A-Za-z0-9']+", line)
            for word in dict.fromkeys(tokens):
                if is_palindrome(word):
                    results.append((lineno, word))
            phrase = normalize(line)
            if len(tokens) > 1 and len(phrase) >= 3 and phrase == phrase[::-1]:
                results.append((lineno, f"(phrase) {line.strip()}"))
    return results


def main(argv) -> int:
    file_arg = argv[1] if len(argv) > 1 else "input.txt"
    path = Path(file_arg)
    if not ensure_input(path):
        print(f"Error: file not found: {file_arg}")
        return 1
    palindromes = find_palindromes(path)
    if not palindromes:
        print("No palindromes found.")
        return 0
    print(f"Found {len(palindromes)} palindrome(s):")
    for lineno, word in palindromes:
        print(f"  line {lineno}: {word}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))