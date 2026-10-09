"""Generate Fibonacci numbers up to a given number."""

import sys

DEFAULT_LIMIT = 100


def fibonacci_up_to(limit):
    """Return a list of Fibonacci numbers less than or equal to limit."""
    if limit < 0:
        return []
    sequence = []
    a, b = 0, 1
    while a <= limit:
        sequence.append(a)
        a, b = b, a + b
    return sequence


def main():
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Error: please provide a valid integer limit.")
            return 1
    elif sys.stdin is None:
        print(f"No input stream available; using default limit {DEFAULT_LIMIT}.")
        limit = DEFAULT_LIMIT
    else:
        try:
            limit = int(input("Enter a number: "))
        except EOFError:
            print(f"\nNo input available; using default limit {DEFAULT_LIMIT}.")
            limit = DEFAULT_LIMIT
        except ValueError:
            print("Error: please enter a valid integer.")
            return 1

    result = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, result)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())