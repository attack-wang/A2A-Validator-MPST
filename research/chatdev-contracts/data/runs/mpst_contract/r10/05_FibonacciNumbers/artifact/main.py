"""Generate Fibonacci numbers up to a given number."""

import sys

DEFAULT_LIMIT = 100


def fibonacci_up_to(limit):
    """Return a list of all Fibonacci numbers less than or equal to limit."""
    if limit < 0:
        return []
    fibs = []
    a, b = 0, 1
    while a <= limit:
        fibs.append(a)
        a, b = b, a + b
    return fibs


def parse_limit(args):
    """Read the limit from a command-line argument or interactive input."""
    if args:
        raw = args[0]
    else:
        try:
            raw = input("Enter the maximum value: ")
        except EOFError:
            print("No input available; using default limit of "
                  f"{DEFAULT_LIMIT}.")
            return DEFAULT_LIMIT
    try:
        return int(raw)
    except ValueError:
        raise ValueError("limit must be an integer")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        limit = parse_limit(argv)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1
    fibs = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, fibs)) if fibs else "(none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())