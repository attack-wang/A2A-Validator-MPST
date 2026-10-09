'''
main.py
Entry point of the Fibonacci Generator application.
Prompts the user for an upper limit, generates all Fibonacci numbers up
to that limit with the FibonacciGenerator class, and displays the results
in a readable report. The user can repeat the process or quit.
'''
from fibonacci import FibonacciGenerator
from utils import get_valid_limit
def format_output(generator, limit):
    """Build a human-readable report of Fibonacci numbers up to limit.
    Args:
        generator (FibonacciGenerator): The generator used to produce values.
        limit (int): The inclusive upper bound requested by the user.
    Returns:
        str: A formatted, multi-line report ready to be printed.
    """
    numbers = generator.generate(limit)
    separator = "=" * 46
    lines = [
        separator,
        f"Fibonacci numbers up to {limit}:",
        separator,
    ]
    if numbers:
        lines.append(", ".join(str(number) for number in numbers))
        # Reuse the already-computed result instead of calling
        # generator.count(limit), which would regenerate the sequence.
        lines.append(f"Total count: {len(numbers)}")
        lines.append(f"Largest value: {numbers[-1]}")
    else:
        lines.append("(no Fibonacci numbers found)")
    lines.append(separator)
    return "\n".join(lines)
def main():
    """Run the interactive Fibonacci Generator application."""
    print("Welcome to the Fibonacci Generator!")
    print("This program lists every Fibonacci number up to a limit you choose.\n")
    generator = FibonacciGenerator()
    while True:
        try:
            limit = get_valid_limit()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. Goodbye!")
            break
        print(format_output(generator, limit))
        try:
            again = input("\nGenerate another sequence? (y/n): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. Goodbye!")
            break
        if again not in ("y", "yes"):
            print("Thank you for using the Fibonacci Generator. Goodbye!")
            break
if __name__ == "__main__":
    main()