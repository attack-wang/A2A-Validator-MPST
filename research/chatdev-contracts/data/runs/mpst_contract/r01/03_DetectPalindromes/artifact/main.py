import sys
from palindrome import find_palindromes


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <textfile>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    words, lines = find_palindromes(text)

    print(f"Palindromic words ({len(words)}):")
    for w in words:
        print(f"  {w}")

    print(f"Palindromic lines ({len(lines)}):")
    for num, line in lines:
        print(f"  Line {num}: {line}")

    if not words and not lines:
        print("No palindromes found.")


if __name__ == "__main__":
    main()