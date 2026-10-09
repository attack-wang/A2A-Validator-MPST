'''
main.py
Entry point of the Fibonacci Generator application.
This program repeatedly asks the user for a number and generates
all Fibonacci numbers up to (and including) that number, displaying
the results along with a short statistical summary.
This version exits gracefully when the input stream is closed
(e.g., EOF in automated test runs or piped input) instead of
crashing with an unhandled EOFError.
'''
from fibonacci import FibonacciGenerator
from input_handler import get_user_input, ask_yes_no, InputClosedError
from display import display_fibonacci, display_summary
def main():
    '''Run the main application loop.'''
    generator = FibonacciGenerator()
    print("=" * 55)
    print("        Welcome to the Fibonacci Generator!")
    print("=" * 55)
    print("This tool generates all Fibonacci numbers up to a")
    print("given number (inclusive).")
    while True:
        try:
            limit = get_user_input(
                "\nEnter a number to generate Fibonacci numbers up to: "
            )
        except InputClosedError:
            print("\nInput stream closed. Exiting.")
            break
        numbers = generator.generate(limit)
        display_fibonacci(numbers, limit)
        display_summary(numbers)
        try:
            if not ask_yes_no("\nGenerate another sequence? (y/n): "):
                break
        except InputClosedError:
            break
    print("\nGoodbye! Thanks for using the Fibonacci Generator.")
if __name__ == "__main__":
    main()