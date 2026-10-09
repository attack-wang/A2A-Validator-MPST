"""Generate Fibonacci numbers up to a given number."""

import sys


def fibonacci_up_to(limit):
    """Yield Fibonacci numbers less than or equal to limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


def main():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        try:
            raw = input("Enter the upper limit: ")
        except EOFError:
            print("No input provided: supply an integer limit as an argument or via stdin.")
            return
    try:
        limit = int(raw)
    except ValueError:
        print("Invalid input: please enter an integer.")
        return
    if limit < 0:
        print("Please enter a non-negative integer.")
        return
    result = list(fibonacci_up_to(limit))
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, result)))


if __name__ == "__main__":
    main()