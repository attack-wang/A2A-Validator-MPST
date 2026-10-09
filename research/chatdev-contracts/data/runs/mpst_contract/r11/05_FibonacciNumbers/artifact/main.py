"""Generate Fibonacci numbers up to a given number."""


def fibonacci_up_to(limit):
    """Return a list of Fibonacci numbers up to and including limit."""
    if limit < 0:
        return []
    fibs = []
    a, b = 0, 1
    while a <= limit:
        fibs.append(a)
        a, b = b, a + b
    return fibs


def main():
    import sys

    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        try:
            arg = input("Enter a number: ")
        except EOFError:
            print("Error: no input provided.")
            sys.exit(1)

    try:
        limit = int(arg)
    except ValueError:
        print("Error: please provide a valid integer.")
        sys.exit(1)

    result = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, result)))


if __name__ == "__main__":
    main()