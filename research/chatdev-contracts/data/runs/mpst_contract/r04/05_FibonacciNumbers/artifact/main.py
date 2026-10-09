"""Generate Fibonacci numbers up to a given number."""

import sys


def fibonacci_up_to(limit):
    """Return a list of Fibonacci numbers less than or equal to limit."""
    if limit < 0:
        return []
    result = []
    a, b = 0, 1
    while a <= limit:
        result.append(a)
        a, b = b, a + b
    return result


def report(limit):
    """Print the Fibonacci numbers up to limit."""
    numbers = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(str(n) for n in numbers) if numbers else "(none)")


def main():
    # Non-interactive mode: accept the limit as a command-line argument.
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Invalid input: please enter an integer.")
            return
        report(limit)
        return

    # Interactive mode: read the limit from stdin, tolerating closed stdin.
    try:
        raw = input("Enter the upper limit: ").strip()
    except EOFError:
        print("\nNo input provided: pass the limit as an argument, e.g. python main.py 100.")
        return
    try:
        limit = int(raw)
    except ValueError:
        print("Invalid input: please enter an integer.")
        return
    report(limit)


if __name__ == "__main__":
    main()