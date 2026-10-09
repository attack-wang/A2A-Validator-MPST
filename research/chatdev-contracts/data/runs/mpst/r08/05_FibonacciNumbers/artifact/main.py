'''
main.py
Entry point of the Fibonacci Number Generator application. It wires the
core generator (fibonacci.py) to the console helpers (utils.py) and
supports two modes:
    1. Command-line mode:  python main.py 100  |  python main.py --limit 1000
    2. Interactive mode:   python main.py      (prompts until 'q' is typed)
'''
import argparse
import sys
from fibonacci import FibonacciGenerator
from utils import parse_limit, format_sequence, print_banner, print_summary
def run_with_limit(limit):
    '''
    Generate and display Fibonacci numbers for a validated limit.
    Args:
        limit (int): Non-negative integer upper bound.
    Returns:
        int: Exit status (0 on success).
    '''
    generator = FibonacciGenerator(limit)
    numbers = generator.generate()
    print()
    print("Fibonacci numbers up to {}:".format(limit))
    print(format_sequence(numbers))
    print_summary(numbers)
    return 0
def run_interactive():
    '''
    Run the application in interactive mode.
    Prompts the user for a limit, validates it, and prints the sequence.
    Accepts 'q', 'quit', or 'exit' to leave; invalid input is reported
    and the user is prompted again.
    Returns:
        int: Exit status (0 on success or user exit).
    '''
    print_banner()
    while True:
        try:
            raw = input("\nEnter a limit (non-negative integer, or 'q' to quit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0
        if raw.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            return 0
        try:
            limit = parse_limit(raw)
        except ValueError as error:
            print("Invalid input: {}".format(error))
            continue
        run_with_limit(limit)
def build_parser():
    '''
    Build the command-line argument parser.
    Returns:
        argparse.ArgumentParser: Configured parser for the application.
    '''
    parser = argparse.ArgumentParser(
        prog="fibonacci_app",
        description="Generate Fibonacci numbers up to a given number.",
    )
    parser.add_argument(
        "limit",
        nargs="?",
        default=None,
        help="Upper bound for the Fibonacci numbers (omit for interactive mode).",
    )
    parser.add_argument(
        "--limit",
        dest="limit_flag",
        default=None,
        help="Upper bound for the Fibonacci numbers (alternative to positional).",
    )
    return parser
def main(argv=None):
    '''
    Application entry point.
    Args:
        argv (list[str] or None): Command-line arguments; defaults to
            sys.argv when None.
    Returns:
        int: Process exit code (0 success, 1 on invalid CLI input).
    '''
    args = build_parser().parse_args(argv)
    raw_limit = args.limit if args.limit is not None else args.limit_flag
    if raw_limit is None:
        return run_interactive()
    try:
        limit = parse_limit(raw_limit)
    except ValueError as error:
        print("Error: {}".format(error), file=sys.stderr)
        return 1
    print_banner()
    return run_with_limit(limit)
if __name__ == "__main__":
    sys.exit(main())