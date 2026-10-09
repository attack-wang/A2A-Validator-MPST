'''
interactive.py
Interactive console mode for the Fibonacci Number Generator.
Provides a read-eval-print loop in which the user repeatedly enters a
non-negative integer limit and receives the list of Fibonacci numbers up
to that limit. The loop ends when the user types a quit command or sends
an end-of-file / interrupt signal.
'''
from typing import Tuple
from cli import format_sequence
from fibonacci import generate_fibonacci_up_to, parse_limit
QUIT_COMMANDS: Tuple[str, ...] = ("q", "quit", "exit")
PROMPT = "Enter a limit (or 'q' to quit): "
def _print_banner() -> None:
    """Print the welcome banner and short usage instructions."""
    print("=" * 60)
    print("Fibonacci Number Generator - Interactive Mode")
    print("=" * 60)
    print("Enter a non-negative integer limit and the program will list")
    print("every Fibonacci number up to (and including) that value.")
    print(f"Type one of {QUIT_COMMANDS} to leave the program.")
    print("-" * 60)
def _read_input() -> str:
    """
    Read one line of user input.
    Returns
    -------
    str
        The raw input line.
    Raises
    ------
    EOFError
        Propagated when input stream is exhausted (Ctrl+D).
    KeyboardInterrupt
        Propagated on Ctrl+C.
    """
    return input(PROMPT)
def run_interactive() -> int:
    """
    Run the application in interactive mode.
    The user is repeatedly asked for a non-negative integer limit; the
    Fibonacci numbers up to that limit are printed after every valid
    entry. Invalid input produces an error message and a new prompt.
    Returns
    -------
    int
        Exit code (always 0 for a normal session end).
    """
    _print_banner()
    while True:
        try:
            raw = _read_input()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended by user. Goodbye!")
            return 0
        command = raw.strip().lower()
        if command in QUIT_COMMANDS:
            print("Goodbye!")
            return 0
        if not command:
            print("Error: empty input. Please enter a non-negative integer.\n")
            continue
        try:
            limit = parse_limit(raw)
        except ValueError as exc:
            print(f"Error: {exc}\n")
            continue
        numbers = generate_fibonacci_up_to(limit)
        print(f"\nFibonacci numbers up to {limit}:")
        print(format_sequence(numbers))
        print(f"Count: {len(numbers)}\n")