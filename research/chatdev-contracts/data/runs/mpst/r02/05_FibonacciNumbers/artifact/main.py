'''
main.py
Entry point for the Fibonacci Number Generator application.
Orchestrates the interactive loop:
  welcome -> prompt for limit -> generate -> display -> repeat/quit.
Gracefully handles QuitSignal (including EOFError-mapped quits) and
KeyboardInterrupt so the program always shuts down cleanly without
an unhandled traceback, even when stdin is closed or exhausted.
'''
from fibonacci import generate_fibonacci_up_to
from interface import (QuitSignal, ask_to_continue, display_results,
                       print_goodbye, print_welcome, prompt_for_limit)
def main():
    """
    Run the interactive Fibonacci generator loop.
    Catches QuitSignal (raised on quit keywords or when EOFError
    signals a closed/exhausted stdin) and KeyboardInterrupt for
    graceful exit, and ValueError for friendly re-prompting on
    invalid input.
    """
    print_welcome()
    while True:
        try:
            limit = prompt_for_limit()
        except (QuitSignal, KeyboardInterrupt):
            break
        except ValueError as error:
            print(f"Invalid input: {error}")
            continue
        sequence = generate_fibonacci_up_to(limit)
        display_results(sequence, limit)
        try:
            if not ask_to_continue():
                break
        except KeyboardInterrupt:
            break
    print_goodbye()
if __name__ == "__main__":
    main()