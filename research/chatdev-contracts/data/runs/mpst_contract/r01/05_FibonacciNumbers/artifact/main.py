import sys


def fibonacci_up_to(limit):
    """Generate Fibonacci numbers up to and including the given limit."""
    if limit < 0:
        return []
    result = []
    a, b = 0, 1
    while a <= limit:
        result.append(a)
        a, b = b, a + b
    return result


def main():
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Error: please provide a valid integer limit.")
            sys.exit(1)
    else:
        try:
            limit = int(input("Enter the maximum Fibonacci number: "))
        except ValueError:
            print("Error: please enter a valid integer.")
            sys.exit(1)
        except EOFError:
            print("No input provided; using default limit of 100.")
            limit = 100
    numbers = fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(", ".join(map(str, numbers)))


if __name__ == "__main__":
    main()