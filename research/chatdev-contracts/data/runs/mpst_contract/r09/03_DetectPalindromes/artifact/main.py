import argparse
import sys

from palindrome import find_palindromes


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("file", help="Path to the input text file")
    parser.add_argument("--strict", action="store_true",
                        help="Consider case when checking (default: case-insensitive)")
    args = parser.parse_args(argv)

    ignore_case = not args.strict
    try:
        palindromes = find_palindromes(args.file, ignore_case=ignore_case)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Error: file is not valid UTF-8 text: {args.file}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        return 1

    if not palindromes:
        print("No palindromes found.")
    else:
        print(f"Found {len(palindromes)} palindrome(s):")
        for word, line_no in palindromes:
            print(f"  line {line_no}: {word}")
    return 0


if __name__ == "__main__":
    sys.exit(main())