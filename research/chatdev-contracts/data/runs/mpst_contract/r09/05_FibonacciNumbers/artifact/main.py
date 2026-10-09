#!/usr/bin/env python3
"""Generate Fibonacci numbers up to a given number."""

import sys

DEFAULT_LIMIT = 100


def fibonacci_up_to(limit):
    """Return a list of all Fibonacci numbers not exceeding limit."""
    if limit < 0:
        return []
    numbers = []
    a, b = 0, 1
    while a <= limit:
        numbers.append(a)
        a, b = b, a + b
    return numbers


def parse_limit(text):
    """Parse a non-negative integer limit; raise ValueError if invalid."""
    value = int(text.strip())
    if value < 0:
        raise ValueError("limit must be non-negative")
    return value


def read_limit(argv):
    """Return raw limit text from argv[1] or interactive input.

    Falls back to DEFAULT_LIMIT when stdin is unavailable (EOFError/OSError).
    """
    if len(argv) > 1:
        return argv[1]
    try:
        return input("Enter the maximum value: ")
    except (EOFError, OSError):
        print(
            f"No interactive input available; using default limit {DEFAULT_LIMIT}.",
            file=sys.stderr,
        )
        return str(DEFAULT_LIMIT)


def main(argv):
    raw = read_limit(argv)
    try:
        limit = parse_limit(raw)
    except ValueError as exc:
        print(f"Error: invalid input ({exc}). Provide a non-negative integer.", file=sys.stderr)
        return 1
    numbers = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, numbers)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))