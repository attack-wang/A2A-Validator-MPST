'''
cli.py
This module handles all user interaction for the Fibonacci Number
Generator application. It provides functions to prompt the user for
a valid upper limit, display the generated Fibonacci numbers in a
readable format, and manage the interactive session loop. All input
calls are defensively wrapped so that a closed stdin stream (EOFError)
or a keyboard interrupt (KeyboardInterrupt) terminates the program
gracefully instead of crashing with an unhandled traceback.
'''
from fibonacci import generate_fibonacci, validate_limit
def safe_input(prompt):
    '''
    Prompt the user for input while handling stream/interrupt errors.
    Wraps the built-in input() call so that a closed or exhausted
    stdin stream (EOFError) or a keyboard interrupt (KeyboardInterrupt)
    results in a clean shutdown signal instead of an unhandled
    exception propagating up and crashing the application.
    Args:
        prompt (str): The prompt text to display to the user.
    Returns:
        str or None: The user's input as a string, or None if the
                     input stream is closed or interrupted.
    '''
    try:
        return input(prompt)
    except EOFError:
        print("\nInput stream closed. Exiting.")
        return None
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        return None
def get_user_input():
    '''
    Prompt the user to enter the upper limit for Fibonacci generation.
    Repeatedly asks for input until a valid non-negative integer
    is provided. If the input stream is closed (EOF) or the user
    interrupts, the program exits gracefully with status code 0.
    Returns:
        int: The validated non-negative upper limit entered by the user.
    '''
    while True:
        raw_value = safe_input("Enter the upper limit for Fibonacci numbers: ")
        if raw_value is None:
            raise SystemExit(0)
        try:
            limit = validate_limit(raw_value)
            return limit
        except ValueError as error:
            print(f"Error: {error} Please try again.")
def display_results(fibonacci_numbers, limit):
    '''
    Display the generated Fibonacci numbers in a formatted table.
    Args:
        fibonacci_numbers (list): The list of Fibonacci numbers to display.
        limit (int): The upper limit that was used for generation.
    '''
    print("\n" + "=" * 50)
    print(f"Fibonacci numbers up to {limit}:")
    print("=" * 50)
    if not fibonacci_numbers:
        print("No Fibonacci numbers found within the given limit.")
    else:
        for index, number in enumerate(fibonacci_numbers, start=1):
            print(f"{index:>3}. {number}")
        print("-" * 50)
        print(f"Total count: {len(fibonacci_numbers)}")
    print("=" * 50 + "\n")
def run_cli():
    '''
    Run the interactive command-line interface session.
    Greets the user, then repeatedly prompts for an upper limit,
    generates the Fibonacci numbers up to that limit, and displays
    the results until the user chooses to quit. EOF or interrupts
    on any prompt terminate the session gracefully.
    '''
    print("=" * 50)
    print("  Welcome to the Fibonacci Number Generator!")
    print("=" * 50)
    while True:
        limit = get_user_input()
        fibonacci_numbers = generate_fibonacci(limit)
        display_results(fibonacci_numbers, limit)
        choice = safe_input("Generate another sequence? (y/n): ")
        if choice is None or choice.strip().lower() != 'y':
            print("Thank you for using the Fibonacci Number Generator. Goodbye!")
            break