"""Generate Fibonacci numbers up to a given number."""

import sys


def fibonacci_up_to(limit):
    """Yield Fibonacci numbers not exceeding the given limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


def parse_limit(args):
    """Read the limit from a command-line argument or interactive input."""
    if len(args) > 1:
        raw = args[1]
    else:
        try:
            raw = input("Enter a number: ").strip()
        except EOFError:
            return None, "No input available: pass the limit as a command-line argument."
    try:
        return int(raw), None
    except ValueError:
        return None, "Invalid input: please enter an integer."


def main(argv):
    limit, error = parse_limit(argv)
    if error:
        print(error)
        return 1
    if limit < 0:
        print("Please enter a non-negative integer.")
        return 1
    numbers = list(fibonacci_up_to(limit))
    print("Fibonacci numbers up to {}:".format(limit))
    print(", ".join(map(str, numbers)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))