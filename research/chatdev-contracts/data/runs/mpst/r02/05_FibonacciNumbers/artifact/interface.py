'''
interface.py
User interaction layer for the Fibonacci Number Generator.
Responsible for prompting the user, validating raw input, displaying
results, and handling quit/continuation flow. Every input() call is
guarded against EOFError so the application exits gracefully when
stdin is closed or exhausted (e.g. non-interactive or piped runs)
instead of crashing with an unhandled traceback.
'''
from utils import parse_non_negative_integer
QUIT_KEYWORDS = {"quit", "q", "exit"}
BANNER_WIDTH = 56
class QuitSignal(Exception):
    """Exception raised when the user chooses to quit the application."""
def print_welcome():
    """Display the application welcome banner."""
    print("=" * BANNER_WIDTH)
    print("     Welcome to the Fibonacci Number Generator!")
    print("=" * BANNER_WIDTH)
def prompt_for_limit():
    """
    Prompt the user for a non-negative integer limit.
    Returns:
        int: The validated non-negative limit.
    Raises:
        QuitSignal: If the user types a quit keyword (quit/q/exit)
                    or if stdin is closed/exhausted (EOFError).
        ValueError: If the input is empty, not an integer, or negative.
    """
    try:
        raw = input("Enter a number to generate Fibonacci numbers up to "
                    "(or 'quit' to exit): ").strip().lower()
    except EOFError:
        # stdin is closed or exhausted (e.g. non-interactive execution):
        # treat it as a quit request so the program exits gracefully.
        raise QuitSignal()
    if raw in QUIT_KEYWORDS:
        raise QuitSignal()
    return parse_non_negative_integer(raw)
def display_results(sequence, limit):
    """
    Display the generated Fibonacci sequence with summary statistics.
    Args:
        sequence (list[int]): Fibonacci numbers <= limit, ascending.
        limit (int): The user-provided upper bound.
    """
    print("=" * BANNER_WIDTH)
    print(f"  Fibonacci numbers up to {limit}:")
    print("=" * BANNER_WIDTH)
    if sequence:
        print("  " + ", ".join(str(number) for number in sequence))
        print("-" * BANNER_WIDTH)
        print(f"  Total count : {len(sequence)}")
        print(f"  Largest     : {sequence[-1]}")
        if sequence[-1] == limit:
            print("  Highlight   : the limit itself is a Fibonacci number!")
    else:
        print("  No Fibonacci numbers found below the given limit.")
    print("=" * BANNER_WIDTH)
def ask_to_continue():
    """
    Ask whether the user wants to generate another sequence.
    Returns:
        bool: True if the user answers yes, False otherwise.
              Also returns False when stdin is closed/exhausted
              (EOFError) so the loop terminates gracefully.
    """
    try:
        answer = input("Generate another sequence? (y/n): ").strip().lower()
    except EOFError:
        # No more input available: do not continue the loop.
        return False
    return answer in ("y", "yes")
def print_goodbye():
    """Display the farewell message."""
    print("Thank you for using the Fibonacci Generator. Goodbye!")