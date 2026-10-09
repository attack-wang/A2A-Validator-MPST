'''
cli.py
Command-line interface for the Fibonacci Number Generator.
Supports two modes:
    1. Direct mode:      python main.py --limit 100
    2. Interactive mode: python main.py   (prompts for input in a loop)
'''
import argparse
import sys
from fibonacci import generate_fibonacci_up_to, validate_limit
from utils import print_result
EXIT_WORDS = {"quit", "exit", "q"}
def build_parser() -> argparse.ArgumentParser:
    """
    Build and configure the command-line argument parser.
    Returns:
        A configured argparse.ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="fibonacci_app",
        description="Generate Fibonacci numbers up to a given number.",
        epilog="Examples:\n"
               "  python main.py --limit 100\n"
               "  python main.py            (interactive mode)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Note: type is kept as 'str' on purpose so that our own validation
    # (validate_limit) produces friendly, consistent error messages.
    parser.add_argument(
        "-l",
        "--limit",
        type=str,
        default=None,
        metavar="N",
        help="Inclusive upper bound (non-negative integer). "
             "Omit to run in interactive mode.",
    )
    return parser
def run_with_limit(raw_limit: str) -> bool:
    """
    Validate the raw limit, generate the sequence, and print the result.
    Args:
        raw_limit: Raw user input, e.g. "100".
    Returns:
        True on success, False if validation failed.
    """
    try:
        limit = validate_limit(raw_limit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return False
    numbers = generate_fibonacci_up_to(limit)
    print_result(numbers, limit)
    return True
def run_interactive_mode() -> None:
    """
    Run the application in interactive mode.
    Repeatedly prompts the user for an upper bound and prints all Fibonacci
    numbers up to that bound. Exits when the user types 'quit', 'exit' or
    'q', or presses Ctrl+C / Ctrl+D.
    """
    print("=" * 52)
    print("    Fibonacci Number Generator - interactive mode")
    print("=" * 52)
    print("Enter a non-negative integer to list every Fibonacci number")
    print("up to that value. Type 'quit' (or 'exit'/'q') to leave.\n")
    while True:
        try:
            raw = input("Enter a limit (or 'quit' to exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return
        if raw.lower() in EXIT_WORDS:
            print("Goodbye!")
            return
        if not raw:
            print("No input given. Please enter a non-negative integer.\n")
            continue
        if run_with_limit(raw):
            print()  # blank line between successful iterations