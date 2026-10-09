'''
main.py
Entry point of the Fibonacci Number Generator application.
Usage:
    python main.py            -> interactive mode (prompt loop)
    python main.py <limit>    -> one-shot mode (e.g. python main.py 100)
The application asks the user for a non-negative integer limit and prints
every Fibonacci number up to and including that limit.
'''
import sys
from fibonacci import fibonacci_generator, generate_fibonacci_up_to
from utils import format_sequence, parse_non_negative_integer
BANNER = "=" * 52
QUIT_COMMANDS = {"quit", "q", "exit"}
def display_results(limit):
    '''
    Generate and display all Fibonacci numbers up to the given limit.
    Demonstrates both the list-based implementation and the memory-efficient
    generator-based implementation.
    Args:
        limit (int): The inclusive upper bound for the Fibonacci sequence.
    '''
    numbers = generate_fibonacci_up_to(limit)
    print(f"\nFibonacci numbers up to {limit} ({len(numbers)} number(s)):")
    print(format_sequence(numbers))
    print("\nSame sequence produced lazily via the generator:")
    print(format_sequence(fibonacci_generator(limit)))
    print()
def run_interactive():
    '''Run the application in interactive mode with a prompt loop.'''
    print(BANNER)
    print("Welcome to the Fibonacci Number Generator!")
    print(BANNER)
    print("Enter a non-negative integer limit and the program will display")
    print("every Fibonacci number up to that limit.")
    print("Type 'quit', 'q', or 'exit' at any time to leave.\n")
    while True:
        try:
            raw = input("Enter a limit (or 'quit' to exit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if raw.strip().lower() in QUIT_COMMANDS:
            print("Goodbye!")
            break
        try:
            limit = parse_non_negative_integer(raw)
        except ValueError as error:
            print(f"Invalid input: {error}\n")
            continue
        display_results(limit)
def main(argv=None):
    '''
    Application entry point.
    Args:
        argv (list[str] | None): Command-line arguments (defaults to sys.argv[1:]).
    Returns:
        int: Process exit code (0 on success, 1 on invalid usage).
    '''
    args = list(sys.argv[1:] if argv is None else argv)
    if args:
        # One-shot mode: treat the first argument as the limit.
        try:
            limit = parse_non_negative_integer(args[0])
        except ValueError as error:
            print(f"Error: {error}")
            print("Usage: python main.py [limit]")
            return 1
        display_results(limit)
        return 0
    # No arguments supplied: fall back to interactive mode.
    run_interactive()
    return 0
if __name__ == "__main__":
    sys.exit(main())