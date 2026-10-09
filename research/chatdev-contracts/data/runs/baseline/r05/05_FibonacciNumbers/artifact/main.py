'''
Main Module
Entry point of the Fibonacci Number Generator application.
This module orchestrates the overall application flow:
  1. Accepts a limit either as a command-line argument or interactively.
  2. Validates the user input.
  3. Generates Fibonacci numbers up to (and including) the limit.
  4. Displays the results in a readable format.
Usage:
    python main.py        -> interactive mode
    python main.py 100    -> generates Fibonacci numbers up to 100
'''
import sys
from fibonacci import generate_fibonacci
from utils import validate_input, format_output
def get_user_input():
    '''
    Prompt the user until a valid non-negative integer is provided.
    Handles EOFError gracefully (e.g., Ctrl+D or a closed/exhausted
    stdin) by exiting the application cleanly instead of crashing.
    Returns:
        int: The validated limit entered by the user.
    '''
    while True:
        try:
            raw = input("Enter a number to generate Fibonacci numbers up to it: ")
        except EOFError:
            print("\nInput stream closed. Goodbye!")
            sys.exit(0)
        try:
            return validate_input(raw)
        except ValueError as error:
            print(f"Invalid input: {error} Please try again.\n")
def display_fibonacci(limit):
    '''
    Generate and display all Fibonacci numbers up to the given limit.
    Args:
        limit (int): The maximum value (inclusive) for Fibonacci numbers.
    '''
    numbers = generate_fibonacci(limit)
    print(format_output(numbers, limit))
def run_interactive():
    '''
    Run the application in interactive mode.
    Repeatedly asks the user for a limit, displays the Fibonacci
    sequence up to that limit, and asks whether to continue.
    A closed input stream (EOFError) is treated as a "no" answer so
    the loop exits gracefully.
    '''
    print("=" * 50)
    print("  Welcome to the Fibonacci Number Generator!")
    print("=" * 50)
    while True:
        limit = get_user_input()
        display_fibonacci(limit)
        try:
            again = input("\nGenerate another sequence? (y/n): ").strip().lower()
        except EOFError:
            again = 'n'  # treat closed stdin as "no" and exit the loop
        if again != 'y':
            print("\nThank you for using the Fibonacci Number Generator. Goodbye!")
            break
def main():
    '''
    Application entry point.
    If a limit is supplied as a command-line argument, generate and
    display the sequence directly; otherwise fall back to the
    interactive loop.
    '''
    if len(sys.argv) > 1:
        try:
            limit = validate_input(sys.argv[1])
            display_fibonacci(limit)
            return
        except ValueError as error:
            print(f"Invalid argument: {error}")
            print("Falling back to interactive mode.\n")
    run_interactive()
if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        # stdin closed (Ctrl+D / piped input exhausted) or user pressed Ctrl+C:
        # exit cleanly instead of showing a traceback.
        print("\nThank you for using the Fibonacci Number Generator. Goodbye!")