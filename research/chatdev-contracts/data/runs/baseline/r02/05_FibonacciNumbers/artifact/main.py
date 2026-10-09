'''
main.py
Entry point of the Fibonacci Generator application.
This module wires everything together: it parses command-line
arguments (or falls back to an interactive prompt), validates the
user-supplied upper limit, delegates the Fibonacci generation to the
`fibonacci` module, and prints a formatted result produced with the
helpers from the `utils` module.
Usage:
    python main.py 100        # non-interactive: numbers up to 100
    python main.py            # interactive mode
'''
import argparse
import sys
from fibonacci import generate_fibonacci_up_to, is_fibonacci
from utils import parse_non_negative_integer, format_output
def show_result(numbers, limit):
    """
    Print the formatted Fibonacci report and an informational note
    when the limit itself is a Fibonacci number.
    This helper is shared by both the interactive and the
    non-interactive modes so their output can never drift apart.
    Args:
        numbers (list[int]): Fibonacci numbers that were generated.
        limit (int): The upper limit that was used.
    """
    print(format_output(numbers, limit))
    if numbers and is_fibonacci(limit):
        print(f"Note: {limit} itself is a Fibonacci number!")
def run_interactive():
    """
    Run the application in interactive mode.
    Repeatedly prompts the user for an upper limit, validates it,
    generates and prints all Fibonacci numbers up to that limit.
    The loop exits when the user types 'q', 'quit', 'exit', or
    presses Ctrl+C / Ctrl+D.
    """
    print("=" * 52)
    print("            Fibonacci Number Generator")
    print("=" * 52)
    print("This program generates every Fibonacci number")
    print("up to (and including) a given number.\n")
    while True:
        try:
            raw = input("Enter the upper limit (non-negative integer), or 'q' to quit: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if raw.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        try:
            limit = parse_non_negative_integer(raw)
        except ValueError as error:
            print(f"Invalid input: {error}\n")
            continue
        numbers = generate_fibonacci_up_to(limit)
        print()
        show_result(numbers, limit)
        print()
def run_with_argument(limit):
    """
    Run the application in non-interactive mode.
    Generates all Fibonacci numbers up to `limit` and prints them.
    Args:
        limit (int): The validated, non-negative upper limit.
    """
    numbers = generate_fibonacci_up_to(limit)
    show_result(numbers, limit)
def build_parser():
    """
    Build and return the command-line argument parser.
    Returns:
        argparse.ArgumentParser: Configured parser for the application.
    """
    parser = argparse.ArgumentParser(
        prog="fibonacci_app",
        description="Generate all Fibonacci numbers up to a given number."
    )
    parser.add_argument(
        "limit",
        nargs="?",
        type=int,
        default=None,
        help="Upper limit (non-negative integer). Omit it to start interactive mode."
    )
    return parser
def main():
    """
    Main entry point of the application.
    Parses command-line arguments and dispatches to either the
    non-interactive mode (when a limit is supplied) or the
    interactive mode (when it is omitted).
    """
    parser = build_parser()
    args = parser.parse_args()
    if args.limit is not None:
        if args.limit < 0:
            print("Error: the limit must be a non-negative integer.", file=sys.stderr)
            sys.exit(1)
        run_with_argument(args.limit)
    else:
        run_interactive()
if __name__ == "__main__":
    main()