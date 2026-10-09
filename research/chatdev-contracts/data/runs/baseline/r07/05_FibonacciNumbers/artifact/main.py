'''
main.py
Entry point for the Fibonacci Generator application.
Dispatches between one-shot CLI mode (a limit passed as a command-line
argument) and interactive mode (the limit entered at prompts).
Modes and error handling follow the behavior documented in readme.md.
Fix applied: interactive mode now catches EOFError (closed/exhausted
stdin, e.g. piped input or automated test harnesses) and KeyboardInterrupt
(Ctrl-C), exiting gracefully with status code 0 instead of crashing.
'''
import sys
from fibonacci import validate_limit, generate_fibonacci_up_to
from utils import format_sequence, build_argument_parser
def run_one_shot(raw_limit):
    """
    One-shot mode: validate the raw limit, generate and print the sequence.
    Exits with status code 1 on invalid input, as specified in the README.
    Args:
        raw_limit: The raw limit string taken from the command line.
    """
    try:
        limit = validate_limit(raw_limit)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    print(f"Fibonacci numbers up to {limit}:")
    print(format_sequence(generate_fibonacci_up_to(limit)))
def run_interactive():
    """
    Interactive mode: repeatedly prompt the user for a limit.
    Empty input re-prompts; 'q', 'quit', or 'exit' quits;
    invalid input shows an error and re-prompts.
    EOF on stdin (closed or exhausted, e.g. `python main.py < /dev/null`,
    empty piped input, or automated test harnesses) and Ctrl-C are treated
    as graceful quit conditions so the program exits cleanly with status
    code 0 instead of raising an uncaught EOFError/KeyboardInterrupt.
    """
    print("Fibonacci Generator (interactive mode)")
    print("Enter a non-negative integer limit, or 'q' to quit.")
    while True:
        try:
            raw = input("Enter a limit: ").strip()
        except EOFError:
            # stdin closed or exhausted (piped input / automated test):
            # quit gracefully instead of crashing with a traceback.
            print("\nInput stream closed. Goodbye!")
            break
        except KeyboardInterrupt:
            # User pressed Ctrl-C: quit gracefully.
            print("\nInterrupted. Goodbye!")
            break
        if raw.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        if not raw:
            print("Input cannot be empty. Please try again.")
            continue
        try:
            limit = validate_limit(raw)
        except ValueError as exc:
            print(f"Error: {exc}")
            continue
        print(f"Fibonacci numbers up to {limit}:")
        print(format_sequence(generate_fibonacci_up_to(limit)))
def main():
    """Application entry point: parse arguments and dispatch to the proper mode."""
    args = build_argument_parser().parse_args()
    if args.limit is None:
        run_interactive()
    else:
        run_one_shot(args.limit)
if __name__ == "__main__":
    main()