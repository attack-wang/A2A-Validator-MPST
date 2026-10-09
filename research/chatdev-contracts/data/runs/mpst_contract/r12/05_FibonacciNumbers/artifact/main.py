import sys

from fibonacci import fibonacci_up_to

DEFAULT_LIMIT = 100


def parse_limit(args):
    """Read the upper limit from a command-line argument or user input."""
    if args:
        source = args[0]
    else:
        try:
            source = input("Enter a number: ")
        except (EOFError, OSError):
            print(f"No input available; using default limit {DEFAULT_LIMIT}.")
            return DEFAULT_LIMIT
    try:
        limit = int(source)
    except ValueError:
        raise SystemExit("Error: please enter a valid integer.")
    if limit < 0:
        raise SystemExit("Error: please enter a non-negative integer.")
    return limit


def main():
    limit = parse_limit(sys.argv[1:])
    fibs = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, fibs)))


if __name__ == "__main__":
    main()