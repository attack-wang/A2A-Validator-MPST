"""Generate Fibonacci numbers up to a given number."""

import sys


def fibonacci_up_to(limit):
    """Return a list of Fibonacci numbers up to and including limit."""
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    result = []
    a, b = 0, 1
    while a <= limit:
        result.append(a)
        a, b = b, a + b
    return result


def parse_limit(raw):
    """Parse an integer limit, returning (limit, error)."""
    try:
        return int(raw), None
    except ValueError:
        return None, "Invalid input. Please enter an integer."


def run(limit):
    """Generate and display Fibonacci numbers up to limit."""
    try:
        fibs = fibonacci_up_to(limit)
    except ValueError as exc:
        print(exc)
        return 1
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, fibs)))
    return 0


def main():
    # Non-interactive mode: python main.py <limit>
    if len(sys.argv) > 1:
        limit, err = parse_limit(sys.argv[1])
        if err:
            print(err)
            return 1
        return run(limit)
    # Interactive mode: prompt for the limit.
    try:
        raw = input("Enter a number: ").strip()
    except EOFError:
        print("\nNo input available (stdin closed).")
        print("Usage: python main.py <limit>   e.g. python main.py 100")
        return 0
    limit, err = parse_limit(raw)
    if err:
        print(err)
        return 1
    return run(limit)


if __name__ == "__main__":
    sys.exit(main())