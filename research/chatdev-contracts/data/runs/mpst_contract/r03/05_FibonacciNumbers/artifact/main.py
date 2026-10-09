#!/usr/bin/env python3
"""Generate Fibonacci numbers up to a given number."""

import sys

DEFAULT_LIMIT = 100


def fibonacci_up_to(limit: int) -> list:
    """Return a list of all Fibonacci numbers less than or equal to limit."""
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    numbers = []
    a, b = 0, 1
    while a <= limit:
        numbers.append(a)
        a, b = b, a + b
    return numbers


def read_limit() -> int:
    """Get the limit from argv[1] or stdin; fall back to a default on EOF."""
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            print("Error: please provide a valid integer.", file=sys.stderr)
            sys.exit(1)
    try:
        return int(input("Enter the maximum Fibonacci number: "))
    except (EOFError, OSError, RuntimeError):
        print(f"No interactive input available; using default limit {DEFAULT_LIMIT}.")
        return DEFAULT_LIMIT
    except ValueError:
        print("Error: please enter a valid integer.", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    limit = read_limit()

    try:
        result = fibonacci_up_to(limit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, result)))


if __name__ == "__main__":
    main()