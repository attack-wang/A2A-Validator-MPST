import sys

from palindrome_detector import find_palindromes, format_results


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <text_file>")
        sys.exit(1)
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        print(f"Error reading file: {error}")
        sys.exit(1)
    print(format_results(find_palindromes(text)))


if __name__ == "__main__":
    main()