'''
main.py
Entry point of the Fibonacci Generator application.
Supports two modes:
  1. One-shot CLI mode:  python main.py 100
  2. Interactive mode:   python main.py
'''
import argparse
import sys
from fibonacci import generate_fibonacci
from utils import parse_limit, format_error
from display import print_result
def run_interactive():
    """Run an interactive loop, prompting the user for limits until quit."""
    print("=" * 50)
    print("      Welcome to the Fibonacci Generator!")
    print("=" * 50)
    print("Enter a non-negative integer to generate all")
    print("Fibonacci numbers up to that value.")
    print("Type 'q', 'quit' or 'exit' to leave.\n")
    while True:
        try:
            raw = input("Enter a limit (or 'q' to quit): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            # Stdin closed (Ctrl+D / piped input) or Ctrl+C: exit gracefully.
            print("\nGoodbye!")
            break
        if raw in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        try:
            limit = parse_limit(raw)
            sequence = generate_fibonacci(limit)
            print_result(limit, sequence)
        except ValueError as exc:
            print(format_error(str(exc)))
        print()
def run_cli(limit):
    """Generate and display Fibonacci numbers for a pre-parsed limit."""
    sequence = generate_fibonacci(limit)
    print_result(limit, sequence)
def main():
    """Parse command-line arguments and dispatch to the proper mode."""
    parser = argparse.ArgumentParser(
        description="Generate all Fibonacci numbers up to a given number."
    )
    parser.add_argument(
        "limit",
        nargs="?",
        default=None,
        help="Non-negative integer limit. Omit it to start interactive mode.",
    )
    args = parser.parse_args()
    if args.limit is None:
        run_interactive()
        return
    try:
        limit = parse_limit(args.limit)
        run_cli(limit)
    except ValueError as exc:
        print(format_error(str(exc)))
        sys.exit(1)
if __name__ == "__main__":
    main()