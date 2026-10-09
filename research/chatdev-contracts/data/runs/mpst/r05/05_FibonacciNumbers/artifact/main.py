'''
Module: main.py
This is the entry point of the Fibonacci Number Generator application.
It supports two modes of operation:
  1. Command-line mode:  python main.py 100
  2. Interactive mode:   python main.py  (then follow the prompts)
Robustness notes:
  - Every input() call is guarded against EOFError so the program exits
    gracefully when stdin is closed or empty (e.g., automated test
    harnesses, piped/redirected input, or CI consoles).
  - The top-level handler catches both KeyboardInterrupt and EOFError.
  - Non-interactive stdin is detected up front and a usage message is
    printed instead of entering the interactive loop.
'''
import sys
from fibonacci import generate_fibonacci
from utils import validate_input, format_output
def run(limit):
    """
    Generate and display Fibonacci numbers up to the given limit.
    Args:
        limit (int): The validated upper bound for the sequence.
    """
    numbers = generate_fibonacci(limit)
    print(format_output(numbers, limit))
def stdin_is_interactive():
    """
    Return True if stdin is attached to an interactive terminal.
    Defensive against exotic environments where sys.stdin may be None
    (e.g., pythonw on Windows) or where isatty() may raise.
    """
    try:
        return sys.stdin is not None and sys.stdin.isatty()
    except (AttributeError, ValueError, OSError):
        return False
def main():
    """Orchestrate the application flow (CLI args or interactive loop)."""
    print("=" * 50)
    print("   Welcome to the Fibonacci Number Generator!")
    print("=" * 50)
    # Command-line mode: python main.py <number>
    if len(sys.argv) > 1:
        try:
            limit = validate_input(sys.argv[1])
        except ValueError as error:
            print(f"Invalid command-line argument: {error}")
            print(f"Usage: python {sys.argv[0]} [non-negative integer]")
            sys.exit(1)
        run(limit)
        return
    # Non-interactive stdin (piped, redirected, or closed):
    # do not enter the interactive loop; print usage and exit cleanly.
    if not stdin_is_interactive():
        print("\nNo interactive terminal detected.")
        print(f"Usage: python {sys.argv[0]} [non-negative integer]")
        sys.exit(0)
    # Interactive mode
    while True:
        # Guard the first prompt against a closed/empty stdin stream.
        try:
            raw = input("\nEnter a number to generate Fibonacci numbers up to it: ")
        except EOFError:
            print("\nInput stream closed. Goodbye!")
            break
        try:
            limit = validate_input(raw)
        except ValueError as error:
            print(f"Invalid input: {error}. Please try again.")
            continue
        run(limit)
        # Guard the follow-up prompt the same way.
        try:
            again = input("\nGenerate another sequence? (y/n): ").strip().lower()
        except EOFError:
            print("\nInput stream closed. Goodbye!")
            break
        if again not in ("y", "yes"):
            print("Thank you for using the Fibonacci Number Generator. Goodbye!")
            break
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Graceful exit for Ctrl+C and for any closed/empty stdin condition
        # that escapes the inner guards (defense in depth).
        print("\nProgram interrupted or input closed. Goodbye!")