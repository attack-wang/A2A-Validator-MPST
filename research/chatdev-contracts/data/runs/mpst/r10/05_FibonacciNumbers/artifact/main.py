'''
Main entry point of the Fibonacci Generator application.
This module orchestrates the application flow:
1. Displays a welcome banner.
2. Repeatedly prompts the user for an upper limit.
3. Validates and parses the input.
4. Generates all Fibonacci numbers up to the limit.
5. Displays the results in a formatted numbered list.
The user can quit at any time by entering 'q', 'quit', or 'exit'.
'''
import sys
from fibonacci import FibonacciGenerator
from input_validator import InputValidator
from display import Display
def run():
    """Run the interactive main loop of the application."""
    Display.show_welcome()
    try:
        while True:
            raw_input = Display.prompt()
            if InputValidator.is_quit_command(raw_input):
                Display.show_goodbye()
                break
            try:
                limit = InputValidator.parse(raw_input)
                InputValidator.validate(limit)
                generator = FibonacciGenerator(limit)
                numbers = generator.generate()
                Display.show_results(numbers, limit)
            except ValueError as error:
                Display.show_error(str(error))
    except (KeyboardInterrupt, EOFError):
        print()
        Display.show_goodbye()
        sys.exit(0)
if __name__ == "__main__":
    run()