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


def main(argv=None):
    """Accept an optional CLI argument, otherwise prompt interactively."""
    args = sys.argv[1:] if argv is None else argv
    if args:
        try:
            limit = int(args[0])
        except ValueError:
            print("Invalid input: please enter an integer.")
            return 1
    else:
        try:
            limit = int(input("Enter a number: "))
        except EOFError:
            print("\nNo input provided. Usage: python main.py [number]")
            return 0
        except ValueError:
            print("Invalid input: please enter an integer.")
            return 1
    numbers = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, numbers)))
    return 0


if __name__ == "__main__":
    sys.exit(main())