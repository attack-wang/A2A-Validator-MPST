'''
main.py
Entry point for the Fibonacci Generator application.
Supports two modes:
  1. Interactive mode (no arguments): repeatedly prompts the user for a
     non-negative integer and displays all Fibonacci numbers up to it.
  2. Command-line mode:
       python main.py 100        -> Fibonacci numbers up to 100
       python main.py --count 10 -> the first 10 Fibonacci numbers
'''
import argparse
import sys
from fibonacci import FibonacciGenerator, fibonacci_list, fibonacci_up_to_count
from utils import parse_limit, format_sequence, build_summary
def run_interactive():
    """
    Run the application in interactive mode, prompting the user for an
    upper bound until they choose to quit.
    """
    print("=" * 50)
    print("Welcome to the Fibonacci Generator!")
    print("=" * 50)
    print("Enter a non-negative integer to see all Fibonacci")
    print("numbers up to that value. Type 'q' to quit.\n")
    generator = FibonacciGenerator()
    while True:
        try:
            user_input = input("Enter a number (or 'q' to quit): ").strip()
        except EOFError:
            print("\nGoodbye!")
            break
        if user_input.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        try:
            limit = parse_limit(user_input)
        except ValueError as error:
            print(f"Invalid input: {error}\n")
            continue
        generator.set_limit(limit)
        sequence = generator.generate()
        print("\n" + build_summary(sequence, f"limit {limit}"))
        print(format_sequence(sequence))
        print()
def run_with_args(args):
    """
    Run the application using parsed command-line arguments.
    Args:
        args (argparse.Namespace): Parsed CLI arguments.
    """
    if args.count is not None:
        try:
            count = parse_limit(args.count)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        sequence = fibonacci_up_to_count(count)
        print(build_summary(sequence, f"the first {count} numbers"))
        print(format_sequence(sequence))
    else:
        try:
            limit = parse_limit(args.limit)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        sequence = fibonacci_list(limit)
        print(build_summary(sequence, f"limit {limit}"))
        print(format_sequence(sequence))
def build_parser():
    """
    Construct the command-line argument parser.
    Returns:
        argparse.ArgumentParser: Configured parser.
    """
    parser = argparse.ArgumentParser(
        description="Generate Fibonacci numbers up to a given number."
    )
    parser.add_argument(
        "limit",
        nargs="?",
        default=None,
        help="Upper bound (inclusive) for Fibonacci numbers. "
             "Omit to enter interactive mode."
    )
    parser.add_argument(
        "--count",
        default=None,
        help="Generate the first N Fibonacci numbers instead of "
             "using an upper bound (takes precedence over LIMIT)."
    )
    return parser
def main():
    """
    Application entry point: dispatch between CLI mode and interactive mode.
    """
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.limit is None and args.count is None:
            run_interactive()
        else:
            run_with_args(args)
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
if __name__ == "__main__":
    main()